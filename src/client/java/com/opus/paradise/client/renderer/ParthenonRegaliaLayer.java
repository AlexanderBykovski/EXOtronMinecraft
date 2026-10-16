package com.opus.paradise.client.renderer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.paradise.client.model.ParthenonRegaliaModel;
import com.opus.paradise.registry.ParadiseItems;
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
 * Parthenon Regalia: pearl chest guard, wide sleeves, six long robe panels and
 * the floating halo. Base cutout pass + full-bright emissive pass (halo edge,
 * chest inset, clasp gem). The halo keeps a slow ceremonial drift.
 */
public final class ParthenonRegaliaLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {
    private static final ResourceLocation TEXTURE =
        new ResourceLocation("opusvsexe:textures/paradise/armor/parthenon_regalia.png");
    private static final ResourceLocation EMISSIVE =
        new ResourceLocation("opusvsexe:textures/paradise/armor/parthenon_regalia_emissive.png");

    private final ParthenonRegaliaModel<T> model;

    public ParthenonRegaliaLayer(RenderLayerParent<T, M> parent, ParthenonRegaliaModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack pose, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        boolean head = entity.getItemBySlot(EquipmentSlot.HEAD).is(ParadiseItems.PARTHENON_HELMET);
        boolean chest = entity.getItemBySlot(EquipmentSlot.CHEST).is(ParadiseItems.PARTHENON_CHESTPLATE);
        boolean legs = entity.getItemBySlot(EquipmentSlot.LEGS).is(ParadiseItems.PARTHENON_LEGGINGS);
        boolean boots = entity.getItemBySlot(EquipmentSlot.FEET).is(ParadiseItems.PARTHENON_BOOTS);
        if (!head && !chest && !legs && !boots) return;

        model.head().copyFrom(getParentModel().head);
        model.body().copyFrom(getParentModel().body);
        model.rightArm().copyFrom(getParentModel().rightArm);
        model.leftArm().copyFrom(getParentModel().leftArm);
        model.rightLeg().copyFrom(getParentModel().rightLeg);
        model.leftLeg().copyFrom(getParentModel().leftLeg);
        model.shoulderLeft().copyFrom(getParentModel().leftArm);
        model.shoulderRight().copyFrom(getParentModel().rightArm);
        model.setPieces(head, chest, legs, boots);
        // slow ceremonial halo drift (invisible unless the headpiece is worn)
        model.halo().yRot = (age + partialTick) * 0.02F;

        VertexConsumer out = buffers.getBuffer(RenderType.entityCutoutNoCull(TEXTURE));
        model.renderToBuffer(pose, out, light, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
        VertexConsumer glow = buffers.getBuffer(RenderType.entityTranslucentEmissive(EMISSIVE));
        model.renderToBuffer(pose, glow, LightTexture.FULL_BRIGHT, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
    }
}
