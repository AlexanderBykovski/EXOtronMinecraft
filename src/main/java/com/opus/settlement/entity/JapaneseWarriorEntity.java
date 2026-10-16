package com.opus.settlement.entity;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Shared brain for the two Japanese warriors. Drives the full action library:
 * locomotion, combat idle, melee swings, guard/parry defense, evasive dodges,
 * the samurai command shout and the per-class special technique (iai lunge /
 * smoke step). Visuals are rendered on the vanilla player rig by
 * {@link com.opus.settlement.client.model.WarriorPlayerModel}, which reads
 * {@link #getActionState()} / {@link #getActionTickClient()}.
 */
public abstract class JapaneseWarriorEntity extends Monster {
    public static final int ACTION_NONE = 0;
    public static final int ACTION_SMOKE_STEP = 1;
    public static final int ACTION_LONG_LUNGE = 2;
    public static final int ACTION_MELEE = 3;
    public static final int ACTION_THROW = 4;
    public static final int ACTION_GUARD = 5;
    public static final int ACTION_PARRY = 6;
    public static final int ACTION_DODGE_L = 7;
    public static final int ACTION_DODGE_R = 8;
    public static final int ACTION_COMMAND = 9;

    private static final EntityDataAccessor<Integer> ACTION = SynchedEntityData.defineId(JapaneseWarriorEntity.class, EntityDataSerializers.INT);
    private int actionTicks;
    private int techniqueCooldown;
    private int guardCooldown;
    private int dodgeCooldown;
    private int commandCooldown;
    private int calmTicks;
    private int meleeVariant;
    // client-side mirror of the action timer (drives the vanilla-rig poses)
    private int clientActionTicks;
    private int clientActionSeen = -1;

    protected JapaneseWarriorEntity(EntityType<? extends Monster> type, Level level) {
        super(type, level);
        setPersistenceRequired();
    }

    protected abstract ItemStack defaultWeapon();
    protected abstract int specialAction();
    protected abstract int actionWindup();
    protected abstract float techniqueDamage();
    /** Command shout is a shogun trait. */
    protected boolean commandsTroops() { return false; }

    @Override protected void defineSynchedData() { super.defineSynchedData(); entityData.define(ACTION, ACTION_NONE); }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15D, true) {
            @Override public boolean canUse() { return canAct() && super.canUse(); }
            @Override public boolean canContinueToUse() { return canAct() && super.canContinueToUse(); }
        });
        goalSelector.addGoal(6, new RandomStrollGoal(this, .8D) {
            @Override public boolean canUse() { return canAct() && super.canUse(); }
        });
        goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 12F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    /** Melee/stroll pause during committed moves only (not during swings/dodges). */
    private boolean canAct() {
        int a = getActionState();
        return a == ACTION_NONE || a == ACTION_MELEE || a == ACTION_DODGE_L || a == ACTION_DODGE_R || a == ACTION_COMMAND;
    }

    @Override
    protected void populateDefaultEquipmentSlots(net.minecraft.util.RandomSource random, net.minecraft.world.DifficultyInstance difficulty) {
        setItemSlot(EquipmentSlot.MAINHAND, defaultWeapon());
        setDropChance(EquipmentSlot.MAINHAND, .08F);
    }

    @Override
    public void swing(InteractionHand hand) {
        super.swing(hand);
        if (!level().isClientSide && getActionState() == ACTION_NONE) {
            setActionForQa(ACTION_MELEE);
            actionTicks = 14;
            meleeVariant++;
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (getMainHandItem().isEmpty()) setItemSlot(EquipmentSlot.MAINHAND, defaultWeapon());
        if (techniqueCooldown > 0) techniqueCooldown--;
        if (guardCooldown > 0) guardCooldown--;
        if (dodgeCooldown > 0) dodgeCooldown--;
        if (commandCooldown > 0) commandCooldown--;
        LivingEntity target = getTarget();

        if (getActionState() == ACTION_NONE && techniqueCooldown == 0 && target != null && target.isAlive()
            && distanceToSqr(target) >= 9D && distanceToSqr(target) <= 100D) beginTechnique();
        tickTechnique(target);

        if (getActionState() == ACTION_NONE && target != null && target.isAlive()) {
            // guard stance when the enemy presses in
            if (guardCooldown == 0 && distanceToSqr(target) < 25D && random.nextInt(40) == 0) {
                setActionForQa(ACTION_GUARD);
                actionTicks = 24;
                guardCooldown = 100;
            } else if (commandsTroops() && commandCooldown == 0) {
                // rally shout when a fight starts after a long calm period
                if (calmTicks > 200) {
                    setActionForQa(ACTION_COMMAND);
                    actionTicks = 28;
                    commandCooldown = 600;
                    calmTicks = 0;
                    playSound(SoundEvents.VILLAGER_NO, 1.1F, 0.6F);
                }
            }
        }
        if (target == null) calmTicks++; else calmTicks = 0;
    }

    public void beginTechnique() {
        entityData.set(ACTION, specialAction());
        actionTicks = actionWindup() + 8;
        techniqueCooldown = specialAction() == ACTION_SMOKE_STEP ? 90 : 120;
        getNavigation().stop();
        if (level() instanceof ServerLevel server) server.sendParticles(
            specialAction() == ACTION_SMOKE_STEP ? ParticleTypes.LARGE_SMOKE : ParticleTypes.CRIT,
            getX(), getY() + 1D, getZ(), specialAction() == ACTION_SMOKE_STEP ? 18 : 12, .45D, .8D, .45D, .04D);
    }

    private void tickTechnique(LivingEntity target) {
        int action = getActionState();
        if (action == ACTION_NONE) return;
        actionTicks--;
        if (target != null) getLookControl().setLookAt(target, 40F, 40F);
        if (action == ACTION_SMOKE_STEP || action == ACTION_LONG_LUNGE) {
            if (actionTicks == 8 && target != null) {
                Vec3 direction = target.position().subtract(position());
                if (direction.lengthSqr() > .01D) {
                    direction = new Vec3(direction.x, 0, direction.z).normalize();
                    setDeltaMovement(direction.scale(action == ACTION_SMOKE_STEP ? 1.45D : 1.10D).add(0, .12D, 0));
                }
            }
            if (actionTicks == 5 && target != null && distanceToSqr(target) <= (action == ACTION_SMOKE_STEP ? 12.25D : 20.25D)) {
                applyTechniqueHit(target);
                swing(InteractionHand.MAIN_HAND);
            }
        }
        if (actionTicks <= 0) entityData.set(ACTION, ACTION_NONE);
    }

    public boolean applyTechniqueHit(LivingEntity target) {
        boolean hit = target.hurt(level().damageSources().mobAttack(this), techniqueDamage());
        if (hit) {
            Vec3 away = target.position().subtract(position()).normalize();
            target.push(away.x * (specialAction() == ACTION_LONG_LUNGE ? 1.2D : .65D), .25D, away.z * (specialAction() == ACTION_LONG_LUNGE ? 1.2D : .65D));
            playSound(SoundEvents.PLAYER_ATTACK_SWEEP, 1F, specialAction() == ACTION_LONG_LUNGE ? .75F : 1.25F);
        }
        return hit;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (level().isClientSide) return super.hurt(source, amount);
        int action = getActionState();
        // parry window: first 8 ticks of the guard
        if (action == ACTION_GUARD && actionTicks > 16 && source.getEntity() instanceof LivingEntity attacker
            && distanceToSqr(attacker) < 36D) {
            setActionForQa(ACTION_PARRY);
            actionTicks = 10;
            playSound(SoundEvents.SHIELD_BLOCK, 1F, 1.2F);
            Vec3 away = attacker.position().subtract(position()).normalize();
            attacker.push(away.x * .8D, .3D, away.z * .8D);
            if (level() instanceof ServerLevel server) server.sendParticles(ParticleTypes.CRIT,
                getX(), getY() + 1.4D, getZ(), 8, .3D, .5D, .3D, .1D);
            return false;
        }
        if (action == ACTION_GUARD) {
            amount *= 0.4F; // guarded: 60% reduction
        } else if ((action == ACTION_NONE || action == ACTION_MELEE) && dodgeCooldown == 0
            && source.getEntity() instanceof LivingEntity && random.nextInt(100) < 30 && onGround()) {
            // evasive sidestep
            boolean left = random.nextBoolean();
            setActionForQa(left ? ACTION_DODGE_L : ACTION_DODGE_R);
            actionTicks = 12;
            dodgeCooldown = 80;
            Vec3 away = position().subtract(source.getEntity().position()).normalize();
            Vec3 side = new Vec3(-away.z, 0, away.x).scale(left ? 0.9D : -0.9D);
            setDeltaMovement(side.add(away.x * .3D, .18D, away.z * .3D));
        }
        return super.hurt(source, amount);
    }

    public int getActionState() { return entityData.get(ACTION); }
    public void setActionForQa(int action) { entityData.set(ACTION, action); }
    public int meleeVariant() { return meleeVariant; }

    /**
     * Local (client) tick counter for the current action, used by the vanilla
     * rig ({@code WarriorPlayerModel}) to pose attacks and techniques.
     */
    public int getActionTickClient() { return this.clientActionTicks; }

    @Override
    public void tick() {
        super.tick();
        if (this.level().isClientSide) {
            int action = getActionState();
            if (action != this.clientActionSeen) {
                this.clientActionSeen = action;
                this.clientActionTicks = 0;
            } else {
                this.clientActionTicks++;
            }
        }
    }

    @Override public boolean removeWhenFarAway(double distance) { return false; }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("WarriorAction", getActionState()); tag.putInt("ActionTicks", actionTicks);
        tag.putInt("TechniqueCooldown", techniqueCooldown); tag.putInt("GuardCooldown", guardCooldown);
        tag.putInt("DodgeCooldown", dodgeCooldown); tag.putInt("CommandCooldown", commandCooldown);
    }
    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        entityData.set(ACTION, tag.getInt("WarriorAction")); actionTicks = tag.getInt("ActionTicks");
        techniqueCooldown = tag.getInt("TechniqueCooldown"); guardCooldown = tag.getInt("GuardCooldown");
        dodgeCooldown = tag.getInt("DodgeCooldown"); commandCooldown = tag.getInt("CommandCooldown");
    }
}
