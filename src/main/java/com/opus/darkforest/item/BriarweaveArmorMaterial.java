package com.opus.darkforest.item;

import com.opus.darkforest.registry.DarkForestItems;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

public final class BriarweaveArmorMaterial implements ArmorMaterial {
    public static final BriarweaveArmorMaterial INSTANCE=new BriarweaveArmorMaterial();
    private static final int[] DURABILITY={13,15,16,11},DEFENSE={3,8,6,3};
    private BriarweaveArmorMaterial(){ }
    @Override public int getDurabilityForType(ArmorItem.Type type){return DURABILITY[type.getSlot().getIndex()]*34;}
    @Override public int getDefenseForType(ArmorItem.Type type){return DEFENSE[type.getSlot().getIndex()];}
    @Override public int getEnchantmentValue(){return 14;}
    @Override public SoundEvent getEquipSound(){return SoundEvents.ARMOR_EQUIP_LEATHER;}
    @Override public Ingredient getRepairIngredient(){return Ingredient.of(DarkForestItems.BRIARWEAVE);}
    @Override public String getName(){return "briarweave";}
    @Override public float getToughness(){return 2F;}
    @Override public float getKnockbackResistance(){return 0;}
}
