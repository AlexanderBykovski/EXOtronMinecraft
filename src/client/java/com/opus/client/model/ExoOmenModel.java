package com.opus.client.model;

import com.opusvsexe.entity.custom.Exo1Sentinel;
import com.opusvsexe.entity.custom.Exo2Hunter;
import com.opusvsexe.entity.custom.Exo3Vanguard;
import com.opusvsexe.entity.custom.Exo4Titan;
import com.opusvsexe.entity.custom.ExosuitEntity;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.GeoModel;

/**
 * Shared GeckoLib model for the EXO-1..4 war frames.
 *
 * Every frame has its own geometry/texture/animation set (red-black-gold design
 * language, see concepts/tasks/36-exo-frames-redesign.md). The resource prefix is
 * picked per entity type; the legacy exo.* set stays as the default fallback so
 * nothing breaks if a new frame type is added later.
 */
public class ExoOmenModel extends GeoModel<ExosuitEntity> {

    private static ResourceLocation res(String path) {
        return new ResourceLocation("opusvsexe", path);
    }

    private static String assetPrefix(ExosuitEntity animatable) {
        if (animatable instanceof Exo4Titan) return "exo_4_titan";
        if (animatable instanceof Exo3Vanguard) return "exo_3_vanguard";
        if (animatable instanceof Exo2Hunter) return "exo_2_hunter";
        if (animatable instanceof Exo1Sentinel) return "exo_1_sentinel";
        return "exo";
    }

    @Override
    public ResourceLocation getModelResource(ExosuitEntity animatable) {
        String prefix = assetPrefix(animatable);
        return prefix.equals("exo")
                ? res("geo/entity/exo.geo.json")
                : res("geo/entity/" + prefix + ".geo.json");
    }

    @Override
    public ResourceLocation getTextureResource(ExosuitEntity animatable) {
        String prefix = assetPrefix(animatable);
        return prefix.equals("exo")
                ? res("textures/entity/exo_omen.png")
                : res("textures/entity/" + prefix + ".png");
    }

    @Override
    public ResourceLocation getAnimationResource(ExosuitEntity animatable) {
        String prefix = assetPrefix(animatable);
        return prefix.equals("exo")
                ? res("animations/entity/exo.animation.json")
                : res("animations/entity/" + prefix + ".animation.json");
    }
}
