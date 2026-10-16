package com.opus.darkforest.client.model;

import com.opus.darkforest.DarkForestLine;
import com.opus.darkforest.item.DarkForestHoeItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.HitResult;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;

import java.util.HashMap;
import java.util.Map;

/** Client triggers for the Dark Forest Hoe (render thread only, M4/M5). */
public final class DarkForestHoeModel extends GeoModel<DarkForestHoeItem> {
    private static final ResourceLocation GEO = DarkForestLine.id("geo/dark_forest/tool_hoe.geo.json");
    private static final ResourceLocation TEXTURE = DarkForestLine.id("textures/dark_forest/item/hoe.png");
    private static final ResourceLocation ANIMATION =
        DarkForestLine.id("animations/dark_forest/tool_hoe.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(DarkForestHoeItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(DarkForestHoeItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(DarkForestHoeItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(DarkForestHoeItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(DarkForestHoeItem animatable, long instanceId,
                                    AnimationState<DarkForestHoeItem> state) {
        super.setCustomAnimations(animatable, instanceId, state);
        Minecraft minecraft = Minecraft.getInstance();
        LocalPlayer player = minecraft.player;
        if (player == null || minecraft.level == null) {
            return;
        }
        ItemStack stack = state.getData(DataTickets.ITEMSTACK);
        if (stack == null || stack.isEmpty()) {
            return;
        }
        boolean held = player.getMainHandItem() == stack || player.getOffhandItem() == stack;

        float swing = player.getAttackAnim(state.getPartialTick());
        float previous = lastAttackAnim.getOrDefault(instanceId, 0.0F);
        lastAttackAnim.put(instanceId, swing);
        if (lastAttackAnim.size() > 256) {
            lastAttackAnim.clear();
            lastAttackAnim.put(instanceId, swing);
        }
        if (held && previous <= SWING_THRESHOLD && swing > SWING_THRESHOLD
                && instanceId != Long.MAX_VALUE) {
            HitResult cross = minecraft.hitResult;
            boolean onEntity = cross != null && cross.getType() == HitResult.Type.ENTITY;
            animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(DarkForestHoeItem.CONTROLLER_MAIN,
                    onEntity ? DarkForestHoeItem.ANIM_ATTACK : DarkForestHoeItem.ANIM_TILL);
            player.playSound(ModSounds.KATANA_SWING, 0.4F, 0.75F);
        }

        ItemDisplayContext perspective = state.getData(DataTickets.ITEM_RENDER_PERSPECTIVE);
        boolean firstPerson = perspective == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND
            || perspective == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
        if (firstPerson && held) {
            int selected = player.getInventory().selected;
            if (lastFirstPersonStack != stack || selected != lastSelectedSlot) {
                lastFirstPersonStack = stack;
                lastSelectedSlot = selected;
                if (instanceId != Long.MAX_VALUE) {
                    animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                        .tryTriggerAnimation(DarkForestHoeItem.CONTROLLER_MAIN,
                            DarkForestHoeItem.ANIM_EQUIP);
                }
            }
        }
    }
}
