package com.opus.settlement.item;

import com.opus.OpusVsExe;
import com.opus.darkforest.DarkForestLine;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.CompassItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.structure.Structure;

import java.util.List;

public final class ExpeditionCompassItem extends CompassItem {
    public enum Target {
        OPUS_RUINS("opus_ruins", "survivor_route_opus"),
        TRIAL_GROUNDS("trial_grounds", "expedition_trial_grounds"),
        SURVIVOR_SETTLEMENT("survivor_settlement", "expedition_survivor_settlement"),
        PARADISE("paradise", "expedition_paradise_island"),
        KIMI_LABORATORY("kimi_laboratory", "expedition_kimi_laboratory"),
        JAPANESE_SETTLEMENT("japanese_settlement", "expedition_japanese_settlement"),
        HAIKU_CITADEL("haiku_citadel", "expedition_haiku_citadel"),
        FRONTIER_FORTRESS("frontier_fortress", "expedition_frontier_fortress"),
        ETERNAL_COLOSSEUM("eternal_colosseum", "expedition_eternal_colosseum"),
        DATA_SPIRE("data_spire", "expedition_data_spire"),
        CODDY_WORKSHOP("coddy_workshop", "expedition_coddy_workshop"),
        ABANDONED_CITY("abandoned_city", "expedition_abandoned_city"),
        DARK_FOREST("dark_forest", null),
        MOON_FOUNTAIN("moon_fountain", "expedition_moon_fountain");

        final String id;
        final TagKey<Structure> structureTag;
        Target(String id, String tag) {
            this.id = id;
            this.structureTag = tag == null ? null : TagKey.create(Registries.STRUCTURE, OpusVsExe.id(tag));
        }
    }

    private final Target target;

    public ExpeditionCompassItem(Target target, Properties properties) {
        super(properties);
        this.target = target;
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (level instanceof ServerLevel server && level.dimension() == Level.OVERWORLD && !stack.getOrCreateTag().contains("LodestonePos")) {
            var tag = stack.getOrCreateTag();
            BlockPos origin = entity.blockPosition();
            boolean movedBeyondRetryRange = !tag.contains("SurveyOrigin") || BlockPos.of(tag.getLong("SurveyOrigin")).distSqr(origin) > 512D * 512D;
            if (!tag.getBoolean("SurveyFailed") || movedBeyondRetryRange) calibrate(stack, server, origin);
        }
    }

    public boolean calibrate(ItemStack stack, ServerLevel level, BlockPos origin) {
        BlockPos destination;
        if (target == Target.DARK_FOREST) {
            var found = level.findClosestBiome3d(holder -> holder.is(DarkForestLine.DARK_FOREST), origin, 4096, 32, 64);
            destination = found == null ? null : found.getFirst();
        } else {
            destination = level.findNearestMapStructure(target.structureTag, origin, 160, false);
        }
        var tag = stack.getOrCreateTag();
        tag.putLong("SurveyOrigin", origin.asLong());
        if (destination == null) {
            tag.putBoolean("SurveyFailed", true);
            return false;
        }
        tag.remove("SurveyFailed");
        tag.put("LodestonePos", NbtUtils.writeBlockPos(destination));
        tag.putString("LodestoneDimension", Level.OVERWORLD.location().toString());
        tag.putBoolean("LodestoneTracked", false);
        return true;
    }

    public Target target() { return target; }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, level, tooltip, flag);
        String state = stack.getOrCreateTag().contains("LodestonePos") ? "calibrated" : stack.getOrCreateTag().getBoolean("SurveyFailed") ? "unresolved" : "pending";
        tooltip.add(Component.translatable("item.opusvsexe.expedition_compass.target." + target.id));
        tooltip.add(Component.translatable("item.opusvsexe.expedition_compass." + state));
    }
}
