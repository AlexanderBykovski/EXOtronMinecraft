package com.opus.fire.item;

import com.opus.item.ToolHarvest;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import com.opus.fire.sound.FireSounds;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.PickaxeItem;
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

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Vein Fire Pickaxe (registry id {@code fire_pickaxe}).
 *
 * <p>Keeps the old tooltip. RMB ability MAGMA VEIN / FORGEHEART EXTRACTION:
 * right-click a harvestable ore to BFS-harvest its connected vein (same ore
 * family stem, radius 8, 26-neighbors, 128 visited cap, 32 broken cap) with
 * tool-aware drops/durability; the project's existing
 * {@link FireToolEvents} furnace rewrite then smelts raw drops (Fortune
 * respected, Silk Touch blocks preserved). Instant, server-side.
 */
public final class FirePickaxeItem extends PickaxeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_MINE = "mine";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "extract_cast";
    public static final String ANIM_EMBER = "ember_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation MINE = RawAnimation.begin().thenPlay(ANIM_MINE);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation EMBER = RawAnimation.begin().thenLoop(ANIM_EMBER);

    public static final int MAX_VEIN_BLOCKS = 32;
    public static final int MAX_SEARCH_RADIUS = 8;
    public static final int MAX_NODES_VISITED = 128;
    public static final int COOLDOWN_TICKS = 120;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public FirePickaxeItem(Properties properties) {
        super(FireToolTier.INSTANCE, 4, -2.8F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<FirePickaxeItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_MINE, MINE);
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
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, level, tooltip, flag);
        tooltip.add(Component.translatable("item.opusvsexe.fire_pickaxe.ability").withStyle(ChatFormatting.GOLD));
        tooltip.add(Component.translatable("item.opusvsexe.fire_pickaxe.vein").withStyle(ChatFormatting.RED));
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
            5, 0.25, 0.25, 0.25, 0.04);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        Player player = context.getPlayer();
        if (player == null || level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return InteractionResult.PASS;
        }
        BlockPos origin = context.getClickedPos();
        BlockState originState = level.getBlockState(origin);
        String family = ToolHarvest.oreFamily(originState);
        if (family == null || !player.hasCorrectToolForDrops(originState)) {
            return InteractionResult.PASS;
        }
        List<BlockPos> vein = ToolHarvest.collectVein(serverLevel, origin, family,
            MAX_VEIN_BLOCKS, MAX_SEARCH_RADIUS, MAX_NODES_VISITED);
        if (vein.isEmpty()) {
            return InteractionResult.PASS;
        }
        ItemStack stack = context.getItemInHand();
        InteractionHand hand = context.getHand();
        List<BlockPos> broken = new ArrayList<>();
        for (BlockPos pos : vein) {
            if (stack.isEmpty()) {
                break;
            }
            if (ToolHarvest.breakWithTool(serverLevel, pos, player, stack, hand)) {
                broken.add(pos);
            } else {
                break;
            }
        }
        if (broken.isEmpty()) {
            return InteractionResult.PASS;
        }
        FireToolEvents.scheduleSmelt(serverLevel, broken);
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        level.playSound(null, origin, FireSounds.FIRE_CHARGE, SoundSource.BLOCKS, 0.8F, 0.9F);
        serverLevel.sendParticles(com.opus.fire.registry.FireParticles.EMBER,
            origin.getX() + 0.5, origin.getY() + 1.0, origin.getZ() + 0.5, 10, 0.8, 0.8, 0.8, 0.05);
        return InteractionResult.sidedSuccess(false);
    }
}
