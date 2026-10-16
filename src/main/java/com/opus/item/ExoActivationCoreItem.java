package com.opus.item;

import com.opus.block.ExoAssemblyFrameBlock;
import com.opus.blockentity.ExoAssemblyFrameBlockEntity;
import com.opusvsexe.entity.custom.ExosuitEntity;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;

import java.util.List;

/** A crafted, tier-specific authorization key for building one EXO frame. */
public final class ExoActivationCoreItem extends Item {
    private final String tierName;
    private final EntityType<? extends ExosuitEntity> entityType;

    public ExoActivationCoreItem(String tierName, EntityType<? extends ExosuitEntity> entityType, Properties properties) {
        super(properties.stacksTo(1));
        this.tierName = tierName;
        this.entityType = entityType;
    }

    public EntityType<? extends ExosuitEntity> entityType() { return entityType; }
    public String tierName() { return tierName; }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        if (!(level.getBlockEntity(context.getClickedPos()) instanceof ExoAssemblyFrameBlockEntity frame)) {
            return InteractionResult.PASS;
        }
        Player player = context.getPlayer();
        if (player == null) return InteractionResult.PASS;
        if (level.isClientSide) return InteractionResult.SUCCESS;
        if (!frame.startAssembly(this, player)) return InteractionResult.FAIL;
        if (!player.getAbilities().instabuild) context.getItemInHand().shrink(1);
        return InteractionResult.CONSUME;
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.opusvsexe.exo_activation_core.desc").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable("item.opusvsexe.exo_activation_core.tier", tierName).withStyle(ChatFormatting.GOLD));
        tooltip.add(Component.translatable("item.opusvsexe.exo_activation_core.use").withStyle(ChatFormatting.AQUA));
    }
}
