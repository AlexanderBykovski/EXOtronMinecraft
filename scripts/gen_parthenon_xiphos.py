#!/usr/bin/env python3
"""Parthenon Xiphos — angelic celestial rework (from scratch).

Hand-authored parametric pixel art on a 32x32 grid, diagonal orientation
(blade up-right, grip down-left) matching the mod's unified weapon language.
Writes ONLY parthenon_sword.png + .png.mcmeta + models/item/parthenon_sword.json.
Idempotent; does not touch katanas or any other Parthenon tool.

Dry-run (ASCII frames, writes nothing):
    python3 scripts/gen_parthenon_xiphos.py --dump
Write assets:
    python3 scripts/gen_parthenon_xiphos.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
SIZE = 32
NAME = "parthenon_sword"
N_FRAMES = 4
FRAMETIME = 5
T = (0, 0, 0, 0)  # transparent

# --- palette (celestial white + angelic gold + Parthenon ruby) -------------
EDGE_HI = (252, 250, 244, 255)   # blinding cutting edge
LIGHT = (226, 233, 238, 255)     # celestial metal light
MID = (203, 213, 221, 255)       # celestial metal mid
COOL = (167, 178, 190, 255)      # cool shadow (lower-right face)
DEEP = (126, 139, 154, 255)      # deep shadow
GOLD_BRIGHT = (255, 238, 150, 255)
GOLD_MID = (232, 190, 92, 255)
GOLD_DEEP = (176, 128, 56, 255)
OUTLINE = (52, 46, 44, 255)
RUBY_BRIGHT = (222, 70, 74, 255)
RUBY_DEEP = (146, 30, 42, 255)
CORE = (255, 248, 240, 255)      # white-hot gem/channel core
GRIP_DARK = (52, 60, 74, 255)
GRIP_DARKER = (33, 40, 52, 255)


class Grid:
    def __init__(self):
        self.c = [[T for _ in range(SIZE)] for _ in range(SIZE)]

    def px(self, x, y, col):
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < SIZE and 0 <= yi < SIZE and self.c[yi][xi] == T:
            self.c[yi][xi] = col
        elif 0 <= xi < SIZE and 0 <= yi < SIZE and col == T:
            self.c[yi][xi] = T

    def cv(self, x, y, col):
        """overwrite (destructive) — for channel/edges on top of base."""
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < SIZE and 0 <= yi < SIZE:
            self.c[yi][xi] = col

    def dump(self):
        cols = {}
        rev = {}
        for y in range(SIZE):
            line = []
            for x in range(SIZE):
                c = self.c[y][x]
                if c == T:
                    line.append(".")
                else:
                    if c not in rev:
                        rev[c] = len(cols)
                        cols[rev[c]] = c[:3]
                    line.append(str(rev[c]))
            print("".join(line))
        for k, v in cols.items():
            print(f"  {k}: {v}")


def draw(g):
    # SINGLE shared diagonal axis: guard base G -> blade tip T (up-right);
    # grip+pommel continue from G down-left.
    gx, gy = 14.0, 18.0          # guard / blade base centre
    tx, ty = 30.0, 4.0           # blade tip (sharp spear point, up-right)
    ax_x, ax_y = tx - gx, ty - gy
    ax_len = math.hypot(ax_x, ax_y)
    ux, uy = ax_x / ax_len, ax_y / ax_len      # along-blade unit (up-right)
    evx, evy = -uy, ux                          # perpendicular (down-right)

    def pt(s, o):
        """point at along-axis s in [0,1] and perpendicular offset o."""
        return gx + ax_x * s + evx * o, gy + ax_y * s + evy * o

    # ------------------------------------------------------------------
    # BLADE — tapered celestial blade. Center gold fuller + bright slicing
    # edges, light face on o<0, cool shadow on o>0 (light from top-left).
    # ------------------------------------------------------------------
    def half_width(s):
        if s < 0.16:
            return 2.2
        if s < 0.70:
            return 1.9
        return 1.9 * ((1.0 - s) / 0.30) ** 1.5

    s = 0.0
    while s <= 1.0:
        w = half_width(s)
        for t in range(-12, 13):
            o = t / 12.0 * w
            px_, py_ = pt(s, o)
            if s > 0.985:
                col = EDGE_HI
            elif abs(o) >= w - 0.5:
                col = EDGE_HI                     # cutting edge
            elif abs(o) <= 0.45:
                col = GOLD_MID                    # divine fuller
            elif o < 0:
                col = LIGHT if o < -1.0 else MID  # light face
            else:
                col = COOL if o < 1.0 else DEEP   # cool face
            g.px(px_, py_, col)
        s += 0.02

    # bright gold shimmer along the fuller
    for i in range(0, 34):
        s = i / 33.0
        if s > 0.76:
            break
        cx, cy = pt(s, 0.0)
        g.cv(cx, cy, GOLD_BRIGHT)

    # ------------------------------------------------------------------
    # ANGELIC GUARD — symmetric gold winged fins protruding perpendicular
    # to the blade axis, plus a central shield and ruby gem. Fins read as
    # a folded celestial wing (broad plate + layered feather + bright tip).
    # Splayed clearly beyond the blade width so the wings read at 16x16.
    # ------------------------------------------------------------------
    def fin(side, lens, o0, o1, col):
        n0 = pt(0, o0 * side)
        n1 = pt(0, o1 * side)
        f2 = pt(lens, o1 * side)
        f3 = pt(lens, o0 * side)
        quad(g, n0, n1, f2, f3, col)

    for side in (1, -1):
        fin(side, 0.28, 2.0, 3.4, GOLD_DEEP)      # broad folded plate (inner)
        fin(side, 0.48, 3.0, 3.9, GOLD_MID)        # layered feather (outer)
        fin(side, 0.62, 3.7, 4.3, GOLD_BRIGHT)     # slim bright tip

    # central gold shield (collar) wrapping the blade junction
    c0 = pt(-0.05, -1.6)
    c1 = pt(-0.05, 1.6)
    c2 = pt(0.12, 1.6)
    c3 = pt(0.12, -1.6)
    quad(g, c0, c1, c2, c3, GOLD_MID)
    g.cv(pt(-0.05, 1.55)[0], pt(-0.05, 1.55)[1], GOLD_BRIGHT)
    g.cv(pt(-0.05, -1.55)[0], pt(-0.05, -1.55)[1], GOLD_BRIGHT)

    # ------------------------------------------------------------------
    # GRIP — dark charcoal-blue wrap with two thin gold rings.
    # Runs straight along the blade axis below the guard (s < 0).
    # ------------------------------------------------------------------
    p_s = -0.62                  # pommel centre along axis
    for i in range(0, 31):
        s = -0.04 - (i / 30.0) * 0.52
        cx, cy = pt(s, 0.0)
        for o in (-1.1, -0.5, 0.5, 1.1):
            g.px(cx + evx * o, cy + evy * o, GRIP_DARK)
        g.cv(cx + evx * 0.9, cy + evy * 0.9, GRIP_DARKER)
    for rs in (-0.22, -0.42):
        cx, cy = pt(rs, 0.0)
        for o in (-1.25, -0.55, 0.55, 1.25):
            g.cv(cx + evx * o, cy + evy * o, GOLD_MID)

    # ------------------------------------------------------------------
    # RUBY DIVINE GEM at the guard centre — upright diamond (rhombus).
    # ------------------------------------------------------------------
    gcx, gcy = pt(0.05, 0.0)
    diamond(g, gcx, gcy, 1.8, 2.6, RUBY_DEEP)
    diamond(g, gcx, gcy, 1.1, 1.85, RUBY_BRIGHT)
    g.cv(gcx, gcy - 0.55, CORE)
    g.cv(gcx - 0.55, gcy, (255, 150, 150, 255))

    # ------------------------------------------------------------------
    # POMMEL — inverted diamond, gold frame, bright core.
    # ------------------------------------------------------------------
    p_x, p_y = pt(p_s, 0.0)
    diamond(g, p_x, p_y, 1.9, 2.1, GOLD_DEEP)
    diamond(g, p_x, p_y, 1.2, 1.5, GOLD_MID)
    g.cv(p_x, p_y, CORE)
    g.cv(p_x, p_y - 0.6, GOLD_BRIGHT)

    # ------------------------------------------------------------------
    # OUTLINE — dark warm outline around the whole silhouette.
    # ------------------------------------------------------------------
    out = [row[:] for row in g.c]
    for y in range(SIZE):
        for x in range(SIZE):
            if g.c[y][x] != T:
                continue
            for ox_, oy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + ox_, y + oy_
                if 0 <= nx < SIZE and 0 <= ny < SIZE and g.c[ny][nx] != T:
                    out[y][x] = OUTLINE
                    break
    g.c = out

    return g


def diamond(g, cx, cy, rx, ry, col):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            ex = abs(x - cx) / rx
            ey = abs(y - cy) / ry
            if ex + ey <= 1.0:
                g.cv(x, y, col)


def quad(g, p0, p1, p2, p3, col):
    pts = [p0, p1, p2, p3]
    ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(SIZE - 1, int(max(ys))) + 1):
        xs = []
        n = len(pts)
        j = n - 1
        for i in range(n):
            if (pts[i][1] <= y < pts[j][1]) or (pts[j][1] <= y < pts[i][1]):
                tt = (y - pts[i][1]) / (pts[j][1] - pts[i][1])
                xs.append(pts[i][0] + tt * (pts[j][0] - pts[i][0]))
            j = i
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                g.px(x, y, col)


# --- emissive animation ------------------------------------------------
# (x,y) -> base col for the shimmering pixels. Only these change across frames.
ANIM = []


def collect_anim(base_grid):
    """Find the gold channel + gem + pommel core pixels so frames can pulse."""
    # We re-derive from known centers rather than scanning color, to keep mask stable.
    return base_grid


def render_frame(base, frame, nframes):
    g = Grid()
    g.c = [row[:] for row in base.c]
    # divine shimmer: brightness envelope around gem/channel/pommel.
    # Identify shimmer sites by color == gold_bright or white-hot core / gem bright.
    shimmer = {
        GOLD_BRIGHT: [GOLD_BRIGHT, GOLD_MID, (255, 244, 180, 255)],
        CORE: [CORE, (255, 242, 224, 255), (255, 246, 236, 255)],
        RUBY_BRIGHT: [RUBY_BRIGHT, (250, 120, 120, 255), RUBY_BRIGHT],
    }
    phase = [0, 1, 0, 1][frame % nframes]
    alt = {GOLD_BRIGHT: 0, CORE: 0, RUBY_BRIGHT: 0}
    for y in range(SIZE):
        for x in range(SIZE):
            c = g.c[y][x]
            if c in (GOLD_BRIGHT, CORE, RUBY_BRIGHT) and alt[c] < 60:
                alt[c] += 1
                pal = shimmer[c]
                g.c[y][x] = pal[(frame % nframes) % len(pal)]
    return g


def main():
    write = "--dump" not in sys.argv
    base = Grid()
    draw(base)
    if not write:
        for f in range(N_FRAMES):
            fr = render_frame(base, f, N_FRAMES)
            print(f"--- frame {f} ---")
            fr.dump()
        return

    # build the atlas
    atlas = Image.new("RGBA", (SIZE, SIZE * N_FRAMES), (0, 0, 0, 0))
    for f in range(N_FRAMES):
        fr = render_frame(base, f, N_FRAMES)
        for y in range(SIZE):
            for x in range(SIZE):
                c = fr.c[y][x]
                if c != T:
                    atlas.putpixel((x, y + f * SIZE), c)
    out = ITEMS / f"{NAME}.png"
    atlas.save(out)
    print("wrote", out)

    mcmeta = {"animation": {"frametime": FRAMETIME, "interpolate": False}}
    (ITEMS / f"{NAME}.png.mcmeta").write_text(json.dumps(mcmeta, indent=2))
    print("wrote", ITEMS / f"{NAME}.png.mcmeta")

    model = {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"opusvsexe:item/{NAME}"},
        "display": VOLUME_DISPLAY,
    }
    (MODELS / f"{NAME}.json").write_text(json.dumps(model, indent=2))
    print("wrote", MODELS / f"{NAME}.json")


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


if __name__ == "__main__":
    main()
