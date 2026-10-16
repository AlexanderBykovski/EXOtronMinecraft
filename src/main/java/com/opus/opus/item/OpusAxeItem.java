package com.opus.opus.item;

import com.opus.sound.ModSounds;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import software.bernie.geckolib.animatable.GeoItem;
import software.bernie.geckolib.core.animatable.GeoAnimatable;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.network.GeckoLibNetwork;
import software.bernie.geckolib.network.packet.AnimTriggerPacket;
import software.bernie.geckolib.util.GeckoLibUtil;

import java.util.List;

/**
 * Opus Axe (registry id {@code opus_axe}) as a GeckoLib 3D item.
 *
 * <p>RMB ability CROSSCUT ARC (see {@link OpusAxeArc}): a short-range blue
 * crescent arc forward, one damage instance per valid target, slight
 * knockback, no terrain destruction.
 */
public final class OpusAxeItem extends AxeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "crosscut_cast";
    public static final String ANIM_PULSE = "energy_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation PULSE = RawAnimation.begin().thenLoop(ANIM_PULSE);

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public OpusAxeItem(Tier tier, float attackDamage, float attackSpeed, Properties properties) {
        super(tier, attackDamage, attackSpeed, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<OpusAxeItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        main.triggerableAnim(ANIM_CAST, CAST);
        controllers.add(main);
        controllers.add(new AnimationController<>(this, CONTROLLER_FX, 5,
            state -> state.setAndContinue(PULSE)));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object stack) {
        return System.nanoTime() / 50_000_000.0;
    }

    void fireTrigger(Player player, long instanceId, String anim) {
        if (instanceId == Long.MAX_VALUE) {
            return;
        }
        if (player.level().isClientSide) {
            getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(CONTROLLER_MAIN, anim);
        } else {
            GeckoLibNetwork.sendToTrackingEntityAndSelf(
                new AnimTriggerPacket(getClass().toString(), instanceId, CONTROLLER_MAIN, anim), player);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> lines, TooltipFlag flag) {
        super.appendHoverText(stack, level, lines, flag);
        lines.add(Component.translatable("item.opusvsexe.opus_axe.ability").withStyle(ChatFormatting.GOLD));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
        }
    }

    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        Vec3 look = player.getLookAngle();
        serverLevel.sendParticles(ParticleTypes.END_ROD,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            5, 0.25, 0.25, 0.25, 0.04);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }
        if (!(level instanceof ServerLevel serverLevel) || player.isSpectator()
                || player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.pass(stack);
        }
        if (stack.getMaxDamage() > 0
                && stack.getDamageValue() + OpusAxeArc.DURABILITY_COST > stack.getMaxDamage()) {
            return InteractionResultHolder.pass(stack);
        }
        int hits = OpusAxeArc.strike(serverLevel, player);
        if (hits == 0) {
            // Whiff is still a cast (cheap, no durability waste beyond 0):
            // play the arc visuals + sound, short cooldown only.
            OpusAxeArc.sound(level, player, ModSounds.KATANA_SWING);
            player.getCooldowns().addCooldown(this, 20);
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, false);
        }
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, OpusAxeArc.COOLDOWN_TICKS);
            stack.hurtAndBreak(OpusAxeArc.DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        OpusAxeArc.sound(level, player, ModSounds.KATANA_ULTIMATE);
        return InteractionResultHolder.sidedSuccess(stack, false);
    }
}
