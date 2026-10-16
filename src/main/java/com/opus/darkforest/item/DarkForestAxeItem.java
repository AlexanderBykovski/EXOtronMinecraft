package com.opus.darkforest.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ItemStack;
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
 * Dark Forest Axe (registry id {@code dark_forest_axe}).
 *
 * <p>Same tier/stats/tooltip/intrinsic as the tool it replaces
 * (DarkForestToolTier, 5.0F, -3.0F, RARE). RMB ability ROOTSNARE CLEAVE:
 * one press launches an 11-cell thorn-root wave (see
 * {@link DarkForestAxeWave}); damage-once + brief root, server-side.
 */
public final class DarkForestAxeItem extends AxeItem implements GeoAnimatable, DarkForestTools.ToolMarker {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "cleave_cast";
    public static final String ANIM_GLOOM = "gloom_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation GLOOM = RawAnimation.begin().thenLoop(ANIM_GLOOM);

    public static final int COOLDOWN_TICKS = 200;
    public static final int DURABILITY_COST = 5;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public DarkForestAxeItem(Properties properties) {
        super(DarkForestToolTier.INSTANCE, 9.0F, -3.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<DarkForestAxeItem> main =
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
            state -> state.setAndContinue(GLOOM)));
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
        lines.add(Component.translatable("item.opusvsexe.dark_forest_tools.tier").withStyle(ChatFormatting.DARK_PURPLE));
        lines.add(Component.translatable("item.opusvsexe.dark_forest_tools.haste").withStyle(ChatFormatting.GREEN));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
            DarkForestEquipment.applyIntrinsic(stack);
        }
    }

    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        boolean crit = player.fallDistance > 0.0F && !player.onGround() && !player.isInWater();
        Vec3 look = player.getLookAngle();
        serverLevel.sendParticles(ParticleTypes.WITCH,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            crit ? 8 : 5, 0.3, 0.3, 0.3, 0.05);
        serverLevel.sendParticles(ParticleTypes.END_ROD,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            crit ? 8 : 5, 0.25, 0.25, 0.25, 0.04);
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
        if (stack.getMaxDamage() > 0 && stack.getDamageValue() + DURABILITY_COST > stack.getMaxDamage()) {
            return InteractionResultHolder.pass(stack);
        }
        DarkForestAxeWave.start(serverLevel, player);
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        level.playSound(null, player.blockPosition(), SoundEvents.GRASS_BREAK, SoundSource.PLAYERS, 0.9F, 0.7F);
        return InteractionResultHolder.sidedSuccess(stack, false);
    }
}
