package com.opus.mixin;

import com.opus.paradise.item.ParadisePlayerState;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Player.class)
public abstract class ParadisePlayerStateMixin extends LivingEntity implements ParadisePlayerState {
    @Unique private long opusvsexe$regaliaHurricaneReady;
    @Unique private boolean opusvsexe$regaliaFlightGranted;
    @Unique private boolean opusvsexe$fireDemonicFlightGranted;
    protected ParadisePlayerStateMixin(EntityType<? extends LivingEntity> type,Level level){super(type,level);}
    @Override public long opusvsexe$getRegaliaHurricaneReady(){return opusvsexe$regaliaHurricaneReady;}
    @Override public void opusvsexe$setRegaliaHurricaneReady(long tick){opusvsexe$regaliaHurricaneReady=tick;}
    @Override public boolean opusvsexe$isRegaliaFlightGranted(){return opusvsexe$regaliaFlightGranted;}
    @Override public void opusvsexe$setRegaliaFlightGranted(boolean granted){opusvsexe$regaliaFlightGranted=granted;}
    @Override public boolean opusvsexe$isFireDemonicFlightGranted(){return opusvsexe$fireDemonicFlightGranted;}
    @Override public void opusvsexe$setFireDemonicFlightGranted(boolean granted){opusvsexe$fireDemonicFlightGranted=granted;}
    @Inject(method="addAdditionalSaveData",at=@At("TAIL")) private void opusvsexe$saveRegalia(CompoundTag tag,CallbackInfo ci){tag.putLong("OpusRegaliaHurricaneReady",opusvsexe$regaliaHurricaneReady);tag.putBoolean("OpusRegaliaFlightGranted",opusvsexe$regaliaFlightGranted);tag.putBoolean("OpusFireDemonicFlightGranted",opusvsexe$fireDemonicFlightGranted);}
    @Inject(method="readAdditionalSaveData",at=@At("TAIL")) private void opusvsexe$loadRegalia(CompoundTag tag,CallbackInfo ci){opusvsexe$regaliaHurricaneReady=tag.getLong("OpusRegaliaHurricaneReady");opusvsexe$regaliaFlightGranted=tag.getBoolean("OpusRegaliaFlightGranted");opusvsexe$fireDemonicFlightGranted=tag.getBoolean("OpusFireDemonicFlightGranted");}
}
