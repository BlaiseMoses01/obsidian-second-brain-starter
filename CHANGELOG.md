# Changelog

All notable changes to this boilerplate are documented here.

## [0.1.1] — 2026-06-22

Tightened the vault to a small **core** plus an opt-in bucket system, and added the `configure` and
`task` skills.

### Added

- **`configure` skill** — derives a bucket set from a free-text use-case blurb or an interactive quiz,
  then scaffolds exactly those buckets (dir + template + `CLAUDE.md` bucket-map row + `index.md`
  section + graph color) via `scripts/scaffold.py`. Re-run anytime to reshape the brain.
- **`task` skill + `tasks/` bucket** — quick-capture standalone asks into `wiki/tasks/open.md`
  (rolling list), archived to `done.md` on completion; adds the `task.md` template.
- **Schema-sync check** — `scaffold.py` keeps the category set aligned across the sources of truth
  (`CLAUDE.md` bucket map, `index.md` sections, `wiki/_templates/`, and graph colors); surfaced as a
  check in `lint`.

### Changed

- **Slimmed the default to core buckets** — ships with only `sources`, `tasks`, and `sessions`; every
  other page type (`people`, `projects`, `goals`, `meetings`, …) is now opt-in via `configure` rather
  than pre-built. `CLAUDE.md`, `README.md`, `home.md`, and `index.md` rewritten to match.
- Trimmed `.obsidian/graph.json` color groups to the core buckets.

### Removed

- **Skills** — `meeting-recap`, `project-snapshot`, `session-planning`, `touchpoint` (superseded by
  the core set + `configure`).
- **Templates** — the pre-shipped non-core templates (`devlog`, `goal`, `journal`, `meeting`,
  `organization`, `pattern`, `person`, `project`, `session-plan`); `configure` now generates these on
  demand.

### Fixed

- Vault-root resolution in the global skills — reworked the Bash snippet that broke on shell
  expansions under the static permission check.

[0.1.1]: https://github.com/BlaiseMoses01/obsidian-starter/releases/tag/v0.1.1

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
