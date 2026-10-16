package com.opus.darkforest.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
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
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.tags.FluidTags;
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

/**
 * Dark Forest Sword (registry id {@code dark_forest_sword}).
 *
 * <p>Same tier/stats/tooltip/intrinsic as the tool it replaces
 * (DarkForestToolTier, 3, -2.4F, RARE). RMB ability SHARE BLOOM... SHADOW
 * BLOOM STEP: short server-authoritative forward teleport (max 10) with
 * wall/void/hazard safety, one slash per target along the path plus brief
 * Darkness, cooldown + durability. Instant execution, no lingering state.
 *
 * <p>Plain {@link GeoAnimatable} per project rule M2.
 */
public final class DarkForestSwordItem extends SwordItem implements GeoAnimatable, DarkForestTools.ToolMarker {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_ATTACK_ALT = "attack_alt";
    public static final String ANIM_CAST = "shadowstep_cast";
    public static final String ANIM_GLOOM = "gloom_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation ATTACK_ALT = RawAnimation.begin().thenPlay(ANIM_ATTACK_ALT);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation GLOOM = RawAnimation.begin().thenLoop(ANIM_GLOOM);

    public static final double MAX_TELEPORT_DISTANCE = 10.0;
    public static final int COOLDOWN_TICKS = 120;
    public static final int DURABILITY_COST = 3;
    public static final float SLASH_DAMAGE = 11.0F;
    public static final int DARKNESS_TICKS = 40;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public DarkForestSwordItem(Properties properties) {
        super(DarkForestToolTier.INSTANCE, 7, -2.4F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<DarkForestSwordItem> main =
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
        level.playSound(null, player.blockPosition(), com.opus.sound.ModSounds.HAMMER_HIT,
            SoundSource.PLAYERS, crit ? 0.7F : 0.6F, crit ? 0.9F : 0.8F);
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
        return tryShadowStep(player, stack, hand)
            ? InteractionResultHolder.sidedSuccess(stack, false)
            : InteractionResultHolder.pass(stack);
    }

    private boolean tryShadowStep(Player player, ItemStack stack, InteractionHand hand) {
        if (!(player.level() instanceof ServerLevel level) || player.isSpectator()) {
            return false;
        }
        if (player.getCooldowns().isOnCooldown(this)) {
            return false;
        }
        if (stack.getMaxDamage() > 0 && stack.getDamageValue() + DURABILITY_COST > stack.getMaxDamage()) {
            return false;
        }
        Vec3 look = player.getLookAngle();
        double clampedY = Math.max(-0.5, Math.min(0.35, look.y));
        Vec3 dir = new Vec3(look.x, clampedY, look.z).normalize();
        Vec3 start = player.position();
        Vec3 best = null;
        for (double t = 0.5; t <= MAX_TELEPORT_DISTANCE + 0.001; t += 0.5) {
            Vec3 probe = start.add(dir.scale(t));
            BlockPos feet = BlockPos.containing(probe.x, probe.y, probe.z);
            BlockPos landing = findLanding(level, feet);
            if (landing == null) {
                continue;
            }
            AABB box = player.getBoundingBox().move(
                landing.getX() + 0.5 - start.x, landing.getY() - start.y, landing.getZ() + 0.5 - start.z);
            if (!level.noCollision(player, box)) {
                continue;
            }
            if (!isPathClear(level, player, start, new Vec3(landing.getX() + 0.5, landing.getY(), landing.getZ() + 0.5))) {
                break;
            }
            best = new Vec3(landing.getX() + 0.5, landing.getY(), landing.getZ() + 0.5);
        }
        if (best == null) {
            return false;
        }
        slashPath(level, player, start, best);
        mark(level, start);
        player.teleportTo(best.x, best.y, best.z);
        player.fallDistance = 0.0F;
        mark(level, best);
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, level), ANIM_CAST);
        level.playSound(null, player.blockPosition(), SoundEvents.ENDERMAN_TELEPORT,
            SoundSource.PLAYERS, 0.8F, 0.9F);
        return true;
    }

    /** Highest standable surface at/below feet within a small window, or null. */
    private static BlockPos findLanding(ServerLevel level, BlockPos feet) {
        for (int dy = 2; dy >= -4; dy--) {
            BlockPos at = feet.offset(0, dy, 0);
            if (at.getY() < level.getMinBuildHeight() + 1 || !level.getWorldBorder().isWithinBounds(at)) {
                continue;
            }
            if (!level.isEmptyBlock(at) || !level.isEmptyBlock(at.above())) {
                continue;
            }
            BlockPos below = at.below();
            if (level.isEmptyBlock(below) || !level.getBlockState(below).isSolidRender(level, below)) {
                continue;
            }
            if (isHazard(level, at) || isHazard(level, at.above()) || isHazard(level, below)) {
                continue;
            }
            return at;
        }
        return null;
    }

    private static boolean isHazard(ServerLevel level, BlockPos pos) {
        if (level.getFluidState(pos).is(FluidTags.LAVA)) {
            return true;
        }
        return level.getBlockState(pos).is(Blocks.FIRE) || level.getBlockState(pos).is(Blocks.SOUL_FIRE)
            || level.getBlockState(pos).is(Blocks.CACTUS)
            || level.getBlockState(pos).is(Blocks.POWDER_SNOW);
    }

    /** No solid obstruction between two points (prevents wall-phasing). */
    private static boolean isPathClear(ServerLevel level, Player player, Vec3 from, Vec3 to) {
        Vec3 diff = to.subtract(from);
        double dist = diff.length();
        int steps = Math.max(1, (int) Math.ceil(dist / 0.5));
        AABB box = player.getBoundingBox();
        // Horizontal sweep only: walls span full height, while vertical drops
        // are validated per-candidate by findLanding (prevents wall-phasing
        // without rejecting legitimate descents).
        for (int i = 1; i <= steps; i++) {
            Vec3 at = from.add(diff.scale((double) i / steps));
            AABB moved = box.move(at.x - from.x, 0.0, at.z - from.z);
            if (!level.noCollision(player, moved)) {
                return false;
            }
        }
        return true;
    }

    private void slashPath(ServerLevel level, Player player, Vec3 from, Vec3 to) {
        AABB query = new AABB(from, to).inflate(1.5, 2.0, 1.5);
        for (LivingEntity target : level.getEntitiesOfClass(LivingEntity.class, query, LivingEntity::isAlive)) {
            if (target == player || target.isSpectator()
                    || (target instanceof Player other && (other.isCreative() || !player.canHarmPlayer(other)))) {
                continue;
            }
            if (distanceToSegment(target.position().add(0.0, target.getBbHeight() / 2.0, 0.0), from, to) > 1.0) {
                continue;
            }
            target.hurt(level.damageSources().playerAttack(player), SLASH_DAMAGE);
            if (target.canBeAffected(new MobEffectInstance(MobEffects.DARKNESS, DARKNESS_TICKS, 0))) {
                target.addEffect(new MobEffectInstance(MobEffects.DARKNESS, DARKNESS_TICKS, 0, false, false, true));
            }
        }
        Vec3 mid = from.add(to).scale(0.5);
        level.sendParticles(ParticleTypes.PORTAL, mid.x, mid.y + 1.0, mid.z, 24, 1.0, 1.0, 1.0, 0.1);
        level.sendParticles(ParticleTypes.WITCH, mid.x, mid.y + 1.0, mid.z, 12, 1.0, 0.8, 1.0, 0.05);
    }

    private static void mark(ServerLevel level, Vec3 at) {
        com.opus.darkforest.entity.MossboundAttackEntity mark =
            com.opus.darkforest.registry.DarkForestEntities.MARKED_STEP.create(level);
        if (mark == null) {
            return;
        }
        mark.setVisualOnly(true);
        mark.setPos(at.x, at.y + 0.1, at.z);
        level.addFreshEntity(mark);
    }

    private static double distanceToSegment(Vec3 p, Vec3 a, Vec3 b) {
        Vec3 ab = b.subtract(a);
        double t = Math.max(0.0, Math.min(1.0, p.subtract(a).dot(ab) / Math.max(1e-6, ab.lengthSqr())));
        return p.subtract(a.add(ab.scale(t))).length();
    }
}
