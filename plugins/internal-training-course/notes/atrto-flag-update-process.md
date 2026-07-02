# ATRTO flag update process notes

Purpose: capture the repeatable workflow used to inventory and triage stale instructor flag guidance so this can become a future Codex skill in the `internal-training-course` plugin.

## Source context
- Course repo: `/home/matthew/Courses/new-course/wiki-course-atrto-instructor`
- Flag guidance source: `content/flags/*.md`
- Working Obsidian note: `C:\Users\Matthew\Documents\Obsidian\SpecterOps\Training\AT-RTO Course Updates\Instructor WIki\Current Flags.md`

## Workflow performed
1. Enumerate all Markdown files under `content/flags`, excluding `_index.md`.
2. Parse frontmatter and the first Markdown metadata table for machine, location/objective, hint, flag number/value, and points.
3. Extract a short prose summary from each file by removing frontmatter, Hugo shortcodes, screenshots, metadata tables, and fenced command blocks.
4. Apply keyword-based stale indicators:
   - Cobalt Strike syntax: `beacon>`, `powerpick`, `powershell-import`, `psinject`, `make_token`, `steal_token`, `rportfwd`, `elevate svc-exe`.
   - PowerShell-heavy workflow: `PowerShell`, `Invoke-*`, `Get-Domain*`, `Get-WinEvent`, `PowerView`, `PowerUp`, `KeeThief`, `Inveigh`.
   - Credential dumping / OPSEC review: `Mimikatz`, `sekurlsa`, `logonpasswords`, `LSASS`, `procdump`, DPAPI backup-key workflows, DCSync.
   - GUI/manual workflow: `xfreerdp`, word-boundary `RDP`/`GUI`, Task Manager, Firefox/FoxyProxy, Group Policy Management.
   - External/legacy tooling: Seatbelt, Rubeus, SharpDPAPI, SharpChrome, DNSpy, KeeThief, PowerSploit, Inveigh, Crack.sh, PortBender/WinDivert.
5. Assign initial triage only; do not decide final disposition automatically:
   - `Likely update needed` when Cobalt Strike or PowerShell-heavy indicators are present.
   - `Review tool fit` when the issue is mostly OPSEC/tool currency/GUI validation.
   - `Probably OK / verify lab still matches` when no stale indicator was found.
6. Write a human-editable Obsidian note with an inventory table and per-flag review checklist.

## Slide-assisted drafting addition
- Locate the current participant slide deck before drafting flag rewrites. For ATRTO this was found at `/home/matthew/Courses/new-course/wiki-course-atrto/public/slides/files/Adversary_Tactics_Red_Team_Operations.pdf`; the matching content copy at `/home/matthew/Courses/new-course/wiki-course-atrto/content/slides/files/Adversary_Tactics_Red_Team_Operations.pdf` had the same SHA-256.
- Extract slide text with `pdftotext -layout` and build a page-level tool/tradecraft index.
- Use slide hits to decide whether a tool is currently taught before making it the primary path in a flag rewrite.
- Prefer slide/walkthrough-backed Mythic/Apollo syntax. If a required technique is not found in the slides, mark it as a validation question in the draft rather than inventing unsupported tradecraft.
- Add slide references to each per-flag draft so reviewers can quickly verify the relevant section of the course material.

## Future skill behavior
- Input: course repo path and destination notes path.
- Output: current-flags inventory note, stale-indicator summary, and optional per-flag rewrite task list.
- Keep the automated triage conservative; leave final Good/Needs Update decisions to the instructor.
- Add a second pass that proposes Mythic/Apollo-compatible command replacements only after a flag is marked for update.

## Validation commands
```bash
find content/flags -maxdepth 1 -type f -name "*.md" | sort
python3 scripts_or_skill/inventory_flags.py --repo . --out "<Current Flags.md>"
```

## 2026-06-16 — Concise flag walkthrough pass

When drafting flag guidance, use a minimal instructor-verification format:

- Replace long explanation, troubleshooting, and command-option sections with direct walkthrough steps.
- Each step should be one short sentence followed by only the necessary command block.
- Avoid multiple paths unless the instructor explicitly wants an alternate; if multiple paths exist, choose the most reliable/current Mythic path.
- Prefer Mythic/Apollo-native commands and course-taught tools over legacy Cobalt Strike or PowerShell phrasing.
- Keep troubleshooting, validation caveats, and alternate tools outside the draft body unless specifically requested.

Applied this format to `Achilles Privesc.md` and `Flag 01` through `Flag 45` in the Obsidian `Flags/` draft directory.

## 2026-06-17 — Required agent/context line

Add a required host/context line at the top of each flag draft body:

```md
**Required agent/context:** Apollo agent on `<HOST>` with `<needed user/token/rights>`.
```

This line should answer, before any commands, where the student/instructor needs an agent and what identity or network reachability is required. Keep the rest of the draft concise: one short step sentence followed by the necessary command block.

## 2026-06-17 — Enumeration in flag drafts

Flag drafts should include enumeration when the learner is expected to discover the path, but enumeration should be clearly separated from the action that obtains the flag.

Recommended concise structure:

```md
**Required agent/context:** Apollo agent on `<HOST>` with `<needed rights>`.

Enumerate `<relationship/objective>` with the current course tool.

```text
<current Mythic/Apollo command>
```

Less-OPSEC PowerShell enumeration performs the same lookup.

```powershell
<PowerView/PowerShell equivalent>
```

Use the discovered/known value to obtain the flag.

```text
<minimal command sequence to get the flag>
```
```

If the current course enumeration tool is brittle in a specific execution context, keep it as the enumeration step but do not make it the only way to complete the flag; the execution path should use the known validated lab relationship.
