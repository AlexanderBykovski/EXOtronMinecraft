package com.opus.ember.client.layer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.ember.client.model.FireDemonicHelmetModel;
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
import net.minecraft.world.item.ArmorItem;

/**
 * Fire Demonic horned helmet: blackened volcanic base pass + full-bright emissive
 * pass (visor slit, horn cracks) rendered from the aligned emissive atlas.
 */
public class FireDemonicHelmetLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/ember/armor/fire_demonic_helmet_layer.png");
    private static final ResourceLocation EMISSIVE =
        new ResourceLocation("opusvsexe:textures/ember/armor/fire_demonic_helmet_layer_emissive.png");

    private final FireDemonicHelmetModel<T> helmModel;

    public FireDemonicHelmetLayer(RenderLayerParent<T, M> parent, FireDemonicHelmetModel<T> helmModel) {
        super(parent);
        this.helmModel = helmModel;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffer, int packedLight, T entity,
                       float limbSwing, float limbSwingAmount, float partialTick, float ageInTicks,
                       float netHeadYaw, float headPitch) {
        if (!(entity.getItemBySlot(EquipmentSlot.HEAD).getItem() instanceof ArmorItem armorItem)
            || armorItem != EmberItems.FIRE_DEMONIC_HELMET) {
            return;
        }
        this.helmModel.head().copyFrom(this.getParentModel().head);
        VertexConsumer base = buffer.getBuffer(RenderType.entityCutoutNoCull(BASE));
        this.helmModel.renderToBuffer(poseStack, base, packedLight, OverlayTexture.NO_OVERLAY,
            1.0F, 1.0F, 1.0F, 1.0F);
        VertexConsumer glow = buffer.getBuffer(RenderType.entityTranslucentEmissive(EMISSIVE));
        this.helmModel.renderToBuffer(poseStack, glow, LightTexture.FULL_BRIGHT, OverlayTexture.NO_OVERLAY,
            1.0F, 1.0F, 1.0F, 1.0F);
    }
}
