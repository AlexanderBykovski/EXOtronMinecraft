package com.opus.client.mixin;

import com.opus.client.model.GreatHelmModel;
import com.opus.client.model.OpusPlateModel;
import com.opus.client.renderer.OpusHelmetLayer;
import com.opus.client.renderer.OpusPlateLayer;
import com.opus.fire.client.layer.FireHelmetLayer;
import com.opus.fire.client.layer.FirePlateLayer;
import com.opus.fire.client.model.FireHelmetModel;
import com.opus.fire.client.model.FirePlateModel;
import com.opus.ember.client.layer.FireDemonicHelmetLayer;
import com.opus.ember.client.layer.FireDemonicPlateLayer;
import com.opus.ember.client.model.FireDemonicHelmetModel;
import com.opus.ember.client.model.FireDemonicPlateModel;
import net.minecraft.client.model.ArmorStandArmorModel;
import net.minecraft.client.renderer.entity.ArmorStandRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.world.entity.decoration.ArmorStand;
import com.opus.paradise.client.model.ParthenonRegaliaModel;
import com.opus.paradise.client.model.AerieBronzeHelmetModel;
import com.opus.paradise.client.model.AerieBronzePlateModel;
import com.opus.paradise.client.renderer.AerieBronzeHelmetLayer;
import com.opus.paradise.client.renderer.AerieBronzePlateLayer;
import com.opus.paradise.client.renderer.ParthenonRegaliaLayer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(ArmorStandRenderer.class)
public abstract class ArmorStandRendererMixin {

    @Inject(method = "<init>(Lnet/minecraft/client/renderer/entity/EntityRendererProvider$Context;)V",
            at = @At("TAIL"))
    private void opusvsexe$addOpusArmorLayers(EntityRendererProvider.Context context, CallbackInfo ci) {
        LivingEntityRendererAccessor<ArmorStand, ArmorStandArmorModel> accessor =
                (LivingEntityRendererAccessor<ArmorStand, ArmorStandArmorModel>) (Object) this;
        accessor.opusvsexe$invokeAddLayer(new OpusHelmetLayer<>((ArmorStandRenderer) (Object) this,
                new GreatHelmModel<>(context.bakeLayer(GreatHelmModel.LAYER_LOCATION))));
        accessor.opusvsexe$invokeAddLayer(new OpusPlateLayer<>((ArmorStandRenderer) (Object) this,
                new OpusPlateModel<>(context.bakeLayer(OpusPlateModel.LAYER_LOCATION))));
        // Fire Biom armor (parallel line)
        accessor.opusvsexe$invokeAddLayer(new FireHelmetLayer<>((ArmorStandRenderer) (Object) this,
                new FireHelmetModel<>(context.bakeLayer(FireHelmetModel.LAYER_LOCATION))));
        accessor.opusvsexe$invokeAddLayer(new FirePlateLayer<>((ArmorStandRenderer) (Object) this,
                new FirePlateModel<>(context.bakeLayer(FirePlateModel.LAYER_LOCATION))));
        // Fire Demonic armor (endgame volcanic set)
        accessor.opusvsexe$invokeAddLayer(new FireDemonicHelmetLayer<>((ArmorStandRenderer) (Object) this,
                new FireDemonicHelmetModel<>(context.bakeLayer(FireDemonicHelmetModel.LAYER_LOCATION))));
        accessor.opusvsexe$invokeAddLayer(new FireDemonicPlateLayer<>((ArmorStandRenderer) (Object) this,
                new FireDemonicPlateModel<>(context.bakeLayer(FireDemonicPlateModel.LAYER_LOCATION))));
        accessor.opusvsexe$invokeAddLayer(new ParthenonRegaliaLayer<>((ArmorStandRenderer)(Object)this,
                new ParthenonRegaliaModel<>(context.bakeLayer(ParthenonRegaliaModel.LAYER_LOCATION))));
        // Aerie Bronze armor layers (roman officer line)
        accessor.opusvsexe$invokeAddLayer(new AerieBronzeHelmetLayer<>((ArmorStandRenderer)(Object)this,
                new AerieBronzeHelmetModel<>(context.bakeLayer(AerieBronzeHelmetModel.LAYER_LOCATION))));
        accessor.opusvsexe$invokeAddLayer(new AerieBronzePlateLayer<>((ArmorStandRenderer)(Object)this,
                new AerieBronzePlateModel<>(context.bakeLayer(AerieBronzePlateModel.LAYER_LOCATION))));
    }
}
