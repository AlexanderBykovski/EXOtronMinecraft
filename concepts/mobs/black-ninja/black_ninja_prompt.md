Follow every applicable instruction from the `skills/` directory.

Read and follow `lore.md`.

Save all concepts, palettes, dimensions, technical decisions, animation notes, and TODO items inside the `concepts/` directory.

Create actual finished assets. Do not stop after planning.

# OBJECTIVE

Create a complete original Dark Ninja character for Minecraft Fabric 1.20.1.

Required result:

1. Blockbench-compatible 3D model.
2. Multilayer stealth clothing.
3. Multilayer pixel-art texture.
4. Correct UV mapping.
5. Animation-ready bone hierarchy.
6. Attached stealth equipment.
7. GeckoLib animations if supported.
8. Fabric entity registration and renderer if required.
9. Complete in-game testing.

# DESIGN PRINCIPLES

The ninja must appear:

- Silent.
- Fast.
- Lightweight.
- Practical.
- Disciplined.
- Dangerous.
- Difficult to notice in darkness.

He is a grounded human stealth operative.

Do not add:

- Magic.
- Smoke powers.
- Teleportation effects.
- Glowing eyes.
- Neon details.
- Energy weapons.
- Fantasy assassin armor.
- Horns.
- Demonic mask.
- Modern military equipment.
- Firearms.

# BODY

Use a lean athletic Minecraft-compatible body.

Recommended:

- Height: 30–31 model units.
- In-game height: approximately 1.8–1.9 blocks.
- Narrow shoulders.
- Slim waist.
- Strong legs.
- Compact silhouette.
- No exaggerated muscles.
- No oversized head.

Build in a neutral pose with arms slightly separated from the torso.

# HEAD AND MASK

Create a layered traditional shinobi-style head covering.

Layers:

1. Base head.
2. Inner dark cloth cap.
3. Wrapped hood.
4. Lower-face mask.
5. Narrow cloth overlap around the neck.

Only the eyes and a narrow section of surrounding skin remain visible.

Eyes:

- Dark brown.
- Focused.
- Calm.
- No glow.
- No permanent rage.

Hood requirements:

- Charcoal-black.
- Slightly asymmetrical cloth folds.
- Close-fitting silhouette.
- Separate lower-face mask.
- Separate neck wrap.
- No long scarf.
- No loose fabric that blocks animation.
- No oversized anime hood.

Recommended distance from the head:

- Inner cap: 0.15–0.25 units.
- Hood: 0.3–0.55 units.
- Mask: 0.25–0.4 units from the face.

# UPPER CLOTHING

Create a short dark shinobi uwagi-style jacket.

Required details:

- Overlapping V-shaped closure.
- Charcoal-black primary fabric.
- Very dark indigo secondary fabric.
- Reinforced shoulder panels.
- Fitted sleeves.
- Narrow cuffs.
- Dark belt around the waist.
- Short split cloth panels around the hips.

Keep the silhouette flexible.

Do not create heavy chest armor.

A thin concealed protective layer may be represented with small dark-gray quilted panels on the shoulders and upper torso.

# ARMS

Create:

- Fitted dark sleeves.
- Layered forearm wraps.
- Thin matte bracers.
- Wrapped wrists.
- Partially exposed fingertips or thin gloves.
- Separate right and left hands.

The hands must be able to hold:

- Short sword.
- Kunai.
- Rope.
- Throwing tools.

# LOWER CLOTHING

Create flexible split-leg trousers.

Requirements:

- Dark charcoal cloth.
- Slightly loose upper legs.
- Tapered lower legs.
- Wrapped calves.
- Black tabi boots.
- Thin reinforced soles.
- No baggy modern cargo trousers.

Represent folds through texture and limited outer geometry.

# EQUIPMENT BELT

Create a functional dark-brown belt and utility sash.

Attach:

- Two small rear utility pouches.
- Two sheathed kunai.
- One compact rope coil.
- A short sword scabbard.
- Optional small flat throwing-tool pouch.

Every item must have:

- A dedicated attachment point.
- Clear orientation.
- Correct scale.
- No intersection with the torso or legs.
- No excessive swinging.

Do not cover the entire body in pouches and straps.

# SHORT SWORD

Create or reuse a short plain ninja sword.

Design:

- Straight or very slightly curved steel blade.
- Matte-black scabbard.
- Simple dark iron guard.
- Black handle wrapping.
- Dark-brown attachment cord.
- No glow.
- No oversized blade.

Place it diagonally across the lower back or left rear hip.

The handle must remain reachable by the right hand.

Do not place the scabbard across the upper back where it prevents natural drawing.

# KUNAI

Create two small sheathed kunai.

Required design:

- Dark dull iron.
- Compact triangular blade.
- Wrapped dark-brown handle.
- Small ring at the end.
- No decorative glow.
- Stored securely at the waist.

Use low cube counts.

# BONE HIERARCHY

Recommended structure:

- `root`
  - `master`
    - `body`
      - `inner_tunic`
      - `outer_jacket`
      - `shoulder_padding`
      - `waist`
      - `belt`
      - `hip_cloth_front`
      - `hip_cloth_back`
    - `head`
      - `face`
      - `inner_cap`
      - `hood`
      - `face_mask`
      - `neck_wrap`
    - `right_arm`
      - `right_sleeve`
      - `right_forearm_wrap`
      - `right_hand`
      - `right_weapon_socket`
    - `left_arm`
      - `left_sleeve`
      - `left_forearm_wrap`
      - `left_hand`
      - `left_weapon_socket`
    - `right_leg`
      - `right_trouser`
      - `right_calf_wrap`
      - `right_foot`
    - `left_leg`
      - `left_trouser`
      - `left_calf_wrap`
      - `left_foot`
    - `equipment`
      - `short_sword_scabbard`
      - `short_sword_handle`
      - `kunai_left`
      - `kunai_right`
      - `rope`
      - `pouch_left`
      - `pouch_right`

# PIVOTS

Place:

- Head pivot at neck base.
- Arms at shoulders.
- Forearms at elbows if separate.
- Hands at wrists.
- Legs at hips.
- Lower legs at knees if separate.
- Feet at ankles.
- Hood pivot at the head.
- Hip-cloth pivots at the belt.
- Sword-scabbard pivot at its belt attachment.
- Pouch and rope pivots at their attachment points.

Test every pivot through rotation.

# MULTILAYER CONSTRUCTION

Required layers:

1. Base body.
2. Inner clothing.
3. Outer jacket.
4. Hood and mask.
5. Reinforced cloth panels.
6. Forearm and calf wraps.
7. Belt and hip panels.
8. Equipment.

Recommended spacing:

- Body to clothing: 0.15–0.3 units.
- Inner clothing to jacket: 0.15–0.3 units.
- Head to cap: 0.15–0.25 units.
- Cap to hood: 0.15–0.35 units.
- Arm to wraps: 0.2–0.35 units.

Prevent z-fighting.

Do not make every layer equally thick.

# TEXTURE RESOLUTION

Preferred:

- 64×64 for a simple model.
- 128×128 for a detailed GeckoLib model.

Palette:

- Near-black blue-gray.
- Charcoal black.
- Dark indigo.
- Muted slate gray.
- Dark brown.
- Dull iron.
- Natural skin.
- Dark-brown eyes.

Do not use one flat black color.

Dark materials must remain separable through:

- Slight hue variation.
- Controlled edge highlights.
- Different pixel patterns.
- Different reflectivity.
- Carefully placed shadows.

# MATERIAL TEXTURING

Hood and mask:

- Soft matte cloth.
- Low-contrast folds.
- Almost no highlights.

Outer jacket:

- Slightly rough woven pattern.
- Dark indigo edge pixels.
- Visible overlapping closure.

Reinforced panels:

- Dark-gray quilted or crosshatched pattern.
- Slightly stronger highlights than cloth.

Leather:

- Muted dark brown.
- Worn edges.
- Sparse warm highlights.

Iron:

- Dull cold gray.
- No polished shine.
- Small edge highlights.

Skin:

- Clean pixel clusters.
- Minimal noise.
- Narrow visible area around eyes.

# PIXEL-ART RULES

Use:

- Nearest-neighbor.
- Hard pixel edges.
- Limited palette.
- Consistent texel density.
- Hand-painted shading.
- Clear material boundaries.

Never use:

- Antialiasing.
- Blur.
- Smooth gradients.
- Photographic materials.
- Random noise.
- Semi-transparent edge pixels.
- Excessive dithering.

# UV MAPPING

Requirements:

- Manual logical UV layout.
- No stretched faces.
- No accidental mirroring.
- Unique UV regions for eyes, hood folds, mask, belt, pouches, and tools.
- Consistent pixel scale.
- Sufficient island padding.
- Every visible face intentionally mapped.

# ANIMATIONS

Create when supported:

- `animation.dark_ninja.idle`
- `animation.dark_ninja.crouch_idle`
- `animation.dark_ninja.walk`
- `animation.dark_ninja.crouch_walk`
- `animation.dark_ninja.run`
- `animation.dark_ninja.draw_sword`
- `animation.dark_ninja.sheathe_sword`
- `animation.dark_ninja.attack_fast`
- `animation.dark_ninja.attack_diagonal`
- `animation.dark_ninja.stab`
- `animation.dark_ninja.throw_kunai`
- `animation.dark_ninja.block`
- `animation.dark_ninja.dodge_left`
- `animation.dark_ninja.dodge_right`
- `animation.dark_ninja.hurt`
- `animation.dark_ninja.death`

Animation principles:

- Low center of gravity.
- Quiet steps.
- Fast acceleration.
- Controlled stopping.
- Minimal arm movement during stealth walking.
- Precise attacks.
- No random spinning.
- No acrobatics without gameplay justification.
- No feet sliding.
- No equipment clipping.
- Short clean recovery after attacks.

# FABRIC INTEGRATION

Suggested identifier:

- `dark_ninja`

Use the actual project namespace.

Create only the necessary:

- Entity class.
- Entity registration.
- Attributes.
- Renderer.
- Model.
- Geometry JSON.
- Animation JSON.
- Texture.
- AI goals.
- Language entries.
- Spawn egg if applicable.
- Loot table if applicable.

Do not add a new animation library without permission.

# VALIDATION

1. Validate model hierarchy.
2. Test all pivots.
3. Remove duplicated cubes.
4. Remove hidden geometry.
5. Remove z-fighting.
6. Inspect UV seams.
7. Test texture in bright and dark lighting.
8. Confirm that black materials remain readable.
9. Check hood and mask intersections.
10. Check sword drawing clearance.
11. Check pouches and rope during movement.
12. Test every animation.
13. Validate hitbox, scale, eye height, and shadow.
14. Build the Fabric 1.20.1 project.
15. Test in the development client.
16. Fix all resource and compilation errors.
17. Report every created and modified file.

Do not leave temporary files, placeholders, incomplete animations, broken resource paths, or TODO comments.
