package com.opus.item;

import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;

import java.util.UUID;

/** Exact, non-potion health fractions for full armour sets. */
public final class SetHealthBonus {
    private SetHealthBonus() { }

    public static void update(Player player, UUID id, String name, double extraHealth, boolean enabled) {
        AttributeInstance maximum = player.getAttribute(Attributes.MAX_HEALTH);
        if (maximum == null) return;
        AttributeModifier existing = maximum.getModifier(id);
        if (enabled) {
            if (existing == null) {
                maximum.addTransientModifier(new AttributeModifier(id, name, extraHealth, AttributeModifier.Operation.ADDITION));
            }
        } else if (existing != null) {
            maximum.removeModifier(id);
            player.setHealth(Math.min(player.getHealth(), player.getMaxHealth()));
        }
    }
}
