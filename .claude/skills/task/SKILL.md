---
name: task
description: Quick-capture standalone tasks from a free-text brain dump into the tasks/ bucket — parse each ask (action, requestor, due date, related project/goal), append to wiki/tasks/open.md, surface to home.md, and log it. Use for ad-hoc asks ("coffee chat with Jane next week", "send Bob the deck by Friday") that don't belong to a meeting/goal/project. Global — works from any CWD.
argument-hint: "[brain dump]"
---

# Capture tasks

Fast capture of one or more standalone tasks from a brain dump. Keep it quick — parse, confirm,
write. This is the lightweight counterpart to `ingest` (no `sources/` summary page).

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes:

**Resolve the vault root first.** Run this in a **Bash tool call** (not via `!`-inline execution — the
static permission check rejects shell expansions, so the inline form fails with "Contains expansion"):

```sh
d="${CLAUDE_SKILL_DIR:-$(pwd)}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi
```

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All paths below (`wiki/`, `home.md`, `log.md`) are relative to this resolved root.**

## Steps

1. **Take the brain dump** from `$ARGUMENTS` (free text). It may contain **multiple** tasks — split
   them. If no argument is given, ask the user what to capture.
2. **Parse each task** into the `wiki/tasks/open.md` line format:
   `- [ ] <task> — requestor: [[people/firstname-lastname]] — due: YYYY-MM-DD — re: [[projects/...]] — src: [[...]]`
   - **task** — the action, phrased imperatively.
   - **requestor** — who asked, if anyone. Wikilink the `people/` page even if it doesn't exist yet
     (a dangling link is a valid future node — same convention as the rest of the vault).
   - **due** — convert any relative date ("next week", "Friday") to an absolute `YYYY-MM-DD` using the
     session date. Omit if none.
   - **re** — link a related `projects/` or `goals/` page if the task clearly serves one. Omit if not.
   - Drop `src:` here (that field is for `ingest`/`meeting-recap` fan-out).
3. **Show the parsed task list and confirm** with the user. Keep it quick — a one-shot confirmation,
   not a full interview. Adjust if they correct anything.
4. **Append** the lines to the `## Tasks` section of `wiki/tasks/open.md` (newest at the top; replace
   the `_None yet._` placeholder if present).
5. **Surface to `home.md`** — ensure the "Open threads" section points at `[[tasks/open]]` as the
   canonical list; optionally name the soonest-due task(s) inline.
6. **Append to `log.md`**: `## [YYYY-MM-DD] task | <n> task(s) captured` followed by the task lines.

## Done when

- The tasks are appended to `wiki/tasks/open.md`, `home.md` reflects them, and `log.md` has a
  correctly-prefixed entry.
