package com.opus.paradise.item;

import com.opus.paradise.entity.HurricaneEntity;
import com.opus.paradise.registry.ParadiseEntities;
import com.opus.paradise.registry.ParadiseItems;
import com.opus.item.SetHealthBonus;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import org.joml.Vector3f;

import java.util.UUID;
import java.util.HashSet;
import java.util.Set;

public final class ParthenonArmorBonus {
    public static final int HURRICANE_COOLDOWN=300;
    private static final UUID HEALTH_ID=UUID.fromString("b03b61b7-b153-4f08-934f-ec820a6fa035");
    private static final UUID AERIE_HEALTH_ID=UUID.fromString("003a54e1-ba84-4c18-baf6-10fdc3aa686a");
    private static final Set<UUID> AERIE_SUITS=new HashSet<>();
    private static final DustParticleOptions CYAN=new DustParticleOptions(new Vector3f(.22F,.94F,1F),1.1F);
    private ParthenonArmorBonus(){ }

    public static boolean isFullSet(Player player){return player!=null&&player.getItemBySlot(EquipmentSlot.HEAD).is(ParadiseItems.PARTHENON_HELMET)&&player.getItemBySlot(EquipmentSlot.CHEST).is(ParadiseItems.PARTHENON_CHESTPLATE)&&player.getItemBySlot(EquipmentSlot.LEGS).is(ParadiseItems.PARTHENON_LEGGINGS)&&player.getItemBySlot(EquipmentSlot.FEET).is(ParadiseItems.PARTHENON_BOOTS);}
    public static boolean isFullAerieSet(Player player){return player!=null&&player.getItemBySlot(EquipmentSlot.HEAD).is(ParadiseItems.AERIE_BRONZE_HELMET)&&player.getItemBySlot(EquipmentSlot.CHEST).is(ParadiseItems.AERIE_BRONZE_CHESTPLATE)&&player.getItemBySlot(EquipmentSlot.LEGS).is(ParadiseItems.AERIE_BRONZE_LEGGINGS)&&player.getItemBySlot(EquipmentSlot.FEET).is(ParadiseItems.AERIE_BRONZE_BOOTS);}
    public static boolean hasChest(Player player){return player!=null&&player.getItemBySlot(EquipmentSlot.CHEST).is(ParadiseItems.PARTHENON_CHESTPLATE);}

    public static boolean tryAimedHurricane(ServerPlayer player){
        if(!player.isAlive()||player.isSpectator()||!isFullSet(player))return false;
        ParadisePlayerState state=(ParadisePlayerState)player;long now=player.server.overworld().getGameTime();long ready=state.opusvsexe$getRegaliaHurricaneReady();
        if(now<ready){player.displayClientMessage(Component.translatable("message.opusvsexe.parthenon_hurricane_cooldown",String.format(java.util.Locale.ROOT,"%.1f",(ready-now)/20D)),true);return false;}
        Vec3 start=player.getEyePosition();Vec3 end=start.add(player.getLookAngle().scale(48));HitResult block=player.level().clip(new ClipContext(start,end,ClipContext.Block.COLLIDER,ClipContext.Fluid.NONE,player));
        float max=(float)(block.getType()==HitResult.Type.MISS?48*48:start.distanceToSqr(block.getLocation()));EntityHitResult entity=ProjectileUtil.getEntityHitResult(player.level(),player,start,end,new AABB(start,end).inflate(1),e->e instanceof LivingEntity&&e!=player&&!e.isSpectator(),max);
        Vec3 target=entity!=null?entity.getLocation():block.getType()!=HitResult.Type.MISS?block.getLocation():end;
        HurricaneEntity hurricane=new HurricaneEntity(ParadiseEntities.HURRICANE,player.level());hurricane.setPos(target);hurricane.setCaster(player,null);player.level().addFreshEntity(hurricane);
        state.opusvsexe$setRegaliaHurricaneReady(now+HURRICANE_COOLDOWN);player.getCooldowns().addCooldown(ParadiseItems.PARTHENON_CHESTPLATE,HURRICANE_COOLDOWN);
        player.serverLevel().sendParticles(CYAN,target.x,target.y+.2,target.z,28,1.2,.3,1.2,.05);player.level().playSound(null,target.x,target.y,target.z,SoundEvents.BEACON_ACTIVATE,SoundSource.PLAYERS,1.4F,1.25F);
        player.displayClientMessage(Component.translatable("message.opusvsexe.parthenon_hurricane_cast"),true);return true;
    }

    public static void init(){ServerTickEvents.END_WORLD_TICK.register(world->{for(ServerPlayer player:world.players())tick(player);});}
    static void tick(ServerPlayer player){for(var stack:player.getArmorSlots())ParadiseEquipment.applyIntrinsic(stack);updateAerie(player);updateHealth(player);updateFlight(player);}
    private static void updateHealth(ServerPlayer player){SetHealthBonus.update(player,HEALTH_ID,"parthenon_regalia_vitality",15D,player.isAlive()&&isFullSet(player));}
    private static void updateAerie(ServerPlayer player){boolean full=player.isAlive()&&isFullAerieSet(player);SetHealthBonus.update(player,AERIE_HEALTH_ID,"aerie_bronze_vitality",10D,full);if(full){apply(player,MobEffects.SLOW_FALLING,0);apply(player,MobEffects.WATER_BREATHING,0);AERIE_SUITS.add(player.getUUID());}else if(AERIE_SUITS.remove(player.getUUID())){player.removeEffect(MobEffects.SLOW_FALLING);player.removeEffect(MobEffects.WATER_BREATHING);}}
    private static void apply(ServerPlayer player,net.minecraft.world.effect.MobEffect effect,int amplifier){var current=player.getEffect(effect);if(current==null||current.getAmplifier()<amplifier||current.getDuration()<210)player.addEffect(new net.minecraft.world.effect.MobEffectInstance(effect,240,amplifier,false,false,true));}
    private static void updateFlight(ServerPlayer player){ParadisePlayerState state=(ParadisePlayerState)player;boolean chest=player.isAlive()&&hasChest(player);if(chest&&!player.getAbilities().mayfly){player.getAbilities().mayfly=true;state.opusvsexe$setRegaliaFlightGranted(true);player.onUpdateAbilities();}else if(!chest&&state.opusvsexe$isRegaliaFlightGranted()&&!player.isCreative()&&!player.isSpectator()){state.opusvsexe$setRegaliaFlightGranted(false);player.getAbilities().mayfly=false;player.getAbilities().flying=false;player.onUpdateAbilities();}}
}
