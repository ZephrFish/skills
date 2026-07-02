# Execution quality gates

Use this when running the planning-collab-brainstorm skill against a folder of notes, especially after a prior run missed files or skipped research.

## Required local-file behavior

1. Confirm the approved Markdown root(s). If the user says they are already in the planning docs directory, use the current working directory as the planning root and record that assumption.
2. Run the collector from the skill directory, not from the project directory.
3. If the collector or shell command fails because of sandboxing/tooling, retry through the available approval/escalation path. Do not proceed with generic brainstorming as a substitute for reading files.
4. If local reads are impossible, stop and ask the user to grant access, paste a file tree, or paste the notes.
5. Read full files after inventory. Inventory excerpts are only a triage tool.

## Coverage thresholds

- If there are 40 or fewer Markdown files and the total readable size is reasonable, read every Markdown file in full.
- If there are more than 40 Markdown files, read all files whose titles/headings/tags/paths indicate planning, design, roadmap, architecture, research, decisions, brainstorm, TODO, MVP, milestone, or handoff.
- Follow resolved local Markdown links from selected files when they remain inside approved roots.
- If any inventory warning says scanning stopped at `--max-files`, rerun with a higher value before deciding coverage is complete.

## Research behavior

- If the user asks to expand or improve a plan, treat quick supporting research as part of the workflow unless they say local-only.
- If authorization is unclear, ask: `I found local notes and can add quick web research for current patterns/examples. Should I do that before synthesizing?`
- When research is authorized, use 3-6 focused queries derived from the notes and cite sources.
- When research is not authorized or not possible, write `Research skipped` and explain why.

## Final answer checklist

Include:

- Process report with counts.
- Source map of local files and URLs.
- Ideas and plan grounded in the notes.
- Assumptions and unresolved questions.
- Follow-up questions limited to the highest-impact gaps.
