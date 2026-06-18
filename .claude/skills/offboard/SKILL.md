---
name: offboard
description: Tear down this vault's machine setup — remove the global skill symlinks from ~/.claude/skills and optionally clear SECOND_BRAIN_DIR. Never deletes vault content (skills, wiki/, dump/, notes). Use to uninstall the vault from a machine or before deleting the repo.
disable-model-invocation: true
argument-hint: "[vault-path]"
---

# Offboard — remove this vault's setup

Reverses **onboard**. Removes only the global symlinks that resolve into this vault; your notes and
the vault's own skills are left completely intact.

## Steps

1. **Confirm intent.** Ask whether to also clear `SECOND_BRAIN_DIR` from `~/.claude/settings.json`
   (say no if other vaults or tools rely on it). Default: leave it.

2. **Run teardown:**
   `python3 ${CLAUDE_SKILL_DIR}/scripts/teardown.py $ARGUMENTS`
   (append `--remove-env` only if the user said yes in step 1).
   - Removes every symlink in `~/.claude/skills` that resolves into this vault.
   - With `--remove-env`, drops `SECOND_BRAIN_DIR` only if it equals this vault.
   - Read its `UNLINKED=` / `SECOND_BRAIN_DIR:` output.

3. **Report** what was removed. Remind the user the vault itself (its `.claude/skills`, `wiki/`,
   `dump/`) is untouched — deleting the repo, if they want that, is a separate manual step.

## Done when

- This vault's global symlinks are gone and vault content is untouched.
