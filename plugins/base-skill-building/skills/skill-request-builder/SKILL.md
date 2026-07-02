---
name: skill-request-builder
description: Turn a missing workflow, repeated task, rough idea, role gap, or user pain point into a clear Skills OS skill request. Use when the user wants to request a skill, define a bounty/help-wanted item, capture acceptance criteria for a future skill, or document a gap without building the skill yet.
---

# Skill Request Builder

Convert a skill idea or workflow gap into an actionable request.

## Boundary

This skill creates a request, not the skill itself. Use `workflow-to-skill` when the workflow was just performed and should be converted into an actual `SKILL.md`.

## Inputs

Accept any of:

- rough skill idea;
- repeated workflow description;
- role/profile gap;
- plugin backlog item;
- complaint like “we keep doing X manually.”

Ask at most one clarifying question if the target users or desired outcome are unclear. Otherwise proceed with assumptions and mark them.

## Request-building workflow

1. Identify the recurring workflow or pain point.
2. Identify target users and roles/profiles.
3. Decide likely plugin placement:
   - existing plugin first;
   - new plugin only when no existing plugin fits;
   - roadmap/backlog if stakeholder input is needed.
4. Define expected inputs and outputs.
5. List example user prompts that should trigger the skill.
6. Define acceptance criteria:
   - what the skill must do;
   - what it must not do;
   - validation or evidence expectations;
   - safety/approval boundaries.
7. Identify useful resources:
   - references;
   - scripts;
   - templates/assets;
   - external docs or SME input.
8. Produce a request that can be added to a README roadmap, issue, or contribution queue.

## Output format

```markdown
# Skill Request: <proposed-skill-name>

## Summary
<one-paragraph request>

## Proposed placement
- Plugin:
- Roles/profiles:
- Status: roadmap/backlog/proposed

## Target users
- ...

## Example triggers
- "..."
- "..."

## Inputs
- ...

## Outputs
- ...

## Acceptance criteria
- [ ] ...

## Non-goals / boundaries
- ...

## Useful resources or SME input
- ...

## Open questions
- ...
```

If writing to repo files, add the request to the most relevant plugin or role README roadmap/backlog section and update any repo-level planning/catalog document the user asks to maintain.
