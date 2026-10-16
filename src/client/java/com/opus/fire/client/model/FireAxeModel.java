package com.opus.fire.client.model;

import com.opus.fire.FireLine;
import com.opus.fire.item.FireAxeItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;

import java.util.HashMap;
import java.util.Map;

/** Client triggers for the Vein Fire Axe (render thread only, M4/M5). */
public final class FireAxeModel extends GeoModel<FireAxeItem> {
    private static final ResourceLocation GEO = FireLine.id("geo/fire/tool_axe.geo.json");
    private static final ResourceLocation TEXTURE = FireLine.id("textures/fire/item/axe.png");
    private static final ResourceLocation ANIMATION =
        FireLine.id("animations/fire/tool_axe.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(FireAxeItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(FireAxeItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(FireAxeItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(FireAxeItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(FireAxeItem animatable, long instanceId,
                                    AnimationState<FireAxeItem> state) {
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
                .tryTriggerAnimation(FireAxeItem.CONTROLLER_MAIN,
                    FireAxeItem.ANIM_ATTACK);
            player.playSound(ModSounds.KATANA_SWING, 0.45F, 0.55F);
            net.minecraft.world.phys.Vec3 look = player.getLookAngle();
            net.minecraft.world.phys.Vec3 eye = player.getEyePosition();
            for (int i = 1; i <= 6; i++) {
                double t = i * 0.22;
                minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.WITCH,
                    eye.x + look.x * t, eye.y + look.y * t, eye.z + look.z * t,
                    -look.x * 0.1, -look.y * 0.1, -look.z * 0.1);
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
                        .tryTriggerAnimation(FireAxeItem.CONTROLLER_MAIN,
                            FireAxeItem.ANIM_EQUIP);
                }
            }
        }
    }
}
