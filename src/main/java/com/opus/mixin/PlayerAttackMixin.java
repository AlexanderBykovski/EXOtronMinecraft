package com.opus.mixin;

import com.opus.item.KatanaItem;
import com.opus.item.WarhammerItem;
import com.opus.opus.item.OpusAxeItem;
import com.opus.opus.item.OpusHoeItem;
import com.opus.opus.item.OpusKatanaItem;
import com.opus.opus.item.OpusPickaxeItem;
import com.opus.opus.item.OpusShovelItem;
import com.opus.opus.item.OpusWarhammerItem;
import com.opus.settlement.item.JapaneseKatanaItem;
import com.opus.paradise.item.ParthenonLabrysItem;
import com.opus.paradise.item.ParthenonPickaxeItem;
import com.opus.paradise.item.ParthenonXiphosItem;
import com.opus.paradise.item.ParthenonShovelItem;
import com.opus.paradise.item.ParthenonHoeItem;
import com.opus.darkforest.item.DarkForestSwordItem;
import com.opus.darkforest.item.DarkForestPickaxeItem;
import com.opus.darkforest.item.DarkForestAxeItem;
import com.opus.darkforest.item.DarkForestShovelItem;
import com.opus.darkforest.item.DarkForestHoeItem;
import com.opus.fire.item.FireSwordItem;
import com.opus.fire.item.FirePickaxeItem;
import com.opus.fire.item.FireAxeItem;
import com.opus.fire.item.FireShovelItem;
import com.opus.fire.item.FireHoeItem;
import com.opus.sound.ModSounds;
import com.opusvsexe.entity.custom.ExosuitEntity;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Player.class)
public class PlayerAttackMixin {

    @Inject(method = "attack", at = @At("HEAD"), cancellable = true)
    private void opusvsexe$exoRideAttack(Entity target, CallbackInfo ci) {
        Player self = (Player) (Object) this;
        if (self.level().isClientSide) {
            return;
        }
        // Attacks while piloting an EXO frame never reach this method: the client
        // mixin redirects left click into the exo_attack packet, and the suit
        // validates it (cooldown, reach, pilot identity). Letting a vanilla
        // attack land here would bypass that validation, so a piloted suit
        // cannot be damaged through this path and swing sounds stay vanilla.
        if (self.getVehicle() instanceof ExosuitEntity) {
            ci.cancel();
            return;
        }
        ItemStack hand = self.getMainHandItem();
        if (hand.getItem() instanceof KatanaItem) {
            self.level().playSound(null, target.blockPosition(), ModSounds.KATANA_SWING, SoundSource.PLAYERS, 0.7f, 1.0f);
        } else if (hand.getItem() instanceof WarhammerItem) {
            self.level().playSound(null, target.blockPosition(), ModSounds.HAMMER_HIT, SoundSource.PLAYERS, 0.7f, 0.7f);
        } else if (hand.getItem() instanceof ParthenonLabrysItem labrys) {
            labrys.onStrike(self, hand);
        } else if (hand.getItem() instanceof ParthenonPickaxeItem pickaxe) {
            pickaxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof ParthenonXiphosItem xiphos) {
            xiphos.onStrike(self, hand);
        } else if (hand.getItem() instanceof ParthenonShovelItem shovel) {
            shovel.onStrike(self, hand);
        } else if (hand.getItem() instanceof ParthenonHoeItem hoe) {
            hoe.onStrike(self, hand);
        } else if (hand.getItem() instanceof DarkForestSwordItem dfSword) {
            dfSword.onStrike(self, hand);
        } else if (hand.getItem() instanceof DarkForestPickaxeItem dfPickaxe) {
            dfPickaxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof DarkForestAxeItem dfAxe) {
            dfAxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof DarkForestShovelItem dfShovel) {
            dfShovel.onStrike(self, hand);
        } else if (hand.getItem() instanceof DarkForestHoeItem dfHoe) {
            dfHoe.onStrike(self, hand);
        } else if (hand.getItem() instanceof FireSwordItem vfSword) {
            vfSword.onStrike(self, hand);
        } else if (hand.getItem() instanceof FirePickaxeItem vfPickaxe) {
            vfPickaxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof FireAxeItem vfAxe) {
            vfAxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof FireShovelItem vfShovel) {
            vfShovel.onStrike(self, hand);
        } else if (hand.getItem() instanceof FireHoeItem vfHoe) {
            vfHoe.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusKatanaItem opKatana) {
            opKatana.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusWarhammerItem opHammer) {
            opHammer.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusPickaxeItem opPickaxe) {
            opPickaxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusAxeItem opAxe) {
            opAxe.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusShovelItem opShovel) {
            opShovel.onStrike(self, hand);
        } else if (hand.getItem() instanceof OpusHoeItem opHoe) {
            opHoe.onStrike(self, hand);
        } else if (hand.getItem() instanceof JapaneseKatanaItem jpKatana) {
            jpKatana.onStrike(self, hand);
        }
    }
}
