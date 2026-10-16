package com.opus.paradise.client.renderer;

import com.opus.paradise.client.model.ParthenonPickaxeModel;
import com.opus.paradise.item.ParthenonPickaxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Parthenon Pickaxe 3D model wherever the item appears. */
public final class ParthenonPickaxeRenderer extends GeoItemRenderer<ParthenonPickaxeItem> {
    public ParthenonPickaxeRenderer() {
        super(new ParthenonPickaxeModel());
    }
}
