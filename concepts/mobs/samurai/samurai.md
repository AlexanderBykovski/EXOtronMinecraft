Follow every applicable instruction from the `skills/` directory.

Read and follow the project lore from `lore.md`.

Save all concepts, dimensions, color palettes, implementation decisions, TODO items, technical notes, and unresolved questions inside the `concepts/` directory.

Do not only write a plan or describe the result. Create the complete production-ready 3D model, multilayer pixel-art texture, UV mapping, animation structure, renderer integration, and all required Fabric 1.20.1 resources.

# OBJECTIVE

Create an original Red Samurai Shogun for a Minecraft Fabric 1.20.1 mod.

The final result must include:

1. A complete Blockbench-compatible humanoid 3D model.
2. Multilayer clothing and armor geometry.
3. A complete pixel-art texture atlas.
4. Correct UV mapping.
5. Correct bone hierarchy and pivots.
6. Traditional katana and wakizashi equipment.
7. GeckoLib animations if GeckoLib is already installed.
8. Entity registration and rendering if this is a new entity.
9. Correct scale, hitbox, shadow, eye height, and equipment attachment.
10. In-game testing and build verification.

Create the entire design from scratch.

Do not copy existing Minecraft mods, skins, games, anime characters, films, marketplace assets, historical reenactment models, or downloaded Blockbench projects.

# CHARACTER IDENTITY

The character is an experienced Japanese military ruler and elite samurai commander.

Approximate age:

- 40–50 years old.

Personality:

- Authoritative.
- Disciplined.
- Patient.
- Strategically intelligent.
- Emotionally controlled.
- Fearless.
- Formal.
- Respected by his soldiers.
- Dangerous without behaving wildly.

His status must be communicated through armor quality, posture, controlled animation, and restrained decorative elements.

He must remain human and non-magical.

Do not add:

- Glowing eyes.
- Aura.
- Flames.
- Runes.
- Demonic features.
- Supernatural powers.
- Fantasy weapons.
- Impossible armor.
- Giant body proportions.

# BODY PROPORTIONS

Use Minecraft-compatible humanoid proportions.

Recommended model dimensions:

- Total height: approximately 31–33 Blockbench units.
- In-game height: approximately 1.9–2.05 blocks.
- Head: approximately 8×8×8 units before outer layers.
- Torso: approximately 8–9 units wide.
- Arms: approximately 4 units wide.
- Legs: approximately 4 units wide.
- Build: tall, strong, and broad-shouldered.
- Body must be powerful but not bodybuilder-like.

The character must look slightly larger and more imposing than an ordinary Minecraft player without becoming a giant.

# NEUTRAL MODELING POSE

Build the model in a neutral symmetrical pose:

- Torso upright.
- Head facing forward.
- Arms slightly separated from the torso.
- Elbows straight.
- Hands facing inward.
- Legs parallel.
- Feet facing forward.
- Katana and wakizashi sheathed at the left waist.
- Armor plates resting in their natural positions.

Do not model the character permanently holding a weapon or standing in a combat pose.

# FACE

Create a mature Japanese male face with:

- Focused dark-brown eyes.
- Thick dark eyebrows.
- A broad but controlled jaw.
- Restrained age lines.
- A serious neutral expression.
- A short dark moustache visible as part of the menpo design or beneath it.
- Natural light-to-medium skin tone.

Do not make him permanently enraged.

The expression must communicate authority and concentration.

# HELMET

Create a traditional red-lacquered kabuto helmet.

Required construction:

- Reinforced red central helmet bowl.
- Multiple visible overlapping plates.
- Black iron plate edges.
- Layered black-and-red shikoro neck protection.
- Side protection around the temples.
- A muted antique-gold crescent-shaped maedate crest.
- A small original circular clan emblem at the center of the crest.
- Restrained gold fastening details.
- Correct clearance around the shoulders and neck.

The crescent must be modelable with stepped cuboids rather than a smooth high-poly curve.

Create it from a limited number of rotated cuboids with consistent thickness.

Do not create horns. The crescent is a decorative crest, not part of the creature’s body.

# MENPO

Create a traditional protective half-mask.

Required characteristics:

- Red-lacquered or dark-red surface.
- Protection for cheeks, nose, and jaw.
- Small ventilation openings.
- Dark iron edges.
- Fierce but historically grounded expression.
- Short dark moustache detail.
- Separate geometry from the face and helmet.

The mask must not resemble a demon skull.

It must not contain glowing parts.

# INNER CLOTHING

Create dark indigo clothing beneath the armor:

- Crossed front collar.
- Narrow off-white inner collar.
- Long sleeves.
- Dark indigo trousers.
- Black tabi.
- Traditional straw sandals or armored footwear consistent with the concept.

The clothing must remain visible at:

- Neck.
- Armpits.
- Elbows.
- Waist.
- Upper legs.
- Behind knees.

# CHEST ARMOR

Create a deep-crimson lamellar do chest armor.

Required geometry:

- Several horizontal or slightly overlapping armor rows.
- Black iron borders.
- Dark-red side panels.
- Muted antique-gold rivets.
- Brown and dark-gold fastening cords.
- Slightly thicker central chest protection.
- Separate front, side, and back armor surfaces.
- Small original clan medallions near the upper chest.

The armor must be layered geometry rather than a pattern painted directly onto the body.

Recommended distance from clothing layer:

- 0.35–0.65 Blockbench units.

Avoid excessive inflation that makes the torso appear swollen.

# SHOULDER ARMOR

Create traditional layered sode shoulder guards.

Requirements:

- Four to six readable horizontal plate rows.
- Dominant deep-red lacquer.
- Black iron borders.
- Muted-gold fasteners.
- Brown connecting cords.
- Broad commanding silhouette.
- Separate left and right bones.
- Correct pivots at shoulder attachment points.

The shoulder armor must move with a controlled delay during animation without intersecting the head or chest.

# ARM ARMOR

Create:

- Dark indigo sleeves.
- Red-and-black kote forearm protection.
- Layered rectangular armor plates.
- Reinforced wrist guards.
- Small dark iron rivets.
- Brown fastening straps.
- Partially visible hands.

The gauntlets must not prevent the character from holding a katana correctly.

# WAIST AND LOWER ARMOR

Create:

- A thick dark-brown waist belt.
- A central decorative knot.
- Multiple layered kusazuri skirt plates.
- Separate front, rear, left, and right armor panels.
- Deep-red lacquered surfaces.
- Black iron borders.
- Muted-gold fasteners.
- Dark indigo trousers visible between panels.

Each skirt panel must have its own pivot if secondary movement is animated.

Prevent panels from intersecting the legs during walking and attacks.

# LEG ARMOR

Create:

- Compact red haidate thigh protection.
- Dark cloth base.
- Red suneate shin guards.
- Black iron vertical reinforcement.
- Brown cords and straps.
- Black tabi.
- Traditional sandals or restrained armored footwear.

Do not turn the lower body into European plate armor.

# WEAPONS

Attach two ordinary traditional Japanese swords to the left waist:

1. Full-sized katana.
2. Short wakizashi.

Design:

- Polished steel blades.
- Plain dark iron tsuba.
- Black handle wrapping with red underlayer.
- Muted-brass habaki.
- Black scabbards with restrained red details.
- Muted-gold fittings.
- No glow or magic.

Placement:

- Katana above and slightly outside.
- Wakizashi below and slightly inside.
- Both handles angled forward.
- Scabbards angled slightly backward.
- Both attached to the waist belt.
- No intersection with legs or armor.

Reuse existing katana and wakizashi assets if they already exist.

# BONE HIERARCHY

Use existing project naming conventions when available.

Otherwise use:

- `root`
  - `master`
    - `body`
      - `inner_clothing`
      - `chest_armor`
      - `back_armor`
      - `waist`
      - `waist_belt`
      - `kusazuri_front`
      - `kusazuri_back`
      - `kusazuri_left`
      - `kusazuri_right`
    - `head`
      - `face`
      - `menpo`
      - `kabuto`
      - `helmet_crest`
      - `shikoro`
    - `right_arm`
      - `right_sleeve`
      - `right_sode`
      - `right_kote`
      - `right_hand`
      - `right_weapon_socket`
    - `left_arm`
      - `left_sleeve`
      - `left_sode`
      - `left_kote`
      - `left_hand`
      - `left_weapon_socket`
    - `right_leg`
      - `right_haidate`
      - `right_suneate`
      - `right_foot`
    - `left_leg`
      - `left_haidate`
      - `left_suneate`
      - `left_foot`
    - `equipment`
      - `katana_scabbard`
      - `katana_handle`
      - `wakizashi_scabbard`
      - `wakizashi_handle`

# MULTILAYER GEOMETRY

Required visual layers:

1. Base body.
2. Inner clothing.
3. Outer cloth folds.
4. Primary armor plates.
5. Black iron armor borders.
6. Fastening cords and belts.
7. Decorative medallions.
8. Helmet.
9. Menpo.
10. Weapon equipment.

Recommended separation:

- Body to clothing: 0.15–0.3 units.
- Clothing to armor: 0.3–0.6 units.
- Armor to borders and cords: 0.1–0.25 units.
- Face to menpo: 0.25–0.5 units.
- Head to helmet: 0.4–0.8 units.

Do not place multiple textured faces on exactly the same plane.

# TEXTURE

Recommended resolution:

- 128×128 for a detailed GeckoLib model.
- 64×64 only if the project uses standard Minecraft entity complexity.

Use a controlled palette:

- Deep crimson.
- Dark vermilion.
- Black-red shadows.
- Black iron.
- Dark indigo.
- Muted antique gold.
- Dark brown leather.
- Straw beige.
- Natural skin colors.
- Steel gray.

Texture rules:

- Nearest-neighbor only.
- No antialiasing.
- No smooth gradients.
- No photographic materials.
- No random noise.
- Consistent texel density.
- Deliberate pixel clusters.
- Clear material separation.
- Manually painted highlights and shadows.
- One consistent light direction.

Material rendering:

- Lacquer: narrow bright highlights and dark reflective shadows.
- Iron: cool-gray edge highlights.
- Cloth: broad low-contrast folds.
- Leather: warm irregular midtones and dark edges.
- Gold: restrained ochre highlights, never bright yellow.
- Skin: minimal texture noise.
- Straw: small woven pixel pattern.

# UV MAPPING

Create manual UV mapping.

Requirements:

- No stretched faces.
- No accidental mirroring.
- No overlapping islands unless intentional.
- Consistent texel density.
- Unique UV space for face, crest, knots, mask, and weapons.
- Symmetrical armor may share UV space only where exact symmetry is intended.
- Sufficient padding between islands.
- Every visible face must be mapped.

# ANIMATIONS

If the project uses GeckoLib, create:

- `animation.red_shogun.idle`
- `animation.red_shogun.walk`
- `animation.red_shogun.run`
- `animation.red_shogun.combat_idle`
- `animation.red_shogun.draw_katana`
- `animation.red_shogun.sheathe_katana`
- `animation.red_shogun.attack_horizontal`
- `animation.red_shogun.attack_diagonal`
- `animation.red_shogun.attack_overhead`
- `animation.red_shogun.block`
- `animation.red_shogun.parry`
- `animation.red_shogun.command`
- `animation.red_shogun.hurt`
- `animation.red_shogun.death`

Movement must feel:

- Heavy.
- Controlled.
- Experienced.
- Deliberate.
- Powerful without being slow and clumsy.

Armor plates should use subtle secondary movement.

# FABRIC INTEGRATION

Suggested identifier:

- `red_shogun`

Use the real project namespace.

Create all required:

- Entity class.
- Entity registration.
- Attributes.
- Renderer.
- Model class.
- Geometry JSON.
- Animation JSON.
- Texture PNG.
- AI goals if required.
- Language entries.
- Spawn egg if the project uses them.
- Loot table if required.
- Sounds only if suitable original or existing project sounds are available.

Do not install new dependencies without permission.

# VALIDATION

Before completion:

1. Open and validate the model in Blockbench.
2. Test every pivot.
3. Remove duplicate and hidden cubes.
4. Remove z-fighting.
5. Verify every UV face.
6. Verify armor-layer spacing.
7. Verify helmet clearance.
8. Verify shoulder-armor movement.
9. Verify skirt-panel movement.
10. Verify sword attachment.
11. Test all animations.
12. Verify scale, eye height, hitbox, and shadow.
13. Build the Fabric 1.20.1 project.
14. Launch the development client if possible.
15. Fix all compilation and resource-loading errors.
16. Report every created and modified file.

Do not leave placeholders, TODO comments, broken references, temporary textures, incomplete animations, or unused exports.
