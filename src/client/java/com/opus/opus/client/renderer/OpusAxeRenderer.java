package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusAxeModel;
import com.opus.opus.item.OpusAxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Opus Axe wherever the item appears. */
public final class OpusAxeRenderer extends GeoItemRenderer<OpusAxeItem> {
    public OpusAxeRenderer() {
        super(new OpusAxeModel());
    }
}
