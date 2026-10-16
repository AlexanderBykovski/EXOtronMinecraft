package com.opus.opus.item;

import com.opus.entity.KatanaSlashEntity;
import com.opus.registry.ModItems;
import com.opus.sound.ModSounds;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
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
 * Opus katanas (registry ids {@code katana_op}, {@code katana_gold},
 * {@code katana_refined}) as GeckoLib 3D items.
 *
 * <p>Gameplay is preserved 1:1 from the old {@code KatanaItem}: same tier,
 * stats and RMB behavior (OPUS forward slash / GOLD ground wave / REFINED
 * 12-blade ring via {@link KatanaSlashEntity}), same cooldowns, same
 * tooltips. Only the visuals (geo/anim/texture) are new.
 */
public final class OpusKatanaItem extends SwordItem implements GeoAnimatable {
    public enum Kind { OPUS, GOLD, REFINED }

    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_ATTACK_ALT = "attack_alt";
    public static final String ANIM_CAST = "special_cast";
    public static final String ANIM_PULSE = "energy_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation ATTACK_ALT = RawAnimation.begin().thenPlay(ANIM_ATTACK_ALT);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation PULSE = RawAnimation.begin().thenLoop(ANIM_PULSE);

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final Kind kind;

    public OpusKatanaItem(Tier tier, int attackDamage, float attackSpeed, Properties properties, Kind kind) {
        super(tier, attackDamage, attackSpeed, properties);
        this.kind = kind;
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    public Kind kind() {
        return kind;
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<OpusKatanaItem> main =
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
        attacker.level().playSound(null, target.blockPosition(), ModSounds.KATANA_HIT, SoundSource.PLAYERS, 1.0f, 1.0f);
        return true;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.fail(stack);
        }
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }

        Vec3 look = player.getLookAngle();
        if (stack.is(ModItems.KATANA_OP)) {
            Vec3 origin = player.getEyePosition().add(look.scale(1.2D)).add(0.0D, -0.55D, 0.0D);
                KatanaSlashEntity.spawn(player, KatanaSlashEntity.OPUS, origin, look, 20.0F, 24);
            player.getCooldowns().addCooldown(this, 50);
        } else if (stack.is(ModItems.KATANA_GOLD)) {
            Vec3 horizontal = new Vec3(look.x, 0.0D, look.z);
            if (horizontal.lengthSqr() < 0.01D) {
                horizontal = new Vec3(0.0D, 0.0D, 1.0D);
            }
            Vec3 origin = player.position().add(horizontal.normalize().scale(1.25D)).add(0.0D, 0.12D, 0.0D);
                KatanaSlashEntity.spawn(player, KatanaSlashEntity.GOLD, origin, horizontal, 18.0F, 22);
            player.getCooldowns().addCooldown(this, 100);
        } else {
            Vec3 origin = player.getEyePosition().add(0.0D, -0.6D, 0.0D);
            for (int i = 0; i < 12; i++) {
                double angle = Math.PI * 2.0D * i / 12.0D;
                Vec3 direction = new Vec3(Math.sin(angle), 0.03D, Math.cos(angle));
                KatanaSlashEntity.spawn(player, KatanaSlashEntity.REFINED,
                        origin.add(direction.scale(0.9D)), direction, 12.0F, 14);
            }
            player.getCooldowns().addCooldown(this, 120);
        }
        level.playSound(null, player.blockPosition(), ModSounds.KATANA_ULTIMATE,
                SoundSource.PLAYERS, 1.0F, stack.is(ModItems.KATANA_GOLD) ? 1.3F : 0.85F);
        if (level instanceof ServerLevel serverLevel) {
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        }
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
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel),
            (serverLevel.getGameTime() & 1L) == 0L ? ANIM_ATTACK : ANIM_ATTACK_ALT);
        level.playSound(null, player.blockPosition(), ModSounds.KATANA_SWING, SoundSource.PLAYERS, 0.7f, 1.0f);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.opusvsexe.katana_lore").withStyle(ChatFormatting.DARK_PURPLE));
        String ability = stack.is(ModItems.KATANA_OP) ? "katana_op"
                : stack.is(ModItems.KATANA_GOLD) ? "katana_gold" : "katana_refined";
        tooltip.add(Component.translatable("item.opusvsexe." + ability + ".ability").withStyle(ChatFormatting.GOLD));
    }
}
