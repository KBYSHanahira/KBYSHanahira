"""Sakura theme shared by every card: palettes, blossoms, falling petals, frames.

The palettes are lifted from assets/header-*.svg so new cards sit next to the
banner without a seam.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from glyphs import Style, measure, text


@dataclass(frozen=True)
class Palette:
    mode: str
    bg0: str
    bg1: str
    glow: str
    glow_op: float
    border: str
    border_op: float
    title: str      # strongest text
    text: str       # body text
    muted: str      # secondary text
    accent: str     # pink used for eyebrows / numbers
    accent2: str    # deeper pink
    petal_a: str
    petal_b: str
    center: str     # blossom stamens
    water: str      # watermark kanji
    chip_bg: str
    chip_fg: str
    track: str      # empty bar / grid lines
    on_accent: str  # text placed on a solid accent fill


DARK = Palette(
    mode="dark", bg0="#140C11", bg1="#26131D", glow="#E4739B", glow_op=0.30,
    border="#E4739B", border_op=0.22, title="#FFF5F7", text="#E8CFD8", muted="#B9919F",
    accent="#F7A8BC", accent2="#E4739B", petal_a="#F7A8BC", petal_b="#E4739B",
    center="#8C2F55", water="#E4739B", chip_bg="#3A1B2A", chip_fg="#F7A8BC",
    track="#3A2230", on_accent="#2A0F1C",
)
LIGHT = Palette(
    mode="light", bg0="#FFF7F9", bg1="#FBE1E9", glow="#F7A8BC", glow_op=0.45,
    border="#C2557E", border_op=0.20, title="#3B1F2B", text="#5A3443", muted="#8C6170",
    accent="#C2557E", accent2="#E4739B", petal_a="#F4A3BA", petal_b="#E4739B",
    center="#B3325C", water="#C2557E", chip_bg="#FBD3DF", chip_fg="#8C2F55",
    track="#F3C9D6", on_accent="#FFF5F7",
)
PALETTES = (DARK, LIGHT)

PETAL = "M0 0C-9-6-12-19-6-29L0-25L6-29C12-19 9-6 0 0Z"

STYLE_BLOCK = """<style>
 .fall{animation:fall var(--d) linear infinite;animation-delay:var(--t)}
 .spin{transform-box:fill-box;transform-origin:center;animation:spin var(--s) ease-in-out infinite alternate}
 .sway{transform-box:fill-box;transform-origin:center;animation:sway 6s ease-in-out infinite alternate}
 @keyframes fall{from{transform:translate(0,-60px);opacity:0}8%{opacity:1}85%{opacity:1}to{transform:translate(var(--dx),var(--h));opacity:0}}
 @keyframes spin{from{transform:rotate(-35deg) scaleX(1)}to{transform:rotate(55deg) scaleX(.55)}}
 @keyframes sway{from{transform:rotate(-6deg)}to{transform:rotate(6deg)}}
 @media (prefers-reduced-motion:reduce){.fall,.spin,.sway{animation:none}}
</style>"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def blossom(x: float, y: float, scale: float, rot: float, fill: str, center: str,
            opacity: float = 1.0, sway: bool = False) -> str:
    petals = "".join(f'<use href="#pt" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288))
    dots = '<circle r="4.2"/>' + "".join(
        f'<circle cx="{cx}" cy="{cy}" r="1.3"/>'
        for cx, cy in ((4.7, -6.47), (7.61, 2.47), (0, 8), (-7.61, 2.47), (-4.7, -6.47)))
    inner = f'<g fill="{fill}">{petals}</g><g fill="{center}">{dots}</g>'
    if sway:
        inner = f'<g class="sway">{inner}</g>'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({scale})" opacity="{opacity}">'
            f'{inner}</g>')


def falling_petals(p: Palette, seed: str, x0: float, x1: float, height: float, n: int,
                   size: tuple[float, float] = (0.36, 0.62)) -> str:
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(x0, x1)
        d = rnd.uniform(9.5, 15.5)
        t = -rnd.uniform(0, d)
        dx = -rnd.uniform(40, 120)
        sc = rnd.uniform(*size)
        fill = p.petal_b if i % 2 == 0 else p.petal_a
        op = rnd.uniform(0.55, 0.9)
        spin = rnd.uniform(2.2, 3.4)
        out.append(
            f'<g transform="translate({x:.0f} 0)"><g class="fall" style="--d:{d:.1f}s;--t:{t:.1f}s;'
            f'--dx:{dx:.0f}px;--h:{height + 60:.0f}px"><g transform="scale({sc:.2f})">'
            f'<use class="spin" href="#pt" fill="{fill}" opacity="{op:.2f}" style="--s:{spin:.1f}s"/>'
            f'</g></g></g>')
    return "".join(out)


def svg_doc(w: float, h: float, label: str, body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="{esc(label)}">\n<title>{esc(label)}</title>\n{STYLE_BLOCK}\n'
            f'<defs>\n <path id="pt" d="{PETAL}"/>\n{defs}</defs>\n{body}\n</svg>\n')


def frame(p: Palette, w: float, h: float, rx: float = 20, glow_at: tuple[float, float] = (0.85, 0.3),
          watermark: str | None = None, wm_size: float | None = None, wm_x: float | None = None,
          wm_y: float | None = None) -> tuple[str, str, str]:
    """Card background. Returns (defs, open_tag+background, close_tag)."""
    defs = (
        f' <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p.bg0}"/>'
        f'<stop offset="1" stop-color="{p.bg1}"/></linearGradient>\n'
        f' <radialGradient id="glow" cx="{glow_at[0]}" cy="{glow_at[1]}" r=".55">'
        f'<stop offset="0" stop-color="{p.glow}" stop-opacity="{p.glow_op}"/>'
        f'<stop offset="1" stop-color="{p.glow}" stop-opacity="0"/></radialGradient>\n'
        f' <clipPath id="clip"><rect width="{w:.0f}" height="{h:.0f}" rx="{rx}"/></clipPath>\n')
    body = ['<g clip-path="url(#clip)">',
            f' <rect width="{w:.0f}" height="{h:.0f}" fill="url(#bg)"/>',
            f' <rect width="{w:.0f}" height="{h:.0f}" fill="url(#glow)"/>']
    if watermark:
        size = wm_size or h * 1.15
        x = wm_x if wm_x is not None else w - 24
        y = wm_y if wm_y is not None else h * 0.5 + size * 0.36
        body.append(" " + text(watermark, x, y, Style("jp", 900, size), p.water, anchor="end", opacity=0.08))
    close = (f'</g>\n<rect x=".5" y=".5" width="{w - 1:.0f}" height="{h - 1:.0f}" rx="{rx - .5}" fill="none" '
             f'stroke="{p.border}" stroke-opacity="{p.border_op}"/>')
    return defs, "\n".join(body), close


def chip(x: float, y: float, label: str, p: Palette, style: Style | None = None, pad: float = 10,
         h: float = 26, solid: str | None = None, fg: str | None = None) -> tuple[str, float]:
    """Pill with text. Returns (svg, width). y is the top edge."""
    style = style or Style("mono", 400, 12.5)
    tw = measure(label, style)
    w = tw + pad * 2
    fill = solid or p.chip_bg
    color = fg or p.chip_fg
    svg = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
           + text(label, x + pad, y + h / 2 + style.size * 0.36, style, color))
    return svg, w


def eyebrow(s: str, x: float, y: float, p: Palette, size: float = 13, anchor: str = "start",
            color: str | None = None) -> str:
    return text(s.upper(), x, y, Style("sans", 600, size, tracking=size * 0.22), color or p.accent, anchor)
