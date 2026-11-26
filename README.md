# Weekly planner: a Claude skill

Version 1.0.0 · [Changelog](CHANGELOG.md)

Tell Claude what you want to get done this week. It turns your goals into a realistic day-by-day checklist sized to the time you actually have, keeps it on a dashboard you can tick, and closes the week with a two-minute review that carries forward what's left.

```
/weekly-planner ship my portfolio, run 3 times, finish Atomic Habits. About 90 minutes a day, Sundays off.
what's on today?
I finished the case study
review my week
```

It asks at most two quick questions, and only when it needs them: how much time you have, and what "done" means for a vague goal.

## What you get

```
Week of Nov 30. Goals: 1) Portfolio v2 live (deployed, 3 projects)  2) Run 3x  3) Finish "Atomic Habits"

Mon (60 of 90 min)  - [ ] Pick the 3 projects and write one line each (20m)  - [ ] Run 30 min easy (30m)
Tue (60 of 90 min)  - [ ] Write case study for project 1 (60m)
...
Fri (light: 30 min) - [ ] Read ch. 15–16 (30m)

10 tasks · 6 h 40 m planned of 9 h 30 m free. Friday is the buffer.
```

- **Realistic by design.** It plans only 70% of the time you say you have, keeps to 3 goals, cuts work into verb-first 15–90 minute tasks, puts at most 4 on a day and leaves one light day as a buffer.
- **A dashboard you can tick.** On plans with artifacts, your week lives on a private **Weekly Planner** page: goals with progress bars, seven day cards, today highlighted. Tick, add or remove tasks there and Claude sees it.
- **Day to day.** "What's on today?", "I did X", "move Thursday's task", and if the week slips, it re-flows what's left instead of piling it all on today.
- **End-of-week review.** Numbers and wins first, three short questions, then unfinished tasks roll into next week. A task that has slipped twice gets a choice: shrink it, do it first, or drop it. Next week is sized from how this one went.
- **Works on every Claude plan.** Without artifacts the plan is a checklist you paste back; without code Claude does the sums by hand.

## Install

- **Claude.ai, any plan**:
  1. Download [`dist/weekly-planner.zip`](dist/weekly-planner.zip) (or the latest [release](../../releases)).
  2. In Settings → Capabilities, turn on **Code execution and file creation** (called **Create and edit files** in newer layouts).
  3. Upload the zip in **Customize → Skills**.
- **Claude Code**: copy the `weekly-planner/` folder into `~/.claude/skills/`.

## Inside

```
weekly-planner/
├── SKILL.md                      the workflow: questions, planning, saving, check-ins, review
├── assets/weekly-planner.html    the dashboard (an artifact with a small database)
├── scripts/week.py               new week skeleton, plan check (capacity, sizing), week review stats
├── scripts/check_update.py       tells you when a newer version is on GitHub
├── VERSION                       the installed version
└── references/
    ├── planning.md               sizing rules and examples (loaded when planning)
    ├── review.md                 review questions and rollover rules (loaded at review)
    └── scheduling.md             optional Monday and Friday nudges
evals/evals.json                  test prompts with expected behaviour
tools/build.py                    builds dist/ and checks it matches the source
```

## Updates

Once per chat the skill reads this repo's `weekly-planner/VERSION` file (a few bytes). If a newer version is out, it adds one line to its reply with the download link; re-upload the new zip to update. Nothing else is sent anywhere, and your plans stay in your own Claude account.

## Developing

Edit `weekly-planner/`, bump `VERSION`, the `Version:` line in `SKILL.md` and `CHANGELOG.md`, then run `python3 tools/build.py` and commit `dist/`. `python3 tools/build.py --check` fails if they disagree.

## License

MIT
