package com.opus.opus.client.renderer;

import com.opus.opus.client.model.OpusPickaxeModel;
import com.opus.opus.item.OpusPickaxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Opus Pickaxe wherever the item appears. */
public final class OpusPickaxeRenderer extends GeoItemRenderer<OpusPickaxeItem> {
    public OpusPickaxeRenderer() {
        super(new OpusPickaxeModel());
    }
}
