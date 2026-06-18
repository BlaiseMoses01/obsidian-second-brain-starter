# Changelog

All notable changes to this boilerplate are documented here.

## [0.1.0] — 2026-06-18

Initial public boilerplate.

### Added

- **Three-layer vault model** — `dump/` (immutable raw sources) → `wiki/` (agent-owned knowledge base)
  → schema (`CLAUDE.md` + `.claude/skills/`).
- **Page templates** for every bucket type in `wiki/_templates/` (source, person, organization, project,
  pattern, devlog, goal, journal, meeting, session, session-plan).
- **Knowledge-graph colors** — per-type `tag:#<type>` color groups in `.obsidian/graph.json`.
- **Projects folder-note convention** — `wiki/projects/<name>/<name>.md` with nested sub-notes.
- **Skills:**
  - Global (run from any directory): `ingest`, `query`, `lint`, `project-snapshot`, `session-ingest`.
  - Vault-local: `meeting-recap`, `session-planning`, `touchpoint`.
  - Setup: `onboard` / `offboard` (symlink global skills + manage `SECOND_BRAIN_DIR`, fully reversible).
- **`dump/` guardrail** — the agent can read but never edit/delete raw sources (enforced in
  `.claude/settings.json`).
- **CI** — pre-commit hooks + a GitHub Actions workflow running ruff (lint + format), markdownlint-cli2,
  and a stdlib broken-`[[wikilink]]` checker (`.github/scripts/check_wikilinks.py`).
- **`.gitignore`** for machine-specific Obsidian/Claude state, keeping portable config tracked.
- **Multi-device sync** documentation (private fork + the Obsidian Git plugin).

[0.1.0]: https://github.com/BlaiseMoses01/obsidian-starter/releases/tag/v0.1.0
