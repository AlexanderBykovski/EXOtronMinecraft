#!/usr/bin/env python3
"""Dark Ninja (`dark_ninja`) asset generator.
Deterministic: geo JSON (box UV, 128x128) + painted texture + 16 GeckoLib animations + QA.
Run from repo root: python3 scripts/gen_dark_ninja_assets.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from geokit import (ASSETS, shelf_pack, Tex, emit_geo, bone, AnimBuilder,
                    emit_anims, validate, face_rects, paint_cloth, paint_leather,
                    paint_metal)

PAL = {
    # hood / charcoal cloth (matte, near-black blue-gray)
    "hood":     (24, 26, 32, 255), "hood_hi": (36, 39, 47, 255), "hood_dk": (14, 14, 18, 255),
    # outer jacket (charcoal with indigo cast, woven)
    "jak":      (30, 32, 46, 255), "jak_hi": (44, 48, 68, 255), "jak_dk": (18, 19, 30, 255),
    # inner tunic (dark indigo)
    "tun":      (26, 28, 48, 255), "tun_hi": (40, 44, 66, 255), "tun_dk": (16, 17, 30, 255),
    # quilted reinforced panels (muted slate, crosshatch)
    "quil":     (62, 68, 84, 255), "quil_hi": (80, 88, 106, 255), "quil_dk": (42, 46, 58, 255),
    # trouser (charcoal)
    "tr":       (22, 23, 28, 255), "tr_hi": (34, 36, 44, 255), "tr_dk": (13, 13, 17, 255),
    # wraps (forearm/calf)
    "wr":       (30, 31, 37, 255), "wr_hi": (46, 48, 57, 255), "wr_dk": (17, 17, 21, 255),
    # leather
    "lea":      (62, 42, 26, 255), "lea_hi": (87, 60, 38, 255), "lea_dk": (40, 26, 16, 255),
    # dull iron
    "iron":     (74, 78, 86, 255), "iron_hi": (94, 100, 110, 255), "iron_dk": (50, 54, 60, 255),
    # skin / eyes
    "skin":     (196, 150, 112, 255), "skin_sh": (168, 126, 92, 255),
    "eye_w":    (238, 234, 226, 255), "eye": (42, 26, 16, 255),
    # steel / blade
    "steel":    (154, 160, 168, 255), "steel_hi": (200, 205, 212, 255), "steel_dk": (106, 112, 120, 255),
    # scabbard matte black
    "blk":      (22, 22, 24, 255), "blk_hi": (44, 44, 48, 255),
    # rope
    "rope":     (107, 76, 46, 255), "rope_hi": (133, 98, 60, 255), "rope_dk": (74, 51, 30, 255),
}

BONES, CUBES = [], []

def C(bone_name, name, origin, size, paint, inflate=0, jrot=None, cpivot=None):
    CUBES.append(dict(bone=bone_name, name=name, origin=list(origin),
                      size=tuple(size), paint=paint, inflate=inflate, jrot=jrot, cpivot=cpivot))

def B(name, parent, pivot, jrot=None):
    BONES.append((name, parent, pivot, jrot or (0, 0, 0)))

# body -------------------------------------------------------------------
B("root", None, (0, 0, 0))
B("master", "root", (0, 12, 0))
B("body", "master", (0, 12, 0))
C("body", "inner_tunic", (-4.0, 12, -2.25), (8, 11, 4.5), "tunic")
C("body", "outer_jacket", (-4.25, 14.4, -2.5), (8.5, 8.6, 5.0), "jacket", 0.05)
B("shoulder_padding", "body", (0, 21.5, 0))
C("shoulder_padding", "shoulder_pad_left", (4.3, 20.6, -2.4), (1.7, 2.7, 4.8), "quilt")
C("shoulder_padding", "shoulder_pad_right", (-6.0, 20.6, -2.4), (1.7, 2.7, 4.8), "quilt")
B("waist_belt", "body", (0, 14.2, 0))
C("waist_belt", "belt", (-4.35, 13.4, -2.4), (8.7, 1.6, 4.8), "belt")
B("hip_cloth_front", "body", (0, 13.4, -2.0), (5, 0, 0))
C("hip_cloth_front", "hip_front", (-3.6, 10.6, -2.75), (7.2, 2.6, 0.7), "hip")
B("hip_cloth_back", "body", (0, 13.4, 2.0), (-5, 0, 0))
C("hip_cloth_back", "hip_back", (-3.6, 10.2, 1.75), (7.2, 3.0, 0.7), "hip")

# head -------------------------------------------------------------------
B("head", "master", (0, 23, 0))
C("head", "face", (-4, 23, -4), (8, 8, 8), "face")
B("inner_cap", "head", (0, 27, 0))
C("inner_cap", "inner_cap", (-4.2, 27.2, -4.2), (8.4, 3.8, 8.4), "hood")
B("hood", "head", (0, 27, 0))
C("hood", "hood", (-4.45, 24.4, -4.45), (8.9, 6.6, 8.9), "hood")
B("face_mask", "head", (0, 24.5, -4))
C("face_mask", "face_mask", (-4.3, 23.2, -4.65), (8.6, 2.6, 0.6), "mask")
B("neck_wrap", "head", (0, 22.9, 0))
C("neck_wrap", "neck_wrap", (-3.9, 22.2, -3.9), (7.8, 1.4, 7.8), "hood")

# arms -------------------------------------------------------------------
for s, sx in (("right", -1), ("left", 1)):
    B(f"{s}_arm", "master", (6.3 * sx, 21.9, 0))
    C(f"{s}_arm", f"{s}_sleeve", (4.5 * sx if sx > 0 else -8.1, 10.0, -1.8), (3.6, 11.9, 3.6), "sleeve")
    B(f"{s}_forearm_wrap", f"{s}_arm", (6.3 * sx, 21.9, 0))
    C(f"{s}_forearm_wrap", f"{s}_bracer", (4.3 * sx, 12.6, -2.0), (4.0, 4.2, 4.0), "wrap")

# legs -------------------------------------------------------------------
for s, sx in (("right", -1), ("left", 1)):
    B(f"{s}_leg", "master", (2.2 * sx, 12, 0))
    C(f"{s}_leg", f"{s}_trouser", (0.2 * sx if sx > 0 else -4.0, 0, -1.8), (3.6, 12, 3.6), "trouser")
    B(f"{s}_calf_wrap", f"{s}_leg", (2.2 * sx, 6, 0))
    C(f"{s}_calf_wrap", f"{s}_calf", (0.25 * sx, 1.6, -1.95), (3.9, 4.4, 3.9), "wrap")
    B(f"{s}_foot", f"{s}_leg", (2.2 * sx, 1.4, 0))
    C(f"{s}_foot", f"{s}_tabi", (0.25 * sx, 0, -3.0), (3.9, 1.4, 4.6), "tabi")

# equipment ---------------------------------------------------------------
B("equipment", "master", (0, 12, 0))
B("short_sword_scabbard", "equipment", (-3.4, 17.0, 2.7), (0, 0, 36))
C("short_sword_scabbard", "ninja_saya", (-4.25, 8.4, 2.6), (1.7, 9.6, 1.7), "saya")
B("short_sword_handle", "short_sword_scabbard", (-3.4, 17.9, 2.7), (0, 0, 0))
C("short_sword_handle", "ninja_tsuka", (-4.15, 17.8, 2.65), (1.5, 3.0, 1.5), "tsuka")
B("kunai_right", "equipment", (-4.1, 14.8, -2.8), (0, 0, -10))
C("kunai_right", "kunai_sheath_r", (-4.7, 12.6, -3.4), (1.2, 4.2, 0.8), "kunai")
B("kunai_left", "equipment", (-2.7, 14.8, -2.8), (0, 0, 10))
C("kunai_left", "kunai_sheath_l", (-3.3, 12.6, -3.4), (1.2, 4.2, 0.8), "kunai")
B("rope", "equipment", (5.4, 14.4, 2.2), (0, 0, -12))
C("rope", "rope_coil", (4.6, 13.3, 1.95), (1.6, 2.0, 0.5), "rope")
B("pouch_left", "equipment", (5.4, 12.1, 2.2), (0, 0, 6))
C("pouch_left", "pouch_l", (4.6, 11.0, 1.95), (1.6, 2.2, 0.55), "pouch")
B("pouch_right", "equipment", (-5.5, 12.9, 2.2), (0, 0, -6))
C("pouch_right", "pouch_r", (-6.3, 11.8, 1.95), (1.6, 2.2, 0.55), "pouch")

shelf_pack(CUBES, atlas=128, pad=1)

# ------------------------------------------------------------------ texture
tex = Tex(128, PAL)

def woven(r, base, hi, dk):
    """Rough woven cloth: subtle column pattern + darker warp rows."""
    x, y, w, h = r
    tex.rect(r, base)
    for i in range(w):
        m = i % 4
        for j in range(h):
            col = hi if m == 0 else (dk if m == 2 and j % 3 == 0 else base)
            tex.set(x + i, y + j, col)
    for j in range(h - 1, y, -3):
        for i in range(x, x + w):
            if (i + j) % 5 == 0:
                tex.set(i, j, dk)

def quilt(r):
    """Crosshatched quilted panel."""
    x, y, w, h = r
    tex.rect(r, PAL["quil"])
    for j in range(h):
        for i in range(w):
            if (i + j) % 4 == 0 or (i - j) % 4 == 0:
                tex.set(x + i, y + j, PAL["quil_dk"])
    for i in range(x, x + w, 4):
        tex.set(i, y, PAL["quil_hi"])

def wraps(r):
    """Cloth wrap bands."""
    x, y, w, h = r
    tex.rect(r, PAL["wr"])
    for j in range(1, h - 1, 2):
        for i in range(w):
            tex.set(x + i, y + j, PAL["wr_dk"] if j % 4 == 1 else PAL["wr_hi"])

def paint(cube):
    u, v = cube["tex"]
    w, h, d = cube["size"]
    R = face_rects(u, v, w, h, d)
    name, kind = cube["name"], cube["paint"]
    n = R["north"]
    if kind == "tunic":
        for f in ("north", "south", "east", "west"):
            paint_cloth(tex, R[f], PAL["tun"], PAL["tun_hi"], PAL["tun_dk"])
        tex.rect(R["up"], PAL["tun_dk"]); tex.rect(R["down"], PAL["tun_dk"])
    elif kind == "jacket":
        for f in ("north", "south", "east", "west"):
            woven(R[f], PAL["jak"], PAL["jak_hi"], PAL["jak_dk"])
        x, y, fw, fh = n                          # overlapping V closure
        for j in range(fh):
            tex.set(x + fw // 2 - 1 + (j // 3) % 2, y + j, PAL["jak_dk"])
        tex.rect((x + fw // 2 - 2, y, 1, fh), PAL["jak_hi"])
        tex.rect(R["up"], PAL["jak_dk"]); tex.rect(R["down"], PAL["jak_dk"])
    elif kind == "quilt":
        for f in ("north", "south", "east", "west", "up", "down"):
            quilt(R[f])
    elif kind == "belt":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_leather(tex, R[f], PAL["lea"], PAL["lea_hi"], PAL["lea_dk"])
        x, y, fw, fh = n
        for i in range(2, fw - 2, 3):
            tex.set(x + i, y + fh // 2, PAL["iron_dk"])   # worn buckle studs
    elif kind == "hip":
        for f in ("north", "south", "east", "west", "up", "down"):
            woven(R[f], PAL["jak"], PAL["jak_hi"], PAL["jak_dk"])
        x, y, fw, fh = n                          # split cloth tails
        tex.rect((x + fw // 2 - 1, y, 2, fh), PAL["tr_dk"])
        tex.rect((x, y + fh - 1, fw, 1), PAL["jak_dk"])
    elif kind == "hood":
        for f in ("up", "down"):
            tex.rect(R[f], PAL["hood_dk"])
        for f in ("east", "west", "south"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["hood"])
            for j in range(2, fh, 3):             # slight asymmetrical folds
                tex.rect((x + (1 if f == "west" else 0), y + j, fw - 1, 1), PAL["hood_dk"])
            tex.set(x + 1, y + 1, PAL["hood_hi"])
        x, y, fw, fh = n
        tex.rect(n, PAL["hood"])                  # eye slit: narrow skin band + eyes
        slit_y = y + fh // 2 - 1
        tex.rect((x, slit_y, fw, 2), PAL["skin"])
        tex.rect((x, slit_y, 1, 2), PAL["hood_dk"])
        tex.rect((x + fw - 1, slit_y, 1, 2), PAL["hood_dk"])
        tex.set(x + 2, slit_y, PAL["eye_w"]); tex.set(x + 3, slit_y, PAL["eye"])
        tex.set(x + fw - 3, slit_y, PAL["eye_w"]); tex.set(x + fw - 2, slit_y, PAL["eye"])
        tex.rect((x + 2, slit_y + 1, fw - 4, 1), PAL["skin_sh"])
        for i in range(1, fw - 1, 3):             # hood folds above slit
            tex.set(x + i, y + 1, PAL["hood_dk"])
    elif kind == "mask":
        for f in ("north", "south", "east", "west", "up", "down"):
            tex.rect(R[f], PAL["hood"])
        x, y, fw, fh = n
        tex.border(n, PAL["hood_dk"])
        for i in range(2, fw - 2, 2):             # breathing weave
            tex.set(x + i, y + fh - 2, PAL["hood_hi"])
    elif kind == "face":
        for f in ("up", "down", "east", "west", "south"):
            tex.rect(R[f], PAL["skin"])
        x, y, fw, fh = n
        tex.rect(n, PAL["skin"])                  # hidden under hood except slit
        for ex in (2, 5):
            tex.set(x + ex, y + 4, PAL["eye_w"]); tex.set(x + ex + 1, y + 4, PAL["eye"])
        for i in range(fw):
            tex.set(x + i, y + 5, PAL["skin_sh"])
    elif kind == "sleeve":
        for f in ("north", "south", "east", "west"):
            woven(R[f], PAL["jak"], PAL["jak_hi"], PAL["jak_dk"])
            x, y, fw, fh = R[f]                   # exposed fingertips
            tex.rect((x, y + fh - 2, fw, 2), PAL["skin"])
            tex.rect((x, y + fh - 1, fw, 1), PAL["skin_sh"])
        tex.rect(R["up"], PAL["jak_dk"]); tex.rect(R["down"], PAL["jak_dk"])
    elif kind == "trouser":
        for f in ("north", "south", "east", "west"):
            paint_cloth(tex, R[f], PAL["tr"], PAL["tr_hi"], PAL["tr_dk"], fold_step=5)
        tex.rect(R["up"], PAL["tr_dk"]); tex.rect(R["down"], PAL["tr_dk"])
    elif kind == "wrap":
        for f in ("north", "south", "east", "west", "up", "down"):
            wraps(R[f])
    elif kind == "tabi":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["blk"])
            tex.rect((x, y, fw, 1), PAL["lea"])   # sole binding
        tex.rect(R["up"], PAL["hood"]); tex.rect(R["down"], PAL["lea_dk"])
    elif kind == "saya":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["blk"])
            tex.rect((x, y, fw, 1), PAL["blk_hi"])
            tex.rect((x, y + fh - 2, fw, 2), PAL["iron_dk"])
        tex.rect(R["up"], PAL["iron"]); tex.rect(R["down"], PAL["blk"])
    elif kind == "iron":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_metal(tex, R[f], PAL["iron"], PAL["iron_hi"], PAL["iron_dk"])
    elif kind == "blade":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            paint_metal(tex, R[f], PAL["steel"], PAL["steel_hi"], PAL["steel_dk"])
            tex.set(x + fw - 1, y, PAL["steel_hi"])
        tex.rect(R["up"], PAL["steel_hi"]); tex.rect(R["down"], PAL["steel_dk"])
    elif kind == "tsuka":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["blk"])
            for j in range(fh):
                for i in range(fw):
                    if (i + j) % 2 == 0:
                        tex.set(x + i, y + j, PAL["lea_dk"])
        tex.rect(R["up"], PAL["blk_hi"]); tex.rect(R["down"], PAL["iron_dk"])
    elif kind == "kunai":
        for f in ("north", "south", "east", "west"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["iron_dk"])
            tex.rect((x, y, fw, 1), PAL["iron"])  # blade tip peeks from sheath
            tex.set(x + fw // 2, y, PAL["steel_hi"])
        tex.rect(R["up"], PAL["blk"]); tex.rect(R["down"], PAL["lea_dk"])
    elif kind == "rope":
        for f in ("north", "south", "east", "west", "up", "down"):
            x, y, fw, fh = R[f]
            tex.rect(R[f], PAL["rope"])
            for j in range(0, fh, 2):
                tex.rect((x, y + j, fw, 1), PAL["rope_dk"])
            tex.set(x, y, PAL["rope_hi"])
    elif kind == "pouch":
        for f in ("north", "south", "east", "west", "up", "down"):
            paint_leather(tex, R[f], PAL["lea_dk"], PAL["lea"], PAL["blk"])
        x, y, fw, fh = n
        tex.rect((x + fw // 2 - 1, y + 1, 2, fh - 2), PAL["blk"])  # flap seam
        tex.set(x + fw // 2, y + fh - 2, PAL["iron_dk"])

for c in CUBES:
    paint(c)

# ------------------------------------------------------------------ animations
A = []

def anim(name, length, loop):
    a = AnimBuilder(f"animation.dark_ninja.{name}", length, loop)
    A.append(a)
    return a

CROUCH = -3.4

# idle: low-profile breathing, subtle scan
a = anim("idle", 3.2, True)
a.bone("body", rot=[(0, (0, 0, 0)), (1.6, (1.8, 0, 0)), (3.2, (0, 0, 0))],
       pos=[(0, (0, 0, 0)), (1.6, (0, -0.3, 0)), (3.2, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 3, 0)), (1.2, (0, -3, 0)), (2.2, (0, 1, 0)), (3.2, (0, 3, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (1.6, (1, 0, 4)), (3.2, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (1.6, (1, 0, -4)), (3.2, (0, 0, -3))])
a.bone("hip_cloth_back", rot=[(0, (0, 0, 0)), (1.6, (-2.5, 0, 0)), (3.2, (0, 0, 0))])

# crouch_idle
a = anim("crouch_idle", 2.8, True)
a.bone("master", pos=[(0, (0, CROUCH, 0)), (1.4, (0, CROUCH - 0.25, 0)), (2.8, (0, CROUCH, 0))])
a.bone("body", rot=[(0, (12, 0, 0)), (1.4, (13.5, 0, 0)), (2.8, (12, 0, 0))])
a.bone("head", rot=[(0, (-10, 4, 0)), (1.2, (-10, -4, 0)), (2.8, (-10, 4, 0))])
a.bone("right_leg", rot=[(0, (-30, 0, 4)), (2.8, (-30, 0, 4))])
a.bone("left_leg", rot=[(0, (30, 0, -4)), (2.8, (30, 0, -4))])
a.bone("right_calf_wrap", rot=[(0, (26, 0, 0)), (2.8, (26, 0, 0))])
a.bone("left_calf_wrap", rot=[(0, (-26, 0, 0)), (2.8, (-26, 0, 0))])
a.bone("right_arm", rot=[(0, (-16, 0, 5)), (1.4, (-14, 0, 6)), (2.8, (-16, 0, 5))])
a.bone("left_arm", rot=[(0, (-16, 0, -5)), (1.4, (-14, 0, -6)), (2.8, (-16, 0, -5))])
a.bone("hip_cloth_back", rot=[(0, (-6, 0, 0)), (1.4, (-8, 0, 0)), (2.8, (-6, 0, 0))])

# walk: quiet steps, minimal arm swing
a = anim("walk", 1.0, True)
a.bone("right_leg", rot=[(0, (30, 0, 0)), (0.25, (3, 0, 0)), (0.5, (-24, 0, 0)), (0.75, (-3, 0, 0)), (1.0, (30, 0, 0))])
a.bone("left_leg", rot=[(0, (-24, 0, 0)), (0.25, (-3, 0, 0)), (0.5, (30, 0, 0)), (0.75, (3, 0, 0)), (1.0, (-24, 0, 0))])
a.bone("right_arm", rot=[(0, (-14, 0, 4)), (0.5, (10, 0, 4)), (1.0, (-14, 0, 4))])
a.bone("left_arm", rot=[(0, (10, 0, -4)), (0.5, (-14, 0, -4)), (1.0, (10, 0, -4))])
a.bone("body", rot=[(0, (2, 3, 0)), (0.5, (2, -3, 0)), (1.0, (2, 3, 0))],
       pos=[(0, (0, 0, 0)), (0.25, (0, -0.4, 0)), (0.5, (0, 0, 0)), (0.75, (0, -0.4, 0)), (1.0, (0, 0, 0))])
a.bone("head", rot=[(0, (-2, -3, 0)), (0.5, (-2, 3, 0)), (1.0, (-2, -3, 0))])
a.bone("right_calf_wrap", rot=[(0, (-8, 0, 0)), (0.5, (6, 0, 0)), (1.0, (-8, 0, 0))])
a.bone("left_calf_wrap", rot=[(0, (6, 0, 0)), (0.5, (-8, 0, 0)), (1.0, (6, 0, 0))])
a.bone("hip_cloth_front", rot=[(0, (-2, 0, 0)), (0.5, (2, 0, 0)), (1.0, (-2, 0, 0))])
a.bone("hip_cloth_back", rot=[(0, (2, 0, 0)), (0.5, (-2, 0, 0)), (1.0, (2, 0, 0))])

# crouch_walk: stalking shuffle
a = anim("crouch_walk", 1.25, True)
a.bone("master", pos=[(0, (0, CROUCH, 0)), (0.3, (0, CROUCH - 0.3, 0)), (0.625, (0, CROUCH, 0)),
                      (0.95, (0, CROUCH - 0.3, 0)), (1.25, (0, CROUCH, 0))])
a.bone("body", rot=[(0, (12, 4, 0)), (0.625, (12, -4, 0)), (1.25, (12, 4, 0))])
a.bone("head", rot=[(0, (-10, -5, 0)), (0.625, (-10, 5, 0)), (1.25, (-10, -5, 0))])
a.bone("right_leg", rot=[(0, (-28, 0, 4)), (0.625, (-34, 0, 4)), (1.25, (-28, 0, 4))])
a.bone("left_leg", rot=[(0, (18, 0, -4)), (0.625, (26, 0, -4)), (1.25, (18, 0, -4))])
a.bone("right_calf_wrap", rot=[(0, (24, 0, 0)), (0.625, (30, 0, 0)), (1.25, (24, 0, 0))])
a.bone("left_calf_wrap", rot=[(0, (-16, 0, 0)), (0.625, (-22, 0, 0)), (1.25, (-16, 0, 0))])
a.bone("right_arm", rot=[(0, (-18, 0, 6)), (0.625, (-14, 0, 6)), (1.25, (-18, 0, 6))])
a.bone("left_arm", rot=[(0, (-14, 0, -6)), (0.625, (-18, 0, -6)), (1.25, (-14, 0, -6))])

# run: fast, low, committed
a = anim("run", 0.65, True)
a.bone("right_leg", rot=[(0, (44, 0, 0)), (0.16, (6, 0, 0)), (0.325, (-36, 0, 0)), (0.49, (-6, 0, 0)), (0.65, (44, 0, 0))])
a.bone("left_leg", rot=[(0, (-36, 0, 0)), (0.16, (-6, 0, 0)), (0.325, (44, 0, 0)), (0.49, (6, 0, 0)), (0.65, (-36, 0, 0))])
a.bone("right_arm", rot=[(0, (-34, 0, 5)), (0.325, (26, 0, 5)), (0.65, (-34, 0, 5))])
a.bone("left_arm", rot=[(0, (26, 0, -5)), (0.325, (-34, 0, -5)), (0.65, (26, 0, -5))])
a.bone("body", rot=[(0, (14, 4, 0)), (0.325, (14, -4, 0)), (0.65, (14, 4, 0))],
       pos=[(0, (0, 0, 0)), (0.16, (0, -0.7, 0)), (0.325, (0, 0, 0)), (0.49, (0, -0.7, 0)), (0.65, (0, 0, 0))])
a.bone("head", rot=[(0, (-10, -4, 0)), (0.325, (-10, 4, 0)), (0.65, (-10, -4, 0))])
a.bone("right_calf_wrap", rot=[(0, (-12, 0, 0)), (0.325, (10, 0, 0)), (0.65, (-12, 0, 0))])
a.bone("left_calf_wrap", rot=[(0, (10, 0, 0)), (0.325, (-12, 0, 0)), (0.65, (10, 0, 0))])
a.bone("hip_cloth_back", rot=[(0, (4, 0, 0)), (0.325, (-3, 0, 0)), (0.65, (4, 0, 0))])

# draw_sword: hand blurs to lower back, blade out
a = anim("draw_sword", 0.9, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.25, (4, -10, 0)), (0.55, (2, 6, 0)), (0.9, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.25, (52, 26, -8)), (0.5, (44, 20, -6)), (0.68, (-92, 0, -10)), (0.9, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.25, (-30, -6, 12)), (0.9, (0, 0, -3))])
a.bone("short_sword_scabbard", rot=[(0, (0, 0, 0)), (0.3, (6, 0, 8)), (0.6, (0, 0, 0)), (0.9, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.3, (0, 10, 0)), (0.9, (0, 0, 0))])

# sheathe_sword
a = anim("sheathe_sword", 1.0, False)
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.3, (46, 22, -8)), (0.7, (40, 18, -6)), (1.0, (0, 0, 3))])
a.bone("short_sword_scabbard", rot=[(0, (0, 0, 0)), (0.35, (5, 0, 7)), (0.75, (0, 0, 0)), (1.0, (0, 0, 0))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.35, (4, -12, 0)), (1.0, (0, 0, 0))])

# attack_fast: straight snap cut
a = anim("attack_fast", 0.8, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.15, (2, -16, 0)), (0.35, (-2, 14, 0)), (0.5, (0, 16, 0)), (0.8, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.15, (-38, 18, 34)), (0.35, (-24, 0, -46)), (0.5, (-20, -2, -56)), (0.8, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.15, (-12, -8, 18)), (0.35, (-8, -10, 26)), (0.8, (0, 0, -3))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.15, (0, 10, 0)), (0.4, (0, -12, 0)), (0.8, (0, 0, 0))])
a.bone("right_leg", rot=[(0, (0, 0, 0)), (0.35, (-6, 0, 4)), (0.8, (0, 0, 0))])
a.bone("left_leg", rot=[(0, (0, 0, 0)), (0.35, (12, 0, -6)), (0.8, (0, 0, 0))])

# attack_diagonal: rising slash
a = anim("attack_diagonal", 0.9, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.18, (6, -14, 0)), (0.4, (-8, 12, 0)), (0.55, (-6, 14, 0)), (0.9, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.18, (34, 16, 40)), (0.4, (-128, 4, -30)), (0.55, (-120, 0, -34)), (0.9, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.18, (26, -10, 22)), (0.45, (-30, -8, 20)), (0.9, (0, 0, -3))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.18, (6, 8, 0)), (0.45, (-8, -10, 0)), (0.9, (0, 0, 0))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.4, (0, -0.5, 0)), (0.9, (0, 0, 0))])

# stab: compact thrust
a = anim("stab", 0.8, False)
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.18, (-30, 10, -6)), (0.35, (-88, 0, 0)), (0.5, (-92, 0, 0)), (0.8, (0, 0, 3))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.18, (4, 8, 0)), (0.35, (-4, -6, 0)), (0.8, (0, 0, 0))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.18, (-20, -8, 16)), (0.35, (-34, -12, 24)), (0.8, (0, 0, -3))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.35, (0, -0.4, 0.3)), (0.55, (0, -0.3, 0.2)), (0.8, (0, 0, 0))])

# throw_kunai: wind-up, whip, follow-through
a = anim("throw_kunai", 0.9, False)
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.22, (-118, 14, 26)), (0.45, (-96, 0, -6)), (0.62, (-40, 0, -14)), (0.9, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.22, (-16, -6, 20)), (0.45, (-26, -10, 30)), (0.9, (0, 0, -3))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.22, (2, -14, 0)), (0.45, (-3, 10, 0)), (0.9, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.22, (0, 10, 0)), (0.5, (0, -6, 0)), (0.9, (0, 0, 0))])

# block: crossed bracers
a = anim("block", 1.2, False)
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.2, (-76, 16, -26)), (1.0, (-74, 16, -26)), (1.2, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.2, (-72, -16, 26)), (1.0, (-70, -16, 26)), (1.2, (0, 0, -3))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.2, (6, -4, 0)), (1.2, (0, 0, 0))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.2, (0, -0.6, 0)), (1.2, (0, 0, 0))])

# dodge_left / dodge_right: low lateral hops
a = anim("dodge_left", 0.6, False)
a.bone("master", pos=[(0, (0, 0, 0)), (0.25, (2.4, -0.9, 0)), (0.6, (0, 0, 0))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.25, (10, 12, 0)), (0.6, (0, 0, 0))])
a.bone("right_leg", rot=[(0, (0, 0, 0)), (0.25, (26, 0, 8)), (0.6, (0, 0, 0))])
a.bone("left_leg", rot=[(0, (0, 0, 0)), (0.25, (-18, 0, -10)), (0.6, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.25, (-20, 0, 14)), (0.6, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.25, (-24, 0, -20)), (0.6, (0, 0, -3))])
a = anim("dodge_right", 0.6, False)
a.bone("master", pos=[(0, (0, 0, 0)), (0.25, (-2.4, -0.9, 0)), (0.6, (0, 0, 0))])
a.bone("body", rot=[(0, (0, 0, 0)), (0.25, (10, -12, 0)), (0.6, (0, 0, 0))])
a.bone("right_leg", rot=[(0, (0, 0, 0)), (0.25, (-18, 0, 10)), (0.6, (0, 0, 0))])
a.bone("left_leg", rot=[(0, (0, 0, 0)), (0.25, (26, 0, -8)), (0.6, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.25, (-24, 0, 20)), (0.6, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.25, (-20, 0, -14)), (0.6, (0, 0, -3))])

# smoke_step: low dash pose (JapaneseWarriorEntity ACTION_SMOKE_STEP, 12t)
a = anim("smoke_step", 0.6, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.15, (12, -10, 0)), (0.4, (10, 8, 0)), (0.6, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.15, (-12, 6, 0)), (0.4, (-8, -6, 0)), (0.6, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.15, (-36, 10, 18)), (0.4, (-20, -6, -10)), (0.6, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.15, (-28, -10, -22)), (0.4, (-14, 6, 14)), (0.6, (0, 0, -3))])
a.bone("right_leg", rot=[(0, (0, 0, 0)), (0.15, (-34, 0, 6)), (0.4, (26, 0, -4)), (0.6, (0, 0, 0))])
a.bone("left_leg", rot=[(0, (0, 0, 0)), (0.15, (20, 0, -6)), (0.4, (-18, 0, 4)), (0.6, (0, 0, 0))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.15, (0, -0.8, 0)), (0.4, (0, -0.4, 0)), (0.6, (0, 0, 0))])
a.bone("hip_cloth_back", rot=[(0, (0, 0, 0)), (0.15, (10, 0, 0)), (0.6, (0, 0, 0))])

# hurt
a = anim("hurt", 0.35, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.08, (-8, 0, 0)), (0.22, (5, 0, 0)), (0.35, (0, 0, 0))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.08, (-10, 0, 0)), (0.35, (0, 0, 0))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.08, (-16, 0, 16)), (0.35, (0, 0, 3))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.08, (-16, 0, -16)), (0.35, (0, 0, -3))])

# death: sink, roll to knee, fall
a = anim("death", 1.8, False)
a.bone("body", rot=[(0, (0, 0, 0)), (0.3, (-8, 4, 0)), (0.7, (22, 0, 0)), (1.1, (46, -6, 0)), (1.8, (52, -6, 0))])
a.bone("head", rot=[(0, (0, 0, 0)), (0.3, (-8, 0, 0)), (1.1, (22, 8, 0)), (1.8, (26, 8, 0))])
a.bone("right_leg", rot=[(0, (0, 0, 0)), (0.5, (-44, 0, 8)), (1.1, (-70, 0, 12)), (1.8, (-74, 0, 14))])
a.bone("left_leg", rot=[(0, (0, 0, 0)), (0.5, (16, 0, -8)), (1.1, (-56, 0, -14)), (1.8, (-60, 0, -16))])
a.bone("right_arm", rot=[(0, (0, 0, 3)), (0.5, (-40, 8, -18)), (1.1, (-10, 6, -28)), (1.8, (-6, 4, -32))])
a.bone("left_arm", rot=[(0, (0, 0, -3)), (0.5, (-34, -8, 20)), (1.1, (-8, -6, 30)), (1.8, (-5, -4, 34))])
a.bone("master", pos=[(0, (0, 0, 0)), (0.7, (0, -4.0, 0)), (1.1, (0, -8.6, 0.5)), (1.8, (0, -9.4, 1.1))])

# ------------------------------------------------------------------ emit
bones_json = [bone(n, p, par, jr, [c for c in CUBES if c["bone"] == n]) for n, par, p, jr in BONES]

geo_path = ASSETS / "geo" / "settlement" / "dark_ninja.geo.json"
emit_geo(geo_path, "geometry.dark_ninja", 128, 128, bones_json, visible_bounds=(5, 5, 2.0))

tex_path = ASSETS / "textures" / "settlement" / "entity" / "dark_ninja.png"
tex_path.parent.mkdir(parents=True, exist_ok=True)
tex.img.save(tex_path)

anim_path = ASSETS / "animations" / "settlement" / "dark_ninja.animation.json"
emit_anims(anim_path, dict(a.entry() for a in A))

errors = validate(bones_json, dict(a.entry() for a in A), tex, CUBES)
if errors:
    print("VALIDATION ERRORS:")
    for e in errors[:40]:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(CUBES)} cubes, {len(BONES)} bones, {len(A)} animations -> {geo_path}")
