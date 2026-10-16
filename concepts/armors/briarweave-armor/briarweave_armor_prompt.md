Follow all instructions from `skills/` and `lore.md`.

Save the full concept and technical documentation inside `concepts/`.

Create the actual model, textures, UV mapping, registration, and renderer resources.

# OBJECTIVE

Create a complete original armor set made from the bark of ancient trees growing in a dark, dense night forest.

Required items:

- `ancient_bark_helmet`
- `ancient_bark_chestplate`
- `ancient_bark_leggings`
- `ancient_bark_boots`

This set has no violet teleportation magic.

Do not add:

- Horns.
- Antlers.
- Purple glow.
- Teleport effects.
- Runes.
- Demonic faces.
- Bright flowers.
- Large green leaves.
- Metal-heavy construction.

# DESIGN IDENTITY

The armor is:

- Natural.
- Ancient.
- Quiet.
- Rough.
- Protective.
- Grown and assembled from thick bark.
- Reinforced by roots.
- Covered with sparse dark moss and pale lichen.
- Adapted to a dense night forest.

The main silhouette must resemble layered tree bark rather than ordinary metal plates painted brown.

# HELMET

Create:

- Low layered bark crown.
- Thick overlapping forehead plates.
- Narrow face opening.
- Short cheek guards.
- Reinforced rear section.
- Root bindings around the sides.
- Small lichen clusters.
- No horns or branch projections.

The helmet must allow full head rotation without colliding with the shoulders.

# CHESTPLATE

Create:

- Thick overlapping bark slabs.
- Central pattern inspired by tree growth rings.
- Dark root network securing the plates.
- Compact bark-scale shoulder protection.
- Reinforced side panels.
- Bark backplate.
- Dark leather inner harness.
- Asymmetrical natural wear.

The growth-ring pattern must be original and must not resemble a magical symbol.

# GAUNTLETS

Create:

- Layered bark forearm guards.
- Twisting root bindings.
- Dark leather wrist straps.
- Small hand protection.
- Open or lightly armored fingers.
- Sparse lichen.

# LEGGINGS

Create:

- Dark leather waist belt.
- Simple wooden buckle.
- Vertical bark-strip skirt panels.
- Separate left and right thigh protection.
- Root-bound knee guards.
- Dark flexible inner trousers.
- Vertical wood ribs along the shins.

# BOOTS

Create:

- Layered bark greaves.
- Root-wrapped ankles.
- Thick wooden soles.
- Compact toe protection.
- Dark moss in recessed areas.
- No claws unless extremely short and structural.

# MULTILAYER GEOMETRY

Required layers:

1. Inner dark cloth.
2. Leather support harness.
3. Main bark slabs.
4. Secondary bark scales.
5. Root bindings.
6. Moss and lichen details.
7. Raised growth-ring sections.

Recommended spacing:

- Body to cloth: 0.15–0.25 units.
- Cloth to bark: 0.25–0.55 units.
- Bark to roots: 0.1–0.25 units.
- Moss geometry: use only for major clusters; paint small moss into the texture.

Avoid using a separate cube for every crack or moss pixel.

# TEXTURE

Preferred:

- 128×128 atlas for a detailed custom model.
- 64×64 only for a simpler renderer.

Palette:

- Near-black brown.
- Deep umber.
- Charcoal bark.
- Muted walnut.
- Dark leather.
- Desaturated moss green.
- Gray-green lichen.
- Pale weathered wood.

Bark texture:

- Directional grain.
- Layered fractures.
- Dark cracks.
- Worn raised edges.
- Slight tonal variation.
- No photographic noise.

Growth rings:

- Concentric stepped bands.
- Irregular spacing.
- Darker inner cracks.
- Subtle worn highlights.
- No glow.

Roots:

- Twisted directional pixels.
- Dark brown base.
- Lighter worn top edges.
- Rough matte surface.

Moss:

- Sparse clusters.
- Dark olive.
- Located primarily in protected creases.
- No bright saturated green.

Lichen:

- Small pale gray-green clusters.
- Irregular shapes.
- Very limited coverage.

# MODEL HIERARCHY

Use:

- `armor_root`
  - `head`
    - `bark_helmet`
    - `cheek_guard_left`
    - `cheek_guard_right`
    - `root_binding`
  - `body`
    - `inner_harness`
    - `chest_bark`
    - `growth_ring_core`
    - `back_bark`
    - `shoulder_left`
    - `shoulder_right`
  - `right_arm`
    - `right_bark_guard`
    - `right_root_binding`
  - `left_arm`
    - `left_bark_guard`
    - `left_root_binding`
  - `right_leg`
    - `right_thigh_bark`
    - `right_knee`
    - `right_greave`
    - `right_boot`
  - `left_leg`
    - `left_thigh_bark`
    - `left_knee`
    - `left_greave`
    - `left_boot`

# UV MAPPING

Requirements:

- Manual UV layout.
- Consistent pixel scale.
- Bark grain oriented along each plate.
- Unique UV regions for chest growth rings and asymmetrical moss.
- No accidental mirrored root patterns.
- No stretched grain.
- Adequate island padding.
- Every visible face mapped.
- No unused temporary UV-guide colors.

# RENDERING

The set must be entirely non-emissive.

Test its readability in:

- Moonlight.
- Dense forest shadows.
- Bright daylight.
- Nether lighting.
- Inventory GUI.

Dark armor must remain visible through controlled highlights, not artificial glow.

# FABRIC INTEGRATION

Create:

- Armor registrations.
- Armor material.
- Geometry and renderer.
- Texture.
- Item models.
- Language entries.
- Recipes if appropriate.
- Creative tab entries.
- Attributes and durability.
- Repair ingredient logic if required.

Suggested identifiers:

- `ancient_bark_helmet`
- `ancient_bark_chestplate`
- `ancient_bark_leggings`
- `ancient_bark_boots`

Do not invent magical abilities unless later requested.

# VALIDATION

Verify:

- Player alignment.
- Head movement.
- Shoulder clearance.
- Walking and crouching.
- Independent leg movement.
- Armor-stand rendering.
- First-person arms.
- Texture seams.
- Grain direction.
- Moss placement.
- No horns.
- No purple elements.
- No emissive pixels.
- No z-fighting.
- No exposed unintended body surfaces.

Build and test the Fabric 1.20.1 project. Fix all errors and report all created and modified files.
