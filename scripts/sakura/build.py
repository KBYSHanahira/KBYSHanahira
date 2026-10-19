#!/usr/bin/env python3
"""Build every sakura card in assets/sakura/{dark,light}/.

    python scripts/sakura/build.py             # fetch live stats (needs GITHUB_TOKEN)
    python scripts/sakura/build.py --offline   # reuse scripts/sakura/data/stats.json

Edit content.json to change text; run subset_fonts.py first if you add
characters the bundled fonts don't have (the build tells you which).
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cards  # noqa: E402
import stats  # noqa: E402
from theme import PALETTES  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "assets", "sakura")
CACHE = os.path.join(HERE, "data", "stats.json")


def write(mode: str, name: str, svg: str) -> None:
    d = os.path.join(OUT, mode)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
        fh.write(svg)


def load_stats(c: dict, offline: bool) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not offline and token:
        try:
            s = stats.fetch(c["user"], token)
        except Exception as e:  # keep yesterday's numbers rather than breaking the profile
            print(f"::warning::live stats unavailable, reusing the cache: {e}", file=sys.stderr)
        else:
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            with open(CACHE, "w", encoding="utf-8") as fh:
                json.dump(s, fh, ensure_ascii=False, indent=1)
            return s
    if not offline and not token:
        print("GITHUB_TOKEN not set — using cached stats", file=sys.stderr)
    with open(CACHE, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    with open(os.path.join(HERE, "content.json"), encoding="utf-8") as fh:
        c = json.load(fh)
    stats.UTC_OFFSET = c.get("utc_offset", 0)
    s = load_stats(c, "--offline" in sys.argv)

    for p in PALETTES:
        m = p.mode
        for key, sec in c["sections"].items():
            write(m, f"section-{key}.svg", cards.section_header(p, sec, seed=key))
        write(m, "about.svg", cards.about_card(p, c["about_code"]))
        for svc in c["services"]:
            write(m, f'service-{svc["id"]}.svg', cards.item_card(
                p, title=svc["name"], host=svc["host"], tag=svc["tag"], icon_name=svc["icon"],
                mark=svc["mark"], desc=svc["desc"], chips=[(t, None) for t in svc["tech"]]))
        for prj in c["projects"]:
            live = s["repos"].get(prj["repo"], {})
            chips = [(prj.get("lang") or live.get("lang") or "—", None),
                     (f'{live.get("stars", 0)}', "star"), (f'{live.get("forks", 0)}', "fork")]
            fork_of = prj.get("fork_of") or live.get("parent")
            write(m, f'project-{prj["repo"]}.svg', cards.item_card(
                p, title=prj["repo"], host=f'{c["user"]}/{prj["repo"]}', tag="fork" if fork_of else "original",
                icon_name=prj["icon"], mark=prj["mark"], desc=prj["desc"] or live.get("desc") or "",
                chips=chips, note=f"fork of {fork_of}" if fork_of else None))
        write(m, "project-older.svg", cards.older_card(p, c["older"], c["user"]))
        write(m, "stack.svg", cards.stack_card(p, c["stack"]))
        write(m, "stats-overview.svg", stats.overview_card(p, s, c["display_name_jp"]))
        write(m, "stats-languages.svg", stats.languages_card(p, s))
        write(m, "stats-hours.svg", stats.hours_card(p, s))
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "cards →", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
