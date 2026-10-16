package com.opus.blockentity;

import com.opus.registry.ModEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public class DormantSpawnerBlockEntity extends BlockEntity {
    private static final int SPAWN_INTERVAL = 120;
    private static final int MAX_SPAWN_RADIUS = 8;
    private static final int SPAWN_ATTEMPTS = 8;
    private String entityId = "opusvsexe:haiku_1_5";
    private int cooldown = SPAWN_INTERVAL;
    private int maxNearby = 4;
    private int spawnRadius = 2;

    public DormantSpawnerBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.DORMANT_SPAWNER, pos, state);
    }

    public void tick(Level level, BlockPos pos, BlockState state) {
        if (level.isClientSide) return;
        boolean active = state.getValue(com.opus.block.DormantSpawnerBlock.ACTIVE);
        if (!active) return;
        if (--cooldown > 0) return;
        cooldown = SPAWN_INTERVAL;

        int nearby = level.getEntitiesOfClass(Mob.class,
                new net.minecraft.world.phys.AABB(pos).inflate(12.0),
                e -> net.minecraft.world.entity.EntityType.getKey(e.getType()).toString().equals(entityId)).size();
        if (nearby >= Math.max(1, maxNearby)) return;

        EntityType<?> type = net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE
                .getOptional(new net.minecraft.resources.ResourceLocation(entityId)).orElse(null);
        if (type == null) return;
        int radius = Math.max(0, Math.min(MAX_SPAWN_RADIUS, spawnRadius));
        for (int attempt = 0; attempt < SPAWN_ATTEMPTS; attempt++) {
            if (!(type.create(level) instanceof Mob mob)) return;
            double x = pos.getX() + 0.5 + (radius == 0 ? 0.0 : (level.random.nextDouble() - 0.5) * radius * 2.0);
            double z = pos.getZ() + 0.5 + (radius == 0 ? 0.0 : (level.random.nextDouble() - 0.5) * radius * 2.0);
            double y = pos.getY() + 1.0;
            mob.moveTo(x, y, z, level.random.nextFloat() * 360.0f, 0.0f);
            if (!level.noCollision(mob)) continue;
            mob.finalizeSpawn((ServerLevel) level, level.getCurrentDifficultyAt(pos), MobSpawnType.SPAWNER, null, null);
            level.addFreshEntity(mob);
            return;
        }
    }

    public void setEntityId(String id) {
        this.entityId = id;
    }

    @Override
    protected void saveAdditional(CompoundTag tag) {
        super.saveAdditional(tag);
        tag.putString("entity_id", entityId);
        tag.putInt("cooldown", cooldown);
        tag.putInt("max_nearby", maxNearby);
        tag.putInt("spawn_radius", spawnRadius);
    }

    @Override
    public void load(CompoundTag tag) {
        super.load(tag);
        if (tag.contains("entity_id")) entityId = tag.getString("entity_id");
        if (tag.contains("cooldown")) cooldown = tag.getInt("cooldown");
        if (tag.contains("max_nearby")) maxNearby = Math.max(1, tag.getInt("max_nearby"));
        if (tag.contains("spawn_radius")) spawnRadius = Math.max(0, Math.min(MAX_SPAWN_RADIUS, tag.getInt("spawn_radius")));
    }
}
