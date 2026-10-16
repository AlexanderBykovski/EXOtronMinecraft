package com.opus.opus.item;

import com.opus.item.CombatEffects;
import com.opus.sound.ModSounds;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
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
 * Opus Warhammer (registry id {@code opus_warhammer}) as a GeckoLib 3D item.
 *
 * <p>Same tier as before (ModTier.OPUS, -3.2F speed). RMB SHOCKWAVE:
 * circular ground slam (radius 6, 24 damage, launch) plus a slowing effect
 * on valid nearby enemies, per the master prompt. Ground-based, controlled,
 * never destroys terrain.
 */
public final class OpusWarhammerItem extends SwordItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "slam_cast";
    public static final String ANIM_PULSE = "energy_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation PULSE = RawAnimation.begin().thenLoop(ANIM_PULSE);

    public static final double SHOCKWAVE_RADIUS = 6.0;
    public static final float SHOCKWAVE_DAMAGE = 24.0F;
    public static final int COOLDOWN_TICKS = 100;
    private static final int SLOW_DURATION_TICKS = 100;
    private static final int SLOW_AMPLIFIER = 1;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public OpusWarhammerItem(Tier tier, int attackDamage, float attackSpeed, Properties properties) {
        super(tier, attackDamage, attackSpeed, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<OpusWarhammerItem> main =
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
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        stack.hurtAndBreak(1, attacker, e -> e.broadcastBreakEvent(EquipmentSlot.MAINHAND));
        target.knockback(1.3, attacker.getX() - target.getX(), attacker.getZ() - target.getZ());
        attacker.level().playSound(null, target.blockPosition(), ModSounds.HAMMER_HIT, SoundSource.PLAYERS, 0.9f, 0.8f);
        return true;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }
        if (player.getCooldowns().isOnCooldown(this) || player.isSpectator()
                || !(level instanceof ServerLevel server)) {
            return InteractionResultHolder.pass(stack);
        }
        CombatEffects.shockwave(player, SHOCKWAVE_RADIUS, SHOCKWAVE_DAMAGE, 2.8, true);
        for (LivingEntity target : level.getEntitiesOfClass(LivingEntity.class,
                player.getBoundingBox().inflate(SHOCKWAVE_RADIUS, 3.0, SHOCKWAVE_RADIUS),
                e -> e != player && e.isAlive() && !player.isAlliedTo(e))) {
            target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, SLOW_DURATION_TICKS, SLOW_AMPLIFIER));
        }
        server.sendParticles(ParticleTypes.END_ROD,
            player.getX(), player.getY() + 0.4, player.getZ(), 40, 2.0, 0.5, 2.0, 0.08);
        level.playSound(null, player.blockPosition(), ModSounds.HAMMER_ULTIMATE, SoundSource.PLAYERS, 1.0f, 0.55f);
        player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        fireTrigger(player, GeoItem.getOrAssignId(stack, server), ANIM_CAST);
        return InteractionResultHolder.sidedSuccess(stack, false);
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
        level.playSound(null, player.blockPosition(), ModSounds.HAMMER_HIT, SoundSource.PLAYERS, 0.7f, 0.7f);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.opusvsexe.hammer_lore").withStyle(ChatFormatting.DARK_PURPLE));
        tooltip.add(Component.translatable("item.opusvsexe.opus_warhammer.ability").withStyle(ChatFormatting.GOLD));
    }
}
