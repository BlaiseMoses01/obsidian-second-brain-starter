# Log

Chronological, append-only record of operations.

## [2026-06-18] lint | full vault

Ran `check_wikilinks.py` (OK, 3 files) and `markdownlint-cli2` (passed). Vault is a fresh starter (only `_templates/`). **Fix applied:** `index.md` was missing the Devlog, Journal, and Plans sections — added all three and reordered the section list to mirror the CLAUDE.md Wiki Bucket Map (11/11 buckets now in sync). Added a "Schema sync" check (#8) to the lint skill to catch bucket-map↔index↔templates drift going forward.
