# obsidian-starter — an LLM-maintained second brain

[![CI](https://github.com/BlaiseMoses01/obsidian-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/BlaiseMoses01/obsidian-starter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A boilerplate [Obsidian](https://obsidian.md) vault that [Claude Code](https://claude.com/claude-code)
maintains for you. You drop raw material in; the agent reads it, writes and cross-links wiki pages, and
keeps a navigable knowledge graph. **You own the sources and the schema — the agent owns the wiki.**

## How it works

### The three layers

1. **`dump/`** — raw sources (articles, PDFs, transcripts, notes, images). Curated by you,
   **immutable to the agent** (it reads, never edits/deletes — enforced in `.claude/settings.json`).
2. **`wiki/`** — the LLM-generated knowledge base. The agent creates, updates, and cross-links these
   pages into a graph. One subject per page; everything cites its source.
3. **The schema** — `CLAUDE.md` (the operating manual the agent reads every session) plus the skills in
   `.claude/skills/`. These conventions are what make the agent a disciplined librarian instead of a
   generic chatbot.

### The loop

```textg
drop a source in dump/  →  /ingest  →  wiki page(s) written + linked  →  /query to ask  →  /lint to keep it healthy
```

- **Ingest** reads one source, discusses takeaways with you, then writes a `sources/` summary and fans
  out facts to the people / orgs / projects / patterns it touches — citing back to the source.
- **Query** answers from what's compiled, with citations, and offers to file good answers back so
  explorations compound instead of vanishing into chat.
- **Lint** periodically checks for contradictions, orphans, stale claims, and missing links.

Navigate the vault from three root files: **`home.md`** (dashboard), **`index.md`** (catalog of every
page), and **`log.md`** (append-only history of operations).

The Obsidian **graph view** is color-coded by page type (people, projects, meetings, …) via tag-based
color groups in `.obsidian/graph.json`. Projects use a **folder-note** layout
(`wiki/projects/<name>/<name>.md`) so a project can grow sub-notes without cluttering the bucket.

## What's included

```text
obsidian-starter/
├── home.md, index.md, log.md   # dashboard · catalog · operation log
├── CLAUDE.md                   # the schema / operating manual (read every session)
├── dump/                       # your raw sources (read-only to the agent); assets/ for images
├── wiki/
│   ├── _templates/             # template per active page type (ships: source, task, session)
│   ├── sources/ tasks/ sessions/  # core buckets — always present
│   └── …                       # add optional buckets (people, projects, …) with /configure
├── .claude/
│   ├── settings.json           # dump/ read-only guardrail + config
│   └── skills/                 # the operations (see below)
├── .github/                    # CI workflow + the wikilink checker
├── .gitignore .pre-commit-config.yaml .markdownlint.json pyproject.toml
└── LICENSE  CHANGELOG.md
```

## Quickstart

**Prerequisites:** [Claude Code](https://claude.com/claude-code), [Obsidian](https://obsidian.md), git,
and Python 3.11+ (the setup scripts are stdlib-only).

1. **Get the files** — click **Use this template** on GitHub (recommended — see below), or clone the repo.
   If this will hold real notes, put it in a **private** repo (see [Multi-device sync](#multi-device-sync)).
2. **Open the vault folder in Claude Code** and run **`/onboard`**. It:
   - symlinks the global skills into `~/.claude/skills`,
   - sets `SECOND_BRAIN_DIR` in `~/.claude/settings.json`,
   - fills in your name + use case in `CLAUDE.md` → Core Info,
   - runs **`/configure`** to scaffold the optional buckets you want (or stay core-only).
3. **Open the same folder in Obsidian** and start from `home.md`.
4. **Drop a source** into `dump/` and run **`/ingest`** to watch it fold into the wiki.

To remove the machine setup later, run **`/offboard`** (it only removes this vault's symlinks — it never
touches your notes).

## The skills

Invoke any skill by name (e.g. `/ingest`). *Global* skills run from **any** directory — they resolve the
vault via `SECOND_BRAIN_DIR` (else by walking up for a folder with `CLAUDE.md` + `wiki/`); `/onboard`
wires this up. Vault-local skills run when the vault is your working folder.

| Skill | When to use | Example |
| --- | --- | --- |
| **ingest** *(global)* | Fold a source into the wiki | `/ingest ~/Downloads/article.pdf` |
| **task** *(global)* | Quick-capture standalone asks/todos | `/task coffee chat with Jane next week` |
| **configure** *(global)* | Pick which optional buckets your brain has | `/configure side projects, learning, people` |
| **query** *(global)* | Ask the wiki a question, with citations | `/query what did we decide about X?` |
| **lint** *(global)* | Health-check the wiki | `/lint` |
| **session-ingest** *(global)* | Fold the current Claude Code session into the wiki | `/session-ingest` (before `/clear`) |
| **onboard / offboard** | Install / uninstall the vault on a machine | `/onboard` |

## Customizing your brain

Make it yours — the schema is meant to evolve:

- **Identity & focus** — edit the `## Core Info` block in `CLAUDE.md` (owner + use case). `/onboard`
  prompts for this on first run.
- **Buckets** — the vault ships **core-only** (`sources/`, `tasks/`, `sessions/`). Run **`/configure`** to add the
  optional page types you want — buckets are open-ended, so it designs whatever fits (driven by a
  use-case blurb or an interview) and scaffolds the dir, template, `CLAUDE.md` row, `index.md`
  section, and graph color from an agent-authored `--spec` JSON. Re-run anytime to add/remove buckets.
- **Templates** — every page type has a template in `wiki/_templates/`; tweak freely. They use
  placeholders like `<First Last>`, `firstname-lastname`, and `YYYY-MM-DD`.
- **Guardrails** — `dump/` is read-only to the agent via deny-rules in `.claude/settings.json`.

## Multi-device sync

The public template lives upstream; **for your real notes, clone it into your own private repo** and sync
that across devices:

1. Create a **private** git repo and push your vault to it.
2. Install the **[Obsidian Git](https://github.com/Vinzent03/obsidian-git)** community plugin on each
   device. Configure auto **pull on open** and **commit + push** on an interval (and on close). Every
   device then stays in sync hands-off.
3. Your `wiki/` and `dump/` (the brain) sync; machine-specific state is git-ignored (see `.gitignore` —
   `.obsidian/workspace.json` etc.). Portable Obsidian config (graph colors, enabled core plugins) stays
   tracked so a fresh clone looks right.
4. Enable pull-before-push to avoid conflicts; add large binaries to `dump/assets/` deliberately.

## Development / CI

Runtime scripts are Python **stdlib-only** (no dependencies). CI is dev tooling only:

```sh
pip install pre-commit
pre-commit install          # run hooks on every commit
pre-commit run --all-files  # run them now
```

Checks (also run in GitHub Actions on push/PR — see `.github/workflows/ci.yml`):

- **ruff** — lint + format the scripts under `.claude/skills/*/scripts/`.
- **markdownlint-cli2** — markdown hygiene (lenient config in `.markdownlint.json`; `dump/` excluded).
- **check-wikilinks** — flags broken `[[wikilinks]]` in the nav files and `wiki/`
  (`.github/scripts/check_wikilinks.py`).

## License

[MIT](LICENSE) © 2026 Blaise Moses. See [`CHANGELOG.md`](CHANGELOG.md) for version history.
Built to be maintained with [Claude Code](https://claude.com/claude-code).
