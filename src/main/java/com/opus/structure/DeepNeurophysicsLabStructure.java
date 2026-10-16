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
 * Terrain-aware anchor for the K-17 template.  The template itself contains
 * all deterministic geometry; this class only makes the surface entrance and
 * its deep lower bound safe on real terrain.
 */
public final class DeepNeurophysicsLabStructure extends Structure {
    public static final Codec<DeepNeurophysicsLabStructure> CODEC = RecordCodecBuilder
            .<DeepNeurophysicsLabStructure>mapCodec(instance -> instance.group(
                    settingsCodec(instance)
            ).apply(instance, DeepNeurophysicsLabStructure::new)).codec();

    private static final int TEMPLATE_HALF_X = 58;
    private static final int TEMPLATE_HALF_Z = 50;
    private static final int SURFACE_OFFSET = 68;
    private static final int MINIMUM_Y_MARGIN = 8;
    private static final int MAX_SURFACE_SLOPE = 7;

    public DeepNeurophysicsLabStructure(StructureSettings settings) {
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
        if (!hasAcceptableSlope(context, centerX, centerZ)) {
            return Optional.empty();
        }

        BlockPos templateOrigin = new BlockPos(centerX - TEMPLATE_HALF_X, surfaceY - SURFACE_OFFSET,
                centerZ - TEMPLATE_HALF_Z);
        Rotation rotation = Rotation.getRandom(context.random());
        return Optional.of(new GenerationStub(templateOrigin, builder -> builder.addPiece(
                new DeepNeurophysicsLabPiece(context.structureTemplateManager(), templateOrigin, rotation)
        )));
    }

    private static int surfaceY(GenerationContext context, int x, int z) {
        return context.chunkGenerator().getBaseHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG,
                context.heightAccessor(), context.randomState()) - 1;
    }

    private static boolean hasAcceptableSlope(GenerationContext context, int centerX, int centerZ) {
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        for (int xOffset = -8; xOffset <= 8; xOffset += 8) {
            for (int zOffset = -8; zOffset <= 8; zOffset += 8) {
                int height = surfaceY(context, centerX + xOffset, centerZ + zOffset);
                min = Math.min(min, height);
                max = Math.max(max, height);
            }
        }
        return max - min <= MAX_SURFACE_SLOPE;
    }

    @Override
    public StructureType<?> type() {
        return ModStructures.DEEP_NEUROPHYSICS_LAB_TYPE;
    }
}
