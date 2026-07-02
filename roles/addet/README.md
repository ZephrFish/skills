# Adversary Detection

## Summary

Adversary Detection starts with BloodHound for defensive graph analysis and detection-support workflows.

Canonical profile manifest: [`profiles/addet.profile.toml`](../../profiles/addet.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Required plugin: `bloodhound`.
- This profile inherits Base.
- Detection-specific skills remain roadmap/backlog pending manager/SME input.

### Required plugins

- [`bloodhound`](../../plugins/bloodhound/)

## Recommended agents

All agents are optional in profile manifests.

- [`bloodhound-analyst`](../../agents/bloodhound-analyst.toml)
- [`researcher`](../../agents/researcher.toml)

## Roadmap

### Near-term

- [ ] Work with Adversary Detection SMEs to define detection hypothesis, telemetry mapping, SIEM/Sigma/YARA, validation, and reporting workflows.
- [ ] Keep BloodHound framed defensively in this role README.
- [ ] Avoid over-specifying detection engineering without stakeholder input.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after the first v2 migration/build pass.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
