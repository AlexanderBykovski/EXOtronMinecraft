"""Shared celestial-set helpers reused by the Parthenon tool generator.

Palette + pixel helpers are lifted from gen_parthenon_xiphos.py so the sword
and the four tools stay perfectly in-family (identical gold, white metal,
ruby gem, dark grip, pommel, and the same 4-frame divine shimmer).
"""
from __future__ import annotations
from PIL import Image  # noqa: E402

SIZE = 32
T = (0, 0, 0, 0)

# palette (identical to the Angelic Sword)
EDGE_HI = (252, 250, 244, 255)
LIGHT = (226, 233, 238, 255)
MID = (203, 213, 221, 255)
COOL = (167, 178, 190, 255)
DEEP = (126, 139, 154, 255)
GOLD_BRIGHT = (255, 238, 150, 255)
GOLD_MID = (232, 190, 92, 255)
GOLD_DEEP = (176, 128, 56, 255)
OUTLINE = (52, 46, 44, 255)
RUBY_BRIGHT = (222, 70, 74, 255)
RUBY_DEEP = (146, 30, 42, 255)
CORE = (255, 248, 240, 255)
GRIP_DARK = (52, 60, 74, 255)
GRIP_DARKER = (33, 40, 52, 255)
RUBY_HOT = (255, 150, 150, 255)


class Grid:
    def __init__(self):
        self.c = [[T for _ in range(SIZE)] for _ in range(SIZE)]

    def px(self, x, y, col):
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < SIZE and 0 <= yi < SIZE and self.c[yi][xi] == T:
            self.c[yi][xi] = col

    def cv(self, x, y, col):
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < SIZE and 0 <= yi < SIZE:
            self.c[yi][xi] = col

    def dump(self):
        cols, rev = {}, {}
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


def quad(g, p0, p1, p2, p3, col):
    pts = [p0, p1, p2, p3]
    ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(SIZE - 1, int(max(ys))) + 1):
        xs, n, j = [], len(pts), len(pts) - 1
        for i in range(n):
            if (pts[i][1] <= y < pts[j][1]) or (pts[j][1] <= y < pts[i][1]):
                tt = (y - pts[i][1]) / (pts[j][1] - pts[i][1])
                xs.append(pts[i][0] + tt * (pts[j][0] - pts[i][0]))
            j = i
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                g.px(x, y, col)


def diamond(g, cx, cy, rx, ry, col):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            ex = abs(x - cx) / rx
            ey = abs(y - cy) / ry
            if ex + ey <= 1.0:
                g.cv(x, y, col)


# --- shared handle / gem / pommel -------------------------------------
def draw_handle(g, ax):
    """Dark charcoal-blue grip running straight along the axis (down-left)
    with two thin gold wrap rings. ax = Axis with .p(s,o), .evx, .evy."""
    for i in range(0, 31):
        s = -0.04 - (i / 30.0) * 0.52
        cx, cy = ax.p(s, 0.0)
        for o in (-1.1, -0.5, 0.5, 1.1):
            g.px(cx + ax.evx * o, cy + ax.evy * o, GRIP_DARK)
        g.cv(cx + ax.evx * 0.9, cy + ax.evy * 0.9, GRIP_DARKER)
    for rs in (-0.22, -0.42):
        cx, cy = ax.p(rs, 0.0)
        for o in (-1.25, -0.55, 0.55, 1.25):
            g.cv(cx + ax.evx * o, cy + ax.evy * o, GOLD_MID)


def draw_gem(g, gcx, gcy):
    """Small upright ruby diamond, matching the sword's guard gem."""
    diamond(g, gcx, gcy, 1.8, 2.6, RUBY_DEEP)
    diamond(g, gcx, gcy, 1.1, 1.85, RUBY_BRIGHT)
    g.cv(gcx, gcy - 0.55, CORE)
    g.cv(gcx - 0.55, gcy, RUBY_HOT)


def draw_pommel(g, p_x, p_y):
    diamond(g, p_x, p_y, 1.9, 2.1, GOLD_DEEP)
    diamond(g, p_x, p_y, 1.2, 1.5, GOLD_MID)
    g.cv(p_x, p_y, CORE)
    g.cv(p_x, p_y - 0.6, GOLD_BRIGHT)


def outline(g):
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


# --- render frame (4-frame divine shimmer, mask stable) ---------------
SHIMMER = {
    GOLD_BRIGHT: [GOLD_BRIGHT, GOLD_MID, (255, 244, 180, 255)],
    CORE: [CORE, (255, 242, 224, 255), (255, 246, 236, 255)],
    RUBY_BRIGHT: [RUBY_BRIGHT, (250, 120, 120, 255), RUBY_BRIGHT],
}


def render_frame(base, frame, nframes=4):
    g = Grid()
    g.c = [row[:] for row in base.c]
    alt = {GOLD_BRIGHT: 0, CORE: 0, RUBY_BRIGHT: 0}
    for y in range(SIZE):
        for x in range(SIZE):
            c = g.c[y][x]
            if c in SHIMMER and alt[c] < 60:
                alt[c] += 1
                g.c[y][x] = SHIMMER[c][frame % len(SHIMMER[c])]
    return g


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
