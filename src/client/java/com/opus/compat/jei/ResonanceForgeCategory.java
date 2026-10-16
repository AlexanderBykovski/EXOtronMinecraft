package com.opus.compat.jei;

import com.opus.OpusVsExe;
import com.opus.registry.ModBlocks;
import com.opus.registry.ModItems;
import mezz.jei.api.constants.VanillaTypes;
import mezz.jei.api.gui.builder.IRecipeLayoutBuilder;
import mezz.jei.api.gui.drawable.IDrawable;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.IFocusGroup;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.recipe.RecipeType;
import mezz.jei.api.recipe.category.IRecipeCategory;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

import java.util.List;

/** JEI view of the hard-coded one-item Resonance Forge transformations. */
public final class ResonanceForgeCategory implements IRecipeCategory<ResonanceForgeCategory.Recipe> {
    public static final RecipeType<Recipe> TYPE =
            RecipeType.create(OpusVsExe.MOD_ID, "resonance_forging", Recipe.class);

    private final IDrawable background;
    private final IDrawable icon;

    public ResonanceForgeCategory(IGuiHelper guiHelper) {
        background = guiHelper.createBlankDrawable(80, 36);
        icon = guiHelper.createDrawableIngredient(VanillaTypes.ITEM_STACK,
                new ItemStack(ModBlocks.RESONANCE_FORGE));
    }

    @Override
    public RecipeType<Recipe> getRecipeType() {
        return TYPE;
    }

    @Override
    public Component getTitle() {
        return Component.translatable("jei.opusvsexe.resonance_forge");
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
    public void setRecipe(IRecipeLayoutBuilder builder, Recipe recipe, IFocusGroup focuses) {
        builder.addSlot(RecipeIngredientRole.INPUT, 8, 10)
                .setStandardSlotBackground()
                .addItemStack(recipe.input());
        builder.addSlot(RecipeIngredientRole.OUTPUT, 56, 10)
                .setOutputSlotBackground()
                .addItemStack(recipe.output());
    }

    public record Recipe(ItemStack input, ItemStack output) { }

    public static List<Recipe> recipes() {
        return List.of(
                new Recipe(new ItemStack(ModItems.RAW_OPUS), new ItemStack(ModItems.STABILIZED_OPUS)),
                new Recipe(new ItemStack(ModItems.STABILIZED_OPUS), new ItemStack(ModItems.RESONANT_OPUS)),
                new Recipe(new ItemStack(ModItems.RESONANT_OPUS), new ItemStack(ModItems.CORE_OPUS))
        );
    }
}
