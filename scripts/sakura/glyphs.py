"""Text → SVG paths.

GitHub serves README images through a proxy that blocks web fonts, so every
piece of text in these cards is drawn as outlines. Shaping (kerning,
ligatures) is done by HarfBuzz, outlines come from fontTools.

Fonts are looked up in ./fonts first (the subsets committed to the repo, so
the GitHub Action can build without system fonts) and fall back to the system
copies that `subset_fonts.py` cuts those subsets from.
"""
from __future__ import annotations

import functools
import os
from dataclasses import dataclass

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(HERE, "fonts")

# name -> (bundled file, system file, collection index)
SOURCES = {
    "inter-400": ("Inter-Regular.otf", "/usr/share/fonts/opentype/inter/Inter-Regular.otf", 0),
    "inter-500": ("Inter-Medium.otf", "/usr/share/fonts/opentype/inter/Inter-Medium.otf", 0),
    "inter-600": ("Inter-SemiBold.otf", "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 0),
    "inter-700": ("Inter-Bold.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf", 0),
    "inter-800": ("Inter-ExtraBold.otf", "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 0),
    "jp-400": ("NotoSansJP-Regular.otf", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 0),
    "jp-500": ("NotoSansJP-Medium.otf", "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc", 0),
    "jp-700": ("NotoSansJP-Bold.otf", "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0),
    "jp-900": ("NotoSansJP-Black.otf", "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", 0),
    "mono-400": ("JetBrainsMono-Regular.ttf", None, 0),
    "mono-700": ("JetBrainsMono-Bold.ttf", None, 0),
}

# family -> weight -> chain of fonts tried per character
FAMILIES = {
    "sans": {w: [f"inter-{w}", f"jp-{min((400, 500, 700, 900), key=lambda j: abs(j - w))}"]
             for w in (400, 500, 600, 700, 800)},
    "jp": {w: [f"jp-{w}", "inter-500"] for w in (400, 500, 700, 900)},
    "mono": {w: [f"mono-{w}", f"jp-{w}"] for w in (400, 700)},
}


def font_file(name: str) -> tuple[str, int]:
    bundled, system, index = SOURCES[name]
    path = os.path.join(BUNDLED, bundled)
    if os.path.exists(path):
        return path, 0
    if system and os.path.exists(system):
        return system, index
    raise FileNotFoundError(f"font {name}: neither {path} nor {system} exists")


class Font:
    def __init__(self, name: str):
        path, index = font_file(name)
        self.name = name
        self.tt = TTFont(path, fontNumber=index, lazy=True)
        self.cmap = self.tt.getBestCmap()
        self.upem = self.tt["head"].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        with open(path, "rb") as fh:
            blob = hb.Blob(fh.read())
        self.hb = hb.Font(hb.Face(blob, index))

    def has(self, ch: str) -> bool:
        return ord(ch) in self.cmap or ch in "  "


@functools.lru_cache(maxsize=None)
def get_font(name: str) -> Font:
    return Font(name)


@dataclass(frozen=True)
class Style:
    family: str = "sans"
    weight: int = 400
    size: float = 16
    tracking: float = 0  # extra px between glyphs

    def chain(self) -> list[Font]:
        return [get_font(n) for n in FAMILIES[self.family][self.weight]]


def _runs(text: str, style: Style):
    chain = style.chain()
    runs: list[tuple[Font, str]] = []
    for ch in text:
        font = next((f for f in chain if f.has(ch)), None)
        if font is None:
            raise ValueError(f"no font in {style.family}/{style.weight} covers {ch!r} (U+{ord(ch):04X}) "
                             "— run subset_fonts.py after adding new characters")
        if runs and runs[-1][0] is font:
            runs[-1] = (font, runs[-1][1] + ch)
        else:
            runs.append((font, ch))
    return runs


def _shape(font: Font, text: str):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font.hb, buf, {"kern": True, "liga": True})
    return buf.glyph_infos, buf.glyph_positions


def measure(text: str, style: Style) -> float:
    width = 0.0
    n = 0
    for font, run in _runs(text, style):
        _, pos = _shape(font, run)
        scale = style.size / font.upem
        width += sum(p.x_advance for p in pos) * scale
        n += len(pos)
    return width + style.tracking * max(n - 1, 0)


def _fmt(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def path_d(text: str, x: float, y: float, style: Style, anchor: str = "start") -> str:
    if anchor != "start":
        w = measure(text, style)
        x -= w if anchor == "end" else w / 2
    parts: list[str] = []
    pen_x = x
    for font, run in _runs(text, style):
        infos, pos = _shape(font, run)
        scale = style.size / font.upem
        for info, p in zip(infos, pos):
            name = font.order[info.codepoint]
            gx = pen_x + p.x_offset * scale
            gy = y - p.y_offset * scale
            svg = SVGPathPen(font.glyphset, ntos=_fmt)
            font.glyphset[name].draw(TransformPen(svg, (scale, 0, 0, -scale, gx, gy)))
            d = svg.getCommands()
            if d:
                parts.append(d)
            pen_x += p.x_advance * scale + style.tracking
    return "".join(parts)


def text(s: str, x: float, y: float, style: Style, fill: str, anchor: str = "start",
         opacity: float | None = None, extra: str = "") -> str:
    d = path_d(s, x, y, style, anchor)
    if not d:
        return ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{d}" fill="{fill}"{op}{extra}/>'


def wrap(s: str, style: Style, max_w: float) -> list[str]:
    words = s.split(" ")
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}" if cur else w
        if measure(trial, style) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def ellipsize(s: str, style: Style, max_w: float) -> str:
    if measure(s, style) <= max_w:
        return s
    while s and measure(s + "…", style) > max_w:
        s = s[:-1]
    return s.rstrip() + "…"
