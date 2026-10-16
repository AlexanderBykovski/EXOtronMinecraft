#!/usr/bin/env python3
"""Aerie Bronze rework (roman officer set, items aerie_bronze_*): bronze helmet
with dark-red transverse crest, anatomical cuirass, layered shoulder straps,
leather pteruges, vambraces, greaves and caligae. NEW custom render pipeline.
Emits AerieBronzeHelmetModel + AerieBronzePlateModel + base atlases (no glow).
Run from repo root: python3 scripts/gen_armor_rework/gen_aerie_bronze.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (A, java_path, CubeSet, metal, leather, cloth, lacquer, mixc, h01)

PAL = {
    'bronze':    (138, 106, 58), 'bronze_hi': (201, 168, 92), 'bronze_dk': (92, 69, 36),
    'bronze_dp': (64, 47, 24),
    'patina':    (78, 122, 94), 'patina_dk': (58, 90, 72),
    'tunic':     (122, 30, 30), 'tunic_hi': (148, 42, 38), 'tunic_dk': (92, 20, 20),
    'leather':   (74, 51, 32), 'leather_hi': (94, 66, 42), 'leather_dk': (52, 35, 22),
    'dark':      (30, 24, 18),
}

bronze = lambda s=7: metal(PAL['bronze'], PAL['bronze_hi'], PAL['bronze_dk'], s, 0.05)
brz_border = lambda s=9: lacquer(PAL['bronze'], PAL['bronze_hi'], PAL['bronze_dk'], PAL['bronze_dp'], s)
tunic = lambda s=3: cloth(PAL['tunic'], PAL['tunic_dk'], PAL['tunic_hi'], s, 4)
leath = lambda s=5: leather(PAL['leather'], PAL['leather_hi'], PAL['leather_dk'], s)

def patina(base_seed):
    """Bronze with patina in recesses/edges."""
    inner = bronze(base_seed)
    def p(x, y, w, h, face, name):
        c = inner(x, y, w, h, face, name)
        if y == h - 1 or x == 0 or x == w - 1:
            if h01(x, y, base_seed + 40) > 0.45:
                c = mixc(c, PAL['patina'], 0.5)
        if h01(x, y, base_seed + 41) > 0.96:
            c = mixc(c, PAL['patina_dk'], 0.6)
        return c
    return p

def crest_hair(seed=15):
    """Dense dark-red horsehair pixel blocks."""
    def p(x, y, w, h, face, name):
        n = h01(x, y, seed)
        c = PAL['tunic']
        if n > 0.72:
            c = PAL['tunic_hi']
        elif n < 0.25:
            c = PAL['tunic_dk']
        if (x + y) % 5 == 0:
            c = PAL['tunic_dk']
        return c
    return p


def build_helmet():
    cs = CubeSet()
    cs.bone('head')
    cs.add('head', 'ab_bowl', (-4.55, -8.8, -4.55), (9.1, 5.6, 9.1), patina(1), 0.55)
    cs.add('head', 'ab_bowl_ridge', (-0.85, -9.5, -4.3), (1.7, 0.9, 8.6), bronze(3), 0.55)
    cs.add('head', 'ab_brow', (-4.65, -6.1, -5.4), (9.3, 1.35, 1.25), brz_border(5), 0.05)
    cs.add('head', 'ab_cheek_l', (3.9, -5.8, -4.5), (1.45, 4.9, 3.7), bronze(7), 0.05)
    cs.add('head', 'ab_cheek_r', (-5.35, -5.8, -4.5), (1.45, 4.9, 3.7), bronze(9), 0.05)
    cs.add('head', 'ab_neck', (-4.2, -4.4, 3.8), (8.4, 4.7, 1.3), patina(11), 0.05)
    cs.add('head', 'ab_crest_base', (-4.7, -10.1, -1.0), (9.4, 0.9, 2.0), brz_border(13), 0.05)
    cs.add('head', 'ab_crest_support', (-1.0, -10.1, -1.55), (2.0, 3.6, 0.55), bronze(15), 0.05)
    cs.add('head', 'ab_crest_lo', (-4.4, -12.9, -0.8), (8.8, 2.9, 1.6), crest_hair(17), 0.05)
    cs.add('head', 'ab_crest_hi', (-3.5, -14.3, -0.65), (7.0, 1.5, 1.3), crest_hair(19), 0.05)
    cs.pack()
    cs.emit_java('com.opus.paradise.client.model', 'AerieBronzeHelmetModel', 'aerie_bronze_helmet',
                 java_path('com.opus.paradise.client.model', 'AerieBronzeHelmetModel'),
                 ['Aerie Bronze helm: rounded segmented bronze bowl with brow band,',
                  'short cheek guards, rear neck plate, rivets and a restrained dark-red',
                  'transverse crest on a narrow bronze base. Fully non-emissive.'])
    img, _ = cs.paint_atlas(PAL)
    out = os.path.join(A, '../..', 'src/main/resources/assets/minecraft/textures/models/armor')
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(A, 'textures/paradise/armor/aerie_bronze_helmet.png'))
    print('bronze helmet atlas saved')


def build_plate():
    cs = CubeSet()
    for b in ('body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)
    for tag, dx, dz in (('front', 0, -2.75), ('back', 0, 2.75), ('left', 4.8, 0), ('right', -4.8, 0)):
        cs.bone(f'body/pteruges_{tag}', f'PartPose.offsetAndRotation({dx}F, 11.9F, {dz}F, 0F, 0F, 0F)')

    # torso: red tunic under leather backing under anatomical bronze cuirass
    cs.add('body', 'ab_tunic_up', (-4.1, 0.5, -2.6), (8.2, 2.6, 5.2), tunic(1), 0.1)
    cs.add('body', 'ab_backing', (-4.2, 2.6, -2.75), (8.4, 7.8, 5.5), leath(3), 0.1)
    cs.add('body', 'ab_cuirass', (-4.5, 1.4, -3.05), (9.0, 8.4, 6.1), patina(5), 0.15)
    cs.add('body', 'ab_muscle_l', (-3.9, 2.4, -3.4), (3.4, 2.6, 0.6), bronze(7), 0.05)
    cs.add('body', 'ab_muscle_r', (0.5, 2.4, -3.4), (3.4, 2.6, 0.6), bronze(9), 0.05)
    cs.add('body', 'ab_sternum', (-0.45, 2.2, -3.45), (0.9, 6.2, 0.55), brz_border(11), 0.0)
    cs.add('body', 'ab_abs_1', (-2.6, 7.3, -3.3), (5.2, 1.0, 0.5), bronze(13), 0.0)
    cs.add('body', 'ab_abs_2', (-2.5, 8.6, -3.25), (5.0, 0.9, 0.5), brz_border(15), 0.0)
    cs.add('body', 'ab_fast_l', (4.35, 4.6, -1.6), (0.6, 2.6, 3.2), bronze(17), 0.0)
    cs.add('body', 'ab_fast_r', (-4.95, 4.6, -1.6), (0.6, 2.6, 3.2), bronze(19), 0.0)
    cs.add('body', 'ab_belt', (-4.6, 9.8, -2.9), (9.2, 2.0, 5.8), leath(21), 0.1)
    cs.add('body', 'ab_buckle', (-1.0, 9.95, -3.35), (2.0, 1.7, 0.6), brz_border(23), 0.0)
    # layered shoulder straps (3 overlapping sections over the shoulder)
    cs.add('shoulder_left', 'ab_strap_l1', (2.9, -2.5, -2.4), (1.6, 1.3, 2.1), bronze(25), 0.05)
    cs.add('shoulder_left', 'ab_strap_l2', (2.8, -1.4, -0.5), (1.7, 1.3, 2.1), brz_border(27), 0.05)
    cs.add('shoulder_left', 'ab_strap_l3', (2.7, -0.4, 1.4), (1.8, 1.3, 2.1), bronze(29), 0.05)
    cs.add('shoulder_right', 'ab_strap_r1', (-4.5, -2.5, -2.4), (1.6, 1.3, 2.1), bronze(31), 0.05)
    cs.add('shoulder_right', 'ab_strap_r2', (-4.5, -1.4, -0.5), (1.7, 1.3, 2.1), brz_border(33), 0.05)
    cs.add('shoulder_right', 'ab_strap_r3', (-4.5, -0.4, 1.4), (1.8, 1.3, 2.1), bronze(35), 0.05)
    # pteruges: two leather slabs per side with bronze tip texture
    cs.add('body/pteruges_front', 'ab_pteru_f', (-3.4, 0.0, -0.3), (3.4, 3.8, 0.6), tunic(37), 0.0)
    cs.add('body/pteruges_front', 'ab_pteru_f2', (0.1, 0.0, -0.3), (3.3, 3.8, 0.6), tunic(39), 0.0)
    cs.add('body/pteruges_back', 'ab_pteru_b', (-3.4, 0.0, -0.3), (3.4, 3.6, 0.6), tunic(41), 0.0)
    cs.add('body/pteruges_back', 'ab_pteru_b2', (0.1, 0.0, -0.3), (3.3, 3.6, 0.6), tunic(43), 0.0)
    cs.add('body/pteruges_left', 'ab_pteru_l', (-0.3, 0.0, -2.55), (0.6, 3.6, 5.1), tunic(45), 0.0)
    cs.add('body/pteruges_right', 'ab_pteru_r', (-0.3, 0.0, -2.55), (0.6, 3.6, 5.1), tunic(47), 0.0)
    cs.add('body', 'ab_skirt', (-3.9, 11.5, -2.4), (7.8, 2.4, 4.8), tunic(49), 0.05)

    # arms: red sleeve under bronze vambrace with raised borders
    cs.add('right_arm', 'ab_sleeve_r', (-3.4, 0.9, -2.3), (4.8, 3.2, 4.6), tunic(51), 0.05)
    cs.add('right_arm', 'ab_vambrace_r', (-3.5, 4.0, -2.4), (5.0, 5.8, 4.8), patina(53), 0.05)
    cs.add('left_arm', 'ab_sleeve_l', (-1.4, 0.9, -2.3), (4.8, 3.2, 4.6), tunic(55), 0.05)
    cs.add('left_arm', 'ab_vambrace_l', (-1.5, 4.0, -2.4), (5.0, 5.8, 4.8), patina(57), 0.05)

    # legs: dark inner legs, bronze greaves with straps, caligae
    cs.add('right_leg', 'ab_inner_r', (-2.2, 0.3, -2.2), (4.4, 11.0, 4.4), leath(59), 0.05)
    cs.add('right_leg', 'ab_greave_r', (-2.0, 5.6, -2.8), (4.0, 6.4, 1.05), patina(61), 0.05)
    cs.add('right_leg', 'ab_sole_r', (-2.4, 11.85, -2.75), (4.8, 0.75, 5.6), leath(63), 0.0)
    cs.add('right_leg', 'ab_toe_r', (-1.9, 11.9, -3.5), (3.8, 0.55, 0.8), bronze(65), 0.0)
    cs.add('right_leg', 'ab_heel_r', (-1.9, 11.3, 2.35), (3.8, 1.3, 0.8), leath(67), 0.0)
    cs.add('left_leg', 'ab_inner_l', (-2.2, 0.3, -2.2), (4.4, 11.0, 4.4), leath(60), 0.05)
    cs.add('left_leg', 'ab_greave_l', (-2.0, 5.6, -2.8), (4.0, 6.4, 1.05), patina(62), 0.05)
    cs.add('left_leg', 'ab_sole_l', (-2.4, 11.85, -2.75), (4.8, 0.75, 5.6), leath(64), 0.0)
    cs.add('left_leg', 'ab_toe_l', (-1.9, 11.9, -3.5), (3.8, 0.55, 0.8), bronze(66), 0.0)
    cs.add('left_leg', 'ab_heel_l', (-1.9, 11.3, 2.35), (3.8, 1.3, 0.8), leath(68), 0.0)

    cs.pack()
    cs.emit_java('com.opus.paradise.client.model', 'AerieBronzePlateModel', 'aerie_bronze_plate',
                 java_path('com.opus.paradise.client.model', 'AerieBronzePlateModel'),
                 ['Aerie Bronze plate: red tunic under a leather backing, stylized',
                  'anatomical bronze cuirass (muscle plates, sternum line, abdominal',
                  'segments), layered shoulder straps, leather pteruges in four groups,',
                  'bronze vambraces, greaves and roman caligae with studded soles.'])
    img, _ = cs.paint_atlas(PAL)
    img.save(os.path.join(A, 'textures/paradise/armor/aerie_bronze_plate.png'))
    print('bronze plate atlas saved')


if __name__ == '__main__':
    build_helmet()
    build_plate()
