---
name: session-ingest
description: Scrape the current Claude Code session's transcript and ingest it into the configured second-brain vault as a sessions/ page, with full fan-out to projects/people/goals. Run at the end of a working session, before /clear. Works from any CWD.
argument-hint: "[vault-path]"
disable-model-invocation: true
---

# Ingest this session into the wiki

Capture the conversation you just had — from any repo — and fold it into the vault like a scoped
`ingest`. A deterministic script scrapes the transcript, a Haiku subagent summarizes it (keeping the
bulky raw text out of this context), then you do the wiki integration after a confirmation step.

## Vault root

Vault (auto-resolved): !`d="${CLAUDE_SKILL_DIR}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi`

## Steps

0. **Resolve the vault root** (precedence):
   1. If `$ARGUMENTS` is non-empty, use it as the vault path.
   2. Else use the auto-resolved path injected above (`$SECOND_BRAIN_DIR`, or derived from this
      skill's location).
   3. If neither yields a directory containing `CLAUDE.md` + `wiki/`, **stop** and tell the user to
      set `SECOND_BRAIN_DIR` (in `~/.claude/settings.json` `env`, or the repo's settings) or pass the
      path as an argument. All vault writes below use this absolute root.

1. **Scrape the transcript:**
   `python3 ${CLAUDE_SKILL_DIR}/scripts/scrape_session.py ${CLAUDE_SESSION_ID}`
   It writes a clean digest to `/tmp/claude-session-<id>.md` and prints `STAGING_FILE=`, `TITLE=`,
   `DATE=`, `CWD=`, `SLUG=`, `TURNS=`. Capture the staging path. If it exits with an error (no
   transcript), stop and report.

2. **Summarize via a Haiku subagent.** Spawn an `Agent` with `model: haiku` whose prompt gives it the
   **absolute staging-file path** and this output contract — it reads the file and returns ONLY:
   - `topic` (short, for the page slug) and a 1–2 line summary
   - what was done / decided
   - **entities touched**: projects, people, organizations, goals (names)
   - action items (owner + absolute due date where stated)
   - open threads / next steps and key takeaways
   The raw transcript stays in the subagent's context, not this one.

3. **Confirm before writing.** Read `<vault>/index.md` to dedup against existing pages. Then show the
   user the proposed `sessions/` page (title + summary) and the list of wiki pages you'll
   create/update. Wait for approval. Convert any relative dates to absolute (today's date is in
   session context).

4. **Full ingest** (mirror the `ingest` discipline; all paths absolute under the vault root):
   - Write `<vault>/wiki/sessions/YYYY-MM-DD-<topic-slug>.md`. If `<vault>/wiki/_templates/session.md`
     exists, use it; otherwise use the embedded structure below.
   - **Fan out**: create or update each touched `projects/`, `people/`, `organizations/`, `goals/`,
     `devlog/` page. Add new facts; cite back with `[[sessions/<slug>]]`; prefer updating an existing
     page over a near-duplicate; on conflicts add a `> [!warning] Contradiction` callout linking both
     and flag it; bump each touched page's `updated:` to today.
   - Update `<vault>/index.md` with the new session and any new pages (one-line summaries).
   - Append to `<vault>/log.md`: `## [YYYY-MM-DD] session-ingest | <topic>` with 1–3 bullets.
   - Update `<vault>/home.md` if active projects, open goals, or recent decisions changed.

5. **Clean up.** Remove the `/tmp` staging file.

## Embedded sessions/ page structure (used when no template is present)

```markdown
---
date: YYYY-MM-DD
repo: <cwd the session ran in>
projects: ["[[projects/project-name]]"]
tags: [session]
---

# <Topic> — YYYY-MM-DD

## Summary
1–2 lines.

## What was done
- ...

## Decisions
- ...

## Action items
- [ ] <action> — owner: [[people/firstname-lastname]] — due: YYYY-MM-DD

## Open threads
- ...

## Links
- [[projects/project-name]] · [[people/firstname-lastname]]
```

## Done when

- A `sessions/` page exists for this session, relevant entity/project pages are updated with
  cite-backs, `index.md` + `log.md` reflect it, and the `/tmp` staging file is removed.
