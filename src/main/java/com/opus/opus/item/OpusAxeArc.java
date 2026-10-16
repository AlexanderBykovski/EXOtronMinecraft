package com.opus.opus.item;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * CROSSCUT ARC: a short-range blue crescent arc forward. Hits valid enemies
 * in front of the player in a controlled corridor, one clean damage instance
 * per target, slight knockback. No terrain destruction. Server-side, bounded.
 */
public final class OpusAxeArc {
    public static final double LENGTH = 12.0;
    public static final double HALF_WIDTH = 2.0;
    public static final double HALF_HEIGHT = 2.5;
    public static final float DAMAGE = 14.0F;
    public static final int COOLDOWN_TICKS = 100;
    public static final int DURABILITY_COST = 2;

    private OpusAxeArc() {
    }

    public static int strike(ServerLevel level, Player player) {
        Vec3 look = player.getLookAngle();
        Vec3 forward = new Vec3(look.x, 0.0, look.z);
        if (forward.lengthSqr() < 0.01) {
            forward = new Vec3(0.0, 0.0, 1.0);
        }
        forward = forward.normalize();
        Vec3 origin = player.position().add(0.0, 1.0, 0.0);
        Vec3 right = new Vec3(-forward.z, 0.0, forward.x);

        Set<UUID> hit = new HashSet<>();
        int hits = 0;
        for (LivingEntity target : level.getEntitiesOfClass(LivingEntity.class,
                player.getBoundingBox().inflate(LENGTH, HALF_HEIGHT + 2.0, LENGTH),
                LivingEntity::isAlive)) {
            if (target == player || !hit.add(target.getUUID()) || player.isAlliedTo(target)) {
                continue;
            }
            if (target instanceof Player other
                    && (other.isCreative() || other.isSpectator() || !player.canHarmPlayer(other))) {
                continue;
            }
            if (target.isInvulnerable()) {
                continue;
            }
            Vec3 to = target.position().add(0.0, 1.0, 0.0).subtract(origin);
            double along = to.dot(forward);
            if (along < 1.0 || along > LENGTH) {
                continue;
            }
            double lateral = Math.abs(to.dot(right));
            if (lateral > HALF_WIDTH + along * 0.08) {
                continue;
            }
            if (Math.abs(to.y) > HALF_HEIGHT) {
                continue;
            }
            Vec3 eye = player.getEyePosition();
            Vec3 targetEye = new Vec3(target.getX(), target.getY() + 1.0, target.getZ());
            if (level.clip(new ClipContext(eye, targetEye, ClipContext.Block.COLLIDER,
                    ClipContext.Fluid.NONE, player)).getType() != HitResult.Type.MISS) {
                continue;
            }
            if (target.hurt(level.damageSources().playerAttack(player), DAMAGE)) {
                Vec3 push = new Vec3(forward.x, 0.0, forward.z).normalize();
                target.push(push.x * 0.6, 0.15, push.z * 0.6);
                level.sendParticles(ParticleTypes.ELECTRIC_SPARK,
                    target.getX(), target.getY() + 1.0, target.getZ(), 5, 0.25, 0.35, 0.25, 0.06);
                hits++;
            }
        }
        for (int i = 1; i <= (int) LENGTH; i++) {
            Vec3 p = origin.add(forward.scale(i));
            level.sendParticles(ParticleTypes.END_ROD,
                p.x, p.y, p.z, 2, 0.35, 0.25, 0.35, 0.02);
        }
        return hits;
    }

    public static void sound(Level level, Player player, net.minecraft.sounds.SoundEvent event) {
        level.playSound(null, player.blockPosition(), event, SoundSource.PLAYERS, 0.9F, 1.1F);
    }
}
