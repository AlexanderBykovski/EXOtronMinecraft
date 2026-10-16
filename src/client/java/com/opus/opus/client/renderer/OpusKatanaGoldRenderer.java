package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusKatanaGoldModel;
import com.opus.opus.item.OpusKatanaItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Golden Katana wherever the item appears. */
public final class OpusKatanaGoldRenderer extends GeoItemRenderer<OpusKatanaItem> {
    public OpusKatanaGoldRenderer() {
        super(new OpusKatanaGoldModel());
    }
}
