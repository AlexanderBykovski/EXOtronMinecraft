#!/usr/bin/env python3
"""Red Samurai Shogun (`red_shogun`) asset generator.
Deterministic: geo JSON (box UV, 128x128) + painted texture + 14 GeckoLib animations + QA.
Run from repo root: python3 scripts/gen_red_shogun_assets.py
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from geokit import (ROOT, ASSETS, shelf_pack, Tex, emit_geo, bone, AnimBuilder,
                    emit_anims, validate, face_rects, paint_cloth, paint_metal,
                    paint_leather, paint_straw, paint_wrap, br_rot)

# ------------------------------------------------------------------ palette
PAL = {
    # skin
    "skin":    (217, 168, 126, 255), "skin_hi": (231, 186, 146, 255),
    "skin_sh": (168, 126, 92, 255),
    # hair / face details
    "hair":    (36, 28, 22, 255),    "brow": (43, 30, 22, 255),
    "eye_w":   (238, 234, 226, 255), "eye": (58, 36, 24, 255),
    # crimson lacquer family
    "lac":     (142, 42, 34, 255),   "lac_hi": (184, 67, 47, 255),
    "lac_dk":  (92, 22, 15, 255),    "verm": (112, 29, 20, 255),
    "lac_blk": (63, 18, 14, 255),
    # black iron
    "iron":    (35, 33, 31, 255),    "iron_hi": (78, 74, 70, 255), "iron_dk": (22, 21, 20, 255),
    # indigo cloth
    "ind":     (28, 30, 48, 255),    "ind_hi": (58, 62, 92, 255), "ind_dk": (18, 19, 32, 255),
    # antique gold
    "gold":    (168, 130, 60, 255),  "gold_hi": (201, 162, 78, 255), "gold_dk": (122, 92, 40, 255),
    # leather / cords
    "lea":     (92, 58, 32, 255),    "lea_hi": (122, 80, 48, 255), "lea_dk": (62, 39, 22, 255),
    # straw
    "straw":   (201, 176, 136, 255), "straw_hi": (222, 200, 162, 255), "straw_dk": (168, 144, 106, 255),
    # steel
    "steel":   (154, 160, 168, 255), "steel_hi": (200, 205, 212, 255), "steel_dk": (106, 112, 120, 255),
    # black lacquer (saya / tsuka)
    "blk":     (24, 22, 22, 255),    "blk_hi": (52, 48, 46, 255),
}

# ------------------------------------------------------------------ skeleton
BONES = []          # (name, parent, pivot, jrot)
CUBES = []          # dicts: bone,name,origin,size,inflate?,mirror?,jrot/cpivot?,paint

def C(bone_name, name, origin, size, paint, inflate=0, jrot=None, cpivot=None):
    CUBES.append(dict(bone=bone_name, name=name, origin=list(origin),
                      size=tuple(size), paint=paint,
                      inflate=inflate, jrot=jrot, cpivot=cpivot))

def B(name, parent, pivot, jrot=None):
    BONES.append((name, parent, pivot, jrot or (0, 0, 0)))

# body ------------------------------------------------------------------
B("root", None, (0, 0, 0))
B("master", "root", (0, 13, 0))
B("body", "master", (0, 13, 0))
C("body", "torso",      (-4.5, 13, -2.75), (9, 12, 5.5), "cloth")
C("body", "do_main",    (-5.0, 16.8, -3.2), (10, 8, 6.4), "do", 0.06)
C("body", "do_upper",   (-5.0, 23.2, -3.4), (10, 2.6, 6.8), "do_top", 0.06)
C("body", "back_plate", (-3.75, 18.2, 3.25), (7.5, 5.5, 1.05), "do")
B("waist_belt", "body", (0, 15.5, 0))
C("waist_belt", "belt",     (-4.9, 15.4, -2.2), (9.8, 1.7, 4.4), "belt")
C("waist_belt", "belt_knot",(-1.0, 15.15, -3.05), (2.0, 1.9, 0.75), "knot")
for side, sx in (("front", 1), ("back", -1)):
    B(f"kusazuri_{side}", "body", (0, 15.4, 2.85 * sx),
      (8 * sx, 0, 0) if side == "front" else (-8 * sx, 0, 0))
    C(f"kusazuri_{side}", f"kusazuri_{side}", (-4, 11.6, -3.35 if side == "front" else 2.35),
      (8, 3.8, 1), "kusazuri")
B("kusazuri_left", "body", (5.05, 15.4, 0), (10, 0, 0))
C("kusazuri_left", "kusazuri_left", (4.55, 11.7, -2.0), (1, 3.7, 3.1), "kusazuri")
B("kusazuri_right", "body", (-5.05, 15.4, 0), (-10, 0, 0))
C("kusazuri_right", "kusazuri_right", (-5.55, 11.7, -2.0), (1, 3.7, 3.1), "kusazuri")

# head ------------------------------------------------------------------
B("head", "master", (0, 25, 0))
C("head", "head", (-4, 25, -4), (8, 8, 8), "head")
B("menpo", "head", (0, 29, -4))
C("menpo", "menpo", (-3.5, 25.0, -4.75), (7, 3.6, 0.8), "menpo")
B("kabuto", "head", (0, 31, 0))
C("kabuto", "kabuto_bowl",  (-4.5, 30.8, -4.5), (9, 3.8, 9), "bowl")
C("kabuto", "kabuto_brim",  (-2.9, 30.7, -6.3), (5.8, 0.7, 2.0), "lacq")
C("kabuto", "shikoro_back", (-3.4, 29.4, 4.2), (6.8, 3.6, 1.0), "shikoro",
  jrot=(-12, 0, 0), cpivot=(0, 30.6, 4.2))
C("kabuto", "shikoro_left", (4.4, 27.6, -2.1), (1.0, 2.8, 4.2), "shikoro",
  jrot=(0, 0, 14), cpivot=(4.9, 30.4, 0))
C("kabuto", "shikoro_right", (-5.4, 27.6, -2.1), (1.0, 2.8, 4.2), "shikoro",
  jrot=(0, 0, -14), cpivot=(-4.9, 30.4, 0))
C("kabuto", "crescent_center", (-1.4, 34.75, -0.3), (2.8, 0.7, 0.6), "gold")
C("kabuto", "crescent_left",  (-0.2, 35.2, -0.3), (3.2, 0.7, 0.6), "gold",
  jrot=(0, 0, 24), cpivot=(-0.2, 35.4, 0))
C("kabuto", "crescent_right", (-3.0, 35.2, -0.3), (3.2, 0.7, 0.6), "gold",
  jrot=(0, 0, -24), cpivot=(0.2, 35.4, 0))
C("kabuto", "crescent_tip_left",  (2.7, 36.5, -0.3), (1.6, 0.6, 0.6), "gold",
  jrot=(0, 0, 42), cpivot=(2.7, 36.7, 0))
C("kabuto", "crescent_tip_right", (-4.3, 36.5, -0.3), (1.6, 0.6, 0.6), "gold",
  jrot=(0, 0, -42), cpivot=(-2.7, 36.7, 0))
C("kabuto", "maedate_disc", (-0.9, 34.9, -0.75), (1.8, 1.8, 0.45), "emblem")

# arms --------------------------------------------------------------------
for s, sx in (("right", -1), ("left", 1)):
    B(f"{s}_arm", "master", (6.55 * sx, 23.4, 0))
    C(f"{s}_arm", f"{s}_sleeve", (4.55 * sx if sx > 0 else -8.45, 11.2, -1.9), (3.9, 12.2, 3.8), "cloth")
    B(f"{s}_sode", f"{s}_arm", (6.55 * sx, 23.4, 0))
    C(f"{s}_sode", f"{s}_sode_plate", (4.95 * sx, 19.7, -2.2), (4.4, 4.7, 4.4), "sode")
    C(f"{s}_sode", f"{s}_sode_rim", (4.8 * sx, 24.1, -2.35), (4.7, 1.3, 4.7), "rim")
    B(f"{s}_kote", f"{s}_arm", (6.55 * sx, 23.4, 0))
    C(f"{s}_kote", f"{s}_kote_plate", (4.25 * sx, 13.2, -2.15), (4.5, 4.6, 4.3), "kote")
    C(f"{s}_kote", f"{s}_wrist", (4.15 * sx, 11.0, -2.25), (4.7, 1.3, 4.5), "strap")

# legs --------------------------------------------------------------------
for s, sx in (("right", -1), ("left", 1)):
    B(f"{s}_leg", "master", (2.35 * sx, 13, 0))
    C(f"{s}_leg", f"{s}_trouser", (0.35 * sx if sx > 0 else -4.25, 0, -1.9), (3.9, 13, 3.8), "cloth")
    B(f"{s}_haidate", f"{s}_leg", (2.35 * sx, 13, 0))
    C(f"{s}_haidate", f"{s}_haidate", (0.05 * sx, 8.8, -2.2), (4.5, 4.0, 4.4), "haidate")
    B(f"{s}_suneate", f"{s}_leg", (2.35 * sx, 6.4, 0))
    C(f"{s}_suneate", f"{s}_suneate", (0.15 * sx, 1.4, -2.1), (4.3, 5.2, 4.2), "suneate")
    B(f"{s}_foot", f"{s}_leg", (2.35 * sx, 1.4, 0))
    C(f"{s}_foot", f"{s}_foot", (0.25 * sx, 0, -3.3), (4.1, 1.4, 5.2), "foot")

# equipment (daisho, left waist: behind arm, slightly back) -----------------
B("equipment", "master", (0, 13, 0))
B("katana_scabbard", "equipment", (5.4, 17.2, 3.85), (-20, 0, 14))
C("katana_scabbard", "katana_saya", (4.5, 6.4, 2.9), (1.8, 11.0, 1.9), "saya")
B("katana_handle", "katana_scabbard", (5.4, 17.3, 3.85), (-12, 0, 3))
C("katana_handle", "katana_tsuka", (4.65, 17.1, 2.9), (1.5, 4.8, 1.9), "tsuka")
B("wakizashi_scabbard", "equipment", (3.5, 16.2, 3.85), (-18, 0, 2))
C("wakizashi_scabbard", "wakizashi_saya", (2.65, 8.2, 2.9), (1.7, 8.4, 1.7), "saya")
B("wakizashi_handle", "wakizashi_scabbard", (3.5, 16.3, 3.85), (-12, 0, 2))
C("wakizashi_handle", "wakizashi_tsuka", (2.7, 16.1, 3.0), (1.6, 4.4, 1.7), "tsuka")

shelf_pack(CUBES, atlas=128, pad=1)

# ------------------------------------------------------------------ texture
tex = Tex(128, PAL)

def lamellar(r, base="lac", hi="lac_hi", dk="lac_dk", rows=3, border="iron", rivets=True):
    x, y, w, h = r
    tex.rect(r, PAL[base])
    for j in range(h):
        m = j % rows
        for i in range(w):
            if m == 0:
                tex.set(x + i, y + j, PAL[dk])
            elif m == 1 and i == 0:
                tex.set(x + i, y + j, PAL[hi])
    if border:
        tex.border(r, PAL[border])
    if rivets and w > 4 and h > 4:
        for j in (1, h - 2):
            for i in range(1, w - 1, max(3, w // 4)):
                tex.set(x + i, y + j, PAL["gold_dk"])

def paint(cube):
    u, v = cube["tex"]
    w, h, d = cube["size"]
    R = face_rects(u, v, w, h, d)
    name, kind = cube["name"], cube["paint"]
    n = R["north"]
    if kind == "cloth":
        for f in ("north", "south", "east", "west"):
            paint_cloth(tex, R[f], PAL["ind"], PAL["ind_hi"], PAL["ind_dk"])
        if "sleeve" in name:                       # exposed hands
            for f in ("north", "south", "east", "west"):
                x, y, fw, fh = R[f]
                tex.rect((x, y + fh - 3, fw, 3), PAL["skin"])
                tex.rect((x, y + fh - 3, fw, 1), PAL["skin_sh"])
        tex.rect(R["up"], PAL["ind_dk"]); tex.rect(R["down"], PAL["ind_dk"])
    elif kind == "do" or kind == "do_top":
        for f in ("north", "south", "up", "down"):
            lamellar(R[f], rivets=(kind == "do"))
        for f in ("east", "west"):                 # dark-red side panels
            lamellar(R[f], base="verm", hi="lac_hi", dk="lac_dk")
        if kind == "do":                           # cords + medallions on chest
            x, y, fw, fh = n
            cx = x + fw // 2
            for j in range(1, fh - 1):
                tex.set(cx - 1, y + j, PAL["lea"]); tex.set(cx, y + j, PAL["lea_dk"])
            for mx in (cx - 4, cx + 3):
                tex.rect((x + mx if mx < cx else x + mx, y + 2, 2, 2), PAL["gold"])
                tex.set(x + mx + (1 if mx < cx else 0), y + 3, PAL["gold_dk"])
    elif kind == "kusazuri":
        for f in ("north", "south", "east", "west", "up", "down"):
            lamellar(R[f], rivets=False)
            x, y, fw, fh = R[f]
            tex.rect((x, y + fh - 1, fw, 1), PAL["iron"])
    elif kind == "sode":
        for f in ("north", "south", "east", "west"):
            lamellar(R[f])
        tex.rect(R["up"], PAL["lac_dk"]); tex.rect(R["down"], PAL["iron"])
    elif kind == "rim":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_metal(tex, R[f], PAL["iron"], PAL["iron_hi"], PAL["iron_dk"])
    elif kind == "kote":
        for f in ("north", "south", "east", "west"):
            lamellar(R[f], base="verm", hi="lac_hi", dk="lac_blk", border="iron_dk")
            x, y, fw, fh = R[f]
            for j in range(2, fh - 2, 3):          # leather straps
                tex.rect((x + 1, y + j, fw - 2, 1), PAL["lea"])
        tex.rect(R["up"], PAL["lac_dk"]); tex.rect(R["down"], PAL["lac_dk"])
    elif kind == "strap":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_leather(tex, R[f], PAL["lea"], PAL["lea_hi"], PAL["lea_dk"])
    elif kind == "belt":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_leather(tex, R[f], PAL["lea"], PAL["lea_hi"], PAL["lea_dk"])
        x, y, fw, fh = R["north"]                  # gold fasteners
        for i in range(2, fw - 2, 3):
            tex.set(x + i, y + fh // 2, PAL["gold"])
    elif kind == "knot":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_leather(tex, R[f], PAL["lea_dk"], PAL["lea"], PAL["blk"])
        x, y, fw, fh = n
        tex.set(x + fw // 2, y + fh // 2, PAL["gold"])
    elif kind == "haidate":
        for f in ("north", "south", "east", "west"):
            lamellar(R[f], rivets=False)
        for f in ("up", "down"):
            tex.rect(R[f], PAL["lac_dk"])
    elif kind == "suneate":
        for f in ("north", "south", "east", "west"):
            lamellar(R[f], rivets=False)
            x, y, fw, fh = R[f]
            cx = x + fw // 2                       # black vertical reinforcement
            tex.rect((cx - 1, y + 1, 2, fh - 2), PAL["lac_blk"])
            tex.set(cx, y + 1, PAL["iron_hi"])
        tex.rect(R["up"], PAL["lac_dk"]); tex.rect(R["down"], PAL["iron"])
    elif kind == "foot":
        for f in ("north", "south", "east", "west"):
            paint_straw(tex, R[f], PAL["straw"], PAL["straw_hi"], PAL["straw_dk"])
        x, y, fw, fh = R["north"]
        tex.rect((x, y, fw, 1), PAL["blk"])        # tabi strap line
        tex.rect(R["up"], PAL["straw_dk"]); tex.rect(R["down"], PAL["blk"])
    elif kind == "lacq":
        for f in ("north", "south", "east", "west", "up", "down"):
            tex.rect(R[f], PAL["lac"])
        x, y, fw, fh = n
        tex.border(n, PAL["lac_dk"]); tex.set(x + 1, y + 1, PAL["lac_hi"])
    elif kind == "shikoro":
        for f in ("north", "south", "east", "west"):
            lamellar(R[f], rows=2, rivets=False)
        tex.rect(R["up"], PAL["lac_dk"]); tex.rect(R["down"], PAL["lac_blk"])
    elif kind == "bowl":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["lac"])
            for i in range(1, fw - 1, 2):          # hachi plate seams
                for j in range(fh):
                    tex.set(x + i, y + j, PAL["lac_dk"])
            cx = x + fw // 2                       # gold suji ridge
            for j in range(fh):
                tex.set(cx, y + j, PAL["gold_dk"])
            tex.border(R[f], PAL["iron_dk"])
        tex.rect(R["up"], PAL["lac_hi"])           # tehen kanamono
        tex.rect((R["up"][0] + R["up"][2] // 2 - 1, R["up"][1] + R["up"][3] // 2 - 1, 2, 2), PAL["gold"])
        tex.rect(R["down"], PAL["iron"])
    elif kind == "gold":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_metal(tex, R[f], PAL["gold"], PAL["gold_hi"], PAL["gold_dk"])
    elif kind == "emblem":
        for f in ("north", "south", "east", "west", "up", "down"):
            tex.rect(R[f], PAL["gold"])
        x, y, fw, fh = n                           # original clan mark: ring + 4 petals
        cx, cy = x + fw // 2, y + fh // 2
        for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            tex.set(cx + i, cy + j, PAL["gold_dk"])
        tex.set(cx, cy, PAL["blk"])
        tex.set(cx, cy - 2, PAL["gold_hi"]); tex.set(cx, cy + 2, PAL["gold_hi"])
        tex.set(cx - 2, cy, PAL["gold_hi"]); tex.set(cx + 2, cy, PAL["gold_hi"])
    elif kind == "saya":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["blk"])
            for j in range(1, fh - 1, 4):          # lacquer gloss
                tex.rect((x + 1, y + j, max(1, fw // 3), 1), PAL["blk_hi"])
            tex.rect((x, y + fh - 2, fw, 2), PAL["gold_dk"])   # kojiri
            if f == "north":
                tex.rect((x, y + fh // 2 - 1, fw, 2), PAL["verm"])  # sageo band
        tex.rect(R["up"], PAL["iron"]); tex.rect(R["down"], PAL["blk"])
    elif kind == "tsuka":
        for f in ("north", "south", "east", "west"):
            paint_wrap(tex, R[f], PAL["blk"], PAL["lea_dk"], gold=PAL["gold"])
        for f in ("up", "down"):
            tex.rect(R[f], PAL["gold_dk"])
    elif kind == "blade":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            paint_metal(tex, R[f], PAL["steel"], PAL["steel_hi"], PAL["steel_dk"])
            tex.set(x + fw - 1, y, PAL["steel_hi"])
        tex.rect(R["up"], PAL["steel_hi"]); tex.rect(R["down"], PAL["steel_dk"])
    elif kind == "head":
        for f in ("up", "down"):
            tex.rect(R[f], PAL["hair"])
        for f in ("east", "west", "south"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["skin"])
            tex.rect((x, y, fw, 2), PAL["hair"])   # hair under helmet
            tex.rect((x, y + fh - 1, fw, 1), PAL["skin_sh"])
        x, y, fw, fh = n
        tex.rect(n, PAL["skin"])
        tex.rect((x, y, fw, 3), PAL["hair"])       # forehead under kabuto
        tex.set(x + 3, y + 2, PAL["skin"]); tex.set(x + 4, y + 2, PAL["skin"])
        for bx in (1, 5):                          # thick brows
            tex.rect((x + bx, y + 3, 2, 1), PAL["brow"])
        for ex in (1, 5):                          # focused dark-brown eyes
            tex.set(x + ex, y + 4, PAL["eye_w"]); tex.set(x + ex + 1, y + 4, PAL["eye"])
        for j in range(5, fh):                     # jaw area (under menpo)
            for i in range(fw):
                tex.set(x + i, y + j, PAL["skin"])
        tex.rect((x, y + fh - 1, fw, 1), PAL["skin_sh"])
    elif kind == "menpo":
        for f in ("north", "south", "east", "west", "up", "down"):
            tex.rect(R[f], PAL["verm"])
        x, y, fw, fh = n
        tex.border(n, PAL["lac_blk"])
        for i in range(2, fw - 2):                 # moustache
            tex.set(x + i, y + 1, PAL["brow"])
        cx = x + fw // 2
        tex.rect((cx - 1, y + 1, 1, 2), PAL["lac_dk"])          # nose ridge
        for sx in (cx - 3, cx + 2):                # ventilation slits
            tex.set(sx, y + 2, PAL["blk"]); tex.set(sx, y + 3, PAL["blk"])
        tex.rect((cx - 1, y + fh - 2, 3, 1), PAL["lac_blk"])    # stern mouth line

for c in CUBES:
    paint(c)

# ------------------------------------------------------------------ animations
A = []

def anim(name, length, loop):
    a = AnimBuilder(f"animation.red_shogun.{name}", length, loop)
    A.append(a)
    return a

# idle: restrained breathing, slow scan
a = anim("idle", 3.4, True)
a.bone("body", rot=[(0, (0, 0, 0)), (1.7, (1.6, 0, 0)), (3.4, (0, 0, 0))],
       pos=[(0, (0, 0, 0)), (1.7, (0, -0.35, 0)), (3.4, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 2.5, 0)), (1.2, (0, -2.5, 0)), (2.3, (0, 1.5, 0)), (3.4, (0, 2.5, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 2)), (1.7, (0.8, 0, 3)), (3.4, (0, 0, 2))])
a.bone("left_arm", rot=[(0, (0, 0, -2)), (1.7, (0.8, 0, -3)), (3.4, (0, 0, -2))])
a.bone("right_sode", rot=[(0, (0.6, 0, 0)), (2.2, (1.8, 0, 0)), (3.4, (0.6, 0, 0))])
a.bone("left_sode", rot=[(0, (0.6, 0, 0)), (2.2, (1.8, 0, 0)), (3.4, (0.6, 0, 0))])
a.bone("kabuto", rot=[(0, (0.4, 0, 0)), (1.7, (-0.4, 0, 0)), (3.4, (0.4, 0, 0))])

# walk: heavy measured stride, secondary sway
a = anim("walk", 1.15, True)
a.bone("right_leg", rot=[(0, (34, 0, 0)), (0.29, (4, 0, 0)), (0.575, (-30, 0, 0)), (0.86, (-4, 0, 0)), (1.15, (34, 0, 0))])
a.bone("left_leg", rot=[(0, (-30, 0, 0)), (0.29, (-4, 0, 0)), (0.575, (34, 0, 0)), (0.86, (4, 0, 0)), (1.15, (-30, 0, 0))])
a.bone("right_arm", rot=[(0, (-26, 0, 2)), (0.575, (24, 0, 2)), (1.15, (-26, 0, 2))])
a.bone("left_arm", rot=[(0, (24, 0, -2)), (0.575, (-26, 0, -2)), (1.15, (24, 0, -2))])
a.bone("body", rot=[(0, (0, 3, 0)), (0.575, (0, -3, 0)), (1.15, (0, 3, 0))],
       pos=[(0, (0, 0, 0)), (0.29, (0, -0.55, 0)), (0.575, (0, 0, 0)), (0.86, (0, -0.55, 0)), (1.15, (0, 0, 0))])
a.bone("head", rot=[(0, (0, -3, 0)), (0.575, (0, 3, 0)), (1.15, (0, -3, 0))])
a.bone("right_suneate", rot=[(0, (-10, 0, 0)), (0.575, (8, 0, 0)), (1.15, (-10, 0, 0))])
a.bone("left_suneate", rot=[(0, (8, 0, 0)), (0.575, (-10, 0, 0)), (1.15, (8, 0, 0))])
a.bone("kusazuri_front", rot=[(0, (3, 0, 0)), (0.575, (-3, 0, 0)), (1.15, (3, 0, 0))])
a.bone("kusazuri_back", rot=[(0, (-3, 0, 0)), (0.575, (3, 0, 0)), (1.15, (-3, 0, 0))])
a.bone("right_sode", rot=[(0, (2, 0, 0)), (0.575, (-2, 0, 0)), (1.15, (2, 0, 0))])
a.bone("left_sode", rot=[(0, (-2, 0, 0)), (0.575, (2, 0, 0)), (1.15, (-2, 0, 0))])

# run: committed forward drive
a = anim("run", 0.8, True)
a.bone("right_leg", rot=[(0, (46, 0, 0)), (0.2, (8, 0, 0)), (0.4, (-42, 0, 0)), (0.6, (-8, 0, 0)), (0.8, (46, 0, 0))])
a.bone("left_leg", rot=[(0, (-42, 0, 0)), (0.2, (-8, 0, 0)), (0.4, (46, 0, 0)), (0.6, (8, 0, 0)), (0.8, (-42, 0, 0))])
a.bone("right_arm", rot=[(0, (-40, 0, 4)), (0.4, (34, 0, 4)), (0.8, (-40, 0, 4))])
a.bone("left_arm", rot=[(0, (34, 0, -4)), (0.4, (-40, 0, -4)), (0.8, (34, 0, -4))])
a.bone("body", rot=[(0, (9, 4, 0)), (0.4, (9, -4, 0)), (0.8, (9, 4, 0))],
       pos=[(0, (0, 0, 0)), (0.2, (0, -0.9, 0)), (0.4, (0, 0, 0)), (0.6, (0, -0.9, 0)), (0.8, (0, 0, 0))])
a.bone("head", rot=[(0, (-6, -4, 0)), (0.4, (-6, 4, 0)), (0.8, (-6, -4, 0))])
a.bone("kusazuri_front", rot=[(0, (5, 0, 0)), (0.4, (-4, 0, 0)), (0.8, (5, 0, 0))])
a.bone("kusazuri_back", rot=[(0, (-4, 0, 0)), (0.4, (5, 0, 0)), (0.8, (-4, 0, 0))])
a.bone("right_sode", rot=[(0, (4, 0, 0)), (0.4, (-3, 0, 0)), (0.8, (4, 0, 0))])
a.bone("left_sode", rot=[(0, (-3, 0, 0)), (0.4, (4, 0, 0)), (0.8, (-3, 0, 0))])

# combat_idle: bladed stance, hand resting near tsuka
a = anim("combat_idle", 2.6, True)
a.bone("body", rot=[(0, (0, -9, 0)), (1.3, (1.4, -9, 0)), (2.6, (0, -9, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (1.3, (-10, 0, 2)), (2.6, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (1.3, (12, 0, -2)), (2.6, (10, 0, -2))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (1.3, (-26, 12, -6)), (2.6, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (1.3, (-14, -6, 12)), (2.6, (-16, -6, 10))])
a.bone("head", rot=[(0, (0, 9, 0)), (1.1, (0, 12, 0)), (2.6, (0, 9, 0))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (1.3, (3.5, 0, 0)), (2.6, (2, 0, 0))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (1.3, (3, 0, 0)), (2.6, (1.5, 0, 0))])
a.bone("left_sode", rot=[(0, (1, 0, 0)), (1.3, (2.5, 0, 0)), (2.6, (1, 0, 0))])

# draw_katana: cross-grip, draw arc, rising guard
a = anim("draw_katana", 1.6, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.4, (3, -18, 0)), (0.75, (2, 14, 0)), (1.1, (0, 10, 0)), (1.6, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.4, (0, 18, 0)), (0.75, (0, -10, 0)), (1.6, (0, 9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.4, (46, -14, -26)), (0.6, (40, -10, -30)),
                          (0.78, (-96, -8, -34)), (1.05, (-112, 0, -26)), (1.6, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.4, (-44, 8, 6)), (0.62, (-38, 10, 4)),
                         (0.85, (-30, 14, 18)), (1.6, (-16, -6, 10))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (0.4, (7, 0, 0)), (0.78, (-6, 0, 0)), (1.6, (1.5, 0, 0))])
a.bone("left_sode", rot=[(0, (1, 0, 0)), (0.4, (6, 0, 0)), (0.85, (4, 0, 0)), (1.6, (1, 0, 0))])
a.bone("katana_scabbard", rot=[(0, (0, 0, 0)), (0.4, (4, 0, -4)), (0.62, (10, 0, -10)), (0.9, (0, 0, 0)), (1.6, (0, 0, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.75, (-6, 0, 4)), (1.6, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.75, (16, 0, -6)), (1.6, (10, 0, -2))])

# sheathe_katana: present, slide home, settle
a = anim("sheathe_katana", 1.5, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.45, (4, -20, 0)), (0.85, (5, -22, 0)), (1.2, (0, -9, 0)), (1.5, (0, -9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.45, (-70, 20, -10)), (0.85, (52, -8, -18)), (1.15, (44, 0, -8)), (1.5, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.45, (-52, 4, 10)), (0.85, (-46, 6, 8)), (1.5, (-16, -6, 10))])
a.bone("katana_scabbard", rot=[(0, (0, 0, 0)), (0.45, (6, 0, -6)), (1.0, (0, 0, 0)), (1.5, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.45, (0, 20, 0)), (1.2, (0, 9, 0)), (1.5, (0, 9, 0))])

# attack_horizontal
a = anim("attack_horizontal", 1.2, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.2, (4, -26, 0)), (0.42, (-3, 24, 0)), (0.58, (0, 28, 0)), (0.9, (1, 2, 0)), (1.2, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.2, (0, 14, 0)), (0.45, (0, -16, 0)), (1.2, (0, 9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.2, (-58, 30, 52)), (0.42, (-26, 6, -62)), (0.58, (-20, -4, -84)), (0.95, (-28, 10, -12)), (1.2, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.2, (-24, -10, 24)), (0.42, (-14, -12, 34)), (0.58, (-12, -14, 40)), (1.2, (-16, -6, 10))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (0.2, (9, 0, 0)), (0.42, (-7, 0, 0)), (1.2, (1.5, 0, 0))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (0.42, (7, 0, 0)), (0.7, (1, 0, 0)), (1.2, (2, 0, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.42, (-4, 0, 6)), (1.2, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.42, (20, 0, -8)), (1.2, (10, 0, -2))])

# attack_diagonal
a = anim("attack_diagonal", 1.2, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.2, (-6, -20, 0)), (0.42, (12, 18, 0)), (0.6, (10, 22, 0)), (1.2, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.2, (-8, 12, 0)), (0.45, (10, -12, 0)), (1.2, (0, 9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.2, (-142, 24, 44)), (0.42, (-38, 2, -50)), (0.6, (-30, -2, -58)), (1.2, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.2, (-120, -20, 30)), (0.45, (-20, -10, 30)), (1.2, (-16, -6, 10))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (0.2, (10, 0, 0)), (0.42, (-6, 0, 0)), (1.2, (1.5, 0, 0))])
a.bone("left_sode", rot=[(0, (1, 0, 0)), (0.2, (9, 0, 0)), (0.5, (3, 0, 0)), (1.2, (1, 0, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.42, (-2, 0, 6)), (1.2, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.42, (22, 0, -8)), (1.2, (10, 0, -2))])

# attack_overhead
a = anim("attack_overhead", 1.4, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.28, (-9, -6, 0)), (0.5, (20, -2, 0)), (0.68, (22, 0, 0)), (1.05, (2, -8, 0)), (1.4, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.28, (-10, 6, 0)), (0.52, (14, -4, 0)), (1.4, (0, 9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.28, (-158, 10, 14)), (0.5, (-24, 4, -10)), (0.68, (-18, 0, -6)), (1.4, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.28, (-150, -10, -14)), (0.5, (-20, -4, 8)), (1.4, (-16, -6, 10))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (0.28, (12, 0, 0)), (0.5, (-8, 0, 0)), (1.4, (1.5, 0, 0))])
a.bone("left_sode", rot=[(0, (1, 0, 0)), (0.28, (11, 0, 0)), (0.5, (-7, 0, 0)), (1.4, (1, 0, 0))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (0.28, (8, 0, 0)), (0.5, (-2, 0, 0)), (1.4, (2, 0, 0))])
a.bone("body_pos", ) if False else None
a.bone("master", pos=[(0, (0, 0, 0)), (0.5, (0, -1.1, 0.4)), (0.75, (0, -0.6, 0.2)), (1.4, (0, 0, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.5, (-6, 0, 8)), (1.4, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.5, (18, 0, -10)), (1.4, (10, 0, -2))])

# block: guarded cross
a = anim("block", 1.8, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.25, (6, -4, 0)), (1.3, (5, -4, 0)), (1.8, (0, -9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.25, (-78, 18, -30)), (1.3, (-76, 18, -28)), (1.8, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.25, (-74, -18, 30)), (1.3, (-72, -18, 28)), (1.8, (-16, -6, 10))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.25, (-18, 0, 4)), (1.8, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.25, (20, 0, -6)), (1.8, (10, 0, -2))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (0.25, (5, 0, 0)), (1.8, (2, 0, 0))])

# parry: short snapping counter
a = anim("parry", 0.7, False)
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.12, (-20, 8, -4)), (0.3, (-84, -6, -48)), (0.7, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.3, (-30, -14, 26)), (0.7, (-16, -6, 10))])
a.bone("body", rot=[(0, (0, -9, 0)), (0.3, (2, -16, 0)), (0.7, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.3, (0, 14, 0)), (0.7, (0, 9, 0))])

# command: fist to hip, pointing order, grounding stomp
a = anim("command", 2.2, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.3, (-3, 0, 0)), (1.0, (-3, 6, 0)), (1.7, (-3, 0, 0)), (2.2, (0, -9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.3, (-88, 0, 0)), (1.6, (-84, 0, 0)), (2.2, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.3, (-6, 0, 46)), (2.0, (-6, 0, 46)), (2.2, (-16, -6, 10))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.4, (0, 0, 0)), (1.0, (-4, -14, 0)), (1.6, (0, 10, 0)), (2.2, (0, 9, 0))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.45, (-30, 0, -4)), (0.62, (14, 0, -2)), (2.2, (10, 0, -2))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.55, (0, -0.7, 0)), (0.7, (0, 0.25, 0)), (0.9, (0, 0, 0)), (2.2, (0, 0, 0))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (0.5, (6, 0, 0)), (0.9, (1, 0, 0)), (2.2, (2, 0, 0))])

# hurt: brief heavy flinch
a = anim("hurt", 0.4, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.1, (-7, -9, 0)), (0.25, (4, -9, 0)), (0.4, (0, -9, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.1, (-9, 9, 0)), (0.4, (0, 9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.1, (-14, 14, -16)), (0.4, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.1, (-8, -10, 20)), (0.4, (-16, -6, 10))])

# long_lunge: committed iai thrust (JapaneseWarriorEntity ACTION_LONG_LUNGE, 16t)
a = anim("long_lunge", 0.8, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.2, (6, -16, 0)), (0.45, (8, 6, 0)), (0.7, (2, -4, 0)), (0.8, (0, -9, 0))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.2, (-64, 10, -22)), (0.45, (-78, 0, 6)), (0.6, (-72, 0, 4)), (0.8, (-30, 12, -8))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.2, (-58, -10, 26)), (0.45, (-44, -8, 30)), (0.8, (-16, -6, 10))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.45, (-24, 0, 8)), (0.8, (-12, 0, 2))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.45, (34, 0, -10)), (0.8, (10, 0, -2))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.2, (0, 12, 0)), (0.45, (0, -6, 0)), (0.8, (0, 9, 0))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.45, (0, -0.7, 0.3)), (0.8, (0, 0, 0))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (0.2, (8, 0, 0)), (0.45, (-5, 0, 0)), (0.8, (1.5, 0, 0))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (0.45, (6, 0, 0)), (0.8, (2, 0, 0))])

# death: stagger, buckle, collapse forward (hold last frame)
a = anim("death", 2.4, False)
a.bone("body", rot=[(0, (0, -9, 0)), (0.3, (-8, -6, 0)), (0.7, (18, 0, 0)), (1.1, (38, 4, 0)), (1.7, (52, 8, 0)), (2.4, (55, 8, 0))])
a.bone("head", rot=[(0, (0, 9, 0)), (0.3, (-6, 6, 0)), (1.1, (16, 0, 0)), (1.7, (26, -4, 0)), (2.4, (28, -4, 0))])
a.bone("right_leg", rot=[(0, (-12, 0, 2)), (0.5, (-38, 0, 6)), (1.1, (-64, 0, 10)), (2.4, (-70, 0, 12))])
a.bone("left_leg", rot=[(0, (10, 0, -2)), (0.5, (18, 0, -8)), (1.1, (-52, 0, -12)), (2.4, (-58, 0, -14))])
a.bone("right_arm", rot=[(0, (-30, 12, -8)), (0.5, (-50, 10, -20)), (1.1, (-14, 8, -26)), (2.4, (-8, 6, -30))])
a.bone("left_arm", rot=[(0, (-16, -6, 10)), (0.5, (-40, -8, 22)), (1.1, (-10, -6, 30)), (2.4, (-6, -4, 34))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.7, (0, -3.4, 0)), (1.1, (0, -8.2, 0.6)), (1.7, (0, -10.6, 1.4)), (2.4, (0, -11.0, 1.6))])
a.bone("kusazuri_front", rot=[(0, (2, 0, 0)), (1.1, (9, 0, 0)), (2.4, (11, 0, 0))])
a.bone("right_sode", rot=[(0, (1.5, 0, 0)), (1.1, (10, 0, 0)), (2.4, (12, 0, 0))])
a.bone("left_sode", rot=[(0, (1, 0, 0)), (1.1, (9, 0, 0)), (2.4, (11, 0, 0))])

# ------------------------------------------------------------------ emit
bones_json = []
for name, parent, pivot, jrot in BONES:
    cubes = [c for c in CUBES if c["bone"] == name]
    bones_json.append(bone(name, pivot, parent, jrot, cubes))

geo_path = ASSETS / "geo" / "settlement" / "red_shogun.geo.json"
emit_geo(geo_path, "geometry.red_shogun", 128, 128, bones_json, visible_bounds=(6, 6, 2.2))

tex_path = ASSETS / "textures" / "settlement" / "entity" / "red_shogun.png"
tex_path.parent.mkdir(parents=True, exist_ok=True)
tex.img.save(tex_path)

anim_path = ASSETS / "animations" / "settlement" / "red_shogun.animation.json"
emit_anims(anim_path, dict(a.entry() for a in A))

errors = validate(bones_json, dict(a.entry() for a in A), tex, CUBES)
if errors:
    print("VALIDATION ERRORS:")
    for e in errors[:40]:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(CUBES)} cubes, {len(BONES)} bones, {len(A)} animations -> {geo_path}")
