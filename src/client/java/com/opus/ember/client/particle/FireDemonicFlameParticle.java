package com.opus.ember.client.particle;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.ParticleRenderType;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.particle.TextureSheetParticle;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.util.RandomSource;

/**
 * Ядро пламени демонической брони: full-bright, сжимается и гаснет,
 * палитра e2 → e5 → white core.
 */
public class FireDemonicFlameParticle extends TextureSheetParticle {

    protected FireDemonicFlameParticle(ClientLevel level, double x, double y, double z,
                                       double vx, double vy, double vz, SpriteSet sprites) {
        super(level, x, y, z, vx, vy, vz);
        RandomSource random = level.random;
        this.lifetime = 6 + random.nextInt(6);
        this.quadSize = 0.14f + random.nextFloat() * 0.06f;
        this.gravity = 0.0f;
        this.alpha = 0.95f;
        this.setSprite(sprites.get(random));
        this.xd = vx;
        this.yd = vy;
        this.zd = vz;
    }

    @Override
    public void tick() {
        super.tick();
        float progress = (float) this.age / this.lifetime;
        this.quadSize *= 1.0F - 0.08F;
        this.alpha = Math.max(0.0F, 0.95F - progress * 0.95F);
        // heat ramp: bright core cools to deep red-orange
        float g = 0.45F + 0.4F * (1.0F - progress);
        float b = 0.10F + 0.55F * (1.0F - progress) * (1.0F - progress);
        this.setColor(1.0F, g, b);
    }

    @Override
    public int getLightColor(float partialTick) {
        return 0xF000F0;
    }

    @Override
    public ParticleRenderType getRenderType() {
        return ParticleRenderType.PARTICLE_SHEET_TRANSLUCENT;
    }

    public static class Provider implements ParticleProvider<SimpleParticleType> {
        private final SpriteSet sprites;

        public Provider(SpriteSet sprites) {
            this.sprites = sprites;
        }

        @Override
        public Particle createParticle(SimpleParticleType type, ClientLevel level, double x, double y, double z,
                                       double vx, double vy, double vz) {
            return new FireDemonicFlameParticle(level, x, y, z, vx, vy, vz, sprites);
        }
    }
}
