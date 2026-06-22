# Log

Chronological, append-only record of operations.

## [2026-06-22] lint | full vault

Ran `check_wikilinks.py` (OK, 5 files; `pre-commit` not installed). Content layer still empty — no sources/tasks/sessions — so contradiction/stale/orphan/missing-page/cross-ref/frontmatter checks (1–6) had nothing to flag. **Schema sync clean** across all 5 sources of truth: buckets `sources`/`tasks`/`sessions` align across the CLAUDE.md bucket-map, `index.md` sections (same order), `_templates/` (`source`/`task`/`session`), and graph colors (`#source`/`#task`/`#session`). All 8 installed skills resolve; every skill reference in `CLAUDE.md` and `home.md` is valid (no dead refs). No fixes needed.

## [2026-06-18] lint | full vault

Ran `check_wikilinks.py` (OK, 3 files) and `markdownlint-cli2` (passed). Vault is a fresh starter (only `_templates/`). **Fix applied:** `index.md` was missing the Devlog, Journal, and Plans sections — added all three and reordered the section list to mirror the CLAUDE.md Wiki Bucket Map (11/11 buckets now in sync). Added a "Schema sync" check (#8) to the lint skill to catch bucket-map↔index↔templates drift going forward.

## [2026-06-22] configure | promote sessions to core

Promoted **`sessions`** from an optional bucket to a **core** (shipped, never-removed) bucket so the global **session-ingest** skill always has a home. Added a `sessions` entry to the `CORE` dict in `configure/scripts/scaffold.py`, shipped `wiki/_templates/session.md`, and ran `scaffold.py --add` to materialize the `wiki/sessions/` dir, CLAUDE.md bucket-map row, `index.md` Sessions section, and `#session` graph color (purple). Removed `sessions` from the optional-examples prose in CLAUDE.md and added it to the core-bucket lists in README. Schema sync **clean** across all 5 sources of truth; `check_wikilinks.py` OK.

## [2026-06-21] lint | full vault

Ran `check_wikilinks.py` (OK, 5 files; `pre-commit` not installed). Vault restructured down to 2 buckets — schema sync **clean**: `sources` + `tasks` align across the CLAUDE.md bucket-map, `index.md` sections, `_templates/`, and graph color groups (`#source`, `#task`). Wiki content layer is empty (no sources/tasks), so contradiction/orphan/frontmatter checks had nothing to flag. **Drift found:** 4 removed skills (`meeting-recap`, `project-snapshot`, `session-planning`, `touchpoint`) are still referenced in `home.md`, `CLAUDE.md`, and `README.md`. **Fix applied:** removed the 4 dead skill references from `home.md` (rewrote "How to use"), `CLAUDE.md` (Agent Skills list), and `README.md` (skills table). CHANGELOG.md left as-is (append-only release history).
