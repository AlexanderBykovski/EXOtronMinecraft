#!/usr/bin/env python3
"""Fire Demonic armor asset generator.
Deterministic: helmet/plate base + emissive atlases (128x128, identical UV layout),
4 item icons, and the Java CubeListBuilder snippets for both client models.
Run from repo root: python3 scripts/gen_fire_demonic_armor_assets.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from geokit import ASSETS, shelf_pack, Tex, face_rects, paint_metal, paint_leather

PAL = {
    # blackened volcanic metal
    "iron":    (26, 26, 28, 255), "iron_hi": (51, 51, 58, 255), "iron_dk": (14, 14, 16, 255),
    # volcanic charcoal
    "char":    (20, 20, 20, 255), "char_hi": (34, 34, 38, 255),
    # deep blood-red / crimson plates
    "red":     (92, 22, 22, 255), "red_hi": (148, 38, 30, 255), "red_dk": (63, 14, 14, 255),
    # ash gray / soot
    "ash":     (74, 74, 80, 255), "ash_hi": (90, 90, 98, 255), "soot": (14, 14, 16, 255),
    # dark steel border
    "steel":   (58, 62, 70, 255), "steel_hi": (82, 88, 98, 255), "steel_dk": (38, 41, 47, 255),
    # ember ramp (dark red-orange -> white core)
    "e1":      (58, 10, 10, 255), "e2": (110, 26, 8, 255), "e3": (179, 62, 8, 255),
    "e4":      (232, 118, 20, 255), "e5": (255, 185, 62, 255), "e6": (255, 245, 200, 255),
}

HELMET = []
PLATE = []

def HC(bone, name, origin, size, paint, inflate=0, emissive=None):
    HELMET.append(dict(bone=bone, name=name, origin=tuple(origin), size=tuple(size),
                       paint=paint, inflate=inflate, emissive=emissive))

def PC(bone, name, origin, size, paint, inflate=0, emissive=None):
    PLATE.append(dict(bone=bone, name=name, origin=tuple(origin), size=tuple(size),
                      paint=paint, inflate=inflate, emissive=emissive))

# ------------------------------------------------------------------ helmet
# head-local coords (vanilla head: -4..4, -8..0, -4..4)
HC("head", "helm_base",   (-4.5, -8.6, -4.5), (9, 9, 9), "helm", 0.55)
HC("head", "faceplate",   (-4.3, -6.9, -5.4), (8.6, 5.8, 1.2), "faceplate", 0.05,
   emissive="visor_slit")
HC("head", "visor",       (-2.9, -5.3, -5.75), (5.8, 1.2, 0.5), "visor", 0.05,
   emissive="visor")
HC("head", "jaw_guard",   (-3.4, -1.9, -4.9), (6.8, 3.3, 1.4), "plate", 0.05)
HC("head", "cheek_left",  (3.5, -4.8, -4.6), (1.5, 4.6, 3.2), "plate", 0.05)
HC("head", "cheek_right", (-5.0, -4.8, -4.6), (1.5, 4.6, 3.2), "plate", 0.05)
HC("head", "neck_guard",  (-4.0, -3.4, 3.2), (8.0, 4.2, 1.5), "plate", 0.05)
HC("head", "crown_ridge", (-0.7, -10.0, -5.0), (1.4, 1.7, 10.0), "ridge", 0.05)
HC("horn_right_root", "horn_r_root", (-1.3, -1.1, -1.3), (2.6, 2.2, 2.6), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_right_01", "horn_r_01", (-1.1, -3.4, -1.1), (2.2, 3.4, 2.2), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_right_02", "horn_r_02", (-0.9, -3.0, -0.9), (1.8, 3.0, 1.8), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_right_03", "horn_r_03", (-0.7, -2.8, -0.7), (1.4, 2.8, 1.4), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_right_tip", "horn_r_tip", (-0.5, -2.4, -0.5), (1.0, 2.4, 1.0), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_left_root", "horn_l_root", (-1.3, -1.1, -1.3), (2.6, 2.2, 2.6), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_left_01", "horn_l_01", (-1.1, -3.4, -1.1), (2.2, 3.4, 2.2), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_left_02", "horn_l_02", (-0.9, -3.0, -0.9), (1.8, 3.0, 1.8), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_left_03", "horn_l_03", (-0.7, -2.8, -0.7), (1.4, 2.8, 1.4), "horn", 0.05,
   emissive="horn_cracks")
HC("horn_left_tip", "horn_l_tip", (-0.5, -2.4, -0.5), (1.0, 2.4, 1.0), "horn", 0.05,
   emissive="horn_cracks")

# ------------------------------------------------------------------ plate
# vanilla part-local coords
PC("body", "chest_core",   (-2.6, 3.2, -3.0), (5.2, 5.6, 1.1), "core", 0.05, emissive="core_seam")
PC("body", "plate_upper",  (-4.4, 1.2, -2.9), (8.8, 3.4, 6.0), "plate_v")
PC("body", "plate_middle", (-4.3, 4.2, -2.85), (8.6, 3.2, 5.8), "plate_v")
PC("body", "plate_lower",  (-4.2, 7.0, -2.8), (8.4, 3.6, 5.6), "abdomen")
PC("body", "rib_left",     (3.9, 3.0, -2.4), (1.2, 5.4, 4.4), "rib")
PC("body", "rib_right",    (-5.1, 3.0, -2.4), (1.2, 5.4, 4.4), "rib")
PC("body", "back_plate",   (-3.6, 2.0, 2.35), (7.2, 6.4, 1.1), "plate")
PC("body", "back_vent_l",  (0.4, 2.6, 3.45), (1.6, 3.2, 0.7), "vent", emissive="vent_core")
PC("body", "back_vent_r",  (-2.0, 2.6, 3.45), (1.6, 3.2, 0.7), "vent", emissive="vent_core")
PC("body", "belt",         (-4.5, 10.6, -2.7), (9.0, 2.0, 5.4), "belt")
PC("body", "buckle",       (-1.3, 10.8, -3.25), (2.6, 1.6, 0.6), "buckle", emissive="buckle_core")
PC("shoulder_left", "pauldron_l",  (3.0, -2.9, -2.5), (2.6, 2.8, 5.0), "plate")
PC("shoulder_left", "spike_l1",    (3.4, -4.2, -2.2), (1.6, 1.7, 1.8), "spike")
PC("shoulder_left", "spike_l2",    (3.6, -4.2, 0.4), (1.4, 1.6, 1.6), "spike")
PC("shoulder_right", "pauldron_r", (-5.6, -2.9, -2.5), (2.6, 2.8, 5.0), "plate")
PC("shoulder_right", "spike_r1",   (-5.0, -4.2, -2.2), (1.6, 1.7, 1.8), "spike")
PC("shoulder_right", "spike_r2",   (-5.0, -4.2, 0.4), (1.4, 1.6, 1.6), "spike")
PC("right_arm", "gauntlet_r",      (-3.5, 1.4, -2.4), (5.0, 5.2, 4.8), "gauntlet")
PC("right_arm", "upper_r",         (-3.2, 3.9, -2.2), (4.4, 3.0, 4.4), "red_plate")
PC("right_arm", "wrist_r",         (-3.6, 6.2, -2.5), (5.2, 1.2, 5.0), "wrist")
PC("right_arm", "claws_r",         (-2.4, 9.9, -1.6), (2.8, 1.3, 3.2), "claw")
PC("left_arm", "gauntlet_l",       (-1.5, 1.4, -2.4), (5.0, 5.2, 4.8), "gauntlet")
PC("left_arm", "upper_l",          (-1.2, 3.9, -2.2), (4.4, 3.0, 4.4), "red_plate")
PC("left_arm", "wrist_l",          (-1.6, 6.2, -2.5), (5.2, 1.2, 5.0), "wrist")
PC("left_arm", "claws_l",          (-0.4, 9.9, -1.6), (2.8, 1.3, 3.2), "claw")
PC("right_leg", "thigh_r",  (-2.4, -0.5, -2.3), (4.8, 5.0, 4.6), "red_plate")
PC("right_leg", "knee_r",   (-2.5, 4.3, -2.4), (5.0, 1.7, 4.8), "knee")
PC("right_leg", "greave_r", (-2.4, 5.8, -2.3), (4.6, 5.0, 4.5), "plate")
PC("right_leg", "boot_r",   (-2.5, 10.6, -2.8), (5.0, 1.8, 5.6), "boot")
PC("right_leg", "vent_r",   (-1.5, 12.3, -1.6), (3.0, 0.6, 3.0), "vent", emissive="vent_core")
PC("left_leg", "thigh_l",   (-2.4, -0.5, -2.3), (4.8, 5.0, 4.6), "red_plate")
PC("left_leg", "knee_l",    (-2.5, 4.3, -2.4), (5.0, 1.7, 4.8), "knee")
PC("left_leg", "greave_l",  (-2.4, 5.8, -2.3), (4.6, 5.0, 4.5), "plate")
PC("left_leg", "boot_l",    (-2.5, 10.6, -2.8), (5.0, 1.8, 5.6), "boot")
PC("left_leg", "vent_l",    (-1.5, 12.3, -1.6), (3.0, 0.6, 3.0), "vent", emissive="vent_core")

shelf_pack(HELMET, atlas=128, pad=1)
shelf_pack(PLATE, atlas=128, pad=1)

# ------------------------------------------------------------------ painting
helm = Tex(128, PAL)
helm_glow = Tex(128, PAL)
plate = Tex(128, PAL)
plate_glow = Tex(128, PAL)

def blacken(tex, cube):
    u, v = cube["tex"]
    w, h, d = cube["size"]
    for f, r in face_rects(u, v, w, h, d).items():
        tex.rect(r, (0, 0, 0, 255))

def ember_cracks(tex, r, density=3, vertical=True):
    """Sparse recessed crack pixels: e1 -> e3 -> occasional e4."""
    x, y, w, h = r
    for j in range(1, h - 1, density):
        for i in range(1, w - 1, density):
            if (i + j) % density == 0:
                tex.set(x + i, y + j, PAL["e3"])
                if (i * 7 + j) % 5 == 0:
                    tex.set(x + i, y + j, PAL["e4"])
                if (i + j) % (density * 2) == 1:
                    tex.set(x + i, y + j, PAL["e1"])

def paint_cube(tex, cube, emissive_tex=None):
    u, v = cube["tex"]
    w, h, d = cube["size"]
    R = face_rects(u, v, w, h, d)
    kind = cube["paint"]
    def plate(r, red=False):
        x, y, fw, fh = r
        base = PAL["red"] if red else PAL["char"]
        base_hi = PAL["red_hi"] if red else PAL["char_hi"]
        base_dk = PAL["red_dk"] if red else PAL["iron_dk"]
        tex.rect(r, base)
        tex.border(r, PAL["steel_dk"])
        tex.set(x + 1, y + 1, base_hi)
        ember_cracks(tex, r, density=max(3, min(fw, fh) // 3))
        _ = (base_dk,)
    def metal(r, base="iron", hi="iron_hi", dk="iron_dk"):
        paint_metal(tex, r, PAL[base], PAL[hi], PAL[dk])
    for f, r in R.items():
        if kind == "helm":
            x, y, fw, fh = r
            metal(r)
            if f in ("east", "west"):           # overlapping forged bands
                for j in range(1, fh - 1, 3):
                    tex.rect((x, y + j, fw, 1), PAL["char"])
            if f == "north":
                tex.border(r, PAL["steel"])
            tex.set(x + 1, y + 1, PAL["ash_hi"])
        elif kind == "faceplate":
            x, y, fw, fh = r
            metal(r)
            tex.border(r, PAL["steel_dk"])
        elif kind == "visor":
            x, y, fw, fh = r
            tex.rect(r, PAL["e2"])
            tex.border(r, PAL["iron_dk"])
            for i in range(x + 1, x + fw - 1):
                tex.set(i, y + fh // 2, PAL["e5"])
            tex.set(x + fw // 2, y + fh // 2, PAL["e6"])
        elif kind == "ridge":
            x, y, fw, fh = r
            metal(r, "char", "ash_hi", "soot")
            if f in ("north", "south", "east", "west"):
                tex.border(r, PAL["steel_dk"])
        elif kind == "horn":
            x, y, fw, fh = r
            metal(r, "char", "ash", "soot")
            tex.border(r, PAL["iron_dk"])
            if f in ("east", "west", "north", "south"):
                for j in range(1, fh - 1, 2):   # segment seams glow faintly in base
                    tex.set(x + (fw // 2), y + j, PAL["e1"])
        elif kind == "plate":
            plate(r)
        elif kind == "plate_v":
            x, y, fw, fh = r
            plate(r, red=True)
            if f == "north":                     # V chevron
                for j in range(fh):
                    tex.set(x + fw // 2 - j // 2, y + j, PAL["red_hi"])
                    tex.set(x + fw // 2 + j // 2, y + j, PAL["red_hi"])
        elif kind == "abdomen":
            x, y, fw, fh = r
            metal(r)
            for i in range(x + 1, x + fw - 1, 3):
                tex.set(i, y + 1, PAL["char_hi"])
        elif kind == "core":
            x, y, fw, fh = r
            plate(r, red=True)
            if f == "north":
                tex.rect((x + fw // 2 - 1, y + 2, 2, fh - 4), PAL["e3"])
                tex.set(x + fw // 2, y + fh // 2, PAL["e5"])
        elif kind == "rib":
            x, y, fw, fh = r
            metal(r, "red", "red_hi", "red_dk")
            tex.border(r, PAL["steel_dk"])
        elif kind == "vent":
            x, y, fw, fh = r
            tex.rect(r, PAL["soot"])
            tex.border(r, PAL["iron_dk"])
            if f == "south":                     # vent interior seen from behind
                tex.rect((x + 1, y + 1, fw - 2, fh - 2), PAL["e3"])
                tex.rect((x + fw // 2 - 1, y + 2, 2, fh - 4), PAL["e5"])
            if f == "down":                      # boot vent core seen from below
                tex.rect((x + 1, y + 1, fw - 2, fh - 2), PAL["e3"])
                tex.rect((x + 1, y + fh // 2 - 1, fw - 2, 2), PAL["e5"])
        elif kind == "belt":
            for f2, r2 in R.items():
                paint_leather(tex, r2, PAL["char"], PAL["ash"], PAL["soot"])
            x, y, fw, fh = r
            tex.border(r, PAL["steel_dk"])
            break
        elif kind == "buckle":
            x, y, fw, fh = r
            metal(r, "char", "ash_hi", "soot")
            tex.border(r, PAL["steel"])
            if f == "north":
                tex.set(x + fw // 2, y + fh // 2, PAL["e5"])
        elif kind == "spike":
            metal(r, "red", "red_hi", "red_dk")
        elif kind == "gauntlet":
            x, y, fw, fh = r
            metal(r)
            tex.border(r, PAL["steel_dk"])
            if f in ("north", "south", "east", "west"):
                for j in range(2, fh - 2, 4):    # ember crack rows near joints
                    tex.set(x + fw // 2, y + j, PAL["e3"])
        elif kind == "red_plate":
            plate(r, red=True)
        elif kind == "wrist":
            x, y, fw, fh = r
            metal(r, "steel", "steel_hi", "steel_dk")
        elif kind == "claw":
            metal(r, "steel_dk", "steel", "soot")
        elif kind == "knee":
            x, y, fw, fh = r
            plate(r, red=True)
            tex.border(r, PAL["steel"])
        elif kind == "boot":
            x, y, fw, fh = r
            metal(r)
            tex.border(r, PAL["steel_dk"])
            if f == "down":
                tex.rect((x + 1, y + 1, fw - 2, fh - 2), PAL["soot"])
    if emissive_tex and cube["emissive"]:
        em = cube["emissive"]
        for f, r in R.items():
            x, y, fw, fh = r
            if em == "visor":
                if f == "north":
                    emissive_tex.rect(r, PAL["e2"])
                    emissive_tex.rect((x + 1, y + fh // 2 - 1, fw - 2, 2), PAL["e5"])
                    emissive_tex.set(x + fw // 2, y + fh // 2, PAL["e6"])
            elif em == "visor_slit":
                pass
            elif em == "vent_core":
                if f == "south":
                    emissive_tex.rect((x + 1, y + 1, fw - 2, fh - 2), PAL["e4"])
                    emissive_tex.rect((x + fw // 2 - 1, y + 2, 2, fh - 4), PAL["e6"])
                if f == "down":
                    emissive_tex.rect((x + 1, y + 1, fw - 2, fh - 2), PAL["e4"])
                    emissive_tex.rect((x + 1, y + fh // 2 - 1, fw - 2, 2), PAL["e6"])
            elif em == "buckle_core":
                if f == "north":
                    emissive_tex.set(x + fw // 2, y + fh // 2, PAL["e5"])
            elif em == "horn_cracks":
                if f in ("east", "west", "north", "south"):
                    ember_cracks(emissive_tex, r, density=2)
            elif em == "core_seam":
                if f == "north":
                    emissive_tex.rect((x + fw // 2 - 1, y + 2, 2, fh - 4), PAL["e3"])
                    emissive_tex.set(x + fw // 2, y + fh // 2, PAL["e5"])

for cube in HELMET:
    paint_cube(helm, cube, helm_glow)
for cube in PLATE:
    paint_cube(plate, cube, plate_glow)
for cube in HELMET + PLATE:                       # black out emissive for non-emissive
    pass

# fill emissive maps black first? They start transparent; fill black base then repaint.
for t in (helm_glow, plate_glow):
    for j in range(128):
        for i in range(128):
            t.px[i, j] = (0, 0, 0, 255)
# repaint emissive after blacking
for cube in HELMET:
    paint_cube(helm, cube, None)                  # base repaint unchanged
for cube in HELMET:
    paint_cube(helm, cube, helm_glow)             # emissive second pass
for cube in PLATE:
    paint_cube(plate, cube, plate_glow)

# ------------------------------------------------------------------ icons
icons = {}
CHAR = {"A": "ash", "e": "e3", "h": "iron", "i": "steel_dk", "r": "red", "R": "red_hi",
        "6": "e6", "5": "e5", "4": "e4", "2": "e2", "b": "e4", "s": "steel", "S": "soot"}

def icon(name, rows):
    im = Tex(16, PAL)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.set(x, y, PAL[CHAR[ch]])
    icons[name] = im

icon("fire_demonic_helmet", [
    "......AA.AA.....",
    ".....AeA.AeA....",
    ".....AeA.AeA....",
    "....AeeA.AeeA...",
    "....AeeAAAeeA...",
    "...iiiiiiiiiii..",
    "..ihhihhhhhihhi.",
    ".ihhhihhhhhihhi.",
    ".ihhhhhhhhhhhhi.",
    ".ihheeeeeeeeehi.",
    ".ihhe6666666ehi.",
    ".ihhe2222222ehi.",
    "..ihhhhhhhhhhi..",
    "..ihhhhihhhhhhi.",
    "...iiiiiiiiiii..",
    "................",
])
icon("fire_demonic_chestplate", [
    "................",
    "..hh........hh..",
    ".hiih......hiih.",
    ".hiihrrrrrrhiih.",
    "..hhreereehreh..",
    "...rrhe66ehrr...".replace("_","h"),
    "...rrhe5e5err...",
    "...irheeeeeri...",
    "...irhheeehri...",
    "...irhhhehhri...",
    "...irhhhehhri...",
    "...irhhhehhri...",
    "...ihhhhhhhhi...",
    "...ihhhbhbbhi...",
    "...iiiiiiiiii...",
    "................",
])
icon("fire_demonic_leggings", [
    "................",
    "...hhhhhhhhhh...",
    "...hiiiiiiiih...",
    "...hi222222ih...",
    "...hiee66eeih...",
    "...hieeeeeeih...",
    "...hihhiihhhih..",
    "...hhih..hihh...",
    "...hhih..hihh...",
    "...hiih..hiih...",
    "...hiih..hiih...",
    "...hiih..hiih...",
    "...heeh..heeh...",
    "...iiii..iiii...",
    "................",
    "................",
])
icon("fire_demonic_boots", [
    "................",
    "................",
    "..hh......hh....",
    "..hih....hih....",
    "..hih....hih....",
    "..hih....hih....",
    "..hih....hih....",
    "..hih....hih....",
    "..hih....hih....",
    "..hihh..hhih....",
    "..hiih..hihh....",
    ".hhiihhhhiihh...",
    ".he55555555eh...",
    ".h6666666666h...",
    ".iiiiiiiiiiii...",
    "................",
])

# ------------------------------------------------------------------ emit
out = ASSETS / "textures" / "ember" / "armor"
out.mkdir(parents=True, exist_ok=True)
helm.img.save(out / "fire_demonic_helmet_layer.png")
helm_glow.img.save(out / "fire_demonic_helmet_layer_emissive.png")
plate.img.save(out / "fire_demonic_plate_layer.png")
plate_glow.img.save(out / "fire_demonic_plate_layer_emissive.png")
for name, im in icons.items():
    im.img.save(ASSETS / "textures" / "item" / f"{name}.png")

# validation: base atlas opaque under all face rects; emissive aligned
def check(cubes, base, glow, label):
    errs = []
    for c in cubes:
        u, v = c["tex"]
        w, h, d = c["size"]
        for f, r in face_rects(u, v, w, h, d).items():
            x, y, fw, fh = r
            for j in range(y, y + fh):
                for i in range(x, x + fw):
                    if base.px[i, j][3] == 0:
                        errs.append(f"{label}:{c['name']}.{f} transparent base ({i},{j})")
                        break
                else:
                    continue
                break
            # emissive must be black or ember ramp (aligned pixels, no transparency)
            for j in range(y, y + fh):
                for i in range(x, x + fw):
                    p = glow.px[i, j]
                    if p[:3] != (0, 0, 0) and p not in {PAL["e1"], PAL["e2"], PAL["e3"], PAL["e4"], PAL["e5"], PAL["e6"]}:
                        errs.append(f"{label}:{c['name']}.{f} bad emissive px {p}")
                        break
                else:
                    continue
                break
    return errs

errors = check(HELMET, helm, helm_glow, "helmet") + check(PLATE, plate, plate_glow, "plate")
# icons: palette check done implicitly; ensure no fully empty icons
for name, im in icons.items():
    if not any(im.px[i, j][3] for j in range(16) for i in range(16)):
        errors.append(f"icon {name} empty")
if errors:
    print("VALIDATION ERRORS:")
    for e in errors[:30]:
        print(" -", e)
    sys.exit(1)

# ------------------------------------------------------------------ java snippets
def java_cubes(cubes, indent="        "):
    lines = []
    cur_bone = None
    for c in cubes:
        if c["bone"] != cur_bone:
            lines.append(f"{indent}// {c['bone']}")
            cur_bone = c["bone"]
        u, v = c["tex"]
        x, y, z = c["origin"]
        w, h, d = c["size"]
        inf = f", new CubeDeformation({c['inflate']}f)" if c.get("inflate") else ""
        lines.append(f"{indent}.texOffs({u}, {v}).addBox({x}F, {y}F, {z}F, {w}F, {h}F, {d}F{inf})")
    return "\n".join(lines)

snippet = "=== HELMET CUBES (per bone) ===\n" + java_cubes(HELMET) + "\n\n=== PLATE CUBES (per bone) ===\n" + java_cubes(PLATE)
Path("/tmp/opencode/fire_demonic_java_snippets.txt").write_text(snippet + "\n")
print(f"OK: helmet {len(HELMET)} cubes, plate {len(PLATE)} cubes, 4 icons; snippets -> /tmp/opencode/fire_demonic_java_snippets.txt")
