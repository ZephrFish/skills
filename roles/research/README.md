# Research

## Summary

Research supports security research, BloodHound/OpenGraph, C2, payload experimentation, reverse engineering, vulnerability-oriented code review, and tradecraft analysis.

Canonical profile manifest: [`profiles/research.profile.toml`](../../profiles/research.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Role-specific required plugins are listed in `profiles/research.profile.toml`.
- This profile inherits Base.
- `report-drafting`, `ops-reconnaissance`, and `ops-appsec` are intentionally not Research defaults.

### Required plugins

- [`bloodhound`](../../plugins/bloodhound/)
- [`c2-cobaltstrike`](../../plugins/c2-cobaltstrike/)
- [`c2-extensions`](../../plugins/c2-extensions/)
- [`c2-mythic`](../../plugins/c2-mythic/)
- [`vulnerability-focused-code-review`](../../plugins/vulnerability-focused-code-review/)
- [`ludus`](../../plugins/ludus/)
- [`ops-adcs`](../../plugins/ops-adcs/)
- [`ops-sccm`](../../plugins/ops-sccm/)
- [`payloads`](../../plugins/payloads/)
- [`reverse-engineering`](../../plugins/reverse-engineering/)
- [`tradecraft-linux`](../../plugins/tradecraft-linux/)
- [`tradecraft-mac`](../../plugins/tradecraft-mac/)
- [`tradecraft-windows`](../../plugins/tradecraft-windows/)

## Recommended agents

All agents are optional in profile manifests.

- [`researcher`](../../agents/researcher.toml)
- [`bloodhound-analyst`](../../agents/bloodhound-analyst.toml)
- [`winternals`](../../agents/winternals.toml)
- [`exploit-dev`](../../agents/exploit-dev.toml)
- [`poc-dev`](../../agents/poc-dev.toml)

## Roadmap

### Near-term

- [x] Split vulnerability-focused code review cleanly.
- [ ] Clarify Research use of C2/payload/tradecraft in README safety language.
- [ ] Complete placeholder tradecraft and ADCS plugin content over time.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after additional role-specific migration/build passes.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
