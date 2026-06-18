---
name: query
description: Answer a question against the wiki — find relevant pages via index.md, read them, synthesize an answer with citations, and offer to file non-trivial answers back into the wiki so explorations compound. Use when the user asks a question about the knowledge base. Global — works from any CWD.
---

# Query the wiki

Answer a question from what's already compiled in the wiki, with citations.

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes:

Vault (auto-resolved): !`d="${CLAUDE_SKILL_DIR}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi`

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All paths below (`wiki/`, `index.md`, `log.md`) are relative to this resolved root.**

## Steps

1. **Read `index.md` first** to locate candidate pages by category. Use it as the map, then drill
   into the specific pages. (If the wiki has grown large and a search tool exists, use it; at this
   scale the index is enough.)
2. **Read the relevant pages** fully. Follow `[[wikilinks]]` to gather connected context.
3. **Synthesize an answer** with **citations** — link the wiki pages and `[[sources/<slug>]]` the
   claims come from. If the wiki doesn't cover it, say so plainly; suggest a web search or a source
   to ingest rather than guessing.
4. **Flag conflicts** — if pages disagree, surface the contradiction instead of silently picking one.
5. **Offer to file the answer back.** If the answer is a non-trivial synthesis, comparison, or newly
   discovered connection, offer to save it as a new page (usually `concepts/` or `patterns/`) so the
   exploration compounds instead of disappearing into chat. If the user says yes:
   - Write the page from the matching template, cite its sources, link it into related pages.
   - Update `index.md` and append a `## [YYYY-MM-DD] query | <topic>` entry to `log.md`.

## Output forms

Default to a markdown answer. Use a table for comparisons, and offer a Marp deck or chart only if
the question calls for it.

## Done when

- The question is answered with citations, conflicts are surfaced, and (if filed) the new page is
  linked and logged.
