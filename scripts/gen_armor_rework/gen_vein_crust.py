#!/usr/bin/env python3
"""Vein Crust armor (items fire_*): columnar basalt + blackstone + trapped magma.
Rewrites FireHelmetModel / FirePlateModel + base/emissive atlases.
Run from repo root: python3 scripts/gen_armor_rework/gen_vein_crust.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (A, java_path, CubeSet, metal, leather, cloth, vertical_cols, rough_stone,
                    magma, emissive_mask, mixc, shadec)

PAL = {
    'basalt':     (46, 46, 54), 'basalt_hi': (66, 66, 78), 'basalt_dk': (30, 30, 37),
    'seam':       (22, 22, 28),
    'black':      (26, 22, 31), 'black_hi': (40, 35, 47), 'black_dk': (16, 14, 20),
    'iron':       (50, 52, 60), 'iron_hi': (72, 75, 85), 'iron_dk': (32, 34, 40),
    'lining':     (18, 16, 20),
    'mag_red':    (142, 27, 16), 'mag_org': (216, 67, 21), 'mag_yel': (255, 138, 60), 'mag_hot': (255, 213, 79),
}

basalt = lambda s=11: vertical_cols(PAL['basalt'], PAL['basalt_hi'], PAL['basalt_dk'], PAL['seam'], s, 4)
black = lambda s=13: rough_stone(PAL['black'], PAL['black_hi'], PAL['black_dk'], s)
ironm = lambda s=7: metal(PAL['iron'], PAL['iron_hi'], PAL['iron_dk'], s)
mag = lambda s=31: magma(PAL['basalt_dk'], PAL['mag_red'], PAL['mag_org'], PAL['mag_yel'], s, 0.24)
lining = lambda: cloth(PAL['lining'], (10, 9, 12), (26, 24, 30), 3, 3)

emi_crack = lambda s=41: emissive_mask(PAL['mag_org'], s, 0.18, PAL['mag_yel'])
emi_core = lambda: (lambda x, y, w, h, face, name:
                    (PAL['mag_hot'] if (x + y) % 2 else PAL['mag_yel'])
                    if 1 <= x < w - 1 and 1 <= y < h - 1 and (face in ('north', 'south')) else None)
emi_visor = lambda: (lambda x, y, w, h, face, name:
                     PAL['mag_red'] if (face == 'north' and 0 <= y < h) else
                     (PAL['mag_org'] if face == 'north' else None))


def build_helmet():
    cs = CubeSet()
    cs.bone('head')
    cs.add('head', 'helmet_core', (-4.6, -8.7, -4.6), (9.2, 9.2, 9.2), basalt(11), 0.55)
    cs.add('head', 'helmet_ribs_c', (-0.65, -9.5, -4.85), (1.3, 1.0, 9.7), basalt(15), 0.55)
    cs.add('head', 'helmet_ribs_l', (2.75, -9.3, -4.5), (1.1, 0.8, 9.0), basalt(17), 0.55)
    cs.add('head', 'helmet_ribs_r', (-3.85, -9.3, -4.5), (1.1, 0.8, 9.0), basalt(19), 0.55)
    cs.add('head', 'brow_band', (-4.5, -6.1, -5.45), (9.0, 1.4, 1.15), black(21), 0.05)
    cs.add('head', 'visor', (-2.9, -5.5, -5.65), (5.8, 0.95, 0.7),
           lambda x, y, w, h, face, name: (PAL['mag_red'] if (x + y) % 3 else PAL['mag_org']), 0.05,
           emissive=emi_visor())
    cs.add('head', 'visor_backing', (-3.1, -5.8, -4.8), (6.2, 1.5, 0.8), lining(), 0.05)
    cs.add('head', 'cheek_left', (3.85, -5.5, -4.4), (1.35, 4.5, 3.5), black(23), 0.05)
    cs.add('head', 'cheek_right', (-5.2, -5.5, -4.4), (1.35, 4.5, 3.5), black(25), 0.05)
    cs.add('head', 'jaw_guard', (-3.3, -1.6, -4.75), (6.6, 2.5, 1.2), black(27), 0.05)
    cs.add('head', 'neck_guard', (-4.2, -3.7, 3.6), (8.4, 4.0, 1.4), basalt(29), 0.05)
    cs.pack()
    cs.emit_java('com.opus.fire.client.model', 'FireHelmetModel', 'fire_helmet',
                 java_path('com.opus.fire.client.model', 'FireHelmetModel'),
                 ['Vein Crust helm: closed columnar-basalt bowl with vertical stone ribs,',
                  'blackstone brow frame around a narrow dark-red visor with magma pixels,',
                  'dark backing behind the visor, rectangular cheeks and thick neck guard.',
                  'No horns, no spikes. Emissive pass: visor interior only.'])
    img, emi = cs.paint_atlas(PAL)
    out = os.path.join(A, 'textures/fire/armor')
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, 'fire_helmet_layer.png'))
    emi.save(os.path.join(out, 'fire_helmet_layer_emissive.png'))
    print('helmet atlas + emissive saved')


def build_plate():
    cs = CubeSet()
    for b in ('body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)

    # torso: interlocking basalt columns + blackstone borders + magma core
    cs.add('body', 'lining', (-4.1, 1.0, -2.6), (8.2, 10.2, 5.2), lining(), 0.1)
    cs.add('body', 'border_top', (-4.6, 0.7, -3.0), (9.2, 0.8, 6.0), black(21), 0.1)
    cs.add('body', 'border_bottom', (-4.5, 9.6, -2.95), (9.0, 0.9, 5.9), black(23), 0.1)
    cs.add('body', 'sternum', (-1.15, 1.6, -3.2), (2.3, 7.8, 1.25), basalt(31), 0.1,
           emissive=emi_crack(51))
    cs.add('body', 'col_c_l', (1.25, 1.5, -3.05), (2.0, 8.0, 1.15), basalt(33), 0.1, emissive=emi_crack(53))
    cs.add('body', 'col_c_r', (-3.25, 1.5, -3.05), (2.0, 8.0, 1.15), basalt(35), 0.1, emissive=emi_crack(55))
    cs.add('body', 'col_o_l', (3.35, 1.8, -2.85), (1.35, 7.4, 1.0), basalt(37), 0.1)
    cs.add('body', 'col_o_r', (-4.7, 1.8, -2.85), (1.35, 7.4, 1.0), basalt(39), 0.1)
    cs.add('body', 'magma_core', (-0.95, 3.6, -3.4), (1.9, 2.8, 0.45),
           lambda x, y, w, h, face, name: PAL['mag_yel'] if (x + y) % 2 else PAL['mag_org'], 0.0,
           emissive=emi_core())
    cs.add('body', 'back_plate', (-4.0, 1.4, 2.55), (8.0, 8.2, 1.1), basalt(41), 0.1, emissive=emi_crack(57))
    cs.add('body', 'belt', (-4.5, 10.4, -2.85), (9.0, 1.6, 5.7), black(25), 0.1)

    # shoulders: compact layered basalt
    cs.add('shoulder_left', 'pauldron_l', (2.9, -2.8, -2.5), (2.9, 2.9, 5.0), basalt(43), 0.08)
    cs.add('shoulder_left', 'pauldron_l_lo', (3.0, 0.2, -2.3), (2.7, 1.3, 4.6), black(45), 0.08)
    cs.add('shoulder_right', 'pauldron_r', (-5.8, -2.8, -2.5), (2.9, 2.9, 5.0), basalt(47), 0.08)
    cs.add('shoulder_right', 'pauldron_r_lo', (-5.7, 0.2, -2.3), (2.7, 1.3, 4.6), black(49), 0.08)

    # arms: segmented basalt forearms, blackstone wrist, knuckle guard
    cs.add('right_arm', 'forearm_r_hi', (-3.4, 3.8, -2.35), (4.7, 3.5, 4.7), basalt(51), 0.05)
    cs.add('right_arm', 'forearm_r_lo', (-3.3, 7.1, -2.3), (4.5, 2.7, 4.6), basalt(53), 0.05)
    cs.add('right_arm', 'wrist_r', (-3.45, 9.6, -2.4), (4.8, 1.3, 4.85), black(55), 0.05)
    cs.add('right_arm', 'knuckle_r', (-3.1, 10.9, -2.2), (4.2, 1.1, 4.35), black(57), 0.05,
           emissive=emi_crack(59))
    cs.add('left_arm', 'forearm_l_hi', (-1.3, 3.8, -2.35), (4.7, 3.5, 4.7), basalt(61), 0.05)
    cs.add('left_arm', 'forearm_l_lo', (-1.2, 7.1, -2.3), (4.5, 2.7, 4.6), basalt(63), 0.05)
    cs.add('left_arm', 'wrist_l', (-1.35, 9.6, -2.4), (4.8, 1.3, 4.85), black(65), 0.05)
    cs.add('left_arm', 'knuckle_l', (-1.1, 10.9, -2.2), (4.2, 1.1, 4.35), black(67), 0.05,
           emissive=emi_crack(69))

    # legs: thigh plate, knee, greave with ribs, heavy boot + magma sole seams
    cs.add('right_leg', 'thigh_r', (-2.4, -0.5, -2.3), (4.8, 5.2, 4.6), basalt(71), 0.05, emissive=emi_crack(81))
    cs.add('right_leg', 'knee_r', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8), black(73), 0.05)
    cs.add('right_leg', 'greave_r', (-2.4, 6.1, -2.3), (4.7, 5.0, 4.6), basalt(75), 0.05, emissive=emi_crack(83))
    cs.add('right_leg', 'boot_r', (-2.5, 11.0, -2.75), (5.0, 1.7, 5.5), black(77), 0.05,
           emissive=emi_crack(85))
    cs.add('right_leg', 'sole_r', (-2.5, 12.55, -2.85), (5.0, 0.5, 5.7), mag(91), 0.0)
    cs.add('left_leg', 'thigh_l', (-2.4, -0.5, -2.3), (4.8, 5.2, 4.6), basalt(72), 0.05, emissive=emi_crack(82))
    cs.add('left_leg', 'knee_l', (-2.5, 4.5, -2.4), (5.0, 1.8, 4.8), black(74), 0.05)
    cs.add('left_leg', 'greave_l', (-2.4, 6.1, -2.3), (4.7, 5.0, 4.6), basalt(76), 0.05, emissive=emi_crack(84))
    cs.add('left_leg', 'boot_l', (-2.5, 11.0, -2.75), (5.0, 1.7, 5.5), black(78), 0.05,
           emissive=emi_crack(86))
    cs.add('left_leg', 'sole_l', (-2.5, 12.55, -2.85), (5.0, 0.5, 5.7), mag(92), 0.0)

    cs.pack()
    cs.emit_java('com.opus.fire.client.model', 'FirePlateModel', 'fire_plate',
                 java_path('com.opus.fire.client.model', 'FirePlateModel'),
                 ['Vein Crust plate: dark heat-resistant lining, interlocking vertical basalt',
                  'columns with blackstone borders, small trapped-magma sternum core, back',
                  'plate, compact layered shoulders, segmented forearms with blackstone',
                  'wrists and knuckle guards, thigh/knee plates, ribbed greaves, heavy',
                  'boots with blackstone ankle frames and magma-seamed soles.'])
    img, emi = cs.paint_atlas(PAL)
    out = os.path.join(A, 'textures/fire/armor')
    img.save(os.path.join(out, 'fire_plate.png'))
    emi.save(os.path.join(out, 'fire_plate_emissive.png'))
    print('plate atlas + emissive saved')


if __name__ == '__main__':
    build_helmet()
    build_plate()
