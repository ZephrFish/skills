# V2 Implementation Status

Date: 2026-07-01
Branch: `skills-os`

## Phase 1 status

Completed in this additive pass:

- Added top-level `profiles/*.profile.toml` manifests.
- Added `roles/<slug>/README.md` files for all accepted launch roles.
- Added repo-wide `docs/` guidance.
- Added skeleton plugin homes for accepted v2 Base/split/roadmap plugins.

## Safety note

The repo already had significant uncommitted work before this pass. This phase intentionally avoids moving or deleting existing plugin files.

A pre-implementation safety snapshot was written under AgentVault:

```text
~/.vaults/agent-vault/codex/projects/skills-os/implementation-snapshots/
```

## Phase 2 status — Base skill moves

Completed in this pass:

- Moved `skills/planning-collab-brainstorm/` -> `plugins/base-planning/skills/planning-collab-brainstorm/`.
- Moved `plugins/workflows-research/skills/source-research/` -> `plugins/base-research/skills/source-research/`.
- Moved `plugins/workflows-development/skills/readme-generation/` -> `plugins/base-documentation/skills/readme-generation/`.
- Moved `plugins/workflows-development/skills/git-preflight/` -> `plugins/base-quality/skills/git-preflight/`.
- Moved `plugins/codex-observability/skills/codex-activity-report/` -> `plugins/codex-agent-observability/skills/codex-activity-report/`.
- Moved `plugins/codex-observability/skills/opentelemetry-codex/` -> `plugins/codex-agent-observability/skills/opentelemetry-codex/`.
- Updated affected plugin READMEs and skill indexes.
- Updated top-level `skills/README.md` after moving `planning-collab-brainstorm`.
- Added new v2 plugin entries to `.agents/plugins/marketplace.json`.
- Updated stale source plugin manifests for moved/deprecated plugins.

## Phase 3 status — Required Base skill builds

Completed in this pass:

- Added `plugins/base-planning/skills/planning-grill/`.
- Added `plugins/base-skill-building/skills/skill-submission-prep/`.
- Added `plugins/base-skill-building/skills/skill-request-builder/`.
- Added `plugins/base-skill-building/skills/workflow-to-skill/`.
- Updated Base Planning and Base Skill Building plugin READMEs and skills indexes.

## Phase 4 status — Code review split

Completed in this pass:

- Moved `plugins/code-review-and-qa/skills/code-review/` -> `plugins/vulnerability-focused-code-review/skills/code-review/`.
- Moved `plugins/code-review-and-qa/skills/cpp-core-guidelines/` -> `plugins/developer-code-review-and-qa/skills/cpp-core-guidelines/`.
- Moved `plugins/code-review-and-qa/skills/webapp-qa/` -> `plugins/developer-code-review-and-qa/skills/webapp-qa/`.
- Updated destination plugin READMEs, skill indexes, and Codex plugin manifests.
- Marked `code-review-and-qa` as a deprecated transition plugin with moved-skill pointers.
- Updated AdSim, Research, and Engineering role READMEs to reflect that the split is complete.
- Validation passed for moved skills, affected plugins, profile references, marketplace entries, and split path checks.

## Phase 5 status — Pre-existing work accepted into v2 scope

The dirty worktree entries that existed before the v2 implementation pass are now intentionally in scope for `skills-os` rather than treated as unrelated noise.

Accepted into the v2 branch scope:

- BloodHound/OpenHound GitHub updates, including saved-search terminology, OpenHound GitHub sample paths, query snapshot/index updates, and BloodHound plugin metadata/doc updates.
- C2 Mythic updates, including the new `mythic-mcp` skill and MythicMCP references.
- Internal training notes under `plugins/internal-training-course/notes/`.
- Root README and legacy Claude marketplace updates that describe the included BloodHound/OpenHound and MythicMCP changes.
- The previously standalone `planning-collab-brainstorm` work, now moved under `base-planning`.

Validation passed for the included pre-existing plugin/skill changes: affected plugin manifests validated, changed/new skills validated, and changed JSON files parsed.

Follow-up: the root README skill links have been refreshed for moved v2 skills; the broader root plugin/profile catalog still needs a final v2-oriented refresh after the remaining moves settle.

## Phase 6 status — Role/profile installer

Completed in this pass:

- Added `scripts/skills-os.py`, a PEP 723 `uv` script for installing Skills OS profiles.
- Added `list-profiles`, `show`, and `install` commands.
- Implemented profile inheritance resolution, marketplace/plugin validation, Codex plugin installation, dry-run mode, and stop-on-failure command execution.
- Added optional agent selection and registration support:
  - rich checkbox selector via `questionary`;
  - recommended-agent labels from profile manifests;
  - unchecked defaults;
  - selected agents copy to `~/.codex/company/agents/`;
  - selected agents register in `~/.codex/config.toml` with config backup before edits.
- Added `docs/profile-installer.md` and updated README/profile schema docs.

Validation passed for script compilation, profile listing/showing, dry-run installs for all launch profiles, selected-agent dry-run registration, helper behavior, and installer documentation references.

## Next implementation steps

- Refresh the root README plugin/profile catalog so it fully reflects the v2 layout.
- Finish cleanup decisions for deprecated aggregate plugins after marketplace/discovery review.
- Decide whether and when to update marketplace/discovery plumbing after existing uncommitted marketplace changes are reviewed.
- Add committed validation tooling/CI checks for profile manifests and plugin references.
