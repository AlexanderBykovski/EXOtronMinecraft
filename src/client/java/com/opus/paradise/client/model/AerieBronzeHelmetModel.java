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
 * Aerie Bronze helm: rounded segmented bronze bowl with brow band,
 * short cheek guards, rear neck plate, rivets and a restrained dark-red
 * transverse crest on a narrow bronze base. Fully non-emissive.
 */
public final class AerieBronzeHelmetModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation LAYER_LOCATION =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "aerie_bronze_helmet"), "main");

    private final ModelPart root;
    public AerieBronzeHelmetModel(ModelPart root) { this.root = root; }
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

        head.addOrReplaceChild("ab_bowl", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 9F, 5F, 9F, new CubeDeformation(0.55f)),
            PartPose.offset(-4.55F, -8.8F, -4.55F));
        head.addOrReplaceChild("ab_bowl_ridge", CubeListBuilder.create()
            .texOffs(37, 0).addBox(0F, 0F, 0F, 1F, 1F, 8F, new CubeDeformation(0.55f)),
            PartPose.offset(-0.85F, -9.5F, -4.3F));
        head.addOrReplaceChild("ab_brow", CubeListBuilder.create()
            .texOffs(19, 15).addBox(0F, 0F, 0F, 9F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.65F, -6.1F, -5.4F));
        head.addOrReplaceChild("ab_cheek_l", CubeListBuilder.create()
            .texOffs(56, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(3.9F, -5.8F, -4.5F));
        head.addOrReplaceChild("ab_cheek_r", CubeListBuilder.create()
            .texOffs(65, 0).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.35F, -5.8F, -4.5F));
        head.addOrReplaceChild("ab_neck", CubeListBuilder.create()
            .texOffs(74, 0).addBox(0F, 0F, 0F, 8F, 4F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.2F, -4.4F, 3.8F));
        head.addOrReplaceChild("ab_crest_base", CubeListBuilder.create()
            .texOffs(100, 0).addBox(0F, 0F, 0F, 9F, 1F, 2F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.7F, -10.1F, -1.0F));
        head.addOrReplaceChild("ab_crest_support", CubeListBuilder.create()
            .texOffs(93, 0).addBox(0F, 0F, 0F, 2F, 3F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.0F, -10.1F, -1.55F));
        head.addOrReplaceChild("ab_crest_lo", CubeListBuilder.create()
            .texOffs(0, 15).addBox(0F, 0F, 0F, 8F, 2F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.4F, -12.9F, -0.8F));
        head.addOrReplaceChild("ab_crest_hi", CubeListBuilder.create()
            .texOffs(40, 15).addBox(0F, 0F, 0F, 7F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.5F, -14.3F, -0.65F));

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
