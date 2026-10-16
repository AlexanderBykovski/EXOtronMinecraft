#!/usr/bin/env python3
"""Full from-scratch rebuild of the two Japanese-warrior rigs.

red_shogun  -> SamuraiEntity   (GeoModel, renderer scale 1.13, hitbox 2.34)
dark_ninja  -> BlackNinjaEntity (GeoModel, renderer scale 0.93, hitbox 1.8)

Conventions (match project's verified framework):
- entity front = -Z (north face of cubes); right side = -X, left = +X
- animation keyframes: bedrock degrees, absolute per bone
Run from repo root:  python3 scripts/gen_mob_rework/japan.py
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import (Model, build_anim, track, h01, vnoise, mix, shade, c01,
                       noisy, grad_v, edge_darken)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
A = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'opusvsexe')

# ------------------------------------------------------------------ palettes
SHOGUN = {
    'crimson':    (128, 28, 26), 'crimson_hi': (166, 48, 38), 'crimson_dk': (84, 16, 16),
    'crimson_dp': (54, 10, 12),
    'iron':       (30, 30, 34), 'iron_hi': (54, 54, 60), 'iron_dk': (18, 18, 22),
    'indigo':     (38, 44, 70), 'indigo_hi': (52, 60, 92), 'indigo_dk': (26, 30, 50),
    'gold':       (186, 152, 74), 'gold_hi': (224, 192, 110), 'gold_dk': (126, 98, 46),
    'skin':       (196, 150, 108), 'skin_dk': (162, 118, 82), 'skin_hi': (216, 174, 130),
    'hair':       (36, 28, 22),
    'steel':      (150, 156, 166),
    'straw':      (196, 172, 118), 'straw_dk': (156, 134, 86),
    'leather':    (74, 52, 32), 'leather_hi': (98, 70, 44), 'leather_dk': (48, 33, 20),
    'bone_w':     (226, 220, 204),
}
NINJA = {
    'char':       (30, 32, 38), 'char_hi': (44, 47, 55), 'char_dk': (20, 21, 26),
    'char_dd':    (14, 15, 18),
    'bluegray':   (52, 58, 72), 'bluegray_hi': (68, 75, 92), 'bluegray_dk': (34, 38, 50),
    'indigo':     (34, 38, 58), 'indigo_hi': (46, 51, 74), 'indigo_dk': (22, 25, 40),
    'slate':      (64, 70, 84), 'slate_hi': (84, 90, 104), 'slate_dk': (44, 48, 60),
    'leather':    (66, 48, 30), 'leather_hi': (88, 64, 40), 'leather_dk': (44, 32, 20),
    'iron':       (92, 96, 104), 'iron_hi': (116, 120, 128), 'iron_dk': (64, 68, 76),
    'skin':       (196, 150, 108), 'skin_dk': (160, 118, 84),
    'eye':        (58, 42, 26), 'eye_core': (30, 20, 12),
}

# ------------------------------------------------------------------ painters
def solid(c):
    def p(x, y, w, h, face):
        return c
    return p

def lacquer(base, hi, dk, seam, seed=1):
    def p(x, y, w, h, face):
        n = vnoise(x * 0.7, y, seed, 2)
        c = base
        if n > 0.66:
            c = mix(base, hi, 0.5)
        elif n < 0.3:
            c = mix(base, dk, 0.55)
        if y == 0:
            c = hi
        elif y == 1:
            c = mix(base, hi, 0.25)
        elif y == h - 1:
            c = seam
        if x == 0:
            c = mix(c, dk, 0.35)
        return c
    return p

def lamellar(base, hi, dk, iron, lacing, seed=2):
    def p(x, y, w, h, face):
        row = y % 6
        if row in (0, 1):
            c = mix(base, hi, 0.55 if row == 0 else 0.25)
        elif row == 3:
            c = lacing
        elif row == 4:
            c = mix(base, dk, 0.5)
        elif row == 5:
            c = mix(base, dk, 0.25)
        else:
            c = base
        if h01(x, y, seed) > 0.93:
            c = mix(c, iron, 0.75)
        if x == 0 or x == w - 1:
            c = mix(c, iron, 0.5)
        return c
    return p

def cloth(base, dk, hi, seed=3, fold=4):
    def p(x, y, w, h, face):
        n = vnoise(x, y // fold, seed, 2)
        if n > 0.62:
            c = mix(base, hi, 0.4)
        elif n < 0.34:
            c = mix(base, dk, 0.5)
        else:
            c = base
        return c
    return p

def leather(base, hi, dk, seed=5):
    def p(x, y, w, h, face):
        n = h01(x, y, seed)
        c = base
        if n > 0.86:
            c = hi
        elif n < 0.16:
            c = dk
        if y == 0:
            c = hi
        if y == h - 1:
            c = dk
        return c
    return p

def metal(base, hi, dk, seed=7, scratches=0.05):
    def p(x, y, w, h, face):
        n = h01(x, y, seed)
        c = base
        if y == 0 or n > 0.9:
            c = hi
        elif y == h - 1 or n < 0.12:
            c = dk
        if h01(x, y, seed + 3) < scratches:
            c = mix(c, hi, 0.6)
        return c
    return p

def straw(base, dk, seed=9):
    def p(x, y, w, h, face):
        c = base if (x + y) % 2 == 0 else mix(base, dk, 0.6)
        if h01(x, y, seed) > 0.92:
            c = dk
        return c
    return p

# ---------------------------------------------------------- shogun details
def mon():
    g, g_hi, g_dk = SHOGUN['gold'], SHOGUN['gold_hi'], SHOGUN['gold_dk']
    def p(x, y, w, h, face):
        if face != 'north':
            return g
        cx, cy = (w - 1) / 2, (h - 1) / 2
        d = max(abs(x - cx), abs(y - cy))
        if d < 0.9:
            return (30, 22, 14)
        if d < 1.3:
            return g_hi
        return g if (x + y) % 2 == 0 else g_dk
    return p

def knot():
    l, l_hi, l_dk = SHOGUN['leather'], SHOGUN['leather_hi'], SHOGUN['leather_dk']
    def p(x, y, w, h, face):
        c = l
        if (x + y) % 3 == 0:
            c = l_hi
        if y == 0 or x == 0:
            c = l_hi
        if y == h - 1:
            c = l_dk
        return c
    return p

def kabuto_bowl():
    red, red_hi, red_dk = SHOGUN['crimson'], SHOGUN['crimson_hi'], SHOGUN['crimson_dk']
    iron, iron_hi, gold = SHOGUN['iron'], SHOGUN['iron_hi'], SHOGUN['gold']
    def p(x, y, w, h, face):
        n = vnoise(x, y, 71, 2)
        if n > 0.6:
            c = mix(red, red_hi, 0.5)
        elif n < 0.3:
            c = mix(red, red_dk, 0.5)
        else:
            c = red
        if x % 4 == 0:
            c = mix(c, iron, 0.55)
        if y == 0:
            c = mix(red_hi, gold, 0.3)
        if y == h - 1:
            c = red_dk
        if h01(x, y, 73) > 0.95:
            c = gold
        return c
    return p

def gold_m(seed=1):
    g, g_hi, g_dk = SHOGUN['gold'], SHOGUN['gold_hi'], SHOGUN['gold_dk']
    def p(x, y, w, h, face):
        n = h01(x, y, seed)
        c = g
        if n > 0.75:
            c = g_hi
        elif n < 0.2:
            c = g_dk
        if y == 0:
            c = g_hi
        if y == h - 1:
            c = g_dk
        return c
    return p

def kote(seed=1):
    red, red_dk = SHOGUN['crimson'], SHOGUN['crimson_dp']
    iron, iron_hi, iron_dk = SHOGUN['iron'], SHOGUN['iron_hi'], SHOGUN['iron_dk']
    def p(x, y, w, h, face):
        c = mix(red, red_dk, 0.4)
        if y % 4 == 0:
            c = mix(c, iron, 0.6)
        if h01(x, y, seed) > 0.93:
            c = iron_hi
        if y == h - 1:
            c = iron_dk
        return c
    return p

def haidate(seed=1):
    red, red_hi, red_dk = SHOGUN['crimson'], SHOGUN['crimson_hi'], SHOGUN['crimson_dk']
    def p(x, y, w, h, face):
        row = y % 5
        if row == 0:
            c = red_hi
        elif row == 2:
            c = mix(red, SHOGUN['iron'], 0.35)
        elif row == 3:
            c = red_dk
        else:
            c = red
        if h01(x, y, seed) > 0.94:
            c = SHOGUN['gold']
        return c
    return p

def suneate(seed=1):
    iron, iron_hi, iron_dk = SHOGUN['iron'], SHOGUN['iron_hi'], SHOGUN['iron_dk']
    def p(x, y, w, h, face):
        if x % 3 == 1:
            c = mix(iron_hi, (200, 205, 212), 0.3)
        elif x % 3 == 2:
            c = iron_dk
        else:
            c = iron
        if h01(x, y, seed) > 0.95:
            c = SHOGUN['gold']
        return c
    return p

def scabbard(seed=1):
    iron_dk, iron = SHOGUN['iron_dk'], SHOGUN['iron']
    def p(x, y, w, h, face):
        c = iron_dk
        if h01(x, y, seed) > 0.85:
            c = iron
        if y in (2, h - 3) and face in ('east', 'west'):
            c = SHOGUN['crimson_dk']
        if y == 0:
            c = iron
        return c
    return p

def tsuka():
    iron_dk = SHOGUN['iron_dk']
    def p(x, y, w, h, face):
        return SHOGUN['crimson'] if (x + y) % 4 in (0, 1) else iron_dk
    return p

def face_shogun():
    skin, skin_dk, skin_hi = SHOGUN['skin'], SHOGUN['skin_dk'], SHOGUN['skin_hi']
    hair, steel = SHOGUN['hair'], SHOGUN['steel']
    def p(x, y, w, h, face):
        if face != 'north':
            return cloth(skin, skin_dk, skin_hi, 41)(x, y, w, h, face)
        c = mix(skin, skin_dk, 0.1 + 0.35 * (y / max(1, h - 1)))
        if y <= 1:
            c = mix(skin, skin_hi, 0.5)
        if y == 2 and h01(x, 9, 44) > 0.6:
            c = mix(c, skin_dk, 0.4)
        # brows (y=3) + focused eyes (y=4-5)
        if y == 3 and (2 <= x <= 3 or w - 4 <= x <= w - 3):
            c = hair
        if y == 4 and (1 <= x <= 2 or 5 <= x <= 6):
            c = hair
        if y == 5:
            if x == 1:
                c = steel
            if x == 2:
                c = (240, 240, 240)
            if x == 5:
                c = (240, 240, 240)
            if x == 6:
                c = steel
        return c
    return p

def menpo():
    red, red_hi, red_dk = SHOGUN['crimson'], SHOGUN['crimson_hi'], SHOGUN['crimson_dp']
    hair, iron_dk, iron = SHOGUN['hair'], SHOGUN['iron_dk'], SHOGUN['iron']
    def p(x, y, w, h, face):
        if face != 'north':
            return lacquer(red, red_hi, red_dk, red_dk, 51)(x, y, w, h, face)
        c = lacquer(red, red_hi, red_dk, red_dk, 51)(x, y, w, h, face)
        if y == 1 and 0.2 * w <= x <= 0.8 * w:
            c = hair
        if y == 2 and h01(x, y, 55) > 0.72:
            c = iron_dk
        return c
    return p

# ----------------------------------------------------------- ninja details
def quilt(base, hi, dk, seed=1):
    def p(x, y, w, h, face):
        if (x + y) % 4 == 0:
            c = mix(base, dk, 0.7)
        elif (x + y) % 4 == 2:
            c = mix(base, hi, 0.35)
        else:
            c = base
        if h01(x, y, seed) > 0.9:
            c = hi
        return c
    return p

def jacket():
    char, char_hi, char_dk = NINJA['char'], NINJA['char_hi'], NINJA['char_dk']
    indigo_hi = NINJA['indigo_hi']
    def p(x, y, w, h, face):
        n = vnoise(x, y, 21, 2)
        if n > 0.62:
            c = mix(char, char_hi, 0.4)
        elif n < 0.3:
            c = mix(char, char_dk, 0.55)
        else:
            c = char
        if face == 'north':
            cx = abs(x - (w - 1) / 2)
            if abs(cx - y * 0.42) < 0.8 and y < h * 0.55:
                c = indigo_hi if (x + y) % 2 else mix(indigo_hi, char_dk, 0.5)
            elif y >= h * 0.55 and cx < 0.8:
                c = char_dk
        if y == h - 1:
            c = char_dk
        return c
    return p

def hood(seed=1):
    char, char_hi, char_dk = NINJA['char'], NINJA['char_hi'], NINJA['char_dk']
    def p(x, y, w, h, face):
        n = vnoise(x + seed, y, seed, 2)
        if n > 0.64:
            c = mix(char, char_hi, 0.35)
        elif n < 0.3:
            c = mix(char, char_dk, 0.6)
        else:
            c = char
        if y == 0:
            c = mix(c, char_hi, 0.3)
        if y == h - 1:
            c = char_dk
        return c
    return p

def mask():
    char, char_hi, char_dk = NINJA['char'], NINJA['char_hi'], NINJA['char_dd']
    def p(x, y, w, h, face):
        c = cloth(char, char_dk, char_hi, 45, 2)(x, y, w, h, face)
        if y == 1 and h01(x, 1, 47) > 0.6:
            c = char_dk
        if y == h - 1:
            c = char_dk
        return c
    return p

def wrap(seed=1):
    slate, slate_hi, slate_dk = NINJA['slate'], NINJA['slate_hi'], NINJA['slate_dk']
    def p(x, y, w, h, face):
        band = (x + y) // 2 % 3
        c = [slate, mix(slate, slate_hi, 0.4), mix(slate, slate_dk, 0.5)][band]
        if h01(x, y, seed) > 0.94:
            c = slate_dk
        return c
    return p

def face_ninja():
    skin, skin_dk = NINJA['skin'], NINJA['skin_dk']
    char, char_dk = NINJA['char'], NINJA['char_dk']
    def p(x, y, w, h, face):
        if face != 'north':
            return cloth(char, NINJA['char_dd'], char_dk, 63, 2)(x, y, w, h, face)
        c = cloth(char, NINJA['char_dd'], char_dk, 63, 2)(x, y, w, h, face)
        # exposed eye strip = rows 3..4 (between face_mask and brow band)
        if y in (3, 4):
            c = skin
            if y == 3 and h01(x, 7, 61) > 0.85:
                c = skin_dk
        for ex in (int(w * 0.18), int(w * 0.6)):
            if y == 3 and ex <= x <= ex + 1:
                c = NINJA['eye']
            if y == 4 and ex <= x <= ex + 1:
                c = NINJA['eye_core'] if x == ex else (240, 240, 240)
        return c
    return p

# ==================================================================
# GEOMETRY
# ==================================================================
def build_shogun():
    S = SHOGUN
    m = Model('red_shogun', 256, 256, visible_bounds=(7, 7))

    red_lac = lambda s=1: lacquer(S['crimson'], S['crimson_hi'], S['crimson_dk'], S['crimson_dp'], s)
    lam = lambda s=2: lamellar(S['crimson'], S['crimson_hi'], S['crimson_dk'], S['iron'], S['crimson_dp'], s)
    indi = lambda s=3: cloth(S['indigo'], S['indigo_dk'], S['indigo_hi'], s)
    iron_m = lambda s=7: metal(S['iron'], S['iron_hi'], S['iron_dk'], s)
    lthr = lambda s=6: leather(S['leather'], S['leather_hi'], S['leather_dk'], s)

    m.bone('root', [0, 0, 0])
    m.bone('master', [0, 13, 0], 'root')

    # ---------------- body ----------------
    m.bone('body', [0, 13, 0], 'master', cubes=[
        {'o': [-4.2, 0.0, -2.7], 's': [8.4, 11.2, 5.4], 'paint': indi(11)},
        {'o': [-1.9, 9.9, -2.95], 's': [3.8, 1.4, 0.7], 'paint': solid(S['bone_w'])},
        {'o': [-4.4, 6.4, -3.0], 's': [8.8, 2.4, 6.0], 'paint': indi(13)},
    ])
    m.bone('chest_armor', [0, 13, 0], 'body', cubes=[
        {'o': [-4.6, 1.2, -3.05], 's': [9.2, 5.6, 6.1], 'paint': lam(21)},
        {'o': [-4.5, 4.9, -3.0], 's': [9.0, 3.6, 6.0], 'paint': lam(23)},
        {'o': [-3.7, 7.8, -2.9], 's': [7.4, 1.9, 5.8], 'paint': red_lac(25)},
        {'o': [1.75, 8.3, -3.55], 's': [1.5, 1.5, 0.45], 'paint': mon()},
        {'o': [-3.25, 8.3, -3.55], 's': [1.5, 1.5, 0.45], 'paint': mon()},
        {'o': [-3.2, 3.4, 2.85], 's': [6.4, 5.6, 0.6], 'paint': red_lac(27)},
        {'o': [-2.6, 4.2, 3.4], 's': [0.5, 4.2, 0.3], 'paint': lthr(29)},
        {'o': [2.1, 4.2, 3.4], 's': [0.5, 4.2, 0.3], 'paint': lthr(31)},
    ])
    m.bone('waist_belt', [0, 13, 0], 'body', cubes=[
        {'o': [-4.7, 6.0, -3.15], 's': [9.4, 1.7, 6.3], 'paint': lthr(33)},
        {'o': [-1.3, 5.9, -3.75], 's': [2.6, 1.9, 0.8], 'paint': knot()},
    ])
    m.bone('kusazuri_front', [0, 20.3, -3.0], 'body', rot=[-6, 0, 0], cubes=[
        {'o': [-3.5, -1.7, -0.4], 's': [7.0, 1.7, 0.7], 'paint': lam(35)},
        {'o': [-3.2, -3.4, -0.25], 's': [6.4, 1.8, 0.6], 'paint': lam(37)},
    ])
    m.bone('kusazuri_back', [0, 20.3, 3.0], 'body', rot=[6, 0, 0], cubes=[
        {'o': [-3.5, -1.7, -0.3], 's': [7.0, 1.7, 0.7], 'paint': lam(39)},
        {'o': [-3.2, -3.4, -0.15], 's': [6.4, 1.8, 0.6], 'paint': lam(41)},
    ])
    m.bone('kusazuri_left', [4.75, 20.3, 0], 'body', rot=[0, 0, -7], cubes=[
        {'o': [-0.4, -1.7, -3.3], 's': [0.7, 1.7, 6.6], 'paint': lam(43)},
        {'o': [-0.3, -3.4, -3.0], 's': [0.6, 1.8, 6.0], 'paint': lam(45)},
    ])
    m.bone('kusazuri_right', [-4.75, 20.3, 0], 'body', rot=[0, 0, 7], cubes=[
        {'o': [-0.3, -1.7, -3.3], 's': [0.7, 1.7, 6.6], 'paint': lam(47)},
        {'o': [-0.3, -3.4, -3.0], 's': [0.6, 1.8, 6.0], 'paint': lam(49)},
    ])

    # ---------------- head ----------------
    m.bone('head', [0, 24.6, 0], 'master', cubes=[
        {'o': [-4.0, 0.0, -4.0], 's': [8, 8, 8], 'paint': face_shogun()},
    ])
    m.bone('menpo', [0, 24.6, 0], 'head', cubes=[
        {'o': [-3.6, 0.5, -4.8], 's': [7.2, 3.0, 1.25], 'paint': menpo()},
        {'o': [-0.6, 3.4, -4.75], 's': [1.2, 2.2, 0.75],
         'paint': lacquer(S['crimson_dk'], S['crimson'], S['crimson_dp'], S['crimson_dp'], 53)},
    ])
    m.bone('kabuto', [0, 24.6, 0], 'head', cubes=[
        {'o': [-4.8, 6.9, -4.8], 's': [9.6, 4.3, 9.6], 'paint': kabuto_bowl()},
        {'o': [-5.2, 5.9, -5.2], 's': [10.4, 1.15, 10.4], 'paint': iron_m(57)},
    ])
    m.bone('shikoro', [0, 30.4, 0], 'head', rot=[5, 0, 0], cubes=[
        {'o': [-4.5, -1.3, 3.2], 's': [9.0, 2.3, 1.5], 'paint': lam(59)},
        {'o': [-4.0, -3.6, 4.1], 's': [8.0, 2.3, 1.2], 'paint': lam(61)},
        {'o': [4.15, -1.3, -3.4], 's': [1.4, 2.3, 6.9], 'paint': lam(63)},
        {'o': [-5.55, -1.3, -3.4], 's': [1.4, 2.3, 6.9], 'paint': lam(65)},
    ])
    m.bone('helmet_crest', [0, 33.3, -5.1], 'head', cubes=[
        {'o': [-0.95, 0.2, -0.5], 's': [1.9, 3.4, 1.0], 'paint': gold_m(67)},
        {'o': [-0.9, 2.6, -0.5], 's': [1.8, 2.6, 1.0], 'paint': gold_m(69), 'rot': [0, 0, 30]},
        {'o': [-0.9, 2.6, -0.5], 's': [1.8, 2.6, 1.0], 'paint': gold_m(71), 'rot': [0, 0, -30]},
        {'o': [-0.85, 4.9, -0.45], 's': [1.7, 1.7, 0.9], 'paint': gold_m(73), 'rot': [0, 0, 60]},
        {'o': [-0.85, 4.9, -0.45], 's': [1.7, 1.7, 0.9], 'paint': gold_m(75), 'rot': [0, 0, -60]},
        {'o': [-0.75, 1.3, -1.1], 's': [1.5, 1.5, 0.4], 'paint': mon()},
    ])

    # ---------------- arms (hands EMPTY) ----------------
    for side, x in (('right', -6.4), ('left', 6.4)):
        r = side == 'right'
        sx = -1 if r else 1
        seed0 = 81 if r else 83
        m.bone(side + '_arm', [x, 22.8, 0], 'master', cubes=[
            {'o': [min(-1.55 * 1, sx * -1.55) if r else -2.35, -6.3, -2.05], 's': [3.9, 6.1, 4.2], 'paint': indi(seed0)},
            {'o': [(-2.0 if r else -3.0), -6.9, -2.6], 's': [5.0, 4.3, 5.2], 'paint': lam(seed0 + 4)},
            {'o': [(-1.8 if r else -2.8), -8.7, -2.4], 's': [4.6, 1.9, 4.8], 'paint': lam(seed0 + 8)},
            {'o': [(-1.45 if r else -2.35), -12.4, -2.15], 's': [3.8, 3.8, 4.3], 'paint': kote(seed0 + 12)},
            {'o': [(-1.5 if r else -2.4), -13.15, -2.2], 's': [3.9, 0.75, 4.4], 'paint': iron_m(seed0 + 16)},
            {'o': [(-1.25 if r else -2.05), -15.25, -1.9], 's': [3.3, 2.1, 3.8],
             'paint': leather(S['leather_dk'], S['leather'], (28, 18, 12), seed0 + 20)},
        ])

    # ---------------- legs ----------------
    for side, x in (('right', -2.4), ('left', 2.4)):
        seed0 = 111 if side == 'right' else 113
        m.bone(side + '_leg', [x, 13, 0], 'master', cubes=[
            {'o': [-2.0, -12.0, -2.1], 's': [4.0, 11.2, 4.3], 'paint': indi(seed0)},
            {'o': [-2.15, -8.2, -2.55], 's': [4.3, 4.9, 5.0], 'paint': haidate(seed0 + 4)},
            {'o': [-1.85, -6.4, -2.8], 's': [3.7, 5.9, 1.15], 'paint': suneate(seed0 + 8)},
            {'o': [-2.0, -12.55, -2.7], 's': [4.0, 1.5, 5.4],
             'paint': leather(S['leather_dk'], S['leather'], (28, 18, 12), seed0 + 12)},
            {'o': [-2.05, -13.0, -2.95], 's': [4.1, 0.5, 5.8], 'paint': straw(S['straw'], S['straw_dk'], seed0 + 16)},
        ])

    # ---------------- daisho (left hip) ----------------
    m.bone('equipment', [0, 13, 0], 'master')
    m.bone('katana_scabbard', [5.5, 17.6, 3.4], 'equipment', rot=[18, 0, 12], cubes=[
        {'o': [-0.65, -0.6, -0.5], 's': [1.3, 6.6, 1.0], 'paint': scabbard(131)},
        {'o': [-0.7, 4.6, -0.55], 's': [1.4, 0.9, 1.1], 'paint': gold_m(133)},
    ])
    m.bone('katana_handle', [5.5, 17.9, 3.4], 'equipment', rot=[24, 0, 8], cubes=[
        {'o': [-0.7, 0.5, -0.7], 's': [1.4, 0.5, 1.4], 'paint': iron_m(135)},
        {'o': [-0.5, 1.0, -0.5], 's': [1.0, 3.6, 1.0], 'paint': tsuka()},
    ])
    m.bone('wakizashi_scabbard', [4.1, 16.5, 3.6], 'equipment', rot=[16, 0, 4], cubes=[
        {'o': [-0.55, -0.5, -0.4], 's': [1.1, 4.9, 0.8], 'paint': scabbard(137)},
    ])
    m.bone('wakizashi_handle', [4.1, 16.8, 3.6], 'equipment', rot=[22, 0, 2], cubes=[
        {'o': [-0.6, 0.3, -0.6], 's': [1.2, 0.4, 1.2], 'paint': iron_m(139)},
        {'o': [-0.45, 0.7, -0.45], 's': [0.9, 2.7, 0.9], 'paint': tsuka()},
    ])

    m.absolutize_origins()
    m.save(os.path.join(A, 'geo/settlement/red_shogun.geo.json'),
           os.path.join(A, 'textures/settlement/entity/red_shogun.png'))


def build_ninja():
    N = NINJA
    m = Model('dark_ninja', 256, 256, visible_bounds=(6, 6))

    char = lambda s=1: cloth(N['char'], N['char_dk'], N['char_hi'], s, 3)
    bgray = lambda s=2: cloth(N['bluegray'], N['bluegray_dk'], N['bluegray_hi'], s, 3)
    indi = lambda s=3: cloth(N['indigo'], N['indigo_dk'], N['indigo_hi'], s, 4)
    slt = lambda s=4: quilt(N['slate'], N['slate_hi'], N['slate_dk'], s)
    iron_m = lambda s=5: metal(N['iron'], N['iron_hi'], N['iron_dk'], s, 0.03)
    lthr = lambda s=6: leather(N['leather'], N['leather_hi'], N['leather_dk'], s)

    m.bone('root', [0, 0, 0])
    m.bone('master', [0, 12.5, 0], 'root')

    # ---------------- body ----------------
    m.bone('body', [0, 12.5, 0], 'master', cubes=[
        {'o': [-3.5, 0.0, -2.3], 's': [7.0, 10.5, 4.6], 'paint': indi(11)},
    ])
    m.bone('outer_jacket', [0, 12.5, 0], 'body', cubes=[
        {'o': [-3.9, 0.5, -2.7], 's': [7.8, 9.4, 5.4], 'paint': jacket()},
        {'o': [-4.0, 5.6, -2.8], 's': [8.0, 1.5, 5.6], 'paint': lthr(13)},
        {'o': [-3.0, 6.9, -2.95], 's': [2.6, 1.3, 0.7],
         'paint': leather(N['leather_hi'], (108, 80, 50), N['leather_dk'], 15)},
    ])
    m.bone('shoulder_padding', [0, 12.5, 0], 'body', cubes=[
        {'o': [3.4, 8.7, -2.3], 's': [1.7, 1.3, 4.4], 'paint': slt(17)},
        {'o': [-5.1, 8.7, -2.3], 's': [1.7, 1.3, 4.4], 'paint': slt(19)},
    ])
    m.bone('hip_cloth_front', [0, 19.1, -2.55], 'body', rot=[-4, 0, 0], cubes=[
        {'o': [-3.1, -2.5, -0.3], 's': [6.2, 2.6, 0.6], 'paint': bgray(21)},
    ])
    m.bone('hip_cloth_back', [0, 19.1, 2.55], 'body', rot=[4, 0, 0], cubes=[
        {'o': [-3.1, -2.5, -0.3], 's': [6.2, 2.6, 0.6], 'paint': bgray(23)},
    ])

    # ---------------- head ----------------
    m.bone('head', [0, 23, 0], 'master', cubes=[
        {'o': [-3.8, 0.0, -3.8], 's': [7.6, 7.6, 7.6], 'paint': face_ninja()},
    ])
    m.bone('hood', [0, 23, 0], 'head', cubes=[
        {'o': [-4.05, 4.5, -4.0], 's': [8.1, 3.5, 8.4], 'paint': hood(31)},
        {'o': [-4.05, -0.3, 0.4], 's': [8.1, 8.6, 4.2], 'paint': hood(33)},
        {'o': [3.45, -0.3, -4.0], 's': [1.15, 8.6, 4.5], 'paint': hood(35)},
        {'o': [-4.6, -0.3, -4.0], 's': [1.15, 8.6, 4.5], 'paint': hood(37)},
        {'o': [-3.9, 4.35, -4.25], 's': [7.8, 1.0, 0.7], 'paint': cloth(N['char_dk'], N['char_dd'], N['char'], 39, 2)},
    ])
    m.bone('face_mask', [0, 23, 0], 'head', cubes=[
        {'o': [-3.8, 0.2, -4.55], 's': [7.6, 2.5, 1.15], 'paint': mask()},
    ])
    m.bone('neck_wrap', [0, 23, 0], 'head', cubes=[
        {'o': [-3.6, -1.15, -3.3], 's': [7.2, 1.5, 6.7],
         'paint': cloth(N['indigo_dk'], (16, 18, 28), N['indigo'], 41, 2)},
    ])

    # ---------------- arms ----------------
    for side, x in (('right', -5.9), ('left', 5.9)):
        r = side == 'right'
        seed0 = 51 if r else 53
        m.bone(side + '_arm', [x, 21.6, 0], 'master', cubes=[
            {'o': [(-1.35 if r else -2.05), -5.3, -1.75], 's': [3.4, 5.3, 3.7], 'paint': char(seed0)},
            {'o': [(-1.3 if r else -2.0), -9.9, -1.7], 's': [3.3, 4.6, 3.6], 'paint': wrap(seed0 + 4)},
            {'o': [(-1.4 if r else -2.1), -10.55, -1.8], 's': [3.5, 0.65, 3.8], 'paint': iron_m(seed0 + 8)},
            {'o': [(-1.2 if r else -1.8), -12.5, -1.55], 's': [3.0, 1.95, 3.4],
             'paint': cloth(N['skin'], N['skin_dk'], (216, 174, 130), seed0 + 12, 2)},
        ])

    # ---------------- legs ----------------
    for side, x in (('right', -2.15), ('left', 2.15)):
        seed0 = 71 if side == 'right' else 73
        m.bone(side + '_leg', [x, 12.5, 0], 'master', cubes=[
            {'o': [-1.9, -7.3, -2.05], 's': [3.8, 7.3, 4.2], 'paint': char(seed0)},
            {'o': [-1.75, -11.9, -1.95], 's': [3.5, 4.6, 3.9], 'paint': char(seed0 + 4)},
            {'o': [-1.8, -11.4, -2.4], 's': [3.6, 5.7, 0.75], 'paint': wrap(seed0 + 8)},
            {'o': [-1.85, -12.55, -2.5], 's': [3.7, 1.95, 5.0],
             'paint': cloth(N['char_dk'], N['char_dd'], N['char'], seed0 + 12, 2)},
        ])

    # ---------------- equipment ----------------
    m.bone('equipment', [0, 12.5, 0], 'master')
    m.bone('short_sword_scabbard', [3.7, 16.3, -2.2], 'equipment', rot=[0, 12, -34], cubes=[
        {'o': [-0.45, -0.4, -0.4], 's': [0.9, 5.6, 0.8],
         'paint': cloth((22, 24, 28), NINJA['char_dd'], (34, 37, 44), 91, 2)},
    ])
    m.bone('short_sword_handle', [3.7, 16.3, -2.2], 'equipment', rot=[0, 12, -34], cubes=[
        {'o': [-0.55, 2.15, -0.55], 's': [1.1, 0.5, 1.1], 'paint': iron_m(93)},
        {'o': [-0.4, 2.65, -0.4], 's': [0.8, 2.4, 0.8], 'paint': wrap(95)},
    ])
    for side, x, rz in (('right', -4.0, -14), ('left', -2.6, 12)):
        m.bone('kunai_' + side, [x, 14.5, -2.5], 'equipment', rot=[0, 0, rz], cubes=[
            {'o': [-0.3, 0.7, -0.25], 's': [0.6, 2.1, 0.5],
             'paint': metal(N['iron_dk'], N['iron'], (48, 52, 60), 97, 0.08)},
            {'o': [-0.25, -1.1, -0.2], 's': [0.5, 1.8, 0.4], 'paint': lthr(99)},
            {'o': [-0.15, -1.65, -0.15], 's': [0.3, 0.55, 0.3], 'paint': iron_m(101)},
        ])
    m.bone('rope', [4.7, 14.4, 2.3], 'equipment', rot=[0, 0, -14], cubes=[
        {'o': [-1.2, -0.25, -1.2], 's': [2.4, 0.55, 2.4],
         'paint': leather(N['leather'], N['leather_hi'], N['leather_dk'], 103)},
        {'o': [-1.0, 0.3, -1.0], 's': [2.0, 0.55, 2.0],
         'paint': leather(N['leather_hi'], (108, 80, 50), N['leather'], 105)},
    ])
    m.bone('pouch_left', [4.8, 12.4, 2.1], 'equipment', rot=[0, 0, 5], cubes=[
        {'o': [-1.0, -0.3, -0.9], 's': [2.0, 2.3, 1.8], 'paint': lthr(107)},
        {'o': [-1.0, 1.6, -0.95], 's': [2.0, 0.8, 1.9],
         'paint': cloth(N['leather_dk'], (36, 26, 16), N['leather'], 109, 2)},
    ])
    m.bone('pouch_right', [-4.9, 13.0, 2.1], 'equipment', rot=[0, 0, -5], cubes=[
        {'o': [-0.9, -0.3, -0.85], 's': [1.8, 2.0, 1.7], 'paint': lthr(111)},
        {'o': [-0.9, 1.35, -0.9], 's': [1.8, 0.7, 1.8],
         'paint': cloth(N['leather_dk'], (36, 26, 16), N['leather'], 113, 2)},
    ])

    m.absolutize_origins()
    m.save(os.path.join(A, 'geo/settlement/dark_ninja.geo.json'),
           os.path.join(A, 'textures/settlement/entity/dark_ninja.png'))


# ==================================================================
# ANIMATION LIBRARY
# ==================================================================
def shogun_anims():
    """15 clips: heavy, controlled, experienced movement."""
    an = {}

    # ----- loops -----
    an['idle'] = build_anim('idle', 3.4, {
        'body': {'rotation': track([(0, [0, 0, 0]), (1.7, [-1.5, 0, 0]), (3.4, [0, 0, 0])]),
                 'position': track([(0, [0, 0, 0]), (1.7, [0, -0.3, 0]), (3.4, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, -3, 0]), (1.1, [0, 3, 0]), (2.2, [-1, 1, 0]), (3.4, [0, -3, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 2.5]), (1.7, [-1.5, 0, 3.5]), (3.4, [0, 0, 2.5])])},
        'left_arm': {'rotation': track([(0, [0, 0, -2.5]), (1.7, [-1.5, 0, -3.5]), (3.4, [0, 0, -2.5])])},
        'kusazuri_left': {'rotation': track([(0, [0, 0, -7]), (1.7, [1.5, 0, -8.5]), (3.4, [0, 0, -7])])},
        'kusazuri_right': {'rotation': track([(0, [0, 0, 7]), (1.7, [1.5, 0, 8.5]), (3.4, [0, 0, 7])])},
    })

    d = 1.15
    an['walk'] = build_anim('walk', d, {
        'right_leg': {'rotation': track([(0, [-32, 0, 0]), (d * .5, [28, 0, 0]), (d * .86, [-6, 0, 0]), (d, [-32, 0, 0])])},
        'left_leg': {'rotation': track([(0, [28, 0, 0]), (d * .5, [-32, 0, 0]), (d * .86, [6, 0, 0]), (d, [28, 0, 0])])},
        'right_arm': {'rotation': track([(0, [24, 0, 2]), (d * .5, [-22, 0, 2]), (d, [24, 0, 2])])},
        'left_arm': {'rotation': track([(0, [-22, 0, -2]), (d * .5, [24, 0, -2]), (d, [-22, 0, -2])])},
        'body': {'rotation': track([(0, [0, 0, 1.5]), (d * .5, [0, 0, -1.5]), (d, [0, 0, 1.5])]),
                 'position': track([(0, [0, 0, 0]), (d * .25, [0, 0.35, 0]), (d * .5, [0, 0, 0]), (d * .75, [0, 0.35, 0]), (d, [0, 0, 0])])},
        'head': {'rotation': track([(0, [2, 2, 0]), (d * .5, [-2, -2, 0]), (d, [2, 2, 0])])},
        'kusazuri_front': {'rotation': track([(0, [-6, 0, 0]), (d * .5, [-2, 0, 0]), (d, [-6, 0, 0])])},
        'kusazuri_back': {'rotation': track([(0, [6, 0, 0]), (d * .5, [2, 0, 0]), (d, [6, 0, 0])])},
        'kusazuri_left': {'rotation': track([(0, [2, 0, -7]), (d * .5, [-2, 0, -7]), (d, [2, 0, -7])])},
        'kusazuri_right': {'rotation': track([(0, [-2, 0, 7]), (d * .5, [2, 0, 7]), (d, [-2, 0, 7])])},
    })

    d = 0.85
    an['run'] = build_anim('run', d, {
        'right_leg': {'rotation': track([(0, [-46, 0, 0]), (d * .5, [40, 0, 0]), (d, [-46, 0, 0])])},
        'left_leg': {'rotation': track([(0, [40, 0, 0]), (d * .5, [-46, 0, 0]), (d, [40, 0, 0])])},
        'right_arm': {'rotation': track([(0, [38, 0, 3]), (d * .5, [-42, 0, 3]), (d, [38, 0, 3])])},
        'left_arm': {'rotation': track([(0, [-42, 0, -3]), (d * .5, [38, 0, -3]), (d, [-42, 0, -3])])},
        'master': {'rotation': track([(0, [-7, 0, 0]), (d * .5, [-5, 0, 0]), (d, [-7, 0, 0])]),
                   'position': track([(0, [0, 0, 0]), (d * .25, [0, 0.55, 0]), (d * .5, [0, 0, 0]), (d * .75, [0, 0.55, 0]), (d, [0, 0, 0])])},
        'head': {'rotation': track([(0, [6, 0, 0]), (d * .5, [4, 0, 0]), (d, [6, 0, 0])])},
        'kusazuri_front': {'rotation': track([(0, [-10, 0, 0]), (d * .5, [4, 0, 0]), (d, [-10, 0, 0])])},
        'kusazuri_back': {'rotation': track([(0, [10, 0, 0]), (d * .5, [-4, 0, 0]), (d, [10, 0, 0])])},
    })

    an['combat_idle'] = build_anim('combat_idle', 2.6, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (1.3, [-26, -10, -4]), (2.6, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (1.3, [-14, 0, -7]), (2.6, [-12, 0, -6])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (1.3, [-1, 2, 0]), (2.6, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (1.3, [2, -1, 0]), (2.6, [0, -4, 0])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (1.3, [-7, 5, 0]), (2.6, [-8, 6, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (1.3, [5, -3, 0]), (2.6, [6, -4, 0])])},
    })

    # ----- katana handling -----
    an['draw_katana'] = build_anim('draw_katana', 0.5, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.18, [-46, -30, -10]), (0.32, [-88, 8, 4]), (0.5, [-70, 4, 2])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.2, [-30, 0, -30]), (0.5, [-16, 0, -8])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.32, [-2, -10, 0]), (0.5, [-1, -6, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.32, [4, 8, 0]), (0.5, [2, 4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.32, [0, -0.8, 0]), (0.5, [0, -0.4, 0])])},
    })

    an['sheathe_katana'] = build_anim('sheathe_katana', 0.7, {
        'right_arm': {'rotation': track([(0, [-70, 4, 2]), (0.3, [-40, -22, -8]), (0.55, [-32, -14, -5]), (0.7, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-16, 0, -8]), (0.3, [-26, 0, -20]), (0.7, [-12, 0, -6])])},
        'body': {'rotation': track([(0, [-1, -6, 0]), (0.55, [1, 3, 0]), (0.7, [0, 4, 0])])},
        'head': {'rotation': track([(0, [2, 4, 0]), (0.55, [-2, -3, 0]), (0.7, [0, -4, 0])])},
        'master': {'position': track([(0, [0, -0.4, 0]), (0.55, [0, 0.2, 0]), (0.7, [0, 0, 0])])},
    })

    # ----- attacks -----
    an['attack_horizontal'] = build_anim('attack_horizontal', 0.7, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.22, [-26, -72, -12]), (0.38, [-38, 62, 8]), (0.55, [-34, 40, 6]), (0.7, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.22, [-20, 0, -12]), (0.38, [-30, 0, -20]), (0.7, [-12, 0, -6])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.22, [2, 16, 0]), (0.38, [-3, -20, 0]), (0.7, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.22, [0, -10, 0]), (0.38, [2, 12, 0]), (0.7, [0, -4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.38, [0, -0.7, 0]), (0.55, [0, -0.3, 0]), (0.7, [0, 0, 0])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (0.38, [-14, 4, 0]), (0.7, [-8, 6, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (0.38, [10, -6, 0]), (0.7, [6, -4, 0])])},
    })

    an['attack_diagonal'] = build_anim('attack_diagonal', 0.75, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.24, [-148, -18, -24]), (0.4, [-22, 10, 34]), (0.56, [-26, 6, 26]), (0.75, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.24, [-40, 0, -24]), (0.4, [-18, 0, -8]), (0.75, [-12, 0, -6])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.24, [-3, 12, 0]), (0.4, [5, -14, 0]), (0.75, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.24, [-6, -8, 0]), (0.4, [6, 10, 0]), (0.75, [0, -4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.4, [0, -1.1, 0]), (0.56, [0, -0.4, 0]), (0.75, [0, 0, 0])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (0.4, [-16, 6, 0]), (0.75, [-8, 6, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (0.4, [12, -8, 0]), (0.75, [6, -4, 0])])},
    })

    an['attack_overhead'] = build_anim('attack_overhead', 0.9, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.28, [-168, -4, -4]), (0.44, [26, 0, 0]), (0.6, [18, 0, 0]), (0.9, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.28, [-120, 0, -14]), (0.44, [-40, 0, -10]), (0.9, [-12, 0, -6])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.28, [-6, 2, 0]), (0.44, [9, 0, 0]), (0.9, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.28, [-10, 0, 0]), (0.44, [10, 0, 0]), (0.9, [0, -4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.28, [0, -1.2, 0]), (0.44, [0, -2.0, 0]), (0.6, [0, -0.8, 0]), (0.9, [0, 0, 0])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (0.28, [-20, 4, 0]), (0.44, [-26, 2, 0]), (0.9, [-8, 6, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (0.28, [14, -4, 0]), (0.44, [22, -6, 0]), (0.9, [6, -4, 0])])},
    })

    # ----- defense -----
    an['block'] = build_anim('block', 0.45, {
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.2, [-96, -38, -10]), (0.45, [-92, -36, -12])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.2, [-88, 34, 12]), (0.45, [-84, 32, 14])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.2, [4, 0, 0]), (0.45, [5, 0, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.45, [-4, 0, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.2, [0, -1.0, 0.3]), (0.45, [0, -1.1, 0.4])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (0.2, [-16, 4, 0]), (0.45, [-17, 4, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (0.2, [14, -6, 0]), (0.45, [15, -6, 0])])},
    })

    an['parry'] = build_anim('parry', 0.35, {
        'right_arm': {'rotation': track([(0, [-92, -36, -12]), (0.12, [-96, -52, -20]), (0.24, [-70, 24, 10]), (0.35, [-60, 10, 4])])},
        'left_arm': {'rotation': track([(0, [-84, 32, 14]), (0.24, [-40, 10, -6]), (0.35, [-30, 0, -8])])},
        'body': {'rotation': track([(0, [5, 0, 0]), (0.12, [4, -6, 0]), (0.24, [2, 8, 0]), (0.35, [0, 4, 0])])},
        'head': {'rotation': track([(0, [-4, 0, 0]), (0.24, [2, 6, 0]), (0.35, [0, -4, 0])])},
    })

    # ----- command -----
    an['command'] = build_anim('command', 1.4, {
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.3, [-124, 0, -26]), (0.9, [-118, 0, -24]), (1.4, [-12, 0, -6])])},
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.3, [-38, -10, -7]), (0.9, [-36, -10, -7]), (1.4, [-30, -14, -5])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.3, [-2, -4, 0]), (0.9, [-2, -4, 0]), (1.4, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.3, [-8, 6, 0]), (0.9, [-8, 6, 0]), (1.4, [0, -4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.3, [0, 0.4, 0]), (0.9, [0, 0.4, 0]), (1.4, [0, 0, 0])])},
    })

    # ----- reactions -----
    an['hurt'] = build_anim('hurt', 0.4, {
        'body': {'rotation': track([(0, [0, 0, 0]), (0.12, [9, 0, 0]), (0.4, [0, 0, 0])]),
                 'position': track([(0, [0, 0, 0]), (0.12, [0, 0.3, 0.5]), (0.4, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.12, [-7, 3, 0]), (0.4, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 2.5]), (0.12, [-12, 0, 9]), (0.4, [0, 0, 2.5])])},
        'left_arm': {'rotation': track([(0, [0, 0, -2.5]), (0.12, [-8, 0, -12]), (0.4, [0, 0, -2.5])])},
    })

    an['death'] = build_anim('death', 1.6, {
        'master': {'rotation': track([(0, [0, 0, 0]), (0.35, [-14, 0, 0]), (0.75, [-78, 0, 0]), (0.95, [-84, 0, 0]), (1.6, [-84, 0, 0])]),
                   'position': track([(0, [0, 0, 0]), (0.35, [0, -1.4, 0]), (0.75, [0, -1.8, 1.6]), (1.6, [0, -1.8, 1.8])])},
        'right_leg': {'rotation': track([(0, [0, 0, 0]), (0.35, [-42, 0, 0]), (0.75, [-58, 6, 0]), (1.6, [-58, 6, 0])])},
        'left_leg': {'rotation': track([(0, [0, 0, 0]), (0.35, [-30, 0, 0]), (0.75, [-48, -6, 0]), (1.6, [-48, -6, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 2.5]), (0.35, [-20, 0, 10]), (0.75, [-46, 0, 26]), (1.6, [-50, 0, 28])])},
        'left_arm': {'rotation': track([(0, [0, 0, -2.5]), (0.35, [-16, 0, -12]), (0.75, [-40, 0, -30]), (1.6, [-44, 0, -32])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.35, [10, 0, 0]), (0.75, [22, 0, 0]), (1.6, [24, 0, 0])])},
        'kusazuri_front': {'rotation': track([(0, [-6, 0, 0]), (0.75, [18, 0, 0]), (1.6, [18, 0, 0])])},
    })

    # ----- technique: iai long lunge -----
    an['long_lunge'] = build_anim('long_lunge', 1.6, {
        'master': {'position': track([(0, [0, 0, 0]), (0.32, [0, -1.8, 0]), (0.46, [0, -2.4, 0]), (1.05, [0, -2.2, 0]), (1.6, [0, 0, 0])]),
                   'rotation': track([(0, [0, 0, 0]), (0.32, [4, -14, 0]), (0.46, [8, 2, 0]), (1.05, [7, 0, 0]), (1.6, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [-30, -14, -5]), (0.32, [-52, -46, -14]), (0.44, [-96, 4, 2]), (0.62, [-92, 2, 2]), (0.8, [-95, 3, 2]), (1.05, [-92, 2, 2]), (1.35, [-50, -10, -3]), (1.6, [-30, -14, -5])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -6]), (0.32, [-34, 0, -26]), (0.46, [-52, 14, -34]), (1.05, [-48, 12, -32]), (1.6, [-12, 0, -6])])},
        'right_leg': {'rotation': track([(0, [-8, 6, 0]), (0.32, [-34, 4, 0]), (0.46, [-52, 2, 0]), (1.05, [-48, 2, 0]), (1.6, [-8, 6, 0])])},
        'left_leg': {'rotation': track([(0, [6, -4, 0]), (0.32, [24, -6, 0]), (0.46, [38, -10, 0]), (1.05, [34, -8, 0]), (1.6, [6, -4, 0])])},
        'body': {'rotation': track([(0, [0, 4, 0]), (0.32, [6, -8, 0]), (0.46, [10, 0, 0]), (1.05, [9, 0, 0]), (1.6, [0, 4, 0])])},
        'head': {'rotation': track([(0, [0, -4, 0]), (0.32, [6, 10, 0]), (0.46, [2, 0, 0]), (1.05, [3, 0, 0]), (1.6, [0, -4, 0])])},
        'kusazuri_front': {'rotation': track([(0, [-6, 0, 0]), (0.46, [14, 0, 0]), (1.05, [12, 0, 0]), (1.6, [-6, 0, 0])])},
        'kusazuri_back': {'rotation': track([(0, [6, 0, 0]), (0.46, [-8, 0, 0]), (1.05, [-6, 0, 0]), (1.6, [6, 0, 0])])},
    })

    return an


def ninja_anims():
    """17 clips: silent, fast, low center of gravity."""
    an = {}

    an['idle'] = build_anim('idle', 3.0, {
        'body': {'rotation': track([(0, [0, 0, 0]), (1.5, [-0.8, 1.5, 0]), (3.0, [0, 0, 0])])},
        'head': {'rotation': track([(0, [1, 4, 0]), (1.0, [0, -5, 0]), (2.0, [1, 2, 0]), (3.0, [1, 4, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 1.5]), (1.5, [-1, 0, 2]), (3.0, [0, 0, 1.5])])},
        'left_arm': {'rotation': track([(0, [0, 0, -1.5]), (1.5, [-1, 0, -2]), (3.0, [0, 0, -1.5])])},
        'hip_cloth_front': {'rotation': track([(0, [-4, 0, 0]), (1.5, [-3, 0, 0]), (3.0, [-4, 0, 0])])},
    })

    an['crouch_idle'] = build_anim('crouch_idle', 2.8, {
        'master': {'position': track([(0, [0, -3.2, 0]), (1.4, [0, -3.5, 0]), (2.8, [0, -3.2, 0])]),
                   'rotation': track([(0, [6, 0, 0]), (1.4, [7, 2, 0]), (2.8, [6, 0, 0])])},
        'right_leg': {'rotation': track([(0, [24, 8, 0]), (1.4, [25, 9, 0]), (2.8, [24, 8, 0])])},
        'left_leg': {'rotation': track([(0, [-24, -8, 0]), (1.4, [-25, -9, 0]), (2.8, [-24, -8, 0])])},
        'body': {'rotation': track([(0, [10, 0, 0]), (1.4, [11, -2, 0]), (2.8, [10, 0, 0])])},
        'head': {'rotation': track([(0, [-14, 3, 0]), (1.2, [-13, -4, 0]), (2.8, [-14, 3, 0])])},
        'right_arm': {'rotation': track([(0, [-14, 0, 4]), (1.4, [-12, 0, 5]), (2.8, [-14, 0, 4])])},
        'left_arm': {'rotation': track([(0, [-22, 0, -8]), (1.4, [-20, 0, -9]), (2.8, [-22, 0, -8])])},
    })

    d = 1.0
    an['walk'] = build_anim('walk', d, {
        'right_leg': {'rotation': track([(0, [-24, 0, 0]), (d * .5, [20, 0, 0]), (d, [-24, 0, 0])])},
        'left_leg': {'rotation': track([(0, [20, 0, 0]), (d * .5, [-24, 0, 0]), (d, [20, 0, 0])])},
        'right_arm': {'rotation': track([(0, [10, 0, 2]), (d * .5, [-8, 0, 2]), (d, [10, 0, 2])])},
        'left_arm': {'rotation': track([(0, [-8, 0, -2]), (d * .5, [10, 0, -2]), (d, [-8, 0, -2])])},
        'body': {'rotation': track([(0, [1, 0, 1]), (d * .5, [1, 0, -1]), (d, [1, 0, 1])]),
                 'position': track([(0, [0, 0, 0]), (d * .25, [0, 0.2, 0]), (d * .5, [0, 0, 0]), (d * .75, [0, 0.2, 0]), (d, [0, 0, 0])])},
        'head': {'rotation': track([(0, [2, 3, 0]), (d * .5, [0, -3, 0]), (d, [2, 3, 0])])},
        'hip_cloth_front': {'rotation': track([(0, [-4, 0, 0]), (d * .5, [-1, 0, 0]), (d, [-4, 0, 0])])},
        'hip_cloth_back': {'rotation': track([(0, [4, 0, 0]), (d * .5, [1, 0, 0]), (d, [4, 0, 0])])},
    })

    d = 1.35
    an['crouch_walk'] = build_anim('crouch_walk', d, {
        'master': {'position': track([(0, [0, -3.2, 0]), (d * .5, [0, -3.5, 0]), (d, [0, -3.2, 0])]),
                   'rotation': track([(0, [6, 0, 0]), (d, [6, 0, 0])])},
        'right_leg': {'rotation': track([(0, [24, -16, 0]), (d * .5, [-8, 12, 0]), (d, [24, -16, 0])])},
        'left_leg': {'rotation': track([(0, [-8, 12, 0]), (d * .5, [24, -16, 0]), (d, [-8, 12, 0])])},
        'body': {'rotation': track([(0, [10, 0, 2]), (d * .5, [10, 0, -2]), (d, [10, 0, 2])])},
        'head': {'rotation': track([(0, [-14, 4, 0]), (d * .5, [-13, -4, 0]), (d, [-14, 4, 0])])},
        'right_arm': {'rotation': track([(0, [-16, 0, 5]), (d * .5, [-12, 0, 4]), (d, [-16, 0, 5])])},
        'left_arm': {'rotation': track([(0, [-24, 0, -9]), (d * .5, [-20, 0, -8]), (d, [-24, 0, -9])])},
    })

    d = 0.7
    an['run'] = build_anim('run', d, {
        'right_leg': {'rotation': track([(0, [-42, 0, 0]), (d * .5, [36, 0, 0]), (d, [-42, 0, 0])])},
        'left_leg': {'rotation': track([(0, [36, 0, 0]), (d * .5, [-42, 0, 0]), (d, [36, 0, 0])])},
        'right_arm': {'rotation': track([(0, [30, 0, 3]), (d * .5, [-34, 0, 3]), (d, [30, 0, 3])])},
        'left_arm': {'rotation': track([(0, [-34, 0, -3]), (d * .5, [30, 0, -3]), (d, [-34, 0, -3])])},
        'master': {'rotation': track([(0, [-10, 0, 0]), (d * .5, [-8, 0, 0]), (d, [-10, 0, 0])]),
                   'position': track([(0, [0, 0, 0]), (d * .25, [0, 0.45, 0]), (d * .5, [0, 0, 0]), (d * .75, [0, 0.45, 0]), (d, [0, 0, 0])])},
        'head': {'rotation': track([(0, [8, 0, 0]), (d * .5, [6, 0, 0]), (d, [8, 0, 0])])},
        'hip_cloth_front': {'rotation': track([(0, [-12, 0, 0]), (d * .5, [4, 0, 0]), (d, [-12, 0, 0])])},
        'hip_cloth_back': {'rotation': track([(0, [12, 0, 0]), (d * .5, [-4, 0, 0]), (d, [12, 0, 0])])},
    })

    an['draw_sword'] = build_anim('draw_sword', 0.45, {
        'right_arm': {'rotation': track([(0, [0, 0, 1.5]), (0.15, [-40, -26, -8]), (0.3, [-80, 10, 4]), (0.45, [-72, 6, 2])])},
        'left_arm': {'rotation': track([(0, [0, 0, -1.5]), (0.2, [-24, 0, -22]), (0.45, [-14, 0, -6])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.3, [-2, -8, 0]), (0.45, [-1, -5, 0])])},
        'head': {'rotation': track([(0, [1, 4, 0]), (0.3, [4, -6, 0]), (0.45, [2, -3, 0])])},
    })

    an['sheathe_sword'] = build_anim('sheathe_sword', 0.6, {
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.3, [-34, -20, -8]), (0.6, [0, 0, 1.5])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.3, [-22, 0, -18]), (0.6, [0, 0, -1.5])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.6, [0, 0, 0])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.6, [1, 4, 0])])},
    })

    an['attack_fast'] = build_anim('attack_fast', 0.45, {
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.12, [-70, -34, -10]), (0.24, [-58, 46, 6]), (0.34, [-60, 30, 4]), (0.45, [-72, 6, 2])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.24, [-30, 0, -14]), (0.45, [-14, 0, -6])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.12, [2, 12, 0]), (0.24, [-3, -14, 0]), (0.45, [-1, -5, 0])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.12, [0, -8, 0]), (0.24, [2, 10, 0]), (0.45, [2, -3, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.24, [0, -0.5, 0]), (0.45, [0, 0, 0])])},
    })

    an['attack_diagonal'] = build_anim('attack_diagonal', 0.55, {
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.16, [-150, -14, -20]), (0.3, [-20, 12, 30]), (0.42, [-26, 8, 22]), (0.55, [-72, 6, 2])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.16, [-38, 0, -20]), (0.3, [-16, 0, -8]), (0.55, [-14, 0, -6])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.16, [-4, 10, 0]), (0.3, [6, -12, 0]), (0.55, [-1, -5, 0])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.16, [-6, -6, 0]), (0.3, [6, 8, 0]), (0.55, [2, -3, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.3, [0, -0.9, 0]), (0.55, [0, 0, 0])])},
    })

    an['stab'] = build_anim('stab', 0.4, {
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.12, [-64, -20, -8]), (0.22, [-92, 4, 0]), (0.32, [-88, 2, 0]), (0.4, [-72, 6, 2])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.22, [-34, 0, -18]), (0.4, [-14, 0, -6])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.22, [4, -6, 0]), (0.4, [-1, -5, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.22, [0, -0.4, -0.4]), (0.4, [0, 0, 0])])},
    })

    an['throw_kunai'] = build_anim('throw_kunai', 0.6, {
        'right_arm': {'rotation': track([(0, [-30, 0, 6]), (0.2, [-140, -20, -10]), (0.34, [-64, 20, 4]), (0.6, [-30, 0, 6])])},
        'left_arm': {'rotation': track([(0, [-12, 0, -8]), (0.34, [-40, 0, -16]), (0.6, [-12, 0, -8])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.2, [-3, 10, 0]), (0.34, [4, -12, 0]), (0.6, [0, 0, 0])])},
        'head': {'rotation': track([(0, [1, 4, 0]), (0.34, [0, -8, 0]), (0.6, [1, 4, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.34, [0, -0.6, 0]), (0.6, [0, 0, 0])])},
    })

    an['block'] = build_anim('block', 0.4, {
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.18, [-96, -40, -14]), (0.4, [-92, -38, -16])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.18, [-86, 36, 16]), (0.4, [-82, 34, 18])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.18, [6, 0, 0]), (0.4, [7, 0, 0])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.4, [-4, 0, 0])])},
        'master': {'position': track([(0, [0, 0, 0]), (0.18, [0, -1.4, 0.4]), (0.4, [0, -1.5, 0.5])])},
    })

    an['dodge_left'] = build_anim('dodge_left', 0.35, {
        'master': {'position': track([(0, [0, 0, 0]), (0.15, [-2.4, -1.6, 0]), (0.35, [-3.4, -0.4, 0])]),
                   'rotation': track([(0, [0, 0, 0]), (0.15, [4, 0, -14]), (0.35, [2, 0, -18])])},
        'right_leg': {'rotation': track([(0, [0, 0, 0]), (0.15, [-30, 0, 0]), (0.35, [-24, 0, 0])])},
        'left_leg': {'rotation': track([(0, [0, 0, 0]), (0.15, [20, 0, 0]), (0.35, [16, 0, 0])])},
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.15, [-50, 0, 14]), (0.35, [-54, 0, 16])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.15, [-40, 0, -22]), (0.35, [-36, 0, -20])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.15, [0, 0, 10]), (0.35, [0, 0, 12])])},
    })

    an['dodge_right'] = build_anim('dodge_right', 0.35, {
        'master': {'position': track([(0, [0, 0, 0]), (0.15, [2.4, -1.6, 0]), (0.35, [3.4, -0.4, 0])]),
                   'rotation': track([(0, [0, 0, 0]), (0.15, [4, 0, 14]), (0.35, [2, 0, 18])])},
        'right_leg': {'rotation': track([(0, [0, 0, 0]), (0.15, [20, 0, 0]), (0.35, [16, 0, 0])])},
        'left_leg': {'rotation': track([(0, [0, 0, 0]), (0.15, [-30, 0, 0]), (0.35, [-24, 0, 0])])},
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.15, [-44, 0, -18]), (0.35, [-48, 0, -20])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.15, [-52, 0, 12]), (0.35, [-48, 0, 14])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.15, [0, 0, -10]), (0.35, [0, 0, -12])])},
    })

    an['hurt'] = build_anim('hurt', 0.35, {
        'body': {'rotation': track([(0, [0, 0, 0]), (0.1, [8, 0, 0]), (0.35, [0, 0, 0])]),
                 'position': track([(0, [0, 0, 0]), (0.1, [0, 0.2, 0.4]), (0.35, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.1, [-8, 2, 0]), (0.35, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 1.5]), (0.1, [-10, 0, 10]), (0.35, [0, 0, 1.5])])},
        'left_arm': {'rotation': track([(0, [0, 0, -1.5]), (0.1, [-6, 0, -12]), (0.35, [0, 0, -1.5])])},
    })

    an['death'] = build_anim('death', 1.2, {
        'master': {'rotation': track([(0, [0, 0, 0]), (0.3, [-20, 0, 0]), (0.65, [-84, 0, 0]), (1.2, [-84, 0, 0])]),
                   'position': track([(0, [0, 0, 0]), (0.3, [0, -2.0, 0]), (0.65, [0, -2.4, 1.4]), (1.2, [0, -2.4, 1.5])])},
        'right_leg': {'rotation': track([(0, [0, 0, 0]), (0.3, [-46, 0, 0]), (0.65, [-60, 8, 0]), (1.2, [-60, 8, 0])])},
        'left_leg': {'rotation': track([(0, [0, 0, 0]), (0.3, [-34, 0, 0]), (0.65, [-50, -8, 0]), (1.2, [-50, -8, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, 1.5]), (0.3, [-24, 0, 14]), (0.65, [-44, 0, 30]), (1.2, [-48, 0, 32])])},
        'left_arm': {'rotation': track([(0, [0, 0, -1.5]), (0.3, [-20, 0, -16]), (0.65, [-38, 0, -34]), (1.2, [-42, 0, -36])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.3, [12, 0, 0]), (0.65, [24, 0, 0]), (1.2, [26, 0, 0])])},
    })

    # technique: smoke-step dash (low explosive pose)
    an['smoke_step'] = build_anim('smoke_step', 0.8, {
        'master': {'position': track([(0, [0, 0, 0]), (0.18, [0, -2.6, 0]), (0.5, [0, -2.2, 0]), (0.8, [0, 0, 0])]),
                   'rotation': track([(0, [0, 0, 0]), (0.18, [12, 0, 0]), (0.5, [8, 0, 0]), (0.8, [0, 0, 0])])},
        'right_leg': {'rotation': track([(0, [0, 0, 0]), (0.18, [-58, 10, 0]), (0.5, [-48, 8, 0]), (0.8, [0, 0, 0])])},
        'left_leg': {'rotation': track([(0, [0, 0, 0]), (0.18, [42, -12, 0]), (0.5, [34, -10, 0]), (0.8, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [-72, 6, 2]), (0.18, [-30, 20, 18]), (0.5, [-36, 16, 14]), (0.8, [-72, 6, 2])])},
        'left_arm': {'rotation': track([(0, [-14, 0, -6]), (0.18, [-60, -14, -26]), (0.5, [-52, -12, -22]), (0.8, [-14, 0, -6])])},
        'body': {'rotation': track([(0, [-1, -5, 0]), (0.18, [14, 8, 0]), (0.5, [10, 6, 0]), (0.8, [-1, -5, 0])])},
        'head': {'rotation': track([(0, [2, -3, 0]), (0.18, [-16, -4, 0]), (0.5, [-12, -3, 0]), (0.8, [2, -3, 0])])},
        'hip_cloth_front': {'rotation': track([(0, [-4, 0, 0]), (0.18, [10, 0, 0]), (0.8, [-4, 0, 0])])},
        'hip_cloth_back': {'rotation': track([(0, [4, 0, 0]), (0.18, [-10, 0, 0]), (0.8, [4, 0, 0])])},
    })

    return an


def save_anims():
    from framework import save_anim
    save_anim(os.path.join(A, 'animations/settlement/red_shogun.animation.json'), shogun_anims())
    save_anim(os.path.join(A, 'animations/settlement/dark_ninja.animation.json'), ninja_anims())


if __name__ == '__main__':
    build_shogun()
    build_ninja()
    save_anims()
