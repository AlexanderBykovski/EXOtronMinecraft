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
 * Vein Crust helm: closed columnar-basalt bowl with vertical stone ribs,
 * blackstone brow frame around a narrow dark-red visor with magma pixels,
 * dark backing behind the visor, rectangular cheeks and thick neck guard.
 * No horns, no spikes. Emissive pass: visor interior only.
 */
public final class FireHelmetModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "fire_helmet"), "main");

    private final ModelPart root;
    public FireHelmetModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart head() { return root.getChild("head"); }

    /** Per-piece visibility: helmet / cuirass+arms / leggings group / boots group. */
    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet) {
        head().visible = head;
    }

    public static LayerDefinition createLayerDefinition() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create(), PartPose.ZERO);

        head.addOrReplaceChild("helmet_core", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 9F, 9F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(-4.6F, -8.7F, -4.6F));
        head.addOrReplaceChild("helmet_ribs_c", CubeListBuilder.create()
            .texOffs(37, 0).addBox(0F, 0F, 0F, 1F, 1F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(-0.65F, -9.5F, -4.85F));
        head.addOrReplaceChild("helmet_ribs_l", CubeListBuilder.create()
            .texOffs(58, 0).addBox(0F, 0F, 0F, 1F, 1F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(2.75F, -9.3F, -4.5F));
        head.addOrReplaceChild("helmet_ribs_r", CubeListBuilder.create()
            .texOffs(79, 0).addBox(0F, 0F, 0F, 1F, 1F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(-3.85F, -9.3F, -4.5F));
        head.addOrReplaceChild("brow_band", CubeListBuilder.create()
            .texOffs(34, 19).addBox(0F, 0F, 0F, 9F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.5F, -6.1F, -5.45F));
        head.addOrReplaceChild("visor", CubeListBuilder.create()
            .texOffs(70, 19).addBox(0F, 0F, 0F, 5F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.9F, -5.5F, -5.65F));
        head.addOrReplaceChild("visor_backing", CubeListBuilder.create()
            .texOffs(55, 19).addBox(0F, 0F, 0F, 6F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.1F, -5.8F, -4.8F));
        head.addOrReplaceChild("cheek_left", CubeListBuilder.create()
            .texOffs(100, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(3.85F, -5.5F, -4.4F));
        head.addOrReplaceChild("cheek_right", CubeListBuilder.create()
            .texOffs(109, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.2F, -5.5F, -4.4F));
        head.addOrReplaceChild("jaw_guard", CubeListBuilder.create()
            .texOffs(19, 19).addBox(0F, 0F, 0F, 6F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.3F, -1.6F, -4.75F));
        head.addOrReplaceChild("neck_guard", CubeListBuilder.create()
            .texOffs(0, 19).addBox(0F, 0F, 0F, 8F, 4F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.2F, -3.7F, 3.6F));

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
