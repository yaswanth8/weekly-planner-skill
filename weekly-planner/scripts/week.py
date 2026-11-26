#!/usr/bin/env python3
"""Weekly planner helper: make an empty week, check a plan is realistic, review a finished week.

Usage:
  python3 week.py new --start 2026-11-30 [--settings settings.json] [--from last_week.json]
      Prints an empty week doc for the Monday-to-Sunday week containing --start (or the days
      left in it, if --start is mid-week). Capacity comes from settings.json's
      {"capacity": {"mon": 90, ...}} or the defaults. With --from, unfinished tasks of last week
      are carried over (rolled + 1), except recurring ones and those whose goal is gone.
  python3 week.py check plan.json [--ratio 0.7]
      Checks each day's planned minutes against ratio x capacity, and flags vague, oversized,
      too-many-a-day and goal-without-task problems. Exit 0 always; read "ok".
  python3 week.py review week.json
      Done/total, per goal, per day, the unfinished list and rollover advice.

All output is JSON on stdout. Standard library only.
"""
import argparse
import datetime as dt
import json
import sys

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DEFAULT_CAPACITY = {"mon": 90, "tue": 90, "wed": 90, "thu": 90, "fri": 90, "sat": 120, "sun": 0}
MAX_TASK, MIN_TASK, MAX_PER_DAY = 90, 15, 4
VAGUE = ("work on", "continue", "keep going", "deal with", "look into", "stuff", "misc", "things")


def load(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def week_bounds(day):
    monday = day - dt.timedelta(days=day.weekday())
    return monday, monday + dt.timedelta(days=6)


def iso_week(day):
    y, w, _ = day.isocalendar()
    return f"{y}-W{w:02d}"


def cmd_new(a):
    start = dt.date.fromisoformat(a.start)
    monday, sunday = week_bounds(start)
    cap = {**DEFAULT_CAPACITY, **(load(a.settings).get("capacity") or {})}
    capacity = {}
    d = monday
    while d <= sunday:
        capacity[d.isoformat()] = 0 if d < start else int(cap[DAYS[d.weekday()]])
        d += dt.timedelta(days=1)
    doc = {"week": iso_week(monday), "start": monday.isoformat(), "end": sunday.isoformat(),
           "status": "active", "capacity": capacity, "goals": [], "tasks": [], "later": [],
           "review": None}
    if a.prev:
        prev = load(a.prev)
        goals = prev.get("goals", [])
        doc["goals"] = goals
        doc["later"] = prev.get("later", [])
        keep = {g.get("id") for g in goals if not g.get("dropped") and not g.get("done")}
        carried = []
        for t in prev.get("tasks", []):
            if t.get("done") or t.get("recurring") or t.get("goal") not in keep:
                continue
            carried.append({**t, "id": f"r{len(carried) + 1}", "day": None, "done": False,
                            "doneAt": None, "rolled": int(t.get("rolled", 0)) + 1})
        doc["tasks"] = carried
        doc["needs_decision"] = [t["id"] for t in carried if t["rolled"] >= 3]
    print(json.dumps(doc, indent=2))


def cmd_check(a):
    plan = load(a.plan)
    capacity = plan.get("capacity") or {}
    tasks = plan.get("tasks") or []
    goals = plan.get("goals") or []
    warnings, days = [], {}
    for date, mins in sorted(capacity.items()):
        days[date] = {"capacity": int(mins or 0), "limit": int((mins or 0) * a.ratio), "planned": 0, "count": 0}
    ids = set()
    for t in tasks:
        tid, text, mins = t.get("id"), (t.get("text") or "").strip(), t.get("mins")
        if tid in ids:
            warnings.append(f"duplicate task id {tid}")
        ids.add(tid)
        if not text:
            warnings.append(f"{tid}: no text")
        elif any(v in text.lower() for v in VAGUE) or len(text.split()) < 2:
            warnings.append(f"{tid}: vague, make it a concrete verb-first step: \"{text}\"")
        if not isinstance(mins, (int, float)) or mins <= 0:
            warnings.append(f"{tid}: no minute estimate")
            mins = 0
        elif mins > MAX_TASK:
            warnings.append(f"{tid}: {mins} min, split into pieces of {MAX_TASK} or less")
        day = t.get("day")
        if day is None:
            warnings.append(f"{tid}: not placed on a day")
            continue
        if day not in days:
            warnings.append(f"{tid}: day {day} is outside this week")
            continue
        if not t.get("done"):
            days[day]["planned"] += mins
        days[day]["count"] += 1
    for date, d in days.items():
        d["over"] = d["planned"] > d["limit"]
        if d["capacity"] == 0 and d["count"]:
            warnings.append(f"{date}: day off but has {d['count']} task(s)")
        elif d["over"]:
            warnings.append(f"{date}: {d['planned']} min planned, limit {d['limit']} ({int(a.ratio * 100)}% of {d['capacity']})")
        if d["count"] > MAX_PER_DAY:
            warnings.append(f"{date}: {d['count']} tasks, keep it to {MAX_PER_DAY}")
    for g in goals:
        if not any(t.get("goal") == g.get("id") for t in tasks):
            warnings.append(f"goal {g.get('id')} \"{g.get('title')}\" has no tasks")
    if len(goals) > 3:
        warnings.append(f"{len(goals)} goals: keep 3 and park the rest in later")
    workdays = [d for d in days.values() if d["capacity"] > 0]
    if len(workdays) >= 4 and all(d["planned"] > d["limit"] * 0.5 for d in workdays):
        warnings.append("no light day: leave one day at half load or less as a buffer")
    total_planned = sum(d["planned"] for d in days.values())
    total_cap = sum(d["capacity"] for d in days.values())
    print(json.dumps({"ok": not warnings, "planned": total_planned, "capacity": total_cap,
                      "days": days, "warnings": warnings}, indent=2))


def cmd_review(a):
    week = load(a.week)
    tasks = week.get("tasks") or []
    goals = week.get("goals") or []
    done = [t for t in tasks if t.get("done")]
    total = len(tasks)
    pct = round(100 * len(done) / total) if total else 0
    per_goal = []
    for g in goals:
        gt = [t for t in tasks if t.get("goal") == g.get("id")]
        per_goal.append({"id": g.get("id"), "title": g.get("title"), "done": sum(1 for t in gt if t.get("done")), "total": len(gt)})
    per_day = {}
    for t in tasks:
        d = per_day.setdefault(t.get("day") or "unplaced", {"done": 0, "total": 0})
        d["total"] += 1
        d["done"] += 1 if t.get("done") else 0
    unfinished = [{"id": t.get("id"), "text": t.get("text"), "goal": t.get("goal"), "rolled": int(t.get("rolled", 0)),
                   "action": "decide: shrink, first on Monday, or drop" if int(t.get("rolled", 0)) >= 2 else "carry"}
                  for t in tasks if not t.get("done")]
    if not total:
        advice = "Nothing was planned this week."
    elif pct < 50:
        advice = "Under half done: plan about a quarter fewer minutes next week, or keep 2 goals."
    elif pct > 90:
        advice = "Over 90% done: keep the same size; if this repeats next week, add a goal or 10% more time."
    else:
        advice = "A realistic week: keep the same size."
    if len(unfinished) > 4:
        advice += f" {len(unfinished)} unfinished: carry at most 4, let the user pick."
    worked = [(d, v) for d, v in per_day.items() if d != "unplaced" and v["total"]]
    best = max(worked, key=lambda kv: (kv[1]["done"] / kv[1]["total"], kv[1]["done"]), default=(None, None))[0]
    worst = min(worked, key=lambda kv: (kv[1]["done"] / kv[1]["total"], -kv[1]["total"]), default=(None, None))[0]
    print(json.dumps({"week": week.get("week"), "done": len(done), "total": total, "pct": pct,
                      "goals": per_goal, "days": dict(sorted(per_day.items())), "best_day": best,
                      "hardest_day": worst if worst != best else None, "unfinished": unfinished,
                      "advice": advice}, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--start", default=dt.date.today().isoformat())
    n.add_argument("--settings")
    n.add_argument("--from", dest="prev")
    c = sub.add_parser("check")
    c.add_argument("plan")
    c.add_argument("--ratio", type=float, default=0.7)
    r = sub.add_parser("review")
    r.add_argument("week")
    a = p.parse_args()
    try:
        {"new": cmd_new, "check": cmd_check, "review": cmd_review}[a.cmd](a)
    except (OSError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
