---
name: configure
description: Tailor the vault's wiki buckets to what the owner actually uses the brain for — derive a bucket set from a free-text "what I want this for" blurb or an interactive quiz, then scaffold exactly those buckets (dir + template + CLAUDE.md row + index.md section + graph color). Re-run anytime to add or remove buckets. Use on first setup (called by /onboard) or whenever the brain's shape should change. Global — works from any CWD.
argument-hint: "[blurb or path to an intent note]"
---

# Configure the vault's buckets

The vault ships nearly empty — only the **core** buckets (`sources/`, `tasks/`) exist. This skill
scaffolds the **optional** buckets the owner actually wants, It's idempotent and re-runnable: run it again to add or remove
buckets as the brain evolves.

## Vault root

This skill is **global** — it runs from any CWD. Resolve the vault root before any reads/writes.
Run this in a **Bash tool call** (not via `!`-inline execution — the static permission check rejects
shell expansions):

```sh
d="${CLAUDE_SKILL_DIR:-$(pwd)}"; if [ -n "${SECOND_BRAIN_DIR:-}" ]; then echo "$SECOND_BRAIN_DIR"; else while [ "$d" != "/" ] && [ -n "$d" ]; do if [ -f "$d/CLAUDE.md" ] && [ -d "$d/wiki" ]; then echo "$d"; break; fi; d=$(dirname "$d"); done; fi
```

Precedence: `$SECOND_BRAIN_DIR` → walk up from the skill dir for a folder with `CLAUDE.md` + `wiki/`.
If neither resolves, **stop** and tell the user to set `SECOND_BRAIN_DIR`. The scaffold script
resolves the root the same way, so you don't need to pass `--vault` unless you want to be explicit.

## Steps

1. **See what exists.** Run `python3 ${CLAUDE_SKILL_DIR}/scripts/scaffold.py --list` to print the
   buckets currently **active** in this vault (`[x] <name> — <scope>`). There is no fixed catalog of
   options — buckets are open-ended and you design them in step 3.

2. **Determine intent.**
   - If `$ARGUMENTS` is a **path to a file**, read it as the owner's "what I want this brain for" note.
   - If `$ARGUMENTS` is **free text**, treat it as that blurb.
   - If `$ARGUMENTS` is **empty**, read the `## Core Info` **Use Case** in `<vault>/CLAUDE.md` for a
     hint, then **interview** the owner conversationally about what they want the brain to track —
     propose a starter bucket set and refine it with them. Don't read from a menu; invent the buckets
     that fit their goals.

3. **Design the bucket set.** Choose wiki buckets that intuitively match the owner's goals and the
   kinds of notes/relations they'll map together. Buckets are **open-ended** — any name works. For
   each **new optional** bucket, author its definition:
   - `name` — kebab-case (becomes the dir `wiki/<name>/`, template `<name>.md`, graph tag `#<name>`,
     and `## <Title Case>` index section).
   - `scope` — the one-line "what goes here" for the CLAUDE.md bucket-map row.
   - `filename` — the filename convention (e.g. `kebab-title.md`, `<name>/<name>.md`).
   - `template` — the full template body. **Tag its frontmatter `tags: [<name>]`** so the graph color
     group (`tag:#<name>`) matches the pages.
   - `color` *(optional)* — `{"a":1,"rgb":<int>}`; omit to let the script auto-assign a distinct one.

   Write these as a JSON array to a temp spec file, e.g. `/tmp/buckets.json`:

   ```json
   [{"name":"recipes","scope":"One dish per page — ingredients, method, notes.",
     "filename":"kebab-title.md","template":"---\ntags: [recipe]\n---\n\n# {{title}}\n\n## Ingredients\n\n## Method\n"}]
   ```

4. **Apply.** Run the scaffold script:
   - `python3 ${CLAUDE_SKILL_DIR}/scripts/scaffold.py --add --spec /tmp/buckets.json` to add the
     designed buckets (core `sources`/`tasks` are always folded in, so a fresh vault becomes
     self-sufficient — `--add` with no `--spec` just ensures core).
   - When **reconfiguring**, also pass `--remove <comma,list>` of optional bucket **names** the owner
     no longer wants. Removal trims the CLAUDE.md row, index.md section, and graph color, deletes the
     template, and removes the dir **only if it holds no pages** (it warns and keeps a dir/section that
     has real content — never destroys notes).
   - Read the `ADDED=` / `REMOVED=` output and any `WARN:` lines; surface warnings to the owner.

5. **Report.** List what was added/removed and note any bucket-specific skills that now apply (e.g. a
   `meetings/` bucket pairs with `/meeting-recap`, `plans/` with `/session-planning`), point the owner
   to `home.md`, and remind them they can re-run `/configure` anytime to change the brain's shape.

## Notes

- Each scaffolded bucket touches five places, all handled by the script: `wiki/<bucket>/` (+ template
  in `wiki/_templates/`), the **Wiki Bucket Map** table in `CLAUDE.md` (between the
  `<!-- BUCKETS:START/END -->` markers), the matching `## Section` in `index.md` (between the
  `<!-- SECTIONS:START/END -->` markers), and a `tag:#<name>` color group in `.obsidian/graph.json`.
- There is no bucket catalog — you design each bucket and author its template body inline in the
  `--spec` JSON. The script derives all locators from the bucket `name`, so add and remove stay in
  sync with nothing to maintain by hand.
- Run `/lint` afterward — its schema check (bucket map ↔ index ↔ templates) confirms the scaffold
  left everything consistent.

## Done when

- The owner's chosen optional buckets exist with their template, CLAUDE.md row, index.md section, and
  graph color; core buckets are intact; and `/lint` reports no schema-alignment gaps.
