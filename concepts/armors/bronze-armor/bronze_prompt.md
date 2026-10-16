Follow all applicable instructions from `skills/` and `lore.md`.

Save the concept, historical references, dimensions, palette, UV plan, and implementation notes inside `concepts/`.

Create the actual Blockbench models, multilayer textures, UV mapping, renderer, and item registrations.

# OBJECTIVE

Create an original complete Bronze Armor set inspired by ancient Roman military equipment.

Required items:

- `roman_bronze_helmet`
- `roman_bronze_chestplate`
- `roman_bronze_leggings`
- `roman_bronze_boots`

The design represents a prestigious Roman officer or elite legionary.

It must remain practical, grounded, and Minecraft-compatible.

Do not copy a specific film costume, museum reconstruction, game asset, or historical artifact exactly.

# HISTORICAL VISUAL LANGUAGE

Use a coherent mixture of:

- Roman bronze helmet construction.
- Officer-style bronze cuirass.
- Layered shoulder straps.
- Dark-red military tunic.
- Leather pteruges.
- Bronze greaves.
- Dark leather sandals.

Avoid combining unrelated periods excessively.

Do not use:

- Greek Corinthian helmet.
- Medieval knight armor.
- Fantasy spikes.
- Wings.
- Glowing effects.
- Oversized gold decoration.
- Modern military details.

# HELMET

Create a Roman-inspired bronze helmet with:

- Rounded segmented bronze bowl.
- Reinforced brow band.
- Short cheek guards.
- Rear neck plate.
- Small rivets.
- Layered edge reinforcement.
- Dark inner lining.
- Restrained dark-red transverse crest.

Crest construction:

- Dense dark-red horsehair-like pixel blocks.
- Mounted across the helmet from left to right.
- Supported by a narrow bronze base.
- Compact enough for normal movement.
- No enormous plume.
- No feathered wings.

Create separate bones:

- `helmet_core`
- `brow_band`
- `cheek_left`
- `cheek_right`
- `neck_guard`
- `crest_base`
- `crest`

# CHESTPLATE

Create a simplified bronze anatomical cuirass.

Required details:

- Broad upper chest.
- Restrained raised chest structure.
- Central sternum line.
- Subtle abdominal segmentation.
- Layered bronze shoulder straps.
- Dark inner leather backing.
- Bronze side fasteners.
- Dark-red tunic visible at neck, shoulders, and lower edge.
- Weathered patina in recessed areas.

Do not create photorealistic human anatomy.

The chest shape must remain blocky and stylized.

# SHOULDER PROTECTION

Create:

- Layered bronze shoulder straps.
- Three to five overlapping rectangular sections.
- Small rivets.
- Correct shoulder pivots.
- Moderate outward extension.
- Dark leather beneath the bronze.

# FOREARM ARMOR

Create:

- Bronze vambraces.
- Dark leather backing.
- Simple raised borders.
- Small rivets.
- Functional hands.
- Restrained asymmetry from wear.

# WAIST AND PTERUGES

Create:

- Wide decorated bronze-and-leather belt.
- Repeating square bronze fittings.
- Central rectangular buckle.
- Two layers of leather pteruges.
- Small bronze plates at the ends.
- Dark-red tunic visible beneath.

Pteruges requirements:

- Separate front, rear, left, and right groups.
- Individual strips may share bones in small clusters.
- Enough separation for leg movement.
- No rigid cylindrical skirt.
- No excessive strip count.

# LEGGINGS

Create:

- Dark-red tunic lower layer.
- Dark leather or cloth inner legs.
- Optional compact upper-leg protection.
- Bronze greaves covering the front of the shins.
- Leather straps around the calves.
- Open or dark-backed rear greave section.

# FOOTWEAR

Create Roman-inspired caligae adapted to Minecraft:

- Dark leather sole.
- Thick practical base.
- Crossed leather straps.
- Small bronze studs or fittings.
- Protected heel.
- Optional small bronze toe edge.
- No modern boot shape.
- No exposed realistic toes if inconsistent with Minecraft style.

# MULTILAYER GEOMETRY

Layers:

1. Inner tunic.
2. Leather backing.
3. Bronze cuirass.
4. Raised chest details.
5. Shoulder straps.
6. Belt.
7. Pteruges.
8. Greaves.
9. Sandal straps.
10. Helmet and crest.

Recommended spacing:

- Body to tunic: 0.15–0.25 units.
- Tunic to leather: 0.1–0.2 units.
- Leather to bronze: 0.2–0.45 units.
- Bronze to raised borders: 0.05–0.2 units.
- Pteruges must begin at the waist and remain clear of the legs.

# MODEL HIERARCHY

Use:

- `armor_root`
  - `head`
    - `helmet_core`
    - `brow_band`
    - `cheek_left`
    - `cheek_right`
    - `neck_guard`
    - `crest`
  - `body`
    - `tunic_upper`
    - `leather_backing`
    - `bronze_cuirass`
    - `shoulder_left`
    - `shoulder_right`
    - `belt`
    - `pteruges_front`
    - `pteruges_back`
    - `pteruges_left`
    - `pteruges_right`
  - `right_arm`
    - `right_vambrace`
  - `left_arm`
    - `left_vambrace`
  - `right_leg`
    - `right_inner_leg`
    - `right_greave`
    - `right_sandal`
  - `left_leg`
    - `left_inner_leg`
    - `left_greave`
    - `left_sandal`

# TEXTURE

Preferred resolution:

- 128×128 for a detailed model.
- 64×64 for a simpler vanilla-scale implementation.

Palette:

- Aged bronze.
- Warm copper-brown.
- Muted golden highlight.
- Deep bronze shadow.
- Green-brown patina.
- Dark-red cloth.
- Dark brown leather.
- Near-black recesses.

Bronze material:

- Warm brown-gold base.
- Narrow pale-gold highlights.
- Dark brown shadows.
- Green patina in seams and recesses.
- Small scratches on raised edges.
- No mirror-like surface.
- No flat bright yellow.

Leather:

- Dark brown.
- Worn warm edges.
- Sparse grain pixels.
- Dark holes around rivets.

Red cloth:

- Deep desaturated red.
- Dark crimson shadows.
- Sparse woven texture.
- No bright scarlet.

# PATINA

Patina must appear naturally:

- Around rivets.
- Under overlapping plates.
- Near lower edges.
- Inside chest recesses.
- Around belt fittings.
- In helmet seams.

Do not cover the complete armor in green.

Most bronze must remain visibly bronze.

# PIXEL-ART RULES

Use:

- Nearest-neighbor.
- Hard pixel edges.
- Limited material-specific palettes.
- Manual shading.
- Consistent texel density.
- One light direction.

Avoid:

- Blur.
- Antialiasing.
- Photographic bronze.
- Random noise.
- Smooth gradients.
- Excessive scratches.
- Modern PBR appearance baked into the texture.

# UV MAPPING

Requirements:

- Unique UV areas for helmet, face guards, cuirass, crest, belt, pteruges, greaves, and sandals.
- Correct orientation of leather strips.
- Consistent texel density.
- No stretched bronze surfaces.
- No accidental mirrored patina.
- Adequate padding.
- Every visible face mapped.

# FABRIC 1.20.1 INTEGRATION

Suggested identifiers:

- `roman_bronze_helmet`
- `roman_bronze_chestplate`
- `roman_bronze_leggings`
- `roman_bronze_boots`

Create:

- Armor registrations.
- Armor material.
- Renderer.
- Geometry.
- Texture.
- Item models.
- Language entries.
- Recipes if appropriate.
- Repair ingredient.
- Durability and armor values.
- Creative tab entries.

Do not introduce unnecessary animation or rendering dependencies.

The armor is fully non-emissive.

# VALIDATION

Test:

- Head rotation with cheek guards and crest.
- Shoulder movement.
- Pteruges during walking and crouching.
- Greave alignment.
- Sandal alignment.
- Normal and slim player models if supported.
- First-person arms.
- Armor stands.
- Inventory icons.
- Daylight and dark interiors.
- Texture seams.
- Patina placement.
- No z-fighting.
- No body intersections.

Build and run Fabric 1.20.1. Fix every compilation and resource-loading problem. Report every created and modified file.
