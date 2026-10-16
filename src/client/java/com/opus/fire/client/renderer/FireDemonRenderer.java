package com.opus.fire.client.renderer;

import com.opus.darkforest.client.renderer.EmissiveGlowGeoLayer;
import com.opus.fire.client.model.FireDemonModel;
import com.opus.fire.entity.FireDemonEntity;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;

/**
 * Rebuilt 2026-08-31: original horned devil (no wings), body ~50/16 = 3.1 blocks,
 * horn tips ~62/16 = 3.9 blocks (outside the 1.4x3.1 hitbox). Digitigrade hooved
 * legs, tail and waistcloth stay within ~1.5 blocks of the body axis; the cryolde
 * seal (ice_* bones) is translucent. Emissive pass lights eyes, sternum fissure,
 * plate/horn cracks and the tail-tip seam from demon_emissive.png.
 */
public class FireDemonRenderer extends GeoEntityRenderer<FireDemonEntity> {

    public FireDemonRenderer(EntityRendererProvider.Context context) {
        super(context, new FireDemonModel());
        addRenderLayer(new EmissiveGlowGeoLayer<>(this));
        shadowRadius = 1.0F;
    }
}
