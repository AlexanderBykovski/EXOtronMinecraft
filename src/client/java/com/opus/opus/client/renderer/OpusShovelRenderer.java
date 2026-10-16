package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusShovelModel;
import com.opus.opus.item.OpusShovelItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Opus Shovel wherever the item appears. */
public final class OpusShovelRenderer extends GeoItemRenderer<OpusShovelItem> {
    public OpusShovelRenderer() {
        super(new OpusShovelModel());
    }
}
