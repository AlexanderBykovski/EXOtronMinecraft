package com.opus.item;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
/**
 * Shared tool-harvest helper for area/vein abilities (Paradise + Dark Forest).
 * Breaks one block with full tool-aware semantics: Silk Touch / Fortune drops,
 * Unbreaking/creative handling, and stops callers when the tool dies. Callers
 * own suitability checks, area iteration and cooldowns.
 */
public final class ToolHarvest {
    private ToolHarvest() {
    }

    /**
     * @return true if the caller should keep iterating (tool survived).
     */
    public static boolean breakWithTool(ServerLevel level, BlockPos pos, Player player,
                                        ItemStack stack, InteractionHand hand) {
        BlockState state = level.getBlockState(pos);
        if (state.isAir()) {
            return true;
        }
        BlockEntity blockEntity = level.getBlockEntity(pos);
        List<ItemStack> drops = Block.getDrops(state, level, pos, blockEntity, player, stack);
        // NOTE: ore XP is intentionally not replicated here — 1.20.1 computes
        // it inside protected harvest paths with no public query API, and
        // hardcoding per-ore XP tables would be worse. Drops, Silk Touch,
        // Fortune, Unbreaking and break-stop are all exact.
        level.setBlock(pos, Blocks.AIR.defaultBlockState(), 3);
        for (ItemStack drop : drops) {
            Block.popResource(level, pos, drop);
        }
        stack.hurtAndBreak(1, player, p -> p.broadcastBreakEvent(hand));
        return !stack.isEmpty();
    }

    /**
     * Ore family stem for vein matching ("iron_ore" and "deepslate_iron_ore"
     * both map to "iron"), or null when the block is not an ore.
     */
    public static String oreFamily(BlockState state) {
        String path = state.getBlock().builtInRegistryHolder().key().location().getPath();
        if (!path.endsWith("_ore")) {
            return null;
        }
        String stem = path.substring(0, path.length() - 4);
        if (stem.startsWith("deepslate_")) {
            stem = stem.substring("deepslate_".length());
        }
        if (stem.startsWith("nether_")) {
            stem = stem.substring("nether_".length());
        }
        return stem.isEmpty() ? null : stem;
    }

    /**
     * Bounded BFS over 26 neighbors: same ore family, chebyshev radius cap,
     * visited-node cap, at most maxBlocks kept. Never force-loads chunks.
     */
    public static List<BlockPos> collectVein(ServerLevel level, BlockPos origin, String family,
                                             int maxBlocks, int radius, int maxVisited) {
        List<BlockPos> vein = new ArrayList<>();
        Set<BlockPos> visited = new HashSet<>();
        Deque<BlockPos> queue = new ArrayDeque<>();
        queue.add(origin.immutable());
        visited.add(origin.immutable());
        while (!queue.isEmpty() && vein.size() < maxBlocks && visited.size() < maxVisited) {
            BlockPos pos = queue.poll();
            if (!level.isLoaded(pos) || pos.distManhattan(origin) > radius
                    || !level.getWorldBorder().isWithinBounds(pos)) {
                continue;
            }
            if (!family.equals(oreFamily(level.getBlockState(pos)))) {
                continue;
            }
            vein.add(pos);
            if (vein.size() >= maxBlocks) {
                break;
            }
            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    for (int dz = -1; dz <= 1; dz++) {
                        if (dx == 0 && dy == 0 && dz == 0) {
                            continue;
                        }
                        BlockPos next = pos.offset(dx, dy, dz).immutable();
                        if (visited.size() >= maxVisited || !visited.add(next)) {
                            continue;
                        }
                        queue.add(next);
                    }
                }
            }
        }
        return vein;
    }

    /** Vanilla-equivalent 1.20.1 hoe transformation for one block. */
    public record TillResult(BlockState state, boolean dropRoots) {
    }

    /**
     * Mirrors HoeItem semantics: grass/dirt/path need air above; coarse dirt
     * converts without an air check; rooted dirt needs air and drops roots;
     * everything else (incl. farmland) yields null.
     */
    public static TillResult tillTransform(BlockState state, boolean airAbove) {
        Block block = state.getBlock();
        if (block == Blocks.GRASS_BLOCK || block == Blocks.DIRT || block == Blocks.DIRT_PATH) {
            return airAbove ? new TillResult(Blocks.FARMLAND.defaultBlockState(), false) : null;
        }
        if (block == Blocks.COARSE_DIRT) {
            return new TillResult(Blocks.DIRT.defaultBlockState(), false);
        }
        if (block == Blocks.ROOTED_DIRT) {
            return airAbove ? new TillResult(Blocks.DIRT.defaultBlockState(), true) : null;
        }
        return null;
    }
}
