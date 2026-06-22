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

The vault ships with only the **core** buckets below. Add whatever optional page types fit your use
case with **/configure** — buckets are open-ended (common ones are `projects`, `people`,
`organizations`, `patterns`, `meetings`, `goals`, `journal`, `plans`, but any name
works). `/configure` scaffolds the dir, the template, this table row, the matching `index.md`
section, and the graph color. The rows between the markers are owned by `/configure`; change them by
re-running it, not by hand.

| Path                | Scope                                                          | Filename convention |
| ------------------- | ------------------------------------------------------------- | ------------------- |
| `wiki/_templates/`  | One template per **active** page type. Reference when creating new pages. | `<type>.md` |
<!-- BUCKETS:START -->
| `wiki/sources/` | One **summary page per ingested source**. (Karpathy core) | `kebab-title.md` |
| `wiki/tasks/` | Standalone asks/todos directed at the owner that don't belong to a meeting/goal/project. **Rolling list, not one page per task.** | `open.md / done.md` |
| `wiki/sessions/` | One **summary page per working session**, scraped from a Claude Code transcript via **/session-ingest**. | `YYYY-MM-DD-topic.md` |
<!-- BUCKETS:END -->

> **Note:** `wiki/tasks/` is the deliberate exception to Golden Rule #3 (one subject per page) — it's
> a fixed-file rolling list (`open.md` active, `done.md` archive), since tasks are inherently a list.
> Capture into it with **/task**; completed tasks move to `done.md` with a `— done: YYYY-MM-DD` suffix.

## Agent Skills & Tools

Skills in `.claude/skills/` encode the operations. Invoke them by name.

- **ingest** — process a new raw source (a file in `dump/` or a path given as an argument) into the wiki. *(global)*
- **task** — quick-capture standalone asks/todos from a brain dump into `tasks/open.md`. *(global)*
- **configure** — tailor which optional wiki buckets exist (from a use-case blurb or a quiz); scaffolds dirs/templates/index/graph. Re-run to reshape the brain. *(global)*
- **query** — answer a question against the wiki, with citations; optionally file the answer back. *(global)*
- **lint** — health-check the wiki for contradictions, stale claims, orphans, and gaps. *(global)*
- **session-ingest** — scrape the current Claude Code session's transcript and ingest it into the vault as a `sessions/` page (full fan-out). Run before `/clear`. *(global)*
- **onboard** — set up the vault on a new machine/user: symlink the global skills, set `SECOND_BRAIN_DIR`, personalize Core Info, then call **configure** to pick buckets. Re-run to reconfigure. Run after cloning.
- **offboard** — reverse onboard: remove this vault's global symlinks (and optionally clear `SECOND_BRAIN_DIR`). Never deletes vault content.

**Global skills (cross-CWD).** Skills marked *(global)* run from any repo, not just the vault. They
resolve the vault root from `SECOND_BRAIN_DIR` (else by walking up from the skill dir for a folder
with `CLAUDE.md` + `wiki/`), and self-declare via a `## Vault root` heading in their `SKILL.md`.
**Setup is automated:** run **/onboard** from the freshly-cloned vault — it symlinks every global
skill into `~/.claude/skills` and sets `SECOND_BRAIN_DIR`. (Manual equivalent: set
`SECOND_BRAIN_DIR=<vault>` in `~/.claude/settings.json` `env` and `ln -s` each global skill.)
