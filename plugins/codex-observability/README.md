# Codex Observability (Deprecated)

## Summary

This v1 plugin has been renamed/re-homed as [`codex-agent-observability`](../codex-agent-observability/) for Skills OS v2.

## What this contains

### Included skills

No skills remain here after the v2 Base move.

Moved to Base during v2 implementation:

- `codex-activity-report` -> `plugins/codex-agent-observability/skills/codex-activity-report/`
- `opentelemetry-codex` -> `plugins/codex-agent-observability/skills/opentelemetry-codex/`

## Recommended agents

Use the destination plugin and role READMEs for current recommendations. The former observability workflow commonly used:

- `telemetry-analyst`

## Roadmap

### Near-term

- [x] Move observability skills to `codex-agent-observability`.
- [ ] Decide whether to remove this compatibility plugin directory after the full v2 reorg is complete.

### Mid-term

- [ ] Update marketplace/discovery plumbing to prefer `codex-agent-observability`.

### Later

- [ ] Remove stale v1 plugin references once migration documentation is complete.
