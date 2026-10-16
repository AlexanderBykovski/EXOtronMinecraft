package com.opus.mixin;

import com.opus.paradise.item.ParthenonLabrysItem;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Fires the Labrys block-hit feedback when vanilla shield mechanics absorb
 * damage into it. Gameplay (direction, durability, sounds) stays vanilla;
 * this only adds the weapon's animation + restrained spark supplement.
 */
@Mixin(LivingEntity.class)
public class ShieldBlockMixin {

    @Inject(method = "hurtCurrentlyUsedShield", at = @At("HEAD"))
    private void opusvsexe$labrysBlockFeedback(float amount, CallbackInfo ci) {
        LivingEntity self = (LivingEntity) (Object) this;
        if (self.level().isClientSide || !(self instanceof Player player)) {
            return;
        }
        ItemStack use = player.getUseItem();
        if (use.getItem() instanceof ParthenonLabrysItem labrys) {
            labrys.onBlocked(player, use);
        }
    }
}
