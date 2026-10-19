"""Every card on the profile, each rendered for one palette."""
from __future__ import annotations

import re

from glyphs import Style, ellipsize, measure, text, wrap
from icons import icon
from theme import Palette, blossom, chip, eyebrow, falling_petals, frame, svg_doc

BODY = Style("sans", 400, 18)


# ── section header ──────────────────────────────────────────────────────────
def section_header(p: Palette, sec: dict, seed: str) -> str:
    w, h = 1200, 124
    defs, bg, close = frame(p, w, h, rx=18, glow_at=(0.9, 0.5), watermark=sec["mark"], wm_size=160,
                            wm_x=w - 30, wm_y=h / 2 + 58)
    body = [bg,
            blossom(1050, 64, 1.35, 12, p.petal_a, p.center, sway=True),
            blossom(1134, 34, 0.75, -18, p.petal_b, p.center, opacity=0.85),
            falling_petals(p, seed, 700, 1180, h, 7, size=(0.3, 0.5)),
            blossom(62, 62, 1.1, 8, p.petal_b, p.center)]
    num_st = Style("sans", 700, 15, tracking=3)
    body.append(text(sec["num"], 108, 46, num_st, p.accent))
    nw = measure(sec["num"], num_st)
    body.append(f'<rect x="{108 + nw + 10:.1f}" y="39.5" width="20" height="2" rx="1" fill="{p.accent}" opacity=".6"/>')
    body.append(text(sec["jp"], 108 + nw + 40, 47, Style("jp", 500, 17, tracking=2), p.accent))
    title_style = Style("sans", 700, 40, tracking=-0.6)
    body.append(text(sec["en"], 106, 94, title_style, p.title))
    tw = measure(sec["en"], title_style)
    body.append(text(sec["sub"], 106 + tw + 22, 93, Style("sans", 400, 19), p.muted))
    body.append(close)
    return svg_doc(w, h, f'{sec["jp"]} · {sec["en"]}', "\n".join(body), defs)


# ── about: the TypeScript object as a code card ─────────────────────────────
TOKEN = re.compile(r'(?P<str>"[^"]*")|(?P<kw>\b(?:const|as)\b)|(?P<key>\b\w+(?=:))|(?P<word>\w+)|(?P<sp>\s+)|(?P<p>.)')


def about_card(p: Palette, code: dict) -> str:
    lines = code["lines"]
    mono = Style("mono", 400, 18)
    lh = 34
    top = 80
    w = 1200
    h = top + lh * len(lines) + 30
    defs, bg, close = frame(p, w, h, rx=20, glow_at=(0.92, 0.25), watermark="花", wm_size=300,
                            wm_x=w - 20, wm_y=h - 20)
    body = [bg]
    # title bar
    body.append(f'<rect width="{w}" height="56" fill="{p.title}" opacity=".035"/>')
    body.append(f'<rect y="56" width="{w}" height="1" fill="{p.border}" opacity="{p.border_op}"/>')
    for i, col in enumerate((p.accent2, p.accent, p.muted)):
        body.append(f'<circle cx="{32 + i * 22}" cy="28" r="6.5" fill="{col}" opacity=".9"/>')
    tab = Style("mono", 400, 15)
    tw = measure(code["file"], tab)
    body.append(f'<rect x="112" y="13" width="{tw + 58:.0f}" height="43" rx="10" fill="{p.bg0}" opacity=".9"/>')
    body.append(icon("book", 125, 25, 17, p.accent))
    body.append(text(code["file"], 150, 40, tab, p.title))
    body.append(eyebrow("私について · about me", w - 30, 34, p, size=13, anchor="end", color=p.muted))

    colors = {"str": p.accent, "kw": p.accent2, "key": p.title, "word": p.text, "p": p.muted}
    for n, line in enumerate(lines):
        y = top + 20 + n * lh
        body.append(text(str(n + 1), 54, y, Style("mono", 400, 15), p.muted, anchor="end", opacity=0.55))
        x = 80.0
        for m in TOKEN.finditer(line):
            kind = m.lastgroup
            tok = m.group()
            if kind != "sp":
                st = Style("mono", 700, 18) if kind == "kw" else mono
                body.append(text(tok, x, y, st, colors[kind]))
            x += measure(tok, mono)
        if n == len(lines) - 2:  # the motto line gets its blossom back
            body.append(blossom(x + 18, y - 6, 0.42, 10, p.petal_b, p.center))
    body.append(blossom(w - 92, h - 84, 2.0, 8, p.petal_a, p.center, sway=True))
    body.append(blossom(w - 44, h - 168, 0.95, -20, p.petal_b, p.center, opacity=0.9))
    body.append(falling_petals(p, "about", 1050, 1190, h, 6))
    body.append(close)
    return svg_doc(w, h, "const hanahira = { … } — about Hanahira", "\n".join(body), defs)


# ── service / project card ──────────────────────────────────────────────────
CARD_W, CARD_H = 590, 268


def _chips_row(p: Palette, items: list[tuple[str, str | None]], x: float, y: float, max_x: float) -> str:
    out = []
    st = Style("mono", 400, 15)
    for label, ico in items:
        if ico:
            tw = measure(label, st)
            w = tw + 24 + 21
            if x + w > max_x:
                break
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="32" rx="16" fill="{p.chip_bg}"/>')
            out.append(icon(ico, x + 11, y + 7.5, 17, p.chip_fg, 2))
            out.append(text(label, x + 33, y + 21.5, st, p.chip_fg))
        else:
            svg, w = chip(x, y, label, p, style=st, pad=13, h=32)
            if x + w > max_x:
                break
            out.append(svg)
        x += w + 9
    return "".join(out)


def _card_base(p: Palette, mark: str, glow_at=(0.95, 0.05)):
    w, h = CARD_W, CARD_H
    return frame(p, w, h, rx=18, glow_at=glow_at, watermark=mark, wm_size=124, wm_x=w - 22, wm_y=h - 58)


def item_card(p: Palette, *, title: str, host: str, tag: str, icon_name: str, mark: str, desc: str,
              chips: list[tuple[str, str | None]], note: str | None = None) -> str:
    w, h = CARD_W, CARD_H
    defs, bg, close = _card_base(p, mark)
    body = [bg]
    # icon tile
    body.append(f'<rect x="26" y="26" width="62" height="62" rx="17" fill="{p.accent2}"/>')
    body.append(icon(icon_name, 39, 39, 36, p.on_accent, 2))
    # title + host
    title_st = Style("sans", 700, 28, tracking=-0.3)
    host_st = Style("mono", 400, 15)
    # tag top-right
    tag_st = Style("sans", 600, 12, tracking=2.4)
    tw = measure(tag.upper(), tag_st)
    tx = w - 28 - tw
    body.append(f'<rect x="{tx - 30:.1f}" y="27" width="{tw + 44:.1f}" height="28" rx="14" fill="{p.chip_bg}"/>')
    body.append(f'<circle cx="{tx - 14:.1f}" cy="41" r="4.2" fill="{p.accent2}"/>')
    if tag == "live":
        body.append(f'<circle cx="{tx - 14:.1f}" cy="41" r="4.2" fill="none" stroke="{p.accent2}" stroke-width="1.6">'
                    '<animate attributeName="r" values="4.2;9;4.2" dur="2.4s" repeatCount="indefinite"/>'
                    '<animate attributeName="opacity" values=".9;0;.9" dur="2.4s" repeatCount="indefinite"/></circle>')
    body.append(text(tag.upper(), tx, 45.5, tag_st, p.chip_fg))
    body.append(text(ellipsize(title, title_st, tx - 50 - 106), 106, 56, title_st, p.title))
    host_txt = ellipsize(host, host_st, w - 150)
    body.append(text(host_txt, 106, 82, host_st, p.accent))
    if host != "the gateway":
        hw = measure(host_txt, host_st)
        body.append(icon("arrow", 106 + hw + 5, 69, 14, p.accent, 2.2))
    # description (max 3 lines)
    y0 = 136
    if note:
        body.append(text(note, 26, 120, Style("sans", 400, 15), p.muted))
        y0 = 150
    max_lines = 3 if not note else 2
    lines = wrap(desc, BODY, w - 52)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = ellipsize(lines[-1] + " …", BODY, w - 52)
    for i, ln in enumerate(lines):
        body.append(text(ln, 26, y0 + i * 26, BODY, p.text))
    body.append(_chips_row(p, chips, 26, h - 56, w - 90))
    body.append(blossom(w - 46, h - 42, 1.05, 14, p.petal_a, p.center, sway=True))
    body.append(close)
    return svg_doc(w, h, f"{title} — {desc}", "\n".join(body), defs)


def older_card(p: Palette, older: list, user: str) -> str:
    w, h = CARD_W, CARD_H
    defs, bg, close = _card_base(p, "昔", glow_at=(0.1, 0.9))
    body = [bg]
    body.append(f'<rect x="27" y="27" width="60" height="60" rx="17" fill="none" stroke="{p.accent2}" '
                f'stroke-width="1.8" stroke-dasharray="5 5"/>')
    body.append(icon("book", 39, 39, 36, p.accent2, 2))
    body.append(text("From the learning days", 106, 56, Style("sans", 700, 28, tracking=-0.3), p.title))
    body.append(text(f"github.com/{user}", 106, 82, Style("mono", 400, 15), p.accent))
    for i, (name, lang) in enumerate(older):
        y = 140 + i * 38
        body.append(f'<circle cx="34" cy="{y - 6}" r="4.5" fill="{p.accent2}"/>')
        body.append(text(name, 50, y, Style("sans", 600, 20), p.title))
        nw = measure(name, Style("sans", 600, 20))
        body.append(text(lang, 50 + nw + 12, y, Style("mono", 400, 15), p.muted))
    body.append(text("all repositories  →", 26, h - 34, Style("sans", 600, 17), p.accent))
    body.append(blossom(w - 46, h - 42, 1.05, 14, p.petal_a, p.center, sway=True))
    body.append(falling_petals(p, "older", 300, 560, h, 4, size=(0.3, 0.45)))
    body.append(close)
    return svg_doc(w, h, "From the learning days — older repositories", "\n".join(body), defs)


# ── tech stack ──────────────────────────────────────────────────────────────
TIERS = [("#E4739B", "#FFF5F7"), ("#C2637F", "#FFF5F7"), ("#8C5162", "#FFF5F7"), ("#F0A8BC", "#5C2E3E")]


def stack_card(p: Palette, stack: list) -> str:
    w = 1200
    label_w = 240
    chip_st = Style("sans", 600, 17)
    row_h = 84
    h = 30 + row_h * len(stack) + 14
    defs, bg, close = frame(p, w, h, rx=20, glow_at=(0.95, 0.1), watermark="技", wm_size=250,
                            wm_x=w - 20, wm_y=h - 14)
    body = [bg]
    for i, row in enumerate(stack):
        y = 30 + i * row_h
        if i:
            body.append(f'<rect x="30" y="{y - 1}" width="{w - 60}" height="1" fill="{p.border}" '
                        f'opacity="{p.border_op * .8:.2f}"/>')
        fill, fg = TIERS[row["tier"]]
        body.append(f'<rect x="30" y="{y + 20}" width="5" height="44" rx="2.5" fill="{fill}"/>')
        body.append(text(row["jp"], 50, y + 42, Style("jp", 700, 22), p.title))
        body.append(eyebrow(row["en"], 50, y + 62, p, size=11.5, color=p.muted))
        x = 30 + label_w
        for item in row["items"]:
            svg, cw = chip(x, y + 22, item, p, style=chip_st, pad=16, h=40, solid=fill, fg=fg)
            if x + cw > w - 30:
                raise ValueError(f"stack row {row['en']!r} is too wide — split it")
            body.append(svg)
            x += cw + 10
    body.append(falling_petals(p, "stack", 980, 1190, h, 6, size=(0.3, 0.5)))
    body.append(close)
    return svg_doc(w, h, "Tech stack — " + "; ".join(f'{r["en"]}: {", ".join(r["items"])}' for r in stack),
                   "\n".join(body), defs)
