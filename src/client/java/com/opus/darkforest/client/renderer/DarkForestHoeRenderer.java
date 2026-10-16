package com.opus.darkforest.client.renderer;

import com.opus.darkforest.client.model.DarkForestHoeModel;
import com.opus.darkforest.item.DarkForestHoeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Dark Forest Hoe 3D model wherever the item appears. */
public final class DarkForestHoeRenderer extends GeoItemRenderer<DarkForestHoeItem> {
    public DarkForestHoeRenderer() {
        super(new DarkForestHoeModel());
    }
}
