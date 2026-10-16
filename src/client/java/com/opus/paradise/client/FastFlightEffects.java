package com.opus.paradise.client;

import com.opus.paradise.entity.ParadiseWyvernEntity;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.Mth;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Range-capped local VFX for the wyvern's fast-flight state. The server only
 * synchronizes the state; this class supplies the dense, smooth wake locally
 * so several riders do not turn the network into a particle transport.
 */
public final class FastFlightEffects {
    private static final DustParticleOptions CYAN = new DustParticleOptions(new Vector3f(0.24F, 0.93F, 1.0F), 1.05F);
    private static final DustParticleOptions GOLD = new DustParticleOptions(new Vector3f(1.0F, 0.67F, 0.18F), 0.78F);

    private FastFlightEffects() { }

    public static void init() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.level == null || client.player == null) return;
            AABB range = client.player.getBoundingBox().inflate(48.0D);
            for (ParadiseWyvernEntity wyvern : client.level.getEntitiesOfClass(ParadiseWyvernEntity.class, range,
                ParadiseWyvernEntity::isFastFlightCharging)) {
                emitCharge(client, wyvern);
            }
            for (ParadiseWyvernEntity wyvern : client.level.getEntitiesOfClass(ParadiseWyvernEntity.class, range,
                ParadiseWyvernEntity::isFastFlightActive)) {
                emitWake(client, wyvern);
            }
        });
    }

    private static void emitCharge(Minecraft client, ParadiseWyvernEntity wyvern) {
        Vec3 center = wyvern.position().add(0.0D, 0.8D, 0.0D);
        int tick = wyvern.tickCount;
        double radius = wyvern.getFastFlightState() == 2
            ? 0.55D + 0.08D * (tick % 7)
            : 0.34D + 0.03D * (tick % 5);
        for (int ring = 0; ring < 2; ring++) {
            double angle = (tick * 0.32D) + ring * Math.PI;
            Vec3 point = center.add(Math.cos(angle) * radius, Math.sin(angle * 1.7D) * 0.2D,
                Math.sin(angle) * radius);
            client.level.addParticle(ring == 0 ? CYAN : GOLD, point.x, point.y, point.z,
                0.0D, 0.02D, 0.0D);
        }
        if (wyvern.getFastFlightState() == 2 && tick % 2 == 0) {
            client.level.addParticle(ParticleTypes.CLOUD, center.x, center.y, center.z,
                0.0D, 0.02D, 0.0D);
        }
    }

    private static void emitWake(Minecraft client, ParadiseWyvernEntity wyvern) {
        Vec3 forward = wyvern.getDeltaMovement().lengthSqr() > 0.02D
            ? wyvern.getDeltaMovement().normalize() : wyvern.getLookAngle().normalize();
        Vec3 back = forward.scale(-1.0D);
        Vec3 center = wyvern.position().add(0.0D, 0.75D, 0.0D);
        int tick = wyvern.tickCount;
        for (int i = 0; i < 3; i++) {
            double distance = 0.7D + i * 0.62D;
            double wobble = Math.sin((tick + i * 9) * 0.31D) * 0.38D;
            Vec3 side = new Vec3(-forward.z, 0.0D, forward.x).scale(wobble);
            Vec3 point = center.add(back.scale(distance)).add(side);
            client.level.addParticle(i == 0 ? CYAN : ParticleTypes.CLOUD, point.x, point.y,
                point.z, back.x * 0.035D, 0.01D, back.z * 0.035D);
        }
        if (tick % 5 == 0) {
            double angle = tick * 0.24D;
            double radius = 0.9D + 0.25D * Mth.sin(tick * 0.16F);
            Vec3 point = center.add(Math.cos(angle) * radius, 0.1D * Math.sin(angle * 2.0D),
                Math.sin(angle) * radius);
            client.level.addParticle(GOLD, point.x, point.y, point.z, back.x * 0.06D, 0.02D, back.z * 0.06D);
        }
    }
}
