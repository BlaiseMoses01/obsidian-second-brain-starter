---
tags: [task]
---

# <Open | Done> Tasks

The `tasks/` bucket is a **rolling list, not one page per task** — a deliberate exception to the
"one subject per page" golden rule. It holds exactly two fixed files:

- `tasks/open.md` — active tasks.
- `tasks/done.md` — completed tasks, moved here with a `— done: YYYY-MM-DD` suffix.

## Tasks

One task per checkbox line. Everything after the task text is optional — omit fields that don't apply.

`- [ ] <task> — requestor: [[people/firstname-lastname]] — due: YYYY-MM-DD — re: [[projects/project-name]] — src: [[sources/slug]]`

- **requestor** — who asked, if anyone (link the `people/` page; a dangling link is fine).
- **due** — absolute date (`YYYY-MM-DD`); convert "next week"/"Friday" before writing.
- **re** — the project/goal the task serves, if any.
- **src** — the `sources/` or `meetings/` page the task came from, if captured via fan-out.
