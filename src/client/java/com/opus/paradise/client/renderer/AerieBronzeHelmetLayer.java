package com.opus.paradise.client.renderer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.paradise.client.model.AerieBronzeHelmetModel;
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
import net.minecraft.world.item.ArmorItem;

/**
 * Aerie Bronze helm: roman bronze bowl with cheek guards and a dark-red
 * transverse crest. Fully non-emissive single pass.
 */
public class AerieBronzeHelmetLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/paradise/armor/aerie_bronze_helmet.png");

    private final AerieBronzeHelmetModel<T> model;

    public AerieBronzeHelmetLayer(RenderLayerParent<T, M> parent, AerieBronzeHelmetModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        if (!(entity.getItemBySlot(EquipmentSlot.HEAD).getItem() instanceof ArmorItem armorItem)
            || armorItem != ParadiseItems.AERIE_BRONZE_HELMET) {
            return;
        }
        model.head().copyFrom(getParentModel().head);
        VertexConsumer base = buffers.getBuffer(RenderType.entityCutoutNoCull(BASE));
        model.renderToBuffer(poseStack, base, light, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
    }
}
