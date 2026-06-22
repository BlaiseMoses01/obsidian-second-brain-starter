---
name: onboard
description: Set up this second-brain vault on a new machine or for a new owner — symlink the global skills into ~/.claude/skills, set SECOND_BRAIN_DIR, and personalize CLAUDE.md. Re-run to reconfigure (e.g. point at a moved/renamed vault). Use right after cloning the boilerplate.
disable-model-invocation: true
argument-hint: "[vault-path]"
---

# Onboard — set up this vault

One-time (but re-runnable) setup so the vault and its **global** skills work from any repo. Safe to
run repeatedly; it never deletes anything.

## Steps

1. **Run setup** (idempotent):
   `python3 ${CLAUDE_SKILL_DIR}/scripts/setup.py $ARGUMENTS`
   - Vault root = `$ARGUMENTS` if a path was given, else auto-detected from this skill's location.
   - It symlinks every skill that declares a `## Vault root` section into `~/.claude/skills`, and
     merges `SECOND_BRAIN_DIR=<vault>` into `~/.claude/settings.json` (preserving other settings).
   - Read its `VAULT=` / `LINKED=` / `SKIPPED=` output. If it errors (not a vault, or invalid
     settings JSON), **stop** and surface the message.

2. **Personalize `<vault>/CLAUDE.md` Core Info.** If `Vault Owner` is still `<YOUR NAME>` (or the
   user wants to change it), ask for their **name** and **primary use case**, then fill in the
   **Core Info** block.

3. **Pick buckets.** The vault ships with only the **core** buckets (`sources/`, `tasks/`). Run
   **/configure** to scaffold the optional page types the owner actually wants — pass the use case
   from step 2 as a blurb, or let it quiz interactively. (Skip only if the owner explicitly wants to
   stay core-only for now; they can run `/configure` anytime.)

4. **Sanity-check structure.** Confirm `dump/` (+ `dump/assets/`) and the core `wiki/` buckets exist;
   create only what's missing. Never touch existing content.

5. **Report** what was linked and set, and point the user to `home.md` to begin. Note: newly
   symlinked skills may require restarting Claude Code to register.

## Reconfigure

- **Moved/renamed vault:** re-run `/onboard` from its new location (auto-detected) or `/onboard
  <new-path>` — it rewrites `SECOND_BRAIN_DIR` and re-links.
- To undo everything, use **offboard**.

## Done when

- The global skills are symlinked, `SECOND_BRAIN_DIR` points at this vault, Core Info is filled in,
  and the owner's buckets are scaffolded (or they've chosen to stay core-only).
