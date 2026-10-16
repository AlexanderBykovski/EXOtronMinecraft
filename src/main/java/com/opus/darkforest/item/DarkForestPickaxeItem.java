package com.opus.darkforest.item;

import com.opus.item.ToolHarvest;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
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

import java.util.ArrayList;
import java.util.List;

/**
 * Dark Forest Pickaxe (registry id {@code dark_forest_pickaxe}).
 *
 * <p>Same tier/stats/tooltip/intrinsic as the tool it replaces
 * (DarkForestToolTier, 1, -2.8F, RARE). RMB ability VEINROOT AWAKENING:
 * right-click a harvestable ore to BFS-harvest its connected vein (same ore
 * family, radius 8, 26-neighbors, 128 visited cap, 32 broken cap) with
 * tool-aware drops/XP/durability. Instant, server-side, no chunk forcing.
 */
public final class DarkForestPickaxeItem extends PickaxeItem implements GeoAnimatable, DarkForestTools.ToolMarker {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_MINE = "mine";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_CAST = "awaken_cast";
    public static final String ANIM_GLOOM = "gloom_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation MINE = RawAnimation.begin().thenPlay(ANIM_MINE);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation CAST = RawAnimation.begin().thenPlay(ANIM_CAST);
    private static final RawAnimation GLOOM = RawAnimation.begin().thenLoop(ANIM_GLOOM);

    public static final int MAX_VEIN_BLOCKS = 32;
    public static final int MAX_SEARCH_RADIUS = 8;
    public static final int MAX_NODES_VISITED = 128;
    public static final int COOLDOWN_TICKS = 80;

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public DarkForestPickaxeItem(Properties properties) {
        super(DarkForestToolTier.INSTANCE, 4, -2.8F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<DarkForestPickaxeItem> main =
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
            5, 0.3, 0.3, 0.3, 0.05);
        serverLevel.sendParticles(ParticleTypes.END_ROD,
            player.getX() + look.x * 1.6, player.getY() + 1.3 + look.y, player.getZ() + look.z * 1.6,
            5, 0.25, 0.25, 0.25, 0.04);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        Player player = context.getPlayer();
        if (player == null) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide) {
            return InteractionResult.PASS;
        }
        if (!(level instanceof ServerLevel serverLevel)) {
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
        int broken = 0;
        for (BlockPos pos : vein) {
            if (stack.isEmpty()) {
                break;
            }
            if (ToolHarvest.breakWithTool(serverLevel, pos, player, stack, hand)) {
                broken++;
            } else {
                break;
            }
        }
        if (broken == 0) {
            return InteractionResult.PASS;
        }
        if (!player.isCreative()) {
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_CAST);
        level.playSound(null, origin, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.BLOCKS, 0.8F, 0.7F);
        serverLevel.sendParticles(ParticleTypes.WITCH,
            origin.getX() + 0.5, origin.getY() + 1.0, origin.getZ() + 0.5, 10, 0.8, 0.8, 0.8, 0.05);
        return InteractionResult.sidedSuccess(false);
    }
}
