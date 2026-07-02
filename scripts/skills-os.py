#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "questionary>=2.0.1",
#   "rich>=13.7.0",
# ]
# ///
"""Skills OS role/profile installer.

Install a role profile's required Codex plugins and optionally register selected
repo agents into the user's Codex config.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import questionary
    from questionary import Choice
except Exception:  # pragma: no cover - direct python fallback
    questionary = None
    Choice = None

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except Exception:  # pragma: no cover - direct python fallback
    Console = None
    Panel = None
    Table = None

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = REPO_ROOT / "profiles"
PLUGINS_DIR = REPO_ROOT / "plugins"
AGENTS_DIR = REPO_ROOT / "agents"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
DEFAULT_AGENT_DEST = DEFAULT_CODEX_HOME / "company" / "agents"
DEFAULT_CODEX_CONFIG = DEFAULT_CODEX_HOME / "config.toml"

console = Console() if Console else None


@dataclass(frozen=True)
class Profile:
    name: str
    display_name: str
    description: str
    status: str
    inherits: tuple[str, ...]
    required_plugins: tuple[str, ...]
    optional_agents: tuple[str, ...]
    path: Path


@dataclass(frozen=True)
class ResolvedProfile:
    profile: Profile
    chain: tuple[Profile, ...]
    plugins: tuple[str, ...]
    agent_recommendations: dict[str, list[str]]


def print_msg(message: str, style: str | None = None) -> None:
    if console:
        console.print(message, style=style)
    else:
        print(message)


def print_panel(message: str, title: str | None = None) -> None:
    if console and Panel:
        console.print(Panel(message, title=title))
    else:
        if title:
            print(f"== {title} ==")
        print(message)


def die(message: str, code: int = 1) -> None:
    print_msg(f"Error: {message}", "bold red")
    raise SystemExit(code)


def run_command(command: list[str], *, dry_run: bool = False, capture: bool = False) -> str:
    printable = " ".join(json.dumps(part) if " " in part else part for part in command)
    if dry_run:
        print_msg(f"DRY-RUN: {printable}", "cyan")
        return ""
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=capture,
        )
    except FileNotFoundError:
        die(f"Command not found: {command[0]}")
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            print(exc.stdout, end="")
        if exc.stderr:
            print(exc.stderr, end="", file=sys.stderr)
        die(
            "Command failed. Re-run with --dry-run to inspect the plan, "
            f"then retry the failed command manually if needed:\n  {printable}",
            exc.returncode,
        )
    return result.stdout if capture else ""


def load_json_command(command: list[str]) -> dict[str, Any]:
    output = run_command(command, capture=True)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        die(f"Expected JSON from {' '.join(command)}, got parse error: {exc}")


def read_profile(name: str) -> Profile:
    path = PROFILES_DIR / f"{name}.profile.toml"
    if not path.exists():
        known = ", ".join(sorted(p.name.removesuffix(".profile.toml") for p in PROFILES_DIR.glob("*.profile.toml")))
        die(f"Unknown profile '{name}'. Available profiles: {known}")
    data = tomllib.loads(path.read_text())
    required_top = ["schema_version", "name", "display_name", "description", "status"]
    for key in required_top:
        if key not in data:
            die(f"{path}: missing required top-level field '{key}'")
    if data["schema_version"] != "0.1":
        die(f"{path}: unsupported schema_version {data['schema_version']!r}; expected '0.1'")
    if data["name"] != name:
        die(f"{path}: profile name {data['name']!r} does not match file name {name!r}")
    profile_section = data.get("profile", {})
    plugins_section = data.get("plugins", {})
    agents_section = data.get("agents", {})
    return Profile(
        name=name,
        display_name=str(data["display_name"]),
        description=str(data["description"]),
        status=str(data["status"]),
        inherits=tuple(profile_section.get("inherits", [])),
        required_plugins=tuple(plugins_section.get("required", [])),
        optional_agents=tuple(agents_section.get("optional", [])),
        path=path,
    )


def list_profiles() -> list[Profile]:
    return [read_profile(p.name.removesuffix(".profile.toml")) for p in sorted(PROFILES_DIR.glob("*.profile.toml"))]


def resolve_profile(name: str) -> ResolvedProfile:
    visiting: set[str] = set()
    visited: set[str] = set()
    chain: list[Profile] = []

    def visit(profile_name: str) -> None:
        if profile_name in visiting:
            die(f"Profile inheritance cycle detected at {profile_name!r}")
        if profile_name in visited:
            return
        visiting.add(profile_name)
        profile = read_profile(profile_name)
        for parent in profile.inherits:
            visit(parent)
        visiting.remove(profile_name)
        visited.add(profile_name)
        chain.append(profile)

    visit(name)
    plugins: list[str] = []
    seen_plugins: set[str] = set()
    agent_recommendations: dict[str, list[str]] = {}
    for profile in chain:
        for plugin in profile.required_plugins:
            if plugin not in seen_plugins:
                plugins.append(plugin)
                seen_plugins.add(plugin)
        for agent in profile.optional_agents:
            agent_recommendations.setdefault(agent, []).append(profile.display_name)
    return ResolvedProfile(read_profile(name), tuple(chain), tuple(plugins), agent_recommendations)


def load_marketplace() -> dict[str, Any]:
    if not MARKETPLACE_PATH.exists():
        die(f"Missing marketplace file: {MARKETPLACE_PATH}")
    return json.loads(MARKETPLACE_PATH.read_text())


def marketplace_name() -> str:
    name = load_marketplace().get("name")
    if not name:
        die(f"{MARKETPLACE_PATH}: missing top-level name")
    return str(name)


def marketplace_plugin_names() -> set[str]:
    data = load_marketplace()
    names = set()
    for entry in data.get("plugins", []):
        name = entry.get("name")
        path = entry.get("source", {}).get("path")
        if name and path and (REPO_ROOT / path).is_dir():
            names.add(str(name))
    return names


def available_agent_names() -> set[str]:
    return {p.name.removesuffix(".toml") for p in AGENTS_DIR.glob("*.toml")}


def validate_resolved_profile(resolved: ResolvedProfile) -> None:
    known_plugins = marketplace_plugin_names()
    for profile in resolved.chain:
        for plugin in profile.required_plugins:
            if plugin not in known_plugins:
                die(f"Profile {profile.name!r} requires plugin {plugin!r}, but it is missing from marketplace metadata or plugin directory")
    agents = available_agent_names()
    for agent in resolved.agent_recommendations:
        if agent not in agents:
            die(f"Profile {resolved.profile.name!r} recommends missing agent {agent!r}")


def all_repo_agents() -> list[tuple[str, Path, str]]:
    agents: list[tuple[str, Path, str]] = []
    for path in sorted(AGENTS_DIR.glob("*.toml")):
        data = tomllib.loads(path.read_text())
        name = str(data.get("name", path.name.removesuffix(".toml")))
        description = str(data.get("description", ""))
        agents.append((name, path, description))
    return agents


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def desired_source_kind(source: str) -> tuple[str, str]:
    maybe_path = Path(source).expanduser()
    if maybe_path.exists():
        return ("local", str(maybe_path.resolve()))
    return ("git", source)


def marketplace_entry(name: str) -> dict[str, Any] | None:
    data = load_json_command(["codex", "plugin", "marketplace", "list", "--json"])
    for entry in data.get("marketplaces", []):
        if entry.get("name") == name:
            return entry
    return None


def marketplace_matches(entry: dict[str, Any], source: str) -> bool:
    kind, value = desired_source_kind(source)
    if kind == "local":
        root = entry.get("root")
        try:
            return bool(root) and Path(root).expanduser().resolve() == Path(value).resolve()
        except OSError:
            return False
    marketplace_source = entry.get("marketplaceSource", {}) or {}
    configured = str(marketplace_source.get("source", ""))

    def normalize_git_source(raw: str) -> str:
        normalized = raw.strip().lower()
        if normalized.startswith("git@github.com:"):
            normalized = "https://github.com/" + normalized.removeprefix("git@github.com:")
        normalized = normalized.removesuffix(".git")
        normalized = normalized.removeprefix("https://github.com/")
        normalized = normalized.removeprefix("http://github.com/")
        return normalized.strip("/")

    return normalize_git_source(configured) == normalize_git_source(value)


def confirm(message: str, *, default: bool = False, yes: bool = False) -> bool:
    if yes:
        return True
    if questionary and sys.stdin.isatty():
        return bool(questionary.confirm(message, default=default).ask())
    if not sys.stdin.isatty():
        return False
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{message} [{suffix}] ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes"}


def ensure_marketplace(source: str, ref: str | None, *, dry_run: bool, yes: bool, replace: bool) -> None:
    name = marketplace_name()
    if not command_exists("codex"):
        die("Codex CLI is not available on PATH")
    entry = None if dry_run else marketplace_entry(name)
    add_cmd = ["codex", "plugin", "marketplace", "add", source]
    if ref:
        add_cmd.extend(["--ref", ref])
    if dry_run:
        print_msg(f"Marketplace: {name}", "bold")
        run_command(add_cmd, dry_run=True)
        return
    if entry is None:
        run_command(add_cmd)
        return
    if marketplace_matches(entry, source) and not ref:
        print_msg(f"Marketplace {name!r} is already configured.", "green")
        return
    print_msg(f"Marketplace {name!r} is already configured with a different source/root.", "yellow")
    print_msg(f"Current: {entry}")
    print_msg(f"Requested source: {source}" + (f" @ {ref}" if ref else ""))
    if not replace and not confirm(f"Replace marketplace {name!r} with the requested source?", default=True, yes=yes):
        die("Marketplace replacement declined. Re-run with --source matching the configured marketplace or --replace-marketplace.")
    run_command(["codex", "plugin", "marketplace", "remove", name])
    run_command(add_cmd)


def installed_plugin_names(marketplace: str) -> set[str]:
    data = load_json_command(["codex", "plugin", "list", "--available", "--json"])
    names: set[str] = set()
    for section in ("installed", "plugins"):
        for record in data.get(section, []) or []:
            if record.get("marketplaceName") == marketplace and record.get("installed"):
                names.add(str(record.get("name")))
    return names


def install_plugins(plugins: Iterable[str], *, dry_run: bool, reinstall: bool) -> None:
    name = marketplace_name()
    installed = set() if dry_run else installed_plugin_names(name)
    for plugin in plugins:
        selector = f"{plugin}@{name}"
        if plugin in installed and not reinstall:
            print_msg(f"Plugin already installed: {selector}", "green")
            continue
        if plugin in installed and reinstall:
            run_command(["codex", "plugin", "remove", selector, "--json"], dry_run=dry_run)
        run_command(["codex", "plugin", "add", selector, "--json"], dry_run=dry_run)


def agent_config_key(agent_name: str) -> str:
    key = re.sub(r"[^A-Za-z0-9]+", "_", agent_name).strip("_").lower()
    if not key:
        die(f"Cannot derive Codex config key for agent name {agent_name!r}")
    return key


def toml_string(value: str) -> str:
    return json.dumps(value)


def upsert_agent_block(config_text: str, *, key: str, description: str, config_file: Path) -> str:
    header = f"[agents.{key}]"
    desc_line = f"description = {toml_string(description)}"
    file_line = f"config_file = {toml_string(str(config_file))}"
    block_re = re.compile(rf"(?ms)^\[agents\.{re.escape(key)}\]\n(?P<body>.*?)(?=^\[|\Z)")
    match = block_re.search(config_text)
    if not match:
        prefix = "" if config_text.endswith("\n") or not config_text else "\n"
        return config_text + prefix + f"\n{header}\n{desc_line}\n{file_line}\n"
    body = match.group("body").strip("\n")
    lines = body.splitlines() if body else []
    found_desc = False
    found_file = False
    new_lines: list[str] = []
    for line in lines:
        if line.strip().startswith("description") and "=" in line:
            new_lines.append(desc_line)
            found_desc = True
        elif line.strip().startswith("config_file") and "=" in line:
            new_lines.append(file_line)
            found_file = True
        else:
            new_lines.append(line)
    if not found_desc:
        new_lines.insert(0, desc_line)
    if not found_file:
        insert_at = 1 if new_lines and new_lines[0] == desc_line else len(new_lines)
        new_lines.insert(insert_at, file_line)
    replacement = header + "\n" + "\n".join(new_lines).rstrip() + "\n"
    return config_text[: match.start()] + replacement + config_text[match.end() :]


def install_agents(agent_names: list[str], *, dry_run: bool, config_path: Path, dest_dir: Path) -> None:
    if not agent_names:
        print_msg("No agents selected.", "yellow")
        return
    source_by_name = {name: (path, description) for name, path, description in all_repo_agents()}
    missing = [name for name in agent_names if name not in source_by_name]
    if missing:
        die(f"Unknown agent(s): {', '.join(missing)}")
    config_text = config_path.read_text() if config_path.exists() else ""
    new_config = config_text
    if dry_run:
        print_msg(f"DRY-RUN: ensure directory {dest_dir}", "cyan")
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
    for name in agent_names:
        source, description = source_by_name[name]
        destination = dest_dir / source.name
        if dry_run:
            print_msg(f"DRY-RUN: copy {source} -> {destination}", "cyan")
        else:
            shutil.copy2(source, destination)
        key = agent_config_key(name)
        new_config = upsert_agent_block(new_config, key=key, description=description, config_file=destination)
    if dry_run:
        print_msg(f"DRY-RUN: update {config_path} with {len(agent_names)} agent registration(s)", "cyan")
        return
    if new_config != config_text:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        if config_path.exists():
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = config_path.with_suffix(config_path.suffix + f".{timestamp}.bak")
            shutil.copy2(config_path, backup)
            print_msg(f"Backed up Codex config to {backup}", "green")
        config_path.write_text(new_config)
        print_msg(f"Updated Codex config: {config_path}", "green")


def select_agents_interactively(resolved: ResolvedProfile) -> list[str]:
    recommendations = resolved.agent_recommendations
    agents = all_repo_agents()
    agents.sort(key=lambda item: (item[0] not in recommendations, item[0]))
    if not agents:
        return []
    if not questionary or Choice is None or not sys.stdin.isatty():
        print_msg("Interactive checkbox prompt unavailable; skipping agents. Use --agents or --all-recommended-agents.", "yellow")
        return []
    choices = []
    for name, _path, description in agents:
        markers = recommendations.get(name, [])
        suffix = f"  recommended for {', '.join(markers)}" if markers else ""
        title = f"{name:<24}{suffix}"
        if description:
            title += f" — {description}"
        choices.append(Choice(title=title, value=name, checked=False))
    selected = questionary.checkbox(
        f"Select optional agents for {resolved.profile.display_name} (Space toggles, Enter confirms)",
        choices=choices,
        validate=lambda answer: True,
    ).ask()
    return list(selected or [])


def render_resolved(resolved: ResolvedProfile) -> None:
    if not console or not Table:
        print(f"{resolved.profile.display_name} ({resolved.profile.name})")
        print(resolved.profile.description)
        print("Profiles:", ", ".join(p.name for p in resolved.chain))
        print("Plugins:", ", ".join(resolved.plugins))
        print("Recommended agents:", ", ".join(resolved.agent_recommendations))
        return
    print_panel(
        f"[bold]{resolved.profile.display_name}[/bold] ({resolved.profile.name})\n"
        f"{resolved.profile.description}\nStatus: {resolved.profile.status}\n"
        f"Profile chain: {' -> '.join(p.name for p in resolved.chain)}",
        title="Skills OS Profile",
    )
    plugin_table = Table(title="Required plugins")
    plugin_table.add_column("Order", justify="right")
    plugin_table.add_column("Plugin")
    for idx, plugin in enumerate(resolved.plugins, start=1):
        plugin_table.add_row(str(idx), plugin)
    console.print(plugin_table)
    agent_table = Table(title="Recommended optional agents")
    agent_table.add_column("Agent")
    agent_table.add_column("Recommended by")
    for agent, profiles in sorted(resolved.agent_recommendations.items()):
        agent_table.add_row(agent, ", ".join(profiles))
    console.print(agent_table)


def command_list_profiles(_args: argparse.Namespace) -> None:
    profiles = list_profiles()
    if console and Table:
        table = Table(title="Skills OS profiles")
        table.add_column("Name")
        table.add_column("Display")
        table.add_column("Status")
        table.add_column("Description")
        for profile in profiles:
            table.add_row(profile.name, profile.display_name, profile.status, profile.description)
        console.print(table)
    else:
        for profile in profiles:
            print(f"{profile.name}\t{profile.display_name}\t{profile.status}\t{profile.description}")


def command_show(args: argparse.Namespace) -> None:
    resolved = resolve_profile(args.profile)
    validate_resolved_profile(resolved)
    render_resolved(resolved)


def parse_agent_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def command_install(args: argparse.Namespace) -> None:
    resolved = resolve_profile(args.profile)
    validate_resolved_profile(resolved)
    source = args.source or str(REPO_ROOT)
    render_resolved(resolved)
    print_panel(
        "This will install required Codex plugins for the resolved profile. "
        "Agents are optional and only selected agents will be copied/registered.",
        title="Install plan",
    )
    if args.dry_run:
        print_msg("Dry-run mode: no marketplace, plugin, agent, or config changes will be made.", "cyan")
    ensure_marketplace(source, args.ref, dry_run=args.dry_run, yes=args.yes, replace=args.replace_marketplace)
    install_plugins(resolved.plugins, dry_run=args.dry_run, reinstall=args.reinstall)
    selected_agents: list[str] = []
    if args.no_agents:
        selected_agents = []
    elif args.all_recommended_agents:
        selected_agents = sorted(resolved.agent_recommendations)
    elif args.agents:
        selected_agents = parse_agent_list(args.agents)
    elif not args.yes:
        selected_agents = select_agents_interactively(resolved)
    if selected_agents:
        print_msg(f"Selected agents: {', '.join(selected_agents)}", "bold")
    install_agents(selected_agents, dry_run=args.dry_run, config_path=args.codex_config, dest_dir=args.agent_dest)
    done_message = (
        "Dry-run complete. No changes were made."
        if args.dry_run
        else "Install complete. Restart Codex or open a new Codex session so newly installed plugins and agents are discovered."
    )
    print_panel(done_message, title="Done")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Skills OS role/profile loadouts for Codex.")
    sub = parser.add_subparsers(dest="command", required=True)
    list_cmd = sub.add_parser("list-profiles", help="List available Skills OS profiles")
    list_cmd.set_defaults(func=command_list_profiles)
    show_cmd = sub.add_parser("show", help="Show resolved plugins and recommended agents for a profile")
    show_cmd.add_argument("profile", help="Profile name, e.g. base, research, adsim")
    show_cmd.set_defaults(func=command_show)
    install = sub.add_parser("install", help="Install a profile's required Codex plugins and selected optional agents")
    install.add_argument("profile", help="Profile name, e.g. base, research, adsim")
    install.add_argument("--source", help="Marketplace source. Defaults to this repo checkout.")
    install.add_argument("--ref", help="Git ref for Git marketplace sources, e.g. skills-os")
    install.add_argument("--dry-run", action="store_true", help="Print actions without changing Codex/plugin/agent config")
    install.add_argument("--yes", action="store_true", help="Do not prompt; accept marketplace replacement and skip interactive agent selection unless agent flags are provided")
    install.add_argument("--replace-marketplace", action="store_true", help="Replace an existing marketplace with the same name when source differs")
    install.add_argument("--reinstall", action="store_true", help="Remove and reinstall plugins that are already installed")
    install.add_argument("--no-agents", action="store_true", help="Skip optional agent selection and registration")
    install.add_argument("--agents", help="Comma-separated agents to install/register without prompting")
    install.add_argument("--all-recommended-agents", action="store_true", help="Install/register all agents recommended by the selected profile chain")
    install.add_argument("--agent-dest", type=Path, default=DEFAULT_AGENT_DEST, help=f"Agent TOML destination directory (default: {DEFAULT_AGENT_DEST})")
    install.add_argument("--codex-config", type=Path, default=DEFAULT_CODEX_CONFIG, help=f"Codex config.toml path (default: {DEFAULT_CODEX_CONFIG})")
    install.set_defaults(func=command_install)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
