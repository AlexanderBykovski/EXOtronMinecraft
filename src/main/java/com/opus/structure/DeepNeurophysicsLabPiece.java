package com.opus.structure;

import com.opus.OpusVsExe;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.TemplateStructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager;

/** Chunk-clipped placement of the authored K-17 NBT template. */
public final class DeepNeurophysicsLabPiece extends TemplateStructurePiece {
    private static final ResourceLocation TEMPLATE = OpusVsExe.id("kimi_laboratory/main");
    private static final BlockPos ROTATION_PIVOT = new BlockPos(58, 0, 50);

    private final Rotation rotation;

    public DeepNeurophysicsLabPiece(StructureTemplateManager templateManager, BlockPos templateOrigin, Rotation rotation) {
        super(ModStructures.DEEP_NEUROPHYSICS_LAB_PIECE, 0, templateManager, TEMPLATE, TEMPLATE.toString(),
                settings(rotation), templateOrigin);
        this.rotation = rotation;
    }

    public DeepNeurophysicsLabPiece(StructurePieceSerializationContext context, CompoundTag tag) {
        super(ModStructures.DEEP_NEUROPHYSICS_LAB_PIECE, tag, context.structureTemplateManager(),
                ignored -> settings(savedRotation(tag)));
        this.rotation = savedRotation(tag);
    }

    private static Rotation savedRotation(CompoundTag tag) {
        String name = tag.getString("K17Rotation");
        try {
            return name.isEmpty() ? Rotation.NONE : Rotation.valueOf(name);
        } catch (IllegalArgumentException ignored) {
            return Rotation.NONE;
        }
    }

    private static StructurePlaceSettings settings(Rotation rotation) {
        return new StructurePlaceSettings()
                .setRotation(rotation)
                .setRotationPivot(ROTATION_PIVOT)
                .setIgnoreEntities(true)
                .setKnownShape(true);
    }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        super.addAdditionalSaveData(context, tag);
        tag.putString("K17Rotation", rotation.name());
    }

    @Override
    protected void handleDataMarker(String metadata, BlockPos pos, ServerLevelAccessor level,
                                    RandomSource random, BoundingBox box) {
        // K-17 intentionally contains no structure-block markers. Its interactive
        // blocks already carry final NBT and are placed by the template itself.
    }
}
