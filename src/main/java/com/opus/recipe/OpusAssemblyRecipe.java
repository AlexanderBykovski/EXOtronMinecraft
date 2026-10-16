package com.opus.recipe;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.opus.registry.ModRecipes;
import net.minecraft.core.NonNullList;
import net.minecraft.core.RegistryAccess;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;

import java.util.Map;
import java.util.HashMap;

/** A shaped recipe whose design space is the full 5x5 Opus assembly table. */
public final class OpusAssemblyRecipe implements Recipe<CraftingContainer> {
    private final ResourceLocation id;
    private final String group;
    private final int width;
    private final int height;
    private final NonNullList<Ingredient> ingredients;
    private final ItemStack result;
    private final boolean shapeless;

    public OpusAssemblyRecipe(ResourceLocation id, String group, int width, int height,
                              NonNullList<Ingredient> ingredients, ItemStack result, boolean shapeless) {
        this.id = id;
        this.group = group;
        this.width = width;
        this.height = height;
        this.ingredients = ingredients;
        this.result = result;
        this.shapeless = shapeless;
    }

    @Override
    public boolean matches(CraftingContainer container, Level level) {
        if (shapeless) return matchesShapeless(container);
        if (container.getWidth() < width || container.getHeight() < height) return false;
        for (int offsetY = 0; offsetY <= container.getHeight() - height; offsetY++) {
            for (int offsetX = 0; offsetX <= container.getWidth() - width; offsetX++) {
                if (matchesAt(container, offsetX, offsetY, false) || matchesAt(container, offsetX, offsetY, true)) return true;
            }
        }
        return false;
    }

    private boolean matchesShapeless(CraftingContainer container) {
        int occupied = 0;
        for (int i = 0; i < container.getContainerSize(); i++) {
            if (!container.getItem(i).isEmpty()) occupied++;
        }
        if (occupied != ingredients.size()) return false;
        boolean[] used = new boolean[ingredients.size()];
        return matchShapelessSlot(container, 0, used);
    }

    private boolean matchShapelessSlot(CraftingContainer container, int slot, boolean[] used) {
        while (slot < container.getContainerSize() && container.getItem(slot).isEmpty()) slot++;
        if (slot >= container.getContainerSize()) return true;
        ItemStack stack = container.getItem(slot);
        for (int ingredientIndex = 0; ingredientIndex < ingredients.size(); ingredientIndex++) {
            if (!used[ingredientIndex] && ingredients.get(ingredientIndex).test(stack)) {
                used[ingredientIndex] = true;
                if (matchShapelessSlot(container, slot + 1, used)) return true;
                used[ingredientIndex] = false;
            }
        }
        return false;
    }

    private boolean matchesAt(CraftingContainer container, int offsetX, int offsetY, boolean mirrored) {
        for (int y = 0; y < container.getHeight(); y++) {
            for (int x = 0; x < container.getWidth(); x++) {
                int patternX = x - offsetX;
                int patternY = y - offsetY;
                Ingredient expected = Ingredient.EMPTY;
                if (patternX >= 0 && patternX < width && patternY >= 0 && patternY < height) {
                    int sourceX = mirrored ? width - patternX - 1 : patternX;
                    expected = ingredients.get(sourceX + patternY * width);
                }
                ItemStack actual = container.getItem(x + y * container.getWidth());
                if (expected.isEmpty() ? !actual.isEmpty() : !expected.test(actual)) return false;
            }
        }
        return true;
    }

    @Override public ItemStack assemble(CraftingContainer container, RegistryAccess access) { return result.copy(); }
    @Override public boolean canCraftInDimensions(int width, int height) { return width >= this.width && height >= this.height; }
    @Override public ItemStack getResultItem(RegistryAccess access) { return result; }
    @Override public NonNullList<ItemStack> getRemainingItems(CraftingContainer container) {
        NonNullList<ItemStack> remaining = NonNullList.withSize(container.getContainerSize(), ItemStack.EMPTY);
        for (int index = 0; index < container.getContainerSize(); index++) {
            ItemStack stack = container.getItem(index);
            if (!stack.isEmpty() && stack.getItem().getCraftingRemainingItem() != null) {
                remaining.set(index, new ItemStack(stack.getItem().getCraftingRemainingItem()));
            }
        }
        return remaining;
    }
    @Override public NonNullList<Ingredient> getIngredients() { return ingredients; }
    public int getWidth() { return width; }
    public int getHeight() { return height; }
    public boolean isShapeless() { return shapeless; }
    @Override public String getGroup() { return group; }
    @Override public ResourceLocation getId() { return id; }
    @Override public RecipeSerializer<?> getSerializer() { return ModRecipes.ASSEMBLY_SERIALIZER; }
    @Override public RecipeType<?> getType() { return ModRecipes.ASSEMBLY; }

    public static final class Serializer implements RecipeSerializer<OpusAssemblyRecipe> {
        private OpusAssemblyRecipe fromShapedJson(ResourceLocation id, JsonObject json) {
            JsonArray patternJson = GsonHelper.getAsJsonArray(json, "pattern");
            if (patternJson.size() == 0 || patternJson.size() > 5) throw new IllegalArgumentException("Assembly pattern height must be 1..5");
            int height = patternJson.size();
            String[] pattern = new String[height];
            int width = -1;
            for (int i = 0; i < height; i++) {
                pattern[i] = GsonHelper.convertToString(patternJson.get(i), "pattern[" + i + "]");
                if (pattern[i].isEmpty() || pattern[i].length() > 5) throw new IllegalArgumentException("Assembly pattern width must be 1..5");
                if (width == -1) width = pattern[i].length();
                if (pattern[i].length() != width) throw new IllegalArgumentException("Assembly pattern rows must have equal width");
            }
            Map<Character, Ingredient> key = new HashMap<>();
            for (Map.Entry<String, JsonElement> entry : GsonHelper.getAsJsonObject(json, "key").entrySet()) {
                if (entry.getKey().length() != 1) throw new IllegalArgumentException("Assembly key must be one character");
                key.put(entry.getKey().charAt(0), Ingredient.fromJson(entry.getValue(), false));
            }
            NonNullList<Ingredient> ingredients = NonNullList.withSize(width * height, Ingredient.EMPTY);
            for (int y = 0; y < height; y++) {
                for (int x = 0; x < width; x++) {
                    char symbol = pattern[y].charAt(x);
                    if (symbol != ' ') {
                        Ingredient ingredient = key.get(symbol);
                        if (ingredient == null) throw new IllegalArgumentException("Unknown assembly key: " + symbol);
                        ingredients.set(x + y * width, ingredient);
                    }
                }
            }
            ItemStack result = net.minecraft.world.item.crafting.ShapedRecipe.itemStackFromJson(GsonHelper.getAsJsonObject(json, "result"));
            return new OpusAssemblyRecipe(id, GsonHelper.getAsString(json, "group", ""), width, height, ingredients, result, false);
        }

        private OpusAssemblyRecipe fromShapelessJson(ResourceLocation id, JsonObject json) {
            JsonArray ingredientsJson = GsonHelper.getAsJsonArray(json, "ingredients");
            if (ingredientsJson.size() == 0 || ingredientsJson.size() > 25) {
                throw new IllegalArgumentException("Assembly shapeless recipe must contain 1..25 ingredients");
            }
            NonNullList<Ingredient> ingredients = NonNullList.withSize(ingredientsJson.size(), Ingredient.EMPTY);
            for (int i = 0; i < ingredientsJson.size(); i++) {
                ingredients.set(i, Ingredient.fromJson(ingredientsJson.get(i), false));
            }
            ItemStack result = net.minecraft.world.item.crafting.ShapedRecipe.itemStackFromJson(GsonHelper.getAsJsonObject(json, "result"));
            return new OpusAssemblyRecipe(id, GsonHelper.getAsString(json, "group", ""), ingredients.size(), 1, ingredients, result, true);
        }

        @Override
        public OpusAssemblyRecipe fromJson(ResourceLocation id, JsonObject json) {
            return json.has("pattern") ? fromShapedJson(id, json) : fromShapelessJson(id, json);
        }

        @Override
        public OpusAssemblyRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buffer) {
            int width = buffer.readVarInt();
            int height = buffer.readVarInt();
            boolean shapeless = buffer.readBoolean();
            String group = buffer.readUtf();
            NonNullList<Ingredient> ingredients = NonNullList.withSize(width * height, Ingredient.EMPTY);
            for (int i = 0; i < ingredients.size(); i++) ingredients.set(i, Ingredient.fromNetwork(buffer));
            ItemStack result = buffer.readItem();
            return new OpusAssemblyRecipe(id, group, width, height, ingredients, result, shapeless);
        }

        @Override
        public void toNetwork(FriendlyByteBuf buffer, OpusAssemblyRecipe recipe) {
            buffer.writeVarInt(recipe.width);
            buffer.writeVarInt(recipe.height);
            buffer.writeBoolean(recipe.shapeless);
            buffer.writeUtf(recipe.group);
            for (Ingredient ingredient : recipe.ingredients) ingredient.toNetwork(buffer);
            buffer.writeItem(recipe.result);
        }
    }
}
