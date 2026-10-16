package com.opus.opus.client.renderer;

import com.opus.opus.client.model.SettlementKatanaModel;
import com.opus.settlement.item.JapaneseKatanaItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Steel Katana wherever the item appears. */
public final class SettlementKatanaRenderer extends GeoItemRenderer<JapaneseKatanaItem> {
    public SettlementKatanaRenderer() {
        super(new SettlementKatanaModel());
    }
}
