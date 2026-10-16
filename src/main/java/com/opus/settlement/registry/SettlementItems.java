package com.opus.settlement.registry;

import com.opus.settlement.SettlementLine;
import com.opus.settlement.item.ExpeditionCompassItem;
import com.opus.settlement.item.JapaneseKatanaItem;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.Tiers;

import java.util.List;

public final class SettlementItems {
    public static final ExpeditionCompassItem OPUS_RUINS_COMPASS = compass("opus_ruins_compass", ExpeditionCompassItem.Target.OPUS_RUINS);
    public static final ExpeditionCompassItem TRIAL_GROUNDS_COMPASS = compass("trial_grounds_expedition_compass", ExpeditionCompassItem.Target.TRIAL_GROUNDS);
    public static final ExpeditionCompassItem SURVIVOR_SETTLEMENT_COMPASS = compass("survivor_settlement_expedition_compass", ExpeditionCompassItem.Target.SURVIVOR_SETTLEMENT);
    public static final ExpeditionCompassItem PARADISE_COMPASS = compass("paradise_expedition_compass", ExpeditionCompassItem.Target.PARADISE);
    public static final ExpeditionCompassItem KIMI_LABORATORY_COMPASS = compass("kimi_laboratory_expedition_compass", ExpeditionCompassItem.Target.KIMI_LABORATORY);
    public static final ExpeditionCompassItem JAPANESE_SETTLEMENT_COMPASS = compass("japanese_settlement_expedition_compass", ExpeditionCompassItem.Target.JAPANESE_SETTLEMENT);
    public static final ExpeditionCompassItem HAIKU_CITADEL_COMPASS = compass("haiku_citadel_expedition_compass", ExpeditionCompassItem.Target.HAIKU_CITADEL);
    public static final ExpeditionCompassItem FRONTIER_FORTRESS_COMPASS = compass("frontier_fortress_expedition_compass", ExpeditionCompassItem.Target.FRONTIER_FORTRESS);
    public static final ExpeditionCompassItem ETERNAL_COLOSSEUM_COMPASS = compass("eternal_colosseum_expedition_compass", ExpeditionCompassItem.Target.ETERNAL_COLOSSEUM);
    public static final ExpeditionCompassItem DATA_SPIRE_COMPASS = compass("data_spire_expedition_compass", ExpeditionCompassItem.Target.DATA_SPIRE);
    public static final ExpeditionCompassItem CODDY_WORKSHOP_COMPASS = compass("coddy_workshop_expedition_compass", ExpeditionCompassItem.Target.CODDY_WORKSHOP);
    public static final ExpeditionCompassItem ABANDONED_CITY_COMPASS = compass("abandoned_city_expedition_compass", ExpeditionCompassItem.Target.ABANDONED_CITY);
    public static final ExpeditionCompassItem DARK_FOREST_COMPASS = compass("dark_forest_expedition_compass", ExpeditionCompassItem.Target.DARK_FOREST);
    public static final ExpeditionCompassItem MOON_FOUNTAIN_COMPASS = compass("moon_fountain_expedition_compass", ExpeditionCompassItem.Target.MOON_FOUNTAIN);
    public static final Item KATANA = register("katana", new JapaneseKatanaItem(Tiers.IRON, 5, -2.1F, false, new Item.Properties().stacksTo(1)));
    public static final Item LONG_KATANA = register("long_katana", new JapaneseKatanaItem(Tiers.DIAMOND, 9, -2.4F, true, new Item.Properties().stacksTo(1).rarity(net.minecraft.world.item.Rarity.UNCOMMON)));
    public static final Item SURVIVOR_SPAWN_EGG = register("survivor_spawn_egg",
        new SpawnEggItem(SettlementEntities.SURVIVOR, 0x5A4034, 0xD8B07C, new Item.Properties()));
    public static final Item BLACK_NINJA_SPAWN_EGG = register("black_ninja_spawn_egg",
        new SpawnEggItem(SettlementEntities.BLACK_NINJA, 0x111116, 0x8D1723, new Item.Properties()));
    public static final Item SAMURAI_SPAWN_EGG = register("samurai_spawn_egg",
        new SpawnEggItem(SettlementEntities.SAMURAI, 0x33251E, 0xC79B50, new Item.Properties()));
    public static final Item YOUNG_SAMURAI_SPAWN_EGG = register("young_samurai_spawn_egg",
        new SpawnEggItem(SettlementEntities.YOUNG_SAMURAI, 0x161017, 0xB81942, new Item.Properties()));
    private static final List<Item> ALL = List.of(OPUS_RUINS_COMPASS, TRIAL_GROUNDS_COMPASS, SURVIVOR_SETTLEMENT_COMPASS,
        PARADISE_COMPASS, KIMI_LABORATORY_COMPASS, JAPANESE_SETTLEMENT_COMPASS, HAIKU_CITADEL_COMPASS,
        FRONTIER_FORTRESS_COMPASS, ETERNAL_COLOSSEUM_COMPASS, DATA_SPIRE_COMPASS, CODDY_WORKSHOP_COMPASS,
        ABANDONED_CITY_COMPASS, DARK_FOREST_COMPASS, MOON_FOUNTAIN_COMPASS,
        KATANA, LONG_KATANA, SURVIVOR_SPAWN_EGG, BLACK_NINJA_SPAWN_EGG, SAMURAI_SPAWN_EGG, YOUNG_SAMURAI_SPAWN_EGG,
        YOUNG_SAMURAI_SPAWN_EGG);

    private SettlementItems() { }
    private static ExpeditionCompassItem compass(String id, ExpeditionCompassItem.Target target) {
        return (ExpeditionCompassItem)register(id, new ExpeditionCompassItem(target, new Item.Properties().stacksTo(1)));
    }
    private static Item register(String id, Item item) { return Registry.register(BuiltInRegistries.ITEM, SettlementLine.id(id), item); }
    public static List<Item> all() { return ALL; }
    public static void init() { }
}
