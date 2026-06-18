#!/usr/bin/env python3
"""Verify every [[wikilink]] / ![[embed]] in the nav files and wiki/ resolves to a
real file. Skips wiki/_templates/ and .claude/ (those hold intentional placeholder
links). Exits non-zero if any link is broken. Stdlib only.
"""

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")


def scan_files():
    files = [VAULT / n for n in ("home.md", "index.md", "log.md") if (VAULT / n).is_file()]
    templates = VAULT / "wiki" / "_templates"
    files += [p for p in (VAULT / "wiki").rglob("*.md") if templates not in p.parents]
    return files


def resolves(target):
    # drop alias ("|...") and heading/block anchors ("#...")
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return True  # same-file heading link
    candidates = [target, target + ".md", f"wiki/{target}", f"wiki/{target}.md"]
    if "." in Path(target).name:  # an extensioned embed (e.g. an image)
        candidates.append(f"dump/assets/{Path(target).name}")
    return any((VAULT / c).exists() for c in candidates)


def main():
    files = scan_files()
    broken = []
    for f in files:
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for m in LINK_RE.finditer(line):
                if not resolves(m.group(1)):
                    broken.append(f"{f.relative_to(VAULT)}:{lineno}: [[{m.group(1)}]]")
    if broken:
        print("Broken wikilinks:")
        for b in broken:
            print(f"  {b}")
        sys.exit(1)
    print(f"Wikilinks OK ({len(files)} files scanned).")


if __name__ == "__main__":
    main()
