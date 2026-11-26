# End-of-week review

Keep it to one message from you, one reply from them, then the new plan. The point is to learn one thing for next week, not to grade the user.

## 1. Lead with the numbers, wins first

```
Week of Nov 23: 8 of 11 tasks done (73%).
✓ Portfolio v2 live: 4/4, it's deployed.
◐ Run 3x: 2/3.
○ Atomic Habits: 2/4 chapters.
Best day: Tuesday (3/3). Thursday slipped (0/2).
```

`python3 scripts/week.py review week.json` prints these figures as JSON (`done`, `total`, `pct`, `goals`, `days`, `unfinished`, `advice`). Without code, count by hand.

Frame misses as information about the plan, never about the person: "Thursday had more than fit" rather than "you didn't do Thursday".

## 2. Three questions, one message

1. What went well, or what are you glad you did?
2. What got in the way?
3. One thing to change next week?

Skip any they already answered. If they reply "just roll it over" or similar, skip the questions entirely. Store their answers in a few words each.

## 3. Rollover rules

| Task state | Next week |
|---|---|
| Unfinished, `rolled` 0 or 1 | Carry with `rolled + 1`, placed first, same goal |
| Unfinished, `rolled` ≥ 2 | Ask: shrink it, put it first on Monday, or drop it. Default if no answer: shrink to a 15–30 min first step |
| Goal dropped or finished | Don't carry its tasks |
| Recurring habit (e.g. a run) | Don't carry the missed instance; the habit is replanned fresh |

Carry at most 4 tasks. If more are unfinished, list them and let the user pick, or carry the 4 tied to goals they keep.

## 4. Adjust the next plan

- Completion < 50%: cut next week's planned minutes by a quarter, or drop to 2 goals.
- 50–90%: keep the same size.
- > 90% two weeks running: allow one more goal or 10% more time.
- Apply their "one thing to change" literally where possible (e.g. "evenings are bad" → move tasks to mornings or weekends).

## 5. Save

On the finished week: `status: "reviewed"`, `review: {done, total, pct, went_well, got_in_way, change, rolled: [task ids], at: ISO time}`. Then write next week's doc with the carried tasks (new ids are fine; keep `rolled`).
