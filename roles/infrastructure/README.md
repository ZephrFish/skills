# Infrastructure

## Summary

Infrastructure is Base-only for v2 until Infrastructure SMEs define concrete default plugins.

Canonical profile manifest: [`profiles/infrastructure.profile.toml`](../../profiles/infrastructure.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- No role-specific required plugins yet.
- This profile inherits Base.
- `infra-iac` is a roadmap/wanted plugin area, not a default yet.

### Required plugins

- No role-specific required plugins yet. This role currently inherits Base only.

## Recommended agents

All agents are optional in profile manifests.

- [`architect`](../../agents/architect.toml)
- [`planner`](../../agents/planner.toml)

## Roadmap

### Near-term

- [ ] Work with Infrastructure SMEs to define `infra-iac`.
- [ ] List Terraform, Kubernetes, Docker/Compose, Ansible, and cloud config review as wanted areas.
- [ ] Do not include `ops-infrastructure` or `ludus` by default.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after the first v2 migration/build pass.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
