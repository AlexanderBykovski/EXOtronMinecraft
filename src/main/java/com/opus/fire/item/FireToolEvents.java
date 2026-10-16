package com.opus.fire.item;

import com.opus.fire.registry.FireItems;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class FireToolEvents {
    private static final TagKey<Block> ORES = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "ores"));
    private static final Map<ServerLevel, List<BlockPos>> PENDING_SMELTS = new IdentityHashMap<>();

    private FireToolEvents() { }

    public static void init() {
        PlayerBlockBreakEvents.AFTER.register((world, player, pos, state, blockEntity) -> {
            ItemStack tool = player.getMainHandItem();
            if (!tool.is(FireItems.FIRE_PICKAXE) || !state.is(ORES)
                    || EnchantmentHelper.getItemEnchantmentLevel(Enchantments.SILK_TOUCH, tool) > 0) {
                return;
            }
            if (world instanceof ServerLevel serverLevel) {
                scheduleSmelt(serverLevel, List.of(pos.immutable()));
            }
        });
        ServerTickEvents.END_WORLD_TICK.register(FireToolEvents::processPendingSmelts);
    }

    /** Queue smelt-rewrite for freshly popped drops (vein ability reuses this). */
    public static void scheduleSmelt(ServerLevel level, java.util.Collection<BlockPos> positions) {
        PENDING_SMELTS.computeIfAbsent(level, key -> new ArrayList<>()).addAll(positions);
    }

    private static void processPendingSmelts(ServerLevel world) {
        List<BlockPos> positions = PENDING_SMELTS.remove(world);
        if (positions == null || positions.isEmpty()) return;

        RegistryAccess access = world.registryAccess();
        Set<Integer> processedEntities = new HashSet<>();
        for (BlockPos pos : positions) {
            AABB drops = new AABB(pos).inflate(1.35D);
            for (ItemEntity itemEntity : world.getEntitiesOfClass(ItemEntity.class, drops,
                    entity -> entity.isAlive() && entity.getAge() <= 2
                            && entity.getOwner() == null
                            && processedEntities.add(entity.getId()))) {
                ItemStack source = itemEntity.getItem();
                world.getRecipeManager().getRecipeFor(RecipeType.SMELTING,
                        new SimpleContainer(source), world).ifPresent(recipe -> {
                    ItemStack result = recipe.getResultItem(access).copy();
                    if (!result.isEmpty()) {
                        int total = result.getCount() * source.getCount();
                        result.setCount(Math.min(result.getMaxStackSize(), total));
                        itemEntity.setItem(result);
                        int remaining = total - result.getCount();
                        while (remaining > 0) {
                            int count = Math.min(result.getMaxStackSize(), remaining);
                            ItemEntity overflow = new ItemEntity(world, itemEntity.getX(), itemEntity.getY(),
                                    itemEntity.getZ(), result.copyWithCount(count));
                            overflow.setDeltaMovement(itemEntity.getDeltaMovement());
                            world.addFreshEntity(overflow);
                            remaining -= count;
                        }
                    }
                });
            }
        }
    }
}
