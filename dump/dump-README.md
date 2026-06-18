# dump — raw sources (drop zone)

Drop raw sources here for the agent to ingest: articles, PDFs, transcripts, notes, images.

- **Immutable to the agent** — it reads these, never edits or deletes them (enforced in `.claude/settings.json`).
- Images / attachments go in `assets/`.
- Run **ingest** to fold a source into the `wiki/`.

This folder lives at the vault root (not under `.claude/`) so Obsidian shows it and humans can drop notes in directly.
