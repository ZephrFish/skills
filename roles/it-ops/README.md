# IT & Operations

## Summary

IT & Operations is Base-only for v2 because current planning does not have enough company-specific IT/Ops workflow context.

Canonical profile manifest: [`profiles/it-ops.profile.toml`](../../profiles/it-ops.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- No role-specific required plugins yet.
- This profile inherits Base.
- Future content should be driven by IT/Ops stakeholder input.

### Required plugins

- No role-specific required plugins yet. This role currently inherits Base only.

## Recommended agents

All agents are optional in profile manifests.

- [`planner`](../../agents/planner.toml)

## Roadmap

### Near-term

- [ ] Collect recurring support and troubleshooting workflows.
- [ ] Define runbook, internal docs, setup, automation, and incident/postmortem skill candidates.
- [ ] Keep `ops-infrastructure` out of this profile by default.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after the first v2 migration/build pass.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
