"""Build the Housemade Studio logo files as SVG, with the letters outlined.

Usage:
    python make_logo.py <fonts-dir> <out-dir>

<fonts-dir> holds the Fontsource WOFF2 files for Barlow Condensed 700 and
Barlow 600 (npm pack @fontsource/barlow-condensed@5.1.0 @fontsource/barlow@5.1.0,
then take files/*-latin-*-normal.woff2). Needs fontTools and brotli.

The mark is a gold roofline over a purple H: the house, and House's initial.
"""
import math
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

PURPLE = "#241773"
GOLD = "#c79a2c"
GOLD_TEXT = "#7d611c"  # gold that reads on ivory (5.54:1)
IVORY = "#fbf9f3"
BLACK = "#000000"
WHITE = "#ffffff"

COLORWAYS = {
    # name: (H and wordmark, roof, STUDIO line, background or None)
    "color": (PURPLE, GOLD, GOLD_TEXT, None),
    "reverse": (IVORY, GOLD, GOLD, None),
    "black": (BLACK, BLACK, BLACK, None),
    "white": (WHITE, WHITE, WHITE, None),
}


def text_path(font_file, text, size, tracking_em, x=0.0, baseline=0.0):
    """Outline `text` at `size` px; returns (svg path d, width in px)."""
    font = TTFont(font_file)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(glyphs)
    cursor = x
    track = tracking_em * size
    names = [cmap[ord(c)] for c in text]
    for i, name in enumerate(names):
        tp = TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline))
        glyphs[name].draw(tp)
        cursor += glyphs[name].width * scale
        if i < len(names) - 1:
            cursor += track
    return pen.getCommands(), cursor - x


def roof_polygon(left, apex_x, apex_y, right, eave_y, thickness):
    """A chevron with horizontal cuts at the eaves, `thickness` measured
    square to each arm."""
    def offset_line(p, q, d):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dy)
        nx, ny = dy / n, -dx / n  # left-hand normal
        return (p[0] + nx * d, p[1] + ny * d), (q[0] + nx * d, q[1] + ny * d)

    def intersect(a1, a2, b1, b2):
        x1, y1 = a1; x2, y2 = a2; x3, y3 = b1; x4, y4 = b2
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        return px, py

    A, B, C = (left, eave_y), (apex_x, apex_y), (right, eave_y)
    h = thickness / 2
    lo1, lo2 = offset_line(A, B, h)    # left arm, upper edge
    li1, li2 = offset_line(A, B, -h)   # left arm, lower edge
    ro1, ro2 = offset_line(B, C, h)    # right arm, upper edge
    ri1, ri2 = offset_line(B, C, -h)   # right arm, lower edge
    eave = ((0, eave_y), (1, eave_y))
    pts = [
        intersect(lo1, lo2, *eave), intersect(lo1, lo2, ro1, ro2), intersect(ro1, ro2, *eave),
        intersect(ri1, ri2, *eave), intersect(li1, li2, ri1, ri2), intersect(li1, li2, *eave),
    ]
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def mark(ox, oy, size, house, roof):
    """The mark in a `size` square at (ox, oy): roof over an H."""
    s = size / 100
    def r(x, y, w, hgt):
        return f'<rect x="{ox + x * s:.2f}" y="{oy + y * s:.2f}" width="{w * s:.2f}" height="{hgt * s:.2f}" fill="{house}"/>'
    roof_d = roof_polygon(ox + 6 * s, ox + 50 * s, oy + 12 * s, ox + 94 * s, oy + 46 * s, 9 * s)
    return "\n".join([
        f'<path d="{roof_d}" fill="{roof}"/>',
        r(22, 52, 11, 44), r(67, 52, 11, 44), r(22, 69, 56, 9),
    ])


def svg(width, height, body, title, bg=None):
    bg_rect = f'<rect width="{width}" height="{height}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
            f'width="{width:.0f}" height="{height:.0f}" role="img" aria-label="{title}">\n'
            f"<title>{title}</title>\n{bg_rect}{body}\n</svg>\n")


def main(fonts_dir, out_dir):
    fonts_dir, out_dir = Path(fonts_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cond = fonts_dir / "barlow-condensed-latin-700-normal.woff2"
    body = fonts_dir / "barlow-latin-600-normal.woff2"

    for name, (house, roof, sub, bg) in COLORWAYS.items():
        # Horizontal: mark, then HOUSEMADE over a tracked STUDIO line.
        word_d, word_w = text_path(cond, "HOUSEMADE", 96, 0.02, x=150, baseline=94)
        sub_d, sub_w = text_path(body, "STUDIO", 26, 0.42, x=154, baseline=132)
        width = 150 + max(word_w, sub_w + 4) + 16
        b = "\n".join([mark(10, 14, 124, house, roof),
                       f'<path d="{word_d}" fill="{house}"/>', f'<path d="{sub_d}" fill="{sub}"/>'])
        (out_dir / f"housemade-horizontal-{name}.svg").write_text(svg(width, 150, b, "Housemade Studio", bg))

        # Stacked: mark centred over the two lines.
        word_d, word_w = text_path(cond, "HOUSEMADE", 96, 0.02)
        sub_d, sub_w = text_path(body, "STUDIO", 26, 0.42)
        width = max(word_w, sub_w) + 40
        wx, sx = (width - word_w) / 2, (width - sub_w) / 2
        word_d, _ = text_path(cond, "HOUSEMADE", 96, 0.02, x=wx, baseline=262)
        sub_d, _ = text_path(body, "STUDIO", 26, 0.42, x=sx, baseline=304)
        b = "\n".join([mark(width / 2 - 85, 6, 170, house, roof),
                       f'<path d="{word_d}" fill="{house}"/>', f'<path d="{sub_d}" fill="{sub}"/>'])
        (out_dir / f"housemade-stacked-{name}.svg").write_text(svg(width, 320, b, "Housemade Studio", bg))

        # Mark alone.
        (out_dir / f"housemade-mark-{name}.svg").write_text(
            svg(120, 120, mark(10, 10, 100, house, roof), "Housemade Studio mark"))

    # App icon and favicon: full purple square so a circle crop stays clean.
    (out_dir / "housemade-icon.svg").write_text(
        svg(512, 512, mark(86, 76, 340, IVORY, GOLD), "Housemade Studio icon", bg=PURPLE))


if __name__ == "__main__":
    main(*sys.argv[1:3])
