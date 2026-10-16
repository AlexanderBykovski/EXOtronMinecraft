#!/usr/bin/env python3
"""Generator for the EXO-1..4 frame models (geo + 256px FFD texture + animations).

Style anchor: exo_plus (EXO-5 VEngeance) — red/black/gold layered armor, same palette.
Conventions (concepts/tasks/14-exo-animations.md): auth space left side x<0, front = -Z;
GeckoLib mirrors X on load (pivot.x -> -x, origin.x -> -(x+w)); static rotation -x/-y;
animation rotation degrees -> radians with X/Y negation (that part lives in the previewer).

QA checks: UV in bounds, soles y=0, L/R mirror symmetry (pivot + cube origins), every
animation bone exists in the geometry, no chest_core where the frame has no beam,
DANGER stripes (long alternating 2-colour runs) = 0.

Usage: python3 scripts/gen_exo_frames.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO_DIR = ROOT / "src/main/resources/assets/opusvsexe/geo/entity"
TEX_DIR = ROOT / "src/main/resources/assets/opusvsexe/textures/entity"
ANIM_DIR = ROOT / "src/main/resources/assets/opusvsexe/animations/entity"
STYLE_DIR = ROOT / "build/preview_exo_frames"

ATLAS = 256
GAP = 1

PALETTE = {
    "D": (74, 14, 14), "R": (139, 26, 26), "r": (179, 45, 45),
    "B": (20, 20, 20), "b": (38, 38, 38), "e": (61, 61, 61),
    "g": (110, 110, 110), "l": (154, 154, 154),
    "G": (138, 109, 31), "A": (212, 160, 23), "Y": (255, 201, 60), "W": (255, 245, 200),
}

# ---------------------------------------------------------------------------
# painters: fn(w, h, seed) -> list[str] rows of palette chars ('.' => transparent)
# ---------------------------------------------------------------------------


def _rnd(seed):
    return (seed * 1103515245 + 12345) & 0x7FFFFFFF


def paint_black(w, h, seed):
    rnd = _rnd(seed + 7)
    rows = [["B"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x == 0 or y == 0:
                rows[y][x] = "b"
            elif x == w - 1 or y == h - 1:
                rows[y][x] = "B"
            else:
                rows[y][x] = "B" if rnd % 11 else "b"
            if rnd % 37 == 0:
                rows[y][x] = "e"
    return ["".join(r) for r in rows]


def paint_red(w, h, seed):
    """Fish-scale armour: arc rows (2px offset per row), D outlines, r highlights."""
    scale = 4
    rows = [["R"] * w for _ in range(h)]
    for y in range(h):
        off = 2 * ((y // scale) % 2)
        for x in range(w):
            xx = (x + off) % scale
            yy = y % scale
            if yy == 0:
                rows[y][x] = "D" if xx in (0, scale - 1) else "R"
            elif yy == 2:
                rows[y][x] = "D" if xx in (0, scale - 1) else "r"
            else:
                rows[y][x] = "R"
            if yy == scale - 1 and xx == 1:
                rows[y][x] = "r"
    return ["".join(r) for r in rows]


def paint_red_plate(w, h, seed):
    rnd = _rnd(seed + 3)
    rows = [["R"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x == 0 and y == 0:
                rows[y][x] = "r"
            elif x == 0 or y == 0:
                rows[y][x] = "R"
            elif x == w - 1 or y == h - 1:
                rows[y][x] = "D"
            elif x % 9 == 8 or y % 13 == 12:
                rows[y][x] = "D"
            elif rnd % 29 == 0:
                rows[y][x] = "r"
    return ["".join(r) for r in rows]


def paint_red_dark(w, h, seed):
    rnd = _rnd(seed + 5)
    rows = [["D"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x == 0 or y == 0:
                rows[y][x] = "R"
            elif rnd % 23 == 0:
                rows[y][x] = "R"
    return ["".join(r) for r in rows]


def paint_gold(w, h, seed):
    rnd = _rnd(seed + 11)
    rows = [["A"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            t = y / max(1, h - 1)
            if t < 0.33:
                rows[y][x] = "G"
            elif t > 0.75:
                rows[y][x] = "Y"
            else:
                rows[y][x] = "A"
            if x == 0 or y == 0:
                rows[y][x] = "G"
            elif x == w - 1 or y == h - 1:
                rows[y][x] = "A"
            if rnd % 31 == 0:
                rows[y][x] = "Y"
    return ["".join(r) for r in rows]


def paint_gold_bright(w, h, seed):
    rnd = _rnd(seed + 13)
    rows = [["A"] * w for _ in range(h)]
    cx, cy = w // 2, h // 2
    r0 = max(1, min(w, h) // 4)
    r1 = max(2, min(w, h) // 2)
    for y in range(h):
        for x in range(w):
            d = abs(x - cx) + abs(y - cy)
            if d <= r0:
                rows[y][x] = "W"
            elif d <= r1:
                rows[y][x] = "Y"
            elif rnd % 17 == 0:
                rows[y][x] = "Y"
    return ["".join(r) for r in rows]


def paint_metal(w, h, seed):
    rnd = _rnd(seed + 17)
    rows = [["g"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x == 0 and y == 0:
                rows[y][x] = "l"
            elif x == 0 or y == 0:
                rows[y][x] = "g"
            elif x == w - 1 or y == h - 1:
                rows[y][x] = "e"
            elif rnd % 19 == 0:
                rows[y][x] = "l"
    return ["".join(r) for r in rows]


def paint_metal_dark(w, h, seed):
    rnd = _rnd(seed + 19)
    rows = [["e"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x == 0 and y == 0:
                rows[y][x] = "g"
            elif x == 0 or y == 0:
                rows[y][x] = "e"
            elif x == w - 1 or y == h - 1:
                rows[y][x] = "b"
            elif rnd % 13 == 0:
                rows[y][x] = "B"
    return ["".join(r) for r in rows]


def paint_eye(w, h, seed):
    """Angry single slant eye on a black panel: moves down toward -x, W sparks."""
    rows = [["B"] * w for _ in range(h)]
    base = h // 2
    for x in range(w):
        y = base - max(0, (x - w // 3))
        for dy in (0, 1):
            if 0 <= y + dy < h:
                rows[y + dy][x] = "r" if dy == 0 else "D"
        if x % 4 == 2 and 0 <= y < h:
            rows[y][x] = "W"
    return ["".join(r) for r in rows]


def paint_eye_twin(w, h, seed):
    """Two slant eyes from the centre outwards, W spark inner edge."""
    rows = [["B"] * w for _ in range(h)]
    mid = w // 2
    for x in range(1, w - 1):
        half = 0 if x <= mid else 1
        i = (mid - x) if half == 0 else (x - mid)
        y = h // 2 - 1 - i
        for dy in (0, 1, 2):
            if 0 <= y + dy < h:
                rows[y + dy][x] = "r" if dy == 0 else "D"
        if i % 3 == 1 and 0 <= y < h:
            rows[y][x] = "W"
    return ["".join(r) for r in rows]


def paint_eye_duo(w, h, seed):
    """Twin horizontal slits (bunker glance) with a gap at the centre; W sparks."""
    rows = [["B"] * w for _ in range(h)]
    mid = w // 2
    for x in range(w):
        if abs(x - mid) < 2:
            continue
        for dy in (0, 1):
            if 0 <= h // 2 + dy < h:
                rows[h // 2 + dy][x] = "r"
            if dy == 0 and abs(x - mid) > 1 and abs(x - mid) % 4 == 1:
                rows[h // 2][x] = "W"
    return ["".join(r) for r in rows]


def paint_chestring(w, h, seed):
    """Circular emitter: black ring -> gold rim -> red core -> white hot centre."""
    rows = [["b"] * w for _ in range(h)]
    cx, cy = w / 2 - 0.5, h / 2 - 0.5, 
    m = (max(abs(w - 3), abs(h - 3)) + 2) / 2.0
    for y in range(h):
        for x in range(w):
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if d <= max(1.2, m * 0.35):
                rows[y][x] = "W"
            elif d <= max(2.2, m * 0.58):
                rows[y][x] = "r"
            elif d <= max(3.0, m * 0.78):
                rows[y][x] = "A"
            else:
                rows[y][x] = "b"
    return ["".join(r) for r in rows]


def paint_claw(w, h, seed):
    rnd = _rnd(seed + 23)
    rows = [["e"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            t = y / max(1, h - 1)
            if t > 0.7:
                rows[y][x] = "l"
            elif rnd % 7 == 0:
                rows[y][x] = "g"
    return ["".join(r) for r in rows]


def paint_nozzle(w, h, seed):
    rows = [["e"] * w for _ in range(h)]
    for x in range(w):
        if h >= 2:
            rows[h - 1][x] = "b"
            rows[h - 2][x] = "A"
        if w % 2 == 0 and x == w // 2 and h >= 1:
            rows[0][x] = "g"
    return ["".join(r) for r in rows]


def paint_coil(w, h, seed):
    rows = [["b"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x % 3 == 1:
                rows[y][x] = "A"
            if (x // 3) % 2 == 1:
                rows[y][x] = "Y" if w % 2 == 0 else rows[y][x]
    return ["".join(r) for r in rows]


def paint_prisma(w, h, seed):
    rows = [["A"] * w for _ in range(h)]
    steps = max(2, min(w, h) // 2 + 1)
    for y in range(h):
        for x in range(w):
            if (x + y) % steps == 0:
                rows[y][x] = "G"
            if abs(x - y) < 2 and (x + y) % 3 == 0:
                rows[y][x] = "W"
    return ["".join(r) for r in rows]


def paint_stack(w, h, seed):
    """Black exhaust pipe: horizontal rings, red band, gold rim."""
    rows = [["b"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if y % 4 == 3:
                rows[y][x] = "e"
            if y == 0 or y == h - 1:
                rows[y][x] = "B"
            if y % 7 == 2 and (y // 7) % 3 == 0:
                rows[y][x] = "R"
            if x in (0, w - 1) and y % 4 == 3:
                rows[y][x] = "b"
    return ["".join(r) for r in rows]


def paint_glass3(w, h, seed):
    rows = [["b"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x % 5 == 0:
                rows[y][x] = "g"
            if y == 0 or y == h - 1:
                rows[y][x] = "l"
            if x % 5 == 2 and y % 2 == 1:
                rows[y][x] = "e"
    return ["".join(r) for r in rows]


def paint_decal2(w, h, seed):
    rnd = _rnd(seed + 29)
    rows = [["D"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if rnd % 5 < 2:
                rows[y][x] = "l"
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                rows[y][x] = "R"
    return ["".join(r) for r in rows]


def paint_vribs(w, h, seed):
    rows = [["R"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if (x + y) % 10 == 0:
                rows[y][x] = "A"
            if (x + y) % 10 == 1:
                rows[y][x] = "G"
            if y == 0 or y == h - 1:
                rows[y][x] = "D"
    return ["".join(r) for r in rows]


def paint_craze(w, h, seed):
    rnd = _rnd(seed + 31)
    rows = [["B"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x - y * 2 in (0, 1, 3, 6, 9) or y - x in (0, 2):
                rows[y][x] = "G"
            if x % 7 == 3 and y % 5 == 1:
                rows[y][x] = "A"
            if rnd % 13 == 0:
                rows[y][x] = "G"
    return ["".join(r) for r in rows]


PAINTERS = {
    "black": paint_black,
    "red": paint_red,
    "red_plate": paint_red_plate,
    "red_dark": paint_red_dark,
    "gold": paint_gold,
    "gold_bright": paint_gold_bright,
    "metal": paint_metal,
    "metal_dark": paint_metal_dark,
    "eye_mono": paint_eye,
    "eye_twin": paint_eye_twin,
    "eye_duo": paint_eye_duo,
    "chestring": paint_chestring,
    "claw": paint_claw,
    "nozzle": paint_nozzle,
    "coil": paint_coil,
    "prisma": paint_prisma,
    "stack": paint_stack,
    "glass3": paint_glass3,
    "decal2": paint_decal2,
    "vribs": paint_vribs,
    "craze": paint_craze,
}

# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------


def C(x, y, z, w, h, d, m, faces=None):
    return {"o": [x, y, z], "s": [w, h, d], "m": m, "faces": faces or {}}


def B(name, parent, pivot, rot=None, cubes=None, single=False):
    return {"n": name, "p": parent, "pivot": pivot, "rot": rot,
            "cubes": cubes or [], "single": single}


# ---------------------------------------------------------------------------
# frame specs (auth space: left x<0, front = -Z, height 72px = 4.5 blocks)
# ---------------------------------------------------------------------------
# NOTE: right-side bones list only mirror-stub entries (empty cubes); the
# generator copies geometry from the left twin via `mirror` pairs.

FRAMES = {
    "exo_1_sentinel": {
        "bones": [
            B("the_omen", None, [0, 0, 0], None, []),
            B("left_hip_joint", "the_omen", [-4, 45, 0], None, [
                C(-8, 40, -4, 7, 6, 8, "black"),
                C(-12, 41, -4.5, 5, 5, 9, "red_plate", {"east": "red_dark"}),
            ]),
            B("left_thigh_joint", "left_hip_joint", [-9, 45, 0], None, [
                C(-13, 28, -5, 9, 13, 10, "red_plate", {"west": "red_dark", "back": "red_dark", "top": "black"}),
                C(-12, 24.5, -4, 7, 2.5, 8, "black"),
                C(-15, 27, -4.5, 2.5, 4, 9, "gold", {"west": "gold_bright"}),
            ]),
            B("left_calf_joint", "left_thigh_joint", [-9, 27, 0], None, [
                C(-13, 10, -4.5, 9, 14, 9, "red_dark"),
                C(-13, 11, -6.5, 9, 12, 2, "red_plate"),
                C(-11.5, 14, 4, 5, 9, 2.5, "black", {"front": "metal_dark"}),
                C(-13, 21.5, -4.8, 9, 3, 9.6, "black"),
                C(-11.5, 3, -2.5, 6, 8, 6, "metal_dark"),
            ]),
            B("left_foot_joint", "left_calf_joint", [-9, 8, 0], None, [
                C(-15, 0, -7, 12, 5, 11, "black", {"top": "metal_dark"}),
                C(-14, 0, -10.5, 10, 3, 4.5, "gold", {"down": "G", "front": "gold_bright"}),
                C(-14, 0, 4, 10, 2, 2.5, "metal_dark"),
            ]),
            B("hips", "the_omen", [0, 45, 0], None, [
                C(-8, 44, -5.5, 16, 4, 11, "black", {"front": "red_dark"}),
                C(-2, 44.5, -6.2, 4, 3, 1.5, "gold"),
                C(-4, 37.5, -5.5, 8, 7, 0.8, "red_dark"),
            ]),
            B("torso", "hips", [0, 57, 0], None, [
                C(-11, 48, -6, 22, 10, 10, "red", {"back": "black", "top": "black", "down": "black", "west": "red_plate", "east": "red_plate"}),
                C(-10, 56, -6.5, 20, 4, 11, "black"),
                C(-5, 49, -6.7, 10, 6, 0.6, "glass3"),
                C(4, 49.5, -6.6, 5, 2, 0.6, "decal2"),
                C(-9, 50, 4, 18, 8, 3, "black", {"front": "metal_dark"}),
                C(-7, 60, -4.5, 14, 2, 8, "metal_dark"),
                C(-13, 57.5, -4, 6, 5, 7, "metal_dark"),
                C(7, 57.5, -4, 6, 5, 7, "metal_dark"),
            ]),
            B("face", "torso", [0, 64, -6], None, [
                C(-6, 60.5, -6.3, 12, 3.5, 0.6, "eye_mono"),
            ]),
            B("head", "torso", [0, 66, -1], None, [
                C(-6, 62, -6, 12, 8, 10, "black", {"front": "red_dark", "top": "red_dark"}),
                C(-4, 69.5, -4, 8, 1.5, 7, "metal", {"top": "black"}),
            ]),
            B("left_pauldron", "torso", [-17, 62, 0], None, [
                C(-24, 57, -6, 12, 7, 10, "black", {"west": "red_dark"}),
                C(-23, 59.5, -6.7, 4, 2.5, 0.8, "gold", {"front": "gold_bright"}),
                C(-24.5, 63.5, -5.5, 11, 1.2, 9, "red_dark", {"top": "R"}),
            ]),
            B("left_arm_joint", "torso", [-19, 61, 0], None, [
                C(-23, 50, -4.5, 8, 9, 9, "black", {"front": "red_dark"}),
                C(-26, 50, -5, 3.5, 9, 10, "red_plate", {"west": "red_dark"}),
                C(-24, 49.5, -5, 9, 2.5, 10, "gold"),
            ]),
            B("left_arm_joint2", "left_arm_joint", [-19, 47, 0], None, [
                C(-24, 34, -4, 8, 11, 9, "metal_dark", {"front": "metal"}),
                C(-22, 43.5, -2.5, 5, 4, 5, "metal"),
                C(-22.5, 43.5, -3, 5, 5, 7, "metal_dark"),
            ]),
            B("left_hand", "left_arm_joint2", [-19, 31, 0], None, [
                C(-26, 20, -6, 13, 12, 13, "black", {"west": "red_dark", "top": "red_dark"}),
                C(-25, 31, -5.5, 11, 3, 11, "red_dark"),
                C(-22.5, 26, -6.8, 4, 3, 0.7, "craze"),
                C(-27, 22, -6, 2.5, 5, 13, "red_plate", {"west": "red_dark"}),
            ]),
            B("back_exhaust_l", "torso", [-8, 60, 9], [-12, 0, 0], [
                C(-11, 54, 8, 6, 12, 6, "stack", {"top": "black"}),
                C(-10, 65.5, 8.5, 4, 2, 4, "black"),
            ]),
            B("right_hip_joint", "the_omen", [4, 45, 0], None, []),
            B("right_thigh_joint", "right_hip_joint", [9, 45, 0], None, []),
            B("right_calf_joint", "right_thigh_joint", [9, 27, 0], None, []),
            B("right_foot_joint", "right_calf_joint", [9, 8, 0], None, []),
            B("right_pauldron", "torso", [17, 62, 0], None, []),
            B("right_arm_joint", "torso", [21, 61, 0], None, []),
            B("right_arm_joint2", "right_arm_joint", [21, 47, 0], None, []),
            B("right_hand", "right_arm_joint2", [21, 31, 0], None, []),
            B("back_exhaust_r", "torso", [8, 60, 9], [-12, 0, 0], []),
        ],
        "mirror": [
            ("left_hip_joint", "right_hip_joint"), ("left_thigh_joint", "right_thigh_joint"),
            ("left_calf_joint", "right_calf_joint"), ("left_foot_joint", "right_foot_joint"),
            ("left_pauldron", "right_pauldron"), ("left_arm_joint", "right_arm_joint"),
            ("left_arm_joint2", "right_arm_joint2"), ("left_hand", "right_hand"),
            ("back_exhaust_l", "back_exhaust_r"),
        ],
    },
    "exo_2_hunter": {
        "bones": [
            B("the_omen", None, [0, 0, 0], None, []),
            B("left_hip_joint", "the_omen", [-3.5, 45, 0], None, [
                C(-5.5, 38, -3, 5, 9, 6, "metal_dark"),
                C(-7.5, 41, -3.5, 2.5, 5, 7, "red_plate", {"west": "red_dark"}),
            ]),
            B("left_thigh_joint", "left_hip_joint", [-8, 45, 0], None, [
                C(-11, 29, -4, 7, 14, 8, "red_plate", {"back": "red_dark", "top": "red_dark"}),
                C(-11, 25.5, -4.5, 7, 2.5, 9, "gold"),
                C(-12.5, 30, -4.5, 2, 11, 9, "red_dark", {"west": "R"}),
            ]),
            B("left_calf_joint", "left_thigh_joint", [-8, 27, 0], None, [
                C(-11, 10, -3.5, 7, 15, 7, "red_dark"),
                C(-11, 12, -5.5, 7, 10, 2, "red_plate"),
                C(-10, 14, 4, 5, 8, 2, "metal_dark", {"back": "metal_dark"}),
                C(-11.5, 11, 3.4, 8, 3, 2.6, "nozzle", {"top": "black"}),
                C(-11, 3, -3, 7, 9, 7, "metal_dark"),
            ]),
            B("left_foot_joint", "left_calf_joint", [-8, 8, 0], None, [
                C(-13, 0, -8, 10, 5, 12, "black", {"front": "red_dark", "top": "black"}),
                C(-12, 0, -10, 8, 2, 3, "red_dark", {"front": "red_plate"}),
                C(-12, 0, 4.4, 8, 2, 2, "gold", {"back": "gold_bright"}),
            ]),
            B("hips", "the_omen", [0, 45, 0], None, [
                C(-7, 44, -4.5, 14, 4, 9, "black", {"front": "red_dark"}),
                C(-2, 44.5, -5.2, 4, 2.5, 1.2, "gold"),
            ]),
            B("torso", "hips", [0, 57, 0], None, [
                C(-8, 46, -5, 16, 11, 9, "black", {"front": "red_dark", "top": "black", "back": "metal_dark"}),
                C(-8, 56, -5, 16, 4, 9, "red_plate", {"top": "black"}),
                C(-5, 44.5, -4, 10, 3, 8, "metal_dark"),
                C(-4, 48, 4, 8, 8, 3, "black"),
                C(-6, 60, -4.5, 12, 2, 8, "metal_dark"),
                C(-12.5, 56, -4.5, 5, 5, 8, "metal_dark"),
                C(7.5, 56, -4.5, 5, 5, 8, "metal_dark"),
            ]),
            B("chest_core", "torso", [0, 58, -7], None, [
                C(-3, 55, -6.3, 6, 4.5, 1, "chestring"),
            ]),
            B("face", "torso", [0, 63, -6], None, [
                C(-5, 60.5, -6.4, 10, 3.5, 0.6, "eye_twin"),
            ]),
            B("head", "torso", [0, 65, -1], None, [
                C(-5, 60, -6, 10, 8, 9, "black", {"front": "red_dark", "top": "red_dark"}),
                C(-5, 66, -5, 10, 1.5, 7, "red_dark", {"top": "R"}),
                C(-4.5, 58, -2, 9, 2, 4, "metal_dark"),
            ]),
            B("head_fin", "head", [-2, 68, 2], [-8, 0, 0], [
                C(-3.5, 68, 2, 2, 6, 1.5, "black", {"back": "metal"}),
                C(-3.5, 73.5, 2, 2, 1.8, 1.5, "gold", {"back": "gold_bright"}),
            ], single=True),
            B("left_pauldron", "torso", [-14, 62, 0], None, [
                C(-18, 58, -4, 8, 4, 7, "black", {"west": "red_dark"}),
                C(-18, 59.2, -4.5, 8, 1.5, 8, "gold", {"top": "gold_bright"}),
            ]),
            B("left_arm_joint", "torso", [-16, 61, 0], None, [
                C(-19, 51, -4, 6, 8, 8, "black", {"front": "red_dark"}),
                C(-20.5, 51, -3.5, 2.5, 8, 7, "red_plate", {"west": "red_dark"}),
                C(-19, 50.5, -4.5, 6, 2, 9, "gold"),
            ]),
            B("left_arm_joint2", "left_arm_joint", [-16, 47, 0], None, [
                C(-19.5, 35, -3.5, 7, 11, 7, "metal_dark", {"front": "metal"}),
                C(-20, 38.5, -4, 9, 2, 8, "gold"),
                C(-19.5, 44, -3.5, 7, 8, 7, "metal_dark"),
            ]),
            B("left_hand", "left_arm_joint2", [-16, 31, 0], None, [
                C(-20, 24, -4.5, 8, 9, 9, "claw", {"top": "metal_dark"}),
                C(-21, 19.5, -5.5, 10, 4.5, 1.6, "claw"),
                C(-21, 19.5, -2.6, 10, 4.5, 1.6, "claw"),
                C(-21, 19.5, 0.3, 10, 4.5, 1.6, "claw"),
            ]),
            B("back_thruster", "torso", [0, 58, 7], None, [
                C(-4, 52, 6, 8, 6, 4, "metal_dark", {"top": "metal"}),
                C(-4, 50.5, 6.2, 8, 2.5, 3.6, "nozzle", {"down": "gold_bright"}),
            ]),
            B("right_hip_joint", "the_omen", [3.5, 45, 0], None, []),
            B("right_thigh_joint", "right_hip_joint", [8, 45, 0], None, []),
            B("right_calf_joint", "right_thigh_joint", [8, 27, 0], None, []),
            B("right_foot_joint", "right_calf_joint", [8, 8, 0], None, []),
            B("right_pauldron", "torso", [14, 62, 0], None, []),
            B("right_arm_joint", "torso", [16, 61, 0], None, []),
            B("right_arm_joint2", "right_arm_joint", [16, 47, 0], None, []),
            B("right_hand", "right_arm_joint2", [16, 31, 0], None, []),
        ],
        "mirror": [
            ("left_hip_joint", "right_hip_joint"), ("left_thigh_joint", "right_thigh_joint"),
            ("left_calf_joint", "right_calf_joint"), ("left_foot_joint", "right_foot_joint"),
            ("left_pauldron", "right_pauldron"), ("left_arm_joint", "right_arm_joint"),
            ("left_arm_joint2", "right_arm_joint2"), ("left_hand", "right_hand"),
        ],
    },
    "exo_3_vanguard": {
        "bones": [
            B("the_omen", None, [0, 0, 0], None, []),
            B("left_hip_joint", "the_omen", [-4, 45, 0], None, [
                C(-8, 40, -4, 7, 6, 8, "metal_dark"),
                C(-10.5, 41, -4.5, 4, 5, 9, "red_plate", {"west": "red_dark"}),
            ]),
            B("left_thigh_joint", "left_hip_joint", [-9, 45, 0], None, [
                C(-13, 28, -5, 9, 14, 10, "red_plate", {"top": "red_dark", "back": "red_dark"}),
                C(-13, 26.5, -5.5, 9, 2.5, 11, "gold"),
                C(-15, 32, -5.5, 2, 9, 11, "red_dark", {"west": "R"}),
            ]),
            B("left_calf_joint", "left_thigh_joint", [-9, 27, 0], None, [
                C(-13, 9, -4.5, 9, 15, 9, "red_dark"),
                C(-13, 11, -6.5, 9, 12, 2, "red_plate"),
                C(-12, 14, 4.5, 7, 10, 2.5, "black", {"back": "metal_dark"}),
                C(-13, 12, -6.9, 9, 2, 0.8, "red_plate", {"front": "r"}),
                C(-11.5, 3, -2.5, 6, 9, 6, "metal_dark"),
            ]),
            B("left_foot_joint", "left_calf_joint", [-9, 8, 0], None, [
                C(-15, 0, -7.5, 12, 5, 12, "black", {"top": "metal_dark", "front": "red_dark"}),
                C(-14, 0, -10, 10, 2.5, 3, "gold", {"front": "gold_bright"}),
                C(-14, 0.5, 4.8, 10, 2, 1.8, "metal_dark"),
            ]),
            B("hips", "the_omen", [0, 45, 0], None, [
                C(-9, 44, -5, 18, 4, 10, "black", {"front": "red_dark"}),
                C(-2, 44.5, -5.6, 4, 2.5, 1.2, "gold"),
            ]),
            B("torso", "hips", [0, 57, 0], None, [
                C(-11, 49, -6, 22, 9, 10, "red_plate", {"top": "black", "back": "red_dark"}),
                C(-9, 56, -6.5, 18, 4, 11, "black", {"front": "red_dark"}),
                C(-6, 60, -4.5, 12, 2, 8, "metal_dark"),
                C(-6, 50, -6.8, 12, 6, 1, "vribs"),
                C(-5, 52, 5.5, 10, 8, 4, "metal_dark", {"top": "metal"}),
                C(-4, 50, 6.2, 2, 1.5, 3, "nozzle", {"down": "gold_bright"}),
                C(-1, 50, 6.2, 2, 1.5, 3, "nozzle", {"down": "gold_bright"}),
                C(2, 50, 6.2, 2, 1.5, 3, "nozzle", {"down": "gold_bright"}),
                C(-13.5, 57, -4, 6, 6, 7, "metal_dark"),
                C(7.5, 57, -4, 6, 6, 7, "metal_dark"),
            ]),
            B("chest_core", "torso", [0, 58, -7.5], None, [
                C(-3, 54, -6.9, 6, 5, 1.2, "chestring"),
            ]),
            B("face", "torso", [0, 64, -6], None, [
                C(-6, 61.5, -6.4, 12, 3.5, 0.6, "eye_twin"),
            ]),
            B("head", "torso", [0, 66, -1], None, [
                C(-6, 61, -6, 12, 9, 10, "black", {"front": "red_dark", "top": "red_dark"}),
                C(-5, 58, -3, 10, 2, 5, "metal_dark"),
            ]),
            B("head_crest", "head", [0, 71, -3], None, [
                C(-2, 69, -5, 4, 4, 6, "gold", {"top": "gold_bright"}),
                C(-0.5, 71.5, -4, 1, 3, 4, "gold_bright"),
            ], single=True),
            B("fin_l", "torso", [-10, 64, 7], [-30, 0, 0], [
                C(-12, 63, 6.2, 4, 6, 1.6, "black", {"back": "metal_dark"}),
                C(-12, 68.2, 6.2, 4, 1.2, 1.8, "gold", {"top": "gold_bright"}),
            ]),
            B("left_pauldron", "torso", [-18, 62, 0], None, [
                C(-23, 57, -5.5, 10, 7, 9, "black", {"west": "red_dark"}),
                C(-24, 56.5, -6, 3, 8, 10, "red_dark", {"west": "R"}),
            ]),
            B("prisma_l", "left_pauldron", [-19, 64, -3], None, [
                C(-20.5, 60, -4, 3, 4, 4, "prisma", {"top": "gold_bright"}),
            ]),
            B("left_arm_joint", "torso", [-20, 61, 0], None, [
                C(-24, 50, -4.5, 8, 9, 9, "black", {"front": "red_dark"}),
                C(-26.5, 50, -5, 3, 9, 10, "red_plate", {"west": "red_dark"}),
            ]),
            B("left_arm_joint2", "left_arm_joint", [-20, 47, 0], None, [
                C(-24.5, 36, -4, 8, 11, 8, "metal_dark", {"front": "metal"}),
                C(-25, 42.5, -4.8, 9, 2, 9.6, "coil"),
                C(-25, 40, -4.8, 9, 1.8, 9.6, "coil"),
                C(-23, 44, -4, 7, 6, 8, "metal_dark"),
            ]),
            B("left_hand", "left_arm_joint2", [-20, 31, 0], None, [
                C(-25.5, 23, -6, 11, 9, 12, "black", {"top": "red_dark", "front": "red_dark"}),
                C(-26.5, 27, -6.5, 2.5, 3, 13, "gold", {"west": "gold_bright"}),
            ]),
            B("fin_r", "torso", [10, 64, 7], [-30, 0, 0], [
                C(8, 63, 6.2, 4, 6, 1.6, "black", {"back": "metal_dark"}),
                C(8, 68.2, 6.2, 4, 1.2, 1.8, "gold", {"top": "gold_bright"}),
            ]),
            B("right_hip_joint", "the_omen", [4, 45, 0], None, []),
            B("right_thigh_joint", "right_hip_joint", [9, 45, 0], None, []),
            B("right_calf_joint", "right_thigh_joint", [9, 27, 0], None, []),
            B("right_foot_joint", "right_calf_joint", [9, 8, 0], None, []),
            B("right_pauldron", "torso", [18, 62, 0], None, []),
            B("prisma_r", "right_pauldron", [19, 64, -3], None, []),
            B("right_arm_joint", "torso", [20, 61, 0], None, []),
            B("right_arm_joint2", "right_arm_joint", [20, 47, 0], None, []),
            B("right_hand", "right_arm_joint2", [20, 31, 0], None, []),
        ],
        "mirror": [
            ("left_hip_joint", "right_hip_joint"), ("left_thigh_joint", "right_thigh_joint"),
            ("left_calf_joint", "right_calf_joint"), ("left_foot_joint", "right_foot_joint"),
            ("left_pauldron", "right_pauldron"), ("prisma_l", "prisma_r"),
            ("left_arm_joint", "right_arm_joint"), ("left_arm_joint2", "right_arm_joint2"),
            ("left_hand", "right_hand"), ("fin_l", "fin_r"),
        ],
    },
    "exo_4_titan": {
        "bones": [
            B("the_omen", None, [0, 0, 0], None, []),
            B("left_hip_joint", "the_omen", [-5, 45, 0], None, [
                C(-10, 39, -4.5, 9, 7, 9, "metal_dark"),
                C(-15, 35, -4.5, 6, 11, 9, "red_plate", {"west": "red_dark", "top": "black"}),
                C(-15, 44, -4.8, 2.2, 2, 9.6, "gold"),
            ]),
            B("left_thigh_joint", "left_hip_joint", [-11, 45, 0], None, [
                C(-17, 28, -5.5, 12, 15, 11, "red_plate", {"top": "red_dark", "back": "red_dark"}),
                C(-19.5, 29, -6, 3, 13, 12, "red_dark", {"west": "R"}),
                C(-17.5, 38, -6, 11, 3.5, 12, "gold"),
            ]),
            B("left_calf_joint", "left_thigh_joint", [-11, 27, 0], None, [
                C(-17, 9, -4.5, 12, 15, 9, "red_dark"),
                C(-17, 11, -6.5, 12, 12, 2.5, "black", {"front": "red_dark"}),
                C(-17, 20, -6.9, 12, 2, 0.8, "red_plate", {"front": "r"}),
                C(-15.5, 13, 4.5, 9, 9, 2.5, "black"),
                C(-14.5, 3, -3, 7, 9, 7, "metal_dark"),
            ]),
            B("left_foot_joint", "left_calf_joint", [-11, 8, 0], None, [
                C(-19, 0, -8, 16, 6, 13, "black", {"top": "metal_dark", "front": "red_dark"}),
                C(-18, 0, -11, 14, 3, 3.5, "gold", {"front": "gold_bright", "down": "G"}),
                C(-18, 0, 5.5, 14, 2, 2.5, "metal", {"back": "metal_dark"}),
            ]),
            B("hips", "the_omen", [0, 45, 0], None, [
                C(-11, 44, -5.5, 22, 4, 11, "black", {"front": "red_dark"}),
                C(-3, 44.5, -6, 6, 3, 1.2, "gold"),
            ]),
            B("torso", "hips", [0, 57, 0], None, [
                C(-14, 47, -6.5, 28, 11, 11, "red_plate", {"top": "black", "back": "red_dark"}),
                C(-12, 55.5, -7, 24, 5, 12, "black", {"front": "red_dark"}),
                C(-8, 60, -5, 16, 2.5, 9, "metal_dark"),
                C(-7, 49, -7.09, 14, 8, 0.7, "black"),
                C(-10, 50, -7.3, 20, 7, 0.7, "vribs"),
                C(-12, 47.5, -7.35, 4, 2, 0.6, "decal2"),
                C(-12, 50, 4.5, 24, 9, 3.5, "black", {"front": "metal_dark"}),
                C(-16, 56, -5, 7, 7, 8, "metal_dark"),
                C(9, 56, -5, 7, 7, 8, "metal_dark"),
            ]),
            B("face", "torso", [0, 62, -7], None, [
                C(-7, 59.5, -7.5, 14, 2.5, 0.7, "eye_duo"),
            ]),
            B("head", "torso", [0, 64, 0], None, [
                C(-8, 58, -7, 16, 8, 10, "black", {"front": "red_dark", "top": "red_dark"}),
                C(-8, 64, -7, 16, 2, 10, "red_plate", {"top": "R"}),
                C(-4, 57.5, -3, 8, 2, 6, "metal_dark"),
            ]),
            B("left_pauldron", "torso", [-22, 62, 0], None, [
                C(-30, 55, -8, 16, 9, 14, "black", {"west": "metal_dark", "front": "red_dark"}),
                C(-29, 56, -8.9, 14, 3, 1.5, "red_plate", {"front": "r"}),
                C(-27, 59.5, -8.8, 5, 4, 0.9, "gold", {"front": "gold_bright"}),
                C(-29.5, 63.8, -8, 15, 1.2, 14, "red_dark", {"top": "R"}),
            ]),
            B("left_arm_joint", "torso", [-23, 61, 0], None, [
                C(-28, 50, -5, 9, 9, 10, "black", {"front": "red_dark"}),
                C(-30.5, 50, -5.5, 3, 9, 11, "red_plate", {"west": "red_dark"}),
                C(-28.5, 49.5, -5.5, 9, 2.5, 11, "gold"),
            ]),
            B("left_arm_joint2", "left_arm_joint", [-23, 47, 0], None, [
                C(-28, 36, -5, 9, 11, 10, "metal_dark", {"front": "metal"}),
                C(-28, 44, -5.5, 9, 2.5, 11, "gold"),
                C(-26, 37, -2.5, 6, 4, 6, "metal"),
                C(-27, 43.5, -5, 9, 6, 10, "metal_dark"),
            ]),
            B("left_hand", "left_arm_joint2", [-23, 31, 0], None, [
                C(-31, 20, -7, 15, 12, 14, "black", {"top": "red_dark", "front": "red_dark"}),
                C(-29, 26, -8, 12, 3, 1.2, "gold", {"front": "gold_bright"}),
                C(-32, 22, -6.5, 2.5, 6, 13, "red_plate", {"west": "red_dark"}),
            ]),
            B("stack_l", "torso", [-14, 64, 9], [-14, 0, 0], [
                C(-19, 52, 7, 9, 14, 9, "stack", {"top": "black"}),
                C(-18.5, 64.5, 7.5, 8, 3, 8, "red_dark", {"top": "R"}),
                C(-18, 67.2, 8, 7, 1.5, 7, "black"),
            ]),
            B("right_hip_joint", "the_omen", [5, 45, 0], None, []),
            B("right_thigh_joint", "right_hip_joint", [11, 45, 0], None, []),
            B("right_calf_joint", "right_thigh_joint", [11, 27, 0], None, []),
            B("right_foot_joint", "right_calf_joint", [11, 8, 0], None, []),
            B("right_pauldron", "torso", [22, 62, 0], None, []),
            B("right_arm_joint", "torso", [23, 61, 0], None, []),
            B("right_arm_joint2", "right_arm_joint", [23, 47, 0], None, []),
            B("right_hand", "right_arm_joint2", [23, 31, 0], None, []),
            B("stack_r", "torso", [14, 64, 9], [-14, 0, 0], []),
        ],
        "mirror": [
            ("left_hip_joint", "right_hip_joint"), ("left_thigh_joint", "right_thigh_joint"),
            ("left_calf_joint", "right_calf_joint"), ("left_foot_joint", "right_foot_joint"),
            ("left_pauldron", "right_pauldron"), ("left_arm_joint", "right_arm_joint"),
            ("left_arm_joint2", "right_arm_joint2"), ("left_hand", "right_hand"),
            ("stack_l", "stack_r"),
        ],
    },
}

# ---------------------------------------------------------------------------
# animation builders (auth-space degrees, validated values from exo_plus / task 14)
# ---------------------------------------------------------------------------


def kf(*points):
    return {str(t): {"vector": list(v)} for t, v in points}


def rot(*points):
    return {"rotation": kf(*points)}


def scl(*points):
    return {"scale": kf(*points)}


def anim_idle(features, length):
    L = length
    bones = {
        "hips": rot((0, [0, 0, 0]), (L / 2, [1.5, 0, 0]), (L, [0, 0, 0])),
        "torso": rot((0, [2, 0, 0]), (L / 2, [4, 0, 0]), (L, [2, 0, 0])),
        "head": rot((0, [0, 0, 0]), (L / 2, [2, 0, 0]), (L, [0, 0, 0])),
        "left_arm_joint": rot((0, [0, 0, 0]), (L / 2, [3, 0, 0]), (L, [0, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (L / 2, [3, 0, 0]), (L, [0, 0, 0])),
        "left_arm_joint2": rot((0, [-8, 0, 0]), (L / 2, [-6, 0, 0]), (L, [-8, 0, 0])),
        "right_arm_joint2": rot((0, [-8, 0, 0]), (L / 2, [-6, 0, 0]), (L, [-8, 0, 0])),
        "left_hand": rot((0, [-4, 0, 0]), (L / 2, [-2, 0, 0]), (L, [-4, 0, 0])),
        "right_hand": rot((0, [-4, 0, 0]), (L / 2, [-2, 0, 0]), (L, [-4, 0, 0])),
    }
    if features["has_core"]:
        bones["chest_core"] = scl((0, [1, 1, 1]), (L / 2, [1.2, 1.2, 1.2]), (L, [1, 1, 1]))
    if features["has_exhaust"]:
        for p in ("back_exhaust_l", "back_exhaust_r"):
            bones[p] = rot((0, [0, 0, 0]), (L / 2, [1.5, 0, 0]), (L, [0, 0, 0]))
    if features["has_fin_head"]:
        bones["head_fin"] = rot((0, [0, 0, 0]), (L / 2, [5, 0, 0]), (L, [0, 0, 0]))
        bones["head"] = rot((0, [0, 0, 0]), (L / 3, [2, -6, 0]), (2 * L / 3, [2, 6, 0]), (L, [0, 0, 0]))
    if features["has_prisma"]:
        for p in ("prisma_l", "prisma_r"):
            bones[p] = scl((0, [1, 1, 1]), (L / 2, [1.12, 1.12, 1.12]), (L, [1, 1, 1]))
    if features["has_fin"]:
        for p in ("fin_l", "fin_r"):
            bones[p] = rot((0, [0, 0, 0]), (L / 2, [2, 0, 0]), (L, [0, 0, 0]))
    if features["has_stack"]:
        for p in ("stack_l", "stack_r"):
            bones[p] = rot((0, [0, 0, 0]), (L / 2, [1.5, 0, 0]), (L, [0, 0, 0]))
        bones["left_pauldron"] = rot((0, [0, 0, 0]), (L / 2, [1, 0, 0]), (L, [0, 0, 0]))
        bones["right_pauldron"] = rot((0, [0, 0, 0]), (L / 2, [1, 0, 0]), (L, [0, 0, 0]))
    return bones


def anim_walk(features, length):
    a = 18 if features["titan"] else 28
    c1, c2 = (-30, 10) if features["titan"] else (-40, 15)
    f1, f2 = (18, -10) if features["titan"] else (25, -15)
    arm = 16 if features["titan"] else (26 if features["light"] else 22)
    L = length
    q = L / 4
    bones = {
        "left_thigh_joint": rot((0, [0, 0, 0]), (q, [a, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [-a, 0, 0]), (L, [0, 0, 0])),
        "right_thigh_joint": rot((0, [0, 0, 0]), (q, [-a, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [a, 0, 0]), (L, [0, 0, 0])),
        "left_calf_joint": rot((0, [0, 0, 0]), (q, [c1, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [c2, 0, 0]), (L, [0, 0, 0])),
        "right_calf_joint": rot((0, [0, 0, 0]), (q, [c2, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [c1, 0, 0]), (L, [0, 0, 0])),
        "left_foot_joint": rot((0, [0, 0, 0]), (q, [f1, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [f2, 0, 0]), (L, [0, 0, 0])),
        "right_foot_joint": rot((0, [0, 0, 0]), (q, [f2, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [f1, 0, 0]), (L, [0, 0, 0])),
        "left_arm_joint": rot((0, [0, 0, 0]), (q, [-arm, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [arm, 0, 0]), (L, [0, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (q, [arm, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [-arm, 0, 0]), (L, [0, 0, 0])),
        "hips": rot((0, [0, 0, 0]), (q, [4, 0, 0]), (L / 2, [0, 0, 0]), (L * 0.75, [4, 0, 0]), (L, [0, 0, 0])),
        "torso": rot((0, [4, 0, 0]), (L, [4, 0, 0])),
        "left_hand": rot((0, [0, 0, 0]), (L / 2, [3, 0, 0]), (L, [0, 0, 0])),
        "right_hand": rot((0, [0, 0, 0]), (L / 2, [3, 0, 0]), (L, [0, 0, 0])),
    }
    if features["has_exhaust"]:
        for p in ("back_exhaust_l", "back_exhaust_r"):
            bones[p] = rot((0, [2, 0, 0]), (L / 2, [-1, 0, 0]), (L, [2, 0, 0]))
    return bones


def anim_attack(features, length):
    if features["double_fist"]:
        bones = {
            "left_arm_joint": rot((0, [0, 0, 0]), (length * 0.3, [60, 0, 0]), (length * 0.6, [-42, 0, 0]), (length * 0.85, [-8, 0, 0]), (length, [0, 0, 0])),
            "right_arm_joint": rot((0, [0, 0, 0]), (length * 0.3, [60, 0, 0]), (length * 0.6, [-42, 0, 0]), (length * 0.85, [-8, 0, 0]), (length, [0, 0, 0])),
            "left_arm_joint2": rot((0, [-8, 0, 0]), (length * 0.3, [30, 0, 0]), (length * 0.6, [-16, 0, 0]), (length, [-8, 0, 0])),
            "right_arm_joint2": rot((0, [-8, 0, 0]), (length * 0.3, [30, 0, 0]), (length * 0.6, [-16, 0, 0]), (length, [-8, 0, 0])),
            "hips": rot((0, [0, 0, 0]), (length * 0.6, [-2, 0, 0]), (length, [0, 0, 0])),
            "torso": rot((0, [2, 0, 0]), (length * 0.5, [-10, 0, 0]), (length, [2, 0, 0])),
            "head": rot((0, [0, 0, 0]), (length * 0.5, [-4, 0, 0]), (length, [0, 0, 0])),
        }
    else:
        bones = {
            "right_arm_joint": rot((0, [0, 0, 0]), (length * 0.2, [55, 0, 0]), (length * 0.5, [-45, 0, 0]), (length * 0.8, [-10, 0, 0]), (length, [0, 0, 0])),
            "right_arm_joint2": rot((0, [-8, 0, 0]), (length * 0.2, [28, 0, 0]), (length * 0.5, [-14, 0, 0]), (length, [-8, 0, 0])),
            "right_hand": rot((0, [0, 0, 0]), (length * 0.5, [-12, 0, 0]), (length, [0, 0, 0])),
            "left_arm_joint": rot((0, [0, 0, 0]), (length * 0.5, [6, 0, 0]), (length, [0, 0, 0])),
            "left_hand": rot((0, [0, 0, 0]), (length * 0.5, [-3, 0, 0]), (length, [0, 0, 0])),
            "torso": rot((0, [2, 0, 0]), (length * 0.5, [-8, 0, -8]), (length, [2, 0, 0])),
            "head": rot((0, [0, 0, 0]), (length * 0.5, [-6, 0, 0]), (length, [0, 0, 0])),
            "hips": rot((0, [0, 0, 0]), (length * 0.5, [-1, 0, 0]), (length, [0, 0, 0])),
        }
    if features["has_stack"]:
        for p in ("stack_l", "stack_r"):
            bones[p] = rot((0, [0, 0, 0]), (length * 0.5, [-4, 0, 0]), (length, [0, 0, 0]))
    return bones


def anim_hurt():
    return {
        "hips": rot((0, [0, 0, 0]), (0.3, [3, 0, 0]), (0.6, [0, 0, 0])),
        "torso": rot((0, [2, 0, 0]), (0.3, [8, 0, 0]), (0.6, [2, 0, 0])),
        "head": rot((0, [0, 0, 0]), (0.3, [10, 0, 0]), (0.6, [0, 0, 0])),
        "left_arm_joint": rot((0, [0, 0, 0]), (0.3, [-8, 0, 0]), (0.6, [0, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (0.3, [-8, 0, 0]), (0.6, [0, 0, 0])),
    }


def anim_death():
    return {
        "hips": rot((0, [0, 0, 0]), (1.3, [-45, 0, 0]), (2.0, [-45, 0, 0])),
        "torso": rot((0, [2, 0, 0]), (1.5, [-70, 0, 0]), (2.0, [-70, 0, 0])),
        "head": rot((0, [0, 0, 0]), (1.5, [14, 0, 0]), (2.0, [14, 0, 0])),
        "left_thigh_joint": rot((0, [0, 0, 0]), (1.3, [-18, 0, 0]), (2.0, [-18, 0, 0])),
        "right_thigh_joint": rot((0, [0, 0, 0]), (1.3, [-18, 0, 0]), (2.0, [-18, 0, 0])),
        "left_calf_joint": rot((0, [0, 0, 0]), (1.4, [55, 0, 0]), (2.0, [55, 0, 0])),
        "right_calf_joint": rot((0, [0, 0, 0]), (1.4, [55, 0, 0]), (2.0, [55, 0, 0])),
        "left_foot_joint": rot((0, [0, 0, 0]), (1.4, [-12, 0, 0]), (2.0, [-12, 0, 0])),
        "right_foot_joint": rot((0, [0, 0, 0]), (1.4, [-12, 0, 0]), (2.0, [-12, 0, 0])),
        "left_arm_joint": rot((0, [0, 0, 0]), (1.4, [40, 0, 0]), (2.0, [40, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (1.4, [40, 0, 0]), (2.0, [40, 0, 0])),
    }


def anim_punch(features, length):
    bones = {
        "right_arm_joint": rot((0, [0, 0, 0]), (length * 0.2, [28, 0, 0]), (length * 0.45, [-60, 0, 0]), (length * 0.7, [-32, 0, 0]), (length, [0, 0, 0])),
        "right_arm_joint2": rot((0, [-8, 0, 0]), (length * 0.2, [38, 0, 0]), (length * 0.45, [-8, 0, 0]), (length, [-8, 0, 0])),
        "right_hand": rot((0, [0, 0, 0]), (length * 0.45, [-14, 0, 0]), (length, [0, 0, 0])),
        "torso": rot((0, [2, 0, 0]), (length * 0.45, [-8, 10, 8]), (length, [2, 0, 0])),
        "head": rot((0, [0, 0, 0]), (length * 0.45, [-4, 0, 0]), (length, [0, 0, 0])),
        "hips": rot((0, [0, 0, 0]), (length * 0.45, [-1, 0, 0]), (length, [0, 0, 0])),
    }
    if features["has_stack"]:
        for p in ("stack_l", "stack_r"):
            bones[p] = rot((0, [0, 0, 0]), (length * 0.45, [-3, 0, 0]), (length, [0, 0, 0]))
    return bones


def anim_energy_shield(features):
    """Activation: back-cock -> thrust FORWARD (towards the face, -Z) -> held pose.
    1.5s covers the 30t duration of newer bases (older stop earlier, no harm)."""
    bones = {
        "hips": rot((0.0, [0, 0, 0]), (0.25, [3, 0, 0]), (0.5, [-5, 0, 0]), (1.1, [0, 0, 0]), (1.5, [0, 0, 0])),
        "torso": rot((0.0, [8, 0, 0]), (0.25, [-2, 0, 0]), (0.5, [-14, 0, 0]), (1.1, [-10, 0, 0]), (1.5, [8, 0, 0])),
        "head": rot((0.0, [-5, 0, 0]), (0.5, [4, 0, 0]), (1.1, [-2, 0, 0]), (1.5, [-5, 0, 0])),
        "left_arm_joint": rot((0.0, [0, 0, 0]), (0.15, [35, 0, 0]), (0.35, [-100, 0, -6]), (0.6, [-90, 0, -8]), (1.1, [-90, 0, -8]), (1.5, [0, 0, 0])),
        "right_arm_joint": rot((0.0, [0, 0, 0]), (0.15, [35, 0, 0]), (0.35, [-100, 0, 6]), (0.6, [-90, 0, 8]), (1.1, [-90, 0, 8]), (1.5, [0, 0, 0])),
        "left_arm_joint2": rot((0.0, [0, 0, 0]), (0.35, [-16, 0, 0]), (0.6, [-10, 0, 0]), (1.5, [0, 0, 0])),
        "right_arm_joint2": rot((0.0, [0, 0, 0]), (0.35, [-16, 0, 0]), (0.6, [-10, 0, 0]), (1.5, [0, 0, 0])),
        "left_hand": rot((0.0, [0, 0, 0]), (0.35, [-16, 0, 0]), (1.1, [-12, 0, 0]), (1.5, [0, 0, 0])),
        "right_hand": rot((0.0, [0, 0, 0]), (0.35, [-16, 0, 0]), (1.1, [-12, 0, 0]), (1.5, [0, 0, 0])),
    }
    if features["has_prisma"]:
        for p in ("prisma_l", "prisma_r"):
            bones[p] = scl((0.0, [1, 1, 1]), (0.5, [1.35, 1.35, 1.35]), (1.1, [1.2, 1.2, 1.2]), (1.5, [1, 1, 1]))
    if features["has_exhaust"]:
        for p in ("back_exhaust_l", "back_exhaust_r"):
            bones[p] = rot((0.0, [0, 0, 0]), (0.5, [-3, 0, 0]), (1.1, [-1.5, 0, 0]), (1.5, [0, 0, 0]))
    return bones


def anim_shield_hold(features):
    bones = {
        "hips": rot((0.0, [0, 0, 0]), (0.8, [-1, 0, 0]), (1.6, [0, 0, 0])),
        "torso": rot((0.0, [-10, 0, 0]), (0.8, [-12, 0, 0]), (1.6, [-10, 0, 0])),
        "head": rot((0.0, [2, 0, 0]), (0.8, [1, 0, 0]), (1.6, [2, 0, 0])),
        "left_arm_joint": rot((0.0, [-90, 0, -8]), (0.8, [-92, 0, -8]), (1.6, [-90, 0, -8])),
        "right_arm_joint": rot((0.0, [-90, 0, 8]), (0.8, [-92, 0, 8]), (1.6, [-90, 0, 8])),
        "left_arm_joint2": rot((0.0, [-10, 0, 0]), (0.8, [-12, 0, 0]), (1.6, [-10, 0, 0])),
        "right_arm_joint2": rot((0.0, [-10, 0, 0]), (0.8, [-12, 0, 0]), (1.6, [-10, 0, 0])),
        "left_hand": rot((0.0, [-12, 0, 0]), (0.8, [-13, 0, 0]), (1.6, [-12, 0, 0])),
        "right_hand": rot((0.0, [-12, 0, 0]), (0.8, [-13, 0, 0]), (1.6, [-12, 0, 0])),
    }
    if features["has_prisma"]:
        for p in ("prisma_l", "prisma_r"):
            bones[p] = scl((0.0, [1.1, 1.1, 1.1]), (0.8, [1.25, 1.25, 1.25]), (1.6, [1.1, 1.1, 1.1]))
    if features["has_exhaust"]:
        for p in ("back_exhaust_l", "back_exhaust_r"):
            bones[p] = rot((0.0, [-1.5, 0, 0]), (0.8, [-0.5, 0, 0]), (1.6, [-1.5, 0, 0]))
    return bones


def anim_slam(features):
    bones = {
        "left_arm_joint": rot((0, [0, 0, 0]), (0.3, [-130, 0, 0]), (0.62, [-40, 0, 0]), (0.85, [-8, 0, 0]), (1.1, [0, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (0.3, [-130, 0, 0]), (0.62, [-40, 0, 0]), (0.85, [-8, 0, 0]), (1.1, [0, 0, 0])),
        "left_arm_joint2": rot((0, [-8, 0, 0]), (0.3, [-20, 0, 0]), (0.62, [-18, 0, 0]), (1.1, [-8, 0, 0])),
        "right_arm_joint2": rot((0, [-8, 0, 0]), (0.3, [-20, 0, 0]), (0.62, [-18, 0, 0]), (1.1, [-8, 0, 0])),
        "left_hand": rot((0, [0, 0, 0]), (0.3, [10, 0, 0]), (0.62, [-12, 0, 0]), (1.1, [0, 0, 0])),
        "right_hand": rot((0, [0, 0, 0]), (0.3, [10, 0, 0]), (0.62, [-12, 0, 0]), (1.1, [0, 0, 0])),
        "hips": rot((0, [0, 0, 0]), (0.3, [4, 0, 0]), (0.62, [-6, 0, 0]), (0.85, [-2, 0, 0]), (1.1, [0, 0, 0])),
        "torso": rot((0, [2, 0, 0]), (0.3, [8, 0, 0]), (0.62, [-14, 0, 0]), (0.85, [-6, 0, 0]), (1.1, [2, 0, 0])),
        "head": rot((0, [0, 0, 0]), (0.3, [-4, 0, 0]), (0.62, [8, 0, 0]), (1.1, [0, 0, 0])),
        "left_thigh_joint": rot((0, [0, 0, 0]), (0.3, [12, 0, 0]), (0.62, [-14, 0, 0]), (1.1, [0, 0, 0])),
        "right_thigh_joint": rot((0, [0, 0, 0]), (0.3, [12, 0, 0]), (0.62, [-14, 0, 0]), (1.1, [0, 0, 0])),
        "left_calf_joint": rot((0, [0, 0, 0]), (0.3, [-14, 0, 0]), (0.62, [32, 0, 0]), (1.1, [0, 0, 0])),
        "right_calf_joint": rot((0, [0, 0, 0]), (0.3, [-14, 0, 0]), (0.62, [32, 0, 0]), (1.1, [0, 0, 0])),
        "left_foot_joint": rot((0, [0, 0, 0]), (0.3, [6, 0, 0]), (0.62, [-10, 0, 0]), (1.1, [0, 0, 0])),
        "right_foot_joint": rot((0, [0, 0, 0]), (0.3, [6, 0, 0]), (0.62, [-10, 0, 0]), (1.1, [0, 0, 0])),
    }
    if features["has_stack"]:
        for p in ("stack_l", "stack_r"):
            bones[p] = rot((0.0, [0, 0, 0]), (0.3, [5, 0, 0]), (0.62, [-6, 0, 0]), (1.1, [0, 0, 0]))
    if features["has_exhaust"]:
        for p in ("back_exhaust_l", "back_exhaust_r"):
            bones[p] = rot((0.0, [0, 0, 0]), (0.3, [4, 0, 0]), (0.62, [-5, 0, 0]), (1.1, [0, 0, 0]))
    return bones


def anim_chest_shot():
    return {
        "torso": rot((0.0, [2, 0, 0]), (0.25, [10, 0, 0]), (0.4, [18, 0, 0]), (0.6, [10, 0, 0]), (0.8, [2, 0, 0])),
        "head": rot((0.0, [0, 0, 0]), (0.4, [-6, 0, 0]), (0.8, [0, 0, 0])),
        "hips": rot((0.0, [0, 0, 0]), (0.4, [-2, 0, 0]), (0.8, [0, 0, 0])),
        "left_arm_joint": rot((0.0, [0, 0, 0]), (0.25, [-30, 0, -35]), (0.4, [-10, 0, -55]), (0.6, [-15, 0, -45]), (0.8, [0, 0, 0])),
        "right_arm_joint": rot((0.0, [0, 0, 0]), (0.25, [-30, 0, 35]), (0.4, [-10, 0, 55]), (0.6, [-15, 0, 45]), (0.8, [0, 0, 0])),
        "left_arm_joint2": rot((0.0, [-8, 0, 0]), (0.4, [-24, 0, 0]), (0.8, [-8, 0, 0])),
        "right_arm_joint2": rot((0.0, [-8, 0, 0]), (0.4, [-24, 0, 0]), (0.8, [-8, 0, 0])),
        "chest_core": scl((0.0, [1.0, 1.0, 1.0]), (0.4, [1.45, 1.45, 1.45]), (0.6, [1.15, 1.15, 1.15]), (0.8, [1.0, 1.0, 1.0])),
    }


def anim_dash(features):
    bones = {
        "hips": rot((0, [0, 0, 0]), (0.12, [-6, 0, 0]), (0.3, [-10, 0, 0]), (0.6, [0, 0, 0])),
        "torso": rot((0, [8, 0, 0]), (0.12, [-20, 0, 0]), (0.3, [-32, 0, 0]), (0.45, [-28, 0, 0]), (0.6, [8, 0, 0])),
        "head": rot((0, [-5, 0, 0]), (0.3, [14, 0, 0]), (0.6, [-5, 0, 0])),
        "left_thigh_joint": rot((0, [0, 0, 0]), (0.12, [-16, 0, 0]), (0.3, [-28, 0, 0]), (0.45, [-24, 0, 0]), (0.6, [0, 0, 0])),
        "right_thigh_joint": rot((0, [0, 0, 0]), (0.12, [14, 0, 0]), (0.3, [22, 0, 0]), (0.45, [18, 0, 0]), (0.6, [0, 0, 0])),
        "left_calf_joint": rot((0, [0, 0, 0]), (0.12, [20, 0, 0]), (0.3, [38, 0, 0]), (0.6, [0, 0, 0])),
        "right_calf_joint": rot((0, [0, 0, 0]), (0.12, [12, 0, 0]), (0.3, [18, 0, 0]), (0.6, [0, 0, 0])),
        "left_foot_joint": rot((0, [0, 0, 0]), (0.12, [-12, 0, 0]), (0.3, [-18, 0, 0]), (0.6, [0, 0, 0])),
        "right_foot_joint": rot((0, [0, 0, 0]), (0.12, [-8, 0, 0]), (0.3, [-8, 0, 0]), (0.6, [0, 0, 0])),
        "left_arm_joint": rot((0, [0, 0, 0]), (0.12, [35, 0, -4]), (0.3, [52, 0, -6]), (0.45, [46, 0, -6]), (0.6, [0, 0, 0])),
        "right_arm_joint": rot((0, [0, 0, 0]), (0.12, [35, 0, 4]), (0.3, [52, 0, 6]), (0.45, [46, 0, 6]), (0.6, [0, 0, 0])),
        "left_arm_joint2": rot((0, [0, 0, 0]), (0.3, [20, 0, 0]), (0.6, [0, 0, 0])),
        "right_arm_joint2": rot((0, [0, 0, 0]), (0.3, [20, 0, 0]), (0.6, [0, 0, 0])),
    }
    if features["has_stack"]:
        for p in ("stack_l", "stack_r"):
            bones[p] = rot((0.0, [0, 0, 0]), (0.3, [8, 0, 0]), (0.45, [-4, 0, 0]), (0.6, [0, 0, 0]))
    if features["has_prisma"]:
        for p in ("prisma_l", "prisma_r"):
            bones[p] = scl((0.0, [1.0, 1.0, 1.0]), (0.3, [1.2, 1.2, 1.2]), (0.6, [1.0, 1.0, 1.0]))
    if features["has_thruster"]:
        bones["back_thruster"] = scl((0.0, [1.0, 1.0, 1.0]), (0.3, [1.25, 1.25, 1.25]), (0.6, [1.0, 1.0, 1.0]))
    return bones


def features_for(key):
    if key == "exo_1_sentinel":
        return {"has_hand": True, "has_core": False, "has_exhaust": True, "has_fin_head": False,
                "has_prisma": False, "has_fin": False, "has_stack": False, "has_thruster": False,
                "titan": False, "light": False, "double_fist": False}
    if key == "exo_2_hunter":
        return {"has_hand": True, "has_core": True, "has_exhaust": False, "has_fin_head": True,
                "has_prisma": False, "has_fin": False, "has_stack": False, "has_thruster": True,
                "titan": False, "light": True, "double_fist": False}
    if key == "exo_3_vanguard":
        return {"has_hand": True, "has_core": True, "has_exhaust": False, "has_fin_head": False,
                "has_prisma": True, "has_fin": True, "has_stack": False, "has_thruster": False,
                "titan": False, "light": False, "double_fist": False}
    return {"has_hand": True, "has_core": False, "has_exhaust": False, "has_fin_head": False,
            "has_prisma": False, "has_fin": False, "has_stack": True, "has_thruster": False,
            "titan": True, "light": False, "double_fist": True}


IDLE_LEN = {"exo_1_sentinel": 2.4, "exo_2_hunter": 1.4, "exo_3_vanguard": 2.0, "exo_4_titan": 2.8}
WALK_LEN = {"exo_1_sentinel": 1.8, "exo_2_hunter": 1.0, "exo_3_vanguard": 1.4, "exo_4_titan": 2.2}
ATK_LEN = {"exo_1_sentinel": 0.9, "exo_2_hunter": 0.6, "exo_3_vanguard": 0.8, "exo_4_titan": 0.95}
PCH_LEN = {"exo_1_sentinel": 0.9, "exo_2_hunter": 0.6, "exo_3_vanguard": 0.9, "exo_4_titan": 1.0}


def frame_anims(key):
    features = features_for(key)
    anims = {
        "idle": {"loop": True, "animation_length": IDLE_LEN[key], "bones": anim_idle(features, IDLE_LEN[key])},
        "walk": {"loop": True, "animation_length": WALK_LEN[key], "bones": anim_walk(features, WALK_LEN[key])},
        "attack": {"loop": False, "animation_length": ATK_LEN[key], "bones": anim_attack(features, ATK_LEN[key])},
        "hurt": {"loop": False, "animation_length": 0.6, "bones": anim_hurt()},
        "death": {"loop": False, "animation_length": 2.0, "bones": anim_death()},
        "punch": {"loop": False, "animation_length": PCH_LEN[key], "bones": anim_punch(features, PCH_LEN[key])},
    }
    if key != "exo_2_hunter":
        shield_hold = {"loop": True, "animation_length": 1.6, "bones": anim_shield_hold(features)}
        # both names: newer bases use energy_shield_hold, older ones loop "block"
        anims["energy_shield"] = {"loop": False, "animation_length": 1.5, "bones": anim_energy_shield(features)}
        anims["energy_shield_hold"] = shield_hold
        anims["block"] = shield_hold
    if key in ("exo_1_sentinel", "exo_3_vanguard", "exo_4_titan"):
        anims["slam"] = {"loop": False, "animation_length": 1.1, "bones": anim_slam(features)}
    if key != "exo_1_sentinel":
        anims["dash"] = {"loop": False, "animation_length": 0.6, "bones": anim_dash(features)}
    if key == "exo_2_hunter":
        anims["chest_shot"] = {"loop": False, "animation_length": 0.8, "bones": anim_chest_shot()}
    return anims


# ---------------------------------------------------------------------------
# mirroring (left -> right, correct pivots, shared cube sizes)
# ---------------------------------------------------------------------------


def _mirror_name(n):
    if n.startswith("left_"):
        return "right_" + n[5:]
    if n.startswith("right_"):
        return "left_" + n[6:]
    if n.endswith("_l"):
        return n[:-2] + "_r"
    if n.endswith("_r"):
        return n[:-2] + "_l"
    return n


def mirror_bone(src, dst_name):
    """Copy a bone and its cubes with x mirrored: pivot.x -> -x, origin.x -> -(x+w)."""
    out = B(dst_name, _mirror_name(src["p"]), [-src["pivot"][0], src["pivot"][1], src["pivot"][2]],
            None if src["rot"] is None else [-src["rot"][0], src["rot"][1], src["rot"][2]], [])
    for c in src["cubes"]:
        o = c["o"]
        s = c["s"]
        out["cubes"].append(C(-o[0] - s[0], o[1], o[2], s[0], s[1], s[2], c["m"], c["faces"]))
    return out


def mirror_cubes(src):
    out = []
    for c in src["cubes"]:
        o = c["o"]
        s = c["s"]
        out.append(C(-o[0] - s[0], o[1], o[2], s[0], s[1], s[2], c["m"], c["faces"]))
    return out


def finalize_bones(spec):
    """Replace mirror-stub bones with mirrored geometry (parent remap stays)."""
    bones = {b["n"]: dict(b) for b in spec["bones"]}
    for left_name, right_name in spec["mirror"]:
        left = bones[left_name]
        if bones[right_name]["cubes"]:
            continue
        mir = mirror_bone(left, right_name)
        bones[right_name] = mir
    seen = set()
    lst = []
    for b in spec["bones"]:
        nb = bones[b["n"]]
        if nb["n"] in seen:
            continue
        seen.add(nb["n"])
        lst.append(nb)
    return lst


# ---------------------------------------------------------------------------
# atlas (FFD with 1px gap) + UV export
# ---------------------------------------------------------------------------

FACE_DIMS = {
    "north": lambda s: (s[0], s[1]),
    "south": lambda s: (s[0], s[1]),
    "east": lambda s: (s[2], s[1]),
    "west": lambda s: (s[2], s[1]),
    "up": lambda s: (s[0], s[2]),
    "down": lambda s: (s[0], s[2]),
}

FACE_NAMES = ["north", "south", "east", "west", "up", "down"]


def pack_cells(cells):
    """Shelf (row) packing, heights descending; returns placements dict or None."""
    order = sorted(range(len(cells)), key=lambda i: (-cells[i][1], -cells[i][0]))
    placements = {}
    shelf_y = 0
    shelf_end = 0
    x = 0
    row_h = 0
    for idx in order:
        w, h = cells[idx]
        if x + w + GAP > ATLAS:
            shelf_y = shelf_end + GAP
            x = 0
            row_h = 0
        if x + w + GAP > ATLAS or shelf_y + h + GAP > ATLAS:
            return None
        placements[idx] = (x, shelf_y)
        x += w + GAP
        row_h = max(row_h, h + GAP)
        shelf_end = shelf_y + row_h
    return placements


def build_frame(fkey):
    spec = FRAMES[fkey]
    bones = finalize_bones(spec)
    blevels = {b["n"]: b for b in bones}
    order = [b["n"] for b in bones]
    seed0 = hash(fkey) & 0x7FFFFF
    cells = []
    cell_owner = []
    for bni, bname in enumerate(order):
        bone = blevels[bname]
        for cci, c in enumerate(bone["cubes"]):
            for face in FACE_NAMES:
                w, h = FACE_DIMS[face](c["s"])
                w = max(1, int(round(w)))
                h = max(1, int(round(h)))
                cells.append((w, h))
                cell_owner.append((bname, cci, face))
    place = pack_cells(cells)
    if place is None:
        raise RuntimeError(f"{fkey}: atlas overflow ({len(cells)} cells)")

    from PIL import Image
    im = Image.new("RGBA", (ATLAS, ATLAS), (0, 0, 0, 0))
    px = im.load()
    for idx, (w, h) in enumerate(cells):
        bname, cci, face = cell_owner[idx]
        cube = None
        for b in blevels.values():
            if b["n"] == bname:
                cube = b["cubes"][cci]
                break
        if cube is None:
            raise RuntimeError(f"cube missing {(bname, cci)}")
        mat = cube["faces"].get(face, cube["m"])
        if mat in PAINTERS:
            rows = PAINTERS[mat](w, h, seed0 + cci * 31 + FACE_NAMES.index(face))
        elif len(mat) == 1 and mat in PALETTE:
            rows = [mat * w for _ in range(h)]
        else:
            raise RuntimeError(f"unknown painter {mat} for {(bname, cci)} face {face}")
        assert len(rows) == h, f"painter {mat} height mismatch {len(rows)} vs {h}"
        x0, y0 = place[idx]
        for yy in range(h):
            row = rows[yy]
            assert len(row) == w, f"painter {mat} width mismatch"
            for xx in range(w):
                ch = row[xx]
                if ch == ".":
                    continue
                px[x0 + xx, y0 + yy] = PALETTE[ch]
    return bones, order, im, cells, cell_owner, place


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def export_frame(fkey):
    bones, order, im, cells, cell_owner, place = build_frame(fkey)
    # geo
    geo_bones = []
    cube_uv = {}
    blist = {b["n"]: b for b in bones}
    cid = 0
    for b in bones:
        entry = {"name": b["n"], "pivot": list(b["pivot"])}
        if b["p"]:
            entry["parent"] = b["p"]
        if b["rot"]:
            entry["rotation"] = list(b["rot"])
        cubes = []
        for c in b["cubes"]:
            faces = {}
            for face in FACE_NAMES:
                w, h = FACE_DIMS[face](c["s"])
                w = max(1, int(round(w)))
                h = max(1, int(round(h)))
                x0, y0 = place[cid]
                faces[face] = {"uv": [x0, y0], "uv_size": [w, h]}
                cid += 1
            cubes.append({"origin": list(c["o"]), "size": list(c["s"]), "uv": faces})
        if cubes:
            entry["cubes"] = cubes
        geo_bones.append(entry)
    geo = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": f"geometry.{fkey}",
                    "texture_width": ATLAS,
                    "texture_height": ATLAS,
                },
                "bones": geo_bones,
            }
        ],
    }
    write_json(GEO_DIR / f"{fkey}.geo.json", geo)
    im.save(TEX_DIR / f"{fkey}.png")
    anims = frame_anims(fkey)
    anim_data = {"format_version": "1.8.0", "animations": anims}
    write_json(ANIM_DIR / f"{fkey}.animation.json", anim_data)
    # styles for the previewer
    styles_map = {}
    cid = 0
    for b in bones:
        cube_styles = []
        for c in b["cubes"]:
            faces = {}
            for face in FACE_NAMES:
                w, h = FACE_DIMS[face](c["s"])
                w = max(1, int(round(w)))
                h = max(1, int(round(h)))
                x0, y0 = place[cid]
                faces[face] = [x0, y0, w, h]
                cid += 1
            cube_styles.append({"o": list(c["o"]), "s": list(c["s"]), "m": c["m"],
                                "faces": c["faces"], "uv": faces})
        styles_map[b["n"]] = cube_styles
    styles = {
        "frame": fkey,
        "atlas": ATLAS,
        "bones": [
            {"name": b["n"], "parent": b["p"], "pivot": list(b["pivot"]), "rot": b["rot"],
             "cubes": styles_map[b["n"]]}
            for b in bones
        ],
    }
    STYLE_DIR.mkdir(parents=True, exist_ok=True)
    (STYLE_DIR / f"styles_{fkey}.json").write_text(
        json.dumps(styles, indent=1), encoding="utf-8")
    return bones, anims, len(cells)


# ---------------------------------------------------------------------------
# QA
# ---------------------------------------------------------------------------


def qa_frame(fkey, bones, anims):
    ok = True
    names = [b["n"] for b in bones]
    # 1) every animated bone exists
    for anim_name, anim in anims.items():
        for bone in anim["bones"]:
            if bone not in names:
                print(f"QA FAIL {fkey}: anim '{anim_name}' uses missing bone '{bone}'")
                ok = False
    # 2) poses: soles on y=0 (only feet cubes touch 0), height <= 76
    min_y = 1e9
    max_y = -1e9
    for b in bones:
        for c in b["cubes"]:
            min_y = min(min_y, c["o"][1])
            max_y = max(max_y, c["o"][1] + c["s"][1])
    if abs(min_y) > 0.01 or max_y > 76:
        print(f"QA FAIL {fkey}: sole y={min_y}, top y={max_y}")
        ok = False
    # 3) mirror: left/right pivot symmetric, cube counts equal
    lefts = {"left_hip_joint": "right_hip_joint", "left_thigh_joint": "right_thigh_joint",
             "left_calf_joint": "right_calf_joint", "left_foot_joint": "right_foot_joint",
             "left_pauldron": "right_pauldron", "left_arm_joint": "right_arm_joint",
             "left_arm_joint2": "right_arm_joint2", "left_hand": "right_hand"}
    pairs = lefts | {p[0]: p[1] for p in FRAMES[fkey]["mirror"] if p[0] in names}
    for lname, rname in pairs.items():
        lb = next((b for b in bones if b["n"] == lname), None)
        rb = next((b for b in bones if b["n"] == rname), None)
        if lb is None or rb is None:
            if (lb is None) != (rb is None):
                print(f"QA FAIL {fkey}: mirror pair {lname}/{rname} asymmetric existence")
                ok = False
            continue
        if abs(lb["pivot"][0] + rb["pivot"][0]) > 0.01:
            print(f"QA FAIL {fkey}: pivot x not mirrored for {lname}")
            ok = False
        if len(lb["cubes"]) != len(rb["cubes"]):
            print(f"QA FAIL {fkey}: cube count mismatch {lname}/{rname}")
            ok = False
    # 4) chest_core only where beam exists (E2/E3)
    has_core = "chest_core" in names
    want_core = fkey in ("exo_2_hunter", "exo_3_vanguard")
    if has_core != want_core:
        print(f"QA FAIL {fkey}: chest_core {'present but frame has no beam' if has_core else 'missing'}")
        ok = False
    # 5) DANGER stripes (alternating runs >= 6) inside 128px slice of atlas paint
    return ok


def check_danger(fkey):
    """Scan generated texture for 1px checkerboard noise (2-cycle runs >= 6 px)."""
    from PIL import Image
    im = Image.open(TEX_DIR / f"{fkey}.png").convert("RGBA")
    px = im.load()
    bad = 0
    for y in range(im.height):
        row = [px[x, y] for x in range(im.width)]
        x = 2
        while x < len(row):
            if row[x] == row[x - 2] and row[x] != row[x - 1]:
                s = x - 2
                e = x
                while e + 1 < len(row) and row[e + 1] == row[s + ((e + 1 - s) % 2)]:
                    e += 1
                length = e - s + 1
                if length >= 6 and all(c[3] > 0 for c in row[s:e + 1]):
                    bad += 1
                    print(f"  DANGER {fkey} y={y} x={s} len={length} cols={sorted(set(c[:3] for c in row[s:e+1]))}")
                x = e + 1
            else:
                x += 1
    return bad


def main():
    total_cells = 0
    for fkey in sorted(FRAMES):
        bones, anims, ncell = export_frame(fkey)
        ok = qa_frame(fkey, bones, anims)
        danger = check_danger(fkey)
        print(f"== {fkey}: bones={len(bones)} cubes={sum(len(b['cubes']) for b in bones)} "
              f"cells={ncell} danger={danger} bonesOK={ok}")
        total_cells += ncell
    print(f"total atlas cells: {total_cells}")


if __name__ == "__main__":
    main()
