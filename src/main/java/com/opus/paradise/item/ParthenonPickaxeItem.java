package com.opus.paradise.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.UseAnim;
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
 * Parthenon Pickaxe — the celestial mining relic (registry id {@code parthenon_pickaxe}).
 *
 * <p>Gameplay parity with the tool it replaces: same {@link ParthenonToolTier},
 * same pickaxe damage/speed ({@code 1}/{@code -2.8F}), same intrinsic Efficiency
 * application and tooltip. New on top:
 * <ul>
 *   <li>full GeckoLib 3D model with idle/equip/mine/attack animations;</li>
 *   <li>RMB channel skill "Forge Attunement": while held, and for 10 seconds
 *       after release, grants Night Vision and Haste V (server-authoritative,
 *       refreshed buffs, no new assets).</li>
 * </ul>
 *
 * <p>Rendering follows the project rule (M2): plain {@link GeoAnimatable} +
 * vanilla baked-model path, never {@code GeoItem}.
 */
public final class ParthenonPickaxeItem extends PickaxeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_MINE = "mine";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_GEM_PULSE = "gem_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation MINE = RawAnimation.begin().thenPlay(ANIM_MINE);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation GEM_PULSE = RawAnimation.begin().thenLoop(ANIM_GEM_PULSE);

    private static final String TAG_ATTUNE_LAST = "ParthenonAttuneLast";
    private static final int ATTUNE_TAIL_TICKS = 200;
    private static final int ATTUNE_HASTE_AMPLIFIER = 4;
    private static final int ATTUNE_MIN_CHARGE_TICKS = 10;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ParthenonPickaxeItem(Properties properties) {
        super(ParthenonToolTier.INSTANCE, 4, -2.8F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<ParthenonPickaxeItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_MINE, MINE);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
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
        if (level.isClientSide || !(entity instanceof Player player) || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        GeoItem.getOrAssignId(stack, serverLevel);
        ParadiseEquipment.applyIntrinsic(stack);
        boolean channeling = selected && player.isUsingItem() && player.getUseItem() == stack;
        long now = level.getGameTime();
        if (channeling) {
            applyAttunement(player, 60);
            stack.getOrCreateTag().putLong(TAG_ATTUNE_LAST, now);
            if (now % 10 == 0) {
                serverLevel.sendParticles(ParticleTypes.END_ROD,
                    player.getX(), player.getY() + 1.2, player.getZ(), 4, 0.5, 0.7, 0.5, 0.03);
            }
        } else {
            long last = stack.getOrCreateTag().getLong(TAG_ATTUNE_LAST);
            if (now - last <= ATTUNE_TAIL_TICKS) {
                applyAttunement(player, 40);
            }
        }
    }

    private static void applyAttunement(Player player, int durationTicks) {
        player.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, durationTicks, 0, false, false, true));
        player.addEffect(new MobEffectInstance(MobEffects.DIG_SPEED, durationTicks,
            ATTUNE_HASTE_AMPLIFIER, false, false, true));
    }

    /**
     * Server-side entity-hit hook, called from the player attack mixin.
     */
    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        level.playSound(null, player.blockPosition(), com.opus.sound.ModSounds.HAMMER_HIT,
            SoundSource.PLAYERS, 0.6F, 1.1F);
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        serverLevel.sendParticles(ParticleTypes.END_ROD, px, py, pz, 6, 0.25, 0.25, 0.25, 0.04);
        serverLevel.sendParticles(ParticleTypes.ENCHANT, px, py, pz, 4, 0.3, 0.3, 0.3, 0.1);
    }

    @Override
    public int getUseDuration(ItemStack stack) {
        return 72000;
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BOW;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(player.getItemInHand(hand));
    }

    @Override
    public void releaseUsing(ItemStack stack, Level level, LivingEntity user, int remaining) {
        if (!(user instanceof Player player)) {
            return;
        }
        if (getUseDuration(stack) - remaining < ATTUNE_MIN_CHARGE_TICKS || level.isClientSide) {
            return;
        }
        ServerLevel serverLevel = (ServerLevel) level;
        level.playSound(null, player, SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 0.7F, 1.2F);
        serverLevel.sendParticles(ParticleTypes.END_ROD,
            player.getX(), player.getY() + 1.4, player.getZ(), 16, 0.6, 0.8, 0.6, 0.06);
    }
}
