#!/usr/bin/env python3
"""Build dist/weekly-planner.zip and dist/weekly-planner.skill from weekly-planner/.

  python3 tools/build.py          rebuild both
  python3 tools/build.py --check  fail if VERSION and SKILL.md disagree, or dist is stale

The zip holds the weekly-planner/ folder (what Claude.ai's Customize > Skills upload expects).
Entries are sorted with fixed timestamps so the same source always gives the same bytes.
"""
import io
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = "weekly-planner"
SRC = ROOT / NAME
SKIP = {"__pycache__", ".DS_Store"}


def files():
    return sorted(p for p in SRC.rglob("*") if p.is_file() and not (set(p.parts) & SKIP) and p.suffix != ".pyc")


def build():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files():
            info = zipfile.ZipInfo(str(pathlib.Path(NAME) / p.relative_to(SRC)), (2026, 1, 1, 0, 0, 0))
            info.external_attr = (0o755 if p.suffix == ".py" else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    return buf.getvalue()


def version_ok():
    v = (SRC / "VERSION").read_text().strip()
    skill = (SRC / "SKILL.md").read_text()
    m = re.search(r"^Version: (\S+)", skill, re.M)
    if not m or m.group(1) != v:
        sys.exit(f"VERSION {v} does not match SKILL.md Version line {m.group(1) if m else 'missing'}")
    if not skill.startswith("---\nname: " + NAME + "\n"):
        sys.exit("SKILL.md frontmatter must start with name: " + NAME)
    return v


def main():
    v = version_ok()
    data = build()
    outs = [ROOT / "dist" / f"{NAME}.zip", ROOT / "dist" / f"{NAME}.skill"]
    if "--check" in sys.argv:
        stale = [o.name for o in outs if not o.exists() or o.read_bytes() != data]
        if stale:
            sys.exit(f"dist is stale: {', '.join(stale)}. Run python3 tools/build.py")
        print(f"ok {v}")
        return
    for o in outs:
        o.parent.mkdir(exist_ok=True)
        o.write_bytes(data)
    print(f"built {v}: {len(files())} files, {len(data)} bytes")


if __name__ == "__main__":
    main()
