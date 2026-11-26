---
name: weekly-planner
description: Turns the user's goals for the week into a realistic day-by-day checklist sized to the time they actually have, tracks what gets done on a private Weekly Planner dashboard, and runs a short end-of-week review that rolls unfinished tasks into next week. Use whenever the user wants to plan their week, set weekly goals, make a weekly to-do list or schedule, check off or update this week's tasks, asks "what should I do today", "how's my week going", wants a weekly review or retro, or wants to carry over what didn't get done, even if they never say "weekly planner". Not for one-off reminders, calendar booking or long-term (quarterly, yearly) planning.
---

# Weekly Planner

Version: 1.0.0 · Source and updates: https://github.com/yaswanth8/weekly-planner-skill

Turn a few goals into a week the user can actually finish, keep the checklist where they can tick it, and close the week with a short review that carries forward what's left.

Two rules shape everything:
- **Realistic beats ambitious.** Fill at most 70% of the time they say they have. A plan they finish builds momentum; a plan they abandon on Wednesday teaches them planning doesn't work.
- **Ask little.** At most one round of questions, only for what you can't infer. Defaults are fine.

**Update check** (once per conversation, a few bytes): with code, run `python3 scripts/check_update.py`; without code, fetch `https://raw.githubusercontent.com/yaswanth8/weekly-planner-skill/main/weekly-planner/VERSION`. If it is higher than the Version line above, end your reply with one line: "A newer Weekly Planner (vX.Y.Z) is out: download https://github.com/yaswanth8/weekly-planner-skill/raw/main/dist/weekly-planner.zip and re-upload it in Customize → Skills." If the check fails, say nothing about it.

## Quick start

`/weekly-planner <goals>`: treat the text as this week's goals, ask only what section 2 allows, build the plan (section 3), save it (section 4).

## 1. What do they want?

Decide without asking:
- **Plan** (default): goals, "plan my week", "help me get X done this week". Sections 2–4.
- **Today / check-in**: "what's on today", "I finished X", "mark Y done", "how's my week going". Section 5.
- **Review**: "review my week", "weekly retro", "what didn't I finish", or it's Friday evening to Sunday and they ask about the week. Section 6, which also plans next week.
- **Change**: add, move, drop or swap a task or goal. Section 5.

Which week: from Monday to Sunday. Planning on Friday to Sunday means next week unless they say "this week"; planning mid-week covers the days left (today included), never past days.

## 2. Ask only if you must

One message, at most two questions (AskUserQuestion when it exists), skipping any the request already answers:
1. **How much time?** "About how many hours a day can you give these goals, and any days off?" Skip if they said it. If they don't answer, assume 1.5 hours on weekdays, 2 on Saturday, Sunday off, and say so in one line.
2. **What does done look like?** Only for a goal too vague to cut into tasks ("get fit", "work on my startup"). Offer a concrete reading: "For 'get fit', is it three 30-minute runs?"

More than 3 goals: ask them to pick the top 3 for this week and park the rest in a "Later" list. Never ask about tools, formats or reminders.

## 3. Build the plan

Read `references/planning.md` for the sizing rules and examples before the first plan in a conversation. The short version:

1. **Capacity**: minutes per day for these goals, then plan to **70%** of it. A day with 0 minutes gets nothing.
2. **Cut each goal into tasks** of 15–90 minutes, each starting with a verb and small enough that "done" is obvious ("Draft the 3 hero lines", not "Work on website"). Give each a minute estimate.
3. **Place them**: the first task of each goal early in the week and small, to start momentum; hard or deep work earlier in the day list and earlier in the week; at most 4 tasks a day; keep one day light as a buffer (Friday by default); recurring habits ("run 3x") spread with a rest day between.
4. **Check it**: with code, write the plan JSON (shape in section 4) and run `python3 scripts/week.py check plan.json`. Fix every `over` day and every `warn` before showing it. Without code, add up each day's minutes by hand against 70% of capacity.

**Show the plan** in one compact message: one line per goal with its done-means, then each day with its tasks as checkboxes and minutes, then a single line of totals ("9 tasks, 6 h 15 m of your 10 h"). Example:

```
Week of Nov 30. Goals: 1) Portfolio v2 live (deployed, 3 projects)  2) Run 3x  3) Finish "Atomic Habits"

Mon (60 of 90 min)  - [ ] Pick the 3 projects and write one line each (20m) - [ ] Run 30 min easy (30m) ...
Tue (75 of 90 min)  ...
Fri (light: 30 min) - [ ] Read ch. 15–16 (30m)

10 tasks · 6 h 40 m planned of 9 h 30 m free. Friday is the buffer.
```

End with one line: "Want changes, or shall I save it?" unless they already asked you to save or track it, then save straight away.

## 4. Save the plan

Pick the richest option the session has, quietly:

**A. Dashboard** (Claude with artifacts that can save data): one **Weekly Planner** artifact holds every week. Find it first (Artifact tool `action: "list"`, title "Weekly Planner"); if none, publish `assets/weekly-planner.html` unchanged with `capabilities: {"db": {}, "user": {}}` and icon `calendar`. Write the week with the ArtifactData tool to `weeks/<ISO week>`, e.g. `weeks/2026-W49`:

```json
{"week": "2026-W49", "start": "2026-11-30", "end": "2026-12-06", "status": "active",
 "capacity": {"2026-11-30": 90, "2026-12-01": 90, "2026-12-02": 90, "2026-12-03": 90, "2026-12-04": 90, "2026-12-05": 120, "2026-12-06": 0},
 "goals": [{"id": "g1", "title": "Portfolio v2 live", "done_means": "Deployed with 3 projects"}],
 "tasks": [{"id": "t1", "goal": "g1", "day": "2026-11-30", "text": "Pick the 3 projects and write one line each", "mins": 20, "done": false, "rolled": 0}],
 "later": ["Learn Rust"], "review": null, "updated": "2026-11-29T18:00:00Z"}
```

With code, `python3 scripts/week.py new --start 2026-11-30` prints an empty week with dates and default capacity to fill in. Task ids are unique within the week; `rolled` counts how many weeks a task has been carried; mark repeated habit instances (each run of "run 3x") `"recurring": true` so a missed one is not carried over. Settings live in `meta/settings`: `{"capacity": {"mon": 90, ...}, "tz": "America/New_York"}`; save what the user told you there so next week needs no question. Tell the user the dashboard link in one line: they can tick tasks there and you will see it.

**B. No dashboard**: the plan message itself is the checklist. Add one line: "Paste this back any time and tell me what's done, and I'll update it." On the next message, parse the ticks they send.

**Schedule** (optional, offer once in one line, only if the session has a scheduler): a Monday morning "today's tasks" nudge and a Friday evening review. See `references/scheduling.md`.

## 5. Day to day

Load the current week (`ArtifactData get weeks/<ISO week>`, or the pasted list).

- **"What's on today?"**: today's unchecked tasks, then any overdue unchecked ones from earlier days (at most 3, oldest first) with "move to today?". Nothing more.
- **"I did X"**: match it to a task (by meaning, not exact words), set `done: true` and `doneAt`, and reply with one encouraging line plus what's next. If it matches nothing, add it as a done task under its goal: unplanned wins count.
- **Behind schedule**: when two or more past days have unchecked tasks, offer to **re-flow** the rest of the week: move overdue tasks onto remaining days within 70% capacity, and if they don't fit, name the one or two tasks to drop or shrink. Never silently pile them onto today.
- **Add / move / drop**: change the week doc with `update` on `tasks` (send the whole array) and confirm in one line. Run `week.py check` again after a move if you can.
- **"How's my week going?"**: one line: done / total tasks, per goal progress, and the single next most useful task.

Write back with `ArtifactData update` (the user may tick on the dashboard at the same time, so read, change, write, in that order, right away).

## 6. End-of-week review

Short and kind, about 2 minutes for the user. Read `references/review.md` for the questions and rollover rules. In brief:

1. **Numbers**: with code, `python3 scripts/week.py review week.json` (done %, per goal, per day, unfinished list, rollover advice). Lead with what got done.
2. **Three questions**, in one message: what went well, what got in the way, one thing to change next week. Skip any they already answered. If they don't want to reflect, skip to 3.
3. **Rollover**: unfinished tasks move to next week with `rolled + 1`. A task that has already rolled twice gets a choice instead: shrink it, schedule it first thing Monday, or drop it. Don't roll a task whose goal they've dropped.
4. **Save** the review on the week (`review: {done, total, pct, went_well, got_in_way, change, rolled: [...ids], at}`, `status: "reviewed"`) and go straight into planning next week (section 3), with rolled tasks placed first and the "change" applied (e.g. less capacity if they over-planned).

If completion was under 50%, the next plan is smaller: cut planned minutes by a quarter. Over 90% two weeks running: they may add a goal or 10% more time.

## Files

| File | When |
|---|---|
| `references/planning.md` | before the first plan in a conversation |
| `references/review.md` | end-of-week review |
| `references/scheduling.md` | setting up weekly nudges |
| `scripts/week.py` | `new`, `check` and `review` (code-capable sessions) |
| `scripts/check_update.py` | once-per-chat update check |
| `assets/weekly-planner.html` | first dashboard publish |
