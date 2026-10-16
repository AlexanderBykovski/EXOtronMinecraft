#!/usr/bin/env python3
"""Parthenon Shovel — single-source generator: geo + texture + animations + QA.

Same proven pipeline as the sibling generators (M1/M6/M7/M8).
Outputs under src/main/resources/assets/opusvsexe/:
  geo/paradise/shovel.geo.json
  animations/paradise/shovel.animation.json
  textures/paradise/item/shovel.png
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

IVORY_HL = (247, 241, 227)
IVORY = (233, 223, 200)
IVORY_SH = (207, 194, 164)
IVORY_DK = (168, 154, 120)
VEIN = (216, 204, 176)
GOLD_HL = (246, 222, 154)
GOLD = (217, 169, 66)
GOLD_SH = (138, 95, 34)
GOLD_DK = (107, 74, 30)
RECESS = (94, 66, 24)
SPEC = (255, 243, 196)
RUBY_OUT = (74, 10, 18)
RUBY = (163, 18, 31)
RUBY_CT = (229, 50, 58)
RUBY_HL = (255, 122, 134)
RUBY_SP = (255, 217, 222)
MARBLE_LN = (200, 186, 158)

C = lambda o, s, m, **kw: dict(o=o, s=s, m=m, **kw)


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


FRAME_L = [
    C([-4.3, 9.5, -0.8], [1.4, 3, 1.6], "gold"),
    C([-4.6, 12, -0.8], [1.4, 4, 1.6], "gold", rot=[0, 0, -10], cp=[-4, 13.5, 0]),
    C([-3.9, 15, -0.8], [1.3, 4.5, 1.6], "gold", rot=[0, 0, -18], cp=[-3, 17, 0]),
]
MARBLE_L = [
    C([-3, 15, -0.6], [3, 4.5, 1.2], "ivory", rot=[0, 0, -15], cp=[-1, 19, 0]),
]
SUN_RAYS = []
for _ang, _len in [(0, 2.2), (20, 2.0), (-20, 2.0), (40, 1.7), (-40, 1.7),
                   (60, 1.4), (-60, 1.4), (80, 1.1), (-80, 1.1)]:
    SUN_RAYS.append(C([-0.275, 10, 0.9], [0.55, _len, 0.4], "gold_hl",
                      rot=[0, 0, _ang], cp=[0, 10, 0.9]))

BONES = [
    dict(name="root", parent=None, pivot=[0, 0, 0], cubes=[]),
    dict(name="shovel", parent="root", pivot=[0, 0, 0], cubes=[]),
    dict(name="head", parent="shovel", pivot=[0, 9, 0], cubes=[]),
    dict(name="head_frame", parent="head", pivot=[0, 14, 0], cubes=FRAME_L + mirror(FRAME_L) + [
        C([-1.8, 19.3, -0.8], [3.6, 2.2, 1.6], "gold"),
        C([-0.5, 21.2, -0.5], [1, 1, 1], "gold_hl"),
    ]),
    dict(name="head_marble", parent="head", pivot=[0, 14, 0], cubes=[
        C([-3, 10, -0.6], [6, 6, 1.2], "ivory"),
    ] + MARBLE_L + mirror(MARBLE_L)),
    dict(name="inner_trim", parent="head", pivot=[0, 13, 0], cubes=[
        C([-2.6, 10.5, 0.6], [0.4, 5, 0.25], "gold_hl"),
        C([2.2, 10.5, 0.6], [0.4, 5, 0.25], "gold_hl"),
    ]),
    dict(name="sun_center", parent="head", pivot=[0, 9.7, 1.0], cubes=[
        # medallion back sits INSIDE the marble panel (z overlaps 0.5..0.6,
        # y overlaps 10..10.6) — no gap between head plate and sun
        C([-1.5, 8.8, 0.5], [3, 1.8, 0.6], "gold"),
    ]),
    dict(name="sun_rays", parent="head", pivot=[0, 10, 0.9], cubes=SUN_RAYS),
    dict(name="head_ruby", parent="head", pivot=[0, 7.8, 1.2], cubes=[
        C([-1.2, 6.8, -1], [2.4, 2, 2], "gold"),
        C([-0.9, 7.3, 1.0], [1.8, 1.3, 0.35], "gold_hl"),
        C([-0.8, 7.2, 1.0], [1.6, 1.6, 0.5], "gold"),
        C([-0.55, 7.45, 1.2], [1.1, 1.1, 0.6], "ruby"),
    ]),
    dict(name="handle", parent="shovel", pivot=[0, 0, 0], cubes=[]),
    dict(name="upper_connector", parent="handle", pivot=[0, 6, 0], cubes=[
        C([-1.2, 5.6, -1.2], [2.4, 1.4, 2.4], "gold"),
    ]),
    dict(name="shaft_upper", parent="handle", pivot=[0, 3.3, 0], cubes=[
        C([-1, 1, -1], [2, 4.6, 2], "marble"),
    ]),
    dict(name="ring_01", parent="handle", pivot=[0, 0.5, 0], cubes=[
        C([-1.3, 0, -1.3], [2.6, 1, 2.6], "gold"),
        C([-1.35, 0.4, -1.35], [2.7, 0.2, 2.7], "gold_hl"),
    ]),
    dict(name="shaft_middle", parent="handle", pivot=[0, -1.7, 0], cubes=[
        C([-1, -3.4, -1], [2, 4.4, 2], "marble"),
    ]),
    dict(name="housing", parent="handle", pivot=[0, -5.4, 0], cubes=[
        C([-1.6, -7.4, -1.6], [3.2, 4, 3.2], "gold"),
        C([-1, -6.9, 1.4], [2, 3, 0.4], "bronze"),
        C([-1.1, -4.2, 1.5], [2.2, 0.5, 0.3], "gold_hl"),
        C([-1.1, -7.2, 1.5], [2.2, 0.5, 0.3], "gold_hl"),
    ]),
    dict(name="lower_ruby", parent="handle", pivot=[0, -5.4, 1.7], cubes=[
        C([-0.9, -6.1, 1.4], [1.8, 1.4, 0.5], "gold"),
        C([-0.6, -5.9, 1.6], [1.2, 1.0, 0.6], "ruby"),
    ]),
    dict(name="shaft_lower", parent="handle", pivot=[0, -8.4, 0], cubes=[
        C([-1, -9.4, -1], [2, 2, 2], "marble"),
    ]),
    dict(name="pommel_body", parent="shovel", pivot=[0, -11, 0], cubes=[
        C([-1.7, -12.4, -1.7], [3.4, 3, 3.4], "gold"),
        C([-1.4, -10.2, 1.6], [2.8, 0.5, 0.3], "gold_hl"),
        C([-1.4, -12.2, 1.6], [2.8, 0.5, 0.3], "gold_hl"),
        C([-1, -13.2, -1], [2, 0.8, 2], "gold_dark"),
    ]),
    dict(name="pommel_ruby", parent="shovel", pivot=[0, -10.9, 1.8], cubes=[
        C([-0.9, -11.6, 1.5], [1.8, 1.4, 0.5], "gold"),
        C([-0.6, -11.4, 1.7], [1.2, 1.0, 0.6], "ruby"),
    ]),
    dict(name="fx_head_ruby", parent="head", pivot=[0, 7.8, 1.8], cubes=[]),
    dict(name="fx_sun", parent="head", pivot=[0, 10.5, 1.3], cubes=[]),
    dict(name="fx_lower_ruby", parent="handle", pivot=[0, -5.4, 2.0], cubes=[]),
    dict(name="fx_pommel_ruby", parent="shovel", pivot=[0, -10.9, 2.1], cubes=[]),
]

BONE_NAMES = [b["name"] for b in BONES]

FACES = ["north", "south", "east", "west", "up", "down"]


def face_dims(size, face):
    sx, sy, sz = size
    if face in ("north", "south"):
        return (sx, sy)
    if face in ("east", "west"):
        return (sz, sy)
    return (sx, sz)


def pack_uv():
    items = []
    for bi, b in enumerate(BONES):
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
            raise RuntimeError("UV overflow at %s cube %d face %s"
                               % (BONES[bi]["name"], ci, f))
        rects[(bi, ci, f)] = (x, y, w, h)
        x += w + PAD
        row_h = max(row_h, h)
    return rects


def shade(img, d, box, base, hl, sh):
    x, y, w, h = box
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=base)
    if w >= 2 and h >= 2:
        d.line([x, y, x + w - 1, y], fill=hl)
        d.line([x, y, x, y + h - 1], fill=hl)
        d.line([x, y + h - 1, x + w - 1, y + h - 1], fill=sh)
        d.line([x + w - 1, y, x + w - 1, y + h - 1], fill=sh)


def veins(d, box, seed):
    import random
    rnd = random.Random(seed)
    x, y, w, h = box
    for _ in range(max(1, (w + h) // 24)):
        x0 = x + rnd.randrange(max(1, w - 1))
        y0 = y + rnd.randrange(max(1, h - 1))
        ln = rnd.randrange(3, max(4, min(w, h) // 2))
        if rnd.random() < 0.5:
            d.line([x0, y0, min(x + w - 1, x0 + ln), y0], fill=VEIN)
        else:
            d.line([x0, y0, x0, min(y + h - 1, y0 + ln)], fill=VEIN)


def meander(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=GOLD)
    d.line([x, y, x + w - 1, y], fill=GOLD_DK)
    d.line([x, y + h - 1, x + w - 1, y + h - 1], fill=GOLD_DK)
    u = 6
    top, bot = y + 1, y + h - 2
    if bot - top < 2:
        return
    mid = (top + bot) // 2
    cx = x + 1
    while cx + u <= x + w:
        d.line([cx, bot, cx, top + 1], fill=GOLD_DK)
        d.line([cx, top + 1, cx + u - 2, top + 1], fill=GOLD_DK)
        d.line([cx + u - 2, top + 1, cx + u - 2, mid], fill=GOLD_DK)
        d.line([cx + u - 2, mid, cx + 2, mid], fill=GOLD_DK)
        d.line([cx + 2, mid, cx + 2, bot - 1], fill=GOLD_DK)
        d.line([cx, bot, cx + u - 2, bot], fill=GOLD_HL)
        cx += u


def paint_ruby_face(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=RUBY_OUT)
    ix, iy = max(1, w // 5), max(1, h // 5)
    d.rectangle([x + ix, y + iy, x + w - 1 - ix, y + h - 1 - iy], fill=RUBY)
    jx, jy = max(1, w // 3), max(1, h // 3)
    d.rectangle([x + jx, y + jy, x + w - 1 - jx, y + h - 1 - jy], fill=RUBY_CT)
    hx, hy = x + max(1, w // 4), y + max(1, h // 5)
    d.ellipse([hx - 1, hy - 1, hx + 1, hy + 1], fill=RUBY_HL)
    d.point((x + w - 2, y + 1), fill=RUBY_SP)


def paint_face(img, d, box, mat, face, seed, pat):
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    if mat == "ivory":
        shade(img, d, box, IVORY, IVORY_HL, IVORY_SH)
        d.rectangle([x, y, x + w - 1, y + h - 1], outline=IVORY_DK)
        veins(d, box, seed)
    elif mat == "gold":
        shade(img, d, box, GOLD, GOLD_HL, GOLD_SH)
    elif mat == "gold_hl":
        shade(img, d, box, GOLD_HL, SPEC, GOLD)
        d.point((x, y), fill=SPEC)
    elif mat == "gold_dark":
        shade(img, d, box, GOLD_SH, GOLD, GOLD_DK)
    elif mat == "gold_border":
        if pat == "key" and face in ("south", "north"):
            meander(d, box)
        else:
            shade(img, d, box, GOLD, GOLD_HL, GOLD_SH)
    elif mat == "bronze":
        shade(img, d, box, RECESS, GOLD_DK, (40, 26, 8))
    elif mat == "marble":
        shade(img, d, box, IVORY, IVORY_HL, IVORY_SH)
        if face in ("south", "north") and h >= 8:
            for yy in range(y + h // 3, y + h, h // 3 + 1):
                if yy < y + h - 1:
                    d.line([x + 1, yy, x + w - 2, yy], fill=MARBLE_LN)
        veins(d, box, seed + 7)
    elif mat == "ruby":
        if face in ("south", "north"):
            paint_ruby_face(d, box)
        else:
            shade(img, d, box, RUBY, RUBY_CT, RUBY_OUT)
    else:
        shade(img, d, box, (255, 0, 255), (255, 0, 255), (255, 0, 255))

def chan(frames):
    return {(f"{t:.3f}".rstrip("0").rstrip(".")): {"vector": list(v)}
            for t, v in frames}


# M6: idle is a STATIC hold.
ANIMS = {
    "idle": (True, 3.0, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (3.0, [0, 0, 0])])},
    }),
    "equip": (False, 0.4, {
        "shovel": {
            "rotation": chan([(0, [-18, 0, 0]), (0.25, [3, 0, 0]), (0.4, [0, 0, 0])]),
            "position": chan([(0, [0, -2, 0]), (0.25, [0, 0.3, 0]), (0.4, [0, 0, 0])]),
        },
        "head_ruby": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
        "pommel_ruby": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.12, 1.12, 1.12]), (0.4, [1, 1, 1])])},
    }),
    "dig": (False, 0.45, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.06, [6, 0, 0]),
                                     (0.12, [-10, 0, 0]), (0.18, [-16, 0, 0]),
                                     (0.22, [-13, 0, 0]), (0.3, [-18, 0, 0]),
                                     (0.45, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.06, [0, 0, -2]),
                                   (0.12, [0, 0, 1.5]), (0.45, [0, 0, 0])])},
        "head_ruby": {"scale": chan([(0, [1, 1, 1]), (0.22, [1.25, 1.25, 1.25]),
                                     (0.32, [1, 1, 1]), (0.45, [1, 1, 1])])},
    }),
    "attack": (False, 0.4, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.08, [10, 0, 0]),
                                     (0.16, [-25, 0, 0]), (0.22, [-21, 0, 0]),
                                     (0.32, [-27, 0, 0]), (0.4, [0, 0, 0])])},
        "head": {"rotation": chan([(0, [0, 0, 0]), (0.08, [0, 0, -3]),
                                   (0.16, [0, 0, 2]), (0.4, [0, 0, 0])])},
        "head_ruby": {"scale": chan([(0, [1, 1, 1]), (0.2, [1.2, 1.2, 1.2]),
                                     (0.32, [1, 1, 1]), (0.4, [1, 1, 1])])},
    }),
    "haste_cast": (False, 0.5, {
        "shovel": {"rotation": chan([(0, [0, 0, 0]), (0.12, [-16, 0, 0]),
                                     (0.3, [-12, 0, 0]), (0.5, [0, 0, 0])])},
        "pommel_ruby": {"scale": chan([(0, [1, 1, 1]), (0.12, [1.3, 1.3, 1.3]),
                                        (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "lower_ruby": {"scale": chan([(0, [1, 1, 1]), (0.18, [1.3, 1.3, 1.3]),
                                      (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "head_ruby": {"scale": chan([(0, [1, 1, 1]), (0.24, [1.35, 1.35, 1.35]),
                                     (0.4, [1, 1, 1]), (0.5, [1, 1, 1])])},
        "sun_rays": {"scale": chan([(0, [1, 1, 1]), (0.3, [1.1, 1.1, 1.1]),
                                    (0.45, [1, 1, 1]), (0.5, [1, 1, 1])])},
    }),
    "haste_recover": (False, 0.3, {
        "shovel": {"rotation": chan([(0, [-12, 0, 0]), (0.15, [-4, 0, 0]), (0.3, [0, 0, 0])])},
        "head_ruby": {"scale": chan([(0, [1.1, 1.1, 1.1]), (0.3, [1, 1, 1])])},
    }),
    "gem_pulse": (True, 2.6, {
        "pommel_ruby": {"scale": chan([(0, [1, 1, 1]), (0.43, [1.03, 1.03, 1.03]),
                                       (0.86, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "lower_ruby": {"scale": chan([(0, [1, 1, 1]), (1.08, [1.03, 1.03, 1.03]),
                                      (1.51, [1, 1, 1]), (2.6, [1, 1, 1])])},
        "head_ruby": {"scale": chan([(0, [1, 1, 1]), (1.73, [1.03, 1.03, 1.03]),
                                     (2.16, [1, 1, 1]), (2.6, [1, 1, 1])])},
    }),
}


def build_geo(rects):
    bones = []
    for bi, b in enumerate(BONES):
        jb = {"name": b["name"], "pivot": b["pivot"]}
        if b["parent"]:
            jb["parent"] = b["parent"]
        cubes = []
        for ci, c in enumerate(b["cubes"]):
            # M1: per-face UV under the "uv" key (object) with uv_size.
            uv = {}
            for f in FACES:
                x, y, w, h = rects[(bi, ci, f)]
                uv[f] = {"uv": [x, y, x + w, y + h], "uv_size": [w, h]}
            # EPS 0.02 volumetric overlap kills exact-coplanar z-fighting.
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
        bones.append(jb)
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.shovel",
                "texture_width": TEX_W,
                "texture_height": TEX_H,
                "visible_bounds_width": 3,
                "visible_bounds_height": 4,
                "visible_bounds_offset": [0, 0, 0],
            },
            "bones": bones,
        }],
    }


def build_animations():
    out = {"format_version": "1.8.0", "animations": {}}
    for name, (loop, length, bones) in ANIMS.items():
        assert all(bn in BONE_NAMES for bn in bones), "unknown bone in " + name
        out["animations"][name] = {"loop": loop, "animation_length": length, "bones": bones}
    return out


def paint_texture(rects):
    img = Image.new("RGBA", (TEX_W, TEX_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    seed = 0
    for bi, b in enumerate(BONES):
        for ci, c in enumerate(b["cubes"]):
            pat = c.get("pat")
            for f in FACES:
                paint_face(img, d, rects[(bi, ci, f)], c["m"], f, seed, pat)
                seed += 1
    return img


def qa_sheet():
    allx, ally = [], []
    projs = []
    for bi, b in enumerate(BONES):
        for ci, c in enumerate(b["cubes"]):
            ox, oy, oz = c["o"]
            sx, sy, sz = c["s"]
            pts = [(ox + dx, oy + dy) for dx in (0, sx) for dy in (0, sy)]
            if "rot" in c and c["rot"][2]:
                ang = math.radians(c["rot"][2])
                px, py = c.get("cp", b["pivot"])[:2]
                npts = []
                for qx, qy in pts:
                    vx, vy = qx - px, qy - py
                    npts.append((px + vx * math.cos(ang) - vy * math.sin(ang),
                                 py + vx * math.sin(ang) + vy * math.cos(ang)))
                pts = npts
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            allx += xs
            ally += ys
            projs.append((oz + sz, min(xs), min(ys), max(xs), max(ys)))
    minx, maxx, miny, maxy = min(allx), max(allx), min(ally), max(ally)
    W = int(math.ceil(maxx - minx)) + 4
    H = int(math.ceil(maxy - miny)) + 4
    Z = 14
    sheet = Image.new("RGBA", (W * Z + 40, H * Z + 60), (16, 14, 20, 255))
    d = ImageDraw.Draw(sheet)
    d.text((12, 8), "PARTHENON SHOVEL front QA  x[%.1f,%.1f] y[%.1f,%.1f]"
           % (minx, maxx, miny, maxy), fill=(240, 230, 200))
    for z, x0, y0, x1, y1 in sorted(projs):
        d.rectangle([20 + (x0 - minx + 2) * Z, 40 + (maxy - y1 + 2) * Z,
                     20 + (x1 - minx + 2) * Z, 40 + (maxy - y0 + 2) * Z],
                    fill=(233, 223, 200, 255), outline=(217, 169, 66), width=1)
    sheet_path = os.path.join(ROOT, "docs", "assets", "concepts", "shovel-qa-2026-09-03.png")
    os.makedirs(os.path.dirname(sheet_path), exist_ok=True)
    sheet.save(sheet_path)
    print("qa:", sheet_path)


def main():
    rects = pack_uv()
    geo = build_geo(rects)
    anims = build_animations()
    tex = paint_texture(rects)
    gp = os.path.join(ASSETS, "geo", "paradise", "shovel.geo.json")
    ap = os.path.join(ASSETS, "animations", "paradise", "shovel.animation.json")
    tp = os.path.join(ASSETS, "textures", "paradise", "item", "shovel.png")
    for p in (gp, ap, tp):
        os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(gp, "w") as f:
        json.dump(geo, f, indent=1)
    with open(ap, "w") as f:
        json.dump(anims, f, indent=1)
    tex.save(tp)
    cubes = sum(len(b["cubes"]) for b in BONES)
    print("bones=%d cubes=%d anims=%s" % (len(BONES), cubes, list(ANIMS)))
    print("wrote", gp)
    print("wrote", ap)
    print("wrote", tp)
    qa_sheet()


if __name__ == "__main__":
    main()
