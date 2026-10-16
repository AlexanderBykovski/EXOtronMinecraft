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

/** Places KSV-01 and its authored persistent Survivor entities chunk by chunk. */
public final class SurvivorsVillagePiece extends TemplateStructurePiece {
    private static final ResourceLocation TEMPLATE = OpusVsExe.id("survivor_settlement/main");
    private static final BlockPos ROTATION_PIVOT = new BlockPos(60, 0, 50);

    private final Rotation rotation;

    public SurvivorsVillagePiece(StructureTemplateManager templateManager, BlockPos templateOrigin, Rotation rotation) {
        super(ModStructures.SURVIVORS_VILLAGE_PIECE, 0, templateManager, TEMPLATE, TEMPLATE.toString(),
                settings(rotation), templateOrigin);
        this.rotation = rotation;
    }

    public SurvivorsVillagePiece(StructurePieceSerializationContext context, CompoundTag tag) {
        super(ModStructures.SURVIVORS_VILLAGE_PIECE, tag, context.structureTemplateManager(),
                ignored -> settings(savedRotation(tag)));
        this.rotation = savedRotation(tag);
    }

    private static Rotation savedRotation(CompoundTag tag) {
        try {
            String name = tag.getString("KsvRotation");
            return name.isEmpty() ? Rotation.NONE : Rotation.valueOf(name);
        } catch (IllegalArgumentException ignored) {
            return Rotation.NONE;
        }
    }

    private static StructurePlaceSettings settings(Rotation rotation) {
        return new StructurePlaceSettings()
                .setRotation(rotation)
                .setRotationPivot(ROTATION_PIVOT)
                .setIgnoreEntities(false)
                .setKnownShape(true);
    }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        super.addAdditionalSaveData(context, tag);
        tag.putString("KsvRotation", rotation.name());
    }

    @Override
    protected void handleDataMarker(String metadata, BlockPos pos, ServerLevelAccessor level,
                                    RandomSource random, BoundingBox box) {
        // KSV-01 deliberately contains neither markers nor deferred mob spawners.
    }
}
