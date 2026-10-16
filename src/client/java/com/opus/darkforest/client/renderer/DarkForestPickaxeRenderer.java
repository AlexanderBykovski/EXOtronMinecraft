package com.opus.darkforest.client.renderer;

import com.opus.darkforest.client.model.DarkForestPickaxeModel;
import com.opus.darkforest.item.DarkForestPickaxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Dark Forest Pickaxe 3D model wherever the item appears. */
public final class DarkForestPickaxeRenderer extends GeoItemRenderer<DarkForestPickaxeItem> {
    public DarkForestPickaxeRenderer() {
        super(new DarkForestPickaxeModel());
    }
}
