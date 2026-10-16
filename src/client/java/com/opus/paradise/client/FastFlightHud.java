package com.opus.paradise.client;

import com.opus.paradise.entity.ParadiseWyvernEntity;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;

/** Small, non-blocking readout for the wyvern flight state and recharge. */
public final class FastFlightHud {
    private FastFlightHud() { }

    public static void init() {
        HudRenderCallback.EVENT.register(FastFlightHud::render);
    }

    private static void render(GuiGraphics gui, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (client.player == null || client.options.hideGui || client.screen != null
            || !(client.player.getVehicle() instanceof ParadiseWyvernEntity wyvern)) return;

        int width = client.getWindow().getGuiScaledWidth();
        int top = client.getWindow().getGuiScaledHeight() - 42;
        int left = width / 2 - 92;
        int right = left + 184;
        gui.fill(left, top, right, top + 26, 0xA0101C20);
        gui.fill(left, top, right, top + 1, 0xFF35E8E7);
        gui.fill(left, top + 25, right, top + 26, 0xFFB78C39);

        if (wyvern.isFastFlightActive()) {
            int remaining = Math.max(0, wyvern.getFastFlightTicks());
            gui.drawString(client.font, Component.translatable("hud.opusvsexe.wyvern.fast_flight",
                String.format(java.util.Locale.ROOT, "%.1f", remaining / 20.0D)), left + 7, top + 4, 0xFFE8FFFF, true);
            int fill = Math.round(170.0F * remaining / ParadiseWyvernEntity.FAST_FLIGHT_DURATION_TICKS);
            gui.fill(left + 7, top + 16, left + 7 + fill, top + 19, 0xFF32E6E5);
        } else if (wyvern.getFastFlightCooldown() <= 0 && !wyvern.isFastFlightCharging()) {
            gui.drawString(client.font, Component.translatable("hud.opusvsexe.wyvern.fast_flight_ready"),
                left + 7, top + 8, 0xFFFFD36A, true);
        } else {
            gui.drawString(client.font, Component.translatable("ability.opusvsexe.wyvern_fast_flight"),
                left + 7, top + 4, 0xFFE8FFFF, true);
            gui.fill(left + 7, top + 16, left + 177, top + 19, 0xFF263C42);
        }
    }
}
