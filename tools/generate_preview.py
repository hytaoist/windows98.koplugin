#!/usr/bin/env python3
"""Generate Windows 98 README previews with the shipped icons and fonts."""

from __future__ import annotations

import base64
import html
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_DIR = ROOT / "preview"
FONT_PATH = ROOT / "assets" / "fonts" / "Windows98UI.ttf"
FONT_BOLD_PATH = ROOT / "assets" / "fonts" / "Windows98UI-Bold.ttf"
SPONSOR_PATH = ROOT / "assets" / "sponsor" / "wechat-reward.jpg"
CHROME_CANDIDATES = (
    os.environ.get("CHROME_BIN"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
)

BLACK = "#000000"
WHITE = "#ffffff"
SILVER = "#c0c0c0"
LIGHT = "#dfdfdf"
DARK = "#808080"
NAVY = "#000080"
BLUE = "#1084d0"
DESKTOP = "#008080"
DESKTOP_DARK = "#006868"
GOLD = "#f0c848"


def import_generator():
    import sys

    sys.path.insert(0, str(ROOT / "tools"))
    import generate_icons  # noqa: PLC0415

    return generate_icons


ICONS = import_generator()


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def font_css() -> str:
    regular = data_uri(FONT_PATH, "font/ttf")
    bold = data_uri(FONT_BOLD_PATH, "font/ttf")
    return (
        "@font-face {"
        "font-family: 'Windows98UI';"
        f"src: url({regular}) format('truetype');"
        "font-weight: 400;"
        "}"
        "@font-face {"
        "font-family: 'Windows98UI';"
        f"src: url({bold}) format('truetype');"
        "font-weight: 700;"
        "}"
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str | None = None,
    stroke: str | None = None,
    sw: float = 1,
) -> str:
    attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
    attrs.append(f'fill="{fill}"' if fill else 'fill="none"')
    if stroke:
        attrs.extend((f'stroke="{stroke}"', f'stroke-width="{sw}"'))
    return f"<rect {' '.join(attrs)}/>"


def text(
    x: float,
    y: float,
    value: object,
    *,
    size: int = 24,
    fill: str = BLACK,
    anchor: str = "start",
    bold: bool = False,
    spacing: float = 0,
) -> str:
    weight = 700 if bold else 400
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="Windows98UI" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        f'letter-spacing="{spacing}">{esc(value)}</text>'
    )


def bevel(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = SILVER,
    sunken: bool = False,
    shadow: bool = False,
    edge: int = 3,
) -> str:
    out = []
    if shadow:
        out.append(rect(x + 8, y + 8, w, h, fill=BLACK))
    out.append(rect(x, y, w, h, fill=BLACK))
    out.append(rect(x + edge, y + edge, w - edge * 2, h - edge * 2, fill=fill))
    high = DARK if sunken else WHITE
    low = WHITE if sunken else DARK
    inner_high = BLACK if sunken else LIGHT
    inner_low = LIGHT if sunken else BLACK
    out.extend(
        (
            rect(x + edge, y + edge, w - edge * 2, edge, fill=high),
            rect(x + edge, y + edge, edge, h - edge * 2, fill=high),
            rect(x + edge, y + h - edge * 2, w - edge * 2, edge, fill=low),
            rect(x + w - edge * 2, y + edge, edge, h - edge * 2, fill=low),
            rect(x + edge * 2, y + edge * 2, w - edge * 4, 2, fill=inner_high),
            rect(x + edge * 2, y + edge * 2, 2, h - edge * 4, fill=inner_high),
            rect(x + edge * 2, y + h - edge * 2 - 2, w - edge * 4, 2, fill=inner_low),
            rect(x + w - edge * 2 - 2, y + edge * 2, 2, h - edge * 4, fill=inner_low),
        )
    )
    return "".join(out)


def icon(name: str, x: float, y: float, size: float, *, simpleui: bool = False) -> str:
    body = ICONS.build_simpleui_icon(name) if simpleui else ICONS.build_icon(name)
    if body is None:
        raise RuntimeError(f"Missing preview icon: {name}")
    scale = size / 32
    return (
        f'<g transform="translate({x},{y}) scale({scale})" '
        f'stroke-linecap="square" stroke-linejoin="miter">{body}</g>'
    )


def sponsor_image(x: float, y: float, size: float) -> str:
    href = data_uri(SPONSOR_PATH, "image/jpeg")
    return (
        f'<image x="{x}" y="{y}" width="{size}" height="{size}" '
        f'href="{href}" preserveAspectRatio="xMidYMid meet"/>'
    )


def svg_document(width: int, height: int, body: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" shape-rendering="crispEdges">\n'
        f"<style>{font_css()}</style>\n"
        '<defs><pattern id="desktop-dots" width="8" height="8" '
        'patternUnits="userSpaceOnUse">'
        f'<rect width="8" height="8" fill="{DESKTOP}"/>'
        f'<rect width="4" height="4" fill="{DESKTOP_DARK}"/>'
        "</pattern></defs>\n"
        f"{body}\n"
        "</svg>\n"
    )


def render_svg(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    chrome = next((path for path in CHROME_CANDIDATES if path and Path(path).exists()), None)
    if chrome:
        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                f"--screenshot={png_path}",
                f"--window-size={width},{height}",
                svg_path.resolve().as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    sips = shutil.which("sips")
    if sips:
        subprocess.run(
            [sips, "-s", "format", "png", str(svg_path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    raise RuntimeError("Chrome/Chromium or sips is required to render previews")


def window_frame(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    *,
    title_icon: str = "appbar.pokeball",
) -> tuple[list[str], int]:
    out = [bevel(x, y, w, h, shadow=True, edge=3)]
    title_h = 58
    out.append(rect(x + 6, y + 6, w - 12, title_h, fill=NAVY))
    out.append(rect(x + 6, y + 6, w - 12, 4, fill=BLUE))
    out.append(rect(x + 6, y + 6, w - 12, 2, fill=WHITE))
    out.append(icon(title_icon, x + 16, y + 13, 34))
    out.append(text(x + w // 2, y + 44, title, size=29, fill=WHITE, anchor="middle", bold=True))
    controls = (
        (x + w - 150, "_"),
        (x + w - 104, "□"),
        (x + w - 58, "×"),
    )
    for bx, symbol in controls:
        out.append(bevel(bx, y + 12, 40, 38, edge=2))
        out.append(text(bx + 20, y + 41, symbol, size=24, anchor="middle", bold=True))
    return out, y + 6 + title_h + 4


def taskbar(width: int, height: int) -> list[str]:
    top = height - 64
    out = [
        bevel(0, top, width, 64, edge=2),
        bevel(8, top + 8, 140, 48, edge=2),
        icon("appbar.pokeball", 18, top + 14, 34),
        text(58, top + 40, "Start", size=22, bold=True),
    ]
    for label, bx, bw in (
        ("KOReader 98 - Documents", 160, 330),
        ("My Computer", 500, 190),
        ("Recycle Bin", 700, 170),
    ):
        out.append(bevel(bx, top + 8, bw, 48, edge=2))
        out.append(text(bx + 16, top + 40, label, size=20))
    out.append(bevel(width - 225, top + 8, 217, 48, edge=2, sunken=True))
    out.append(icon("wifi_toggle", width - 212, top + 14, 31, simpleui=True))
    out.append(text(width - 166, top + 40, "10:09 AM", size=19))
    return out


def desktop_background(width: int, height: int) -> list[str]:
    out = [rect(0, 0, width, height, fill="url(#desktop-dots)")]
    desktop_items = (
        ("appbar.filebrowser", "My Computer", 58, 45),
        ("book.opened", "KOReader", 58, 205),
        ("folder", "Books", 58, 365, True),
    )
    for item in desktop_items:
        icon_name, label, x, y = item[:4]
        simpleui = len(item) == 5 and item[4]
        out.append(icon(icon_name, x + 4, y, 58, simpleui=simpleui))
        out.append(text(x + 33, y + 94, label, size=20, fill=WHITE, anchor="middle"))
    return out


def main_window_svg() -> str:
    width, height = 1200, 1320
    x, y, w, h = 160, 32, 1000, 1180
    out = desktop_background(width, height)
    window, menu_y = window_frame(x, y, w, h, "KOReader 98 - Documents")

    menu_y += 2
    menu_h = 52
    out.extend(window)
    out.append(bevel(x + 6, menu_y, w - 12, menu_h, edge=2))
    menu_items = (("File", 26), ("Edit", 108), ("View", 198), ("Go", 302), ("Favorites", 388), ("Tools", 548))
    for label, offset in menu_items:
        out.append(text(x + offset, menu_y + 34, label, size=21))
    out.append(text(x + w - 24, menu_y + 34, "10:09", size=21, anchor="end"))

    toolbar_y = menu_y + menu_h + 8
    out.append(bevel(x + 6, toolbar_y, w - 12, 78, edge=2))
    toolbar = (
        ("chevron.left", "Back"),
        ("chevron.right", "Forward"),
        ("back.top", "Up"),
        ("appbar.search", "Search"),
        ("appbar.pageview", "Views"),
    )
    for index, (icon_name, label) in enumerate(toolbar):
        bx = x + 18 + index * 142
        out.append(bevel(bx, toolbar_y + 10, 42, 42, edge=2))
        out.append(icon(icon_name, bx + 7, toolbar_y + 15, 28))
        out.append(text(bx + 50, toolbar_y + 40, label, size=19))
    out.append(rect(x + 728, toolbar_y + 12, 2, 52, fill=DARK))

    address_y = toolbar_y + 86
    out.append(text(x + 20, address_y + 33, "Address", size=19))
    out.append(bevel(x + 111, address_y, w - 132, 48, fill=WHITE, sunken=True, edge=2))
    out.append(icon("appbar.filebrowser", x + 123, address_y + 8, 30))
    out.append(text(x + 164, address_y + 32, r"/mnt/us/documents", size=20))
    out.append(bevel(x + w - 168, address_y, 42, 48, edge=2))
    out.append(text(x + w - 147, address_y + 33, "▼", size=17, anchor="middle"))

    header_y = address_y + 60
    out.append(bevel(x + 6, header_y, w - 28, 42, edge=2))
    out.append(text(x + 88, header_y + 29, "Name", size=19, bold=True))
    out.append(text(x + 704, header_y + 29, "Size", size=19, bold=True))
    out.append(text(x + 805, header_y + 29, "Modified", size=19, bold=True))

    rows = (
        ("Books", "folder", "24 items", "Today 09:41", True),
        ("Articles", "folder", "18 items", "Yesterday", True),
        ("KOReader Manual.pdf", "license", "5.1 MB", "Oct 25", False),
        ("The Design of Everyday Things.epub", "book.opened", "2.8 MB", "Oct 27", False),
        ("Notes.txt", "edit", "12 KB", "Oct 24", False),
        ("Screensaver.png", "texture-box", "940 KB", "Oct 20", False),
        ("Dictionary", "folder", "6 items", "Oct 18", True),
        ("Windows-theme.css", "appbar.settings", "8 KB", "Oct 12", False),
    )
    row_y = header_y + 46
    row_h = 91
    for index, (name, icon_name, size_text, date_text, simpleui) in enumerate(rows):
        top = row_y + index * row_h
        selected = index == 3
        fill = NAVY if selected else WHITE
        ink = WHITE if selected else BLACK
        out.append(rect(x + 8, top, w - 52, row_h - 2, fill=fill))
        if not selected:
            out.append(rect(x + 8, top + row_h - 3, w - 52, 1, fill=LIGHT))
        out.append(icon(icon_name, x + 22, top + 22, 42, simpleui=simpleui))
        out.append(text(x + 82, top + 57, name, size=21, fill=ink))
        out.append(text(x + 704, top + 57, size_text, size=19, fill=ink))
        out.append(text(x + 805, top + 57, date_text, size=19, fill=ink))

    scroll_x = x + w - 42
    out.append(bevel(scroll_x, header_y + 46, 28, 728, fill=LIGHT, sunken=True, edge=2))
    out.append(bevel(scroll_x + 6, header_y + 113, 16, 245, edge=2))
    out.append(text(scroll_x + 14, header_y + 90, "▲", size=16, anchor="middle"))
    out.append(text(scroll_x + 14, header_y + 759, "▼", size=16, anchor="middle"))

    status_y = row_y + len(rows) * row_h + 14
    out.append(bevel(x + 6, status_y, w - 12, 60, edge=2))
    for offset, cell_width in ((20, 360), (386, 280), (672, 282)):
        out.append(rect(x + offset, status_y + 10, cell_width, 40, fill=LIGHT))
    out.append(text(x + 30, status_y + 38, "12 objects", size=19))
    out.append(text(x + 396, status_y + 38, "1.2 GB free", size=19))
    out.append(icon("wifi.secure.100", x + 682, status_y + 14, 30))
    out.append(text(x + 720, status_y + 38, "Connected", size=18))
    out.append(icon("power", x + 858, status_y + 14, 30, simpleui=True))
    out.append(text(x + 898, status_y + 38, "87%", size=18))

    px, py = 742, 650
    cursor = f"M{px},{py} v72 l14,-14 l11,25 l14,-7 l-11,-24 h17 z"
    out.append(f'<path d="{cursor}" fill="{WHITE}" stroke="{BLACK}" stroke-width="3"/>')
    out.extend(taskbar(width, height))
    return svg_document(width, height, "".join(out))


def about_window_svg() -> str:
    width, height = 1200, 1600
    out = desktop_background(width, height)
    x, y, w, h = 190, 210, 820, 990
    out.append(bevel(x, y, w, h, shadow=True, edge=3))
    out.append(rect(x + 6, y + 6, w - 12, 58, fill=NAVY))
    out.append(rect(x + 6, y + 6, w - 12, 4, fill=BLUE))
    out.append(rect(x + 6, y + 6, w - 12, 2, fill=WHITE))
    out.append(icon("appbar.pokeball", x + 16, y + 13, 34))
    out.append(
        text(x + w // 2, y + 44, "About Windows 98 for KOReader",
             size=26, fill=WHITE, anchor="middle", bold=True)
    )
    out.append(bevel(x + w - 56, y + 12, 40, 38, edge=2))
    out.append(text(x + w - 36, y + 42, "×", size=24, anchor="middle", bold=True))

    out.append(bevel(x + 42, y + 98, 116, 116, shadow=True, edge=3))
    out.append(icon("appbar.pokeball", x + 58, y + 114, 84))
    out.append(text(x + 188, y + 132, "Windows 98 for KOReader", size=29, bold=True))
    out.append(text(x + 188, y + 172, "Version 1.0.0", size=21))
    out.append(rect(x + 42, y + 238, w - 84, 2, fill=DARK))
    out.append(text(x + 42, y + 282, "103 KOReader icons · 34 SimpleUI icons", size=20))
    out.append(text(x + 42, y + 316, "Silver shell · navy title bars · two-stage bevels", size=20))
    out.append(text(x + 42, y + 350, "Windows98UI regular + bold · Storefront / OTA", size=20))
    out.append(text(x + 42, y + 416, "Support continued maintenance", size=21, bold=True))

    out.append(bevel(x + 42, y + 440, w - 84, 210, fill=WHITE, sunken=True, edge=2))
    out.append(bevel(x + 58, y + 456, 164, 164, fill=WHITE, sunken=True, edge=2))
    out.append(sponsor_image(x + 64, y + 462, 152))
    out.append(icon("star.full", x + 248, y + 466, 46))
    out.append(text(x + 306, y + 494, "Sponsor this project", size=21, bold=True))
    out.append(text(x + 248, y + 538, "Scan with WeChat", size=20))
    out.append(text(x + 248, y + 570, "Sponsor this project", size=20))
    out.append(text(x + 248, y + 602, "Bundled offline - no network needed", size=17, fill=DARK))

    out.append(bevel(x + 42, y + 690, 236, 64, edge=3))
    out.append(text(x + 160, y + 732, "Sponsor", size=21, anchor="middle", bold=True))
    out.append(bevel(x + 296, y + 690, 196, 64, edge=3))
    out.append(text(x + 394, y + 732, "Close", size=21, anchor="middle", bold=True))
    out.append(text(x + 42, y + 840, "github.com/hytaoist/windows98.koplugin", size=18, fill=DARK))
    out.append(text(x + 42, y + 876, "Unofficial fan theme. Not affiliated with Microsoft.", size=17, fill=DARK))
    out.extend(taskbar(width, height))
    return svg_document(width, height, "".join(out))


def icon_sheet_svg(
    names: list[str],
    title: str,
    *,
    simpleui: bool = False,
    cols: int = 8,
) -> tuple[str, int, int]:
    cell_w = 132 if simpleui else 142
    cell_h = 164
    margin = 38
    header = 94
    rows = (len(names) + cols - 1) // cols
    width = margin * 2 + cols * cell_w
    height = header + margin + rows * cell_h
    out = [rect(0, 0, width, height, fill=SILVER)]
    out.append(rect(margin, 30, width - margin * 2, 3, fill=BLACK))
    out.append(text(margin, 72, title, size=27, bold=True))
    out.append(text(width - margin, 72, f"{len(names)} icons", size=19, anchor="end", fill=DARK))
    for index, name in enumerate(names):
        row, col = divmod(index, cols)
        x = margin + col * cell_w
        y = header + row * cell_h
        out.append(bevel(x + 12, y + 6, 108, 108, fill=WHITE, edge=2))
        out.append(icon(name, x + 26, y + 20, 80, simpleui=simpleui))
        out.append(text(x + 66, y + 145, name[:17], size=15, anchor="middle"))
    return svg_document(width, height, "".join(out)), width, height


def write_and_render(svg_name: str, png_name: str, svg: str, width: int, height: int) -> None:
    svg_path = PREVIEW_DIR / svg_name
    png_path = PREVIEW_DIR / png_name
    svg_path.write_text(svg, encoding="utf-8")
    render_svg(svg_path, png_path, width, height)


def main() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    write_and_render(
        "windows98-ui.svg",
        "windows98-ui.png",
        main_window_svg(),
        1200,
        1320,
    )
    write_and_render(
        "windows98-about.svg",
        "windows98-about.png",
        about_window_svg(),
        1200,
        1600,
    )

    koreader_sheet, width, height = icon_sheet_svg(
        sorted(ICONS.EXPECTED_ICONS),
        "Windows 98 for KOReader / KOReader icon set",
    )
    write_and_render("icon-sheet.svg", "icon-sheet.png", koreader_sheet, width, height)

    simpleui_sheet, width, height = icon_sheet_svg(
        sorted(ICONS.SIMPLEUI_ICON_NAMES),
        "Windows 98 for KOReader / SimpleUI icon pack",
        simpleui=True,
        cols=6,
    )
    write_and_render(
        "simpleui-icon-sheet.svg",
        "simpleui-icon-sheet.png",
        simpleui_sheet,
        width,
        height,
    )
    print(
        "Generated preview/windows98-ui.png, preview/windows98-about.png, "
        "preview/icon-sheet.png and preview/simpleui-icon-sheet.png"
    )


if __name__ == "__main__":
    main()
