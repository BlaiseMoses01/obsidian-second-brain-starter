---
name: lint
description: Health-check the wiki — find contradictions, stale/superseded claims, orphan pages, missing concept pages, missing cross-references, and frontmatter gaps. Produce a prioritized fix list and suggested next questions/sources, then log the pass. Use periodically as the wiki grows. Global — works from any CWD.
---

# Lint the wiki

Periodic health check. Keeps the wiki consistent as it grows.

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes:

**Resolve the vault root first.** Run this in a **Bash tool call** (not via `!`-inline execution — the
static permission check rejects shell expansions, so the inline form fails with "Contains expansion"):

```sh
d="${CLAUDE_SKILL_DIR:-$(pwd)}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi
```

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All paths below (`wiki/`, `index.md`, `log.md`) are relative to this resolved root.**

## Run the tooling first

The repo ships pre-commit **hooks** that deterministically catch the mechanical issues — run them
before any by-hand checking, so you spend your own effort only on what tooling can't judge. From the
vault root:

```sh
pre-commit run --all-files                   # all hooks: markdownlint + broken-wikilink check
# or just the wiki-relevant ones:
pre-commit run markdownlint-cli2 --all-files
python3 .github/scripts/check_wikilinks.py   # broken/dangling [[wikilinks]]
```

If `pre-commit` isn't installed, fall back to running `check_wikilinks.py` directly.

How the hooks map to the checks below:

- **check-wikilinks** → dangling links to pages that don't exist (feeds **4** *Missing pages* and
  **5** *Missing cross-references* — a broken link is usually a typo or a page that needs creating).
- **markdownlint-cli2** → markdown style/structure issues (supports **6** *Frontmatter gaps* hygiene).
- ruff is for the Python tooling, not wiki content — ignore its output for lint purposes.

The hooks find broken links but **not** orphans (pages with no *inbound* links) — that's still a
manual check (**3**). Use the tool output as the starting fix list, then do the judgment-based
checks below.

## Checks

1. **Contradictions** — claims that conflict across pages. Flag both, link their sources.
2. **Stale / superseded claims** — older statements a newer source has overtaken. Mark the old
   `status: superseded` (or update it) and link the newer source. Also flag **overdue tasks** in
   `wiki/tasks/open.md` (a `due:` date in the past, still unchecked) for follow-up or archiving.
3. **Orphan pages** — pages with no inbound `[[links]]`. Either link them in from relevant pages or
   propose archiving.
4. **Missing pages** — concepts/entities referenced (linked or named) but lacking their own page.
5. **Missing cross-references** — related pages that should link to each other but don't.
6. **Frontmatter gaps** — pages missing required fields, or with relative/empty dates.
7. **Index/log drift** — pages not listed in `index.md`; recent operations missing from `log.md`.
8. **Schema sync** — the category set must match across sources of truth. Cross-check the CLAUDE.md
   **Wiki Bucket Map** against `index.md` sections and `wiki/_templates/` (one template per bucket).
   Every bucket should have a matching `index.md` section (in bucket-map order) and a template; flag
   any bucket missing from `index.md`, any orphan `index.md` section with no bucket, and any bucket
   lacking a template.
9. **Data gaps** — important questions the wiki can't answer that a web search or new source could
   fill.

## Output

- A **prioritized fix list** (highest-impact first). Apply the safe, mechanical fixes directly
   (missing links, frontmatter, index entries); ask before anything lossy (archiving, deleting,
   superseding a claim).
- A short list of **suggested next questions to investigate and sources to find**.
- Append `## [YYYY-MM-DD] lint | <scope>` to `log.md` with a summary of what was checked and fixed.

## Done when

- The report is delivered, safe fixes are applied, and the pass is logged.
