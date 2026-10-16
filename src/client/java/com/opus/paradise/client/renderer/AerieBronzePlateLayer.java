package com.opus.paradise.client.renderer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.paradise.client.model.AerieBronzePlateModel;
import com.opus.paradise.registry.ParadiseItems;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;

/**
 * Aerie Bronze plate: bronze cuirass, shoulder straps, pteruges, vambraces,
 * greaves and caligae. Fully non-emissive single pass; pteruges/skirt render
 * with chest or leggings.
 */
public class AerieBronzePlateLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/paradise/armor/aerie_bronze_plate.png");

    private final AerieBronzePlateModel<T> model;

    public AerieBronzePlateLayer(RenderLayerParent<T, M> parent, AerieBronzePlateModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        boolean chest = entity.getItemBySlot(EquipmentSlot.CHEST).is(ParadiseItems.AERIE_BRONZE_CHESTPLATE);
        boolean legs = entity.getItemBySlot(EquipmentSlot.LEGS).is(ParadiseItems.AERIE_BRONZE_LEGGINGS);
        boolean boots = entity.getItemBySlot(EquipmentSlot.FEET).is(ParadiseItems.AERIE_BRONZE_BOOTS);
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
    }
}
