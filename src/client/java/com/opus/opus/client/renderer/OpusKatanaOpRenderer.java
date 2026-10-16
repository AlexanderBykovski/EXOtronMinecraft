package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusKatanaOpModel;
import com.opus.opus.item.OpusKatanaItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Katana-OP wherever the item appears. */
public final class OpusKatanaOpRenderer extends GeoItemRenderer<OpusKatanaItem> {
    public OpusKatanaOpRenderer() {
        super(new OpusKatanaOpModel());
    }
}
