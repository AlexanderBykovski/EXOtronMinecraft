package com.opus.opus.client.model;

import com.opus.OpusVsExe;
import com.opus.settlement.item.JapaneseKatanaItem;
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

/** Client triggers for the Long Katana (render thread only, M4/M5). */
public final class SettlementLongKatanaModel extends GeoModel<JapaneseKatanaItem> {
    private static final ResourceLocation GEO = OpusVsExe.id("geo/settlement/long_katana.geo.json");
    private static final ResourceLocation TEXTURE = OpusVsExe.id("textures/settlement/item/long_katana.png");
    private static final ResourceLocation ANIMATION = OpusVsExe.id("animations/settlement/long_katana.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;
    private int swingParity = 0;

    @Override
    public ResourceLocation getModelResource(JapaneseKatanaItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(JapaneseKatanaItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(JapaneseKatanaItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(JapaneseKatanaItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(JapaneseKatanaItem animatable, long instanceId,
                                    AnimationState<JapaneseKatanaItem> state) {
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
            swingParity++;
            String next = (swingParity & 1) == 0 ? JapaneseKatanaItem.ANIM_ATTACK : JapaneseKatanaItem.ANIM_ATTACK_ALT;
            animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(JapaneseKatanaItem.CONTROLLER_MAIN, next);
            player.playSound(ModSounds.KATANA_SWING, 0.45F, 1.0F);
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
                        .tryTriggerAnimation(JapaneseKatanaItem.CONTROLLER_MAIN,
                            JapaneseKatanaItem.ANIM_EQUIP);
                }
            }
        }
    }
}
