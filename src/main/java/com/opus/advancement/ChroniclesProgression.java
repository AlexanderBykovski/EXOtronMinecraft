package com.opus.advancement;

import com.opus.OpusVsExe;
import net.minecraft.advancements.Advancement;
import net.minecraft.server.level.ServerPlayer;

/** Small server-side bridge for mechanics that are not vanilla advancement triggers. */
public final class ChroniclesProgression {
    private ChroniclesProgression() { }

    public static void award(ServerPlayer player, String path, String criterion) {
        Advancement advancement = player.getServer().getAdvancements().getAdvancement(OpusVsExe.id(path));
        if (advancement != null) player.getAdvancements().award(advancement, criterion);
    }
}
