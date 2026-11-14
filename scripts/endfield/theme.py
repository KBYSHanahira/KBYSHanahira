"""Endfield-style industrial theme shared by every card.

Orange on near-black (and a concrete-grey light variant): chamfered frames,
hazard stripes, a faint blueprint grid, corner brackets, HUD readouts,
barcodes, rotating reticles and a slow scan line.
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
    grid: str
    grid_op: float
    border: str
    border_op: float
    title: str      # strongest text
    text: str       # body text
    muted: str      # secondary text / readouts
    accent: str     # signal orange
    accent2: str    # brighter orange
    ink: str        # the "black" of the hazard stripes
    water: str      # watermark kanji
    chip_bg: str
    chip_fg: str
    track: str      # empty bar / grid lines
    on_accent: str  # text placed on a solid accent fill


DARK = Palette(
    mode="dark", bg0="#0A0A0B", bg1="#16130F", glow="#FF7A1A", glow_op=0.16,
    grid="#FFFFFF", grid_op=0.035, border="#FF7A1A", border_op=0.30,
    title="#F4F1EA", text="#CFCAC0", muted="#7F7A72",
    accent="#FF7A1A", accent2="#FF9A3C", ink="#0A0A0B", water="#FF7A1A",
    chip_bg="#1F1B16", chip_fg="#FFB070", track="#26221D", on_accent="#0A0A0B",
)
LIGHT = Palette(
    mode="light", bg0="#F1EFEA", bg1="#E2DED6", glow="#FF7A1A", glow_op=0.14,
    grid="#000000", grid_op=0.045, border="#111111", border_op=0.22,
    title="#0E0E0E", text="#2C2A27", muted="#76716A",
    accent="#E8620A", accent2="#FF7A1A", ink="#111111", water="#111111",
    chip_bg="#111111", chip_fg="#FFB070", track="#D3CEC4", on_accent="#0E0E0E",
)
PALETTES = (DARK, LIGHT)

STYLE_BLOCK = """<style>
 .rot{transform-box:fill-box;transform-origin:center;animation:rot var(--r,24s) linear infinite}
 .rev{animation-direction:reverse}
 .hz{animation:hz 1.6s linear infinite}
 .scan{animation:scan var(--d,7s) cubic-bezier(.6,0,.4,1) infinite}
 .blink{animation:blink 1.2s steps(2,start) infinite}
 .up{animation:up var(--d) linear infinite;animation-delay:var(--t)}
 @keyframes rot{to{transform:rotate(360deg)}}
 @keyframes hz{to{transform:translateX(-22.63px)}}
 @keyframes scan{0%{transform:translateX(-80px);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateX(var(--w));opacity:0}}
 @keyframes blink{to{visibility:hidden}}
 @keyframes up{from{transform:translateY(0);opacity:0}15%{opacity:1}80%{opacity:1}to{transform:translateY(var(--h));opacity:0}}
 @media (prefers-reduced-motion:reduce){.rot,.hz,.scan,.blink,.up{animation:none}}
</style>"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def chamfer(x: float, y: float, w: float, h: float, c: float, c2: float | None = None) -> str:
    """Rectangle with the top-left and bottom-right corners cut off."""
    c2 = c if c2 is None else c2
    return (f"M{x + c:.1f} {y:.1f}H{x + w:.1f}V{y + h - c2:.1f}L{x + w - c2:.1f} {y + h:.1f}"
            f"H{x:.1f}V{y + c:.1f}Z")


def svg_doc(w: float, h: float, label: str, body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="{esc(label)}">\n<title>{esc(label)}</title>\n{STYLE_BLOCK}\n'
            f'<defs>\n{defs}</defs>\n{body}\n</svg>\n')


def hazard_defs(p: Palette) -> str:
    return (f' <pattern id="hzp" width="16" height="16" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)"><rect width="16" height="16" fill="{p.ink}"/>'
            f'<rect width="8" height="16" fill="{p.accent}"/></pattern>\n')


def hazard(x: float, y: float, w: float, h: float, cid: str, animate: bool = True) -> str:
    """A strip of diagonal orange/black stripes. Needs hazard_defs() once per document."""
    cls = ' class="hz"' if animate else ""
    return (f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><g{cls}><rect x="{x - 2:.1f}" y="{y:.1f}" width="{w + 30:.1f}" '
            f'height="{h:.1f}" fill="url(#hzp)"/></g></g>')


def brackets(x: float, y: float, w: float, h: float, color: str, arm: float = 14, sw: float = 2,
             op: float = 1) -> str:
    """Four corner brackets around a box."""
    d = (f"M{x} {y + arm}V{y}H{x + arm}M{x + w - arm} {y}H{x + w}V{y + arm}"
         f"M{x + w} {y + h - arm}V{y + h}H{x + w - arm}M{x + arm} {y + h}H{x}V{y + h - arm}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" opacity="{op}"/>'


def barcode(x: float, y: float, w: float, h: float, seed: str, color: str, op: float = 0.7) -> str:
    rnd = random.Random(seed)
    out = []
    cx = x
    while cx < x + w:
        bw = rnd.choice((1, 1, 1.5, 2, 3))
        if rnd.random() < 0.7:
            out.append(f'<rect x="{cx:.1f}" y="{y}" width="{bw}" height="{h}"/>')
        cx += bw + rnd.choice((1, 1.5, 2))
    return f'<g fill="{color}" opacity="{op}">{"".join(out)}</g>'


def ticks(x: float, y: float, w: float, color: str, step: float = 8, op: float = 0.5) -> str:
    """A ruler: short ticks with a taller one every fifth."""
    d = "".join(f"M{x + i * step:.1f} {y}v{6 if i % 5 else 11}" for i in range(int(w // step) + 1))
    return f'<path d="{d}" stroke="{color}" stroke-width="1" opacity="{op}"/>'


def diamond(x: float, y: float, r: float, fill: str, op: float = 1) -> str:
    return f'<path d="M{x} {y - r}L{x + r} {y}L{x} {y + r}L{x - r} {y}Z" fill="{fill}" opacity="{op}"/>'


def reticle(x: float, y: float, r: float, p: Palette, op: float = 1, spin: bool = True) -> str:
    """Targeting reticle: a dashed rotating ring, a segmented ring, crosshair ticks and a core diamond."""
    a = p.accent
    rot = ' class="rot"' if spin else ""
    rev = ' class="rot rev" style="--r:16s"' if spin else ""
    r2 = r * .72
    return "".join([
        f'<g transform="translate({x} {y})" opacity="{op}">',
        f'<g{rot}><circle r="{r}" fill="none" stroke="{a}" stroke-width="1.4" stroke-dasharray="2 6"/></g>',
        f'<g{rev}><circle r="{r2:.1f}" fill="none" stroke="{a}" stroke-width="2.4" '
        f'stroke-dasharray="{r2 * 1.4:.1f} {r2 * 0.17:.1f}"/></g>',
        f'<circle r="{r * .46:.1f}" fill="none" stroke="{p.title}" stroke-opacity=".25" stroke-width="1"/>',
        f'<path d="M{-r - 8} 0h{r * .38:.1f}M{r + 8} 0h{-r * .38:.1f}M0 {-r - 8}v{r * .38:.1f}M0 {r + 8}v{-r * .38:.1f}" '
        f'stroke="{p.title}" stroke-opacity=".55" stroke-width="1.4"/>',
        diamond(0, 0, r * .16, a),
        '</g>'])


def motes(p: Palette, seed: str, x0: float, x1: float, height: float, n: int) -> str:
    """Small squares drifting upwards, like dust in a work light."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(height * .55, height + 10)
        d = rnd.uniform(6, 12)
        t = -rnd.uniform(0, d)
        s = rnd.choice((2, 2, 3, 4))
        col = p.accent if i % 3 else p.title
        op = rnd.uniform(.35, .8)
        out.append(f'<rect class="up" x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{col}" '
                   f'opacity="{op:.2f}" style="--d:{d:.1f}s;--t:{t:.1f}s;--h:-{height * .6:.0f}px"/>')
    return "".join(out)


def scanline(p: Palette, w: float, h: float, dur: float = 7) -> str:
    return (f'<g class="scan" style="--w:{w + 80:.0f}px;--d:{dur}s">'
            f'<rect x="0" y="0" width="80" height="{h:.0f}" fill="url(#scg)"/>'
            f'<rect x="79" y="0" width="1.5" height="{h:.0f}" fill="{p.accent}" opacity=".55"/></g>')


def frame(p: Palette, w: float, h: float, c: float = 18, glow_at: tuple[float, float] = (0.85, 0.3),
          watermark: str | None = None, wm_size: float | None = None, wm_x: float | None = None,
          wm_y: float | None = None, scan: bool = True, code: str | None = None) -> tuple[str, str, str]:
    """Card background. Returns (defs, open+background, close)."""
    shape = chamfer(0, 0, w, h, c)
    defs = (
        f' <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p.bg0}"/>'
        f'<stop offset="1" stop-color="{p.bg1}"/></linearGradient>\n'
        f' <radialGradient id="glow" cx="{glow_at[0]}" cy="{glow_at[1]}" r=".6">'
        f'<stop offset="0" stop-color="{p.glow}" stop-opacity="{p.glow_op}"/>'
        f'<stop offset="1" stop-color="{p.glow}" stop-opacity="0"/></radialGradient>\n'
        f' <linearGradient id="scg" x1="0" x2="1"><stop offset="0" stop-color="{p.accent}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{p.accent}" stop-opacity=".10"/></linearGradient>\n'
        f' <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M24 0H0V24" fill="none" stroke="{p.grid}" stroke-opacity="{p.grid_op}"/></pattern>\n'
        f' <clipPath id="clip"><path d="{shape}"/></clipPath>\n'
        + hazard_defs(p))
    body = ['<g clip-path="url(#clip)">',
            f' <rect width="{w:.0f}" height="{h:.0f}" fill="url(#bg)"/>',
            f' <rect width="{w:.0f}" height="{h:.0f}" fill="url(#grid)"/>',
            f' <rect width="{w:.0f}" height="{h:.0f}" fill="url(#glow)"/>']
    if watermark:
        size = wm_size or h * 1.15
        x = wm_x if wm_x is not None else w - 24
        y = wm_y if wm_y is not None else h * 0.5 + size * 0.36
        body.append(" " + text(watermark, x, y, Style("jp", 900, size), p.water, anchor="end", opacity=0.06))
    if scan:
        body.append(" " + scanline(p, w, h))
    close = ['</g>',
             f'<path d="{chamfer(.75, .75, w - 1.5, h - 1.5, c - .3)}" fill="none" stroke="{p.border}" '
             f'stroke-opacity="{p.border_op}" stroke-width="1.5"/>',
             f'<path d="M1.5 {c + 22}V{c}L{c} 1.5H{c + 22}" fill="none" stroke="{p.accent}" stroke-width="3"/>',
             f'<path d="M{w - 1.5} {h - c - 22}V{h - c}L{w - c} {h - 1.5}H{w - c - 22}" fill="none" '
             f'stroke="{p.accent}" stroke-width="3"/>',
             f'<path d="M{w - 30} 1.5H{w - 1.5}V30" fill="none" stroke="{p.title}" stroke-opacity=".45" stroke-width="1.5"/>',
             f'<path d="M1.5 {h - 30}V{h - 1.5}H30" fill="none" stroke="{p.title}" stroke-opacity=".45" stroke-width="1.5"/>']
    if code:
        close.append(readout(code, w - c - 32, h - 9, p, size=10.5, anchor="end", op=0.85))
    return defs, "\n".join(body), "\n".join(close)


def chip(x: float, y: float, label: str, p: Palette, style: Style | None = None, pad: float = 10,
         h: float = 26, solid: str | None = None, fg: str | None = None, outline: bool = False) -> tuple[str, float]:
    """Angular tag with text. Returns (svg, width). y is the top edge."""
    style = style or Style("mono", 400, 12.5)
    tw = measure(label, style)
    w = tw + pad * 2
    fill = solid or p.chip_bg
    color = fg or p.chip_fg
    c = min(8, h * .3)
    if outline:
        shape = (f'<path d="{chamfer(x + .75, y + .75, w - 1.5, h - 1.5, c)}" fill="none" stroke="{fill}" '
                 f'stroke-width="1.5"/>')
    else:
        shape = f'<path d="{chamfer(x, y, w, h, c)}" fill="{fill}"/>'
    svg = shape + text(label, x + pad, y + h / 2 + style.size * 0.36, style, color)
    return svg, w


def eyebrow(s: str, x: float, y: float, p: Palette, size: float = 13, anchor: str = "start",
            color: str | None = None) -> str:
    return text(s.upper(), x, y, Style("sans", 600, size, tracking=size * 0.22), color or p.accent, anchor)


def readout(s: str, x: float, y: float, p: Palette, size: float = 11, anchor: str = "start",
            color: str | None = None, op: float | None = None) -> str:
    return text(s, x, y, Style("mono", 400, size, tracking=size * .12), color or p.muted, anchor, opacity=op)
