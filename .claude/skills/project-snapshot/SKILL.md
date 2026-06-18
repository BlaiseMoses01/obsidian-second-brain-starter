---
name: project-snapshot
description: Survey the repo/project you're currently working in (README, structure, git history, key files) and fold an ingestible project page into the second-brain vault — creates or updates the projects/ folder-note and fans out to related people/orgs/sources. Use to capture "what is this codebase / what have we done here" without writing it by hand. Global — works from any CWD.
argument-hint: "[repo-path]"
---

# Snapshot the current project into the wiki

Capture the repo you're working in as a wiki `projects/` page. This is **generate-then-ingest**: you
survey the codebase yourself (no file is pre-written), draft an overview, confirm, then integrate.

## Vault root

This skill is **global** — it runs from inside any repo. Resolve the vault root before any writes:

**Resolve the vault root first.** Run this in a **Bash tool call** (not via `!`-inline execution — the
static permission check rejects shell expansions, so the inline form fails with "Contains expansion"):

```sh
d="${CLAUDE_SKILL_DIR:-$(pwd)}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi
```

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`. If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. **All `wiki/`, `index.md`, `log.md` paths below are relative to this resolved root.** The **repo being snapshotted** is `$ARGUMENTS` if given, else the current working directory.

## Steps

1. **Survey the repo** with scoped, read-only commands — don't dump whole files into context:
   - `git -C <repo> remote -v` and `git -C <repo> log --oneline -20` (origin + recent work).
   - Top-level structure (e.g. `ls`, a 2-level tree), the `README`, and the package manifest
     (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`, whichever exists).
   - Skim the main entry point(s) only as needed. For a large repo, delegate the survey to an
     `Explore` subagent and work from its summary.
2. **Draft the overview** — project name (kebab), one-line purpose, stack, current status, what it
   does, notable decisions, and which people/orgs it touches. Convert relative dates to absolute.
3. **Confirm before writing.** Read `<vault>/index.md` to dedup. Show the user the proposed project
   name + summary and the pages you'll create/update. **Prefer updating an existing project** over a
   near-duplicate. Wait for approval.
4. **Write the project folder-note** at `<vault>/wiki/projects/<name>/<name>.md` from
   `wiki/_templates/project.md`. Record the repo path / git remote in the body so the page points
   back at the code. Nest any sub-notes (e.g. a dated `devlog/`) inside the same folder.
5. **Fan out (scoped).** Create or update related `people/`, `organizations/`, and a `sources/` entry
   if the snapshot itself is worth citing. Add `[[wikilinks]]` both ways; bump `updated:`.
6. **Update `index.md`** — add the project (and any new pages) with one-line summaries.
7. **Append to `log.md`**: `## [YYYY-MM-DD] project-snapshot | <Project>` with 1–3 bullets.
8. **Update `home.md`** if this is now an active project.

## Done when

- A `projects/<name>/<name>.md` folder-note exists (pointing back at the repo), related pages are
  linked, and `index.md` + `log.md` are current.
