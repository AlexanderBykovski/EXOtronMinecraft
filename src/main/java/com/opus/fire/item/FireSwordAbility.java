package com.opus.fire.item;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import com.opus.fire.sound.FireSounds;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * INFERNAL BRAND / DEVIL'S VERDICT: a broad 3-wide molten wave (~16 forward,
 * terrain-occluded) hits each entity once (5.0) and brands it; after 20 ticks
 * the brand collapses into a compact entity-only eruption (6.0). No fire
 * blocks, no lava, no terrain damage. Server-side, per-cast state.
 */
public final class FireSwordAbility {
    public static final int WAVE_RANGE = 16;
    public static final int WAVE_HALF_WIDTH = 1;
    public static final int COOLDOWN_TICKS = 160;
    public static final int DURABILITY_COST = 4;
    public static final float WAVE_DAMAGE = 8.0F;
    public static final float ERUPT_DAMAGE = 9.0F;
    public static final int ERUPT_DELAY_TICKS = 20;

    private static final int TICKS_PER_LAYER = 1;

    private static final Map<UUID, Cast> CASTS = new ConcurrentHashMap<>();

    private FireSwordAbility() {
    }

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(FireSwordAbility::tickAll);
    }

    public static boolean start(ServerLevel level, Player player) {
        List<BlockPos> path = genPath(level, player);
        if (path.isEmpty()) {
            return false;
        }
        Cast cast = new Cast(UUID.randomUUID(), level.dimension(), player.getUUID(), path);
        CASTS.put(cast.id, cast);
        return true;
    }

    static List<BlockPos> genPath(ServerLevel level, Player player) {
        double yaw = Math.toRadians(player.getYRot());
        double fx = -Math.sin(yaw);
        double fz = Math.cos(yaw);
        double px = player.getX();
        double pz = player.getZ();
        int prevY = player.blockPosition().getY();
        Set<BlockPos> cells = new LinkedHashSet<>();
        for (int d = 1; d <= WAVE_RANGE; d++) {
            boolean walled = false;
            for (int o = -WAVE_HALF_WIDTH; o <= WAVE_HALF_WIDTH; o++) {
                double x = px + fx * d - fz * o;
                double z = pz + fz * d + fx * o;
                BlockPos surface = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                    new BlockPos((int) Math.floor(x), 0, (int) Math.floor(z)));
                if (surface.getY() < level.getMinBuildHeight() + 1
                        || !level.getWorldBorder().isWithinBounds(surface)) {
                    continue;
                }
                if (surface.getY() - prevY > 3) {
                    walled = true;
                    break;
                }
                cells.add(surface.immutable());
            }
            if (walled) {
                break;
            }
            BlockPos mid = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                new BlockPos((int) Math.floor(px + fx * d), 0, (int) Math.floor(pz + fz * d)));
            prevY = mid.getY();
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
        private final List<UUID> branded = new ArrayList<>();
        private int age;
        private int next;
        private boolean erupted;

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
                ignite(level, player, cells.get(next));
                next++;
            }
            if (!erupted && age >= ERUPT_DELAY_TICKS) {
                erupted = true;
                erupt(level, player);
            }
            age++;
            return erupted && next >= cells.size() && age > cells.size() / 3 * TICKS_PER_LAYER + 4;
        }

        private void ignite(ServerLevel level, Player player, BlockPos pos) {
            level.sendParticles(ParticleTypes.FLAME,
                pos.getX() + 0.5, pos.getY() + 0.6, pos.getZ() + 0.5, 5, 0.5, 0.3, 0.5, 0.04);
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
                target.hurt(level.damageSources().playerAttack(player), WAVE_DAMAGE);
                branded.add(target.getUUID());
                level.sendParticles(ParticleTypes.FIREWORK,
                    target.getX(), target.getY() + 1.0, target.getZ(), 3, 0.2, 0.3, 0.2, 0.05);
            }
        }

        private void erupt(ServerLevel level, Player player) {
            boolean any = false;
            for (UUID uuid : branded) {
                if (level.getEntity(uuid) instanceof LivingEntity target && target.isAlive()) {
                    target.hurt(level.damageSources().playerAttack(player), ERUPT_DAMAGE);
                    level.sendParticles(ParticleTypes.FIREWORK,
                        target.getX(), target.getY() + 1.0, target.getZ(), 5, 0.25, 0.4, 0.25, 0.06);
                    level.sendParticles(ParticleTypes.FLAME,
                        target.getX(), target.getY() + 1.0, target.getZ(), 6, 0.3, 0.4, 0.3, 0.05);
                    any = true;
                }
            }
            if (any) {
                level.playSound(null, player.blockPosition(), FireSounds.FIRE_EXPLODE,
                    SoundSource.PLAYERS, 0.6F, 1.0F);
            }
        }
    }
}
