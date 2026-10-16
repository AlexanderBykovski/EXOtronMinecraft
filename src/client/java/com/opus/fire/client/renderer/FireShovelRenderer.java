package com.opus.fire.client.renderer;

import com.opus.fire.client.model.FireShovelModel;
import com.opus.fire.item.FireShovelItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Vein Fire Shovel 3D model wherever the item appears. */
public final class FireShovelRenderer extends GeoItemRenderer<FireShovelItem> {
    public FireShovelRenderer() {
        super(new FireShovelModel());
    }
}
