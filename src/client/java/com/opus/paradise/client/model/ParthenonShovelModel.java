package com.opus.paradise.client.model;

import com.opus.paradise.ParadiseLine;
import com.opus.paradise.item.ParthenonShovelItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;
import net.minecraft.client.renderer.RenderType;

import java.util.HashMap;
import java.util.Map;

/**
 * Client model for the Parthenon Shovel. Render-thread-only triggers
 * (M4/M5): swing edge plays {@code dig} on blocks and {@code attack} on
 * entities; equip fires once per first-person stack/slot. The Haste cast
 * itself is triggered from {@code use()} (both sides), not here.
 */
public final class ParthenonShovelModel extends GeoModel<ParthenonShovelItem> {
    private static final ResourceLocation GEO = ParadiseLine.id("geo/paradise/shovel.geo.json");
    private static final ResourceLocation TEXTURE = ParadiseLine.id("textures/paradise/item/shovel.png");
    private static final ResourceLocation ANIMATION = ParadiseLine.id("animations/paradise/shovel.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(ParthenonShovelItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(ParthenonShovelItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(ParthenonShovelItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(ParthenonShovelItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(ParthenonShovelItem animatable, long instanceId,
                                    AnimationState<ParthenonShovelItem> state) {
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
            net.minecraft.world.phys.HitResult cross = minecraft.hitResult;
            boolean onEntity = cross != null && cross.getType() == net.minecraft.world.phys.HitResult.Type.ENTITY;
            animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(ParthenonShovelItem.CONTROLLER_MAIN,
                    onEntity ? ParthenonShovelItem.ANIM_ATTACK : ParthenonShovelItem.ANIM_DIG);
            player.playSound(ModSounds.KATANA_SWING, 0.45F, 0.65F);
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
                        .tryTriggerAnimation(ParthenonShovelItem.CONTROLLER_MAIN,
                            ParthenonShovelItem.ANIM_EQUIP);
                }
            }
        }
    }
}
