package com.opus.darkforest.client.renderer;

import com.opus.darkforest.client.model.DarkForestShovelModel;
import com.opus.darkforest.item.DarkForestShovelItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Dark Forest Shovel 3D model wherever the item appears. */
public final class DarkForestShovelRenderer extends GeoItemRenderer<DarkForestShovelItem> {
    public DarkForestShovelRenderer() {
        super(new DarkForestShovelModel());
    }
}
