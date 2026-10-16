Follow all instructions from `skills/` and the lore from `lore.md`.

Save the concept, model dimensions, robe structure, halo implementation, palette, UV plan, and rendering decisions inside `concepts/`.

Create actual production-ready assets.

# ORIGINALITY REQUIREMENT

Create an entirely original angelic armor design.

The user’s reference to Otsutsuki describes only a broad concept:

- Long pale ceremonial robe.
- Otherworldly elegance.
- Light armor.
- Clean silhouette.

Do not copy or reproduce:

- Any Naruto character.
- Otsutsuki costume patterns.
- Black magatama symbols.
- Horns.
- Forehead markings.
- Facial features.
- Color layouts.
- Named character silhouettes.
- Clan symbols.
- Naruto weapons.
- Anime-specific attributes.

Do not include any Naruto reference in filenames, code, textures, or documentation.

# OBJECTIVE

Create a complete Angelic Armor set for Fabric 1.20.1.

Required items:

- `angelic_headpiece`
- `angelic_chestplate`
- `angelic_leggings`
- `angelic_boots`

Required visual components:

- Light pearl-white armor.
- Long layered ivory robe.
- Pale-gold borders.
- Floating halo.
- Separate robe panels.
- Restrained celestial glow.
- No wings unless requested later.

# DESIGN IDENTITY

The set must appear:

- Light.
- Serene.
- Dignified.
- Ceremonial.
- Ethereal.
- Clean.
- Mobile.
- More cloth than metal.

It must not resemble a heavy paladin set.

# HEAD AND HALO

The player’s face remains visible unless the existing concept requires a hood.

Use:

- A minimal pale-gold forehead band or no physical helmet shell.
- Small pearl-white temple guards if protection is necessary.
- A floating circular halo above and slightly behind the head.

Halo requirements:

- Thin solid ring.
- Pale warm gold.
- Complete circle.
- Built from stepped rotated cuboids or a low-segment model supported by the renderer.
- Consistent thickness.
- Dedicated `halo` bone.
- Centered on the head.
- Approximately horizontal.
- Does not rotate wildly with normal head movement.
- Does not intersect the head.
- Subtle white-gold emissive edge.
- No symbols.
- No cross.
- No readable writing.
- No religious iconography.

Test halo alignment while:

- Looking up.
- Looking down.
- Turning.
- Crouching.
- Swimming.
- Sleeping.
- Riding.

# ROBE

Create a long ivory ceremonial robe.

Required layers:

1. Pale-gray inner garment.
2. Ivory main robe.
3. Overlapping front panels.
4. Long divided lower panels.
5. Two side panels.
6. Rear panel.
7. Wide but controlled sleeves.
8. Pale-gold edge trim.

The robe must allow:

- Walking.
- Running.
- Crouching.
- Jumping.
- Riding.
- Hovering if the project includes it.

Do not create a single rigid cylinder around both legs.

Separate lower panels:

- `robe_front_left`
- `robe_front_right`
- `robe_side_left`
- `robe_side_right`
- `robe_back_left`
- `robe_back_right`

Each panel should pivot from the waist or lower torso.

# CHEST ARMOR

Create:

- Slim pearl-white chest guard.
- Soft V-shaped upper edge.
- Pale-gold border.
- Small central colorless or warm-white inset.
- High robe collar behind the chest guard.
- Light upper-back plate.
- Small attached shoulder plates.

Keep the armor close to the body.

Do not add giant pauldrons.

# ARMS

Create:

- Wide ivory outer sleeves.
- Pale-gray inner sleeves.
- Narrow pearl-metal vambraces.
- Thin gold borders.
- Clean gloves or lightly protected hands.

The sleeves must not intersect the hands or chest during normal animation.

# LEGGINGS

The leggings consist primarily of the robe and inner garment.

Add:

- Pale-gray fitted trousers.
- Light knee protection.
- Small gold-edged plates.
- Separate robe panels.
- Clean waist clasp.

# BOOTS

Create:

- Pearl-white light greaves.
- Gold-edged ankle guards.
- Ivory inner footwear.
- Clean armored sandals or light boots.
- Thin soles.
- No claws.
- No oversized feet.

# MODEL HIERARCHY

Use:

- `armor_root`
  - `head`
    - `headpiece`
    - `halo`
  - `body`
    - `inner_garment`
    - `main_robe`
    - `chest_guard`
    - `back_guard`
    - `shoulder_left`
    - `shoulder_right`
    - `waist_clasp`
    - `robe_front_left`
    - `robe_front_right`
    - `robe_side_left`
    - `robe_side_right`
    - `robe_back_left`
    - `robe_back_right`
  - `right_arm`
    - `right_outer_sleeve`
    - `right_vambrace`
  - `left_arm`
    - `left_outer_sleeve`
    - `left_vambrace`
  - `right_leg`
    - `right_inner_leg`
    - `right_knee_guard`
    - `right_greave`
    - `right_boot`
  - `left_leg`
    - `left_inner_leg`
    - `left_knee_guard`
    - `left_greave`
    - `left_boot`

# MULTILAYER SPACING

Recommended:

- Body to inner garment: 0.15–0.25 units.
- Inner garment to robe: 0.15–0.35 units.
- Robe to armor: 0.2–0.45 units.
- Gold trim: 0.05–0.15 units above supporting surface.
- Halo: clearly separated above the head.

Avoid z-fighting and inflated clothing.

# TEXTURE

Preferred:

- 128×128 base atlas.
- Matching emissive atlas for halo and minimal celestial accents.

Palette:

- Ivory.
- Pearl white.
- Warm pale gold.
- Light stone gray.
- Faint desaturated sky-blue shadows.
- Soft warm white.
- Minimal dark gray in deep recesses.

White materials must not use flat pure white.

Use:

- Warm ivory midtones.
- Cool gray-blue shadows.
- Small pearl highlights.
- Gold edge pixels.

# MATERIALS

Robe:

- Matte woven cloth.
- Broad controlled folds.
- Low contrast.
- Slight warm color.

Pearl armor:

- Smooth narrow highlights.
- Pale gray shading.
- No mirror-like reflection.

Gold:

- Muted warm ochre base.
- Pale-yellow highlight.
- Brown-gold shadow.
- Never saturated orange.

Halo:

- Warm gold center.
- Pale-yellow-white emissive edge.
- Controlled bloom.

# EMISSIVE MAP

Emission only on:

- Halo.
- Tiny chest inset.
- Optional narrow gold-white seam.
- Optional hovering particles.

Do not make the entire robe emissive.

# UV MAPPING

Requirements:

- Unique UV regions for robe panels.
- Continuous gold trim where possible.
- Consistent cloth texel density.
- No stretched sleeve textures.
- No accidental mirrored asymmetric folds.
- Matching emissive atlas.
- Sufficient padding.
- Every visible face mapped.

# OPTIONAL HOVER VISUAL

Only implement hovering if the project or lore requires it.

Visual behavior:

- Robe panels drift slightly downward and outward.
- Halo remains stable.
- Sparse warm-white particles descend slowly.
- No wings.
- No jet effect.
- No huge beam.
- No constant screen-filling glow.

Do not automatically grant flight without gameplay approval.

# FABRIC INTEGRATION

Suggested identifiers:

- `angelic_headpiece`
- `angelic_chestplate`
- `angelic_leggings`
- `angelic_boots`

Create:

- Item registration.
- Armor material.
- Custom armor renderer.
- Geometry.
- Base texture.
- Emissive texture if supported.
- Item models.
- Language entries.
- Recipes if required.
- Attributes.
- Creative tab entries.

# VALIDATION

Test:

- Normal and slim player models.
- Halo alignment.
- Head rotation.
- Robe-panel movement.
- Walking.
- Running.
- Crouching.
- Swimming.
- Riding.
- Sleeping.
- Armor stands.
- First-person sleeves.
- Bright and dark lighting.
- Inventory icons.
- Base/emissive alignment.

Confirm that no Naruto symbols, costume patterns, horns, wings, or franchise references remain.

Build Fabric 1.20.1, fix all errors, and report every changed file.
