package com.opus.entity;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import java.util.List;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * EXO-6 "Extra Laser": a heavy blaster beam scaled up to 2.5x diameter. On top
 * of burning everything in the wider beam, every solid block it touches is
 * blown apart with a TNT-strength explosion — the beam carves terrain as it
 * travels.
 */
public class ExtraLaserBeamEntity extends BlasterBeamEntity {

    /** 2.5x the heavy blaster's 0.5-block diameter. */
    public static final float DIAMETER_BLOCKS = 1.25F;
    public static final float BASE_DAMAGE = 18.0F;
    public static final float EXPLOSION_POWER = 2.0F;
    private static final int MAX_PATH_EXPLOSIONS = 12;

    public ExtraLaserBeamEntity(EntityType<? extends BlasterBeamEntity> entityType, Level level) {
        super(entityType, level);
    }

    @Override
    public void tick() {
        // Base tick handles lifetime discard, the client early return, muzzle
        // particles and the standard (narrow) damage pulse.
        super.tick();
        if (this.level().isClientSide || !this.isAlive()) {
            return;
        }
        if (this.tickCount >= DAMAGE_START_TICK && this.tickCount % DAMAGE_INTERVAL_TICKS == 0) {
            this.damageAndExplode();
        }
    }

    private void damageAndExplode() {
        Vec3 start = this.position();
        Vec3 dir = this.getBeamDirection();
        Vec3 end = start.add(dir.scale(this.getBeamLength()));
        double radius = DIAMETER_BLOCKS / 2.0D + 0.3D;
        AABB beam = new AABB(start, end).inflate(radius);

        UUID shooter = this.getShooterUUID();
        List<LivingEntity> targets = this.level().getEntitiesOfClass(LivingEntity.class, beam,
                entity -> entity.isAlive() && !entity.isSpectator()
                        && (shooter == null || !entity.getUUID().equals(shooter)));
        Player player = shooter != null ? this.level().getPlayerByUUID(shooter) : null;
        DamageSource source = player != null
                ? this.level().damageSources().playerAttack(player)
                : this.level().damageSources().generic();
        for (LivingEntity target : targets) {
            target.hurt(source, BASE_DAMAGE);
        }

        if (this.level() instanceof ServerLevel server) {
            this.explodePath(server, start, end, radius);
        }
    }

    private void explodePath(ServerLevel server, Vec3 start, Vec3 end, double radius) {
        Vec3 path = end.subtract(start);
        double length = path.length();
        if (length < 1.0E-6D) return;
        int samples = Math.min(MAX_PATH_EXPLOSIONS, Math.max(1, (int) Math.ceil(length / 6.0D)));
        int blockRadius = Math.max(1, (int) Math.ceil(radius));
        Set<BlockPos> exploded = new HashSet<>();
        for (int sample = 0; sample < samples; sample++) {
            Vec3 point = start.add(path.scale((sample + 0.5D) / samples));
            BlockPos center = BlockPos.containing(point);
            BlockPos hit = null;
            for (BlockPos candidate : BlockPos.betweenClosed(center.offset(-blockRadius, -blockRadius, -blockRadius),
                    center.offset(blockRadius, blockRadius, blockRadius))) {
                if (!server.hasChunkAt(candidate)) continue;
                BlockState state = server.getBlockState(candidate);
                if (!state.isAir()) {
                    hit = candidate.immutable();
                    break;
                }
            }
            if (hit != null && exploded.add(hit)) {
                server.explode(null, hit.getX() + 0.5D, hit.getY() + 0.5D, hit.getZ() + 0.5D,
                        EXPLOSION_POWER, false, Level.ExplosionInteraction.TNT);
            }
        }
    }
}
