package com.opus.fire.item;

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
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BonemealableBlock;
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
 * Vein Fire Hoe (registry id {@code fire_hoe}).
 *
 * <p>Same tier/stats as before (FireToolTier, -3, 0.0F, fire-resistant).
 * Contextual behavior, NO separate ability mode:
 * <ul>
 *   <li>clicked immature crop: ASHEN BLOOM matures a bounded 5x5 crop area
 *       (radius 2, no harvest/plant/hydration/drops, mature skipped);</li>
 *   <li>clicked tillable soil: ordinary 3x3 tilling (radius 1, same rules as
 *       a vanilla hoe);</li>
 *   <li>otherwise: PASS.</li>
 * </ul>
 * The growth cooldown applies ONLY to Ashen Bloom and never blocks tilling.
 */
public final class FireHoeItem extends HoeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_TILL = "till";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "bloom_cast";
    public static final String ANIM_EMBER = "ember_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation TILL = RawAnimation.begin().thenPlay(ANIM_TILL);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation EMBER = RawAnimation.begin().thenLoop(ANIM_EMBER);

    public static final int TILL_RADIUS = 1;
    public static final int TILL_SIZE = 3;
    public static final int TILL_MAX = 9;
    public static final int BLOOM_RADIUS = 2;
    public static final int BLOOM_SIZE = 5;
    public static final int BLOOM_MAX = 25;
    public static final int BLOOM_COOLDOWN_TICKS = 200;
    public static final int BLOOM_DURABILITY_COST = 2;
    private static final int GROWTH_MAX_ATTEMPTS = 16;
    private static final int SUCCESS_VFX_CAP = 9;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public FireHoeItem(Properties properties) {
        super(FireToolTier.INSTANCE, 0, 0.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<FireHoeItem> main =
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
            state -> state.setAndContinue(EMBER)));
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
        lines.add(Component.translatable("item.opusvsexe.fire_hoe.ability").withStyle(ChatFormatting.GOLD));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
        }
    }

    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        Vec3 look = player.getLookAngle();
        serverLevel.sendParticles(ParticleTypes.FLAME,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            3, 0.25, 0.25, 0.25, 0.04);
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
        if (isGrowthTarget(level, center)) {
            return ashenBloom(player, context, serverLevel, center);
        }
        if (context.getClickedFace() != Direction.UP || !isTillableCenter(level, center)) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        int successes = 0;
        int vfx = 0;
        for (int dx = -TILL_RADIUS; dx <= TILL_RADIUS && !stack.isEmpty(); dx++) {
            for (int dz = -TILL_RADIUS; dz <= TILL_RADIUS && !stack.isEmpty(); dz++) {
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

    static boolean isGrowthTarget(Level level, BlockPos center) {
        BlockState state = level.getBlockState(center);
        return state.getBlock() instanceof BonemealableBlock growable
            && growable.isValidBonemealTarget(level, center, state, false);
    }

    private InteractionResult ashenBloom(Player player, UseOnContext context, ServerLevel level, BlockPos center) {
        BlockState state = level.getBlockState(center);
        if (!(state.getBlock() instanceof BonemealableBlock growable)
                || !growable.isValidBonemealTarget(level, center, state, false)) {
            return InteractionResult.PASS;
        }
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        int grown = 0;
        for (int dx = -BLOOM_RADIUS; dx <= BLOOM_RADIUS && grown < BLOOM_MAX; dx++) {
            for (int dz = -BLOOM_RADIUS; dz <= BLOOM_RADIUS && grown < BLOOM_MAX; dz++) {
                for (int dy = 0; dy <= 1; dy++) {
                    BlockPos pos = center.offset(dx, dy, dz);
                    if (!level.getWorldBorder().isWithinBounds(pos) || !level.isLoaded(pos)) {
                        continue;
                    }
                    BlockState target = level.getBlockState(pos);
                    if (!(target.getBlock() instanceof BonemealableBlock plant)) {
                        continue;
                    }
                    int attempts = 0;
                    boolean advanced = false;
                    BlockState current = target;
                    while (attempts < GROWTH_MAX_ATTEMPTS && current.getBlock() instanceof BonemealableBlock g
                            && g.isValidBonemealTarget(level, pos, current, false)) {
                        g.performBonemeal(level, level.random, pos, current);
                        attempts++;
                        advanced = true;
                        current = level.getBlockState(pos);
                    }
                    if (advanced) {
                        grown++;
                        level.sendParticles(ParticleTypes.HAPPY_VILLAGER,
                            pos.getX() + 0.5, pos.getY() + 0.7, pos.getZ() + 0.5, 3, 0.3, 0.3, 0.3, 0.05);
                        level.sendParticles(ParticleTypes.FLAME,
                            pos.getX() + 0.5, pos.getY() + 0.7, pos.getZ() + 0.5, 2, 0.25, 0.25, 0.25, 0.03);
                    }
                }
            }
        }
        if (grown == 0) {
            return InteractionResult.PASS;
        }
        player.getCooldowns().addCooldown(this, BLOOM_COOLDOWN_TICKS);
        if (!player.isCreative()) {
            stack.hurtAndBreak(BLOOM_DURABILITY_COST, player, p -> p.broadcastBreakEvent(hand));
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, level), ANIM_CAST);
        level.playSound(null, center, SoundEvents.BONE_MEAL_USE, SoundSource.BLOCKS, 0.9F, 1.0F);
        return InteractionResult.sidedSuccess(false);
    }
}
