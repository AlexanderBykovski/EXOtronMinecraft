package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusKatanaRefinedModel;
import com.opus.opus.item.OpusKatanaItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Refined Opus Katana wherever the item appears. */
public final class OpusKatanaRefinedRenderer extends GeoItemRenderer<OpusKatanaItem> {
    public OpusKatanaRefinedRenderer() {
        super(new OpusKatanaRefinedModel());
    }
}
