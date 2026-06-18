#!/usr/bin/env python3
"""onboard: symlink this vault's global skills into ~/.claude/skills and set
SECOND_BRAIN_DIR in ~/.claude/settings.json. Idempotent — safe to re-run.

Vault root = argv[1] if given, else auto-detected from this script's location
(<vault>/.claude/skills/onboard/scripts/setup.py). A skill counts as "global" if
its SKILL.md contains a "## Vault root" section, so new global skills are picked
up automatically.
"""

import json
import sys
from pathlib import Path


def resolve_vault(argv):
    if len(argv) > 1 and argv[1].strip():
        return Path(argv[1]).expanduser().resolve()
    return Path(__file__).resolve().parents[4]


def main():
    vault = resolve_vault(sys.argv)
    if not (vault / "CLAUDE.md").is_file() or not (vault / "wiki").is_dir():
        print(f"ERROR: {vault} is not a vault (missing CLAUDE.md + wiki/).")
        sys.exit(1)

    skills_dir = vault / ".claude" / "skills"

    # A skill is "global" if its SKILL.md has a "## Vault root" heading line
    # (an exact heading, so prose mentions of the phrase don't false-match).
    def is_global(skill_md):
        return any(
            line.strip() == "## Vault root"
            for line in skill_md.read_text(encoding="utf-8", errors="ignore").splitlines()
        )

    global_skills = sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md") if is_global(p))

    target = Path.home() / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    linked, skipped = [], []
    for name in global_skills:
        link = target / name
        if link.is_symlink():
            link.unlink()
        elif link.exists():
            skipped.append(name)  # a real file/dir already owns this name — don't clobber
            continue
        link.symlink_to(skills_dir / name)
        linked.append(name)

    settings = Path.home() / ".claude" / "settings.json"
    data = {}
    if settings.is_file():
        try:
            data = json.loads(settings.read_text() or "{}")
        except json.JSONDecodeError:
            print(f"ERROR: {settings} is not valid JSON; fix or remove it, then re-run.")
            sys.exit(1)
    data.setdefault("env", {})["SECOND_BRAIN_DIR"] = str(vault)
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(data, indent=2) + "\n")

    print(f"VAULT={vault}")
    print(f"LINKED={','.join(linked) or '(none)'}")
    if skipped:
        print(f"SKIPPED={','.join(skipped)} (name already exists, not a symlink)")
    print(f"SECOND_BRAIN_DIR set in {settings}")


if __name__ == "__main__":
    main()
