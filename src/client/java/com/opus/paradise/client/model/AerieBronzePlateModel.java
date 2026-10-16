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
 * Aerie Bronze plate: red tunic under a leather backing, stylized
 * anatomical bronze cuirass (muscle plates, sternum line, abdominal
 * segments), layered shoulder straps, leather pteruges in four groups,
 * bronze vambraces, greaves and roman caligae with studded soles.
 */
public final class AerieBronzePlateModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "aerie_bronze_plate"), "main");

    private final ModelPart root;
    public AerieBronzePlateModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart body() { return root.getChild("body"); }
    public ModelPart rightArm() { return root.getChild("right_arm"); }
    public ModelPart leftArm() { return root.getChild("left_arm"); }
    public ModelPart rightLeg() { return root.getChild("right_leg"); }
    public ModelPart leftLeg() { return root.getChild("left_leg"); }
    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }
    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }
    public ModelPart pteruges_front() { return root.getChild("body").getChild("pteruges_front"); }
    public ModelPart pteruges_back() { return root.getChild("body").getChild("pteruges_back"); }
    public ModelPart pteruges_left() { return root.getChild("body").getChild("pteruges_left"); }
    public ModelPart pteruges_right() { return root.getChild("body").getChild("pteruges_right"); }

    /** Per-piece visibility: helmet / cuirass+arms / leggings group / boots group. */
    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {
        body().visible = chest;
        shoulderLeft().visible = chest;
        shoulderRight().visible = chest;
        body().getChild("pteruges_front").visible = chest || legs;
        body().getChild("pteruges_back").visible = chest || legs;
        body().getChild("pteruges_left").visible = chest || legs;
        body().getChild("pteruges_right").visible = chest || legs;
        rightArm().visible = chest;
        leftArm().visible = chest;
        rightLeg().getChild("ab_inner_r").visible = legs || feet;
        rightLeg().getChild("ab_greave_r").visible = feet;
        rightLeg().getChild("ab_sole_r").visible = feet;
        rightLeg().getChild("ab_toe_r").visible = feet;
        rightLeg().getChild("ab_heel_r").visible = legs || feet;
        leftLeg().getChild("ab_inner_l").visible = legs || feet;
        leftLeg().getChild("ab_greave_l").visible = feet;
        leftLeg().getChild("ab_sole_l").visible = feet;
        leftLeg().getChild("ab_toe_l").visible = feet;
        leftLeg().getChild("ab_heel_l").visible = legs || feet;
    }

    public static LayerDefinition createLayerDefinition() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_arm = root.addOrReplaceChild("right_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_arm = root.addOrReplaceChild("left_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_leg = root.addOrReplaceChild("right_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_leg = root.addOrReplaceChild("left_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));
        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));
        PartDefinition pteruges_front = body.addOrReplaceChild("pteruges_front", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 11.9F, -2.75F, 0F, 0F, 0F));
        PartDefinition pteruges_back = body.addOrReplaceChild("pteruges_back", CubeListBuilder.create(), PartPose.offsetAndRotation(0F, 11.9F, 2.75F, 0F, 0F, 0F));
        PartDefinition pteruges_left = body.addOrReplaceChild("pteruges_left", CubeListBuilder.create(), PartPose.offsetAndRotation(4.8F, 11.9F, 0F, 0F, 0F, 0F));
        PartDefinition pteruges_right = body.addOrReplaceChild("pteruges_right", CubeListBuilder.create(), PartPose.offsetAndRotation(-4.8F, 11.9F, 0F, 0F, 0F, 0F));

        body.addOrReplaceChild("ab_tunic_up", CubeListBuilder.create()
            .texOffs(74, 16).addBox(0F, 0F, 0F, 8F, 2F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.1F, 0.5F, -2.6F));
        body.addOrReplaceChild("ab_backing", CubeListBuilder.create()
            .texOffs(65, 0).addBox(0F, 0F, 0F, 8F, 7F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.2F, 2.6F, -2.75F));
        body.addOrReplaceChild("ab_cuirass", CubeListBuilder.create()
            .texOffs(34, 0).addBox(0F, 0F, 0F, 9F, 8F, 6F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.5F, 1.4F, -3.05F));
        body.addOrReplaceChild("ab_muscle_l", CubeListBuilder.create()
            .texOffs(36, 34).addBox(0F, 0F, 0F, 3F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.9F, 2.4F, -3.4F));
        body.addOrReplaceChild("ab_muscle_r", CubeListBuilder.create()
            .texOffs(45, 34).addBox(0F, 0F, 0F, 3F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(0.5F, 2.4F, -3.4F));
        body.addOrReplaceChild("ab_sternum", CubeListBuilder.create()
            .texOffs(39, 26).addBox(0F, 0F, 0F, 1F, 6F, 1F),
            PartPose.offset(-0.45F, 2.2F, -3.45F));
        body.addOrReplaceChild("ab_abs_1", CubeListBuilder.create()
            .texOffs(96, 34).addBox(0F, 0F, 0F, 5F, 1F, 1F),
            PartPose.offset(-2.6F, 7.3F, -3.3F));
        body.addOrReplaceChild("ab_abs_2", CubeListBuilder.create()
            .texOffs(109, 34).addBox(0F, 0F, 0F, 5F, 1F, 1F),
            PartPose.offset(-2.5F, 8.6F, -3.25F));
        body.addOrReplaceChild("ab_fast_l", CubeListBuilder.create()
            .texOffs(105, 26).addBox(0F, 0F, 0F, 1F, 2F, 3F),
            PartPose.offset(4.35F, 4.6F, -1.6F));
        body.addOrReplaceChild("ab_fast_r", CubeListBuilder.create()
            .texOffs(114, 26).addBox(0F, 0F, 0F, 1F, 2F, 3F),
            PartPose.offset(-4.95F, 4.6F, -1.6F));
        body.addOrReplaceChild("ab_belt", CubeListBuilder.create()
            .texOffs(45, 16).addBox(0F, 0F, 0F, 9F, 2F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.6F, 9.8F, -2.9F));
        body.addOrReplaceChild("ab_buckle", CubeListBuilder.create()
            .texOffs(36, 39).addBox(0F, 0F, 0F, 2F, 1F, 1F),
            PartPose.offset(-1.0F, 9.95F, -3.35F));
        shoulder_left.addOrReplaceChild("ab_strap_l1", CubeListBuilder.create()
            .texOffs(54, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(2.9F, -2.5F, -2.4F));
        shoulder_left.addOrReplaceChild("ab_strap_l2", CubeListBuilder.create()
            .texOffs(61, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(2.8F, -1.4F, -0.5F));
        shoulder_left.addOrReplaceChild("ab_strap_l3", CubeListBuilder.create()
            .texOffs(68, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(2.7F, -0.4F, 1.4F));
        shoulder_right.addOrReplaceChild("ab_strap_r1", CubeListBuilder.create()
            .texOffs(75, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.5F, -2.5F, -2.4F));
        shoulder_right.addOrReplaceChild("ab_strap_r2", CubeListBuilder.create()
            .texOffs(82, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.5F, -1.4F, -0.5F));
        shoulder_right.addOrReplaceChild("ab_strap_r3", CubeListBuilder.create()
            .texOffs(89, 34).addBox(0F, 0F, 0F, 1F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.5F, -0.4F, 1.4F));
        pteruges_front.addOrReplaceChild("ab_pteru_f", CubeListBuilder.create()
            .texOffs(0, 34).addBox(0F, 0F, 0F, 3F, 3F, 1F),
            PartPose.offset(-3.4F, 0.0F, -0.3F));
        pteruges_front.addOrReplaceChild("ab_pteru_f2", CubeListBuilder.create()
            .texOffs(9, 34).addBox(0F, 0F, 0F, 3F, 3F, 1F),
            PartPose.offset(0.1F, 0.0F, -0.3F));
        pteruges_back.addOrReplaceChild("ab_pteru_b", CubeListBuilder.create()
            .texOffs(18, 34).addBox(0F, 0F, 0F, 3F, 3F, 1F),
            PartPose.offset(-3.4F, 0.0F, -0.3F));
        pteruges_back.addOrReplaceChild("ab_pteru_b2", CubeListBuilder.create()
            .texOffs(27, 34).addBox(0F, 0F, 0F, 3F, 3F, 1F),
            PartPose.offset(0.1F, 0.0F, -0.3F));
        pteruges_left.addOrReplaceChild("ab_pteru_l", CubeListBuilder.create()
            .texOffs(19, 16).addBox(0F, 0F, 0F, 1F, 3F, 5F),
            PartPose.offset(-0.3F, 0.0F, -2.55F));
        pteruges_right.addOrReplaceChild("ab_pteru_r", CubeListBuilder.create()
            .texOffs(32, 16).addBox(0F, 0F, 0F, 1F, 3F, 5F),
            PartPose.offset(-0.3F, 0.0F, -2.55F));
        body.addOrReplaceChild("ab_skirt", CubeListBuilder.create()
            .texOffs(44, 26).addBox(0F, 0F, 0F, 7F, 2F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.9F, 11.5F, -2.4F));
        right_arm.addOrReplaceChild("ab_sleeve_r", CubeListBuilder.create()
            .texOffs(101, 16).addBox(0F, 0F, 0F, 4F, 3F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.4F, 0.9F, -2.3F));
        right_arm.addOrReplaceChild("ab_vambrace_r", CubeListBuilder.create()
            .texOffs(92, 0).addBox(0F, 0F, 0F, 5F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.5F, 4.0F, -2.4F));
        left_arm.addOrReplaceChild("ab_sleeve_l", CubeListBuilder.create()
            .texOffs(0, 26).addBox(0F, 0F, 0F, 4F, 3F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.4F, 0.9F, -2.3F));
        left_arm.addOrReplaceChild("ab_vambrace_l", CubeListBuilder.create()
            .texOffs(0, 16).addBox(0F, 0F, 0F, 5F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.5F, 4.0F, -2.4F));
        right_leg.addOrReplaceChild("ab_inner_r", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 4F, 11F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.2F, 0.3F, -2.2F));
        right_leg.addOrReplaceChild("ab_greave_r", CubeListBuilder.create()
            .texOffs(17, 26).addBox(0F, 0F, 0F, 4F, 6F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.0F, 5.6F, -2.8F));
        right_leg.addOrReplaceChild("ab_sole_r", CubeListBuilder.create()
            .texOffs(67, 26).addBox(0F, 0F, 0F, 4F, 1F, 5F),
            PartPose.offset(-2.4F, 11.85F, -2.75F));
        right_leg.addOrReplaceChild("ab_toe_r", CubeListBuilder.create()
            .texOffs(0, 39).addBox(0F, 0F, 0F, 3F, 1F, 1F),
            PartPose.offset(-1.9F, 11.9F, -3.5F));
        right_leg.addOrReplaceChild("ab_heel_r", CubeListBuilder.create()
            .texOffs(9, 39).addBox(0F, 0F, 0F, 3F, 1F, 1F),
            PartPose.offset(-1.9F, 11.3F, 2.35F));
        left_leg.addOrReplaceChild("ab_inner_l", CubeListBuilder.create()
            .texOffs(17, 0).addBox(0F, 0F, 0F, 4F, 11F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.2F, 0.3F, -2.2F));
        left_leg.addOrReplaceChild("ab_greave_l", CubeListBuilder.create()
            .texOffs(28, 26).addBox(0F, 0F, 0F, 4F, 6F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.0F, 5.6F, -2.8F));
        left_leg.addOrReplaceChild("ab_sole_l", CubeListBuilder.create()
            .texOffs(86, 26).addBox(0F, 0F, 0F, 4F, 1F, 5F),
            PartPose.offset(-2.4F, 11.85F, -2.75F));
        left_leg.addOrReplaceChild("ab_toe_l", CubeListBuilder.create()
            .texOffs(18, 39).addBox(0F, 0F, 0F, 3F, 1F, 1F),
            PartPose.offset(-1.9F, 11.9F, -3.5F));
        left_leg.addOrReplaceChild("ab_heel_l", CubeListBuilder.create()
            .texOffs(27, 39).addBox(0F, 0F, 0F, 3F, 1F, 1F),
            PartPose.offset(-1.9F, 11.3F, 2.35F));

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
