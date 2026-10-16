package com.opus.block;

import com.opus.blockentity.ExoAssemblyFrameBlockEntity;
import com.opus.blockentity.ModBlockEntities;
import com.opus.item.ExoActivationCoreItem;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import org.jetbrains.annotations.Nullable;

public final class ExoAssemblyFrameBlock extends Block implements EntityBlock {
    public static final BooleanProperty ACTIVE = BooleanProperty.create("active");

    public ExoAssemblyFrameBlock(Properties properties) {
        super(properties);
        registerDefaultState(defaultBlockState().setValue(ACTIVE, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(ACTIVE); }

    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player,
                                 InteractionHand hand, BlockHitResult hit) {
        if (state.getValue(ACTIVE)) {
            if (!level.isClientSide) player.displayClientMessage(Component.translatable("message.opusvsexe.exo_frame.assembling"), true);
            return InteractionResult.sidedSuccess(level.isClientSide);
        }
        if (player.getItemInHand(hand).getItem() instanceof ExoActivationCoreItem core
            && level.getBlockEntity(pos) instanceof ExoAssemblyFrameBlockEntity frame) {
            if (level.isClientSide) return InteractionResult.SUCCESS;
            if (!frame.startAssembly(core, player)) return InteractionResult.FAIL;
            if (!player.getAbilities().instabuild) player.getItemInHand(hand).shrink(1);
            return InteractionResult.CONSUME;
        }
        if (!level.isClientSide) player.displayClientMessage(Component.translatable("message.opusvsexe.exo_frame.insert_core"), true);
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Nullable
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new ExoAssemblyFrameBlockEntity(pos, state); }

    @Nullable
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        return type == ModBlockEntities.EXO_ASSEMBLY_FRAME
            ? (world, pos, blockState, blockEntity) -> ((ExoAssemblyFrameBlockEntity) blockEntity).tick(world, pos, blockState)
            : null;
    }
}
