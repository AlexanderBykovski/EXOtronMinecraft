package com.opus.compat.jei;

import com.opus.OpusVsExe;
import com.opus.paradise.recipe.ParthenonForgingRecipe;
import com.opus.paradise.registry.ParadiseBlocks;
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

/** JEI view of the 3x3 Parthenon Forge recipes. */
public final class ParthenonForgeCategory implements IRecipeCategory<ParthenonForgingRecipe> {
    public static final RecipeType<ParthenonForgingRecipe> TYPE =
            RecipeType.create(OpusVsExe.MOD_ID, "parthenon_forging", ParthenonForgingRecipe.class);
    private static final int SLOT = 18;
    private static final int OUTPUT_X = 81;
    private static final int OUTPUT_Y = 19;

    private final IDrawable background;
    private final IDrawable icon;

    public ParthenonForgeCategory(IGuiHelper guiHelper) {
        background = guiHelper.createBlankDrawable(OUTPUT_X + SLOT + 1, 3 * SLOT + 2);
        icon = guiHelper.createDrawableIngredient(VanillaTypes.ITEM_STACK,
                new ItemStack(ParadiseBlocks.PARTHENON_FORGE));
    }

    @Override
    public RecipeType<ParthenonForgingRecipe> getRecipeType() {
        return TYPE;
    }

    @Override
    public Component getTitle() {
        return Component.translatable("jei.opusvsexe.parthenon_forge");
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
    public void setRecipe(IRecipeLayoutBuilder builder, ParthenonForgingRecipe recipe, IFocusGroup focuses) {
        List<Ingredient> ingredients = recipe.getIngredients();
        for (int y = 0; y < recipe.getHeight(); y++) {
            for (int x = 0; x < recipe.getWidth(); x++) {
                Ingredient ingredient = ingredients.get(x + y * recipe.getWidth());
                IRecipeSlotBuilder slot = builder.addSlot(RecipeIngredientRole.INPUT,
                                1 + x * SLOT, 1 + y * SLOT)
                        .setStandardSlotBackground();
                if (!ingredient.isEmpty()) slot.addIngredients(ingredient);
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
