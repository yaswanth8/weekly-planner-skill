# Sizing a realistic week

## Capacity

Ask for hours a day once, then reuse `meta/settings.capacity`. Convert to minutes per date. Plan to **70%** of each day's minutes: the rest absorbs interruptions, tasks that run long and low-energy evenings. People reliably underestimate how long things take (the planning fallacy); the 30% is not slack, it's the real cost of the plan.

| They say | Capacity per day | Plan up to |
|---|---|---|
| "an hour each evening" | 60 | 42 |
| "2 hours on weekdays, free weekends" | 120 weekdays, ask nothing more, use 180 on Sat/Sun | 84 / 126 |
| "I'm slammed this week" | 30 | 21: one small task a day |
| nothing | 90 weekdays, 120 Sat, 0 Sun | 63 / 84 |

## Goals

- At most **3 goals** in a week. More dilutes all of them; park the rest in `later`.
- Each goal gets a `done_means`: something you can see at the end of the week ("3 runs logged", "PR merged", "chapters 1–6 read"), not a feeling ("be healthier").
- A goal bigger than the week (e.g. "launch my app") gets a this-week slice: "Sign-up page live on staging".

## Tasks

Good tasks are **verb-first, concrete, 15–90 minutes**, and you know when they're done.

| Vague | Realistic tasks |
|---|---|
| Work on portfolio | Pick 3 projects and write one line each (20m) · Write case study for project 1 (60m) · Deploy to Vercel (45m) |
| Get fit | Run 30 min easy (30m) ×3, never two days in a row |
| Study for AWS exam | Watch IAM module, take notes (45m) · Do 20 practice questions on IAM (30m) · Review the wrong answers (20m) |
| Clean up finances | List every subscription from last month's statement (25m) · Cancel the 2 you don't use (15m) |

A task over 90 minutes is split. A task under 15 minutes is merged with a related one, unless it is the first, momentum-building task of a goal.

## Placement

1. Rolled tasks from last week go first, early in the week.
2. Each goal's first task is small and on Monday or Tuesday.
3. Deep or hard tasks come early in the week and first in a day's list; easy ones (admin, reading) later in the week and on tired days.
4. At most 4 tasks a day. The light day (default Friday) gets at most 50% of normal.
5. Spread repeated habits with gaps. If a task depends on another, put it on a later day.

## Self-check before showing the plan

- Every day's minutes ≤ 70% of its capacity; 0-capacity days are empty.
- Every goal has at least one task, and its tasks would actually produce `done_means` if all ticked.
- No task over 90 minutes, none vague.
- One light day exists.

`python3 scripts/week.py check plan.json` checks all of this and prints JSON: `ok`, per-day `planned` vs `limit`, and a `warnings` list. Fix everything before showing.
