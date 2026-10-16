package com.opus.paradise.client.model;

import com.opus.paradise.ParadiseLine;
import com.opus.paradise.item.ParthenonXiphosItem;
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
 * Client model for the Parthenon Xiphos. Render-thread-only triggers
 * (M4/M5): successive swings alternate {@code attack}/{@code attack_alt}
 * (both share the 0-0.1s anticipation, so a server trigger landing inside it
 * never snaps); equip fires once per first-person stack/slot.
 */
public final class ParthenonXiphosModel extends GeoModel<ParthenonXiphosItem> {
    private static final ResourceLocation GEO = ParadiseLine.id("geo/paradise/xiphos.geo.json");
    private static final ResourceLocation TEXTURE = ParadiseLine.id("textures/paradise/item/xiphos.png");
    private static final ResourceLocation ANIMATION = ParadiseLine.id("animations/paradise/xiphos.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private final Map<Long, Integer> swingParity = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;

    @Override
    public ResourceLocation getModelResource(ParthenonXiphosItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(ParthenonXiphosItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(ParthenonXiphosItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(ParthenonXiphosItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(ParthenonXiphosItem animatable, long instanceId,
                                    AnimationState<ParthenonXiphosItem> state) {
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
            int parity = (swingParity.getOrDefault(instanceId, 0) + 1) % 2;
            swingParity.put(instanceId, parity);
            animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(ParthenonXiphosItem.CONTROLLER_MAIN,
                    parity == 0 ? ParthenonXiphosItem.ANIM_ATTACK : ParthenonXiphosItem.ANIM_ATTACK_ALT);
            player.playSound(ModSounds.KATANA_SWING, 0.5F, 0.8F);
            if (minecraft.level != null) {
                net.minecraft.world.phys.Vec3 look = player.getLookAngle();
                net.minecraft.world.phys.Vec3 eye = player.getEyePosition();
                for (int i = 1; i <= 6; i++) {
                    double t = i * 0.22;
                    minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.END_ROD,
                        eye.x + look.x * t, eye.y + look.y * t, eye.z + look.z * t,
                        -look.x * 0.12, -look.y * 0.12, -look.z * 0.12);
                }
                minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.FIREWORK,
                    eye.x + look.x * 1.2, eye.y + look.y * 1.2, eye.z + look.z * 1.2,
                    0.0, 0.02, 0.0);
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
                        .tryTriggerAnimation(ParthenonXiphosItem.CONTROLLER_MAIN,
                            ParthenonXiphosItem.ANIM_EQUIP);
                }
            }
        }
    }
}
