---
name: lint
description: Health-check the wiki — find contradictions, stale/superseded claims, orphan pages, missing concept pages, missing cross-references, and frontmatter gaps. Produce a prioritized fix list and suggested next questions/sources, then log the pass. Use periodically as the wiki grows. Global — works from any CWD.
---

# Lint the wiki

Periodic health check. Keeps the wiki consistent as it grows.

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes:

Vault (auto-resolved): !`d="${CLAUDE_SKILL_DIR}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi`

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All paths below (`wiki/`, `index.md`, `log.md`) are relative to this resolved root.**

## Checks

1. **Contradictions** — claims that conflict across pages. Flag both, link their sources.
2. **Stale / superseded claims** — older statements a newer source has overtaken. Mark the old
   `status: superseded` (or update it) and link the newer source.
3. **Orphan pages** — pages with no inbound `[[links]]`. Either link them in from relevant pages or
   propose archiving.
4. **Missing pages** — concepts/entities referenced (linked or named) but lacking their own page.
5. **Missing cross-references** — related pages that should link to each other but don't.
6. **Frontmatter gaps** — pages missing required fields, or with relative/empty dates.
7. **Index/log drift** — pages not listed in `index.md`; recent operations missing from `log.md`.
8. **Data gaps** — important questions the wiki can't answer that a web search or new source could
   fill.

## Output

- A **prioritized fix list** (highest-impact first). Apply the safe, mechanical fixes directly
   (missing links, frontmatter, index entries); ask before anything lossy (archiving, deleting,
   superseding a claim).
- A short list of **suggested next questions to investigate and sources to find**.
- Append `## [YYYY-MM-DD] lint | <scope>` to `log.md` with a summary of what was checked and fixed.

## Done when

- The report is delivered, safe fixes are applied, and the pass is logged.
