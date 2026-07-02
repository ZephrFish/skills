# Skills OS Profile Installer

The Skills OS profile installer applies a role/profile loadout for Codex from the declarative manifests in `profiles/`.

## Quick start

From a checkout of this repository:

```bash
uv run scripts/skills-os.py list-profiles
uv run scripts/skills-os.py show research
uv run scripts/skills-os.py install research
```

For a dry run:

```bash
uv run scripts/skills-os.py install research --dry-run
```

For GitHub usage from the v2 branch:

```bash
uv run scripts/skills-os.py install research --source SpecterOps/skills --ref skills-os
```

## What install does

The installer:

1. Parses the selected `profiles/<name>.profile.toml` file.
2. Resolves inherited profiles, including Base.
3. Validates that every required plugin exists in the repo marketplace metadata.
4. Ensures the `specterops-skills` Codex marketplace is configured.
5. Installs each required plugin with `codex plugin add <plugin>@specterops-skills`.
6. Shows an optional checkbox selector for agents.
7. Copies selected agents into `~/.codex/company/agents/`.
8. Backs up and updates `~/.codex/config.toml` with `[agents.<name>]` entries for selected agents.

Agents are never installed by default. The checkbox list marks profile-recommended agents, but leaves all boxes unchecked until the user selects them.

## Useful options

```bash
# No changes, just print planned actions.
uv run scripts/skills-os.py install engineering --dry-run

# Non-interactive install of plugins only.
uv run scripts/skills-os.py install base --yes --no-agents

# Install all agents recommended by the resolved profile chain.
uv run scripts/skills-os.py install research --all-recommended-agents

# Install selected agents without opening the checkbox selector.
uv run scripts/skills-os.py install engineering --agents architect,code-reviewer,qa-tester

# Reinstall plugins that are already installed.
uv run scripts/skills-os.py install adsim --reinstall

# Replace an existing marketplace named specterops-skills if it points elsewhere.
uv run scripts/skills-os.py install research --replace-marketplace
```

## Failure behavior

The installer validates all profile references before changing anything. During install, it stops on the first failed Codex command and prints the exact command that failed so the user can retry or troubleshoot manually.

If a marketplace named `specterops-skills` already exists but points to a different source, the installer prompts before replacing it. Use `--replace-marketplace` or `--yes` for non-interactive replacement.

## Requirements

- `uv`
- Python 3.11+
- Codex CLI on `PATH`
- Network access when using a Git marketplace source

The installer is a PEP 723 `uv` script and declares its own Python dependencies (`questionary` and `rich`).
