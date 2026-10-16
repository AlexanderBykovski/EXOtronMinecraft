package com.opus.fire.client.renderer;

import com.opus.fire.client.model.FireAxeModel;
import com.opus.fire.item.FireAxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Vein Fire Axe 3D model wherever the item appears. */
public final class FireAxeRenderer extends GeoItemRenderer<FireAxeItem> {
    public FireAxeRenderer() {
        super(new FireAxeModel());
    }
}
