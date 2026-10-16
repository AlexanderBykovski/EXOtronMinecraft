#!/usr/bin/env python3
"""Fire Demonic armor rework: bigger segmented horns, V-overlap chest plates,
rib side plates, back+boot vents, clawed gauntlets. Emits both client models
and base+emissive atlases.
Run from repo root: python3 scripts/gen_armor_rework/gen_fire_demonic.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (A, java_path, CubeSet, metal, leather, cloth, lacquer,
                    emissive_mask, mixc, shadec)

PAL = {
    'iron':    (26, 26, 28), 'iron_hi': (51, 51, 58), 'iron_dk': (14, 14, 16),
    'char':    (20, 20, 20), 'char_hi': (34, 34, 38), 'char_dk': (12, 12, 14),
    'red':     (92, 22, 22), 'red_hi': (148, 38, 30), 'red_dk': (63, 14, 14),
    'ash':     (74, 74, 80), 'steel': (58, 62, 70), 'steel_hi': (82, 88, 98),
    'e1':      (58, 10, 10), 'e2': (110, 26, 8), 'e3': (179, 62, 8),
    'e4':      (232, 118, 20), 'e5': (255, 185, 62), 'e6': (255, 245, 200),
    'soot':    (12, 12, 13),
}

ironm = lambda s=7: metal(PAL['iron'], PAL['iron_hi'], PAL['iron_dk'], s)
redm = lambda s=9: lacquer(PAL['red'], PAL['red_hi'], PAL['red_dk'], PAL['e1'], s)
charcoal = lambda s=13: metal(PAL['char'], PAL['char_hi'], PAL['char_dk'], s, 0.04)
steel = lambda s=15: metal(PAL['steel'], PAL['steel_hi'], PAL['iron_dk'], s)
leath = lambda s=17: leather((42, 30, 22), (58, 42, 30), (28, 20, 14), s)

def emi_cracks(seed, density=0.2):
    return emissive_mask(PAL['e4'], seed, density, PAL['e6'])

def emi_visor():
    def p(x, y, w, h, face, name):
        if face != 'north':
            return None
        t = 1.0 - abs((y / max(1, h - 1)) - 0.5) * 2
        if t > 0.5:
            return PAL['e5'] if t > 0.8 else PAL['e4']
        return PAL['e2'] if t > 0.2 else None
    return p

def emi_full():
    def p(x, y, w, h, face, name):
        if face in ('north', 'south'):
            return PAL['e4'] if (x + y) % 2 == 0 else PAL['e5']
        return PAL['e3']
    return p

def visor_paint():
    def p(x, y, w, h, face, name):
        c = charcoal(21)(x, y, w, h, face, name)
        if face == 'north':
            t = 1.0 - abs((y / max(1, h - 1)) - 0.5) * 2
            if t > 0.55:
                c = PAL['e4']
            elif t > 0.3:
                c = PAL['e2']
        return c
    return p


def build_helmet():
    cs = CubeSet()
    cs.bone('head')
    # horn roots + segmented horns curving up and back (asymmetric: left thicker)
    cs.bone('head/horn_left_root', 'PartPose.offsetAndRotation(3.4F, -8.6F, -1.6F, -18F, 10F, -26F)')
    cs.bone('head/horn_left_01', 'PartPose.offsetAndRotation(-0.9F, -1.6F, -0.9F, -16F, 4F, -10F)')
    cs.bone('head/horn_left_02', 'PartPose.offsetAndRotation(-0.8F, -2.6F, -0.8F, -14F, 0F, -8F)')
    cs.bone('head/horn_left_03', 'PartPose.offsetAndRotation(-0.7F, -2.3F, -0.7F, -10F, -2F, -6F)')
    cs.bone('head/horn_left_tip', 'PartPose.offsetAndRotation(-0.5F, -2.0F, -0.6F, -8F, 0F, -8F)')
    cs.bone('head/horn_right_root', 'PartPose.offsetAndRotation(-4.0F, -8.6F, -1.6F, -18F, -10F, 26F)')
    cs.bone('head/horn_right_01', 'PartPose.offsetAndRotation(-0.8F, -1.6F, -0.9F, -16F, -4F, 10F)')
    cs.bone('head/horn_right_02', 'PartPose.offsetAndRotation(-0.8F, -2.6F, -0.8F, -14F, 0F, 8F)')
    cs.bone('head/horn_right_03', 'PartPose.offsetAndRotation(-0.6F, -2.3F, -0.7F, -10F, 2F, 6F)')
    cs.bone('head/horn_right_tip', 'PartPose.offsetAndRotation(-0.5F, -2.0F, -0.6F, -8F, 0F, 8F)')

    cs.add('head', 'helm_base', (-4.5, -8.7, -4.5), (9.0, 9.0, 9.0), ironm(1), 0.55)
    cs.add('head', 'faceplate', (-4.3, -7.1, -5.45), (8.6, 6.0, 1.2), redm(3), 0.05)
    cs.add('head', 'visor', (-2.9, -5.5, -5.8), (5.8, 1.3, 0.55), visor_paint(), 0.05,
           emissive=emi_visor())
    cs.add('head', 'visor_backing', (-3.0, -5.7, -4.85), (6.0, 1.5, 0.7),
           lambda x, y, w, h, face, name: PAL['soot'], 0.05)
    cs.add('head', 'jaw_guard', (-3.4, -2.0, -4.95), (6.8, 3.4, 1.4), ironm(5), 0.05)
    cs.add('head', 'cheek_left', (3.6, -4.9, -4.6), (1.5, 4.8, 3.3), redm(7), 0.05)
    cs.add('head', 'cheek_right', (-5.1, -4.9, -4.6), (1.5, 4.8, 3.3), redm(9), 0.05)
    cs.add('head', 'neck_guard', (-4.0, -3.5, 3.3), (8.0, 4.3, 1.5), charcoal(11), 0.05)
    cs.add('head', 'crown_ridge', (-0.7, -10.1, -5.0), (1.4, 1.8, 10.0), redm(13), 0.05)

    cs.add('head/horn_left_root', 'horn_l_root', (-1.5, -1.2, -1.5), (3.0, 2.4, 3.0), charcoal(31), 0.05, emissive=emi_cracks(61, 0.14))
    cs.add('head/horn_left_01', 'horn_l_01', (-1.2, -3.4, -1.2), (2.4, 3.6, 2.4), charcoal(33), 0.05, emissive=emi_cracks(63, 0.16))
    cs.add('head/horn_left_02', 'horn_l_02', (-1.0, -3.0, -1.0), (2.0, 3.2, 2.0), charcoal(35), 0.05, emissive=emi_cracks(65, 0.16))
    cs.add('head/horn_left_03', 'horn_l_03', (-0.8, -2.7, -0.8), (1.6, 2.9, 1.6), charcoal(37), 0.05, emissive=emi_cracks(67, 0.18))
    cs.add('head/horn_left_tip', 'horn_l_tip', (-0.6, -2.3, -0.6), (1.2, 2.5, 1.2), ironm(39), 0.05)
    cs.add('head/horn_right_root', 'horn_r_root', (-1.4, -1.2, -1.5), (2.8, 2.4, 3.0), charcoal(41), 0.05, emissive=emi_cracks(71, 0.14))
    cs.add('head/horn_right_01', 'horn_r_01', (-1.1, -3.4, -1.2), (2.2, 3.6, 2.4), charcoal(43), 0.05, emissive=emi_cracks(73, 0.16))
    cs.add('head/horn_right_02', 'horn_r_02', (-0.9, -3.0, -1.0), (1.8, 3.2, 2.0), charcoal(45), 0.05, emissive=emi_cracks(75, 0.16))
    cs.add('head/horn_right_03', 'horn_r_03', (-0.7, -2.7, -0.8), (1.4, 2.9, 1.6), charcoal(47), 0.05, emissive=emi_cracks(77, 0.18))
    cs.add('head/horn_right_tip', 'horn_r_tip', (-0.55, -2.3, -0.6), (1.1, 2.5, 1.2), ironm(49), 0.05)

    cs.pack()
    cs.emit_java('com.opus.ember.client.model', 'FireDemonicHelmetModel', 'fire_demonic_helmet',
                 java_path('com.opus.ember.client.model', 'FireDemonicHelmetModel'),
                 ['Fire Demonic helm: blackened volcanic base, red forehead plates, narrow',
                  'infernal visor (brightest center) with dark backing, jaw guard, layered',
                  'cheeks, neck guard, central ridge and two enormous segmented horns',
                  'curving upward and backward with ember cracks between segments.'])
    img, emi = cs.paint_atlas(PAL)
    out = os.path.join(A, 'textures/ember/armor')
    img.save(os.path.join(out, 'fire_demonic_helmet_layer.png'))
    emi.save(os.path.join(out, 'fire_demonic_helmet_layer_emissive.png'))
    print('demonic helmet atlas saved')


def build_plate():
    cs = CubeSet()
    for b in ('body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)

    # torso: sternum core + V-overlap plates + rib plates + back vents + belt
    cs.add('body', 'lining', (-4.1, 0.8, -2.6), (8.2, 10.4, 5.2), leath(1), 0.1)
    cs.add('body', 'chest_core', (-2.6, 3.0, -3.15), (5.2, 5.8, 1.15), ironm(3), 0.05,
           emissive=emi_cracks(51, 0.22))
    cs.add('body', 'plate_upper', (-4.4, 1.0, -2.95), (8.8, 3.4, 6.0), redm(5), 0.1)
    cs.add('body', 'plate_middle', (-4.3, 4.1, -2.9), (8.6, 3.2, 5.8), redm(7), 0.1)
    cs.add('body', 'plate_lower', (-4.2, 6.9, -2.85), (8.4, 3.6, 5.6), charcoal(9), 0.1)
    cs.add('body', 'rib_left', (3.9, 3.0, -2.45), (1.2, 5.6, 4.5), charcoal(11), 0.05, emissive=emi_cracks(53, 0.16))
    cs.add('body', 'rib_right', (-5.1, 3.0, -2.45), (1.2, 5.6, 4.5), charcoal(13), 0.05, emissive=emi_cracks(55, 0.16))
    cs.add('body', 'back_plate', (-3.6, 1.8, 2.4), (7.2, 6.6, 1.1), ironm(15), 0.05)
    cs.add('body', 'back_vent_l', (0.6, 2.6, 3.5), (1.7, 3.4, 0.7),
           lambda x, y, w, h, face, name: PAL['e2'] if face == 'south' else charcoal(17)(x, y, w, h, face, name),
           0.0, emissive=emi_full())
    cs.add('body', 'back_vent_r', (-2.3, 2.6, 3.5), (1.7, 3.4, 0.7),
           lambda x, y, w, h, face, name: PAL['e2'] if face == 'south' else charcoal(19)(x, y, w, h, face, name),
           0.0, emissive=emi_full())
    cs.add('body', 'belt', (-4.5, 10.5, -2.8), (9.0, 1.9, 5.6), leath(21), 0.1)
    cs.add('body', 'buckle', (-1.3, 10.7, -3.35), (2.6, 1.6, 0.6), steel(23), 0.0,
           emissive=emi_cracks(57, 0.3))

    # jagged pauldrons with broken-plate spikes
    cs.add('shoulder_left', 'pauldron_l', (3.0, -2.9, -2.5), (2.7, 2.9, 5.0), redm(25), 0.08)
    cs.add('shoulder_left', 'pauldron_l_lo', (3.1, 0.0, -2.3), (2.5, 1.3, 4.6), charcoal(27), 0.08)
    cs.add('shoulder_left', 'spike_l1', (3.5, -4.4, -2.2), (1.7, 1.8, 1.8), ironm(29), 0.0)
    cs.add('shoulder_left', 'spike_l2', (3.7, -4.2, 0.5), (1.5, 1.6, 1.6), ironm(31), 0.0)
    cs.add('shoulder_right', 'pauldron_r', (-5.7, -2.9, -2.5), (2.7, 2.9, 5.0), redm(33), 0.08)
    cs.add('shoulder_right', 'pauldron_r_lo', (-5.6, 0.0, -2.3), (2.5, 1.3, 4.6), charcoal(35), 0.08)
    cs.add('shoulder_right', 'spike_r1', (-5.2, -4.4, -2.2), (1.7, 1.8, 1.8), ironm(37), 0.0)
    cs.add('shoulder_right', 'spike_r2', (-5.2, -4.2, 0.5), (1.5, 1.6, 1.6), ironm(39), 0.0)

    # arms: blackened forearm plates + red secondaries + claws (<= fingers)
    cs.add('right_arm', 'gauntlet_r', (-3.5, 3.9, -2.4), (5.0, 4.4, 4.8), charcoal(41), 0.05)
    cs.add('right_arm', 'upper_r', (-3.3, 8.0, -2.2), (4.6, 2.2, 4.5), redm(43), 0.05)
    cs.add('right_arm', 'wrist_r', (-3.6, 10.1, -2.5), (5.2, 1.2, 5.0), steel(45), 0.05)
    cs.add('right_arm', 'claws_r', (-2.5, 11.2, -1.7), (3.0, 1.2, 3.3), ironm(47), 0.0)
    cs.add('left_arm', 'gauntlet_l', (-1.5, 3.9, -2.4), (5.0, 4.4, 4.8), charcoal(49), 0.05)
    cs.add('left_arm', 'upper_l', (-1.3, 8.0, -2.2), (4.6, 2.2, 4.5), redm(51), 0.05)
    cs.add('left_arm', 'wrist_l', (-1.6, 10.1, -2.5), (5.2, 1.2, 5.0), steel(53), 0.05)
    cs.add('left_arm', 'claws_l', (-0.5, 11.2, -1.7), (3.0, 1.2, 3.3), ironm(55), 0.0)

    # legs: thigh/knee/greave + heavy boot with claw toes + sole vent
    cs.add('right_leg', 'thigh_r', (-2.4, -0.5, -2.3), (4.8, 5.0, 4.6), redm(61), 0.05, emissive=emi_cracks(71, 0.14))
    cs.add('right_leg', 'knee_r', (-2.5, 4.4, -2.4), (5.0, 1.8, 4.8), charcoal(63), 0.05)
    cs.add('right_leg', 'greave_r', (-2.4, 6.1, -2.3), (4.6, 5.0, 4.5), charcoal(65), 0.05, emissive=emi_cracks(73, 0.16))
    cs.add('right_leg', 'boot_r', (-2.5, 11.0, -2.8), (5.0, 1.8, 5.6), ironm(67), 0.05)
    cs.add('right_leg', 'toe_r', (-2.2, 11.3, -3.5), (4.4, 1.2, 0.8), ironm(69), 0.0)
    cs.add('right_leg', 'vent_r', (-1.5, 12.2, -1.6), (3.0, 0.7, 3.0),
           lambda x, y, w, h, face, name: PAL['e3'] if face == 'down' else charcoal(75)(x, y, w, h, face, name),
           0.0, emissive=emi_full())
    cs.add('left_leg', 'thigh_l', (-2.4, -0.5, -2.3), (4.8, 5.0, 4.6), redm(62), 0.05, emissive=emi_cracks(72, 0.14))
    cs.add('left_leg', 'knee_l', (-2.5, 4.4, -2.4), (5.0, 1.8, 4.8), charcoal(64), 0.05)
    cs.add('left_leg', 'greave_l', (-2.4, 6.1, -2.3), (4.6, 5.0, 4.5), charcoal(66), 0.05, emissive=emi_cracks(74, 0.16))
    cs.add('left_leg', 'boot_l', (-2.5, 11.0, -2.8), (5.0, 1.8, 5.6), ironm(68), 0.05)
    cs.add('left_leg', 'toe_l', (-2.2, 11.3, -3.5), (4.4, 1.2, 0.8), ironm(70), 0.0)
    cs.add('left_leg', 'vent_l', (-1.5, 12.2, -1.6), (3.0, 0.7, 3.0),
           lambda x, y, w, h, face, name: PAL['e3'] if face == 'down' else charcoal(76)(x, y, w, h, face, name),
           0.0, emissive=emi_full())

    cs.pack()
    cs.emit_java('com.opus.ember.client.model', 'FireDemonicPlateModel', 'fire_demonic_plate',
                 java_path('com.opus.ember.client.model', 'FireDemonicPlateModel'),
                 ['Fire Demonic plate: sternum core under V-overlap chest plates, rib side',
                  'plates, jagged pauldrons with broken-plate spikes, back plate with two',
                  'fire vents, ember-buckled belt, clawed gauntlets, thigh/knee/greave legs',
                  'and heavy boots with claw toes and sole fire vents.'])
    img, emi = cs.paint_atlas(PAL)
    out = os.path.join(A, 'textures/ember/armor')
    img.save(os.path.join(out, 'fire_demonic_plate_layer.png'))
    emi.save(os.path.join(out, 'fire_demonic_plate_layer_emissive.png'))
    print('demonic plate atlas saved')


if __name__ == '__main__':
    build_helmet()
    build_plate()
