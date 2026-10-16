# Dark Forest Toolset — Master Production Prompts

> **Target:** Minecraft Fabric 1.20.1 + GeckoLib 4.x + Blockbench-compatible 3D assets  
> **Set:** Dark Forest Sword, Pickaxe, Axe, Shovel, Hoe  
> **Purpose:** five independent, self-contained, ultra-detailed production prompts for an AI coding/3D agent. Each prompt contains at least 70 numbered specification sections, including a unique gameplay ability, model construction, GeckoLib animation, Fabric 1.20.1 implementation, VFX, networking, optimization, testing, and Definition of Done.

## Full concept art

![Dark Forest full toolset concept](concept_art/dark_forest_full_set.png)

## Shared visual language of the Dark Forest set

The entire set must look as if it was grown and forged by one ancient nocturnal forest civilization. The recurring design language is: **charcoal-black fractured metal/stone + living ancient roots + violet arcane cracks + small violet night-flowers + sparse cyan/teal bioluminescent fungal growth**. The tools are not clean royal artifacts and not generic demonic weapons. They should feel like forgotten relics reclaimed by an impossibly old, sentient forest.

The dark metal should be almost black with cold gray highlights and irregular plate segmentation. The roots should be deep brown-black, twisted, thorny, fibrous and physically wrapped around the structure rather than merely painted on it. Violet energy should appear inside cracks, seams and flower cores, not as a constant full-screen neon glow. Cyan/teal growth is a secondary accent and should remain sparse. The small purple flowers are a major set identifier and must look like actual physical ornaments/growths, not flat stickers.

**Important:** each prompt below is intentionally standalone. Do not assume the agent has read another prompt first.


## Unique abilities included in this expanded specification

- **Dark Forest Sword — Shadow Bloom Step:** short safe forward shadow-root teleport with a single controlled slash against entities intersecting the path.
- **Dark Forest Pickaxe — Veinroot Awakening:** bounded connected-vein mining for a clicked eligible ore family, with normal drops, enchantments and durability.
- **Dark Forest Axe — Rootsnare Cleave:** irregular forward ground wave of thorn-roots that damages each target once and briefly roots eligible victims.
- **Dark Forest Shovel — Nightroot Excavation:** controlled 5x5 same-layer area excavation of legitimate shovel-mineable blocks.
- **Dark Forest Hoe — Night Bloom:** contextual 7x7 legitimate bone-meal-style growth pulse while preserving normal vanilla hoe tilling.

Every ability is specified again inside its item's standalone prompt, including exact validation, animation, VFX, networking, performance limits and QA.

---

# 1. Dark Forest Sword

![Dark Forest Sword concept](concept_art/dark_forest_sword.png)

```text
# =====================================================================
# MASTER PRODUCTION PROMPT — DARK FOREST SWORD
# Minecraft Fabric 1.20.1 + GeckoLib 4.x
# Full 3D model + UV + texture + rig + animations + melee VFX + code
# =====================================================================

You are acting simultaneously as a senior Minecraft Fabric 1.20.1 developer, GeckoLib 4 specialist, Blockbench 3D artist, low-poly prop artist, pixel-art texture artist, technical animator, VFX artist, gameplay programmer, optimization engineer, and QA engineer.

Your task is to recreate the supplied DARK FOREST SWORD concept as a COMPLETE, PRODUCTION-READY animated 3D item for the existing mod project.

REFERENCE FILES:
- concept_art/dark_forest_sword.png — primary sword reference.
- concept_art/dark_forest_full_set.png — shared set-language reference.

Do not merely explain how it could be made. Inspect the project and actually implement it.

=====================================================================
1. PROJECT AUDIT — DO THIS BEFORE MODELING OR CODING
=====================================================================

Inspect the real project first:
- build.gradle / build.gradle.kts;
- gradle.properties;
- settings.gradle;
- fabric.mod.json;
- exact Minecraft version;
- exact Yarn mappings;
- exact Fabric Loader/Fabric API versions;
- exact GeckoLib dependency/API version;
- Java version;
- existing item registration;
- existing ToolMaterial classes;
- existing GeckoLib animated items;
- model/renderer conventions;
- client initializer;
- particle and sound registries;
- resource directory conventions;
- existing Dark Forest content if any.

If the repository contains skills/, SKILL.md, lore.md, project conventions, or concept documentation, read and follow them before implementing anything relevant.

Do NOT use Forge, NeoForge, GeckoLib 3 APIs, or examples from incompatible Minecraft versions. Do not invent methods. Compile against what is actually installed.

=====================================================================
2. ITEM IDENTITY
=====================================================================

Recommended registry ID:
    dark_forest_sword

Recommended display name:
    Dark Forest Sword

This is a legendary sword grown from an ancient living forest around a fractured black-metal blade.

Core identity:
ANCIENT NIGHT FOREST
+ BLACKENED FRACTURED METAL
+ LIVING THORNY ROOTS
+ VIOLET ARCANE ENERGY
+ PURPLE NIGHT FLOWERS
+ SPARSE CYAN BIOLUMINESCENT GROWTH.

It must NOT become:
- a Nether/demonic sword;
- a generic purple neon sword;
- a clean royal sword;
- a sci-fi energy blade;
- a simple recolored vanilla sword;
- an overgrown green jungle weapon.

The mood is old, cold, nocturnal, dangerous, organic, mysterious and beautiful.

=====================================================================
3. EXACT SILHOUETTE FROM THE CONCEPT
=====================================================================

The sword is very tall and narrow, with a long pointed blade. The blade is predominantly dark segmented metal/stone. Its silhouette is not perfectly smooth: several small thorn-like protrusions emerge from both sides at irregular vertical intervals.

The upper tip is sharply faceted rather than a simple triangular plane. The blade body tapers gradually toward the point and widens slightly toward the lower third.

A major violet fissure runs longitudinally through the center of the blade. Smaller purple-lit cracks branch from it into the black plate surfaces.

Near the base, the blade enters an organic root-grown guard. The crossguard is not a conventional straight bar. It resembles dark ancient roots branching outward like antlers or thorns.

At the exact visual center of the guard is a luminous violet flower with several petals and a bright purple core.

Below the guard, the handle is entirely wrapped/grown from twisted black-brown roots, with sparse cyan fungal filaments and tiny violet flowers. The bottom ends in a square block-like dark pommel with another flower emblem/growth.

Preserve this hierarchy:
1. tall blade;
2. purple central fissure;
3. thorny blade silhouette;
4. root crossguard;
5. central purple flower;
6. root handle;
7. square flower pommel.

=====================================================================
4. BLADE GEOMETRY
=====================================================================

The blade must have real 3D thickness. Never make it a flat plane.

Build the blade from a low-poly central mass and segmented surface plates. Use a controlled, readable silhouette rather than hundreds of tiny pieces.

Suggested structure:
- core blade volume;
- front plate segmentation;
- back plate segmentation;
- edge bevels;
- central recessed fissure channel;
- side thorn/spike accents;
- faceted tip.

The metal should look like several ancient plates fused into one weapon. Plate seams must be intentional and follow the concept art.

The cutting edges should be lighter cold gray than the inner surfaces. Use geometry and texture shading together to create a sharpened bevel.

The sword must remain Minecraft-compatible low-poly. Do not create realistic micro-topology or 30-sided bevels.

=====================================================================
5. VIOLET FISSURE SYSTEM
=====================================================================

The central violet crack is one of the sword's primary identifiers.

Create a recessed or slightly inset structural channel rather than painting one random purple stripe over the blade.

The fissure should:
- begin near the lower blade/guard region;
- travel upward through most of the blade;
- branch subtly;
- vary slightly in width;
- remain mostly vertical;
- terminate before/near the tip depending on reference fidelity.

Use dark violet around the recess and brighter purple only in the deepest core. Do NOT make the entire crack pure white-purple.

If the existing rendering stack supports emissive layers cleanly, make only the hottest inner portions emissive. Otherwise simulate luminosity with texture contrast and restrained particles during actions.

=====================================================================
6. BLADE THORNS
=====================================================================

Small blade-side thorns/spikes emerge at several heights. These are not random huge spikes.

They should feel like either:
- corrupted metal growths;
- roots/mineralized thorns forcing themselves through the blade.

Use approximately the number and distribution visible in the concept. Keep left/right balance without perfect mirror repetition.

Each thorn must be physically attached and have believable root/metal transition. No floating pieces.

=====================================================================
7. CROSSGUARD — LIVING ROOT STRUCTURE
=====================================================================

The guard should be built from multiple twisted root branches, not a horizontal metal bar.

Visual structure:
- thick central root knot around blade base;
- left branch forks outward/downward/upward;
- right branch mirrors the overall mass but may differ subtly;
- sharpened thorn tips;
- violet cracks or flower accents near the center.

The guard should visually lock the blade into the living handle.

Use real geometry for the major roots. Use texture for bark striations and tiny fibers.

=====================================================================
8. CENTRAL NIGHT FLOWER
=====================================================================

At the guard center create a physically modeled violet flower.

Approximate form:
- 5–7 major petals;
- dark indigo outer petal edges;
- richer violet midtones;
- bright lavender core;
- tiny emissive-like center if supported.

The flower should sit in/front of the root knot and be immediately readable in first-person and GUI scale.

Do not make it a flat decal.

=====================================================================
9. HANDLE
=====================================================================

The handle is a column of tightly twisted ancient roots.

It should NOT be a smooth wooden stick.

Construct several major root strands wrapping helically around a central grip volume. Add a few small thorn nubs, but preserve a believable hand grip area.

Primary wood palette:
- near-black brown recess;
- dark walnut;
- muted brown-gray highlight;
- cold gray-brown worn ridges.

Avoid orange wood tones.

Sparse cyan/teal bioluminescent fungal threads may appear in narrow cracks between roots. They are secondary accents only.

Tiny violet flowers can grow at 1–3 points on the lower handle.

=====================================================================
10. POMMEL
=====================================================================

The pommel is a compact square/block-like dark structure, visually similar to an ancient forest-brick cap.

It should contain:
- dark stone/metal square body;
- slightly raised border blocks;
- central violet flower/gem motif;
- root transition into the handle.

Keep it heavy and readable.

=====================================================================
11. MATERIAL PALETTE
=====================================================================

MATERIAL A — BLACKENED METAL / FOREST STONE
- almost black charcoal;
- cold graphite;
- dark bluish gray;
- silver-gray worn edges.

MATERIAL B — ANCIENT ROOTS
- black-brown;
- deep walnut;
- gray-brown highlights;
- muted bark fibers.

MATERIAL C — ARCANE VIOLET
- deep indigo;
- saturated violet;
- lavender hotspot;
- tiny near-white violet center only for focal glow.

MATERIAL D — CYAN BIOLUMINESCENCE
- dark teal;
- cyan-blue accents;
- tiny bright aqua pixels.

MATERIAL E — NIGHT FLOWERS
- indigo petal edges;
- purple midtones;
- lavender centers.

Never let cyan compete with violet as the primary magic color.

=====================================================================
12. TEXTURE STYLE
=====================================================================

Preferred master resolution: 256x256 unless the project has a strict existing standard.

Maintain deliberate Minecraft pixel-art discipline:
- crisp edge shading;
- no photographic bark texture;
- no blurry stock materials;
- no high-frequency random noise;
- intentional cracks;
- sparse scratches;
- controlled highlights.

Use texture detail for:
- bark fibers;
- tiny plate scratches;
- small fissure branches;
- tiny fungal dots;
- petal shading.

=====================================================================
13. UV
=====================================================================

Create clean UVs with adequate padding.

Prioritize texture space for:
1. blade front/back;
2. central fissure;
3. guard flower;
4. root handle;
5. pommel flower.

Mirroring is acceptable only where it does not create obviously duplicated organic wear. The root guard should not look mechanically mirrored at pixel level.

=====================================================================
14. BONE HIERARCHY
=====================================================================

Use a clean GeckoLib bone structure such as:

root
└── sword
    ├── blade
    │   ├── blade_core
    │   ├── blade_thorns
    │   └── blade_fissure_fx
    ├── guard
    │   ├── guard_root_left
    │   ├── guard_root_right
    │   └── guard_flower
    ├── handle
    │   ├── root_grip
    │   ├── fungal_fx
    │   └── small_flowers
    ├── pommel
    │   └── pommel_flower
    └── fx
        ├── fx_blade
        └── fx_main_flower

Adjust to actual model needs. Do not create one bone per tiny cube.

=====================================================================
15. REQUIRED ANIMATIONS
=====================================================================

At minimum create:
- animation.dark_forest_sword.idle
- animation.dark_forest_sword.equip
- animation.dark_forest_sword.attack
- animation.dark_forest_sword.attack_alt

Optional only if architecture benefits:
- animation.dark_forest_sword.crit

Idle must be nearly static. The weapon is rigid. A flower-core pulse and <1° root/ornament motion is enough.

Equip: 0.25–0.45 sec, controlled rise, tiny inertia, no spinning.

Attack: faster than a heavy axe, deliberate and sharp. Use anticipation → acceleration → contact → follow-through → recovery.

Attack_alt may reverse the cutting direction for visual variety if the existing combat/render architecture can alternate cleanly.

=====================================================================
16. MELEE VFX
=====================================================================

Normal air swing:
- short translucent dark-violet/gray blade trail;
- tiny cyan fungal motes near the handle only rarely;
- no impact burst on miss.

Confirmed hit:
- compact violet contact flash;
- 3–7 dark metal sparks;
- 2–5 violet arcane fragments;
- 0–2 cyan motes;
- tiny flower-core pulse.

Critical hit:
- slightly brighter violet starburst;
- ~30–50% more particles;
- still no giant explosion.

Do not use blood-like red particles. Do not create a screen-filling purple aura.

=====================================================================
17. SOUND IDENTITY
=====================================================================

Swing: heavy cold-metal whoosh with faint woody/root resonance.
Hit: dark metallic impact + brief arcane crackle.
Critical: slightly sharper violet crystal/forest resonance.

No thunder. No infernal roar. No generic sci-fi laser.

=====================================================================
18. GAMEPLAY CLASS
=====================================================================

Implement as the correct Fabric/Yarn 1.20.1 SwordItem or project-specific sword base class.

Reuse the project's Dark Forest/advanced ToolMaterial if one exists. Do not invent absurd balance values before inspecting progression.

Preserve normal sword behavior and appropriate enchantments.

MANDATORY UNIQUE ABILITY: SHADOW BLOOM STEP. A normal right-click performs a short server-authoritative shadow-root teleport forward, up to 10 blocks, stopping at the farthest safe unobstructed destination. A compact spectral root/flower trail marks the path. Living targets intersected by the swept path can be struck once by a controlled shadow-slash and receive a very short Darkness effect. The ability must have a cooldown, explicit destination safety checks, multiplayer synchronization, and no wall-phasing.

=====================================================================
19. FIRST-PERSON / THIRD-PERSON
=====================================================================

Tune transforms carefully because the blade is long.

First person:
- grip should emerge naturally from lower-right;
- sword should be slightly diagonal;
- central flower should remain visible;
- blade must not cover the crosshair constantly.

Third person:
- hand grips root handle, not pommel or flower;
- blade does not clip excessively through player torso/head.

Also test GUI, dropped item, item frame where relevant, and enchantment glint.

=====================================================================
20. PERFORMANCE / NETWORKING
=====================================================================

Do not create global tick particle loops.
Do not allocate heavy objects every frame.
Confirmed-hit VFX must correspond to actual gameplay hits, not client guesses.
Keep cosmetic effects lightweight and multiplayer-safe.
Client renderer classes must never crash a dedicated server.

=====================================================================
21. REFERENCE-FIDELITY CHECKLIST
=====================================================================

The final sword must preserve:
[ ] long narrow dark blade;
[ ] sharp faceted tip;
[ ] segmented black metal/stone surface;
[ ] central violet fissure;
[ ] side thorn protrusions;
[ ] living root crossguard;
[ ] large violet flower at guard center;
[ ] twisted root handle;
[ ] sparse cyan bioluminescent growth;
[ ] small violet flowers;
[ ] square dark pommel with flower motif.

=====================================================================
22. VALIDATION
=====================================================================

Test:
- item registration;
- model loading;
- texture paths;
- first/third person;
- GUI/drop;
- attack animation;
- confirmed-hit VFX;
- critical VFX;
- durability;
- enchantments;
- multiplayer visibility;
- resource reload;
- dedicated-server class safety.

Run the real Gradle wrapper, then runClient if available. Fix all errors before reporting completion.

FINAL DEFINITION OF DONE:
The task is complete only when the sword is a real, functional Fabric 1.20.1 GeckoLib item that strongly matches the supplied concept and shares the exact Dark Forest visual language with the rest of the set.

=====================================================================
23. UNIQUE ABILITY — SHADOW BLOOM STEP
=====================================================================

The sword has a mandatory active ability called SHADOW BLOOM STEP.

Trigger:
- one normal right-click while the sword is held;
- no hold-to-charge phase;
- no release-to-cast behavior;
- one accepted input creates one cast.

Fantasy: the wielder briefly dissolves into black roots, violet petals and cold forest shadow, moves forward through a short corridor of darkness, and reforms at the farthest safe point. The effect must look like movement through a living nocturnal forest, not a generic Ender Pearl teleport.

The ability must be strong but readable, deterministic on the server, safe around walls, and bounded for performance.

=====================================================================
24. ABILITY RANGE AND CORE CONSTANTS
=====================================================================

Use named constants rather than scattered magic numbers. Recommended initial tuning:
- MAX_TELEPORT_DISTANCE = 10.0 blocks;
- SEARCH_STEP = 0.25–0.5 blocks;
- COOLDOWN = 6 seconds;
- DURABILITY_COST = 3;
- PATH_DAMAGE_RADIUS = approximately 0.65–0.85 blocks;
- PATH_DAMAGE = moderate and below a full critical axe hit;
- DARKNESS_DURATION = approximately 30–50 ticks;
- MAX_TARGET_HITS_PER_CAST = once per target.

Range 10 blocks is the default design target. Keep it easy to rebalance from one location.

=====================================================================
25. HORIZONTAL DIRECTION AND PLAYER PITCH
=====================================================================

The cast should primarily follow the actual view direction while preventing absurd vertical teleport abuse. Use the player's look vector but clamp or validate the vertical component. Looking slightly upward/downward may influence destination, but the ability must not launch the player 10 blocks into the sky or bury them underground.

If the project prefers a ground-following dash, project the direction mostly onto the horizontal X/Z plane and solve safe Y separately. Choose one coherent rule and document it in code.

=====================================================================
26. SAFE DESTINATION SEARCH
=====================================================================

Do not teleport directly to `playerPos + look * 10` and hope the space is valid.

Sample positions from near to far, remembering the farthest safe candidate. A valid candidate requires sufficient collision-free space for the player's bounding box, a legal world position, and no solid obstruction between the player and candidate according to the chosen dash semantics.

Prefer the farthest safe destination before the first hard obstruction. This makes the ability feel responsive near walls without granting wall-phasing.

=====================================================================
27. COLLISION AND WALL-PHASING PREVENTION
=====================================================================

The ability must never allow movement through a solid wall, closed door, thick tree trunk, protected barrier, or other collision shape merely because the final position happens to be empty.

Use ray/collision sweeps or repeated bounding-box checks along the path. Test non-full cubes and irregular collision shapes. The path itself matters, not only the endpoint.

=====================================================================
28. DESTINATION BODY SPACE
=====================================================================

Validate the complete player volume at destination, not only one block coordinate. Ensure feet, torso and head space are valid for the current player dimensions. Respect crouching only if the game's collision system naturally reports a valid crouched shape; do not force a standing player into a one-block-high cavity.

Never intentionally suffocate the player inside geometry.

=====================================================================
29. FLOOR AND FALL SAFETY
=====================================================================

The default behavior should prefer a stable destination with support beneath the player. Do not place the player over a lethal void merely because the horizontal path is clear. A small step down is acceptable; a huge cliff drop is not.

Recommended: search a small vertical window around each candidate for a collision-free position with solid/supporting ground, while limiting vertical correction to a few blocks.

=====================================================================
30. LAVA, FIRE AND HAZARD SAFETY
=====================================================================

Do not automatically teleport the player into lava, fire, cactus collision, powder snow, or another immediately hazardous destination when a nearer safe location exists. Reuse existing project hazard checks where available. Hazard safety should be a quality feature, not a giant hard-coded list if tags/fluid states already provide the needed semantics.

=====================================================================
31. SERVER AUTHORITY
=====================================================================

All gameplay-critical decisions occur on the logical server:
- cooldown validation;
- path construction;
- destination validation;
- target intersection;
- damage;
- status effects;
- durability cost;
- actual teleport.

The client may predict a small cast animation, but it must never decide the final destination or apply damage.

=====================================================================
32. COOLDOWN AND SPAM CONTROL
=====================================================================

Use `ItemCooldownManager` or the project's existing ability cooldown abstraction. Cooldown begins only after a successful cast. Failed casts caused by no valid destination should not consume the full cooldown unless project conventions say otherwise.

Do not allow macro/right-click spam to queue multiple teleports in the same tick.

=====================================================================
33. DURABILITY COST
=====================================================================

Consume the ability durability cost once per successful teleport, not once per sampled path position or target. Use normal ItemStack damage APIs so Unbreaking/creative-mode behavior follows project conventions.

If the sword would break from the ability, handle break animation/event correctly and never leave a stale active cast state.

=====================================================================
34. SWEPT PATH HIT VOLUME
=====================================================================

The teleport may slash entities crossed by the shadow corridor. This is a secondary effect, not a screen-clearing AoE.

Construct a bounded swept volume from origin to destination, or query a conservative expanded box and then test each candidate's distance/intersection against the actual segment. Only entities genuinely close to the path should count.

=====================================================================
35. ONE HIT PER TARGET
=====================================================================

Maintain a per-cast set of entity IDs/UUIDs so a target is damaged at most once even if multiple path samples overlap its hitbox. Never apply damage every 0.25-block sample.

This rule is essential for deterministic balance and server performance.

=====================================================================
36. PATH DAMAGE DESIGN
=====================================================================

Use moderate controlled damage. The ability's value is mobility plus one shadow slash, not a guaranteed one-shot. Reuse the project's combat scaling or a dedicated damage source if one already exists.

Do not automatically apply normal sword enchantment on-hit hooks repeatedly. If enchantment interaction is desired, invoke it once and intentionally.

=====================================================================
37. DARKNESS / DISORIENTATION EFFECT
=====================================================================

Targets struck by the path may receive a very short Darkness effect to sell the nocturnal forest fantasy. Keep duration low enough that repeated PvP use is not oppressive. If the project has its own shadow-mark effect, prefer that instead.

Do not apply blindness/darkness to bosses or immune entities in ways that break scripted encounters; respect effect immunity and project rules.

=====================================================================
38. PVP AND TEAM RULES
=====================================================================

Respect server PvP, team/friendly-fire settings, invulnerable/spectator states, and existing combat protection. The ability must not become a bypass for spawn protection or friendly-fire restrictions.

=====================================================================
39. BOSS AND LARGE-ENTITY BEHAVIOR
=====================================================================

Large entities may intersect the path even when their center is outside it. Use bounding-box proximity, not center-point-only tests. Bosses can take damage if ordinary combat rules allow it, but status-control effects should respect immunity and not trivialize encounters.

=====================================================================
40. ABILITY CAST ANIMATION
=====================================================================

Add `animation.dark_forest_sword.shadow_step` and, if useful, `animation.dark_forest_sword.shadow_step_recover`.

The motion should be fast and predatory: slight backward draw, central flower ignition, blade fissure intensification, a compact forward thrust/slash, disappearance, and short recovery. Do not spin the sword or create a long cinematic lockout.

=====================================================================
41. CAST TIMELINE
=====================================================================

Recommended visual timing:
- 0.00 s: normal pose;
- 0.05 s: pommel/handle flowers pulse;
- 0.10 s: energy climbs the root handle;
- 0.15 s: guard flower brightens;
- 0.20 s: blade fissure becomes intense;
- 0.24 s: teleport executes / travel VFX begins;
- 0.28–0.38 s: destination reform flash;
- 0.45 s: weapon settles.

Gameplay teleport should align closely with the visual release frame.

=====================================================================
42. ORIGIN VFX
=====================================================================

At the departure point create a compact silhouette break-up, not a smoke bomb. Use dark root fragments, 4–8 violet petals, a few purple sparks and at most 1–3 cyan spores. A thin flower-shaped flash may briefly appear at feet/guard height.

Lifetime should be under roughly 0.5 seconds.

=====================================================================
43. TRAVEL TRAIL VFX
=====================================================================

The path should show a sparse, broken corridor of shadow rather than a continuous opaque beam. Use short root-shaped streaks and violet petal motes distributed along the path, with slightly denser particles near origin and destination.

Never make a perfect purple laser line.

=====================================================================
44. DESTINATION VFX
=====================================================================

At reform, reverse the visual logic: dark root wisps contract inward, violet petals converge, the central flower flashes once, and the sword fissure returns to normal. Keep the flash compact enough not to blind the player in first person.

=====================================================================
45. FLOWER MOTIF DURING ABILITY
=====================================================================

The violet flower is not decoration only; it is the visual "heart" of the teleport. The guard flower should be the brightest object during activation, with the pommel flower and tiny handle flowers responding in sequence. Avoid turning every purple pixel emissive.

=====================================================================
46. CYAN BIOLUMINESCENT ACCENT
=====================================================================

Cyan/teal is secondary. Use it as a rare biological accent in the travel trail—tiny spores, fungal dust or root-vein glints. Purple remains dominant. If cyan becomes equally bright, the set identity will become noisy.

=====================================================================
47. SOUND DESIGN
=====================================================================

Layer the cast from three ideas:
1. short woody/root tension;
2. low shadow "fold" or air displacement;
3. delicate violet crystal/flower resonance.

Departure and arrival should be distinguishable but part of one sound phrase. Avoid Enderman imitation, thunder, fire and sci-fi teleport sounds.

=====================================================================
48. EMISSIVE / RENDER LAYER STRATEGY
=====================================================================

If the existing GeckoLib renderer supports clean emissive layers, limit them to fissure cores and flower centers. During the cast, animate intensity through supported render state or texture/animation systems. Do not install a shader dependency solely for this sword.

=====================================================================
49. FIRST-PERSON CAST PRESENTATION
=====================================================================

Keep the camera playable. The sword may move toward screen center during the 0.2-second charge cue, but the blade must not cover the entire view. Avoid full-screen motion blur or white flash. The spatial travel effect should exist in the world, not as a giant HUD overlay.

=====================================================================
50. THIRD-PERSON CAST PRESENTATION
=====================================================================

Other players should see a clear disappearance/reappearance sequence with a brief root-and-petal corridor. The character must not remain visibly standing at origin for several ticks after the server has moved them. Synchronize animation and teleport event closely.

=====================================================================
51. MULTIPLAYER SYNCHRONIZATION
=====================================================================

Use ordinary server entity movement synchronization for the teleport. Spawn world-visible particles from the server or send one compact ability event, rather than each client inventing a different path. Do not send dozens of packets per sampled position.

=====================================================================
52. ABILITY FAILURE FEEDBACK
=====================================================================

If no safe destination exists, do not teleport. Prefer a tiny muted flower flicker or short failed-root sound rather than the full cast. Do not consume full durability or produce a misleading travel trail.

=====================================================================
53. EDGE CASE — DOORS, FENCES, SLABS, LEAVES
=====================================================================

Test irregular collision shapes. Leaves may or may not count as an obstruction depending on intended design, but decide explicitly. Doors/fences/slabs must follow real collision, not block-ID assumptions. Use collision shapes whenever possible.

=====================================================================
54. EDGE CASE — WATER
=====================================================================

Decide whether water destinations are allowed. Recommended: allow shallow/safe water if body space is valid, but avoid teleporting into fully submerged hazardous locations when a dry nearer location exists. Never use a naive "air only" rule that breaks beaches and rivers unnecessarily.

=====================================================================
55. ENCHANTMENT AND ATTACK COMPATIBILITY
=====================================================================

Normal SwordItem attacks, enchantments, cooldown strength, durability and hit logic remain intact. The ability is additional behavior; it must not turn normal left-click attacks into teleport attacks or disable blocking/use interactions required elsewhere in the mod.

=====================================================================
56. CODE ARCHITECTURE
=====================================================================

Keep `DarkForestSwordItem` focused. If the ability becomes large, split reusable logic into narrowly scoped helpers such as `ShadowBloomStepAbility`, `SafeTeleportSolver` and `ShadowPathHitResolver`. Do not create a monolithic 600-line item class.

=====================================================================
57. CONFIGURATION / BALANCE CONSTANTS
=====================================================================

Centralize range, cooldown, durability, damage and status duration. If the project has a config system, expose them there. Otherwise use private static final constants with descriptive names and comments explaining units (blocks, ticks, damage points).

=====================================================================
58. PERFORMANCE BUDGET
=====================================================================

Maximum range is short, so bounded 0.25–0.5 block path sampling is acceptable. Do not scan all entities in a giant radius every tick. Build one conservative query box per cast, filter once, and end the ability immediately after execution.

=====================================================================
59. MEMORY / STATE SAFETY
=====================================================================

The ability should be essentially instantaneous and not require a long-lived global cast object. If a brief scheduled visual sequence is used, key it by cast ID/player UUID and remove it deterministically. Never retain stale world/player references.

=====================================================================
60. MODEL REFINEMENT — BLADE SILHOUETTE
=====================================================================

After gameplay works, revisit the model at silhouette scale. The blade must remain tall, severe and thorned even with all textures disabled. Side thorns should be asymmetrical enough to feel grown, but arranged so the weapon does not look randomly jagged.

=====================================================================
61. MODEL REFINEMENT — ROOT GUARD
=====================================================================

The guard should look grown around the blade tang. Create interlocking root branches with believable overlap, taper, bark segmentation and thorn direction. Avoid identical mirrored cylinders. Maintain enough negative space that the central flower remains readable.

=====================================================================
62. TEXTURE REFINEMENT — BLACK PLATES
=====================================================================

Use multiple charcoal values and cold gray edge wear. Plate segmentation should remain visible under Minecraft lighting. Purple cracks belong mainly in recesses. Do not flood the entire blade with purple gradients.

=====================================================================
63. TEXTURE REFINEMENT — ROOTS AND FUNGUS
=====================================================================

Roots should use brown-black, muted umber and cold highlights rather than pure black. Cyan fungal growth should be sparse and granular. Small violet flowers need clear petal silhouettes and dark centers around a luminous core.

=====================================================================
64. ANIMATION QA
=====================================================================

Check idle, equip, two melee attacks, crit reaction and shadow-step transitions at normal game speed. No bone should snap because two controllers fight for the same transform. The central fissure/flower effects must return to baseline after every interrupted action.

=====================================================================
65. TELEPORT SAFETY TEST MATRIX
=====================================================================

Test casts toward:
- open flat terrain;
- one-block wall;
- two-block-thick wall;
- fence;
- slab stair-step;
- doorway;
- tree trunk;
- cliff edge;
- shallow water;
- lava edge;
- low ceiling;
- unloaded/chunk-edge positions;
- world border.

No test should produce suffocation or wall phasing.

=====================================================================
66. COMBAT TEST MATRIX
=====================================================================

Test one mob directly on path, multiple mobs spaced along path, large entities, teammate/friendly-fire scenario, armored target, boss, spectator/creative target, and target just outside the path radius. Verify exactly one ability hit per eligible target.

=====================================================================
67. MULTIPLAYER TEST MATRIX
=====================================================================

Player A casts while Player B observes from side and from destination. Verify no rubber-banding beyond normal teleport correction, particles agree between clients, cooldown is authoritative, and repeated network latency does not duplicate damage.

=====================================================================
68. RESOURCE / RELOAD QA
=====================================================================

Test F3+T/resource reload where relevant, world reload, reconnect, dedicated-server launch, enchantment glint, GUI display and dropped rendering. Missing emissive resources must fail gracefully rather than crash common code.

=====================================================================
69. ABILITY DEFINITION OF DONE
=====================================================================

Shadow Bloom Step is complete only when:
[ ] right-click triggers exactly once;
[ ] max range is bounded;
[ ] walls cannot be crossed;
[ ] destination is collision-safe;
[ ] hazard preference works;
[ ] server performs teleport;
[ ] path targets are hit at most once;
[ ] cooldown works;
[ ] durability cost works;
[ ] origin/travel/destination VFX are synchronized;
[ ] first/third-person animation reads clearly;
[ ] multiplayer does not duplicate damage.

=====================================================================
70. FINAL SWORD DEFINITION OF DONE
=====================================================================

Do not report completion until the sword simultaneously satisfies MODEL, TEXTURE, GECKOLIB, GAMEPLAY and ABILITY requirements. The final item must unmistakably match the supplied concept, function as a real Fabric 1.20.1 sword, and deliver Shadow Bloom Step as a polished Dark Forest mechanic rather than a generic teleport command.

```

---

# 2. Dark Forest Pickaxe

![Dark Forest Pickaxe concept](concept_art/dark_forest_pickaxe.png)

```text
# =====================================================================
# MASTER PRODUCTION PROMPT — DARK FOREST PICKAXE
# Minecraft Fabric 1.20.1 + GeckoLib 4.x
# Full 3D model + UV + texture + rig + mining animations/VFX + code
# =====================================================================

You are a senior Fabric 1.20.1 developer, GeckoLib specialist, Blockbench artist, low-poly prop modeler, texture artist, animator, VFX designer and QA engineer.

Create the supplied DARK FOREST PICKAXE as a COMPLETE production-ready item, not a description.

REFERENCE FILES:
- concept_art/dark_forest_pickaxe.png
- concept_art/dark_forest_full_set.png

Inspect the real project and all version/dependency conventions before implementation. If skills/, lore.md, or existing style documentation exists, follow it. Never mix Forge/NeoForge or incompatible GeckoLib APIs.

=====================================================================
1. ITEM IDENTITY
=====================================================================

Recommended ID:
    dark_forest_pickaxe

The pickaxe must look like an ancient mining relic overtaken by a living night forest.

Shared set language:
- charcoal-black fractured metal/stone;
- cold gray cutting edges;
- twisted dark roots;
- thorn growth;
- violet arcane seams/cracks;
- small purple flowers;
- sparse cyan/teal fungal luminescence.

Do not make it a purple recolor of a vanilla pickaxe.

=====================================================================
2. HEAD SILHOUETTE
=====================================================================

The concept shows a wide two-sided pick head with a strongly curved, predatory profile.

The left and right ends taper into pointed mining tips. The two sides are not plain straight bars: they arc downward and forward slightly, resembling hooked dark-metal beaks emerging from a root-grown central socket.

The upper central section contains a squared dark-metal/stone cap with a strong violet-lit face/channel.

A network of dark roots wraps over and under the metal head, with several thorn spikes protruding upward and backward.

Preserve this readable order:
1. broad double-ended pick silhouette;
2. curved dark blades;
3. central violet block/plate;
4. root entanglement;
5. thorns;
6. long root handle;
7. square flower pommel.

=====================================================================
3. PICK HEAD GEOMETRY
=====================================================================

Build the head as a layered 3D structure:
- central socket mass;
- left inner arm;
- left outer pointed arm;
- right inner arm;
- right outer pointed arm;
- upper plate/cap;
- root overlays;
- thorn accents.

Each end must have real thickness and a sharpened or chisel-like bevel.

Do not use one long rotated cuboid. The shallow curved shape should be constructed from a few coherent segments with clean transitions.

The head should be readable from front, side and 3/4 views.

=====================================================================
4. METAL / STONE HEAD MATERIAL
=====================================================================

Use blackened cold material that sits between forged metal, obsidian-like stone and ancient forest relic plate.

Palette:
- near-black charcoal recess;
- dark graphite midtone;
- bluish-gray secondary plane;
- pale cold gray chipped edge.

Surface treatment:
- irregular plate cuts;
- restrained scratches;
- subtle chips;
- violet energy lines in deep seams.

Do not make it glossy black plastic.

=====================================================================
5. CENTRAL VIOLET STRUCTURE
=====================================================================

The top-center cap/plate is a major focal element. It should be a blocky ancient dark-metal structure with an intense violet central seam or face.

Build actual depth:
rear block → raised frame → recessed purple-lit channel.

If emissive rendering is supported, only the narrow inner purple portions should emit light.

=====================================================================
6. ROOT ENTANGLEMENT
=====================================================================

Large living roots physically bind the pick head to the shaft.

They should:
- wrap around the central socket;
- cross over some metal surfaces;
- fork into thorn branches;
- merge into the handle below.

Root geometry should be low-poly and deliberately twisted, not a smooth procedural cylinder.

Bark palette must match the set: black-brown, dark walnut, gray-brown ridges.

=====================================================================
7. HANDLE
=====================================================================

The handle is almost entirely living root mass.

Create 3–5 major twisted strands around a central grip volume. Allow slight asymmetry.

Include sparse:
- violet flowers;
- tiny purple buds;
- cyan/teal fungal filaments or glowing moss.

Do not overload the handle; the dark roots remain the dominant material.

Keep the hand-grip region sufficiently clean that the player's hand can plausibly hold it.

=====================================================================
8. POMMEL
=====================================================================

Use the set's square dark block pommel with a central violet flower emblem/growth.

The pommel should resemble old forest masonry or black metal bricks grown together with roots.

=====================================================================
9. FLOWERS AND CYAN GROWTH
=====================================================================

Purple flowers are a signature, but this pickaxe should contain fewer major flowers than the axe/shovel. Use small blossoms as secondary accents on handle/pommel.

Cyan bioluminescence should appear as tiny fungus/moss veins and specks, especially where roots overlap.

Violet = primary magic.
Cyan = secondary biological glow.

=====================================================================
10. TEXTURE / UV
=====================================================================

Preferred texture resolution: 256x256 unless project convention differs.

Use crisp pixel-art shading. Do not use photographic wood or stone.

UV priority:
1. pick head surfaces;
2. central violet cap;
3. roots near head;
4. handle;
5. pommel flower.

Do not mirror all organic details perfectly.

=====================================================================
11. BONE HIERARCHY
=====================================================================

Recommended conceptual bones:

root
└── pickaxe
    ├── head
    │   ├── head_center
    │   ├── pick_left
    │   ├── pick_right
    │   ├── central_violet_plate
    │   ├── head_roots
    │   └── head_thorns
    ├── handle
    │   ├── root_grip
    │   ├── small_flowers
    │   └── fungal_fx
    ├── pommel
    │   └── pommel_flower
    └── fx
        ├── fx_head
        └── fx_violet_core

Only create bones that have organizational/animation value.

=====================================================================
12. REQUIRED ANIMATIONS
=====================================================================

Create:
- animation.dark_forest_pickaxe.idle
- animation.dark_forest_pickaxe.equip
- animation.dark_forest_pickaxe.mine
- animation.dark_forest_pickaxe.attack

Idle: nearly static; tiny purple pulse, <1° root/head motion.

Equip: short, heavy but controlled.

Mine: coordinate with vanilla hand/mining movement instead of doubling it. Add subtle head lag/recoil, violet seam pulse and root inertia.

Attack: slightly heavier than normal sword attack, but not as dramatic as Dark Forest Axe.

=====================================================================
13. MINING VFX
=====================================================================

When hitting/breaking a valid pickaxe block:
- preserve vanilla block particles;
- add only a few dark-violet sparks;
- optional 1–2 cyan spores;
- short central plate pulse.

Do not replace stone/ore feedback with purple magic.

Do not spawn custom particles every render tick. Block-breaking can occur quickly with enchantments; rate-limit expensive effects if necessary.

=====================================================================
14. ENTITY HIT VFX
=====================================================================

Confirmed melee hit:
- compact dark-metal flash;
- 3–6 violet sparks;
- tiny root/flower glow response.

No giant AoE and no lightning. Normal entity hits must NOT automatically trigger Veinroot Awakening; the mining ability is contextual and only activates through its specified right-click-on-ore input.

=====================================================================
15. GAMEPLAY
=====================================================================

Implement using the correct Fabric/Yarn 1.20.1 PickaxeItem or existing custom base.

Reuse an existing DarkForestToolMaterial if present. Preserve normal mining tags, appropriate mining level, durability, Efficiency/Unbreaking/Fortune/Silk Touch/Mending compatibility where applicable.

Do not hard-code enormous lists of blocks if vanilla tag logic already handles them.

MANDATORY UNIQUE ABILITY: VEINROOT AWAKENING. Right-clicking a valid ore block performs bounded connected-vein mining for the clicked ore family, using server-authoritative BFS/DFS, a hard block cap, normal drops/enchantments/durability, protection checks, no forced chunk loading, and restrained root/VFX propagation. Right-click elsewhere preserves normal item behavior.

=====================================================================
16. FIRST-PERSON / THIRD-PERSON
=====================================================================

First-person transforms must show the distinctive head without covering the crosshair. The hand should grip the lower-middle root shaft.

Third-person: head orientation must clearly read as a pickaxe; avoid clipping into player head/torso.

Test GUI, ground, item frame where relevant, glint.

=====================================================================
17. PERFORMANCE / CLIENT-SERVER SAFETY
=====================================================================

Common gameplay code must remain dedicated-server safe. Renderer/model code stays client-only.

Avoid global scans, per-tick allocations and particle spam.

=====================================================================
18. REFERENCE CHECKLIST
=====================================================================

[ ] broad curved two-sided pick head;
[ ] dark segmented plates;
[ ] sharpened pointed ends;
[ ] central blocky violet structure;
[ ] root binding around head;
[ ] several thorn spikes;
[ ] twisted living-root handle;
[ ] sparse cyan growth;
[ ] small purple flowers;
[ ] square dark flower pommel.

=====================================================================
19. QA
=====================================================================

Test stone, deepslate, ores, obsidian/high-tier blocks appropriate to material, wrong-tool blocks, enchantments, durability, first/third person, mine animation, attack, resource reload, multiplayer and dedicated-server loading.

Run Gradle build and runClient. Fix all errors before declaring success.

=====================================================================
20. UNIQUE ABILITY — VEINROOT AWAKENING
=====================================================================

The Dark Forest Pickaxe has a mandatory contextual ability called VEINROOT AWAKENING.

Trigger: right-click directly on a valid ore block while holding the pickaxe. The ancient root network "awakens" inside the stone and harvests the connected vein of the SAME eligible ore family, subject to strict limits and normal mining rules.

This is controlled vein mining, not unrestricted excavation and not X-ray.

=====================================================================
21. ABILITY LIMITS
=====================================================================

Recommended named constants:
- MAX_VEIN_BLOCKS = 32;
- MAX_SEARCH_RADIUS_FROM_ORIGIN = 8 blocks;
- COOLDOWN = 3–5 seconds;
- DURABILITY = normal per successfully broken block;
- MAX_NODES_VISITED = hard safety bound, e.g. 128;
- adjacency = 26-neighbor or 6-neighbor depending design.

Use 26-neighbor adjacency if diagonal ore veins should count naturally, but keep a hard cap.

=====================================================================
22. VALID TRIGGER BLOCK
=====================================================================

The ability only begins if the directly clicked block is an eligible ore that the current pickaxe can legitimately harvest. Clicking stone, dirt, decorative blocks, chests or an invalid mining-tier ore must not initiate a hidden scan.

Prefer tags or a project-defined ore classification rather than a giant hand-written list.

=====================================================================
23. ORE FAMILY MATCHING
=====================================================================

Connected blocks must belong to the same logical ore family as the origin. Handle stone/deepslate variants intentionally. For example, iron ore and deepslate iron ore may be considered one family if the project's intended behavior says so. Do not let one coal block chain into every ore type in a cave.

=====================================================================
24. SEARCH ALGORITHM
=====================================================================

Use bounded BFS/DFS with a visited set. Never recurse through Java call stack without a hard bound. Each discovered position is checked for loaded chunk, range from origin, ore-family compatibility and mining legality before being queued.

=====================================================================
25. HARD NODE-VISIT BUDGET
=====================================================================

Even if only 32 blocks may break, limit visited nodes so unusual modded structures cannot cause a huge search. Once MAX_NODES_VISITED is reached, stop exploration gracefully and use the already collected valid vein positions.

=====================================================================
26. CHUNK LOADING SAFETY
=====================================================================

Do not force-load chunks merely to continue vein detection. If a neighboring ore position is in an unloaded chunk, stop at that boundary. Never turn one click into remote chunk generation.

=====================================================================
27. WORLD BORDER AND BUILD HEIGHT
=====================================================================

Validate positions against world border/build-height bounds before reading or modifying them. Skip invalid positions without throwing exceptions.

=====================================================================
28. MINING SUITABILITY
=====================================================================

Every candidate block must individually pass the same tool-tier/suitability checks required for normal harvesting. A vein ability must not allow a low-tier tool to obtain blocks it cannot normally mine.

=====================================================================
29. PROTECTION / EVENT COMPATIBILITY
=====================================================================

If the project or server exposes block-break protection hooks, invoke/respect them per candidate where practical. Do not bypass claims, spawn protection or scripted unbreakable areas with raw `setBlockState(AIR)`.

=====================================================================
30. BREAK SEMANTICS AND DROPS
=====================================================================

Break blocks using server-authoritative semantics that preserve drops, experience, block-break callbacks, Silk Touch/Fortune behavior and relevant mod hooks. Do not manually spawn guessed drops unless the project already has a canonical helper.

=====================================================================
31. FORTUNE / SILK TOUCH
=====================================================================

The ability must behave as though the same enchanted pickaxe legitimately mined each ore. Fortune should not be applied twice. Silk Touch should not be ignored. Enchantment logic belongs in the normal break pathway.

=====================================================================
32. DURABILITY PER BLOCK
=====================================================================

Charge durability for each successfully harvested block using normal ItemStack damage rules. Invalid/skipped/protected blocks cost nothing. If the pickaxe breaks mid-vein, stop immediately and leave remaining blocks untouched.

=====================================================================
33. UNBREAKING AND CREATIVE MODE
=====================================================================

Use normal durability APIs so Unbreaking can reduce actual durability loss according to Minecraft semantics. Creative mode should follow project conventions and normally avoid durability consumption while still respecting ability cooldown if desired.

=====================================================================
34. BREAK ORDER
=====================================================================

Prefer deterministic near-to-far order from the clicked ore. This looks like roots travelling into the vein and makes low-durability behavior predictable. Sort by BFS discovery depth or squared distance from origin rather than random order.

=====================================================================
35. TEMPORAL PRESENTATION
=====================================================================

Gameplay may break the vein rapidly, but for visual quality consider a very short wave—e.g. a few blocks per tick—without making the player wait multiple seconds. If scheduled breaking is used, the server owns the schedule and cancels safely on disconnect/world change/tool loss.

=====================================================================
36. ROOT-TRAVEL VFX
=====================================================================

For each progression step, show sparse dark root wisps and a violet pulse moving from the previous harvested ore toward the next. Do not draw X-ray lines through the entire cave before blocks are broken. The effect reveals only blocks that the server has already accepted into this cast.

=====================================================================
37. ORE-BREAK VFX
=====================================================================

Preserve vanilla ore particles and add only 1–3 violet crack sparks plus rare cyan fungal dust per harvested block. Because up to 32 blocks can break, secondary VFX must be very cheap.

=====================================================================
38. CENTRAL HEAD RESPONSE
=====================================================================

The pickaxe's violet central head should pulse in waves synchronized with vein progression. Roots wrapping the head may shift by fractions of a degree, as though tension is travelling through them. Do not bend solid metal plates.

=====================================================================
39. ABILITY ANIMATION
=====================================================================

Create `animation.dark_forest_pickaxe.veinroot_cast`. The player plants/angles the pickaxe toward the clicked ore, the central violet structure brightens, roots tighten, and the mine animation releases. Keep it under roughly 0.5–0.7 seconds so mining remains responsive.

=====================================================================
40. SOUND DESIGN
=====================================================================

Cast sound: low stone resonance + root creak + small violet crystal tone. During the vein sequence use quiet localized crack/tick accents, not one full-volume explosion for every ore. A final soft root relaxation sound can mark completion.

=====================================================================
41. NO X-RAY INFORMATION LEAK
=====================================================================

Do not highlight or expose eligible ores beyond the blocks actually accepted by the server for the current vein. Do not add persistent outlines through walls, client-side ore scanners, minimap markers or coordinates.

=====================================================================
42. NO GENERAL 3D EXCAVATION
=====================================================================

The search may traverse connected ore positions, but only ore-family candidates are broken. Stone between separated veins remains untouched. Do not tunnel through rock to connect two ore clusters.

=====================================================================
43. MULTIPLE ORE TYPES IN CONTACT
=====================================================================

If iron touches coal, redstone or another ore, only the clicked ore's family is harvested. The foreign ore may remain physically adjacent but must not be queued.

=====================================================================
44. MODDED ORE SUPPORT
=====================================================================

Prefer an extensible tag/family system so modded ores can opt in. If the project has common tags (`c:ores/...`) or its own registry metadata, use them. Avoid fragile class-name string checks.

=====================================================================
45. BLOCK ENTITY SAFETY
=====================================================================

Ore-like blocks with block entities or custom inventories should not be assumed safe to mass-break. Follow normal break behavior and opt-out tags if needed. Never duplicate inventories/drops by performing both custom removal and normal break callbacks.

=====================================================================
46. COOLDOWN
=====================================================================

Start cooldown only after at least one block is successfully harvested by the ability. A failed click on an invalid ore should behave like normal interaction and not lock the tool for several seconds.

=====================================================================
47. ABILITY INPUT CONFLICTS
=====================================================================

Right-click on ore invokes Veinroot Awakening. Right-click elsewhere should preserve normal item/use semantics and return PASS/appropriate result. Sneak behavior may be used as an opt-out if the project needs players to interact with adjacent blocks without triggering the ability.

=====================================================================
48. SERVER AUTHORITY
=====================================================================

The client never decides which blocks belong to the vein. It may start a cast animation, but the server computes all candidate positions, break legality, order, drops, durability and cooldown.

=====================================================================
49. NETWORKING
=====================================================================

Prefer ordinary block updates plus one compact cast/event packet or server particles. Do not send a custom packet for every BFS neighbor check. Clients only need accepted visual events, not internal search details.

=====================================================================
50. FAILURE / PARTIAL SUCCESS
=====================================================================

If protection, tool breakage or unloaded chunks interrupt the vein, stop or skip those blocks cleanly. Already harvested blocks remain valid; do not roll back. Final sound/VFX should reflect partial completion without errors.

=====================================================================
51. MODEL REFINEMENT — HEAD PLATES
=====================================================================

The pickaxe head must look like curved fractured stone/metal plates bound by roots, not a smooth purple crescent. Use cold edge highlights, plate gaps and a strong dark mass. Keep purple mainly in recesses and central structure.

=====================================================================
52. MODEL REFINEMENT — POINTS
=====================================================================

Both outer pick points should taper into believable mining edges. They may be asymmetrical in small chips/thorns but must remain functionally recognizable. Avoid oversized fantasy scythes.

=====================================================================
53. MODEL REFINEMENT — ROOT WRAP
=====================================================================

Roots should visibly grip the head near structural stress points, pass behind/around plates, and continue into the handle. Avoid floating branch pieces or uniform barber-pole wrapping.

=====================================================================
54. TEXTURE REFINEMENT
=====================================================================

Black plates: charcoal, graphite and cold gray. Roots: dark bark with muted brown highlights. Violet: deep purple glow concentrated in seams. Cyan: rare fungal pinpoints. Flowers: crisp petal silhouettes with luminous centers.

=====================================================================
55. FIRST-PERSON ABILITY PRESENTATION
=====================================================================

During the cast, angle the head toward the targeted ore without covering the crosshair for long. The player should clearly see the central violet block ignite. Avoid a giant screen flash when multiple ore blocks break quickly.

=====================================================================
56. THIRD-PERSON ABILITY PRESENTATION
=====================================================================

Other players should see a compact plant-and-pull mining gesture and a root pulse travelling into nearby ore positions. Do not make the character repeatedly swing once per harvested block.

=====================================================================
57. PERFORMANCE BUDGET
=====================================================================

One bounded BFS per cast is acceptable. Avoid repeated world-wide tag scans, recursive raycasts, or entity queries. Cache family identity for the origin block for the duration of the cast.

=====================================================================
58. CODE ARCHITECTURE
=====================================================================

Keep `DarkForestPickaxeItem` readable. Consider `VeinrootMiningAbility`, `OreFamilyResolver` and `AreaBreakHelper` only if the project lacks equivalents. One helper should have one clear responsibility.

=====================================================================
59. CONSTANTS AND CONFIG
=====================================================================

Centralize max vein size, node visit cap, search radius, cooldown and visual cadence. If configuration exists, expose them with sane bounds so a bad config cannot set 100,000 vein blocks.

=====================================================================
60. TEST — SIMPLE VEIN
=====================================================================

Create a straight 8-block ore vein. Right-click the nearest ore and verify all eligible blocks are harvested in near-to-far order with correct drops and durability.

=====================================================================
61. TEST — DIAGONAL VEIN
=====================================================================

Create diagonal/branching ore positions. Verify behavior matches chosen adjacency rule exactly and remains bounded.

=====================================================================
62. TEST — MIXED ORES
=====================================================================

Place iron, coal and redstone touching each other. Trigger on each type separately. Only the chosen family should break.

=====================================================================
63. TEST — MAX CAP
=====================================================================

Create a vein larger than MAX_VEIN_BLOCKS. Exactly the configured maximum or fewer should break, never an unbounded chain. Remaining ore stays intact.

=====================================================================
64. TEST — TOOL BREAKAGE
=====================================================================

Use a nearly broken pickaxe. Ensure the ability stops when durability is exhausted and does not harvest remaining ore for free.

=====================================================================
65. TEST — ENCHANTMENTS
=====================================================================

Verify Fortune, Silk Touch, Unbreaking, Mending/XP behavior where appropriate, and mining-tier restrictions. Compare representative drops with normal single-block mining.

=====================================================================
66. TEST — MULTIPLAYER / PROTECTION
=====================================================================

Test one protected ore within an otherwise valid vein, two players casting nearby, high latency, and chunk boundary. No duplication, bypass or desync is acceptable.

=====================================================================
67. ANIMATION / CONTROLLER QA
=====================================================================

Ensure veinroot_cast does not fight idle/mine/attack controllers. The central glow returns to baseline after canceled and partial casts. No animation should restart every tick while the server sequence is active.

=====================================================================
68. RESOURCE QA
=====================================================================

Verify geo, animation, textures, emissive resources if any, language, sounds, glint, GUI, dropped item, resource reload and dedicated-server class safety.

=====================================================================
69. ABILITY DEFINITION OF DONE
=====================================================================

[ ] right-click only triggers on valid ore;
[ ] connected search is bounded;
[ ] only same ore family is collected;
[ ] no forced chunk loads;
[ ] normal drops/enchantments work;
[ ] durability is per block;
[ ] tool break stops the cast;
[ ] no X-ray information leaks;
[ ] VFX progression is readable;
[ ] cooldown/networking are authoritative.

=====================================================================
70. FINAL PICKAXE DEFINITION OF DONE
=====================================================================

The pickaxe is complete only when it is both a faithful Dark Forest 3D asset and a safe production-quality mining tool. Veinroot Awakening must feel like living roots discovering an ore vein while remaining mechanically equivalent to legitimate bounded mining—not a cheat command that deletes connected blocks.

```

---

# 3. Dark Forest Axe

![Dark Forest Axe concept](concept_art/dark_forest_axe.png)

```text
# =====================================================================
# MASTER PRODUCTION PROMPT — DARK FOREST AXE
# Minecraft Fabric 1.20.1 + GeckoLib 4.x
# Full 3D model + textures + rig + heavy melee/chopping VFX + code
# =====================================================================

Act as a senior Fabric 1.20.1 / GeckoLib developer and production 3D artist. Recreate the supplied DARK FOREST AXE as a complete in-game item.

REFERENCE FILES:
- concept_art/dark_forest_axe.png
- concept_art/dark_forest_full_set.png

Inspect the actual project versions and conventions before work. Follow any skills/, lore.md and existing Dark Forest code/art conventions. Do not use incompatible APIs.

=====================================================================
1. ITEM IDENTITY
=====================================================================

Recommended ID:
    dark_forest_axe

This is the heaviest and most monumental member of the Dark Forest tool set.

It should look like a double-bladed ceremonial execution/battle axe whose black metal has cracked under violet forest magic and whose center/handle have been consumed by ancient thorn roots.

Visual language:
BLACK FRACTURED PLATE
+ HUGE CRESCENT BLADES
+ TWISTED ROOT HEART
+ VIOLET ENERGY VEINS
+ LARGE NIGHT FLOWER
+ CYAN SPORE/FUNGAL ACCENTS.

No Paradise gold/marble. No demonic red lava. No sci-fi glow.

=====================================================================
2. OVERALL SILHOUETTE
=====================================================================

The head is large and approximately double-crescent/dual-bladed, with a central root mass. The concept is asymmetrically organic even though the overall left/right mass remains balanced.

Each blade is broad, thick and made from dark segmented plate. The outer cutting edges form large crescent arcs. Violet cracks travel through the plate seams.

A massive root knot emerges through the center and visually grows into/around the blades.

A large violet flower sits high near the central/upper root structure and acts as the primary focal accent.

The handle below is a long twisted root column with cyan fungal growth and smaller purple flowers, ending in a square flower pommel.

=====================================================================
3. BLADE GEOMETRY
=====================================================================

Both blade masses require real thickness and believable cutting bevels.

Build each blade from several large plate sections rather than one flat crescent plane.

Recommended hierarchy per blade:
- structural inner plate;
- middle plate bands;
- outer cutting plate;
- bevel/cutting edge;
- crack/recess details.

The outer silhouette should remain sharp and readable but intentionally chipped/segmented.

Avoid paper-thin blades and avoid excessive micro-geometry.

=====================================================================
4. SEGMENTED BLACK PLATES
=====================================================================

The axe head looks like ancient black slabs fitted into a crescent frame.

Surface palette:
- near-black recess;
- graphite face;
- dark slate-blue planes;
- cold gray edge wear.

Plate boundaries may be slightly stepped in depth. Use subtle irregularity, but preserve a strong coherent blade shape.

=====================================================================
5. VIOLET CRACK NETWORK
=====================================================================

Violet fissures are especially prominent on this axe.

They should travel across multiple plate seams, creating the impression that forest magic is glowing from inside the blade.

Use:
- deep indigo outer crack;
- rich violet core;
- small lavender hotspots at intersections.

Do not fill every seam with light. Roughly 10–20% of visible crack network should carry strong glow; the rest may remain dark.

If emissive rendering is supported, keep emission localized to crack cores.

=====================================================================
6. CENTRAL ROOT HEART
=====================================================================

The axe center is not a normal metal eye/socket. It is a dense living root heart.

Major roots should:
- twist around the blade bases;
- branch upward between blades;
- form thorn points;
- descend continuously into the handle.

Use real 3D root geometry. The roots should look old, almost petrified, with black-brown bark and sharp gray-brown ridges.

This organic structure must visually appear to HOLD the axe together.

=====================================================================
7. LARGE FLOWER FOCAL POINT
=====================================================================

Create the large purple flower near the central upper axe head exactly as a physical modeled ornament/growth.

It should be larger and more elaborate than the small handle flowers.

Approximate structure:
- 6–8 petals;
- dark indigo outer edges;
- purple mids;
- lavender inner petals;
- bright violet/blue core.

Optional emissive center only.

The flower should not look cute/cartoonish. It is an eerie nocturnal bloom growing from ancient roots.

=====================================================================
8. THORNS
=====================================================================

Several sharpened root thorns rise around the head center and root branches.

They should be irregularly distributed and oriented. Keep them structurally plausible and avoid random spike clutter.

=====================================================================
9. HANDLE
=====================================================================

The handle is a heavy braided/twisted root column.

Use multiple root strands with changes in thickness and overlaps. The visual centerline should remain stable enough for a believable grip.

Add sparse cyan fungal strands, small blue-green spores and several tiny purple flowers.

The cyan should be strongest in recessed root gaps, not painted over all bark.

=====================================================================
10. POMMEL
=====================================================================

Use the set's square black forest-brick pommel with a violet flower emblem/growth at its center.

Give it thickness, raised edge blocks and root integration.

=====================================================================
11. TEXTURE / MATERIALS
=====================================================================

Preferred texture: 256x256 unless existing assets dictate another size.

Use crisp Minecraft-style texture work.

Do not use photographic bark, realistic rust, or generic noise.

Material hierarchy:
1. black plate;
2. roots;
3. violet cracks/flower;
4. cyan secondary growth.

The weapon must remain dark overall; emissive accents should not turn it into a glowing purple object.

=====================================================================
12. UV
=====================================================================

Highest texel priority:
- blade fronts;
- blade edges;
- violet crack network;
- central root heart;
- large flower.

Give handle/pommel consistent density. Organic roots may share some texture motifs but avoid obvious cloned patterns.

=====================================================================
13. BONE HIERARCHY
=====================================================================

Recommended conceptual structure:

root
└── axe
    ├── head
    │   ├── blade_left
    │   ├── blade_right
    │   ├── root_heart
    │   ├── head_thorns
    │   └── main_flower
    ├── handle
    │   ├── root_grip
    │   ├── fungal_growth
    │   └── small_flowers
    ├── pommel
    │   └── pommel_flower
    └── fx
        ├── fx_blade_left
        ├── fx_blade_right
        └── fx_flower

=====================================================================
14. REQUIRED ANIMATIONS
=====================================================================

Create:
- animation.dark_forest_axe.idle
- animation.dark_forest_axe.equip
- animation.dark_forest_axe.attack
- animation.dark_forest_axe.chop

Optional if existing combat system supports alternating attacks cleanly:
- animation.dark_forest_axe.attack_alt

Idle: almost static. Large flower pulse can be subtle; root heart movement should be fractions of a degree.

Equip: weapon rises with noticeable mass, slight overshoot.

Attack: heavy anticipation, rapid acceleration, strong follow-through and slower recovery.

Chop: synchronize with axe-effective block interaction and vanilla hand motion. Do not double-rotate the entire root model.

=====================================================================
15. HEAVY ATTACK VFX
=====================================================================

Air swing:
- short broad dark-violet translucent crescent trail;
- faint gray-black edge;
- a few violet crack sparks.

Confirmed hit:
- compact violet impact flash;
- 5–10 cold dark-metal sparks;
- 3–7 purple fragments;
- 0–3 cyan spores;
- flower core pulse;
- subtle local pressure ring if lightweight.

Critical hit:
- stronger violet star-shaped flash;
- more sparks;
- no giant explosion.

Do not give normal attacks AoE just because the visual trail is wide.

=====================================================================
16. CHOPPING VFX
=====================================================================

When chopping logs/wood:
- retain the block's normal particles;
- add 1–3 violet motes and maybe one cyan spore;
- tiny root-heart pulse.

Do not replace wood particles with generic magic.

=====================================================================
17. SOUND
=====================================================================

Swing: deep heavy air displacement plus low woody strain.
Hit: dark metal/stone impact plus short violet crackle.
Wood chop: vanilla/appropriate wood feedback plus restrained ancient-root resonance.

No thunder, no fire, no infernal soundscape.

=====================================================================
18. GAMEPLAY
=====================================================================

Use the correct Fabric/Yarn 1.20.1 AxeItem or existing custom axe base. Preserve normal axe mining behavior and enchantments.

Reuse existing Dark Forest ToolMaterial if present.

MANDATORY UNIQUE ABILITY: ROOTSNARE CLEAVE. Right-click performs a heavy forward cleave that sends an irregular wave of thorny shadow-roots across the ground in front of the player. The wave deals controlled damage once per target and briefly roots/immobilizes eligible victims using a safe, bounded status-effect or project-specific root state. It is not a shield, not a projectile spam attack, and not a terrain-destroying explosion.

=====================================================================
19. RENDER TRANSFORMS
=====================================================================

The head is huge, so tune first-person placement carefully:
- keep crosshair visible;
- show enough of the large flower/root heart to communicate identity;
- hand grips lower-middle root handle.

Third person must avoid head clipping through the player's skull/torso. Test standing, sprinting, sneaking, attack and chopping.

=====================================================================
20. QA / PERFORMANCE
=====================================================================

No particle-per-tick aura. No heavy global scans. Keep client renderer server-safe.

Test:
- registration;
- model/texture;
- GUI/drop;
- attacks;
- crits;
- wood chopping;
- mining tags;
- durability/enchantments;
- multiplayer;
- resource reload;
- dedicated server.

REFERENCE CHECKLIST:
[ ] huge dual crescent blades;
[ ] segmented black plate;
[ ] violet fissures;
[ ] central living root heart;
[ ] thorns;
[ ] large purple flower near head center;
[ ] twisted root handle;
[ ] cyan growth;
[ ] small purple flowers;
[ ] square flower pommel.

Run Gradle build and runClient. Do not declare completion until the item works in-game and visually matches the concept.

=====================================================================
21. UNIQUE ABILITY — ROOTSNARE CLEAVE
=====================================================================

The Dark Forest Axe has a mandatory active ability called ROOTSNARE CLEAVE.

One right-click performs a heavy forward cleave. A jagged wave of black thorn-roots erupts along the ground in front of the player, dealing controlled damage and briefly rooting eligible targets. It is crowd control, not a shield and not a terrain explosion.

=====================================================================
22. ABILITY SHAPE
=====================================================================

Recommended footprint:
- length: 10–12 blocks forward;
- average width: 3 blocks;
- irregular left/right protrusions up to 1 block;
- ground-following within a small vertical tolerance;
- no 360-degree radius around player.

The wave must clearly travel forward and should not be a perfect rectangle.

=====================================================================
23. PATH GENERATION
=====================================================================

Generate a short sequence of forward cells from player yaw. Maintain a lateral offset random walk clamped around center and optionally add sparse neighboring cells. Seed the path server-side once per cast so all clients observe the same root eruption.

=====================================================================
24. GROUND PROJECTION
=====================================================================

For each forward cell, resolve a nearby ground surface within a small Y search window. The roots should climb gentle slopes and descend small steps. Do not scan hundreds of vertical blocks or tunnel through cliffs.

=====================================================================
25. WALL / OBSTRUCTION BEHAVIOR
=====================================================================

A substantial wall should stop the root wave rather than allowing damage through mountains. Detect forward obstruction using collision/solid block semantics. Small vegetation may be ignored if project style allows it, but decide explicitly.

=====================================================================
26. NO TERRAIN DESTRUCTION
=====================================================================

The eruption is visual/gameplay control only. Do not break blocks, replace grass, uproot crops, create holes or leave permanent roots unless the project already has a dedicated temporary-root block system designed for cleanup.

=====================================================================
27. DAMAGE MODEL
=====================================================================

Each eligible target intersecting the wave receives damage at most once per cast. Use moderate ability damage, ideally comparable to a strong axe hit but balanced by cooldown. Do not apply damage once per occupied root cell.

=====================================================================
28. TARGET DEDUPLICATION
=====================================================================

Track affected entity IDs/UUIDs for the cast. Large mobs spanning multiple cells still take one controlled hit. This is non-negotiable for balance.

=====================================================================
29. ROOT / IMMOBILIZE EFFECT
=====================================================================

Targets hit by the wave are briefly "rooted". Preferred implementation: reuse a project-specific Rooted effect if one exists. Otherwise apply a short, high-level Slowness plus optional Jump Boost suppression/Weakness in a controlled way. Keep duration around 1.5–2.5 seconds.

Do not use permanent movement modification or raw attribute corruption.

=====================================================================
30. ROOT IMMUNITY
=====================================================================

Bosses, flying entities, spectators, vehicles or entities explicitly immune to movement effects should not be forcibly frozen in a way that breaks AI/scripts. They may still receive damage if combat rules allow it.

=====================================================================
31. PVP SAFETY
=====================================================================

Respect PvP, team and friendly-fire settings. Keep root duration especially conservative in PvP. The ability must not bypass invulnerability frames, spawn protection or spectator rules.

=====================================================================
32. COOLDOWN
=====================================================================

Recommended starting cooldown: 9–12 seconds. Use a named constant and server-authoritative ItemCooldownManager/project equivalent. Do not start cooldown on invalid/canceled use.

=====================================================================
33. DURABILITY COST
=====================================================================

Consume a fixed ability durability cost once per successful cast, e.g. 4–6 points, in addition to normal axe durability during ordinary attacks/chopping. Do not charge per visual root cell.

=====================================================================
34. CAST ANIMATION
=====================================================================

Create `animation.dark_forest_axe.rootsnare_cleave`. The animation should be heavier than the normal attack: short wind-up, root-heart contraction, violent forward/downward cleave, impact frame, recoil, recovery.

No 360-degree spin.

=====================================================================
35. CAST TIMELINE
=====================================================================

Suggested:
- 0.00–0.12 s: heavy anticipation;
- 0.12–0.22 s: central flower and fissures brighten;
- 0.22–0.30 s: blade accelerates;
- ~0.30 s: ground-release frame;
- 0.30–0.70 s: roots propagate forward;
- 0.70–0.90 s: recovery.

=====================================================================
36. ROOT WAVE PROPAGATION
=====================================================================

Do not spawn the full 12-block line simultaneously. Advance one or two forward layers per tick so the player perceives an eruption travelling away from the axe.

Gameplay damage can be checked as each layer activates, with per-cast deduplication.

=====================================================================
37. ROOT GEOMETRY / PARTICLE LANGUAGE
=====================================================================

Use temporary particle/model effects that resemble splintered black-brown roots with violet sap cracks. Each burst should have a thick base near ground and 1–3 thorn silhouettes, then disappear quickly. Avoid spawning dozens of persistent entities.

=====================================================================
38. FLOWER BLOOM ACCENTS
=====================================================================

Occasionally a tiny violet flower can flash between root segments, especially when a target is successfully rooted. Keep frequency low; flowers are mystical punctuation, not confetti.

=====================================================================
39. CYAN SPORES
=====================================================================

Use 0–2 cyan spores per active segment or only on successful target contact. The teal accent suggests living fungal ecology without competing with violet energy.

=====================================================================
40. HIT VFX
=====================================================================

On a confirmed target hit, produce a compact violet fissure flash at feet/lower body, 3–6 dark root splinters, 2–4 violet sparks, and a brief flower-core pulse on the axe. No giant explosion or opaque smoke.

=====================================================================
41. ROOTED TARGET FEEDBACK
=====================================================================

While the short root state is active, show restrained dark root curls around the target's ankles and rare violet motes. Avoid an always-on particle fountain. Visual state must end when the gameplay effect ends.

=====================================================================
42. SOUND DESIGN
=====================================================================

Layer:
- heavy axe air displacement;
- deep wood/root strain;
- ground crack/thud;
- short violet arcane resonance.

Propagation can use quiet sequential root-crack sounds, not 12 full-volume impacts.

=====================================================================
43. ABILITY INPUT
=====================================================================

One right-click = one cast. No hold-to-charge. No repeated use ticks. Validate hand, cooldown, item stack and server side before execution.

=====================================================================
44. SERVER AUTHORITY
=====================================================================

Path seed, ground cells, hit detection, damage, root status, durability and cooldown are computed on the server. Clients render accepted world VFX only.

=====================================================================
45. NETWORKING
=====================================================================

Prefer one cast event containing origin/yaw/seed or accepted cell list rather than one packet per root particle. Gameplay damage should not depend on client reconstruction.

=====================================================================
46. MULTIPLE CASTERS
=====================================================================

Support multiple players using the ability simultaneously. Cast state must be isolated by unique cast ID/player. Never store a single global `currentRootWave`.

=====================================================================
47. DISCONNECT / WORLD CHANGE
=====================================================================

If scheduled propagation is used, cancel remaining layers if the world unloads, the caster disappears, or the cast becomes invalid. Remove cast state deterministically.

=====================================================================
48. NORMAL AXE ATTACKS REMAIN DISTINCT
=====================================================================

Left-click remains the polished heavy melee attack described earlier. It may use blade trails and violet hit sparks but must not automatically create Rootsnare Cleave. The RMB ability remains visually special.

=====================================================================
49. CHOPPING REMAINS DISTINCT
=====================================================================

Normal log/wood mining must not trigger the root wave. Preserve standard AxeItem block behavior, stripping/scraping interactions where relevant to the actual version/project, and normal durability.

=====================================================================
50. ENCHANTMENT COMPATIBILITY
=====================================================================

Sharpness/Smite/Bane/Unbreaking/Mending and other legal axe enchantments must continue to function. Ability damage should not accidentally invoke melee enchantment hooks multiple times unless intentionally designed once.

=====================================================================
51. MODEL REFINEMENT — CRESCENT BLADES
=====================================================================

The enormous dual crescent plates should read as fractured ancient material, with cold gray cutting edges, purple cracks and thickness visible in side view. Do not smooth them into identical semicircles.

=====================================================================
52. MODEL REFINEMENT — ROOT HEART
=====================================================================

The central root mass should look structurally grown around the axe eye. Roots twist across front/back, split into thorns and support the large violet flower. Preserve negative space so the flower does not disappear in visual clutter.

=====================================================================
53. MODEL REFINEMENT — HANDLE
=====================================================================

The handle is a braided living trunk, not a cylinder with bark texture. Use several low-poly root strands with varying twist and occasional thorns, all converging cleanly into the square pommel.

=====================================================================
54. TEXTURE REFINEMENT
=====================================================================

Keep plate interiors near-black, bevels cold gray, roots dark umber, fissures deep violet with tiny hot cores, cyan fungus sparse, and flowers rich purple. No large neon surfaces.

=====================================================================
55. FIRST-PERSON ABILITY POSE
=====================================================================

Because the head is huge, move it down/sideways during wind-up and reveal the target corridor. On release, a brief center-screen cleave is acceptable, but the player must immediately regain clear vision.

=====================================================================
56. THIRD-PERSON ABILITY POSE
=====================================================================

The player should visibly brace and drive the axe toward the ground/forward direction. If the project has arm posing, use it; otherwise tune item transforms/GeckoLib root motion without introducing a new dependency.

=====================================================================
57. CAMERA EFFECT
=====================================================================

Optional tiny local camera impulse at the release frame if a project camera-shake system already exists. Never add aggressive screen shake or create a new dependency solely for this effect.

=====================================================================
58. PERFORMANCE BUDGET
=====================================================================

A 12-block bounded wave is small. Generate cells once, query entities in a conservative swept box, filter against active cells/layers, and use lightweight particles. Do not perform a full-radius entity scan for every cell.

=====================================================================
59. CODE ARCHITECTURE
=====================================================================

Keep `DarkForestAxeItem` focused. A `RootsnareCleaveAbility`, `GroundWavePathGenerator`, and `RootedEffectHelper` are appropriate if no project equivalents exist. Avoid giant common/client mixed classes.

=====================================================================
60. CONSTANTS / CONFIG
=====================================================================

Centralize wave length, width, lateral variance, cooldown, damage, root duration, durability cost and propagation speed. Clamp configuration to safe maxima.

=====================================================================
61. TEST — FLAT GROUND
=====================================================================

Cast repeatedly on flat ground. The path should always move forward, vary subtly left/right, remain bounded, and propagate visibly rather than appear all at once.

=====================================================================
62. TEST — SLOPES / STEPS
=====================================================================

Test one-block rises, drops and uneven forest terrain. The wave should follow small changes but stop/skip unreasonable cliffs and walls without floating high in the air.

=====================================================================
63. TEST — WALL
=====================================================================

Place targets behind a thick wall. They must not be damaged/rooted if the root wave cannot physically reach them according to the chosen obstruction rule.

=====================================================================
64. TEST — MULTIPLE TARGETS
=====================================================================

Place several mobs across multiple cells including one large entity. Every eligible target should be affected once, not once per occupied cell.

=====================================================================
65. TEST — PVP / IMMUNITY
=====================================================================

Test teammates, PvP-disabled conditions, boss/immune entities, flying mobs and spectators. Root state must respect game rules and never permanently corrupt movement.

=====================================================================
66. TEST — COOLDOWN / DURABILITY
=====================================================================

Spam RMB, switch items during cast, use a nearly broken axe, disconnect mid-wave. No duplicate wave, negative durability or stale scheduler state.

=====================================================================
67. ANIMATION QA
=====================================================================

Attack, crit, chop, rootsnare and idle must transition without snaps. Root-heart flower brightness must return to baseline after interrupted casts.

=====================================================================
68. RESOURCE / SERVER QA
=====================================================================

Test geo/animation JSON, emissive layer if used, particles, sounds, GUI/drop/glint, resource reload, multiplayer and dedicated server. No client renderer class may be loaded in common server code.

=====================================================================
69. ABILITY DEFINITION OF DONE
=====================================================================

[ ] one RMB cast;
[ ] bounded forward irregular ground path;
[ ] wall behavior correct;
[ ] no terrain destruction;
[ ] one damage event per target;
[ ] short root state works;
[ ] cooldown/durability work;
[ ] propagation VFX/sound are controlled;
[ ] multiplayer synchronization works;
[ ] no performance spikes.

=====================================================================
70. FINAL AXE DEFINITION OF DONE
=====================================================================

The finished axe must match the concept at model/material level, remain a fully functional AxeItem, have deeply polished normal attack effects, and deliver Rootsnare Cleave as a distinctive living-forest control mechanic. Do not report success until all four layers—asset, combat, ability and technical safety—work together in-game.

```

---

# 4. Dark Forest Shovel

![Dark Forest Shovel concept](concept_art/dark_forest_shovel.png)

```text
# =====================================================================
# MASTER PRODUCTION PROMPT — DARK FOREST SHOVEL
# Minecraft Fabric 1.20.1 + GeckoLib 4.x
# Full 3D model + texture + rig + digging/path VFX + code
# =====================================================================

Act as a senior Fabric/GeckoLib developer and production Blockbench artist. Recreate the supplied DARK FOREST SHOVEL as a fully functional animated 3D shovel.

REFERENCE FILES:
- concept_art/dark_forest_shovel.png
- concept_art/dark_forest_full_set.png

Inspect exact project versions, existing model architecture, tool materials, particles and any skills/lore files first. Use only correct Fabric 1.20.1 / installed GeckoLib APIs.

=====================================================================
1. ITEM IDENTITY
=====================================================================

Recommended ID:
    dark_forest_shovel

This shovel resembles a massive ancient leaf/shield made from fractured dark plates, grown into a living root shaft.

The shovel-specific visual motif is:
BLACK LEAF-SHAPED BLADE
+ CENTRAL VIOLET BRANCH/FISSURE
+ ROOT VEINS
+ LARGE PURPLE FLOWER AT BLADE BASE
+ TWISTED ROOT HANDLE.

It should feel like a sacred digging implement from a moonlit haunted forest, not a normal iron shovel.

=====================================================================
2. HEAD SILHOUETTE
=====================================================================

The shovel head is broad, tall and pointed at the top, with a shape reminiscent of a dark leaf or stylized shield.

It should taper toward the shaft at the bottom.

The left/right sides are approximately balanced but the segmented plate structure and roots create organic asymmetry.

The upper point must remain sharp and clearly readable.

=====================================================================
3. HEAD PLATE CONSTRUCTION
=====================================================================

Build the shovel head from several large dark plate panels arranged like leaf segments.

Suggested:
- central plate/spine;
- left upper plate;
- left lower plate;
- right upper plate;
- right lower plate;
- outer edge bevel;
- lower socket/root transition.

Each plate should have subtle depth differences and cold gray edge highlights.

The head must have real thickness. No flat plane.

=====================================================================
4. CENTRAL VIOLET LEAF VEIN / FISSURE
=====================================================================

A major violet line runs from the upper center downward, branching like a leaf vein/tree branch.

This is both a crack in the black material and a magical visual motif.

The line should:
- follow the vertical axis;
- split into a few controlled branches;
- remain recessed/inset;
- glow strongest near intersections and the lower flower.

Use dark indigo edges and brighter violet core. Keep emission localized if available.

=====================================================================
5. ROOT OVERGROWTH
=====================================================================

Dark roots emerge from the lower blade and creep upward along some plate seams.

They should appear to hold the blade together and connect directly into the handle.

Include a few thorny protrusions but do not obscure the broad leaf silhouette.

=====================================================================
6. LARGE LOWER FLOWER
=====================================================================

At the lower blade near the shaft connection, create the prominent purple flower from the reference.

It should be a physical modeled focal point with 5–7 petals, dark indigo edges and a luminous lavender center.

Around it, small cyan fungal/spore clusters can appear in the root recesses.

=====================================================================
7. HANDLE
=====================================================================

Use the common Dark Forest root handle:
- multiple twisted dark roots;
- black-brown bark;
- gray-brown raised ridges;
- sparse violet flowers;
- sparse cyan fungal strings.

Keep a clean grip region.

=====================================================================
8. POMMEL
=====================================================================

Square dark forest-brick/metal pommel with central purple flower emblem. Raised border blocks and root integration are required.

=====================================================================
9. MATERIALS / TEXTURE
=====================================================================

Preferred 256x256 texture unless project uses another standard.

Head material:
- charcoal black;
- dark graphite;
- cold slate;
- worn silver-gray edges.

Roots:
- deep black-brown;
- walnut-gray highlights.

Magic:
- violet primary;
- lavender focal highlights;
- cyan/teal minor biology accents.

Avoid photorealism, muddy noise and neon saturation.

=====================================================================
10. UV
=====================================================================

Highest priority:
- shovel head front/back;
- central violet vein;
- lower flower/root region;
- handle;
- pommel.

Do not mirror all root wear perfectly.

=====================================================================
11. BONE HIERARCHY
=====================================================================

Recommended:

root
└── shovel
    ├── head
    │   ├── head_plates
    │   ├── edge
    │   ├── root_veins
    │   ├── main_flower
    │   └── fissure_fx
    ├── handle
    │   ├── root_grip
    │   ├── fungal_growth
    │   └── small_flowers
    ├── pommel
    │   └── pommel_flower
    └── fx
        └── fx_head

=====================================================================
12. ANIMATIONS
=====================================================================

Create:
- animation.dark_forest_shovel.idle
- animation.dark_forest_shovel.equip
- animation.dark_forest_shovel.dig
- animation.dark_forest_shovel.attack

Idle: essentially static; tiny flower/fissure pulse.

Equip: short controlled rise.

Dig: controlled downward digging motion coordinated with Minecraft hand animation. The broad head should visibly move into the ground-contact direction without passing through the camera.

Attack: restrained tool swing, less dramatic than sword/axe.

=====================================================================
13. DIGGING VFX
=====================================================================

When breaking shovel-effective blocks:
- preserve vanilla dirt/sand/gravel/snow particles;
- add only 1–3 violet motes;
- occasional tiny cyan spore;
- brief blade-vein pulse.

Do not create a magical explosion for every dirt block.

When creating a dirt path through standard ShovelItem right-click behavior, add only a tiny root/flower pulse and a few ground motes if desired.

=====================================================================
14. GAMEPLAY
=====================================================================

Use correct Fabric/Yarn 1.20.1 ShovelItem behavior or the project's existing base.

Preserve:
- shovel-effective blocks;
- normal mining behavior;
- path creation/right-click interactions;
- durability;
- appropriate enchantments.

MANDATORY UNIQUE ABILITY: NIGHTROOT EXCAVATION. Right-clicking a valid shovel-mineable surface performs a controlled 5x5 one-layer excavation centered on the clicked block. Only blocks that the shovel is genuinely allowed to harvest are broken; drops, enchantments, durability, protection hooks, block entities, world border, and loaded-chunk safety must be respected. It is an area-tool action, not an explosion.

Reuse existing Dark Forest ToolMaterial if present.

=====================================================================
15. FIRST / THIRD PERSON
=====================================================================

The broad head can obstruct vision. Tune first-person scale and angle so the leaf-shaped profile remains visible while the crosshair stays clear.

Third-person hand must grip the root shaft naturally. Test digging, running, sneaking and attacking.

=====================================================================
16. REFERENCE CHECKLIST
=====================================================================

[ ] tall pointed leaf/shield shovel head;
[ ] segmented black plate panels;
[ ] cold gray cutting/outer edges;
[ ] central branching violet fissure;
[ ] dark root veins on blade;
[ ] large purple flower near blade base;
[ ] cyan fungal/spore accents;
[ ] twisted root handle;
[ ] small flowers;
[ ] square flower pommel.

=====================================================================
17. QA
=====================================================================

Test dirt, grass, sand, gravel, snow, path creation, wrong-tool blocks, enchantments, durability, first/third person, GUI/drop, animations, multiplayer, resource reload and dedicated-server safety.

Run Gradle build and runClient and fix all discovered errors before completion.

=====================================================================
18. UNIQUE ABILITY — NIGHTROOT EXCAVATION
=====================================================================

The Dark Forest Shovel has a mandatory area-tool ability called NIGHTROOT EXCAVATION.

Trigger: right-click a valid shovel-mineable surface block. One accepted use excavates a 5x5 horizontal square centered on the clicked block at the same Y level, breaking only blocks that the shovel may legitimately harvest.

This is controlled area digging, not an explosion.

=====================================================================
19. EXACT AREA
=====================================================================

Radius = 2 blocks on X and Z.
Candidate offsets: -2, -1, 0, +1, +2.
Maximum candidates = 25.
Only the clicked Y plane is considered by default.

Do not accidentally implement 7x7, 5x5x5, a sphere or a rotated diamond.

=====================================================================
20. CENTER VALIDATION
=====================================================================

The area ability should begin only when the directly clicked center block is a valid shovel-use/mining target according to project rules. Clicking stone should not secretly excavate nearby dirt two blocks away.

=====================================================================
21. TOOL SUITABILITY PER BLOCK
=====================================================================

Every candidate is validated independently. Dirt, sand, gravel, clay, snow and other legitimate shovel-mineable blocks may qualify according to actual tags/tool logic. Stone, containers and unrelated materials are skipped.

=====================================================================
22. NO BLIND `setBlockState(AIR)`
=====================================================================

Break blocks using normal server mining semantics so drops, experience, callbacks and mod hooks remain correct. Do not directly erase 25 blocks and manually guess drops.

=====================================================================
23. ENCHANTMENT COMPATIBILITY
=====================================================================

Silk Touch/Fortune behavior where applicable, Unbreaking, Mending and Efficiency must remain valid. Area breaking must not duplicate enchantment application or XP.

=====================================================================
24. DURABILITY MODEL
=====================================================================

Consume normal durability per successfully broken block. Invalid/protected/skipped candidates cost nothing. If the shovel breaks after N successful blocks, stop and leave remaining candidates untouched.

=====================================================================
25. CREATIVE MODE
=====================================================================

Follow standard project conventions: area excavation works, but durability normally is not consumed. Keep cooldown behavior consistent with the intended gameplay even in creative if necessary for effect spam control.

=====================================================================
26. COOLDOWN
=====================================================================

Recommended short cooldown: 3–5 seconds. Because the action can remove 25 blocks at once, a small cooldown prevents macros from becoming extreme terrain deletion while preserving tool usability.

Only successful area excavation starts cooldown.

=====================================================================
27. BLOCK ENTITY / INVENTORY SAFETY
=====================================================================

Never mass-break chests, barrels, shulker boxes or arbitrary block entities merely because a tag is misconfigured. Use mining tags plus explicit safety/normal break semantics. If uncertain, skip blocks with sensitive block entities.

=====================================================================
28. PROTECTION HOOKS
=====================================================================

Respect world protection, claims, spawn rules and existing block-break event systems. The area action must not bypass protected blocks by modifying world state beneath normal interaction hooks.

=====================================================================
29. CHUNK SAFETY
=====================================================================

Do not force-load chunks. The 5x5 is tiny; if edge candidates lie in unloaded chunks, skip them rather than triggering loads/generation.

=====================================================================
30. WORLD BORDER / HEIGHT
=====================================================================

Validate candidates against world border and build limits. Never read invalid coordinates.

=====================================================================
31. BREAK ORDER
=====================================================================

Recommended: center-outward ring order. This provides predictable low-durability behavior and matches the visual fantasy of roots spreading from the shovel impact.

=====================================================================
32. SERVER AUTHORITY
=====================================================================

Candidate calculation, break legality, actual block breaking, drops, durability and cooldown happen on the logical server. The client never performs speculative block removal.

=====================================================================
33. ABILITY ANIMATION
=====================================================================

Create `animation.dark_forest_shovel.nightroot_excavate`. It should be a stronger version of the normal dig: short lift, root tension through handle, decisive downward press, head fissure/flower flash, ground pulse, recovery.

Keep it under roughly 0.7 seconds.

=====================================================================
34. GROUND VFX CONCEPT
=====================================================================

At impact, send a dark-violet root pulse outward from center across the 5x5. Do not draw a perfect glowing square. Use broken root-like streaks that briefly connect only successful candidate positions.

=====================================================================
35. PER-BLOCK VFX BUDGET
=====================================================================

Because up to 25 blocks can break, keep custom VFX per block minimal: 0–2 violet sparks, occasional cyan spore, plus the block's normal break particles. Prefer one global center pulse over 25 elaborate effects.

=====================================================================
36. SOUND DESIGN
=====================================================================

Use one dominant impact/dig sound for the cast: deep soil crunch + root strain + muted arcane pulse. Do not play the normal full break sound 25 times at full volume if the engine already creates enough block feedback.

=====================================================================
37. HEAD FLOWER RESPONSE
=====================================================================

The large violet flower near the shovel head should flare at the impact frame and fade quickly. Small handle/pommel flowers may answer with a delayed low-intensity pulse.

=====================================================================
38. CYAN FUNGAL RESPONSE
=====================================================================

Tiny cyan spores may rise from the excavated soil, especially from organic blocks. Keep them rare. Never turn sand/gravel excavation into a cyan particle storm.

=====================================================================
39. NO AREA DAMAGE
=====================================================================

The 5x5 ability breaks eligible blocks only. It must not damage entities, knock mobs away, or create explosions. Entities standing in the area continue to obey normal block-fall physics after blocks are removed.

=====================================================================
40. NO VERTICAL SHAFT
=====================================================================

Only the clicked Y layer is processed. Do not excavate downward multiple layers or create a quarry column. Players can use the ability repeatedly if they intentionally want to descend.

=====================================================================
41. NO AUTOMATIC TERRAIN FOLLOWING
=====================================================================

The base behavior uses one horizontal plane. Small height differences are not automatically searched. This keeps 5x5 cuts predictable. If the project later requests terrain-following, implement it as a separate explicit feature.

=====================================================================
42. INTERACTION WITH PATH CREATION
=====================================================================

`ShovelItem` has right-click path behavior, creating an input conflict. Resolve intentionally. Recommended: normal RMB on a valid excavatable block invokes Nightroot Excavation; Sneak+RMB can preserve vanilla path creation, or vice versa according to project UX conventions. Document the chosen mapping clearly.

=====================================================================
43. INTERACTION FAILURE
=====================================================================

If the clicked center is not eligible for area excavation, fall back to normal shovel use/path interaction rather than consuming the click with nothing. Do not start cooldown or durability cost on a complete failure.

=====================================================================
44. NORMAL DIGGING REMAINS AVAILABLE
=====================================================================

Left-click block mining still behaves like a standard shovel. The special area action is only the contextual right-click mechanic and must not globally change all block-break events into 5x5 behavior.

=====================================================================
45. NORMAL MELEE REMAINS AVAILABLE
=====================================================================

Entity attack remains normal tool melee with the restrained VFX described earlier. Nightroot Excavation never triggers on entity hits.

=====================================================================
46. MODEL REFINEMENT — LEAF HEAD
=====================================================================

The tall leaf/shield-shaped head must retain a clear cold gray cutting perimeter, dark segmented inner plates, branching violet fissure and root veins. It should look heavy enough to excavate, not like a decorative shield attached to a stick.

=====================================================================
47. MODEL REFINEMENT — FLOWER BASE
=====================================================================

The large purple flower near the blade base should sit physically among roots, with several distinct petals and a recessed luminous core. Keep it below the widest plate region so it does not obscure the head silhouette.

=====================================================================
48. MODEL REFINEMENT — HANDLE
=====================================================================

Build the handle from twisted roots with visible strand hierarchy, bark facets and occasional thorns. Cyan growth should appear in small clusters where roots overlap, implying moisture and age.

=====================================================================
49. TEXTURE REFINEMENT
=====================================================================

Use matte charcoal plate faces, metallic/cold-stone bevels, deep brown roots, violet crack cores, rare cyan fungus and purple flowers. Maintain set consistency with sword/pickaxe/axe.

=====================================================================
50. FIRST-PERSON ABILITY POSE
=====================================================================

During area excavation, lower the head toward the target without putting the broad plate directly over the crosshair for the entire animation. The contact frame can briefly dominate the lower-center view, then recover quickly.

=====================================================================
51. THIRD-PERSON ABILITY POSE
=====================================================================

The character should visibly drive the shovel down/forward. Avoid a combat slash pose. If player arm animation is unavailable, item motion still must clearly communicate digging.

=====================================================================
52. GUI / DROPPED PRESENTATION
=====================================================================

The broad head and purple flower need enough scale in GUI to remain readable while still fitting the entire tool. Dropped form should show the leaf silhouette and root handle rather than lying edge-on invisible.

=====================================================================
53. PERFORMANCE BUDGET
=====================================================================

25 bounded candidate checks are trivial. Do not introduce asynchronous workers, global scans or complex schedulers. The primary performance risk is particle/sound spam, so keep effects aggregate and bounded.

=====================================================================
54. CODE ARCHITECTURE
=====================================================================

A small `NightrootExcavationHelper` may own radius iteration, validation, break ordering and success count. `DarkForestShovelItem` should handle input and animation triggers, not contain unrelated renderer/particle code.

=====================================================================
55. CONSTANTS / CONFIG
=====================================================================

Centralize AREA_RADIUS=2, AREA_SIZE=5, MAX_CANDIDATES=25, cooldown and any ability durability surcharge. If project config exists, clamp area radius to safe bounds.

=====================================================================
56. TEST — FULL 5x5 DIRT
=====================================================================

Prepare a flat 5x5 area of shovel-mineable blocks and trigger the ability at center. All 25 eligible candidates should break with correct drops/durability if tool survives.

=====================================================================
57. TEST — OUTER RING
=====================================================================

Place additional eligible blocks at distance 3 from center. They must remain untouched. This catches accidental 7x7/off-by-one implementation.

=====================================================================
58. TEST — MIXED MATERIALS
=====================================================================

Mix dirt, sand, gravel, stone, chest, farmland and water within 5x5. Only legitimate safe shovel targets should break.

=====================================================================
59. TEST — LOW DURABILITY
=====================================================================

Use a shovel with only a few durability points left. Verify it stops when broken and remaining candidate blocks stay intact.

=====================================================================
60. TEST — ENCHANTMENTS
=====================================================================

Verify Unbreaking durability behavior and Silk Touch/Fortune where relevant to the block types. Compare representative drops to normal mining.

=====================================================================
61. TEST — PROTECTION
=====================================================================

Protect one or more blocks in the area. Those positions should remain untouched while allowed blocks may proceed according to server rules. No claim bypass.

=====================================================================
62. TEST — CHUNK EDGE / WORLD BORDER
=====================================================================

Use the ability near a loaded-chunk edge and world border. It must not force-load remote chunks or throw errors.

=====================================================================
63. TEST — INPUT CONFLICT
=====================================================================

Verify the chosen RMB/Sneak+RMB mapping allows both area excavation and vanilla path creation in a predictable way. Tooltips/documentation should match actual controls.

=====================================================================
64. TEST — MULTIPLAYER
=====================================================================

Two players observe the same 5x5 break. All clients receive normal block updates once, effects do not duplicate, and cooldown/durability stay server-authoritative.

=====================================================================
65. ANIMATION QA
=====================================================================

Idle/equip/dig/attack/nightroot_excavate transitions must not snap or restart every tick. Head flower intensity must return to baseline after canceled/failed casts.

=====================================================================
66. SOUND / PARTICLE QA
=====================================================================

Repeatedly excavate full 5x5 areas and assess FPS/TPS and audio. The result should feel powerful without sounding like 25 simultaneous explosions or filling the screen with particles.

=====================================================================
67. RESOURCE QA
=====================================================================

Check model paths, animation identifiers, particle textures, sounds.json, lang, GUI, ground, glint, resource reload and dedicated-server safety.

=====================================================================
68. ABILITY DEFINITION OF DONE
=====================================================================

[ ] contextual RMB works;
[ ] exact 5x5 same-Y candidate area;
[ ] center validation works;
[ ] only legitimate shovel blocks break;
[ ] drops/enchantments/protection work;
[ ] durability is per successful block;
[ ] tool break stops processing;
[ ] cooldown works;
[ ] VFX/sound are bounded;
[ ] no area damage/explosion.

=====================================================================
69. VISUAL DEFINITION OF DONE
=====================================================================

The shovel must remain faithful to its tall pointed leaf-head concept: segmented black plate, cold edge, violet branching seam, root veins, large base flower, cyan fungal details, living-root handle and flower pommel. The ability may not overshadow this design language.

=====================================================================
70. FINAL SHOVEL DEFINITION OF DONE
=====================================================================

Do not report success until the item works as a real Fabric 1.20.1 ShovelItem and Nightroot Excavation behaves like a bounded, legitimate 5x5 area tool with correct drops, durability, multiplayer synchronization and Dark Forest audiovisual identity.

```

---

# 5. Dark Forest Hoe

![Dark Forest Hoe concept](concept_art/dark_forest_hoe.png)

```text
# =====================================================================
# MASTER PRODUCTION PROMPT — DARK FOREST HOE
# Minecraft Fabric 1.20.1 + GeckoLib 4.x
# Full 3D model + texture + rig + tilling VFX + vanilla HoeItem behavior
# =====================================================================

Act as a senior Minecraft Fabric 1.20.1 developer, GeckoLib specialist, Blockbench artist, low-poly prop designer, texture artist, animator, VFX designer and QA engineer.

Recreate the supplied DARK FOREST HOE as a complete production-ready item.

REFERENCE FILES:
- concept_art/dark_forest_hoe.png
- concept_art/dark_forest_full_set.png

Inspect the actual project, exact versions, existing Dark Forest assets, ToolMaterial, renderers and any skills/lore documentation before implementation. Use only APIs compatible with the installed Fabric/Yarn/GeckoLib environment.

=====================================================================
1. ITEM IDENTITY
=====================================================================

Recommended ID:
    dark_forest_hoe

This is not a normal flat farm hoe. Its head is an eerie hooked/C-shaped structure grown from ancient thorn roots and dark blocky cutting plates.

Visual identity:
LIVING ROOT HOOK
+ BLOCKY BLACK WORKING PLATES
+ THORNS
+ VIOLET ENERGY
+ CYAN FUNGAL GROWTH
+ NIGHT FLOWERS.

It should clearly belong to the same set while remaining immediately recognizable as the hoe.

=====================================================================
2. HEAD SILHOUETTE
=====================================================================

The concept head bends forward and downward in a large hook/C profile.

The rear/upper arc is formed primarily by twisted thorny roots. Along the working side/end, dark rectangular metal/stone plate segments are attached like heavy cultivation teeth/blades.

Do not turn this into:
- a scythe;
- a sickle weapon;
- a pickaxe;
- a shepherd hook;
- a simple L-shaped vanilla hoe.

The shape must read as an agricultural tool with a supernatural hooked working head.

=====================================================================
3. ROOT ARC
=====================================================================

Build the upper curved structure from several major root sections that form one continuous arc.

Use:
- thick base root near shaft;
- middle curved root section;
- upper/forward bend;
- several thorn points;
- branch transitions into metal working segments.

Do not use one smooth high-poly tube. Use stylized low-poly root geometry with visible bark planes.

The root arc should look strong enough to support the metal plates.

=====================================================================
4. WORKING METAL PLATES
=====================================================================

The concept shows dark block-like plate elements along the forward/downward working end.

These should resemble ancient black cultivation teeth or a segmented dark blade.

Build actual 3D cuboid/wedge plates with:
- charcoal faces;
- cold gray edges;
- violet seams in selected joints;
- slight individual angular differences while maintaining a coherent tool edge.

Keep enough thickness for believable ground contact.

=====================================================================
5. VIOLET SEAMS
=====================================================================

Purple energy should appear selectively between some dark plate segments and inside cracks where root meets metal.

Do not make every joint bright purple.

Use deep indigo → violet → lavender hotspot hierarchy.

=====================================================================
6. THORNS
=====================================================================

Several dark root thorns should project outward from the upper arc and around the shaft/head transition.

Keep them directional and structural, not random noise. Avoid creating spikes near the exact hand-grip zone.

=====================================================================
7. CYAN BIOLOGICAL GROWTH
=====================================================================

Use small cyan/teal fungal clusters especially along the inner root curve and upper handle.

They can be represented as:
- tiny emissive dots;
- thin fungal filaments;
- small clustered growth.

Cyan is secondary; violet remains the set's main magical color.

=====================================================================
8. PURPLE FLOWERS
=====================================================================

Place several small night flowers on the handle and possibly near the head arc. The pommel carries the common central flower motif.

Flowers should use real geometry for major blossoms, not flat decals.

=====================================================================
9. HANDLE
=====================================================================

Continue the set's twisted living-root shaft:
- multiple intertwined dark roots;
- thorn remnants;
- bark ridge shading;
- sparse cyan fungus;
- small purple flowers.

Keep a clear physical grip zone.

=====================================================================
10. POMMEL
=====================================================================

Create the set's square dark block pommel with a purple flower center and raised border. Blend the handle roots naturally into the top of the pommel.

=====================================================================
11. MATERIAL / TEXTURE STYLE
=====================================================================

Preferred 256x256 unless project convention differs.

Black plates:
- charcoal;
- graphite;
- slate-blue shadows;
- cold gray worn edges.

Roots:
- black-brown;
- deep walnut;
- muted gray-brown highlights.

Violet:
- indigo recess;
- saturated violet;
- lavender highlight.

Cyan:
- dark teal;
- aqua specks.

Keep all textures crisp and pixel-art compatible. No photographic bark or generic procedural noise.

=====================================================================
12. UV
=====================================================================

Prioritize:
1. head hook/root arc;
2. metal working plates;
3. violet seams;
4. handle;
5. pommel flower.

Do not perfectly mirror all organic root details.

=====================================================================
13. BONE HIERARCHY
=====================================================================

Recommended:

root
└── hoe
    ├── head
    │   ├── root_arc
    │   ├── working_plates
    │   ├── head_thorns
    │   └── violet_fx
    ├── handle
    │   ├── root_grip
    │   ├── fungal_growth
    │   └── small_flowers
    ├── pommel
    │   └── pommel_flower
    └── fx
        └── fx_head

=====================================================================
14. REQUIRED ANIMATIONS
=====================================================================

Create:
- animation.dark_forest_hoe.idle
- animation.dark_forest_hoe.equip
- animation.dark_forest_hoe.till
- animation.dark_forest_hoe.attack

Idle: nearly static with minute flower/violet pulse.

Equip: controlled short movement.

Till: agricultural downward/forward contact motion, not a combat spin. Let the hook working edge visibly move toward soil.

Attack: restrained emergency melee swing.

=====================================================================
15. TILLING VFX
=====================================================================

When a normal vanilla hoe transformation succeeds:
- preserve recognizable soil feedback;
- spawn a few dark-earth particles if appropriate;
- 1–3 tiny violet motes;
- optional single cyan spore;
- short head seam/flower pulse.

No explosion. No lightning. No giant root eruption.

Do not play sound or effects repeatedly when the block cannot be tilled.

=====================================================================
16. GAMEPLAY — IMPORTANT
=====================================================================

Implement as a correct Fabric/Yarn 1.20.1 HoeItem or existing custom hoe base.

Preserve actual vanilla 1.20.1 hoe transformations, special dirt cases, durability and appropriate enchantments.

The Dark Forest Hoe keeps normal vanilla-scale tilling on ordinary tillable terrain. It ALSO has one unique contextual ability: NIGHT BLOOM. When right-clicking existing farmland/crops rather than an untilled dirt target, the hoe releases a bounded 7x7 nocturnal growth pulse that applies legitimate bone-meal-style growth attempts to eligible crops/plants. It must not auto-harvest, auto-replant, create drops from nothing, bypass crop growth rules, or affect arbitrary blocks. Normal hoe tilling remains available and must not be replaced.

=====================================================================
17. FIRST-PERSON / THIRD-PERSON
=====================================================================

The hooked head is unusual and must be tuned so it does not cover the crosshair.

First person:
- handle from lower-right;
- head visible at upper/right region;
- inner hook shape readable;
- working plate orientation points logically toward terrain during till animation.

Third person:
- hand grips root shaft;
- hook does not clip excessively into torso/head;
- till animation is readable.

Test GUI/drop/item-frame/glint as relevant.

=====================================================================
18. PERFORMANCE / SAFETY
=====================================================================

No constant particle aura. No client-side block modification. Standard tilling remains server authoritative through normal item logic.

Renderer/model classes remain client-only and dedicated-server safe.

=====================================================================
19. REFERENCE CHECKLIST
=====================================================================

[ ] large C/hook-shaped head;
[ ] head arc formed by ancient roots;
[ ] blocky dark metal/stone working plates;
[ ] violet seams/cracks;
[ ] thorn protrusions;
[ ] cyan fungal accents;
[ ] twisted root handle;
[ ] small violet flowers;
[ ] square flower pommel;
[ ] visual consistency with all other Dark Forest tools.

=====================================================================
20. QA
=====================================================================

Test all vanilla hoe transformations relevant to Minecraft 1.20.1, invalid blocks, durability, enchantments, first/third person, till animation, attack, resource reload, multiplayer and dedicated server.

Run the actual Gradle build and runClient. Fix every compile/resource/runtime error before completion.

=====================================================================
21. UNIQUE CONTEXTUAL ABILITY — NIGHT BLOOM
=====================================================================

The Dark Forest Hoe has a mandatory contextual ability called NIGHT BLOOM.

Normal right-click on ordinary tillable terrain still performs normal vanilla-scale hoe tilling. When right-clicking existing farmland/crop context, the tool releases a nocturnal growth pulse over a bounded 7x7 horizontal area centered on the clicked block.

The ability attempts legitimate bone-meal-style growth on eligible crops/plants. It does NOT auto-harvest or create drops.

=====================================================================
22. EXACT AREA
=====================================================================

Night Bloom candidate area:
- radius = 3 on X/Z;
- size = 7x7;
- max horizontal candidates = 49;
- same general crop/farmland level, with plant block usually one block above farmland.

Do not turn it into a sphere or world-wide farm buff.

=====================================================================
23. CONTEXTUAL INPUT RESOLUTION
=====================================================================

Input rule must be intuitive:
1. if clicked block is a normal tillable dirt-type target, preserve standard HoeItem tilling;
2. if clicked context is farmland, crop or eligible growable plant, attempt Night Bloom;
3. otherwise fall back to normal/PASS behavior.

This prevents the ability from replacing basic farming functionality.

=====================================================================
24. NO AUTO-HARVEST
=====================================================================

Night Bloom never breaks mature crops, never collects produce, never replants seeds and never transfers items to inventory. Its sole farming effect is growth acceleration via legitimate plant growth semantics.

=====================================================================
25. BONE-MEAL SEMANTICS
=====================================================================

Where practical, use the block's existing fertilizable/bone-meal interfaces or the project's canonical growth helper. Do not directly set wheat `AGE=7` or guess property names across modded crops.

Each candidate receives a bounded number of legitimate growth attempts.

=====================================================================
26. MODDED CROP COMPATIBILITY
=====================================================================

Prefer generic Fertilizable/growable interfaces and tags rather than hard-coded vanilla crop classes. If a modded plant intentionally rejects bone meal, Night Bloom must respect that behavior.

=====================================================================
27. GROWTH ATTEMPT COUNT
=====================================================================

Recommended: one successful bone-meal-style growth attempt per eligible plant per cast. Do not loop until every crop is mature. This keeps the ability powerful but not an instant guaranteed maturity cheat.

If the project explicitly wants stronger growth later, expose attempts as a bounded constant.

=====================================================================
28. RANDOMNESS
=====================================================================

Use server-side world random according to the plant's existing growth method. Clients must not independently decide stages. Every player should observe the same resulting crops.

=====================================================================
29. ELIGIBLE PLANTS
=====================================================================

Typical eligible examples may include crops and fertilizable plants that legitimately respond to bone meal. Do not assume cactus, chorus, saplings, mushrooms or modded plants all use identical rules—query actual interfaces/behavior.

=====================================================================
30. FARMLAND SAFETY
=====================================================================

Do not replace farmland, reset moisture or modify soil blocks unnecessarily. Night Bloom primarily targets the plants above/around farmland. Existing crop blocks remain in place and only their legitimate growth state changes.

=====================================================================
31. NO FREE ITEM GENERATION
=====================================================================

Because no harvesting occurs, the ability must not spawn seeds, crops, flowers or bone meal items. All output remains potential future harvest from legitimately grown plants.

=====================================================================
32. COOLDOWN
=====================================================================

Recommended cooldown: 15–20 seconds. The effect covers up to 49 positions, so it needs a meaningful cooldown. Start it only if at least one plant actually accepts a growth action.

=====================================================================
33. DURABILITY COST
=====================================================================

Recommended fixed ability durability cost: 4–8 points once per successful cast, not per crop. Normal tilling still consumes normal hoe durability according to vanilla semantics.

If the project prefers per-plant cost, cap it aggressively; do not allow a full 49 durability loss unexpectedly without explicit design.

=====================================================================
34. SERVER AUTHORITY
=====================================================================

Area resolution, fertilizable checks, random growth calls, durability and cooldown all execute on the logical server. Client side is visual only.

=====================================================================
35. PROTECTION / CLAIMS
=====================================================================

If the server/project has interaction protection, respect it. Growth should not be applied to crops the player is not allowed to interact with where such hooks exist.

=====================================================================
36. CHUNK SAFETY
=====================================================================

Do not force-load neighboring chunks. The 7x7 is small; skip unloaded edge positions if necessary.

=====================================================================
37. NIGHT BLOOM ANIMATION
=====================================================================

Create `animation.dark_forest_hoe.night_bloom`. Motion: the hooked head draws inward, root coils tighten, the head fissures/flowers illuminate, and the player performs a gentle forward/downward sweep as the bloom pulse spreads.

It should feel ritualistic but quick—roughly 0.6–0.9 seconds.

=====================================================================
38. HOOK HEAD VISUAL RESPONSE
=====================================================================

The C-shaped head should appear to "close" energy around the inner arc through emissive progression rather than physically bending metal. Purple seams illuminate from the handle-side root base toward the working plates.

=====================================================================
39. FLOWER SEQUENCE
=====================================================================

Pommel flower → small handle flowers → head flower clusters should pulse upward in sequence. At release, a brief larger violet flower shape may appear near the clicked crop center.

=====================================================================
40. GROUND / CROP VFX
=====================================================================

Create a low, expanding wave of dark-violet root wisps across the 7x7. Successful plants emit 1–2 violet petal motes and an occasional cyan spore. Do not cover every crop with a large particle column.

=====================================================================
41. VISUAL GROWTH FEEDBACK
=====================================================================

Let the actual block-state change be the main feedback. Additional VFX should be small enough that players can see crops grow. Avoid opaque effects that hide the field.

=====================================================================
42. SOUND DESIGN
=====================================================================

Use one central nocturnal bloom sound: soft root creak, soil resonance, reversed/airy forest breath and delicate purple flower chime. Avoid loud thunder or combat impacts.

=====================================================================
43. NO CONSTANT AURA
=====================================================================

The hoe does not emit a persistent farm aura. Particles occur mainly during Night Bloom and ordinary tilling contact. Idle remains subtle.

=====================================================================
44. NORMAL TILLING VFX
=====================================================================

Standard single-block hoe tilling should use restrained Dark Forest feedback only: tiny head-flower pulse, a few soil particles and perhaps one violet mote. Do not play the full 7x7 bloom for ordinary dirt conversion.

=====================================================================
45. NORMAL ATTACKS
=====================================================================

Entity attacks remain normal HoeItem/tool melee with small dark-metal/violet impact effects. Night Bloom never targets entities and provides no combat damage.

=====================================================================
46. NO HASTE / REGEN / BUFFS
=====================================================================

Do not add player status effects. The ability only affects eligible plants. It is not copied from the Paradise Shovel or another set.

=====================================================================
47. NO AUTOMATIC TILLING AREA
=====================================================================

Unlike the Paradise Hoe, Dark Forest Hoe's ordinary tilling remains vanilla scale unless another explicit project rule says otherwise. Night Bloom is about growth, not 7x7 soil conversion.

=====================================================================
48. MODEL REFINEMENT — C-SHAPED HEAD
=====================================================================

The head must read clearly as a hooked farming implement: ancient roots form the outer arc, dark rectangular working plates line the inner/terminal regions, and thorn spikes emerge from root bends. Do not accidentally make a scythe or question-mark staff.

=====================================================================
49. MODEL REFINEMENT — WORKING PLATES
=====================================================================

Metal/stone plates should have thickness, stepped segmentation, cold-gray worn working edges and deep violet seams. Their alignment should suggest contact with soil during the till animation.

=====================================================================
50. MODEL REFINEMENT — ROOT HANDLE
=====================================================================

Use multiple intertwined root strands with dark bark facets, small thorn branches, cyan fungal pinpoints and occasional purple flowers. The handle should feel grown, not wrapped with a repeating texture spiral.

=====================================================================
51. TEXTURE REFINEMENT
=====================================================================

Keep contrast controlled: black plate interiors, brown-black roots, violet energy in recesses, cyan as rare biology, flowers saturated but small. Match all other Dark Forest tools precisely.

=====================================================================
52. FIRST-PERSON NIGHT BLOOM
=====================================================================

During cast, keep the hooked head visible at the right/upper side and sweep it toward the target field. Do not cover the center for the entire animation. A short central flower flash is acceptable at release.

=====================================================================
53. THIRD-PERSON NIGHT BLOOM
=====================================================================

The player should perform a deliberate cultivation sweep rather than a combat strike. Other players need to understand that the effect is spreading over crops, not damaging them.

=====================================================================
54. GUI / DROPPED PRESENTATION
=====================================================================

Rotate the hook so its C silhouette is immediately readable in GUI. The square flower pommel and living root shaft should still be visible. Dropped render must not appear like an unidentifiable curved stick.

=====================================================================
55. PERFORMANCE BUDGET
=====================================================================

At most 49 candidate checks and one growth attempt per eligible plant per cast is inexpensive. The main risk is particles. Aggregate VFX and do not spawn heavy effects for ineligible cells.

=====================================================================
56. CODE ARCHITECTURE
=====================================================================

Use a focused helper such as `NightBloomAbility` or `CropGrowthAreaHelper` if needed. It should resolve area and call legitimate growth APIs. Renderer/particle code remains client-side and separate.

=====================================================================
57. CONSTANTS / CONFIG
=====================================================================

Centralize AREA_RADIUS=3, AREA_SIZE=7, MAX_CANDIDATES=49, cooldown, durability cost and growth attempts per plant. Clamp any configurable growth-attempt value to a small safe range.

=====================================================================
58. TEST — VANILLA TILLING
=====================================================================

Verify normal dirt/grass/coarse/rooted dirt transformations still behave exactly as intended for Minecraft 1.20.1. Night Bloom must not intercept those clicks incorrectly.

=====================================================================
59. TEST — 7x7 CROPS
=====================================================================

Create a 7x7 mixed-age wheat field. Activate at center. Every eligible crop should receive at most the configured legitimate growth attempt; no crop should be harvested or replaced.

=====================================================================
60. TEST — OUTSIDE RADIUS
=====================================================================

Place eligible crops at distance 4. They must remain untouched. This confirms exact 7x7 bounds.

=====================================================================
61. TEST — MIXED PLANTS
=====================================================================

Mix wheat, carrots, potatoes, beetroot, saplings/flowers or other fertilizable and non-fertilizable plants. Each must follow its actual growth interface without exceptions guessed by block name.

=====================================================================
62. TEST — MATURE CROPS
=====================================================================

Mature crops should remain mature and produce no free drops/items. Calling a growth method on a max-age crop should either no-op or be skipped according to its interface.

=====================================================================
63. TEST — MODDED CROPS
=====================================================================

If modded crops exist, test one that accepts bone meal and one that rejects it. Night Bloom must respect both.

=====================================================================
64. TEST — COOLDOWN / FAILURE
=====================================================================

Activate on an area with no eligible growth. Full cooldown/durability should not be consumed. Activate on a valid field, then spam RMB; exactly one accepted cast should occur until cooldown expires.

=====================================================================
65. TEST — MULTIPLAYER / PROTECTION
=====================================================================

Two players observe the same crop field. Growth states synchronize once, VFX do not duplicate, and protected crops remain unchanged when interaction rules disallow them.

=====================================================================
66. ANIMATION QA
=====================================================================

Idle/equip/till/attack/night_bloom transitions must be clean. Violet seam brightness returns to baseline after cast. No controller should restart the bloom every tick while cooldown is active.

=====================================================================
67. SOUND / VFX QA
=====================================================================

Repeatedly use Night Bloom on dense farms. Ensure audio remains one coherent bloom event and particles remain readable, sparse and performant.

=====================================================================
68. RESOURCE / SERVER QA
=====================================================================

Verify geo, animations, textures, particles, sounds, lang, GUI/drop/glint, resource reload, world reload, multiplayer and dedicated-server class separation.

=====================================================================
69. ABILITY DEFINITION OF DONE
=====================================================================

[ ] vanilla tilling preserved;
[ ] Night Bloom is contextual;
[ ] exact 7x7 bound;
[ ] legitimate bone-meal semantics;
[ ] no auto-harvest/replant/items;
[ ] modded fertilizable compatibility;
[ ] cooldown/durability work;
[ ] server authority/protection respected;
[ ] VFX/sound are bounded;
[ ] multiplayer synchronization works.

=====================================================================
70. FINAL HOE DEFINITION OF DONE
=====================================================================

The final hoe must be a faithful C-shaped root-and-plate Dark Forest asset, a correct Fabric 1.20.1 HoeItem, and a polished contextual farming tool. Night Bloom must feel like an ancient nocturnal forest encouraging legitimate plant growth—not a command that instantly sets every crop to maximum age.

```

---

# Final set-level QA instructions

After all five items are implemented, compare them together in the same inventory, first-person view, third-person view, and ideally a neutral item-display scene.

The set is not visually finished until all five share:

- the same black-metal value range;
- the same root bark palette;
- the same violet glow intensity;
- the same cyan accent intensity;
- the same flower design language;
- similar texture density;
- consistent level of geometric detail;
- compatible handle thickness/grip scale;
- consistent pommel motif;
- consistent animation quality and VFX restraint.

The five tools must look like one intentional **Dark Forest artifact set**, not five separately generated fantasy items.
