package com.opus.paradise.client.model;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;

/**
 * Parthenon Regalia (see scripts/gen_armor_rework/gen_parthenon.py): pearl chest
 * guard with a warm inset, high collar, small shoulder plates, wide sleeves with
 * vambraces, six long robe panels hanging from the waist, pearl greaves and an
 * eight-segment floating halo with a soft emissive edge. Face stays visible.
 */
public final class ParthenonRegaliaModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "parthenon_regalia"), "main");

    private final ModelPart root;
    public ParthenonRegaliaModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart head() { return root.getChild("head"); }
    public ModelPart body() { return root.getChild("body"); }
    public ModelPart rightArm() { return root.getChild("right_arm"); }
    public ModelPart leftArm() { return root.getChild("left_arm"); }
    public ModelPart rightLeg() { return root.getChild("right_leg"); }
    public ModelPart leftLeg() { return root.getChild("left_leg"); }
    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }
    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }
    public ModelPart halo() { return root.getChild("head").getChild("halo"); }

    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {
        head().visible = head;
        body().visible = chest;
        rightArm().visible = chest;
        leftArm().visible = chest;
        shoulderLeft().visible = chest;
        shoulderRight().visible = chest;
        rightLeg().getChild("pt_trouser_r").visible = legs || feet;
        rightLeg().getChild("pt_knee_r").visible = legs || feet;
        rightLeg().getChild("pt_greave_r").visible = feet;
        rightLeg().getChild("pt_boot_r").visible = feet;
        rightLeg().getChild("pt_sole_r").visible = feet;
        leftLeg().getChild("pt_trouser_l").visible = legs || feet;
        leftLeg().getChild("pt_knee_l").visible = legs || feet;
        leftLeg().getChild("pt_greave_l").visible = feet;
        leftLeg().getChild("pt_boot_l").visible = feet;
        leftLeg().getChild("pt_sole_l").visible = feet;
        body().getChild("robe_front_left").visible = chest || legs;
        body().getChild("robe_front_right").visible = chest || legs;
        body().getChild("robe_side_left").visible = chest || legs;
        body().getChild("robe_side_right").visible = chest || legs;
        body().getChild("robe_back_left").visible = chest || legs;
        body().getChild("robe_back_right").visible = chest || legs;
    }

    public static LayerDefinition createLayerDefinition() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_arm = root.addOrReplaceChild("right_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_arm = root.addOrReplaceChild("left_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_leg = root.addOrReplaceChild("right_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_leg = root.addOrReplaceChild("left_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));
        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));
        PartDefinition halo = head.addOrReplaceChild("halo", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, -9.6F, 1.1F, 8F, 0F, 0F));
        PartDefinition halo_s0 = head.addOrReplaceChild("halo_s0", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 0F, 0F));
        PartDefinition halo_s1 = head.addOrReplaceChild("halo_s1", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 45F, 0F));
        PartDefinition halo_s2 = head.addOrReplaceChild("halo_s2", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 90F, 0F));
        PartDefinition halo_s3 = head.addOrReplaceChild("halo_s3", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 135F, 0F));
        PartDefinition halo_s4 = head.addOrReplaceChild("halo_s4", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 180F, 0F));
        PartDefinition halo_s5 = head.addOrReplaceChild("halo_s5", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 225F, 0F));
        PartDefinition halo_s6 = head.addOrReplaceChild("halo_s6", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 270F, 0F));
        PartDefinition halo_s7 = head.addOrReplaceChild("halo_s7", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 0F, 0F, 0F, 315F, 0F));
        PartDefinition robe_front_left = body.addOrReplaceChild("robe_front_left", CubeListBuilder.create(), PartPose.offsetAndRotation(2.15F, 10.6F, -2.75F, 0F, 0F, 0F));
        PartDefinition robe_front_right = body.addOrReplaceChild("robe_front_right", CubeListBuilder.create(), PartPose.offsetAndRotation(-2.15F, 10.6F, -2.75F, 0F, 0F, 0F));
        PartDefinition robe_side_left = body.addOrReplaceChild("robe_side_left", CubeListBuilder.create(), PartPose.offsetAndRotation(5.0F, 10.6F, 0F, 0F, 0F, 0F));
        PartDefinition robe_side_right = body.addOrReplaceChild("robe_side_right", CubeListBuilder.create(), PartPose.offsetAndRotation(-5.0F, 10.6F, 0F, 0F, 0F, 0F));
        PartDefinition robe_back_left = body.addOrReplaceChild("robe_back_left", CubeListBuilder.create(), PartPose.offsetAndRotation(2.0F, 10.6F, 2.75F, 0F, 0F, 0F));
        PartDefinition robe_back_right = body.addOrReplaceChild("robe_back_right", CubeListBuilder.create(), PartPose.offsetAndRotation(-2.0F, 10.6F, 2.75F, 0F, 0F, 0F));
        head.addOrReplaceChild("pt_band", CubeListBuilder.create()
            .texOffs(82, 17).addBox(0F, 0F, 0F, 8F, 1F, 8F, new CubeDeformation(0.45f)),
            PartPose.offset(-4.2F, -7.3F, -4.2F));
        head.addOrReplaceChild("pt_temple_l", CubeListBuilder.create()
            .texOffs(13, 45).addBox(0F, 0F, 0F, 1F, 2F, 2F, new CubeDeformation(0.2f)),
            PartPose.offset(4.0F, -6.9F, -2.5F));
        head.addOrReplaceChild("pt_temple_r", CubeListBuilder.create()
            .texOffs(20, 45).addBox(0F, 0F, 0F, 1F, 2F, 2F, new CubeDeformation(0.2f)),
            PartPose.offset(-5.2F, -6.9F, -2.5F));
        halo_s0.addOrReplaceChild("pt_halo_0", CubeListBuilder.create()
            .texOffs(58, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s1.addOrReplaceChild("pt_halo_1", CubeListBuilder.create()
            .texOffs(63, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s2.addOrReplaceChild("pt_halo_2", CubeListBuilder.create()
            .texOffs(68, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s3.addOrReplaceChild("pt_halo_3", CubeListBuilder.create()
            .texOffs(73, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s4.addOrReplaceChild("pt_halo_4", CubeListBuilder.create()
            .texOffs(78, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s5.addOrReplaceChild("pt_halo_5", CubeListBuilder.create()
            .texOffs(83, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s6.addOrReplaceChild("pt_halo_6", CubeListBuilder.create()
            .texOffs(88, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        halo_s7.addOrReplaceChild("pt_halo_7", CubeListBuilder.create()
            .texOffs(93, 45).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(5.35F, -0.45F, -0.6F));
        body.addOrReplaceChild("pt_inner", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 8F, 11F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.0F, 0.4F, -2.5F));
        body.addOrReplaceChild("pt_chest", CubeListBuilder.create()
            .texOffs(87, 0).addBox(0F, 0F, 0F, 8F, 7F, 5F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.3F, 1.0F, -2.9F));
        body.addOrReplaceChild("pt_inset", CubeListBuilder.create()
            .texOffs(44, 45).addBox(0F, 0F, 0F, 2F, 2F, 1F),
            PartPose.offset(-1.1F, 3.2F, -3.2F));
        body.addOrReplaceChild("pt_collar", CubeListBuilder.create()
            .texOffs(27, 45).addBox(0F, 0F, 0F, 7F, 2F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.6F, 0.4F, 1.5F));
        body.addOrReplaceChild("pt_back", CubeListBuilder.create()
            .texOffs(68, 29).addBox(0F, 0F, 0F, 6F, 7F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.4F, 1.2F, 2.5F));
        body.addOrReplaceChild("pt_clasp", CubeListBuilder.create()
            .texOffs(51, 45).addBox(0F, 0F, 0F, 2F, 1F, 1F),
            PartPose.offset(-1.2F, 9.9F, -3.1F));
        shoulder_left.addOrReplaceChild("pt_sh_l", CubeListBuilder.create()
            .texOffs(114, 38).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(2.9F, -2.6F, -2.3F));
        shoulder_right.addOrReplaceChild("pt_sh_r", CubeListBuilder.create()
            .texOffs(0, 45).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(-5.6F, -2.6F, -2.3F));
        robe_front_left.addOrReplaceChild("pt_robe_fl", CubeListBuilder.create()
            .texOffs(46, 17).addBox(0F, 0F, 0F, 3F, 10F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.95F, 0.0F, -0.35F));
        robe_front_right.addOrReplaceChild("pt_robe_fr", CubeListBuilder.create()
            .texOffs(55, 17).addBox(0F, 0F, 0F, 3F, 10F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.95F, 0.0F, -0.35F));
        robe_side_left.addOrReplaceChild("pt_robe_sl", CubeListBuilder.create()
            .texOffs(61, 0).addBox(0F, 0F, 0F, 1F, 10F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.4F, 0.0F, -2.55F));
        robe_side_right.addOrReplaceChild("pt_robe_sr", CubeListBuilder.create()
            .texOffs(74, 0).addBox(0F, 0F, 0F, 1F, 10F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.4F, 0.0F, -2.55F));
        robe_back_left.addOrReplaceChild("pt_robe_bl", CubeListBuilder.create()
            .texOffs(64, 17).addBox(0F, 0F, 0F, 3F, 10F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.9F, 0.0F, -0.35F));
        robe_back_right.addOrReplaceChild("pt_robe_br", CubeListBuilder.create()
            .texOffs(73, 17).addBox(0F, 0F, 0F, 3F, 10F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.9F, 0.0F, -0.35F));
        right_arm.addOrReplaceChild("pt_sleeve_r", CubeListBuilder.create()
            .texOffs(0, 17).addBox(0F, 0F, 0F, 6F, 6F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.0F, -0.4F, -2.95F));
        right_arm.addOrReplaceChild("pt_sleeve_r_trim", CubeListBuilder.create()
            .texOffs(83, 29).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.9F, 5.9F, -2.85F));
        right_arm.addOrReplaceChild("pt_vambrace_r", CubeListBuilder.create()
            .texOffs(0, 29).addBox(0F, 0F, 0F, 4F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.2F, 7.0F, -2.4F));
        left_arm.addOrReplaceChild("pt_sleeve_l", CubeListBuilder.create()
            .texOffs(23, 17).addBox(0F, 0F, 0F, 6F, 6F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-2.1F, -0.4F, -2.95F));
        left_arm.addOrReplaceChild("pt_sleeve_l_trim", CubeListBuilder.create()
            .texOffs(104, 29).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-2.0F, 5.9F, -2.85F));
        left_arm.addOrReplaceChild("pt_vambrace_l", CubeListBuilder.create()
            .texOffs(17, 29).addBox(0F, 0F, 0F, 4F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.3F, 7.0F, -2.4F));
        right_leg.addOrReplaceChild("pt_trouser_r", CubeListBuilder.create()
            .texOffs(27, 0).addBox(0F, 0F, 0F, 4F, 11F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.1F, 0.1F, -2.2F));
        right_leg.addOrReplaceChild("pt_knee_r", CubeListBuilder.create()
            .texOffs(0, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.3F, 4.6F, -2.5F));
        right_leg.addOrReplaceChild("pt_greave_r", CubeListBuilder.create()
            .texOffs(34, 29).addBox(0F, 0F, 0F, 4F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.3F, 6.4F, -2.4F));
        right_leg.addOrReplaceChild("pt_boot_r", CubeListBuilder.create()
            .texOffs(19, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 11.0F, -2.7F));
        right_leg.addOrReplaceChild("pt_sole_r", CubeListBuilder.create()
            .texOffs(38, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F),
            PartPose.offset(-2.4F, 12.5F, -2.75F));
        left_leg.addOrReplaceChild("pt_trouser_l", CubeListBuilder.create()
            .texOffs(44, 0).addBox(0F, 0F, 0F, 4F, 11F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.1F, 0.1F, -2.2F));
        left_leg.addOrReplaceChild("pt_knee_l", CubeListBuilder.create()
            .texOffs(57, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.3F, 4.6F, -2.5F));
        left_leg.addOrReplaceChild("pt_greave_l", CubeListBuilder.create()
            .texOffs(51, 29).addBox(0F, 0F, 0F, 4F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.3F, 6.4F, -2.4F));
        left_leg.addOrReplaceChild("pt_boot_l", CubeListBuilder.create()
            .texOffs(76, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 11.0F, -2.7F));
        left_leg.addOrReplaceChild("pt_sole_l", CubeListBuilder.create()
            .texOffs(95, 38).addBox(0F, 0F, 0F, 4F, 1F, 5F),
            PartPose.offset(-2.4F, 12.5F, -2.75F));
        return LayerDefinition.create(mesh, 128, 128);
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks,
                          float netHeadYaw, float headPitch) {
    }
    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay,
                               float red, float green, float blue, float alpha) {
        root.render(poseStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}
