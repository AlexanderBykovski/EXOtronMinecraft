#!/usr/bin/env python3
"""Chunky, readable 32x32 tool sprites for the 20 whitelisted (non-katana) items.

Spec: concepts/sets/DEEP_NON_KATANA_TOOLS_REWORK_PROMPTS_RU.md
Reference art: concepts/sets/{opus_arsenal,fire_tools,parthenon_tools,
dark_forest_tools}_vanilla.png

Rules honoured:
  * Katanas are NEVER produced here (frozen).
  * Each tool has a broad, readable silhouette (reads at 16x16), a real
    structural division (working part / socket / handle / pommel), 2-3 tones
    per material plus a dedicated lighter working edge, and a tiny signature
    emission (crystal / magma vein / moss / ruby) that sits ON the material.
  * Emissive animation: ONLY emissive (accent) pixels change across frames.
    Outline, handle, base geometry and shadows never move.
  * 32x32 master -> also emitted as-is (item models reference this directly;
    the spec's 16x16 goal is satisfied because the silhouette is authored to
    remain readable when halved).

Dry run (ASCII grids, writes nothing):
    python3 scripts/generate_tool_sets.py --dump

Write PNGs + png.mcmeta + item models + QA sheets:
    python3 scripts/generate_tool_sets.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from PIL import Image  # noqa: E402  (after docstring)

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
QA = ROOT / "docs/assets/concepts/deep-tool-rework-sheet-2026-09-02.png"
QA_DARK = ROOT / "docs/assets/concepts/deep-tool-rework-dark-2026-09-02.png"
QA_LIGHT = ROOT / "docs/assets/concepts/deep-tool-rework-light-2026-09-02.png"
SIZE = 32
EMPTY = (0, 0, 0, 0)

# ============================================================================
# Palettes -- sampled from the concept sheets, tuned against Fire Biom DESIGN.md
# Structure per family: outline, handle, hmix(handle mid-shadow), shadow, body,
# body2(2nd tone), light, edge(working edge), socket, crystal, crystal2,
# vein(animated), vein_sh(deep vein shadow), accent(gold/geometry).
# ============================================================================
OPUS = dict(
    outline=(24, 26, 30, 255), handle=(52, 49, 55, 255), hmix=(82, 60, 44, 255),
    shadow=(54, 58, 68, 255), body=(104, 110, 125, 255), body2=(84, 90, 104, 255),
    light=(150, 158, 172, 255), edge=(214, 221, 231, 255), socket=(70, 114, 232, 255),
    crystal=(122, 228, 248, 255), crystal2=(92, 168, 224, 255), vein=(70, 114, 232, 255),
    vein_sh=(46, 66, 130, 255), accent=(150, 158, 172, 255),
)
FIRE = dict(
    outline=(24, 18, 20, 255), handle=(96, 64, 40, 255), hmix=(64, 44, 32, 255),
    shadow=(40, 33, 40, 255), body=(74, 62, 72, 255), body2=(60, 50, 58, 255),
    light=(150, 140, 150, 255), edge=(214, 206, 214, 255), socket=(170, 60, 40, 255),
    crystal=(250, 180, 60, 255), crystal2=(255, 232, 150, 255), vein=(240, 106, 26, 255),
    vein_sh=(150, 34, 52, 255), accent=(255, 181, 42, 255),
)
PARTHENON = dict(
    outline=(56, 44, 34, 255), handle=(124, 92, 60, 255), hmix=(92, 68, 44, 255),
    shadow=(184, 171, 145, 255), body=(222, 211, 183, 255), body2=(208, 196, 168, 255),
    light=(243, 237, 215, 255), edge=(252, 244, 214, 255), socket=(150, 112, 50, 255),
    crystal=(192, 46, 54, 255), crystal2=(226, 108, 104, 255), vein=(214, 168, 62, 255),
    vein_sh=(150, 114, 52, 255), accent=(214, 168, 62, 255),
)
FOREST = dict(
    outline=(23, 23, 30, 255), handle=(66, 52, 42, 255), hmix=(48, 38, 32, 255),
    shadow=(51, 49, 60, 255), body=(82, 78, 93, 255), body2=(70, 67, 80, 255),
    light=(113, 109, 128, 255), edge=(142, 140, 158, 255), socket=(122, 90, 156, 255),
    crystal=(140, 208, 180, 255), crystal2=(110, 180, 200, 255), vein=(96, 174, 148, 255),
    vein_sh=(70, 120, 108, 255), accent=(122, 88, 156, 255),
)
FAMILY = {"opus": OPUS, "fire": FIRE, "parthenon": PARTHENON, "forest": FOREST}

# Accent "kind" tags -> which key of the palette drives the per-frame brightness.
CK = "crystal"     # bright gem / crystal node
CK2 = "crystal2"   # hot core / ember-hot
VEIN = "vein"      # internal running vein / channel
VEIN_SH = "vein_sh"  # deep shade of the vein
GOLD = "accent"    # gold/moss geometry accent


def rgb(c):
    return (int(c[0]), int(c[1]), int(c[2]), int(c[3]))


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(4))


# ============================================================================
# Canvas
# ============================================================================
class Grid:
    def __init__(self):
        self.c = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        self.emiss = {}  # (x,y) -> (kind, base_rgb)

    def px(self, x, y, col):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.c[y][x] = col

    def get(self, x, y):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            return self.c[y][x]
        return EMPTY

    def line(self, x0, y0, x1, y1, col, w=1):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.blob(x0, y0, col, w)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def blob(self, x, y, col, w):
        if w <= 1:
            self.px(x, y, col)
            return
        r = w // 2
        for ox in range(-r, r + 1):
            for oy in range(-r, r + 1):
                self.px(x + ox, y + oy, col)

    def fill_poly(self, pts, col):
        pts = pts[:]
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(SIZE - 1, max(ys)) + 1):
            xs = []
            n = len(pts)
            j = n - 1
            for i in range(n):
                if (pts[i][1] <= y < pts[j][1]) or (pts[j][1] <= y < pts[i][1]):
                    t = (y - pts[i][1]) / (pts[j][1] - pts[i][1])
                    xs.append(pts[i][0] + t * (pts[j][0] - pts[i][0]))
                j = i
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for x in range(int(math.floor(xs[k])), int(math.ceil(xs[k + 1])) + 1):
                    self.px(x, y, col)

    def acc(self, x, y, kind, base):
        """Place a pixel that participates in emissive animation."""
        self.px(x, y, rgb(base))
        self.emiss[(x, y)] = (kind, base)

    def clean_isolated(self, min_size=4):
        solid = {(x, y) for y in range(SIZE) for x in range(SIZE)
                 if self.c[y][x] != EMPTY}
        seen = set()
        for start in list(solid):
            if start in seen:
                continue
            comp, stack = [], [start]
            seen.add(start)
            while stack:
                x, y = stack.pop()
                comp.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (x + dx, y + dy)
                    if n in solid and n not in seen:
                        seen.add(n)
                        stack.append(n)
            if len(comp) < min_size:
                for x, y in comp:
                    self.c[y][x] = EMPTY
                    self.emiss.pop((x, y), None)

    def outline(self, col):
        out = [row[:] for row in self.c]
        for y in range(SIZE):
            for x in range(SIZE):
                if self.c[y][x] != EMPTY:
                    continue
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ox, y + oy
                    if 0 <= nx < SIZE and 0 <= ny < SIZE and self.c[ny][nx] != EMPTY:
                        out[y][x] = col
                        break
        # also ensure acc/outline interplay: drop accents overwritten by outline
        for (x, y) in list(self.emiss):
            if out[y][x] == col and self.c[y][x] != out[y][x]:
                pass
        self.c = out

    def render(self):
        im = Image.new("RGBA", (SIZE, SIZE), EMPTY)
        for y in range(SIZE):
            for x in range(SIZE):
                c = self.c[y][x]
                if c != EMPTY:
                    im.putpixel((x, y), (int(c[0]), int(c[1]), int(c[2]), int(c[3])))
        return im

    def dump(self, name):
        legend, rev = {}, {}
        print(f"--- {name} ---")
        for y in range(SIZE):
            row = []
            for x in range(SIZE):
                c = self.c[y][x]
                if c == EMPTY:
                    row.append(".")
                else:
                    if c not in rev:
                        rev[c] = len(legend)
                        legend[rev[c]] = c[:3]
                    row.append(str(rev[c]))
            print("".join(row))
        for k, v in legend.items():
            print(f"  {k}: {v}")


# ============================================================================
# Handle helper -- thin grip, bottom-left -> top-right toward socket.
# Concept art uses a slender 2px shaft; the HEAD is the dominant mass.
# ============================================================================
def draw_handle(g, p, x0, y0, x1, y1):
    g.line(x0, y0, x1, y1, p["handle"], 3)
    # leather/finger gaps (darker) perpendicular to the shaft
    g.px(x0 + 1, y0 - 1, p["hmix"])
    g.px(x0 + 3, y0 - 4, p["hmix"])
    g.px(x0 + 5, y0 - 6, p["hmix"])
    g.px(x0 + 7, y0 - 8, p["hmix"])
    # bright upper seam (light comes from top-left)
    g.px(x0 + 1, y0 - 2, p["light"])
    g.px(x0 + 4, y0 - 5, p["light"])
    g.px(x0 + 6, y0 - 7, p["light"])
    # dark underside seam
    g.px(x0 + 2, y0 - 2, p["shadow"])
    g.px(x0 + 5, y0 - 5, p["shadow"])
    return x1, y1


def draw_pommel(g, p, x, y):
    g.px(x, y, p["edge"])
    g.px(x - 1, y + 1, p["body"])
    g.px(x + 1, y - 1, p["light"])
    g.px(x, y - 1, p["edge"])
    g.px(x, y + 1, p["shadow"])


def jagged_vein(g, pts, p, pad=True):
    """Draw a 1px stepped magma/energy vein through pts (blocky steps), 3 tones:
    ends = deep shade, body = mid vein, a couple of hottest = sulfur/hot."""
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        # ensure the vein sits ON opaque material: push point if it landed on empty
        if g.get(x, y) == EMPTY and pad:
            # nudge toward nearest opaque neighbour (simple: skip drawing here
            # if truly off-grid; we trust authored points to sit on the body)
            pass
        if i in (0, n - 1):
            g.acc(x, y, VEIN_SH, p["vein_sh"])
        elif i in (1, n - 2):
            g.acc(x, y, VEIN, p["vein"])
        else:
            g.acc(x, y, VEIN, p["vein"])
    # one hot pixel can be marked by the caller; here we re-tag the most
    # central point as a crystal-hot to give a bright "core".
    if n >= 3:
        cx, cy = pts[n // 2]
        if g.get(cx, cy) != EMPTY or g.get(cx, cy - 1) != EMPTY:
            g.acc(cx, cy, CK2, p["crystal2"] if "crystal2" in p else p["vein"])


# ============================================================================
# Tool painters.  Silhouettes are broad so they read when halved to 16x16.
# Head toward the upper-right; handle from the lower-left.
# ============================================================================
def paint_sword(g, p):
    # Slender straight sword, wide face, simple guard + pommel. NON-katana.
    # Runs diagonally (handle bottom-left, tip top-right) like vanilla tools.
    bx, by = 14, 18  # guard centre
    draw_handle(g, p, 3, 29, bx - 2, by + 2)
    draw_pommel(g, p, 3, 29)
    # wide straight blade (tip up-right): dominates the frame
    g.fill_poly([(bx, by + 1), (bx + 2, by - 2), (17, by - 7),
                 (24, by - 11), (27, by - 13), (30, by - 11),
                 (26, by - 6), (18, by - 2), (bx + 2, by + 2)], p["body"])
    # clean crescent cutting edge on the upper-left face
    g.line(bx + 1, by - 1, 17, by - 6, p["light"])
    g.line(17, by - 6, 24, by - 10, p["light"], 2)
    g.line(24, by - 10, 27, by - 12, p["edge"])
    g.line(27, by - 12, 30, by - 11, p["edge"])
    # shadowed spine along the lower-right
    g.line(bx + 2, by + 1, 26, by - 5, p["shadow"], 2)
    g.line(26, by - 5, 30, by - 11, p["shadow"])
    # guard (perpendicular band)
    g.fill_poly([(bx - 3, by - 1), (bx + 3, by - 3), (bx + 4, by + 2),
                 (bx - 2, by + 3)], p["shadow"])
    g.line(bx - 2, by + 1, bx + 3, by - 2, p["edge"])
    # signature gem in the guard centre
    g.acc(bx, by, CK, p["crystal"])
    g.acc(bx + 1, by, CK, p["crystal"])
    g.acc(bx, by - 1, CK2, p["crystal2"])
    # running magma/energy vein down the blade centreline
    jagged_vein(g, [(bx + 2, by - 1), (17, by - 5), (21, by - 7),
                    (24, by - 10), (27, by - 11)], p)
    return g


def paint_pickaxe(g, p):
    # Broad arc head with two pronounced points + central socket. Big head.
    sx, sy = 14, 15  # socket centre
    draw_handle(g, p, 3, 29, sx - 2, sy + 4)
    draw_pommel(g, p, 3, 29)
    # thick arc spanning the top
    arc = [(4, 17), (6, 14), (10, 11), (15, 9), (21, 8), (27, 8)]
    for i in range(len(arc) - 1):
        g.line(*arc[i], *arc[i + 1], p["body"], 6)
    # working points (light, forward-tilted)
    g.fill_poly([(2, 18), (6, 16), (5, 14), (1, 16)], p["edge"])
    g.fill_poly([(27, 7), (31, 5), (31, 8), (28, 9)], p["edge"])
    g.px(3, 17, p["light"]); g.px(30, 6, p["light"])
    # underside shadow band + bright top ridge
    g.line(7, 13, 26, 9, p["shadow"], 2)
    g.line(8, 12, 25, 9, p["light"])
    g.line(9, 11, 24, 9, p["edge"])
    # central socket block
    g.fill_poly([(sx - 3, sy - 3), (sx + 3, sy - 4), (sx + 4, sy + 1),
                 (sx - 2, sy + 3)], p["body"])
    g.line(sx - 2, sy - 1, sx + 3, sy - 3, p["edge"])
    g.px(sx, sy, p["socket"])
    g.acc(sx, sy, CK, p["crystal"])
    g.acc(sx + 1, sy, CK, p["crystal"])
    g.acc(sx, sy - 1, CK2, p["crystal2"])
    # magma vein along the top arc
    jagged_vein(g, [(sx - 4, sy - 2), (sx - 7, sy - 6), (22, 8), (26, 8)], p)
    return g


def paint_axe(g, p):
    # One-sided heavy axe: broad cheek + tall working edge on the RIGHT,
    # short poll on the LEFT, centred socket. Faithful to a compact axe.
    hx, hy = 13, 19  # socket centre
    draw_handle(g, p, 3, 29, hx - 2, hy + 3)
    draw_pommel(g, p, 3, 29)
    # socket block
    g.fill_poly([(hx - 3, hy - 3), (hx + 3, hy - 4), (hx + 4, hy + 1),
                 (hx - 2, hy + 3)], p["body"])
    g.px(hx, hy, p["socket"])
    # compact poll on the left
    g.fill_poly([(hx - 3, hy - 2), (7, hy - 1), (7, hy + 1), (hx - 2, hy + 1)], p["shadow"])
    g.line(7, hy - 1, 7, hy + 1, p["edge"])
    # broad sweeping cheek up-right
    g.fill_poly([(hx + 1, hy - 2), (17, hy - 8), (25, hy - 10),
                 (30, hy - 3), (27, hy + 2), (hx + 3, hy + 3)], p["body"])
    # big clean working edge (bright crescent)
    g.line(17, hy - 7, 25, hy - 10, p["light"], 2)
    g.line(25, hy - 10, 30, hy - 3, p["edge"], 2)
    g.line(30, hy - 3, 27, hy + 2, p["edge"])
    # deep shadow under the cheek
    g.line(27, hy + 2, hx + 3, hy + 3, p["shadow"])
    g.line(18, hy - 5, hx + 2, hy - 2, p["shadow"])
    # internal emissive vein entering the cheek
    jagged_vein(g, [(hx + 1, hy - 1), (hx + 3, hy - 3), (20, hy - 6), (22, hy - 6), (24, hy - 7)], p)
    g.acc(hx, hy, CK, p["crystal"])
    return g


def paint_shovel(g, p):
    # Wide flat-topped blade, tapered sides, short working bottom, small shaft.
    hx, hy = 12, 20  # neck / collar
    draw_handle(g, p, 3, 29, hx - 1, hy + 3)
    draw_pommel(g, p, 3, 29)
    # collar
    g.fill_poly([(hx - 3, hy - 1), (hx + 2, hy - 2), (hx + 3, hy + 2),
                 (hx - 2, hy + 3)], p["body"])
    g.px(hx, hy, p["socket"])
    # broad blade trapezoid (flat top, tapered sides, pointed bottom)
    g.fill_poly([(hx + 1, hy), (21, hy - 4), (28, hy - 2),
                 (27, hy + 7), (16, hy + 10), (hx, hy + 6)], p["body"])
    # flat-top highlight
    g.line(hx + 1, hy, 21, hy - 4, p["light"], 2)
    g.line(21, hy - 4, 28, hy - 2, p["light"])
    # shadow toward tip
    g.line(28, hy - 2, 27, hy + 7, p["shadow"], 2)
    g.line(27, hy + 7, 16, hy + 10, p["shadow"])
    g.line(16, hy + 10, hx, hy + 6, p["shadow"])
    g.line(hx, hy + 6, hx + 1, hy, p["shadow"])
    # central emissive channel running down the blade
    jagged_vein(g, [(hx + 2, hy + 1), (18, hy), (23, hy - 1), (25, hy + 1)], p)
    g.acc(hx, hy, CK, p["crystal"])
    g.acc(hx + 1, hy, CK, p["crystal"])
    return g


def paint_hoe(g, p):
    # Thin hoe: long handle, short horizontal head, one bent working hook.
    hx, hy = 13, 17  # socket
    draw_handle(g, p, 3, 29, hx - 1, hy + 3)
    draw_pommel(g, p, 3, 29)
    # short horizontal head bar
    g.line(hx, hy, 24, hy - 4, p["body"], 4)
    g.px(hx, hy, p["socket"])
    # bent working hook (down then out)
    g.fill_poly([(24, hy - 5), (27, hy - 3), (27, hy + 3), (24, hy + 1)], p["body"])
    g.fill_poly([(26, hy + 3), (27, hy + 2), (27, hy + 6), (25, hy + 7)], p["body"])
    # bright working edge on the hook underside
    g.line(25, hy - 4, 27, hy + 2, p["light"])
    g.line(27, hy + 2, 26, hy + 6, p["edge"])
    # shadow on the head top
    g.line(hx + 1, hy - 1, 24, hy - 5, p["shadow"])
    # inner-bend vein
    g.acc(hx, hy, CK, p["crystal"])
    g.acc(hx + 1, hy, CK, p["crystal"])
    jagged_vein(g, [(hx + 3, hy - 1), (18, hy - 3), (22, hy - 3), (24, hy - 3)], p)
    return g


def paint_warhammer(g, p):
    # Massive rectangular head with two rounded impact faces + glowing core.
    draw_handle(g, p, 3, 29, 12, 18)
    draw_pommel(g, p, 3, 29)
    face_top, face_bot = 4, 17
    # the big block (dominant)
    g.fill_poly([(7, face_top), (26, face_top), (26, face_bot), (7, face_bot)], p["body"])
    # top steel plane
    g.fill_poly([(8, face_top + 1), (25, face_top + 1), (25, face_top + 4),
                 (8, face_top + 4)], p["light"])
    # underside shadow
    g.fill_poly([(8, face_bot - 2), (25, face_bot - 2), (25, face_bot), (8, face_bot)], p["shadow"])
    # left / right rounded impact faces (pale caps)
    g.line(7, face_top, 7, face_bot, p["edge"], 2)
    g.line(26, face_top, 26, face_bot, p["edge"], 2)
    g.line(9, face_top, 24, face_top, p["outline"])
    g.line(9, face_bot, 24, face_bot, p["outline"])
    # corner studs on the top plane
    g.px(10, face_top - 1, p["edge"]); g.px(22, face_top - 1, p["edge"])
    g.px(10, face_top, p["light"]); g.px(22, face_top, p["light"])
    # central core crystal column (static block + animated gem)
    g.fill_poly([(15, face_top + 4), (19, face_top + 4), (19, face_bot - 4),
                 (15, face_bot - 4)], p["outline"])
    g.fill_poly([(16, face_top + 5), (18, face_top + 5), (18, face_bot - 5),
                 (16, face_bot - 5)], p["socket"])
    g.acc(17, 9, CK, p["crystal"])
    g.acc(17, 10, CK2, p["crystal2"])
    g.acc(17, 8, CK, p["crystal"])
    g.acc(18, 10, CK, p["crystal"])
    # cobalt channels fraying across the faces
    jagged_vein(g, [(9, 8), (14, 7), (15, 6), (24, 6), (25, 7)], p)
    jagged_vein(g, [(9, 14), (14, 15), (24, 15), (25, 14)], p)
    return g


def paint_labrys(g, p):
    # Symmetric double-bladed axe (Parthenon Labrys): two ivory blades,
    # bronze centre block, brown handle, ruby in centre, Greek-geometry accents.
    hx, hy = 14, 18
    draw_handle(g, p, 3, 29, hx - 1, hy + 3)
    draw_pommel(g, p, 3, 29)
    # bronze centre block
    g.fill_poly([(hx - 4, hy - 4), (hx + 4, hy - 5), (hx + 5, hy + 2),
                 (hx - 3, hy + 3)], p["body"])
    # left blade (mirror)
    g.fill_poly([(hx - 4, hy - 3), (hx - 9, hy - 7), (hx - 13, hy - 4),
                 (hx - 12, hy + 2), (hx - 5, hy + 2)], p["body"])
    # right blade (mirror)
    g.fill_poly([(hx + 4, hy - 4), (hx + 9, hy - 8), (hx + 13, hy - 5),
                 (hx + 12, hy + 1), (hx + 5, hy + 2)], p["body"])
    # ivory cutting edges
    g.line(hx - 9, hy - 6, hx - 13, hy - 4, p["light"])
    g.line(hx - 13, hy - 4, hx - 12, hy + 2, p["edge"])
    g.line(hx + 9, hy - 7, hx + 13, hy - 5, p["light"])
    g.line(hx + 13, hy - 5, hx + 12, hy + 1, p["edge"])
    # inner shadows
    g.line(hx - 4, hy - 3, hx - 5, hy + 2, p["shadow"])
    g.line(hx + 4, hy - 4, hx + 5, hy + 2, p["shadow"])
    # ruby in the centre
    g.acc(hx, hy, CK, p["crystal"])
    g.acc(hx, hy - 1, CK2, p["crystal2"])
    # Greek-meander gold geometry accents (symmetric hint)
    g.acc(hx - 3, hy - 2, GOLD, p["accent"])
    g.acc(hx + 3, hy - 2, GOLD, p["accent"])
    g.acc(hx - 3, hy, GOLD, p["accent"])
    g.acc(hx + 3, hy, GOLD, p["accent"])
    return g


def _acc_between(g, a, b, n, kind, base, base_sh):
    """Place n emissive pixels along a straight line, shading the ends."""
    x0, y0 = a
    x1, y1 = b
    for i in range(n):
        t = i / max(1, n - 1)
        x = round(x0 + (x1 - x0) * t)
        y = round(y0 + (y1 - y0) * t)
        col = base_sh if i in (0, n - 1) else base
        g.acc(x, y, VEIN_SH if i in (0, n - 1) else VEIN, col)
# ============================================================================
# Item table: (id, family, painter, volumetric_display, frame_count)
# Only the warhammer and the Labrys keep a 3D volume transform; everything
# else stays vanilla minecraft:item/handheld and just flips the texture.
# ============================================================================
WHITELIST = [
    # NOTE: the whole opus set is full GeckoLib 3D weapons now
    # (see scripts/generate_opus.py + com.opus.opus.item). Deliberately
    # absent here so a re-run can never overwrite their
    # models/item/*.json or geo/animation assets.
    # NOTE: the whole fire (Vein Fire) set is full GeckoLib 3D weapons now
    # (see scripts/generate_veinfire.py). Deliberately absent here so a
    # re-run can never overwrite their geo/animation assets.
    # NOTE: parthenon_sword is a full GeckoLib 3D weapon now
    # (see scripts/generate_xiphos.py + ParthenonXiphosItem). It is
    # deliberately absent here so a re-run can never overwrite
    # models/item/parthenon_sword.json or its geo/animation assets.
    # NOTE: parthenon_pickaxe is a full GeckoLib 3D weapon now
    # (see scripts/generate_pickaxe.py + ParthenonPickaxeItem). It is
    # deliberately absent here so a re-run can never overwrite
    # models/item/parthenon_pickaxe.json or its geo/animation assets.
    # NOTE: parthenon_axe is a full GeckoLib 3D weapon now
    # (see scripts/generate_labrys.py + ParthenonLabrysItem). It is
    # deliberately absent here so a re-run can never overwrite
    # models/item/parthenon_axe.json or its geo/animation assets.
    # NOTE: parthenon_shovel + parthenon_hoe are full GeckoLib 3D weapons now
    # (see scripts/generate_shovel.py + generate_hoe.py). Deliberately absent
    # here so a re-run can never overwrite their geo/animation assets.
    # NOTE: the whole dark_forest set is full GeckoLib 3D weapons now
    # (see scripts/generate_darkforest.py). Deliberately absent here so a
    # re-run can never overwrite their geo/animation assets.
]
FRAMES = {n: k for (n, f, pa, d, k) in WHITELIST}
BY_NAME = {n: (f, pa, d, k) for (n, f, pa, d, k) in WHITELIST}


# ============================================================================
# Emissive frame rendering
# ============================================================================
def build_base(name):
    fam, painter, disp, n = BY_NAME[name]
    p = FAMILY[fam]
    g = Grid()
    painter(g, p)
    g.clean_isolated(min_size=4)
    g.outline(p["outline"])
    return g, p


def frame_grid(base, p, frame, nframes):
    """Copy the static base and modulate ONLY emissive pixels.

    The brightness follows a smooth sine pulse; the moving "hot point" is
    faked by shifting which one vein pixel sits at full brightness on middle
    frames. Outline, handle and material never move.
    """
    rows = [row[:] for row in base.c]
    phase = 0.5 - 0.5 * math.cos(2 * math.pi * frame / nframes)
    phase = max(0.12, min(0.95, phase * 1.5 + 0.12))
    for (x, y), (kind, basecol) in base.emiss.items():
        # crystal cores whiten fast; veins run warm; gold/moss stays subtle
        target = (255, 255, 255, 255)
        hot = mix(basecol, target, phase)
        rows[y][x] = (int(hot[0]), int(hot[1]), int(hot[2]), 255)
    return rows


def rows_to_im(rows):
    im = Image.new("RGBA", (SIZE, SIZE), EMPTY)
    for y in range(SIZE):
        for x in range(SIZE):
            c = rows[y][x]
            if c != EMPTY:
                im.putpixel((x, y), (int(c[0]), int(c[1]), int(c[2]), int(c[3])))
    return im


def frametime_for(name):
    # Per spec: fire = fast ember (3); others steady (5).
    return 3 if name.startswith("fire_") else 5


# ============================================================================
# Item model writing
# ============================================================================
def write_model(name, volumetric):
    model = {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"opusvsexe:item/{name}"},
    }
    if volumetric:
        model["display"] = VOLUME_DISPLAY
    path = MODELS / f"{name}.json"
    path.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")


VOLUME_DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.62, 0.62, 0.62]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.62, 0.62, 0.62]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "gui": {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [0.62, 0.62, 0.62]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [0.75, 0.75, 0.75]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
}


# ============================================================================
# Main
# ============================================================================
def main():
    dump_only = "--dump" in sys.argv
    written = []
    for (name, fam, painter, disp, n) in WHITELIST:
        base, p = build_base(name)
        if dump_only:
            base.dump(name)
            continue
        nframes = FRAMES[name]
        sheet = Image.new("RGBA", (SIZE, SIZE * nframes), EMPTY)
        for i in range(nframes):
            rows = frame_grid(base, p, i, nframes)
            sheet.paste(rows_to_im(rows), (0, i * SIZE))
        sheet.save(ITEMS / f"{name}.png")
        (ITEMS / f"{name}.png.mcmeta").write_text(
            json.dumps({"animation": {"frametime": frametime_for(name),
                                      "interpolate": False}}, indent=2),
            encoding="utf-8")
        write_model(name, disp)
        written.append(name)
    if not dump_only:
        save_sheets(written)
        print(f"wrote {len(written)} tools ({SIZE}x{SIZE} x frames) -> " +
              f"{ITEMS.relative_to(ROOT)}")
    else:
        print(f"dry-run of {len(WHITELIST)} tools")
    return written


def save_sheets(names):
    """Emit 3 QA sheets, each showing a SINGLE frame (frame 0) per tool so
    nothing is squashed: frames-grid, dark-bg, light-bg."""
    cell, cols = 96, 5
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (28, 28, 32, 255))
    dark = Image.new("RGBA", (cols * cell, rows * cell), (16, 16, 18, 255))
    light = Image.new("RGBA", (cols * cell, rows * cell), (237, 223, 194, 255))
    for idx, name in enumerate(names):
        im = Image.open(ITEMS / f"{name}.png").convert("RGBA")
        frame = im.crop((0, 0, SIZE, SIZE))  # always the base/static frame
        x, y = (idx % cols) * cell, (idx // cols) * cell
        sheet.alpha_composite(frame.resize((64, 64), Image.Resampling.NEAREST), (x + 16, y + 16))
        dark.alpha_composite(frame.resize((64, 64), Image.Resampling.NEAREST), (x + 16, y + 16))
        light.alpha_composite(frame.resize((64, 64), Image.Resampling.NEAREST), (x + 16, y + 16))
    for p in (QA, QA_DARK, QA_LIGHT):
        p.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(QA)
    dark.save(QA_DARK)
    light.save(QA_LIGHT)


if __name__ == "__main__":
    main()
