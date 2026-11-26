# Changelog

## 1.0.0 (2026-11-26)
- `/weekly-planner <goals>`: turns up to 3 goals into a day-by-day checklist sized to 70% of the time you have, with verb-first 15–90 minute tasks, a light buffer day and at most 4 tasks a day.
- At most two questions (time per day, and what "done" means for a vague goal), with sensible defaults.
- Weekly Planner dashboard artifact: goals with progress, seven day cards, tick, add and remove tasks; Claude reads the ticks.
- Day-to-day check-ins ("what's on today", "I did X") and re-flowing a week that slipped.
- End-of-week review: numbers first, three short questions, rollover of unfinished tasks (a task carried twice gets shrink / first / drop), and next week sized from how this one went.
- `scripts/week.py` (`new`, `check`, `review`), optional Monday and Friday nudges, and a once-per-chat update check.
