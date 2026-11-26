#!/usr/bin/env python3
"""Is a newer weekly-planner on GitHub? Reads only the repo's VERSION file (a few bytes).

Usage: python3 check_update.py
Prints one line, only when the installed copy is older:
  UPDATE: weekly-planner <new> is out (you have <old>). Download https://github.com/yaswanth8/weekly-planner-skill/raw/main/dist/weekly-planner.zip and re-upload it in Customize > Skills.
Prints nothing when up to date or offline. Never fails loudly: a version check must not get in the way.
"""
import json
import os
import urllib.request

REPO = "yaswanth8/weekly-planner-skill"
URLS = [
    f"https://raw.githubusercontent.com/{REPO}/main/weekly-planner/VERSION",
    f"https://api.github.com/repos/{REPO}/contents/weekly-planner/VERSION?ref=main",
]
ZIP = f"https://github.com/{REPO}/raw/main/dist/weekly-planner.zip"


def parse(v):
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except ValueError:
        return None


def latest():
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "weekly-planner-skill", "Accept": "application/vnd.github.raw"})
            body = urllib.request.urlopen(req, timeout=5).read(200).decode("utf-8", "replace")
            if body.lstrip().startswith("{"):  # API answered with JSON despite the raw Accept header
                import base64
                body = base64.b64decode(json.loads(body).get("content", "")).decode()
            if parse(body):
                return body.strip()
        except Exception:
            continue
    return None


def main():
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION")
    try:
        installed = open(here).read().strip()
    except OSError:
        return
    new = latest()
    if new and parse(new) > parse(installed):
        print(f"UPDATE: weekly-planner {new} is out (you have {installed}). Download {ZIP} and re-upload it in Customize > Skills.")


if __name__ == "__main__":
    main()
