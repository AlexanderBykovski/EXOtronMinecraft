package com.opus.paradise.item;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * "Celestial Path" — the Xiphos RMB ability. One press, one wave: a jagged,
 * forward-directed strip of triple lightning up to 25 blocks long.
 *
 * <p>Design split (prompt sections 53-58): MANY visual bolts, but ONE
 * controlled gameplay damage event per entity per cast. Real
 * {@link LightningBolt}s are always {@code visualOnly} (no fire, no vanilla
 * damage); the 2nd/3rd strike of each triple is a lightweight particle echo,
 * which keeps ~100 thunder sounds from stacking (§81, §121).
 *
 * <p>All gameplay is server-side, tick-scheduled (never {@code Thread.sleep}),
 * per-cast state (multi-caster safe), dropped on logout/death/unload.
 */
public final class ParadiseSwordAbility {
    public static final int RANGE_BLOCKS = 25;
    public static final int MAX_LATERAL_OFFSET = 2;
    public static final int COOLDOWN_TICKS = 160;
    public static final float ABILITY_DAMAGE = 12.0F;
    public static final int DURABILITY_COST = 5;

    private static final double KEEP_PROBABILITY = 0.55;
    private static final double PROTRUSION_PROBABILITY = 0.35;
    private static final int TICKS_PER_LAYER = 1;
    private static final int ECHO_SECOND_TICKS = 2;
    private static final int ECHO_THIRD_TICKS = 4;
    private static final int RECOVER_AT_TICK = 12;
    private static final int MAX_WALL_STEP_UP = 3;

    private static final Map<UUID, ActiveCast> CASTS = new ConcurrentHashMap<>();

    private ParadiseSwordAbility() {
    }

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(ParadiseSwordAbility::tickAll);
    }

    public static boolean tryCast(Player player, ItemStack stack, InteractionHand hand, ParthenonXiphosItem item) {
        if (!(player.level() instanceof ServerLevel level) || player.isSpectator()) {
            return false;
        }
        if (player.getCooldowns().isOnCooldown(item)) {
            return false;
        }
        if (stack.isEmpty() || (stack.getMaxDamage() > 0
                && stack.getDamageValue() + DURABILITY_COST > stack.getMaxDamage())) {
            return false;
        }
        List<BlockPos> path = genPath(level, player, level.random);
        if (path.isEmpty()) {
            return false;
        }
        ActiveCast cast = new ActiveCast(UUID.randomUUID(), level.dimension(), player.getUUID(), path);
        CASTS.put(cast.id, cast);
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(item, COOLDOWN_TICKS);
            stack.hurtAndBreak(DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        item.playCastAnim(player, stack);
        level.playSound(null, player, SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 0.8F, 1.1F);
        return true;
    }

    /**
     * Constrained random walk, 1..25 forward: keep offset (55%), else step +-1,
     * clamped to +-2 with drift back to center at extremes. Occasional single
     * side protrusions (35%). Y from heightmap; walls (step up &gt; 3) stop the
     * path; void gaps skip one cell. Cells deduplicated.
     */
    /**
     * Pure lateral random walk, unit-testable without a world: {@code steps}
     * offsets in [-2, 2] where consecutive values differ by at most 1
     * (never -2 -&gt; +2 in one step), usually holding, drifting back to
     * center at the extremes.
     */
    static List<Integer> genOffsets(net.minecraft.util.RandomSource random, int steps) {
        List<Integer> offsets = new ArrayList<>(steps);
        int offset = 0;
        for (int d = 0; d < steps; d++) {
            double roll = random.nextDouble();
            if (offset >= MAX_LATERAL_OFFSET) {
                if (roll < 0.6) {
                    offset--;
                }
            } else if (offset <= -MAX_LATERAL_OFFSET) {
                if (roll < 0.6) {
                    offset++;
                }
            } else if (roll >= KEEP_PROBABILITY) {
                offset += roll < KEEP_PROBABILITY + (1.0 - KEEP_PROBABILITY) / 2.0 ? -1 : 1;
            }
            offset = Math.max(-MAX_LATERAL_OFFSET, Math.min(MAX_LATERAL_OFFSET, offset));
            offsets.add(offset);
        }
        return offsets;
    }

    static List<BlockPos> genPath(ServerLevel level, Player player, net.minecraft.util.RandomSource random) {
        double yaw = Math.toRadians(player.getYRot());
        double fx = -Math.sin(yaw);
        double fz = Math.cos(yaw);
        double rx = -fz;
        double rz = fx;
        double px = player.getX();
        double pz = player.getZ();
        int prevY = player.blockPosition().getY();
        List<Integer> offsets = genOffsets(random, RANGE_BLOCKS);
        Set<BlockPos> cells = new LinkedHashSet<>();
        for (int d = 1; d <= RANGE_BLOCKS; d++) {
            int offset = offsets.get(d - 1);
            BlockPos surface = surfaceAt(level, px + fx * d + rx * offset, pz + fz * d + rz * offset);
            if (surface == null) {
                continue;
            }
            if (surface.getY() - prevY > MAX_WALL_STEP_UP) {
                break;
            }
            prevY = surface.getY();
            cells.add(surface.immutable());
            if (random.nextDouble() < PROTRUSION_PROBABILITY) {
                int side = random.nextBoolean() ? 1 : -1;
                int po = Math.max(-MAX_LATERAL_OFFSET, Math.min(MAX_LATERAL_OFFSET, offset + side));
                if (po != offset) {
                    BlockPos extra = surfaceAt(level, px + fx * d + rx * po, pz + fz * d + rz * po);
                    if (extra != null && Math.abs(extra.getY() - prevY) <= MAX_WALL_STEP_UP) {
                        cells.add(extra.immutable());
                    }
                }
            }
        }
        return new ArrayList<>(cells);
    }

    private static BlockPos surfaceAt(ServerLevel level, double x, double z) {
        BlockPos pos = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            new BlockPos((int) Math.floor(x), 0, (int) Math.floor(z)));
        if (pos.getY() < level.getMinBuildHeight() + 1) {
            return null;
        }
        return pos;
    }

    private static void tickAll(MinecraftServer server) {
        CASTS.values().removeIf(cast -> cast.tick(server));
    }

    private record PendingEcho(int tick, BlockPos pos, boolean finale) {
    }

    private static final class ActiveCast {
        private final UUID id;
        private final ResourceKey<Level> dimension;
        private final UUID caster;
        private final List<BlockPos> cells;
        private final Set<UUID> hit = new HashSet<>();
        private final List<PendingEcho> echoes = new ArrayList<>();
        private int age;
        private int next;
        private boolean recoverFired;

        private ActiveCast(UUID id, ResourceKey<Level> dimension, UUID caster, List<BlockPos> cells) {
            this.id = id;
            this.dimension = dimension;
            this.caster = caster;
            this.cells = cells;
        }

        /** @return true when finished and safe to drop. */
        private boolean tick(MinecraftServer server) {
            ServerLevel level = server.getLevel(dimension);
            Player player = level == null ? null : server.getPlayerList().getPlayer(caster);
            if (level == null || player == null || !player.isAlive()) {
                return true;
            }
            while (next < cells.size() && next * TICKS_PER_LAYER <= age) {
                strikeCell(level, player, next);
                next++;
            }
            Iterator<PendingEcho> it = echoes.iterator();
            while (it.hasNext()) {
                PendingEcho echo = it.next();
                if (echo.tick <= age) {
                    echoFx(level, echo.pos, echo.finale);
                    it.remove();
                }
            }
            if (!recoverFired && age >= RECOVER_AT_TICK) {
                recoverFired = true;
                ItemStack held = player.getMainHandItem();
                if (!(held.getItem() instanceof ParthenonXiphosItem)) {
                    held = player.getOffhandItem();
                }
                if (held.getItem() instanceof ParthenonXiphosItem xiphos) {
                    xiphos.playRecoverAnim(player, held);
                }
            }
            age++;
            return next >= cells.size() && echoes.isEmpty() && age > cells.size() * TICKS_PER_LAYER + 4;
        }

        private void strikeCell(ServerLevel level, Player player, int index) {
            BlockPos pos = cells.get(index);
            boolean finale = index == cells.size() - 1;
            LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(level);
            if (bolt != null) {
                bolt.moveTo(pos.getX() + 0.5 + (level.random.nextDouble() - 0.5) * 0.4, pos.getY(),
                    pos.getZ() + 0.5 + (level.random.nextDouble() - 0.5) * 0.4);
                bolt.setVisualOnly(true);
                level.addFreshEntity(bolt);
            }
            echoes.add(new PendingEcho(age + ECHO_SECOND_TICKS, pos, false));
            echoes.add(new PendingEcho(age + ECHO_THIRD_TICKS, pos, finale));
            level.sendParticles(ParticleTypes.FIREWORK,
                pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, 3, 0.2, 0.2, 0.2, 0.05);
            AABB box = new AABB(pos).inflate(1.0);
            for (LivingEntity target : level.getEntitiesOfClass(LivingEntity.class, box, LivingEntity::isAlive)) {
                if (target.getUUID().equals(caster) || !hit.add(target.getUUID())) {
                    continue;
                }
                if (target instanceof Player other && (other.isCreative() || other.isSpectator())) {
                    continue;
                }
                if (target.isInvulnerable()) {
                    continue;
                }
                target.hurt(level.damageSources().lightningBolt(), ABILITY_DAMAGE);
                Vec3 push = target.position().subtract(player.position());
                push = new Vec3(push.x, 0.0, push.z).normalize();
                target.push(push.x * 0.35, 0.22, push.z * 0.35);
            }
            if (finale) {
                level.playSound(null, pos, SoundEvents.LIGHTNING_BOLT_IMPACT,
                    SoundSource.WEATHER, 0.9F, 0.9F);
                level.sendParticles(ParticleTypes.FIREWORK,
                    pos.getX() + 0.5, pos.getY() + 1.2, pos.getZ() + 0.5, 6, 0.4, 0.4, 0.4, 0.08);
            }
        }

        private void echoFx(ServerLevel level, BlockPos pos, boolean finale) {
            double x = pos.getX() + 0.5;
            double z = pos.getZ() + 0.5;
            for (double dy : new double[]{0.5, 1.5, 2.5}) {
                level.sendParticles(ParticleTypes.END_ROD, x, pos.getY() + dy, z, 4, 0.15, 0.15, 0.15, 0.01);
            }
            level.sendParticles(ParticleTypes.FIREWORK, x, pos.getY() + 1.0, z, finale ? 5 : 3,
                0.2, 0.2, 0.2, 0.05);
        }
    }
}
