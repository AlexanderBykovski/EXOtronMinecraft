package com.opus.darkforest.client.model;

import com.opus.darkforest.DarkForestLine;
import com.opus.darkforest.item.DarkForestPickaxeItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;

import java.util.HashMap;
import java.util.Map;

/** Client triggers for the Dark Forest Pickaxe (render thread only, M4/M5). */
public final class DarkForestPickaxeModel extends GeoModel<DarkForestPickaxeItem> {
    private static final ResourceLocation GEO = DarkForestLine.id("geo/dark_forest/tool_pickaxe.geo.json");
    private static final ResourceLocation TEXTURE = DarkForestLine.id("textures/dark_forest/item/pickaxe.png");
    private static final ResourceLocation ANIMATION =
        DarkForestLine.id("animations/dark_forest/tool_pickaxe.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(DarkForestPickaxeItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(DarkForestPickaxeItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(DarkForestPickaxeItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(DarkForestPickaxeItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(DarkForestPickaxeItem animatable, long instanceId,
                                    AnimationState<DarkForestPickaxeItem> state) {
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
                .tryTriggerAnimation(DarkForestPickaxeItem.CONTROLLER_MAIN,
                    onEntity ? DarkForestPickaxeItem.ANIM_ATTACK : DarkForestPickaxeItem.ANIM_MINE);
            player.playSound(ModSounds.KATANA_SWING, 0.4F, 0.7F);
            if (!onEntity && cross instanceof BlockHitResult block) {
                BlockPos pos = block.getBlockPos();
                for (int i = 0; i < 3; i++) {
                    minecraft.level.addParticle(ParticleTypes.WITCH,
                        pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, 0.0, 0.05, 0.0);
                }
            }
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
                        .tryTriggerAnimation(DarkForestPickaxeItem.CONTROLLER_MAIN,
                            DarkForestPickaxeItem.ANIM_EQUIP);
                }
            }
        }
    }
}
