#!/usr/bin/env python3
"""Full from-scratch rebuild of the Diablo rig (fire_demon).

Original horned devil ruler: volcanic plates, digitigrade hooved legs, long tail,
mane, waistcloth. No wings (user rework directive 2026-08-31, see
concepts/mobs/diablo/REWORK.md). Gameplay timings of FireDemonEntity are preserved:
awaken 2.0, melee 0.9 (impact .45), toss 1.5 (impact .8), fireball 1.7 (spawn 1.0),
aura 2.6 (waves 1.2/1.5/1.8), trident 1.8 (release .85), summon 2.2 (spawn 1.2),
death 2.5.

Conventions (match project's verified framework):
- entity front = -Z (north face of cubes); entity left = +X
- animation rotation keyframes are ABSOLUTE bone rotations (replace geo rest rotation)
- -X rotation = tilt toward the face (lean forward / look down / jaw open)
- +Z rotation swings a hanging limb toward +X (outward for the left side)
Run from repo root:  python3 scripts/gen_mob_rework/devil.py
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import (Model, build_anim, track, h01, vnoise, mix, shade, c01,
                       noisy, edge_darken, overlay_faces)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
A = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'opusvsexe')

# ------------------------------------------------------------------ palette
SKIN      = (134, 32, 42)    # deep blood red
SKIN_DK   = (92, 22, 30)     # dark crimson shadow
SKIN_DD   = (56, 16, 22)     # crease / deep shadow
SKIN_HI   = (166, 58, 44)    # burnt red highlight
SKIN_HI2  = (180, 84, 58)    # muted red-orange (sparse)
CHAR      = (36, 16, 20)     # charred extremity
CHAR_DK   = (22, 12, 15)
PLATE     = (31, 18, 22)     # charred volcanic plate
PLATE_HI  = (58, 42, 48)     # dark volcanic gray facet
PLATE_MID = (74, 38, 46)     # red-black reflected midtone
ASH       = (113, 99, 106)   # sparse worn ash edge
HORN      = (25, 18, 22)
HORN_RIDGE= (52, 42, 48)
HORN_ROOT = (87, 24, 32)
CLOTH     = (30, 24, 28)
CLOTH_DK  = (20, 15, 18)
CLOTH_WN  = (62, 36, 40)     # dark red-brown wear
CLOTH_FR  = (90, 74, 80)     # ash fray
IRON      = (46, 37, 43)
IRON_HI   = (80, 65, 74)
IRON_DK   = (28, 22, 26)
TOOTH     = (138, 122, 102)
MOUTH     = (20, 9, 12)
TONGUE    = (74, 26, 32)
ICE       = (143, 31, 50)    # blood glass family
ICE_HI    = (188, 66, 84)
ICE_DK    = (94, 20, 36)
ICE_HOT   = (216, 58, 31)
GLOW_IRIS = (255, 120, 40)
GLOW_CORE = (255, 214, 140)
GLOW_CRACK= (240, 80, 28)
GLOW_CRACK_HI = (255, 160, 60)

# base pose (absolute bone degrees)
B_UL, B_LL, B_HK, B_HF = -10.0, 26.0, -30.0, 14.0


# ------------------------------------------------------------------ painters
def skin(seed=1, darken=0.0):
    """Thick leathery blood-red hide: large clumps, sparse rough patches, creases."""
    base = noisy(SKIN, SKIN_DK, SKIN_HI, seed)
    def p(x, y, w, h, face):
        c = base(x, y, w, h, face)
        n = vnoise(x, y, seed + 40, 5)
        if n < 0.22:
            c = mix(c, SKIN_DD, 0.55)
        if h01(x // 3, y // 3, seed + 44) > 0.93:
            c = mix(c, SKIN_HI2, 0.4)
        if darken > 0:
            c = mix(c, CHAR if darken > 0.5 else SKIN_DD, darken)
        if y >= h - 1 and h > 3:
            c = mix(c, SKIN_DD, 0.4)
        return c
    return p


def plate(seed=2, ember=False):
    """Hard black volcanic growth: jagged facets, chipped edges, optional fissures."""
    def p(x, y, w, h, face):
        n = vnoise(x, y, seed, 2)
        if n > 0.66:
            c = mix(PLATE, PLATE_HI, 0.6)
        elif n > 0.4:
            c = mix(PLATE, PLATE_MID, 0.35)
        elif n < 0.2:
            c = shade(PLATE, 0.75)
        else:
            c = PLATE
        if h01(x, y, seed + 9) > 0.94:
            c = mix(c, ASH, 0.5)
        if y == 0:
            c = mix(c, PLATE_HI, 0.45)
        if y == h - 1:
            c = shade(c, 0.7)
        if x == 0 or x == w - 1:
            c = shade(c, 0.82)
        if ember and h01(x, y // 2, seed + 15) > 0.965 and 0 < y < h - 1:
            c = GLOW_CRACK if h01(x, y, seed + 16) > 0.6 else mix(c, GLOW_CRACK, 0.5)
        return c
    return p


def horn(seed=3, root_t=0.0):
    """Charred horn material: stepped growth rings, volcanic ridges, dark tip."""
    def p(x, y, w, h, face):
        ring = y % 4
        if ring == 0:
            c = mix(HORN, HORN_RIDGE, 0.55)
        elif ring == 3:
            c = shade(HORN, 0.72)
        else:
            c = HORN
        if h01(x // 2, y, seed) > 0.92:
            c = mix(c, HORN_RIDGE, 0.4)
        if root_t > 0 and y > h * (1.0 - root_t):
            c = mix(c, HORN_ROOT, 0.65)
        if h01(x, y // 3, seed + 5) > 0.95:
            c = ASH if h01(x, y, seed + 6) > 0.5 else shade(c, 1.25)
        return c
    return p


def claw_p():
    def p(x, y, w, h, face):
        c = HORN
        if y == 0:
            c = mix(HORN, HORN_RIDGE, 0.5)
        if y == h - 1 or x == w - 1:
            c = shade(HORN, 0.6)
        if h01(x, y, 91) > 0.93:
            c = mix(c, ASH, 0.35)
        return c
    return p


def cloth(seed=4):
    """Heavy charcoal weave, worn dark-red edges, sparse ash fray."""
    def p(x, y, w, h, face):
        n = vnoise(x, y // 2, seed, 2)
        c = CLOTH
        if n > 0.62:
            c = mix(CLOTH, (44, 36, 42), 0.5)
        elif n < 0.3:
            c = mix(CLOTH, CLOTH_DK, 0.6)
        if h01(x, y, seed + 21) > 0.95:
            c = mix(c, CLOTH_WN, 0.55)
        if y == 0:
            c = mix(c, CLOTH_WN, 0.35)
        if y >= h - 1:
            c = CLOTH_FR if h01(x, y, seed + 22) > 0.6 else CLOTH_DK
        return c
    return p


def belt_p():
    def p(x, y, w, h, face):
        c = IRON
        if y == 0:
            c = IRON_HI
        if y == h - 1:
            c = IRON_DK
        if h01(x, y, 61) > 0.9:
            c = mix(c, IRON_HI, 0.5)
        if h01(x * 2, y, 62) < 0.08:
            c = mix(c, PLATE_MID, 0.5)
        return c
    return p


def buckle_p():
    def p(x, y, w, h, face):
        cx, cy = (w - 1) / 2, (h - 1) / 2
        d = max(abs(x - cx), abs(y - cy))
        if face != 'north':
            return belt_p()(x, y, w, h, face)
        if d > min(cx, cy) - 1.2:
            return IRON_HI if (x + y) % 3 else IRON
        if d < 1.0:
            return shade(IRON_DK, 0.7)
        return IRON
    return p


def ice_p():
    """Translucent crimson cryolde: angular facets, dark streaks, sparse hot edges."""
    def p(x, y, w, h, face):
        n = vnoise(x, y, 77, 3)
        if n > 0.64:
            c = (ICE_HI[0], ICE_HI[1], ICE_HI[2], 172)
        elif n < 0.3:
            c = (ICE_DK[0], ICE_DK[1], ICE_DK[2], 132)
        else:
            c = (ICE[0], ICE[1], ICE[2], 152)
        if h01(x // 2, y // 7, 78) > 0.94:
            c = (ICE_HOT[0], ICE_HOT[1], ICE_HOT[2], 190)
        if y == 0:
            c = (c[0] + 30, c[1] + 18, c[2] + 16, c[3])
        return c
    return p


def trident_p():
    def p(x, y, w, h, face):
        c = mix(IRON_DK, IRON, 0.4 + 0.3 * h01(x, y // 2, 81))
        if y == 0:
            c = IRON_HI
        if h01(x, y, 82) > 0.95:
            c = mix(c, PLATE_MID, 0.6)
        return c
    return p


def face_p():
    """Head north face: heavy brow, ember eyes, angular nose, stern mouth, chin nodules."""
    def p(x, y, w, h, face):
        c = skin(11)(x, y, w, h, face)
        cx = (w - 1) / 2
        lx, rx = int(round(cx - w * 0.28)), int(round(cx + w * 0.28))
        if y <= 1:
            c = mix(c, SKIN_DD, 0.4 if y == 1 else 0.2)
        if y == 2:
            if lx <= x <= lx + 1 or rx <= x <= rx + 1:
                return GLOW_IRIS if x in (lx, rx + 1) else GLOW_CORE
        if y == 3:
            if lx <= x <= lx + 1 or rx <= x <= rx + 1:
                c = mix(CHAR, SKIN_DD, 0.4)
            elif abs(x - cx) <= 1:
                c = mix(c, SKIN_DK, 0.5)
            elif x == 0 or x == w - 1:
                c = mix(c, SKIN_HI, 0.45)
        if y == 4:
            if abs(x - cx) <= 1:
                c = mix(c, SKIN_DD, 0.6 if y == 4 else 0.3)
            if x == int(cx) - 1 or x == int(cx) + 1:
                c = mix(c, CHAR, 0.45)
            elif x == 0 or x == w - 1:
                c = mix(c, SKIN_HI, 0.3)
        if y == h - 2:
            if 1 <= x <= w - 2:
                c = mix(c, SKIN_DD, 0.75)
        if y == h - 1:
            c = mix(c, SKIN_DK, 0.35)
            if x == int(cx) - 2 or x == int(cx) + 2:
                c = CHAR_DK
        return c
    return p


def face_emissive():
    def p(x, y, w, h, face):
        cx = (w - 1) / 2
        lx, rx = int(round(cx - w * 0.28)), int(round(cx + w * 0.28))
        if face == 'north' and y == 2:
            if x in (lx, rx + 1):
                return GLOW_IRIS
            if x in (lx + 1, rx):
                return GLOW_CORE
        return (0, 0, 0, 0)
    return p


def mouth_interior():
    """Mouth cavity for open-jaw frames: near-black, dark-red tongue, muted teeth."""
    def p(x, y, w, h, face):
        c = MOUTH
        if y == 0:
            c = TONGUE if abs(x - (w - 1) / 2) <= w * 0.2 else shade(MOUTH, 1.4)
        if face == 'north' and y >= h - 2:
            c = TOOTH if h01(x, 3, 71) > 0.45 else shade(TOOTH, 0.7)
        if face == 'south' and y <= 1:
            c = TOOTH if h01(x, 5, 72) > 0.45 else shade(TOOTH, 0.7)
        return c
    return p


def emissive_none():
    return lambda x, y, w, h, face: (0, 0, 0, 0)


def crack_emissive(seed):
    """Deterministic broken vertical ember seam on the north face (restrained)."""
    def p(x, y, w, h, face):
        if face != 'north' or w < 2:
            return (0, 0, 0, 0)
        if x == w // 2 and (y * 5 + seed) % 7 < 3:
            return GLOW_CRACK_HI if (y + seed) % 3 == 0 else GLOW_CRACK
        return (0, 0, 0, 0)
    return p


# ------------------------------------------------------------------ geometry
def build_devil():
    m = Model('demon', 256, 256, visible_bounds=(9, 7.5))

    skin_side = {'right': skin(21), 'left': skin(23)}
    plate_side = {'right': plate(31, True), 'left': plate(37, True)}

    m.bone('root', [0, 0, 0])
    m.bone('master', [0, 25, 0], 'root')

    # ---------------- pelvis / hips ----------------
    m.bone('pelvis', [0, 25, 0], 'master', cubes=[
        {'o': [-4.8, -2.2, -3.1], 's': [9.6, 5.5, 6.2], 'paint': skin(13)}])

    m.bone('body', [0, 27, 0], 'pelvis', cubes=[
        {'o': [-4.9, -1.2, -3.4], 's': [9.8, 6.5, 6.6], 'paint': skin(15)}])
    m.bone('abdomen', [0, 28.5, 0], 'body', cubes=[
        {'o': [-4.6, -1.8, -3.2], 's': [9.2, 5.4, 6.2], 'paint': skin(17)}])
    m.bone('mane_middle', [0, 31, 5.0], 'abdomen', cubes=[
        {'o': [-2.3, -6.2, 0.0], 's': [4.6, 7.2, 1.6], 'paint': horn(41)}])

    # ---------------- chest ----------------
    m.bone('chest', [0, 33, 0], 'body', cubes=[
        {'o': [-6.5, -1.5, -4.4], 's': [13.0, 10.5, 8.2], 'paint': skin(19)},
        {'o': [-6.3, 3.0, -4.9], 's': [5.2, 4.4, 1.4], 'paint': skin(25, 0.15)},
        {'o': [1.1, 3.0, -4.9], 's': [5.2, 4.4, 1.4], 'paint': skin(27, 0.15)}])

    m.bone('sternum_plate', [0, 39.5, -4.6], 'chest', cubes=[
        {'o': [-1.3, -2.6, -0.7], 's': [2.6, 4.6, 1.4], 'paint': plate(33, True),
         'emissive': crack_emissive(301)},
        {'o': [-1.1, -6.6, -0.65], 's': [2.2, 4.2, 1.3], 'paint': plate(35, True),
         'emissive': crack_emissive(303)}])
    m.bone('spine_plate', [0, 38.5, 4.0], 'chest', cubes=[
        {'o': [-2.2, -2.0, -0.7], 's': [4.4, 3.6, 1.4], 'paint': plate(39)},
        {'o': [-1.9, -5.2, -0.65], 's': [3.8, 3.4, 1.3], 'paint': plate(43)}])

    # ---------------- neck / head ----------------
    m.bone('neck', [0, 42.5, 0.4], 'chest', cubes=[
        {'o': [-2.5, -1.8, -2.8], 's': [5.0, 4.0, 5.2], 'paint': skin(29, 0.25)}])
    m.bone('head', [0, 44.2, 0.2], 'neck', cubes=[
        {'o': [-4.0, 0.0, -4.2], 's': [8.0, 7.0, 8.0], 'paint': overlay_faces(
            {'north': face_p(), 'bottom': mouth_interior()}, skin(11)),
         'emissive': face_emissive()},
        {'o': [-4.2, 4.6, -4.9], 's': [8.4, 1.6, 1.4], 'paint': skin(31, 0.35)}])

    m.bone('jaw', [0, 45.0, -1.4], 'head', cubes=[
        {'o': [-2.8, -3.0, -3.2], 's': [5.6, 2.6, 5.4],
         'paint': overlay_faces({'top': mouth_interior()}, skin(45, 0.25))}])
    for side, sgn in (('left', 1), ('right', -1)):
        m.bone(f'lower_tusk_{side}', [sgn * 2.0, 42.6, -4.0], 'jaw', rot=[-10, 0, 0], cubes=[
            {'o': [sgn * -0.5 - 0.5 * 0, -0.6, -0.6], 's': [1.0, 1.8, 1.0], 'paint': claw_p()}])

    # mane: skull crest + spine locks
    m.bone('mane_head', [0, 48.5, 3.6], 'head', rot=[-8, 0, 0], cubes=[
        {'o': [-2.7, -1.4, 0.0], 's': [5.4, 3.2, 1.8], 'paint': horn(47)},
        {'o': [-2.0, -6.2, 0.2], 's': [4.0, 5.0, 1.5], 'paint': horn(49)}])
    m.bone('mane_upper', [0, 40, 5.0], 'chest', cubes=[
        {'o': [-2.4, -5.6, 0.0], 's': [4.8, 6.4, 1.6], 'paint': horn(51)}])
    m.bone('mane_lower', [0, 27, 4.9], 'pelvis', cubes=[
        {'o': [-1.9, -4.2, 0.0], 's': [3.8, 5.4, 1.4], 'paint': horn(53)}])

    # ---------------- horns: out, up, back, taper ----------------
    horn_side = {'left': horn(55, 0.5), 'right': horn(59, 0.5)}
    for side, sgn in (('left', 1), ('right', -1)):
        hp = horn_side[side]
        seg = [
            ('horn_%s_root' % side, [sgn * 3.0, 48.6, 0.6], None, [0, 0, sgn * 38],
             {'o': [sgn * 0.4, -1.5, -1.7], 's': [3.4, 3.0, 3.4]}),
            ('horn_%s_01' % side, [sgn * 6.0, 49.2, 0.6], 'horn_%s_root' % side, [-12, 0, sgn * 44],
             {'o': [sgn * -1.3, 0.9, -1.5], 's': [3.0, 3.8, 3.0]}),
            ('horn_%s_02' % side, [sgn * 8.2, 52.6, 0.0], 'horn_%s_01' % side, [-18, 0, sgn * 30],
             {'o': [sgn * -1.2, 1.3, -1.3], 's': [2.6, 4.2, 2.6]}),
            ('horn_%s_03' % side, [sgn * 9.6, 56.2, -1.0], 'horn_%s_02' % side, [-26, 0, sgn * 14],
             {'o': [sgn * -1.0, 1.3, -1.1], 's': [2.2, 3.9, 2.2]}),
            ('horn_%s_04' % side, [sgn * 9.8, 59.6, -2.4], 'horn_%s_03' % side, [-38, 0, sgn * -2],
             {'o': [sgn * -0.9, 1.1, -0.9], 's': [1.8, 3.4, 1.8]}),
            ('horn_%s_tip' % side, [sgn * 9.6, 62.2, -4.0], 'horn_%s_04' % side, [-30, 0, sgn * -10],
             {'o': [sgn * -0.65, 0.7, -0.65], 's': [1.3, 2.7, 1.3]}),
        ]
        for idx, (name, pivot, parent, rot, cube) in enumerate(seg):
            spec = dict(cube)
            spec['paint'] = hp
            if idx in (2, 4):
                spec['emissive'] = crack_emissive(311 if side == 'left' else 313)
            m.bone(name, pivot, parent, rot=rot, cubes=[spec])
        m.bone(f'horn_stub_{side}', [sgn * 1.6, 49.8, 2.6], 'head', rot=[-30, 0, sgn * 18], cubes=[
            {'o': [sgn * -0.6, 0.0, -0.6], 's': [1.2, 1.8, 1.2], 'paint': horn(63)}])

    # ---------------- arms ----------------
    for side, sgn in (('left', 1), ('right', -1)):
        sk, pl = skin_side[side], plate_side[side]
        z_out = sgn * 3
        m.bone(f'{side}_arm', [sgn * 10.2, 39.5, -0.2], 'pelvis', rot=[0, 0, z_out], cubes=[
            {'o': [sgn * -3.1 - sgn * 1.0, -1.9, -2.6], 's': [4.6, 4.2, 5.0], 'paint': pl}])
        m.bone(f'{side}_upper_arm', [sgn * 9.8, 36.0, -0.2], f'{side}_arm', rot=[0, 0, z_out * 0.6], cubes=[
            {'o': [-2.1, -6.4, -2.4], 's': [4.2, 7.5, 4.6], 'paint': sk}])
        m.bone(f'{side}_forearm', [sgn * 9.9, 29.4, -0.2], f'{side}_upper_arm', rot=[-6, 0, 0], cubes=[
            {'o': [-2.0, -6.2, -2.3], 's': [4.0, 7.0, 4.4], 'paint': skin(65 if side == 'left' else 67, 0.45)}])
        m.bone(f'{side}_forearm_plate', [sgn * 9.9, 28.0, -0.2], f'{side}_forearm', cubes=[
            {'o': [sgn * 1.2, -5.0, -2.4], 's': [1.4, 5.6, 4.6], 'paint': pl,
             'emissive': crack_emissive(321 if side == 'left' else 323)}])
        m.bone(f'{side}_hand', [sgn * 9.9, 22.4, -0.2], f'{side}_forearm', cubes=[
            {'o': [-2.0, -3.2, -2.4], 's': [4.0, 3.6, 4.4], 'paint': skin(69 if side == 'left' else 70, 0.75)}])
        claws = [
            {'o': [sgn * -2.5, -2.4, -1.0], 's': [1.0, 2.8, 1.0], 'paint': claw_p(), 'rot': [-25, 0, 0]},
            {'o': [sgn * -1.25 - 0.5, -2.6, -1.1], 's': [1.0, 2.6, 1.0], 'paint': claw_p(), 'rot': [-28, 0, 0]},
            {'o': [-0.5 * sgn + 0.25 * sgn, -2.7, -1.15], 's': [1.0, 2.7, 1.0], 'paint': claw_p(), 'rot': [-28, 0, 0]},
            {'o': [sgn * 0.9, -2.5, -1.05], 's': [1.0, 2.4, 1.0], 'paint': claw_p(), 'rot': [-24, 0, 0]},
        ]
        m.bone(f'{side}_claws', [sgn * 9.9, 19.4, -0.2], f'{side}_hand', cubes=claws)

    m.bone('weapon_anchor', [-9.9, 20.2, -2.8], 'right_hand')
    m.bone('trident', [-9.9, 20.2, -2.8], 'weapon_anchor', cubes=[
        {'o': [-0.55, 0.0, -0.55], 's': [1.1, 13.0, 1.1], 'paint': trident_p()},
        {'o': [-3.6, 12.2, -0.6], 's': [7.2, 1.3, 1.3], 'paint': trident_p()},
        {'o': [-3.6, 12.2, -0.6], 's': [1.1, 6.5, 1.3], 'paint': trident_p()},
        {'o': [-0.55, 12.2, -0.6], 's': [1.1, 9.5, 1.3], 'paint': trident_p()},
        {'o': [2.5, 12.2, -0.6], 's': [1.1, 6.5, 1.3], 'paint': trident_p()}])

    # ---------------- digitigrade legs ----------------
    for side, sgn in (('left', 1), ('right', -1)):
        sk, pl = skin_side[side], plate_side[side]
        m.bone(f'{side}_leg', [sgn * 4.6, 25.0, 0.5], 'pelvis')
        m.bone(f'{side}_upper_leg', [sgn * 4.6, 25.0, 0.5], f'{side}_leg', rot=[B_UL, 0, 0], cubes=[
            {'o': [-2.4, -8.0, -2.8], 's': [4.8, 9.5, 5.2], 'paint': sk}])
        m.bone(f'{side}_thigh_plate', [sgn * 4.6, 23.0, 0.5], f'{side}_upper_leg', cubes=[
            {'o': [sgn * -3.3 - sgn * 0.0 + (sgn * -0.9 if sgn < 0 else 0), -6.5, -2.6],
             's': [1.6, 6.0, 4.8], 'paint': pl,
             'emissive': crack_emissive(331 if side == 'left' else 333)}])
        m.bone(f'{side}_lower_leg', [sgn * 4.6, 16.5, -0.9], f'{side}_upper_leg', rot=[B_LL, 0, 0], cubes=[
            {'o': [-2.1, -7.4, -2.5], 's': [4.2, 8.0, 4.6], 'paint': skin(73 if side == 'left' else 75, 0.55)}])
        m.bone(f'{side}_hock', [sgn * 4.6, 9.6, 0.4], f'{side}_lower_leg', rot=[B_HK, 0, 0], cubes=[
            {'o': [-1.8, -3.6, -2.2], 's': [3.6, 4.2, 4.2], 'paint': skin(77 if side == 'left' else 79, 0.8)}])
        hoof_paint = plate(83 if side == 'left' else 87)
        m.bone(f'{side}_hoof', [sgn * 4.6, 6.4, -0.8], f'{side}_hock', rot=[B_HF, 0, 0], cubes=[
            {'o': [-2.0, -6.2, -2.7], 's': [1.9, 6.2, 4.8], 'paint': hoof_paint},
            {'o': [0.1, -6.2, -2.7], 's': [1.9, 6.2, 4.8], 'paint': hoof_paint}])

    # ---------------- belt + waistcloth ----------------
    m.bone('belt', [0, 25.0, 0], 'pelvis', cubes=[
        {'o': [-5.3, -1.0, -3.6], 's': [10.6, 2.0, 7.2], 'paint': belt_p()},
        {'o': [-1.4, -1.4, -4.4], 's': [2.8, 2.8, 1.4], 'paint': buckle_p()}])
    m.bone('waistcloth_front', [0, 24.2, -3.9], 'pelvis', cubes=[
        {'o': [-3.4, -8.4, -0.4], 's': [6.8, 8.6, 1.5], 'paint': cloth(93)}])
    m.bone('waistcloth_left', [5.05, 24.2, 0], 'pelvis', cubes=[
        {'o': [0.0, -7.4, -2.7], 's': [1.5, 7.6, 5.4], 'paint': cloth(95)}])
    m.bone('waistcloth_right', [-5.05, 24.2, 0], 'pelvis', cubes=[
        {'o': [-1.5, -7.4, -2.7], 's': [1.5, 7.6, 5.4], 'paint': cloth(97)}])
    m.bone('waistcloth_back_left', [1.7, 24.2, 3.4], 'pelvis', cubes=[
        {'o': [-1.7, -7.6, -0.4], 's': [3.4, 7.8, 1.5], 'paint': cloth(99)}])
    m.bone('waistcloth_back_right', [-1.7, 24.2, 3.4], 'pelvis', cubes=[
        {'o': [-1.7, -7.6, -0.4], 's': [3.4, 7.8, 1.5], 'paint': cloth(101)}])

    # ---------------- tail ----------------
    tail_paint = [skin(103, t) for t in (0.0, 0.12, 0.24, 0.38, 0.52, 0.66, 0.8)]
    tail_spec = [
        ('tail_root', [0, 25.6, 3.8], None, [-1.7, -1.6, -0.4], [3.4, 3.2, 4.2]),
        ('tail_01', [0.8, 24.2, 7.4], 'tail_root', [-1.5, -1.45, -0.4], [3.0, 2.9, 4.2]),
        ('tail_02', [1.8, 22.4, 11.0], 'tail_01', [-1.35, -1.3, -0.4], [2.7, 2.6, 4.2]),
        ('tail_03', [2.6, 20.2, 14.4], 'tail_02', [-1.2, -1.15, -0.4], [2.4, 2.3, 4.2]),
        ('tail_04', [3.0, 17.8, 17.6], 'tail_03', [-1.05, -1.0, -0.4], [2.1, 2.0, 4.2]),
        ('tail_05', [2.8, 15.4, 20.4], 'tail_04', [-0.9, -0.85, -0.4], [1.8, 1.7, 3.8]),
        ('tail_06', [2.0, 13.4, 22.6], 'tail_05', [-0.75, -0.7, -0.35], [1.5, 1.4, 3.2]),
    ]
    for i, (name, pivot, parent, o, s) in enumerate(tail_spec):
        m.bone(name, pivot, parent, cubes=[
            {'o': o, 's': s, 'paint': tail_paint[i]}])
    m.bone('tail_tip', [1.2, 12.2, 24.4], 'tail_06', cubes=[
        {'o': [-0.8, -0.7, -0.3], 's': [1.6, 1.4, 1.6], 'paint': plate(105, True),
         'emissive': crack_emissive(341)},
        {'o': [-0.45, -0.4, 1.1], 's': [0.9, 0.8, 2.2], 'paint': plate(107, True),
         'emissive': crack_emissive(343)}])

    # ---------------- cryolde prison (static, children of root) ----------------
    ip = ice_p()
    m.bone('ice_front', [0, 32, -9.2], 'root', cubes=[
        {'o': [-10.0, -32.0, -0.8], 's': [20.0, 64.0, 1.6], 'paint': ip}])
    m.bone('ice_back', [0, 32, 9.2], 'root', cubes=[
        {'o': [-10.0, -32.0, -0.8], 's': [20.0, 64.0, 1.6], 'paint': ip}])
    m.bone('ice_left', [10.8, 32, 0], 'root', cubes=[
        {'o': [-0.8, -32.0, -7.6], 's': [1.6, 64.0, 15.2], 'paint': ip}])
    m.bone('ice_right', [-10.8, 32, 0], 'root', cubes=[
        {'o': [-0.8, -32.0, -7.6], 's': [1.6, 64.0, 15.2], 'paint': ip}])
    m.bone('ice_top', [0, 64.8, 0], 'root', cubes=[
        {'o': [-10.8, -0.8, -9.2], 's': [21.6, 1.6, 18.4], 'paint': ip}])
    m.bone('ice_floor', [0, -0.4, 0], 'root', cubes=[
        {'o': [-10.8, -0.4, -9.2], 's': [21.6, 0.8, 18.4], 'paint': ip}])

    m.absolutize_origins()
    return m


# ------------------------------------------------------------------ animation helpers
def cyc(fn, d, n=14, phase=0.0):
    """Sample a phase function fn(p in [0,1)) -> [x,y,z] into a closed loop track."""
    keys = []
    for i in range(n):
        p = (i / n + phase) % 1.0
        t = round(d * (i / n), 3)
        keys.append((t, [round(v, 2) for v in fn(p)]))
    keys.append((d, [round(v, 2) for v in fn(phase % 1.0)]))
    return track(keys)


def leg_walk(sgn_phase):
    """Digitigrade gait: stance + swing with knee/hock/hoof coordination.
    p=0 is foot contact (forward), stance to p=0.5 (push-off), swing p=0.5..1."""
    def ul(p):
        return [-9 - 25 * math.cos(2 * math.pi * p), 0, 0]
    def ll(p):
        return [B_LL + 4 + 34 * max(0.0, math.sin(2 * math.pi * (p - 0.25))), 0, 0]
    def hk(p):
        return [B_HK - 4 + 12 * max(0.0, math.sin(2 * math.pi * (p - 0.20)))
                - 14 * max(0.0, math.sin(2 * math.pi * (p - 0.45))), 0, 0]
    def hf(p):
        return [B_HF - 2 + 10 * max(0.0, math.sin(2 * math.pi * (p - 0.15)))
                - 10 * max(0.0, math.sin(2 * math.pi * (p - 0.50))), 0, 0]
    def sh(fn):
        def g(p):
            return fn((p - sgn_phase) % 1.0)
        return g
    return ul, ll, hk, hf, sh


def tail_sway(amp, keys_fn):
    """Coordinated tail wave: each segment lags the previous one."""
    out = {}
    segs = ['tail_root', 'tail_01', 'tail_02', 'tail_03', 'tail_04', 'tail_05', 'tail_06', 'tail_tip']
    for i, name in enumerate(segs):
        out[name] = keys_fn(i, amp)
    return out


# ------------------------------------------------------------------ animations
def devil_anims():
    an = {}

    # ----- sealed: barely alive inside the cryolde -----
    an['sealed'] = build_anim('sealed', 3.0, {
        'chest': {'scale': track([(0, [1, 1, 1]), (1.5, [1.012, 1.012, 1.012]), (3.0, [1, 1, 1])])},
        'tail_05': {'rotation': track([(0, [0, 0, 0]), (1.5, [-1.5, 0, 0]), (3.0, [0, 0, 0])])},
        'tail_06': {'rotation': track([(0, [0, 0, 0]), (1.5, [1.5, 0, 0]), (3.0, [0, 0, 0])])},
    })

    # ----- idle: slow regal breathing, occasional deliberate head turn -----
    an['idle'] = build_anim('idle', 2.4, {
        'chest': {'scale': track([(0, [1, 1, 1]), (1.2, [1.02, 1.025, 1.02]), (2.4, [1, 1, 1])])},
        'body': {'rotation': track([(0, [0.5, 0, 0]), (1.2, [0, 0, 0.6]), (2.4, [0.5, 0, 0])]),
                 'position': track([(0, [0, 0, 0]), (1.2, [0, -0.25, 0]), (2.4, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (1.2, [-1.2, 0, 4.2]), (2.4, [0, 0, 3])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (1.2, [-1.2, 0, -4.2]), (2.4, [0, 0, -3])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.8, [-1, 8, 0]), (1.6, [0.5, -6, 0]), (2.4, [0, 0, 0])])},
        'neck': {'rotation': track([(0, [0, 0, 0]), (1.2, [0.8, 0, 0]), (2.4, [0, 0, 0])])},
        'mane_head': {'rotation': track([(0, [-8, 0, 0]), (1.2, [-9, 0, 0]), (2.4, [-8, 0, 0])])},
        'mane_upper': {'rotation': track([(0, [0, 0, 0]), (1.2, [-1.2, 0, 0]), (2.4, [0, 0, 0])])},
        'waistcloth_front': {'rotation': track([(0, [0, 0, 0]), (1.2, [-0.8, 0, 0]), (2.4, [0, 0, 0])])},
        **tail_sway(3.0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]),
            (round(0.6 + 0.25 * i, 2), [-amp * 0.4 if i < 4 else amp * 0.6, (1 if i % 2 else -1) * amp * 0.5, 0]),
            (round(1.5 + 0.2 * i, 2) if 1.5 + 0.2 * i < 2.4 else 2.3, [amp * 0.3, 0, 0]),
            (2.4, [0, 0, 0])])}),
    })

    # ----- walk: heavy, deliberate, digitigrade -----
    d = 1.0
    ul, ll, hk, hf, sh = leg_walk(0.0)
    ul2, ll2, hk2, hf2, sh2 = leg_walk(0.5)
    an['walk'] = build_anim('walk', d, {
        'right_upper_leg': {'rotation': cyc(sh(ul), d)},
        'right_lower_leg': {'rotation': cyc(sh(ll), d)},
        'right_hock': {'rotation': cyc(sh(hk), d)},
        'right_hoof': {'rotation': cyc(sh(hf), d)},
        'left_upper_leg': {'rotation': cyc(sh2(ul2), d)},
        'left_lower_leg': {'rotation': cyc(sh2(ll2), d)},
        'left_hock': {'rotation': cyc(sh2(hk2), d)},
        'left_hoof': {'rotation': cyc(sh2(hf2), d)},
        'pelvis': {'position': cyc(lambda p: [0, -0.15 + 0.5 * abs(math.sin(math.pi * 2 * p)), 0], d),
                   'rotation': cyc(lambda p: [0, 0, 1.6 * math.sin(2 * math.pi * p)], d)},
        'body': {'rotation': cyc(lambda p: [-4 + 0.8 * math.sin(2 * math.pi * p), 2.5 * math.sin(2 * math.pi * p + math.pi), 0], d)},
        'head': {'rotation': cyc(lambda p: [4 - 1 * math.sin(2 * math.pi * p), -2.5 * math.sin(2 * math.pi * p + math.pi), 0], d)},
        'right_arm': {'rotation': cyc(lambda p: [14 * math.cos(2 * math.pi * p), 0, -3], d)},
        'left_arm': {'rotation': cyc(lambda p: [-14 * math.cos(2 * math.pi * p), 0, 3], d)},
        'right_forearm': {'rotation': cyc(lambda p: [-6 + 4 * math.cos(2 * math.pi * p + 0.8), 0, 0], d)},
        'left_forearm': {'rotation': cyc(lambda p: [-6 - 4 * math.cos(2 * math.pi * p + 0.8), 0, 0], d)},
        'waistcloth_front': {'rotation': cyc(lambda p: [4 * math.sin(2 * math.pi * p + 1.2), 0, 0], d)},
        'waistcloth_left': {'rotation': cyc(lambda p: [1.5 * math.sin(2 * math.pi * p + 1.2), 0, 3 * math.sin(2 * math.pi * p + 1.2)], d)},
        'waistcloth_right': {'rotation': cyc(lambda p: [1.5 * math.sin(2 * math.pi * p + 1.2), 0, -3 * math.sin(2 * math.pi * p + 1.2)], d)},
        'waistcloth_back_left': {'rotation': cyc(lambda p: [-3 * math.sin(2 * math.pi * p + 1.2), 0, 0], d)},
        'waistcloth_back_right': {'rotation': cyc(lambda p: [-3 * math.sin(2 * math.pi * p + 1.2), 0, 0], d)},
        'mane_head': {'rotation': cyc(lambda p: [-8 + 1.5 * math.sin(2 * math.pi * p + 1.0), 0, 0], d)},
        **tail_sway(5.0, lambda i, amp: {'rotation': cyc(
            lambda p, i=i, amp=amp: [2 * math.sin(2 * math.pi * p + 0.9 - 0.35 * i),
                                     amp * math.sin(2 * math.pi * p + 0.3 - 0.4 * i) * (1.0 - 0.08 * i), 0], d)}),
    })

    # ----- awaken: coiled under the seal, then ERUPTION upward (arms stay in the box) -----
    an['awaken'] = build_anim('awaken', 2.0, loop=False, bones={
        'root': {'position': track([(0, [0, 0, 0]), (0.65, [0, -1.6, 0]), (1.3, [0, -1.8, 0]),
                                    (1.5, [0, -0.2, 0]), (1.7, [0, 0.35, 0]), (2.0, [0, 0, 0])]),
                'rotation': track([(0, [0, 0, 0]), (1.3, [-4, 0, 0]), (1.5, [3, 0, 0]), (2.0, [0, 0, 0])])},
        'left_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (1.3, [14, 0, 0]), (1.6, [-16, 0, 0]), (2.0, [B_UL, 0, 0])])},
        'right_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (1.3, [14, 0, 0]), (1.6, [-16, 0, 0]), (2.0, [B_UL, 0, 0])])},
        'left_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (1.3, [52, 0, 0]), (1.6, [B_LL + 4, 0, 0]), (2.0, [B_LL, 0, 0])])},
        'right_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (1.3, [52, 0, 0]), (1.6, [B_LL + 4, 0, 0]), (2.0, [B_LL, 0, 0])])},
        'left_hock': {'rotation': track([(0, [B_HK, 0, 0]), (1.3, [-56, 0, 0]), (1.6, [B_HK - 6, 0, 0]), (2.0, [B_HK, 0, 0])])},
        'right_hock': {'rotation': track([(0, [B_HK, 0, 0]), (1.3, [-56, 0, 0]), (1.6, [B_HK - 6, 0, 0]), (2.0, [B_HK, 0, 0])])},
        'left_hoof': {'rotation': track([(0, [B_HF, 0, 0]), (1.3, [12, 0, 0]), (2.0, [B_HF, 0, 0])])},
        'right_hoof': {'rotation': track([(0, [B_HF, 0, 0]), (1.3, [12, 0, 0]), (2.0, [B_HF, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (1.3, [5, 0, 0]), (1.55, [-8, 0, 0]), (2.0, [0, 0, 0])])},
        'chest': {'scale': track([(0, [1, 1, 1]), (1.3, [0.97, 0.97, 0.97]), (1.55, [1.06, 1.06, 1.06]), (2.0, [1.015, 1.015, 1.015])])},
        'neck': {'rotation': track([(0, [0, 0, 0]), (1.3, [7, 0, 0]), (1.6, [-8, 0, 0]), (2.0, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (1.3, [-14, 0, 0]), (1.6, [18, 0, 0]), (2.0, [2, 0, 0])])},
        'jaw': {'rotation': track([(0, [0, 0, 0]), (1.4, [0, 0, 0]), (1.6, [-32, 0, 0]), (1.9, [-10, 0, 0]), (2.0, [-8, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (1.3, [16, 0, 7]), (1.55, [-150, 0, 10]), (1.75, [-158, 0, 12]), (2.0, [-8, 0, 26])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (1.3, [16, 0, -7]), (1.55, [-150, 0, -10]), (1.75, [-158, 0, -12]), (2.0, [-8, 0, -26])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (1.3, [-38, 0, 0]), (1.55, [-10, 0, 0]), (2.0, [-8, 0, 0])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (1.3, [-38, 0, 0]), (1.55, [-10, 0, 0]), (2.0, [-8, 0, 0])])},
        'left_hand': {'rotation': track([(0, [0, 0, 0]), (1.55, [-14, 0, 0]), (2.0, [-6, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (1.55, [-14, 0, 0]), (2.0, [-6, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (1.3, [10, 0, 0]), (1.55, [-16 - 2 * i, 0, 0]), (1.8, [6 - i, 0, 0]), (2.0, [0, 0, 0])])}),
    })

    # ----- melee: single right claw slash (damage tick 9 = 0.45s) -----
    an['melee'] = build_anim('melee', 0.9, loop=False, bones={
        'pelvis': {'rotation': track([(0, [0, 0, 0]), (0.25, [-2, 5, 0]), (0.45, [-3, -6, 0]), (0.65, [-2, -7, 0]), (0.9, [0, 0, 0])]),
                   'position': track([(0, [0, 0, 0]), (0.25, [0, -0.4, 0]), (0.45, [0, -0.2, 0]), (0.9, [0, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.25, [4, 12, 0]), (0.45, [-7, -18, 0]), (0.65, [-4, -14, 0]), (0.9, [0, 0, 0])])},
        'chest': {'rotation': track([(0, [0, 0, 0]), (0.25, [2, 6, 0]), (0.45, [-4, -8, 0]), (0.9, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.25, [-2, -6, 0]), (0.45, [3, 8, 0]), (0.9, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.25, [52, 0, -16]), (0.45, [-88, 0, -20]), (0.65, [-108, 0, -14]), (0.9, [0, 0, -3])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.25, [26, 0, 0]), (0.45, [-22, 0, 0]), (0.65, [-10, 0, 0]), (0.9, [-6, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (0.25, [12, 0, 0]), (0.45, [-14, 0, 0]), (0.9, [0, 0, 0])])},
        'right_claws': {'rotation': track([(0, [0, 0, 0]), (0.25, [16, 0, 0]), (0.45, [-8, 0, 0]), (0.9, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.25, [14, 0, 8]), (0.45, [26, 0, 12]), (0.9, [0, 0, 3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.45, [-16, 0, 0]), (0.9, [-6, 0, 0])])},
        'waistcloth_front': {'rotation': track([(0, [0, 0, 0]), (0.25, [-4, 0, 0]), (0.45, [5, 0, 0]), (0.9, [0, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.25, [2, 6, 0]), (0.5, [-3, -8, 0]), (0.9, [0, 0, 0])])}),
    })

    # ----- toss: seize and hurl (impact tick 16 = 0.8s) -----
    an['toss'] = build_anim('toss', 1.5, loop=False, bones={
        'pelvis': {'position': track([(0, [0, 0, 0]), (0.45, [0, -1.2, 0]), (0.8, [0, 0.3, 0]), (0.95, [0, -0.2, 0]), (1.5, [0, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.45, [-16, 0, 0]), (0.8, [8, 0, 0]), (0.95, [-6, 0, 0]), (1.5, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.45, [-8, 0, 0]), (0.8, [10, 0, 0]), (1.5, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.45, [-58, 0, 14]), (0.8, [-138, 0, 22]), (0.95, [-64, 0, 16]), (1.5, [0, 0, 3])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.45, [-58, 0, -14]), (0.8, [-138, 0, -22]), (0.95, [-64, 0, -16]), (1.5, [0, 0, -3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.45, [-36, 0, 0]), (0.8, [-18, 0, 0]), (0.95, [-26, 0, 0]), (1.5, [-6, 0, 0])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.45, [-36, 0, 0]), (0.8, [-18, 0, 0]), (0.95, [-26, 0, 0]), (1.5, [-6, 0, 0])])},
        'left_hand': {'rotation': track([(0, [0, 0, 0]), (0.45, [-14, 0, 0]), (0.8, [-8, 0, 0]), (1.5, [0, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (0.45, [-14, 0, 0]), (0.8, [-8, 0, 0]), (1.5, [0, 0, 0])])},
        'left_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.45, [-26, 0, 8]), (0.8, [-14, 0, 10]), (1.5, [B_UL, 0, 0])])},
        'right_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.45, [4, 0, -8]), (0.8, [-4, 0, -10]), (1.5, [B_UL, 0, 0])])},
        'left_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.45, [40, 0, 0]), (1.5, [B_LL, 0, 0])])},
        'right_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.45, [46, 0, 0]), (1.5, [B_LL, 0, 0])])},
        'left_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.45, [-40, 0, 0]), (1.5, [B_HK, 0, 0])])},
        'right_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.45, [-46, 0, 0]), (1.5, [B_HK, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.45, [8, 0, 0]), (0.8, [-10, 0, 0]), (1.2, [2, 0, 0]), (1.5, [0, 0, 0])])}),
    })

    # ----- fireball: gather at the palm, release at 1.0s (tick 20) -----
    an['fireball'] = build_anim('fireball', 1.7, loop=False, bones={
        'body': {'rotation': track([(0, [0, 0, 0]), (0.55, [-4, -6, 0]), (1.0, [-3, -4, 0]), (1.7, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.55, [-3, 8, 0]), (1.0, [-1, 6, 0]), (1.7, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.55, [-55, 0, -16]), (0.85, [-52, 0, -15]),
                                         (0.95, [-54, 0, -16]), (1.0, [-50, 0, -14]), (1.15, [-44, 0, -10]), (1.7, [0, 0, -3])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.55, [-95, 0, 0]), (0.85, [-93, 0, 0]),
                                             (0.95, [-97, 0, 0]), (1.0, [-90, 0, 0]), (1.7, [-6, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (0.55, [-20, 0, 0]), (0.85, [-17, 0, 0]),
                                          (0.95, [-21, 0, 0]), (1.0, [-12, 0, 0]), (1.7, [0, 0, 0])])},
        'right_claws': {'rotation': track([(0, [0, 0, 0]), (0.55, [22, 0, 0]), (1.0, [-6, 0, 0]), (1.7, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.55, [8, 0, 6]), (1.0, [6, 0, 5]), (1.7, [0, 0, 3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.55, [-18, 0, 0]), (1.7, [-6, 0, 0])])},
        'chest': {'scale': track([(0, [1, 1, 1]), (0.85, [1.025, 1.025, 1.025]), (1.0, [1.01, 1.01, 1.01]), (1.7, [1, 1, 1])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.85, [3 - i * 0.5, 0, 0]), (1.0, [-4 + i * 0.5, 0, 0]), (1.7, [0, 0, 0])])}),
    })

    # ----- aura: three pulse-presses on wave ticks 24/30/36 -----
    an['aura'] = build_anim('aura', 2.6, loop=False, bones={
        'pelvis': {'position': track([(0, [0, 0, 0]), (0.7, [0, -0.5, 0]), (1.2, [0, -0.9, 0]),
                                      (1.35, [0, -0.6, 0]), (1.5, [0, -0.9, 0]), (1.65, [0, -0.6, 0]),
                                      (1.8, [0, -0.9, 0]), (2.6, [0, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.7, [-5, 0, 0]), (1.2, [-8, 0, 0]),
                                    (1.5, [-8, 0, 0]), (1.8, [-8, 0, 0]), (2.6, [0, 0, 0])])},
        'chest': {'scale': track([(0, [1, 1, 1]), (0.7, [1.05, 1.05, 1.05]), (1.2, [1.02, 1.02, 1.02]),
                                  (1.35, [1.05, 1.05, 1.05]), (1.5, [1.02, 1.02, 1.02]),
                                  (1.65, [1.05, 1.05, 1.05]), (1.8, [1.02, 1.02, 1.02]), (2.6, [1, 1, 1])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.7, [6, 0, 0]), (1.2, [8, 0, 0]), (1.8, [8, 0, 0]), (2.6, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.7, [-24, 0, 76]), (1.2, [-18, 0, 64]),
                                        (1.5, [-20, 0, 66]), (1.8, [-18, 0, 64]), (2.6, [0, 0, 3])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.7, [-24, 0, -76]), (1.2, [-18, 0, -64]),
                                         (1.5, [-20, 0, -66]), (1.8, [-18, 0, -64]), (2.6, [0, 0, -3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.7, [-20, 0, 0]), (2.6, [-6, 0, 0])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.7, [-20, 0, 0]), (2.6, [-6, 0, 0])])},
        'left_hand': {'rotation': track([(0, [0, 0, 0]), (0.7, [-22, 0, 0]), (2.6, [0, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (0.7, [-22, 0, 0]), (2.6, [0, 0, 0])])},
        'left_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.7, [-8, 0, 14]), (2.6, [B_UL, 0, 0])])},
        'right_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.7, [-8, 0, -14]), (2.6, [B_UL, 0, 0])])},
        'left_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.7, [B_LL - 6, 0, 0]), (2.6, [B_LL, 0, 0])])},
        'right_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.7, [B_LL - 6, 0, 0]), (2.6, [B_LL, 0, 0])])},
        'left_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.7, [B_HK - 6, 0, 0]), (2.6, [B_HK, 0, 0])])},
        'right_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.7, [B_HK - 6, 0, 0]), (2.6, [B_HK, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.7, [10, 0, 0]), (1.2, [6, 0, 0]), (1.8, [6, 0, 0]), (2.6, [0, 0, 0])])}),
    })

    # ----- trident: wind-up, aim, release at 0.85s (tick 17) -----
    an['trident'] = build_anim('trident', 1.8, loop=False, bones={
        'pelvis': {'rotation': track([(0, [0, 0, 0]), (0.4, [-2, 7, 0]), (0.85, [-3, -8, 0]), (1.1, [-2, -9, 0]), (1.8, [0, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.4, [3, 9, 0]), (0.85, [-6, -10, 0]), (1.1, [-3, -11, 0]), (1.8, [0, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.4, [-3, -5, 0]), (0.85, [2, 6, 0]), (1.8, [0, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.4, [58, 0, -14]), (0.85, [-92, 0, -18]),
                                         (1.1, [-114, 0, -12]), (1.8, [0, 0, -3])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.4, [-118, 0, 0]), (0.85, [-28, 0, 0]),
                                             (1.1, [-16, 0, 0]), (1.8, [-6, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (0.4, [-14, 0, 0]), (0.85, [8, 0, 0]), (1.8, [0, 0, 0])])},
        'weapon_anchor': {'rotation': track([(0, [0, 0, 0]), (0.4, [-34, 0, 0]), (0.85, [26, 0, 0]), (1.8, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.4, [18, 0, 10]), (0.85, [-30, 0, 22]), (1.8, [0, 0, 3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.4, [-24, 0, 0]), (0.85, [-34, 0, 0]), (1.8, [-6, 0, 0])])},
        'left_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.4, [-18, 0, 6]), (0.85, [-24, 0, 8]), (1.8, [B_UL, 0, 0])])},
        'right_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.4, [8, 0, -6]), (0.85, [12, 0, -8]), (1.8, [B_UL, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.4, [4, 7, 0]), (0.85, [-4, -9, 0]), (1.8, [0, 0, 0])])}),
    })

    # ----- summon: call the slime spawn at 1.2s (tick 24) -----
    an['summon'] = build_anim('summon', 2.2, loop=False, bones={
        'pelvis': {'position': track([(0, [0, 0, 0]), (0.7, [0, -0.6, 0]), (1.2, [0, -0.3, 0]), (2.2, [0, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.7, [-7, 0, 0]), (1.2, [-4, 0, 0]), (2.2, [0, 0, 0])])},
        'chest': {'scale': track([(0, [1, 1, 1]), (0.9, [1.045, 1.045, 1.045]), (1.2, [1.02, 1.02, 1.02]), (2.2, [1, 1, 1])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.7, [12, 0, 0]), (1.2, [6, 0, 0]), (2.2, [0, 0, 0])])},
        'jaw': {'rotation': track([(0, [0, 0, 0]), (0.7, [0, 0, 0]), (1.0, [-35, 0, 0]), (1.2, [-28, 0, 0]), (1.5, [-4, 0, 0]), (2.2, [0, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.7, [-22, 0, 82]), (1.2, [-46, 0, 58]), (1.5, [-20, 0, 30]), (2.2, [0, 0, 3])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.7, [-22, 0, -82]), (1.2, [-46, 0, -58]), (1.5, [-20, 0, -30]), (2.2, [0, 0, -3])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.7, [-16, 0, 0]), (1.2, [-30, 0, 0]), (2.2, [-6, 0, 0])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.7, [-16, 0, 0]), (1.2, [-30, 0, 0]), (2.2, [-6, 0, 0])])},
        'left_hand': {'rotation': track([(0, [0, 0, 0]), (1.0, [-16, 0, 0]), (1.2, [12, 0, 0]), (2.2, [0, 0, 0])])},
        'right_hand': {'rotation': track([(0, [0, 0, 0]), (1.0, [-16, 0, 0]), (1.2, [12, 0, 0]), (2.2, [0, 0, 0])])},
        'left_claws': {'rotation': track([(0, [0, 0, 0]), (1.0, [18, 0, 0]), (1.2, [-14, 0, 0]), (2.2, [0, 0, 0])])},
        'right_claws': {'rotation': track([(0, [0, 0, 0]), (1.0, [18, 0, 0]), (1.2, [-14, 0, 0]), (2.2, [0, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.7, [12, 0, 0]), (1.2, [8, 0, 0]), (2.2, [0, 0, 0])])}),
    })

    # ----- death: stagger, kneel, collapse; stable final pose -----
    an['death'] = build_anim('death', 2.5, loop=False, bones={
        'root': {'position': track([(0, [0, 0, 0]), (0.9, [0, -1.2, 0]), (1.5, [0, -2.4, 0]), (2.1, [0, -2.8, 0]), (2.3, [0, -2.6, 0]), (2.5, [0, -2.7, 0])]),
                'rotation': track([(0, [0, 0, 0]), (0.4, [3, 0, 0]), (0.9, [2, 0, 5]), (2.5, [2, 0, 5])])},
        'pelvis': {'rotation': track([(0, [0, 0, 0]), (0.9, [6, 0, 0]), (1.5, [10, 0, 0]), (2.5, [10, 0, 0])])},
        'body': {'rotation': track([(0, [0, 0, 0]), (0.4, [8, 0, 0]), (0.9, [-12, 0, 0]), (1.5, [-26, 0, 0]), (2.1, [-32, 0, 0]), (2.5, [-30, 0, 0])])},
        'chest': {'rotation': track([(0, [0, 0, 0]), (1.5, [-8, 0, 0]), (2.5, [-6, 0, 0])])},
        'neck': {'rotation': track([(0, [0, 0, 0]), (0.4, [10, 0, 0]), (1.5, [6, 0, 0]), (2.5, [4, 0, 0])])},
        'head': {'rotation': track([(0, [0, 0, 0]), (0.4, [16, 0, 0]), (1.2, [-18, 0, 0]), (1.9, [-30, 0, 0]), (2.5, [-28, 0, 0])])},
        'jaw': {'rotation': track([(0, [0, 0, 0]), (0.4, [-10, 0, 0]), (1.0, [-14, 0, 0]), (1.6, [-6, 0, 0]), (2.5, [-8, 0, 0])])},
        'left_arm': {'rotation': track([(0, [0, 0, 3]), (0.4, [12, 0, 10]), (0.9, [-68, 0, 18]), (1.5, [-74, 0, 20]), (2.5, [-70, 0, 18])])},
        'left_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.9, [-18, 0, 0]), (2.5, [-22, 0, 0])])},
        'right_arm': {'rotation': track([(0, [0, 0, -3]), (0.4, [-16, 0, -24]), (0.9, [30, 0, -38]), (2.5, [26, 0, -34])])},
        'right_forearm': {'rotation': track([(0, [-6, 0, 0]), (0.9, [-8, 0, 0]), (2.5, [-10, 0, 0])])},
        'left_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.9, [-4, 0, 4]), (1.5, [-6, 0, 4]), (2.5, [-6, 0, 4])])},
        'left_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.9, [30, 0, 0]), (2.5, [30, 0, 0])])},
        'left_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.9, [-34, 0, 0]), (2.5, [-34, 0, 0])])},
        'left_hoof': {'rotation': track([(0, [B_HF, 0, 0]), (0.9, [B_HF, 0, 0]), (2.5, [B_HF, 0, 0])])},
        'right_upper_leg': {'rotation': track([(0, [B_UL, 0, 0]), (0.9, [34, 0, -6]), (1.5, [40, 0, -6]), (2.5, [38, 0, -6])])},
        'right_lower_leg': {'rotation': track([(0, [B_LL, 0, 0]), (0.9, [56, 0, 0]), (2.5, [58, 0, 0])])},
        'right_hock': {'rotation': track([(0, [B_HK, 0, 0]), (0.9, [-62, 0, 0]), (2.5, [-64, 0, 0])])},
        'right_hoof': {'rotation': track([(0, [B_HF, 0, 0]), (0.9, [18, 0, 0]), (2.5, [16, 0, 0])])},
        'mane_head': {'rotation': track([(0, [-8, 0, 0]), (1.5, [-2, 0, 0]), (2.5, [-3, 0, 0])])},
        **tail_sway(0, lambda i, amp: {'rotation': track([
            (0, [0, 0, 0]), (0.5, [-4, 0, 0]), (1.2, [10 + 2 * i, 0, 0]), (1.9, [16 + 2 * i, 0, 0]), (2.5, [14 + 2 * i, 0, 0])])}),
    })

    return an


def main():
    m = build_devil()
    m.save(os.path.join(A, 'geo/fire/demon.geo.json'),
           os.path.join(A, 'textures/fire/entity/demon.png'),
           os.path.join(A, 'textures/fire/entity/demon_emissive.png'))
    save_anims(os.path.join(A, 'animations/fire/demon.animation.json'), devil_anims())


def save_anims(path, animations):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump({'format_version': '1.8.0', 'animations': animations}, f, indent=1)
    print(f'saved {os.path.basename(path)} ({len(animations)} animations)')


if __name__ == '__main__':
    main()
