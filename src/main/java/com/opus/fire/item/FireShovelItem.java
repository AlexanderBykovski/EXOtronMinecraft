package com.opus.fire.item;

import com.opus.item.ToolHarvest;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
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
 * Vein Fire Shovel (registry id {@code fire_shovel}).
 *
 * <p>Same tier/stats as before (FireToolTier, 1.5F, -3.0F, fire-resistant).
 * RMB ability INFERNAL EXCAVATION: a precise 5x5x1 plane centered on the
 * clicked block, oriented by the clicked face (top/bottom XZ, north/south
 * XY, east/west ZY); only shovel-mineable blocks break, with normal drops
 * and durability; never stone/ores/containers/bedrock.
 */
public final class FireShovelItem extends ShovelItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_DIG = "dig";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "excavate_cast";
    public static final String ANIM_EMBER = "ember_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation DIG = RawAnimation.begin().thenPlay(ANIM_DIG);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation EMBER = RawAnimation.begin().thenLoop(ANIM_EMBER);

    public static final int AREA_RADIUS = 2;
    public static final int AREA_SIZE = 5;
    public static final int MAX_CANDIDATES = 25;
    public static final int COOLDOWN_TICKS = 60;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public FireShovelItem(Properties properties) {
        super(FireToolTier.INSTANCE, 4.0F, -3.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<FireShovelItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_DIG, DIG);
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
        lines.add(Component.translatable("item.opusvsexe.fire_shovel.ability").withStyle(ChatFormatting.GOLD));
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
            4, 0.25, 0.25, 0.25, 0.04);
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
            if (diggable(level, center)) {
                fireTrigger(player, GeoItem.getId(context.getItemInHand()), ANIM_CAST);
                return InteractionResult.sidedSuccess(true);
            }
            return InteractionResult.PASS;
        }
        if (!(level instanceof ServerLevel serverLevel)) {
            return InteractionResult.PASS;
        }
        if (!diggable(level, center)) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        Direction face = context.getClickedFace();
        int broken = 0;
        for (int a = -AREA_RADIUS; a <= AREA_RADIUS && !stack.isEmpty(); a++) {
            for (int b = -AREA_RADIUS; b <= AREA_RADIUS && !stack.isEmpty(); b++) {
                BlockPos pos = planePos(center, face, a, b);
                if (!level.getWorldBorder().isWithinBounds(pos) || level.getBlockEntity(pos) != null
                        || !diggable(level, pos)) {
                    continue;
                }
                if (ToolHarvest.breakWithTool(serverLevel, pos, player, stack, hand)) {
                    broken++;
                } else {
                    break;
                }
            }
        }
        if (broken == 0) {
            return InteractionResult.PASS;
        }
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        level.playSound(null, center, SoundEvents.GRAVEL_BREAK, SoundSource.BLOCKS, 0.9F, 0.8F);
        serverLevel.sendParticles(ParticleTypes.LAVA,
            center.getX() + 0.5, center.getY() + 1.0, center.getZ() + 0.5, 4, 0.8, 0.5, 0.8, 0.0);
        return InteractionResult.sidedSuccess(false);
    }

    static BlockPos planePos(BlockPos center, Direction face, int a, int b) {
        return switch (face) {
            case UP, DOWN -> center.offset(a, 0, b);
            case NORTH, SOUTH -> center.offset(a, b, 0);
            case EAST, WEST -> center.offset(0, b, a);
        };
    }

    private static boolean diggable(Level level, BlockPos pos) {
        BlockState state = level.getBlockState(pos);
        return !state.isAir() && state.is(BlockTags.MINEABLE_WITH_SHOVEL);
    }
}
