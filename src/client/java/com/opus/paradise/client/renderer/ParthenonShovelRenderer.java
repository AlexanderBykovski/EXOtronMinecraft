package com.opus.paradise.client.renderer;

import com.opus.paradise.client.model.ParthenonShovelModel;
import com.opus.paradise.item.ParthenonShovelItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Parthenon Shovel 3D model wherever the item appears. */
public final class ParthenonShovelRenderer extends GeoItemRenderer<ParthenonShovelItem> {
    public ParthenonShovelRenderer() {
        super(new ParthenonShovelModel());
    }
}
