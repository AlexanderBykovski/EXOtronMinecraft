package com.opus.opus.client.renderer;

import com.opus.opus.client.model.SettlementLongKatanaModel;
import com.opus.settlement.item.JapaneseKatanaItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Long Katana wherever the item appears. */
public final class SettlementLongKatanaRenderer extends GeoItemRenderer<JapaneseKatanaItem> {
    public SettlementLongKatanaRenderer() {
        super(new SettlementLongKatanaModel());
    }
}
