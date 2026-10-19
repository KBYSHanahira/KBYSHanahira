"""Live numbers: fetched from the GitHub GraphQL API, drawn as sakura cards."""
from __future__ import annotations

import base64
import collections
import datetime as dt
import json
import urllib.request

from glyphs import Style, measure, text
from theme import Palette, blossom, eyebrow, falling_petals, frame, svg_doc

API = "https://api.github.com/graphql"

USER_Q = """
query($login: String!) {
  user(login: $login) {
    id name login createdAt avatarUrl(size: 240)
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection { totalCommitContributions contributionCalendar { totalContributions } }
    repositories(ownerAffiliations: OWNER, first: 100, privacy: PUBLIC) {
      nodes { name isFork stargazerCount forkCount description url
              primaryLanguage { name }
              parent { nameWithOwner }
              defaultBranchRef { name } }
    }
  }
}"""

HISTORY_Q = """
query($owner: String!, $name: String!, $author: ID!, $after: String) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef { target { ... on Commit {
      history(first: 100, after: $after, author: { id: $author }) {
        pageInfo { hasNextPage endCursor }
        nodes { committedDate }
      } } } }
  }
}"""


def _gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": f"bearer {token}", "User-Agent": "sakura-cards"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch(login: str, token: str) -> dict:
    u = _gql(token, USER_Q, {"login": login})["user"]
    hours = [0] * 24
    commits_by_lang: collections.Counter = collections.Counter()
    total_commits = 0
    for repo in u["repositories"]["nodes"]:
        if not repo["defaultBranchRef"]:
            continue
        after = None
        n = 0
        for _ in range(20):  # ≤ 2000 commits per repo is plenty
            h = _gql(token, HISTORY_Q, {"owner": login, "name": repo["name"], "author": u["id"],
                                        "after": after})["repository"]["defaultBranchRef"]["target"]["history"]
            for c in h["nodes"]:
                hours[_local_hour(c["committedDate"])] += 1
                n += 1
            if not h["pageInfo"]["hasNextPage"]:
                break
            after = h["pageInfo"]["endCursor"]
        total_commits += n
        if n and repo["primaryLanguage"]:
            commits_by_lang[repo["primaryLanguage"]["name"]] += n
    avatar = None
    try:
        with urllib.request.urlopen(u["avatarUrl"], timeout=30) as r:
            avatar = "data:" + r.headers.get_content_type() + ";base64," + base64.b64encode(r.read()).decode()
    except Exception as e:  # the cards still render without the photo
        print("avatar:", e)
    repos = {r["name"]: {"stars": r["stargazerCount"], "forks": r["forkCount"],
                         "lang": (r["primaryLanguage"] or {}).get("name"), "desc": r["description"],
                         "parent": (r["parent"] or {}).get("nameWithOwner")}
             for r in u["repositories"]["nodes"]}
    return {
        "login": u["login"], "name": u["name"] or u["login"], "since": u["createdAt"][:4],
        "avatar": avatar,
        "followers": u["followers"]["totalCount"],
        "prs": u["pullRequests"]["totalCount"], "issues": u["issues"]["totalCount"],
        "contrib_year": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "commits_year": u["contributionsCollection"]["totalCommitContributions"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "public_repos": len(u["repositories"]["nodes"]),
        "total_commits": total_commits,
        "hours": hours,
        "langs": commits_by_lang.most_common(),
        "repos": repos,
    }


UTC_OFFSET = 7


def _local_hour(iso: str) -> int:
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (t + dt.timedelta(hours=UTC_OFFSET)).hour


def _fmt(n: int) -> str:
    return f"{n / 1000:.1f}k" if n >= 10000 else f"{n:,}"


# ── overview ────────────────────────────────────────────────────────────────
def overview_card(p: Palette, s: dict, name_jp: str) -> str:
    w, h = 1200, 260
    defs, bg, close = frame(p, w, h, rx=20, glow_at=(0.12, 0.3))
    body = [bg]
    cx, cy, r = 128, 130, 76
    defs += f' <clipPath id="av"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>\n'
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="none" stroke="{p.accent2}" stroke-width="2.5" '
                f'stroke-dasharray="3 7" stroke-linecap="round" opacity=".7"/>')
    if s.get("avatar"):
        body.append(f'<image href="{s["avatar"]}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" '
                    f'clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>')
    else:
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{p.chip_bg}"/>')
        body.append(blossom(cx, cy, 2.4, 0, p.petal_a, p.center))
    body.append(blossom(cx + 52, cy + 50, 0.95, 18, p.petal_b, p.center, sway=True))

    name_st = Style("sans", 800, 44, tracking=-0.8)
    body.append(eyebrow("Hanahira Network", 244, 86, p, size=14))
    body.append(text(s["name"], 241, 136, name_st, p.title))
    nw = measure(s["name"], name_st)
    body.append(text(name_jp, 241 + nw + 14, 133, Style("jp", 500, 28), p.accent))
    body.append(text(f'@{s["login"]} · since {s["since"]}', 244, 170, Style("mono", 400, 16), p.muted))
    body.append(text(f'{_fmt(s["total_commits"])} commits · {s["public_repos"]} public repos',
                     244, 198, Style("sans", 400, 17), p.text))

    metrics = [("Contribs · 1y", s["contrib_year"]), ("Commits · 1y", s["commits_year"]),
               ("Stars earned", s["stars"]), ("Pull requests", s["prs"]),
               ("Issues", s["issues"]), ("Followers", s["followers"])]
    gx, gy, cw, rh = 652, 46, 182, 94
    for i, (label, val) in enumerate(metrics):
        x = gx + (i % 3) * cw
        y = gy + (i // 3) * rh
        body.append(f'<rect x="{x - 18}" y="{y + 6}" width="2.5" height="60" rx="1.25" fill="{p.accent2}" opacity=".55"/>')
        body.append(text(_fmt(val), x, y + 44, Style("sans", 800, 40, tracking=-0.8), p.accent))
        body.append(eyebrow(label, x, y + 66, p, size=11.5, color=p.muted))
    body.append(falling_petals(p, "overview", 380, 1180, h, 8, size=(0.3, 0.5)))
    body.append(close)
    label = (f'{s["name"]} — {s["contrib_year"]} contributions in the last year, {s["stars"]} stars, '
             f'{s["followers"]} followers')
    return svg_doc(w, h, label, "\n".join(body), defs)


def _ramp(p: Palette) -> list[str]:
    if p.mode == "dark":
        return ["#E4739B", "#F7A8BC", "#C2557E", "#FFD6E1", "#8C4F68", "#B9919F", "#6E3A50"]
    return ["#E4739B", "#C2557E", "#F4A3BA", "#8C2F55", "#D98BA5", "#8C6170", "#F3C9D6"]


# ── languages ───────────────────────────────────────────────────────────────
def languages_card(p: Palette, s: dict) -> str:
    w, h = 590, 330
    defs, bg, close = frame(p, w, h, rx=18, glow_at=(0.95, 0.05), watermark="言", wm_size=124,
                            wm_x=w - 22, wm_y=h - 58)
    body = [bg]
    body.append(eyebrow("言語 · by commits", 28, 46, p, size=13))
    body.append(text("Where my commits go", 28, 84, Style("sans", 700, 28, tracking=-0.3), p.title))
    langs = s["langs"][:6]
    total = sum(n for _, n in s["langs"]) or 1
    ramp = _ramp(p)
    x, bw, by = 28.0, w - 56, 112
    defs += f' <clipPath id="bar"><rect x="28" y="{by}" width="{bw}" height="18" rx="9"/></clipPath>\n'
    seg = ['<g clip-path="url(#bar)">', f'<rect x="28" y="{by}" width="{bw}" height="18" fill="{p.track}"/>']
    for i, (lang, n) in enumerate(langs):
        sw = bw * n / total
        seg.append(f'<rect x="{x:.1f}" y="{by}" width="{max(sw - 3, 1):.1f}" height="18" fill="{ramp[i]}"/>')
        x += sw
    seg.append("</g>")
    body.append("".join(seg))
    for i, (lang, n) in enumerate(langs):
        col, row = i % 2, i // 2
        lx, ly = 28 + col * 276, 178 + row * 46
        body.append(f'<rect x="{lx}" y="{ly - 14}" width="15" height="15" rx="4.5" fill="{ramp[i]}"/>')
        body.append(text(lang, lx + 26, ly, Style("sans", 600, 19), p.title))
        pct = f"{100 * n / total:.0f}%"
        body.append(text(pct, lx + 250, ly, Style("mono", 400, 16), p.muted, anchor="end"))
    if not langs:
        body.append(text("no commits found yet", 28, 160, Style("sans", 400, 15), p.muted))
    body.append(blossom(w - 50, 52, 1.05, 14, p.petal_a, p.center, sway=True))
    body.append(close)
    label = "Most-committed languages: " + ", ".join(f"{l} {100 * n / total:.0f}%" for l, n in langs)
    return svg_doc(w, h, label, "\n".join(body), defs)


# ── productive time ─────────────────────────────────────────────────────────
def hours_card(p: Palette, s: dict) -> str:
    w, h = 590, 330
    defs, bg, close = frame(p, w, h, rx=18, glow_at=(0.05, 0.05), watermark="時", wm_size=124,
                            wm_x=w - 22, wm_y=h - 58)
    body = [bg]
    hours = s["hours"]
    peak = max(range(24), key=lambda i: hours[i]) if any(hours) else 0
    body.append(eyebrow(f"時間 · commits by hour · UTC+{UTC_OFFSET}", 28, 46, p, size=13))
    body.append(text(f"Most awake around {peak:02d}:00", 28, 84, Style("sans", 700, 28, tracking=-0.3), p.title))
    top, base = 128, 276
    cw = (w - 56) / 24
    mx = max(hours) or 1
    for g in (0.5, 1.0):
        gy = base - (base - top) * g
        body.append(f'<rect x="28" y="{gy:.1f}" width="{w - 56}" height="1" fill="{p.track}"/>')
    for i, n in enumerate(hours):
        bh = max((base - top) * n / mx, 3 if n else 2)
        x = 28 + i * cw + 2.5
        fill = p.accent2 if i == peak else p.accent
        op = 1 if i == peak else (0.35 + 0.5 * n / mx)
        body.append(f'<rect x="{x:.1f}" y="{base - bh:.1f}" '
                    f'width="{cw - 5:.1f}" height="{bh:.1f}" rx="{min(4, (cw - 5) / 2):.1f}" fill="{fill}" '
                    f'opacity="{op:.2f}"/>')
    if any(hours):
        px = 28 + peak * cw + cw / 2
        ph = (base - top) * hours[peak] / mx
        body.append(blossom(px, base - ph - 14, 0.45, 0, p.petal_a, p.center, sway=True))
    for hr in (0, 6, 12, 18, 23):
        body.append(text(f"{hr:02d}", 28 + hr * cw + cw / 2, base + 28, Style("mono", 400, 15), p.muted,
                         anchor="middle"))
    body.append(close)
    return svg_doc(w, h, f"Commits by hour (UTC+{UTC_OFFSET}); busiest around {peak:02d}:00",
                   "\n".join(body), defs)
