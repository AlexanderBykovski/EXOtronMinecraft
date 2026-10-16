package com.opus.fire.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import com.opus.fire.sound.FireSounds;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.item.enchantment.Enchantments;
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
 * Vein Fire Sword (registry id {@code fire_sword}).
 *
 * <p>Keeps everything the old item did (FireToolTier 3/-2.4F, intrinsic
 * Fire Aspect II, 8s ignite, ability tooltip) and adds the GeckoLib model
 * plus INFERNAL BRAND / DEVIL'S VERDICT on RMB (see
 * {@link FireSwordAbility}). Plain {@link GeoAnimatable} per rule M2.
 */
public final class FireSwordItem extends SwordItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_ATTACK_ALT = "attack_alt";
    public static final String ANIM_CAST = "brand_cast";
    public static final String ANIM_EMBER = "ember_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation ATTACK_ALT = RawAnimation.begin().thenPlay(ANIM_ATTACK_ALT);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation EMBER = RawAnimation.begin().thenLoop(ANIM_EMBER);

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public FireSwordItem(Properties properties) {
        super(FireToolTier.INSTANCE, 7, -2.4F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    private static void ensureFireAspect(ItemStack stack) {
        if (EnchantmentHelper.getItemEnchantmentLevel(Enchantments.FIRE_ASPECT, stack) >= 2) {
            return;
        }
        var enchantments = EnchantmentHelper.getEnchantments(stack);
        enchantments.put(Enchantments.FIRE_ASPECT, 2);
        EnchantmentHelper.setEnchantments(enchantments, stack);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<FireSwordItem> main =
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
        controllers.add(main);
        controllers.add(new AnimationController<>(this, CONTROLLER_FX, 5,
            state -> state.setAndContinue(EMBER)));
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
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide) {
            ensureFireAspect(stack);
            if (level instanceof ServerLevel serverLevel) {
                GeoItem.getOrAssignId(stack, serverLevel);
            }
        }
    }

    @Override
    public void onCraftedBy(ItemStack stack, Level level, Player player) {
        ensureFireAspect(stack);
        super.onCraftedBy(stack, level, player);
    }

    @Override
    public ItemStack getDefaultInstance() {
        ItemStack stack = super.getDefaultInstance();
        ensureFireAspect(stack);
        return stack;
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.setSecondsOnFire(8);
        return super.hurtEnemy(stack, target, attacker);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, level, tooltip, flag);
        tooltip.add(Component.translatable("item.opusvsexe.fire_sword.ability").withStyle(ChatFormatting.GOLD));
        tooltip.add(Component.translatable("item.opusvsexe.fire_sword.brand").withStyle(ChatFormatting.RED));
    }

    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        boolean crit = player.fallDistance > 0.0F && !player.onGround() && !player.isInWater();
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        serverLevel.sendParticles(ParticleTypes.FLAME, px, py, pz, crit ? 8 : 5, 0.25, 0.25, 0.25, 0.04);
        serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py, pz, crit ? 4 : 2, 0.2, 0.2, 0.2, 0.05);
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
                && stack.getDamageValue() + FireSwordAbility.DURABILITY_COST > stack.getMaxDamage()) {
            return InteractionResultHolder.pass(stack);
        }
        if (!FireSwordAbility.start(serverLevel, player)) {
            return InteractionResultHolder.pass(stack);
        }
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, FireSwordAbility.COOLDOWN_TICKS);
            stack.hurtAndBreak(FireSwordAbility.DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        level.playSound(null, player, FireSounds.FIRE_CHARGE, SoundSource.PLAYERS, 0.9F, 0.9F);
        level.playSound(null, player, FireSounds.FIREBALL_LAUNCH, SoundSource.PLAYERS, 0.8F, 0.8F);
        return InteractionResultHolder.sidedSuccess(stack, false);
    }
}
