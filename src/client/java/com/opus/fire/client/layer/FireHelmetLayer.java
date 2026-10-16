package com.opus.fire.client.layer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.opus.fire.client.model.FireHelmetModel;
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
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;

/**
 * Vein Crust helm: closed columnar-basalt bowl with a narrow magma visor.
 * Second pass renders the pixel-aligned emissive atlas (visor interior).
 */
public class FireHelmetLayer<T extends LivingEntity, M extends HumanoidModel<T>> extends RenderLayer<T, M> {

    private static final ResourceLocation BASE =
        new ResourceLocation("opusvsexe:textures/fire/armor/fire_helmet_layer.png");
    private static final ResourceLocation EMISSIVE =
        new ResourceLocation("opusvsexe:textures/fire/armor/fire_helmet_layer_emissive.png");

    private final FireHelmetModel<T> model;

    public FireHelmetLayer(RenderLayerParent<T, M> parent, FireHelmetModel<T> model) {
        super(parent);
        this.model = model;
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffers, int light, T entity, float limbSwing,
                       float limbAmount, float partialTick, float age, float yaw, float pitch) {
        ItemStack stack = entity.getItemBySlot(EquipmentSlot.HEAD);
        if (!(stack.getItem() instanceof ArmorItem) || stack.getItem() != FireItems.FIRE_HELMET) return;

        model.head().copyFrom(getParentModel().head);
        model.head().visible = true;

        VertexConsumer base = buffers.getBuffer(RenderType.entityCutoutNoCull(BASE));
        model.renderToBuffer(poseStack, base, light, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
        VertexConsumer glow = buffers.getBuffer(RenderType.entityTranslucentEmissive(EMISSIVE));
        model.renderToBuffer(poseStack, glow, LightTexture.FULL_BRIGHT, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
    }
}
