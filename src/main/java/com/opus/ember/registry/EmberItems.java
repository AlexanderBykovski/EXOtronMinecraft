package com.opus.ember.registry;

import com.opus.ember.EmberLine;
import com.opus.ember.item.FireDemonicArmorItem;
import com.opus.ember.item.FireDemonicArmorMaterial;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;

public class EmberItems {
    // Fire Demonic set — endgame volcanic-metal armor above the Four Veins.
    public static final Item FIRE_DEMONIC_HELMET = register("fire_demonic_helmet",
        new FireDemonicArmorItem(FireDemonicArmorMaterial.INSTANCE, ArmorItem.Type.HELMET, fireProperties()));
    public static final Item FIRE_DEMONIC_CHESTPLATE = register("fire_demonic_chestplate",
        new FireDemonicArmorItem(FireDemonicArmorMaterial.INSTANCE, ArmorItem.Type.CHESTPLATE, fireProperties()));
    public static final Item FIRE_DEMONIC_LEGGINGS = register("fire_demonic_leggings",
        new FireDemonicArmorItem(FireDemonicArmorMaterial.INSTANCE, ArmorItem.Type.LEGGINGS, fireProperties()));
    public static final Item FIRE_DEMONIC_BOOTS = register("fire_demonic_boots",
        new FireDemonicArmorItem(FireDemonicArmorMaterial.INSTANCE, ArmorItem.Type.BOOTS, fireProperties()));

    private static Item register(String name, Item item) {
        return Registry.register(BuiltInRegistries.ITEM, EmberLine.id(name), item);
    }

    private static Item.Properties fireProperties() { return new Item.Properties().fireResistant(); }

    public static void init() {}
}
