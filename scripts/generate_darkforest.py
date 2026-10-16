#!/usr/bin/env python3
"""Dark Forest toolset — single generator for all 5 tools.

Shared framework + Dark Forest palette/painters; per-tool BONES/ANIMS tables.
Lessons applied: M1 (uv object+uv_size), M6 (static idle), M7 (upright display
values live in model JSONs, not here), M8 (single source per tool).

Outputs under src/main/resources/assets/opusvsexe/:
  geo/dark_forest/tool_<name>.geo.json
  animations/dark_forest/tool_<name>.animation.json
  textures/dark_forest/item/<name>.png
"""
import json
import math
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe")

TEX_W, TEX_H = 256, 256
S = 4
PAD = 2

# ---------------------------------------------------------------- palette
# Charcoal fractured plates + cold gray edges
IRON = (35, 34, 40)
IRON_DK = (22, 21, 26)
IRON_SH = (28, 27, 33)
EDGE = (110, 110, 120)
EDGE_HL = (150, 150, 160)
# Violet arcane cracks
CRACK_DK = (42, 18, 69)
CRACK = (139, 63, 217)
CRACK_HL = (217, 167, 255)
# Root wood: brown-black twisted
ROOTWOOD = (42, 31, 24)
ROOTWOOD_DK = (23, 18, 16)
ROOTWOOD_HL = (61, 44, 30)
# Night flowers
PETAL = (107, 63, 160)
PETAL_DK = (70, 40, 110)
PETAL_HL = (139, 95, 217)
CORE = (224, 179, 255)
CORE_WH = (245, 235, 255)
# Teal fungal speckle
TEAL = (46, 139, 139)
TEAL_HL = (95, 217, 217)
# Crystal core
CRYS_DK = (45, 20, 80)
CRYS = (120, 60, 200)
CRYS_HL = (210, 160, 255)

C = lambda o, s, m, **kw: dict(o=o, s=s, m=m, **kw)
FACES = ["north", "south", "east", "west", "up", "down"]
# faces that may carry flower / crack / meander patterns
PAT_FACES = ("south", "north", "up", "down")


def face_dims(size, face):
    sx, sy, sz = size
    if face in ("north", "south"):
        return (sx, sy)
    if face in ("east", "west"):
        return (sz, sy)
    return (sx, sz)


def pack_uv(bones):
    items = []
    for bi, b in enumerate(bones):
        for ci, c in enumerate(b["cubes"]):
            for f in FACES:
                wu, hu = face_dims(c["s"], f)
                items.append((bi, ci, f, int(math.ceil(wu * S)), int(math.ceil(hu * S))))
    items.sort(key=lambda t: -t[4])
    rects = {}
    x = y = row_h = 0
    for bi, ci, f, w, h in items:
        if w <= 0 or h <= 0:
            rects[(bi, ci, f)] = (0, 0, 1, 1)
            continue
        if x + w + PAD > TEX_W:
            x = 0
            y += row_h + PAD
            row_h = 0
        if y + h + PAD > TEX_H:
            raise RuntimeError("UV overflow")
        rects[(bi, ci, f)] = (x, y, w, h)
        x += w + PAD
        row_h = max(row_h, h)
    return rects


def shade(d, box, base, hl, sh):
    x, y, w, h = box
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=base)
    if w >= 2 and h >= 2:
        d.line([x, y, x + w - 1, y], fill=hl)
        d.line([x, y, x, y + h - 1], fill=hl)
        d.line([x, y + h - 1, x + w - 1, y + h - 1], fill=sh)
        d.line([x + w - 1, y, x + w - 1, y + h - 1], fill=sh)


def crack(d, box, seed):
    """Jagged arcane fissure: dark trench -> violet -> bright core."""
    import random
    rnd = random.Random(seed * 31 + 7)
    x, y, w, h = box
    cx = x + w // 2 + rnd.randrange(-1, 2)
    for yy in range(y + 1, y + h - 1):
        cx += rnd.randrange(-1, 2)
        cx = max(x + 1, min(x + w - 2, cx))
        d.point((cx, yy), fill=CRACK_DK)
        d.point((cx + (1 if cx < x + w - 2 else -1), yy), fill=CRACK)
        if (yy + seed) % 3 == 0:
            d.point((cx, yy), fill=CRACK_HL)


def roots(d, box, seed):
    """Twisted diagonal root bands + speckle."""
    import random
    rnd = random.Random(seed * 17 + 3)
    x, y, w, h = box
    for i in range(-h, w, 5):
        for k in range(3):
            xx = x + i + k
            yy0 = y + max(0, -i - k)
            yy1 = y + min(h - 1, w - i - k)
            if 0 <= xx - x < w and yy0 <= yy1:
                d.line([xx, yy0, xx, yy1], fill=ROOTWOOD_HL if k == 1 else ROOTWOOD_DK)
    for _ in range(max(2, w * h // 60)):
        d.point((x + rnd.randrange(w), y + rnd.randrange(h)),
                fill=TEAL_HL if rnd.random() < 0.4 else TEAL)


def flower(d, box, petals=6):
    """Night flower: dark socket, violet petals, luminous core (front faces)."""
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    r = min(w, h) / 2 - 1
    if r < 2:
        return
    import math as m
    for i in range(petals):
        a = m.pi * 2 * i / petals - m.pi / 2
        for rr in (r, r - 1):
            px, py = int(cx + m.cos(a) * rr * 1.15), int(cy + m.sin(a) * rr * 1.15)
            if x <= px < x + w and y <= py < y + h:
                d.point((px, py), fill=PETAL_HL if rr == r else PETAL)
    d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=CORE)
    d.point((int(cx), int(cy)), fill=CORE_WH)


def paint_face(d, box, mat, face, seed, pat):
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    if mat == "iron":
        shade(d, box, IRON, IRON_SH, IRON_DK)
        if face in PAT_FACES and (pat == "crack" or (pat is None and seed % 3 == 0)):
            crack(d, box, seed)
        if w >= 10 and h >= 6 and face in PAT_FACES:
            d.line([x + 1, y + h // 2, x + w - 2, y + h // 2], fill=IRON_DK)
    elif mat == "edge":
        shade(d, box, EDGE, EDGE_HL, IRON_DK)
    elif mat == "root":
        shade(d, box, ROOTWOOD, ROOTWOOD_HL, ROOTWOOD_DK)
        roots(d, box, seed)
    elif mat == "charcoal":
        shade(d, box, IRON_DK, IRON, (10, 9, 12))
        if w >= 8 and h >= 8:
            d.rectangle([x + 1, y + 1, x + w - 2, y + h - 2], outline=IRON)
    elif mat == "crystal":
        shade(d, box, CRYS_DK, CRYS, CRYS_DK)
        if w >= 3:
            d.line([x + w // 2, y, x + w // 2, y + h - 1], fill=CRYS_HL)
            if w >= 5:
                d.line([x + w // 2 - 1, y, x + w // 2 - 1, y + h - 1], fill=CRYS)
    elif mat == "petal":
        if face in PAT_FACES and pat in ("flower6", "flower4", None):
            shade(d, box, PETAL_DK, PETAL, PETAL_DK)
            flower(d, box, 6 if pat != "flower4" else 4)
        else:
            shade(d, box, PETAL, PETAL_HL, PETAL_DK)
    elif mat == "core":
        shade(d, box, CORE, CORE_WH, PETAL)
        d.point((x, y), fill=CORE_WH)
    elif mat == "fungus":
        shade(d, box, ROOTWOOD_DK, ROOTWOOD, (8, 8, 10))
        import random
        rnd = random.Random(seed)
        for _ in range(max(2, w * h // 40)):
            d.point((x + rnd.randrange(w), y + rnd.randrange(h)),
                    fill=TEAL_HL if rnd.random() < 0.5 else TEAL)
    else:
        shade(d, box, (255, 0, 255), (255, 0, 255), (255, 0, 255))


def chan(frames):
    return {(f"{t:.3f}".rstrip("0").rstrip(".")): {"vector": list(v)}
            for t, v in frames}


def build_geo(name, bones, rects):
    out = []
    for bi, b in enumerate(bones):
        jb = {"name": b["name"], "pivot": b["pivot"]}
        if b["parent"]:
            jb["parent"] = b["parent"]
        cubes = []
        for ci, c in enumerate(b["cubes"]):
            uv = {}
            for f in FACES:
                x, y, w, h = rects[(bi, ci, f)]
                uv[f] = {"uv": [x, y, x + w, y + h], "uv_size": [w, h]}
            # EPS 0.02 volumetric overlap: stacked segments meet exactly at
            # shared planes by construction; expanding every cube a hair turns
            # exact coplanar same-normal contacts into harmless intersections
            # and kills z-fighting without changing the silhouette.
            EPS = 0.01
            o, s = c["o"], c["s"]
            jc = {"origin": [o[0] - EPS, o[1] - EPS, o[2] - EPS],
                  "size": [s[0] + 2 * EPS, s[1] + 2 * EPS, s[2] + 2 * EPS],
                  "uv": uv}
            if "rot" in c:
                jc["pivot"] = c.get("cp", b["pivot"])
                jc["rotation"] = c["rot"]
            cubes.append(jc)
        if cubes:
            jb["cubes"] = cubes
        out.append(jb)
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.df_" + name,
                "texture_width": TEX_W,
                "texture_height": TEX_H,
                "visible_bounds_width": 3,
                "visible_bounds_height": 4,
                "visible_bounds_offset": [0, 0, 0],
            },
            "bones": out,
        }],
    }


def paint_texture(bones, rects):
    img = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    seed = 0
    for bi, b in enumerate(bones):
        for ci, c in enumerate(b["cubes"]):
            pat = c.get("pat")
            for f in FACES:
                paint_face(d, rects[(bi, ci, f)], c["m"], f, seed, pat)
                seed += 1
    return img

def mirror(cubes):
    out = []
    for c in cubes:
        o = [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]]
        kw = {}
        if "rot" in c:
            kw["rot"] = [c["rot"][0], c["rot"][1], -c["rot"][2]]
            cp = c.get("cp")
            if cp:
                kw["cp"] = [-cp[0], cp[1], cp[2]]
        if "pat" in c:
            kw["pat"] = c["pat"]
        out.append(C(o, list(c["s"]), c["m"], **kw))
    return out


def B(name, parent, pivot, cubes):
    return dict(name=name, parent=parent, pivot=pivot, cubes=cubes)


# ================================================================ SWORD
SWORD_BONES = [
    B("root", None, [0, 0, 0], []),
    B("sword", "root", [0, 0, 0], []),
    B("blade", "sword", [0, 11, 0], [
        C([-1.5, 4, -0.7], [3, 15, 1.4], "iron"),
        C([-0.3, 4, 0.7], [0.6, 15, 0.25], "iron", pat="crack"),
    ]),
    B("edge_l", "sword", [-1.7, 11, 0], [
        C([-1.9, 4, -0.75], [0.5, 15, 1.5], "edge"),
    ]),
    B("edge_r", "sword", [1.7, 11, 0], [
        C([1.4, 4, -0.75], [0.5, 15, 1.5], "edge"),
    ]),
    B("tip", "sword", [0, 21.5, 0], [
        C([-1.6, 19, -0.7], [1.7, 2.0, 1.4], "iron"),
        C([-0.1, 19, -0.7], [1.7, 2.0, 1.4], "iron"),
        C([-2.0, 19, -0.75], [0.5, 2.0, 1.5], "edge"),
        C([1.5, 19, -0.75], [0.5, 2.0, 1.5], "edge"),
        C([-1.2, 21, -0.65], [1.3, 1.5, 1.3], "iron"),
        C([-0.1, 21, -0.65], [1.3, 1.5, 1.3], "iron"),
        C([-1.6, 21, -0.7], [0.5, 1.5, 1.4], "edge"),
        C([1.1, 21, -0.7], [0.5, 1.5, 1.4], "edge"),
        C([-0.85, 22.5, -0.6], [0.95, 1.2, 1.2], "iron"),
        C([-0.1, 22.5, -0.6], [0.95, 1.2, 1.2], "iron"),
        C([-1.15, 22.5, -0.65], [0.4, 1.2, 1.3], "edge"),
        C([0.75, 22.5, -0.65], [0.4, 1.2, 1.3], "edge"),
        C([-0.5, 23.7, -0.55], [0.6, 1.0, 1.1], "iron"),
        C([-0.1, 23.7, -0.55], [0.6, 1.0, 1.1], "iron"),
        C([-0.45, 24.7, -0.5], [0.9, 0.6, 1.0], "edge"),
    ]),
    B("thorns_l", "sword", [-2, 12, 0], [
        C([-2.6, 6, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([-2.6, 9, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([-2.6, 12, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([-2.6, 15, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([-2.5, 18, -0.4], [0.8, 0.6, 0.8], "edge"),
    ]),
    B("thorns_r", "sword", [2, 12, 0], [
        C([1.7, 7.5, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([1.7, 10.5, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([1.7, 13.5, -0.4], [0.9, 0.6, 0.9], "edge"),
        C([1.7, 16.5, -0.4], [0.9, 0.6, 0.9], "edge"),
    ]),
    B("guard", "sword", [0, 2, 0], [
        C([-4, 1.2, -0.9], [8, 1.8, 1.8], "root"),
        C([-5.2, 2.2, -0.7], [1.6, 1.0, 1.2], "root"),
        C([-6.0, 3.0, -0.6], [1.2, 0.9, 1.0], "root"),
        C([3.8, 2.0, -0.7], [1.8, 1.0, 1.2], "root"),
        C([5.0, 2.8, -0.6], [1.4, 0.9, 1.0], "root"),
        C([5.8, 3.5, -0.5], [1.0, 0.8, 0.9], "root"),
        C([-3.5, -0.2, -0.7], [1.4, 1.6, 1.2], "root"),
        C([2.8, -0.4, -0.7], [1.2, 1.8, 1.2], "root"),
        # ricasso: bridges guard top (3.0) into blade bottom (4.0) — no gap
        C([-1, 2.2, -0.6], [2, 2.2, 1.2], "iron", pat="crack"),
    ]),
    B("guard_flower", "sword", [0, 2.1, 1.0], [
        C([-1.3, 0.9, 0.7], [2.6, 2.6, 0.5], "charcoal"),
        C([-1.2, 1.0, 1.1], [2.4, 2.4, 0.3], "petal", pat="flower6"),
        C([-0.35, 3.0, 1.0], [0.7, 1.0, 0.4], "petal"),
        C([-0.35, 1.0, 1.0], [0.7, 1.0, 0.4], "petal"),
        C([0.5, 1.95, 1.0], [1.0, 0.7, 0.4], "petal"),
        C([-1.2, 1.95, 1.0], [1.0, 0.7, 0.4], "petal"),
        C([-0.4, 1.9, 1.3], [0.8, 0.8, 0.3], "core"),
    ]),
    B("handle", "sword", [0, -5, 0], [
        # shaft runs up INTO the guard flower (top y=1 overlaps flower bottom 0.9)
        C([-1, -9, -1], [2, 10, 2], "root"),
        C([-1.3, -2, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, -5.5, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, -8, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([1.0, -3.5, -0.5], [0.5, 0.5, 0.5], "edge"),
        C([-1.5, -6.5, -0.5], [0.5, 0.5, 0.5], "edge"),
        C([-0.8, -4, 1.0], [0.6, 0.6, 0.4], "fungus"),
        C([0.4, -7, 1.0], [0.6, 0.6, 0.4], "fungus"),
    ]),
    B("pommel", "sword", [0, -11, 0], [
        # body top overlaps handle shaft bottom (y=-9) — no gap
        C([-1.6, -12.4, -1.6], [3.2, 3.6, 3.2], "charcoal"),
        C([-1.1, -11.9, 1.5], [2.2, 2.2, 0.3], "petal", pat="flower6"),
        C([-0.4, -11.2, 1.7], [0.8, 0.8, 0.3], "core"),
        C([-1, -13.2, -1], [2, 0.8, 2], "charcoal"),
    ]),
    B("fx_sword", "sword", [0, 12, 1.0], []),
    B("fx_pommel", "sword", [0, -11, 1.8], []),
]

SWORD_ANIMS = {
    "idle": (True, 3.0, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "sword": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "guard_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-28, 0, 0]), (0.2, [-22, 0, 0]),
                                     (0.28, [-30, 0, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "guard_flower": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.2, 1.2, 1.2]),
                                        (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "attack_alt": (False, 0.4, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-24, -6, 0]), (0.2, [-19, -4, 0]),
                                     (0.28, [-26, -7, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, -2.5]), (0.4, [0, 0, 0])])},
        "guard_flower": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.2, 1.2, 1.2]),
                                        (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "shadowstep_cast": (False, 0.4, {
        "sword": {
            "rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                              (0.25, [10, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, 0, 0]), (0.12, [0, -1.5, 0]),
                              (0.25, [0, 0.5, 0]), (0.4, [0, 0, 0])]),
        },
        "guard_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.35, 1.35, 1.35]),
                                        (0.4, [1, 1, 1])])},
    }),
    "gloom_pulse": (True, 2.6, {
        "guard_flower": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                        (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "tip": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                               (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ============================================================== PICKAXE
PICKAXE_BONES = [
    B("root", None, [0, 0, 0], []),
    B("pickaxe", "root", [0, 0, 0], []),
    B("head", "pickaxe", [0, 11, 0], []),
    B("housing", "head", [0, 11.5, 0], [
        C([-2, 9, -1.5], [4, 5, 3], "charcoal"),
        C([-1.5, 14, -1.2], [3, 1, 2.4], "iron"),
        C([-2.2, 9.5, 1.5], [4.4, 0.6, 0.35], "edge"),
        C([-2.2, 12.9, 1.5], [4.4, 0.6, 0.35], "edge"),
    ]),
    B("crystal", "head", [0, 11, 1.2], [
        C([-0.9, 9.8, 0.9], [1.8, 2.4, 0.6], "charcoal"),
        C([-0.55, 10.1, 1.2], [1.1, 1.8, 0.5], "crystal"),
        C([-0.3, 11.9, 1.2], [0.6, 0.8, 0.5], "crystal"),
    ]),
    B("beak_l", "head", [-2, 11.5, 0], [
        C([-6, 10.5, -0.9], [4, 2.5, 1.8], "iron"),
        C([-8.5, 9.3, -0.8], [3, 2.2, 1.6], "iron"),
        C([-10.5, 7.8, -0.7], [2.5, 2, 1.4], "iron"),
        C([-11.4, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([-8.5, 9.0, -0.75], [6, 0.5, 1.5], "edge"),
        C([-4, 12.6, -0.8], [2, 0.7, 1.6], "edge"),
    ]),
    B("beak_r", "head", [2, 11.5, 0], [
        C([2, 10.5, -0.9], [4, 2.5, 1.8], "iron"),
        C([5.5, 9.3, -0.8], [3, 2.2, 1.6], "iron"),
        C([8, 7.8, -0.7], [2.5, 2, 1.4], "iron"),
        C([10.2, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([2.5, 9.0, -0.75], [6, 0.5, 1.5], "edge"),
        C([2, 12.6, -0.8], [2, 0.7, 1.6], "edge"),
    ]),
    B("handle", "pickaxe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "root"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-0.8, 2.5, 1.0], [1.6, 1.6, 0.3], "petal", pat="flower4"),
        C([-0.8, -5, 1.0], [0.6, 0.6, 0.4], "fungus"),
        C([0.3, -3, 1.0], [0.6, 0.6, 0.4], "fungus"),
    ]),
    B("pommel", "pickaxe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-1.1, -3.9, 1.5], [2.2, 2.2, 0.3], "petal", pat="flower6"),
        C([-0.4, -3.2, 1.7], [0.8, 0.8, 0.3], "core"),
        C([-1, -5.4, -1], [2, 0.8, 2], "charcoal"),
    ]),
    B("fx_pick", "pickaxe", [0, 11, 1.5], []),
    B("fx_pommel", "pickaxe", [0, -2.8, 1.8], []),
]

PICKAXE_ANIMS = {
    "idle": (True, 3.0, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "pickaxe": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "crystal": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
    }),
    "mine": (False, 0.35, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.07, [8, 0, 0]),
                                      (0.14, [-18, 0, 0]), (0.2, [-14, 0, 0]),
                                      (0.26, [-20, 0, 0]), (0.35, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.07, [0, 0, -2]),
                                   (0.14, [0, 0, 1.5]), (0.35, [0, 0, 0])])},
        "crystal": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.25, 1.25, 1.25]),
                                   (0.28, [1, 1, 1]), (0.35, [1, 1, 1])])},
    }),
    "attack": (False, 0.45, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                      (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                      (0.32, [-27, 0, 0]), (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.45, [0, 0, 0])])},
        "crystal": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                   (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "awaken_cast": (False, 0.5, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.15, [-16, 0, 0]),
                                      (0.3, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "crystal": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.35, 1.35, 1.35]),
                                   (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "beak_l": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
        "beak_r": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
    }),
    "gloom_pulse": (True, 2.6, {
        "crystal": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                   (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# Axe head is authored big-blade-LEFT then mirrored so the functional
# crescent sits at +X: with the family yaw (-90) +X maps to world-forward
# in both first and third person (vanilla axe convention). Authoring it at
# -X held the axe backwards (big blade trailing). This also matches the
# concept art (grand crescent upper-right).
_AXE_BIG_L = [
    C([-7, 10, -0.9], [5, 4, 1.8], "iron", pat="crack"),
    C([-10, 11, -0.8], [3.5, 5, 1.6], "iron", pat="crack"),
    C([-12, 8, -0.7], [2.5, 4, 1.4], "iron"),
    C([-10.3, 16, -0.75], [2.6, 1.8, 1.5], "iron"),
    C([-10, 17.8, -0.7], [1.8, 1.6, 1.4], "iron"),
    C([-9.7, 19.4, -0.65], [1.2, 1.2, 1.3], "edge"),
    C([-10.3, 6.2, -0.7], [2.6, 1.8, 1.5], "iron"),
    C([-10, 4.6, -0.65], [1.8, 1.6, 1.4], "iron"),
    C([-9.7, 3.4, -0.6], [1.2, 1.2, 1.3], "edge"),
    C([-10.5, 15.2, -0.75], [4, 0.8, 1.5], "edge"),
    C([-12.2, 8, -0.65], [0.7, 8, 1.3], "edge"),
    C([-7, 9.5, -0.85], [5, 0.6, 1.7], "edge"),
]
_AXE_SMALL_R = [
    C([2, 10.5, -0.7], [3, 3, 1.4], "iron"),
    C([4.5, 9.5, -0.6], [1.5, 2.5, 1.2], "iron"),
    C([4.8, 9.3, -0.65], [0.6, 3, 1.3], "edge"),
]
# ================================================================= AXE
AXE_BONES = [
    B("root", None, [0, 0, 0], []),
    B("axe", "root", [0, 0, 0], []),
    B("head", "axe", [0, 10, 0], []),
    B("blade_main", "head", [4, 12, 0], mirror(_AXE_BIG_L)),
    B("blade_back", "head", [-3, 11, 0], mirror(_AXE_SMALL_R)),
    B("housing", "head", [0, 11.5, 0], [
        C([-2, 9, -1.3], [4, 5, 2.6], "charcoal"),
        C([-2.2, 9.5, 1.3], [4.4, 0.6, 0.35], "edge"),
        C([-2.2, 12.9, 1.3], [4.4, 0.6, 0.35], "edge"),
    ]),
    B("head_flower", "head", [0, 11.8, 1.2], [
        C([-1.3, 10.4, 1.2], [2.6, 2.6, 0.4], "charcoal"),
        C([-1.2, 10.5, 1.5], [2.4, 2.4, 0.3], "petal", pat="flower6"),
        C([-2.2, 11.5, 1.0], [1.2, 0.8, 0.4], "petal"),
        C([1.0, 11.5, 1.0], [1.2, 0.8, 0.4], "petal"),
        C([-0.4, 11.4, 1.7], [0.8, 0.8, 0.3], "core"),
    ]),
    B("handle", "axe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "root"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([1.0, 3.0, -0.5], [0.5, 0.5, 0.5], "edge"),
        C([-1.5, -0.5, 1.0], [0.6, 0.6, 0.4], "fungus"),
    ]),
    B("pommel", "axe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-1.1, -3.9, 1.5], [2.2, 2.2, 0.3], "petal", pat="flower6"),
        C([-0.4, -3.2, 1.7], [0.8, 0.8, 0.3], "core"),
        C([-1, -5.4, -1], [2, 0.8, 2], "charcoal"),
    ]),
    B("fx_axe", "axe", [0, 11, 1.5], []),
    B("fx_pommel", "axe", [0, -2.8, 1.8], []),
]

AXE_ANIMS = {
    "idle": (True, 3.0, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "axe": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.45, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                  (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                  (0.32, [-27, 0, 0]), (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.45, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                       (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "cleave_cast": (False, 0.7, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [14, 0, 0]),
                                  (0.3, [-30, 0, 0]), (0.45, [-22, 0, 0]),
                                  (0.7, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.35, 1.35, 1.35]),
                                       (0.5, [1, 1, 1]), (0.7, [1, 1, 1])])},
        "blade_main": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.05, 1.05, 1.05]),
                                      (0.55, [1, 1, 1]), (0.7, [1, 1, 1])])},
    }),
    "gloom_pulse": (True, 2.6, {
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                       (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ============================================================== SHOVEL
SHOVEL_BONES = [
    B("root", None, [0, 0, 0], []),
    B("shovel", "root", [0, 0, 0], []),
    B("head", "shovel", [0, 9, 0], []),
    B("head_frame", "head", [0, 14, 0], [
        C([-4.3, 9.5, -0.8], [1.4, 3, 1.6], "iron"),
        C([2.9, 9.5, -0.8], [1.4, 3, 1.6], "iron"),
        C([-4.6, 12, -0.8], [1.4, 4, 1.6], "iron"),
        C([3.2, 12, -0.8], [1.4, 4, 1.6], "iron"),
        C([-3.9, 15, -0.8], [1.3, 4.5, 1.6], "iron"),
        C([2.6, 15, -0.8], [1.3, 4.5, 1.6], "iron"),
        C([-1.8, 18.5, -0.8], [3.6, 2.2, 1.6], "iron"),
        C([-0.5, 20.4, -0.5], [1, 1, 1], "edge"),
    ]),
    B("head_panel", "head", [0, 14, 0], [
        # panel foot reaches down INTO the flower (bottom y=8.6 overlaps
        # flower top 9.2, z overlaps) — no gap between head and socket
        C([-3, 8.6, -0.6], [6, 7.4, 1.2], "iron", pat="crack"),
        C([-2.4, 15, -0.6], [4.8, 4, 1.2], "iron", pat="crack"),
        C([-1.4, 18, -0.6], [2.8, 2, 1.2], "iron", pat="crack"),
        C([-0.3, 10, 0.6], [0.6, 8, 0.25], "iron", pat="crack"),
    ]),
    B("head_flower", "head", [0, 8.0, 1.0], [
        C([-1.5, 6.6, 0.6], [3, 2.6, 0.6], "charcoal"),
        C([-1.2, 6.9, 1.1], [2.4, 2.2, 0.3], "petal", pat="flower6"),
        C([-2.3, 7.5, 0.8], [1.0, 0.7, 0.4], "petal"),
        C([1.3, 7.5, 0.8], [1.0, 0.7, 0.4], "petal"),
        C([-0.4, 7.6, 1.3], [0.8, 0.8, 0.3], "core"),
    ]),
    B("collar", "head", [0, 5.6, 0], [
        C([-1.5, 4.4, -1.5], [3, 2.4, 3], "charcoal"),
    ]),
    B("handle", "shovel", [0, 0, 0], [
        C([-1, -1, -1], [2, 5.4, 2], "root"),
        C([-1.3, 3.4, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, -1.4, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([1.0, 1.0, -0.5], [0.5, 0.5, 0.5], "edge"),
        C([-0.8, -0.5, 1.0], [0.6, 0.6, 0.4], "fungus"),
    ]),
    B("pommel", "shovel", [0, -2.9, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -5.2, -1.6], [3.2, 4.4, 3.2], "charcoal"),
        C([-1.1, -4.7, 1.5], [2.2, 2.2, 0.3], "petal", pat="flower6"),
        C([-0.4, -4.0, 1.7], [0.8, 0.8, 0.3], "core"),
        C([-1, -6.0, -1], [2, 0.8, 2], "charcoal"),
    ]),
    B("fx_shovel", "shovel", [0, 8, 1.5], []),
    B("fx_pommel", "shovel", [0, -3.6, 1.8], []),
]

SHOVEL_ANIMS = {
    "idle": (True, 3.0, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "shovel": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "dig": (False, 0.45, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.06, [6, 0, 0]),
                                     (0.12, [-10, 0, 0]), (0.18, [-16, 0, 0]),
                                     (0.22, [-13, 0, 0]), (0.3, [-18, 0, 0]),
                                     (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]),
                                   (0.12, [0, 0, 1.5]), (0.45, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.2, 1.2, 1.2]),
                                       (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                     (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                     (0.32, [-27, 0, 0]), (0.4, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                       (0.32, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "excavate_cast": (False, 0.5, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                     (0.25, [-20, 0, 0]), (0.5, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.35, 1.35, 1.35]),
                                       (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "head_frame": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.04, 1.04, 1.04]),
                                      (0.5, [1, 1, 1])])},
    }),
    "gloom_pulse": (True, 2.6, {
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                       (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ================================================================== HOE
HOE_BONES = [
    B("root", None, [0, 0, 0], []),
    B("hoe", "root", [0, 0, 0], []),
    B("head", "hoe", [0, 10, 0], []),
    B("socket", "head", [0, 11, 0], [
        C([-1.5, 12.5, -1.5], [3, 1.5, 3], "charcoal"),
        C([-1.7, 9.5, -1.7], [3.4, 3, 3.4], "charcoal"),
        C([-1, 14, -1], [2, 0.8, 2], "iron"),
        C([-0.6, 14.8, -0.6], [1.2, 0.7, 1.2], "edge"),
    ]),
    B("head_flower", "head", [0, 10.8, 1.8], [
        C([-0.9, 10.0, 1.6], [1.8, 1.6, 0.4], "charcoal"),
        C([-0.8, 10.1, 1.9], [1.6, 1.4, 0.3], "petal", pat="flower6"),
        C([-0.35, 10.5, 2.1], [0.7, 0.7, 0.3], "core"),
    ]),
    B("beak_inner", "head", [0, 10, 1.5], [
        C([-1.5, 9.2, -1.0], [3, 2.2, 4], "iron", pat="crack"),
        C([-1.2, 10.6, -1.0], [2.4, 0.8, 4], "edge"),
        C([-1.7, 8.6, 2.8], [0.6, 1.2, 0.6], "edge"),
        C([1.1, 8.6, 2.8], [0.6, 1.2, 0.6], "edge"),
    ]),
    B("beak_mid", "head", [0, 9.2, 4.5], [
        C([-1.4, 8.2, 2.6], [2.8, 2.0, 3.4], "iron", pat="crack"),
        C([-1.1, 9.4, 2.6], [2.2, 0.8, 3.4], "edge"),
        # spikes reach down INTO the mid body (bottom y=10.2 meets top) — no gap
        C([-0.5, 10.2, 3.5], [0.5, 1.2, 0.5], "edge"),
        C([0.0, 10.2, 3.5], [0.5, 1.2, 0.5], "edge"),
    ]),
    B("beak_outer", "head", [0, 8.2, 7.0], [
        C([-1.2, 7.2, 5.8], [2.4, 1.7, 2.8], "iron"),
        C([-0.9, 8.1, 5.8], [1.8, 0.8, 2.8], "edge"),
        C([-1.0, 6.8, 8.2], [2.0, 1.2, 0.8], "edge"),
    ]),
    B("handle", "hoe", [0, 0, 0], [
        C([-1, 0, -1], [2, 9.5, 2], "root"),
        C([-1.3, 7, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 1, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([1.0, 4.0, -0.5], [0.5, 0.5, 0.5], "edge"),
        C([-0.8, 5.5, 1.0], [0.6, 0.6, 0.4], "fungus"),
    ]),
    B("pommel", "hoe", [0, -1.5, 0], [
        # body top overlaps handle shaft bottom (y=0) — no gap
        C([-1.6, -3.4, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-1.1, -2.9, 1.5], [2.2, 2.2, 0.3], "petal", pat="flower6"),
        C([-0.4, -2.2, 1.7], [0.8, 0.8, 0.3], "core"),
        C([-1, -4.2, -1], [2, 0.8, 2], "charcoal"),
    ]),
    B("fx_hoe", "hoe", [0, 10, 4], []),
    B("fx_pommel", "hoe", [0, -1.8, 1.8], []),
]

HOE_ANIMS = {
    "idle": (True, 3.0, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "hoe": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "till": (False, 0.45, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.06, [5, 0, 0]),
                                  (0.12, [-8, 0, 0]), (0.18, [-14, 0, 0]),
                                  (0.22, [-11, 0, 0]), (0.3, [-15, 0, 0]),
                                  (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]),
                                   (0.12, [0, 0, 1.5]), (0.45, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.2, 1.2, 1.2]),
                                       (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                  (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                  (0.32, [-27, 0, 0]), (0.4, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                       (0.32, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "bloom_cast": (False, 0.5, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                  (0.28, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (0.12, [1.08, 1.08, 1.08]),
                                  (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.3, 1.3, 1.3]),
                                       (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
    }),
    "gloom_pulse": (True, 2.6, {
        "head_flower": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                       (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

TOOLS = {
    "sword": (SWORD_BONES, SWORD_ANIMS),
    "pickaxe": (PICKAXE_BONES, PICKAXE_ANIMS),
    "axe": (AXE_BONES, AXE_ANIMS),
    "shovel": (SHOVEL_BONES, SHOVEL_ANIMS),
    "hoe": (HOE_BONES, HOE_ANIMS),
}


def check_anims(name, bones, anims):
    names = [b["name"] for b in bones]
    for aname, (loop, length, bb) in anims.items():
        for bn in bb:
            assert bn in names, "%s: unknown bone %s in %s" % (name, bn, aname)


def qa_sheet(name, bones):
    allx, ally = [], []
    projs = []
    for bi, b in enumerate(bones):
        for ci, c in enumerate(b["cubes"]):
            ox, oy, oz = c["o"]
            sx, sy, sz = c["s"]
            pts = [(ox + dx, oy + dy) for dx in (0, sx) for dy in (0, sy)]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            allx += xs
            ally += ys
            projs.append((oz + sz, min(xs), min(ys), max(xs), max(ys)))
    minx, maxx, miny, maxy = min(allx), max(allx), min(ally), max(ally)
    Z = 14
    sheet = Image.new("RGBA", ((int(maxx - minx) + 4) * Z + 40, (int(maxy - miny) + 4) * Z + 60),
                      (16, 14, 20, 255))
    d = ImageDraw.Draw(sheet)
    d.text((12, 8), "DARK FOREST %s front QA  x[%.1f,%.1f] y[%.1f,%.1f]"
           % (name.upper(), minx, maxx, miny, maxy), fill=(200, 170, 230))
    for z, x0, y0, x1, y1 in sorted(projs):
        d.rectangle([20 + (x0 - minx + 2) * Z, 40 + (maxy - y1 + 2) * Z,
                     20 + (x1 - minx + 2) * Z, 40 + (maxy - y0 + 2) * Z],
                    fill=(60, 55, 70, 255), outline=(139, 63, 217), width=1)
    path = os.path.join(ROOT, "docs", "assets", "concepts", "df-%s-qa-2026-09-03.png" % name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sheet.save(path)
    print("qa:", path)


def main():
    only = [a for a in os.sys.argv[1:] if not a.startswith("-")]
    for name, (bones, anims) in TOOLS.items():
        if only and name not in only:
            continue
        check_anims(name, bones, anims)
        rects = pack_uv(bones)
        geo = build_geo(name, bones, rects)
        tex = paint_texture(bones, rects)
        gp = os.path.join(ASSETS, "geo", "dark_forest", "tool_" + name + ".geo.json")
        ap = os.path.join(ASSETS, "animations", "dark_forest", "tool_" + name + ".animation.json")
        tp = os.path.join(ASSETS, "textures", "dark_forest", "item", name + ".png")
        for p in (gp, ap, tp):
            os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(gp, "w") as f:
            json.dump(geo, f, indent=1)
        with open(ap, "w") as f:
            json.dump({"format_version": "1.8.0", "animations": {
                an: {"loop": lo, "animation_length": ln, "bones": bb}
                for an, (lo, ln, bb) in anims.items()}}, f, indent=1)
        tex.save(tp)
        cubes = sum(len(b["cubes"]) for b in bones)
        print("%s: bones=%d cubes=%d anims=%s" % (name, len(bones), cubes, sorted(anims)))
        qa_sheet(name, bones)


if __name__ == "__main__":
    main()

