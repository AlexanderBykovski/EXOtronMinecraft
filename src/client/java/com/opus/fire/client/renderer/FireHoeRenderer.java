package com.opus.fire.client.renderer;

import com.opus.fire.client.model.FireHoeModel;
import com.opus.fire.item.FireHoeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Vein Fire Hoe 3D model wherever the item appears. */
public final class FireHoeRenderer extends GeoItemRenderer<FireHoeItem> {
    public FireHoeRenderer() {
        super(new FireHoeModel());
    }
}
