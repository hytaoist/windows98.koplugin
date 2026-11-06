#!/usr/bin/env python3
"""Generate the Windows 98 KOReader and SimpleUI icon sets.

The artwork uses a deliberately constrained Windows 98 vocabulary: opaque
silver panels, two-stage raised/sunken bevels, navy title bars, gold shell
folders, hard drop shadows and crisp one-pixel outlines.
"""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
SIMPLEUI_ICON_DIR = ROOT / "assets" / "simpleui-icons"

BLACK = "#000000"
WHITE = "#ffffff"
SILVER = "#c0c0c0"
LIGHT = "#dfdfdf"
DARK = "#808080"
NAVY = "#000080"
BLUE = "#1084d0"
GOLD = "#f0c848"
GOLD_LIGHT = "#ffe890"
GOLD_DARK = "#b07818"
TEAL = "#008080"
WINDOWS_RED = "#d40000"
WINDOWS_GREEN = "#00a000"
WINDOWS_BLUE = "#0000c0"
WINDOWS_YELLOW = "#ffc000"

EXPECTED_ICONS = {
    "align.auto",
    "align.center",
    "align.justify",
    "align.left",
    "align.right",
    "appbar.contrast",
    "appbar.crop",
    "appbar.filebrowser",
    "appbar.menu",
    "appbar.navigation",
    "appbar.pagefit",
    "appbar.pageview",
    "appbar.pokeball",
    "appbar.rotation",
    "appbar.search",
    "appbar.settings",
    "appbar.textsize",
    "appbar.tools",
    "appbar.typeset",
    "back.top.rtl",
    "back.top",
    "book.opened",
    "bookmark",
    "cancel",
    "check",
    "chevron.first",
    "chevron.last",
    "chevron.left",
    "chevron.right",
    "chevron.up",
    "close",
    "column.one",
    "column.three",
    "column.two",
    "control.collapse",
    "control.expand.alpha",
    "control.expand",
    "cre.render.partial",
    "cre.render.ready",
    "cre.render.reload.alpha",
    "cre.render.reload",
    "cre.render.working",
    "direction.BTLR",
    "direction.BTRL",
    "direction.LRBT",
    "direction.LRTB",
    "direction.RLBT",
    "direction.RLTB",
    "direction.TBLR",
    "direction.TBRL",
    "dogear.abandoned.rtl",
    "dogear.abandoned",
    "dogear.alpha",
    "dogear.complete.rtl",
    "dogear.complete",
    "dogear.opaque",
    "dogear.reading",
    "edit",
    "exit",
    "home",
    "info",
    "license",
    "move.down",
    "move.up",
    "notice-info",
    "notice-question",
    "notice-warning",
    "plus",
    "position.marker",
    "position.marker.top",
    "rotation.0UR",
    "rotation.180UD",
    "rotation.90CCW",
    "rotation.90CW",
    "rotation.L.0UR",
    "rotation.L.180UD",
    "rotation.L.90CCW",
    "rotation.L.90CW",
    "rotation.P.0UR",
    "rotation.P.180UD",
    "rotation.P.90CCW",
    "rotation.P.90CW",
    "star.empty",
    "star.full",
    "star.white",
    "texture-box",
    "triangle",
    "wifi.open.0",
    "wifi.open.100",
    "wifi.open.25",
    "wifi.open.50",
    "wifi.open.75",
    "wifi.secure.0",
    "wifi.secure.100",
    "wifi.secure.25",
    "wifi.secure.50",
    "wifi.secure.75",
    "wifi",
    "zoom.column",
    "zoom.content",
    "zoom.manual",
    "zoom.page",
    "zoom.row",
}

SIMPLEUI_ICON_NAMES = {
    "authors",
    "bookmark_browser",
    "chevron_left",
    "chevron_right",
    "coll_back",
    "collections",
    "continue",
    "favorites",
    "folder",
    "frontlight",
    "history",
    "homescreen",
    "library",
    "menu",
    "night_mode",
    "pager_first",
    "pager_last",
    "power",
    "qa_group",
    "qa_plugin",
    "random_document",
    "recent",
    "search",
    "series",
    "settings",
    "stats_calendar",
    "tab_filebrowser",
    "tab_fm_settings",
    "tab_navigation",
    "tab_qs_panel",
    "tab_tools",
    "tab_typeset",
    "tags",
    "wifi_toggle",
}


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str | None = None,
    stroke: str | None = BLACK,
    sw: float = 1,
) -> str:
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    stroke_attr = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {fill_attr} {stroke_attr}/>'


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = BLACK,
    sw: float = 1,
) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{sw}"/>'
    )


def poly(
    points: str,
    *,
    fill: str | None = None,
    stroke: str | None = BLACK,
    sw: float = 1,
) -> str:
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    stroke_attr = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return f'<polygon points="{points}" {fill_attr} {stroke_attr}/>'


def path(
    d: str,
    *,
    fill: str | None = None,
    stroke: str | None = BLACK,
    sw: float = 1,
) -> str:
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    stroke_attr = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return f'<path d="{d}" {fill_attr} {stroke_attr}/>'


def circle(
    cx: float,
    cy: float,
    r: float,
    *,
    fill: str | None = None,
    stroke: str | None = BLACK,
    sw: float = 1,
) -> str:
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    stroke_attr = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {fill_attr} {stroke_attr}/>'


def bevel(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = SILVER,
    sunken: bool = False,
    shadow: bool = False,
) -> str:
    """Return a two-stage Windows 98 raised or sunken panel."""
    out = []
    if shadow:
        out.append(rect(x + 2, y + 2, w, h, fill=BLACK, stroke=None))
    out.append(rect(x, y, w, h, fill=BLACK, stroke=None))
    out.append(rect(x + 1, y + 1, w - 2, h - 2, fill=fill, stroke=None))
    high = DARK if sunken else WHITE
    low = WHITE if sunken else DARK
    inner_high = BLACK if sunken else LIGHT
    inner_low = LIGHT if sunken else BLACK
    out.extend(
        (
            rect(x + 1, y + 1, w - 2, 1, fill=high, stroke=None),
            rect(x + 1, y + 1, 1, h - 2, fill=high, stroke=None),
            rect(x + 1, y + h - 2, w - 2, 1, fill=low, stroke=None),
            rect(x + w - 2, y + 1, 1, h - 2, fill=low, stroke=None),
        )
    )
    if w >= 10 and h >= 10:
        out.extend(
            (
                rect(x + 2, y + 2, w - 4, 1, fill=inner_high, stroke=None),
                rect(x + 2, y + 2, 1, h - 4, fill=inner_high, stroke=None),
                rect(x + 2, y + h - 3, w - 4, 1, fill=inner_low, stroke=None),
                rect(x + w - 3, y + 2, 1, h - 4, fill=inner_low, stroke=None),
            )
        )
    return "".join(out)


def button(x: int, y: int, w: int, h: int, *content: str) -> str:
    return bevel(x, y, w, h) + "".join(content)


def window(x: int, y: int, w: int, h: int, *, shadow: bool = True) -> str:
    return (
        bevel(x, y, w, h, shadow=shadow)
        + rect(x + 3, y + 3, w - 6, 6, fill=NAVY, stroke=None)
        + rect(x + 3, y + 3, w - 6, 1, fill=BLUE, stroke=None)
        + rect(x + 5, y + 5, max(2, w // 7), 1, fill=WHITE, stroke=None)
        + rect(x + w - 9, y + 4, 5, 4, fill=SILVER, stroke=BLACK)
    )


def document(
    x: int = 6,
    y: int = 3,
    w: int = 20,
    h: int = 26,
    *,
    lines: int = 3,
    fold: bool = True,
) -> str:
    out = [
        rect(x + 2, y + 2, w, h, fill=BLACK, stroke=None),
        rect(x, y, w, h, fill=WHITE),
    ]
    if fold:
        out.append(poly(f"{x + w - 6},{y} {x + w},{y + 6} {x + w - 6},{y + 6}", fill=SILVER))
        out.append(path(f"M{x + w - 6} {y}h6v6", sw=1))
    for index in range(lines):
        line_y = y + 9 + index * 5
        out.append(line(x + 4, line_y, x + w - 4, line_y, color=DARK, sw=1))
    return "".join(out)


def folder_icon() -> str:
    return "".join(
        (
            rect(4, 8, 25, 19, fill=BLACK, stroke=None),
            rect(2, 10, 25, 18, fill=BLACK, stroke=None),
            path("M2 8h10l3 3h14v18H2z", fill=GOLD_DARK),
            path("M2 13h28v16H2z", fill=GOLD),
            line(3, 14, 28, 14, color=GOLD_LIGHT, sw=1),
            line(3, 28, 28, 28, color=GOLD_DARK, sw=1),
            rect(4, 9, 8, 2, fill=GOLD_LIGHT, stroke=None),
            rect(5, 16, 22, 3, fill=GOLD_LIGHT, stroke=None),
        )
    )


def computer_icon() -> str:
    return "".join(
        (
            rect(3, 4, 27, 21, fill=BLACK, stroke=None),
            rect(2, 3, 27, 21, fill=SILVER, sw=1),
            bevel(5, 6, 21, 13, fill=TEAL, sunken=True),
            rect(8, 9, 8, 2, fill=WHITE, stroke=None),
            rect(8, 13, 12, 1, fill=LIGHT, stroke=None),
            rect(10, 24, 13, 3, fill=BLACK, stroke=None),
            bevel(8, 24, 17, 3, fill=SILVER),
            rect(12, 27, 9, 2, fill=DARK, stroke=None),
            rect(19, 21, 3, 1, fill=WINDOWS_GREEN, stroke=None),
        )
    )


def chevron(direction: str) -> str:
    paths = {
        "left": "M21 7L10 16l11 9v-4l-7-5 7-5z",
        "right": "M11 7l11 9-11 9v-4l7-5-7-5z",
        "up": "M7 21l9-11 9 11h-4l-5-7-5 7z",
        "first": "M7 7h3v18H7zM25 7l-11 9 11 9v-4l-7-5 7-5z",
        "last": "M25 7h-3v18h3zM10 7l11 9-11 9v-4l7-5-7-5z",
    }
    return path(paths[direction], fill=BLACK, stroke=None)


def checkmark() -> str:
    return path("M5 16l6 7 16-16v5L11 29 5 22z", fill=BLACK, stroke=None)


def plusmark() -> str:
    return rect(13, 5, 6, 22, fill=BLACK, stroke=None) + rect(5, 13, 22, 6, fill=BLACK, stroke=None)


def minusmark() -> str:
    return rect(5, 13, 22, 6, fill=BLACK, stroke=None)


def close_x() -> str:
    return path(
        "M7 5l9 11 9-11h5L18 16l12 11h-5L16 18 6 27H1l12-11L1 5z",
        fill=BLACK,
        stroke=None,
    )


def star(fill_kind: str) -> str:
    points = "16,2 21,11 31,12 23,19 26,29 16,24 6,29 9,19 1,12 11,11"
    fill = BLACK if fill_kind == "full" else SILVER if fill_kind == "white" else WHITE
    return (
        poly(points, fill=fill, sw=2)
        + poly("12,7 16,4 19,10 14,11", fill=WHITE, stroke=None)
        + line(10, 25, 12, 19, color=WHITE, sw=1)
    )


def magnifier() -> str:
    return (
        circle(14, 13, 10, fill=WHITE, sw=2)
        + circle(14, 13, 6, fill=SILVER, sw=1)
        + path("M21 20l9 9-4 4-9-9z", fill=SILVER, sw=2)
        + line(23, 22, 28, 27, color=WHITE, sw=1)
        + line(8, 8, 13, 6, color=WHITE, sw=1)
    )


def wifi(level: int, secure: bool) -> str:
    out = []
    heights = [4, 8, 12, 16]
    for index, bar_height in enumerate(heights):
        x = 2 + index * 7
        y = 25 - bar_height
        active = index < level
        out.append(bevel(x, y, 5, bar_height, fill=SILVER if active else WHITE))
        if active:
            out.append(rect(x + 2, y + 2, 1, bar_height - 4, fill=BLACK, stroke=None))
    if secure:
        out.extend(
            (
                bevel(19, 19, 11, 10, fill=SILVER, shadow=True),
                path("M21 19v-3a3 3 0 016 0v3", sw=2),
                line(24, 22, 24, 25, sw=1),
            )
        )
    return "".join(out)


def network_icon() -> str:
    return "".join(
        (
            bevel(2, 7, 13, 11, fill=SILVER, shadow=True),
            bevel(17, 7, 13, 11, fill=SILVER, shadow=True),
            bevel(5, 10, 7, 5, fill=TEAL, sunken=True),
            bevel(20, 10, 7, 5, fill=TEAL, sunken=True),
            rect(15, 12, 2, 5, fill=BLACK, stroke=None),
            rect(9, 18, 14, 2, fill=DARK, stroke=None),
            rect(13, 22, 6, 3, fill=WINDOWS_GREEN),
        )
    )


def zoom(kind: str) -> str:
    out = [magnifier()]
    if kind == "content":
        out.extend((line(9, 10, 18, 10, sw=1), line(9, 13, 18, 13, sw=1), line(9, 16, 15, 16, sw=1)))
    elif kind == "column":
        out.extend((rect(8, 8, 12, 10, fill=WHITE), line(14, 8, 14, 18, sw=1)))
    elif kind == "row":
        out.extend((rect(8, 8, 12, 10, fill=WHITE), line(8, 13, 20, 13, sw=1)))
    elif kind == "page":
        out.append(rect(9, 8, 10, 10, fill=WHITE))
    elif kind == "manual":
        out.append(rect(9, 8, 10, 10, fill=WHITE))
        out.extend((line(14, 9, 14, 17, sw=1), line(10, 13, 18, 13, sw=1)))
    return "".join(out)


def align_lines(kind: str) -> str:
    out = [bevel(3, 4, 26, 24, fill=WHITE, shadow=True)]
    widths = [16, 20, 13, 18]
    for index, width in enumerate(widths):
        y = 9 + index * 4
        if kind == "right":
            x = 26 - width
        elif kind in {"center", "auto"}:
            x = 16 - width / 2
        elif kind == "justify":
            width = 20
            x = 6
        else:
            x = 6
        out.append(rect(x, y, width, 2, fill=BLACK, stroke=None))
    if kind == "auto":
        out.append(button(20, 20, 8, 8, poly("24,22 28,26 20,26", fill=BLACK, stroke=None)))
    return "".join(out)


def layout_columns(count: int) -> str:
    out = [window(3, 5, 26, 22)]
    if count >= 2:
        out.append(line(16, 9, 16, 26, sw=1))
    if count == 3:
        out.extend((line(11, 9, 11, 26, sw=1), line(21, 9, 21, 26, sw=1)))
    if count == 4:
        out.extend((line(5, 12, 27, 12, sw=1), line(5, 18, 27, 18, sw=1)))
    return "".join(out)


def rotation_icon(variant: str) -> str:
    out = [bevel(6, 7, 20, 18, fill=SILVER, shadow=True), rect(10, 11, 12, 10, fill=WHITE)]
    if "90CW" in variant:
        out.extend((path("M24 5v8h-8", sw=2), path("M23 12c-3-4-8-4-12-1", sw=2)))
    elif "90CCW" in variant:
        out.extend((path("M8 5v8h8", sw=2), path("M9 12c3-4 8-4 12-1", sw=2)))
    elif "180" in variant:
        out.extend((path("M24 6l3 6-7 1", sw=2), path("M8 26l-3-6 7-1", sw=2)))
    else:
        out.extend((path("M16 2v7M12 5l4-4 4 4", sw=2), line(16, 9, 16, 12, sw=2)))
    if variant.startswith("rotation.L."):
        out.append(button(2, 2, 7, 7, rect(4, 4, 3, 3, fill=BLACK, stroke=None)))
    elif variant.startswith("rotation.P."):
        out.append(button(23, 23, 7, 7, rect(25, 25, 3, 3, fill=BLACK, stroke=None)))
    return "".join(out)


def direction_icon(name: str) -> str:
    out = [bevel(2, 2, 28, 28, fill=SILVER)]
    if name in {"direction.LRBT", "direction.RLBT"}:
        out.extend(
            (
                rect(6, 15, 20, 2, fill=BLACK, stroke=None),
                poly("3,16 10,11 10,21", fill=BLACK, stroke=None),
                poly("29,16 22,11 22,21", fill=BLACK, stroke=None),
            )
        )
    elif name in {"direction.BTLR", "direction.TBLR"}:
        out.extend(
            (
                rect(15, 6, 2, 20, fill=BLACK, stroke=None),
                poly("16,3 11,10 21,10", fill=BLACK, stroke=None),
                poly("16,29 11,22 21,22", fill=BLACK, stroke=None),
            )
        )
    elif name in {"direction.LRTB", "direction.BTRL"}:
        out.extend(
            (
                path("M5 6l21 20", sw=2),
                poly("27,5 26,13 19,6", fill=BLACK, stroke=None),
                poly("5,27 6,19 13,26", fill=BLACK, stroke=None),
            )
        )
    else:
        out.extend(
            (
                rect(6, 8, 20, 2, fill=BLACK, stroke=None),
                rect(6, 22, 20, 2, fill=BLACK, stroke=None),
                poly("29,9 22,5 22,13", fill=BLACK, stroke=None),
                poly("3,23 10,19 10,27", fill=BLACK, stroke=None),
            )
        )
    return "".join(out)


def dogear(kind: str) -> str:
    out = [document(lines=0)]
    fold_fill = BLACK if kind == "complete" else SILVER
    out.append(poly("20,3 26,9 20,9", fill=fold_fill, stroke=None))
    if kind == "abandoned":
        out.extend((path("M10 13l12 12", sw=2), path("M22 13L10 25", sw=2)))
    elif kind == "reading":
        out.extend((rect(9, 14, 14, 2, fill=BLACK, stroke=None), rect(9, 19, 14, 2, fill=DARK, stroke=None)))
    else:
        out.extend((rect(9, 14, 14, 2, fill=BLACK, stroke=None), rect(9, 19, 10, 2, fill=DARK, stroke=None)))
    if kind == "opaque":
        out.append(rect(22, 22, 7, 7, fill=SILVER, sw=2))
    return "".join(out)


def notice(symbol: str) -> str:
    out = [bevel(3, 4, 26, 20, fill=SILVER, shadow=True), rect(7, 8, 18, 12, fill=WHITE)]
    if symbol == "warning":
        out.extend(
            (
                poly("16,8 24,22 8,22", fill=SILVER, sw=2),
                rect(15, 12, 2, 6, fill=BLACK, stroke=None),
                rect(15, 19, 2, 2, fill=BLACK, stroke=None),
            )
        )
    elif symbol == "question":
        out.extend(
            (
                path("M12 12c0-5 7-6 9-1 2 4-5 5-5 8", sw=2),
                rect(15, 21, 3, 3, fill=BLACK, stroke=None),
            )
        )
    else:
        out.extend((rect(15, 9, 2, 9, fill=BLACK, stroke=None), rect(15, 20, 2, 2, fill=BLACK, stroke=None)))
    return "".join(out)


def book() -> str:
    return "".join(
        (
            rect(4, 6, 25, 22, fill=BLACK, stroke=None),
            path("M3 5c5-2 9-1 13 2v20c-4-3-8-4-13-2z", fill=SILVER),
            path("M29 5c-5-2-9-1-13 2v20c4-3 8-4 13-2z", fill=SILVER),
            line(15, 8, 15, 26, color=DARK, sw=1),
            line(5, 9, 12, 10, color=WHITE, sw=1),
            line(20, 10, 27, 9, color=WHITE, sw=1),
        )
    )


def pencil() -> str:
    return "".join((
        poly("4,27 7,18 21,4 27,10 13,24", fill=SILVER, sw=2),
        poly("7,18 13,24 8,27 4,27", fill=WHITE, stroke=None),
        path("M4 27h4l-4 3z", fill=BLACK, stroke=None),
        line(20, 6, 25, 11, color=WHITE, sw=1),
    ))


def house() -> str:
    return "".join((
        rect(4, 15, 24, 14, fill=SILVER, sw=2),
        poly("2,16 16,4 30,16 27,18 26,17 26,27 6,27 6,17 5,18", fill=SILVER, sw=2),
        rect(10, 18, 5, 5, fill=WHITE, sw=1),
        rect(18, 20, 6, 9, fill=DARK, sw=1),
        line(3, 16, 16, 5, color=WHITE, sw=1),
    ))


def bookmark_icon() -> str:
    return "".join((
        bevel(8, 2, 16, 27, fill=SILVER, shadow=True),
        poly("10,5 22,5 22,24 16,20 10,24", fill=BLACK, stroke=None),
        line(12, 7, 12, 19, color=WHITE, sw=1),
    ))


def settings_sliders() -> str:
    out = [bevel(3, 4, 26, 24, fill=SILVER, shadow=True)]
    for y, knob in ((9, 11), (16, 21), (23, 8)):
        out.extend(
            (
                rect(6, y, 20, 2, fill=BLACK, stroke=None),
                bevel(knob - 3, y - 2, 7, 6, fill=LIGHT),
                line(knob, y, knob, y + 2, color=BLACK, sw=1),
            )
        )
    return "".join(out)


def pageview() -> str:
    return document(2, 5, 13, 22, lines=2) + document(17, 5, 13, 22, lines=2)


def appbar_pagefit() -> str:
    return "".join((
        window(3, 5, 26, 23),
        rect(7, 10, 18, 14, fill=WHITE),
        path("M9 18l4-4 4 4M21 15l-4 4-4-4", sw=2),
    ))


def appbar_textsize() -> str:
    return "".join((
        button(2, 2, 28, 28),
        path("M7 24L13 8h3l6 16h-3l-2-5h-6l-2 5z", fill=BLACK, stroke=None),
        rect(12, 16, 5, 2, fill=SILVER, stroke=None),
        poly("25,7 29,12 21,12", fill=BLACK, stroke=None),
        poly("25,25 21,20 29,20", fill=BLACK, stroke=None),
    ))


def appbar_typeset() -> str:
    return "".join((
        button(2, 2, 28, 28),
        rect(7, 7, 18, 4, fill=BLACK, stroke=None),
        rect(16, 7, 3, 19, fill=BLACK, stroke=None),
        rect(12, 25, 11, 2, fill=BLACK, stroke=None),
        rect(6, 11, 4, 2, fill=DARK, stroke=None),
        rect(23, 11, 4, 2, fill=DARK, stroke=None),
    ))


def appbar_contrast() -> str:
    return "".join((
        circle(16, 16, 13, fill=WHITE, sw=2),
        path("M16 4a12 12 0 010 24z", fill=BLACK, stroke=None),
        circle(16, 16, 9, fill=SILVER, sw=1),
        path("M16 7a9 9 0 010 18z", fill=BLACK, stroke=None),
    ))


def appbar_crop() -> str:
    return "".join((
        path("M7 2v23h23", sw=3),
        path("M2 7h23v23", sw=3),
        path("M12 12h8v8h-8z", sw=1),
        line(12, 12, 20, 20, sw=1),
        line(20, 12, 12, 20, sw=1),
    ))


def pokeball() -> str:
    return "".join((
        poly("3,9 15,4 15,15 3,19", fill=WINDOWS_RED, sw=1),
        poly("17,4 29,9 29,19 17,15", fill=WINDOWS_GREEN, sw=1),
        poly("3,21 15,17 15,28 3,23", fill=WINDOWS_BLUE, sw=1),
        poly("17,17 29,21 29,30 17,28", fill=WINDOWS_YELLOW, sw=1),
        line(15, 4, 15, 28, color=WHITE, sw=1),
        line(17, 4, 17, 28, color=BLACK, sw=1),
        path("M4 10l9-4v5L4 15z", fill=WHITE, stroke=None),
        path("M18 6l9 4v5l-9-4z", fill=WHITE, stroke=None),
    ))


def appbar_rotation() -> str:
    return "".join((
        button(3, 3, 26, 26),
        rect(9, 9, 14, 14, fill=WHITE, sw=2),
        path("M5 7V2h6", sw=2),
        path("M5 6c5-5 14-5 20 1", sw=2),
    ))


def appbar_tools() -> str:
    return "".join((
        bevel(3, 5, 26, 22, fill=SILVER, shadow=True),
        path("M10 5v-2h12v3", sw=2),
        rect(2, 10, 28, 3, fill=DARK, stroke=None),
        poly("8 25l13-13 3 3-13 13z", fill=BLACK, stroke=None),
        rect(5, 22, 5, 5, fill=WHITE, sw=1),
    ))


def texture_box() -> str:
    out = [bevel(3, 3, 26, 26, fill=SILVER, shadow=True)]
    for y in range(6, 27, 4):
        for x in range(6, 27, 4):
            if ((x - 6) // 4 + (y - 6) // 4) % 2 == 0:
                out.append(rect(x, y, 3, 3, fill=BLACK, stroke=None))
    return "".join(out)


def simpleui_authors() -> str:
    return "".join((
        circle(12, 10, 5, fill=SILVER, sw=2),
        circle(23, 8, 4, fill=SILVER, sw=2),
        path("M3 29v-3c0-5 4-8 9-8s9 3 9 8v3z", fill=SILVER, sw=2),
        path("M20 18c5 0 9 3 9 8v3h-6v-3", fill=SILVER, sw=2),
        line(6, 22, 9, 22, color=WHITE, sw=1),
    ))


def simpleui_bookmark_browser() -> str:
    return document(3, 3, 17, 26, lines=4) + bookmark_icon()


def simpleui_collection_back() -> str:
    return folder_icon() + button(
        13, 14, 13, 10, path("M22 16l-5 3 5 3", fill=BLACK, stroke=None)
    )


def simpleui_collections() -> str:
    return "".join((
        bevel(9, 3, 19, 16, fill=SILVER, shadow=True),
        bevel(5, 8, 19, 16, fill=SILVER, shadow=True),
        bevel(2, 14, 19, 15, fill=SILVER, shadow=True),
        line(5, 20, 18, 20, sw=1),
        line(8, 24, 18, 24, sw=1),
    ))


def simpleui_continue() -> str:
    return book() + button(
        19, 12, 11, 9, poly("23,14 29,16.5 23,19", fill=BLACK, stroke=None)
    )


def simpleui_frontlight() -> str:
    return "".join((
        button(5, 4, 22, 25),
        circle(16, 13, 7, fill=WHITE, sw=2),
        rect(13, 20, 6, 2, fill=BLACK, stroke=None),
        rect(14, 23, 4, 2, fill=DARK, stroke=None),
        path("M16 1v3M4 13H1M31 13h-3M7 4L5 2M25 4l2-2", sw=1),
    ))


def simpleui_history() -> str:
    return "".join((
        button(2, 3, 28, 27),
        circle(17, 17, 9, fill=WHITE, sw=2),
        rect(16, 10, 2, 8, fill=BLACK, stroke=None),
        poly("18,17 24,21 23,23 16,18", fill=BLACK, stroke=None),
        path("M6 9V3h6", sw=2),
        path("M5 8c3-5 9-6 14-4", sw=2),
    ))


def simpleui_library() -> str:
    return "".join((
        bevel(2, 5, 28, 24, fill=SILVER, shadow=True),
        rect(6, 9, 5, 16, fill=WHITE, sw=1),
        rect(13, 9, 5, 16, fill=WHITE, sw=1),
        rect(20, 9, 6, 16, fill=WHITE, sw=1),
        line(5, 26, 27, 26, sw=2),
    ))


def simpleui_night_mode() -> str:
    return "".join((
        button(2, 2, 28, 28),
        path(
            "M25 5C16 6 10 13 12 21c2 8 11 11 18 6-5 6-15 6-20-1C4 18 8 8 17 5c3-1 6-1 8 0z",
            fill=BLACK,
            stroke=None,
        ),
        circle(8, 8, 1, fill=WHITE, stroke=None),
        rect(24, 7, 2, 2, fill=WHITE, stroke=None),
    ))


def simpleui_power() -> str:
    return "".join((
        button(3, 3, 26, 26),
        line(16, 6, 16, 16, sw=3),
        path("M9 9a10 10 0 1014 0", sw=2),
    ))


def simpleui_qa_group() -> str:
    return "".join(
        button(x, y, 11, 11, rect(x + 3, y + 3, 5, 5, fill=WHITE))
        for x, y in ((2, 2), (19, 2), (2, 19), (19, 19))
    )


def simpleui_qa_plugin() -> str:
    return "".join((
        button(4, 7, 24, 20),
        bevel(10, 11, 13, 12, fill=LIGHT),
        line(13, 11, 13, 5, sw=2),
        line(20, 11, 20, 5, sw=2),
        line(16, 24, 16, 29, sw=2),
        rect(14, 16, 5, 2, fill=BLACK, stroke=None),
    ))


def simpleui_random_document() -> str:
    return "".join((
        document(4, 3, 22, 26, lines=0),
        rect(10, 10, 3, 3, fill=BLACK, stroke=None),
        rect(17, 10, 3, 3, fill=BLACK, stroke=None),
        rect(13, 15, 3, 3, fill=SILVER, sw=1),
        rect(10, 20, 3, 3, fill=BLACK, stroke=None),
        rect(17, 20, 3, 3, fill=BLACK, stroke=None),
    ))


def simpleui_recent() -> str:
    return "".join((
        button(2, 3, 28, 27),
        circle(16, 16, 9, fill=WHITE, sw=2),
        rect(15, 9, 2, 8, fill=BLACK, stroke=None),
        poly("17,16 23,20 22,22 15,17", fill=BLACK, stroke=None),
    ))


def simpleui_series() -> str:
    return "".join(
        (
            bevel(4, 4, 24, 6, fill=SILVER),
            bevel(4, 13, 24, 6, fill=SILVER),
            bevel(4, 22, 24, 6, fill=SILVER),
            rect(8, 4, 2, 6, fill=BLACK, stroke=None),
            rect(8, 13, 2, 6, fill=BLACK, stroke=None),
            rect(8, 22, 2, 6, fill=BLACK, stroke=None),
        )
    )


def simpleui_stats_calendar() -> str:
    return "".join(
        (
            bevel(3, 6, 26, 23, fill=SILVER, shadow=True),
            rect(5, 12, 22, 15, fill=WHITE),
            rect(5, 7, 22, 5, fill=DARK, stroke=None),
            line(10, 3, 10, 8, sw=2),
            line(22, 3, 22, 8, sw=2),
            *(
                rect(x, y, 3, 3, fill=BLACK, stroke=None)
                for y in (16, 22)
                for x in (8, 14, 20)
            ),
        )
    )


def simpleui_tab_fm_settings() -> str:
    return folder_icon() + button(
        9,
        15,
        19,
        12,
        rect(12, 18, 13, 2, fill=BLACK, stroke=None),
        rect(12, 22, 13, 2, fill=BLACK, stroke=None),
        rect(14, 17, 3, 4, fill=WHITE, sw=1),
        rect(21, 21, 3, 4, fill=WHITE, sw=1),
    )


def simpleui_tab_qs_panel() -> str:
    out = [window(2, 3, 28, 26)]
    for y, knob in ((9, 2), (15, 7), (21, 4)):
        out.extend(
            (
                rect(6, y, 20, 2, fill=BLACK, stroke=None),
                bevel(6 + knob * 3, y - 2, 6, 6, fill=LIGHT),
            )
        )
    return "".join(out)


def simpleui_tags() -> str:
    return "".join((
        path("M3 4h13l13 13-12 12L3 15z", fill=SILVER, sw=2),
        circle(10, 10, 3, fill=WHITE, sw=2),
        line(11, 18, 20, 9, color=WHITE, sw=1),
    ))


def simpleui_menu() -> str:
    return button(
        3,
        4,
        26,
        24,
        rect(7, 9, 18, 3, fill=BLACK, stroke=None),
        rect(7, 15, 18, 3, fill=BLACK, stroke=None),
        rect(7, 21, 18, 3, fill=BLACK, stroke=None),
    )


def build_simpleui_icon(name: str) -> str | None:
    fixed = {
        "authors": simpleui_authors,
        "bookmark_browser": simpleui_bookmark_browser,
        "coll_back": simpleui_collection_back,
        "collections": simpleui_collections,
        "continue": simpleui_continue,
        "folder": folder_icon,
        "frontlight": simpleui_frontlight,
        "history": simpleui_history,
        "homescreen": house,
        "library": simpleui_library,
        "menu": simpleui_menu,
        "night_mode": simpleui_night_mode,
        "power": simpleui_power,
        "qa_group": simpleui_qa_group,
        "qa_plugin": simpleui_qa_plugin,
        "random_document": simpleui_random_document,
        "recent": simpleui_recent,
        "series": simpleui_series,
        "settings": settings_sliders,
        "stats_calendar": simpleui_stats_calendar,
        "tab_filebrowser": folder_icon,
        "tab_fm_settings": simpleui_tab_fm_settings,
        "tab_navigation": book,
        "tab_qs_panel": simpleui_tab_qs_panel,
        "tab_tools": appbar_tools,
        "tab_typeset": appbar_typeset,
        "tags": simpleui_tags,
    }
    if name in fixed:
        return fixed[name]()
    if name == "chevron_left":
        return chevron("left")
    if name == "chevron_right":
        return chevron("right")
    if name == "favorites":
        return star("full")
    if name == "pager_first":
        return chevron("first")
    if name == "pager_last":
        return chevron("last")
    if name == "search":
        return magnifier()
    if name == "wifi_toggle":
        return network_icon()
    return None


def build_icon(name: str) -> str | None:
    if name.startswith("align."):
        return align_lines(name.split(".", 1)[1])
    if name == "appbar.filebrowser":
        return computer_icon()
    if name == "appbar.menu":
        return simpleui_menu()
    if name == "appbar.navigation":
        return book()
    if name == "appbar.pagefit":
        return appbar_pagefit()
    if name == "appbar.pageview":
        return pageview()
    if name == "appbar.pokeball":
        return pokeball()
    if name == "appbar.rotation":
        return appbar_rotation()
    if name == "appbar.search":
        return zoom("page")
    if name == "appbar.settings":
        return settings_sliders()
    if name == "appbar.textsize":
        return appbar_textsize()
    if name == "appbar.tools":
        return appbar_tools()
    if name == "appbar.typeset":
        return appbar_typeset()
    if name == "appbar.contrast":
        return appbar_contrast()
    if name == "appbar.crop":
        return appbar_crop()
    if name.startswith("back.top"):
        return button(
            2,
            2,
            28,
            28,
            rect(6, 6, 20, 3, fill=BLACK, stroke=None),
            poly("16,9 9,18 13,18 13,26 19,26 19,18 23,18", fill=BLACK, stroke=None),
        )
    if name == "book.opened":
        return book()
    if name == "bookmark":
        return bookmark_icon()
    if name == "cancel":
        return button(2, 2, 28, 28, close_x())
    if name == "check":
        return button(2, 2, 28, 28, checkmark())
    if name.startswith("chevron."):
        return chevron(name.split(".", 1)[1])
    if name == "close":
        return button(2, 2, 28, 28, close_x())
    if name.startswith("column."):
        return layout_columns({"one": 1, "two": 2, "three": 3}[name.split(".", 1)[1]])
    if name == "control.collapse":
        return button(2, 2, 28, 28, minusmark())
    if name.startswith("control.expand"):
        return button(2, 2, 28, 28, plusmark())
    if name.startswith("cre.render."):
        state = name.rsplit(".", 1)[1]
        out = [document(5, 2, 20, 27, lines=2)]
        if state == "partial":
            out.append(rect(8, 14, 14, 6, fill=DARK, sw=1))
        elif state == "ready":
            out.append(checkmark())
        elif state == "reload":
            out.extend((path("M10 15a6 6 0 019-2", sw=2), path("M22 8v6h-6", sw=2)))
        else:
            out.append(poly("9,12 21,12 15,18 21,25 9,25 15,18", fill=SILVER, sw=1))
        return "".join(out)
    if name.startswith("direction."):
        return direction_icon(name)
    if name.startswith("dogear."):
        return dogear(name.split(".")[1])
    if name == "edit":
        return pencil()
    if name == "exit":
        return "".join(
            (
                bevel(2, 4, 16, 24, fill=SILVER, shadow=True),
                rect(5, 8, 9, 17, fill=WHITE),
                rect(5, 8, 2, 2, fill=BLACK, stroke=None),
                line(19, 16, 30, 16, sw=3),
                poly("31,16 24,10 24,22", fill=BLACK, stroke=None),
            )
        )
    if name == "home":
        return house()
    if name == "info":
        return button(
            3,
            3,
            26,
            26,
            circle(16, 10, 3, fill=BLACK, stroke=None),
            rect(14, 14, 4, 11, fill=BLACK, stroke=None),
        )
    if name == "license":
        return document(3, 3, 20, 25, lines=4) + circle(24, 23, 5, fill=SILVER, sw=2) + path(
            "M22 27l-2 5 4-2 3 2-2-5", fill=BLACK, stroke=None
        )
    if name == "move.down":
        return button(
            3,
            3,
            26,
            26,
            rect(14, 5, 4, 15, fill=BLACK, stroke=None),
            poly("16,27 8,18 24,18", fill=BLACK, stroke=None),
        )
    if name == "move.up":
        return button(
            3,
            3,
            26,
            26,
            rect(14, 10, 4, 15, fill=BLACK, stroke=None),
            poly("16,4 8,13 24,13", fill=BLACK, stroke=None),
        )
    if name.startswith("notice-"):
        return notice(name.split("-", 1)[1])
    if name == "plus":
        return button(2, 2, 28, 28, plusmark())
    if name.startswith("position.marker"):
        out = [
            button(3, 3, 26, 26),
            poly("8,7 25,7 16,24", fill=SILVER, sw=2),
            rect(13, 9, 6, 10, fill=WHITE, stroke=None),
        ]
        if name.endswith(".top"):
            out.append(rect(6, 5, 20, 2, fill=BLACK, stroke=None))
        return "".join(out)
    if name.startswith("rotation."):
        return rotation_icon(name)
    if name.startswith("star."):
        return star(name.split(".", 1)[1])
    if name == "texture-box":
        return texture_box()
    if name == "triangle":
        return poly("4,27 16,4 28,27", fill=SILVER, sw=2) + path(
            "M16 10l-6 13h12z", fill=WHITE, stroke=None
        )
    if name.startswith("wifi"):
        if name == "wifi":
            return wifi(3, False)
        secure = ".secure." in name
        level = int(name.rsplit(".", 1)[1]) // 25
        return wifi(level, secure)
    if name.startswith("zoom."):
        return zoom(name.split(".", 1)[1])
    return None


def render_svg(name: str, body: str) -> str:
    title = html.escape(name.replace(".", " ").replace("-", " "))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" '
        'viewBox="0 0 32 32" shape-rendering="crispEdges">\n'
        f"  <title>{title}</title>\n"
        '  <g stroke="#000000" stroke-linecap="square" stroke-linejoin="miter">\n'
        f"    {body}\n"
        "  </g>\n"
        "</svg>\n"
    )


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    for name in sorted(EXPECTED_ICONS):
        body = build_icon(name)
        if body is None:
            raise RuntimeError(f"No drawing for icon: {name}")
        (ICON_DIR / f"{name}.svg").write_text(render_svg(name, body), encoding="utf-8")

    leftovers = {path.stem for path in ICON_DIR.glob("*.svg")} - EXPECTED_ICONS
    if leftovers:
        raise RuntimeError(f"Generated set does not cover: {sorted(leftovers)}")

    SIMPLEUI_ICON_DIR.mkdir(parents=True, exist_ok=True)
    for name in sorted(SIMPLEUI_ICON_NAMES):
        body = build_simpleui_icon(name)
        if body is None:
            raise RuntimeError(f"No drawing for SimpleUI icon: {name}")
        (SIMPLEUI_ICON_DIR / f"{name}.svg").write_text(
            render_svg(name, body), encoding="utf-8"
        )

    simpleui_leftovers = {
        path.stem for path in SIMPLEUI_ICON_DIR.glob("*.svg")
    } - SIMPLEUI_ICON_NAMES
    if simpleui_leftovers:
        raise RuntimeError(
            f"Generated SimpleUI set does not cover: {sorted(simpleui_leftovers)}"
        )

    print(f"Generated {len(EXPECTED_ICONS)} KOReader icons in {ICON_DIR}")
    print(f"Generated {len(SIMPLEUI_ICON_NAMES)} SimpleUI icons in {SIMPLEUI_ICON_DIR}")


if __name__ == "__main__":
    main()
