package com.opus.paradise.client.model;

import com.opus.paradise.ParadiseLine;
import com.opus.paradise.item.ParthenonPickaxeItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
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
import net.minecraft.client.renderer.RenderType;

import java.util.HashMap;
import java.util.Map;

/**
 * Client model for the Parthenon Pickaxe. Render-thread-only triggers
 * (M4/M5): swing rising edge plays {@code mine} when the crosshair is on a
 * block and {@code attack} when it is on an entity; equip fires once per
 * first-person stack/slot; a heavy swing whoosh is pitched for a lighter tool.
 */
public final class ParthenonPickaxeModel extends GeoModel<ParthenonPickaxeItem> {
    private static final ResourceLocation GEO = ParadiseLine.id("geo/paradise/pickaxe.geo.json");
    private static final ResourceLocation TEXTURE = ParadiseLine.id("textures/paradise/item/pickaxe.png");
    private static final ResourceLocation ANIMATION = ParadiseLine.id("animations/paradise/pickaxe.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(ParthenonPickaxeItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(ParthenonPickaxeItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(ParthenonPickaxeItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(ParthenonPickaxeItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(ParthenonPickaxeItem animatable, long instanceId,
                                    AnimationState<ParthenonPickaxeItem> state) {
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
                .tryTriggerAnimation(ParthenonPickaxeItem.CONTROLLER_MAIN,
                    onEntity ? ParthenonPickaxeItem.ANIM_ATTACK : ParthenonPickaxeItem.ANIM_MINE);
            player.playSound(ModSounds.KATANA_SWING, 0.4F, 0.7F);
            if (!onEntity && cross instanceof BlockHitResult block) {
                BlockPos pos = block.getBlockPos();
                for (int i = 0; i < 4; i++) {
                    minecraft.level.addParticle(ParticleTypes.END_ROD,
                        pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5,
                        0.0, 0.06, 0.0);
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
                        .tryTriggerAnimation(ParthenonPickaxeItem.CONTROLLER_MAIN,
                            ParthenonPickaxeItem.ANIM_EQUIP);
                }
            }
        }
    }
}
