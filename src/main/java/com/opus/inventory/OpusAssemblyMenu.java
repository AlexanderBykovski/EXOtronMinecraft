package com.opus.inventory;

import com.opus.OpusVsExe;
import com.opus.advancement.ChroniclesProgression;
import com.opus.registry.ModBlocks;
import com.opus.registry.ModMenus;
import com.opus.registry.ModRecipes;
import net.minecraft.core.NonNullList;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.Container;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.ResultContainer;
import net.minecraft.world.inventory.ResultSlot;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.inventory.TransientCraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeType;

import java.util.Optional;

public final class OpusAssemblyMenu extends AbstractContainerMenu {
    private final TransientCraftingContainer inputs = new TransientCraftingContainer(this, 5, 5);
    private final ResultContainer result = new ResultContainer();
    private final ContainerLevelAccess access;
    private final Player player;

    public OpusAssemblyMenu(int id, Inventory inventory) { this(id, inventory, ContainerLevelAccess.NULL); }

    public OpusAssemblyMenu(int id, Inventory inventory, ContainerLevelAccess access) {
        super(ModMenus.OPUS_ASSEMBLY_TABLE, id);
        this.access = access;
        this.player = inventory.player;
        addSlot(new AssemblyResultSlot(player, inputs, result, 0, 150, 53));
        for (int row = 0; row < 5; row++) for (int col = 0; col < 5; col++) {
            addSlot(new Slot(inputs, col + row * 5, 35 + col * 18, 22 + row * 18));
        }
        for (int row = 0; row < 3; row++) for (int col = 0; col < 9; col++) {
            addSlot(new Slot(inventory, col + row * 9 + 9, 8 + col * 18, 126 + row * 18));
        }
        for (int col = 0; col < 9; col++) addSlot(new Slot(inventory, col, 8 + col * 18, 184));
    }

    public Container getInputs() { return inputs; }

    /** The assembly table accepts its native 5x5 recipes and ordinary 3x3 recipes. */
    private Optional<Recipe<net.minecraft.world.inventory.CraftingContainer>> findRecipe() {
        Optional<com.opus.recipe.OpusAssemblyRecipe> assembly = player.level().getRecipeManager()
            .getRecipeFor(ModRecipes.ASSEMBLY, inputs, player.level())
            .map(recipe -> recipe);
        if (assembly.isPresent()) return assembly.map(recipe -> (Recipe<net.minecraft.world.inventory.CraftingContainer>) recipe);
        return player.level().getRecipeManager().getAllRecipesFor(RecipeType.CRAFTING).stream()
            .filter(recipe -> recipe.getId().getNamespace().equals(OpusVsExe.MOD_ID))
            .filter(recipe -> recipe.matches(inputs, player.level()))
            .map(recipe -> (Recipe<net.minecraft.world.inventory.CraftingContainer>) recipe)
            .findFirst();
    }

    @Override
    public void slotsChanged(Container container) {
        super.slotsChanged(container);
        if (player.level().isClientSide) return;
        Optional<Recipe<net.minecraft.world.inventory.CraftingContainer>> match = findRecipe();
        ItemStack output = match.map(recipe -> recipe.assemble(inputs, player.level().registryAccess())).orElse(ItemStack.EMPTY);
        match.ifPresent(result::setRecipeUsed);
        result.setItem(0, output);
        if (player instanceof ServerPlayer serverPlayer) {
            serverPlayer.connection.send(new net.minecraft.network.protocol.game.ClientboundContainerSetSlotPacket(
                containerId, incrementStateId(), 0, output));
        }
    }

    @Override public void removed(Player player) { super.removed(player); access.execute((level, pos) -> clearContainer(player, inputs)); }
    @Override public boolean stillValid(Player player) { return stillValid(access, player, ModBlocks.OPUS_ASSEMBLY_TABLE); }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = slots.get(index);
        if (!slot.hasItem()) return ItemStack.EMPTY;
        ItemStack stack = slot.getItem();
        ItemStack copy = stack.copy();
        if (index == 0) {
            if (!moveItemStackTo(stack, 26, 62, true)) return ItemStack.EMPTY;
            slot.onQuickCraft(stack, copy);
        } else if (index >= 26) {
            if (!moveItemStackTo(stack, 1, 26, false)) return ItemStack.EMPTY;
        } else if (!moveItemStackTo(stack, 26, 62, false)) return ItemStack.EMPTY;
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY); else slot.setChanged();
        if (stack.getCount() == copy.getCount()) return ItemStack.EMPTY;
        slot.onTake(player, stack);
        return copy;
    }

    private final class AssemblyResultSlot extends ResultSlot {
        private final Player player;
        private final TransientCraftingContainer inputs;
        private AssemblyResultSlot(Player player, TransientCraftingContainer inputs, ResultContainer result,
                                   int index, int x, int y) {
            super(player, inputs, result, index, x, y);
            this.player = player;
            this.inputs = inputs;
        }

        @Override
        public void onTake(Player player, ItemStack crafted) {
            if (player instanceof ServerPlayer serverPlayer) {
                findRecipe()
                    .ifPresent(recipe -> {
                        String recipeId = recipe.getId().getPath();
                        ChroniclesProgression.award(serverPlayer, "chronicles/route/recipes", recipeId);
                    });
            }
            checkTakeAchievements(crafted);
            NonNullList<ItemStack> remaining = findRecipe()
                .map(recipe -> recipe.getRemainingItems(inputs))
                .orElseGet(() -> NonNullList.withSize(inputs.getContainerSize(), ItemStack.EMPTY));
            for (int index = 0; index < remaining.size(); index++) {
                ItemStack input = inputs.getItem(index);
                ItemStack remainder = remaining.get(index);
                if (!input.isEmpty()) { inputs.removeItem(index, 1); input = inputs.getItem(index); }
                if (remainder.isEmpty()) continue;
                if (input.isEmpty()) inputs.setItem(index, remainder);
                else if (ItemStack.isSameItemSameTags(input, remainder)) { remainder.grow(input.getCount()); inputs.setItem(index, remainder); }
                else if (!this.player.getInventory().add(remainder)) this.player.drop(remainder, false);
            }
        }
    }
}
