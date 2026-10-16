Follow every applicable instruction from the `skills/` directory.

Read and follow `lore.md`.

Save the complete armor concept, dimensions, palette, particle behavior, flight-effect design, implementation decisions, and TODO items inside the `concepts/` directory.

Do not only describe the armor. Create the complete wearable 3D armor set, multilayer textures, UV mapping, emissive layer, flight effects, renderer integration, and Fabric 1.20.1 resources.

# OBJECTIVE

Create an original Fire Demonic Armor set for Minecraft Fabric 1.20.1.

The set consists of:

1. Horned demonic helmet.
2. Demonic chestplate.
3. Demonic leggings.
4. Demonic boots.
5. Complete wearable Blockbench models.
6. Multilayer pixel-art textures.
7. Separate emissive texture.
8. Fire particles and flight effects.
9. Correct first-person and third-person rendering.
10. Correct armor registration, attributes, and equipment behavior.
11. Full in-game validation.

This is supernatural demonic armor, but it must remain readable, wearable, and compatible with Minecraft geometry.

# ORIGINALITY

Create the complete design from scratch.

Do not copy armor from:

- Minecraft mods.
- Games.
- Anime.
- Films.
- Marketplace assets.
- Existing fantasy franchises.
- Downloaded Blockbench models.

Do not reuse unrelated existing concepts unless the user explicitly named them.

# DESIGN LANGUAGE

The armor is forged from supernatural volcanic metal.

Primary visual qualities:

- Heavy.
- Infernal.
- Demonic.
- Ancient.
- Aggressive.
- Heat-damaged.
- Structurally layered.
- Dark when inactive.
- Bright along internal cracks when powered.

The armor must look like blackened metal plates containing enormous internal heat.

The glow must come from recessed seams and cracks, not from every surface.

# COLOR PALETTE

Primary colors:

- Blackened iron.
- Volcanic charcoal.
- Deep blood-red metal.
- Dark crimson.
- Ember orange.
- Molten yellow-orange.
- Ash gray.
- Soot black.

Emissive gradient:

1. Pale yellow-white at the hottest centers.
2. Bright yellow.
3. Vivid orange.
4. Deep red-orange.
5. Dark red at cooling edges.
6. Black ash outside the flame.

Do not add:

- Purple magic.
- Blue fire unless explicitly requested later.
- Ice.
- Electricity.
- Green poison.
- Rainbow colors.

# BASE ARMOR CONSTRUCTION

Build each armor piece as separate wearable geometry.

Required armor layers:

1. Base inner dark layer.
2. Primary volcanic-metal plates.
3. Deep-red secondary plates.
4. Black iron edge reinforcement.
5. Recessed molten cracks.
6. Raised demonic details.
7. Fire-vent geometry.
8. Optional emissive overlay.

Do not merge the entire armor into one entity model if it must be wearable as separate equipment items.

Follow the existing project’s armor-rendering architecture.

If GeckoLib armor is already used, create a GeckoLib armor model.

If the project uses a custom armor renderer, follow that system.

Do not install GeckoLib automatically if it is absent.

# MODELING REQUIREMENTS

Use:

- Cuboids.
- Stepped curves.
- Limited rotations.
- Consistent plate thickness.
- Clear armor layering.
- Logical groups.
- Correct body-part pivots.
- Minecraft-compatible proportions.

Avoid:

- Smooth high-poly meshes.
- Subdivision surfaces.
- Excessive micro-cubes.
- Coplanar overlapping faces.
- Zero-thickness geometry.
- Invisible decorative cubes.
- Unsupported rotations.
- Armor parts that prevent normal movement.

Model the armor around standard or project-specific player proportions.

Test on both slim and normal player geometry if the project supports both.

# HELMET

Create a fully enclosed demonic helmet.

Required features:

- Blackened volcanic-metal base.
- Deep-red layered forehead plates.
- Narrow horizontal visor.
- Ember-orange light visible inside the visor.
- Reinforced jaw guard.
- Layered cheek protection.
- Neck protection.
- Central dark ridge running from forehead toward the rear.
- Two enormous demonic horns growing directly from the upper sides of the helmet.

The helmet must not reveal the player’s face.

# HORNS

The horns are a defining feature.

Construction:

- One horn emerges from the upper-left side of the helmet.
- One horn emerges from the upper-right side.
- Both visibly connect to reinforced horn bases.
- Horns curve upward and then backward.
- Use segmented cuboids to create the curve.
- Horns become narrower toward their tips.
- Horn tips angle slightly inward or backward.
- The silhouette must remain approximately balanced.
- Small asymmetry is allowed to make them feel natural.
- Cracks between horn segments may glow with ember-orange light.

Recommended hierarchy:

- `helmet`
  - `horn_left_root`
    - `horn_left_01`
    - `horn_left_02`
    - `horn_left_03`
    - `horn_left_tip`
  - `horn_right_root`
    - `horn_right_01`
    - `horn_right_02`
    - `horn_right_03`
    - `horn_right_tip`

Each segment should overlap structurally without producing z-fighting.

Do not create:

- Antlers.
- Thin goat horns.
- Floating horns.
- Smooth high-poly curves.
- Horns attached to the shoulders.
- Horns that intersect the chestplate during normal head rotation.

Test full head rotation.

# VISOR

Create a narrow infernal visor.

Requirements:

- Thin horizontal opening.
- Brightest at the center.
- Dark red toward the outer edges.
- Separate emissive UV region.
- No visible human eyes.
- No glow covering the entire helmet.
- No transparent hole exposing an empty head interior.

Create dark internal backing behind the visor.

# CHESTPLATE

Create a heavy layered demonic chestplate.

Required design:

- Central blackened sternum plate.
- V-shaped overlapping red plates.
- Rib-like side plate arrangement.
- Reinforced neck guard.
- Compact jagged shoulder protection.
- Dark abdominal plates.
- Ember cracks between plate layers.
- Two narrow fire vents on the upper back near the shoulder blades.
- Strong silhouette without excessive width.

The rib-like shapes must remain metallic armor geometry.

Do not use actual bones, flesh, or gore.

Recommended groups:

- `body`
  - `chest_core`
  - `chest_plate_upper`
  - `chest_plate_middle`
  - `chest_plate_lower`
  - `rib_plate_left`
  - `rib_plate_right`
  - `shoulder_left`
  - `shoulder_right`
  - `back_plate`
  - `back_vent_left`
  - `back_vent_right`

# SHOULDER ARMOR

Create compact jagged pauldrons.

Requirements:

- Two or three layered plates per shoulder.
- Black-red metal.
- Small upward-facing spikes or broken-plate silhouettes.
- Correct clearance from helmet horns.
- Separate left and right bones.
- No enormous World-of-Warcraft-style shoulders.
- No intersection during arm lifting.

# GAUNTLETS

Create segmented demonic gauntlets:

- Blackened forearm plates.
- Red secondary plates.
- Ember cracks near joints.
- Reinforced wrist.
- Articulated hand and finger silhouette.
- Small claw-like fingertips that remain functional.

The gauntlets must allow the player to hold normal Minecraft items.

Do not make the claws longer than the hand.

# LEGGINGS

Create:

- Reinforced demonic waist belt.
- Central ember-like buckle.
- Layered hip plates.
- Separate front, side, and rear skirt plates.
- Black inner leg protection.
- Red thigh plates.
- Segmented knee protection.
- Recessed molten cracks.

Do not create a single rigid skirt around both legs.

The legs must animate independently.

# BOOTS

Create heavy demonic boots with:

- Reinforced greaves.
- Layered ankle protection.
- Broad stable soles.
- Short claw-like toe plates.
- Ember cracks.
- Dedicated fire vents beneath both soles.
- Dark internal vent cavities.
- Bright emissive cores visible only inside vents.

The boots must not look like modern rocket boots.

The vents should appear like supernatural forge openings integrated into ancient armor.

# BONE HIERARCHY

Recommended structure:

- `armor_root`
  - `head`
    - `helmet`
    - `visor`
    - `horn_left_root`
    - `horn_right_root`
  - `body`
    - `chest_core`
    - `chest_outer`
    - `shoulder_left`
    - `shoulder_right`
    - `back_plate`
    - `back_vent_left`
    - `back_vent_right`
  - `right_arm`
    - `right_upper_armor`
    - `right_gauntlet`
  - `left_arm`
    - `left_upper_armor`
    - `left_gauntlet`
  - `right_leg`
    - `right_thigh_armor`
    - `right_knee_armor`
    - `right_greave`
    - `right_boot`
    - `right_boot_vent`
  - `left_leg`
    - `left_thigh_armor`
    - `left_knee_armor`
    - `left_greave`
    - `left_boot`
    - `left_boot_vent`
  - `effects`
    - `back_flame_left`
    - `back_flame_right`
    - `boot_flame_left`
    - `boot_flame_right`

Do not model particle flames as permanent solid armor cubes.

Effect bones exist only as attachment points.

# MULTILAYER SPACING

Recommended spacing from the player body:

- Inner armor lining: 0.15–0.3 units.
- Main plates: 0.35–0.65 units.
- Raised secondary plates: additional 0.15–0.3 units.
- Reinforced borders: additional 0.1–0.2 units.
- Horn bases: structurally connected to helmet.
- Emissive crack geometry: recessed or offset by only 0.02–0.08 units where the renderer permits.

Prefer texture-based cracks where separate geometry would cause z-fighting.

# TEXTURE RESOLUTION

Preferred:

- 128×128 for the complete armor atlas.
- Separate 128×128 emissive atlas if supported.
- Multiple 64×64 textures only if the existing renderer requires one texture per armor item.

Suggested files:

- `fire_demonic_armor.png`
- `fire_demonic_armor_emissive.png`

If the project uses separate textures:

- `fire_demonic_helmet.png`
- `fire_demonic_chestplate.png`
- `fire_demonic_leggings.png`
- `fire_demonic_boots.png`

Follow the existing resource architecture.

# BASE TEXTURE

Create:

- Black volcanic-metal surfaces.
- Deep-red raised plates.
- Charcoal shadows.
- Dark steel borders.
- Scorched edges.
- Sparse soot.
- Recessed orange cracks.
- Controlled wear.

Do not make every plate equally bright.

Large surfaces should remain primarily dark.

# EMISSIVE TEXTURE

Only these parts may be emissive:

- Visor.
- Deep armor cracks.
- Chestplate core seams.
- Back-vent interiors.
- Boot-vent interiors.
- Small belt core.
- Selected horn cracks.

Everything else must be black on the emissive map.

Emissive strength must preserve texture detail.

Do not turn the complete armor into a glowing silhouette.

If emissive rendering is unsupported, reproduce the appearance using bright pixels in the base texture and document the limitation. Do not add an unsafe renderer dependency without permission.

# UV MAPPING

Requirements:

- Manual UV layout.
- No stretched surfaces.
- No accidental mirroring of asymmetrical horn damage.
- Unique UV areas for visor, horns, chest core, vents, and boots.
- Consistent texel density.
- Sufficient island padding.
- Clear grouping by armor item.
- Matching base and emissive UV layouts.
- Every visible face mapped.

The emissive atlas must align perfectly with the base atlas.

# FIRE FLIGHT EFFECT

Fire appears when the player is actively flying.

Primary emitters:

1. Left boot sole.
2. Right boot sole.
3. Left upper-back vent.
4. Right upper-back vent.

Boot flames provide the primary thrust.

Back flames stabilize the character.

Do not use wings.

# FLAME APPEARANCE

Each flame should contain:

- Pale-yellow core.
- Bright-yellow inner region.
- Orange middle region.
- Red-orange outer region.
- Dark-red cooling pixels.
- Small ember particles.
- Sparse dark smoke particles.

The flame must taper away from the emitter.

Flames must point opposite the player’s movement direction while remaining visually stable.

At low speed:

- Short compact flames.
- Few embers.
- Almost no smoke.

At high speed:

- Longer flames.
- Brighter core.
- More embers.
- Slightly longer smoke trail.
- Increased particle velocity.

During hovering:

- Boot flames point downward.
- Back vents emit short stabilizing bursts.
- Particle density remains moderate.

During forward flight:

- Character leans forward.
- Boot flames extend backward and downward.
- Back-vent flames extend backward.
- Trails become longer.

During braking:

- Flames shorten.
- Stabilizing bursts may briefly intensify.
- Do not reverse flames unrealistically through the player’s body.

# PARTICLE IMPLEMENTATION

Use the project’s existing particle system.

Create separate particles if necessary:

- Flame-core particle.
- Outer-flame particle.
- Ember particle.
- Small smoke particle.

Particle requirements:

- Additive or emissive appearance only where supported.
- Short lifetime near the emitter.
- Longer ember lifetime.
- Gradual scale reduction.
- Controlled random spread.
- No excessive screen-filling effects.
- No permanent particles when armor is inactive.
- No particles in inventory or GUI rendering.
- No particles when the armor is displayed on an armor stand unless explicitly activated.

Synchronize effects on client and server appropriately.

Do not spawn an excessive number of particles every tick.

Use rate limiting and distance checks.

# FLIGHT ACTIVATION

Integrate with the project’s existing flight system.

Do not independently create unrestricted creative-mode flight unless requested.

Effects should activate only when:

- The complete required armor set is equipped, if full-set activation is intended.
- The player is actually flying or using the armor’s flight ability.
- The player is alive.
- The armor is active.
- The client is within the configured particle-rendering distance.

Deactivate effects immediately when:

- Flight ends.
- Armor is removed.
- Player enters water if the design requires extinguishing.
- Player dies.
- Ability is disabled.

# OPTIONAL HEAT STATE

If supported, implement visual intensity states:

- Inactive: cracks are dark red.
- Ready: cracks emit dim orange.
- Flying: vents and selected cracks glow brightly.
- Overheated: increased glow and smoke, without covering the model.

Keep gameplay logic separate from rendering logic.

# ITEM ICONS

Create clear inventory presentation for:

- Helmet.
- Chestplate.
- Leggings.
- Boots.

Each icon must:

- Show the complete item.
- Preserve the red-black-orange palette.
- Remain readable at Minecraft inventory size.
- Avoid cropping horns.
- Avoid excessive emissive bloom.
- Use correct item-model transforms.

# FIRST-PERSON RENDERING

Verify:

- Gauntlets do not cover the entire screen.
- Horns do not appear in first-person unless the project intentionally renders the helmet interior.
- Held items align with armored hands.
- Fire particles do not spawn directly inside the camera.
- Flight particles do not blind the player.
- View bobbing does not reveal missing inner faces.

# THIRD-PERSON RENDERING

Verify:

- Horns follow head rotation.
- Shoulder armor follows arm movement correctly.
- Leg armor does not merge during walking.
- Boot flames originate exactly from the soles.
- Back flames originate exactly from the vents.
- Effects follow the player without delayed detachment.
- Armor remains aligned while crouching, swimming, riding, and flying.

# FABRIC 1.20.1 INTEGRATION

Suggested identifiers:

- `fire_demonic_helmet`
- `fire_demonic_chestplate`
- `fire_demonic_leggings`
- `fire_demonic_boots`

Potential required files:

- Armor material class or registration.
- Item registrations.
- Custom armor renderer.
- GeckoLib armor model if already supported.
- Geometry JSON.
- Base texture.
- Emissive texture.
- Item model definitions.
- Particle registrations.
- Particle textures.
- Particle factories.
- Flight-effect controller.
- Language entries.
- Recipes if consistent with project progression.
- Armor attributes and durability values.
- Creative tab entries.

Use the actual mod namespace.

Do not add new libraries without explicit permission.

# ANIMATIONS

If the armor uses animated GeckoLib bones, create:

- `animation.fire_demonic_armor.idle`
- `animation.fire_demonic_armor.flight_start`
- `animation.fire_demonic_armor.flight_hover`
- `animation.fire_demonic_armor.flight_forward`
- `animation.fire_demonic_armor.flight_fast`
- `animation.fire_demonic_armor.flight_brake`
- `animation.fire_demonic_armor.flight_end`
- `animation.fire_demonic_armor.overheat`

Keep movements restrained.

The armor must follow the player rather than replacing normal player animation incorrectly.

# PERFORMANCE

Optimize:

- Cube count.
- Particle count.
- Texture resolution.
- Renderer state changes.
- Distance-based particle rendering.
- Animation calculations.
- Emissive passes.

Do not create hundreds of cubes for cracks.

Prefer texture detail over unnecessary geometry.

Do not spawn particles for distant players beyond a reasonable render distance.

# VALIDATION

Before completion:

1. Open every model in Blockbench.
2. Verify armor alignment on the player.
3. Test normal and slim body types if supported.
4. Verify all horn segments.
5. Test full head rotation.
6. Test shoulder movement.
7. Test walking, running, crouching, swimming, riding, and flying.
8. Remove all z-fighting.
9. Validate all UV mappings.
10. Verify exact base/emissive atlas alignment.
11. Test textures in bright and dark environments.
12. Confirm glow remains controlled.
13. Verify first-person visibility.
14. Verify third-person visibility.
15. Test on an armor stand.
16. Test equipping and removing every piece.
17. Verify flight-effect activation and deactivation.
18. Verify all four particle emitters.
19. Confirm particles do not spawn inside the camera.
20. Verify particle performance with multiple players.
21. Verify item icons and transforms.
22. Build the Fabric 1.20.1 project.
23. Launch the development client.
24. Fix every compilation, rendering, and resource-loading error.
25. Report every created and modified file.

Do not leave placeholders, temporary particle textures, unfinished UV regions, broken animations, unused renderers, TODO comments, missing item models, or invalid resource paths.
