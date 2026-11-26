# Weekly nudges (optional)

Offer once, in one line, after the first saved plan: "Want a Monday-morning nudge with today's tasks and a Friday-evening review?" Set up only on a yes, and only if the session has a scheduler. Look for the tools with ToolSearch before deciding none exists.

## The prompts

Monday 8:30 AM, user's local time:
```
Weekly planner check-in: use the weekly-planner skill to show me today's tasks from my
Weekly Planner dashboard (<dashboard URL>) and anything overdue. Keep it to a few lines.
```

Friday 6:30 PM:
```
Weekly planner review: use the weekly-planner skill to review this week on my Weekly
Planner dashboard (<dashboard URL>): numbers first, then the three questions, then
offer to plan next week with the unfinished tasks rolled over.
```

The dashboard URL must be in the prompt: each scheduled run starts fresh.

## Pick a scheduler

| Environment | Tool | Notes |
|---|---|---|
| Claude Code on the web / cloud sessions | `create_trigger` (claude-code-remote) | Cron routine; each run is a new session. |
| Claude Code CLI or desktop | `CronCreate`, or the app's scheduled tasks | Runs while the app or machine is on. |
| Claude.ai / Cowork with scheduled tasks | the scheduled-task tool or Schedule button | Same prompts. |
| None | Tell the user | "Say 'what's on today' or 'review my week' any time." |

Cron (local time): Monday `27 8 * * 1`, Friday `33 18 * * 5`. Use an odd minute so runs don't all start on the hour. Say the times in the user's time zone; if unknown and the scheduler needs one, use UTC and say so.

Before creating, list existing jobs (`list_triggers`, `CronList`) and reuse any that already runs the weekly planner. When they stop using the planner, offer to delete both.
