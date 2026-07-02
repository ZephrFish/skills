# Engineering

## Summary

Engineering starts with developer-focused review/QA and development workflow capabilities.

Canonical profile manifest: [`profiles/engineering.profile.toml`](../../profiles/engineering.profile.toml).

The profile manifest is declarative. It does not install anything by itself; installation requires an explicit Skills OS installer command.

## What this contains

- Required plugins: `developer-code-review-and-qa` and `workflows-development`.
- This profile inherits Base.
- Engineering is a best-effort seed and needs broader Engineering stakeholder input.

### Required plugins

- [`developer-code-review-and-qa`](../../plugins/developer-code-review-and-qa/)
- [`workflows-development`](../../plugins/workflows-development/)

## Recommended agents

All agents are optional in profile manifests.

- [`architect`](../../agents/architect.toml)
- [`code-reviewer`](../../agents/code-reviewer.toml)
- [`qa-tester`](../../agents/qa-tester.toml)
- [`planner`](../../agents/planner.toml)

## Roadmap

### Near-term

- [x] Split developer review/QA from current `code-review-and-qa`.
- [ ] Keep `git-cleanup`, `git-merge`, and scaffolding workflows in Engineering.
- [ ] Solicit Engineering team input for CI, testing, architecture, and release workflows.

### Mid-term

- [ ] Add stakeholder-reviewed examples and acceptance criteria.
- [ ] Update this README after additional role-specific migration/build passes.

### Later

- [ ] Revisit role defaults after internal adoption feedback.
