---
name: planning-grill
description: Stress-test a plan, design, proposal, roadmap, architecture, workflow, or implementation approach through a one-question-at-a-time interrogation loop. Use when the user asks to be grilled, wants plan/design critique, wants assumptions challenged, wants a stronger plan before implementation, or needs decisions explored one at a time with recommended answers.
---

# Planning Grill

Interrogate a plan until the user and agent have a clearer, safer, more actionable version of it.

Inspired by TimothyVang/Grill-me's one-question-at-a-time plan interview concept. Do not copy external skill text; use this Skills OS workflow and preserve source attribution in plugin documentation when relevant.

## Core behavior

- Ask exactly one question at a time.
- Prefer high-leverage questions over exhaustive checklists.
- For each question, include a concise recommended answer or default position.
- Wait for the user's answer before asking the next question.
- When the answer can be discovered from local repo/context, inspect the relevant files instead of asking.
- Track decisions, assumptions, risks, and follow-up items as the loop progresses.
- Stop when the plan is good enough to move forward, not when every theoretical question is exhausted.

## Question strategy

Prioritize questions that expose:

1. Goal ambiguity.
2. User/audience mismatch.
3. Hidden constraints.
4. Missing acceptance criteria.
5. Sequencing or dependency risk.
6. Reversibility and rollback concerns.
7. Ownership and maintenance gaps.
8. Validation and evidence requirements.
9. Safety, privacy, legal, or operational risk.
10. Overbuilding or premature implementation.

## Workflow

1. Restate the plan in one or two sentences.
2. Identify the current biggest uncertainty.
3. Ask one question and give a recommended answer.
4. Incorporate the user's answer into a running decision/assumption summary.
5. Repeat with the next highest-leverage uncertainty.
6. When the plan is ready, produce:
   - refined plan summary,
   - decisions made,
   - remaining assumptions,
   - risks and mitigations,
   - next implementation step.

## Question format

Use this format by default:

```markdown
Question N: <single focused question>

Recommended answer: <short default recommendation and why>
```

If local inspection is better than asking, say what you will inspect and then inspect it before continuing.

## Stop conditions

Stop grilling and summarize when:

- the user says to stop;
- the next questions are low-value detail;
- the plan has clear goals, scope, sequence, ownership, and validation;
- implementation can begin safely with known assumptions;
- remaining uncertainty belongs to later stakeholder review.

## Output

Keep intermediate turns short. Only produce the full summary at the end or when the user asks for it.
