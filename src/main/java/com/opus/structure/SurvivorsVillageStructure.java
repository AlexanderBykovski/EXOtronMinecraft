package com.opus.structure;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;

import java.util.Optional;

/**
 * Bounded terrain selection for KSV-01.  All village geometry remains in a
 * single deterministic NBT; this type only rejects terrain that would bury a
 * doorway, float a foundation or expose the underground shelter.
 */
public final class SurvivorsVillageStructure extends Structure {
    public static final Codec<SurvivorsVillageStructure> CODEC = RecordCodecBuilder
            .<SurvivorsVillageStructure>mapCodec(instance -> instance.group(
                    settingsCodec(instance)
            ).apply(instance, SurvivorsVillageStructure::new)).codec();

    private static final int TEMPLATE_HALF_X = 60;
    private static final int TEMPLATE_HALF_Z = 50;
    private static final int SURFACE_OFFSET = 16;
    private static final int MINIMUM_Y_MARGIN = 8;
    private static final int MAX_FOOTPRINT_SLOPE = 6;
    private static final int MAX_CRITICAL_OFFSET = 3;
    private static final int[] GRID = {-54, -36, -18, 0, 18, 36, 54};
    private static final int[][] CRITICAL_ACCESS = {
            {0, 47}, {0, -47}, {-58, 11}, {58, 0}, {-58, 3}
    };

    public SurvivorsVillageStructure(StructureSettings settings) {
        super(settings);
    }

    @Override
    public Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        ChunkPos chunk = context.chunkPos();
        int centerX = chunk.getMinBlockX() + 8;
        int centerZ = chunk.getMinBlockZ() + 8;
        int surfaceY = surfaceY(context, centerX, centerZ);
        if (surfaceY - SURFACE_OFFSET < context.heightAccessor().getMinBuildHeight() + MINIMUM_Y_MARGIN) {
            return Optional.empty();
        }
        if (!hasAcceptableTerrain(context, centerX, centerZ, surfaceY)) {
            return Optional.empty();
        }

        BlockPos templateOrigin = new BlockPos(centerX - TEMPLATE_HALF_X, surfaceY - SURFACE_OFFSET,
                centerZ - TEMPLATE_HALF_Z);
        Rotation rotation = Rotation.getRandom(context.random());
        return Optional.of(new GenerationStub(templateOrigin, builder -> builder.addPiece(
                new SurvivorsVillagePiece(context.structureTemplateManager(), templateOrigin, rotation)
        )));
    }

    private static int surfaceY(GenerationContext context, int x, int z) {
        return context.chunkGenerator().getBaseHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG,
                context.heightAccessor(), context.randomState()) - 1;
    }

    private static boolean hasAcceptableTerrain(GenerationContext context, int centerX, int centerZ, int centerY) {
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        for (int xOffset : GRID) {
            for (int zOffset : GRID) {
                int height = surfaceY(context, centerX + xOffset, centerZ + zOffset);
                min = Math.min(min, height);
                max = Math.max(max, height);
            }
        }
        if (max - min > MAX_FOOTPRINT_SLOPE) return false;
        // Check both axes, so every possible template rotation has safe south,
        // north, west-postern and east road access before the rotation is drawn.
        for (int[] access : CRITICAL_ACCESS) {
            int height = surfaceY(context, centerX + access[0], centerZ + access[1]);
            if (Math.abs(height - centerY) > MAX_CRITICAL_OFFSET) return false;
        }
        return true;
    }

    @Override
    public StructureType<?> type() {
        return ModStructures.SURVIVORS_VILLAGE_TYPE;
    }
}
