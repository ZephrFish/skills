#!/usr/bin/env python3
"""Collect a bounded brainstorming inventory from Markdown/Obsidian notes.

The script reads local Markdown files only. It never fetches external URLs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse


DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".cache",
}

MARKDOWN_LINK_RE = re.compile(r"(!)?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BARE_URL_RE = re.compile(r"https?://[^\s<>)\"']+")
WIKILINK_RE = re.compile(r"(!)?\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
TAG_RE = re.compile(r"(?<![\w/])#([A-Za-z0-9][A-Za-z0-9_/-]*)")


@dataclass
class LinkInfo:
    raw: str
    kind: str
    target: str
    label: str | None = None
    resolved_path: str | None = None
    status: str = "unresolved"


@dataclass
class FileInfo:
    path: str
    title: str
    bytes_read: int
    truncated: bool
    headings: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    frontmatter: dict[str, str] = field(default_factory=dict)
    local_links: list[LinkInfo] = field(default_factory=list)
    wikilinks: list[LinkInfo] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    llm_notes: list[str] = field(default_factory=list)
    excerpt: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect titles, headings, tags, excerpts, and links from Markdown notes."
    )
    parser.add_argument("roots", nargs="+", help="Markdown file(s) or folder root(s) to scan")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--max-files", type=int, default=200)
    parser.add_argument("--max-bytes-per-file", type=int, default=60_000)
    parser.add_argument("--snippet-chars", type=int, default=1_200)
    parser.add_argument("--include-hidden", action="store_true")
    parser.add_argument("--follow-symlinks", action="store_true")
    parser.add_argument(
        "--ignore-dir",
        action="append",
        default=[],
        help="Directory name to ignore; can be supplied multiple times",
    )
    return parser.parse_args()


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts if part not in {".", ".."})


def is_markdown(path: Path) -> bool:
    return path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkdn"}


def safe_relative(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_roots(raw_roots: list[str]) -> tuple[list[Path], list[str]]:
    roots: list[Path] = []
    warnings: list[str] = []
    for raw in raw_roots:
        path = Path(raw).expanduser()
        if not path.exists():
            warnings.append(f"Missing root: {raw}")
            continue
        roots.append(path.resolve())
    return roots, warnings


def iter_markdown_files(
    roots: list[Path],
    *,
    max_files: int,
    include_hidden: bool,
    follow_symlinks: bool,
    ignore_dirs: set[str],
) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    warnings: list[str] = []

    for root in roots:
        if root.is_file():
            if is_markdown(root):
                files.append(root)
            else:
                warnings.append(f"Skipped non-Markdown file: {root}")
            continue

        for current, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
            current_path = Path(current)

            kept_dirs = []
            for dirname in dirnames:
                child = current_path / dirname
                if dirname in ignore_dirs:
                    continue
                if not include_hidden and dirname.startswith("."):
                    continue
                if child.is_symlink() and not follow_symlinks:
                    warnings.append(f"Skipped symlinked directory: {child}")
                    continue
                kept_dirs.append(dirname)
            dirnames[:] = kept_dirs

            for filename in filenames:
                path = current_path / filename
                if not is_markdown(path):
                    continue
                if not include_hidden and is_hidden(path.relative_to(root)):
                    continue
                if path.is_symlink() and not follow_symlinks:
                    warnings.append(f"Skipped symlinked file: {path}")
                    continue
                files.append(path.resolve())
                if len(files) >= max_files:
                    warnings.append(f"Stopped after --max-files={max_files}")
                    return sorted(dict.fromkeys(files)), warnings

    return sorted(dict.fromkeys(files)), warnings


def read_bounded(path: Path, max_bytes: int) -> tuple[str, int, bool, str | None]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return "", 0, False, f"Could not read {path}: {exc}"

    truncated = len(data) > max_bytes
    chunk = data[:max_bytes]
    try:
        text = chunk.decode("utf-8")
    except UnicodeDecodeError:
        text = chunk.decode("utf-8", errors="replace")
    return text, min(len(data), max_bytes), truncated, None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    rest = text[end + 4 :].lstrip("\n")
    values: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line) and current_key:
            values[current_key] = (values[current_key] + ", " + line.strip()[2:]).strip(", ")
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            current_key = key.strip()
            values[current_key] = value.strip().strip("'\"")
    return values, rest


def normalize_title(path: Path, frontmatter: dict[str, str], text: str) -> str:
    for key in ("title", "name"):
        if frontmatter.get(key):
            return frontmatter[key]
    match = HEADING_RE.search(text)
    if match:
        return match.group(2).strip()
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def extract_excerpt(text: str, snippet_chars: int) -> str:
    lines = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        if stripped.startswith(("---", "%%")):
            continue
        lines.append(stripped)
        if sum(len(item) + 1 for item in lines) >= snippet_chars:
            break
    excerpt = " ".join(lines)
    return excerpt[:snippet_chars].strip()


def strip_markdown_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


ITALIC_SPAN_RE = re.compile(r"(?<![*_])([*_])([^*_\n]{2,700})\1(?![*_])")
LLM_NOTE_PREFIX_RE = re.compile(
    r"^(?:(?:llm|ai|codex|assistant)(?:\s+(?:note|context|question|todo|hint))?|note\s+(?:for|to)\s+(?:the\s+)?(?:llm|ai|codex|assistant))\s*[:\-]\s*",
    re.IGNORECASE,
)


def extract_italic_llm_notes(text: str, max_notes: int = 50) -> list[str]:
    """Extract user-authored italic notes for the LLM from Markdown text.

    Standalone italic paragraphs are treated as notes. Inline italic spans are
    treated as notes only when prefixed with LLM:/AI:/Codex:/Assistant: to
    avoid treating ordinary emphasis as instructions. Code spans/blocks should
    already be stripped by the caller.
    """
    notes: list[str] = []
    seen: set[str] = set()

    def add(note: str) -> None:
        clean = re.sub(r"\s+", " ", note).strip()
        if not clean or clean in seen:
            return
        seen.add(clean)
        notes.append(clean)

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if len(line) < 4:
            continue
        # Standalone italic paragraph: *note* or _note_, but not bold.
        if (
            line[0] in "*_"
            and line[-1] == line[0]
            and not line.startswith(line[0] * 2)
            and not line.endswith(line[0] * 2)
        ):
            add(line[1:-1])
            if len(notes) >= max_notes:
                return notes
            continue

        for match in ITALIC_SPAN_RE.finditer(line):
            content = match.group(2).strip()
            if LLM_NOTE_PREFIX_RE.match(content):
                add(content)
                if len(notes) >= max_notes:
                    return notes

    return notes


def split_target_fragment(target: str) -> tuple[str, str | None]:
    if "#" not in target:
        return target, None
    left, right = target.split("#", 1)
    return left, right or None


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https"}


def is_skipped_scheme(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme) and parsed.scheme not in {"http", "https"}


def build_stem_index(files: Iterable[Path], roots: list[Path]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        index[path.stem.lower()].append(path)
        for root in roots:
            try:
                rel = path.relative_to(root).with_suffix("").as_posix().lower()
                index[rel].append(path)
            except ValueError:
                continue
    return index


def within_roots(path: Path, roots: list[Path]) -> bool:
    try:
        real = path.resolve()
    except OSError:
        return False
    for root in roots:
        try:
            real.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def resolve_markdown_link(raw_target: str, source: Path, roots: list[Path]) -> tuple[str | None, str]:
    target, _fragment = split_target_fragment(unquote(raw_target))
    if not target or is_external(target) or is_skipped_scheme(target):
        return None, "skipped"
    candidate = (source.parent / target).resolve()
    candidates = [candidate]
    if candidate.suffix == "":
        candidates.append(candidate.with_suffix(".md"))
        candidates.append(candidate.with_suffix(".markdown"))
    for item in candidates:
        if item.exists() and item.is_file() and within_roots(item, roots):
            return item.as_posix(), "resolved"
    return None, "unresolved"


def resolve_wikilink(raw_target: str, stem_index: dict[str, list[Path]]) -> tuple[str | None, str]:
    target = raw_target.split("|", 1)[0]
    target = target.split("#", 1)[0]
    target = unquote(target).strip()
    if not target:
        return None, "unresolved"
    key = target.removesuffix(".md").removesuffix(".markdown").lower()
    matches = stem_index.get(key) or stem_index.get(Path(key).stem.lower())
    if not matches:
        return None, "unresolved"
    unique = sorted(dict.fromkeys(matches))
    if len(unique) > 1:
        return unique[0].as_posix(), "ambiguous"
    return unique[0].as_posix(), "resolved"


def analyze_file(
    path: Path,
    roots: list[Path],
    stem_index: dict[str, list[Path]],
    args: argparse.Namespace,
) -> tuple[FileInfo | None, str | None]:
    text, bytes_read, truncated, warning = read_bounded(path, args.max_bytes_per_file)
    if warning:
        return None, warning

    frontmatter, body = parse_frontmatter(text)
    body_for_links = strip_markdown_code(body)
    headings = [match.group(2).strip() for match in HEADING_RE.finditer(body)][:20]
    tags = sorted(set(TAG_RE.findall(body_for_links)))
    if "tags" in frontmatter:
        tags.extend(
            [item.strip(" []'\"") for item in re.split(r"[, ]+", frontmatter["tags"]) if item.strip(" []'\"")]
        )
        tags = sorted(set(filter(None, tags)))

    external_links = set(BARE_URL_RE.findall(body_for_links))
    llm_notes = extract_italic_llm_notes(body_for_links)
    local_links: list[LinkInfo] = []
    wikilinks: list[LinkInfo] = []

    for match in MARKDOWN_LINK_RE.finditer(body_for_links):
        is_image, label, target = match.groups()
        clean_target = target.strip()
        if is_external(clean_target):
            external_links.add(clean_target)
            continue
        if is_skipped_scheme(clean_target):
            local_links.append(
                LinkInfo(
                    raw=match.group(0),
                    kind="image" if is_image else "skipped-scheme",
                    target=clean_target,
                    label=label,
                    status="skipped",
                )
            )
            continue
        resolved, status = resolve_markdown_link(clean_target, path, roots)
        local_links.append(
            LinkInfo(
                raw=match.group(0),
                kind="image" if is_image else "markdown",
                target=clean_target,
                label=label or None,
                resolved_path=resolved,
                status=status,
            )
        )

    for match in WIKILINK_RE.finditer(body_for_links):
        is_embed, target = match.groups()
        resolved, status = resolve_wikilink(target, stem_index)
        wikilinks.append(
            LinkInfo(
                raw=match.group(0),
                kind="embed" if is_embed else "wikilink",
                target=target,
                resolved_path=resolved,
                status=status,
            )
        )

    base = roots[0] if roots else Path.cwd()
    info = FileInfo(
        path=safe_relative(path, base),
        title=normalize_title(path, frontmatter, body),
        bytes_read=bytes_read,
        truncated=truncated,
        headings=headings,
        tags=tags[:30],
        frontmatter={
            k: v
            for k, v in frontmatter.items()
            if k in {"title", "name", "status", "created", "updated", "tags", "type"}
        },
        local_links=local_links,
        wikilinks=wikilinks,
        external_links=sorted(external_links),
        llm_notes=llm_notes,
        excerpt=extract_excerpt(body, args.snippet_chars),
    )
    return info, None


def to_plain_dict(info: FileInfo) -> dict:
    return asdict(info)


def render_markdown(payload: dict) -> str:
    lines: list[str] = []
    lines.append("# Markdown Brainstorm Inventory")
    lines.append("")
    lines.append(f"- Generated: {payload['generated_at']}")
    lines.append(f"- Files scanned: {payload['summary']['files_scanned']}")
    lines.append(f"- External links: {payload['summary']['external_links']}")
    lines.append(f"- Italic LLM notes: {payload['summary']['llm_notes']}")
    lines.append(f"- Local links: {payload['summary']['local_links']}")
    lines.append(f"- Wikilinks: {payload['summary']['wikilinks']}")
    lines.append(f"- Unresolved local links: {payload['summary']['unresolved_links']}")
    if payload["warnings"]:
        lines.append("")
        lines.append("## Warnings")
        for warning in payload["warnings"]:
            lines.append(f"- {warning}")

    top_tags = payload["summary"].get("top_tags", [])
    if top_tags:
        lines.append("")
        lines.append("## Top tags")
        for tag, count in top_tags:
            lines.append(f"- `#{tag}` ({count})")

    lines.append("")
    lines.append("## Files")
    for item in payload["files"]:
        lines.append("")
        lines.append(f"### `{item['path']}`")
        lines.append(f"- Title: {item['title']}")
        lines.append(f"- Bytes read: {item['bytes_read']}{' (truncated)' if item['truncated'] else ''}")
        if item["tags"]:
            lines.append("- Tags: " + ", ".join(f"`#{tag}`" for tag in item["tags"]))
        if item["headings"]:
            lines.append("- Headings:")
            for heading in item["headings"][:12]:
                lines.append(f"  - {heading}")
        resolved_locals = [link for link in item["local_links"] if link["status"] == "resolved"]
        unresolved_locals = [link for link in item["local_links"] if link["status"] != "resolved"]
        resolved_wikis = [link for link in item["wikilinks"] if link["status"] == "resolved"]
        unresolved_wikis = [link for link in item["wikilinks"] if link["status"] != "resolved"]
        if item.get("llm_notes"):
            lines.append("- Italic LLM/user notes:")
            for note in item["llm_notes"][:12]:
                lines.append(f"  - {note}")
        if resolved_locals or resolved_wikis:
            lines.append("- Resolved local links:")
            for link in (resolved_locals + resolved_wikis)[:12]:
                lines.append(f"  - {link['target']} -> `{link['resolved_path']}`")
        if unresolved_locals or unresolved_wikis:
            lines.append("- Unresolved/ambiguous local links:")
            for link in (unresolved_locals + unresolved_wikis)[:12]:
                lines.append(f"  - {link['target']} ({link['status']})")
        if item["external_links"]:
            lines.append("- External links:")
            for url in item["external_links"][:12]:
                lines.append(f"  - {url}")
        if item["excerpt"]:
            lines.append("- Excerpt:")
            lines.append("")
            lines.append("  > " + item["excerpt"].replace("\n", "\n  > "))

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    roots, warnings = resolve_roots(args.roots)
    if not roots:
        print("No valid roots supplied.", file=sys.stderr)
        for warning in warnings:
            print(warning, file=sys.stderr)
        return 2

    files, walk_warnings = iter_markdown_files(
        roots,
        max_files=args.max_files,
        include_hidden=args.include_hidden,
        follow_symlinks=args.follow_symlinks,
        ignore_dirs=DEFAULT_IGNORE_DIRS | set(args.ignore_dir),
    )
    warnings.extend(walk_warnings)
    stem_index = build_stem_index(files, roots)

    analyzed: list[FileInfo] = []
    for path in files:
        info, warning = analyze_file(path, roots, stem_index, args)
        if warning:
            warnings.append(warning)
        if info:
            analyzed.append(info)

    tag_counter = Counter(tag for info in analyzed for tag in info.tags)
    unresolved = 0
    local_count = 0
    wiki_count = 0
    external_count = 0
    llm_note_count = 0
    for info in analyzed:
        local_count += len(info.local_links)
        wiki_count += len(info.wikilinks)
        external_count += len(info.external_links)
        llm_note_count += len(info.llm_notes)
        unresolved += sum(1 for link in info.local_links + info.wikilinks if link.status != "resolved")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": [root.as_posix() for root in roots],
        "summary": {
            "files_scanned": len(analyzed),
            "external_links": external_count,
            "llm_notes": llm_note_count,
            "local_links": local_count,
            "wikilinks": wiki_count,
            "unresolved_links": unresolved,
            "top_tags": tag_counter.most_common(20),
        },
        "warnings": warnings,
        "files": [to_plain_dict(info) for info in analyzed],
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
