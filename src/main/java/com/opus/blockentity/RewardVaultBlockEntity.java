package com.opus.blockentity;

import com.opus.block.RewardVaultBlock;
import com.opus.inventory.RewardVaultMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.WorldlyContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

import java.util.stream.IntStream;

public class RewardVaultBlockEntity extends RandomizableContainerBlockEntity implements WorldlyContainer {
    private static final int SIZE = 27;
    private static final int[] SLOTS = IntStream.range(0, SIZE).toArray();
    private NonNullList<ItemStack> items = NonNullList.withSize(SIZE, ItemStack.EMPTY);

    public RewardVaultBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.REWARD_VAULT, pos, state);
    }

    @Override
    protected Component getDefaultName() {
        return Component.translatable("container.opusvsexe.reward_vault");
    }

    @Override
    protected AbstractContainerMenu createMenu(int id, Inventory inventory) {
        return new RewardVaultMenu(id, inventory, this);
    }

    @Override
    public int getContainerSize() {
        return SIZE;
    }

    @Override
    protected NonNullList<ItemStack> getItems() {
        return items;
    }

    @Override
    protected void setItems(NonNullList<ItemStack> items) {
        this.items = items;
    }

    @Override
    public void load(CompoundTag tag) {
        super.load(tag);
        this.items = NonNullList.withSize(SIZE, ItemStack.EMPTY);
        if (!tryLoadLootTable(tag)) ContainerHelper.loadAllItems(tag, this.items);
    }

    @Override
    protected void saveAdditional(CompoundTag tag) {
        super.saveAdditional(tag);
        if (!trySaveLootTable(tag)) ContainerHelper.saveAllItems(tag, this.items);
    }

    @Override
    public boolean stillValid(Player player) {
        if (level == null || level.getBlockEntity(worldPosition) != this || !isOpen()) return false;
        return player.distanceToSqr(worldPosition.getX() + 0.5, worldPosition.getY() + 0.5,
                worldPosition.getZ() + 0.5) <= 64.0;
    }

    @Override
    public int[] getSlotsForFace(Direction side) {
        return isOpen() ? SLOTS : new int[0];
    }

    @Override
    public boolean canPlaceItemThroughFace(int slot, ItemStack stack, @Nullable Direction direction) {
        return isOpen();
    }

    @Override
    public boolean canTakeItemThroughFace(int slot, ItemStack stack, Direction direction) {
        return isOpen();
    }

    private boolean isOpen() {
        return getBlockState().getBlock() instanceof RewardVaultBlock
                && getBlockState().getValue(RewardVaultBlock.OPEN);
    }

    public void tick(net.minecraft.world.level.Level level, BlockPos pos, BlockState state) {
    }
}
