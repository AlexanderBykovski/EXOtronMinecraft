package com.opus.paradise.client.renderer;

import com.opus.paradise.client.model.ParthenonXiphosModel;
import com.opus.paradise.item.ParthenonXiphosItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Parthenon Xiphos 3D model wherever the item appears. */
public final class ParthenonXiphosRenderer extends GeoItemRenderer<ParthenonXiphosItem> {
    public ParthenonXiphosRenderer() {
        super(new ParthenonXiphosModel());
    }
}
