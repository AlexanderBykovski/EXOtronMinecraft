#!/usr/bin/env python3
"""Parthenon Regalia rework (angelic set, items parthenon_*): pearl-white armor,
long ivory robe with six hanging panels, pale-gold trim, floating 8-segment halo.
Emits ParthenonRegaliaModel.java + base + emissive atlases.
Run from repo root: python3 scripts/gen_armor_rework/gen_parthenon.py
"""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (A, java_path, CubeSet, metal, leather, cloth, gold_trim, mixc, shadec, h01)

PAL = {
    'ivory':    (232, 226, 212), 'ivory_hi': (244, 241, 232), 'ivory_dk': (206, 198, 182),
    'pearl':    (240, 237, 228), 'pearl_hi': (250, 248, 242), 'pearl_dk': (214, 210, 198),
    'gold':     (201, 168, 92), 'gold_hi': (228, 205, 138), 'gold_dk': (138, 109, 59),
    'stone':    (196, 192, 184), 'stone_dk': (172, 168, 160),
    'shadow':   (168, 174, 192), 'shadow_dk': (146, 152, 172),
    'inner':    (216, 212, 204), 'inner_dk': (196, 190, 180),
    'glow':     (255, 244, 214), 'glow_hi': (255, 252, 238),
}

ivory = lambda s=3: cloth(PAL['ivory'], PAL['ivory_dk'], PAL['ivory_hi'], s, 5)
pearlm = lambda s=5: metal(PAL['pearl'], PAL['pearl_hi'], PAL['pearl_dk'], s, 0.03)
stonec = lambda s=7: cloth(PAL['stone'], PAL['stone_dk'], (208, 204, 196), s, 4)
goldm = lambda s=9: gold_trim(PAL['gold'], PAL['gold_hi'], PAL['gold_dk'], s)

def gold_edge(inner, seed=11):
    """Trim: top row gold, rest material."""
    def p(x, y, w, h, face, name):
        c = inner(x, y, w, h, face, name)
        if y == 0 or y == h - 1:
            return PAL['gold'] if h01(x, y, seed) > 0.3 else PAL['gold_hi']
        return c
    return p

def emi_glow_full():
    def p(x, y, w, h, face, name):
        return PAL['glow'] if (x + y) % 3 else PAL['glow_hi']
    return p

def emi_inset():
    def p(x, y, w, h, face, name):
        if face not in ('north', 'south'):
            return None
        cx, cy = (w - 1) / 2, (h - 1) / 2
        if max(abs(x - cx), abs(y - cy)) < 0.9:
            return PAL['glow_hi']
        return PAL['glow']
    return p


def build():
    cs = CubeSet()
    for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg', 'shoulder_left', 'shoulder_right'):
        cs.bone(b)
    cs.bone('head/halo', 'PartPose.offsetAndRotation(0F, -9.6F, 1.1F, 8F, 0F, 0F)')
    for i in range(8):
        cs.bone(f'head/halo_s{i}', f'PartPose.offsetAndRotation(0F, 0F, 0F, 0F, {i * 45}F, 0F)')
    for tag, dx, dz in (('front_left', 2.15, -2.75), ('front_right', -2.15, -2.75),
                        ('side_left', 5.0, 0), ('side_right', -5.0, 0),
                        ('back_left', 2.0, 2.75), ('back_right', -2.0, 2.75)):
        cs.bone(f'body/robe_{tag}', f'PartPose.offsetAndRotation({dx}F, 10.6F, {dz}F, 0F, 0F, 0F)')

    # head: minimal gold band + pearl temple guards; face of the player stays visible
    cs.add('head', 'pt_band', (-4.2, -7.3, -4.2), (8.4, 1.7, 8.4), goldm(1), 0.45)
    cs.add('head', 'pt_temple_l', (4.0, -6.9, -2.5), (1.2, 2.8, 2.2), pearlm(3), 0.2)
    cs.add('head', 'pt_temple_r', (-5.2, -6.9, -2.5), (1.2, 2.8, 2.2), pearlm(5), 0.2)
    # halo: thin warm-gold ring, emissive edge
    for i in range(8):
        cs.add(f'head/halo_s{i}', f'pt_halo_{i}', (5.35, -0.45, -0.6), (1.5, 0.9, 1.2), goldm(13), 0.0,
               emissive=emi_glow_full())

    # body: inner garment, chest guard with V edge + inset, collar, back, clasp
    cs.add('body', 'pt_inner', (-4.0, 0.4, -2.5), (8.0, 11.0, 5.0), stonec(15), 0.1)
    cs.add('body', 'pt_chest', (-4.3, 1.0, -2.9), (8.6, 7.6, 5.7), gold_edge(pearlm(17)), 0.15)
    cs.add('body', 'pt_inset', (-1.1, 3.2, -3.2), (2.2, 2.2, 0.5),
           lambda x, y, w, h, face, name: PAL['glow'] if face in ('north', 'south') else PAL['gold_dk'],
           0.0, emissive=emi_inset())
    cs.add('body', 'pt_collar', (-3.6, 0.4, 1.5), (7.2, 2.8, 1.3), gold_edge(ivory(19)), 0.1)
    cs.add('body', 'pt_back', (-3.4, 1.2, 2.5), (6.8, 7.2, 1.0), pearlm(21), 0.1)
    cs.add('body', 'pt_clasp', (-1.2, 9.9, -3.1), (2.4, 1.6, 0.7), goldm(23), 0.0,
           emissive=emi_inset())
    # small shoulder plates
    cs.add('shoulder_left', 'pt_sh_l', (2.9, -2.6, -2.3), (2.7, 2.5, 4.7), gold_edge(pearlm(25)), 0.1)
    cs.add('shoulder_right', 'pt_sh_r', (-5.6, -2.6, -2.3), (2.7, 2.5, 4.7), gold_edge(pearlm(27)), 0.1)
    # robe panels (hang from the waist)
    cs.add('body/robe_front_left', 'pt_robe_fl', (-1.95, 0.0, -0.35), (3.9, 10.6, 0.7), gold_edge(ivory(29)), 0.05)
    cs.add('body/robe_front_right', 'pt_robe_fr', (-1.95, 0.0, -0.35), (3.9, 10.6, 0.7), gold_edge(ivory(31)), 0.05)
    cs.add('body/robe_side_left', 'pt_robe_sl', (-0.4, 0.0, -2.55), (0.8, 10.0, 5.1), ivory(33), 0.05)
    cs.add('body/robe_side_right', 'pt_robe_sr', (-0.4, 0.0, -2.55), (0.8, 10.0, 5.1), ivory(35), 0.05)
    cs.add('body/robe_back_left', 'pt_robe_bl', (-1.9, 0.0, -0.35), (3.8, 10.9, 0.7), ivory(37), 0.05)
    cs.add('body/robe_back_right', 'pt_robe_br', (-1.9, 0.0, -0.35), (3.8, 10.9, 0.7), ivory(39), 0.05)

    # arms: wide outer sleeve + narrow vambrace with gold trim
    cs.add('right_arm', 'pt_sleeve_r', (-4.0, -0.4, -2.95), (6.1, 6.6, 5.9), ivory(41), 0.1)
    cs.add('right_arm', 'pt_sleeve_r_trim', (-3.9, 5.9, -2.85), (5.9, 0.8, 5.7), goldm(43), 0.1)
    cs.add('right_arm', 'pt_vambrace_r', (-3.2, 7.0, -2.4), (4.5, 4.6, 4.7), gold_edge(pearlm(45)), 0.05)
    cs.add('left_arm', 'pt_sleeve_l', (-2.1, -0.4, -2.95), (6.1, 6.6, 5.9), ivory(47), 0.1)
    cs.add('left_arm', 'pt_sleeve_l_trim', (-2.0, 5.9, -2.85), (5.9, 0.8, 5.7), goldm(49), 0.1)
    cs.add('left_arm', 'pt_vambrace_l', (-1.3, 7.0, -2.4), (4.5, 4.6, 4.7), gold_edge(pearlm(51)), 0.05)

    # legs: fitted trousers, light knees, pearl greaves, thin-soled boots
    cs.add('right_leg', 'pt_trouser_r', (-2.1, 0.1, -2.2), (4.2, 11.2, 4.4), stonec(53), 0.05)
    cs.add('right_leg', 'pt_knee_r', (-2.3, 4.6, -2.5), (4.6, 1.6, 5.0), gold_edge(pearlm(55)), 0.05)
    cs.add('right_leg', 'pt_greave_r', (-2.3, 6.4, -2.4), (4.6, 4.8, 4.8), gold_edge(pearlm(57)), 0.05)
    cs.add('right_leg', 'pt_boot_r', (-2.4, 11.0, -2.7), (4.8, 1.6, 5.4), pearlm(59), 0.05)
    cs.add('right_leg', 'pt_sole_r', (-2.4, 12.5, -2.75), (4.8, 0.35, 5.5), stonec(61), 0.0)
    cs.add('left_leg', 'pt_trouser_l', (-2.1, 0.1, -2.2), (4.2, 11.2, 4.4), stonec(62), 0.05)
    cs.add('left_leg', 'pt_knee_l', (-2.3, 4.6, -2.5), (4.6, 1.6, 5.0), gold_edge(pearlm(63)), 0.05)
    cs.add('left_leg', 'pt_greave_l', (-2.3, 6.4, -2.4), (4.6, 4.8, 4.8), gold_edge(pearlm(64)), 0.05)
    cs.add('left_leg', 'pt_boot_l', (-2.4, 11.0, -2.7), (4.8, 1.6, 5.4), pearlm(65), 0.05)
    cs.add('left_leg', 'pt_sole_l', (-2.4, 12.5, -2.75), (4.8, 0.35, 5.5), stonec(66), 0.0)

    cs.pack()
    return cs


def emit(cs):
    out = java_path('com.opus.paradise.client.model', 'ParthenonRegaliaModel')
    L = []
    w = L.append
    w('package com.opus.paradise.client.model;')
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
    w(' * Parthenon Regalia (see scripts/gen_armor_rework/gen_parthenon.py): pearl chest')
    w(' * guard with a warm inset, high collar, small shoulder plates, wide sleeves with')
    w(' * vambraces, six long robe panels hanging from the waist, pearl greaves and an')
    w(' * eight-segment floating halo with a soft emissive edge. Face stays visible.')
    w(' */')
    w('public final class ParthenonRegaliaModel<T extends LivingEntity> extends EntityModel<T> {')
    w('    public static final ModelLayerLocation LAYER_LOCATION =')
    w('        new ModelLayerLocation(new ResourceLocation("opusvsexe", "parthenon_regalia"), "main");')
    w('')
    w('    private final ModelPart root;')
    w('    public ParthenonRegaliaModel(ModelPart root) { this.root = root; }')
    w('    public ModelPart root() { return root; }')
    w('    public ModelPart head() { return root.getChild("head"); }')
    w('    public ModelPart body() { return root.getChild("body"); }')
    w('    public ModelPart rightArm() { return root.getChild("right_arm"); }')
    w('    public ModelPart leftArm() { return root.getChild("left_arm"); }')
    w('    public ModelPart rightLeg() { return root.getChild("right_leg"); }')
    w('    public ModelPart leftLeg() { return root.getChild("left_leg"); }')
    w('    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }')
    w('    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }')
    w('    public ModelPart halo() { return root.getChild("head").getChild("halo"); }')
    w('')
    w('    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {')
    w('        head().visible = head;')
    w('        body().visible = chest;')
    w('        rightArm().visible = chest;')
    w('        leftArm().visible = chest;')
    w('        shoulderLeft().visible = chest;')
    w('        shoulderRight().visible = chest;')
    for bone, getter in (('right_leg', 'rightLeg'), ('left_leg', 'leftLeg')):
        for c in [c for c in cs.cubes if c['bone'] == bone]:
            n = c['name']
            if 'trouser' in n:
                w(f'        {getter}().getChild("{n}").visible = legs || feet;')
            elif 'knee' in n:
                w(f'        {getter}().getChild("{n}").visible = legs || feet;')
            else:
                w(f'        {getter}().getChild("{n}").visible = feet;')
    for tag in ('front_left', 'front_right', 'side_left', 'side_right', 'back_left', 'back_right'):
        w(f'        body().getChild("robe_{tag}").visible = chest || legs;')
    w('    }')
    w('')
    w('    public static LayerDefinition createLayerDefinition() {')
    w('        MeshDefinition mesh = new MeshDefinition();')
    w('        PartDefinition root = mesh.getRoot();')
    for b in ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg'):
        w(f'        PartDefinition {b} = root.addOrReplaceChild("{b}", CubeListBuilder.create(), PartPose.ZERO);')
    w('        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));')
    w('        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));')
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
    from common import cube_list_lines
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
    cs = build()
    emit(cs)
    outd = os.path.join(A, 'textures/paradise/armor')
    os.makedirs(outd, exist_ok=True)
    img, emi = cs.paint_atlas(PAL)
    img.save(os.path.join(outd, 'parthenon_regalia.png'))
    emi.save(os.path.join(outd, 'parthenon_regalia_emissive.png'))
    print('parthenon atlases saved')
