package com.opus.darkforest.client.renderer;

import com.opus.darkforest.client.model.DarkForestAxeModel;
import com.opus.darkforest.item.DarkForestAxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Dark Forest Axe 3D model wherever the item appears. */
public final class DarkForestAxeRenderer extends GeoItemRenderer<DarkForestAxeItem> {
    public DarkForestAxeRenderer() {
        super(new DarkForestAxeModel());
    }
}
