#!/usr/bin/env python3
"""Briarweave (ancient bark, no magic) + Dark Forest Vestments (ancient violet).
One union model class with two LayerDefinitions; the render layer passes the
variant flag. Emits DarkForestArmorModel.java + 2x (base atlas) + emissive.
Run from repo root: python3 scripts/gen_armor_rework/gen_darkforest.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (A, java_path, CubeSet, cube_list_lines, metal, leather, cloth,
                    bark, rough_stone, lacquer, emissive_mask, moss_overlay,
                    lichen_overlay, mixc, shadec, h01, vnoise)

BRIAR = {
    'bark':      (46, 35, 26), 'bark_hi': (66, 50, 36), 'bark_dk': (30, 22, 16),
    'bark_old':  (58, 46, 34), 'wood':    (143, 123, 94), 'wood_dk': (104, 88, 66),
    'leather':   (58, 42, 30), 'leather_hi': (76, 56, 40), 'leather_dk': (38, 27, 19),
    'cloth_in':  (36, 30, 24), 'moss':   (74, 82, 50), 'lichen': (138, 144, 120),
    'buckle':    (104, 88, 66),
}
VEST = {
    'bark':      (25, 20, 32), 'bark_hi': (38, 30, 48), 'bark_dk': (15, 12, 20),
    'metal':     (32, 28, 40), 'metal_hi': (48, 42, 60), 'metal_dk': (20, 18, 27),
    'violet':    (107, 63, 160), 'violet_hi': (139, 92, 246), 'violet_dk': (72, 40, 112),
    'amethyst':  (176, 140, 255), 'silver': (126, 130, 144),
    'moss':      (68, 80, 58), 'root':    (46, 36, 28), 'root_hi': (62, 48, 36),
    'cloth_in':  (22, 19, 28),
}

# ---------------------------------------------------------------- painters
briar_bark = lambda s=17: bark(BRIAR['bark'], BRIAR['bark_hi'], BRIAR['bark_dk'], s)
briar_old = lambda s=19: bark(BRIAR['bark_old'], BRIAR['bark_hi'], BRIAR['bark_dk'], s)
briar_leath = lambda s=5: leather(BRIAR['leather'], BRIAR['leather_hi'], BRIAR['leather_dk'], s)
briar_cloth = lambda: cloth(BRIAR['cloth_in'], (24, 20, 16), (48, 40, 32), 3, 3)
briar_wood = lambda s=23: (lambda x, y, w, h, face, name:
                           (BRIAR['wood'] if (x % 3) else BRIAR['wood_dk'])
                           if h01(x, y, s) > 0.2 else BRIAR['wood_dk'])
briar_mossy = lambda inner, s=47: moss_overlay(inner, BRIAR['moss'], s, 0.13)
briar_lichen = lambda inner, s=53: lichen_overlay(inner, BRIAR['lichen'], s, 0.07)

vest_bark = lambda s=27: bark(VEST['bark'], VEST['bark_hi'], VEST['bark_dk'], s)
vest_metal = lambda s=7: metal(VEST['metal'], VEST['metal_hi'], VEST['metal_dk'], s)
vest_root = lambda s=13: rough_stone(VEST['root'], VEST['root_hi'], (30, 23, 18), s)

def vest_leaf(seed=29):
    base, vein, dk = VEST['violet'], VEST['violet_hi'], VEST['violet_dk']
    def p(x, y, w, h, face, name):
        c = base
        cx = abs(x - (w - 1) / 2)
        if cx < 0.9:
            c = vein
        elif cx < 1.7:
            c = mixc(base, dk, 0.5)
        n = vnoise(x, y, seed, 2)
        if n > 0.72:
            c = mixc(c, VEST['amethyst'], 0.25)
        if y == h - 1:
            c = dk
        return c
    return p

def growth_rings():
    """Original concentric stepped growth rings (unique painted island)."""
    b, b_hi, b_dk = BRIAR['bark'], BRIAR['bark_hi'], BRIAR['bark_dk']
    crack = (24, 18, 13)
    def p(x, y, w, h, face, name):
        cx, cy = (w - 1) / 2, (h - 1) / 2
        r = max(abs(x - cx), abs(y - cy))
        band = int(r) % 4
        if r > min(cx, cy) - 0.5:
            return mixc(b_dk, crack, 0.5)
        if band == 0:
            c = b_hi
        elif band == 2:
            c = b_dk
        else:
            c = b
        if r == int(r) and h01(x, y, 91) > 0.5:
            c = crack
        if h01(x, y, 93) > 0.95:
            c = mixc(c, BRIAR['wood'], 0.4)
        return c
    return p

def ring_emissive_none():
    return None

def vest_emissive(seed=41, density=0.2, hot=True):
    return emissive_mask(VEST['amethyst'], seed, density, VEST['violet_hi'] if hot else None)

def vest_core():
    def p(x, y, w, h, face, name):
        if face not in ('north', 'south'):
            return None
        cx, cy = (w - 1) / 2, (h - 1) / 2
        d = max(abs(x - cx), abs(y - cy))
        if d < 1.2:
            return VEST['violet_hi']
        if d < 2.0:
            return VEST['amethyst']
        if d < 2.6:
            return VEST['violet']
        return None
    return p

def vest_visor():
    def p(x, y, w, h, face, name):
        if face != 'north':
            return None
        return VEST['violet'] if (x + y) % 2 else VEST['violet_dk']
    return p

def briar_emissive_none():
    return None


# ================================================================ briarweave
def build_briar():
    cs = CubeSet()
    for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)
    # helmet: low layered bark crown, thick overlapping forehead plates, narrow window
    cs.add('head', 'briar_crown', (-4.6, -8.6, -4.6), (9.2, 4.6, 9.2), briar_mossy(briar_bark(11)), 0.5)
    cs.add('head', 'briar_crown_lo', (-4.9, -4.3, -4.9), (9.8, 2.4, 9.8), briar_old(13), 0.5)
    cs.add('head', 'briar_forehead_1', (-4.3, -8.4, -5.5), (8.6, 2.2, 1.2), briar_bark(15), 0.1)
    cs.add('head', 'briar_forehead_2', (-3.7, -6.6, -5.6), (7.4, 2.0, 1.3), briar_old(17), 0.1)
    cs.add('head', 'briar_window', (-2.4, -6.9, -5.1), (4.8, 3.0, 0.8), briar_cloth(), 0.0)
    cs.add('head', 'briar_cheek_l', (4.0, -6.4, -4.3), (1.3, 4.2, 3.4), briar_bark(19), 0.05)
    cs.add('head', 'briar_cheek_r', (-5.3, -6.4, -4.3), (1.3, 4.2, 3.4), briar_bark(21), 0.05)
    cs.add('head', 'briar_rear', (-4.2, -6.6, 3.9), (8.4, 4.6, 1.3), briar_old(23), 0.05)
    cs.add('head', 'briar_root_bind_l', (4.4, -5.2, -2.4), (0.9, 3.0, 5.6), briar_lichen(briar_root_like(25)), 0.05)
    cs.add('head', 'briar_root_bind_r', (-5.3, -5.2, -2.4), (0.9, 3.0, 5.6), briar_lichen(briar_root_like(27)), 0.05)
    cs.add('head', 'briar_lichen_c', (-1.4, -9.2, 2.0), (2.4, 0.7, 2.2), briar_lichen(briar_bark(29), 0.4), 0.1)

    # body: cloth inner, harness, bark slabs, growth-ring core, back bark, belt
    cs.add('body', 'briar_inner', (-4.0, 0.6, -2.5), (8.0, 10.6, 5.0), briar_cloth(), 0.1)
    cs.add('body', 'briar_harness', (-4.3, 1.0, -2.8), (8.6, 10.0, 0.9), briar_leath(31), 0.1)
    cs.add('body', 'briar_slab_top', (-4.5, 1.2, -3.0), (9.0, 3.6, 6.1), briar_mossy(briar_bark(33)), 0.15)
    cs.add('body', 'briar_slab_mid', (-4.4, 4.6, -2.95), (8.8, 3.4, 6.0), briar_old(35), 0.15)
    cs.add('body', 'briar_slab_low', (-4.3, 7.8, -2.9), (8.6, 3.2, 5.9), briar_bark(37), 0.15)
    cs.add('body', 'briar_ring_core', (-2.2, 2.6, -3.25), (4.4, 4.4, 0.6), growth_rings(), 0.0)
    cs.add('body', 'briar_back', (-3.9, 1.6, 2.6), (7.8, 8.6, 1.1), briar_mossy(briar_old(39)), 0.1)
    cs.add('body', 'briar_belt', (-4.4, 10.6, -2.8), (8.8, 1.5, 5.6), briar_leath(41), 0.1)
    cs.add('body', 'briar_buckle', (-1.0, 10.7, -3.3), (2.0, 1.3, 0.55), briar_wood(43), 0.0)
    # bark-scale shoulders
    cs.add('shoulder_left', 'briar_sh_l', (2.9, -2.7, -2.4), (2.8, 2.8, 4.9), briar_mossy(briar_bark(45)), 0.1)
    cs.add('shoulder_left', 'briar_sh_l_lo', (3.0, 0.1, -2.2), (2.6, 1.3, 4.5), briar_old(47), 0.1)
    cs.add('shoulder_right', 'briar_sh_r', (-5.7, -2.7, -2.4), (2.8, 2.8, 4.9), briar_mossy(briar_bark(49)), 0.1)
    cs.add('shoulder_right', 'briar_sh_r_lo', (-5.6, 0.1, -2.2), (2.6, 1.3, 4.5), briar_old(51), 0.1)
    # arms: bark guard + root binding, open fingers
    cs.add('right_arm', 'briar_guard_r', (-3.4, 3.9, -2.35), (4.6, 5.2, 4.6), briar_lichen(briar_bark(53), 0.1), 0.05)
    cs.add('right_arm', 'briar_bind_r', (-3.5, 9.0, -2.45), (4.8, 1.4, 4.8), briar_root_like(55), 0.05)
    cs.add('right_arm', 'briar_cuff_r', (-3.3, 10.4, -2.3), (4.5, 1.6, 4.5), briar_leath(57), 0.05)
    cs.add('left_arm', 'briar_guard_l', (-1.2, 3.9, -2.35), (4.6, 5.2, 4.6), briar_lichen(briar_bark(59), 0.1), 0.05)
    cs.add('left_arm', 'briar_bind_l', (-1.3, 9.0, -2.45), (4.8, 1.4, 4.8), briar_root_like(61), 0.05)
    cs.add('left_arm', 'briar_cuff_l', (-1.2, 10.4, -2.3), (4.5, 1.6, 4.5), briar_leath(63), 0.05)
    # legs: bark strip skirt handled by body? no: thigh bark, root knee, ribbed greave, mossy boot
    cs.add('right_leg', 'briar_thigh_r', (-2.4, -0.4, -2.3), (4.8, 5.0, 4.6), briar_old(65), 0.05)
    cs.add('right_leg', 'briar_knee_r', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8), briar_root_like(67), 0.05)
    cs.add('right_leg', 'briar_greave_r', (-2.4, 6.2, -2.3), (4.7, 5.0, 4.6), briar_mossy(briar_bark(69), 0.1), 0.05)
    cs.add('right_leg', 'briar_boot_r', (-2.5, 11.1, -2.75), (5.0, 1.6, 5.5), briar_leath(71), 0.05)
    cs.add('left_leg', 'briar_thigh_l', (-2.4, -0.4, -2.3), (4.8, 5.0, 4.6), briar_old(72), 0.05)
    cs.add('left_leg', 'briar_knee_l', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8), briar_root_like(73), 0.05)
    cs.add('left_leg', 'briar_greave_l', (-2.4, 6.2, -2.3), (4.7, 5.0, 4.6), briar_mossy(briar_bark(74), 0.1), 0.05)
    cs.add('left_leg', 'briar_boot_l', (-2.5, 11.1, -2.75), (5.0, 1.6, 5.5), briar_leath(75), 0.05)
    cs.pack()
    return cs

def briar_root_like(seed):
    return bark(BRIAR['leather_dk'], BRIAR['leather'], (24, 17, 12), seed)


# ================================================================ vestments
def build_vest():
    cs = CubeSet()
    for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)
    cs.bone('head/antler_left_root', 'PartPose.offsetAndRotation(2.9F, -8.8F, -1.2F, 6F, 14F, -22F)')
    cs.bone('head/antler_left_trunk', 'PartPose.offsetAndRotation(-0.7F, -5.2F, -0.5F, -8F, 6F, -8F)')
    cs.bone('head/antler_left_branch_a', 'PartPose.offsetAndRotation(0.2F, -2.4F, -0.2F, -20F, 0F, 30F)')
    cs.bone('head/antler_left_branch_b', 'PartPose.offsetAndRotation(-0.6F, -2.2F, 0.4F, 14F, 0F, -26F)')
    cs.bone('head/antler_left_tip', 'PartPose.offsetAndRotation(-0.4F, -2.6F, -0.2F, -6F, 0F, -10F)')
    cs.bone('head/antler_right_root', 'PartPose.offsetAndRotation(-3.5F, -8.8F, -1.2F, 6F, -14F, 22F)')
    cs.bone('head/antler_right_trunk', 'PartPose.offsetAndRotation(-0.6F, -5.2F, -0.5F, -8F, -6F, 8F)')
    cs.bone('head/antler_right_branch_a', 'PartPose.offsetAndRotation(-0.5F, -2.4F, -0.2F, -20F, 0F, -30F)')
    cs.bone('head/antler_right_branch_b', 'PartPose.offsetAndRotation(-0.6F, -2.2F, 0.4F, 14F, 0F, 26F)')
    cs.bone('head/antler_right_tip', 'PartPose.offsetAndRotation(-0.4F, -2.6F, -0.2F, -6F, 0F, 10F)')

    # helmet: closed near-black shell + petrified crown + T visor + root cheeks
    cs.add('head', 'vest_helm', (-4.5, -8.6, -4.5), (9.0, 8.8, 9.0), vest_metal(1), 0.5)
    cs.add('head', 'vest_crown', (-4.8, -9.4, -4.8), (9.6, 2.0, 9.6), vest_bark(3), 0.5)
    cs.add('head', 'vest_brow', (-4.4, -6.4, -5.5), (8.8, 1.3, 1.2), vest_bark(5), 0.05)
    cs.add('head', 'vest_visor', (-1.1, -6.2, -5.5), (2.2, 4.6, 0.7),
           lambda x, y, w, h, face, name: VEST['violet_dk'] if (x + y) % 2 else VEST['violet'],
           0.05, emissive=vest_visor())
    cs.add('head', 'vest_visor_h', (-2.6, -4.9, -5.45), (5.2, 0.9, 0.65),
           lambda x, y, w, h, face, name: VEST['violet_dk'], 0.05,
           emissive=vest_visor())
    cs.add('head', 'vest_visor_back', (-2.7, -6.3, -4.7), (5.4, 5.0, 0.8),
           lambda x, y, w, h, face, name: VEST['cloth_in'], 0.05)
    cs.add('head', 'vest_cheek_l', (4.0, -6.2, -4.3), (1.3, 4.6, 3.4), vest_root(7), 0.05)
    cs.add('head', 'vest_cheek_r', (-5.3, -6.2, -4.3), (1.3, 4.6, 3.4), vest_root(9), 0.05)
    cs.add('head', 'vest_neck', (-4.1, -3.4, 3.6), (8.2, 3.6, 1.4), vest_bark(11), 0.05)
    # antlers: blackened branches with moss + violet fissures
    cs.add('head/antler_left_root', 'vest_antler_l_root', (-1.1, -1.2, -1.1), (2.2, 5.4, 2.2),
           vest_root(13), 0.0, emissive=vest_emissive(61, 0.1))
    cs.add('head/antler_left_trunk', 'vest_antler_l_trunk', (-0.9, -5.2, -0.9), (1.8, 5.4, 1.8),
           vest_root(15), 0.0, emissive=vest_emissive(63, 0.12))
    cs.add('head/antler_left_branch_a', 'vest_antler_l_ba', (-0.7, -3.0, -0.7), (1.4, 3.2, 1.4),
           vest_root(17), 0.0, emissive=vest_emissive(65, 0.1))
    cs.add('head/antler_left_branch_b', 'vest_antler_l_bb', (-0.7, -2.8, -0.7), (1.4, 3.0, 1.4),
           vest_root(19), 0.0)
    cs.add('head/antler_left_tip', 'vest_antler_l_tip', (-0.5, -2.4, -0.5), (1.0, 2.6, 1.0),
           vest_metal(21), 0.0)
    cs.add('head/antler_right_root', 'vest_antler_r_root', (-1.1, -5.0, -1.1), (2.2, 5.2, 2.2),
           vest_root(23), 0.0, emissive=vest_emissive(67, 0.1))
    cs.add('head/antler_right_trunk', 'vest_antler_r_trunk', (-0.9, -5.0, -0.9), (1.8, 5.2, 1.8),
           vest_root(25), 0.0, emissive=vest_emissive(69, 0.12))
    cs.add('head/antler_right_branch_a', 'vest_antler_r_ba', (-0.7, -2.8, -0.7), (1.4, 3.0, 1.4),
           vest_root(27), 0.0)
    cs.add('head/antler_right_branch_b', 'vest_antler_r_bb', (-0.7, -3.0, -0.7), (1.4, 3.2, 1.4),
           vest_root(29), 0.0, emissive=vest_emissive(71, 0.1))
    cs.add('head/antler_right_tip', 'vest_antler_r_tip', (-0.5, -2.4, -0.5), (1.0, 2.6, 1.0),
           vest_metal(31), 0.0)

    # body: dark shell, leaf plates, cavity + core, root-bound back + seam
    cs.add('body', 'vest_inner', (-4.0, 0.6, -2.5), (8.0, 10.6, 5.0),
           cloth(VEST['cloth_in'], (12, 10, 16), (34, 30, 42), 3, 3), 0.1)
    cs.add('body', 'vest_shell', (-4.4, 0.9, -2.9), (8.8, 10.2, 5.8), vest_metal(33), 0.1)
    cs.add('body', 'vest_leaf_top', (-4.5, 1.1, -3.05), (9.0, 3.4, 6.1), vest_leaf(35), 0.15)
    cs.add('body', 'vest_leaf_mid', (-4.4, 4.4, -3.0), (8.8, 3.2, 6.0), vest_leaf(37), 0.15)
    cs.add('body', 'vest_leaf_low', (-4.3, 7.5, -2.95), (8.6, 3.6, 5.9), vest_leaf(39), 0.15)
    cs.add('body', 'vest_cavity', (-2.3, 3.0, -3.3), (4.6, 5.2, 0.9),
            lambda x, y, w, h, face, name: (12, 8, 20), 0.0)
    cs.add('body', 'vest_core', (-1.6, 3.7, -3.45), (3.2, 3.8, 0.5), vest_core(), 0.0,
           emissive=vest_core())
    cs.add('body', 'vest_back', (-3.8, 1.4, 2.6), (7.6, 8.8, 1.1), vest_bark(41), 0.1)
    cs.add('body', 'vest_back_seam', (-0.5, 2.2, 3.75), (1.0, 5.6, 0.35),
           lambda x, y, w, h, face, name: VEST['violet'], 0.0, emissive=vest_core())
    cs.add('body', 'vest_belt', (-4.4, 10.6, -2.85), (8.8, 1.6, 5.7), vest_root(43), 0.1)
    # leaf-scale shoulders
    cs.add('shoulder_left', 'vest_sh_l', (2.9, -2.8, -2.45), (2.8, 2.9, 4.9), vest_leaf(45), 0.1)
    cs.add('shoulder_left', 'vest_sh_l_lo', (3.0, 0.1, -2.25), (2.6, 1.3, 4.5), vest_root(47), 0.1)
    cs.add('shoulder_right', 'vest_sh_r', (-5.7, -2.8, -2.45), (2.8, 2.9, 4.9), vest_leaf(49), 0.1)
    cs.add('shoulder_right', 'vest_sh_r_lo', (-5.6, 0.1, -2.25), (2.6, 1.3, 4.5), vest_root(51), 0.1)
    # arms: dark shell + root wrap + leaf guard with fissures
    cs.add('right_arm', 'vest_fore_r', (-3.4, 3.8, -2.35), (4.6, 5.6, 4.6), vest_metal(53), 0.05)
    cs.add('right_arm', 'vest_wrap_r', (-3.5, 9.2, -2.45), (4.8, 1.6, 4.8), vest_root(55), 0.05)
    cs.add('right_arm', 'vest_leaf_r', (-3.3, 10.6, -2.3), (4.4, 1.5, 4.4), vest_leaf(57), 0.05,
           emissive=vest_emissive(73, 0.2))
    cs.add('left_arm', 'vest_fore_l', (-1.2, 3.8, -2.35), (4.6, 5.6, 4.6), vest_metal(59), 0.05)
    cs.add('left_arm', 'vest_wrap_l', (-1.3, 9.2, -2.45), (4.8, 1.6, 4.8), vest_root(61), 0.05)
    cs.add('left_arm', 'vest_leaf_l', (-1.1, 10.6, -2.3), (4.4, 1.5, 4.4), vest_leaf(63), 0.05,
           emissive=vest_emissive(75, 0.2))
    # legs: leaf thigh, violet knee, petrified greave, boot with teleport seams
    cs.add('right_leg', 'vest_thigh_r', (-2.4, -0.4, -2.3), (4.8, 5.0, 4.6), vest_leaf(65), 0.05)
    cs.add('right_leg', 'vest_knee_r', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8),
           lambda x, y, w, h, face, name: VEST['violet'] if (x + y) % 3 else VEST['violet_dk'], 0.05)
    cs.add('right_leg', 'vest_greave_r', (-2.4, 6.2, -2.3), (4.7, 5.0, 4.6), vest_bark(67), 0.05)
    cs.add('right_leg', 'vest_boot_r', (-2.5, 11.1, -2.75), (5.0, 1.6, 5.5), vest_metal(69), 0.05,
           emissive=vest_emissive(77, 0.22))
    cs.add('left_leg', 'vest_thigh_l', (-2.4, -0.4, -2.3), (4.8, 5.0, 4.6), vest_leaf(66), 0.05)
    cs.add('left_leg', 'vest_knee_l', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8),
           lambda x, y, w, h, face, name: VEST['violet_dk'] if (x + y) % 3 else VEST['violet'], 0.05)
    cs.add('left_leg', 'vest_greave_l', (-2.4, 6.2, -2.3), (4.7, 5.0, 4.6), vest_bark(68), 0.05)
    cs.add('left_leg', 'vest_boot_l', (-2.5, 11.1, -2.75), (5.0, 1.6, 5.5), vest_metal(70), 0.05,
           emissive=vest_emissive(78, 0.22))
    cs.pack()
    return cs


def emit_union(briar, vest):
    out = java_path('com.opus.darkforest.client.model', 'DarkForestArmorModel')
    L = []
    w = L.append
    w('package com.opus.darkforest.client.model;')
    w('')
    for imp in ('com.mojang.blaze3d.vertex.PoseStack', 'com.mojang.blaze3d.vertex.VertexConsumer',
                'net.minecraft.client.model.EntityModel', 'net.minecraft.client.model.geom.ModelLayerLocation',
                'net.minecraft.client.model.geom.ModelPart', 'net.minecraft.client.model.geom.PartPose',
                'net.minecraft.client.model.geom.builders.CubeDeformation', 'net.minecraft.client.model.geom.builders.CubeListBuilder',
                'net.minecraft.client.model.geom.builders.LayerDefinition', 'net.minecraft.client.model.geom.builders.MeshDefinition',
                'net.minecraft.client.model.geom.builders.PartDefinition', 'net.minecraft.resources.ResourceLocation',
                'net.minecraft.world.entity.LivingEntity'):
        w(f'import {imp};')
    w('')
    w('/**')
    w(' * Union rig for the two dark-forest sets (see scripts/gen_armor_rework/gen_darkforest.py):')
    w(' * briarweave (ancient bark, growth-ring core, root bindings, moss/lichen, NO glow)')
    w(' * and dark forest vestments (branching antlers, petrified crown, T-visor, leaf')
    w(' * plates around a violet spatial core, teleport seams). Variant is chosen by the')
    w(' * render layer; bones of the other variant stay hidden.')
    w(' */')
    w('public final class DarkForestArmorModel<T extends LivingEntity> extends EntityModel<T> {')
    w('    public static final ModelLayerLocation BRIAR_LAYER =')
    w('        new ModelLayerLocation(new ResourceLocation("opusvsexe", "briarweave_armor"), "main");')
    w('    public static final ModelLayerLocation VESTMENTS_LAYER =')
    w('        new ModelLayerLocation(new ResourceLocation("opusvsexe", "dark_forest_vestments"), "main");')
    w('')
    w('    private final ModelPart root;')
    w('    public DarkForestArmorModel(ModelPart root) { this.root = root; }')
    w('    public ModelPart root() { return root; }')
    w('    public ModelPart head() { return root.getChild("head"); }')
    w('    public ModelPart body() { return root.getChild("body"); }')
    w('    public ModelPart rightArm() { return root.getChild("right_arm"); }')
    w('    public ModelPart leftArm() { return root.getChild("left_arm"); }')
    w('    public ModelPart rightLeg() { return root.getChild("right_leg"); }')
    w('    public ModelPart leftLeg() { return root.getChild("left_leg"); }')
    w('    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }')
    w('    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }')
    w('')
    w('    /** Per-piece visibility for the active variant (children exist per bake). */')
    w('    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet, boolean vestments) {')
    w('        head().visible = head;')
    w('        body().visible = chest;')
    w('        rightArm().visible = chest;')
    w('        leftArm().visible = chest;')
    w('        shoulderLeft().visible = chest;')
    w('        shoulderRight().visible = chest;')
    w('        if (vestments) {')
    for bone, getter in (('right_leg', 'rightLeg'), ('left_leg', 'leftLeg')):
        for c in [c for c in vest.cubes if c['bone'] == bone]:
            n = c['name']
            if any(k in n for k in ('thigh', 'hip')):
                w(f'            {getter}().getChild("{n}").visible = legs;')
            elif any(k in n for k in ('boot', 'greave', 'vent', 'sole')):
                w(f'            {getter}().getChild("{n}").visible = feet;')
            else:
                w(f'            {getter}().getChild("{n}").visible = legs || feet;')
    w('            head().getChild("antler_left_root").visible = head;')
    w('            head().getChild("antler_right_root").visible = head;')
    w('        } else {')
    for bone, getter in (('right_leg', 'rightLeg'), ('left_leg', 'leftLeg')):
        for c in [c for c in briar.cubes if c['bone'] == bone]:
            n = c['name']
            if any(k in n for k in ('thigh', 'hip')):
                w(f'            {getter}().getChild("{n}").visible = legs;')
            elif any(k in n for k in ('boot', 'greave', 'vent', 'sole')):
                w(f'            {getter}().getChild("{n}").visible = feet;')
            else:
                w(f'            {getter}().getChild("{n}").visible = legs || feet;')
    w('        }')
    w('    }')
    w('')

    for tag, cs, layer in (('createBriarLayer', briar, 'BRIAR_LAYER'), ('createVestmentsLayer', vest, 'VESTMENTS_LAYER')):
        w(f'    public static LayerDefinition {tag}() {{')
        w('        MeshDefinition mesh = new MeshDefinition();')
        w('        PartDefinition root = mesh.getRoot();')
        for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg'):
            w(f'        PartDefinition {b} = root.addOrReplaceChild("{b}", CubeListBuilder.create(), PartPose.ZERO);')
        w('        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));')
        w('        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));')
        # child bones (antlers)
        for pth, pose in cs.bone_poses.items():
            if '/' not in pth:
                continue
            parent, name = pth.split('/')
            w(f'        PartDefinition {name} = {parent}.addOrReplaceChild("{name}", CubeListBuilder.create(), {pose});')
        targets = {b: b for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg',
                                  'shoulder_left', 'shoulder_right')}
        for pth in cs.bone_poses:
            if '/' in pth:
                targets[pth] = pth.rsplit('/', 1)[1]
        L.extend(cube_list_lines(cs, targets))
        w(f'        return LayerDefinition.create(mesh, {cs.atlas}, {cs.atlas});')
        w('    }')
        w('')
    w('    @Override')
    w('    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks,')
    w('                          float netHeadYaw, float headPitch) {')
    w('    }')
    w('    @Override')
    w('    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay,')
    w('                               float red, float green, float blue, float alpha) {')
    w('        root.render(poseStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);')
    w('    }')
    w('}')
    with open(out, 'w') as f:
        f.write('\n'.join(L) + '\n')
    print(f'wrote {out}')


if __name__ == '__main__':
    briar = build_briar()
    vest = build_vest()
    emit_union(briar, vest)
    outd = os.path.join(A, 'textures/dark_forest/armor')
    os.makedirs(outd, exist_ok=True)
    bi, _ = briar.paint_atlas(BRIAR)
    bi.save(os.path.join(outd, 'briarweave.png'))
    vi, ve = vest.paint_atlas(VEST)
    vi.save(os.path.join(outd, 'dark_forest_vestments.png'))
    ve.save(os.path.join(outd, 'dark_forest_vestments_emissive.png'))
    print('dark forest atlases saved')
