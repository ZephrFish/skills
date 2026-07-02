---
name: skill-submission-prep
description: Prepare an existing skill or draft skill for submission to the Skills OS repository. Use when the user wants to submit, review, package, validate, or ready a skill for approval, including provenance, target plugin/profile fit, quality checks, safety notes, README/index updates, and reviewer handoff. Does not approve or promote the skill.
---

# Skill Submission Prep

Prepare a skill for repository review without approving it.

## Boundary

This skill packages and validates a submission. It does not decide final acceptance, maturity, or promotion.

Use `workflow-to-skill` instead when the user first needs to create a reusable skill from a completed workflow.
Use `skill-request-builder` instead when the user is requesting a missing skill rather than submitting one.

## Inputs

Accept any of:

- path to an existing skill directory;
- path to a draft `SKILL.md`;
- pasted skill content;
- a plugin/role target and rough skill draft;
- a request to prepare the current skill for repo submission.

If the target skill or plugin is ambiguous, ask one concise question. Otherwise proceed with best judgment and record assumptions.

## Review package workflow

1. Inspect the skill directory or draft.
2. Confirm required structure:
   - `SKILL.md` exists;
   - frontmatter has only `name` and `description` unless repo policy says otherwise;
   - folder name matches skill name;
   - optional `agents/openai.yaml` is present or intentionally absent;
   - bundled `scripts/`, `references/`, and `assets/` are actually needed.
3. Validate the trigger description:
   - says what the skill does;
   - says when to use it;
   - includes common user phrasing/triggers;
   - is not too broad for Base or the target role.
4. Review body quality:
   - concise workflow;
   - clear inputs and outputs;
   - progressive disclosure for references;
   - safe handling of external sources, credentials, secrets, and destructive actions;
   - no unnecessary README/changelog clutter inside the skill folder.
5. Check target placement:
   - target plugin;
   - relevant profiles/roles;
   - whether the skill is Base, role-specific, or roadmap/backlog.
6. Capture provenance:
   - original author/source if known;
   - whether original, adapted, inspired, or copied;
   - license or attribution follow-up if external content was used.
7. Run available validation scripts when local execution is safe and requested/appropriate.
8. Prepare the submission summary.

## Output format

Return a concise review packet:

```markdown
# Skill Submission Prep: <skill-name>

## Proposed placement
- Plugin:
- Roles/profiles:
- Maturity suggestion:

## Validation status
- Structure:
- Frontmatter:
- Trigger description:
- Resources:
- Local validation:

## Provenance / attribution
- Source:
- License/attribution notes:
- Follow-up needed:

## Safety / risk notes
- Data/secrets:
- External execution:
- Offensive/security impact:

## Required changes before review
- [ ] ...

## Suggested reviewer notes
...
```

If editing files, update only the skill, owning plugin README/index, and repo catalog/docs needed for submission readiness.
