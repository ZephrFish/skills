# Training

## Summary

Training supports internal course wiki scaffolding, content migration, and QA workflows.

Canonical profile manifest: [`profiles/training.profile.toml`](../../profiles/training.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Required plugin: `internal-training-course`.
- This profile inherits Base.
- Broader course-authoring and lab-guide work stays in roadmap/backlog until Training stakeholders define it.

### Required plugins

- [`internal-training-course`](../../plugins/internal-training-course/)

## Recommended agents

All agents are optional in profile manifests.

- [`planner`](../../agents/planner.toml)
- [`researcher`](../../agents/researcher.toml)

## Roadmap

### Near-term

- [ ] Add course-authoring support.
- [ ] Add training-content review and instructor-material workflows.
- [ ] Add lab-guide support and training QA beyond wiki migration.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after the first v2 migration/build pass.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
