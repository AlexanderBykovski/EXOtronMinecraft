package com.opus.fire.item;

import com.opus.fire.entity.projectile.DemonicTridentEntity;
import com.opus.fire.registry.FireEntities;
import com.opus.fire.sound.FireSounds;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import com.google.common.collect.ImmutableMultimap;
import com.google.common.collect.Multimap;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.core.animatable.GeoAnimatable;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.util.GeckoLibUtil;

public final class DemonicTridentItem extends Item implements GeoAnimatable {
    /**
     * Melee mirrors a netherite axe 1:1 (9 attack damage, 1.0 attack speed):
     * base player 1 damage + 8 modifier, base 4.0 speed - 3.0 modifier.
     * Thrown-projectile behavior is untouched.
     */
    private static final double MELEE_DAMAGE_MODIFIER = 8.0D;
    private static final double MELEE_SPEED_MODIFIER = -3.0D;
    private final Multimap<Attribute, AttributeModifier> attributeModifiers;

    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop("item_idle");
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    {
        ImmutableMultimap.Builder<Attribute, AttributeModifier> builder = ImmutableMultimap.builder();
        builder.put(Attributes.ATTACK_DAMAGE, new AttributeModifier(BASE_ATTACK_DAMAGE_UUID, "Weapon modifier",
            MELEE_DAMAGE_MODIFIER, AttributeModifier.Operation.ADDITION));
        builder.put(Attributes.ATTACK_SPEED, new AttributeModifier(BASE_ATTACK_SPEED_UUID, "Weapon modifier",
            MELEE_SPEED_MODIFIER, AttributeModifier.Operation.ADDITION));
        attributeModifiers = builder.build();
    }

    public DemonicTridentItem(Properties properties) {
        super(properties);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "inventory_idle", 0, state -> {
            state.getController().setAnimation(IDLE);
            return PlayState.CONTINUE;
        }));
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
    @Override public double getTick(Object itemStack) { return System.nanoTime() / 50_000_000.0; }

    @Override
    public Multimap<Attribute, AttributeModifier> getDefaultAttributeModifiers(EquipmentSlot slot) {
        return slot == EquipmentSlot.MAINHAND ? attributeModifiers : super.getDefaultAttributeModifiers(slot);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        stack.hurtAndBreak(1, attacker, e -> e.broadcastBreakEvent(EquipmentSlot.MAINHAND));
        return true;
    }

    @Override public int getUseDuration(ItemStack stack) { return 72000; }
    @Override public UseAnim getUseAnimation(ItemStack stack) { return UseAnim.SPEAR; }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(player.getItemInHand(hand));
    }

    @Override
    public void releaseUsing(ItemStack stack, Level level, LivingEntity user, int remaining) {
        if (!(user instanceof Player player) || getUseDuration(stack) - remaining < 10) return;
        if (!level.isClientSide) {
            DemonicTridentEntity trident = new DemonicTridentEntity(FireEntities.DEMONIC_TRIDENT_ENTITY, level, player);
            trident.setPos(player.getEyePosition().add(player.getLookAngle().scale(0.75)));
            trident.shootFromRotation(player, player.getXRot(), player.getYRot(), 0.0f, 2.1f, 0.75f);
            level.addFreshEntity(trident);
            stack.hurtAndBreak(1, player, entity -> entity.broadcastBreakEvent(player.getUsedItemHand()));
            player.getCooldowns().addCooldown(this, 36);
            level.playSound(null, player, FireSounds.FIREBALL_LAUNCH, SoundSource.PLAYERS, 1.0f, 0.72f);
        }
    }
}
