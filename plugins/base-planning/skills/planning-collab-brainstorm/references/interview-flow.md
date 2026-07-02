# Interview flow

Use this interview loop to turn rough notes into an implementable concept without overwhelming the user.

## Opening questions

Ask up to five questions, choosing the most relevant:

1. What outcome should exist when this idea is "done"?
2. Who is the primary user or audience?
3. What problem, pain, or opportunity motivated the notes?
4. What constraints are fixed: budget, timeline, platform, language, team, privacy, security, integrations?
5. What does success look like in measurable terms?
6. What should be explicitly out of scope?
7. Are there examples, competitors, prior art, or inspirations to compare against?
8. What risks or failure modes are already worrying you?
9. What is the smallest useful first version?
10. What decisions have already been made and should not be reopened?

## Answer modes

Offer both:

- "Reply here with answers."
- "Add/update Markdown notes in the folder, then tell me to re-scan."
- "Leave notes for the LLM as standalone italic paragraphs, or inline as `*LLM: ...*`, `_AI: ..._`, `*Codex: ...*`, or `_Assistant: ..._`."

When the user chooses file-based answers:

1. Suggest a simple note name such as `_brainstorm-answers.md` or `questions.md`.
2. Ask the user to keep answers in Markdown bullets, with optional italic LLM notes for priorities, uncertainty, or private brainstorming cues.
3. Re-run `scripts/collect_markdown_context.py` after they finish.
4. Read changed/new relevant files in full.

## Follow-up strategy

After initial synthesis, ask at most three follow-up questions. Prioritize questions that unblock:

- Scope boundaries.
- Core architecture or workflow.
- Data ownership, privacy, or safety.
- First milestone definition.
- Validation/testing strategy.
- Dependency or integration choices.

If the user does not answer, proceed with an assumption log:

```markdown
## Assumptions to Validate
- A1: ...
- A2: ...
```

## Brainstorming modes

### Exploratory mode

Use when the idea is vague.

- Generate divergent options first.
- Cluster related ideas.
- Name promising directions.
- Identify "wild cards" that are unusual but potentially valuable.
- End with recommended next questions, not a premature build plan.

### Product/project mode

Use when the idea has a user-facing outcome.

- Define user segments and jobs-to-be-done.
- Draft user journeys.
- Identify must-have, should-have, could-have, and non-goal items.
- Propose MVP, v1, and later roadmap.

### Technical design mode

Use when implementation is likely.

- Define constraints and interfaces.
- Sketch architecture alternatives.
- Compare tradeoffs.
- Call out security, privacy, reliability, and observability risks.
- Produce acceptance criteria and test strategy.

### Research synthesis mode

Use when notes contain many links or claims.

- Extract claims from notes.
- Verify high-impact claims with sources.
- Mark unsupported claims as hypotheses.
- Summarize contradictions and confidence.

## Question style

- Ask concrete questions that are easy to answer.
- Avoid long questionnaires unless the user requests depth.
- Prefer "choose one of these options or add another" when decision fatigue is likely.
- Preserve creative ambiguity early; force precision only when planning implementation.
- Reflect back what changed after each answer so the user can correct course.
