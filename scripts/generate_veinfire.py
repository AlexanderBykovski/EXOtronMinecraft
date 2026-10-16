#!/usr/bin/env python3
"""Vein Fire toolset — single generator for all 5 tools.

Shared framework + infernal palette/painters; per-tool BONES/ANIMS tables.
Lessons: M1 (uv object+uv_size), M6 (static idle), M7, M8. Tips/horns are
stepped axis-aligned boxes (no rotation-convention risk).
Outputs under src/main/resources/assets/opusvsexe/:
  geo/fire/tool_<name>.geo.json
  animations/fire/tool_<name>.animation.json
  textures/fire/item/<name>.png
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
BASALT = (40, 37, 44)
BASALT_DK = (22, 20, 26)
BASALT_SH = (30, 28, 36)
EDGE = (110, 110, 122)
EDGE_HL = (158, 158, 170)
MAGMA_DK = (90, 20, 10)
MAGMA = (255, 110, 20)
MAGMA_HL = (255, 200, 80)
MAGMA_WH = (255, 240, 200)
WRAP = (48, 34, 26)
WRAP_DK = (26, 18, 14)
WRAP_HL = (72, 50, 36)
SOOT = (12, 10, 12)

C = lambda o, s, m, **kw: dict(o=o, s=s, m=m, **kw)
FACES = ["north", "south", "east", "west", "up", "down"]
PAT_FACES = ("south", "north", "up", "down")


def mirror(cubes):
    out = []
    for c in cubes:
        o = [-c["o"][0] - c["s"][0], c["o"][1], c["o"][2]]
        kw = {}
        if "pat" in c:
            kw["pat"] = c["pat"]
        out.append(C(o, list(c["s"]), c["m"], **kw))
    return out


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


def magma_fissure(d, box, seed):
    """Stress crack: dark red halo -> orange core -> yellow-white peaks."""
    import random
    rnd = random.Random(seed * 41 + 11)
    x, y, w, h = box
    cx = x + w // 2 + rnd.randrange(-1, 2)
    for yy in range(y + 1, y + h - 1):
        cx += rnd.randrange(-1, 2)
        cx = max(x + 1, min(x + w - 2, cx))
        d.point((cx - 1, yy), fill=MAGMA_DK)
        d.point((cx + 1, yy), fill=MAGMA_DK)
        d.point((cx, yy), fill=MAGMA)
        if (yy + seed) % 4 == 0:
            d.point((cx, yy), fill=MAGMA_HL)
        if (yy + seed) % 11 == 0:
            d.point((cx, yy), fill=MAGMA_WH)


def forged_pits(d, box, seed):
    import random
    rnd = random.Random(seed * 23 + 5)
    x, y, w, h = box
    for _ in range(max(2, w * h // 70)):
        px, py = x + rnd.randrange(w), y + rnd.randrange(h)
        d.point((px, py), fill=SOOT if rnd.random() < 0.6 else BASALT_SH)


def infernal_core(d, box):
    """Diamond socket face: dark frame, hot cross, white-hot heart."""
    x, y, w, h = box
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=BASALT_DK)
    d.line([cx, y + 1, cx, y + h - 2], fill=MAGMA)
    d.line([x + 1, cy, x + w - 2, cy], fill=MAGMA)
    r = max(1, min(w, h) // 4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGMA_HL)
    d.point((cx, cy), fill=MAGMA_WH)


def wrap_bands(d, box, seed):
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
                    d.line([xx, yy0, xx, yy1], fill=WRAP_HL if k == 0 else WRAP_DK)
    for _ in range(max(1, w * h // 90)):
        d.point((x + rnd.randrange(w), y + rnd.randrange(h)), fill=WRAP_DK)


def paint_face(d, box, mat, face, seed, pat):
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    if mat == "basalt":
        shade(d, box, BASALT, BASALT_SH, BASALT_DK)
        forged_pits(d, box, seed)
        if face in PAT_FACES and pat == "fissure":
            magma_fissure(d, box, seed)
        if w >= 10 and h >= 6 and face in PAT_FACES and pat is None and seed % 4 == 0:
            d.line([x + 1, y + h // 2, x + w - 2, y + h // 2], fill=BASALT_DK)
    elif mat == "edge":
        shade(d, box, EDGE, EDGE_HL, BASALT_DK)
    elif mat == "magma":
        shade(d, box, MAGMA, MAGMA_HL, MAGMA_DK)
        if h >= 4:
            d.line([x + w // 2, y, x + w // 2, y + h - 1], fill=MAGMA_WH)
    elif mat == "core":
        if face in PAT_FACES:
            infernal_core(d, box)
        else:
            shade(d, box, MAGMA, MAGMA_HL, MAGMA_DK)
    elif mat == "wrap":
        shade(d, box, WRAP, WRAP_HL, WRAP_DK)
        wrap_bands(d, box, seed)
    elif mat == "charcoal":
        shade(d, box, BASALT_DK, BASALT, SOOT)
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
            # EPS overlap kills exact-coplanar z-fighting (audit-proven).
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
                "identifier": "geometry.vf_" + name,
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

# ================================================================ SWORD
SWORD_BONES = [
    B("root", None, [0, 0, 0], []),
    B("sword", "root", [0, 0, 0], []),
    B("blade", "sword", [0, 12, 0], [
        C([-2, 5, -0.7], [4, 15, 1.4], "basalt"),
        C([-0.35, 5, 0.7], [0.7, 15, 0.3], "basalt", pat="fissure"),
    ]),
    B("edge_l", "sword", [-2.1, 12, 0], [
        C([-2.4, 5, -0.75], [0.5, 15, 1.5], "edge"),
    ]),
    B("edge_r", "sword", [2.1, 12, 0], [
        C([1.9, 5, -0.75], [0.5, 15, 1.5], "edge"),
    ]),
    B("tip", "sword", [0, 22, 0], [
        C([-1.9, 20, -0.7], [2.0, 1.5, 1.4], "basalt"),
        C([-0.1, 20, -0.7], [2.0, 1.5, 1.4], "basalt"),
        C([-2.3, 20, -0.75], [0.5, 1.5, 1.5], "edge"),
        C([1.8, 20, -0.75], [0.5, 1.5, 1.5], "edge"),
        C([-1.3, 21.5, -0.65], [1.4, 1.0, 1.3], "basalt"),
        C([-0.1, 21.5, -0.65], [1.4, 1.0, 1.3], "basalt"),
        C([-1.7, 21.5, -0.7], [0.5, 1.0, 1.4], "edge"),
        C([1.2, 21.5, -0.7], [0.5, 1.0, 1.4], "edge"),
        C([-0.85, 22.5, -0.6], [0.95, 1.0, 1.2], "basalt"),
        C([-0.1, 22.5, -0.6], [0.95, 1.0, 1.2], "basalt"),
        C([-1.15, 22.5, -0.65], [0.4, 1.0, 1.3], "edge"),
        C([0.75, 22.5, -0.65], [0.4, 1.0, 1.3], "edge"),
        C([-0.45, 23.5, -0.55], [0.9, 0.8, 1.1], "basalt"),
        C([-0.2, 23.9, -0.5], [0.4, 0.4, 1.0], "magma"),
    ]),
    B("guard", "sword", [0, 2.5, 0], [
        C([-4.5, 1.5, -1], [9, 2, 2], "basalt"),
        C([-5, 1.2, -1.1], [1.2, 2.6, 2.2], "charcoal"),
        C([3.8, 1.2, -1.1], [1.2, 2.6, 2.2], "charcoal"),
        # neck: bridges guard top (3.8) into blade bottom (5.0) — no gap
        C([-1.2, 3.0, -0.8], [2.4, 2.4, 1.6], "basalt"),
        C([-0.4, 3.0, 0.8], [0.8, 2.4, 0.3], "magma"),
    ]),
    B("core", "sword", [0, 2.4, 1.2], [
        C([-1.4, 1.0, 1.0], [2.8, 2.8, 0.6], "charcoal"),
        C([-0.9, 1.5, 1.3], [1.8, 1.8, 0.5], "core"),
    ]),
    B("handle", "sword", [0, -2.5, 0], [
        # shaft runs up INTO the guard (top y=1.6 overlaps guard bottom 1.2)
        C([-1, -6, -1], [2, 7.6, 2], "wrap"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, -3.5, -1.3], [2.6, 1, 2.6], "charcoal"),
    ]),
    B("pommel", "sword", [0, -7.5, 0], [
        C([-1.5, -9, -1.5], [3, 3, 3], "charcoal"),
        C([-0.5, -8, 1.4], [1, 1, 0.3], "magma"),
        C([-0.5, -8, -1.7], [1, 1, 0.3], "magma"),
        C([-1.7, -8, -0.5], [0.3, 1, 1], "magma"),
        C([1.4, -8, -0.5], [0.3, 1, 1], "magma"),
        C([-1, -10.3, -1], [2, 1.3, 2], "charcoal"),
    ]),
    B("fx_sword", "sword", [0, 14, 1.0], []),
    B("fx_pommel", "sword", [0, -7.5, 1.8], []),
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
        "core": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-28, 0, 0]), (0.2, [-22, 0, 0]),
                                     (0.28, [-30, 0, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.25, 1.25, 1.25]),
                                (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "attack_alt": (False, 0.4, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (0.06, [8, 0, 0]), (0.1, [4, 0, 0]),
                                     (0.14, [-24, -6, 0]), (0.2, [-19, -4, 0]),
                                     (0.28, [-26, -7, 0]), (0.4, [0, 0, 0])])},
        "blade": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]), (0.1, [0, 0, -1]),
                                    (0.14, [0, 0, -2.5]), (0.4, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.25, 1.25, 1.25]),
                                (0.3, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "brand_cast": (False, 0.5, {
        "sword": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-16, 0, 0]),
                                    (0.28, [22, 0, 0]), (0.4, [16, 0, 0]),
                                    (0.5, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.4, 1.4, 1.4]),
                                (0.4, [1.45, 1.45, 1.45]), (0.5, [1, 1, 1])])},
        "tip": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.25, 1.25, 1.25]),
                               (0.5, [1, 1, 1])])},
    }),
    "ember_pulse": (True, 2.6, {
        "core": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
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
    B("furnace", "head", [0, 11.5, 0], [
        C([-2, 9, -1.5], [4, 5, 3], "charcoal"),
        C([-1.5, 14, -1.2], [3, 1, 2.4], "basalt"),
        C([-2.2, 9.5, 1.5], [4.4, 0.6, 0.35], "edge"),
        C([-2.2, 12.9, 1.5], [4.4, 0.6, 0.35], "edge"),
    ]),
    B("core", "head", [0, 11.5, 1.4], [
        C([-1.1, 10.2, 1.2], [2.2, 2.6, 0.5], "charcoal"),
        C([-0.7, 10.6, 1.5], [1.4, 1.8, 0.4], "core"),
    ]),
    B("beak_l", "head", [-2, 11.5, 0], [
        C([-6, 10.5, -0.9], [4, 2.5, 1.8], "basalt"),
        C([-8.5, 9.3, -0.8], [3, 2.2, 1.6], "basalt"),
        C([-10.5, 7.8, -0.7], [2.5, 2, 1.4], "basalt"),
        C([-11.4, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([-8.5, 9.0, -0.75], [6, 0.5, 1.5], "magma"),
        C([-4, 12.6, -0.8], [2, 0.7, 1.6], "magma"),
    ]),
    B("beak_r", "head", [2, 11.5, 0], [
        C([2, 10.5, -0.9], [4, 2.5, 1.8], "basalt"),
        C([5.5, 9.3, -0.8], [3, 2.2, 1.6], "basalt"),
        C([8, 7.8, -0.7], [2.5, 2, 1.4], "basalt"),
        C([10.2, 6.5, -0.6], [1.2, 1.6, 1.2], "edge"),
        C([2.5, 9.0, -0.75], [6, 0.5, 1.5], "magma"),
        C([2, 12.6, -0.8], [2, 0.7, 1.6], "magma"),
    ]),
    B("handle", "pickaxe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "wrap"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "charcoal"),
    ]),
    B("pommel", "pickaxe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-0.6, -3.9, 1.5], [1.2, 1.2, 0.3], "core"),
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
    "extract_cast": (False, 0.5, {
        "pickaxe": {"rotation": chan([(0, [0, 0, 0]), (0.15, [-16, 0, 0]),
                                      (0.3, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "core": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.35, 1.35, 1.35]),
                                (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "beak_l": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
        "beak_r": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.06, 1.06, 1.06]),
                                  (0.5, [1, 1, 1])])},
    }),
    "ember_pulse": (True, 2.6, {
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
        C([2, 10, -0.9], [5, 4, 1.8], "basalt"),
        C([6.5, 11, -0.8], [3.5, 5, 1.6], "basalt"),
        C([9.5, 8, -0.7], [2.5, 4, 1.4], "basalt"),
        C([9.5, 16, -0.75], [2.6, 1.8, 1.5], "basalt"),
        C([9.8, 17.8, -0.7], [1.8, 1.6, 1.4], "basalt"),
        C([10.1, 19.4, -0.65], [1.2, 1.2, 1.3], "edge"),
        C([9.5, 6.2, -0.7], [2.6, 1.8, 1.5], "basalt"),
        C([9.8, 4.6, -0.65], [1.8, 1.6, 1.4], "basalt"),
        C([10.1, 3.4, -0.6], [1.2, 1.2, 1.3], "edge"),
        C([6.5, 15.2, -0.75], [4, 0.8, 1.5], "magma"),
        C([11.5, 8, -0.65], [0.7, 8, 1.3], "magma"),
        C([2, 9.5, -0.85], [5, 0.6, 1.7], "edge"),
    ]),
    B("blade_back", "head", [-3, 11, 0], [
        C([-5, 10.5, -0.7], [3, 3, 1.4], "basalt"),
        C([-6.5, 9.5, -0.6], [1.5, 2.5, 1.2], "basalt"),
        C([-6.8, 9.3, -0.65], [0.6, 3, 1.3], "edge"),
    ]),
    B("socket", "head", [0, 11.5, 0], [
        C([-2, 9, -1.3], [4, 5, 2.6], "charcoal"),
        C([-1.1, 10.2, 1.3], [2.2, 2.6, 0.5], "charcoal"),
        C([-0.7, 10.6, 1.5], [1.4, 1.8, 0.4], "core"),
    ]),
    B("handle", "axe", [0, 0, 0], [
        C([-1, -1, -1], [2, 10, 2], "wrap"),
        C([-1.3, 6, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "charcoal"),
    ]),
    B("pommel", "axe", [0, -2.5, 0], [
        # body top overlaps handle shaft bottom (y=-1) — no gap
        C([-1.6, -4.6, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-0.6, -3.9, 1.5], [1.2, 1.2, 0.3], "core"),
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
    "cleave_cast": (False, 0.6, {
        "axe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [14, 0, 0]),
                                  (0.25, [-28, 0, 0]), (0.4, [-20, 0, 0]),
                                  (0.6, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.35, 1.35, 1.35]),
                                  (0.45, [1, 1, 1]), (0.6, [1, 1, 1])])},
        "blade_main": {"scale": chan([(0, [1, 1, 1]), (0.28, [1.05, 1.05, 1.05]),
                                      (0.5, [1, 1, 1]), (0.6, [1, 1, 1])])},
    }),
    "ember_pulse": (True, 2.6, {
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
        C([-3.5, 16.5, -0.9], [7, 2, 1.8], "basalt"),
        C([-4.2, 9, -0.9], [1.4, 8, 1.6], "basalt"),
        C([2.8, 9, -0.9], [1.4, 8, 1.6], "basalt"),
        C([-3.5, 7, -0.9], [7, 2, 1.8], "basalt"),
        C([-4.1, 16.2, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([3.3, 16.2, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([-4.1, 6.7, -0.8], [0.8, 0.8, 1.6], "edge"),
        C([3.3, 6.7, -0.8], [0.8, 0.8, 1.6], "edge"),
    ]),
    B("panel", "head", [0, 12.7, 0], [
        C([-2.8, 9, -0.7], [5.6, 7.5, 1.2], "basalt", pat="fissure"),
    ]),
    B("core", "head", [0, 12.5, 0.6], [
        C([-0.5, 9.5, 0.5], [1, 6, 0.3], "magma"),
    ]),
    B("socket", "head", [0, 5.7, 0], [
        C([-2, 4.5, -1.2], [4, 2.5, 2.4], "charcoal"),
        C([-2.6, 5.5, -1.0], [1.0, 1.2, 2.0], "basalt"),
        C([1.6, 5.5, -1.0], [1.0, 1.2, 2.0], "basalt"),
        C([-0.9, 5.0, 1.1], [1.8, 1.5, 0.4], "core"),
    ]),
    B("handle", "shovel", [0, 0, 0], [
        C([-1, -4, -1], [2, 8.5, 2], "wrap"),
        C([-1.3, 3.5, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, -1.5, -1.3], [2.6, 1, 2.6], "charcoal"),
    ]),
    B("pommel", "shovel", [0, -5.9, 0], [
        # body top overlaps handle shaft bottom (y=-4) — no gap
        C([-1.6, -7.4, -1.6], [3.2, 3.6, 3.2], "charcoal"),
        C([-0.6, -6.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -8.2, -1], [2, 0.8, 2], "charcoal"),
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
    "excavate_cast": (False, 0.5, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                     (0.25, [-20, 0, 0]), (0.5, [0, 0, 0])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.3, 1.3, 1.3]),
                                  (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "frame": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.04, 1.04, 1.04]),
                                 (0.5, [1, 1, 1])])},
    }),
    "ember_pulse": (True, 2.6, {
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
        C([-1.7, 9, -1.7], [3.4, 3.5, 3.4], "charcoal"),
        C([-1, 12.5, -1], [2, 1, 2], "basalt"),
        C([-0.8, 10, 1.6], [1.6, 1.6, 0.4], "core"),
        C([-2.1, 9.5, -1.2], [0.8, 1.0, 2.4], "basalt"),
        C([1.3, 9.5, -1.2], [0.8, 1.0, 2.4], "basalt"),
    ]),
    B("beak1", "head", [0, 10, 1.5], [
        C([-1.5, 9, 0], [3, 2.2, 3.5], "basalt"),
        C([-1.2, 10.4, 0], [2.4, 0.8, 3.5], "edge"),
    ]),
    B("beak2", "head", [2, 9.2, 4.5], [
        C([1.0, 8.2, 3.2], [2.8, 2.0, 3.2], "basalt"),
        C([1.3, 9.4, 3.2], [2.2, 0.8, 3.2], "edge"),
    ]),
    B("beak3", "head", [4.5, 8.0, 7.0], [
        C([3.5, 7.2, 6.0], [2.6, 1.8, 3.0], "basalt"),
        C([5.7, 6.6, 8.2], [1.0, 1.6, 1.2], "magma"),
    ]),
    B("handle", "hoe", [0, 0, 0], [
        C([-1, 0, -1], [2, 9, 2], "wrap"),
        C([-1.3, 7, -1.3], [2.6, 1, 2.6], "charcoal"),
        C([-1.3, 1, -1.3], [2.6, 1, 2.6], "charcoal"),
    ]),
    B("pommel", "hoe", [0, -1.5, 0], [
        # body top overlaps handle shaft bottom (y=0) — no gap
        C([-1.6, -3.4, -1.6], [3.2, 3.8, 3.2], "charcoal"),
        C([-0.6, -2.9, 1.5], [1.2, 1.2, 0.3], "core"),
        C([-1, -4.2, -1], [2, 0.8, 2], "charcoal"),
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
    "bloom_cast": (False, 0.5, {
        "hoe": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-14, 0, 0]),
                                  (0.28, [-10, 0, 0]), (0.5, [0, 0, 0])])},
        "pommel": {"scale": chan([(0, [1, 1, 1]), (0.12, [1.08, 1.08, 1.08]),
                                  (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.25, [1.3, 1.3, 1.3]),
                                  (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
    }),
    "ember_pulse": (True, 2.6, {
        "socket": {"scale": chan([(0, [1, 1, 1]), (0.65, [1.04, 1.04, 1.04]),
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
    d.text((12, 8), "VEIN FIRE %s front QA  x[%.1f,%.1f] y[%.1f,%.1f]"
           % (name.upper(), minx, maxx, miny, maxy), fill=(255, 200, 150))
    for z, x0, y0, x1, y1 in sorted(projs):
        d.rectangle([20 + (x0 - minx + 2) * Z, 40 + (maxy - y1 + 2) * Z,
                     20 + (x1 - minx + 2) * Z, 40 + (maxy - y0 + 2) * Z],
                    fill=(70, 60, 60, 255), outline=(255, 110, 20), width=1)
    path = os.path.join(ROOT, "docs", "assets", "concepts", "vf-%s-qa-2026-09-03.png" % name)
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
        gp = os.path.join(ASSETS, "geo", "fire", "tool_" + name + ".geo.json")
        ap = os.path.join(ASSETS, "animations", "fire", "tool_" + name + ".animation.json")
        tp = os.path.join(ASSETS, "textures", "fire", "item", name + ".png")
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

