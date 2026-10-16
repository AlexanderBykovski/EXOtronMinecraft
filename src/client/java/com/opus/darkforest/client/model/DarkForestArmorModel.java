package com.opus.darkforest.client.model;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;

/**
 * Union rig for the two dark-forest sets (see scripts/gen_armor_rework/gen_darkforest.py):
 * briarweave (ancient bark, growth-ring core, root bindings, moss/lichen, NO glow)
 * and dark forest vestments (branching antlers, petrified crown, T-visor, leaf
 * plates around a violet spatial core, teleport seams). Variant is chosen by the
 * render layer; bones of the other variant stay hidden.
 */
public final class DarkForestArmorModel<T extends LivingEntity> extends EntityModel<T> {
    public static final ModelLayerLocation BRIAR_LAYER =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "briarweave_armor"), "main");
    public static final ModelLayerLocation VESTMENTS_LAYER =
        new ModelLayerLocation(new ResourceLocation("opusvsexe", "dark_forest_vestments"), "main");

    private final ModelPart root;
    public DarkForestArmorModel(ModelPart root) { this.root = root; }
    public ModelPart root() { return root; }
    public ModelPart head() { return root.getChild("head"); }
    public ModelPart body() { return root.getChild("body"); }
    public ModelPart rightArm() { return root.getChild("right_arm"); }
    public ModelPart leftArm() { return root.getChild("left_arm"); }
    public ModelPart rightLeg() { return root.getChild("right_leg"); }
    public ModelPart leftLeg() { return root.getChild("left_leg"); }
    public ModelPart shoulderLeft() { return root.getChild("body").getChild("shoulder_left"); }
    public ModelPart shoulderRight() { return root.getChild("body").getChild("shoulder_right"); }

    /** Per-piece visibility for the active variant (children exist per bake). */
    public void setPieces(boolean head, boolean chest, boolean legs, boolean feet, boolean vestments) {
        head().visible = head;
        body().visible = chest;
        rightArm().visible = chest;
        leftArm().visible = chest;
        shoulderLeft().visible = chest;
        shoulderRight().visible = chest;
        if (vestments) {
            rightLeg().getChild("vest_thigh_r").visible = legs;
            rightLeg().getChild("vest_knee_r").visible = legs || feet;
            rightLeg().getChild("vest_greave_r").visible = feet;
            rightLeg().getChild("vest_boot_r").visible = feet;
            leftLeg().getChild("vest_thigh_l").visible = legs;
            leftLeg().getChild("vest_knee_l").visible = legs || feet;
            leftLeg().getChild("vest_greave_l").visible = feet;
            leftLeg().getChild("vest_boot_l").visible = feet;
            head().getChild("antler_left_root").visible = head;
            head().getChild("antler_right_root").visible = head;
        } else {
            rightLeg().getChild("briar_thigh_r").visible = legs;
            rightLeg().getChild("briar_knee_r").visible = legs || feet;
            rightLeg().getChild("briar_greave_r").visible = feet;
            rightLeg().getChild("briar_boot_r").visible = feet;
            leftLeg().getChild("briar_thigh_l").visible = legs;
            leftLeg().getChild("briar_knee_l").visible = legs || feet;
            leftLeg().getChild("briar_greave_l").visible = feet;
            leftLeg().getChild("briar_boot_l").visible = feet;
        }
    }

    public static LayerDefinition createBriarLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_arm = root.addOrReplaceChild("right_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_arm = root.addOrReplaceChild("left_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_leg = root.addOrReplaceChild("right_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_leg = root.addOrReplaceChild("left_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));
        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));
        head.addOrReplaceChild("briar_crown", CubeListBuilder.create()
            .texOffs(27, 0).addBox(0F, 0F, 0F, 9F, 4F, 9F, new CubeDeformation(0.5f)),
            PartPose.offset(-4.6F, -8.6F, -4.6F));
        head.addOrReplaceChild("briar_crown_lo", CubeListBuilder.create()
            .texOffs(64, 0).addBox(0F, 0F, 0F, 9F, 2F, 9F, new CubeDeformation(0.5f)),
            PartPose.offset(-4.9F, -4.3F, -4.9F));
        head.addOrReplaceChild("briar_forehead_1", CubeListBuilder.create()
            .texOffs(35, 49).addBox(0F, 0F, 0F, 8F, 2F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.3F, -8.4F, -5.5F));
        head.addOrReplaceChild("briar_forehead_2", CubeListBuilder.create()
            .texOffs(54, 49).addBox(0F, 0F, 0F, 7F, 2F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.7F, -6.6F, -5.6F));
        head.addOrReplaceChild("briar_window", CubeListBuilder.create()
            .texOffs(24, 49).addBox(0F, 0F, 0F, 4F, 3F, 1F),
            PartPose.offset(-2.4F, -6.9F, -5.1F));
        head.addOrReplaceChild("briar_cheek_l", CubeListBuilder.create()
            .texOffs(104, 26).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(4.0F, -6.4F, -4.3F));
        head.addOrReplaceChild("briar_cheek_r", CubeListBuilder.create()
            .texOffs(113, 26).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.3F, -6.4F, -4.3F));
        head.addOrReplaceChild("briar_rear", CubeListBuilder.create()
            .texOffs(95, 36).addBox(0F, 0F, 0F, 8F, 4F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.2F, -6.6F, 3.9F));
        head.addOrReplaceChild("briar_root_bind_l", CubeListBuilder.create()
            .texOffs(78, 26).addBox(0F, 0F, 0F, 1F, 3F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(4.4F, -5.2F, -2.4F));
        head.addOrReplaceChild("briar_root_bind_r", CubeListBuilder.create()
            .texOffs(91, 26).addBox(0F, 0F, 0F, 1F, 3F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.3F, -5.2F, -2.4F));
        head.addOrReplaceChild("briar_lichen_c", CubeListBuilder.create()
            .texOffs(71, 49).addBox(0F, 0F, 0F, 2F, 1F, 2F, new CubeDeformation(0.1f)),
            PartPose.offset(-1.4F, -9.2F, 2.0F));
        body.addOrReplaceChild("briar_inner", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 8F, 10F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.0F, 0.6F, -2.5F));
        body.addOrReplaceChild("briar_harness", CubeListBuilder.create()
            .texOffs(101, 0).addBox(0F, 0F, 0F, 8F, 10F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.3F, 1.0F, -2.8F));
        body.addOrReplaceChild("briar_slab_top", CubeListBuilder.create()
            .texOffs(0, 16).addBox(0F, 0F, 0F, 9F, 3F, 6F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.5F, 1.2F, -3.0F));
        body.addOrReplaceChild("briar_slab_mid", CubeListBuilder.create()
            .texOffs(31, 16).addBox(0F, 0F, 0F, 8F, 3F, 6F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.4F, 4.6F, -2.95F));
        body.addOrReplaceChild("briar_slab_low", CubeListBuilder.create()
            .texOffs(51, 26).addBox(0F, 0F, 0F, 8F, 3F, 5F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.3F, 7.8F, -2.9F));
        body.addOrReplaceChild("briar_ring_core", CubeListBuilder.create()
            .texOffs(13, 49).addBox(0F, 0F, 0F, 4F, 4F, 1F),
            PartPose.offset(-2.2F, 2.6F, -3.25F));
        body.addOrReplaceChild("briar_back", CubeListBuilder.create()
            .texOffs(60, 16).addBox(0F, 0F, 0F, 7F, 8F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.9F, 1.6F, 2.6F));
        body.addOrReplaceChild("briar_belt", CubeListBuilder.create()
            .texOffs(0, 36).addBox(0F, 0F, 0F, 8F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.4F, 10.6F, -2.8F));
        body.addOrReplaceChild("briar_buckle", CubeListBuilder.create()
            .texOffs(80, 49).addBox(0F, 0F, 0F, 2F, 1F, 1F),
            PartPose.offset(-1.0F, 10.7F, -3.3F));
        shoulder_left.addOrReplaceChild("briar_sh_l", CubeListBuilder.create()
            .texOffs(69, 36).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(2.9F, -2.7F, -2.4F));
        shoulder_left.addOrReplaceChild("briar_sh_l_lo", CubeListBuilder.create()
            .texOffs(106, 43).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(3.0F, 0.1F, -2.2F));
        shoulder_right.addOrReplaceChild("briar_sh_r", CubeListBuilder.create()
            .texOffs(82, 36).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(-5.7F, -2.7F, -2.4F));
        shoulder_right.addOrReplaceChild("briar_sh_r_lo", CubeListBuilder.create()
            .texOffs(0, 49).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(-5.6F, 0.1F, -2.2F));
        right_arm.addOrReplaceChild("briar_guard_r", CubeListBuilder.create()
            .texOffs(77, 16).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.4F, 3.9F, -2.35F));
        right_arm.addOrReplaceChild("briar_bind_r", CubeListBuilder.create()
            .texOffs(38, 43).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.5F, 9.0F, -2.45F));
        right_arm.addOrReplaceChild("briar_cuff_r", CubeListBuilder.create()
            .texOffs(55, 43).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.3F, 10.4F, -2.3F));
        left_arm.addOrReplaceChild("briar_guard_l", CubeListBuilder.create()
            .texOffs(94, 16).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.2F, 3.9F, -2.35F));
        left_arm.addOrReplaceChild("briar_bind_l", CubeListBuilder.create()
            .texOffs(72, 43).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.3F, 9.0F, -2.45F));
        left_arm.addOrReplaceChild("briar_cuff_l", CubeListBuilder.create()
            .texOffs(89, 43).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.2F, 10.4F, -2.3F));
        right_leg.addOrReplaceChild("briar_thigh_r", CubeListBuilder.create()
            .texOffs(111, 16).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.4F, -2.3F));
        right_leg.addOrReplaceChild("briar_knee_r", CubeListBuilder.create()
            .texOffs(0, 43).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        right_leg.addOrReplaceChild("briar_greave_r", CubeListBuilder.create()
            .texOffs(0, 26).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.2F, -2.3F));
        right_leg.addOrReplaceChild("briar_boot_r", CubeListBuilder.create()
            .texOffs(27, 36).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.1F, -2.75F));
        left_leg.addOrReplaceChild("briar_thigh_l", CubeListBuilder.create()
            .texOffs(17, 26).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.4F, -2.3F));
        left_leg.addOrReplaceChild("briar_knee_l", CubeListBuilder.create()
            .texOffs(19, 43).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        left_leg.addOrReplaceChild("briar_greave_l", CubeListBuilder.create()
            .texOffs(34, 26).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.2F, -2.3F));
        left_leg.addOrReplaceChild("briar_boot_l", CubeListBuilder.create()
            .texOffs(48, 36).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.1F, -2.75F));
        return LayerDefinition.create(mesh, 128, 128);
    }

    public static LayerDefinition createVestmentsLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_arm = root.addOrReplaceChild("right_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_arm = root.addOrReplaceChild("left_arm", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition right_leg = root.addOrReplaceChild("right_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition left_leg = root.addOrReplaceChild("left_leg", CubeListBuilder.create(), PartPose.ZERO);
        PartDefinition shoulder_left = body.addOrReplaceChild("shoulder_left", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));
        PartDefinition shoulder_right = body.addOrReplaceChild("shoulder_right", CubeListBuilder.create(), PartPose.offset(-5.0F, 2.0F, 0.0F));
        PartDefinition antler_left_root = head.addOrReplaceChild("antler_left_root", CubeListBuilder.create(), PartPose.offsetAndRotation(2.9F, -8.8F, -1.2F, 6F, 14F, -22F));
        PartDefinition antler_left_trunk = head.addOrReplaceChild("antler_left_trunk", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.7F, -5.2F, -0.5F, -8F, 6F, -8F));
        PartDefinition antler_left_branch_a = head.addOrReplaceChild("antler_left_branch_a", CubeListBuilder.create(), PartPose.offsetAndRotation(0.2F, -2.4F, -0.2F, -20F, 0F, 30F));
        PartDefinition antler_left_branch_b = head.addOrReplaceChild("antler_left_branch_b", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.6F, -2.2F, 0.4F, 14F, 0F, -26F));
        PartDefinition antler_left_tip = head.addOrReplaceChild("antler_left_tip", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.4F, -2.6F, -0.2F, -6F, 0F, -10F));
        PartDefinition antler_right_root = head.addOrReplaceChild("antler_right_root", CubeListBuilder.create(), PartPose.offsetAndRotation(-3.5F, -8.8F, -1.2F, 6F, -14F, 22F));
        PartDefinition antler_right_trunk = head.addOrReplaceChild("antler_right_trunk", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.6F, -5.2F, -0.5F, -8F, -6F, 8F));
        PartDefinition antler_right_branch_a = head.addOrReplaceChild("antler_right_branch_a", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.5F, -2.4F, -0.2F, -20F, 0F, -30F));
        PartDefinition antler_right_branch_b = head.addOrReplaceChild("antler_right_branch_b", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.6F, -2.2F, 0.4F, 14F, 0F, 26F));
        PartDefinition antler_right_tip = head.addOrReplaceChild("antler_right_tip", CubeListBuilder.create(), PartPose.offsetAndRotation(-0.4F, -2.6F, -0.2F, -6F, 0F, 10F));
        head.addOrReplaceChild("vest_helm", CubeListBuilder.create()
            .texOffs(0, 0).addBox(0F, 0F, 0F, 9F, 8F, 9F, new CubeDeformation(0.5f)),
            PartPose.offset(-4.5F, -8.6F, -4.5F));
        head.addOrReplaceChild("vest_crown", CubeListBuilder.create()
            .texOffs(91, 0).addBox(0F, 0F, 0F, 9F, 2F, 9F, new CubeDeformation(0.5f)),
            PartPose.offset(-4.8F, -9.4F, -4.8F));
        head.addOrReplaceChild("vest_brow", CubeListBuilder.create()
            .texOffs(78, 52).addBox(0F, 0F, 0F, 8F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.4F, -6.4F, -5.5F));
        head.addOrReplaceChild("vest_visor", CubeListBuilder.create()
            .texOffs(13, 52).addBox(0F, 0F, 0F, 2F, 4F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.1F, -6.2F, -5.5F));
        head.addOrReplaceChild("vest_visor_h", CubeListBuilder.create()
            .texOffs(97, 52).addBox(0F, 0F, 0F, 5F, 1F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.6F, -4.9F, -5.45F));
        head.addOrReplaceChild("vest_visor_back", CubeListBuilder.create()
            .texOffs(69, 38).addBox(0F, 0F, 0F, 5F, 5F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.7F, -6.3F, -4.7F));
        head.addOrReplaceChild("vest_cheek_l", CubeListBuilder.create()
            .texOffs(78, 28).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(4.0F, -6.2F, -4.3F));
        head.addOrReplaceChild("vest_cheek_r", CubeListBuilder.create()
            .texOffs(87, 28).addBox(0F, 0F, 0F, 1F, 4F, 3F, new CubeDeformation(0.05f)),
            PartPose.offset(-5.3F, -6.2F, -4.3F));
        head.addOrReplaceChild("vest_neck", CubeListBuilder.create()
            .texOffs(20, 52).addBox(0F, 0F, 0F, 8F, 3F, 1F, new CubeDeformation(0.05f)),
            PartPose.offset(-4.1F, -3.4F, 3.6F));
        antler_left_root.addOrReplaceChild("vest_antler_l_root", CubeListBuilder.create()
            .texOffs(96, 28).addBox(0F, 0F, 0F, 2F, 5F, 2F),
            PartPose.offset(-1.1F, -1.2F, -1.1F));
        antler_left_trunk.addOrReplaceChild("vest_antler_l_trunk", CubeListBuilder.create()
            .texOffs(119, 38).addBox(0F, 0F, 0F, 1F, 5F, 1F),
            PartPose.offset(-0.9F, -5.2F, -0.9F));
        antler_left_branch_a.addOrReplaceChild("vest_antler_l_ba", CubeListBuilder.create()
            .texOffs(48, 52).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(-0.7F, -3.0F, -0.7F));
        antler_left_branch_b.addOrReplaceChild("vest_antler_l_bb", CubeListBuilder.create()
            .texOffs(53, 52).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(-0.7F, -2.8F, -0.7F));
        antler_left_tip.addOrReplaceChild("vest_antler_l_tip", CubeListBuilder.create()
            .texOffs(68, 52).addBox(0F, 0F, 0F, 1F, 2F, 1F),
            PartPose.offset(-0.5F, -2.4F, -0.5F));
        antler_right_root.addOrReplaceChild("vest_antler_r_root", CubeListBuilder.create()
            .texOffs(105, 28).addBox(0F, 0F, 0F, 2F, 5F, 2F),
            PartPose.offset(-1.1F, -5.0F, -1.1F));
        antler_right_trunk.addOrReplaceChild("vest_antler_r_trunk", CubeListBuilder.create()
            .texOffs(124, 38).addBox(0F, 0F, 0F, 1F, 5F, 1F),
            PartPose.offset(-0.9F, -5.0F, -0.9F));
        antler_right_branch_a.addOrReplaceChild("vest_antler_r_ba", CubeListBuilder.create()
            .texOffs(58, 52).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(-0.7F, -2.8F, -0.7F));
        antler_right_branch_b.addOrReplaceChild("vest_antler_r_bb", CubeListBuilder.create()
            .texOffs(63, 52).addBox(0F, 0F, 0F, 1F, 3F, 1F),
            PartPose.offset(-0.7F, -3.0F, -0.7F));
        antler_right_tip.addOrReplaceChild("vest_antler_r_tip", CubeListBuilder.create()
            .texOffs(73, 52).addBox(0F, 0F, 0F, 1F, 2F, 1F),
            PartPose.offset(-0.5F, -2.4F, -0.5F));
        body.addOrReplaceChild("vest_inner", CubeListBuilder.create()
            .texOffs(37, 0).addBox(0F, 0F, 0F, 8F, 10F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.0F, 0.6F, -2.5F));
        body.addOrReplaceChild("vest_shell", CubeListBuilder.create()
            .texOffs(64, 0).addBox(0F, 0F, 0F, 8F, 10F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.4F, 0.9F, -2.9F));
        body.addOrReplaceChild("vest_leaf_top", CubeListBuilder.create()
            .texOffs(0, 18).addBox(0F, 0F, 0F, 9F, 3F, 6F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.5F, 1.1F, -3.05F));
        body.addOrReplaceChild("vest_leaf_mid", CubeListBuilder.create()
            .texOffs(31, 18).addBox(0F, 0F, 0F, 8F, 3F, 6F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.4F, 4.4F, -3.0F));
        body.addOrReplaceChild("vest_leaf_low", CubeListBuilder.create()
            .texOffs(51, 28).addBox(0F, 0F, 0F, 8F, 3F, 5F, new CubeDeformation(0.15f)),
            PartPose.offset(-4.3F, 7.5F, -2.95F));
        body.addOrReplaceChild("vest_cavity", CubeListBuilder.create()
            .texOffs(108, 38).addBox(0F, 0F, 0F, 4F, 5F, 1F),
            PartPose.offset(-2.3F, 3.0F, -3.3F));
        body.addOrReplaceChild("vest_core", CubeListBuilder.create()
            .texOffs(39, 52).addBox(0F, 0F, 0F, 3F, 3F, 1F),
            PartPose.offset(-1.6F, 3.7F, -3.45F));
        body.addOrReplaceChild("vest_back", CubeListBuilder.create()
            .texOffs(60, 18).addBox(0F, 0F, 0F, 7F, 8F, 1F, new CubeDeformation(0.1f)),
            PartPose.offset(-3.8F, 1.4F, 2.6F));
        body.addOrReplaceChild("vest_back_seam", CubeListBuilder.create()
            .texOffs(0, 45).addBox(0F, 0F, 0F, 1F, 5F, 1F),
            PartPose.offset(-0.5F, 2.2F, 3.75F));
        body.addOrReplaceChild("vest_belt", CubeListBuilder.create()
            .texOffs(0, 38).addBox(0F, 0F, 0F, 8F, 1F, 5F, new CubeDeformation(0.1f)),
            PartPose.offset(-4.4F, 10.6F, -2.85F));
        shoulder_left.addOrReplaceChild("vest_sh_l", CubeListBuilder.create()
            .texOffs(82, 38).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(2.9F, -2.8F, -2.45F));
        shoulder_left.addOrReplaceChild("vest_sh_l_lo", CubeListBuilder.create()
            .texOffs(111, 45).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(3.0F, 0.1F, -2.25F));
        shoulder_right.addOrReplaceChild("vest_sh_r", CubeListBuilder.create()
            .texOffs(95, 38).addBox(0F, 0F, 0F, 2F, 2F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(-5.7F, -2.8F, -2.45F));
        shoulder_right.addOrReplaceChild("vest_sh_r_lo", CubeListBuilder.create()
            .texOffs(0, 52).addBox(0F, 0F, 0F, 2F, 1F, 4F, new CubeDeformation(0.1f)),
            PartPose.offset(-5.6F, 0.1F, -2.25F));
        right_arm.addOrReplaceChild("vest_fore_r", CubeListBuilder.create()
            .texOffs(77, 18).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.4F, 3.8F, -2.35F));
        right_arm.addOrReplaceChild("vest_wrap_r", CubeListBuilder.create()
            .texOffs(43, 45).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.5F, 9.2F, -2.45F));
        right_arm.addOrReplaceChild("vest_leaf_r", CubeListBuilder.create()
            .texOffs(60, 45).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-3.3F, 10.6F, -2.3F));
        left_arm.addOrReplaceChild("vest_fore_l", CubeListBuilder.create()
            .texOffs(94, 18).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.2F, 3.8F, -2.35F));
        left_arm.addOrReplaceChild("vest_wrap_l", CubeListBuilder.create()
            .texOffs(77, 45).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.3F, 9.2F, -2.45F));
        left_arm.addOrReplaceChild("vest_leaf_l", CubeListBuilder.create()
            .texOffs(94, 45).addBox(0F, 0F, 0F, 4F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-1.1F, 10.6F, -2.3F));
        right_leg.addOrReplaceChild("vest_thigh_r", CubeListBuilder.create()
            .texOffs(111, 18).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.4F, -2.3F));
        right_leg.addOrReplaceChild("vest_knee_r", CubeListBuilder.create()
            .texOffs(5, 45).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        right_leg.addOrReplaceChild("vest_greave_r", CubeListBuilder.create()
            .texOffs(0, 28).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.2F, -2.3F));
        right_leg.addOrReplaceChild("vest_boot_r", CubeListBuilder.create()
            .texOffs(27, 38).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.1F, -2.75F));
        left_leg.addOrReplaceChild("vest_thigh_l", CubeListBuilder.create()
            .texOffs(17, 28).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, -0.4F, -2.3F));
        left_leg.addOrReplaceChild("vest_knee_l", CubeListBuilder.create()
            .texOffs(24, 45).addBox(0F, 0F, 0F, 5F, 1F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 4.5F, -2.4F));
        left_leg.addOrReplaceChild("vest_greave_l", CubeListBuilder.create()
            .texOffs(34, 28).addBox(0F, 0F, 0F, 4F, 5F, 4F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.4F, 6.2F, -2.3F));
        left_leg.addOrReplaceChild("vest_boot_l", CubeListBuilder.create()
            .texOffs(48, 38).addBox(0F, 0F, 0F, 5F, 1F, 5F, new CubeDeformation(0.05f)),
            PartPose.offset(-2.5F, 11.1F, -2.75F));
        return LayerDefinition.create(mesh, 128, 128);
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks,
                          float netHeadYaw, float headPitch) {
    }
    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay,
                               float red, float green, float blue, float alpha) {
        root.render(poseStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}
