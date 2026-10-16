package com.opus.darkforest.item;

import com.opus.darkforest.entity.MossboundAttackEntity;
import com.opus.darkforest.registry.DarkForestEntities;
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
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Rootsnare Cleave wave: an irregular forward ground eruption (11 cells,
 * ~3 wide, +-1 lateral walk) that damages each target once and briefly roots
 * ground-bound victims. One layer per tick; visuals reuse the project's
 * {@link MossboundAttackEntity} ROOT effect in visual-only mode (no new
 * entities); damage is custom and server-authoritative.
 */
public final class DarkForestAxeWave {
    public static final int WAVE_LENGTH = 11;
    public static final int MAX_LATERAL = 1;
    public static final int TICKS_PER_LAYER = 1;
    public static final float WAVE_DAMAGE = 13.0F;
    public static final int ROOT_TICKS = 40;
    public static final int ROOT_AMPLIFIER = 4;

    private static final Map<UUID, Cast> CASTS = new ConcurrentHashMap<>();

    private DarkForestAxeWave() {
    }

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(DarkForestAxeWave::tickAll);
    }

    public static void start(ServerLevel level, Player player) {
        List<BlockPos> path = genPath(level, player);
        if (path.isEmpty()) {
            return;
        }
        Cast cast = new Cast(UUID.randomUUID(), level.dimension(), player.getUUID(), path);
        CASTS.put(cast.id, cast);
    }

    /** Lateral walk in [-1, 1], unit-testable without a world. */
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

    static List<BlockPos> genPath(ServerLevel level, Player player) {
        double yaw = Math.toRadians(player.getYRot());
        double fx = -Math.sin(yaw);
        double fz = Math.cos(yaw);
        double px = player.getX();
        double pz = player.getZ();
        int prevY = player.blockPosition().getY();
        List<Integer> offsets = genOffsets(level.random, WAVE_LENGTH);
        List<BlockPos> cells = new ArrayList<>();
        for (int d = 1; d <= WAVE_LENGTH; d++) {
            int offset = offsets.get(d - 1);
            double x = px + fx * d - fz * offset;
            double z = pz + fz * d + fx * offset;
            BlockPos surface = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING,
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
        return cells;
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
            while (next < cells.size() && next * TICKS_PER_LAYER <= age) {
                erupt(level, player, cells.get(next));
                next++;
            }
            age++;
            return next >= cells.size() && age > cells.size() * TICKS_PER_LAYER + 4;
        }

        private void erupt(ServerLevel level, Player player, BlockPos pos) {
            MossboundAttackEntity root = DarkForestEntities.ROOT_SNARE.create(level);
            if (root != null) {
                root.setVisualOnly(true);
                root.setPos(pos.getX() + 0.5, pos.getY() + 0.1, pos.getZ() + 0.5);
                level.addFreshEntity(root);
            }
            level.sendParticles(ParticleTypes.WITCH,
                pos.getX() + 0.5, pos.getY() + 0.6, pos.getZ() + 0.5, 3, 0.4, 0.3, 0.4, 0.03);
            AABB box = new AABB(pos).inflate(1.2, 1.5, 1.2);
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
                target.hurt(level.damageSources().playerAttack(player), WAVE_DAMAGE);
                boolean grounded = target.onGround() || target instanceof Player;
                if (grounded && target.canBeAffected(
                        new net.minecraft.world.effect.MobEffectInstance(
                            net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, ROOT_TICKS, ROOT_AMPLIFIER))) {
                    target.addEffect(new net.minecraft.world.effect.MobEffectInstance(
                        net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN,
                        ROOT_TICKS, ROOT_AMPLIFIER, false, false, true));
                }
            }
        }
    }
}
