package com.opus.ember.client;

import com.opus.ember.item.FireDemonicArmorBonus;
import com.opus.ember.registry.EmberParticles;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.Mth;
import net.minecraft.world.phys.Vec3;

/**
 * Fire flight VFX: while the full Fire Demonic suit is worn and the wearer is
 * actually flying, flames emit from the two boot soles (thrust) and the two
 * upper-back vents (stabilizers). Rate-limited, distance-culled, purely visual.
 */
public final class FireDemonicFlightEffects {
    private static final double RANGE_SQR = 64.0D * 64.0D;
    private FireDemonicFlightEffects() { }

    public static void init() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            LocalPlayer self = client.player;
            if (self == null || client.level == null) return;
            for (AbstractClientPlayer player : client.level.players()) {
                if (!player.isAlive() || player.isSpectator()) continue;
                if (!FireDemonicArmorBonus.isFullSuitClient(player)) continue;
                boolean flying = player.getAbilities().flying || player.isFallFlying();
                if (!flying) continue;
                if (player.distanceToSqr(self) > RANGE_SQR) continue;
                spawnFlames(player, client, self == player);
            }
        });
    }

    private static void spawnFlames(AbstractClientPlayer player, Minecraft client, boolean isSelf) {
        float partial = client.getFrameTime();
        Vec3 pos = player.getPosition(partial);
        float yaw = player.getYRot() * Mth.DEG_TO_RAD;
        Vec3 look = new Vec3(-Mth.sin(yaw), 0, Mth.cos(yaw));
        Vec3 right = new Vec3(-Mth.cos(yaw), 0, -Mth.sin(yaw));
        Vec3 motion = player.getDeltaMovement();
        double speed = motion.horizontalDistance();
        var level = client.level;
        var random = level.random;
        boolean braking = speed < 0.14D;
        boolean hovering = speed < 0.28D;

        Vec3 bootLeft = pos.add(right.scale(-0.26D));
        Vec3 bootRight = pos.add(right.scale(0.26D));
        Vec3 ventLeft = pos.add(look.scale(-0.30D)).add(right.scale(-0.22D)).add(0, 1.32D, 0);
        Vec3 ventRight = pos.add(look.scale(-0.30D)).add(right.scale(0.22D)).add(0, 1.32D, 0);

        // boot thrust: flames point opposite movement; straight down while hovering
        Vec3 thrust = hovering ? new Vec3((random.nextDouble() - 0.5D) * 0.02D, -0.14D - random.nextDouble() * 0.06D,
                (random.nextDouble() - 0.5D) * 0.02D)
            : motion.scale(-0.55D).add(0, -0.08D - speed * 0.1D, 0);
        int flames = braking ? 1 : hovering ? 1 : speed > 0.55D ? 2 : 1;
        for (Vec3 boot : new Vec3[]{bootLeft, bootRight}) {
            for (int i = 0; i < flames; i++) {
                level.addParticle(ParticleTypes.FLAME, false,
                    boot.x, boot.y + 0.02D, boot.z,
                    thrust.x + (random.nextDouble() - 0.5D) * 0.02D,
                    thrust.y,
                    thrust.z + (random.nextDouble() - 0.5D) * 0.02D);
                if (random.nextInt(3) == 0) {
                    level.addParticle(EmberParticles.FIRE_DEMONIC_FLAME, false,
                        boot.x + (random.nextDouble() - 0.5D) * 0.1D, boot.y + 0.06D, boot.z + (random.nextDouble() - 0.5D) * 0.1D,
                        thrust.x * 0.7D, thrust.y * 0.7D, thrust.z * 0.7D);
                }
            }
            if (random.nextInt(braking ? 4 : 8) == 0) {
                level.addParticle(ParticleTypes.LAVA, boot.x, boot.y, boot.z, 0, -0.02D, 0);
            }
        }

        // back vents: short stabilizing bursts; slightly stronger while braking
        Vec3 ventDrift = hovering ? new Vec3(0, 0.015D, 0) : motion.scale(-0.35D);
        int bursts = braking ? 2 : 1;
        for (Vec3 vent : new Vec3[]{ventLeft, ventRight}) {
            for (int i = 0; i < bursts; i++) {
                if (random.nextInt(2) == 0) {
                    level.addParticle(EmberParticles.FIRE_DEMONIC_FLAME, false,
                        vent.x, vent.y, vent.z,
                        ventDrift.x + (random.nextDouble() - 0.5D) * 0.03D,
                        ventDrift.y + 0.01D,
                        ventDrift.z + (random.nextDouble() - 0.5D) * 0.03D);
                }
            }
        }

        // high speed smoke trail
        if (speed > 0.45D && random.nextInt(3) == 0) {
            Vec3 tail = pos.add(motion.scale(-1.2D)).add(0, 1.0D, 0);
            level.addParticle(ParticleTypes.SMOKE, tail.x, tail.y, tail.z,
                motion.x * -0.1D, 0.005D, motion.z * -0.1D);
        }
    }
}
