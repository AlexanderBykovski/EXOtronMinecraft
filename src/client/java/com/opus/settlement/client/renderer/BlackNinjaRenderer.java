package com.opus.settlement.client.renderer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.opus.settlement.SettlementLine;
import com.opus.settlement.client.model.WarriorPlayerModel;
import com.opus.settlement.entity.BlackNinjaEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.client.renderer.entity.layers.ItemInHandLayer;
import net.minecraft.resources.ResourceLocation;

/**
 * Black Ninja on the regular player rig (same proportions/animation as a player
 * skin, vanilla attack timing); the short sword is a real held item rendered by
 * ItemInHandLayer with the stock player pose.
 */
public final class BlackNinjaRenderer extends HumanoidMobRenderer<BlackNinjaEntity, WarriorPlayerModel<BlackNinjaEntity>> {
    private static final ResourceLocation TEXTURE = SettlementLine.id("textures/entity/japanese/black_ninja.png");

    public BlackNinjaRenderer(EntityRendererProvider.Context context) {
        super(context, new WarriorPlayerModel<>(context.bakeLayer(WarriorPlayerModel.BLACK_NINJA_LAYER)), 0.5F);
        addLayer(new ItemInHandLayer<>(this, context.getItemInHandRenderer()));
        shadowRadius = 0.55F; // light, stealthy silhouette
    }

    @Override
    protected void scale(BlackNinjaEntity entity, PoseStack poseStack, float partialTick) {
        poseStack.scale(1.0F, 1.0F, 1.0F);
    }

    @Override
    public ResourceLocation getTextureLocation(BlackNinjaEntity entity) {
        return TEXTURE;
    }
}
