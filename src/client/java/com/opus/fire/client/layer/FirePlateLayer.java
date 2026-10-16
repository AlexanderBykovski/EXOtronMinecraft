package com.opus.fire.client.layer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.fire.client.model.FirePlateModel;
import com.opus.fire.registry.FireItems;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;

/**
 * Vein Crust cuirass, gauntlets, hip plates, greaves and boots. Base pass uses
 * entityCutoutNoCull; a second full-bright pass renders the pixel-aligned
 * emissive atlas (sternum core, column cracks, joint seams, sole seams).
 */
public class FirePlateLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/fire/armor/fire_plate.png");
    private static final ResourceLocation EMISSIVE =
        new ResourceLocation("opusvsexe:textures/fire/armor/fire_plate_emissive.png");

    private final FirePlateModel<T> model;

    public FirePlateLayer(RenderLayerParent<T, M> parent, FirePlateModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        boolean chest = entity.getItemBySlot(EquipmentSlot.CHEST).is(FireItems.FIRE_CHESTPLATE);
        boolean legs = entity.getItemBySlot(EquipmentSlot.LEGS).is(FireItems.FIRE_LEGGINGS);
        boolean boots = entity.getItemBySlot(EquipmentSlot.FEET).is(FireItems.FIRE_BOOTS);
        if (!chest && !legs && !boots) return;

        model.body().copyFrom(getParentModel().body);
        model.rightArm().copyFrom(getParentModel().rightArm);
        model.leftArm().copyFrom(getParentModel().leftArm);
        model.rightLeg().copyFrom(getParentModel().rightLeg);
        model.leftLeg().copyFrom(getParentModel().leftLeg);
        model.shoulderLeft().copyFrom(getParentModel().leftArm);
        model.shoulderRight().copyFrom(getParentModel().rightArm);
        model.setPieces(false, chest, legs, boots);

        VertexConsumer base = buffers.getBuffer(RenderType.entityCutoutNoCull(BASE));
        model.renderToBuffer(poseStack, base, light, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
        VertexConsumer glow = buffers.getBuffer(RenderType.entityTranslucentEmissive(EMISSIVE));
        model.renderToBuffer(poseStack, glow, LightTexture.FULL_BRIGHT, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
    }
}
