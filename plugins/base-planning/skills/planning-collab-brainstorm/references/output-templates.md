# Output templates

Use these structures selectively. Do not create every artifact unless it helps the user.

## 00-source-map.md

```markdown
# Source Map

## Process Report
- Local roots scanned:
- Markdown files scanned:
- Files read in full:
- Local links followed:
- External links reviewed:
- Supplemental research performed:
- Skipped items and reasons:

## Local Notes
| Path | Why it mattered | Key takeaways |
|---|---|---|
| `path/to/note.md` | ... | ... |

## External Sources
| URL | Why it mattered | Key takeaways | Date checked |
|---|---|---|---|
| https://example.com | ... | ... | YYYY-MM-DD |

## Italic LLM / User Notes
| Path | Note | How it affected synthesis |
|---|---|---|
| `path/to/note.md` | ... | ... |

## Unread or Skipped Sources
| Source | Reason |
|---|---|
| ... | outside scope / unsafe scheme / duplicate / low relevance |
```

## 01-idea-brief.md

```markdown
# Idea Brief: <Name>

## One-sentence concept
...

## Problem
...

## Audience / users
...

## Value proposition
...

## Goals
- ...

## Non-goals
- ...

## Success metrics
- ...

## Constraints
- ...

## Assumptions to validate
- ...
```

## 02-brainstorm-map.md

```markdown
# Brainstorm Map

## Themes
- ...

## Promising directions
### Direction A
- Description:
- Why it is interesting:
- Risks:
- Best next step:

## Edge ideas
- ...

## Rejected or parked ideas
| Idea | Why parked | Revisit when |
|---|---|---|
| ... | ... | ... |

## Open questions
- ...
```

## 03-design-doc.md

```markdown
# Design Document: <Name>

## Context
...

## Goals and non-goals
...

## Requirements
### Functional
- ...
### Non-functional
- ...

## Proposed design
...

## Alternatives considered
| Option | Pros | Cons | Decision |
|---|---|---|---|
| ... | ... | ... | ... |

## Data model / content model
...

## Interfaces and integrations
...

## Security, privacy, and safety considerations
- ...

## Testing and validation
- ...

## Risks and mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| ... | ... | ... |
```

## 04-roadmap.md

```markdown
# Roadmap

## Phase 0: Discovery
- Outcomes:
- Tasks:
- Exit criteria:

## Phase 1: MVP
- Outcomes:
- Tasks:
- Exit criteria:

## Phase 2: v1
- Outcomes:
- Tasks:
- Exit criteria:

## Later
- ...

## Dependencies
- ...
```

## 05-implementation-plan.md

```markdown
# Implementation Plan

## Work breakdown
1. ...
2. ...

## Milestones
| Milestone | Deliverable | Acceptance criteria |
|---|---|---|
| ... | ... | ... |

## Task backlog
### M1: ...
- [ ] Task — acceptance criteria

## Test strategy
- Unit:
- Integration:
- Manual/UX:
- Security/privacy:

## Definition of done
- ...
```

## 06-agent-handoff.md

```markdown
# Agent Handoff

## Objective
...

## Context to preserve
- ...

## Files and sources read
- `path/to/file.md`
- https://example.com

## Decisions
- ...

## Assumptions
- ...

## Open questions
- ...

## Recommended next actions
1. ...
2. ...

## Guardrails for implementation
- Do not ...
- Confirm before ...
```
