#!/usr/bin/env python3
"""Cut the small font subsets in ./fonts from full system fonts.

Needs Inter and Noto Sans CJK installed (Debian/Ubuntu: fonts-inter,
fonts-noto-cjk). Run it whenever content.json gains characters the bundled
fonts don't cover — build.py names the missing character when that happens.
Latin fonts keep all of Latin, punctuation and arrows so live numbers and repo
names always render; the Japanese fonts keep only the characters in use.
"""
from __future__ import annotations

import glob
import os
import re

from fontTools import subset
from fontTools.ttLib import TTFont

from glyphs import BUNDLED, HERE, SOURCES

LATIN = "".join(chr(c) for c in list(range(0x20, 0x7F)) + list(range(0xA0, 0x250))
                + list(range(0x2000, 0x2070)) + list(range(0x2190, 0x21FF)) + [0x2026, 0x2122, 0x2605, 0x2606])
KANA = "".join(chr(c) for c in range(0x3000, 0x3100)) + "".join(chr(c) for c in range(0x30A0, 0x3100))


def used_text() -> str:
    chunks = []
    for path in [os.path.join(HERE, "content.json")] + glob.glob(os.path.join(HERE, "*.py")):
        with open(path, encoding="utf-8") as fh:
            chunks.append(fh.read())
    return "".join(chunks)


def main() -> None:
    os.makedirs(BUNDLED, exist_ok=True)
    cjk = "".join(sorted({ch for ch in used_text() if ord(ch) > 0x2FFF}))
    for name, (out_name, system, index) in SOURCES.items():
        if not system:
            continue  # shipped as-is (JetBrains Mono)
        font = TTFont(system, fontNumber=index)
        chars = (cjk + KANA + LATIN) if name.startswith("jp-") else (LATIN + "·")
        opts = subset.Options()
        opts.layout_features = ["kern", "liga", "calt", "palt", "tnum"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        sub = subset.Subsetter(opts)
        sub.populate(text=chars)
        sub.subset(font)
        out = os.path.join(BUNDLED, out_name)
        font.save(out)
        print(f"{out_name:28s} {os.path.getsize(out) / 1024:7.1f} KB")
    print("CJK characters kept:", re.sub(r"\s", "", cjk))


if __name__ == "__main__":
    main()
