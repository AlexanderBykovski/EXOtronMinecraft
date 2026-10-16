package com.opus.ember.item;

import com.opus.ember.sound.EmberSounds;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

/**
 * Fire Demonic armor: endgame volcanic-metal set above the Four Veins.
 * All visuals are 3D (FireDemonicHelmetLayer / FireDemonicPlateLayer with emissive pass);
 * vanilla HumanoidArmorLayer is cancelled for these items via mixin.
 */
public class FireDemonicArmorMaterial implements ArmorMaterial {
    public static final FireDemonicArmorMaterial INSTANCE = new FireDemonicArmorMaterial();

    private static final int[] DURABILITY = new int[]{33, 39, 41, 30};
    private static final int[] DEFENSE = new int[]{4, 8, 9, 4};

    @Override
    public int getDurabilityForType(ArmorItem.Type type) {
        return DURABILITY[type.getSlot().getIndex()] * 41;
    }

    @Override
    public int getDefenseForType(ArmorItem.Type type) {
        return DEFENSE[type.getSlot().getIndex()];
    }

    @Override
    public int getEnchantmentValue() {
        return 22;
    }

    @Override
    public SoundEvent getEquipSound() {
        return EmberSounds.EMBER_EQUIP;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return Ingredient.of(com.opus.fire.registry.FireItems.FIRE_ESSENCE);
    }

    @Override
    public String getName() {
        return "fire_demonic";
    }

    @Override
    public float getToughness() {
        return 3.5f;
    }

    @Override
    public float getKnockbackResistance() {
        return 0.15f;
    }
}
