#!/usr/bin/env python3
"""configure: scaffold (or remove) wiki buckets in this vault.

Core buckets (sources, tasks, sessions) are fixed infrastructure and always present.
Optional buckets are open-ended: the /configure agent designs them and passes
their definitions as a JSON spec to `--add --spec`. Each bucket instantiates five
things — a wiki/<name>/ dir, a wiki/_templates/<name>.md template, a row in
CLAUDE.md's Wiki Bucket Map, a section in index.md, and a tag color group in
.obsidian/graph.json. This script is the deterministic half of the /configure
skill; the interactive bucket design lives in SKILL.md.

A bucket's locators are derived by convention from its name (dir wiki/<name>,
template <name>.md, graph query tag:#<name>, index heading title-cased), so add
and remove stay symmetric with no stored catalog. The agent authors only the
descriptive content per bucket: scope, filename convention, and the template body.

Idempotent: re-adding an existing bucket is a no-op; removing a missing one is a
no-op. Core buckets are always added and never removed. The script never deletes
a bucket dir that holds real pages, nor an index.md section that holds content —
it warns and skips instead.

Vault root precedence: --vault arg -> $SECOND_BRAIN_DIR -> auto-detect from this
script's location (<vault>/.claude/skills/configure/scripts/scaffold.py).

Usage:
  scaffold.py --add --spec buckets.json
  scaffold.py --add                       # ensure core only (fresh vault)
  scaffold.py --remove meetings,goals
  scaffold.py --list
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

TABLE_START, TABLE_END = "<!-- BUCKETS:START -->", "<!-- BUCKETS:END -->"
SECTIONS_START, SECTIONS_END = "<!-- SECTIONS:START -->", "<!-- SECTIONS:END -->"

# Core buckets are fixed infrastructure — always present, never removed. Their
# templates ship in wiki/_templates/, so core adds carry no template_body.
CORE = {
    "sources": {
        "path": "wiki/sources/",
        "scope": "One **summary page per ingested source**. (Karpathy core)",
        "filename": "kebab-title.md",
        "index_section": "Sources",
        "graph_tag": "#source",
        "graph_color": {"a": 1, "rgb": 14726204},
        "template": "source.md",
    },
    "tasks": {
        "path": "wiki/tasks/",
        "scope": "Standalone asks/todos directed at the owner that don't belong to a "
        "meeting/goal/project. **Rolling list, not one page per task.**",
        "filename": "open.md / done.md",
        "index_section": "Tasks",
        "graph_tag": "#task",
        "graph_color": {"a": 1, "rgb": 3447003},
        "template": "task.md",
    },
    "sessions": {
        "path": "wiki/sessions/",
        "scope": "One **summary page per working session**, scraped from a Claude Code "
        "transcript via **/session-ingest**.",
        "filename": "YYYY-MM-DD-topic.md",
        "index_section": "Sessions",
        "graph_tag": "#session",
        "graph_color": {"a": 1, "rgb": 13007069},
        "template": "session.md",
    },
}

# Distinct color groups auto-assigned to optional buckets (a bucket may override
# with its own `color` in the spec). Shape matches .obsidian/graph.json.
PALETTE = [
    {"a": 1, "rgb": 14707829},  # red
    {"a": 1, "rgb": 15057019},  # yellow
    {"a": 1, "rgb": 10011513},  # green
    {"a": 1, "rgb": 6402031},  # blue
    {"a": 1, "rgb": 13007069},  # purple
    {"a": 1, "rgb": 5682882},  # cyan
    {"a": 1, "rgb": 13736550},  # orange
]

TASKS_OPEN_SEED = """---
tags: [task]
---

# Open Tasks

Standalone asks and todos directed at the owner that don't belong to a specific
meeting/goal/project. Rolling list — newest at the top. Check a task off and move it to
[[tasks/done]] with a `— done: YYYY-MM-DD` suffix once complete.

Line format (every field after the task text is optional — omit what doesn't apply); see
`wiki/_templates/task.md` for the full field reference:

`- [ ] <task> — requestor: people/firstname-lastname — due: YYYY-MM-DD — re: projects/name — src: sources/slug`

(wrap the `requestor`/`re`/`src` paths in `[[ ]]` when writing a real task so they link)

## Tasks

_None yet._
"""

TASKS_DONE_SEED = """---
tags: [task]
---

# Done Tasks

Archive of completed tasks moved out of [[tasks/open]], so the open list stays scannable.
Each line keeps its original fields plus a `— done: YYYY-MM-DD` suffix. Newest at the top.

## Tasks

_None yet._
"""


def resolve_vault(arg):
    if arg and arg.strip():
        return Path(arg).expanduser().resolve()
    env = os.environ.get("SECOND_BRAIN_DIR", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[4]


def titlecase(name):
    """Bucket name -> index-section heading, e.g. 'meeting-notes' -> 'Meeting Notes'."""
    return " ".join(w.capitalize() for w in name.replace("_", "-").split("-") if w)


def bucket_from_name(name):
    """Locators derived purely by convention — enough to find/remove a bucket's edits."""
    return {
        "path": f"wiki/{name}/",
        "index_section": titlecase(name),
        "graph_tag": f"#{name}",
        "template": f"{name}.md",
    }


def pick_color(used):
    """First palette color whose rgb isn't already taken; records it in `used`."""
    for c in PALETTE:
        if c["rgb"] not in used:
            used.add(c["rgb"])
            return c
    return PALETTE[0]  # palette exhausted — reuse is harmless


def bucket_from_spec(entry, used):
    """An agent-authored spec entry -> the bucket dict the edit_* functions expect."""
    name = entry["name"].strip()
    b = bucket_from_name(name)
    b["scope"] = (entry.get("scope") or "").strip() or f"One page per {name} entry."
    b["filename"] = (entry.get("filename") or "").strip() or "kebab-title.md"
    color = entry.get("color")
    if color:
        used.add(color.get("rgb"))
    else:
        color = pick_color(used)
    b["graph_color"] = color
    b["template_body"] = entry.get("template") or ""
    return name, b


def load_spec(path):
    """Read the --spec JSON: a list of bucket entries (or {"buckets": [...]})."""
    if not path or not path.strip():
        return []
    text = Path(path).expanduser().read_text(encoding="utf-8").strip()
    if not text:
        return []
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("buckets", [])
    return data


def marker_region(lines, start, end):
    """Return (i, j) so lines[i+1:j] is the content between the markers, or None."""
    si = next((k for k, ln in enumerate(lines) if ln.strip() == start), None)
    ei = next((k for k, ln in enumerate(lines) if ln.strip() == end), None)
    if si is None or ei is None or ei < si:
        return None
    return si, ei


# --- CLAUDE.md Wiki Bucket Map table -------------------------------------------------


def table_row(b):
    return f"| `{b['path']}` | {b['scope']} | `{b['filename']}` |"


def edit_table(path, bucket, action):
    lines = path.read_text(encoding="utf-8").splitlines()
    region = marker_region(lines, TABLE_START, TABLE_END)
    if region is None:
        return f"WARN: no BUCKETS markers in {path.name}; skipped table edit"
    si, ei = region
    token = f"`{bucket['path']}`"
    present = next((k for k in range(si + 1, ei) if token in lines[k]), None)
    if action == "add":
        if present is not None:
            return None
        lines.insert(ei, table_row(bucket))
    else:
        if present is None:
            return None
        del lines[present]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return None


# --- index.md sections ---------------------------------------------------------------


def edit_index(path, bucket, action):
    lines = path.read_text(encoding="utf-8").splitlines()
    region = marker_region(lines, SECTIONS_START, SECTIONS_END)
    if region is None:
        return f"WARN: no SECTIONS markers in {path.name}; skipped index edit"
    si, ei = region
    heading = f"## {bucket['index_section']}"
    hi = next((k for k in range(si + 1, ei) if lines[k].strip() == heading), None)
    if action == "add":
        if hi is not None:
            return None
        block = [heading, ""]
        if ei > 0 and lines[ei - 1].strip():  # keep a blank line before the new heading
            block = ["", *block]
        lines[ei:ei] = block
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return None
    # remove: only if the section holds no content
    if hi is None:
        return None
    j = hi + 1
    while j < ei and not lines[j].strip().startswith("## "):
        j += 1
    has_content = any(lines[k].strip() for k in range(hi + 1, j))
    if has_content:
        return f"WARN: index section '{heading}' has content; left in place"
    del lines[hi:j]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return None


# --- .obsidian/graph.json color groups -----------------------------------------------


def edit_graph(path, bucket, action):
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    groups = data.setdefault("colorGroups", [])
    query = f"tag:{bucket['graph_tag']}"
    exists = any(g.get("query") == query for g in groups)
    if action == "add":
        if exists:
            return None
        groups.append({"query": query, "color": bucket["graph_color"]})
    else:
        data["colorGroups"] = [g for g in groups if g.get("query") != query]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return None


# --- wiki dir + template -------------------------------------------------------------


def has_pages(vault, name):
    """True if wiki/<name>/ holds any file other than .gitkeep (recursively)."""
    d = vault / "wiki" / name
    return d.is_dir() and any(p.is_file() and p.name != ".gitkeep" for p in d.rglob("*"))


def edit_files(vault, name, bucket, action):
    notes = []
    bucket_dir = vault / "wiki" / name
    tpl_dst = vault / "wiki" / "_templates" / bucket["template"]
    if action == "add":
        bucket_dir.mkdir(parents=True, exist_ok=True)
        if name == "tasks":
            for fname, seed in (("open.md", TASKS_OPEN_SEED), ("done.md", TASKS_DONE_SEED)):
                if not (bucket_dir / fname).exists():
                    (bucket_dir / fname).write_text(seed, encoding="utf-8")
        elif not any(bucket_dir.iterdir()):
            (bucket_dir / ".gitkeep").touch()
        # Optional buckets carry their template body inline; core templates ship in
        # wiki/_templates/ already, so they carry no body and are left untouched.
        body = bucket.get("template_body")
        if body and not tpl_dst.exists():
            tpl_dst.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
    else:
        # apply() guarantees the bucket has no pages before we get here.
        if tpl_dst.exists():
            tpl_dst.unlink()
        if bucket_dir.is_dir():
            shutil.rmtree(bucket_dir)
    return notes


# --- orchestration -------------------------------------------------------------------


def apply(vault, buckets, action, core):
    claude_md, index_md = vault / "CLAUDE.md", vault / "index.md"
    graph = vault / ".obsidian" / "graph.json"
    done, notes = [], []
    for name, b in buckets.items():
        if action == "remove" and name in core:
            notes.append(f"WARN: '{name}' is a core bucket; cannot remove")
            continue
        if action == "remove" and has_pages(vault, name):
            notes.append(f"WARN: '{name}' has pages; move/delete them first, then re-run. Skipped.")
            continue
        for warn in (
            edit_table(claude_md, b, action),
            edit_index(index_md, b, action),
            edit_graph(graph, b, action),
            *edit_files(vault, name, b, action),
        ):
            if warn:
                notes.append(warn)
        done.append(name)
    return done, notes


def active_buckets(vault):
    """(name, scope) for each row in the CLAUDE.md Wiki Bucket Map, in order."""
    md = vault / "CLAUDE.md"
    if not md.is_file():
        return []
    lines = md.read_text(encoding="utf-8").splitlines()
    region = marker_region(lines, TABLE_START, TABLE_END)
    if region is None:
        return []
    si, ei = region
    out = []
    for ln in (s.strip() for s in lines[si + 1 : ei]):
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 2:
            continue
        name = cells[0].strip("`").strip("/").split("/")[-1]
        out.append((name, cells[1]))
    return out


def split(arg):
    return [s.strip() for s in (arg or "").split(",") if s.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", action="store_true", help="ensure core + spec buckets")
    ap.add_argument("--spec", default="", help="JSON file of optional bucket definitions")
    ap.add_argument("--remove", default="", help="comma list of bucket names to remove")
    ap.add_argument("--vault", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    vault = resolve_vault(args.vault)

    if args.list:
        for name, scope in active_buckets(vault):
            print(f"[x] {name} — {scope}")
        return

    if not (vault / "CLAUDE.md").is_file() or not (vault / "wiki").is_dir():
        print(f"ERROR: {vault} is not a vault (missing CLAUDE.md + wiki/).")
        sys.exit(1)

    core = set(CORE)
    added, removed, notes = [], [], []

    if args.add:
        graph = vault / ".obsidian" / "graph.json"
        used = {c["color"].get("rgb") for c in _existing_groups(graph)}
        used |= {c["graph_color"]["rgb"] for c in CORE.values()}
        buckets = {name: dict(b) for name, b in CORE.items()}  # core always folded in
        for entry in load_spec(args.spec):
            name, b = bucket_from_spec(entry, used)
            buckets[name] = b
        added, na = apply(vault, buckets, "add", core)
        notes += na

    if args.remove:
        names = [n for n in split(args.remove) if n not in core]
        buckets = {n: bucket_from_name(n) for n in names}
        removed, nr = apply(vault, buckets, "remove", core)
        notes += nr

    print(f"VAULT={vault}")
    print(f"ADDED={','.join(added) or '(none)'}")
    print(f"REMOVED={','.join(removed) or '(none)'}")
    for n in notes:
        print(n)


def _existing_groups(graph_path):
    if not graph_path.is_file():
        return []
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    return [g for g in data.get("colorGroups", []) if isinstance(g.get("color"), dict)]


if __name__ == "__main__":
    main()
