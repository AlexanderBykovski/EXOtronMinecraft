package com.opus.settlement.client.renderer;

import com.mojang.blaze3d.vertex.PoseStack;
import com.opus.settlement.SettlementLine;
import com.opus.settlement.client.model.WarriorPlayerModel;
import com.opus.settlement.entity.SamuraiEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.client.renderer.entity.layers.ItemInHandLayer;
import net.minecraft.resources.ResourceLocation;

/**
 * Red Shogun on the regular player rig: imposing samurai with the same
 * humanoid proportions/animation as a player; the long katana is a real held
 * item rendered by ItemInHandLayer with the stock player pose.
 */
public final class SamuraiRenderer extends HumanoidMobRenderer<SamuraiEntity, WarriorPlayerModel<SamuraiEntity>> {
    private static final ResourceLocation TEXTURE = SettlementLine.id("textures/entity/japanese/samurai.png");

    public SamuraiRenderer(EntityRendererProvider.Context context) {
        super(context, new WarriorPlayerModel<>(context.bakeLayer(WarriorPlayerModel.SAMURAI_LAYER)), 0.85F);
        addLayer(new ItemInHandLayer<>(this, context.getItemInHandRenderer()));
        shadowRadius = 0.85F;
    }

    @Override
    protected void scale(SamuraiEntity entity, PoseStack poseStack, float partialTick) {
        // player-sized rig stretched to the samurai hitbox (2.34 blocks)
        poseStack.scale(1.30F, 1.30F, 1.30F);
    }

    @Override
    public ResourceLocation getTextureLocation(SamuraiEntity entity) {
        return TEXTURE;
    }
}
