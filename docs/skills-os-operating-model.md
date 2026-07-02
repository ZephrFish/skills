# Skills OS Operating Model

Skills OS v2 is plugin-first with role/profile overlays.

## Top-level model

```text
plugins/   # plugin-owned skills and resources
profiles/  # declarative loadout manifests
roles/     # human-facing role READMEs
agents/    # top-level optional subagents
docs/      # repo-wide standards and guidance
```

## Profiles and roles

Profiles are machine-readable loadout manifests. Role READMEs are human-facing explanations that link to their matching profile manifest and relevant plugins.

Role profiles inherit Base explicitly and list only role-specific required plugins.

## Plugins and skills

Plugins are the install/setup unit. Skills live inside plugin directories. Existing v1 plugins may be split during v2 implementation when a single current plugin contains multiple v2 capability areas.

## Current implementation posture

This phase is additive and non-destructive because the repo already had uncommitted work. It creates the v2 loadout layer and skeleton plugin destinations without moving existing plugin files yet.
