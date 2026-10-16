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
 * Fire Demonic helm: blackened volcanic base, red forehead plates, narrow
 * infernal visor (brightest center) with dark backing, jaw guard, layered
 * cheeks, neck guard, central ridge and two enormous segmented horns
 * curving upward and backward with ember cracks between segments.
 */
public final class FireDemonicHelmetModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "fire_demonic_helmet"), "main");

    private final ModelPart root;
    public FireDemonicHelmetModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart head() { return root.getChild("head"); }
    public ModelPart horn_left_root() { return root.getChild("head").getChild("horn_left_root"); }
    public ModelPart horn_left_01() { return root.getChild("head").getChild("horn_left_01"); }
    public ModelPart horn_left_02() { return root.getChild("head").getChild("horn_left_02"); }
    public ModelPart horn_left_03() { return root.getChild("head").getChild("horn_left_03"); }
    public ModelPart horn_left_tip() { return root.getChild("head").getChild("horn_left_tip"); }
    public ModelPart horn_right_root() { return root.getChild("head").getChild("horn_right_root"); }
    public ModelPart horn_right_01() { return root.getChild("head").getChild("horn_right_01"); }
    public ModelPart horn_right_02() { return root.getChild("head").getChild("horn_right_02"); }
    public ModelPart horn_right_03() { return root.getChild("head").getChild("horn_right_03"); }
    public ModelPart horn_right_tip() { return root.getChild("head").getChild("horn_right_tip"); }

    /** Per-piece visibility: helmet / cuirass+arms / leggings group / boots group. */
    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {
        head().visible = head;
    }

    public static LayerDefinition createLayerDefinition() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition horn_left_root = head.addOrReplaceChild("horn_left_root", CubeListBuilder.create(), PartPose.offsetAndRotation(3.4F, -8.6F, -1.6F, -18F, 10F, -26F));
        PartDefinition horn_left_01 = head.addOrReplaceChild("horn_left_01", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.9F, -1.6F, -0.9F, -16F, 4F, -10F));
        PartDefinition horn_left_02 = head.addOrReplaceChild("horn_left_02", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.8F, -2.6F, -0.8F, -14F, 0F, -8F));
        PartDefinition horn_left_03 = head.addOrReplaceChild("horn_left_03", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.7F, -2.3F, -0.7F, -10F, -2F, -6F));
        PartDefinition horn_left_tip = head.addOrReplaceChild("horn_left_tip", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.5F, -2.0F, -0.6F, -8F, 0F, -8F));
        PartDefinition horn_right_root = head.addOrReplaceChild("horn_right_root", CubeListBuilder.create(), PartPose.offsetAndRotation(-4.0F, -8.6F, -1.6F, -18F, -10F, 26F));
        PartDefinition horn_right_01 = head.addOrReplaceChild("horn_right_01", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.8F, -1.6F, -0.9F, -16F, -4F, 10F));
        PartDefinition horn_right_02 = head.addOrReplaceChild("horn_right_02", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.8F, -2.6F, -0.8F, -14F, 0F, 8F));
        PartDefinition horn_right_03 = head.addOrReplaceChild("horn_right_03", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.6F, -2.3F, -0.7F, -10F, 2F, 6F));
        PartDefinition horn_right_tip = head.addOrReplaceChild("horn_right_tip", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.5F, -2.0F, -0.6F, -8F, 0F, 8F));

        head.addOrReplaceChild("helm_base", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 9F, 9F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(-4.5F, -8.7F, -4.5F));
        head.addOrReplaceChild("faceplate", CubeListBuilder.create()
            .texOffs(60, 0).addBox(0F, 0F, 0F, 8F, 6F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.3F, -7.1F, -5.45F));
        head.addOrReplaceChild("visor", CubeListBuilder.create()
            .texOffs(95, 19).addBox(0F, 0F, 0F, 5F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.9F, -5.5F, -5.8F));
        head.addOrReplaceChild("visor_backing", CubeListBuilder.create()
            .texOffs(80, 19).addBox(0F, 0F, 0F, 6F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.0F, -5.7F, -4.85F));
        head.addOrReplaceChild("jaw_guard", CubeListBuilder.create()
            .texOffs(45, 19).addBox(0F, 0F, 0F, 6F, 3F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.4F, -2.0F, -4.95F));
        head.addOrReplaceChild("cheek_left", CubeListBuilder.create()
            .texOffs(79, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(3.6F, -4.9F, -4.6F));
        head.addOrReplaceChild("cheek_right", CubeListBuilder.create()
            .texOffs(88, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.1F, -4.9F, -4.6F));
        head.addOrReplaceChild("neck_guard", CubeListBuilder.create()
            .texOffs(97, 0).addBox(0F, 0F, 0F, 8F, 4F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.0F, -3.5F, 3.3F));
        head.addOrReplaceChild("crown_ridge", CubeListBuilder.create()
            .texOffs(37, 0).addBox(0F, 0F, 0F, 1F, 1F, 10F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.7F, -10.1F, -5.0F));
        horn_left_root.addOrReplaceChild("horn_l_root", CubeListBuilder.create()
            .texOffs(116, 0).addBox(0F, 0F, 0F, 3F, 2F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.5F, -1.2F, -1.5F));
        horn_left_01.addOrReplaceChild("horn_l_01", CubeListBuilder.create()
            .texOffs(11, 19).addBox(0F, 0F, 0F, 2F, 3F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.2F, -3.4F, -1.2F));
        horn_left_02.addOrReplaceChild("horn_l_02", CubeListBuilder.create()
            .texOffs(20, 19).addBox(0F, 0F, 0F, 2F, 3F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.0F, -3.0F, -1.0F));
        horn_left_03.addOrReplaceChild("horn_l_03", CubeListBuilder.create()
            .texOffs(60, 19).addBox(0F, 0F, 0F, 1F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.8F, -2.7F, -0.8F));
        horn_left_tip.addOrReplaceChild("horn_l_tip", CubeListBuilder.create()
            .texOffs(65, 19).addBox(0F, 0F, 0F, 1F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.6F, -2.3F, -0.6F));
        horn_right_root.addOrReplaceChild("horn_r_root", CubeListBuilder.create()
            .texOffs(0, 19).addBox(0F, 0F, 0F, 2F, 2F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.4F, -1.2F, -1.5F));
        horn_right_01.addOrReplaceChild("horn_r_01", CubeListBuilder.create()
            .texOffs(29, 19).addBox(0F, 0F, 0F, 2F, 3F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.1F, -3.4F, -1.2F));
        horn_right_02.addOrReplaceChild("horn_r_02", CubeListBuilder.create()
            .texOffs(38, 19).addBox(0F, 0F, 0F, 1F, 3F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.9F, -3.0F, -1.0F));
        horn_right_03.addOrReplaceChild("horn_r_03", CubeListBuilder.create()
            .texOffs(70, 19).addBox(0F, 0F, 0F, 1F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.7F, -2.7F, -0.8F));
        horn_right_tip.addOrReplaceChild("horn_r_tip", CubeListBuilder.create()
            .texOffs(75, 19).addBox(0F, 0F, 0F, 1F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-0.55F, -2.3F, -0.6F));

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
