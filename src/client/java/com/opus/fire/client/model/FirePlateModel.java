package com.opus.fire.client.model;

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
 * Vein Crust plate: dark heat-resistant lining, interlocking vertical basalt
 * columns with blackstone borders, small trapped-magma sternum core, back
 * plate, compact layered shoulders, segmented forearms with blackstone
 * wrists and knuckle guards, thigh/knee plates, ribbed greaves, heavy
 * boots with blackstone ankle frames and magma-seamed soles.
 */
public final class FirePlateModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "fire_plate"), "main");

    private final ModelPart root;
    public FirePlateModel(ModelPart root) { this.root = root; }
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
        rightLeg().getChild("sole_r").visible = feet;
        leftLeg().getChild("thigh_l").visible = legs;
        leftLeg().getChild("knee_l").visible = legs || feet;
        leftLeg().getChild("greave_l").visible = feet;
        leftLeg().getChild("boot_l").visible = feet;
        leftLeg().getChild("sole_l").visible = feet;
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
            PartPose.offset(-4.1F, 1.0F, -2.6F));
        body.addOrReplaceChild("border_top", CubeListBuilder.create()
            .texOffs(17, 16).addBox(0F, 0F, 0F, 9F, 1F, 6F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.6F, 0.7F, -3.0F));
        body.addOrReplaceChild("border_bottom", CubeListBuilder.create()
            .texOffs(0, 25).addBox(0F, 0F, 0F, 9F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.5F, 9.6F, -2.95F));
        body.addOrReplaceChild("sternum", CubeListBuilder.create()
            .texOffs(0, 16).addBox(0F, 0F, 0F, 2F, 7F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-1.15F, 1.6F, -3.2F));
        body.addOrReplaceChild("col_c_l", CubeListBuilder.create()
            .texOffs(114, 0).addBox(0F, 0F, 0F, 2F, 8F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(1.25F, 1.5F, -3.05F));
        body.addOrReplaceChild("col_c_r", CubeListBuilder.create()
            .texOffs(121, 0).addBox(0F, 0F, 0F, 2F, 8F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.25F, 1.5F, -3.05F));
        body.addOrReplaceChild("col_o_l", CubeListBuilder.create()
            .texOffs(7, 16).addBox(0F, 0F, 0F, 1F, 7F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(3.35F, 1.8F, -2.85F));
        body.addOrReplaceChild("col_o_r", CubeListBuilder.create()
            .texOffs(12, 16).addBox(0F, 0F, 0F, 1F, 7F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.7F, 1.8F, -2.85F));
        body.addOrReplaceChild("magma_core", CubeListBuilder.create()
            .texOffs(60, 39).addBox(0F, 0F, 0F, 1F, 2F, 1F),
            PartPose.offset(-0.95F, 3.6F, -3.4F));
        body.addOrReplaceChild("back_plate", CubeListBuilder.create()
            .texOffs(27, 0).addBox(0F, 0F, 0F, 8F, 8F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.0F, 1.4F, 2.55F));
        body.addOrReplaceChild("belt", CubeListBuilder.create()
            .texOffs(29, 25).addBox(0F, 0F, 0F, 9F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.5F, 10.4F, -2.85F));
        shoulder_left.addOrReplaceChild("pauldron_l", CubeListBuilder.create()
            .texOffs(82, 16).addBox(0F, 0F, 0F, 2F, 2F, 5F, new CubeDeformation(0.08f)),
            PartPose.offset(2.9F, -2.8F, -2.5F));
        shoulder_left.addOrReplaceChild("pauldron_l_lo", CubeListBuilder.create()
            .texOffs(34, 39).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.08f)),
            PartPose.offset(3.0F, 0.2F, -2.3F));
        shoulder_right.addOrReplaceChild("pauldron_r", CubeListBuilder.create()
            .texOffs(97, 16).addBox(0F, 0F, 0F, 2F, 2F, 5F, new CubeDeformation(0.08f)),
            PartPose.offset(-5.8F, -2.8F, -2.5F));
        shoulder_right.addOrReplaceChild("pauldron_r_lo", CubeListBuilder.create()
            .texOffs(47, 39).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.08f)),
            PartPose.offset(-5.7F, 0.2F, -2.3F));
        right_arm.addOrReplaceChild("forearm_r_hi", CubeListBuilder.create()
            .texOffs(48, 16).addBox(0F, 0F, 0F, 4F, 3F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.4F, 3.8F, -2.35F));
        right_arm.addOrReplaceChild("forearm_r_lo", CubeListBuilder.create()
            .texOffs(21, 32).addBox(0F, 0F, 0F, 4F, 2F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.3F, 7.1F, -2.3F));
        right_arm.addOrReplaceChild("wrist_r", CubeListBuilder.create()
            .texOffs(93, 32).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.45F, 9.6F, -2.4F));
        right_arm.addOrReplaceChild("knuckle_r", CubeListBuilder.create()
            .texOffs(110, 32).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.1F, 10.9F, -2.2F));
        left_arm.addOrReplaceChild("forearm_l_hi", CubeListBuilder.create()
            .texOffs(65, 16).addBox(0F, 0F, 0F, 4F, 3F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.3F, 3.8F, -2.35F));
        left_arm.addOrReplaceChild("forearm_l_lo", CubeListBuilder.create()
            .texOffs(38, 32).addBox(0F, 0F, 0F, 4F, 2F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.2F, 7.1F, -2.3F));
        left_arm.addOrReplaceChild("wrist_l", CubeListBuilder.create()
            .texOffs(0, 39).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.35F, 9.6F, -2.4F));
        left_arm.addOrReplaceChild("knuckle_l", CubeListBuilder.create()
            .texOffs(17, 39).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.1F, 10.9F, -2.2F));
        right_leg.addOrReplaceChild("thigh_r", CubeListBuilder.create()
            .texOffs(46, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.5F, -2.3F));
        right_leg.addOrReplaceChild("knee_r", CubeListBuilder.create()
            .texOffs(55, 32).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        right_leg.addOrReplaceChild("greave_r", CubeListBuilder.create()
            .texOffs(63, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.1F, -2.3F));
        right_leg.addOrReplaceChild("boot_r", CubeListBuilder.create()
            .texOffs(58, 25).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.0F, -2.75F));
        right_leg.addOrReplaceChild("sole_r", CubeListBuilder.create()
            .texOffs(79, 25).addBox(0F, 0F, 0F, 5F, 1F, 5F),
            PartPose.offset(-2.5F, 12.55F, -2.85F));
        left_leg.addOrReplaceChild("thigh_l", CubeListBuilder.create()
            .texOffs(80, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.5F, -2.3F));
        left_leg.addOrReplaceChild("knee_l", CubeListBuilder.create()
            .texOffs(74, 32).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        left_leg.addOrReplaceChild("greave_l", CubeListBuilder.create()
            .texOffs(97, 0).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.1F, -2.3F));
        left_leg.addOrReplaceChild("boot_l", CubeListBuilder.create()
            .texOffs(100, 25).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.0F, -2.75F));
        left_leg.addOrReplaceChild("sole_l", CubeListBuilder.create()
            .texOffs(0, 32).addBox(0F, 0F, 0F, 5F, 1F, 5F),
            PartPose.offset(-2.5F, 12.55F, -2.85F));

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
