package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusWarhammerModel;
import com.opus.opus.item.OpusWarhammerItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Opus Warhammer wherever the item appears. */
public final class OpusWarhammerRenderer extends GeoItemRenderer<OpusWarhammerItem> {
    public OpusWarhammerRenderer() {
        super(new OpusWarhammerModel());
    }
}
