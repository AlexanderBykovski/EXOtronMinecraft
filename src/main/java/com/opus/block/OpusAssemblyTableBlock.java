package com.opus.block;

import com.opus.inventory.OpusAssemblyMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.CraftingTableBlock;
import net.minecraft.world.level.block.state.BlockState;

public final class OpusAssemblyTableBlock extends CraftingTableBlock {
    private static final Component TITLE = Component.translatable("container.opusvsexe.opus_assembly_table");

    public OpusAssemblyTableBlock(Properties properties) { super(properties); }

    @Override
    public MenuProvider getMenuProvider(BlockState state, Level level, BlockPos pos) {
        return new SimpleMenuProvider((id, inventory, player) ->
            new OpusAssemblyMenu(id, inventory, ContainerLevelAccess.create(level, pos)), TITLE);
    }
}
