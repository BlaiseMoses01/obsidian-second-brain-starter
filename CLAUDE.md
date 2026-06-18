# Second Brain Schemas & Operating Manual

This file is the **schema**: it tells the LLM agent how this vault is structured and how to operateit. It is the single most important file in the system. Read it at the start of every session.

## Core Info

- **Vault Owner**: `<YOUR NAME>`
- **Use Case**: `What your primary goals , use cases, and areas of concern are for the brain. ex: " self, goals , people , learning , side projects"`

## GOLDEN RULES, ALWAYS FOLLOW

1. The agent **owns the wiki**; the owner rarely writes wiki pages themselves.
2. **Never** edit or delete anything in `dump/`.
3. One subject per page. Link liberally. Always cite sources.
4. On every **ingest**, update `index.md` and append to `log.md`.
5. Use **absolute dates** (today is provided in session context — convert "today"/"last week" to a
   real date before writing).
6. Prefer **updating an existing page** over creating a near-duplicate. Check `index.md` first.
7. Stay **interactive and one-source-at-a-time** by default; discuss takeaways before mass edits.
8. Note contradictions explicitly when a new source disagrees with an existing page — don't silently
  overwrite. Use a `> [!warning] Contradiction` callout and link both sources.

## Three key layers

1. **Raw sources** (`dump/`) — the curated, **immutable** source of truth. Articles,
   PDFs, transcripts, notes, images, whatever the user wants to ingest into the wiki in whatever format is convienient. The agent **reads** these but **never edits or deletes** them.Images go in `dump/assets/`.

2. **The wiki** (`wiki/`) — LLM-generated and managed markdown.  **The agent owns this layer entirely** — it creates, updates, and cross-links pages to build our knowledge graph.

3. **The schema** (this file + `.claude/skills/`) — the conventions and workflows that make the
   agent a disciplined wiki maintainer rather than a generic chatbot. Co-evolved over time.

## Root navigation files

| File       | Purpose                                                                                                                                              |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `home.md`  | The FOB dashboard / entry point. How to use the vault + active projects, open goals, recent decisions.                                               |
| `index.md` | **Content catalog** — every page listed under its category with a one-line summary. Read this first when answering a query. Updated on every ingest. |
| `log.md`   | **Chronological**, append-only record of operations (ingest/query/lint/setup).                                                                       |

## Wiki Bucket Map

| Path                     | Scope                                                               | Filename convention     |
| ------------------------ | ------------------------------------------------------------------- | ----------------------- |
| `wiki/sources/`          | One **summary page per ingested source**. (Karpathy core)           | `kebab-title.md`        |
| `wiki/people/`           | People: contacts, colleagues, interviewees, social, public figures. | `firstname-lastname.md` |
| `wiki/organizations/`    | Companies/orgs: employers, clients, competitors, vendors, schools.  | `org-name.md`           |
| `wiki/projects/`         | initatives, pocs , or greater organized deliveries (folder per project; nest sub-notes inside) | `project-name/project-name.md` |
| `wiki/patterns/`         | Reusable playbooks, mental models, designs, how-tos.                | `pattern-name.md`       |
| `wiki/devlog/`           | Dated engineering/work-log entries, per project or repo.            | `YYYY-MM-DD-slug.md`    |
| `wiki/meetings/`         | Dated notes: meetings, calls, interviews, social conversations.     | `YYYY-MM-DD-slug.md`    |
| `wiki/goals/`            | Goals, greater ambitions, things to work towards and track          | `goal-name.md`          |
| `wiki/journal/`          | Dated personal reflections, feelings, thoughts, and insights        | `YYYY-MM-DD.md`         |
| `wiki/_templates/`       | One template per page type. Reference when creating new pages.      | `<type>.md`             |
| `wiki/sessions/`          | working sessions logged wholistically                              | `YYYY-MM-DD-topic.md`   |
| `wiki/plans/`            | Dated daily plans: dependency-ordered task lists + time-blocked schedules. | `YYYY-MM-DD.md`         |

## Agent Skills & Tools

Skills in `.claude/skills/` encode the operations. Invoke them by name.

- **ingest** — process a new raw source (a file in `dump/` or a path given as an argument) into the wiki. *(global)*
- **query** — answer a question against the wiki, with citations; optionally file the answer back. *(global)*
- **lint** — health-check the wiki for contradictions, stale claims, orphans, and gaps. *(global)*
- **project-snapshot** — survey the repo you're working in and fold an ingestible `projects/` folder-note into the vault. *(global)*
- **meeting-recap** — right after a call, quiz the user and integrate a targeted recap (meeting note + people/orgs/projects/goals + action items).
- **touchpoint** — alignment gut-check: is recent time spent moving the goals forward? Advisory; recommends priorities.
- **session-planning** — morning setup: dependency-order the day's tasks, time-block them, write a `plans/` note, refresh `home.md`.
- **session-ingest** — scrape the current Claude Code session's transcript and ingest it into the vault as a `sessions/` page (full fan-out). Run before `/clear`. *(global)*
- **onboard** — set up the vault on a new machine/user: symlink the global skills, set `SECOND_BRAIN_DIR`, personalize Core Info. Re-run to reconfigure. Run after cloning.
- **offboard** — reverse onboard: remove this vault's global symlinks (and optionally clear `SECOND_BRAIN_DIR`). Never deletes vault content.

**Global skills (cross-CWD).** Skills marked *(global)* run from any repo, not just the vault. They
resolve the vault root from `SECOND_BRAIN_DIR` (else by walking up from the skill dir for a folder
with `CLAUDE.md` + `wiki/`), and self-declare via a `## Vault root` heading in their `SKILL.md`.
**Setup is automated:** run **/onboard** from the freshly-cloned vault — it symlinks every global
skill into `~/.claude/skills` and sets `SECOND_BRAIN_DIR`. (Manual equivalent: set
`SECOND_BRAIN_DIR=<vault>` in `~/.claude/settings.json` `env` and `ln -s` each global skill.)
