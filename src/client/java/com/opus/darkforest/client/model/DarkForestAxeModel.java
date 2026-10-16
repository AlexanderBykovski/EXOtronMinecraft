package com.opus.darkforest.client.model;

import com.opus.darkforest.DarkForestLine;
import com.opus.darkforest.item.DarkForestAxeItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;

import java.util.HashMap;
import java.util.Map;

/** Client triggers for the Dark Forest Axe (render thread only, M4/M5). */
public final class DarkForestAxeModel extends GeoModel<DarkForestAxeItem> {
    private static final ResourceLocation GEO = DarkForestLine.id("geo/dark_forest/tool_axe.geo.json");
    private static final ResourceLocation TEXTURE = DarkForestLine.id("textures/dark_forest/item/axe.png");
    private static final ResourceLocation ANIMATION =
        DarkForestLine.id("animations/dark_forest/tool_axe.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(DarkForestAxeItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(DarkForestAxeItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(DarkForestAxeItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(DarkForestAxeItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(DarkForestAxeItem animatable, long instanceId,
                                    AnimationState<DarkForestAxeItem> state) {
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
            animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(DarkForestAxeItem.CONTROLLER_MAIN,
                    DarkForestAxeItem.ANIM_ATTACK);
            player.playSound(ModSounds.KATANA_SWING, 0.45F, 0.55F);
            Vec3 look = player.getLookAngle();
            Vec3 eye = player.getEyePosition();
            for (int i = 1; i <= 7; i++) {
                double t = i * 0.22;
                minecraft.level.addParticle(ParticleTypes.WITCH,
                    eye.x + look.x * t, eye.y + look.y * t, eye.z + look.z * t,
                    -look.x * 0.12, -look.y * 0.12, -look.z * 0.12);
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
                        .tryTriggerAnimation(DarkForestAxeItem.CONTROLLER_MAIN,
                            DarkForestAxeItem.ANIM_EQUIP);
                }
            }
        }
    }
}
