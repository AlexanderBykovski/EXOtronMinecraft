package com.opus.compat.jei;

import com.opus.OpusVsExe;
import com.opus.client.screen.OpusAssemblyScreen;
import com.opus.inventory.OpusAssemblyMenu;
import com.opus.recipe.OpusAssemblyRecipe;
import com.opus.paradise.inventory.ParthenonForgeMenu;
import com.opus.paradise.registry.ParadiseBlocks;
import com.opus.paradise.registry.ParadiseMenus;
import com.opus.paradise.registry.ParadiseRecipes;
import com.opus.registry.ModBlocks;
import com.opus.registry.ModMenus;
import com.opus.registry.ModRecipes;
import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.registration.IGuiHandlerRegistration;
import mezz.jei.api.registration.IRecipeCatalystRegistration;
import mezz.jei.api.registration.IRecipeCategoryRegistration;
import mezz.jei.api.registration.IRecipeRegistration;
import mezz.jei.api.registration.IRecipeTransferRegistration;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.crafting.RecipeManager;

/**
 * Shows the mod's custom assembly, forge and resonance recipes in JEI.
 * Loaded through the {@code jei_mod_plugin} entrypoint only when JEI is installed.
 */
@JeiPlugin
public final class OpusJeiPlugin implements IModPlugin {
    @Override
    public ResourceLocation getPluginUid() {
        return new ResourceLocation(OpusVsExe.MOD_ID, "assembly");
    }

    @Override
    public void registerCategories(IRecipeCategoryRegistration registration) {
        registration.addRecipeCategories(
            new AssemblyCategory(registration.getJeiHelpers().getGuiHelper()),
            new ParthenonForgeCategory(registration.getJeiHelpers().getGuiHelper()),
            new ResonanceForgeCategory(registration.getJeiHelpers().getGuiHelper()));
    }

    @Override
    public void registerRecipes(IRecipeRegistration registration) {
        Minecraft minecraft = Minecraft.getInstance();
        registration.addRecipes(ResonanceForgeCategory.TYPE, ResonanceForgeCategory.recipes());
        RecipeManager recipeManager = minecraft.getConnection() != null
                ? minecraft.getConnection().getRecipeManager()
                : minecraft.level != null ? minecraft.level.getRecipeManager() : null;
        if (recipeManager == null) return;
        registration.addRecipes(AssemblyCategory.TYPE,
                recipeManager.getAllRecipesFor(ModRecipes.ASSEMBLY));
        registration.addRecipes(ParthenonForgeCategory.TYPE,
                recipeManager.getAllRecipesFor(ParadiseRecipes.PARTHENON_FORGING));
    }

    @Override
    public void registerRecipeCatalysts(IRecipeCatalystRegistration registration) {
        registration.addRecipeCatalyst(ModBlocks.OPUS_ASSEMBLY_TABLE, AssemblyCategory.TYPE);
        registration.addRecipeCatalyst(ParadiseBlocks.PARTHENON_FORGE, ParthenonForgeCategory.TYPE);
        registration.addRecipeCatalyst(ModBlocks.RESONANCE_FORGE, ResonanceForgeCategory.TYPE);
    }

    @Override
    public void registerRecipeTransferHandlers(IRecipeTransferRegistration registration) {
        // Menu slots: 0 = result, 1-25 = 5x5 matrix, 26-61 = player inventory.
        registration.addRecipeTransferHandler(OpusAssemblyMenu.class, ModMenus.OPUS_ASSEMBLY_TABLE,
            AssemblyCategory.TYPE, 1, 25, 26, 36);
        registration.addRecipeTransferHandler(ParthenonForgeMenu.class, ParadiseMenus.PARTHENON_FORGE,
                ParthenonForgeCategory.TYPE, 1, 9, 10, 36);
    }

    @Override
    public void registerGuiHandlers(IGuiHandlerRegistration registration) {
        // Neutral strip between the 5x5 matrix and the result slot: plain clicks do nothing there.
        registration.addRecipeClickArea(OpusAssemblyScreen.class, 139, 46, 32, 21, AssemblyCategory.TYPE);
        registration.addRecipeClickArea(com.opus.paradise.client.screen.ParthenonForgeScreen.class,
                89, 27, 31, 23, ParthenonForgeCategory.TYPE);
    }
}
