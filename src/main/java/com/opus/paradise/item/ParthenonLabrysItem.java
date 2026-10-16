package com.opus.paradise.item;

import com.opus.sound.ModSounds;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
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
 * Parthenon Labrys — the divine double-bladed axe (registry id {@code parthenon_axe}).
 *
 * <p>Gameplay parity with the tool it replaces: same {@link ParthenonToolTier},
 * same axe damage/speed ({@code 9.0F}/{@code -3.0F}), same tooltip. Only the
 * presentation changes: a full GeckoLib 3D model with idle/equip/attack/block
 * animations instead of a flat sprite.
 *
 * <p>RIGHT CLICK IS BLOCK, not an ability: {@link UseAnim#BLOCK} + 72000-tick
 * duration plugs the axe into vanilla {@code LivingEntity.isBlocking()}
 * mechanics (5-tick startup, frontal arc, shield bypass rules, durability via
 * {@code hurtCurrentlyUsedShield}, axe-disable, projectiles). No custom damage
 * logic exists anywhere in this class.
 *
 * <p>Rendering goes through the vanilla baked-model path ({@code builtin/entity}
 * + {@code BuiltinItemRendererRegistry}, same as the Demonic Trident): the item
 * deliberately implements plain {@link GeoAnimatable}, <em>not</em> {@code GeoItem},
 * because GeckoLib's {@code ItemRenderer} mixin hijacks every {@code GeoItem} to a
 * {@code RenderProvider} that cannot exist in this project's split
 * main/client source sets.
 *
 * <p>Animation triggers (names must match {@code labrys.animation.json}):
 * <ul>
 *   <li>{@code idle} — default loop on the {@code main} controller.</li>
 *   <li>{@code attack} — client prediction in the model when the local swing
 *       starts, plus a server trigger in {@code onStrike} so every tracking
 *       client sees entity hits. Re-triggering the same animation is a no-op
 *       in GeckoLib 4, so the two paths never snap.</li>
 *   <li>{@code equip} — client-side when a new stack appears in first person.</li>
 *   <li>{@code block_enter}/{@code block_idle}/{@code block_hit}/{@code block_exit}
 *       — defensive stance cycle; enter/exit on use edges (client model),
 *       hit on the shield-damage hook (server, all viewers).</li>
 *   <li>{@code gem_pulse} — staggered ruby breathing on the {@code fx} controller.</li>
 * </ul>
 */
public final class ParthenonLabrysItem extends AxeItem implements GeoAnimatable {
    public static final String CONTROLLER_MAIN = "main";
    public static final String CONTROLLER_FX = "fx";
    public static final String ANIM_IDLE = "idle";
    public static final String ANIM_EQUIP = "equip";
    public static final String ANIM_ATTACK = "attack";
    public static final String ANIM_BLOCK_ENTER = "block_enter";
    public static final String ANIM_BLOCK_IDLE = "block_idle";
    public static final String ANIM_BLOCK_HIT = "block_hit";
    public static final String ANIM_BLOCK_EXIT = "block_exit";
    public static final String ANIM_GEM_PULSE = "gem_pulse";

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop(ANIM_IDLE);
    private static final RawAnimation EQUIP = RawAnimation.begin().thenPlay(ANIM_EQUIP);
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay(ANIM_ATTACK);
    private static final RawAnimation BLOCK_ENTER = RawAnimation.begin().thenPlay(ANIM_BLOCK_ENTER);
    private static final RawAnimation BLOCK_IDLE = RawAnimation.begin().thenLoop(ANIM_BLOCK_IDLE);
    private static final RawAnimation BLOCK_HIT = RawAnimation.begin().thenPlay(ANIM_BLOCK_HIT);
    private static final RawAnimation BLOCK_EXIT = RawAnimation.begin().thenPlay(ANIM_BLOCK_EXIT);
    private static final RawAnimation GEM_PULSE = RawAnimation.begin().thenLoop(ANIM_GEM_PULSE);

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ParthenonLabrysItem(Properties properties) {
        super(ParthenonToolTier.INSTANCE, 9.0F, -3.0F, properties);
        GeckoLibNetwork.registerSyncedAnimatable(this);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        AnimationController<ParthenonLabrysItem> main =
            new AnimationController<>(this, CONTROLLER_MAIN, 5, state -> {
                if (state.getController().isPlayingTriggeredAnimation()) {
                    return PlayState.CONTINUE;
                }
                return state.setAndContinue(IDLE);
            });
        main.triggerableAnim(ANIM_EQUIP, EQUIP);
        main.triggerableAnim(ANIM_ATTACK, ATTACK);
        main.triggerableAnim(ANIM_BLOCK_ENTER, BLOCK_ENTER);
        main.triggerableAnim(ANIM_BLOCK_IDLE, BLOCK_IDLE);
        main.triggerableAnim(ANIM_BLOCK_HIT, BLOCK_HIT);
        main.triggerableAnim(ANIM_BLOCK_EXIT, BLOCK_EXIT);
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

    /**
     * Fires a triggerable animation for one stack: directly on the client,
     * or via GeckoLib's trigger packet to every tracking client from the server.
     * Same routing as {@code SingletonGeoAnimatable.triggerAnim}, inlined here
     * because plain {@link GeoAnimatable} does not provide it.
     */
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
        }
    }

    /**
     * Server-side entity-hit hook, called from the player attack mixin.
     * Visual only: contact flash, directional gold sparks, ivory motes and a
     * few crimson fragments at the impact point. Critical hits (falling) get
     * a ~50% larger burst plus a firework star. No gameplay effect.
     */
    public void onStrike(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        long id = GeoItem.getOrAssignId(stack, serverLevel);
        fireTrigger(player, id, ANIM_ATTACK);
        boolean crit = player.fallDistance > 0.0F && !player.onGround()
            && !player.isInWater() && !player.hasEffect(net.minecraft.world.effect.MobEffects.BLINDNESS);
        level.playSound(null, player.blockPosition(), ModSounds.HAMMER_HIT, SoundSource.PLAYERS,
            crit ? 0.9F : 0.8F, crit ? 0.85F : 0.75F);
        Vec3 look = player.getLookAngle();
        double px = player.getX() + look.x * 1.6;
        double py = player.getY() + 1.3 + look.y;
        double pz = player.getZ() + look.z * 1.6;
        int sparks = crit ? 12 : 8;
        serverLevel.sendParticles(ParticleTypes.END_ROD, px, py, pz, sparks, 0.25, 0.25, 0.25, 0.04);
        serverLevel.sendParticles(ParticleTypes.ENCHANT, px, py, pz, crit ? 9 : 6, 0.3, 0.3, 0.3, 0.1);
        serverLevel.sendParticles(ParticleTypes.FIREWORK, px, py, pz, crit ? 6 : 3, 0.2, 0.2, 0.2, 0.05);
    }

    /**
     * Server-side blocked-hit hook, called from the shield-damage mixin when
     * vanilla blocking absorbs damage into this axe. Small, distinct from the
     * attack burst: a few gold/ivory sparks and a short clang on top of the
     * vanilla shield-block sound. No gameplay effect.
     */
    public void onBlocked(Player player, ItemStack stack) {
        Level level = player.level();
        if (level.isClientSide || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        fireTrigger(player, GeoItem.getOrAssignId(stack, serverLevel), ANIM_BLOCK_HIT);
        level.playSound(null, player.blockPosition(), ModSounds.HAMMER_HIT, SoundSource.PLAYERS, 0.35F, 1.2F);
        serverLevel.sendParticles(ParticleTypes.END_ROD,
            player.getX(), player.getY() + 1.3, player.getZ(), 4, 0.3, 0.3, 0.3, 0.03);
        serverLevel.sendParticles(ParticleTypes.FIREWORK,
            player.getX(), player.getY() + 1.3, player.getZ(), 2, 0.25, 0.25, 0.25, 0.02);
    }

    @Override
    public int getUseDuration(ItemStack stack) {
        return 72000;
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BLOCK;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(player.getItemInHand(hand));
    }
}
