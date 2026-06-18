#!/usr/bin/env python3
"""Scrape a Claude Code session transcript into a clean markdown digest.

Locates the transcript for a given session id under ~/.claude/projects, strips
tool / thinking / sidechain / slash-command noise, and writes a readable
User/Assistant digest to a staging file. Stdlib only.

Usage:
    scrape_session.py <session_id> [--out PATH] [--projects-dir DIR]
"""

import argparse
import json
import sys
from pathlib import Path


def find_transcript(session_id, projects_dir):
    """Return the top-level transcript path for session_id, or None.

    Subagent transcripts live under <session_id>/subagents/ and are named
    agent-*.jsonl, so matching '<session_id>.jsonl' already excludes them.
    """
    matches = [p for p in projects_dir.rglob(f"{session_id}.jsonl") if "subagents" not in p.parts]
    if not matches:
        return None
    # If somehow more than one, prefer the most recently modified.
    return max(matches, key=lambda p: p.stat().st_mtime)


def text_from_assistant(content):
    """Join the human-readable text blocks of an assistant message."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(p for p in parts if p).strip()
    return ""


def scrape(path):
    """Parse a transcript file into (turns, metadata)."""
    turns = []  # list of (role, text)
    meta = {
        "ai_title": None,
        "cwd": None,
        "slug": None,
        "first_ts": None,
        "last_ts": None,
        "session_id": path.stem,
    }
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                # Tolerate a partially-flushed final line on a live session.
                continue

            ts = rec.get("timestamp")
            if ts:
                meta["first_ts"] = meta["first_ts"] or ts
                meta["last_ts"] = ts
            if rec.get("cwd") and not meta["cwd"]:
                meta["cwd"] = rec["cwd"]
            if rec.get("slug"):
                meta["slug"] = rec["slug"]

            rtype = rec.get("type")
            if rtype == "ai-title" and rec.get("aiTitle"):
                meta["ai_title"] = rec["aiTitle"]
                continue
            if rec.get("isSidechain"):
                continue

            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue

            if rtype == "user":
                content = msg.get("content")
                # Real human turns are plain strings; tool-results arrive as
                # arrays. Tags like <command-name> are system-injected.
                if isinstance(content, str):
                    text = content.strip()
                    if text and not text.startswith("<"):
                        turns.append(("user", text))
            elif rtype == "assistant":
                text = text_from_assistant(msg.get("content"))
                if text:
                    turns.append(("assistant", text))

    return turns, meta


def render(turns, meta):
    title = meta["ai_title"] or meta["slug"] or meta["session_id"]
    date = (meta["last_ts"] or "")[:10]
    lines = [
        f"# Session transcript: {title}",
        "",
        f"- date: {date}",
        f"- cwd: {meta['cwd'] or 'unknown'}",
        f"- slug: {meta['slug'] or ''}",
        f"- session_id: {meta['session_id']}",
        f"- turns: {len(turns)}",
        "",
        "---",
        "",
    ]
    for role, text in turns:
        lines.append(f"## {role.capitalize()}")
        lines.append("")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Scrape a Claude session transcript.")
    ap.add_argument("session_id")
    ap.add_argument("--out", help="staging file path (default: /tmp/claude-session-<id>.md)")
    ap.add_argument(
        "--projects-dir",
        default=str(Path.home() / ".claude" / "projects"),
        help="root of Claude project transcripts",
    )
    args = ap.parse_args()

    projects_dir = Path(args.projects_dir)
    if not projects_dir.is_dir():
        sys.exit(f"ERROR: projects dir not found: {projects_dir}")

    transcript = find_transcript(args.session_id, projects_dir)
    if transcript is None:
        sys.exit(f"ERROR: no transcript found for session id {args.session_id} under {projects_dir}")

    turns, meta = scrape(transcript)
    if not turns:
        sys.exit(f"ERROR: transcript {transcript} produced no conversation turns")

    out = Path(args.out) if args.out else Path("/tmp") / f"claude-session-{meta['session_id']}.md"
    out.write_text(render(turns, meta), encoding="utf-8")

    title = meta["ai_title"] or meta["slug"] or meta["session_id"]
    print(f"STAGING_FILE={out}")
    print(f"TITLE={title}")
    print(f"DATE={(meta['last_ts'] or '')[:10]}")
    print(f"CWD={meta['cwd'] or 'unknown'}")
    print(f"SLUG={meta['slug'] or ''}")
    print(f"TURNS={len(turns)}")


if __name__ == "__main__":
    main()
