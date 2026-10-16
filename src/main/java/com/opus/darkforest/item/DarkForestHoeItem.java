package com.opus.darkforest.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.stats.Stats;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import software.bernie.geckolib.animatable.GeoItem;
import software.bernie.geckolib.core.animatable.GeoAnimatable;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.network.GeckoLibNetwork;
import software.bernie.geckolib.network.packet.AnimTriggerPacket;
import software.bernie.geckolib.util.GeckoLibUtil;

import java.util.List;

/**
 * Dark Forest Hoe (registry id {@code dark_forest_hoe}).
 *
 * <p>Same tier/stats/tooltip/intrinsic as the tool it replaces
 * (DarkForestToolTier, -1, 0.0F, RARE). Contextual behavior, NO separate
 * ability item-mode:
 * <ul>
 *   <li>clicked farmland or a bonemeal-valid plant: NIGHT BLOOM — a bounded
 *       7x7 growth pulse (radius 3, Y and Y+1, one legitimate bonemeal attempt
 *       per plant, no harvest, no drops);</li>
 *   <li>clicked tillable dirt-type: normal vanilla single-block tilling
 *       ({@code super.useOn});</li>
 *   <li>otherwise: PASS.</li>
 * </ul>
 */
public final class DarkForestHoeItem extends HoeItem implements GeoAnimatable, DarkForestTools.ToolMarker {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_TILL = "till";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "bloom_cast";
    public static final String ANIM_GLOOM = "gloom_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation TILL = RawAnimation.begin().thenPlay(ANIM_TILL);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation GLOOM = RawAnimation.begin().thenLoop(ANIM_GLOOM);

    public static final int AREA_RADIUS = 1;
    public static final int AREA_SIZE = 3;
    public static final int MAX_CANDIDATES = 9;
    public static final int GROWTH_COOLDOWN_TICKS = 200;
    public static final int GROWTH_DURABILITY_COST = 1;
    private static final int SUCCESS_VFX_CAP = 9;
    private static final int GROWTH_MAX_ATTEMPTS = 16;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public DarkForestHoeItem(Properties properties) {
        super(DarkForestToolTier.INSTANCE, 0, 0.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<DarkForestHoeItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_TILL, TILL);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        main.triggerableAnim(ANIM_CAST, CAST);
        controllers.add(main);
        controllers.add(new AnimationController<>(this, CONTROLLER_FX, 5,
            state -> state.setAndContinue(GLOOM)));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object stack) {
        return System.nanoTime() / 50_000_000.0;
    }

    private void fireTrigger(Player player, long instanceId, String anim) {
        if (instanceId == Long.MAX_VALUE) {
            return;
        }
        if (player.level().isClientSide) {
            getAnimatableInstanceCache().getManagerForId(instanceId)
                .tryTriggerAnimation(CONTROLLER_MAIN, anim);
        } else {
            GeckoLibNetwork.sendToTrackingEntityAndSelf(
                new AnimTriggerPacket(getClass().toString(), instanceId, CONTROLLER_MAIN, anim), player);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> lines, TooltipFlag flag) {
        super.appendHoverText(stack, level, lines, flag);
        lines.add(Component.translatable("item.opusvsexe.dark_forest_tools.tier").withStyle(ChatFormatting.DARK_PURPLE));
        lines.add(Component.translatable("item.opusvsexe.dark_forest_tools.haste").withStyle(ChatFormatting.GREEN));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
            DarkForestEquipment.applyIntrinsic(stack);
        }
    }

    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        Vec3 look = player.getLookAngle();
        serverLevel.sendParticles(ParticleTypes.WITCH,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            3, 0.3, 0.3, 0.3, 0.05);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        Player player = context.getPlayer();
        BlockPos center = context.getClickedPos();
        if (player == null) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide) {
            if (isGrowthTarget(level, center)) {
                fireTrigger(player, GeoItem.getId(context.getItemInHand()), ANIM_CAST);
                return InteractionResult.sidedSuccess(true);
            }
            if (context.getClickedFace() == Direction.UP && isTillableCenter(level, center)) {
                fireTrigger(player, GeoItem.getId(context.getItemInHand()), ANIM_TILL);
                return InteractionResult.sidedSuccess(true);
            }
            return InteractionResult.PASS;
        }
        if (!(level instanceof ServerLevel serverLevel)) {
            return InteractionResult.PASS;
        }
        // PATH B first: planted crop -> instant growth (only path with a cooldown).
        if (isGrowthTarget(level, center)) {
            return tryGrow(player, context, serverLevel, center);
        }
        // PATH A: ordinary 3x3 tilling. NEVER gated by the growth cooldown.
        if (context.getClickedFace() != Direction.UP || !isTillableCenter(level, center)) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        int successes = 0;
        int vfx = 0;
        for (int dx = -AREA_RADIUS; dx <= AREA_RADIUS && !stack.isEmpty(); dx++) {
            for (int dz = -AREA_RADIUS; dz <= AREA_RADIUS && !stack.isEmpty(); dz++) {
                BlockPos pos = center.offset(dx, 0, dz);
                if (!level.getWorldBorder().isWithinBounds(pos)) {
                    continue;
                }
                BlockState state = level.getBlockState(pos);
                if (state.is(Blocks.FARMLAND)) {
                    continue;
                }
                com.opus.item.ToolHarvest.TillResult result = com.opus.item.ToolHarvest.tillTransform(
                    state, level.getBlockState(pos.above()).isAir());
                if (result == null) {
                    continue;
                }
                level.setBlock(pos, result.state(), 3);
                if (result.dropRoots()) {
                    Block.popResource(level, pos, new ItemStack(Items.HANGING_ROOTS));
                }
                stack.hurtAndBreak(1, player, p -> p.broadcastBreakEvent(hand));
                successes++;
                if (vfx < SUCCESS_VFX_CAP) {
                    vfx++;
                    serverLevel.sendParticles(ParticleTypes.END_ROD,
                        pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5,
                        1, 0.1, 0.15, 0.1, 0.02);
                }
            }
        }
        if (successes == 0) {
            return InteractionResult.PASS;
        }
        level.playSound(null, center, SoundEvents.HOE_TILL, SoundSource.BLOCKS, 1.0F, 1.0F);
        player.awardStat(Stats.ITEM_USED.get(this));
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_TILL);
        return InteractionResult.sidedSuccess(false);
    }

    private static boolean isTillableCenter(Level level, BlockPos center) {
        return com.opus.item.ToolHarvest.tillTransform(level.getBlockState(center),
            level.getBlockState(center.above()).isAir()) != null;
    }

    /** Clicked block itself is a bonemeal-valid plant. */
    static boolean isGrowthTarget(Level level, BlockPos center) {
        BlockState state = level.getBlockState(center);
        return state.getBlock() instanceof BonemealableBlock growable
            && growable.isValidBonemealTarget(level, center, state, false);
    }

    /**
     * Instant full-maturity growth: bounded legitimate performBonemeal loop
     * (no harvest, no planting). Cooldown + durability ONLY on success;
     * mature/invalid targets fall through untouched.
     */
    private InteractionResult tryGrow(Player player, UseOnContext context, ServerLevel level, BlockPos pos) {
        BlockState state = level.getBlockState(pos);
        if (!(state.getBlock() instanceof BonemealableBlock growable)
                || !growable.isValidBonemealTarget(level, pos, state, false)) {
            return InteractionResult.PASS;
        }
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        int attempts = 0;
        BlockState current = level.getBlockState(pos);
        while (attempts < GROWTH_MAX_ATTEMPTS && current.getBlock() instanceof BonemealableBlock g
                && g.isValidBonemealTarget(level, pos, current, false)) {
            g.performBonemeal(level, level.random, pos, current);
            attempts++;
            current = level.getBlockState(pos);
        }
        if (attempts == 0) {
            return InteractionResult.PASS;
        }
        player.getCooldowns().addCooldown(this, GROWTH_COOLDOWN_TICKS);
        if (!player.isCreative()) {
            stack.hurtAndBreak(GROWTH_DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, level), ANIM_CAST);
        level.playSound(null, pos, SoundEvents.BONE_MEAL_USE, SoundSource.BLOCKS, 0.9F, 1.1F);
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER,
            pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, 6, 0.4, 0.4, 0.4, 0.05);
        level.sendParticles(ParticleTypes.WITCH,
            pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, 4, 0.3, 0.4, 0.3, 0.03);
        return InteractionResult.sidedSuccess(false);
    }
}
