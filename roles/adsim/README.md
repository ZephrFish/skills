# Adversary Simulation

## Summary

Adversary Simulation is the broad operator profile for assessment, C2, BloodHound, reporting, payload, infrastructure-ops, tradecraft, and social-engineering workflows.

Canonical profile manifest: [`profiles/adsim.profile.toml`](../../profiles/adsim.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Role-specific required plugins are listed in `profiles/adsim.profile.toml`.
- This profile inherits Base and adds the accepted broad AdSim plugin set.
- High-risk/internal workflows should be handled by governance and README safety language rather than omitted from the planning baseline.

### Required plugins

- [`bloodhound`](../../plugins/bloodhound/)
- [`c2-cobaltstrike`](../../plugins/c2-cobaltstrike/)
- [`c2-extensions`](../../plugins/c2-extensions/)
- [`c2-mythic`](../../plugins/c2-mythic/)
- [`vulnerability-focused-code-review`](../../plugins/vulnerability-focused-code-review/)
- [`ludus`](../../plugins/ludus/)
- [`ops-adcs`](../../plugins/ops-adcs/)
- [`ops-appsec`](../../plugins/ops-appsec/)
- [`ops-infrastructure`](../../plugins/ops-infrastructure/)
- [`ops-mssql`](../../plugins/ops-mssql/)
- [`ops-reconnaissance`](../../plugins/ops-reconnaissance/)
- [`ops-sccm`](../../plugins/ops-sccm/)
- [`payloads`](../../plugins/payloads/)
- [`report-drafting`](../../plugins/report-drafting/)
- [`report-timeline`](../../plugins/report-timeline/)
- [`reverse-engineering`](../../plugins/reverse-engineering/)
- [`social-engineering`](../../plugins/social-engineering/)
- [`tradecraft-linux`](../../plugins/tradecraft-linux/)
- [`tradecraft-mac`](../../plugins/tradecraft-mac/)
- [`tradecraft-windows`](../../plugins/tradecraft-windows/)

## Recommended agents

All agents are optional in profile manifests.

- [`bloodhound-analyst`](../../agents/bloodhound-analyst.toml)
- [`domain-ops`](../../agents/domain-ops.toml)
- [`internal-network-recon`](../../agents/internal-network-recon.toml)
- [`osint-recon`](../../agents/osint-recon.toml)
- [`sccm-ops`](../../agents/sccm-ops.toml)
- [`security-researcher`](../../agents/security-researcher.toml)
- [`ssh-operator`](../../agents/ssh-operator.toml)
- [`report-writer`](../../agents/report-writer.toml)
- [`winternals`](../../agents/winternals.toml)
- [`exploit-dev`](../../agents/exploit-dev.toml)

## Roadmap

### Near-term

- [ ] Add safety/governance notes for high-risk workflows.
- [ ] Complete empty/backlog plugins such as `ops-adcs`, `ops-mssql`, `tradecraft-linux`, and `tradecraft-mac`.
- [x] Split vulnerability-focused code review cleanly from developer review.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after additional role-specific migration/build passes.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
