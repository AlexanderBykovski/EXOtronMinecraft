package com.opus.settlement.client.model;

import com.opus.settlement.SettlementLine;
import com.opus.settlement.entity.YoungSamuraiEntity;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.util.Mth;

/**
 * Traditional young samurai — calm, disciplined, lean athletic build.
 * Grounded historical design adapted to Minecraft: dark indigo kosode,
 * charcoal hakama, black-brown lacquered do, straw sandals, topknot.
 * No fantasy elements, no glow, no oversized plates.
 *
 * Vanilla second-layer cubes (hat/jacket/sleeves/pants/ear/cloak) are emptied
 * so the custom clothing/armor geometry is the only outer layer (no z-fighting).
 * UV layout: concepts/provmt/young_samurai.md (all regions disjoint on 128x128).
 */
public final class YoungSamuraiModel extends PlayerModel<YoungSamuraiEntity> {
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(SettlementLine.id("young_samurai"), "main");

    public YoungSamuraiModel(ModelPart root) { super(root, false); }

    private static CubeListBuilder empty() { return CubeListBuilder.create(); }

    public static LayerDefinition createLayer() {
        MeshDefinition mesh = PlayerModel.createMesh(CubeDeformation.NONE, false);
        var root = mesh.getRoot();

        // Remove vanilla second-layer cubes (child nodes stay — PlayerModel requires them).
        // NOTE: in 1.20.1 hat/jacket/sleeves/pants/ear/cloak are ROOT children, not nested.
        root.addOrReplaceChild("hat", empty(), PartPose.ZERO);
        root.addOrReplaceChild("jacket", empty(), PartPose.ZERO);
        root.addOrReplaceChild("right_sleeve", empty(), PartPose.ZERO);
        root.addOrReplaceChild("left_sleeve", empty(), PartPose.ZERO);
        root.addOrReplaceChild("right_pants", empty(), PartPose.ZERO);
        root.addOrReplaceChild("left_pants", empty(), PartPose.ZERO);
        root.addOrReplaceChild("ear", empty(), PartPose.ZERO);
        root.addOrReplaceChild("cloak", empty(), PartPose.ZERO);
        var head = root.getChild("head");
        var body = root.getChild("body");
        var rightArm = root.getChild("right_arm");
        var leftArm = root.getChild("left_arm");
        var rightLeg = root.getChild("right_leg");
        var leftLeg = root.getChild("left_leg");

        // HEAD — hair: base layer, controlled hairline, temple strands, rear tie, compact topknot
        head.addOrReplaceChild("hair_base", CubeListBuilder.create().texOffs(56, 0)
            .addBox(-4.5F, -8.8F, -4.5F, 9F, 3F, 9F, new CubeDeformation(0.22F)), PartPose.ZERO);
        // Front fringe strips protrude in front of hair_base (visible hairline, eyes unobstructed)
        head.addOrReplaceChild("hair_front_left", CubeListBuilder.create().texOffs(112, 0)
            .addBox(-4.2F, -8.2F, -4.9F, 3F, 2.8F, 1F, new CubeDeformation(0.08F)), PartPose.ZERO);
        head.addOrReplaceChild("hair_front_right", CubeListBuilder.create().texOffs(112, 5)
            .addBox(1.2F, -8.2F, -4.9F, 3F, 2.8F, 1F, new CubeDeformation(0.08F)), PartPose.ZERO);
        // Restrained temple strands
        head.addOrReplaceChild("hair_side_left", CubeListBuilder.create().texOffs(56, 16)
            .addBox(-5.1F, -7F, -2.2F, 1F, 5F, 4F, new CubeDeformation(0.10F)), PartPose.ZERO);
        head.addOrReplaceChild("hair_side_right", CubeListBuilder.create().texOffs(67, 16)
            .addBox(4.1F, -7F, -2.2F, 1F, 5F, 4F, new CubeDeformation(0.10F)), PartPose.ZERO);
        // Rear tied section
        head.addOrReplaceChild("hair_back", CubeListBuilder.create().texOffs(93, 0)
            .addBox(-3.5F, -7.5F, 3.8F, 7F, 7F, 2F, new CubeDeformation(0.12F)), PartPose.ZERO);
        // Compact topknot, pivot at the tie point on the rear head
        head.addOrReplaceChild("topknot", CubeListBuilder.create().texOffs(93, 10)
            .addBox(-1.75F, -4.1F, -1.75F, 3.5F, 3F, 3.5F, new CubeDeformation(0.05F)),
            PartPose.offset(0F, -7.5F, 3.5F));

        // BODY — inner collar, lacquered do, sode, obi, hakama panels, crest, daisho
        // Off-white inner collar visible at the throat above the do neckline
        body.addOrReplaceChild("collar", CubeListBuilder.create().texOffs(78, 26)
            .addBox(-3.4F, -1.2F, -2.5F, 6.8F, 3F, 1F, new CubeDeformation(0.05F)), PartPose.ZERO);
        // Lightweight black-brown lacquered do, outer layer clear of torso and obi
        body.addOrReplaceChild("chest_armor", CubeListBuilder.create().texOffs(0, 104)
            .addBox(-4.5F, 1.8F, -2.9F, 9F, 8F, 5F, new CubeDeformation(0.38F)), PartPose.ZERO);
        // Narrow practical sode — minimal extension for mobility
        body.addOrReplaceChild("sode_right", CubeListBuilder.create().texOffs(78, 16)
            .addBox(-7.6F, -1F, -2.6F, 4F, 5F, 4F, new CubeDeformation(0.12F)), PartPose.ZERO);
        body.addOrReplaceChild("sode_left", CubeListBuilder.create().texOffs(95, 16)
            .addBox(3.6F, -1F, -2.6F, 4F, 5F, 4F, new CubeDeformation(0.12F)), PartPose.ZERO);
        // Waist obi with knot at back
        body.addOrReplaceChild("obi", CubeListBuilder.create().texOffs(0, 80)
            .addBox(-4.5F, 9F, -2.6F, 9F, 3F, 5F, new CubeDeformation(0.14F)), PartPose.ZERO);
        body.addOrReplaceChild("obi_knot", CubeListBuilder.create().texOffs(112, 16)
            .addBox(-2F, 9.5F, 2.6F, 4F, 3F, 2F, new CubeDeformation(0.08F)), PartPose.ZERO);
        // Hakama front/back panels with vertical folds (upper legs, move with torso)
        body.addOrReplaceChild("hakama_front", CubeListBuilder.create().texOffs(0, 92)
            .addBox(-4.2F, 12F, -2.5F, 8F, 7F, 1F, new CubeDeformation(0.08F)), PartPose.ZERO);
        body.addOrReplaceChild("hakama_back", CubeListBuilder.create().texOffs(20, 92)
            .addBox(-4.2F, 12F, 1.5F, 8F, 7F, 1F, new CubeDeformation(0.08F)), PartPose.ZERO);
        // Small restrained family crest, clear of the do front face (no z-fighting)
        body.addOrReplaceChild("crest", CubeListBuilder.create().texOffs(112, 10)
            .addBox(-4.0F, 3.2F, -3.5F, 3F, 3F, 0.3F), PartPose.ZERO);
        // Daisho at the left waist: katana above/outer, wakizashi below/inner,
        // handles leaning forward, scabbard tips flaring back-down behind the left leg
        body.addOrReplaceChild("katana", CubeListBuilder.create()
            .texOffs(50, 92)
            .addBox(-1F, -5.2F, -1F, 2F, 5F, 2F)                       // tsuka (up, forward)
            .texOffs(40, 92)
            .addBox(-1F, 0.2F, -1F, 2F, 13F, 2F, new CubeDeformation(0.02F)), // saya (down)
            PartPose.offsetAndRotation(3.0F, 9.0F, 3.8F, 0.06F, 0F, -0.34F));
        body.addOrReplaceChild("wakizashi", CubeListBuilder.create()
            .texOffs(70, 92)
            .addBox(-1F, -4.2F, -1F, 2F, 4F, 2F)                       // tsuka
            .texOffs(60, 92)
            .addBox(-1F, 0.2F, -1F, 2F, 10F, 2F, new CubeDeformation(0.02F)), // saya
            PartPose.offsetAndRotation(2.2F, 11.4F, 3.8F, 0.06F, 0F, -0.26F));

        // ARMS — fitted indigo sleeve + kote forearm guard (outer layer, wrist free)
        rightArm.addOrReplaceChild("sleeve_right", CubeListBuilder.create().texOffs(0, 64)
            .addBox(-3.6F, -2F, -2.5F, 4F, 8F, 4F, new CubeDeformation(0.18F)), PartPose.ZERO);
        rightArm.addOrReplaceChild("kote_right", CubeListBuilder.create().texOffs(16, 64)
            .addBox(-3.4F, 3.5F, -2.6F, 4F, 7F, 4F, new CubeDeformation(0.22F)), PartPose.ZERO);
        leftArm.addOrReplaceChild("sleeve_left", CubeListBuilder.create().texOffs(32, 64)
            .addBox(-0.4F, -2F, -2.5F, 4F, 8F, 4F, new CubeDeformation(0.18F)), PartPose.ZERO);
        leftArm.addOrReplaceChild("kote_left", CubeListBuilder.create().texOffs(48, 64)
            .addBox(-0.6F, 3.5F, -2.6F, 4F, 7F, 4F, new CubeDeformation(0.22F)), PartPose.ZERO);

        // LEGS — wide hakama upper leg, compact shin guard, straw sandal
        rightLeg.addOrReplaceChild("hakama_right", CubeListBuilder.create().texOffs(64, 64)
            .addBox(-2.6F, 0F, -2.6F, 5F, 7F, 5F, new CubeDeformation(0.28F)), PartPose.ZERO);
        rightLeg.addOrReplaceChild("shin_right", CubeListBuilder.create().texOffs(104, 64)
            .addBox(-2.8F, 6.5F, -2.8F, 5F, 5F, 5F, new CubeDeformation(0.14F)), PartPose.ZERO);
        rightLeg.addOrReplaceChild("sandal_right", CubeListBuilder.create().texOffs(64, 77)
            .addBox(-2.6F, 11.2F, -3.1F, 5F, 1F, 6F), PartPose.ZERO);
        leftLeg.addOrReplaceChild("hakama_left", CubeListBuilder.create().texOffs(84, 64)
            .addBox(-2.4F, 0F, -2.6F, 5F, 7F, 5F, new CubeDeformation(0.28F)), PartPose.ZERO);
        leftLeg.addOrReplaceChild("shin_left", CubeListBuilder.create().texOffs(104, 75)
            .addBox(-2.2F, 6.5F, -2.8F, 5F, 5F, 5F, new CubeDeformation(0.14F)), PartPose.ZERO);
        leftLeg.addOrReplaceChild("sandal_left", CubeListBuilder.create().texOffs(87, 77)
            .addBox(-2.4F, 11.2F, -3.1F, 5F, 1F, 6F), PartPose.ZERO);

        return LayerDefinition.create(mesh, 128, 128);
    }

    @Override public void setupAnim(YoungSamuraiEntity entity, float limbSwing, float limbAmount, float ageTicks, float netHeadYaw, float headPitch) {
        rightArmPose = HumanoidModel.ArmPose.ITEM;
        leftArmPose = HumanoidModel.ArmPose.EMPTY;
        super.setupAnim(entity, limbSwing, limbAmount, ageTicks, netHeadYaw, headPitch);

        // Economical disciplined walk (applies whenever moving, stance overlays add on top)
        if (limbAmount > 0.1F) {
            float walkSpeed = limbAmount > 0.7F ? 1.0F : 0.6F;
            float swing = Mth.sin(limbSwing * 0.65F) * 0.45F * walkSpeed;
            float swingOpp = Mth.cos(limbSwing * 0.65F) * 0.45F * walkSpeed;
            rightArm.xRot += swing;
            leftArm.xRot += -swing;
            rightLeg.xRot += -swing;
            leftLeg.xRot += swing;
            body.yRot += swingOpp * 0.08F;
        }

        YoungSamuraiEntity.Action action = entity.getAction();
        float tick = entity.getActionTick();

        if (action == YoungSamuraiEntity.Action.NONE) {
            if (entity.hasAura() || entity.getPhase() == 2) {
                // Combat idle: balanced ready stance, knees bent, sword hand ready near the waist
                rightArm.xRot = -0.65F + Mth.sin(ageTicks * 0.07F) * 0.06F;
                rightArm.yRot = -0.22F;
                leftArm.xRot = -0.35F + Mth.sin(ageTicks * 0.07F + 0.9F) * 0.04F;
                leftArm.yRot = 0.30F;
                rightLeg.xRot = -0.18F;
                leftLeg.xRot = 0.12F;
                body.yRot += Mth.sin(ageTicks * 0.04F) * 0.06F;
            } else {
                // Neutral idle: controlled breathing, observant stillness
                float breath = Mth.sin(ageTicks * 0.075F) * 0.04F;
                body.xRot += breath;
            }
            return;
        }

        switch (action) {
            case PHASE -> {
                // Controlled transition — slight torso lift, arms gathering, feet stable, no spin
                float lift = Mth.sin(tick * 0.22F) * 0.10F;
                body.xRot = -0.12F + lift;
                rightArm.xRot = -0.9F - lift;
                leftArm.xRot = -0.9F + lift;
                rightArm.zRot = 0.25F;
                leftArm.zRot = -0.25F;
                rightLeg.xRot = -0.12F;
                leftLeg.xRot = 0.12F;
            }
            case CRIMSON_DRAW -> {
                // Iaido draw: left hand stabilizes the saya, right hand draws in a controlled arc,
                // hips wind then release; dash and cut land on the server contact tick (11)
                if (tick < 7) {
                    float prog = tick / 7F;
                    body.yRot = -0.18F * prog;
                    rightArm.xRot = Mth.lerp(prog, 0F, -1.25F);
                    rightArm.yRot = Mth.lerp(prog, 0F, -0.35F);
                    leftArm.xRot = Mth.lerp(prog, 0F, -0.55F);
                    leftArm.yRot = Mth.lerp(prog, 0F, 0.45F);
                } else if (tick < 12) {
                    float prog = (tick - 7) / 5F;
                    body.yRot = -0.18F - prog * 0.28F;
                    rightArm.xRot = -1.25F - prog * 0.75F;
                    rightArm.yRot = -0.35F - prog * 0.45F;
                    leftArm.xRot = -0.55F - prog * 0.35F;
                    rightLeg.xRot = -0.18F - prog * 0.22F;
                    leftLeg.xRot = 0.12F + prog * 0.18F;
                } else {
                    float prog = (tick - 12) / 16F;
                    body.yRot = Mth.lerp(prog, -0.46F, -0.1F);
                    rightArm.xRot = Mth.lerp(prog, -2.0F, -0.7F);
                    rightArm.yRot = Mth.lerp(prog, -0.80F, -0.25F);
                    leftArm.xRot = Mth.lerp(prog, -0.90F, -0.35F);
                    leftArm.yRot = Mth.lerp(prog, 0.55F, 0.30F);
                    rightLeg.xRot = Mth.lerp(prog, -0.40F, -0.18F);
                    leftLeg.xRot = Mth.lerp(prog, 0.30F, 0.12F);
                }
            }
            case CRESCENT_SWEEP -> {
                // Horizontal cut driven by hip rotation; weight transfers to the front foot,
                // contact on tick 17, balanced recovery through the second half
                float prog = tick / 36F;
                float arc = Mth.sin(prog * 3.14159F) * 0.85F;
                body.yRot = arc * 0.65F;
                rightArm.xRot = -1.45F + arc * 0.22F;
                rightArm.yRot = -0.85F - arc * 0.45F;
                leftArm.xRot = -0.95F - arc * 0.20F;
                leftArm.yRot = 0.40F + arc * 0.30F;
                rightLeg.xRot = -0.22F - arc * 0.25F;
                leftLeg.xRot = 0.22F + arc * 0.18F;
            }
            case RISING_KNEE -> {
                // Stable center, guard covers the rise; strike on tick 15, controlled descent
                if (tick < 18) {
                    float prog = tick / 18F;
                    rightLeg.xRot = Mth.lerp(prog, -0.15F, -1.35F);
                    rightLeg.yRot = -0.08F * prog;
                    leftLeg.xRot = Mth.lerp(prog, 0.12F, 0.38F);
                    rightArm.xRot = Mth.lerp(prog, -0.60F, -1.35F);
                    leftArm.xRot = Mth.lerp(prog, -0.30F, 0.22F);
                    body.xRot = -0.18F * prog;
                } else {
                    float prog = (tick - 18) / 22F;
                    rightLeg.xRot = Mth.lerp(prog, -1.35F, -0.15F);
                    leftLeg.xRot = Mth.lerp(prog, 0.38F, 0.12F);
                    rightArm.xRot = Mth.lerp(prog, -1.35F, -0.60F);
                    leftArm.xRot = Mth.lerp(prog, 0.22F, -0.30F);
                    body.xRot = -0.18F * (1F - prog);
                }
            }
            case LOTUS_BARRAGE -> {
                // Alternating diagonal cuts, torso counterswing, feet planted, contact on 8/14/20/26
                float cross = Mth.sin(tick * 0.65F) * 0.55F;
                rightArm.xRot = -1.42F + cross * 0.55F;
                leftArm.xRot = -1.28F - cross * 0.45F;
                rightArm.yRot = -0.45F * cross;
                body.yRot = 0.28F * cross;
                rightLeg.xRot = -0.18F + Mth.abs(cross) * 0.20F;
                leftLeg.xRot = 0.18F - Mth.abs(cross) * 0.12F;
            }
            case FLASH_STEP -> {
                // Dodge step: crouch load, precise strike after relocation, balanced recovery
                if (tick < 8) {
                    float prog = tick / 8F;
                    body.xRot = 0.12F * prog;
                    body.yRot = -0.35F * prog;
                    rightArm.xRot = Mth.lerp(prog, -0.60F, -1.85F);
                    leftArm.xRot = Mth.lerp(prog, -0.30F, 0.42F);
                    rightLeg.xRot = Mth.lerp(prog, -0.18F, -0.65F);
                    leftLeg.xRot = Mth.lerp(prog, 0.12F, 0.55F);
                } else if (tick < 14) {
                    rightArm.xRot = -1.85F;
                    rightArm.yRot = -0.32F;
                    leftArm.xRot = 0.42F;
                    body.yRot = -0.35F;
                } else {
                    float prog = (tick - 14) / 12F;
                    body.yRot = Mth.lerp(prog, -0.35F, 0F);
                    rightArm.xRot = Mth.lerp(prog, -1.85F, -0.65F);
                    leftArm.xRot = Mth.lerp(prog, 0.42F, -0.30F);
                    body.xRot = 0.12F * (1F - prog);
                }
            }
            default -> { }
        }
    }
}
