# Base

## Summary

Base is the shared Skills OS foundation installed by itself or inherited by every role profile.

Canonical profile manifest: [`profiles/base.profile.toml`](../../profiles/base.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Required profile plugins: `base-orientation`, `base-planning`, `base-research`, `base-documentation`, `base-quality`, `base-handoff`, `base-skill-building`, `codex-agent-observability`.
- Existing skills planned for Base migration: `planning-collab-brainstorm`, `source-research`, `readme-generation`, `git-preflight`, `codex-activity-report`, and `opentelemetry-codex`.
- Required v2 build areas: `base-skill-building`, `planning-grill`, `base-orientation`, and handoff/backlog docs.

### Required plugins

- [`base-orientation`](../../plugins/base-orientation/)
- [`base-planning`](../../plugins/base-planning/)
- [`base-research`](../../plugins/base-research/)
- [`base-documentation`](../../plugins/base-documentation/)
- [`base-quality`](../../plugins/base-quality/)
- [`base-handoff`](../../plugins/base-handoff/)
- [`base-skill-building`](../../plugins/base-skill-building/)
- [`codex-agent-observability`](../../plugins/codex-agent-observability/)

## Recommended agents

All agents are optional in profile manifests.

- [`planner`](../../agents/planner.toml)
- [`researcher`](../../agents/researcher.toml)

## Roadmap

### Near-term

- [ ] Move accepted existing skills into Base plugin homes.
- [ ] Build required Base Skill Building skills.
- [ ] Keep Base broadly useful and avoid specialized role defaults.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after the first v2 migration/build pass.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
