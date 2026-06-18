#!/usr/bin/env python3
"""offboard: remove this vault's global skill symlinks from ~/.claude/skills.
With --remove-env, also drop SECOND_BRAIN_DIR (only if it points at this vault).
Never touches vault content (wiki/, dump/, notes).

Vault root = first non-flag arg if given, else auto-detected from this script's
location (<vault>/.claude/skills/offboard/scripts/teardown.py).
"""

import json
import sys
from pathlib import Path


def resolve_vault(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if args and args[0].strip():
        return Path(args[0]).expanduser().resolve()
    return Path(__file__).resolve().parents[4]


def main():
    vault = resolve_vault(sys.argv)
    remove_env = "--remove-env" in sys.argv

    target = Path.home() / ".claude" / "skills"
    removed = []
    if target.is_dir():
        for link in target.iterdir():
            if not link.is_symlink():
                continue
            try:
                dest = link.resolve()
            except OSError:
                continue
            if dest == vault or str(dest).startswith(str(vault) + "/"):
                link.unlink()
                removed.append(link.name)

    settings = Path.home() / ".claude" / "settings.json"
    env_note = "left as-is"
    if remove_env and settings.is_file():
        try:
            data = json.loads(settings.read_text() or "{}")
        except json.JSONDecodeError:
            data = None
        if data is not None and data.get("env", {}).get("SECOND_BRAIN_DIR") == str(vault):
            data["env"].pop("SECOND_BRAIN_DIR", None)
            if not data["env"]:
                data.pop("env", None)
            settings.write_text(json.dumps(data, indent=2) + "\n")
            env_note = "removed"

    print(f"VAULT={vault}")
    print(f"UNLINKED={','.join(sorted(removed)) or '(none)'}")
    print(f"SECOND_BRAIN_DIR: {env_note}")
    print("Vault content untouched (skills, wiki/, dump/, notes).")


if __name__ == "__main__":
    main()
