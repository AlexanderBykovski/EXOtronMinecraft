package com.opus.client.screen;

import com.opus.inventory.OpusAssemblyMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;

/** Responsive in-code UI for the 5x5 grid; no missing GUI texture can black it out. */
public final class OpusAssemblyScreen extends AbstractContainerScreen<OpusAssemblyMenu> {
    private static final int PANEL = 0xFF14252A;
    private static final int PANEL_EDGE = 0xFF071114;
    private static final int PANEL_LIGHT = 0xFF2B6869;
    private static final int SLOT_BG = 0xFF0A171B;
    private static final int SLOT_EDGE = 0xFF328F8C;
    private static final int OUTPUT_EDGE = 0xFFD7A33A;

    public OpusAssemblyScreen(OpusAssemblyMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
        imageWidth = 224;
        imageHeight = 218;
        inventoryLabelY = 113;
        titleLabelY = 5;
    }

    @Override
    protected void renderBg(GuiGraphics gui, float partialTick, int mouseX, int mouseY) {
        int x = leftPos, y = topPos;
        gui.fill(x - 2, y - 2, x + imageWidth + 2, y + imageHeight + 2, PANEL_EDGE);
        gui.fill(x, y, x + imageWidth, y + imageHeight, PANEL);
        gui.fill(x, y, x + imageWidth, y + 2, PANEL_LIGHT);
        // Keep the matrix plate behind all 25 standard 18px slots. The old
        // plate ended at x+109 while the fifth column reached x+125.
        gui.fill(x + 31, y + 19, x + 127, y + 113, 0xFF0B1B1D);
        gui.fill(x + 32, y + 20, x + 126, y + 21, 0xFF1C5557);
        for (Slot slot : menu.slots) {
            int edge = slot.index == 0 ? OUTPUT_EDGE : SLOT_EDGE;
            gui.fill(x + slot.x - 1, y + slot.y - 1, x + slot.x + 17, y + slot.y + 17, edge);
            gui.fill(x + slot.x, y + slot.y, x + slot.x + 16, y + slot.y + 16, SLOT_BG);
        }
        gui.fill(x + 139, y + 48, x + 171, y + 49, 0xFF3D8987);
        gui.fill(x + 139, y + 64, x + 171, y + 65, 0xFF3D8987);
    }

    @Override
    protected void renderLabels(GuiGraphics gui, int mouseX, int mouseY) {
        gui.drawString(font, title, titleLabelX, titleLabelY, 0xFFE6FFFF, true);
        gui.drawString(font, Component.translatable("container.opusvsexe.opus_assembly_table.grid"), 11, 20, 0xFF70E8E4, false);
        gui.drawString(font, Component.translatable("container.opusvsexe.opus_assembly_table.output"), 140, 33, 0xFFFFD66A, false);
        gui.drawString(font, playerInventoryTitle, titleLabelX, inventoryLabelY, 0xFFE6FFFF, false);
    }
}
