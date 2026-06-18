---
name: meeting-recap
description: Capture a meeting or call while it's fresh — quiz the user for attendees, talking points, decisions, and action items, then integrate the recap into the wiki (meeting note + people/orgs/projects/goals), surface action items to home.md, and log it. A targeted, interview-driven ingest. Use right after a call.
---

# Recap a meeting

Capture a just-finished call while it's fresh. This is a **scoped `ingest`** where the source is
the user's memory, drawn out by interview rather than read from a file.

## Steps

1. **Seed (optional).** If a transcript or notes file is sitting in `dump/`, read it first to seed
   sharper questions. Never edit anything in `dump/`.
2. **Quiz the user** — ask in small clusters, one at a time, not all at once. Cover:
   - **Context** — which meeting, when (convert "today"/"this morning" to an absolute date), medium.
   - **Attendees** — names, roles, orgs. Flag who is new vs. already in the wiki.
   - **Talking points** — 3–6 key topics discussed.
   - **Decisions** — what was decided, and why.
   - **Action items** — each with an owner and an absolute due date.
   - **Open questions** — anything left unresolved.
   - **Pivotal extras** — sentiment, risks, or anything that contradicts what the wiki already says.
3. **Write the meeting note** `wiki/meetings/YYYY-MM-DD-slug.md` from `wiki/_templates/meeting.md`.
4. **Integrate (scoped to this meeting).** Create or update the pages it touches — attendee
   `people/`, `organizations/`, `projects/`, `goals/`:
   - Add new facts/decisions; cite back with `[[meetings/<slug>]]`.
   - Prefer updating an existing page over a near-duplicate (check `index.md` first).
   - If it **contradicts** an existing claim, don't overwrite — add a `> [!warning] Contradiction`
     callout linking both and flag it to the user.
   - Bump each touched page's `updated:` to today and add new `[[wikilinks]]`.
5. **Surface action items to `home.md`** under open tasks / next actions, with owners and due dates.
6. **Update `index.md`** — add the meeting and any new pages with one-line summaries.
7. **Append to `log.md`**: `## [YYYY-MM-DD] meeting-recap | <Meeting Title>` with 1–3 bullets listing
   pages created/updated.

## Done when

- A `meetings/` note exists, attendees' `people/` pages and any relevant `projects/`/`goals/` pages
  were updated, action items are reflected in `home.md`, and `index.md` + `log.md` are current.
