package com.opus.ember.item;

import com.opus.ember.registry.EmberItems;
import com.opus.item.SetHealthBonus;
import com.opus.paradise.item.ParadisePlayerState;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * Fire Demonic set logic (server-authoritative):
 * full suit — fire resistance + strength I + regeneration + exact 5/6 health row;
 * controlled flight is available only while the full suit is worn.
 */
public final class FireDemonicArmorBonus {
    private static final Set<UUID> SUITED = new HashSet<>();
    private static final UUID HEALTH_ID = UUID.fromString("3dff11b4-86f0-41bc-93b4-fb663df12ddc");
    private static final int SET_EFFECT_DURATION = 24000;
    private FireDemonicArmorBonus() { }

    public static boolean isFullSuit(Player player) {
        return player != null
            && player.getInventory().getArmor(3).is(EmberItems.FIRE_DEMONIC_HELMET)
            && player.getInventory().getArmor(2).is(EmberItems.FIRE_DEMONIC_CHESTPLATE)
            && player.getInventory().getArmor(1).is(EmberItems.FIRE_DEMONIC_LEGGINGS)
            && player.getInventory().getArmor(0).is(EmberItems.FIRE_DEMONIC_BOOTS);
    }

    public static boolean isFullSuitClient(Player player) { return isFullSuit(player); }

    public static void init() {
        ServerTickEvents.END_WORLD_TICK.register(world -> {
            for (ServerPlayer player : world.players()) {
                if (player.isSpectator()) continue;
                updateEffects(player);
                updateFlight(player);
            }
        });
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            ServerPlayer player = handler.player;
            revokeGrantedFlight(player);
            SUITED.remove(player.getUUID());
        });
    }

    private static void updateEffects(ServerPlayer player) {
        UUID id = player.getUUID();
        if (isFullSuit(player) && player.isAlive()) {
            SetHealthBonus.update(player, HEALTH_ID, "fire_demonic_set_vitality", 20.0D / 3.0D, true);
            if (SUITED.add(id) || hasExpiringEffect(player)) applySet(player);
        } else if (SUITED.remove(id)) {
            removeSet(player);
            SetHealthBonus.update(player, HEALTH_ID, "fire_demonic_set_vitality", 20.0D / 3.0D, false);
        } else {
            SetHealthBonus.update(player, HEALTH_ID, "fire_demonic_set_vitality", 20.0D / 3.0D, false);
        }
    }

    private static void applySet(ServerPlayer player) {
        player.addEffect(effect(MobEffects.FIRE_RESISTANCE));
        player.addEffect(effect(MobEffects.DAMAGE_BOOST));
        player.addEffect(effect(MobEffects.REGENERATION));
    }

    private static void removeSet(ServerPlayer player) {
        player.removeEffect(MobEffects.FIRE_RESISTANCE);
        player.removeEffect(MobEffects.DAMAGE_BOOST);
        player.removeEffect(MobEffects.REGENERATION);
    }

    private static MobEffectInstance effect(net.minecraft.world.effect.MobEffect effect) {
        return new MobEffectInstance(effect, SET_EFFECT_DURATION, 0, true, false, true);
    }

    private static boolean hasExpiringEffect(ServerPlayer player) {
        return player.getEffect(MobEffects.FIRE_RESISTANCE) == null || player.getEffect(MobEffects.FIRE_RESISTANCE).getDuration() < 300
            || player.getEffect(MobEffects.DAMAGE_BOOST) == null || player.getEffect(MobEffects.DAMAGE_BOOST).getDuration() < 300
            || player.getEffect(MobEffects.REGENERATION) == null || player.getEffect(MobEffects.REGENERATION).getDuration() < 300;
    }

    private static void updateFlight(ServerPlayer player) {
        boolean fullSuit = player.isAlive() && isFullSuit(player);
        ParadisePlayerState state = (ParadisePlayerState) player;
        if (fullSuit && !player.getAbilities().mayfly) {
            player.getAbilities().mayfly = true;
            state.opusvsexe$setFireDemonicFlightGranted(true);
            player.onUpdateAbilities();
        } else if (!fullSuit && state.opusvsexe$isFireDemonicFlightGranted()) {
            state.opusvsexe$setFireDemonicFlightGranted(false);
            if (!player.isCreative() && !player.isSpectator()) {
                player.getAbilities().mayfly = false;
                player.getAbilities().flying = false;
                player.onUpdateAbilities();
            }
        }
    }

    private static void revokeGrantedFlight(ServerPlayer player) {
        ParadisePlayerState state = (ParadisePlayerState) player;
        if (!state.opusvsexe$isFireDemonicFlightGranted()) return;
        state.opusvsexe$setFireDemonicFlightGranted(false);
        if (player.isCreative() || player.isSpectator()) return;
        player.getAbilities().mayfly = false;
        player.getAbilities().flying = false;
        player.onUpdateAbilities();
    }
}
