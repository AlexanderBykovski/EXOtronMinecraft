Follow every instruction from the `skills/` directory and the lore from `lore.md`.

Save all concepts, teleportation rules, dimensions, palette values, model hierarchy, particle behavior, and implementation decisions inside `concepts/`.

Create actual finished assets and code.

# OBJECTIVE

Create an original Ancient Violet Armor set from a dense, nocturnal, impossibly old forest.

The armor grants a controlled short-distance teleportation ability and has two large branching horns growing from its helmet.

Required items:

- `ancient_violet_helmet`
- `ancient_violet_chestplate`
- `ancient_violet_leggings`
- `ancient_violet_boots`

Required systems:

- Complete wearable 3D models.
- Multilayer textures.
- Emissive texture.
- Teleportation VFX.
- Teleportation sound hooks.
- Safe teleportation logic.
- Cooldown handling.
- Fabric 1.20.1 integration.

# DESIGN IDENTITY

The armor combines:

- Petrified ancient wood.
- Near-black forest metal.
- Deep-violet lacquer.
- Root-like reinforcement.
- Rigid leaf-shaped plates.
- Small controlled amethyst-colored fissures.
- Remains of moss from a nocturnal forest.

It represents forgotten forest royalty and spatial magic.

It must not look like demonic fire armor or generic purple Nether armor.

# HELMET

Create:

- Closed near-black helmet.
- Layered petrified-wood crown.
- Narrow T-shaped or vertical visor.
- Deep-violet inner darkness.
- Reinforced forehead ridge.
- Root-like cheek protection.
- Layered rear neck protection.
- Two branching backward-curving horns.

# HORNS

The horns must:

- Grow directly from reinforced helmet bases.
- Resemble extremely old blackened tree branches.
- Curve upward, outward, and then backward.
- Contain several controlled branch forks.
- Remain balanced but not perfectly symmetrical.
- Narrow toward their tips.
- Include sparse dark moss.
- Include a few recessed violet fissures.
- Never float above the helmet.
- Never intersect the shoulders during head rotation.

Recommended hierarchy:

- `horn_left_root`
  - `horn_left_trunk`
  - `horn_left_branch_a`
  - `horn_left_branch_b`
  - `horn_left_tip`
- `horn_right_root`
  - `horn_right_trunk`
  - `horn_right_branch_a`
  - `horn_right_branch_b`
  - `horn_right_tip`

Construct all curves from stepped rotated cuboids.

Do not use smooth meshes.

# CHESTPLATE

Create:

- Near-black metal inner shell.
- Layered violet leaf-shaped outer plates.
- Root-like borders.
- Compact leaf-scale shoulder protection.
- Ancient hollow central cavity.
- Controlled violet spatial core inside the cavity.
- Tapered waist silhouette.
- Root-bound back protection.
- A narrow vertical violet seam along the upper back.

The central cavity must appear deep. Add dark backing geometry behind it.

# GAUNTLETS

Create:

- Dark forearm shell.
- Root-wrapped outer plates.
- Violet leaf-shaped guards.
- Small glowing fissures.
- Articulated hands.
- Restrained claw-like fingertips.

Do not make the claws longer than the fingers.

# LEGGINGS

Create:

- Root-reinforced waist belt.
- Rigid overlapping leaf panels.
- Separate front, rear, and side sections.
- Black inner leggings.
- Twisting root ribs along thighs and shins.
- Violet knee plates.
- Small moss patches in protected recesses.

# BOOTS

Create:

- Heavy petrified-wood greaves.
- Root-wrapped ankles.
- Dark metal sole support.
- Short wooden claw-like toe plates.
- Small violet teleportation seams near heels and ankles.

# MULTILAYER STRUCTURE

Layers:

1. Inner black fabric or metal.
2. Ancient dark metal.
3. Petrified wood plates.
4. Violet leaf armor.
5. Root bindings.
6. Moss and small natural deposits.
7. Recessed spatial fissures.
8. Emissive overlay.

Recommended separation:

- Body to inner layer: 0.15–0.25 units.
- Inner layer to main armor: 0.3–0.55 units.
- Main armor to roots: 0.1–0.25 units.
- Leaf plates: 0.15–0.35 units above supporting surface.

# TEXTURE

Preferred resolution:

- 128×128 base atlas.
- Matching 128×128 emissive atlas.

Palette:

- Near-black bark.
- Charcoal forest metal.
- Midnight purple.
- Deep violet.
- Muted amethyst.
- Cold silver-gray.
- Desaturated moss green.
- Dark brown roots.

Keep most of the armor dark.

Bright violet must occupy less than approximately 15% of the visible surface.

# MATERIAL DIFFERENTIATION

Petrified wood:

- Directional grain.
- Deep cracks.
- Hard mineral highlights.
- Black-brown base.

Metal:

- Cool narrow edge highlights.
- Smoothest material in the set.
- Almost black midtones.

Leaf plates:

- Deep violet.
- Controlled central vein.
- Chipped rigid edges.
- No bright natural green.

Roots:

- Twisted brown-black pixel patterns.
- Rough matte texture.
- Slightly lighter worn edges.

Moss:

- Sparse.
- Desaturated.
- Limited to sheltered creases.
- Never bright green.

# EMISSIVE MAP

Allow emission only from:

- Visor.
- Central spatial core.
- Deep fissures.
- Selected horn cracks.
- Teleport seams near boots.
- Narrow back seam.

Do not make roots, moss, or entire plates glow.

# TELEPORTATION VISUAL EFFECT

The teleport effect must consist of:

- Blocky violet-black fragments.
- Thin vertical violet streaks.
- Dark leaf particles.
- Small shadow fragments.
- Compact circular arrival distortion.
- Brief silhouette afterimage.
- Controlled purple mist.
- No large opaque portal covering the screen.

Teleport sequence:

1. Armor fissures brighten.
2. Dark-violet particles gather around boots and torso.
3. The body begins fragmenting from the outer edges.
4. The player disappears rapidly.
5. A short trail remains at the departure point.
6. A compact arrival ring appears at the destination.
7. The player reassembles from block fragments.
8. The glow returns to its idle intensity.

Total visual duration should remain fast enough for combat.

# SAFE TELEPORT LOGIC

Implement only if gameplay implementation is included in the task.

Requirements:

- Use a configurable maximum range.
- Raycast from the player’s view direction.
- Check destination collision.
- Check headroom.
- Check floor support where required.
- Reject destinations inside blocks.
- Reject destinations inside hazardous unloaded areas.
- Respect world borders.
- Respect dimension restrictions.
- Do not teleport into unloaded chunks without approved logic.
- Preserve facing direction unless design specifies otherwise.
- Apply a configurable cooldown.
- Synchronize server position and client effects.
- Spawn departure and arrival effects at correct locations.
- Prevent repeated activation while on cooldown.
- Prevent duplication caused by client-only movement.

Keep cooldown, range, sound, and particle density configurable.

# MODEL HIERARCHY

Use:

- `armor_root`
  - `head`
    - `helmet`
    - `visor`
    - `horn_left_root`
    - `horn_right_root`
  - `body`
    - `inner_shell`
    - `chest_armor`
    - `spatial_core`
    - `back_armor`
    - `shoulder_left`
    - `shoulder_right`
  - `right_arm`
    - `right_forearm_armor`
    - `right_gauntlet`
  - `left_arm`
    - `left_forearm_armor`
    - `left_gauntlet`
  - `right_leg`
    - `right_thigh`
    - `right_knee`
    - `right_greave`
    - `right_boot`
  - `left_leg`
    - `left_thigh`
    - `left_knee`
    - `left_greave`
    - `left_boot`
  - `effects`
    - `teleport_core`
    - `departure_origin`
    - `arrival_origin`

Effect bones are attachment points, not permanent solid effects.

# UV AND PIXEL ART

Use:

- Manual UV mapping.
- Matching base and emissive atlases.
- Consistent texel density.
- Unique UV regions for horns, core, visor, roots, boots, and asymmetrical moss.
- Nearest-neighbor filtering.
- No antialiasing.
- No smooth gradients.
- No random noise.
- No accidental mirrored horn damage.
- No coplanar surfaces.

# FABRIC INTEGRATION

Suggested identifiers:

- `ancient_violet_helmet`
- `ancient_violet_chestplate`
- `ancient_violet_leggings`
- `ancient_violet_boots`
- `ancient_violet_teleport`
- `ancient_violet_fragment`
- `ancient_violet_leaf`
- `ancient_violet_arrival`

Follow the existing armor, ability, networking, cooldown, renderer, and particle systems.

Do not introduce new dependencies without permission.

# VALIDATION

Test:

- Helmet rotation with horns.
- All player animations.
- Slim and normal player models if supported.
- First-person visibility.
- Armor stands.
- Teleporting horizontally.
- Teleporting upward and downward.
- Blocked destination.
- Insufficient headroom.
- World border.
- Cooldown.
- Multiplayer synchronization.
- Particle performance.
- Unloaded destination handling.
- Death or armor removal during activation.
- Base/emissive atlas alignment.

Build and launch Fabric 1.20.1. Fix all errors and report every modified file.
