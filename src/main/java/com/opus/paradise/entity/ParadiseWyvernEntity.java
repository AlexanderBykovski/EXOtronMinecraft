package com.opus.paradise.entity;

import com.opus.paradise.ParadiseLine;
import com.opus.paradise.registry.ParadiseBlocks;
import com.opus.paradise.registry.ParadiseEntities;
import com.opus.paradise.registry.ParadiseItems;
import com.opus.advancement.ChroniclesProgression;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.MoveControl;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FollowOwnerGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.SitWhenOrderedToGoal;
import net.minecraft.world.entity.ai.goal.TemptGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomFlyingGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;
import org.jetbrains.annotations.Nullable;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.core.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.core.animation.AnimatableManager;
import software.bernie.geckolib.core.animation.AnimationController;
import software.bernie.geckolib.core.animation.AnimationState;
import software.bernie.geckolib.core.animation.RawAnimation;
import software.bernie.geckolib.core.object.PlayState;
import software.bernie.geckolib.util.GeckoLibUtil;

public final class ParadiseWyvernEntity extends TamableAnimal implements GeoEntity {
    public static final int FAST_FLIGHT_DURATION_TICKS = 240;
    public static final int FAST_FLIGHT_COOLDOWN_TICKS = 360;
    private static final int FAST_CHARGE_TICKS = 8;
    private static final int FAST_BURST_TICKS = 7;
    private static final int FAST_RECOVERY_TICKS = 12;
    private static final byte FAST_READY = 0;
    private static final byte FAST_CHARGE = 1;
    private static final byte FAST_BURST = 2;
    private static final byte FAST_ACTIVE = 3;
    private static final byte FAST_RECOVERY = 4;
    private static final EntityDataAccessor<Boolean> SADDLED = SynchedEntityData.defineId(ParadiseWyvernEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Byte> FAST_STATE = SynchedEntityData.defineId(ParadiseWyvernEntity.class, EntityDataSerializers.BYTE);
    private static final EntityDataAccessor<Integer> FAST_TICKS = SynchedEntityData.defineId(ParadiseWyvernEntity.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Integer> FAST_COOLDOWN = SynchedEntityData.defineId(ParadiseWyvernEntity.class, EntityDataSerializers.INT);
    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop("idle_flight");
    private static final RawAnimation FLY = RawAnimation.begin().thenLoop("fly");
    private static final RawAnimation SIT = RawAnimation.begin().thenLoop("sit");
    private static final RawAnimation FAST_CHARGE_ANIM = RawAnimation.begin().thenPlay("fast_charge");
    private static final RawAnimation FAST_BURST_ANIM = RawAnimation.begin().thenPlay("fast_burst");
    private static final RawAnimation FAST_FLIGHT_ANIM = RawAnimation.begin().thenLoop("fast_flight");
    private static final RawAnimation FAST_RECOVERY_ANIM = RawAnimation.begin().thenPlay("fast_recovery");

    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private float pilotStrafe;
    private float pilotForward;
    private float pilotYaw;
    private float pilotPitch;
    private boolean pilotAscend;
    private boolean pilotDescend;
    private int lastPilotInputTick = Integer.MIN_VALUE;
    private static final DustParticleOptions CYAN_DUST = new DustParticleOptions(new Vector3f(0.24F, 0.93F, 1.0F), 1.15F);
    private static final DustParticleOptions GOLD_DUST = new DustParticleOptions(new Vector3f(1.0F, 0.67F, 0.18F), 0.9F);

    public ParadiseWyvernEntity(EntityType<? extends TamableAnimal> type, Level level) {
        super(type, level);
        moveControl = new WyvernMoveControl(this);
        setNoGravity(true);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        entityData.define(SADDLED, false);
        entityData.define(FAST_STATE, FAST_READY);
        entityData.define(FAST_TICKS, 0);
        entityData.define(FAST_COOLDOWN, 0);
    }

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation navigation = new FlyingPathNavigation(this, level);
        navigation.setCanFloat(true);
        navigation.setCanOpenDoors(false);
        return navigation;
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new SitWhenOrderedToGoal(this));
        goalSelector.addGoal(1, new FollowOwnerGoal(this, 1.05, 7.0F, 2.5F, true));
        goalSelector.addGoal(2, new BreedGoal(this, 0.9));
        goalSelector.addGoal(3, new TemptGoal(this, 1.0, Ingredient.of(ParadiseItems.PARADISE_FRUIT), false));
        goalSelector.addGoal(4, new CloudBandRoamGoal());
        goalSelector.addGoal(5, new WaterAvoidingRandomFlyingGoal(this, 0.78));
        goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 12.0F));
        goalSelector.addGoal(7, new RandomLookAroundGoal(this));
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes().add(Attributes.MAX_HEALTH, 42.0).add(Attributes.ARMOR, 6.0)
            .add(Attributes.MOVEMENT_SPEED, 0.28).add(Attributes.FLYING_SPEED, 0.48)
            .add(Attributes.FOLLOW_RANGE, 32.0).add(Attributes.KNOCKBACK_RESISTANCE, 0.25);
    }

    public static boolean canSpawn(EntityType<ParadiseWyvernEntity> type, ServerLevelAccessor level, MobSpawnType reason,
                                   BlockPos pos, RandomSource random) {
        boolean canopyLaunch = level.getBlockState(pos.below()).is(BlockTags.LEAVES);
        boolean cloudBand = pos.getY() >= 112 && pos.getY() <= 160 && level.getBlockState(pos.below()).isAir();
        return level.getBlockState(pos).isAir() && level.getBlockState(pos.above()).isAir()
            && (canopyLaunch || cloudBand) && level.getRawBrightness(pos, 0) > 8;
    }

    public boolean isSaddled() { return entityData.get(SADDLED); }
    public byte getFastFlightState() { return entityData.get(FAST_STATE); }
    public int getFastFlightTicks() { return entityData.get(FAST_TICKS); }
    public int getFastFlightCooldown() { return entityData.get(FAST_COOLDOWN); }
    public boolean isFastFlightCharging() { return getFastFlightState() == FAST_CHARGE || getFastFlightState() == FAST_BURST; }
    public boolean isFastFlightActive() { return getFastFlightState() == FAST_ACTIVE; }

    public void acceptPilotInput(ServerPlayer player, float strafe, float forward, float yaw, float pitch,
                                 boolean ascend, boolean descend) {
        acceptPilotInput((Player) player, strafe, forward, yaw, pitch, ascend, descend);
    }

    public void acceptPilotInput(Player player, float strafe, float forward, float yaw, float pitch,
                                 boolean ascend, boolean descend) {
        if (player != getControllingPassenger() || !isOwnedBy(player) || !isSaddled()) return;
        pilotStrafe = Mth.clamp(strafe, -1.0F, 1.0F);
        pilotForward = Mth.clamp(forward, -1.0F, 1.0F);
        pilotYaw = Mth.wrapDegrees(yaw);
        pilotPitch = Mth.clamp(pitch, -80.0F, 80.0F);
        pilotAscend = ascend;
        pilotDescend = descend;
        lastPilotInputTick = tickCount;
    }

    public boolean tryActivateFastFlight(ServerPlayer player) {
        if (level().isClientSide || player != getControllingPassenger() || !isOwnedBy(player)
            || !isSaddled() || !isAlive()) return false;
        if (isFastFlightCharging()) return false;
        if (isFastFlightActive()) {
            beginFastRecovery();
            return true;
        }
        if (getFastFlightState() == FAST_RECOVERY || getFastFlightCooldown() > 0) {
            player.displayClientMessage(net.minecraft.network.chat.Component.translatable(
                "message.opusvsexe.wyvern.fast_flight_cooldown",
                String.format(java.util.Locale.ROOT, "%.1f", getFastFlightCooldown() / 20.0D)), true);
            return false;
        }
        entityData.set(FAST_STATE, FAST_CHARGE);
        entityData.set(FAST_TICKS, FAST_CHARGE_TICKS);
        entityData.set(FAST_COOLDOWN, FAST_FLIGHT_COOLDOWN_TICKS);
        ChroniclesProgression.award(player, "chronicles/paradise/fast_flight", "activated");
        setDeltaMovement(getDeltaMovement().scale(0.18D));
        playSound(net.minecraft.sounds.SoundEvents.PHANTOM_FLAP, 1.2F, 0.65F);
        if (level() instanceof net.minecraft.server.level.ServerLevel server) {
            server.sendParticles(ParticleTypes.CLOUD, getX(), getY() + 0.55D, getZ(), 26, 0.65D, 0.35D, 0.65D, 0.08D);
            server.sendParticles(CYAN_DUST, getX(), getY() + 0.8D, getZ(), 16, 0.45D, 0.25D, 0.45D, 0.04D);
        }
        return true;
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack held = player.getItemInHand(hand);
        if (!isTame() && !isBaby() && held.is(ParadiseItems.PARADISE_FRUIT)) {
            if (!level().isClientSide) {
                if (!player.getAbilities().instabuild) held.shrink(1);
                if (random.nextInt(3) == 0) {
                    tame(player);
                    setOrderedToSit(false);
                    setPersistenceRequired();
                    level().broadcastEntityEvent(this, (byte) 7);
                } else {
                    level().broadcastEntityEvent(this, (byte) 6);
                }
            }
            return InteractionResult.sidedSuccess(level().isClientSide);
        }
        if (isTame() && isOwnedBy(player)) {
            if (held.is(ParadiseItems.PARADISE_FRUIT) && getHealth() < getMaxHealth()) {
                if (!level().isClientSide) {
                    if (!player.getAbilities().instabuild) held.shrink(1);
                    heal(8.0F);
                }
                return InteractionResult.sidedSuccess(level().isClientSide);
            }
            if (!isSaddled() && !isBaby() && held.is(Items.SADDLE)) {
                if (!level().isClientSide) {
                    entityData.set(SADDLED, true);
                    if (!player.getAbilities().instabuild) held.shrink(1);
                }
                return InteractionResult.sidedSuccess(level().isClientSide);
            }
            if (player.isSecondaryUseActive()) {
                if (!level().isClientSide) {
                    setOrderedToSit(!isOrderedToSit());
                    navigation.stop();
                }
                return InteractionResult.sidedSuccess(level().isClientSide);
            }
            if (isSaddled() && held.isEmpty() && !isVehicle() && !isBaby()) {
                if (!level().isClientSide) {
                    setOrderedToSit(false);
                    player.startRiding(this);
                }
                return InteractionResult.sidedSuccess(level().isClientSide);
            }
        }
        return super.mobInteract(player, hand);
    }

    @Nullable
    @Override
    public Player getControllingPassenger() {
        Entity passenger = getFirstPassenger();
        return passenger instanceof Player player && isOwnedBy(player) ? player : null;
    }

    @Override
    protected boolean canAddPassenger(Entity passenger) {
        return passenger instanceof Player player && isSaddled() && isOwnedBy(player) && getPassengers().isEmpty();
    }

    @Override public double getPassengersRidingOffset() { return 1.18D; }

    @Override
    protected void dropEquipment() {
        super.dropEquipment();
        if (isSaddled()) spawnAtLocation(Items.SADDLE);
    }

    @Override
    public void travel(Vec3 travelVector) {
        Player rider = getControllingPassenger();
        if (rider == null || !isSaddled()) {
            super.travel(travelVector);
            return;
        }
        if (!level().isClientSide && tickCount - lastPilotInputTick > 10) {
            pilotStrafe = 0.0F;
            pilotForward = 0.0F;
            pilotAscend = false;
            pilotDescend = false;
        }
        setYRot(pilotYaw);
        yRotO = getYRot();
        setXRot(pilotPitch * 0.35F);
        yBodyRot = getYRot();
        yHeadRot = getYRot();

        double radians = Math.toRadians(pilotYaw);
        Vec3 forward = new Vec3(-Math.sin(radians), 0.0, Math.cos(radians));
        Vec3 right = new Vec3(Math.cos(radians), 0.0, Math.sin(radians));
        Vec3 horizontal = forward.scale(pilotForward).add(right.scale(pilotStrafe * 0.72));
        if (horizontal.lengthSqr() > 1.0) horizontal = horizontal.normalize();
        Vec3 motion;
        if (isFastFlightCharging()) {
            Vec3 look = rider.getViewVector(1.0F).normalize();
            double burstSpeed = getFastFlightState() == FAST_BURST ? 1.35D : 0.12D;
            motion = getDeltaMovement().scale(0.72D).add(look.scale(burstSpeed));
        } else if (isFastFlightActive()) {
            Vec3 look = rider.getViewVector(1.0F).normalize();
            Vec3 steer = look.scale(Math.max(0.0D, pilotForward));
            if (Math.abs(pilotStrafe) > 0.05F) steer = steer.add(right.scale(pilotStrafe * 0.42D));
            if (steer.lengthSqr() < 0.04D) {
                Vec3 carried = getDeltaMovement();
                steer = carried.lengthSqr() > 0.04D ? carried.normalize() : look;
            } else {
                steer = steer.normalize();
            }
            double speed = pilotForward < -0.05F ? 0.65D : 1.78D;
            Vec3 desired = steer.scale(speed);
            if (pilotAscend != pilotDescend) desired = new Vec3(desired.x, pilotAscend ? 0.85D : -0.85D, desired.z);
            else desired = new Vec3(desired.x, Mth.clamp(-pilotPitch / 70.0D * 0.72D, -0.72D, 0.72D), desired.z);
            motion = getDeltaMovement().scale(0.78D).add(desired.scale(0.22D));
            if (motion.lengthSqr() > 1.78D * 1.78D) motion = motion.normalize().scale(1.78D);
        } else {
            double cruise = pilotForward < 0.0F ? 0.22 : 0.44;
            horizontal = horizontal.scale(cruise);
            double vertical = Math.abs(pilotForward) + Math.abs(pilotStrafe) < 0.05F ? -0.035 : -pilotPitch / 80.0 * 0.24;
            if (pilotAscend != pilotDescend) vertical = pilotAscend ? 0.34 : -0.30;
            vertical = Mth.clamp(vertical, -0.34, 0.38);
            Vec3 desired = new Vec3(horizontal.x, vertical, horizontal.z);
            motion = getDeltaMovement().scale(0.58).add(desired.scale(0.42));
        }
        setDeltaMovement(motion);
        move(MoverType.SELF, motion);
        hasImpulse = true;
        calculateEntityAnimation(false);
        tryCheckInsideBlocks();
    }

    @Override
    public void tick() {
        super.tick();
        setNoGravity(true);
        if (!level().isClientSide) {
            if (getFastFlightCooldown() > 0) entityData.set(FAST_COOLDOWN, getFastFlightCooldown() - 1);
            byte state = getFastFlightState();
            if ((state == FAST_CHARGE || state == FAST_BURST)
                && (getControllingPassenger() == null || !isSaddled())) {
                beginFastRecovery();
                state = FAST_RECOVERY;
            }
            if (state == FAST_CHARGE || state == FAST_BURST || state == FAST_RECOVERY) {
                int remaining = getFastFlightTicks() - 1;
                entityData.set(FAST_TICKS, Math.max(0, remaining));
                if (remaining <= 0) {
                    if (state == FAST_CHARGE) {
                        entityData.set(FAST_STATE, FAST_BURST);
                        entityData.set(FAST_TICKS, FAST_BURST_TICKS);
                        Player rider = getControllingPassenger();
                        Vec3 look = rider != null ? rider.getViewVector(1.0F).normalize() : getLookAngle();
                        setDeltaMovement(look.scale(1.55D));
                        playSound(net.minecraft.sounds.SoundEvents.FIREWORK_ROCKET_LAUNCH, 1.4F, 0.75F);
                        if (level() instanceof net.minecraft.server.level.ServerLevel server) {
                            server.sendParticles(ParticleTypes.EXPLOSION, getX(), getY() + 0.55D, getZ(), 2, 0.15D, 0.15D, 0.15D, 0.0D);
                            server.sendParticles(CYAN_DUST, getX(), getY() + 0.55D, getZ(), 34, 0.8D, 0.5D, 0.8D, 0.08D);
                            server.sendParticles(GOLD_DUST, getX(), getY() + 0.55D, getZ(), 18, 0.9D, 0.35D, 0.9D, 0.06D);
                        }
                    } else if (state == FAST_BURST) {
                        entityData.set(FAST_STATE, FAST_ACTIVE);
                        entityData.set(FAST_TICKS, FAST_FLIGHT_DURATION_TICKS);
                    } else {
                        entityData.set(FAST_STATE, FAST_READY);
                    }
                }
            } else if (state == FAST_ACTIVE) {
                int remaining = getFastFlightTicks() - 1;
                entityData.set(FAST_TICKS, Math.max(0, remaining));
                if (remaining <= 0 || getControllingPassenger() == null || !isSaddled()) beginFastRecovery();
            }
        }
    }

    @Override public boolean isFood(ItemStack stack) { return stack.is(ParadiseItems.PARADISE_FRUIT); }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        return ParadiseEntities.PARADISE_WYVERN.create(level);
    }

    @Override public boolean causeFallDamage(float distance, float multiplier, net.minecraft.world.damagesource.DamageSource source) { return false; }
    @Override protected void checkFallDamage(double y, boolean onGround, net.minecraft.world.level.block.state.BlockState state, BlockPos pos) { }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Saddle", isSaddled());
        tag.putInt("FastFlightCooldown", getFastFlightCooldown());
        tag.putInt("FastFlightTicks", getFastFlightTicks());
        tag.putByte("FastFlightState", getFastFlightState());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        entityData.set(SADDLED, tag.getBoolean("Saddle"));
        entityData.set(FAST_COOLDOWN, Math.max(0, tag.getInt("FastFlightCooldown")));
        entityData.set(FAST_TICKS, Math.max(0, tag.getInt("FastFlightTicks")));
        byte state = tag.contains("FastFlightState") ? tag.getByte("FastFlightState") : FAST_READY;
        entityData.set(FAST_STATE, state >= FAST_READY && state <= FAST_RECOVERY ? state : FAST_READY);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "body", 2, this::animation));
    }

    private PlayState animation(AnimationState<ParadiseWyvernEntity> state) {
        RawAnimation animation = switch (getFastFlightState()) {
            case FAST_CHARGE -> FAST_CHARGE_ANIM;
            case FAST_BURST -> FAST_BURST_ANIM;
            case FAST_ACTIVE -> FAST_FLIGHT_ANIM;
            case FAST_RECOVERY -> FAST_RECOVERY_ANIM;
            default -> isOrderedToSit() ? SIT : state.isMoving() ? FLY : IDLE;
        };
        state.getController().setAnimation(animation);
        return PlayState.CONTINUE;
    }

    private void beginFastRecovery() {
        if (getFastFlightState() == FAST_RECOVERY || getFastFlightState() == FAST_READY) return;
        entityData.set(FAST_STATE, FAST_RECOVERY);
        entityData.set(FAST_TICKS, FAST_RECOVERY_TICKS);
        setDeltaMovement(getDeltaMovement().scale(0.52D));
        if (level() instanceof net.minecraft.server.level.ServerLevel server) {
            server.sendParticles(ParticleTypes.CLOUD, getX(), getY() + 0.45D, getZ(), 14, 0.5D, 0.25D, 0.5D, 0.04D);
        }
    }

    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }

    /** Keeps wild wyverns visibly circling the cloud layer instead of drifting down to terrain. */
    private final class CloudBandRoamGoal extends Goal {
        private Vec3 destination;
        private int remainingTicks;

        @Override public boolean canUse() {
            return !isTame() && !isOrderedToSit() && random.nextInt(24) == 0;
        }

        @Override public void start() {
            double angle = random.nextDouble() * Math.PI * 2.0D;
            double range = 14.0D + random.nextDouble() * 28.0D;
            destination = new Vec3(getX() + Math.cos(angle) * range,
                Mth.clamp(getY() + random.nextInt(33) - 16.0D, 112.0D, 160.0D),
                getZ() + Math.sin(angle) * range);
            remainingTicks = 120;
        }

        @Override public boolean canContinueToUse() {
            return !isTame() && remainingTicks > 0 && destination != null && distanceToSqr(destination) > 9.0D;
        }

        @Override public void tick() {
            remainingTicks--;
            getMoveControl().setWantedPosition(destination.x, destination.y, destination.z, 1.0D);
        }
    }

    private static final class WyvernMoveControl extends MoveControl {
        private WyvernMoveControl(Mob mob) { super(mob); }

        @Override
        public void tick() {
            if (mob.isVehicle()) return;
            if (operation != Operation.MOVE_TO) {
                mob.setDeltaMovement(mob.getDeltaMovement().scale(0.91));
                return;
            }
            Vec3 delta = new Vec3(wantedX - mob.getX(), wantedY - mob.getY(), wantedZ - mob.getZ());
            if (delta.lengthSqr() < 0.25) {
                operation = Operation.WAIT;
                return;
            }
            Vec3 desired = delta.normalize().scale(Math.min(0.30, speedModifier * 0.11));
            mob.setDeltaMovement(mob.getDeltaMovement().scale(0.76).add(desired.scale(0.24)));
            float yaw = (float) Math.toDegrees(Math.atan2(delta.x, delta.z));
            mob.setYRot(yaw);
            mob.yBodyRot = yaw;
        }
    }
}
