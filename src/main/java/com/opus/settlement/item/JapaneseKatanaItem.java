package com.opus.settlement.item;

import com.opus.sound.ModSounds;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
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
import net.minecraft.world.phys.AABB;
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

public final class JapaneseKatanaItem extends SwordItem implements GeoAnimatable {
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
    private final boolean longBlade;

    public JapaneseKatanaItem(Tier tier, int damage, float speed, boolean longBlade, Properties properties) {
        super(tier, damage, speed, properties);
        this.longBlade = longBlade;
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    public boolean isLongBlade() { return longBlade; }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<JapaneseKatanaItem> main =
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
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) return InteractionResultHolder.fail(stack);
        if (level.isClientSide) {
            fireTrigger(player, GeoItem.getId(stack), ANIM_CAST);
            return InteractionResultHolder.sidedSuccess(stack, true);
        }
        executeTechnique(player);
        player.getCooldowns().addCooldown(this, longBlade ? 80 : 60);
        stack.hurtAndBreak(1, player, user -> user.broadcastBreakEvent(hand == InteractionHand.MAIN_HAND ? EquipmentSlot.MAINHAND : EquipmentSlot.OFFHAND));
        if (level instanceof ServerLevel serverLevel) {
            fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        }
        return InteractionResultHolder.sidedSuccess(stack, false);
    }

    public int executeTechnique(Player player) {
        if (!(player.level() instanceof ServerLevel server)) return 0;
        Vec3 look = player.getLookAngle();
        Vec3 horizontal = new Vec3(look.x, 0, look.z);
        if (horizontal.lengthSqr() < .01D) horizontal = new Vec3(0, 0, 1);
        horizontal = horizontal.normalize();
        double reach = longBlade ? 5.5D : 4.0D;
        Vec3 center = player.position().add(horizontal.scale(reach * .55D)).add(0, 1D, 0);
        AABB sweep = new AABB(center, center).inflate(longBlade ? 2.5D : 1.65D, 1.6D, longBlade ? 2.5D : 1.65D);
        int hits = 0;
        float damage = longBlade ? 14F : 9F;
        for (LivingEntity target : server.getEntitiesOfClass(LivingEntity.class, sweep,
            living -> living != player && living.isAlive() && !player.isAlliedTo(living))) {
            Vec3 relative = target.position().subtract(player.position());
            if (relative.lengthSqr() <= reach * reach && relative.normalize().dot(horizontal) > .20D
                && target.hurt(server.damageSources().playerAttack(player), damage)) {
                target.knockback(longBlade ? 1.1D : .65D, -horizontal.x, -horizontal.z);
                hits++;
            }
        }
        if (!longBlade) player.setDeltaMovement(player.getDeltaMovement().add(horizontal.scale(.95D)));
        server.playSound(null, player.blockPosition(), longBlade ? ModSounds.KATANA_ULTIMATE : ModSounds.KATANA_SWING,
            SoundSource.PLAYERS, 1.1F, longBlade ? .82F : 1.28F);
        int points = longBlade ? 24 : 16;
        for (int i = 0; i < points; i++) {
            double side = (i - points / 2D) / (points / 2D);
            double forward = 1.2D + Math.sqrt(Math.max(0, 1D - side * side)) * reach;
            server.sendParticles(longBlade ? ParticleTypes.CRIT : ParticleTypes.CLOUD,
                player.getX() + horizontal.x * forward + horizontal.z * side * 2.2D,
                player.getY() + 1.0D + Math.cos(side * Math.PI) * 1.1D,
                player.getZ() + horizontal.z * forward - horizontal.x * side * 2.2D,
                1, 0, 0, 0, 0);
        }
        return hits;
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.opusvsexe." + (longBlade ? "long_katana" : "katana") + ".ability")
            .withStyle(longBlade ? ChatFormatting.GOLD : ChatFormatting.GRAY));
    }
}
