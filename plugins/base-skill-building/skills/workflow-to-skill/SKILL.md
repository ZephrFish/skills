---
name: workflow-to-skill
description: Convert a completed conversation, Codex session, operator walkthrough, implementation attempt, or reusable workflow into a concrete Skills OS skill. Use when the user just completed a repeatable task and wants Codex to inspect what was asked, what was done, the result, problems and fixes, and then create/place a generalized skill in the relevant plugin while updating plugin README/docs and repo skill indexes. Does not create submission/review packages.
---

# Workflow To Skill

Turn a successful, repeatable workflow into a repository skill.

## Boundary

Create the skill and place it in the repo. Do not produce a submission/review package by default; `skill-submission-prep` owns that.

This skill is usually invoked when the user believes the workflow is strong enough to capture. Do not over-interview by default.

## Inputs

Accept any of:

- current conversation context;
- Codex session artifacts or rollout logs;
- paths to notes, diffs, scripts, terminal logs, or output files;
- a verbal summary of a workflow that just worked;
- a target plugin or installed/relevant plugin hint.

If the target plugin is ambiguous, ask one concise placement question. Otherwise choose the most relevant existing plugin and record the assumption.

## Artifact review

When session artifacts are available, inspect enough to identify:

- original user request;
- starting context and constraints;
- steps performed;
- tools/scripts/files used;
- end result;
- errors or blockers;
- how blockers were solved;
- what should be generalized;
- what should be removed as session-specific detail.

Do not preserve secrets, customer-specific data, credentials, private endpoints, or one-off paths unless they are converted into placeholders.

## Skill creation workflow

1. Identify the reusable workflow.
2. Propose or infer a short lowercase hyphenated skill name.
3. Pick the target plugin:
   - prefer an installed/relevant existing plugin;
   - use a Base plugin only for broadly useful workflows;
   - recommend a new plugin only for rare structural gaps.
4. Create `plugins/<plugin>/skills/<skill-name>/SKILL.md`.
5. Add `agents/openai.yaml` when possible using concise UI metadata.
6. Add `scripts/`, `references/`, or `assets/` only when they are genuinely needed and derivable from the workflow.
7. Write a concise `SKILL.md` that includes:
   - clear trigger description in frontmatter;
   - input contract;
   - workflow steps;
   - validation/evidence expectations;
   - safety or approval gates;
   - output format.
8. Update the owning plugin README and `skills/README.md`.
9. Update repo-level skill/catalog docs if they exist and are in scope.
10. Run available validation.

## Generalization rules

- Replace project-specific values with placeholders.
- Convert one-off commands into parameterized patterns.
- Preserve proven ordering when ordering mattered.
- Keep hard-won failure fixes as guardrails.
- Remove chatty session narrative.
- Avoid adding unrelated best practices that were not part of the working pattern.

## Default output

Report:

```markdown
Created skill: <skill-name>
Plugin: <plugin>
Files changed:
- ...
Validation:
- ...
Assumptions:
- ...
Next optional step:
- Run skill-submission-prep if this should be submitted for formal review.
```
