package com.opus.ember.client.layer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.ember.client.model.FireDemonicPlateModel;
import com.opus.ember.registry.EmberItems;
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
 * Fire Demonic cuirass, gauntlets, hip plates, greaves and boots. Base pass uses
 * entityCutoutNoCull; a second full-bright pass renders the pixel-aligned emissive
 * atlas (visor cracks, chest core seam, back/boot vent cores, belt buckle).
 */
public class FireDemonicPlateLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/ember/armor/fire_demonic_plate_layer.png");
    private static final ResourceLocation EMISSIVE =
        new ResourceLocation("opusvsexe:textures/ember/armor/fire_demonic_plate_layer_emissive.png");

    private final FireDemonicPlateModel<T> model;

    public FireDemonicPlateLayer(RenderLayerParent<T, M> parent, FireDemonicPlateModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        boolean chest = entity.getItemBySlot(EquipmentSlot.CHEST).is(EmberItems.FIRE_DEMONIC_CHESTPLATE);
        boolean legs = entity.getItemBySlot(EquipmentSlot.LEGS).is(EmberItems.FIRE_DEMONIC_LEGGINGS);
        boolean boots = entity.getItemBySlot(EquipmentSlot.FEET).is(EmberItems.FIRE_DEMONIC_BOOTS);
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
