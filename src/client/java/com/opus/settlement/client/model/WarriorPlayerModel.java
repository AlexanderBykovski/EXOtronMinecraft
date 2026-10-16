package com.opus.settlement.client.model;

import com.opus.settlement.SettlementLine;
import com.opus.settlement.entity.JapaneseWarriorEntity;
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
 * Regular-player-style models for the Black Ninja and the Red Shogun.
 *
 * Concept: concepts/mobs/black-ninja + concepts/mobs/samurai (prompt AND art),
 * readjusted onto the VANILLA PLAYER RIG (like a normal player: same boxes,
 * same pivot math, vanilla walk/attack animation from HumanoidModel) instead of
 * the old GeckoLib rigs. All clothing/armor/equipment is layered geometry on
 * top of the player body, texture at 128x128, zone UVs (x>=64) packed by
 * scripts/gen_mob_rework/player_skins.py — texOffs below MUST match that
 * script's printed constants.
 *
 * Vanilla second-layer cubes (hat/jacket/sleeves/pants/ear/cloak) are emptied
 * so the custom layers are the only outer geometry (no z-fighting).
 */
public final class WarriorPlayerModel<T extends JapaneseWarriorEntity> extends PlayerModel<T> {
    public static final ModelLayerLocation BLACK_NINJA_LAYER = new ModelLayerLocation(SettlementLine.id("black_ninja"), "main");
    public static final ModelLayerLocation SAMURAI_LAYER = new ModelLayerLocation(SettlementLine.id("samurai"), "main");

    public WarriorPlayerModel(ModelPart root) { super(root, false); }

    private static CubeListBuilder empty() { return CubeListBuilder.create(); }

    // ------------------------------------------------------------------ rig
    private static MeshDefinition baseMesh() {
        MeshDefinition mesh = PlayerModel.createMesh(CubeDeformation.NONE, false);
        var root = mesh.getRoot();
        root.addOrReplaceChild("hat", empty(), PartPose.ZERO);
        root.addOrReplaceChild("jacket", empty(), PartPose.ZERO);
        root.addOrReplaceChild("right_sleeve", empty(), PartPose.ZERO);
        root.addOrReplaceChild("left_sleeve", empty(), PartPose.ZERO);
        root.addOrReplaceChild("right_pants", empty(), PartPose.ZERO);
        root.addOrReplaceChild("left_pants", empty(), PartPose.ZERO);
        root.addOrReplaceChild("ear", empty(), PartPose.ZERO);
        root.addOrReplaceChild("cloak", empty(), PartPose.ZERO);
        return mesh;
    }

    /** texOffs constants printed by scripts/gen_mob_rework/player_skins.py. */
    private static final int NINJA_HOOD_MAIN_U = 64, NINJA_HOOD_MAIN_V = 0;
    private static final int NINJA_HOOD_SIDE_U = 102, NINJA_HOOD_SIDE_V = 0;
    private static final int NINJA_HOOD_BACK_U = 64, NINJA_HOOD_BACK_V = 14;
    private static final int NINJA_MASK_U = 86, NINJA_MASK_V = 14;
    private static final int NINJA_NECK_U = 83, NINJA_NECK_V = 14;
    private static final int NINJA_JACKET_U = 89, NINJA_JACKET_V = 21;
    private static final int NINJA_SHOULDER_U = 93, NINJA_SHOULDER_V = 22;
    private static final int NINJA_BELT_U = 64, NINJA_BELT_V = 38;
    private static final int NINJA_HIP_FRONT_U = 91, NINJA_HIP_FRONT_V = 38;
    private static final int NINJA_HIP_BACK_U = 110, NINJA_HIP_BACK_V = 38;
    private static final int NINJA_ROPE_U = 64, NINJA_ROPE_V = 46;
    private static final int NINJA_POUCH_U = 75, NINJA_POUCH_V = 46;
    private static final int NINJA_KUNAI_U = 84, NINJA_KUNAI_V = 46;
    private static final int NINJA_SAYA_U = 90, NINJA_SAYA_V = 46;
    private static final int NINJA_TSUKA_U = 99, NINJA_TSUKA_V = 46;
    private static final int NINJA_SLEEVE_U = 108, NINJA_SLEEVE_V = 46;
    private static final int NINJA_WRAP_U = 64, NINJA_WRAP_V = 60;
    private static final int NINJA_BRACER_U = 83, NINJA_BRACER_V = 60;
    private static final int NINJA_TROUSER_U = 103, NINJA_TROUSER_V = 60;
    private static final int NINJA_CALF_U = 64, NINJA_CALF_V = 70;

    /** Black Ninja geometry — layered shinobi wear per prompt: hood + eye slit +
     *  separate lower mask + neck wrap, uwagi jacket (V closure), padded shoulder
     *  panels, belt + sash, hip cloth, forearm wraps + matte bracers, loose
     *  trousers with wrapped calves, belt kit (pouch, rope coil, 2 kunai) and the
     *  short sword sheathed diagonally at the left hip. */
    public static LayerDefinition createNinjaLayer() {
        MeshDefinition mesh = baseMesh();
        var root = mesh.getRoot();
        var head = root.getChild("head");
        var body = root.getChild("body");
        var rightArm = root.getChild("right_arm");
        var leftArm = root.getChild("left_arm");
        var rightLeg = root.getChild("right_leg");
        var leftLeg = root.getChild("left_leg");

        // HEAD: hood shell (above the eye line), side flaps, back flap,
        // lower-face mask and thin neck wrap under the chin.
        head.addOrReplaceChild("hood_main", CubeListBuilder.create()
            .texOffs(NINJA_HOOD_MAIN_U, NINJA_HOOD_MAIN_V)
            .addBox(-4.6F, -8.7F, -4.6F, 9.2F, 4.2F, 9.2F), PartPose.ZERO);
        head.addOrReplaceChild("hood_side_l", CubeListBuilder.create()
            .texOffs(NINJA_HOOD_SIDE_U, NINJA_HOOD_SIDE_V)
            .addBox(-5.35F, -4.6F, -4.3F, 0.95F, 5.1F, 8.6F), PartPose.ZERO);
        head.addOrReplaceChild("hood_side_r", CubeListBuilder.create()
            .texOffs(NINJA_HOOD_SIDE_U, NINJA_HOOD_SIDE_V)
            .addBox(4.4F, -4.6F, -4.3F, 0.95F, 5.1F, 8.6F), PartPose.ZERO);
        head.addOrReplaceChild("hood_back", CubeListBuilder.create()
            .texOffs(NINJA_HOOD_BACK_U, NINJA_HOOD_BACK_V)
            .addBox(-4.5F, -4.6F, 4.15F, 9.0F, 5.1F, 1.1F), PartPose.ZERO);

        head.addOrReplaceChild("face_mask", CubeListBuilder.create()
            .texOffs(NINJA_MASK_U, NINJA_MASK_V)
            .addBox(-3.95F, -1.5F, -4.72F, 7.9F, 3.7F, 0.9F), PartPose.ZERO);
        head.addOrReplaceChild("neck_wrap", CubeListBuilder.create()
            .texOffs(NINJA_NECK_U, NINJA_NECK_V)
            .addBox(-3.4F, -0.85F, -2.5F, 6.8F, 1.6F, 5.0F), PartPose.ZERO);

        // BODY: fitted uwagi, quilted shoulder panels, obi belt, split hip cloth.
        body.addOrReplaceChild("jacket", CubeListBuilder.create()
            .texOffs(NINJA_JACKET_U, NINJA_JACKET_V)
            .addBox(-4.3F, -0.15F, -2.3F, 8.6F, 12.3F, 4.6F), PartPose.ZERO);
        body.addOrReplaceChild("shoulder_pad_r", CubeListBuilder.create()
            .texOffs(NINJA_SHOULDER_U, NINJA_SHOULDER_V)
            .addBox(0.45F, -1.35F, -2.62F, 3.5F, 2.7F, 1.0F), PartPose.ZERO);
        body.addOrReplaceChild("shoulder_pad_l", CubeListBuilder.create()
            .texOffs(NINJA_SHOULDER_U, NINJA_SHOULDER_V)
            .addBox(-3.95F, -1.35F, -2.62F, 3.5F, 2.7F, 1.0F), PartPose.ZERO);
        body.addOrReplaceChild("belt", CubeListBuilder.create()
            .texOffs(NINJA_BELT_U, NINJA_BELT_V)
            .addBox(-4.0F, 8.55F, -2.42F, 8.0F, 2.5F, 4.9F), PartPose.ZERO);
        body.addOrReplaceChild("hip_cloth_front", CubeListBuilder.create()
            .texOffs(NINJA_HIP_FRONT_U, NINJA_HIP_FRONT_V)
            .addBox(-3.9F, 11.0F, -2.62F, 7.8F, 4.6F, 0.85F), PartPose.ZERO);
        body.addOrReplaceChild("hip_cloth_back", CubeListBuilder.create()
            .texOffs(NINJA_HIP_BACK_U, NINJA_HIP_BACK_V)
            .addBox(-3.9F, 11.0F, 1.77F, 7.8F, 4.6F, 0.85F), PartPose.ZERO);

        // Belt kit: rope coil right-back, rear pouch, two sheathed kunai.
        body.addOrReplaceChild("rope", CubeListBuilder.create()
            .texOffs(NINJA_ROPE_U, NINJA_ROPE_V)
            .addBox(1.05F, 8.3F, 1.85F, 2.9F, 1.8F, 2.0F), PartPose.ZERO);
        body.addOrReplaceChild("pouch", CubeListBuilder.create()
            .texOffs(NINJA_POUCH_U, NINJA_POUCH_V)
            .addBox(-3.45F, 7.5F, 1.85F, 2.2F, 3.0F, 1.6F), PartPose.ZERO);
        body.addOrReplaceChild("kunai_l", CubeListBuilder.create()
            .texOffs(NINJA_KUNAI_U, NINJA_KUNAI_V)
            .addBox(-3.05F, 9.2F, 2.62F, 1.1F, 2.7F, 0.95F), PartPose.ZERO);
        body.addOrReplaceChild("kunai_r", CubeListBuilder.create()
            .texOffs(NINJA_KUNAI_U, NINJA_KUNAI_V)
            .addBox(1.95F, 9.2F, 2.62F, 1.1F, 2.7F, 0.95F), PartPose.ZERO);
        // Short sword sheathed at the left hip (saya behind, tsuka up-forward).
        body.addOrReplaceChild("short_sword", CubeListBuilder.create()
            .texOffs(NINJA_SAYA_U, NINJA_SAYA_V)
            .addBox(-1.0F, 0.15F, -1.0F, 2.0F, 11.2F, 2.0F)
            .texOffs(NINJA_TSUKA_U, NINJA_TSUKA_V)
            .addBox(-1.0F, -4.4F, -1.0F, 2.0F, 4.4F, 2.0F),
            PartPose.offsetAndRotation(2.6F, 9.2F, 3.0F, 0.10F, 0.0F, -0.42F));

        // ARMS: fitted sleeve, layered forearm wrap, thin matte bracer.
        rightArm.addOrReplaceChild("sleeve_r", CubeListBuilder.create()
            .texOffs(NINJA_SLEEVE_U, NINJA_SLEEVE_V)
            .addBox(-3.66F, -2.1F, -2.56F, 4.2F, 7.9F, 4.2F), PartPose.ZERO);
        rightArm.addOrReplaceChild("wrap_r", CubeListBuilder.create()
            .texOffs(NINJA_WRAP_U, NINJA_WRAP_V)
            .addBox(-3.72F, 4.3F, -2.62F, 4.4F, 5.3F, 4.4F), PartPose.ZERO);
        rightArm.addOrReplaceChild("bracer_r", CubeListBuilder.create()
            .texOffs(NINJA_BRACER_U, NINJA_BRACER_V)
            .addBox(-3.86F, 6.9F, -2.76F, 4.6F, 3.0F, 4.6F), PartPose.ZERO);
        leftArm.addOrReplaceChild("sleeve_l", CubeListBuilder.create()
            .texOffs(NINJA_SLEEVE_U, NINJA_SLEEVE_V)
            .addBox(-0.54F, -2.1F, -2.56F, 4.2F, 7.9F, 4.2F), PartPose.ZERO);
        leftArm.addOrReplaceChild("wrap_l", CubeListBuilder.create()
            .texOffs(NINJA_WRAP_U, NINJA_WRAP_V)
            .addBox(-0.68F, 4.3F, -2.62F, 4.4F, 5.3F, 4.4F), PartPose.ZERO);
        leftArm.addOrReplaceChild("bracer_l", CubeListBuilder.create()
            .texOffs(NINJA_BRACER_U, NINJA_BRACER_V)
            .addBox(-0.74F, 6.9F, -2.76F, 4.6F, 3.0F, 4.6F), PartPose.ZERO);

        // LEGS: loose trousers above, wrapped calves below.
        for (var leg : java.util.List.of(rightLeg, leftLeg)) {
            leg.addOrReplaceChild("trouser", CubeListBuilder.create()
                .texOffs(NINJA_TROUSER_U, NINJA_TROUSER_V)
                .addBox(-2.32F, -0.12F, -2.32F, 4.64F, 4.7F, 4.64F), PartPose.ZERO);
            leg.addOrReplaceChild("calf_wrap", CubeListBuilder.create()
                .texOffs(NINJA_CALF_U, NINJA_CALF_V)
                .addBox(-2.38F, 4.6F, -2.38F, 4.76F, 4.7F, 4.76F), PartPose.ZERO);
        }

        return LayerDefinition.create(mesh, 128, 128);
    }

    /** texOffs constants printed by scripts/gen_mob_rework/player_skins.py. */
    private static final int SAM_MENPO_U = 64, SAM_MENPO_V = 0;
    private static final int SAM_BOWL_U = 82, SAM_BOWL_V = 0;
    private static final int SAM_BRIM_U = 64, SAM_BRIM_V = 14;
    private static final int SAM_SHIKORO_BACK_U = 84, SAM_SHIKORO_BACK_V = 14;
    private static final int SAM_SHIKORO_SIDE_U = 107, SAM_SHIKORO_SIDE_V = 14;
    private static final int SAM_HORN_U = 64, SAM_HORN_V = 26;
    private static final int SAM_DISC_U = 70, SAM_DISC_V = 26;
    private static final int SAM_CLOTH_U = 64, SAM_CLOTH_V = 38;
    private static final int SAM_CHEST_U = 91, SAM_CHEST_V = 38;
    private static final int SAM_SODE_U = 64, SAM_SODE_V = 55;
    private static final int SAM_SLEEVE_U = 77, SAM_SLEEVE_V = 26;
    private static final int SAM_KOTE_U = 95, SAM_KOTE_V = 26;
    private static final int SAM_OBI_U = 86, SAM_OBI_V = 55;
    private static final int SAM_KNOT_U = 115, SAM_KNOT_V = 55;
    private static final int SAM_KUSA_FRONT_U = 64, SAM_KUSA_FRONT_V = 66;
    private static final int SAM_KUSA_SIDE_U = 85, SAM_KUSA_SIDE_V = 66;
    private static final int SAM_HAIDATE_U = 99, SAM_HAIDATE_V = 66;
    private static final int SAM_SUNEATE_U = 64, SAM_SUNEATE_V = 78;
    private static final int SAM_SANDAL_U = 86, SAM_SANDAL_V = 78;
    private static final int SAM_SAYA_U = 110, SAM_SAYA_V = 78;
    private static final int SAM_TSUKA_U = 119, SAM_TSUKA_V = 78;
    private static final int SAM_WAKI_SAYA_U = 64, SAM_WAKI_SAYA_V = 94;
    private static final int SAM_WAKI_TSUKA_U = 73, SAM_WAKI_TSUKA_V = 94;

    /** Red Shogun geometry — red lacquered kabuto with black iron plate edges,
     *  stepped gold crescent + clan disc, layered shikoro, red menpo, indigo
     *  visibility layers, crimson lamellar do with gold rivets, broad sode,
     *  kote, obi + knot, four kusazuri panels, haidate, suneate, straw sandals,
     *  katana + wakizashi daisho at the left waist. */
    public static LayerDefinition createSamuraiLayer() {
        MeshDefinition mesh = baseMesh();
        var root = mesh.getRoot();
        var head = root.getChild("head");
        var body = root.getChild("body");
        var rightArm = root.getChild("right_arm");
        var leftArm = root.getChild("left_arm");
        var rightLeg = root.getChild("right_leg");
        var leftLeg = root.getChild("left_leg");

        // HEAD: kabuto bowl + brim + side neck guards + crescent (2 horns + disc).
        head.addOrReplaceChild("kabuto_bowl", CubeListBuilder.create()
            .texOffs(SAM_BOWL_U, SAM_BOWL_V)
            .addBox(-4.5F, -8.7F, -4.5F, 9.0F, 4.6F, 9.0F), PartPose.ZERO);
        head.addOrReplaceChild("kabuto_brim", CubeListBuilder.create()
            .texOffs(SAM_BRIM_U, SAM_BRIM_V)
            .addBox(-4.0F, -5.6F, -4.85F, 8.0F, 1.7F, 1.2F), PartPose.ZERO);
        head.addOrReplaceChild("shikoro_back", CubeListBuilder.create()
            .texOffs(SAM_SHIKORO_BACK_U, SAM_SHIKORO_BACK_V)
            .addBox(-4.6F, -4.3F, 2.85F, 9.2F, 4.7F, 1.75F), PartPose.ZERO);
        head.addOrReplaceChild("shikoro_side_l", CubeListBuilder.create()
            .texOffs(SAM_SHIKORO_SIDE_U, SAM_SHIKORO_SIDE_V)
            .addBox(-5.12F, -4.3F, -1.5F, 1.0F, 4.7F, 6.8F), PartPose.ZERO);
        head.addOrReplaceChild("shikoro_side_r", CubeListBuilder.create()
            .texOffs(SAM_SHIKORO_SIDE_U, SAM_SHIKORO_SIDE_V)
            .addBox(4.12F, -4.3F, -1.5F, 1.0F, 4.7F, 6.8F), PartPose.ZERO);
        head.addOrReplaceChild("crest_horn_l", CubeListBuilder.create()
            .texOffs(SAM_HORN_U, SAM_HORN_V)
            .addBox(-0.8F, 0.0F, -0.45F, 1.6F, 3.0F, 0.9F),
            PartPose.offsetAndRotation(-3.1F, -9.0F, -4.35F, 0.0F, 0.0F, 0.42F));
        head.addOrReplaceChild("crest_horn_r", CubeListBuilder.create()
            .texOffs(SAM_HORN_U, SAM_HORN_V)
            .addBox(-0.8F, 0.0F, -0.45F, 1.6F, 3.0F, 0.9F),
            PartPose.offsetAndRotation(3.1F, -9.0F, -4.35F, 0.0F, 0.0F, -0.42F));
        head.addOrReplaceChild("crest_disc", CubeListBuilder.create()
            .texOffs(SAM_DISC_U, SAM_DISC_V)
            .addBox(-1.05F, -1.05F, -0.33F, 2.1F, 2.1F, 0.66F),
            PartPose.offset(0.0F, -6.55F, -4.72F));
        // Menpo covers cheeks/nose/jaw; eyes and brow band stay visible.
        head.addOrReplaceChild("menpo", CubeListBuilder.create()
            .texOffs(SAM_MENPO_U, SAM_MENPO_V)
            .addBox(-3.75F, -4.35F, -4.55F, 7.5F, 3.95F, 0.85F), PartPose.ZERO);

        // BODY: indigo under-cloth, lamellar do, obi + knot, 4 kusazuri panels,
        // daisho (katana above/outer, wakizashi below/inner) at the left waist.
        body.addOrReplaceChild("inner_cloth", CubeListBuilder.create()
            .texOffs(SAM_CLOTH_U, SAM_CLOTH_V)
            .addBox(-4.25F, -0.2F, -2.25F, 8.5F, 12.3F, 4.5F), PartPose.ZERO);
        body.addOrReplaceChild("chest_armor", CubeListBuilder.create()
            .texOffs(SAM_CHEST_U, SAM_CHEST_V)
            .addBox(-4.85F, -0.85F, -2.8F, 9.7F, 9.5F, 5.6F), PartPose.ZERO);
        body.addOrReplaceChild("obi", CubeListBuilder.create()
            .texOffs(SAM_OBI_U, SAM_OBI_V)
            .addBox(-4.3F, 8.7F, -2.6F, 8.6F, 2.5F, 5.3F), PartPose.ZERO);
        body.addOrReplaceChild("obi_knot", CubeListBuilder.create()
            .texOffs(SAM_KNOT_U, SAM_KNOT_V)
            .addBox(-1.9F, 9.0F, 2.25F, 3.8F, 2.5F, 1.4F), PartPose.ZERO);
        body.addOrReplaceChild("kusazuri_front", CubeListBuilder.create()
            .texOffs(SAM_KUSA_FRONT_U, SAM_KUSA_FRONT_V)
            .addBox(-4.5F, 11.35F, -2.95F, 9.0F, 6.1F, 1.0F), PartPose.ZERO);
        body.addOrReplaceChild("kusazuri_back", CubeListBuilder.create()
            .texOffs(SAM_KUSA_FRONT_U, SAM_KUSA_FRONT_V)
            .addBox(-4.5F, 11.35F, 1.9F, 9.0F, 6.1F, 1.0F), PartPose.ZERO);
        body.addOrReplaceChild("kusazuri_left", CubeListBuilder.create()
            .texOffs(SAM_KUSA_SIDE_U, SAM_KUSA_SIDE_V)
            .addBox(3.92F, 11.35F, -2.4F, 1.1F, 6.1F, 5.35F), PartPose.ZERO);
        body.addOrReplaceChild("kusazuri_right", CubeListBuilder.create()
            .texOffs(SAM_KUSA_SIDE_U, SAM_KUSA_SIDE_V)
            .addBox(-5.02F, 11.35F, -2.4F, 1.1F, 6.1F, 5.35F), PartPose.ZERO);
        body.addOrReplaceChild("katana", CubeListBuilder.create()
            .texOffs(SAM_SAYA_U, SAM_SAYA_V)
            .addBox(-1.0F, 0.15F, -1.0F, 2.0F, 13.8F, 2.0F)
            .texOffs(SAM_TSUKA_U, SAM_TSUKA_V)
            .addBox(-1.0F, -6.2F, -1.0F, 2.0F, 6.1F, 2.0F),
            PartPose.offsetAndRotation(3.25F, 7.6F, 3.7F, 0.08F, 0.0F, -0.40F));
        body.addOrReplaceChild("wakizashi", CubeListBuilder.create()
            .texOffs(SAM_WAKI_SAYA_U, SAM_WAKI_SAYA_V)
            .addBox(-1.0F, 0.15F, -1.0F, 2.0F, 11.3F, 2.0F)
            .texOffs(SAM_WAKI_TSUKA_U, SAM_WAKI_TSUKA_V)
            .addBox(-1.0F, -4.6F, -1.0F, 2.0F, 4.4F, 2.0F),
            PartPose.offsetAndRotation(2.55F, 10.2F, 3.7F, 0.08F, 0.0F, -0.28F));

        // ARMS: indigo sleeves, red/black kote, broad layered sode.
        rightArm.addOrReplaceChild("sleeve_r", CubeListBuilder.create()
            .texOffs(SAM_SLEEVE_U, SAM_SLEEVE_V)
            .addBox(-3.62F, -2.18F, -2.52F, 4.24F, 7.5F, 4.24F), PartPose.ZERO);
        rightArm.addOrReplaceChild("kote_r", CubeListBuilder.create()
            .texOffs(SAM_KOTE_U, SAM_KOTE_V)
            .addBox(-3.92F, 4.1F, -2.82F, 4.84F, 5.5F, 4.84F), PartPose.ZERO);
        rightArm.addOrReplaceChild("sode_r", CubeListBuilder.create()
            .texOffs(SAM_SODE_U, SAM_SODE_V)
            .addBox(-4.95F, -3.1F, -3.0F, 5.2F, 5.8F, 5.0F), PartPose.ZERO);
        leftArm.addOrReplaceChild("sleeve_l", CubeListBuilder.create()
            .texOffs(SAM_SLEEVE_U, SAM_SLEEVE_V)
            .addBox(-0.62F, -2.18F, -2.52F, 4.24F, 7.5F, 4.24F), PartPose.ZERO);
        leftArm.addOrReplaceChild("kote_l", CubeListBuilder.create()
            .texOffs(SAM_KOTE_U, SAM_KOTE_V)
            .addBox(-0.92F, 4.1F, -2.82F, 4.84F, 5.5F, 4.84F), PartPose.ZERO);
        leftArm.addOrReplaceChild("sode_l", CubeListBuilder.create()
            .texOffs(SAM_SODE_U, SAM_SODE_V)
            .addBox(0.25F, -3.1F, -3.0F, 5.2F, 5.8F, 5.0F), PartPose.ZERO);

        // LEGS: haidate thigh plates, red suneate shin guards, straw sandals.
        for (var leg : java.util.List.of(rightLeg, leftLeg)) {
            leg.addOrReplaceChild("haidate", CubeListBuilder.create()
                .texOffs(SAM_HAIDATE_U, SAM_HAIDATE_V)
                .addBox(-2.55F, -0.12F, -2.55F, 5.1F, 4.7F, 5.1F), PartPose.ZERO);
            leg.addOrReplaceChild("suneate", CubeListBuilder.create()
                .texOffs(SAM_SUNEATE_U, SAM_SUNEATE_V)
                .addBox(-2.55F, 4.5F, -2.55F, 5.1F, 4.7F, 5.1F), PartPose.ZERO);
            leg.addOrReplaceChild("sandal", CubeListBuilder.create()
                .texOffs(SAM_SANDAL_U, SAM_SANDAL_V)
                .addBox(-2.6F, 11.15F, -3.05F, 5.2F, 1.0F, 6.1F), PartPose.ZERO);
        }

        return LayerDefinition.create(mesh, 128, 128);
    }

    // ------------------------------------------------------------------ poses
    @Override
    public void setupAnim(T entity, float limbSwing, float limbAmount, float ageInTicks,
                          float netHeadYaw, float headPitch) {
        rightArmPose = ArmPose.ITEM;
        leftArmPose = ArmPose.EMPTY;
        super.setupAnim(entity, limbSwing, limbAmount, ageInTicks, netHeadYaw, headPitch);

        if (entity.isDeadOrDying()) {
            return; // vanilla lie-down pose
        }

        int action = entity.getActionState();
        float t = entity.getActionTickClient();
        if (action == JapaneseWarriorEntity.ACTION_NONE) {
            if (entity.getTarget() != null) {
                // Combat ready stance: balanced crouch, sword hand relaxed by the waist
                rightArm.xRot = -0.55F + Mth.sin(ageInTicks * 0.06F) * 0.05F;
                leftArm.xRot = -0.30F + Mth.sin(ageInTicks * 0.06F + 1.2F) * 0.04F;
                body.xRot = -0.06F;
            }
            return;
        }

        switch (action) {
            case JapaneseWarriorEntity.ACTION_MELEE -> {
                // quick controlled cut: wind up then sweep through
                float k = Mth.clamp(t / 8.0F, 0.0F, 1.0F);
                rightArm.xRot = Mth.lerp(k, -2.15F, -0.35F);
                rightArm.yRot = -0.55F * (1.0F - k);
                body.yRot = -0.25F * (1.0F - k);
                leftArm.xRot = -0.25F;
            }
            case JapaneseWarriorEntity.ACTION_GUARD -> {
                rightArm.xRot = -1.5F;
                rightArm.yRot = -0.5F;
                leftArm.xRot = -1.15F;
                leftArm.yRot = 0.4F;
                body.xRot = -0.10F;
            }
            case JapaneseWarriorEntity.ACTION_PARRY -> {
                float k = Mth.clamp(t / 9.0F, 0.0F, 1.0F);
                rightArm.xRot = Mth.lerp(k, -1.6F, -0.6F);
                rightArm.yRot = Mth.lerp(k, -0.7F, -0.15F);
                body.yRot = Mth.lerp(k, -0.35F, 0.15F);
            }
            case JapaneseWarriorEntity.ACTION_DODGE_L -> {
                body.yRot = 0.45F;
                body.zRot = 0.18F;
                rightLeg.xRot = -0.75F;
                leftLeg.xRot = 0.35F;
            }
            case JapaneseWarriorEntity.ACTION_DODGE_R -> {
                body.yRot = -0.45F;
                body.zRot = -0.18F;
                leftLeg.xRot = -0.75F;
                rightLeg.xRot = 0.35F;
            }
            case JapaneseWarriorEntity.ACTION_COMMAND -> {
                // rally: right arm raised high, chin slightly up
                float k = Mth.clamp(t / 8.0F, 0.0F, 1.0F);
                rightArm.xRot = Mth.lerp(k, -0.5F, -2.65F);
                leftArm.xRot = Mth.lerp(k, -0.2F, -0.35F);
                body.xRot = -0.05F;
            }
            case JapaneseWarriorEntity.ACTION_SMOKE_STEP -> {
                // low sprint: forward lean, arms swept back
                float k = Mth.clamp(t / 8.0F, 0.0F, 1.0F);
                body.xRot = 0.30F * k;
                rightArm.xRot = 0.55F * k;
                leftArm.xRot = 0.65F * k;
            }
            case JapaneseWarriorEntity.ACTION_LONG_LUNGE -> {
                // iai dash: crouch load then thrust straight forward
                if (t < 9.0F) {
                    float k = t / 9.0F;
                    body.xRot = -0.14F * k;
                    rightArm.xRot = Mth.lerp(k, -0.45F, -1.45F);
                    rightLeg.xRot = Mth.lerp(k, 0.0F, -0.55F);
                    leftLeg.xRot = Mth.lerp(k, 0.0F, 0.65F);
                } else {
                    float k = Mth.clamp((t - 9.0F) / 8.0F, 0.0F, 1.0F);
                    rightArm.xRot = Mth.lerp(k, -1.5F, -0.7F);
                    rightArm.yRot = Mth.lerp(k, -0.5F, -0.2F);
                    body.xRot = -0.14F * (1.0F - k);
                    rightLeg.xRot = Mth.lerp(k, -0.55F, 0.0F);
                    leftLeg.xRot = Mth.lerp(k, 0.65F, 0.0F);
                }
            }
            case JapaneseWarriorEntity.ACTION_THROW -> {
                // overhead kunai toss (AI-free, QA/technique only)
                float k = Mth.clamp(t / 10.0F, 0.0F, 1.0F);
                rightArm.xRot = Mth.lerp(k, -2.4F, -0.8F);
                leftArm.xRot = -0.35F;
                body.yRot = -0.18F * (1.0F - k);
            }
            default -> { }
        }
    }
}
