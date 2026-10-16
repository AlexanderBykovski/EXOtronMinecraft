package com.opus.paradise.world;

import com.opus.paradise.entity.CloudGrazerEntity;
import com.opus.paradise.entity.ParadiseWyvernEntity;
import com.opus.paradise.entity.SunfinchEntity;
import com.opus.paradise.registry.ParadiseEntities;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;

/**
 * High-frequency ambient Paradise wildlife.  Vanilla creature spawning chooses
 * a height-map surface, which cannot express "stand on a leaf crown" or
 * "fly through the cloud band".  This server-side sampler deliberately does.
 * Tuned for visibility: every player gets an attempt every 2 seconds inside
 * a close ring, flocks/herds are bigger and local caps are generous — the old
 * 1-attempt-per-minute at 52..108 blocks meant players almost never met them.
 */
public final class ParadiseWildlifeSpawner {
    private static final int INTERVAL_TICKS = 40;
    private static final int MIN_RANGE = 20;
    private static final int MAX_RANGE = 80;
    private static final double LOCAL_CAP_RANGE = 96.0D;
    private static final int SUNFINCH_FLOCK = 5;
    private static final int SUNFINCH_CAP = 12;
    private static final int GRAZER_HERD = 3;
    private static final int GRAZER_CAP = 8;

    private ParadiseWildlifeSpawner() { }

    public static void init() {
        ServerTickEvents.END_WORLD_TICK.register(ParadiseWildlifeSpawner::tick);
    }

    private static void tick(Level level) {
        if (!(level instanceof ServerLevel server) || server.dimension() != Level.OVERWORLD
            || server.getGameTime() % INTERVAL_TICKS != 0) return;

        for (ServerPlayer player : server.players()) {
            if (player.isSpectator()) continue;
            trySpawnNear(server, player);
        }
    }

    private static void trySpawnNear(ServerLevel level, ServerPlayer player) {
        RandomSource random = player.getRandom();
        double angle = random.nextDouble() * Math.PI * 2.0D;
        double range = MIN_RANGE + random.nextDouble() * (MAX_RANGE - MIN_RANGE);
        int x = player.getBlockX() + Mth.floor(Math.cos(angle) * range);
        int z = player.getBlockZ() + Mth.floor(Math.sin(angle) * range);
        BlockPos canopy = findCanopy(level, x, z);

        // 2 : 1 : 1 keeps the small songbird as the most recognisable sight,
        // while either of the larger creatures remains a memorable encounter.
        switch (random.nextInt(4)) {
            case 0, 1 -> spawnSunfinch(level, random, x, z, canopy);
            case 2 -> spawnGrazer(level, random, x, z, canopy);
            default -> spawnWyvern(level, random, x, z, canopy);
        }
    }

    private static void spawnSunfinch(ServerLevel level, RandomSource random, int x, int z, BlockPos canopy) {
        // Songbirds gather in small forest flocks, on crowns or in the air above them.
        for (int i = 0; i < SUNFINCH_FLOCK; i++) {
            int sx = x + random.nextInt(7) - 3;
            int sz = z + random.nextInt(7) - 3;
            if (!level.getBiome(new BlockPos(sx, 0, sz)).is(net.minecraft.tags.BiomeTags.IS_FOREST)) {
                continue;
            }
            BlockPos pos;
            if (canopy != null && random.nextBoolean()) {
                pos = canopy.above();
            } else {
                int surface = level.getHeight(Heightmap.Types.WORLD_SURFACE, sx, sz);
                pos = new BlockPos(sx, Math.min(level.getMaxBuildHeight() - 3, surface + 14 + random.nextInt(22)), sz);
            }
            if (SunfinchEntity.canSpawn(ParadiseEntities.SUNFINCH, level, MobSpawnType.NATURAL, pos, random)
                && belowCap(level, pos, ParadiseEntities.SUNFINCH, SUNFINCH_CAP)) {
                spawn(level, random, pos, ParadiseEntities.SUNFINCH);
            }
        }
    }

    private static void spawnGrazer(ServerLevel level, RandomSource random, int x, int z, BlockPos canopy) {
        // No crown at the exact column: sweep nearby columns for one instead of
        // skipping the attempt entirely (old code returned here, starving grazers).
        if (canopy == null) {
            for (int attempt = 0; attempt < 6 && canopy == null; attempt++) {
                canopy = findCanopy(level, x + random.nextInt(25) - 12, z + random.nextInt(25) - 12);
            }
            if (canopy == null) return;
        }
        // Grazers browse treetops in small herds: try the crown and its neighbors.
        for (int i = 0; i < GRAZER_HERD; i++) {
            BlockPos crown = i == 0 ? canopy
                : canopy.offset(random.nextInt(7) - 3, 0, random.nextInt(7) - 3);
            if (!level.getBiome(crown).is(net.minecraft.tags.BiomeTags.IS_FOREST)) {
                continue;
            }
            BlockPos top = crown;
            for (int y = 0; y < 6 && !level.getBlockState(top).is(net.minecraft.tags.BlockTags.LEAVES); y++) {
                top = top.below();
            }
            if (!level.getBlockState(top).is(net.minecraft.tags.BlockTags.LEAVES)) {
                continue;
            }
            BlockPos pos = top.above();
            if (CloudGrazerEntity.canSpawn(ParadiseEntities.CLOUD_GRAZER, level, MobSpawnType.NATURAL, pos, random)
                && belowCap(level, pos, ParadiseEntities.CLOUD_GRAZER, GRAZER_CAP)) {
                spawn(level, random, pos, ParadiseEntities.CLOUD_GRAZER);
            }
        }
    }

    private static void spawnWyvern(ServerLevel level, RandomSource random, int x, int z, BlockPos canopy) {
        BlockPos pos;
        if (canopy != null && random.nextInt(3) == 0) {
            pos = canopy.above(2);
        } else {
            int cloudY = 128 + random.nextInt(33) - 16;
            pos = new BlockPos(x, Mth.clamp(cloudY, level.getMinBuildHeight() + 3, level.getMaxBuildHeight() - 3), z);
        }
        if (ParadiseWyvernEntity.canSpawn(ParadiseEntities.PARADISE_WYVERN, level, MobSpawnType.NATURAL, pos, random)
            && belowCap(level, pos, ParadiseEntities.PARADISE_WYVERN, 1)) {
            spawn(level, random, pos, ParadiseEntities.PARADISE_WYVERN);
        }
    }

    private static BlockPos findCanopy(ServerLevel level, int x, int z) {
        int top = level.getHeight(Heightmap.Types.WORLD_SURFACE, x, z) - 1;
        int minY = Math.max(level.getMinBuildHeight(), top - 28);
        for (int y = top; y >= minY; y--) {
            BlockPos pos = new BlockPos(x, y, z);
            if (level.getBlockState(pos).is(BlockTags.LEAVES)) return pos;
        }
        return null;
    }

    private static boolean belowCap(ServerLevel level, BlockPos pos, EntityType<?> type, int cap) {
        AABB area = new AABB(pos).inflate(LOCAL_CAP_RANGE, 48.0D, LOCAL_CAP_RANGE);
        return level.getEntitiesOfClass(type.getBaseClass(), area, entity -> entity.isAlive()).size() < cap;
    }

    private static void spawn(ServerLevel level, RandomSource random, BlockPos pos, EntityType<? extends Mob> type) {
        Mob mob = type.create(level);
        if (mob == null) return;
        mob.moveTo(pos.getX() + 0.5D, pos.getY(), pos.getZ() + 0.5D, random.nextFloat() * 360.0F, 0.0F);
        if (!level.noCollision(mob)) return;
        mob.finalizeSpawn(level, level.getCurrentDifficultyAt(pos), MobSpawnType.NATURAL, null, null);
        level.addFreshEntity(mob);
    }
}
