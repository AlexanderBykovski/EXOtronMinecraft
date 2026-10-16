package com.opus.fire.client.renderer;

import com.opus.fire.client.model.FirePickaxeModel;
import com.opus.fire.item.FirePickaxeItem;
import software.bernie.geckolib.renderer.GeoItemRenderer;

/** Renders the Vein Fire Pickaxe 3D model wherever the item appears. */
public final class FirePickaxeRenderer extends GeoItemRenderer<FirePickaxeItem> {
    public FirePickaxeRenderer() {
        super(new FirePickaxeModel());
    }
}
