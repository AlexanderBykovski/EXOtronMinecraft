package com.opus.registry;

import com.opus.OpusVsExe;
import com.opus.recipe.OpusAssemblyRecipe;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;

public final class ModRecipes {
    public static final RecipeType<OpusAssemblyRecipe> ASSEMBLY = Registry.register(
        BuiltInRegistries.RECIPE_TYPE, OpusVsExe.id("assembly"), new RecipeType<>() {
            @Override public String toString() { return "opusvsexe:assembly"; }
        });
    public static final RecipeSerializer<OpusAssemblyRecipe> ASSEMBLY_SERIALIZER = Registry.register(
        BuiltInRegistries.RECIPE_SERIALIZER, OpusVsExe.id("assembly"), new OpusAssemblyRecipe.Serializer());

    private ModRecipes() { }
    public static void init() { }
}
