package com.opus.paradise.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
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
 * Parthenon Xiphos — the celestial lightning sword (registry id {@code parthenon_sword}).
 *
 * <p>Gameplay parity with the tool it replaces: same {@link ParthenonToolTier},
 * same sword damage/speed ({@code 3}/{@code -2.4F}), same tooltip, plus an
 * ability tooltip. New on top:
 * <ul>
 *   <li>full GeckoLib 3D model with idle/equip/attack/attack_alt/cast/recover;</li>
 *   <li>RMB single-press ability "Celestial Path" (see {@link ParadiseSwordAbility}):
 *       a jagged 25-block triple-lightning wave. Server-authoritative.</li>
 * </ul>
 *
 * <p>Rendering follows the project rule (M2): plain {@link GeoAnimatable} +
 * vanilla baked-model path, never {@code GeoItem}.
 */
public final class ParthenonXiphosItem extends SwordItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_ATTACK_ALT = "attack_alt";
    public static final String ANIM_CAST = "lightning_cast";
    public static final String ANIM_RECOVER = "lightning_recover";
    public static final String ANIM_GEM_PULSE = "gem_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation ATTACK_ALT = RawAnimation.begin().thenPlay(ANIM_ATTACK_ALT);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation RECOVER = RawAnimation.begin().thenPlay(ANIM_RECOVER);
    private static final RawAnimation GEM_PULSE = RawAnimation.begin().thenLoop(ANIM_GEM_PULSE);

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ParthenonXiphosItem(Properties properties) {
        super(ParthenonToolTier.INSTANCE, 7, -2.4F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<ParthenonXiphosItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        main.triggerableAnim(ANIM_ATTACK_ALT, ATTACK_ALT);
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

    /** Cast/recover hooks for {@link ParadiseSwordAbility} (server side). */
    public void playCastAnim(Player player, ItemStack stack) {
        if (player.level() instanceof ServerLevel serverLevel) {
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        }
    }

    public void playRecoverAnim(Player player, ItemStack stack) {
        if (player.level() instanceof ServerLevel serverLevel) {
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_RECOVER);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> lines, TooltipFlag flag) {
        super.appendHoverText(stack, level, lines, flag);
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.tier").withStyle(ChatFormatting.AQUA));
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.repair").withStyle(ChatFormatting.DARK_PURPLE));
        lines.add(Component.translatable("item.opusvsexe.parthenon_sword.ability").withStyle(ChatFormatting.GOLD));
        lines.add(Component.translatable("item.opusvsexe.parthenon_sword.cooldown").withStyle(ChatFormatting.GRAY));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
        }
    }

    /**
     * Server-side entity-hit hook, called from the player attack mixin.
     * Visual only: compact flash, directional gold sparks, few crimson motes.
     */
    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        boolean crit = player.fallDistance > 0.0F && !player.onGround() && !player.isInWater();
        level.playSound(null, player.blockPosition(), com.opus.sound.ModSounds.HAMMER_HIT,
            SoundSource.PLAYERS, crit ? 0.8F : 0.7F, crit ? 1.0F : 0.9F);
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py, pz, crit ? 5 : 3, 0.2, 0.2, 0.2, 0.05);
        serverLevel.sendParticles(ParticleTypes.END_ROD, px, py, pz, crit ? 9 : 6, 0.25, 0.25, 0.25, 0.04);
        serverLevel.sendParticles(ParticleTypes.ENCHANT, px, py, pz, crit ? 4 : 2, 0.3, 0.3, 0.3, 0.1);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }
        boolean cast = ParadiseSwordAbility.tryCast(player, stack, hand, this);
        return cast ? InteractionResultHolder.sidedSuccess(stack, false)
            : InteractionResultHolder.pass(stack);
    }
}
