"""Every card on the profile, each rendered for one palette."""
from __future__ import annotations

import re

from glyphs import Style, ellipsize, measure, text, wrap
from icons import icon
from theme import (Palette, barcode, brackets, chamfer, chip, diamond, eyebrow, frame, hazard,
                   motes, readout, reticle, svg_doc, ticks)

BODY = Style("sans", 400, 18)


# ── banner ──────────────────────────────────────────────────────────────────
def header_card(p: Palette, c: dict) -> str:
    w, h = 1200, 300
    defs, bg, close = frame(p, w, h, c=26, glow_at=(0.78, 0.45), watermark=c["display_name_jp"], wm_size=300,
                            wm_x=w - 30, wm_y=h - 6, code=f'OPERATOR FILE // {c["user"].upper()} // REV.{c["rev"]}')
    body = [bg]
    # hazard band slanting across the top-right
    body.append(f'<g transform="translate(760 0) skewX(-30)">{hazard(0, 0, 520, 14, "hzt")}</g>')
    body.append(hazard(0, h - 10, 360, 10, "hzb"))
    # left identity block
    body.append(f'<rect x="56" y="58" width="6" height="150" fill="{p.accent}"/>')
    body.append(readout("// OPERATOR PROFILE · HANAHIRA NETWORK", 82, 74, p, size=12, color=p.accent))
    name_st = Style("sans", 800, 92, tracking=-2)
    body.append(text(c["display_name"].upper(), 78, 160, name_st, p.title))
    nw = measure(c["display_name"].upper(), name_st)
    body.append(text(c["display_name_jp"], 78 + nw + 18, 156, Style("jp", 900, 54), p.accent))
    body.append(text(c["tagline"].upper(), 82, 198, Style("sans", 600, 17, tracking=4), p.text))
    # stat line
    x = 82
    for k, v in c["header_tags"]:
        svg, cw = chip(x, 226, f"{k} {v}", p, style=Style("mono", 700, 12.5, tracking=1), pad=12, h=28,
                       solid=p.accent if k == "STATUS" else p.chip_bg,
                       fg=p.on_accent if k == "STATUS" else p.chip_fg)
        body.append(svg)
        x += cw + 8
    body.append(f'<rect class="blink" x="{x + 6}" y="236" width="9" height="9" fill="{p.accent}"/>')
    # right HUD
    body.append(reticle(980, 150, 74, p))
    body.append(brackets(880, 50, 200, 200, p.title, arm=18, sw=1.5, op=.35))
    body.append(readout("TGT.LOCK", 892, 72, p, size=10.5, color=p.accent))
    body.append(readout("X 0980 / Y 0150", 1068, 240, p, size=10.5, anchor="end"))
    body.append(ticks(1110, 60, 64, p.title, step=8, op=.35))
    body.append(barcode(1110, 84, 64, 26, "hdr", p.title, op=.5))
    body.append(readout("HNW-001", 1174, 128, p, size=10.5, anchor="end", color=p.accent))
    body.append(motes(p, "header", 700, 1180, h, 12))
    body.append(close)
    return svg_doc(w, h, f'{c["display_name"]} {c["display_name_jp"]} — {c["tagline"]}', "\n".join(body), defs)


def footer_card(p: Palette, c: dict) -> str:
    w, h = 1200, 120
    defs, bg, close = frame(p, w, h, c=16, glow_at=(0.5, 1.0), scan=False)
    body = [bg]
    body.append(hazard(0, 0, w, 8, "hzf"))
    body.append(text("ご覧いただきありがとうございます", w / 2, 64, Style("jp", 700, 26, tracking=2), p.title,
                     anchor="middle"))
    body.append(readout("THANKS FOR STOPPING BY  //  END OF TRANSMISSION", w / 2, 94, p, size=12.5,
                        anchor="middle", color=p.accent))
    body.append(diamond(w / 2 - 300, 88, 4, p.accent))
    body.append(diamond(w / 2 + 300, 88, 4, p.accent))
    body.append(barcode(40, 40, 120, 40, "foot", p.title, op=.35))
    body.append(readout(c["user"].upper(), w - 40, 60, p, size=11, anchor="end"))
    body.append(readout("HANAHIRA.DEV", w - 40, 80, p, size=11, anchor="end", color=p.accent))
    body.append(close)
    return svg_doc(w, h, "ご覧いただきありがとうございます — Thanks for stopping by", "\n".join(body), defs)


# ── section header ──────────────────────────────────────────────────────────
def section_header(p: Palette, sec: dict, seed: str) -> str:
    w, h = 1200, 124
    defs, bg, close = frame(p, w, h, c=16, glow_at=(0.92, 0.5), watermark=sec["mark"], wm_size=150,
                            wm_x=w - 150, wm_y=h / 2 + 54, code=f'SEC-{sec["num"]} // {seed.upper()}')
    body = [bg]
    # orange index block
    body.append(f'<path d="{chamfer(0, 0, 118, h, 16, 0)}" fill="{p.accent}"/>')
    body.append(text(sec["num"], 59, 84, Style("sans", 800, 54, tracking=-1.5), p.on_accent, anchor="middle"))
    body.append(f'<rect x="118" y="0" width="5" height="{h}" fill="{p.ink}"/>')
    body.append(hazard(123, 0, 12, h, "hzs"))
    x0 = 162
    body.append(readout(f'// {sec["jp"]}', x0, 40, p, size=13, color=p.accent))
    title_style = Style("sans", 800, 38, tracking=0.5)
    body.append(text(sec["en"].upper(), x0 - 2, 88, title_style, p.title))
    tw = measure(sec["en"].upper(), title_style)
    body.append(f'<rect x="{x0 + tw + 18:.0f}" y="70" width="22" height="2" fill="{p.accent}"/>')
    body.append(text(sec["sub"], x0 + tw + 50, 87, Style("sans", 400, 18), p.muted))
    body.append(reticle(w - 70, h / 2, 30, p, op=.9))
    body.append(barcode(w - 260, 30, 70, 18, seed, p.title, op=.35))
    body.append(motes(p, seed, 800, 1160, h, 6))
    body.append(close)
    return svg_doc(w, h, f'{sec["jp"]} · {sec["en"]}', "\n".join(body), defs)


# ── about: the TypeScript object as a terminal card ─────────────────────────
TOKEN = re.compile(r'(?P<str>"[^"]*")|(?P<kw>\b(?:const|as)\b)|(?P<key>\b\w+(?=:))|(?P<word>\w+)|(?P<sp>\s+)|(?P<p>.)')


def about_card(p: Palette, code: dict) -> str:
    lines = code["lines"]
    mono = Style("mono", 400, 18)
    lh = 34
    top = 82
    w = 1200
    h = top + lh * len(lines) + 34
    defs, bg, close = frame(p, w, h, c=20, glow_at=(0.92, 0.25), watermark="花", wm_size=300,
                            wm_x=w - 20, wm_y=h - 20, code="TERMINAL // READ-ONLY")
    body = [bg]
    # title bar
    body.append(f'<rect width="{w}" height="56" fill="{p.title}" opacity=".04"/>')
    body.append(f'<rect y="56" width="{w}" height="1.5" fill="{p.accent}" opacity=".5"/>')
    body.append(hazard(0, 0, 60, 56, "hzab"))
    tab = Style("mono", 400, 15)
    tw = measure(code["file"], tab)
    body.append(f'<path d="{chamfer(78, 12, tw + 58, 44, 10, 0)}" fill="{p.bg0}"/>')
    body.append(f'<rect x="78" y="54" width="{tw + 58:.0f}" height="3" fill="{p.accent}"/>')
    body.append(icon("book", 91, 24, 17, p.accent))
    body.append(text(code["file"], 116, 39, tab, p.title))
    body.append(eyebrow("私について · about me", w - 30, 34, p, size=13, anchor="end", color=p.muted))

    colors = {"str": p.accent, "kw": p.accent2, "key": p.title, "word": p.text, "p": p.muted}
    body.append(f'<rect x="66" y="{top - 4}" width="1" height="{lh * len(lines)}" fill="{p.accent}" opacity=".35"/>')
    for n, line in enumerate(lines):
        y = top + 20 + n * lh
        body.append(text(f"{n + 1:02d}", 52, y, Style("mono", 400, 14), p.muted, anchor="end", opacity=0.7))
        x = 84.0
        for m in TOKEN.finditer(line):
            kind = m.lastgroup
            tok = m.group()
            if kind != "sp":
                st = Style("mono", 700, 18) if kind == "kw" else mono
                body.append(text(tok, x, y, st, colors[kind]))
            x += measure(tok, mono)
        if n == len(lines) - 1:
            body.append(f'<rect class="blink" x="{x + 8:.0f}" y="{y - 16}" width="11" height="20" fill="{p.accent}"/>')
    body.append(reticle(w - 110, h - 100, 56, p, op=.9))
    body.append(motes(p, "about", 980, 1190, h, 8))
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
            out.append(f'<path d="{chamfer(x, y, w, 32, 8)}" fill="{p.chip_bg}"/>')
            out.append(icon(ico, x + 11, y + 7.5, 17, p.chip_fg, 2))
            out.append(text(label, x + 33, y + 21.5, st, p.chip_fg))
        else:
            svg, w = chip(x, y, label, p, style=st, pad=13, h=32)
            if x + w > max_x:
                break
            out.append(svg)
        x += w + 9
    return "".join(out)


def _card_base(p: Palette, mark: str, code: str, glow_at=(0.95, 0.05)):
    w, h = CARD_W, CARD_H
    return frame(p, w, h, c=18, glow_at=glow_at, watermark=mark, wm_size=124, wm_x=w - 22, wm_y=h - 58,
                 code=code)


def item_card(p: Palette, *, title: str, host: str, tag: str, icon_name: str, mark: str, desc: str,
              chips: list[tuple[str, str | None]], note: str | None = None, code: str = "") -> str:
    w, h = CARD_W, CARD_H
    defs, bg, close = _card_base(p, mark, code)
    body = [bg]
    # icon tile
    body.append(f'<path d="{chamfer(26, 26, 62, 62, 14)}" fill="{p.accent}"/>')
    body.append(icon(icon_name, 39, 39, 36, p.on_accent, 2))
    body.append(brackets(20, 20, 74, 74, p.title, arm=8, sw=1.2, op=.4))
    # tag top-right
    tag_st = Style("mono", 700, 12, tracking=2)
    tw = measure(tag.upper(), tag_st)
    tx = w - 28 - tw
    live = tag == "live"
    body.append(f'<path d="{chamfer(tx - 30, 27, tw + 44, 28, 8)}" fill="{p.accent if live else p.chip_bg}"/>')
    blink = ' class="blink"' if live else ""
    body.append(f'<rect{blink} x="{tx - 19:.1f}" y="37" width="8" height="8" '
                f'fill="{p.on_accent if live else p.accent}"/>')
    body.append(text(tag.upper(), tx, 45.5, tag_st, p.on_accent if live else p.chip_fg))
    # title + host
    title_st = Style("sans", 800, 28, tracking=-0.2)
    host_st = Style("mono", 400, 15)
    body.append(text(ellipsize(title, title_st, tx - 50 - 110), 110, 56, title_st, p.title))
    host_txt = ellipsize(host, host_st, w - 150)
    body.append(text(host_txt, 110, 82, host_st, p.accent))
    if host != "the gateway":
        hw = measure(host_txt, host_st)
        body.append(icon("arrow", 110 + hw + 5, 69, 14, p.accent, 2.2))
    body.append(f'<rect x="26" y="106" width="{w - 52}" height="1" fill="{p.title}" opacity=".12"/>')
    body.append(f'<rect x="26" y="105" width="40" height="3" fill="{p.accent}"/>')
    # description (max 3 lines)
    y0 = 140
    if note:
        body.append(readout(note, 26, 128, p, size=13.5))
        y0 = 156
    max_lines = 3 if not note else 2
    lines = wrap(desc, BODY, w - 52)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = ellipsize(lines[-1] + " …", BODY, w - 52)
    for i, ln in enumerate(lines):
        body.append(text(ln, 26, y0 + i * 26, BODY, p.text))
    body.append(_chips_row(p, chips, 26, h - 58, w - 100))
    body.append(barcode(w - 86, h - 56, 52, 22, title, p.title, op=.35))
    body.append(close)
    return svg_doc(w, h, f"{title} — {desc}", "\n".join(body), defs)


def older_card(p: Palette, older: list, user: str) -> str:
    w, h = CARD_W, CARD_H
    defs, bg, close = _card_base(p, "昔", "ARCHIVE // LEGACY", glow_at=(0.1, 0.9))
    body = [bg]
    body.append(f'<path d="{chamfer(27, 27, 60, 60, 14)}" fill="none" stroke="{p.accent}" '
                f'stroke-width="1.8" stroke-dasharray="5 5"/>')
    body.append(icon("book", 39, 39, 36, p.accent, 2))
    body.append(text("From the learning days", 110, 56, Style("sans", 800, 28, tracking=-0.2), p.title))
    body.append(text(f"github.com/{user}", 110, 82, Style("mono", 400, 15), p.accent))
    body.append(f'<rect x="26" y="106" width="{w - 52}" height="1" fill="{p.title}" opacity=".12"/>')
    body.append(f'<rect x="26" y="105" width="40" height="3" fill="{p.accent}"/>')
    for i, (name, lang) in enumerate(older):
        y = 148 + i * 38
        body.append(diamond(34, y - 6, 5, p.accent))
        body.append(text(name, 50, y, Style("sans", 600, 20), p.title))
        nw = measure(name, Style("sans", 600, 20))
        body.append(text(lang, 50 + nw + 12, y, Style("mono", 400, 15), p.muted))
    body.append(text("ALL REPOSITORIES  →", 26, h - 34, Style("sans", 700, 16, tracking=2), p.accent))
    body.append(motes(p, "older", 300, 560, h, 5))
    body.append(close)
    return svg_doc(w, h, "From the learning days — older repositories", "\n".join(body), defs)


# ── tech stack ──────────────────────────────────────────────────────────────
def _tiers(p: Palette):
    # (fill, text, outline?)
    if p.mode == "dark":
        return [("#FF7A1A", "#0A0A0B", False), ("#FFB070", "#0A0A0B", False),
                ("#F4F1EA", "#0A0A0B", False), ("#FF7A1A", "#FFB070", True)]
    return [("#E8620A", "#FFFFFF", False), ("#111111", "#FFB070", False),
            ("#4A4640", "#F1EFEA", False), ("#E8620A", "#C2500A", True)]


def stack_card(p: Palette, stack: list) -> str:
    w = 1200
    label_w = 240
    chip_st = Style("sans", 600, 17)
    row_h = 84
    h = 30 + row_h * len(stack) + 18
    defs, bg, close = frame(p, w, h, c=20, glow_at=(0.95, 0.1), watermark="技", wm_size=250,
                            wm_x=w - 20, wm_y=h - 14, code="LOADOUT // 4 SLOTS")
    tiers = _tiers(p)
    body = [bg]
    for i, row in enumerate(stack):
        y = 30 + i * row_h
        if i:
            body.append(f'<rect x="30" y="{y - 1}" width="{w - 60}" height="1" fill="{p.title}" opacity=".1"/>')
        fill, fg, outline = tiers[row["tier"]]
        body.append(f'<rect x="30" y="{y + 20}" width="5" height="44" fill="{fill}"/>')
        body.append(readout(f"SLOT-{i + 1:02d}", 50, y + 24, p, size=10.5, color=p.accent))
        body.append(text(row["jp"], 50, y + 50, Style("jp", 700, 22), p.title))
        body.append(eyebrow(row["en"], 50, y + 68, p, size=11, color=p.muted))
        x = 30 + label_w
        for item in row["items"]:
            svg, cw = chip(x, y + 22, item, p, style=chip_st, pad=16, h=40, solid=fill, fg=fg, outline=outline)
            if x + cw > w - 30:
                raise ValueError(f"stack row {row['en']!r} is too wide — split it")
            body.append(svg)
            x += cw + 10
    body.append(motes(p, "stack", 980, 1190, h, 8))
    body.append(close)
    return svg_doc(w, h, "Tech stack — " + "; ".join(f'{r["en"]}: {", ".join(r["items"])}' for r in stack),
                   "\n".join(body), defs)
