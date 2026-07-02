# Codex Agent Observability

## Summary

Codex and agentic workflow observability, activity reporting, evidence, and telemetry workflows.

## What this contains

### Included skills

- `codex-activity-report` — Generate a normalized UTC timeline and evidence-based narrative from Codex activity artifacts. Use when Codex needs to turn `.codex` logs, rollout JSONL files, archived session bundles, history files, SQLite logs, or planner state into Markdown reporting under `reports/`, especially for after-action reporting, operator handoff, chronology reconstruction, or evidence-backed engagement summaries.
- `opentelemetry-codex` — Install and configure OpenTelemetry for Codex-oriented workflows, including OTLP exporter setup, collector endpoint wiring, and validation that traces/logs/metrics are emitted and stored under PROJECT_PATH/OpenTelemetry.

### Planned skill areas

- `session-evidence-map`
- `agent-run-debugging`

## Recommended agents

- `telemetry-analyst`

## Roadmap

### Near-term

- [x] ~~Move `codex-activity-report` and `opentelemetry-codex` into this plugin.~~
- [ ] Complete rename/rehome cleanup from `codex-observability`.
- [ ] Add troubleshooting examples for agent sessions.

### Mid-term

- [ ] Update examples after initial internal usage.
- [ ] Add validation guidance for new skills in this plugin.

### Later

- [ ] Revisit plugin scope after v2 adoption feedback.
