# MASTER PROMPTS — OPUS WEAPONS/TOOLS + EXISTING VISUAL ITEMS

![Opus master concept](concept_art/opus_master_concept.png)

This archive is built for an AI agent that must work **inside the existing mod project**.

## Critical master rule

- The agent must **find the real existing items in the mod files** and recreate **those exact items in-place**.
- It must not create duplicate registrations or replacement items with new IDs unless a prompt explicitly says otherwise (none of these prompts do).
- For the concept-art tools, the supplied concept image is the primary visual reference.
- For items with no concept art, the agent must create the concept from the provided textual description while still editing the existing item in-place.
- For the final batch of ingredient/resource items, the task is **visual-only**. Their functional code already exists and must remain untouched.

## Opus tool / weapon ability overview

- **Katana-OP — Blue Air Slash**: RMB releases a fast forward blue cutting-wave / wind-blade slash. The slash travels in front of the player in a clean line, damages every valid enemy it intersects once, and visually leaves a compressed blue air-separation trail rather than an explosion.
- **Golden Katana — ChoCho Sword style special**: Implement the special with the same FEEL as the ChoCho Sword ability from Shindo Life: a flashy aggressive golden-energy katana technique centered on fast slashing pressure and dramatic anime-style golden strike effects. Preserve the idea and gameplay feel while implementing it cleanly in the actual Fabric/GeckoLib project.
- **Refined Opus Katana — Circular Air Cut**: RMB emits a circular air-blade around the player: a ring-like outward slash that expands from the wielder, damaging valid enemies in a controlled radius around the player one time each. It is a clean air-pressure cut, not an explosion.
- **Opus Warhammer — Shockwave**: RMB slams the hammer into the ground and emits a circular ground shockwave around the player. Valid nearby enemies are thrown slightly upward / popped into the air and receive a slowing effect. The shockwave is ground-based, controlled, and never destroys terrain.
- **Opus Pickaxe — Azure Vein Resonance**: RMB on a valid ore triggers a bounded vein resonance. Blue energy spreads through the connected ore vein and mines a limited number of connected matching ore blocks through legitimate server loot logic. The action is bounded, clean, and enchantment-compatible.
- **Opus Axe — Crosscut Arc**: RMB sends a short-range blue crescent arc forward. It hits valid enemies in front of the player in a controlled fan or corridor, applies one clean damage instance per target, and slightly knocks them back. No terrain destruction.
- **Opus Hoe — Growth Lattice**: Ordinary tilling is intrinsically upgraded to 3x3 on valid soil. RMB/context-use on a planted crop triggers Growth Lattice: a bounded blue energy pulse that instantly matures valid crops in a controlled area. The growth cooldown must never block ordinary 3x3 tilling.
- **Opus Shovel — Prism Trench**: RMB on a valid shovel block excavates a precise 3x3x1 plane based on the clicked face. Only legitimate shovel-mineable blocks are affected. The action is clean, bounded, and respects real drops and durability.
- **Steel Katana — No new ability**: Do not invent a new special ability unless the existing item already has one in code. The focus here is concept creation from text, model creation and clean katana animations while preserving the mod's existing functionality.
- **Long Katana — No new ability**: Do not invent a new special ability unless the existing item already has one in code. The focus is concept generation from the description, longer-blade modeling and appropriate animations while preserving existing functionality.

---

## Part I — Concept-art-based weapons and tools

# Katana-OP — ULTRA-DETAILED MASTER PROMPT

![Katana-OP concept](concept_art/katana_op.png)

```text
# ITEM: Katana-OP
# Recommended likely registry id: katana_op
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Katana-OP, katana_op, Katana OP. Check lang files, item registration classes, item
model JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place;
do not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: Opus blue techno-forged style: dark steel / black forged metal, blue crystal
or energy core, blue emissive cuts, black wrapped grip. Visual target: a long dark katana with a
bright vertical blue energy channel, angular guard details, black wrapped handle, blue crystal
accents and a high-end anime-tech sword silhouette. Preserve katana identity, sharp tip, blade
curvature discipline, elegant but aggressive blue energy treatment. Do not redesign into a generic
broadsword. If concept art is present, treat it as the primary silhouette/layout reference. If
concept art is absent, generate the concept from the provided description only while staying
consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Katana-OP and do not let it drift into a generic
sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: Opus blue techno-forged style: dark
steel / black forged metal, blue crystal or energy core, blue emissive cuts, black wrapped grip. Use
controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the item already exists in the mod; the agent must
find the exact current Katana-OP files and replace that item's model/animation/visuals in-place If
the current item already has some functional code, inspect it and preserve any logic not explicitly
replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Blue Air Slash. RMB releases a fast forward blue cutting-wave / wind-blade slash.
The slash travels in front of the player in a clean line, damages every valid enemy it intersects
once, and visually leaves a compressed blue air-separation trail rather than an explosion.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a forward
corridor around 12–16 blocks long and 1.5–2 blocks wide, clipped by solid obstacles.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a forward corridor around 12–16 blocks long and 1.5–2 blocks
wide, clipped by solid obstacles Keep the action bounded, deduplicate targets where necessary and
prevent the action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB releases a
fast forward blue cutting-wave / wind-blade slash. The slash travels in front of the player in a
clean line, damages every valid enemy it intersects once, and visually leaves a compressed blue air-
separation trail rather than an explosion. Prevent accidental duplicate damage, duplicate ore drops,
broken crop logic or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown around 5–8 seconds; normal melee must remain usable during cooldown
If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions unless
the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: a modest fixed durability cost once per successful cast. Apply the cost
using normal item-damage APIs where possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
Opus blue techno-forged style: dark steel / black forged metal, blue crystal or energy core, blue
emissive cuts, black wrapped grip and the ability Blue Air Slash. Use concise purposeful effects
rather than endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Katana-OP and Blue Air Slash (or
the fact that there is no new ability). Keep tooltip language player-facing rather than internal/dev
jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Katana-OP in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Katana-OP. Search for it, verify it in files, and base the
rework on that exact existing item.

END OF PROMPT.
```

---

# Golden Katana — ULTRA-DETAILED MASTER PROMPT

![Golden Katana concept](concept_art/golden_katana.png)

```text
# ITEM: Golden Katana
# Recommended likely registry id: golden_katana
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Golden Katana, golden_katana. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: royal gold Opus/Pantheon-adjacent style: antique bright gold body, black
grip, warm golden glow accents, sacred elite katana presentation. Visual target: a golden long
katana with clean angular blade lines, premium golden frame, black wrapped grip, and noble high-
status warrior silhouette. Keep the weapon elegant, regal and anime-fast. The golden style must feel
premium rather than simply yellow recolor. If concept art is present, treat it as the primary
silhouette/layout reference. If concept art is absent, generate the concept from the provided
description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Golden Katana and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: royal gold Opus/Pantheon-adjacent
style: antique bright gold body, black grip, warm golden glow accents, sacred elite katana
presentation. Use controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the agent must locate the already-existing Golden
Katana item in code/assets and rebuild THAT item's visual implementation, not register a duplicate
If the current item already has some functional code, inspect it and preserve any logic not
explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: ChoCho Sword style special. Implement the special with the same FEEL as the ChoCho
Sword ability from Shindo Life: a flashy aggressive golden-energy katana technique centered on fast
slashing pressure and dramatic anime-style golden strike effects. Preserve the idea and gameplay
feel while implementing it cleanly in the actual Fabric/GeckoLib project.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a short-to-
medium forward offensive technique or chained slash pattern, implemented in a clean bounded area and
never as uncontrolled world destruction.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a short-to-medium forward offensive technique or chained slash
pattern, implemented in a clean bounded area and never as uncontrolled world destruction Keep the
action bounded, deduplicate targets where necessary and prevent the action from turning into
uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. Implement the
special with the same FEEL as the ChoCho Sword ability from Shindo Life: a flashy aggressive golden-
energy katana technique centered on fast slashing pressure and dramatic anime-style golden strike
effects. Preserve the idea and gameplay feel while implementing it cleanly in the actual
Fabric/GeckoLib project. Prevent accidental duplicate damage, duplicate ore drops, broken crop logic
or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown appropriate to a flashy katana technique, while normal melee
remains fully available If the ability is cooldown-gated, that cooldown must not disable unrelated
ordinary actions unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: a fixed ability durability cost once per successful use. Apply the cost
using normal item-damage APIs where possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
royal gold Opus/Pantheon-adjacent style: antique bright gold body, black grip, warm golden glow
accents, sacred elite katana presentation and the ability ChoCho Sword style special. Use concise
purposeful effects rather than endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Golden Katana and ChoCho Sword
style special (or the fact that there is no new ability). Keep tooltip language player-facing rather
than internal/dev jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Golden Katana in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Golden Katana. Search for it, verify it in files, and base
the rework on that exact existing item.

END OF PROMPT.
```

---

# Refined Opus Katana — ULTRA-DETAILED MASTER PROMPT

![Refined Opus Katana concept](concept_art/refined_opus_katana.png)

```text
# ITEM: Refined Opus Katana
# Recommended likely registry id: refined_opus_katana
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Refined Opus Katana, refined_opus_katana. Check lang files, item registration classes,
item model JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-
place; do not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: refined blue-white Opus style: cleaner silver/steel body with bright cyan-
blue core lines, precise engineered elegance. Visual target: a refined luminous blue katana with
pale metallic blade planes, blue core channel, dark wrapped grip and elite upgraded Opus
craftsmanship. This katana should feel like an upgraded cleaner cousin of Katana-OP, with more
precision and less raw brutality. If concept art is present, treat it as the primary
silhouette/layout reference. If concept art is absent, generate the concept from the provided
description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Refined Opus Katana and do not let it drift into
a generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: refined blue-white Opus style:
cleaner silver/steel body with bright cyan-blue core lines, precise engineered elegance. Use
controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. find the exact existing Refined Opus Katana item
and recreate its model/animations in-place If the current item already has some functional code,
inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Circular Air Cut. RMB emits a circular air-blade around the player: a ring-like
outward slash that expands from the wielder, damaging valid enemies in a controlled radius around
the player one time each. It is a clean air-pressure cut, not an explosion.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a bounded
circular area around the player, roughly 4–6 blocks radius with one damage resolution per entity.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a bounded circular area around the player, roughly 4–6 blocks
radius with one damage resolution per entity Keep the action bounded, deduplicate targets where
necessary and prevent the action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB emits a
circular air-blade around the player: a ring-like outward slash that expands from the wielder,
damaging valid enemies in a controlled radius around the player one time each. It is a clean air-
pressure cut, not an explosion. Prevent accidental duplicate damage, duplicate ore drops, broken
crop logic or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown around 6–10 seconds; normal katana combat remains available during
cooldown If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions
unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: a fixed cost once per successful ring slash. Apply the cost using normal
item-damage APIs where possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
refined blue-white Opus style: cleaner silver/steel body with bright cyan-blue core lines, precise
engineered elegance and the ability Circular Air Cut. Use concise purposeful effects rather than
endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Refined Opus Katana and Circular
Air Cut (or the fact that there is no new ability). Keep tooltip language player-facing rather than
internal/dev jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Refined Opus Katana in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Refined Opus Katana. Search for it, verify it in files,
and base the rework on that exact existing item.

END OF PROMPT.
```

---

# Opus Warhammer — ULTRA-DETAILED MASTER PROMPT

![Opus Warhammer concept](concept_art/opus_warhammer.png)

```text
# ITEM: Opus Warhammer
# Recommended likely registry id: opus_warhammer
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Opus Warhammer, opus_warhammer. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: heavy Opus artifact style: dark steel mass, large blue crystal/furnace core,
thick blocky geometry, black wrapped handle. Visual target: a huge square-headed warhammer with dark
segmented metal plates, a bright blue glowing central crystal core, reinforced shaft and a brutal
high-mass silhouette. The slam must feel massively heavy. The head must not float, and the core
should visually pulse during windup and release. If concept art is present, treat it as the primary
silhouette/layout reference. If concept art is absent, generate the concept from the provided
description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Opus Warhammer and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: heavy Opus artifact style: dark steel
mass, large blue crystal/furnace core, thick blocky geometry, black wrapped handle. Use controlled
broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the agent must identify the real existing Opus
Warhammer item files and rebuild that exact item If the current item already has some functional
code, inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Shockwave. RMB slams the hammer into the ground and emits a circular ground
shockwave around the player. Valid nearby enemies are thrown slightly upward / popped into the air
and receive a slowing effect. The shockwave is ground-based, controlled, and never destroys terrain.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a bounded
circular ground radius around the player, around 5–7 blocks, limited to nearby valid entities.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a bounded circular ground radius around the player, around 5–7
blocks, limited to nearby valid entities Keep the action bounded, deduplicate targets where
necessary and prevent the action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB slams the
hammer into the ground and emits a circular ground shockwave around the player. Valid nearby enemies
are thrown slightly upward / popped into the air and receive a slowing effect. The shockwave is
ground-based, controlled, and never destroys terrain. Prevent accidental duplicate damage, duplicate
ore drops, broken crop logic or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown around 8–12 seconds; normal hammer melee must still function during
cooldown If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions
unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: a moderate fixed cost once per successful slam. Apply the cost using
normal item-damage APIs where possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
heavy Opus artifact style: dark steel mass, large blue crystal/furnace core, thick blocky geometry,
black wrapped handle and the ability Shockwave. Use concise purposeful effects rather than endless
particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Opus Warhammer and Shockwave (or
the fact that there is no new ability). Keep tooltip language player-facing rather than internal/dev
jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Opus Warhammer in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Opus Warhammer. Search for it, verify it in files, and
base the rework on that exact existing item.

END OF PROMPT.
```

---

# Opus Pickaxe — ULTRA-DETAILED MASTER PROMPT

![Opus Pickaxe concept](concept_art/opus_pickaxe.png)

```text
# ITEM: Opus Pickaxe
# Recommended likely registry id: opus_pickaxe
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Opus Pickaxe, opus_pickaxe. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: Opus forged-tech mining style: dark steel head, blue crystalline core, sharp
angular pick tips, wrapped shaft. Visual target: a symmetrical blue-tech pickaxe with strong
metallic arms, blue core accents, black handle wrapping and an efficient industrial-elite mining
silhouette. Use proper ore validation, preserve Fortune/Silk Touch where reasonable, and keep the
visual effect blue and crystalline. If concept art is present, treat it as the primary
silhouette/layout reference. If concept art is absent, generate the concept from the provided
description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Opus Pickaxe and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: Opus forged-tech mining style: dark
steel head, blue crystalline core, sharp angular pick tips, wrapped shaft. Use controlled broad
value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. find the existing Opus Pickaxe item and rebuild
that item's visuals/ability implementation in-place If the current item already has some functional
code, inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Azure Vein Resonance. RMB on a valid ore triggers a bounded vein resonance. Blue
energy spreads through the connected ore vein and mines a limited number of connected matching ore
blocks through legitimate server loot logic. The action is bounded, clean, and enchantment-
compatible.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: connected
valid ore blocks from the clicked ore, bounded by a hard count cap like 24–32 blocks and a limited
search radius.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. connected valid ore blocks from the clicked ore, bounded by a
hard count cap like 24–32 blocks and a limited search radius Keep the action bounded, deduplicate
targets where necessary and prevent the action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB on a valid
ore triggers a bounded vein resonance. Blue energy spreads through the connected ore vein and mines
a limited number of connected matching ore blocks through legitimate server loot logic. The action
is bounded, clean, and enchantment-compatible. Prevent accidental duplicate damage, duplicate ore
drops, broken crop logic or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown around 5–8 seconds; ordinary pickaxe mining must continue during
cooldown If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions
unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: durability should scale with successfully mined blocks; do not give 24+
blocks for one durability point. Apply the cost using normal item-damage APIs where possible so
Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
Opus forged-tech mining style: dark steel head, blue crystalline core, sharp angular pick tips,
wrapped shaft and the ability Azure Vein Resonance. Use concise purposeful effects rather than
endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Opus Pickaxe and Azure Vein
Resonance (or the fact that there is no new ability). Keep tooltip language player-facing rather
than internal/dev jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Opus Pickaxe in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Opus Pickaxe. Search for it, verify it in files, and base
the rework on that exact existing item.

END OF PROMPT.
```

---

# Opus Axe — ULTRA-DETAILED MASTER PROMPT

![Opus Axe concept](concept_art/opus_axe.png)

```text
# ITEM: Opus Axe
# Recommended likely registry id: opus_axe
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Opus Axe, opus_axe. Check lang files, item registration classes, item model JSONs,
textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do not
create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: Opus battle-axe style: dark steel body, blue crystal core, angular double-
sided head, tech-forged elite weapon language. Visual target: a broad double-sided or broad-head
blue Opus axe with crystalline blue centerpiece, angular blade panels and a long wrapped grip. The
axe must be oriented correctly in-hand and not held backwards. Emphasize clean head thickness and
blue crystal focal point. If concept art is present, treat it as the primary silhouette/layout
reference. If concept art is absent, generate the concept from the provided description only while
staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Opus Axe and do not let it drift into a generic
sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: Opus battle-axe style: dark steel
body, blue crystal core, angular double-sided head, tech-forged elite weapon language. Use
controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the agent must search for Opus Axe in the mod files
and edit the existing item, not add a copy If the current item already has some functional code,
inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Crosscut Arc. RMB sends a short-range blue crescent arc forward. It hits valid
enemies in front of the player in a controlled fan or corridor, applies one clean damage instance
per target, and slightly knocks them back. No terrain destruction.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a bounded
forward arc or corridor around 8–12 blocks long, clipped by terrain and deduplicated per entity.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a bounded forward arc or corridor around 8–12 blocks long,
clipped by terrain and deduplicated per entity Keep the action bounded, deduplicate targets where
necessary and prevent the action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB sends a
short-range blue crescent arc forward. It hits valid enemies in front of the player in a controlled
fan or corridor, applies one clean damage instance per target, and slightly knocks them back. No
terrain destruction. Prevent accidental duplicate damage, duplicate ore drops, broken crop logic or
double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a named cooldown around 6–10 seconds; normal melee and axe block interactions remain
usable If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions
unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: a fixed ability cost once per use. Apply the cost using normal item-damage
APIs where possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
Opus battle-axe style: dark steel body, blue crystal core, angular double-sided head, tech-forged
elite weapon language and the ability Crosscut Arc. Use concise purposeful effects rather than
endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Opus Axe and Crosscut Arc (or
the fact that there is no new ability). Keep tooltip language player-facing rather than internal/dev
jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Opus Axe in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Opus Axe. Search for it, verify it in files, and base the
rework on that exact existing item.

END OF PROMPT.
```

---

# Opus Hoe — ULTRA-DETAILED MASTER PROMPT

![Opus Hoe concept](concept_art/opus_hoe.png)

```text
# ITEM: Opus Hoe
# Recommended likely registry id: opus_hoe
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Opus Hoe, opus_hoe. Check lang files, item registration classes, item model JSONs,
textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do not
create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: Opus utility style: dark steel with blue energy channel, compact precise
farming head and wrapped handle. Visual target: a compact blue-tech hoe with a sleek angular head,
dark metal body, blue energy inset and a practical but premium silhouette. The prompt must
explicitly separate soil tilling path and growth path so cooldown never disables normal hoe use. If
concept art is present, treat it as the primary silhouette/layout reference. If concept art is
absent, generate the concept from the provided description only while staying consistent with the
mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Opus Hoe and do not let it drift into a generic
sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: Opus utility style: dark steel with
blue energy channel, compact precise farming head and wrapped handle. Use controlled broad value
shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. find the exact existing Opus Hoe and rework that
item in-place If the current item already has some functional code, inspect it and preserve any
logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Growth Lattice. Ordinary tilling is intrinsically upgraded to 3x3 on valid soil.
RMB/context-use on a planted crop triggers Growth Lattice: a bounded blue energy pulse that
instantly matures valid crops in a controlled area. The growth cooldown must never block ordinary
3x3 tilling.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: normal tilling
= exact 3x3 same-Y soil area; Growth Lattice = bounded crop area such as 3x3 or 5x5 around the
clicked crop, valid growable planted crops only.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. normal tilling = exact 3x3 same-Y soil area; Growth Lattice =
bounded crop area such as 3x3 or 5x5 around the clicked crop, valid growable planted crops only Keep
the action bounded, deduplicate targets where necessary and prevent the action from turning into
uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. Ordinary
tilling is intrinsically upgraded to 3x3 on valid soil. RMB/context-use on a planted crop triggers
Growth Lattice: a bounded blue energy pulse that instantly matures valid crops in a controlled area.
The growth cooldown must never block ordinary 3x3 tilling. Prevent accidental duplicate damage,
duplicate ore drops, broken crop logic or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: cooldown applies only to the crop-growth action; ordinary 3x3 tilling must remain
fully usable at all times If the ability is cooldown-gated, that cooldown must not disable unrelated
ordinary actions unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: 3x3 tilling costs durability per successfully tilled block; crop growth
uses a small fixed or per-successful-crop cost. Apply the cost using normal item-damage APIs where
possible so Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
Opus utility style: dark steel with blue energy channel, compact precise farming head and wrapped
handle and the ability Growth Lattice. Use concise purposeful effects rather than endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Opus Hoe and Growth Lattice (or
the fact that there is no new ability). Keep tooltip language player-facing rather than internal/dev
jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Opus Hoe in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Opus Hoe. Search for it, verify it in files, and base the
rework on that exact existing item.

END OF PROMPT.
```

---

# Opus Shovel — ULTRA-DETAILED MASTER PROMPT

![Opus Shovel concept](concept_art/opus_shovel.png)

```text
# ITEM: Opus Shovel
# Recommended likely registry id: opus_shovel
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Opus Shovel, opus_shovel. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: Opus utility excavation style: dark steel head, blue energy strip, angular
spade form and wrapped handle. Visual target: a compact but strong blue-tech shovel with angular
spade head, central blue inset, dark steel frame and black grip. The shovel head must look like a
shovel, not a shield or hammer. Keep the effect precise and useful. If concept art is present, treat
it as the primary silhouette/layout reference. If concept art is absent, generate the concept from
the provided description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Opus Shovel and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: Opus utility excavation style: dark
steel head, blue energy strip, angular spade form and wrapped handle. Use controlled broad value
shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the agent must locate the existing Opus Shovel item
and recreate that exact item's model/animation/ability implementation If the current item already
has some functional code, inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: Prism Trench. RMB on a valid shovel block excavates a precise 3x3x1 plane based on
the clicked face. Only legitimate shovel-mineable blocks are affected. The action is clean, bounded,
and respects real drops and durability.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: a face-
oriented 3x3x1 plane centered on the clicked block, with per-block validation.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. a face-oriented 3x3x1 plane centered on the clicked block, with
per-block validation Keep the action bounded, deduplicate targets where necessary and prevent the
action from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. RMB on a valid
shovel block excavates a precise 3x3x1 plane based on the clicked face. Only legitimate shovel-
mineable blocks are affected. The action is clean, bounded, and respects real drops and durability.
Prevent accidental duplicate damage, duplicate ore drops, broken crop logic or double execution
caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: a short named cooldown if balance needs it; ordinary single-block shovel use must
remain available during cooldown If the ability is cooldown-gated, that cooldown must not disable
unrelated ordinary actions unless the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: durability should scale with successful block breaks and stop if the tool
breaks. Apply the cost using normal item-damage APIs where possible so Unbreaking/Mending/creative
behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
Opus utility excavation style: dark steel head, blue energy strip, angular spade form and wrapped
handle and the ability Prism Trench. Use concise purposeful effects rather than endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Opus Shovel and Prism Trench (or
the fact that there is no new ability). Keep tooltip language player-facing rather than internal/dev
jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Opus Shovel in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Opus Shovel. Search for it, verify it in files, and base
the rework on that exact existing item.

END OF PROMPT.
```

---

## Part II — Existing katanas without concept art (concept + model + animations from description)

# Steel Katana — ULTRA-DETAILED MASTER PROMPT

```text
# ITEM: Steel Katana
# Recommended likely registry id: steel_katana
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Steel Katana, steel_katana. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: traditional Japanese steel katana style: polished steel blade, classic tsuba,
wrapped tsuka, simple respectable craftsmanship. Visual target: a shorter katana in a classic
Japanese style with a polished steel blade, modest guard, wrapped handle and disciplined authentic
proportions. Make it a shorter katana / wakizashi-like profile if appropriate, elegant, practical
and authentic, without unnecessary fantasy excess. If concept art is present, treat it as the
primary silhouette/layout reference. If concept art is absent, generate the concept from the
provided description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Steel Katana and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: traditional Japanese steel katana
style: polished steel blade, classic tsuba, wrapped tsuka, simple respectable craftsmanship. Use
controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. the item exists in the mod but has no concept art
here. The agent must find Steel Katana in the files and create its visual concept/model/animations
from this description only, preserving existing logic. If the current item already has some
functional code, inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: No new ability. Do not invent a new special ability unless the existing item already
has one in code. The focus here is concept creation from text, model creation and clean katana
animations while preserving the mod's existing functionality.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: no new special
target rules unless the existing code already defines them.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. no new special target rules unless the existing code already
defines them Keep the action bounded, deduplicate targets where necessary and prevent the action
from turning into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. Do not invent a
new special ability unless the existing item already has one in code. The focus here is concept
creation from text, model creation and clean katana animations while preserving the mod's existing
functionality. Prevent accidental duplicate damage, duplicate ore drops, broken crop logic or double
execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: no new cooldown system should be introduced unless the existing item already has one
If the ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions unless
the design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: preserve existing durability/logic; this request is mainly
concept/model/animation. Apply the cost using normal item-damage APIs where possible so
Unbreaking/Mending/creative behavior remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
traditional Japanese steel katana style: polished steel blade, classic tsuba, wrapped tsuka, simple
respectable craftsmanship and the ability No new ability. Use concise purposeful effects rather than
endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Steel Katana and No new ability
(or the fact that there is no new ability). Keep tooltip language player-facing rather than
internal/dev jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Steel Katana in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Steel Katana. Search for it, verify it in files, and base
the rework on that exact existing item.

END OF PROMPT.
```

---

# Long Katana — ULTRA-DETAILED MASTER PROMPT

```text
# ITEM: Long Katana
# Recommended likely registry id: long_katana
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench modeler, low-poly item artist, animator, gameplay programmer, VFX/sound designer and QA engineer.

====================================================================================
1. PROJECT AUDIT AND EXACT ITEM DISCOVERY
====================================================================================
Inspect the actual project first: build.gradle, gradle.properties, fabric.mod.json, Yarn mappings,
GeckoLib dependency, ModItems, existing model/renderer classes, sound/particle registries, client
initializer, item groups, tool materials, abilities, cooldown systems and any already-working
animated items. Determine the exact API and project structure before changing anything.

====================================================================================
2. LOCATE THE REAL EXISTING ITEM FILES
====================================================================================
Search the codebase and resources for the REAL existing item, using the in-game name and probable
identifiers: Long Katana, long_katana. Check lang files, item registration classes, item model
JSONs, textures, GeckoLib geo/animation files and renderers. Rebuild THAT exact item in-place; do
not create a new item entry.

====================================================================================
3. CONCEPT / STYLE ANALYSIS
====================================================================================
Use this style target: traditional long Japanese katana / nodachi-influenced style: longer blade,
refined curvature, wrapped handle, disciplined elegance. Visual target: a longer katana in a
Japanese style with an elongated blade, refined point, classic tsuba, wrapped handle and a graceful
elite swordsman silhouette. This should be visibly longer and more elegant than Steel Katana, but
still remain rooted in traditional Japanese weapon design. If concept art is present, treat it as
the primary silhouette/layout reference. If concept art is absent, generate the concept from the
provided description only while staying consistent with the mod's existing world.

====================================================================================
4. SILHOUETTE AND IDENTITY LOCK
====================================================================================
Lock the silhouette before detail work. The item must be recognizable in flat color from normal
gameplay distance. Preserve the correct identity of Long Katana and do not let it drift into a
generic sword/axe/tool of another class.

====================================================================================
5. OVERALL PROPORTIONS AND SCALE
====================================================================================
Establish sensible Minecraft scale and proportions. Compare the final size with the player's
hand/body and with other modded tools. The item can be premium and slightly oversized, but must
remain usable in first person, readable in inventory, and believable relative to the rest of the
set.

====================================================================================
6. PRIMARY GEOMETRY BLOCKOUT
====================================================================================
Create a primary blockout with only the major masses first: main blade/head/working part,
guard/socket/core, handle/grip, pommel. Validate orientation and working direction before adding
small details.

====================================================================================
7. SECONDARY STRUCTURAL GEOMETRY
====================================================================================
Add secondary structure such as segmented plates, edge frames, crystal housings, collars, recessed
panels, spine ridges, sockets and other architecture that supports the main form. All important
pieces must connect physically and not float.

====================================================================================
8. SIDE PROFILE AND REAL THICKNESS
====================================================================================
Give the item real 3D thickness from the side and 3/4 views. Separate structural body thickness from
thinner cutting/working edges where appropriate. Avoid flat-card geometry.

====================================================================================
9. TIPS, EDGES, BLADES AND WORKING FACES
====================================================================================
Pay special attention to tips, edges, the working face and orientation. The tip or striking edge
must look clean, centered and intentional. The item must not appear backward in the player's hand,
and no tool head should be accidentally mirrored or reversed.

====================================================================================
10. MATERIAL HIERARCHY
====================================================================================
Separate the material families clearly through both geometry and values: structural body, accent
lines/frames, energy channels or cores, and grip materials. The object must remain readable even in
dark scenes.

====================================================================================
11. PRIMARY MATERIAL RENDERING
====================================================================================
Render the primary material in a way appropriate to the style: traditional long Japanese katana /
nodachi-influenced style: longer blade, refined curvature, wrapped handle, disciplined elegance. Use
controlled broad value shapes rather than noisy textures.

====================================================================================
12. ACCENT MATERIAL / GLOW / CRYSTALS / CORES
====================================================================================
Accent material, crystals, glowing lines or cores must be modeled and textured as focal points.
Bright glow should remain controlled and selective; do not turn the entire item into fullbright
neon.

====================================================================================
13. GRIP / HANDLE / WRAPPING
====================================================================================
Handle / grip / wrapping must read clearly as the graspable area. Use wrapped leather, cord, or
another suitable material with enough contrast that the player's grip location is visually obvious.

====================================================================================
14. SURFACE WEAR AND FINISHING
====================================================================================
Add disciplined wear and finish only where appropriate: small edge highlights, mild scuffs, refined
polish, or subtle heat/weathering depending on the style. Do not bury the asset under random noise.

====================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
====================================================================================
Use a texture size consistent with the mod's asset quality, preferably 128x128 or 256x256 depending
on the set standard. Keep texel density reasonable and consistent.

====================================================================================
16. UV LAYOUT AND PADDING
====================================================================================
Lay out UVs logically with enough padding to avoid bleeding. Mirror only where it does not damage
the design. Preserve extra resolution for focal faces, cores and blade or tool-head surfaces.

====================================================================================
17. TEXTURE PAINTING RULES
====================================================================================
Texture painting must remain Minecraft-compatible: crisp, readable, stylized, not photorealistic.
Use pixel-art shading, clean crack/core gradients and strong edge readability.

====================================================================================
18. GEOMETRY BUDGET AND OPTIMIZATION
====================================================================================
Use geometry for the silhouette, major bevels, head/blade thickness, guards/cores and other large
forms. Use textures for micro lines, minor engravings and small wear. Remove hidden duplicate faces
and zero-size cubes.

====================================================================================
19. GECKOLIB BONE HIERARCHY
====================================================================================
Create a practical GeckoLib hierarchy. At minimum provide root, main item, major head/blade or tool
working part, handle/grip, pommel, and any necessary FX bones. Do not create pointless bones for
every tiny cube.

====================================================================================
20. PIVOT PLACEMENT AND ORIGIN SETUP
====================================================================================
Set pivots at real joints and choose a stable origin/reference point so held transforms and
animations behave cleanly. Wrong pivots will create broken swings and backward-looking items.

====================================================================================
21. FIRST-PERSON TRANSFORMS
====================================================================================
Tune first-person right-hand transforms carefully. The hand must grip the item naturally, the
functional edge must point correctly, the key focal area must remain visible, and the asset must not
cover the crosshair excessively.

====================================================================================
22. OFFHAND AND THIRD-PERSON TRANSFORMS
====================================================================================
Verify offhand and third-person presentation independently. Do not assume mirroring fixes itself.
The tool/weapon must still face the correct direction, and the player should hold the real grip
instead of empty air.

====================================================================================
23. GUI / DROPPED / ITEM FRAME PRESENTATION
====================================================================================
Create polished transforms for inventory GUI, dropped item and item frame. The whole silhouette must
fit the slot, remain readable on the ground and not clip absurdly into frames/walls.

====================================================================================
24. IDLE ANIMATION
====================================================================================
Idle animation should be subtle and loop cleanly. Small energy/core pulse or tiny rigid breathing
motion is enough. Do not let a held item wobble wildly.

====================================================================================
25. EQUIP ANIMATION
====================================================================================
Equip animation should be short and responsive: slight raise, tiny overshoot and settle, with
perhaps a brief pulse in the accent/core area.

====================================================================================
26. ATTACK / WORK ANIMATION
====================================================================================
Create a primary attack/work animation suited to the item class: slash for katanas, heavy swing/slam
for hammer/axe, mining stroke for pickaxe, digging for shovel, till motion for hoe. Respect the feel
of the class and avoid overanimating the root.

====================================================================================
27. SECONDARY MOTION AND INERTIA
====================================================================================
Add rigid secondary inertia: the handle/hand leads, the heavier head or blade lags slightly and
catches up, then settles. Never bend the whole weapon/tool like rubber.

====================================================================================
28. ANIMATION CONTROLLER RULES
====================================================================================
Use clean animation controller priorities so special ability > attack/work > equip > idle. Verify
the actual GeckoLib version's triggerable animation API in the project and do not paste syntax from
another version blindly.

====================================================================================
29. PRESERVE OR INSPECT EXISTING GAMEPLAY LOGIC
====================================================================================
Preserve the base item logic already in the mod. find the existing Long Katana item and remake THAT
model/animation set from this textual description If the current item already has some functional
code, inspect it and preserve any logic not explicitly replaced by this prompt.

====================================================================================
30. UNIQUE ABILITY OVERVIEW
====================================================================================
UNIQUE ABILITY: No new ability. Do not invent a new special ability unless the existing item already
has one in code. The focus is concept generation from the description, longer-blade modeling and
appropriate animations while preserving existing functionality.

====================================================================================
31. ABILITY ACTIVATION AND VALIDATION
====================================================================================
Ability activation must be deterministic and context-aware. Validate item state, hand/context,
cooldown, relevant target conditions and server-side legality before triggering the ability. If
invalid, do not consume durability or play the full successful cast. Targeting rules: no new special
target rules unless they already exist in code.

====================================================================================
32. ABILITY TARGETING / AREA RULES
====================================================================================
Implement precise target/area rules. no new special target rules unless they already exist in code
Keep the action bounded, deduplicate targets where necessary and prevent the action from turning
into uncontrolled world-scale logic.

====================================================================================
33. SERVER AUTHORITY AND STATE FLOW
====================================================================================
All real gameplay effects must be server-authoritative. Use a clean state flow: validate -> commit
-> resolve -> cleanup/cooldown. The client may only display visuals or harmless prediction; it must
not decide real damage, block changes or crop growth.

====================================================================================
34. ABILITY GAMEPLAY RESOLUTION
====================================================================================
Gameplay resolution must match the ability promise and remain internally consistent. Do not invent a
new special ability unless the existing item already has one in code. The focus is concept
generation from the description, longer-blade modeling and appropriate animations while preserving
existing functionality. Prevent accidental duplicate damage, duplicate ore drops, broken crop logic
or double execution caused by client/server overlap.

====================================================================================
35. COOLDOWN RULES
====================================================================================
Cooldown rules: do not add a cooldown system unless the existing item already uses one If the
ability is cooldown-gated, that cooldown must not disable unrelated ordinary actions unless the
design explicitly requires it.

====================================================================================
36. DURABILITY / RESOURCE COST
====================================================================================
Durability/resource cost: preserve existing durability/logic; prioritize visual/animation work.
Apply the cost using normal item-damage APIs where possible so Unbreaking/Mending/creative behavior
remain sane.

====================================================================================
37. SPECIAL VFX SEQUENCE
====================================================================================
Create a staged special VFX sequence that communicates what is happening. It should fit the style
traditional long Japanese katana / nodachi-influenced style: longer blade, refined curvature,
wrapped handle, disciplined elegance and the ability No new ability. Use concise purposeful effects
rather than endless particles.

====================================================================================
38. SPECIAL SOUND DESIGN
====================================================================================
Design a sound package that supports the ability: activation cue, release/impact cue and any short
aftereffect. Avoid sound spam and keep the sound readable in normal gameplay.

====================================================================================
39. NETWORKING AND MULTIPLAYER BEHAVIOR
====================================================================================
Use efficient networking and multiplayer-safe logic. Nearby players should see the important world-
visible effects. Every player and every cast/operation must keep separate state; no shared global
'current ability' variables.

====================================================================================
40. NORMAL-USE VFX AND SOUNDS
====================================================================================
Normal use also deserves restrained feedback. Ordinary swings, mining strokes, digs or tills may
have small trails, core pulses, sparks or soil particles, plus one clean sound layer, but should
remain much less flashy than the special ability.

====================================================================================
41. ENVIRONMENTAL AND WORLD SAFETY
====================================================================================
The asset and ability must be safe for the world. Do not create uncontrolled explosions, griefing,
accidental fire/lava placement, random structure damage or unintended block replacement unless
explicitly required—and it is NOT required here.

====================================================================================
42. PERFORMANCE SAFEGUARDS
====================================================================================
Keep performance bounded. No unbounded searches, no whole-world scans, no Thread.sleep, no long-
lived garbage state, and no packet-per-particle networking. Use hard caps for entity counts, ore
counts, crop counts, or area sizes where relevant.

====================================================================================
43. INVALID-USE AND NO-OP BEHAVIOR
====================================================================================
Invalid/no-op behavior must be cheap and clean. If the player uses the item during cooldown, on an
invalid block, on a mature crop, or in another no-op context, avoid the full success effect and do
not waste durability unnecessarily.

====================================================================================
44. EDGE CASES AND FAILURE RECOVERY
====================================================================================
Handle edge cases explicitly: target death/despawn, tool breaking mid-action, chunk boundaries,
protection checks, unloaded chunks, offhand use, creative mode, disconnects, dimension changes,
blocked line of sight and multiplayer latency.

====================================================================================
45. REQUIRED FILES AND RESOURCES
====================================================================================
Create or modify all required files for the EXISTING item: geo, animation, texture, item model JSON,
lang entries, renderer/model classes, ability/helper classes, particles/sounds if needed, always
under the actual namespace and file structure used by the project.

====================================================================================
46. LOCALIZATION AND TOOLTIP
====================================================================================
Add concise localization and tooltip text that clearly communicates Long Katana and No new ability
(or the fact that there is no new ability). Keep tooltip language player-facing rather than
internal/dev jargon.

====================================================================================
47. CODE ARCHITECTURE AND CLASS BOUNDARIES
====================================================================================
Keep code architecture maintainable. Use a focused item class plus small helpers where needed
instead of one giant unreadable class. Reuse shared utilities already present in the mod.

====================================================================================
48. MODEL GAPS / Z-FIGHTING / SEAM QA
====================================================================================
Inspect and fix model gaps, open seams, accidental holes, mirrored offsets, missing side faces and
z-fighting. Distinguish deliberate recesses from broken geometry. The final model must not have
obvious unintended cracks between pieces.

====================================================================================
49. GAMEPLAY TEST MATRIX
====================================================================================
Gameplay-test the item comprehensively: normal attacks/work, special ability, cooldown, low
durability, enchantments, protection/terrain interactions, invalid targets, repeated use,
multiplayer and any context-specific mechanics.

====================================================================================
50. VISUAL TEST MATRIX
====================================================================================
Visual-test the item from front/back/side/top/3/4, first person at several FOVs, offhand, third
person, GUI, ground and item frame. Confirm the silhouette, orientation, scale, animation and
readability are correct.

====================================================================================
51. BUILD / RUNCLIENT VALIDATION
====================================================================================
Build with the real Gradle wrapper and run the client if possible. Read and fix compile errors,
resource errors, animation mismatches, missing textures, and runtime issues. Do not claim success
with an untested asset.

====================================================================================
52. DEFINITION OF DONE
====================================================================================
Definition of Done: the item matches its concept/description, the model is clean, transforms are
correct, animations work, existing gameplay is preserved, the specified ability behaves correctly
and safely, no duplicate item was created, and the build/runtime validation succeeds.

====================================================================================
53. HARD RULE: RECREATE THE EXISTING ITEM IN-PLACE
====================================================================================
HARD RULE: you are not inventing a brand-new unrelated item. You must recreate the existing mod item
named Long Katana in-place.

====================================================================================
54. HARD RULE: DO NOT CREATE DUPLICATES
====================================================================================
HARD RULE: do not register duplicates, placeholder clones, temporary copies or new parallel items
with slightly different IDs. Rework the existing item.

====================================================================================
55. HARD RULE: RESPECT FABRIC 1.20.1 + GECKOLIB
====================================================================================
HARD RULE: respect the actual environment—Minecraft Fabric 1.20.1, the mod's real dependencies and
the installed GeckoLib API. No Forge code, no 1.21 snippets, no imaginary helper methods.

====================================================================================
56. HARD RULE: USE THE EXACT NAMED ITEM
====================================================================================
HARD RULE: the exact named target item is Long Katana. Search for it, verify it in files, and base
the rework on that exact existing item.

END OF PROMPT.
```

---

## Part III — Visual-only existing items

# Shade Silk — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Shade Silk
# Recommended likely registry id: shade_silk
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Shade Silk' and the likely id
'shade_silk'. Check registrations, lang files, item model JSONs, textures and any renderer/model
classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Dark Forest. Dark Forest style = dark woods, thorny roots, shadow-purple primary
accent, moonlit magical glow, organic mystical mood. Item description: a dark mystical silk material
from the Dark Forest, soft but sinister, dark charcoal-to-purple fibers with faint moonlit sheen

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Dark Forest style = dark woods, thorny roots, shadow-purple
primary accent, moonlit magical glow, organic mystical mood. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Dark Forest style = dark
woods, thorny roots, shadow-purple primary accent, moonlit magical glow, organic mystical mood. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Shade Silk', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Moonwing membrane — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Moonwing membrane
# Recommended likely registry id: moonwing_membrane
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Moonwing membrane' and the
likely id 'moonwing_membrane'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Dark Forest. Dark Forest style = dark woods, thorny roots, shadow-purple primary
accent, moonlit magical glow, organic mystical mood. Item description: a thin nocturnal membrane or
wing fragment with dark-violet translucency, organic veining and lunar glow accents

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Dark Forest style = dark woods, thorny roots, shadow-purple
primary accent, moonlit magical glow, organic mystical mood. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Dark Forest style = dark
woods, thorny roots, shadow-purple primary accent, moonlit magical glow, organic mystical mood. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Moonwing membrane', not a duplicate, placeholder or new
registry entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Moon flower heart — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Moon flower heart
# Recommended likely registry id: moon_flower_heart
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Moon flower heart' and the
likely id 'moon_flower_heart'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Dark Forest. Dark Forest style = dark woods, thorny roots, shadow-purple primary
accent, moonlit magical glow, organic mystical mood. Item description: the glowing core-heart of a
moon flower, deep purple petals or organic casing around a luminous magical center

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Dark Forest style = dark woods, thorny roots, shadow-purple
primary accent, moonlit magical glow, organic mystical mood. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Dark Forest style = dark
woods, thorny roots, shadow-purple primary accent, moonlit magical glow, organic mystical mood. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Moon flower heart', not a duplicate, placeholder or new
registry entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Rootbound Eye — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Rootbound Eye
# Recommended likely registry id: rootbound_eye
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Rootbound Eye' and the likely id
'rootbound_eye'. Check registrations, lang files, item model JSONs, textures and any renderer/model
classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Dark Forest. Dark Forest style = dark woods, thorny roots, shadow-purple primary
accent, moonlit magical glow, organic mystical mood. Item description: an eerie eye wrapped in roots
and briar, dark organic mass with purple supernatural focal iris

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Dark Forest style = dark woods, thorny roots, shadow-purple
primary accent, moonlit magical glow, organic mystical mood. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Dark Forest style = dark
woods, thorny roots, shadow-purple primary accent, moonlit magical glow, organic mystical mood. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Rootbound Eye', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Briarweave — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Briarweave
# Recommended likely registry id: briarweave
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Briarweave' and the likely id
'briarweave'. Check registrations, lang files, item model JSONs, textures and any renderer/model
classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Dark Forest. Dark Forest style = dark woods, thorny roots, shadow-purple primary
accent, moonlit magical glow, organic mystical mood. Item description: dark forest bark or woven
root-bark material, thorny woody texture with muted purple-magical hints

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Dark Forest style = dark woods, thorny roots, shadow-purple
primary accent, moonlit magical glow, organic mystical mood. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Dark Forest style = dark
woods, thorny roots, shadow-purple primary accent, moonlit magical glow, organic mystical mood. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Briarweave', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Paradise Fruit — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Paradise Fruit
# Recommended likely registry id: paradise_fruit
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Paradise Fruit' and the likely
id 'paradise_fruit'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: a divine paradise apple or
fruit: pale, golden, marble-clean and holy, with ruby or halo-like accents

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Paradise Fruit', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Cloud Fleece — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Cloud Fleece
# Recommended likely registry id: cloud_fleece
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Cloud Fleece' and the likely id
'cloud_fleece'. Check registrations, lang files, item model JSONs, textures and any renderer/model
classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: a heavenly fleece or wool-
like material, soft cloud-white with subtle gold warmth

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Cloud Fleece', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Aerie Bronze Ingot — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Aerie Bronze Ingot
# Recommended likely registry id: aerie_bronze_ingot
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Aerie Bronze Ingot' and the
likely id 'aerie_bronze_ingot'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: a refined bronze ingot from
the aerial paradise culture, clean warm bronze with premium sacred finish

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Aerie Bronze Ingot', not a duplicate, placeholder or new
registry entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Seraphic Pinions — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Seraphic Pinions
# Recommended likely registry id: seraphic_pinions
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Seraphic Pinions' and the likely
id 'seraphic_pinions'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: holy wing feathers or wing
fragments, bright ivory-white with subtle gold edges and celestial purity

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Seraphic Pinions', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Ruby Halo Shard — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Ruby Halo Shard
# Recommended likely registry id: ruby_halo_shard
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Ruby Halo Shard' and the likely
id 'ruby_halo_shard'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: a fragment of a sacred ruby
halo, red gemstone with fine gold celestial framing

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Ruby Halo Shard', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Paradise Sapling — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Paradise Sapling
# Recommended likely registry id: paradise_sapling
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Paradise Sapling' and the likely
id 'paradise_sapling'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Paradise / Pantheon. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Item description: a sapling of a paradise
tree, elegant ivory-gold trunk and leaves with sacred bright accents

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Paradise / Pantheon style = ivory marble, sacred gold, ruby
accents, divine cleanliness, airy celestial nobility. Keep values readable and use accents
sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Paradise / Pantheon
style = ivory marble, sacred gold, ruby accents, divine cleanliness, airy celestial nobility. The
item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Paradise Sapling', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Ember Kapok Sapling — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Ember Kapok Sapling
# Recommended likely registry id: ember_kapok_sapling
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Ember Kapok Sapling' and the
likely id 'ember_kapok_sapling'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Hell / Infernal. Hell / Infernal style = charred black material, ember-orange glow,
volcanic cracks, infernal heat and controlled demonic intensity. Item description: a sapling of an
infernal kapok tree: charred dark bark, ember-orange glow, hellish seedling presence

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Hell / Infernal style = charred black material, ember-orange
glow, volcanic cracks, infernal heat and controlled demonic intensity. Keep values readable and use
accents sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Hell / Infernal style =
charred black material, ember-orange glow, volcanic cracks, infernal heat and controlled demonic
intensity. The item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Ember Kapok Sapling', not a duplicate, placeholder or new
registry entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---

# Ember Kapok Pod — VISUAL-ONLY MASTER PROMPT

```text
# ITEM: Ember Kapok Pod
# Recommended likely registry id: ember_kapok_pod
# VISUAL-ONLY REWORK / DO NOT TOUCH GAMEPLAY
# Minecraft Fabric 1.20.1

You are working on an item that already exists in the mod. This task is ONLY about the visual side: model / texture / item presentation. Functional code already exists and must remain intact.

==============================================================================
1. FIND THE EXACT EXISTING ITEM IN THE PROJECT
==============================================================================
Find the exact existing item in code/assets using the in-game name 'Ember Kapok Pod' and the likely
id 'ember_kapok_pod'. Check registrations, lang files, item model JSONs, textures and any
renderer/model classes.

==============================================================================
2. INSPECT THE VISUAL PIPELINE ALREADY USED BY THE MOD
==============================================================================
Inspect how the mod currently renders normal item assets. Determine whether this item should stay a
lightweight 2D item texture, use a custom item model, or use a 3D Blockbench/GeckoLib item style
already present in the project.

==============================================================================
3. DEFINE THE VISUAL FAMILY AND ROLE
==============================================================================
Visual family: Hell / Infernal. Hell / Infernal style = charred black material, ember-orange glow,
volcanic cracks, infernal heat and controlled demonic intensity. Item description: a lava-fruit /
infernal pod with charred shell and molten orange-red interior glow

==============================================================================
4. SILHOUETTE AND RECOGNIZABILITY
==============================================================================
Lock a readable silhouette and identity. Even a small ingredient item must be immediately
recognizable in inventory and in hand. Avoid clutter that destroys icon readability.

==============================================================================
5. OVERALL PROPORTIONS AND SCALE
==============================================================================
Set proportions and scale appropriately for an item icon / held item / dropped item. Keep the object
large enough to be identifiable but not absurdly oversized.

==============================================================================
6. PRIMARY SHAPE / BLOCKOUT
==============================================================================
Create a primary shape blockout or main item silhouette first. If the asset stays 2D, block out the
icon composition. If the asset uses 3D geometry, establish the main mass before adding small
decoration.

==============================================================================
7. SECONDARY FORMS AND SMALL DETAILS
==============================================================================
Add secondary details that reinforce the theme: fibers, petals, bark seams, halo framing, feather
barbs, root wraps, ember cracks, berry/pod segmentation, or other family-appropriate detail.

==============================================================================
8. REAL THICKNESS / 3D DEPTH WHERE APPROPRIATE
==============================================================================
Use real thickness or 3D depth only where it improves readability and matches the project's
rendering style. Do not force every simple ingredient into heavy geometry if the mod normally uses
flatter item assets.

==============================================================================
9. MATERIAL PALETTE
==============================================================================
Material palette must fit the family. Hell / Infernal style = charred black material, ember-orange
glow, volcanic cracks, infernal heat and controlled demonic intensity. Keep values readable and use
accents sparingly.

==============================================================================
10. MAIN TEXTURE TREATMENT
==============================================================================
Texture treatment must be crisp and stylized for Minecraft. Use readable shapes, controlled
highlights and restrained noise. Do not paint photorealistic textures.

==============================================================================
11. ACCENT DETAILS AND FOCAL POINTS
==============================================================================
Choose one clear focal point—for example the eye iris, ruby shard, glowing heart center, fruit
highlight, feather tip, bark thorn cluster or ember core—so the item is interesting at a glance.

==============================================================================
12. TEXTURE SIZE AND UV LAYOUT
==============================================================================
Use a texture size appropriate to the mod's pipeline, often 32x32, 64x64 or 128x128 depending on
whether the asset is simple or 3D. Keep UVs/padding clean if a custom model is used.

==============================================================================
13. PIXEL-ART / TEXTURE PAINTING RULES
==============================================================================
Texture painting should emphasize clean stylized forms, not noisy filters. Use concise shading and
color ramps suited to the family.

==============================================================================
14. GEOMETRY BUDGET AND OPTIMIZATION
==============================================================================
Keep geometry efficient. If the item is better as a texture/icon, do that. If a small custom model
is justified, use only enough geometry for silhouette, thickness and focal detail.

==============================================================================
15. TRANSFORMS FOR GUI, HELD, DROPPED AND FRAME
==============================================================================
Verify how the item appears in GUI, in the player's hand, as a dropped entity and in an item frame.
Adjust transforms so the object remains readable in all display contexts.

==============================================================================
16. OPTIONAL IDLE / DISPLAY ANIMATION ONLY IF THE PROJECT ALREADY SUPPORTS IT
==============================================================================
Only add idle/display animation if the mod already supports subtle item animations or if a minimal
animation significantly improves the item. For simple ingredients, static visuals are usually
better.

==============================================================================
17. KEEP GAMEPLAY AND ITEM LOGIC UNTOUCHED
==============================================================================
Keep gameplay and item logic untouched. Do not add new abilities, consume behavior, growth logic,
drops or hidden mechanics as part of this task.

==============================================================================
18. DO NOT CHANGE REGISTRY IDS, CLASSES OR FUNCTIONAL CODE
==============================================================================
Do not change registry IDs, base item classes, use actions, recipe links, tags or functional code
unless a tiny unavoidable visual pipeline edit requires it.

==============================================================================
19. RESOURCE FILES TO EDIT
==============================================================================
Edit only the visual resource files required by the existing item: texture, model JSON, optional
custom model/renderer files or animation assets if already supported.

==============================================================================
20. LOCALIZATION / TOOLTIP CONSISTENCY
==============================================================================
Keep names, localization keys and tooltip identity consistent with the existing item. Update visual-
facing tooltip flavor only if the project already uses such flavor text.

==============================================================================
21. CATEGORY-WIDE STYLE CONSISTENCY
==============================================================================
Maintain category-wide consistency with the other items in the same family. Hell / Infernal style =
charred black material, ember-orange glow, volcanic cracks, infernal heat and controlled demonic
intensity. The item should feel like it belongs to a coherent biome/faction/set.

==============================================================================
22. GAP / SEAM / Z-FIGHTING QA
==============================================================================
Inspect for gaps, broken seams, open geometry, missing side faces, bad alpha edges or z-fighting.
Even simple items should not look technically broken.

==============================================================================
23. VISUAL TEST MATRIX
==============================================================================
Visual tests should include inventory readability, hand readability, dropped readability, contrast
on bright and dark backgrounds, and consistency with neighboring items from the same family.

==============================================================================
24. BUILD / RESOURCE RELOAD VALIDATION
==============================================================================
Validate by reloading resources and, if possible, building/running the mod. Fix missing texture
paths, wrong item models, broken JSON and any visual pipeline issues.

==============================================================================
25. DEFINITION OF DONE
==============================================================================
Definition of Done: the item's visual identity is clear and attractive, the style fits its family,
the existing item in the mod has been updated in-place, and no gameplay behavior was altered.

==============================================================================
26. HARD RULE: VISUAL-ONLY REWORK
==============================================================================
HARD RULE: this is a visual-only rework. Do not implement or change functionality.

==============================================================================
27. HARD RULE: MODIFY THE EXISTING ITEM, NOT A NEW ONE
==============================================================================
HARD RULE: modify the existing item 'Ember Kapok Pod', not a duplicate, placeholder or new registry
entry.

==============================================================================
28. HARD RULE: KEEP THE MOD'S EXISTING FUNCTIONALITY INTACT
==============================================================================
HARD RULE: keep the mod's existing functionality intact while improving only the visual component.

END OF PROMPT.
```

---
