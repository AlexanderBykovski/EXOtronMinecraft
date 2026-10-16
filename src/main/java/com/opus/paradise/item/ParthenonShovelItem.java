package com.opus.paradise.item;

import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
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
 * Parthenon Shovel — the celestial digging relic (registry id {@code parthenon_shovel}).
 *
 * <p>Gameplay parity with the tool it replaces: same {@link ParthenonToolTier},
 * same shovel damage/speed ({@code 1.5F}/{@code -3.0F}), same intrinsic
 * Efficiency application and tooltip. New on top:
 * <ul>
 *   <li>full GeckoLib 3D model with idle/equip/dig/attack/cast/recover;</li>
 *   <li>sneak+RMB keeps vanilla path creation; plain RMB fires the Haste
 *       ability instead (documented resolution of the useOn/use conflict);</li>
 *   <li>RMB ability: Haste LEVEL 255 (amplifier 254, exactly), 200 ticks,
 *       cooldown 400 ticks, durability -2, caster only, server-side.</li>
 * </ul>
 *
 * <p>Rendering follows the project rule (M2): plain {@link GeoAnimatable} +
 * vanilla baked-model path, never {@code GeoItem}.
 */
public final class ParthenonShovelItem extends ShovelItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_DIG = "dig";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "haste_cast";
    public static final String ANIM_RECOVER = "haste_recover";
    public static final String ANIM_GEM_PULSE = "gem_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation DIG = RawAnimation.begin().thenPlay(ANIM_DIG);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation RECOVER = RawAnimation.begin().thenPlay(ANIM_RECOVER);
    private static final RawAnimation GEM_PULSE = RawAnimation.begin().thenLoop(ANIM_GEM_PULSE);

    /** Displayed Haste level 255 == zero-based amplifier 254. NEVER 255. */
    public static final int HASTE_AMPLIFIER = 254;
    public static final int HASTE_DURATION_TICKS = 200;
    public static final int ABILITY_COOLDOWN_TICKS = 400;
    public static final int ABILITY_DURABILITY_COST = 2;
    private static final String TAG_RECOVER_AT = "ParthenonHasteRecoverAt";

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ParthenonShovelItem(Properties properties) {
        super(ParthenonToolTier.INSTANCE, 4.0F, -3.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    /** Rate-limited mining sparkle under extreme Haste (max ~1 per 6 ticks globally). */
    public static void init() {
        PlayerBlockBreakEvents.AFTER.register((world, player, pos, state, blockEntity) -> {
            if (world.isClientSide || world.getGameTime() % 6 != 0) {
                return;
            }
            if (!(player.getMainHandItem().getItem() instanceof ParthenonShovelItem)) {
                return;
            }
            if (world instanceof ServerLevel serverLevel) {
                serverLevel.sendParticles(ParticleTypes.END_ROD,
                    pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5,
                    1, 0.1, 0.1, 0.1, 0.02);
            }
        });
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<ParthenonShovelItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_DIG, DIG);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        main.triggerableAnim(ANIM_CAST, CAST);
        main.triggerableAnim(ANIM_RECOVER, RECOVER);
        controllers.add(main);
        controllers.add(new AnimationController<>(this, CONTROLLER_FX, 5,
            state -> state.setAndContinue(GEM_PULSE)));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object stack) {
        return System.nanoTime() / 50_000_000.0;
    }

    private void fireTrigger(Player player, long instanceId, String anim) {
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
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.efficiency").withStyle(ChatFormatting.AQUA));
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.repair").withStyle(ChatFormatting.DARK_PURPLE));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)
                || !(entity instanceof Player player)) {
            return;
        }
        GeoItem.getOrAssignId(stack, serverLevel);
        ParadiseEquipment.applyIntrinsic(stack);
        long recoverAt = stack.getOrCreateTag().getLong(TAG_RECOVER_AT);
        if (recoverAt > 0 && level.getGameTime() >= recoverAt) {
            stack.getOrCreateTag().remove(TAG_RECOVER_AT);
            fireTrigger(player, GeoItem.getId(stack), ANIM_RECOVER);
        }
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Player player = context.getPlayer();
        if (player != null && player.isShiftKeyDown()) {
            return super.useOn(context);
        }
        return InteractionResult.PASS;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }
        return tryHaste(player, stack, hand)
            ? InteractionResultHolder.sidedSuccess(stack, false)
            : InteractionResultHolder.pass(stack);
    }

    private boolean tryHaste(Player player, ItemStack stack, InteractionHand hand) {
        Level level = player.level();
        if (player.isSpectator() || player.getCooldowns().isOnCooldown(this)) {
            return false;
        }
        if (stack.getMaxDamage() > 0
                && stack.getDamageValue() + ABILITY_DURABILITY_COST > stack.getMaxDamage()) {
            return false;
        }
        player.addEffect(new MobEffectInstance(MobEffects.DIG_SPEED, HASTE_DURATION_TICKS,
            HASTE_AMPLIFIER, false, false, true));
        player.getCooldowns().addCooldown(this, ABILITY_COOLDOWN_TICKS);
        if (!player.isCreative()) {
            stack.hurtAndBreak(ABILITY_DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        if (level instanceof ServerLevel serverLevel) {
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
            stack.getOrCreateTag().putLong(TAG_RECOVER_AT, level.getGameTime() + 10);
            level.playSound(null, player, SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 0.7F, 1.3F);
            double px = player.getX();
            double py = player.getY();
            double pz = player.getZ();
            for (int i = 0; i < 12; i++) {
                double a = i * Math.PI * 2.0 / 12.0;
                serverLevel.sendParticles(ParticleTypes.END_ROD,
                    px + Math.cos(a) * 0.7, py + 0.2, pz + Math.sin(a) * 0.7,
                    1, 0.0, 0.06, 0.0, 0.02);
            }
            serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py + 1.0, pz, 4, 0.3, 0.5, 0.3, 0.05);
        }
        return true;
    }

    /**
     * Server-side entity-hit hook, called from the player attack mixin.
     * Restrained: small flash, few sparks, short ruby pulse. No lightning.
     */
    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        level.playSound(null, player.blockPosition(), com.opus.sound.ModSounds.HAMMER_HIT,
            SoundSource.PLAYERS, 0.5F, 1.0F);
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py, pz, 2, 0.2, 0.2, 0.2, 0.04);
        serverLevel.sendParticles(ParticleTypes.END_ROD, px, py, pz, 4, 0.25, 0.25, 0.25, 0.04);
    }
}
