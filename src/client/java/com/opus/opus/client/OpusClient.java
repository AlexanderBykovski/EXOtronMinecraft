package com.opus.opus.client;

import com.opus.opus.client.renderer.*;
import com.opus.registry.ModItems;
import com.opus.settlement.registry.SettlementItems;
import net.fabricmc.fabric.api.client.rendering.v1.BuiltinItemRendererRegistry;

/** Registers Opus + settlement katana 3D item renderers (see scripts/generate_opus.py). */
public final class OpusClient {
    private OpusClient() { }

    public static void init() {
        OpusKatanaOpRenderer katanaOp = new OpusKatanaOpRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.KATANA_OP, katanaOp::renderByItem);
        OpusKatanaGoldRenderer katanaGold = new OpusKatanaGoldRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.KATANA_GOLD, katanaGold::renderByItem);
        OpusKatanaRefinedRenderer katanaRefined = new OpusKatanaRefinedRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.KATANA_REFINED, katanaRefined::renderByItem);
        OpusWarhammerRenderer warhammer = new OpusWarhammerRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.OPUS_WARHAMMER, warhammer::renderByItem);
        OpusPickaxeRenderer pickaxe = new OpusPickaxeRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.OPUS_PICKAXE, pickaxe::renderByItem);
        OpusAxeRenderer axe = new OpusAxeRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.OPUS_AXE, axe::renderByItem);
        OpusShovelRenderer shovel = new OpusShovelRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.OPUS_SHOVEL, shovel::renderByItem);
        OpusHoeRenderer hoe = new OpusHoeRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(ModItems.OPUS_HOE, hoe::renderByItem);
        SettlementKatanaRenderer steelKatana = new SettlementKatanaRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(SettlementItems.KATANA, steelKatana::renderByItem);
        SettlementLongKatanaRenderer longKatana = new SettlementLongKatanaRenderer();
        BuiltinItemRendererRegistry.INSTANCE.register(SettlementItems.LONG_KATANA, longKatana::renderByItem);
    }
}
