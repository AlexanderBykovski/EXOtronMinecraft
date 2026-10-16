package com.opus.paradise.item;

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
 * Parthenon Hoe — the celestial tilling relic (registry id {@code parthenon_hoe}).
 *
 * <p>Gameplay parity with the tool it replaces: same {@link ParthenonToolTier},
 * same hoe damage/speed ({@code -3}/{@code 0.0F}), same intrinsic Efficiency
 * application and tooltip. One intrinsic upgrade, and ONLY one:
 * <ul>
 *   <li>normal hoe use tills a <b>7x7</b> square (radius 3, same Y, max 49
 *       candidates) instead of one block. No cooldown, no buff, no damage.</li>
 * </ul>
 *
 * <p>Every candidate is validated with vanilla-equivalent 1.20.1 hoe rules
 * (air above, known transformations only); farmland, crops above it, and
 * invalid blocks are skipped; durability costs 1 per SUCCESS via
 * {@code hurtAndBreak} (Unbreaking/creative/break-stop behave natively).
 * Server-authoritative; one sound, bounded VFX, one stat per use.
 *
 * <p>Rendering follows the project rule (M2): plain {@link GeoAnimatable} +
 * vanilla baked-model path, never {@code GeoItem}.
 */
public final class ParthenonHoeItem extends HoeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_TILL = "till";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_GEM_PULSE = "gem_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation TILL = RawAnimation.begin().thenPlay(ANIM_TILL);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation GEM_PULSE = RawAnimation.begin().thenLoop(ANIM_GEM_PULSE);

    public static final int AREA_RADIUS = 3;
    public static final int AREA_DIAMETER = 7;
    public static final int MAX_CANDIDATES = 49;
    private static final int SUCCESS_VFX_CAP = 24;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ParthenonHoeItem(Properties properties) {
        super(ParthenonToolTier.INSTANCE, 0, 0.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<ParthenonHoeItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_TILL, TILL);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        controllers.add(main);
        controllers.add(new AnimationController<>(this, CONTROLLER_FX, 5,
            state -> state.setAndContinue(GEM_PULSE)));
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
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.efficiency").withStyle(ChatFormatting.AQUA));
        lines.add(Component.translatable("item.opusvsexe.parthenon_tools.repair").withStyle(ChatFormatting.DARK_PURPLE));
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        super.inventoryTick(stack, level, entity, slot, selected);
        if (!level.isClientSide && level instanceof ServerLevel serverLevel) {
            GeoItem.getOrAssignId(stack, serverLevel);
            ParadiseEquipment.applyIntrinsic(stack);
        }
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos center = context.getClickedPos();
        Player player = context.getPlayer();
        if (player == null || context.getClickedFace() != Direction.UP) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide) {
            com.opus.item.ToolHarvest.TillResult preview = com.opus.item.ToolHarvest.tillTransform(level.getBlockState(center),
                level.getBlockState(center.above()).isAir());
            if (preview != null) {
                fireTrigger(player, GeoItem.getId(context.getItemInHand()), ANIM_TILL);
                return InteractionResult.sidedSuccess(true);
            }
            return InteractionResult.PASS;
        }
        if (!(level instanceof ServerLevel serverLevel)) {
            return InteractionResult.PASS;
        }
        com.opus.item.ToolHarvest.TillResult centerResult = com.opus.item.ToolHarvest.tillTransform(level.getBlockState(center),
            level.getBlockState(center.above()).isAir());
        if (centerResult == null) {
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
                com.opus.item.ToolHarvest.TillResult result = com.opus.item.ToolHarvest.tillTransform(state, level.getBlockState(pos.above()).isAir());
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
        serverLevel.sendParticles(ParticleTypes.FIREWORK,
            center.getX() + 0.5, center.getY() + 1.0, center.getZ() + 0.5,
            4, 0.5, 0.3, 0.5, 0.05);
        player.awardStat(Stats.ITEM_USED.get(this));
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_TILL);
        return InteractionResult.sidedSuccess(false);
    }

    /**
     * Server-side entity-hit hook, called from the player attack mixin.
     * Restrained: small spark cluster, tiny flash. No area effect, ever.
     */
    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_ATTACK);
        level.playSound(null, player.blockPosition(), com.opus.sound.ModSounds.HAMMER_HIT,
            SoundSource.PLAYERS, 0.45F, 1.1F);
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py, pz, 2, 0.2, 0.2, 0.2, 0.04);
        serverLevel.sendParticles(ParticleTypes.END_ROD, px, py, pz, 3, 0.25, 0.25, 0.25, 0.04);
    }
}
