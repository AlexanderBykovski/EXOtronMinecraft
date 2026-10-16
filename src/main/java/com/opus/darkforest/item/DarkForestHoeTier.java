package com.opus.darkforest.item;

import com.opus.darkforest.registry.DarkForestItems;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;

/**
 * Dark Forest Hoe tier: identical combat/mining profile to
 * {@link DarkForestToolTier}, but a 30000-point durability reservoir,
 * because the hoe is a pure workhorse (3x3 tilling, no abilities).
 */
public enum DarkForestHoeTier implements Tier {
    INSTANCE;
    @Override public int getUses() { return 30000; }
    @Override public float getSpeed() { return 9F; }
    @Override public float getAttackDamageBonus() { return 3F; }
    @Override public int getLevel() { return 3; }
    @Override public int getEnchantmentValue() { return 22; }
    @Override public Ingredient getRepairIngredient() { return Ingredient.of(DarkForestItems.BRIARWEAVE); }
}
