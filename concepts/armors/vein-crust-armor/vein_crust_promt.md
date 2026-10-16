Follow every applicable instruction from the `skills/` directory.

Read and follow the project lore from `lore.md`.

Save the complete concept, dimensions, palette, UV decisions, model hierarchy, implementation notes, and TODO items inside the `concepts/` directory.

Do not only describe or plan the armor. Create the complete production-ready 3D models, multilayer pixel-art textures, UV mapping, item resources, renderer integration, and Fabric 1.20.1 registration.

# OBJECTIVE

Create a complete original Basalt Armor set themed around Minecraft’s Nether.

Required items:

- `basalt_helmet`
- `basalt_chestplate`
- `basalt_leggings`
- `basalt_boots`

The armor must look forged from:

- Columnar basalt.
- Blackstone.
- Dark volcanic stone.
- Small quantities of trapped magma.
- Blackened metal reinforcement.

It must not look like recolored vanilla Netherite armor.

# DESIGN IDENTITY

The armor is:

- Heavy.
- Dense.
- Extremely durable-looking.
- Ancient.
- Heat-resistant.
- Built from vertically fractured volcanic stone.
- Rough but deliberately constructed.
- Suitable for survival in the Nether.

Primary silhouette:

- Broad torso.
- Thick boots.
- Compact layered shoulders.
- Reinforced helmet.
- Vertical basalt ribs.
- Rectangular segmented construction.
- No horns, wings, spikes, or demonic face.

# HELMET

Create a closed basalt helmet with:

- Thick columnar basalt crown.
- Several vertical stone ribs.
- Low reinforced forehead plate.
- Narrow dark-red visor opening.
- Blackstone frame around the visor.
- Rectangular cheek guards.
- Thick rear neck protection.
- Chipped but structurally strong edges.
- Small recessed magma pixels inside the visor.

The visor glow must remain restrained.

Do not expose the player’s face through an empty opening. Add a dark inner backing layer.

# CHESTPLATE

Create a heavy chestplate built from interlocking vertical basalt columns.

Required structure:

- Central vertical sternum column.
- Two or three smaller columns on each side.
- Blackstone borders between major sections.
- Compact layered shoulder armor.
- Thick upper-back protection.
- Dark abdominal reinforcement.
- Small recessed magma core in the center of the sternum.
- Sparse thin magma seams around plate joints.
- Broad but wearable silhouette.

The central magma core must not resemble a glowing gemstone. It should look like heat trapped inside fractured volcanic rock.

# GAUNTLETS

Create:

- Segmented basalt forearm plates.
- Blackstone wrist reinforcement.
- Thick knuckle guards.
- Dark inner glove layer.
- Small ember cracks near joints.
- Functional Minecraft-compatible hands.

Do not make the hands excessively large.

The gauntlets must still align with held items.

# LEGGINGS

Create:

- Blackstone waist belt.
- Heavy basalt buckle.
- Layered front, side, and rear hip plates.
- Separate left and right thigh protection.
- Dark flexible inner leg layer.
- Reinforced basalt knee plates.
- Sparse magma cracks near major joints.

Do not connect both legs with a rigid armor skirt.

# BOOTS

Create:

- Thick basalt greaves.
- Blackstone ankle frames.
- Broad volcanic soles.
- Layered toe guards.
- Vertical basalt surface ridges.
- Recessed ember seams.
- Dark inner cavities.

The boots must feel heavy without making the character look unable to walk.

# MULTILAYER MODEL

Required geometry layers:

1. Player body or inner mannequin reference.
2. Dark heat-resistant inner lining.
3. Main basalt plates.
4. Vertical basalt ribs.
5. Blackstone reinforcement.
6. Recessed magma details.
7. Raised chipped edges.
8. Optional emissive overlay.

Recommended spacing:

- Body to inner lining: 0.15–0.25 units.
- Inner lining to main plates: 0.25–0.55 units.
- Main plates to raised ribs: 0.1–0.3 units.
- Magma detail offset: 0.02–0.08 units only if separate geometry is necessary.

Prefer texture-based cracks where geometry would create z-fighting.

# MODEL HIERARCHY

Use the existing project conventions. Otherwise use:

- `armor_root`
  - `head`
    - `helmet_core`
    - `helmet_ribs`
    - `visor`
    - `neck_guard`
  - `body`
    - `chest_core`
    - `chest_columns`
    - `magma_core`
    - `back_plate`
    - `shoulder_left`
    - `shoulder_right`
  - `right_arm`
    - `right_forearm_armor`
    - `right_gauntlet`
  - `left_arm`
    - `left_forearm_armor`
    - `left_gauntlet`
  - `right_leg`
    - `right_thigh_armor`
    - `right_knee`
    - `right_greave`
    - `right_boot`
  - `left_leg`
    - `left_thigh_armor`
    - `left_knee`
    - `left_greave`
    - `left_boot`

Use correct player-body pivots.

# TEXTURE

Preferred texture resolution:

- 128×128 for a custom GeckoLib armor model.
- 64×64 per armor layer only if the existing renderer requires it.

Palette:

- Basalt charcoal.
- Cool ash gray.
- Dark volcanic purple-gray.
- Blackstone black.
- Dark iron.
- Deep ember red.
- Restrained magma orange.

Material treatment:

Basalt:

- Vertical striations.
- Uneven cool-gray bands.
- Chipped edges.
- Low reflectivity.
- Irregular but controlled cracks.

Blackstone:

- Darker than basalt.
- Rough granular pixel clusters.
- Sparse gray highlights.
- Almost no reflection.

Magma:

- Dark red outer edge.
- Orange inner line.
- Tiny yellow center only at the hottest point.
- Restricted to seams and internal cavities.

# EMISSIVE MAP

If emissive rendering is already supported, create:

- `basalt_armor_emissive.png`

Only these regions may emit:

- Visor interior.
- Central magma core.
- Selected deep cracks.
- Small boot and joint seams.

All other pixels must be black or transparent according to the project’s emissive-map convention.

Do not make entire plates glow.

# PIXEL-ART RULES

Use:

- Nearest-neighbor filtering.
- Hard pixel edges.
- Limited palette.
- Hand-painted pixel clusters.
- Consistent light direction.
- Consistent texel density.

Do not use:

- Blur.
- Antialiasing.
- Smooth gradients.
- Photographic stone.
- Random procedural noise.
- Excessive dithering.
- Semi-transparent edges.

If the project uses `gen_textures.py` and an ASCII palette pipeline, follow that pipeline instead of introducing an unrelated generator.

# UV MAPPING

Requirements:

- Manually organize the atlas.
- Keep equal texel density across all pieces.
- Give the vertical basalt ribs enough vertical texture space.
- Use unique UV regions for visor, core, chest columns, knees, and boots.
- Avoid stretching.
- Avoid accidental mirroring of chipped details.
- Maintain padding between islands.
- Ensure the base and emissive UV layouts match exactly.
- Map every visible face intentionally.

# FABRIC 1.20.1 INTEGRATION

Inspect the project before implementation.

Use the existing:

- Armor registration system.
- Armor material architecture.
- Custom renderer.
- GeckoLib armor system, if present.
- Creative tab system.
- Data-generation system.

Create all required:

- Armor item registrations.
- Armor material.
- Model or geometry files.
- Renderer.
- Base texture.
- Emissive texture if supported.
- Item-model JSON files.
- Language entries.
- Recipes if consistent with project progression.
- Durability and protection values.
- Repair ingredient logic if required.

Do not add dependencies without permission.

Do not automatically add fire resistance unless the lore or existing gameplay plan requires it. Keep gameplay behavior separate from rendering.

# RENDERING VALIDATION

Test:

- Normal player model.
- Slim player model if supported.
- First-person arms.
- Third-person front and back.
- Walking.
- Running.
- Crouching.
- Swimming.
- Riding.
- Sleeping.
- Armor stands.
- Held items.
- Bright Overworld lighting.
- Dark Nether lighting.

Confirm that:

- Helmet follows head rotation.
- Shoulders do not intersect the helmet.
- Leg plates move independently.
- Boots align with feet.
- Magma glow remains controlled.
- There is no z-fighting.
- No body parts remain visibly uncovered accidentally.

Build and run the Fabric 1.20.1 development client. Fix every compilation, model, texture, renderer, and resource-loading error. Report every created and modified file.
