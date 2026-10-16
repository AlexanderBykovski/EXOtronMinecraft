package com.opus.paradise.client.model;

import com.opus.paradise.ParadiseLine;
import com.opus.paradise.item.ParthenonLabrysItem;
import com.opus.sound.ModSounds;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import software.bernie.geckolib.constant.DataTickets;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;
import net.minecraft.client.renderer.RenderType;

import java.util.HashMap;
import java.util.Map;

/**
 * Client model for the Parthenon Labrys. Besides resource bindings this is the
 * home of all purely client-side animation triggers (render thread only, so no
 * dedicated-server class-loading risk):
 * <ul>
 *   <li>attack prediction on the local swing rising edge (covers air swings,
 *       which never reach the server attack hook), plus a short client-side
 *       ivory/gold swing trail;</li>
 *   <li>equip flourish when a new stack appears in first person;</li>
 *   <li>block stance cycle on the shield-like RMB use edges
 *       (enter -&gt; looping idle -&gt; exit);</li>
 *   <li>a heavy swing whoosh pitched down for weight.</li>
 * </ul>
 */
public final class ParthenonLabrysModel extends GeoModel<ParthenonLabrysItem> {
    private static final ResourceLocation GEO = ParadiseLine.id("geo/paradise/labrys.geo.json");
    private static final ResourceLocation TEXTURE = ParadiseLine.id("textures/paradise/item/labrys.png");
    private static final ResourceLocation ANIMATION = ParadiseLine.id("animations/paradise/labrys.animation.json");

    private static final float SWING_THRESHOLD = 0.05F;

    /** Last observed swing per animatable id, for rising-edge detection. */
    private final Map<Long, Float> lastAttackAnim = new HashMap<>();
    // Equip tracking is first-person ONLY. GUI/hotbar renders draw the same
    // ItemStack objects every frame; letting them touch this state caused the
    // equip flourish to retrigger each frame (constant rocking). Slot index
    // covers re-selecting the identical stack.
    private ItemStack lastFirstPersonStack = ItemStack.EMPTY;
    private int lastSelectedSlot = -1;
    /** Block-stance tracking per animatable id (first-person only, see above). */
    private final Map<Long, Boolean> wasUsing = new HashMap<>();
    private final Map<Long, Integer> blockEnterTick = new HashMap<>();

    @Override
    public ResourceLocation getModelResource(ParthenonLabrysItem item) {
        return GEO;
    }

    @Override
    public ResourceLocation getTextureResource(ParthenonLabrysItem item) {
        return TEXTURE;
    }

    @Override
    public ResourceLocation getAnimationResource(ParthenonLabrysItem item) {
        return ANIMATION;
    }

    @Override
    public RenderType getRenderType(ParthenonLabrysItem item, ResourceLocation texture) {
        return RenderType.entityCutoutNoCull(texture);
    }

    @Override
    public void setCustomAnimations(ParthenonLabrysItem animatable, long instanceId,
                                    AnimationState<ParthenonLabrysItem> state) {
        super.setCustomAnimations(animatable, instanceId, state);
        Minecraft minecraft = Minecraft.getInstance();
        LocalPlayer player = minecraft.player;
        if (player == null) {
            return;
        }
        ItemStack stack = state.getData(DataTickets.ITEMSTACK);
        if (stack == null || stack.isEmpty()) {
            return;
        }
        boolean held = player.getMainHandItem() == stack || player.getOffhandItem() == stack;

        float swing = player.getAttackAnim(state.getPartialTick());
        float previous = lastAttackAnim.getOrDefault(instanceId, 0.0F);
        lastAttackAnim.put(instanceId, swing);
        if (lastAttackAnim.size() > 256) {
            lastAttackAnim.clear();
            lastAttackAnim.put(instanceId, swing);
        }
        if (held && previous <= SWING_THRESHOLD && swing > SWING_THRESHOLD) {
            if (instanceId != Long.MAX_VALUE) {
                animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                    .tryTriggerAnimation(ParthenonLabrysItem.CONTROLLER_MAIN,
                        ParthenonLabrysItem.ANIM_ATTACK);
            }
            player.playSound(ModSounds.KATANA_SWING, 0.45F, 0.55F);
            if (minecraft.level != null) {
                net.minecraft.world.phys.Vec3 look = player.getLookAngle();
                net.minecraft.world.phys.Vec3 eye = player.getEyePosition();
                for (int i = 1; i <= 8; i++) {
                    double t = i * 0.22;
                    minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.END_ROD,
                        eye.x + look.x * t, eye.y + look.y * t, eye.z + look.z * t,
                        -look.x * 0.15, -look.y * 0.15, -look.z * 0.15);
                }
                minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.FIREWORK,
                    eye.x + look.x * 1.2, eye.y + look.y * 1.2, eye.z + look.z * 1.2,
                    0.0, 0.02, 0.0);
                minecraft.level.addParticle(net.minecraft.core.particles.ParticleTypes.FIREWORK,
                    eye.x + look.x * 1.7, eye.y + look.y * 1.7, eye.z + look.z * 1.7,
                    0.0, 0.02, 0.0);
            }
        }

        ItemDisplayContext perspective = state.getData(DataTickets.ITEM_RENDER_PERSPECTIVE);
        boolean firstPerson = perspective == ItemDisplayContext.FIRST_PERSON_RIGHT_HAND
            || perspective == ItemDisplayContext.FIRST_PERSON_LEFT_HAND;
        if (firstPerson && held) {
            int selected = player.getInventory().selected;
            if (lastFirstPersonStack != stack || selected != lastSelectedSlot) {
                lastFirstPersonStack = stack;
                lastSelectedSlot = selected;
                if (instanceId != Long.MAX_VALUE) {
                    animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                        .tryTriggerAnimation(ParthenonLabrysItem.CONTROLLER_MAIN,
                            ParthenonLabrysItem.ANIM_EQUIP);
                }
            }
            boolean using = player.isUsingItem() && player.getUseItem() == stack;
            boolean was = wasUsing.getOrDefault(instanceId, false);
            wasUsing.put(instanceId, using);
            if (using && !was) {
                blockEnterTick.put(instanceId, player.tickCount);
                if (instanceId != Long.MAX_VALUE) {
                    animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                        .tryTriggerAnimation(ParthenonLabrysItem.CONTROLLER_MAIN,
                            ParthenonLabrysItem.ANIM_BLOCK_ENTER);
                }
            } else if (using) {
                int entered = blockEnterTick.getOrDefault(instanceId, player.tickCount);
                if (player.tickCount - entered > 6 && instanceId != Long.MAX_VALUE) {
                    animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                        .tryTriggerAnimation(ParthenonLabrysItem.CONTROLLER_MAIN,
                            ParthenonLabrysItem.ANIM_BLOCK_IDLE);
                }
            } else if (was && instanceId != Long.MAX_VALUE) {
                animatable.getAnimatableInstanceCache().getManagerForId(instanceId)
                    .tryTriggerAnimation(ParthenonLabrysItem.CONTROLLER_MAIN,
                        ParthenonLabrysItem.ANIM_BLOCK_EXIT);
            }
        }
    }
}
