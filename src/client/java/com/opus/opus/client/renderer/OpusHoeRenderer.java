package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusHoeModel;
import com.opus.opus.item.OpusHoeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Opus Hoe wherever the item appears. */
public final class OpusHoeRenderer extends GeoItemRenderer<OpusHoeItem> {
    public OpusHoeRenderer() {
        super(new OpusHoeModel());
    }
}
