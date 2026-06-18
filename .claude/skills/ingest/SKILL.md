---
name: ingest
description: Process a new raw source into the wiki — read it, discuss takeaways, write a source summary, update affected entity/concept/project pages, update index.md, and append to log.md. Use when a source is added to dump/ (or a file path is given) and you want it integrated. Global — works from any CWD.
argument-hint: "[source-path]"
---

# Ingest a source

Integrate one new source into the wiki. Default to **one source at a time** and stay interactive.

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes:

Vault (auto-resolved): !`d="${CLAUDE_SKILL_DIR}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi`

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All paths below (`dump/`, `wiki/`, `index.md`, `log.md`) are relative to this resolved root.**

## Steps

1. **Read the source** in full. The source is either the file at `$ARGUMENTS` (a path in any repo/CWD)
   or, if no argument is given, the new file(s) in `<vault>/dump/`. If it references images in
   `<vault>/dump/assets/`, read the text first, then view the relevant images for extra context.
   Never modify anything in `<vault>/dump/`.
2. **Discuss takeaways** with the user — 3–6 key points — before making mass edits. Confirm what to
   emphasize and which entities/concepts matter.
3. **Write the source summary page** in `wiki/sources/<kebab-title>.md`. Include frontmatter
   (`url` for hard-linked websites, `author`, `source_date`, `ingested` = today, `media`), a 1–2 line
   summary, key points, and `[[links]]` to every entity/concept it touches. (Rough notes jotted into
   `dump/` are fair game to delete after ingestion; hard-linked sources live on via their `url`.)
4. **Integrate across the wiki.** Create or update the affected pages — `people/`,
   `organizations/`, `concepts/`, `projects/`, `areas/`, etc. A single source often touches 10–15
   pages. For each:
   - Add new facts; cite back with `[[sources/<slug>]]`.
   - Prefer updating an existing page over making a near-duplicate (check `index.md` first).
   - If the source **contradicts** an existing claim, don't overwrite silently — add a
     `> [!warning] Contradiction` callout linking both sources and flag it to the user.
   - Bump each touched page's `updated:` to today and add new `[[wikilinks]]`.
5. **Update `index.md`** — add the new source and any new pages under their category sections with
   one-line summaries.
6. **Append to `log.md`**: `## [YYYY-MM-DD] ingest | <Source Title>` followed by 1–3 bullets listing
   the pages created/updated.
7. **Update `home.md`** if the ingest changed active projects, open goals, or recent decisions.

## Done when

- A `sources/` summary exists, ≥1 entity/concept page was updated, `index.md` reflects the new
  pages, and `log.md` has a correctly-prefixed entry.
