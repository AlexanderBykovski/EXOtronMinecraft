package com.opus.fire.item;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * HELLCLEAVER: THREE molten crescent arcs (center + +-40 deg) fanning 10
 * blocks forward. One shared per-cast dedupe set: overlapping arcs never
 * double-hit. Solid terrain stops each arc. Blocks are never broken or burned.
 */
public final class FireAxeFan {
    public static final int FAN_LENGTH = 10;
    public static final double FAN_HALF_ANGLE_DEG = 40.0;
    public static final int MAX_LATERAL = 1;
    public static final int COOLDOWN_TICKS = 160;
    public static final int DURABILITY_COST = 5;
    public static final float FAN_DAMAGE = 13.0F;

    private static final int TICKS_PER_LAYER = 1;

    private static final Map<UUID, Cast> CASTS = new ConcurrentHashMap<>();

    private FireAxeFan() {
    }

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(FireAxeFan::tickAll);
    }

    public static void start(ServerLevel level, Player player) {
        List<BlockPos> cells = genFan(level, player);
        if (cells.isEmpty()) {
            return;
        }
        Cast cast = new Cast(UUID.randomUUID(), level.dimension(), player.getUUID(), cells);
        CASTS.put(cast.id, cast);
    }

    /** Lateral walk in [-1, 1] for one arc, unit-testable without a world. */
    static List<Integer> genOffsets(net.minecraft.util.RandomSource random, int steps) {
        List<Integer> offsets = new ArrayList<>(steps);
        int offset = 0;
        for (int d = 0; d < steps; d++) {
            double roll = random.nextDouble();
            if (roll >= 0.6) {
                offset += roll < 0.8 ? -1 : 1;
            }
            offset = Math.max(-MAX_LATERAL, Math.min(MAX_LATERAL, offset));
            offsets.add(offset);
        }
        return offsets;
    }

    static List<BlockPos> genFan(ServerLevel level, Player player) {
        Set<BlockPos> cells = new LinkedHashSet<>();
        double baseYaw = Math.toRadians(player.getYRot());
        double[] yaws = {baseYaw - Math.toRadians(FAN_HALF_ANGLE_DEG), baseYaw,
            baseYaw + Math.toRadians(FAN_HALF_ANGLE_DEG)};
        for (double yaw : yaws) {
            double fx = -Math.sin(yaw);
            double fz = Math.cos(yaw);
            // lateral frame for this arc
            double rx = -fz;
            double rz = fx;
            double px = player.getX();
            double pz = player.getZ();
            int prevY = player.blockPosition().getY();
            List<Integer> offsets = genOffsets(level.random, FAN_LENGTH);
            for (int d = 1; d <= FAN_LENGTH; d++) {
                int offset = offsets.get(d - 1);
                double x = px + fx * d + rx * offset;
                double z = pz + fz * d + rz * offset;
                BlockPos surface = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                    new BlockPos((int) Math.floor(x), 0, (int) Math.floor(z)));
                if (surface.getY() < level.getMinBuildHeight() + 1
                        || !level.getWorldBorder().isWithinBounds(surface)) {
                    continue;
                }
                if (surface.getY() - prevY > 3) {
                    break;
                }
                prevY = surface.getY();
                cells.add(surface.immutable());
            }
        }
        return new ArrayList<>(cells);
    }

    private static void tickAll(MinecraftServer server) {
        CASTS.values().removeIf(cast -> cast.tick(server));
    }

    private static final class Cast {
        private final UUID id;
        private final ResourceKey<Level> dimension;
        private final UUID caster;
        private final List<BlockPos> cells;
        private final Set<UUID> hit = new HashSet<>();
        private int age;
        private int next;

        private Cast(UUID id, ResourceKey<Level> dimension, UUID caster, List<BlockPos> cells) {
            this.id = id;
            this.dimension = dimension;
            this.caster = caster;
            this.cells = cells;
        }

        private boolean tick(MinecraftServer server) {
            ServerLevel level = server.getLevel(dimension);
            Player player = level == null ? null : server.getPlayerList().getPlayer(caster);
            if (level == null || player == null || !player.isAlive()) {
                return true;
            }
            while (next < cells.size() && next / 3 * TICKS_PER_LAYER <= age) {
                slash(level, player, cells.get(next));
                next++;
            }
            age++;
            return next >= cells.size() && age > cells.size() / 3 * TICKS_PER_LAYER + 4;
        }

        private void slash(ServerLevel level, Player player, BlockPos pos) {
            level.sendParticles(ParticleTypes.FLAME,
                pos.getX() + 0.5, pos.getY() + 0.6, pos.getZ() + 0.5, 4, 0.5, 0.3, 0.5, 0.04);
            level.sendParticles(ParticleTypes.LAVA,
                pos.getX() + 0.5, pos.getY() + 0.6, pos.getZ() + 0.5, 2, 0.4, 0.3, 0.4, 0.0);
            AABB box = new AABB(pos).inflate(1.0, 1.5, 1.0);
            for (LivingEntity target : level.getEntitiesOfClass(LivingEntity.class, box, LivingEntity::isAlive)) {
                if (target.getUUID().equals(caster) || !hit.add(target.getUUID())) {
                    continue;
                }
                if (target instanceof Player other
                        && (other.isCreative() || other.isSpectator() || !player.canHarmPlayer(other))) {
                    continue;
                }
                if (target.isInvulnerable()) {
                    continue;
                }
                target.hurt(level.damageSources().playerAttack(player), FAN_DAMAGE);
                Vec3 push = target.position().subtract(player.position());
                push = new Vec3(push.x, 0.0, push.z).normalize();
                target.push(push.x * 0.3, 0.18, push.z * 0.3);
                level.sendParticles(ParticleTypes.FIREWORK,
                    target.getX(), target.getY() + 1.0, target.getZ(), 3, 0.2, 0.3, 0.2, 0.05);
            }
        }
    }
}
