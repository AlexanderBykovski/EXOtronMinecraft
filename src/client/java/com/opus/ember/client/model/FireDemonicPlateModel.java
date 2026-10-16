package com.opus.ember.client.model;

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
 * Fire Demonic plate: sternum core under V-overlap chest plates, rib side
 * plates, jagged pauldrons with broken-plate spikes, back plate with two
 * fire vents, ember-buckled belt, clawed gauntlets, thigh/knee/greave legs
 * and heavy boots with claw toes and sole fire vents.
 */
public final class FireDemonicPlateModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "fire_demonic_plate"), "main");

    private final ModelPart root;
    public FireDemonicPlateModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart body() { return root.getChild("body"); }
    public ModelPart rightArm() { return root.getChild("right_arm"); }
    public ModelPart leftArm() { return root.getChild("left_arm"); }
    public ModelPart rightLeg() { return root.getChild("right_leg"); }
    public ModelPart leftLeg() { return root.getChild("left_leg"); }
    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }
    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }

    /** Per-piece visibility: helmet / cuirass+arms / leggings group / boots group. */
    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {
        body().visible = chest;
        shoulderLeft().visible = chest;
        shoulderRight().visible = chest;
        rightArm().visible = chest;
        leftArm().visible = chest;
        rightLeg().getChild("thigh_r").visible = legs;
        rightLeg().getChild("knee_r").visible = legs || feet;
        rightLeg().getChild("greave_r").visible = feet;
        rightLeg().getChild("boot_r").visible = feet;
        rightLeg().getChild("toe_r").visible = feet;
        rightLeg().getChild("vent_r").visible = feet;
        leftLeg().getChild("thigh_l").visible = legs;
        leftLeg().getChild("knee_l").visible = legs || feet;
        leftLeg().getChild("greave_l").visible = feet;
        leftLeg().getChild("boot_l").visible = feet;
        leftLeg().getChild("toe_l").visible = feet;
        leftLeg().getChild("vent_l").visible = feet;
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

        body.addOrReplaceChild("lining", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 8F, 10F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.1F, 0.8F, -2.6F));
        body.addOrReplaceChild("chest_core", CubeListBuilder.create()
            .texOffs(76, 34).addBox(0F, 0F, 0F, 5F, 5F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.6F, 3.0F, -3.15F));
        body.addOrReplaceChild("plate_upper", CubeListBuilder.create()
            .texOffs(27, 0).addBox(0F, 0F, 0F, 8F, 3F, 6F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.4F, 1.0F, -2.95F));
        body.addOrReplaceChild("plate_middle", CubeListBuilder.create()
            .texOffs(22, 16).addBox(0F, 0F, 0F, 8F, 3F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.3F, 4.1F, -2.9F));
        body.addOrReplaceChild("plate_lower", CubeListBuilder.create()
            .texOffs(49, 16).addBox(0F, 0F, 0F, 8F, 3F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.2F, 6.9F, -2.85F));
        body.addOrReplaceChild("rib_left", CubeListBuilder.create()
            .texOffs(0, 16).addBox(0F, 0F, 0F, 1F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(3.9F, 3.0F, -2.45F));
        body.addOrReplaceChild("rib_right", CubeListBuilder.create()
            .texOffs(11, 16).addBox(0F, 0F, 0F, 1F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.1F, 3.0F, -2.45F));
        body.addOrReplaceChild("back_plate", CubeListBuilder.create()
            .texOffs(0, 26).addBox(0F, 0F, 0F, 7F, 6F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.6F, 1.8F, 2.4F));
        body.addOrReplaceChild("back_vent_l", CubeListBuilder.create()
            .texOffs(78, 41).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(0.6F, 2.6F, 3.5F));
        body.addOrReplaceChild("back_vent_r", CubeListBuilder.create()
            .texOffs(83, 41).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(-2.3F, 2.6F, 3.5F));
        body.addOrReplaceChild("belt", CubeListBuilder.create()
            .texOffs(47, 26).addBox(0F, 0F, 0F, 9F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.5F, 10.5F, -2.8F));
        body.addOrReplaceChild("buckle", CubeListBuilder.create()
            .texOffs(110, 41).addBox(0F, 0F, 0F, 2F, 1F, 1F),
            PartPose.offset(-1.3F, 10.7F, -3.35F));
        shoulder_left.addOrReplaceChild("pauldron_l", CubeListBuilder.create()
            .texOffs(17, 26).addBox(0F, 0F, 0F, 2F, 2F, 5F, new CubeDeformation(0.08f)),
            PartPose.offset(3.0F, -2.9F, -2.5F));
        shoulder_left.addOrReplaceChild("pauldron_l_lo", CubeListBuilder.create()
            .texOffs(0, 41).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.08f)),
            PartPose.offset(3.1F, 0.0F, -2.3F));
        shoulder_left.addOrReplaceChild("spike_l1", CubeListBuilder.create()
            .texOffs(117, 41).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(3.5F, -4.4F, -2.2F));
        shoulder_left.addOrReplaceChild("spike_l2", CubeListBuilder.create()
            .texOffs(122, 41).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(3.7F, -4.2F, 0.5F));
        shoulder_right.addOrReplaceChild("pauldron_r", CubeListBuilder.create()
            .texOffs(32, 26).addBox(0F, 0F, 0F, 2F, 2F, 5F, new CubeDeformation(0.08f)),
            PartPose.offset(-5.7F, -2.9F, -2.5F));
        shoulder_right.addOrReplaceChild("pauldron_r_lo", CubeListBuilder.create()
            .texOffs(13, 41).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.08f)),
            PartPose.offset(-5.6F, 0.0F, -2.3F));
        shoulder_right.addOrReplaceChild("spike_r1", CubeListBuilder.create()
            .texOffs(0, 47).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(-5.2F, -4.4F, -2.2F));
        shoulder_right.addOrReplaceChild("spike_r2", CubeListBuilder.create()
            .texOffs(5, 47).addBox(0F, 0F, 0F, 1F, 1F, 1F),
            PartPose.offset(-5.2F, -4.2F, 0.5F));
        right_arm.addOrReplaceChild("gauntlet_r", CubeListBuilder.create()
            .texOffs(76, 16).addBox(0F, 0F, 0F, 5F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.5F, 3.9F, -2.4F));
        right_arm.addOrReplaceChild("upper_r", CubeListBuilder.create()
            .texOffs(42, 34).addBox(0F, 0F, 0F, 4F, 2F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.3F, 8.0F, -2.2F));
        right_arm.addOrReplaceChild("wrist_r", CubeListBuilder.create()
            .texOffs(76, 26).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.6F, 10.1F, -2.5F));
        right_arm.addOrReplaceChild("claws_r", CubeListBuilder.create()
            .texOffs(26, 41).addBox(0F, 0F, 0F, 3F, 1F, 3F),
            PartPose.offset(-2.5F, 11.2F, -1.7F));
        left_arm.addOrReplaceChild("gauntlet_l", CubeListBuilder.create()
            .texOffs(95, 16).addBox(0F, 0F, 0F, 5F, 4F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.5F, 3.9F, -2.4F));
        left_arm.addOrReplaceChild("upper_l", CubeListBuilder.create()
            .texOffs(59, 34).addBox(0F, 0F, 0F, 4F, 2F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.3F, 8.0F, -2.2F));
        left_arm.addOrReplaceChild("wrist_l", CubeListBuilder.create()
            .texOffs(97, 26).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.6F, 10.1F, -2.5F));
        left_arm.addOrReplaceChild("claws_l", CubeListBuilder.create()
            .texOffs(39, 41).addBox(0F, 0F, 0F, 3F, 1F, 3F),
            PartPose.offset(-0.5F, 11.2F, -1.7F));
        right_leg.addOrReplaceChild("thigh_r", CubeListBuilder.create()
            .texOffs(56, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.5F, -2.3F));
        right_leg.addOrReplaceChild("knee_r", CubeListBuilder.create()
            .texOffs(89, 34).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.4F, -2.4F));
        right_leg.addOrReplaceChild("greave_r", CubeListBuilder.create()
            .texOffs(73, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.1F, -2.3F));
        right_leg.addOrReplaceChild("boot_r", CubeListBuilder.create()
            .texOffs(0, 34).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.0F, -2.8F));
        right_leg.addOrReplaceChild("toe_r", CubeListBuilder.create()
            .texOffs(88, 41).addBox(0F, 0F, 0F, 4F, 1F, 1F),
            PartPose.offset(-2.2F, 11.3F, -3.5F));
        right_leg.addOrReplaceChild("vent_r", CubeListBuilder.create()
            .texOffs(52, 41).addBox(0F, 0F, 0F, 3F, 1F, 3F),
            PartPose.offset(-1.5F, 12.2F, -1.6F));
        left_leg.addOrReplaceChild("thigh_l", CubeListBuilder.create()
            .texOffs(90, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.5F, -2.3F));
        left_leg.addOrReplaceChild("knee_l", CubeListBuilder.create()
            .texOffs(108, 34).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.4F, -2.4F));
        left_leg.addOrReplaceChild("greave_l", CubeListBuilder.create()
            .texOffs(107, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.1F, -2.3F));
        left_leg.addOrReplaceChild("boot_l", CubeListBuilder.create()
            .texOffs(21, 34).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.0F, -2.8F));
        left_leg.addOrReplaceChild("toe_l", CubeListBuilder.create()
            .texOffs(99, 41).addBox(0F, 0F, 0F, 4F, 1F, 1F),
            PartPose.offset(-2.2F, 11.3F, -3.5F));
        left_leg.addOrReplaceChild("vent_l", CubeListBuilder.create()
            .texOffs(65, 41).addBox(0F, 0F, 0F, 3F, 1F, 3F),
            PartPose.offset(-1.5F, 12.2F, -1.6F));

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
