package com.opus.blockentity;

import com.opus.advancement.ChroniclesProgression;
import com.opus.block.ExoAssemblyFrameBlock;
import com.opus.item.ExoActivationCoreItem;
import com.opusvsexe.entity.custom.ExosuitEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.joml.Vector3f;

import java.util.UUID;

/** Persistent 60-tick assembly sequence for an activation core. */
public final class ExoAssemblyFrameBlockEntity extends BlockEntity {
    public static final int ASSEMBLY_TICKS = 60;
    private static final DustParticleOptions CYAN = new DustParticleOptions(new Vector3f(0.24F, 0.93F, 1.0F), 1.15F);
    private static final DustParticleOptions GOLD = new DustParticleOptions(new Vector3f(1.0F, 0.67F, 0.18F), 1.0F);
    private String entityId = "";
    private int progress;
    private UUID assemblyPlayer;

    public ExoAssemblyFrameBlockEntity(BlockPos pos, BlockState state) { super(ModBlockEntities.EXO_ASSEMBLY_FRAME, pos, state); }

    public boolean isAssembling() { return progress > 0; }
    public int progress() { return progress; }

    public boolean startAssembly(ExoActivationCoreItem core, net.minecraft.world.entity.player.Player player) {
        if (isAssembling() || level == null || !(level instanceof ServerLevel server)) return false;
        if (server.getEntitiesOfClass(ExosuitEntity.class, new net.minecraft.world.phys.AABB(worldPosition).inflate(4.0D)).size() > 0) {
            player.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.opusvsexe.exo_frame.busy"), true);
            return false;
        }
        Mob probe = core.entityType().create(server);
        if (probe == null || !server.noCollision(probe, new net.minecraft.world.phys.AABB(
            worldPosition.getX() + 0.5D, worldPosition.getY() + 1.0D, worldPosition.getZ() + 0.5D,
            worldPosition.getX() + 0.5D, worldPosition.getY() + 1.0D + probe.getBbHeight(), worldPosition.getZ() + 0.5D))) {
            if (probe != null) probe.discard();
            player.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.opusvsexe.exo_frame.no_space"), true);
            return false;
        }
        if (probe != null) probe.discard();
        entityId = net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(core.entityType()).toString();
        assemblyPlayer = player instanceof ServerPlayer serverPlayer ? serverPlayer.getUUID() : null;
        progress = ASSEMBLY_TICKS;
        level.setBlock(worldPosition, getBlockState().setValue(ExoAssemblyFrameBlock.ACTIVE, true), 3);
        setChanged();
        server.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1.2F, 1.2F);
        player.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.opusvsexe.exo_frame.started", core.tierName()), true);
        return true;
    }

    public void tick(Level level, BlockPos pos, BlockState state) {
        if (level.isClientSide || progress <= 0) return;
        ServerLevel server = (ServerLevel) level;
        progress--;
        if (progress % 5 == 0 || progress <= 3) {
            double angle = progress * 0.32D;
            double radius = 0.7D + (ASSEMBLY_TICKS - progress) * 0.008D;
            server.sendParticles(progress % 10 == 0 ? GOLD : CYAN, pos.getX() + 0.5D + Math.cos(angle) * radius,
                pos.getY() + 1.0D + (ASSEMBLY_TICKS - progress) * 0.018D,
                pos.getZ() + 0.5D + Math.sin(angle) * radius, 6, 0.08D, 0.08D, 0.08D, 0.02D);
            if (progress % 15 == 0) server.sendParticles(ParticleTypes.END_ROD, pos.getX() + 0.5D, pos.getY() + 1.2D, pos.getZ() + 0.5D, 8, 0.35D, 0.4D, 0.35D, 0.02D);
        }
        if (progress == 0) complete(server, pos);
        setChanged();
    }

    private void complete(ServerLevel level, BlockPos pos) {
        EntityTypeLookup lookup = new EntityTypeLookup(entityId);
        if (lookup.type == null) { reset(level, pos); return; }
        Mob entity = lookup.type.create(level);
        if (entity == null) { reset(level, pos); return; }
        entity.moveTo(pos.getX() + 0.5D, pos.getY() + 1.05D, pos.getZ() + 0.5D, level.random.nextFloat() * 360.0F, 0.0F);
        if (!level.noCollision(entity)) { entity.discard(); reset(level, pos); return; }
        level.addFreshEntity(entity);
        if (assemblyPlayer != null) {
            ServerPlayer player = level.getServer().getPlayerList().getPlayer(assemblyPlayer);
            if (player != null) ChroniclesProgression.award(player, "chronicles/route/exo_models", "assembled");
        }
        level.sendParticles(ParticleTypes.EXPLOSION, pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D, 2, 0.2D, 0.2D, 0.2D, 0.0D);
        level.sendParticles(CYAN, pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D, 36, 0.9D, 0.8D, 0.9D, 0.08D);
        level.playSound(null, pos, SoundEvents.BEACON_POWER_SELECT, SoundSource.BLOCKS, 1.5F, 0.75F);
        reset(level, pos);
    }

    private void reset(Level level, BlockPos pos) {
        progress = 0;
        entityId = "";
        assemblyPlayer = null;
        level.setBlock(pos, getBlockState().setValue(ExoAssemblyFrameBlock.ACTIVE, false), 3);
        setChanged();
    }

    @Override protected void saveAdditional(CompoundTag tag) {
        super.saveAdditional(tag);
        tag.putString("AssemblyEntity", entityId);
        tag.putInt("AssemblyProgress", progress);
        if (assemblyPlayer != null) tag.putUUID("AssemblyPlayer", assemblyPlayer);
    }

    @Override public void load(CompoundTag tag) {
        super.load(tag);
        entityId = tag.getString("AssemblyEntity");
        progress = Math.max(0, Math.min(ASSEMBLY_TICKS, tag.getInt("AssemblyProgress")));
        assemblyPlayer = tag.hasUUID("AssemblyPlayer") ? tag.getUUID("AssemblyPlayer") : null;
    }

    private record EntityTypeLookup(net.minecraft.world.entity.EntityType<? extends Mob> type) {
        private EntityTypeLookup(String id) { this(resolve(id)); }
        @SuppressWarnings("unchecked") private static net.minecraft.world.entity.EntityType<? extends Mob> resolve(String id) {
            if (id == null || id.isEmpty()) return null;
            return (net.minecraft.world.entity.EntityType<? extends Mob>) net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE
                .getOptional(new ResourceLocation(id)).orElse(null);
        }
    }
}
