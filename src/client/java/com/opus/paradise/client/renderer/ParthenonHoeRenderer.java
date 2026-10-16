package com.opus.paradise.client.renderer;

import com.opus.paradise.client.model.ParthenonHoeModel;
import com.opus.paradise.item.ParthenonHoeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Parthenon Hoe 3D model wherever the item appears. */
public final class ParthenonHoeRenderer extends GeoItemRenderer<ParthenonHoeItem> {
    public ParthenonHoeRenderer() {
        super(new ParthenonHoeModel());
    }
}
