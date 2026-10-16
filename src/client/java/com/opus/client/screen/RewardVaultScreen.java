package com.opus.client.screen;

import com.opus.inventory.RewardVaultMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;

public class RewardVaultScreen extends AbstractContainerScreen<RewardVaultMenu> {
    private static final ResourceLocation TEXTURE = new ResourceLocation("minecraft", "textures/gui/container/generic_54.png");
    private static final int VAULT_ROWS = 3;

    public RewardVaultScreen(RewardVaultMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title);
        this.imageWidth = 176;
        this.imageHeight = 114 + VAULT_ROWS * 18;
        this.inventoryLabelY = this.imageHeight - 94;
    }

    @Override
    protected void renderBg(GuiGraphics gui, float partialTick, int mouseX, int mouseY) {
        int vaultHeight = VAULT_ROWS * 18 + 17;
        gui.blit(TEXTURE, this.leftPos, this.topPos, 0, 0, this.imageWidth, vaultHeight);
        gui.blit(TEXTURE, this.leftPos, this.topPos + vaultHeight, 0, 126,
                this.imageWidth, 96);
    }

    @Override
    protected void renderLabels(GuiGraphics gui, int mouseX, int mouseY) {
        gui.drawString(this.font, this.playerInventoryTitle, this.titleLabelX, this.inventoryLabelY, 4210752, false);
    }
}
