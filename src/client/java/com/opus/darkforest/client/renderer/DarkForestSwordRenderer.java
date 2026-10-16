package com.opus.darkforest.client.renderer;

import com.opus.darkforest.client.model.DarkForestSwordModel;
import com.opus.darkforest.item.DarkForestSwordItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Dark Forest Sword 3D model wherever the item appears. */
public final class DarkForestSwordRenderer extends GeoItemRenderer<DarkForestSwordItem> {
    public DarkForestSwordRenderer() {
        super(new DarkForestSwordModel());
    }
}
