package com.opus.fire.client.renderer;

import com.opus.fire.client.model.FireSwordModel;
import com.opus.fire.item.FireSwordItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Vein Fire Sword 3D model wherever the item appears. */
public final class FireSwordRenderer extends GeoItemRenderer<FireSwordItem> {
    public FireSwordRenderer() {
        super(new FireSwordModel());
    }
}
