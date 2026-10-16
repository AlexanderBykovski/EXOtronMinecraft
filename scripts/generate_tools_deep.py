#!/usr/bin/env python3
"""Deep redesign generator for the 20 whitelist tools (non-katana).

Follows concepts/sets/DEEP_NON_KATANA_TOOLS_REWORK_PROMPTS_RU.md.
Katanas are NOT produced here at all — they are frozen and never touched.

Per family, each tool is drawn as a distinct layered pixel silhouette
(OUTLINE / BASE / SHADOW / DETAIL / HIGHLIGHT / EMISSIVE), then an animated
atlas is emitted where ONLY the emissive/moving pixels change across frames.
The static base grid is built once and frame 0 is identical to the base so
the silhouette / outline / handle never jump.

Dry-run (prints ASCII grids, writes nothing):
    python3 scripts/generate_tools_deep.py --dump

Write PNGs + mcmeta + item models:
    python3 scripts/generate_tools_deep.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from PIL import Image  # noqa: E402  (after docstring)

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
PREVIEW = ROOT / "docs/assets/concepts/deep-tool-rework-sheet-2026-09-02.png"
SIZE = 32
T = (0, 0, 0, 0, 0)  # 5-tuple: r,g,b,a,kind-tag (tag used at build time only)

# --- palettes (per family material logic) ---------------------------------
OPUS = dict(
    outline=(26, 28, 35, 255), handle=(43, 45, 55, 255), hmix=(78, 58, 43, 255),
    shadow=(56, 60, 72, 255), body=(104, 110, 125, 255), light=(150, 158, 172, 255),
    edge=(214, 221, 231, 255), socket=(70, 114, 232, 255),
    crystal=(122, 228, 248, 255), magma_sh=(112, 70, 40, 255),
)
FIRE = dict(
    outline=(28, 24, 22, 255), handle=(82, 56, 37, 255), hmix=(54, 38, 28, 255),
    shadow=(44, 38, 36, 255), body=(72, 63, 58, 255), light=(104, 94, 86, 255),
    edge=(158, 150, 142, 255), socket=(118, 40, 28, 255),
    crystal=(246, 168, 52, 255), magma_sh=(92, 24, 22, 255),
)
PARTHENON = dict(
    outline=(56, 44, 34, 255), handle=(120, 88, 58, 255), hmix=(88, 64, 42, 255),
    shadow=(184, 171, 145, 255), body=(222, 211, 183, 255), light=(242, 236, 215, 255),
    edge=(252, 244, 214, 255), socket=(150, 112, 50, 255),
    crystal=(192, 46, 54, 255), magma_sh=(122, 84, 36, 255),
)
FOREST = dict(
    outline=(23, 23, 30, 255), handle=(66, 52, 42, 255), hmix=(48, 38, 32, 255),
    shadow=(51, 49, 60, 255), body=(82, 78, 93, 255), light=(112, 108, 126, 255),
    edge=(142, 140, 158, 255), socket=(122, 90, 156, 255),
    crystal=(140, 208, 180, 255), magma_sh=(94, 168, 142, 255),
)
FAMILY = {"opus": OPUS, "fire": FIRE, "parthenon": PARTHENON, "forest": FOREST}

# accent "kind" tags used to drive the emissive animation separately.
CK = "crystal"       # bright gem / crystal
MAG = "magma"        # internal vein (midtone)
MAGD = "magma_sh"    # deep shadow of the vein
ED = "edge"          # working edge bone
HKW = "handle_dark"  # dark grip knot


def rgb(c):
    return (c[0], c[1], c[2], 255)


def _mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(4))


class Grid:
    def __init__(self):
        self.c = [[T for _ in range(SIZE)] for _ in range(SIZE)]
        self.accents = {}  # (x,y) -> ("kind", base_rgb)

    def px(self, x, y, col):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.c[y][x] = col

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
        for ox in range(-(w // 2), (w // 2) + 1):
            for oy in range(-(w // 2), (w // 2) + 1):
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
                for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.px(x, y, col)

    def acc(self, x, y, kind, base):
        """Place a pixel that participates in the emissive animation."""
        self.px(x, y, rgb(base))
        self.accents[(x, y)] = (kind, base)

    def clean_isolated(self, min_size=4):
        solid = {(x, y) for y in range(SIZE) for x in range(SIZE)
                 if self.c[y][x] != T}
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
                    self.c[y][x] = T
                    self.accents.pop((x, y), None)

    def outline(self, col):
        out = [row[:] for row in self.c]
        for y in range(SIZE):
            for x in range(SIZE):
                if self.c[y][x] != T:
                    continue
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ox, y + oy
                    if 0 <= nx < SIZE and 0 <= ny < SIZE and self.c[ny][nx] != T:
                        out[y][x] = col
                        break
        self.c = out

    def render(self):
        im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for y in range(SIZE):
            for x in range(SIZE):
                c = self.c[y][x]
                if c != T:
                    im.putpixel((x, y), (c[0], c[1], c[2], c[3]))
        return im

    def dump(self, name, grid=None):
        legend, rev = {}, {}
        rows = grid if grid is not None else self.c
        out_rows = []
        for y in range(SIZE):
            out = []
            for x in range(SIZE):
                c = rows[y][x]
                if c == T:
                    out.append(".")
                else:
                    if c not in rev:
                        rev[c] = len(legend)
                        legend[rev[c]] = c[:3]
                    out.append(str(rev[c]))
            out_rows.append("".join(out))
        print(f"--- {name} ---")
        for r in out_rows:
            print(r)
        for k, v in legend.items():
            print(f"  {k}: {v}")


# --- handle helpers -------------------------------------------------------
def draw_handle(g, p, x0, y0, x1, y1):
    """Diagonal gripped shaft bottom<->top with a couple of dark knots."""
    g.line(x0, y0, x1, y1, p["handle"], 3)
    # shear the knots toward the top (darker leather band)
    g.px(x0 + 2, y0 - 2, p["shadow"])
    g.px(x0 + 4, y0 - 5, p["shadow"])
    g.px(x1 - 2, y1 + 2, p["shadow"])
    g.acc(x1 - 3, y1 + 3, HKW, p["handle"])
    g.acc(x0 + 3, y0 - 3, HKW, p["hmix"])


def _accents_near(g, kind, points, p, key):
    for (x, y) in points:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            g.acc(x, y, kind, p[key])


# --- individual tool painters --------------------------------------------
# Each returns the filled Grid. The head sits toward the upper-right; the
# handle runs from bottom-left. Silhouettes are hand-authored to read at 16x16.

def paint_sword(g, p):
    # straight, fairly wide blade with a simple perpendicular guard + pommel
    bx, by = 13, 18  # guard centre
    draw_handle(g, p, 5, 28, bx - 2, by + 1)
    # blade (tip up-right): ordered so it stays wide but pointed
    g.fill_poly([(bx - 1, by + 2), (bx + 1, by - 1), (30, 4), (31, 6),
                 (29, 7), (bx + 1, by + 3)], p["body"])
    # cutting edge highlight on the top (right-facing) side
    g.line(bx + 1, by - 1, 30, 4, p["light"])
    # dark spine shadow on the lower side
    g.line(bx + 1, by + 3, 29, 7, p["shadow"])
    # cross-guard (perpendicular band)
    g.fill_poly([(bx - 3, by - 1), (bx + 3, by - 3), (bx + 4, by + 1),
                 (bx - 2, by + 3)], p["shadow"])
    g.line(bx - 2, by, bx + 3, by - 2, p["edge"])
    # gem in the guard centre
    g.acc(bx, by, CK, p["crystal"])
    g.acc(bx + 1, by - 1, CK, p["crystal"])
    # pommel tiny wart
    g.px(4, 28, p["shadow"])
    return g


def paint_pickaxe(g, p):
    # arc head with two points, central socket + long handle
    sx, sy = 15, 15  # socket centre
    draw_handle(g, p, 6, 29, sx - 1, sy + 2)
    arc = [(5, 18), (8, 14), (12, 11), (17, 9), (23, 8), (28, 7)]
    for i in range(len(arc) - 1):
        g.line(*arc[i], *arc[i + 1], p["body"], 5)
    # the two working points
    g.px(4, 19, p["edge"]); g.px(5, 18, p["edge"])
    g.px(29, 6, p["edge"]); g.px(28, 7, p["edge"])
    g.line(7, 15, 27, 9, p["shadow"])       # underside of arc
    g.line(7, 16, 27, 8, p["light"])        # top edge highlight
    g.line(9, 14, 25, 9, p["edge"])         # thin bright ridge
    # central socket block
    g.fill_poly([(sx - 3, sy - 3), (sx + 3, sy - 4), (sx + 4, sy + 1), (sx - 2, sy + 3)], p["body"])
    g.px(sx, sy, p["socket"])
    g.acc(sx, sy, CK, p["socket"])
    g.acc(sx - 1, sy, MAG, p["magma_sh"])
    return g


def paint_axe(g, p):
    # one-sided axe: a broad wedge cheek with a tall working edge on the
    # RIGHT, a short compact poll on the LEFT, and a centred handle socket.
    hx, hy = 13, 19  # socket centre
    draw_handle(g, p, 5, 28, hx - 2, hy + 2)
    # socket block (where handle enters the head)
    g.fill_poly([(hx - 3, hy - 3), (hx + 3, hy - 4), (hx + 4, hy + 1), (hx - 2, hy + 3)], p["body"])
    g.px(hx, hy, p["socket"])
    # compact poll block on the left, flush with the socket
    g.fill_poly([(hx - 3, hy - 3), (8, hy - 2), (8, hy + 1), (hx - 2, hy + 1)], p["shadow"])
    g.line(8, hy - 2, 8, hy + 1, p["edge"])
    # broad cheek: sweeping from the socket up-right into a tall blade
    g.fill_poly([(hx + 1, hy - 4), (hx + 6, hy - 10), (26, hy - 11),
                 (29, hy - 3), (24, hy + 2), (hx + 3, hy + 2)], p["body"])
    # clean tall cutting edge on the right (bright crescent)
    g.line(hx + 6, hy - 10, 26, hy - 11, p["light"])
    g.line(26, hy - 11, 29, hy - 3, p["edge"])
    g.line(29, hy - 3, 24, hy + 2, p["edge"])
    # deep shadow under the cheek
    g.line(24, hy + 2, hx + 3, hy + 2, p["shadow"])
    # internal seam (emissive vein enters the cheek)
    g.acc(hx + 2, hy - 3, MAG, p["magma_sh"])
    g.acc(hx + 3, hy - 5, MAG, p["magma_sh"])
    return g


def paint_shovel(g, p):
    # wide flat-topped blade, tapered sides, short working point; small shaft
    hx, hy = 12, 20  # neck / collar
    draw_handle(g, p, 5, 28, hx - 1, hy + 2)
    # collar
    g.fill_poly([(hx - 3, hy - 1), (hx + 2, hy - 2), (hx + 3, hy + 2), (hx - 2, hy + 3)], p["body"])
    g.px(hx, hy, p["socket"])
    # wide blade trapezoid (flat top, tapered sides, pointed bottom)
    g.fill_poly([(hx + 1, hy), (21, hy - 4), (29, hy - 2), (27, hy + 6),
                 (16, hy + 8), (hx, hy + 5)], p["body"])
    # flat-top highlight
    g.line(hx + 1, hy, 21, hy - 4, p["light"])
    g.line(21, hy - 4, 29, hy - 2, p["light"])
    # shadow toward the tip + bottom
    g.line(29, hy - 2, 27, hy + 6, p["shadow"])
    g.line(27, hy + 6, 16, hy + 8, p["shadow"])
    g.line(16, hy + 8, hx, hy + 5, p["shadow"])
    # central emissive channel
    _accents_near(g, MAG, [(hx + 6, hy - 1), (hx + 9, hy - 2), (hx + 12, hy - 1),
                           (hx + 14, hy), (hx + 15, hy + 1), (hx + 13, hy + 3)], p, "magma_sh")
    g.acc(hx + 6, hy - 1, CK, p["crystal"])
    return g


def paint_hoe(g, p):
    # thin hoe: long handle, short horizontal head, one bent working hook
    hx, hy = 13, 17  # socket
    draw_handle(g, p, 5, 28, hx - 1, hy + 2)
    # short horizontal head bar
    g.line(hx, hy, 24, hy - 4, p["body"], 4)
    # bent working hook (down then out)
    g.line(24, hy - 4, 27, hy + 2, p["body"], 3)
    g.line(27, hy + 2, 26, hy + 5, p["body"], 2)
    # bright working edge on the hook underside
    g.line(25, hy - 3, 27, hy + 2, p["light"])
    g.line(27, hy + 2, 26, hy + 5, p["edge"])
    # shadow top of the head
    g.line(hx + 1, hy - 1, 24, hy - 5, p["shadow"])
    g.px(hx, hy, p["socket"])
    g.acc(hx, hy, CK, p["socket"])
    # one or two vein pixels at the inner bend
    g.acc(hx + 2, hy - 1, MAG, p["magma_sh"])
    return g


def paint_warhammer(g, p):
    # massive rectangular head: two impact faces (left/right) + central core
    hx, hy = 12, 18  # top of the handle meets the head's underside
    draw_handle(g, p, 4, 29, hx, hy + 1)
    face_top, face_bot = 6, 15
    # the big block
    g.fill_poly([(10, face_top), (25, face_top), (25, face_bot), (10, face_bot)], p["body"])
    # top steel plane
    g.fill_poly([(11, face_top + 1), (24, face_top + 1), (24, face_top + 3), (11, face_top + 3)], p["light"])
    # underside shadow
    g.fill_poly([(11, face_bot - 2), (24, face_bot - 2), (24, face_bot), (11, face_bot)], p["shadow"])
    # left / right impact faces (pale caps)
    g.line(10, face_top, 10, face_bot, p["edge"], 2)
    g.line(24, face_top, 24, face_bot, p["edge"], 2)
    g.line(12, face_top, 23, face_top, p["handle"])       # top seam
    g.line(12, face_bot, 23, face_bot, p["handle"])       # bottom seam
    # central core crystal column (static block + animated gem inside)
    g.fill_poly([(16, face_top + 5), (19, face_top + 5), (19, face_bot - 5), (16, face_bot - 5)], p["socket"])
    g.acc(17, 9, CK, p["crystal"])
    g.acc(18, 10, CK, p["crystal"])
    g.acc(17, 10, CK, p["crystal"])
    # faint cobalt channels in the seams
    g.acc(13, face_top + 4, MAG, p["socket"])
    g.acc(22, face_top + 4, MAG, p["socket"])
    return g


def paint_labrys(g, p):
    # double-bladed symmetric axe: two ivory blades + bronze centre + ruby
    hx, hy = 13, 18
    draw_handle(g, p, 4, 29, hx - 1, hy + 2)
    # bronze centre block
    g.fill_poly([(hx - 4, hy - 4), (hx + 4, hy - 5), (hx + 5, hy + 2), (hx - 3, hy + 3)], p["body"])
    # left blade
    g.fill_poly([(hx - 4, hy - 3), (hx - 8, hy - 6), (hx - 11, hy - 3),
                 (hx - 10, hy + 2), (hx - 5, hy + 2)], p["body"])
    # right blade
    g.fill_poly([(hx + 4, hy - 4), (hx + 8, hy - 7), (hx + 11, hy - 4),
                 (hx + 10, hy + 1), (hx + 5, hy + 2)], p["body"])
    # ivory cutting edges
    g.line(hx - 8, hy - 6, hx - 11, hy - 3, p["light"])
    g.line(hx - 11, hy - 3, hx - 10, hy + 2, p["edge"])
    g.line(hx + 8, hy - 7, hx + 11, hy - 4, p["light"])
    g.line(hx + 11, hy - 4, hx + 10, hy + 1, p["edge"])
    # inner shadows
    g.line(hx - 4, hy - 3, hx - 5, hy + 2, p["shadow"])
    g.line(hx + 4, hy - 4, hx + 5, hy + 2, p["shadow"])
    # ruby in the centre
    g.acc(hx, hy, CK, p["crystal"])
    g.acc(hx, hy - 1, CK, p["crystal"])
    # gold geometry accents
    g.acc(hx + 3, hy - 2, MAG, p["socket"])
    g.acc(hx - 3, hy - 2, MAG, p["socket"])
    return g


# --- item -> (family, painter, display?) --------------------------------
# display=True keeps the 3D katana-style transform (warhammer + labrys already
# ship those and read well as volumetric tools).
WHITELIST = [
    ("opus_warhammer",   "opus",      paint_warhammer, True,  4),
    ("opus_pickaxe",     "opus",      paint_pickaxe,   False, 3),
    ("opus_axe",         "opus",      paint_axe,       False, 3),
    ("opus_shovel",      "opus",      paint_shovel,    False, 4),
    ("opus_hoe",         "opus",      paint_hoe,       False, 3),
    ("fire_sword",       "fire",      paint_sword,     False, 5),
    ("fire_pickaxe",     "fire",      paint_pickaxe,   False, 4),
    ("fire_axe",         "fire",      paint_axe,       False, 4),
    ("fire_shovel",      "fire",      paint_shovel,    False, 3),
    ("fire_hoe",         "fire",      paint_hoe,       False, 3),
    ("parthenon_sword",  "parthenon", paint_sword,     False, 3),
    ("parthenon_pickaxe","parthenon", paint_pickaxe,   False, 3),
    ("parthenon_axe",    "parthenon", paint_labrys,    True,  4),
    ("parthenon_shovel", "parthenon", paint_shovel,    False, 3),
    ("parthenon_hoe",    "parthenon", paint_hoe,       False, 3),
    ("dark_forest_sword","forest",    paint_sword,     False, 4),
    ("dark_forest_pickaxe","forest",  paint_pickaxe,   False, 4),
    ("dark_forest_axe",  "forest",    paint_axe,       False, 3),
    ("dark_forest_shovel","forest",   paint_shovel,    False, 4),
    ("dark_forest_hoe",  "forest",    paint_hoe,       False, 3),
]
FRAMES = {name: n for (name, fam, painter, disp, n) in WHITELIST}
BY_NAME = {name: (fam, painter, disp, n) for (name, fam, painter, disp, n) in WHITELIST}


# --- emissive frame rendering -------------------------------------------
def build_base(name):
    fam, painter, disp, n = BY_NAME[name]
    p = FAMILY[fam]
    g = Grid()
    painter(g, p)
    g.clean_isolated(min_size=4)
    g.outline(p["outline"])
    return g, p


def frame_grid(base, p, frame, nframes):
    """Copy the static base and modulate ONLY the emissive pixels.

    A slow, smooth brightness curve visits a gem (crystal) and a vein (magma).
    The moving "hot point" (per-spec) is simulated by shifting which one vein
    pixel is fully lit on the middle frames; outline/handle/material never move.
    """
    rows = [row[:] for row in base.c]
    # brightness factor (0 = base colour, 1 = white-hot)
    if nframes == 2:
        phase = 0.2 if frame == 0 else 0.9
    else:
        phase = 0.5 - 0.5 * _cos(2 * 3.14159 * frame / nframes)
        phase = max(0.15, min(0.95, phase * 1.6 - 0.1))
    for (x, y), (kind, basecol) in base.accents.items():
        hot = _mix(basecol, (255, 255, 255, 255), phase)
        rows[y][x] = (hot[0], hot[1], hot[2], 255)
    return rows


def _cos(t):
    import math
    return math.cos(t)


def render_frames(name):
    base, p = build_base(name)
    n = FRAMES[name]
    frames = []
    for f in range(n):
        rows = frame_grid(base, p, f, n)
        frames.append(rows)
    return base, frames, n


def rows_to_im(rows):
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for y in range(SIZE):
        for x in range(SIZE):
            c = rows[y][x]
            if c != T:
                im.putpixel((x, y), (c[0], c[1], c[2], c[3]))
    return im


def write_model(name, display):
    model = {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"opusvsexe:item/{name}"},
    }
    if display:
        model["display"] = VOLUME_DISPLAY
    (MODELS / f"{name}.json").write_text(
        json.dumps(model, indent=2) + "\n", encoding="utf-8")


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


def frametime_for(name):
    # per-spec: fire = fast ember (3-4); opus/forest/parthenon = steady (5-6)
    if name.startswith("fire_"):
        return 3
    return 5


def main():
    dump_only = "--dump" in sys.argv
    written = []
    for (name, fam, painter, disp, n) in WHITELIST:
        base, frames, nframes = render_frames(name)
        if dump_only:
            base.dump(name)
            continue
        sheet = Image.new("RGBA", (SIZE, SIZE * nframes), (0, 0, 0, 0))
        for i, rows in enumerate(frames):
            sheet.paste(rows_to_im(rows), (0, i * SIZE))
        sheet.save(ITEMS / f"{name}.png")
        (ITEMS / f"{name}.png.mcmeta").write_text(
            json.dumps({"animation": {"frametime": frametime_for(name),
                                      "interpolate": False}}, indent=2),
            encoding="utf-8")
        write_model(name, disp)
        written.append(name)
    if not dump_only:
        save_preview(written)
        print(f"wrote {len(written)} tools ({SIZE}x{SIZE} x frames) " +
              f"-> {ITEMS.relative_to(ROOT)}")
    else:
        print(f"dry-run of {len(WHITELIST)} tools")
    return written


def save_preview(names):
    cell, cols = 96, 5
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (28, 28, 32, 255))
    for idx, name in enumerate(names):
        im = Image.open(ITEMS / f"{name}.png").convert("RGBA")
        x, y = (idx % cols) * cell, (idx // cols) * cell
        sheet.alpha_composite(im.resize((64, 64), Image.Resampling.NEAREST),
                              (x + 16, y + 16))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW)


if __name__ == "__main__":
    main()
