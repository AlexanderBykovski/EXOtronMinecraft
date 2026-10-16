#!/usr/bin/env python3
"""Opus weapon/tool set — single generator for 8 Opus + 2 settlement katanas.

Opus blue techno-forged style: dark steel / black forged metal, blue energy
core, blue emissive cuts, black wrapped grip. Golden Katana: royal gold
variant. Settlement katanas: plain steel, NO energy (no new ability).

Lessons: M1 (uv object+uv_size), M6 (static idle), M7 (JSON display), M8
(single source of truth). Tips are stepped axis-aligned boxes (no rotation
risk). EPS 0.01 volumetric overlap kills exact-coplanar z-fighting.

Outputs under src/main/resources/assets/opusvsexe/:
  geo/opus/<name>.geo.json          (katana_op, katana_gold, katana_refined,
                                      warhammer, pickaxe, axe, shovel, hoe)
  geo/settlement/<name>.geo.json    (katana, long_katana)
  animations/opus|settlement/<name>.animation.json
  textures/opus|settlement/item/<name>.png
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

# ---------------------------------------------------------------- palettes
PALETTES = {
    "opus": dict(
        body=(52, 56, 72), body_sh=(36, 39, 52), body_dk=(22, 23, 32),
        edge=(160, 170, 195), edge_hl=(214, 224, 244),
        energy_dk=(12, 42, 92), energy=(60, 180, 255),
        energy_hl=(150, 220, 255), energy_wh=(232, 248, 255),
        wrap=(24, 24, 30), wrap_dk=(10, 10, 14), wrap_hl=(52, 55, 68),
        soot=(8, 8, 12),
    ),
    "gold": dict(
        body=(196, 150, 70), body_sh=(150, 108, 44), body_dk=(96, 64, 24),
        edge=(255, 222, 140), edge_hl=(255, 244, 210),
        energy_dk=(150, 80, 10), energy=(255, 170, 40),
        energy_hl=(255, 214, 120), energy_wh=(255, 246, 220),
        wrap=(26, 22, 26), wrap_dk=(10, 8, 10), wrap_hl=(58, 48, 52),
        soot=(30, 20, 10),
    ),
    "steel": dict(
        body=(128, 132, 144), body_sh=(92, 95, 106), body_dk=(52, 54, 62),
        edge=(202, 206, 216), edge_hl=(238, 240, 246),
        energy_dk=(52, 54, 62), energy=(150, 154, 166),
        energy_hl=(202, 206, 216), energy_wh=(238, 240, 246),
        wrap=(64, 48, 36), wrap_dk=(32, 24, 18), wrap_hl=(96, 74, 54),
        soot=(20, 20, 24),
    ),
}

C = lambda o, s, m, **kw: dict(o=o, s=s, m=m, **kw)
FACES = ["north", "south", "east", "west", "up", "down"]
PAT_FACES = ("south", "north", "up", "down")


def B(name, parent, pivot, cubes):
    return dict(name=name, parent=parent, pivot=pivot, cubes=cubes)


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


def energy_channel(d, box, seed, P):
    import random
    rnd = random.Random(seed * 41 + 11)
    x, y, w, h = box
    cx = x + w // 2 + rnd.randrange(-1, 2)
    for yy in range(y + 1, y + h - 1):
        cx += rnd.randrange(-1, 2)
        cx = max(x + 1, min(x + w - 2, cx))
        d.point((cx - 1, yy), fill=P["energy_dk"])
        d.point((cx + 1, yy), fill=P["energy_dk"])
        d.point((cx, yy), fill=P["energy"])
        if (yy + seed) % 4 == 0:
            d.point((cx, yy), fill=P["energy_hl"])
        if (yy + seed) % 11 == 0:
            d.point((cx, yy), fill=P["energy_wh"])


def forged_pits(d, box, seed, P):
    import random
    rnd = random.Random(seed * 23 + 5)
    x, y, w, h = box
    for _ in range(max(2, w * h // 70)):
        px, py = x + rnd.randrange(w), y + rnd.randrange(h)
        d.point((px, py), fill=P["soot"] if rnd.random() < 0.6 else P["body_sh"])


def energy_core(d, box, P):
    x, y, w, h = box
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=P["body_dk"])
    d.line([cx, y + 1, cx, y + h - 2], fill=P["energy"])
    d.line([x + 1, cy, x + w - 2, cy], fill=P["energy"])
    r = max(1, min(w, h) // 4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=P["energy_hl"])
    d.point((cx, cy), fill=P["energy_wh"])


def wrap_bands(d, box, seed, P):
    import random
    rnd = random.Random(seed)
    x, y, w, h = box
    for i in range(0, w + h, 4):
        for k in range(2):
            xx = x + i + k - h
            if 0 <= xx - x < w:
                yy0 = y + max(0, h - i - k)
                yy1 = y + min(h - 1, h + w - i - k)
                if yy0 <= yy1:
                    d.line([xx, yy0, xx, yy1], fill=P["wrap_hl"] if k == 0 else P["wrap_dk"])
    for _ in range(max(1, w * h // 90)):
        d.point((x + rnd.randrange(w), y + rnd.randrange(h)), fill=P["wrap_dk"])


def paint_face(d, box, mat, face, seed, pat, P):
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    if mat == "body":
        shade(d, box, P["body"], P["body_sh"], P["body_dk"])
        forged_pits(d, box, seed, P)
        if face in PAT_FACES and pat == "channel":
            energy_channel(d, box, seed, P)
        if w >= 10 and h >= 6 and face in PAT_FACES and pat is None and seed % 4 == 0:
            d.line([x + 1, y + h // 2, x + w - 2, y + h // 2], fill=P["body_dk"])
    elif mat == "edge":
        shade(d, box, P["edge"], P["edge_hl"], P["body_dk"])
    elif mat == "energy":
        shade(d, box, P["energy"], P["energy_hl"], P["energy_dk"])
        if h >= 4:
            d.line([x + w // 2, y, x + w // 2, y + h - 1], fill=P["energy_wh"])
    elif mat == "core":
        if face in PAT_FACES:
            energy_core(d, box, P)
        else:
            shade(d, box, P["energy"], P["energy_hl"], P["energy_dk"])
    elif mat == "wrap":
        shade(d, box, P["wrap"], P["wrap_hl"], P["wrap_dk"])
        wrap_bands(d, box, seed, P)
    elif mat == "dark":
        shade(d, box, P["body_dk"], P["body"], P["soot"])
    else:
        shade(d, box, (255, 0, 255), (255, 0, 255), (255, 0, 255))


def chan(frames):
    return {(f"{t:.3f}".rstrip("0").rstrip(".")): {"vector": list(v)}
            for t, v in frames}


def build_geo(identifier, bones, rects):
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
            EPS = 0.01
            o, s = c["o"], c["s"]
            jc = {"origin": [o[0] - EPS, o[1] - EPS, o[2] - EPS],
                  "size": [s[0] + 2 * EPS, s[1] + 2 * EPS, s[2] + 2 * EPS],
                  "uv": uv}
            cubes.append(jc)
        if cubes:
            jb["cubes"] = cubes
        out.append(jb)
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": identifier,
                "texture_width": TEX_W,
                "texture_height": TEX_H,
                "visible_bounds_width": 3,
                "visible_bounds_height": 4,
                "visible_bounds_offset": [0, 0, 0],
            },
            "bones": out,
        }],
    }


def paint_texture(bones, rects, P):
    img = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    seed = 0
    for bi, b in enumerate(bones):
        for ci, c in enumerate(b["cubes"]):
            pat = c.get("pat")
            for f in FACES:
                paint_face(d, rects[(bi, ci, f)], c["m"], f, seed, pat, P)
                seed += 1
    return img


# ================================================================ KATANA
def katana_bones(blade_len, chan_pat, collar_extra=False):
    y0 = 4.0
    y1 = y0 + blade_len
    bones = [
        B("root", None, [0, 0, 0], []),
        B("katana", "root", [0, 0, 0], []),
        B("blade", "katana", [0, 12, 0], [
            C([-1.3, y0, -0.6], [2.6, blade_len, 1.2], "body", pat=chan_pat),
        ]),
        B("edge", "katana", [1.4, 12, 0], [
            C([1.3, y0, -0.65], [0.5, blade_len, 1.3], "edge"),
        ]),
        B("spine", "katana", [-1.5, 12, 0], [
            C([-1.8, y0, -0.65], [0.5, blade_len, 1.3], "dark"),
        ]),
        B("tip", "katana", [0, y1, 0], [
            # stepped pyramid: 3 narrowing steps + energy point
            C([-1.2, y1, -0.55], [2.4, 1.2, 1.1], "body"),
            C([1.2, y1, -0.6], [0.5, 1.2, 1.2], "edge"),
            C([-1.7, y1, -0.6], [0.5, 1.2, 1.2], "dark"),
            C([-0.8, y1 + 1.2, -0.5], [1.6, 1.0, 1.0], "body"),
            C([0.8, y1 + 1.2, -0.55], [0.4, 1.0, 1.1], "edge"),
            C([-1.2, y1 + 1.2, -0.55], [0.4, 1.0, 1.1], "dark"),
            C([-0.4, y1 + 2.2, -0.45], [0.8, 0.9, 0.9], "body"),
            C([-0.15, y1 + 3.1, -0.4], [0.3, 0.5, 0.8], "energy"),
        ]),
        B("guard", "katana", [0, 2.5, 0], [
            C([-3.2, 1.7, -0.9], [6.4, 1.6, 1.8], "dark"),
            C([-3.6, 1.5, -1.0], [1.0, 2.0, 2.0], "body"),
            C([2.6, 1.5, -1.0], [1.0, 2.0, 2.0], "body"),
            C([-0.9, 1.9, 0.9], [1.8, 1.2, 0.4], "core"),
            # neck: bridges guard top (3.3) into blade bottom (y0) — no gap
            C([-1.2, 2.8, -0.8], [2.4, 1.6, 1.6], "body"),
            C([-0.5, 2.8, 0.8], [1.0, 1.6, 0.3], "energy"),
        ]),
        B("handle", "katana", [0, -2.5, 0], [
            # shaft runs up INTO the guard (top y=2.0 overlaps guard bottom 1.5)
            C([-1, -6, -1], [2, 8, 2], "wrap"),
            C([-1.3, 0, -1.3], [2.6, 1, 2.6], "dark"),
            C([-1.3, -3.5, -1.3], [2.6, 1, 2.6], "dark"),
        ]),
        B("pommel", "katana", [0, -7.5, 0], [
            C([-1.5, -9, -1.5], [3, 3, 3], "dark"),
            C([-0.6, -8.2, 1.4], [1.2, 1.2, 0.3], "core"),
            C([-1, -10.3, -1], [2, 1.3, 2], "dark"),
        ]),
        B("fx_katana", "katana", [0, 14, 1.0], []),
        B("fx_pommel", "katana", [0, -7.5, 1.8], []),
    ]
    if collar_extra:
        # refined ring-emitter collar above guard (connected, not floating)
        bones.insert(7, B("collar", "katana", [0, 3.5, 0], [
            C([-2.2, 3.3, -1.1], [4.4, 1.2, 2.2], "body"),
            C([-1.2, 3.5, 1.0], [2.4, 0.8, 0.4], "energy"),
        ]))
    return bones


KATANA_ANIMS = {
    "idle": (True, 3.0, {
        "katana": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "katana": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "guard": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "katana": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-28, 0, 0]), (0.2, [-22, 0, 0]),
                                     (0.28, [-30, 0, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "guard": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.2, 1.2, 1.2]),
                                (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "attack_alt": (False, 0.4, {
        "katana": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-24, -6, 0]), (0.2, [-19, -4, 0]),
                                     (0.28, [-26, -7, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, -2.5]), (0.4, [0, 0, 0])])},
        "guard": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.2, 1.2, 1.2]),
                                (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "special_cast": (False, 0.55, {
        "katana": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-16, 0, 0]),
                                    (0.28, [22, 0, 0]), (0.4, [16, 0, 0]),
                                    (0.55, [0, 0, 0])])},
        "guard": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.35, 1.35, 1.35]),
                                (0.45, [1, 1, 1]), (0.55, [1, 1, 1])])},
        "tip": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.25, 1.25, 1.25]),
                               (0.55, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "guard": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "tip": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                               (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# Steel katanas: same anims minus energy pulse scale on guard? Keep same
# skeleton; pulse only breathes pommel (no glow). Reuse table as-is.

# ============================================================== WARHAMMER
WARHAMMER_BONES = [
    B("root", None, [0, 0, 0], []),
    B("hammer", "root", [0, 0, 0], []),
    B("head", "hammer", [0, 12, 0], [
        C([-5, 10, -1.5], [10, 4.5, 3], "body"),
        C([-5.5, 9.5, -1.2], [11, 1.2, 2.4], "dark"),
        C([-5.5, 13.3, -1.2], [11, 1.2, 2.4], "dark"),
    ]),
    B("cap_l", "head", [-5, 12, 0], [
        C([-8, 9.5, -1.3], [3, 5, 2.6], "body"),
        C([-8.6, 10.5, -1.0], [0.8, 3, 2.0], "edge"),
        C([-7.2, 11.0, 1.3], [1.6, 2.0, 0.4], "core"),
    ]),
    B("cap_r", "head", [5, 12, 0], [
        C([5, 9.5, -1.3], [3, 5, 2.6], "body"),
        C([7.8, 10.5, -1.0], [0.8, 3, 2.0], "edge"),
        C([5.6, 11.0, 1.3], [1.6, 2.0, 0.4], "core"),
    ]),
    B("core", "head", [0, 12.2, 1.5], [
        C([-1.4, 10.9, 1.3], [2.8, 2.6, 0.5], "dark"),
        C([-0.9, 11.4, 1.5], [1.8, 1.6, 0.4], "core"),
    ]),
    B("crown", "head", [0, 14.5, 0], [
        C([-1.5, 14.5, -1.0], [3, 1.5, 2.0], "body"),
        C([-0.5, 16.0, -0.7], [1.0, 1.2, 1.4], "energy"),
    ]),
    B("handle", "hammer", [0, 0, 0], [
        C([-1, -4, -1], [2, 14, 2], "wrap"),
        C([-1.4, 8, -1.4], [2.8, 1.2, 2.8], "dark"),
        C([-1.4, 0, -1.4], [2.8, 1.2, 2.8], "dark"),
    ]),
    B("pommel", "hammer", [0, -5.5, 0], [
        C([-1.7, -7.4, -1.7], [3.4, 3.4, 3.4], "dark"),
        C([-0.7, -6.8, 1.6], [1.4, 1.4, 0.3], "core"),
        C([-1, -8.2, -1], [2, 0.8, 2], "dark"),
    ]),
    B("fx_hammer", "hammer", [0, 12, 1.5], []),
    B("fx_pommel", "hammer", [0, -5.7, 1.8], []),
]

WARHAMMER_ANIMS = {
    "idle": (True, 3.0, {
        "hammer": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "hammer": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "core": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.5, {
        "hammer": {"rotation": chan([(0, [0, 0, 0]), (0.1, [16, 0, 0]),
                                    (0.2, [-30, 0, 0]), (0.28, [-24, 0, 0]),
                                    (0.38, [-32, 0, 0]), (0.5, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.1, [0, 0, -3]),
                                   (0.2, [0, 0, 2]), (0.5, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.24, [1.25, 1.25, 1.25]),
                               (0.38, [1, 1, 1]), (0.5, [1, 1, 1])])},
    }),
    "slam_cast": (False, 0.65, {
        "hammer": {"rotation": chan([(0, [0, 0, 0]), (0.15, [24, 0, 0]),
                                    (0.3, [-34, 0, 0]), (0.42, [-26, 0, 0]),
                                    (0.65, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.28, [1.4, 1.4, 1.4]),
                               (0.5, [1, 1, 1]), (0.65, [1, 1, 1])])},
        "crown": {"scale": chan([(0, [1, 1, 1]), (0.32, [1.2, 1.2, 1.2]),
                                (0.65, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "core": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                               (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                 (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ============================================================== PICKAXE
PICKAXE_BONES = [
    B("root", None, [0, 0, 0], []),
    B("pickaxe", "root", [0, 0, 0], []),
    B("head", "pickaxe", [0, 11, 0], []),
    B("socket", "head", [0, 11.5, 0], [
        C([-2, 9, -1.5], [4, 5, 3], "dark"),
        C([-1.5, 14, -1.2], [3, 1, 2.4], "body"),
        C([-2.2, 9.5, 1.5], [4.4, 0.6, 0.35], "edge"),
        C([-2.2, 12.9, 1.5], [4.4, 0.6, 0.35], "edge"),
    ]),
    B("core", "head", [0, 11.5, 1.4], [
        C([-1.1, 10.2, 1.2], [2.2, 2.6, 0.5], "dark"),
        C([-0.7, 10.6, 1.5], [1.4, 1.8, 0.4], "core"),
    ]),
    B("beak_l", "head", [-2, 11.5, 0], [
        C([-6, 10.5, -0.9], [4, 2.5, 1.8], "body"),
        C([-8.5, 9.3, -0.8], [3, 2.2, 1.6], "body"),
        C([-10.5, 7.8, -0.7], [2.5, 2, 1.4], "body"),
        C([-11.4, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([-8.5, 9.0, -0.75], [6, 0.5, 1.5], "energy"),
        C([-4, 12.6, -0.8], [2, 0.7, 1.6], "energy"),
    ]),
    B("beak_r", "head", [2, 11.5, 0], [
        C([2, 10.5, -0.9], [4, 2.5, 1.8], "body"),
        C([5.5, 9.3, -0.8], [3, 2.2, 1.6], "body"),
        C([8, 7.8, -0.7], [2.5, 2, 1.4], "body"),
        C([10.2, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([2.5, 9.0, -0.75], [6, 0.5, 1.5], "energy"),
        C([2, 12.6, -0.8], [2, 0.7, 1.6], "energy"),
    ]),
    B("handle", "pickaxe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "wrap"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "dark"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "dark"),
    ]),
    B("pommel", "pickaxe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "dark"),
        C([-0.6, -3.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -5.4, -1], [2, 0.8, 2], "dark"),
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
        "core": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
    }),
    "mine": (False, 0.35, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.07, [8, 0, 0]),
                                      (0.14, [-18, 0, 0]), (0.2, [-14, 0, 0]),
                                      (0.26, [-20, 0, 0]), (0.35, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.07, [0, 0, -2]),
                                   (0.14, [0, 0, 1.5]), (0.35, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.25, 1.25, 1.25]),
                                (0.28, [1, 1, 1]), (0.35, [1, 1, 1])])},
    }),
    "attack": (False, 0.45, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                      (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                      (0.32, [-27, 0, 0]), (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.45, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "resonance_cast": (False, 0.5, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.15, [-16, 0, 0]),
                                      (0.3, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.35, 1.35, 1.35]),
                                (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "beak_l": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
        "beak_r": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "core": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ================================================================== AXE
AXE_BONES = [
    B("root", None, [0, 0, 0], []),
    B("axe", "root", [0, 0, 0], []),
    B("head", "axe", [0, 10, 0], []),
    B("blade_main", "head", [4, 12, 0], [
        C([2, 10, -0.9], [5, 4, 1.8], "body"),
        C([6.5, 11, -0.8], [3.5, 5, 1.6], "body"),
        C([9.5, 8, -0.7], [2.5, 4, 1.4], "body"),
        C([9.5, 16, -0.75], [2.6, 1.8, 1.5], "body"),
        C([9.8, 17.8, -0.7], [1.8, 1.6, 1.4], "body"),
        C([10.1, 19.4, -0.65], [1.2, 1.2, 1.3], "edge"),
        C([9.5, 6.2, -0.7], [2.6, 1.8, 1.5], "body"),
        C([9.8, 4.6, -0.65], [1.8, 1.6, 1.4], "body"),
        C([10.1, 3.4, -0.6], [1.2, 1.2, 1.3], "edge"),
        C([6.5, 15.2, -0.75], [4, 0.8, 1.5], "energy"),
        C([11.5, 8, -0.65], [0.7, 8, 1.3], "energy"),
        C([2, 9.5, -0.85], [5, 0.6, 1.7], "edge"),
    ]),
    B("blade_back", "head", [-3, 11, 0], [
        C([-5, 10.5, -0.7], [3, 3, 1.4], "body"),
        C([-6.5, 9.5, -0.6], [1.5, 2.5, 1.2], "body"),
        C([-6.8, 9.3, -0.65], [0.6, 3, 1.3], "edge"),
    ]),
    B("socket", "head", [0, 11.5, 0], [
        C([-2, 9, -1.3], [4, 5, 2.6], "dark"),
        C([-1.1, 10.2, 1.3], [2.2, 2.6, 0.5], "dark"),
        C([-0.7, 10.6, 1.5], [1.4, 1.8, 0.4], "core"),
    ]),
    B("handle", "axe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "wrap"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "dark"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "dark"),
    ]),
    B("pommel", "axe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "dark"),
        C([-0.6, -3.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -5.4, -1], [2, 0.8, 2], "dark"),
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
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.45, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                  (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                  (0.32, [-27, 0, 0]), (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.45, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                  (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "crosscut_cast": (False, 0.55, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [14, 0, 0]),
                                  (0.25, [-28, 0, 0]), (0.4, [-20, 0, 0]),
                                  (0.55, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.35, 1.35, 1.35]),
                                  (0.45, [1, 1, 1]), (0.55, [1, 1, 1])])},
        "blade_main": {"scale": chan([(0, [1, 1, 1]), (0.28, [1.05, 1.05, 1.05]),
                                      (0.5, [1, 1, 1]), (0.55, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                  (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ============================================================== SHOVEL
SHOVEL_BONES = [
    B("root", None, [0, 0, 0], []),
    B("shovel", "root", [0, 0, 0], []),
    B("head", "shovel", [0, 12, 0], []),
    B("frame", "head", [0, 13, 0], [
        C([-3.5, 16.5, -0.9], [7, 2, 1.8], "body"),
        C([-4.2, 9, -0.9], [1.4, 8, 1.6], "body"),
        C([2.8, 9, -0.9], [1.4, 8, 1.6], "body"),
        C([-3.5, 7, -0.9], [7, 2, 1.8], "body"),
        C([-4.1, 16.2, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([3.3, 16.2, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([-4.1, 6.7, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([3.3, 6.7, -0.8], [0.8, 0.8, 1.6], "edge"),
    ]),
    B("panel", "head", [0, 12.7, 0], [
        C([-2.8, 9, -0.7], [5.6, 7.5, 1.2], "body", pat="channel"),
    ]),
    B("core", "head", [0, 12.5, 0.6], [
        C([-0.5, 9.5, 0.5], [1, 6, 0.3], "energy"),
    ]),
    B("socket", "head", [0, 5.7, 0], [
        C([-2, 4.5, -1.2], [4, 2.5, 2.4], "dark"),
        C([-2.6, 5.5, -1.0], [1.0, 1.2, 2.0], "body"),
        C([1.6, 5.5, -1.0], [1.0, 1.2, 2.0], "body"),
        C([-0.9, 5.0, 1.1], [1.8, 1.5, 0.4], "core"),
    ]),
    B("handle", "shovel", [0, 0, 0], [
        C([-1, -4, -1], [2, 8.5, 2], "wrap"),
        C([-1.3, 3.5, -1.3], [2.6, 1, 2.6], "dark"),
        C([-1.3, -1.5, -1.3], [2.6, 1, 2.6], "dark"),
    ]),
    B("pommel", "shovel", [0, -5.9, 0], [
        # body top overlaps handle shaft bottom (y=-4) — no gap
        C([-1.6, -7.4, -1.6], [3.2, 3.6, 3.2], "dark"),
        C([-0.6, -6.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -8.2, -1], [2, 0.8, 2], "dark"),
    ]),
    B("fx_shovel", "shovel", [0, 12, 1.0], []),
    B("fx_pommel", "shovel", [0, -5.9, 1.8], []),
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
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "dig": (False, 0.45, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.06, [6, 0, 0]),
                                     (0.12, [-10, 0, 0]), (0.18, [-16, 0, 0]),
                                     (0.22, [-13, 0, 0]), (0.3, [-18, 0, 0]),
                                     (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]),
                                   (0.12, [0, 0, 1.5]), (0.45, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.2, 1.2, 1.2]),
                                  (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                     (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                     (0.32, [-27, 0, 0]), (0.4, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                  (0.32, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "trench_cast": (False, 0.5, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                     (0.25, [-20, 0, 0]), (0.5, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.3, 1.3, 1.3]),
                                  (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "frame": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.04, 1.04, 1.04]),
                                 (0.5, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
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
        C([-1.7, 9, -1.7], [3.4, 3.5, 3.4], "dark"),
        C([-1, 12.5, -1], [2, 1, 2], "body"),
        C([-0.8, 10, 1.6], [1.6, 1.6, 0.4], "core"),
        C([-2.1, 9.5, -1.2], [0.8, 1.0, 2.4], "body"),
        C([1.3, 9.5, -1.2], [0.8, 1.0, 2.4], "body"),
    ]),
    B("beak1", "head", [0, 10, 1.5], [
        C([-1.5, 9, 0], [3, 2.2, 3.5], "body"),
        C([-1.2, 10.4, 0], [2.4, 0.8, 3.5], "edge"),
    ]),
    B("beak2", "head", [2, 9.2, 4.5], [
        C([1.0, 8.2, 3.2], [2.8, 2.0, 3.2], "body"),
        C([1.3, 9.4, 3.2], [2.2, 0.8, 3.2], "edge"),
    ]),
    B("beak3", "head", [4.5, 8.0, 7.0], [
        C([3.5, 7.2, 6.0], [2.6, 1.8, 3.0], "body"),
        C([5.7, 6.6, 8.2], [1.0, 1.6, 1.2], "energy"),
    ]),
    B("handle", "hoe", [0, 0, 0], [
        C([-1, 0, -1], [2, 9, 2], "wrap"),
        C([-1.3, 7, -1.3], [2.6, 1, 2.6], "dark"),
        C([-1.3, 1, -1.3], [2.6, 1, 2.6], "dark"),
    ]),
    B("pommel", "hoe", [0, -1.5, 0], [
        # body top overlaps handle shaft bottom (y=0) — no gap
        C([-1.6, -3.4, -1.6], [3.2, 3.8, 3.2], "dark"),
        C([-0.6, -2.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -4.2, -1], [2, 0.8, 2], "dark"),
    ]),
    B("fx_hoe", "hoe", [4, 8, 6], []),
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
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.1, 1.1, 1.1]), (0.4, [1, 1, 1])])},
    }),
    "till": (False, 0.45, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.06, [5, 0, 0]),
                                  (0.12, [-8, 0, 0]), (0.18, [-14, 0, 0]),
                                  (0.22, [-11, 0, 0]), (0.3, [-15, 0, 0]),
                                  (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]),
                                   (0.12, [0, 0, 1.5]), (0.45, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.2, 1.2, 1.2]),
                                  (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                  (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                  (0.32, [-27, 0, 0]), (0.4, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                  (0.32, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "lattice_cast": (False, 0.5, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                  (0.28, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (0.12, [1.08, 1.08, 1.08]),
                                  (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.3, 1.3, 1.3]),
                                  (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
    }),
    "energy_pulse": (True, 2.6, {
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
                                  (1.3, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (1.3, [1.02, 1.02, 1.02]),
                                  (1.95, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}

# ================================================================ registry
# (out_name, subdir, geo_id, palette, bones_fn/bones, anims)
ITEMS = [
    ("katana_op", "opus", "geometry.opus_katana_op", "opus",
     katana_bones(16, "channel"), KATANA_ANIMS),
    ("katana_gold", "opus", "geometry.opus_katana_gold", "gold",
     katana_bones(17, "channel"), KATANA_ANIMS),
    ("katana_refined", "opus", "geometry.opus_katana_refined", "opus",
     katana_bones(15, "channel", collar_extra=True), KATANA_ANIMS),
    ("warhammer", "opus", "geometry.opus_warhammer", "opus",
     WARHAMMER_BONES, WARHAMMER_ANIMS),
    ("pickaxe", "opus", "geometry.opus_pickaxe", "opus",
     PICKAXE_BONES, PICKAXE_ANIMS),
    ("axe", "opus", "geometry.opus_axe", "opus",
     AXE_BONES, AXE_ANIMS),
    ("shovel", "opus", "geometry.opus_shovel", "opus",
     SHOVEL_BONES, SHOVEL_ANIMS),
    ("hoe", "opus", "geometry.opus_hoe", "opus",
     HOE_BONES, HOE_ANIMS),
    ("katana", "settlement", "geometry.settlement_katana", "steel",
     katana_bones(13, None), KATANA_ANIMS),
    ("long_katana", "settlement", "geometry.settlement_long_katana", "steel",
     katana_bones(20, None), KATANA_ANIMS),
]


def check_anims(name, bones, anims):
    names = [b["name"] for b in bones]
    for aname, (loop, length, bb) in anims.items():
        for bn in bb:
            assert bn in names, "%s: unknown bone %s in %s" % (name, bn, aname)


def audit_gaps(name, bones):
    """Touching-face audit: faces that meet exactly are EPS-covered by
    build_geo; report exact coplanar contacts for the log."""
    boxes = []
    for b in bones:
        for c in b["cubes"]:
            ox, oy, oz = c["o"]
            sx, sy, sz = c["s"]
            boxes.append((b["name"], (ox, oy, oz, ox + sx, oy + sy, oz + sz)))
    contacts = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            _, a = boxes[i]
            _, b = boxes[j]
            # overlap-or-touch on all axes with exact face match on one axis
            touch = (
                (abs(a[3] - b[0]) < 1e-9 or abs(b[3] - a[0]) < 1e-9)
                or (abs(a[4] - b[1]) < 1e-9 or abs(b[4] - a[1]) < 1e-9)
                or (abs(a[5] - b[2]) < 1e-9 or abs(b[5] - a[2]) < 1e-9)
            )
            overlap = (a[0] <= b[3] and b[0] <= a[3] and a[1] <= b[4]
                       and b[1] <= a[4] and a[2] <= b[5] and b[2] <= a[5])
            if touch and overlap:
                contacts += 1
    print("%s: gap-audit touching contacts=%d (all EPS-covered)" % (name, contacts))


def main():
    only = [a for a in os.sys.argv[1:] if not a.startswith("-")]
    for name, subdir, geo_id, pal, bones, anims in ITEMS:
        if only and name not in only:
            continue
        P = PALETTES[pal]
        check_anims(name, bones, anims)
        rects = pack_uv(bones)
        geo = build_geo(geo_id, bones, rects)
        tex = paint_texture(bones, rects, P)
        gp = os.path.join(ASSETS, "geo", subdir, name + ".geo.json")
        ap = os.path.join(ASSETS, "animations", subdir, name + ".animation.json")
        tp = os.path.join(ASSETS, "textures", subdir, "item", name + ".png")
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
        print("%s [%s/%s]: bones=%d cubes=%d anims=%s" % (
            name, subdir, pal, len(bones), cubes, sorted(anims)))
        audit_gaps(name, bones)


if __name__ == "__main__":
    main()
