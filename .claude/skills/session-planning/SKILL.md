---
name: session-planning
description: Morning planning — align on the day's tasks, dependency-order them to minimize rework, build a time-blocked schedule, write it to wiki/plans/YYYY-MM-DD.md, and refresh the home.md dashboard. Use during morning setup.
---

# Plan the day

Set up the day during morning planning: decide what to do, order it so the least work gets the most
done, time-block it, and record it.

## Steps

1. **Pull context** — read `home.md` (priorities, open tasks), active `goals/` and `projects/`, open
   action items from recent `meetings/`, and yesterday's `plans/` note for carryover.
2. **Quiz the user** — in small clusters: what's on today's plate, hard commitments (with times),
   available hours, energy and constraints.
3. **Build the task list** — combine carryover + new + goal-driven tasks; give each a rough effort
   estimate.
4. **Dependency-order** — find where one task's output **feeds** another and sequence the feeding
   task first, so the downstream task is done once instead of redone. (E.g. if part of B feeds a task
   in A, do B before A.) Front-load deep-focus work to peak energy; batch shallow/low-context tasks.
   State the ordering rationale in one line.
5. **Time-block** — lay tasks into the day around fixed commitments, with buffers.
6. **Write `wiki/plans/YYYY-MM-DD.md`** from `wiki/_templates/session-plan.md` — top focus, carryover,
   the ordered task list with dependency notes, and the time-blocked schedule.
7. **Refresh `home.md`** — today's top 3 and a schedule summary so the dashboard reflects the day.
8. **Append to `log.md`**: `## [YYYY-MM-DD] session-planning | <focus>`.

## Done when

- A `plans/YYYY-MM-DD.md` note exists with a dependency-ordered, time-blocked schedule; `home.md`
  reflects today's focus; and `log.md` has the entry.
