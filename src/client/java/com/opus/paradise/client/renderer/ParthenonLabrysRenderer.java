package com.opus.paradise.client.renderer;

import com.opus.paradise.client.model.ParthenonLabrysModel;
import com.opus.paradise.item.ParthenonLabrysItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Parthenon Labrys 3D model wherever the item appears. */
public final class ParthenonLabrysRenderer extends GeoItemRenderer<ParthenonLabrysItem> {
    public ParthenonLabrysRenderer() {
        super(new ParthenonLabrysModel());
    }
}
