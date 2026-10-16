package com.opus.ember.item;

import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;

/** Fire Demonic armor piece. Rendering: 3D layers + emissive; set bonuses in FireDemonicArmorBonus. */
public class FireDemonicArmorItem extends ArmorItem {

    public FireDemonicArmorItem(ArmorMaterial material, Type type, Properties properties) {
        super(material, type, properties);
    }
}
