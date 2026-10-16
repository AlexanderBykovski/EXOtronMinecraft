package com.opus.compat.jei;

import com.opus.OpusVsExe;
import com.opus.recipe.OpusAssemblyRecipe;
import com.opus.registry.ModBlocks;
import mezz.jei.api.constants.VanillaTypes;
import mezz.jei.api.gui.builder.IRecipeLayoutBuilder;
import mezz.jei.api.gui.builder.IRecipeSlotBuilder;
import mezz.jei.api.gui.drawable.IDrawable;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.IFocusGroup;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.recipe.RecipeType;
import mezz.jei.api.recipe.category.IRecipeCategory;
import net.minecraft.client.Minecraft;
import net.minecraft.core.RegistryAccess;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.List;

/** JEI view of the 5x5 Opus assembly table: full matrix plus result. */
public final class AssemblyCategory implements IRecipeCategory<OpusAssemblyRecipe> {
    public static final RecipeType<OpusAssemblyRecipe> TYPE =
        RecipeType.create(OpusVsExe.MOD_ID, "assembly", OpusAssemblyRecipe.class);
    private static final int SLOT = 18;
    private static final int GRID_X = 1;
    private static final int GRID_Y = 1;
    private static final int OUTPUT_X = 99;
    private static final int OUTPUT_Y = 37;

    private final IDrawable background;
    private final IDrawable icon;

    public AssemblyCategory(IGuiHelper guiHelper) {
        background = guiHelper.createBlankDrawable(OUTPUT_X + SLOT + 1, 5 * SLOT + 2);
        icon = guiHelper.createDrawableIngredient(VanillaTypes.ITEM_STACK,
            new ItemStack(ModBlocks.OPUS_ASSEMBLY_TABLE));
    }

    @Override
    public RecipeType<OpusAssemblyRecipe> getRecipeType() {
        return TYPE;
    }

    @Override
    public Component getTitle() {
        return Component.translatable("jei.opusvsexe.assembly");
    }

    @Override
    public IDrawable getBackground() {
        return background;
    }

    @Override
    public IDrawable getIcon() {
        return icon;
    }

    @Override
    public void setRecipe(IRecipeLayoutBuilder builder, OpusAssemblyRecipe recipe, IFocusGroup focuses) {
        if (recipe.isShapeless()) {
            builder.setShapeless();
            List<Ingredient> ingredients = recipe.getIngredients();
            for (int i = 0; i < ingredients.size(); i++) {
                Ingredient ingredient = ingredients.get(i);
                IRecipeSlotBuilder slot = builder.addSlot(RecipeIngredientRole.INPUT,
                        GRID_X + (i % 5) * SLOT, GRID_Y + (i / 5) * SLOT)
                    .setStandardSlotBackground();
                if (!ingredient.isEmpty()) slot.addIngredients(ingredient);
            }
        } else {
            List<Ingredient> ingredients = recipe.getIngredients();
            for (int y = 0; y < recipe.getHeight(); y++) {
                for (int x = 0; x < recipe.getWidth(); x++) {
                    Ingredient ingredient = ingredients.get(x + y * recipe.getWidth());
                    IRecipeSlotBuilder slot = builder.addSlot(RecipeIngredientRole.INPUT,
                            GRID_X + x * SLOT, GRID_Y + y * SLOT)
                        .setStandardSlotBackground();
                    if (!ingredient.isEmpty()) slot.addIngredients(ingredient);
                }
            }
        }
        builder.addSlot(RecipeIngredientRole.OUTPUT, OUTPUT_X, OUTPUT_Y)
            .setOutputSlotBackground()
            .addIngredients(VanillaTypes.ITEM_STACK,
                List.of(recipe.getResultItem(registryAccess())));
    }

    private static RegistryAccess registryAccess() {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.getConnection() != null) return minecraft.getConnection().registryAccess();
        if (minecraft.level != null) return minecraft.level.registryAccess();
        return RegistryAccess.EMPTY;
    }
}
