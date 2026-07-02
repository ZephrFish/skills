# Developer Code Review and QA

## Summary

Developer-focused review guidance and web application QA workflows for Engineering.

This v2 split receives the non-offensive engineering pieces from the former `code-review-and-qa` aggregate plugin. Vulnerability-oriented source review intentionally lives in `vulnerability-focused-code-review`.

## What this contains

### Included skills

- `cpp-core-guidelines` — Apply a condensed ISO C++ Core Guidelines workflow to design, implementation, refactoring, modernization, and review.
- `webapp-qa` — Quick-invoke web application QA workflow for smoke testing, flow checks, and Lighthouse-style validation through the QA agent.

### Planned skill areas

- `developer-code-review` — General engineering review for correctness, maintainability, tests, API design, and merge readiness without centering offensive vulnerability hunting.

## Recommended agents

All agents are optional in profile manifests.

- `code-reviewer`
- `qa-tester`
- `architect`

## Roadmap

### Near-term

- [x] Split developer QA skills out of `code-review-and-qa`.
- [ ] Add a general developer-code-review workflow for Engineering.
- [ ] Document how this differs from vulnerability-focused review.

### Mid-term

- [ ] Add stakeholder-reviewed examples for C++, web QA, and general implementation review.
- [ ] Add validation guidance for local app QA and CI-assisted checks.

### Later

- [ ] Revisit Engineering defaults after broader Engineering adoption feedback.
