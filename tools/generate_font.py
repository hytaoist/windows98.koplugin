#!/usr/bin/env python3
"""Build the Windows 98 UI font family from Liberation Sans.

The source is rendered at a small size, thresholded, and rebuilt as square
TrueType outlines. This keeps Latin UI text crisp on 300 ppi e-ink panels while
KOReader continues to use its normal CJK fallback fonts for non-Latin text.
"""

from __future__ import annotations

from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
SOURCES = {
    "Regular": FONT_DIR / "LiberationSans-Regular.ttf",
    "Bold": FONT_DIR / "LiberationSans-Bold.ttf",
}
OUTPUTS = {
    "Regular": FONT_DIR / "Windows98UI.ttf",
    "Bold": FONT_DIR / "Windows98UI-Bold.ttf",
}

PIXEL_SIZE = 11
BASELINE = 40
RENDER_LEFT = 10
THRESHOLD = 96
UNITS_PER_EM = 1024
PIXEL_UNITS = 64
FIXED_TIMESTAMP = 2981318400  # 1998-06-25 UTC in TrueType's 1904 epoch.


def glyph_name(codepoint: int) -> str:
    return "space" if codepoint == 32 else f"uni{codepoint:04X}"


def add_rect(pen: TTGlyphPen, x0: int, y0: int, x1: int, y1: int) -> None:
    pen.moveTo((x0, y0))
    pen.lineTo((x0, y1))
    pen.lineTo((x1, y1))
    pen.lineTo((x1, y0))
    pen.closePath()


def bitmap_for(character: str, source: ImageFont.FreeTypeFont) -> tuple[Image.Image, int]:
    image = Image.new("L", (64, 64), 0)
    draw = ImageDraw.Draw(image)
    draw.text(
        (RENDER_LEFT, BASELINE),
        character,
        font=source,
        fill=255,
        anchor="ls",
    )
    bbox = image.getbbox()
    if not bbox:
        return Image.new("1", (1, 1), 0), 0

    left, top, right, bottom = bbox
    crop = image.crop(bbox).point(lambda value: 255 if value >= THRESHOLD else 0)
    return crop.convert("1"), top - BASELINE


def build_glyph(
    character: str, source: ImageFont.FreeTypeFont
) -> tuple[TTGlyphPen, int, int]:
    bitmap, top = bitmap_for(character, source)
    width, height = bitmap.size

    pen = TTGlyphPen(None)
    pixels = bitmap.load()
    for row in range(height):
        column = 0
        while column < width:
            if not pixels[column, row]:
                column += 1
                continue
            run_start = column
            while column < width and pixels[column, row]:
                column += 1
            x0 = (run_start + 1) * PIXEL_UNITS
            x1 = (column + 1) * PIXEL_UNITS
            y1 = -(top + row) * PIXEL_UNITS
            y0 = y1 - PIXEL_UNITS
            add_rect(pen, x0, y0, x1, y1)

    source_advance = max(1, round(source.getlength(character)))
    advance = max(width + 2, source_advance) * PIXEL_UNITS
    bottom = max(0, -(top + height) * PIXEL_UNITS)
    return pen, advance, bottom


def build_font(style: str) -> None:
    source_path = SOURCES[style]
    if not source_path.exists():
        raise SystemExit(f"Missing source font: {source_path}")

    source = ImageFont.truetype(str(source_path), PIXEL_SIZE)
    codepoints = list(range(32, 127))
    names = [".notdef"] + [glyph_name(codepoint) for codepoint in codepoints]

    notdef = TTGlyphPen(None)
    add_rect(notdef, 64, 0, 9 * PIXEL_UNITS, 10 * PIXEL_UNITS)

    glyphs = {".notdef": notdef.glyph()}
    metrics = {".notdef": (10 * PIXEL_UNITS, 0)}
    cmap = {}
    max_bottom = 0

    for codepoint in codepoints:
        name = glyph_name(codepoint)
        if codepoint == 32:
            pen = TTGlyphPen(None)
            advance = max(2, round(source.getlength(" "))) * PIXEL_UNITS
            glyphs[name] = pen.glyph()
            metrics[name] = (advance, 0)
        else:
            pen, advance, bottom = build_glyph(chr(codepoint), source)
            glyphs[name] = pen.glyph()
            metrics[name] = (advance, PIXEL_UNITS)
            max_bottom = max(max_bottom, bottom)
        cmap[codepoint] = name

    ascent = 11 * PIXEL_UNITS
    descent = max(3 * PIXEL_UNITS, max_bottom)
    weight = 700 if style == "Bold" else 400

    builder = FontBuilder(UNITS_PER_EM, isTTF=True)
    builder.setupGlyphOrder(names)
    builder.setupCharacterMap(cmap)
    builder.setupGlyf(glyphs)
    builder.setupHorizontalMetrics(metrics)
    builder.setupHorizontalHeader(ascent=ascent, descent=-descent)
    builder.setupNameTable(
        {
            "familyName": "Windows98UI",
            "styleName": style,
            "uniqueFontIdentifier": f"Windows98UI-{style};2.000",
            "fullName": f"Windows 98 UI {style}",
            "psName": f"Windows98UI-{style}",
            "version": "Version 2.000",
            "copyright": (
                "Derived from Liberation Sans, copyright (c) 2010 Google "
                "Corporation and (c) 2012 Red Hat, Inc. Generated for "
                "Windows 98 for KOReader under the SIL Open Font License 1.1."
            ),
        }
    )
    builder.setupOS2(
        sTypoAscender=ascent,
        sTypoDescender=-descent,
        sTypoLineGap=0,
        usWinAscent=ascent,
        usWinDescent=descent,
        sxHeight=7 * PIXEL_UNITS,
        sCapHeight=10 * PIXEL_UNITS,
        usWeightClass=weight,
        fsSelection=0x20 if style == "Bold" else 0x40,
        achVendID="W98U",
        fsType=0,
    )
    builder.setupPost()
    builder.font["head"].flags = 0x000B
    builder.font["head"].macStyle = 0x01 if style == "Bold" else 0
    builder.font["head"].created = FIXED_TIMESTAMP
    builder.font["head"].modified = FIXED_TIMESTAMP
    builder.font["OS/2"].panose.bFamilyType = 2
    builder.font["OS/2"].panose.bProportion = 3
    output_path = OUTPUTS[style]
    builder.save(output_path)
    print(f"Generated {output_path} from {source_path.name} ({len(names)} glyphs)")


def main() -> None:
    for style in ("Regular", "Bold"):
        build_font(style)


if __name__ == "__main__":
    main()
