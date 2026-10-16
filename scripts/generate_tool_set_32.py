#!/usr/bin/env python3
"""32x32 vanilla-style item sprites for the four tool families + five katanas.

Hand-authored pixel silhouettes (stepped diagonals, one dark outline, 2-3 tones
per material, a single signature accent).  The prompts in
concepts/sets/VANILLA_TOOL_PROMPTS_RU.md are the spec; this file holds the final
pixels so the game gets readable tools, not down-scaled concept art.

Dry-run (prints ASCII grids for review, writes nothing):
    python3 scripts/generate_tool_set_32.py --dump

Write PNGs + item models + mcmeta animations:
    python3 scripts/generate_tool_set_32.py
"""
from pathlib import Path
import json
import sys
from PIL import Image  # noqa: E402  (kept after docstring for clarity)

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
PREVIEW = ROOT / "docs/assets/concepts/vanilla-tool-texture-sheet-32-2026-09-02.png"
SIZE = 32
T = (0, 0, 0, 0)

# --- palettes -------------------------------------------------------------
# Each entry: outline, handle, shadow, body, light, edge(working-light edge),
#             accent (the signature pixel), accent2 (secondary), white/crystal.
OPUS = dict(
    outline=(26, 27, 34, 255), handle=(42, 43, 54, 255), hmix=(84, 61, 45, 255),
    shadow=(57, 61, 74, 255), body=(108, 114, 130, 255), light=(166, 173, 188, 255),
    edge=(224, 231, 240, 255), accent=(60, 92, 214, 255), accent2=(70, 158, 235, 255),
    crystal=(124, 229, 248, 255),
)
FIRE = dict(
    outline=(26, 22, 20, 255), handle=(80, 54, 36, 255), hmix=(52, 36, 26, 255),
    shadow=(46, 40, 38, 255), body=(76, 66, 60, 255), light=(100, 90, 82, 255),
    edge=(150, 141, 130, 255), accent=(120, 26, 24, 255), accent2=(196, 70, 30, 255),
    crystal=(247, 166, 46, 255),
)
PARTHENON = dict(
    outline=(58, 46, 36, 255), handle=(118, 86, 56, 255), hmix=(86, 62, 40, 255),
    shadow=(188, 175, 149, 255), body=(222, 211, 182, 255), light=(243, 237, 215, 255),
    edge=(250, 236, 190, 255), accent=(150, 114, 52, 255), accent2=(214, 168, 62, 255),
    crystal=(190, 44, 52, 255),
)
FOREST = dict(
    outline=(24, 23, 31, 255), handle=(64, 50, 40, 255), hmix=(46, 36, 30, 255),
    shadow=(52, 50, 61, 255), body=(83, 79, 94, 255), light=(113, 109, 128, 255),
    edge=(140, 138, 156, 255), accent=(122, 88, 156, 255), accent2=(96, 174, 148, 255),
    crystal=(140, 208, 180, 255),
)

KATANAS = {
    "katana": dict(
        outline=(24, 25, 29, 255), shadow=(66, 69, 75, 255), body=(137, 143, 151, 255),
        light=(196, 203, 210, 255), edge=(226, 231, 234, 255), handle=(42, 43, 54, 255),
        wrap=(72, 73, 84, 255), accent=(84, 61, 45, 255), crystal=(124, 229, 248, 255),
    ),
    "long_katana": dict(
        outline=(24, 25, 29, 255), shadow=(60, 63, 70, 255), body=(150, 156, 164, 255),
        light=(214, 219, 223, 255), edge=(236, 240, 242, 255), handle=(42, 43, 54, 255),
        wrap=(74, 76, 88, 255), accent=(66, 108, 210, 255), crystal=(96, 190, 224, 255),
    ),
    "katana_op": dict(
        outline=(26, 25, 34, 255), shadow=(56, 40, 92, 255), body=(70, 50, 108, 255),
        light=(126, 92, 176, 255), edge=(200, 160, 235, 255), handle=(40, 41, 52, 255),
        wrap=(70, 72, 86, 255), accent=(64, 96, 226, 255), crystal=(120, 230, 250, 255),
    ),
    "katana_gold": dict(
        outline=(54, 42, 26, 255), shadow=(112, 80, 34, 255), body=(182, 134, 50, 255),
        light=(222, 182, 84, 255), edge=(248, 214, 122, 255), handle=(58, 44, 32, 255),
        wrap=(82, 62, 40, 255), accent=(126, 88, 38, 255), crystal=(196, 150, 66, 255),
    ),
    "katana_refined": dict(
        outline=(30, 29, 43, 255), shadow=(74, 72, 98, 255), body=(150, 142, 176, 255),
        light=(206, 198, 228, 255), edge=(232, 226, 246, 255), handle=(46, 45, 58, 255),
        wrap=(78, 76, 94, 255), accent=(96, 118, 200, 255), crystal=(124, 229, 248, 255),
    ),
}

FAMILY = {
    "opus": OPUS, "fire": FIRE, "parthenon": PARTHENON, "forest": FOREST,
}


class Grid:
    def __init__(self):
        self.c = [[T for _ in range(SIZE)] for _ in range(SIZE)]

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

    def clean_isolated(self, min_size=4):
        """Flood-fill connected components of opaque pixels and delete any
        component smaller than min_size (kills stray accent specks)."""
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
        im = Image.new("RGBA", (SIZE, SIZE), T)
        for y in range(SIZE):
            for x in range(SIZE):
                if self.c[y][x] != T:
                    im.putpixel((x, y), self.c[y][x])
        return im

    def dump(self, name):
        legend = {}
        rev = {}
        for y in range(SIZE):
            for x in range(SIZE):
                c = self.c[y][x]
                if c == T:
                    continue
                if c not in rev:
                    rev[c] = len(legend)
                    legend[rev[c]] = c
        print(f"--- {name} ---")
        for y in range(SIZE):
            row = []
            for x in range(SIZE):
                c = self.c[y][x]
                if c == T:
                    row.append(".")
                else:
                    row.append(str(rev[c]))
            print("".join(row))
        for k, v in legend.items():
            print(f"  {k}: {v}")


def ops_base(sel):
    s = Grid()
    p = FAMILY[sel]
    hx, hy = (5, 27) if sel in ("fire",) else (5, 27)

    def handle(gx, gy):
        s.line(5, 27, gx, gy, p["handle"], 3)
        # a couple of grip knots (one tone darker)
        s.px(7, 25, p["shadow"])
        s.px(9, 23, p["shadow"])
        s.px(11, 21, p["shadow"])
        return gx, gy

    return s, p, handle


def make_sword(sel):
    s, p, handle = ops_base(sel)
    gx, gy = 14, 19
    handle(gx, gy)
    s.fill_poly([(12, 16), (18, 22), (31, 4)], p["body"])      # blade (tip up-right)
    s.line(13, 15, 30, 4, p["light"])                          # cutting edge highlight
    s.line(17, 21, 29, 5, p["shadow"])                         # spine shadow
    s.fill_poly([(11, 15), (17, 15), (17, 21), (11, 21)], p["shadow"])  # crossguard
    s.px(12, 18, p["edge"]); s.px(12, 19, p["edge"]); s.px(13, 20, p["edge"])
    s.px(14, 18, p["crystal"])                                 # gem in guard centre
    s.px(15, 18, p["accent"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def make_pickaxe(sel):
    s, p, handle = ops_base(sel)
    gx, gy = 13, 19
    handle(gx, gy)
    arc = [(7, 18), (10, 15), (14, 12), (18, 10), (22, 9), (26, 8)]
    for i in range(len(arc) - 1):
        s.line(*arc[i], *arc[i + 1], p["body"], 5)
    s.px(5, 19, p["body"]); s.px(6, 18, p["body"])             # left point
    s.px(27, 7, p["body"]); s.px(28, 6, p["body"])             # right point
    s.line(8, 17, 25, 8, p["shadow"])
    s.line(9, 16, 24, 7, p["light"])
    s.px(13, 13, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def make_axe(sel):
    s, p, handle = ops_base(sel)
    gx, gy = 14, 18
    handle(gx, gy)
    s.fill_poly([(15, 17), (19, 11), (26, 6), (27, 9), (24, 14), (18, 18)], p["body"])
    s.line(19, 11, 26, 6, p["light"])                          # working edge
    s.line(26, 6, 27, 9, p["edge"])
    s.line(24, 14, 18, 18, p["shadow"])
    s.px(17, 15, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def make_shovel(sel):
    s, p, handle = ops_base(sel)
    gx, gy = 12, 21
    handle(gx, gy)
    s.fill_poly([(9, 23), (15, 17), (21, 11), (24, 14), (18, 20), (12, 26)], p["body"])
    s.line(15, 17, 21, 11, p["light"])
    s.line(18, 20, 12, 26, p["shadow"])
    s.line(12, 22, 17, 17, p["accent2"])
    s.px(15, 20, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def make_hoe(sel):
    s, p, handle = ops_base(sel)
    gx, gy = 14, 19
    handle(gx, gy)
    s.line(10, 17, 24, 11, p["body"], 4)                       # top bar
    s.line(21, 12, 24, 16, p["body"], 3)                       # bent working hook
    s.line(11, 16, 23, 10, p["light"])
    s.line(22, 13, 24, 15, p["shadow"])
    s.px(14, 14, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


TOOLS = {
    "sword": make_sword, "pickaxe": make_pickaxe, "axe": make_axe,
    "shovel": make_shovel, "hoe": make_hoe,
}


def make_katana(name, long=False, wide=False):
    p = KATANAS[name]
    s = Grid()
    # --- grip (bottom-left, longer + thinner for long_katana) ---
    grip = Blade()
    gs = (5, 28) if long else (6, 28)
    ge = (16, 17) if long else (15, 18)
    grip.line(gs, ge, p["handle"])
    for x, y, c in grip.pixels:
        s.px(x, y, c)
    # diagonal wrap knots (a katana grip is diamond-wrapped)
    for t in (0.25, 0.45, 0.65, 0.85):
        x, y = grip.pt_on(gs, ge, t)
        s.px(round(x), round(y), p["wrap"])
    # --- tsuba (guard): a small compact square perpendicular to the blade ---
    s.fill_poly([(ge[0] - 1, ge[1] - 1), (ge[0] + 3, ge[1] - 1),
                 (ge[0] + 3, ge[1] + 3), (ge[0] - 1, ge[1] + 3)], p["body"])
    s.px(ge[0] + 1, ge[1], p["crystal"])   # gem set in the tsuba
    # --- blade: gently curved bezier from tsuba to tip (up-right) ---
    blade = Blade()
    blade.accents = _katana_accents(name, p)
    bx0, by0 = ge[0] + 2, ge[1] - 1
    tip = (31, 2) if long else (30, 4)
    # a real curve: midpoint is lifted perpendicular to the blade axis
    mid = ((bx0 + tip[0]) // 2, (by0 + tip[1]) // 2 + (4 if long else 2))
    blade.bezier3(bx0, by0, mid[0], mid[1], tip[0], tip[1], p["body"], p["light"], p["shadow"], wide)
    for x, y, c in blade.pixels:
        s.px(x, y, c)
    # signature accents placed ON the blade path (no detached specks)
    for frac, col in blade.accents:
        if blade.path:
            x, y = blade.path[min(len(blade.path) - 1, int(len(blade.path) * frac))]
            s.px(x, y, col)
            s.px(x - 1, y, col)
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def _katana_accents(name, p):
    if name == "long_katana":
        return [(0.55, p["accent"]), (0.80, p["accent"]), (0.40, p["crystal"])]
    if name == "katana_gold":
        return [(0.55, p["shadow"]), (0.78, p["shadow"])]
    if name == "katana_op":
        return [(0.55, p["accent"]), (0.78, p["accent"]), (0.42, p["crystal"])]
    if name == "katana_refined":
        return [(0.55, p["accent"]), (0.78, p["accent"]), (0.40, p["crystal"])]
    return []


class Blade:
    """Builds a clean stepped diagonal blade (bezier) with a light edge +
    shadow spine, plus grip helpers."""

    def __init__(self):
        self.pixels = []
        self.path = []

    @staticmethod
    def pt_on(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    def line(self, a, b, col):
        x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, col, False)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def px(self, x, y, col, wide):
        self.pixels.append((x, y, col))
        self.path.append((x, y))
        if wide:
            self.pixels.append((x - 1, y, col))
            self.pixels.append((x + 1, y, col))

    def bezier3(self, x0, y0, cx, cy, x1, y1, body, light, shadow, wide):
        """Sample a quadratic bezier; draw body along it with a one-pixel
        light edge above and shadow spine below."""
        steps = max(abs(x1 - x0), abs(y1 - y0), abs(cx - x0), abs(cy - y0)) * 2
        last = None
        for i in range(steps + 1):
            t = i / steps
            x = round((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1)
            y = round((1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1)
            pad = 0 if not wide else 0
            self.px(x, y, body, wide)
            self.px(x, y - 1, light, False)
            self.px(x, y + 1, shadow, False)


def make_warhammer():
    p = OPUS
    s = Grid()
    s.line(4, 28, 13, 19, p["handle"], 3)
    s.px(6, 26, p["shadow"]); s.px(9, 23, p["shadow"])
    # two massive rect hammer faces centred on the head
    s.fill_poly([(11, 18), (24, 18), (24, 6), (11, 6)], p["body"])
    s.fill_poly([(12, 17), (23, 17), (23, 7), (12, 7)], p["light"])
    s.line(12, 8, 23, 8, p["handle"])
    s.line(12, 16, 23, 16, p["handle"])
    s.line(16, 17, 16, 7, p["edge"])
    s.line(19, 17, 19, 7, p["shadow"])
    s.fill_poly([(16, 12), (19, 12), (19, 14), (16, 14)], p["accent"])  # blue groove
    s.px(17, 12, p["crystal"]); s.px(18, 13, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


def make_labrys():
    p = PARTHENON
    s = Grid()
    s.line(5, 27, 14, 18, p["handle"], 3)
    s.px(7, 25, p["hmix"]); s.px(11, 21, p["hmix"])
    s.fill_poly([(12, 18), (24, 18), (24, 6), (12, 6)], p["body"])   # bronze centre block
    s.fill_poly([(9, 15), (12, 12), (12, 6), (9, 9)], p["body"])     # left blade
    s.fill_poly([(24, 15), (27, 12), (27, 6), (24, 9)], p["body"])   # right blade
    s.line(9, 9, 9, 15, p["light"]); s.line(27, 9, 27, 15, p["light"])
    s.line(12, 12, 12, 6, p["shadow"]); s.line(24, 12, 24, 6, p["shadow"])
    s.px(18, 12, p["crystal"]); s.px(18, 13, p["crystal"])
    s.clean_isolated()
    s.outline(p["outline"])
    return s, p


# name -> builder
# NOTE: katana/long_katana/katana_op/katana_gold/katana_refined/opus_warhammer
# and the whole opus tool family are full GeckoLib 3D weapons now
# (see scripts/generate_opus.py). Deliberately absent here so a re-run can
# never overwrite their models/item/*.json or geo/animation assets.
BUILDERS = {
    "parthenon_axe": make_labrys,
}
FAMILY_PREFIX = {"fire": "fire", "parthenon": "parthenon", "forest": "dark_forest"}

for fam, prefix in FAMILY_PREFIX.items():
    for kind in ("sword", "pickaxe", "axe", "shovel", "hoe"):
        if f"{fam}_axe" == "parthenon_axe" and kind == "axe":  # handled by labrys
            continue
        BUILDERS[f"{prefix}_{kind}"] = (
            lambda f=fam, k=kind: make_tool_family(f, k))


def make_tool_family(sel, kind):
    return TOOLS[kind](sel)


ASSET_ORDER = [
    "fire_sword", "fire_pickaxe", "fire_axe", "fire_shovel", "fire_hoe",
    "parthenon_sword", "parthenon_pickaxe", "parthenon_axe", "parthenon_shovel", "parthenon_hoe",
    "dark_forest_sword", "dark_forest_pickaxe", "dark_forest_axe", "dark_forest_shovel", "dark_forest_hoe",
]


def glow_swap(im, pal):
    out = im.copy()
    px = out.load()
    for y in range(SIZE):
        for x in range(SIZE):
            c = px[x, y]
            if c in pal["_glow"]:
                px[x, y] = pal["_glow"][c]
    return out


def main():
    dump_only = "--dump" in sys.argv
    written = []
    for name in ASSET_ORDER:
        if name == "opus_sword":  # no vanilla opus_sword item; opus uses katanas
            continue
        builder = BUILDERS.get(name)
        if builder is None:
            continue
        g, p = builder()
        if dump_only:
            g.dump(name)
            continue
        im = g.render()
        assert im.size == (SIZE, SIZE) and im.mode == "RGBA"
        frame2 = glow_swap(im, _pal_glow(name, p))
        sheet = Image.new("RGBA", (SIZE, SIZE * 2), T)
        sheet.paste(im, (0, 0))
        sheet.paste(frame2, (0, SIZE))
        sheet.save(ITEMS / f"{name}.png")
        (ITEMS / f"{name}.png.mcmeta").write_text(
            json.dumps({"animation": {"frametime": 4, "interpolate": False}}, indent=2),
            encoding="utf-8")
        written.append(name)
    if not dump_only:
        for name in written:
            write_model(name)
        save_preview(written)
        print(f"wrote {len(written)} sprites (2-frame) / models / mcmeta -> {ITEMS.relative_to(ROOT)}")
    else:
        print(f"dry-run of {len(ASSET_ORDER)} assets")
    return written


def _pal_glow(name, pal):
    crystal = pal.get("crystal", pal.get("accent2"))
    accent = pal.get("accent")
    light = pal.get("light", pal.get("body"))
    g = {}
    g.setdefault("_glow", {})
    # glow = shift crystal/accent toward white; light stays
    g["_glow"][crystal] = _mix(crystal, (255, 255, 255, 255), 0.45)
    if accent:
        g["_glow"][accent] = _mix(accent, (255, 255, 255, 255), 0.30)
    g["_glow"][light] = _mix(light, (255, 255, 255, 255), 0.18)
    return g


def _mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(4))


def write_model(name):
    model = {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"opusvsexe:item/{name}"},
    }
    if name in KATANAS or name in ("opus_warhammer", "parthenon_axe"):
        model["display"] = KATANA_DISPLAY
    (MODELS / f"{name}.json").write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")


KATANA_DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "gui": {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [0.62, 0.62, 0.62]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [0.75, 0.75, 0.75]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
}


def save_preview(names):
    columns, cell = 5, 96
    rows = (len(names) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell, rows * cell), (28, 28, 32, 255))
    for index, name in enumerate(names):
        im = Image.open(ITEMS / f"{name}.png").convert("RGBA")
        x, y = (index % columns) * cell, (index // columns) * cell
        sheet.alpha_composite(im.resize((64, 64), Image.Resampling.NEAREST), (x + 16, y + 16))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW)


if __name__ == "__main__":
    main()
