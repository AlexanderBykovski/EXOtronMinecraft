# FIRE DEVIL TOOLSET — ULTRA-DETAILED MASTER PROMPTS

![Full Fire Devil concept](concept_art/fire_devil_full_set.png)

This package contains **5 independent production prompts**. Each prompt contains **exactly 70 detailed implementation sections** covering model creation, UV/textures, emissive materials, GeckoLib rig/animation, transforms, gameplay, a unique ability, VFX, audio, networking, optimization, edge cases, testing and Definition of Done.

## Unique abilities

- **Fire Devil Sword — INFERNAL BRAND / DEVIL'S VERDICT:** One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave.
- **Fire Devil Pickaxe — MAGMA VEIN / FORGEHEART EXTRACTION:** RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated.
- **Fire Devil Axe — HELLCLEAVER:** One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks.
- **Fire Devil Shovel — INFERNAL EXCAVATION:** RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square.
- **Fire Devil Hoe — ASHEN BLOOM:** When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling.

---

# Fire Devil Sword — 70-POINT ULTRA-DETAILED PROMPT

![Fire Devil Sword concept](concept_art/fire_devil_sword.png)

```text
# FIRE DEVIL SWORD — MASTER PRODUCTION TASK
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench
# Recommended registry id: fire_devil_sword

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench 3D modeler, Minecraft low-poly artist, pixel texture artist, animator, gameplay programmer, VFX/sound designer, networking engineer, optimization engineer and QA engineer.

This is not a concept-only task. Inspect the actual existing project first, then IMPLEMENT the item and verify it in-game. Use the exact installed Fabric/Yarn/GeckoLib APIs. Do not use Forge, NeoForge, incompatible version examples, imagined methods or pseudocode in place of compiling code.

Shared FIRE DEVIL visual language:
- fractured black volcanic steel / obsidian-like forged metal;
- incandescent orange-red magma fissures with tiny yellow-hot cores;
- square/diamond furnace cores trapped inside heavy forged frames;
- dark heat-blackened leather wrapping;
- stepped brutal architectural plates, bevels and collars;
- restrained sparks, embers and ash rather than permanent screen-filling fire.
The set must look forged by the same infernal civilization, not like five unrelated red recolors.

PRIMARY VISUAL TARGET: a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel.
MANDATORY UNIQUE ABILITY: INFERNAL BRAND / DEVIL'S VERDICT — One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave.

======================================================================================
1. PROJECT AUDIT AND EXACT VERSION VERIFICATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Before touching code or assets, inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric Loader/API versions, GeckoLib dependency, Java version, package structure, ModItems, ToolMaterial classes, renderers, client initializer, existing Fire Devil tools, sound/particle registries, networking, and any helper utilities. Do not assume an API because an online example looks similar. If the project already contains a working animated SwordItem, treat that implementation as the technical reference while preserving this item's unique visual/gameplay identity. Record exact resource namespace and file conventions before creating anything.

======================================================================================
2. REFERENCE DECOMPOSITION AND VISUAL MEASUREMENT
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Study the supplied per-item concept and the full-set sheet. Decompose the object into measurable masses: long thick blade, centered pointed apex, layered dark edge plates, recessed luminous central fissure, angular crossguard blocks, core socket, wrapped grip and cubic pommel. Note which silhouette features define recognition, which details can be texture-only, which components need depth, where emissive cracks originate, and how the object is expected to connect structurally. Inspect the reference from an imagined front/side/3/4 view and infer hidden rear geometry conservatively rather than inventing unrelated machinery.

======================================================================================
3. SILHOUETTE LOCK BEFORE DETAIL WORK
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Create a flat-color silhouette blockout and judge it before any ornamentation. At normal gameplay distance the item must be recognizable solely from geometry. Do not use cracks, emissive colors or tiny details to hide incorrect proportions. If the silhouette is wrong, stop and correct it before proceeding.

======================================================================================
4. OVERALL PROPORTIONS AND MINECRAFT SCALE
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Establish a consistent Blockbench coordinate system and compare the item with player hand/body scale and the other Fire Devil tools. Preserve the relative visual weight from the reference. The item may be legendary and larger than vanilla, but must remain usable in first person and readable in inventory. Document the final model scale so later transforms do not compensate for arbitrary export scaling.

======================================================================================
5. PRIMARY BLOCKOUT WORKFLOW
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Build only the primary masses first: long thick blade, centered pointed apex, layered dark edge plates, recessed luminous central fissure, angular crossguard blocks, core socket, wrapped grip and cubic pommel. Keep the blockout low complexity and physically connected. Validate working direction and grip orientation now, before UVs and animation. Do not proceed to cracks, rivets, runes or particles until the blockout survives front/back/side/top/3/4 inspection.

======================================================================================
6. SECONDARY FORMS AND STRUCTURAL LAYERING
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Add secondary structural plates, sockets, collars, recesses, ribs and working-edge reinforcement in a hierarchy that makes physical sense. Every visible major plate should either connect to another component or be clearly mounted. Avoid floating decoration and accidental interior holes. Use repeated Fire Devil motifs consistently across the set without copying another tool's silhouette.

======================================================================================
7. SIDE PROFILE AND PHYSICAL THICKNESS
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Give every major working component real side depth. Separate rear structural thickness, middle body plate, recessed inner panel/channel, and thinner working edge where appropriate. The item must not look like a 2D concept image extruded by one pixel. Check side and 3/4 views for believable mass and ensure the hand/shaft connection is structurally thick enough.

======================================================================================
8. BEVELS, EDGES, TIPS AND WORKING SURFACES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Use deliberate low-poly chamfers instead of high-segment bevels. Working tips/edges should transition from thick structural body to narrower edge through a few readable planes. Corners, sockets and pommels may use stepped bevels. Never add dozens of tiny cubes for curvature that will be invisible in gameplay.

======================================================================================
9. MATERIAL HIERARCHY AND READABILITY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Keep four material families visually separable: dark volcanic metal, incandescent magma/emissive cracks, dark wrapped grip, and infernal cores. Use geometry depth plus value contrast—not color alone—to distinguish them. The black body should still be readable in darkness and the orange glow should remain an accent rather than flooding every surface.

======================================================================================
10. BLACK VOLCANIC METAL TEXTURING
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Paint volcanic metal using broad charcoal/blue-black planes, medium-gray chipped bevels, sparse forged pits and controlled scratches. Avoid uniform pure black and avoid noisy rock photographs. Working areas may show brighter abrasion. Recesses can approach near-black, but silhouette edges need enough value separation for Minecraft lighting.

======================================================================================
11. INCANDESCENT MAGMA CRACK DESIGN
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Design magma fractures as stress-driven networks that originate around the core, joints and working edge. Use a hot center hierarchy: tiny pale-yellow/white-orange pixels at peaks, orange core, red-orange falloff, dark red heat halo. Do not draw random equal-brightness scribbles everywhere; secondary cracks must remain subordinate to the principal energy path.

======================================================================================
12. INFERNAL CORE / GEM CONSTRUCTION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Model each infernal core as a physical socket with an inset faceted hot center and surrounding dark frame. The core should look trapped inside forged metal. Give the brightest region a small area so emission feels intense rather than flat. Reuse the same core language across the set while scaling shape/size to this item.

======================================================================================
13. HANDLE, GRIP AND WRAPPING CONSTRUCTION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Construct the grip as dark heat-blackened leather/hide or tightly wrapped material over a rigid shaft/tang. Use diagonal or crossed wrap bands, subtle brown-black value variation, and forged collars. Keep the hand-contact area visually calmer than the head/blade so the grip location remains obvious.

======================================================================================
14. HEAT WEAR, SOOT AND EDGE AGING
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Add restrained heat wear: dark red-brown discoloration near cores and working edges, small soot deposits in recesses, and bright worn metal on exposed bevels. Do not rust the set green/brown or cover everything in dirt. These are maintained infernal artifacts, not abandoned scrap.

======================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Prefer 256x256 texture for this high-detail GeckoLib item unless the existing set uses 128x128. Maintain consistent texel density across all five tools. Allocate more pixels to focal front faces, cores and working edges; allocate fewer to hidden undersides. Tiny details that disappear at inventory scale should be simplified.

======================================================================================
16. UV LAYOUT AND ISLAND PADDING
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Create clean UV islands with padding, logical orientation and minimal distortion. Separate front/back focal faces where unique fracture patterns matter. Mirror only genuinely symmetrical surfaces where duplicated wear is acceptable. Keep emissive orange islands away from unrelated dark islands to prevent filtering/bleeding.

======================================================================================
17. PIXEL-ART TEXTURE PAINTING RULES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Use crisp Minecraft-compatible pixel shading. Do not bake strong environmental highlights from the concept art into the texture. Build depth with edge highlights, plate-to-plate occlusion shadows, hot crack cores and controlled material variation. Avoid blurry photographic gradients and excessive antialiasing.

======================================================================================
18. EMISSIVE-LAYER IMPLEMENTATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Inspect the project for an existing GeckoLib emissive/render-layer solution. If supported, use emission only on core centers, selected magma crack centers and hot working strips. Outer metal, grip and most crack falloff remain normally lit. If no clean emissive system exists, use bright texture values and particles rather than installing a heavy shader dependency solely for this set.

======================================================================================
19. GEOMETRY BUDGET AND OPTIMIZATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Optimize deliberately: geometry for silhouette, thickness, major bevels, sockets, cores and major plates; textures for micro-cracks, scratches, tiny rivets and engraved seams. Remove hidden duplicate cubes, zero-size geometry and unseen internal faces. Normal idle rendering should add negligible cost compared with another GeckoLib item.

======================================================================================
20. GECKOLIB BONE HIERARCHY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Create a small meaningful bone tree: root -> item -> main working assembly/head/blade -> handle -> pommel -> optional FX bones. Sub-bones exist only when animation or organization benefits. Do not create one bone per decorative plate. Use names that are stable, snake_case or project-consistent, and easy to reference in animation JSON.

======================================================================================
21. BONE PIVOTS AND ROTATION ORIGINS
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Place pivots at physical joints: main head/blade pivot near the shaft/hilt connection, handle pivot along the grip axis, pommel at lower connector, cores at their centers, and working sub-parts at actual attachment points. Bad pivots create 'exploding' animation even with correct keyframes, so validate each pivot in Blockbench before export.

======================================================================================
22. ROOT ORIGIN AND HELD-ITEM REFERENCE POINT
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Place root/origin around the natural held-item reference rather than blindly at geometric center. The origin must support first person, third person, GUI and dropped transforms without extreme translations. Follow the same convention as already-working set items when possible to simplify shared renderer logic.

======================================================================================
23. FIRST-PERSON RIGHT-HAND TRANSFORM
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Tune first-person right hand only after the model orientation is correct. The hand must visibly contact the grip, the functional edge must face the correct working/attack direction, and the main head/blade should remain readable without covering the crosshair. Test normal and low/high FOV, idle and action animation.

======================================================================================
24. FIRST-PERSON LEFT/OFFHAND TRANSFORM
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Test offhand/left-hand rendering independently. Do not assume automatic mirroring preserves working direction. Correct mirrored yaw/roll or use display-context-specific transforms so the item does not suddenly face backwards, expose only its thin side, or intersect the camera.

======================================================================================
25. THIRD-PERSON TRANSFORM AND HAND CONTACT
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. In third person, align the player's hand with the actual grip and keep the working end logically forward during attacks/mining/tilling. Test standing, walking, sprinting, jumping, sneaking and action states. Small Minecraft-style clipping is acceptable; gross torso/head penetration or a floating grip is not.

======================================================================================
26. GUI INVENTORY TRANSFORM
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Create a dedicated GUI transform that shows the strongest 3/4 silhouette, the infernal core and emissive fractures. Fit the entire item into the slot without cropping major working geometry. Do not simply reuse first-person transforms.

======================================================================================
27. DROPPED-ITEM AND ITEM-FRAME TRANSFORM
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. For ground/item-frame display, preserve sensible scale and a stable attractive angle. The item should not become building-sized or vanish into a block. Verify item-frame depth so thick GeckoLib geometry does not clip almost entirely through the wall.

======================================================================================
28. IDLE ANIMATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Idle animation should be restrained and loop smoothly for roughly 2.5–4 seconds: a 1–2% core pulse, tiny heat breathing, and at most fractions of a degree of rigid secondary movement. Do not make a forged tool constantly wobble or emit a permanent flame fountain.

======================================================================================
29. EQUIP ANIMATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Equip animation should be short and responsive, around 0.25–0.45 seconds: raise from a slightly lowered pose, tiny heavy overshoot, brief core brightening, settle. Avoid full spins, anime flourishes or animation that delays actual gameplay control.

======================================================================================
30. PRIMARY ATTACK / WORK ANIMATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Design the primary action animation around this item's real role: full vanilla/project sword melee behavior with normal attack cooldown, damage attributes, enchantments and durability. Use anticipation -> fast working/attack motion -> clear impact/contact frame -> physical follow-through -> recovery. If vanilla player-hand motion already supplies the main swing, let GeckoLib add internal inertia and core response instead of doubling root rotation.

======================================================================================
31. SECONDARY INERTIA AND MECHANICAL MOTION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Secondary motion must communicate rigid mass: shaft/hand begins motion, heavy head/blade lags by a few degrees, catches up near impact, then slightly overshoots during recovery. Metal plates do not flex like rubber. Small core/socket counter-rotation can enrich close-up animation without looking mechanical.

======================================================================================
32. MAGMA/CORE PULSE ANIMATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Animate heat as a short energy flow rather than constant maximal glow. A lower core/pommel may brighten first, followed by the main head/core and working crack network. Peak emission aligns with impact or special release, then fades rapidly to idle. Keep ordinary idle dark enough that special activation feels meaningful.

======================================================================================
33. ANIMATION CONTROLLERS AND PRIORITIES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Define controller priority so mutually exclusive actions never fight over root bones. A safe conceptual order is special ability > normal attack/work > equip > idle, with a separate FX controller only if the installed GeckoLib version benefits. Use the exact triggerable-animation API present in the project, not copied syntax from another version.

======================================================================================
34. ANIMATION-EVENT SYNCHRONIZATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Separate animation-timed cosmetics from gameplay confirmation. Whoosh/equip/core pulses can be keyframe-driven. Successful damage, block breaks, crop growth or vein extraction must be triggered by server-authoritative gameplay logic. Damage/work must never depend on render FPS or whether a client skipped an animation frame.

======================================================================================
35. VANILLA GAMEPLAY BASE CLASS AND BEHAVIOR
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Implement the item using the project's real SwordItem (or established custom subclass) so it retains full vanilla/project sword melee behavior with normal attack cooldown, damage attributes, enchantments and durability. Do not replace vanilla tool behavior with a generic Item just to make GeckoLib easier. Preserve tags, interaction semantics, attack/mining attributes and vanilla action results appropriate to Minecraft 1.20.1.

======================================================================================
36. TOOL MATERIAL / COMBAT OR MINING BALANCE
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Reuse an existing FireDevilToolMaterial if present. If absent, derive values from the mod's progression and compare with Netherite and other endgame sets. Keep named constants for durability, mining speed, attack damage and enchantability. Do not use absurd values unless the mod's established progression explicitly requires them.

======================================================================================
37. DURABILITY BEHAVIOR
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Normal durability follows standard item semantics. For the unique ability, follow this item-specific rule: about 4 durability once per successful cast, never per target or per visual bolt. Use ItemStack damage APIs compatible with Unbreaking/creative behavior where appropriate. Never perform the full gameplay effect and only afterwards discover the tool should have broken halfway through.

======================================================================================
38. ENCHANTMENTS AND VANILLA COMPATIBILITY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Preserve appropriate vanilla enchantments and loot/interaction semantics. Efficiency/Sharpness/Fortune/Silk Touch/Unbreaking/Mending compatibility depends on item type; do not disable them accidentally. Special abilities must explicitly define how enchantments interact instead of silently duplicating drops or multiplying damage unexpectedly.

======================================================================================
39. UNIQUE ABILITY CONCEPT
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. **INFERNAL BRAND / DEVIL'S VERDICT** is the mandatory unique mechanic. One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave. This ability is part of the production definition, not an optional idea. Implement it only after ordinary item behavior is correct so the special system cannot hide broken base gameplay.

======================================================================================
40. ABILITY ACTIVATION INPUT AND VALIDATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Activation must be deterministic and context-aware. One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave. Validate the held item, hand/context, cooldown and server-side state before committing. Invalid use must not consume durability or start a fake successful animation. One user input should create one ability execution, not repeated triggers every use tick.

======================================================================================
41. ABILITY TARGETING / AFFECTED REGION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Targeting is strictly bounded: a forward corridor/wave about 14–18 blocks long and roughly 2 blocks wide, derived from the player's look direction and clipped by solid obstacles. Build the target set once per use with hard numerical limits. Never replace a bounded local calculation with a whole-world scan. Solid collision, block suitability or crop/ore validity must be respected according to this item's design.

======================================================================================
42. SERVER-AUTHORITATIVE ABILITY EXECUTION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. The server is authoritative for every gameplay consequence of INFERNAL BRAND / DEVIL'S VERDICT: target selection, damage/block/crop changes, cooldown, durability and state transitions. Client-side code may predict harmless visual startup, but cannot decide outcomes. Keep MinecraftClient and renderer classes out of common/server class paths.

======================================================================================
43. ABILITY STATE MACHINE
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Use an explicit, finite state flow rather than scattered booleans. For this ability incorporate the special constraint: brand targets are deduplicated by cast ID; if a branded target dies, unloads, changes dimension, or becomes invalid before detonation, the delayed burst cancels safely. Every active cast/operation must have a clear start, progress/resolve phase and cleanup. World unload, player disconnect or invalid target must not leave stale global state.

======================================================================================
44. ABILITY GAMEPLAY RESOLUTION RULES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Gameplay resolution must follow the exact item-specific promise: One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave. Prevent accidental duplicate effects caused by overlapping samples, repeated ticks or client/server double execution. Preserve normal protection, loot, PvP and block-update semantics rather than bypassing them with raw uncontrolled world mutation.

======================================================================================
45. ABILITY COOLDOWN SEMANTICS
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Cooldown semantics: 8 seconds as an initial named balance constant; cooldown affects only the RMB ability and never disables normal sword attacks. Use a named constant and the project's cooldown system. Cooldown should begin only at the correct committed stage. Never let the ability cooldown unintentionally disable unrelated ordinary item actions unless explicitly required by this design.

======================================================================================
46. ABILITY DURABILITY / RESOURCE COST
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Ability cost: about 4 durability once per successful cast, never per target or per visual bolt. Apply cost exactly once at the intended successful stage, or per successfully processed block only where this item's definition calls for it. Invalid/no-op actions cost nothing. Stop safely if the item breaks during multi-block work.

======================================================================================
47. ABILITY VFX TIMELINE
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Create a tightly choreographed VFX timeline: guard core ignites -> magma spine becomes yellow-hot -> short orange-white crescent wave tears forward -> hit target gains a compact glowing sigil -> sigil contracts -> one dark-red/orange burst with ash and sparks. Favor a small number of layered purposeful effects—hot core, emissive path, sparks, ash, contact flash—over hundreds of identical particles. First-person effects must preserve visibility; world-visible effects must make the action understandable to observers.

======================================================================================
48. ABILITY SOUND DESIGN
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Sound identity: furnace ignition, heavy blade whoosh, molten tear, quiet brand hiss, then a compact bassy flare on detonation. Use layering and pitch variation intentionally, but aggregate repeated multi-target/multi-block events so the action does not produce dozens of maximum-volume identical sounds. Keep ordinary tool sounds recognizable beneath the infernal accent.

======================================================================================
49. ABILITY NETWORKING AND SYNCHRONIZATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Use efficient synchronization. Prefer normal world/entity synchronization or one compact ability event containing origin/direction/seed/positions over one custom packet per particle. The server remains authoritative even if clients reconstruct deterministic visuals from a seed. Avoid trusting client-reported hit lists or block lists.

======================================================================================
50. ABILITY MULTIPLAYER BEHAVIOR
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Test simultaneous multiplayer use. Every player/cast/area operation needs independent state; never store 'current target/current cast' in one global mutable variable. Nearby observers should see important world effects, while camera-only micro-effects may remain local. Handle latency without changing gameplay damage/work result.

======================================================================================
51. NORMAL-USE VFX
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Ordinary attacks/mining/tilling should use restrained Fire Devil feedback: brief core pulse, a few orange forge sparks or a short translucent dark-orange trail, while preserving vanilla material/block particles. Do not make every basic action visually equal to the special ability.

======================================================================================
52. SUCCESSFUL HIT / SUCCESSFUL WORK VFX
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Successful confirmed work/hits should add localized feedback at the actual target/block: compact orange-white contact flash, sparse metal/ember sparks, brief core response and normal block debris where relevant. Misses/no-op interactions must not spawn a fake success burst.

======================================================================================
53. CRITICAL / HIGH-VALUE RESULT VFX
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Critical hits or especially valuable successful results may receive a slightly brighter star/core pulse and a modest particle increase, but never auto-trigger the full unique ability unless explicitly designed. Keep special activation visually distinct and readable.

======================================================================================
54. PARTICLE BUDGET AND LIFETIME
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Set explicit budgets. Normal action: roughly single-digit to low-teens custom particles. Special ability: bounded tens, scaled to fixed target cap. Most particles should die within 0.1–0.6 seconds. Never spawn particles every tick merely because the item is held or because a long status/cooldown is active.

======================================================================================
55. ORDINARY-USE SOUND LAYERING
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Ordinary sound should preserve the physical role—blade whoosh, pick impact, soil scrape, etc.—then add a restrained forged-metal/furnace overtone. Avoid stacking five loud sounds on every mundane action. Special ability receives the more elaborate audio signature.

======================================================================================
56. ENVIRONMENTAL SAFETY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. The infernal aesthetic does NOT automatically authorize griefing. By default, never create fire blocks, lava, TNT-like explosions or permanent burning terrain unless the specific ability explicitly requires it—which these designs do not. Cosmetic embers and entity fire status are separate from world fire placement.

======================================================================================
57. WORLD/BLOCK INTERACTION SAFETY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. World/block changes are limited to this item's legitimate rules: One RMB press performs a short infernal cast and launches a broad molten cutting wave roughly 16 blocks forward. Each valid entity intersected by the wave can be hit only once and receives an Infernal Brand. After about 1.0 second the brand collapses inward and erupts once on that same target as a compact controlled infernal burst. The delayed eruption is entity-only: it does not explode terrain, place fire blocks, or create lava. Solid terrain occludes the wave. Respect block hardness/suitability, crops/farmland safety, loot contexts, world border, chunk availability and protection hooks where the project exposes them. Do not use force-loading or raw setBlockState loops to bypass gameplay systems.

======================================================================================
58. ENTITY FILTERING AND FRIENDLY-FIRE BEHAVIOR
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Respect teams, PvP/friendly-fire, creative/spectator rules, invulnerable entities and caster exclusion for combat abilities. Farming/mining abilities should not damage entities unless explicitly stated. Deduplicate targets per cast so overlapping effect geometry cannot multiply unintended damage.

======================================================================================
59. PERFORMANCE SAFEGUARDS
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Hard-code safe upper bounds for every search, target list, area size and duration. No whole-world scans, no unbounded recursion, no Thread.sleep, no rendering-dependent gameplay and no long-lived unused state. Rate-limit particles/sounds under fast mining or repeated work.

======================================================================================
60. INVALID-USE AND NO-OP BEHAVIOR
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Invalid use must be cheap and predictable. If cooldown is active, target/context is invalid, protection denies action, tool is broken, crop is mature, ore search finds nothing, or no eligible blocks exist, do not consume durability or play full successful VFX. Return/fall back using the correct Minecraft action result.

======================================================================================
61. EDGE CASES AND FAILURE RECOVERY
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Handle edge cases explicitly for this ability, including: brand targets are deduplicated by cast ID; if a branded target dies, unloads, changes dimension, or becomes invalid before detonation, the delayed burst cancels safely. Also test chunk boundaries, world border, target changes between validation and execution, dimension change, disconnect, tool break, high latency, offhand, creative mode, and concurrent players. Cleanup must be idempotent and safe.

======================================================================================
62. REQUIRED RESOURCE FILES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Expected resources normally include assets/<modid>/geo/fire_devil_sword.geo.json, animations/fire_devil_sword.animation.json, textures/item/fire_devil_sword.png, item model JSON if renderer requires it, lang entries, optional particle textures and sounds.json entries. Follow the project's actual namespace/path conventions exactly.

======================================================================================
63. LOCALIZATION AND TOOLTIP
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Add en_us and any existing project languages. Tooltip should state the unique mechanic in player-facing terms, e.g. 'INFERNAL BRAND / DEVIL'S VERDICT' and its main range/area, without implementation jargon. Keep names consistent across registry ID, translation key, advancements/recipes if any.

======================================================================================
64. CODE ARCHITECTURE AND CLASS RESPONSIBILITIES
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Prefer a focused FireDevilSwordItem class plus existing/shared model and renderer patterns. Put complex bounded area/target algorithms into small helpers only when that improves clarity. Reuse shared FireDevilToolMaterial, VFX, sound and animation utilities instead of copy-pasting five divergent systems.

======================================================================================
65. JSON/RESOURCE IDENTIFIER VALIDATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Validate every identifier: Java animation trigger strings, geo filename, texture path, namespace, sound ID, particle ID, translation key and JSON schema. Run resource reload where possible. A one-character mismatch that yields missing texture or silent animation means the task is not done.

======================================================================================
66. MODEL GAPS, SEAMS AND Z-FIGHTING QA
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Inspect the final model for unintended holes and seams around long thick blade, centered pointed apex, layered dark edge plates, recessed luminous central fissure, angular crossguard blocks, core socket, wrapped grip and cubic pommel. Distinguish deliberate magma channels/recesses from accidental open geometry. Remove z-fighting from coplanar plates, close missing side faces, fix mirrored gaps, and verify there are no zero-size cubes or floating decorative components.

======================================================================================
67. GAMEPLAY TEST MATRIX
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Gameplay QA must cover ordinary behavior plus INFERNAL BRAND / DEVIL'S VERDICT. Test valid/invalid use, cooldown, durability, low-durability break, enchantments, multiplayer, protection/solid obstacles or block suitability as relevant, repeated use, and concurrency. Verify actual server results, not only pretty animation.

======================================================================================
68. VISUAL TEST MATRIX
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Visual QA: inspect front/back/left/right/top/bottom and 3/4 views, first-person at several FOVs, offhand, third-person movement/actions, GUI, dropped item, item frame, bright daylight and dark environments. Confirm emissive hierarchy, correct working orientation, no camera obstruction, no gaps/z-fighting and coherent animation.

======================================================================================
69. BUILD AND RUNCLIENT VALIDATION
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. Run the actual Gradle wrapper build and then runClient when available. Read compiler/resource/runtime logs, fix errors, reload resources, and repeat until stable. If dedicated-server run is available, verify no client-only renderer/model class causes classloading failure.

======================================================================================
70. FINAL DEFINITION OF DONE
======================================================================================
**Item-specific target:** a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel. The item is DONE only when it strongly matches the supplied concept (a towering straight black volcanic sword whose broad slab-like blade is split by a brilliant vertical magma fissure; the point is faceted and sharp, the guard is compact and brutal, the hilt houses a square/diamond infernal core, and the grip is dark heat-blackened wrapping ending in a glowing cubic pommel); geometry is clean and connected; UV/texture/emissive layers are polished; first/third/GUI/ground transforms are correct; GeckoLib animations work; ordinary SwordItem behavior remains intact; **INFERNAL BRAND / DEVIL'S VERDICT** behaves exactly as specified with server authority, safe cooldown/cost/networking/performance; no unintended world grief occurs; and build/runtime validation succeeds.

END OF PROMPT.
```

---


# Fire Devil Pickaxe — 70-POINT ULTRA-DETAILED PROMPT

![Fire Devil Pickaxe concept](concept_art/fire_devil_pickaxe.png)

```text
# FIRE DEVIL PICKAXE — MASTER PRODUCTION TASK
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench
# Recommended registry id: fire_devil_pickaxe

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench 3D modeler, Minecraft low-poly artist, pixel texture artist, animator, gameplay programmer, VFX/sound designer, networking engineer, optimization engineer and QA engineer.

This is not a concept-only task. Inspect the actual existing project first, then IMPLEMENT the item and verify it in-game. Use the exact installed Fabric/Yarn/GeckoLib APIs. Do not use Forge, NeoForge, incompatible version examples, imagined methods or pseudocode in place of compiling code.

Shared FIRE DEVIL visual language:
- fractured black volcanic steel / obsidian-like forged metal;
- incandescent orange-red magma fissures with tiny yellow-hot cores;
- square/diamond furnace cores trapped inside heavy forged frames;
- dark heat-blackened leather wrapping;
- stepped brutal architectural plates, bevels and collars;
- restrained sparks, embers and ash rather than permanent screen-filling fire.
The set must look forged by the same infernal civilization, not like five unrelated red recolors.

PRIMARY VISUAL TARGET: a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel.
MANDATORY UNIQUE ABILITY: MAGMA VEIN / FORGEHEART EXTRACTION — RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated.

======================================================================================
1. PROJECT AUDIT AND EXACT VERSION VERIFICATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Before touching code or assets, inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric Loader/API versions, GeckoLib dependency, Java version, package structure, ModItems, ToolMaterial classes, renderers, client initializer, existing Fire Devil tools, sound/particle registries, networking, and any helper utilities. Do not assume an API because an online example looks similar. If the project already contains a working animated PickaxeItem, treat that implementation as the technical reference while preserving this item's unique visual/gameplay identity. Record exact resource namespace and file conventions before creating anything.

======================================================================================
2. REFERENCE DECOMPOSITION AND VISUAL MEASUREMENT
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Study the supplied per-item concept and the full-set sheet. Decompose the object into measurable masses: central thick socket, two segmented curved pick arms with tapered functional tips, recessed crack channels, square furnace core, long wrapped shaft, collars and cubic pommel. Note which silhouette features define recognition, which details can be texture-only, which components need depth, where emissive cracks originate, and how the object is expected to connect structurally. Inspect the reference from an imagined front/side/3/4 view and infer hidden rear geometry conservatively rather than inventing unrelated machinery.

======================================================================================
3. SILHOUETTE LOCK BEFORE DETAIL WORK
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Create a flat-color silhouette blockout and judge it before any ornamentation. At normal gameplay distance the item must be recognizable solely from geometry. Do not use cracks, emissive colors or tiny details to hide incorrect proportions. If the silhouette is wrong, stop and correct it before proceeding.

======================================================================================
4. OVERALL PROPORTIONS AND MINECRAFT SCALE
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Establish a consistent Blockbench coordinate system and compare the item with player hand/body scale and the other Fire Devil tools. Preserve the relative visual weight from the reference. The item may be legendary and larger than vanilla, but must remain usable in first person and readable in inventory. Document the final model scale so later transforms do not compensate for arbitrary export scaling.

======================================================================================
5. PRIMARY BLOCKOUT WORKFLOW
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Build only the primary masses first: central thick socket, two segmented curved pick arms with tapered functional tips, recessed crack channels, square furnace core, long wrapped shaft, collars and cubic pommel. Keep the blockout low complexity and physically connected. Validate working direction and grip orientation now, before UVs and animation. Do not proceed to cracks, rivets, runes or particles until the blockout survives front/back/side/top/3/4 inspection.

======================================================================================
6. SECONDARY FORMS AND STRUCTURAL LAYERING
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Add secondary structural plates, sockets, collars, recesses, ribs and working-edge reinforcement in a hierarchy that makes physical sense. Every visible major plate should either connect to another component or be clearly mounted. Avoid floating decoration and accidental interior holes. Use repeated Fire Devil motifs consistently across the set without copying another tool's silhouette.

======================================================================================
7. SIDE PROFILE AND PHYSICAL THICKNESS
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Give every major working component real side depth. Separate rear structural thickness, middle body plate, recessed inner panel/channel, and thinner working edge where appropriate. The item must not look like a 2D concept image extruded by one pixel. Check side and 3/4 views for believable mass and ensure the hand/shaft connection is structurally thick enough.

======================================================================================
8. BEVELS, EDGES, TIPS AND WORKING SURFACES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Use deliberate low-poly chamfers instead of high-segment bevels. Working tips/edges should transition from thick structural body to narrower edge through a few readable planes. Corners, sockets and pommels may use stepped bevels. Never add dozens of tiny cubes for curvature that will be invisible in gameplay.

======================================================================================
9. MATERIAL HIERARCHY AND READABILITY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Keep four material families visually separable: dark volcanic metal, incandescent magma/emissive cracks, dark wrapped grip, and infernal cores. Use geometry depth plus value contrast—not color alone—to distinguish them. The black body should still be readable in darkness and the orange glow should remain an accent rather than flooding every surface.

======================================================================================
10. BLACK VOLCANIC METAL TEXTURING
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Paint volcanic metal using broad charcoal/blue-black planes, medium-gray chipped bevels, sparse forged pits and controlled scratches. Avoid uniform pure black and avoid noisy rock photographs. Working areas may show brighter abrasion. Recesses can approach near-black, but silhouette edges need enough value separation for Minecraft lighting.

======================================================================================
11. INCANDESCENT MAGMA CRACK DESIGN
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Design magma fractures as stress-driven networks that originate around the core, joints and working edge. Use a hot center hierarchy: tiny pale-yellow/white-orange pixels at peaks, orange core, red-orange falloff, dark red heat halo. Do not draw random equal-brightness scribbles everywhere; secondary cracks must remain subordinate to the principal energy path.

======================================================================================
12. INFERNAL CORE / GEM CONSTRUCTION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Model each infernal core as a physical socket with an inset faceted hot center and surrounding dark frame. The core should look trapped inside forged metal. Give the brightest region a small area so emission feels intense rather than flat. Reuse the same core language across the set while scaling shape/size to this item.

======================================================================================
13. HANDLE, GRIP AND WRAPPING CONSTRUCTION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Construct the grip as dark heat-blackened leather/hide or tightly wrapped material over a rigid shaft/tang. Use diagonal or crossed wrap bands, subtle brown-black value variation, and forged collars. Keep the hand-contact area visually calmer than the head/blade so the grip location remains obvious.

======================================================================================
14. HEAT WEAR, SOOT AND EDGE AGING
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Add restrained heat wear: dark red-brown discoloration near cores and working edges, small soot deposits in recesses, and bright worn metal on exposed bevels. Do not rust the set green/brown or cover everything in dirt. These are maintained infernal artifacts, not abandoned scrap.

======================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Prefer 256x256 texture for this high-detail GeckoLib item unless the existing set uses 128x128. Maintain consistent texel density across all five tools. Allocate more pixels to focal front faces, cores and working edges; allocate fewer to hidden undersides. Tiny details that disappear at inventory scale should be simplified.

======================================================================================
16. UV LAYOUT AND ISLAND PADDING
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Create clean UV islands with padding, logical orientation and minimal distortion. Separate front/back focal faces where unique fracture patterns matter. Mirror only genuinely symmetrical surfaces where duplicated wear is acceptable. Keep emissive orange islands away from unrelated dark islands to prevent filtering/bleeding.

======================================================================================
17. PIXEL-ART TEXTURE PAINTING RULES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Use crisp Minecraft-compatible pixel shading. Do not bake strong environmental highlights from the concept art into the texture. Build depth with edge highlights, plate-to-plate occlusion shadows, hot crack cores and controlled material variation. Avoid blurry photographic gradients and excessive antialiasing.

======================================================================================
18. EMISSIVE-LAYER IMPLEMENTATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Inspect the project for an existing GeckoLib emissive/render-layer solution. If supported, use emission only on core centers, selected magma crack centers and hot working strips. Outer metal, grip and most crack falloff remain normally lit. If no clean emissive system exists, use bright texture values and particles rather than installing a heavy shader dependency solely for this set.

======================================================================================
19. GEOMETRY BUDGET AND OPTIMIZATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Optimize deliberately: geometry for silhouette, thickness, major bevels, sockets, cores and major plates; textures for micro-cracks, scratches, tiny rivets and engraved seams. Remove hidden duplicate cubes, zero-size geometry and unseen internal faces. Normal idle rendering should add negligible cost compared with another GeckoLib item.

======================================================================================
20. GECKOLIB BONE HIERARCHY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Create a small meaningful bone tree: root -> item -> main working assembly/head/blade -> handle -> pommel -> optional FX bones. Sub-bones exist only when animation or organization benefits. Do not create one bone per decorative plate. Use names that are stable, snake_case or project-consistent, and easy to reference in animation JSON.

======================================================================================
21. BONE PIVOTS AND ROTATION ORIGINS
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Place pivots at physical joints: main head/blade pivot near the shaft/hilt connection, handle pivot along the grip axis, pommel at lower connector, cores at their centers, and working sub-parts at actual attachment points. Bad pivots create 'exploding' animation even with correct keyframes, so validate each pivot in Blockbench before export.

======================================================================================
22. ROOT ORIGIN AND HELD-ITEM REFERENCE POINT
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Place root/origin around the natural held-item reference rather than blindly at geometric center. The origin must support first person, third person, GUI and dropped transforms without extreme translations. Follow the same convention as already-working set items when possible to simplify shared renderer logic.

======================================================================================
23. FIRST-PERSON RIGHT-HAND TRANSFORM
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Tune first-person right hand only after the model orientation is correct. The hand must visibly contact the grip, the functional edge must face the correct working/attack direction, and the main head/blade should remain readable without covering the crosshair. Test normal and low/high FOV, idle and action animation.

======================================================================================
24. FIRST-PERSON LEFT/OFFHAND TRANSFORM
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Test offhand/left-hand rendering independently. Do not assume automatic mirroring preserves working direction. Correct mirrored yaw/roll or use display-context-specific transforms so the item does not suddenly face backwards, expose only its thin side, or intersect the camera.

======================================================================================
25. THIRD-PERSON TRANSFORM AND HAND CONTACT
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. In third person, align the player's hand with the actual grip and keep the working end logically forward during attacks/mining/tilling. Test standing, walking, sprinting, jumping, sneaking and action states. Small Minecraft-style clipping is acceptable; gross torso/head penetration or a floating grip is not.

======================================================================================
26. GUI INVENTORY TRANSFORM
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Create a dedicated GUI transform that shows the strongest 3/4 silhouette, the infernal core and emissive fractures. Fit the entire item into the slot without cropping major working geometry. Do not simply reuse first-person transforms.

======================================================================================
27. DROPPED-ITEM AND ITEM-FRAME TRANSFORM
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. For ground/item-frame display, preserve sensible scale and a stable attractive angle. The item should not become building-sized or vanish into a block. Verify item-frame depth so thick GeckoLib geometry does not clip almost entirely through the wall.

======================================================================================
28. IDLE ANIMATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Idle animation should be restrained and loop smoothly for roughly 2.5–4 seconds: a 1–2% core pulse, tiny heat breathing, and at most fractions of a degree of rigid secondary movement. Do not make a forged tool constantly wobble or emit a permanent flame fountain.

======================================================================================
29. EQUIP ANIMATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Equip animation should be short and responsive, around 0.25–0.45 seconds: raise from a slightly lowered pose, tiny heavy overshoot, brief core brightening, settle. Avoid full spins, anime flourishes or animation that delays actual gameplay control.

======================================================================================
30. PRIMARY ATTACK / WORK ANIMATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Design the primary action animation around this item's real role: true pickaxe mining suitability, correct tags, drops, mining level, normal combat attributes, enchantments and durability. Use anticipation -> fast working/attack motion -> clear impact/contact frame -> physical follow-through -> recovery. If vanilla player-hand motion already supplies the main swing, let GeckoLib add internal inertia and core response instead of doubling root rotation.

======================================================================================
31. SECONDARY INERTIA AND MECHANICAL MOTION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Secondary motion must communicate rigid mass: shaft/hand begins motion, heavy head/blade lags by a few degrees, catches up near impact, then slightly overshoots during recovery. Metal plates do not flex like rubber. Small core/socket counter-rotation can enrich close-up animation without looking mechanical.

======================================================================================
32. MAGMA/CORE PULSE ANIMATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Animate heat as a short energy flow rather than constant maximal glow. A lower core/pommel may brighten first, followed by the main head/core and working crack network. Peak emission aligns with impact or special release, then fades rapidly to idle. Keep ordinary idle dark enough that special activation feels meaningful.

======================================================================================
33. ANIMATION CONTROLLERS AND PRIORITIES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Define controller priority so mutually exclusive actions never fight over root bones. A safe conceptual order is special ability > normal attack/work > equip > idle, with a separate FX controller only if the installed GeckoLib version benefits. Use the exact triggerable-animation API present in the project, not copied syntax from another version.

======================================================================================
34. ANIMATION-EVENT SYNCHRONIZATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Separate animation-timed cosmetics from gameplay confirmation. Whoosh/equip/core pulses can be keyframe-driven. Successful damage, block breaks, crop growth or vein extraction must be triggered by server-authoritative gameplay logic. Damage/work must never depend on render FPS or whether a client skipped an animation frame.

======================================================================================
35. VANILLA GAMEPLAY BASE CLASS AND BEHAVIOR
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Implement the item using the project's real PickaxeItem (or established custom subclass) so it retains true pickaxe mining suitability, correct tags, drops, mining level, normal combat attributes, enchantments and durability. Do not replace vanilla tool behavior with a generic Item just to make GeckoLib easier. Preserve tags, interaction semantics, attack/mining attributes and vanilla action results appropriate to Minecraft 1.20.1.

======================================================================================
36. TOOL MATERIAL / COMBAT OR MINING BALANCE
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Reuse an existing FireDevilToolMaterial if present. If absent, derive values from the mod's progression and compare with Netherite and other endgame sets. Keep named constants for durability, mining speed, attack damage and enchantability. Do not use absurd values unless the mod's established progression explicitly requires them.

======================================================================================
37. DURABILITY BEHAVIOR
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Normal durability follows standard item semantics. For the unique ability, follow this item-specific rule: durability is charged per successfully mined ore through normal item-damage semantics, so 20 ores do not cost only one durability point. Use ItemStack damage APIs compatible with Unbreaking/creative behavior where appropriate. Never perform the full gameplay effect and only afterwards discover the tool should have broken halfway through.

======================================================================================
38. ENCHANTMENTS AND VANILLA COMPATIBILITY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Preserve appropriate vanilla enchantments and loot/interaction semantics. Efficiency/Sharpness/Fortune/Silk Touch/Unbreaking/Mending compatibility depends on item type; do not disable them accidentally. Special abilities must explicitly define how enchantments interact instead of silently duplicating drops or multiplying damage unexpectedly.

======================================================================================
39. UNIQUE ABILITY CONCEPT
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. **MAGMA VEIN / FORGEHEART EXTRACTION** is the mandatory unique mechanic. RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated. This ability is part of the production definition, not an optional idea. Implement it only after ordinary item behavior is correct so the special system cannot hide broken base gameplay.

======================================================================================
40. ABILITY ACTIVATION INPUT AND VALIDATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Activation must be deterministic and context-aware. RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated. Validate the held item, hand/context, cooldown and server-side state before committing. Invalid use must not consume durability or start a fake successful animation. One user input should create one ability execution, not repeated triggers every use tick.

======================================================================================
41. ABILITY TARGETING / AFFECTED REGION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Targeting is strictly bounded: connected valid ore positions beginning at the clicked ore, bounded to at most 32 blocks and a limited search radius; never an unbounded world/chunk scan. Build the target set once per use with hard numerical limits. Never replace a bounded local calculation with a whole-world scan. Solid collision, block suitability or crop/ore validity must be respected according to this item's design.

======================================================================================
42. SERVER-AUTHORITATIVE ABILITY EXECUTION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. The server is authoritative for every gameplay consequence of MAGMA VEIN / FORGEHEART EXTRACTION: target selection, damage/block/crop changes, cooldown, durability and state transitions. Client-side code may predict harmless visual startup, but cannot decide outcomes. Keep MinecraftClient and renderer classes out of common/server class paths.

======================================================================================
43. ABILITY STATE MACHINE
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Use an explicit, finite state flow rather than scattered booleans. For this ability incorporate the special constraint: use iterative queue/BFS with visited set and hard count/radius limits; stop safely when tool breaks, chunks are unavailable, protection denies a block, or the block changed. Every active cast/operation must have a clear start, progress/resolve phase and cleanup. World unload, player disconnect or invalid target must not leave stale global state.

======================================================================================
44. ABILITY GAMEPLAY RESOLUTION RULES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Gameplay resolution must follow the exact item-specific promise: RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated. Prevent accidental duplicate effects caused by overlapping samples, repeated ticks or client/server double execution. Preserve normal protection, loot, PvP and block-update semantics rather than bypassing them with raw uncontrolled world mutation.

======================================================================================
45. ABILITY COOLDOWN SEMANTICS
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Cooldown semantics: 6 seconds for the vein ability; ordinary pickaxe mining remains available during cooldown. Use a named constant and the project's cooldown system. Cooldown should begin only at the correct committed stage. Never let the ability cooldown unintentionally disable unrelated ordinary item actions unless explicitly required by this design.

======================================================================================
46. ABILITY DURABILITY / RESOURCE COST
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Ability cost: durability is charged per successfully mined ore through normal item-damage semantics, so 20 ores do not cost only one durability point. Apply cost exactly once at the intended successful stage, or per successfully processed block only where this item's definition calls for it. Invalid/no-op actions cost nothing. Stop safely if the item breaks during multi-block work.

======================================================================================
47. ABILITY VFX TIMELINE
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Create a tightly choreographed VFX timeline: central core flares -> orange fractures race into both pick arms -> connected ore cells receive sparse forge sparks -> extraction ripples outward rapidly -> core settles. Favor a small number of layered purposeful effects—hot core, emissive path, sparks, ash, contact flash—over hundreds of identical particles. First-person effects must preserve visibility; world-visible effects must make the action understandable to observers.

======================================================================================
48. ABILITY SOUND DESIGN
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Sound identity: one heavy pick strike plus a low furnace ignition and rate-limited cracking/forge ticks, never 32 full-volume sounds. Use layering and pitch variation intentionally, but aggregate repeated multi-target/multi-block events so the action does not produce dozens of maximum-volume identical sounds. Keep ordinary tool sounds recognizable beneath the infernal accent.

======================================================================================
49. ABILITY NETWORKING AND SYNCHRONIZATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Use efficient synchronization. Prefer normal world/entity synchronization or one compact ability event containing origin/direction/seed/positions over one custom packet per particle. The server remains authoritative even if clients reconstruct deterministic visuals from a seed. Avoid trusting client-reported hit lists or block lists.

======================================================================================
50. ABILITY MULTIPLAYER BEHAVIOR
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Test simultaneous multiplayer use. Every player/cast/area operation needs independent state; never store 'current target/current cast' in one global mutable variable. Nearby observers should see important world effects, while camera-only micro-effects may remain local. Handle latency without changing gameplay damage/work result.

======================================================================================
51. NORMAL-USE VFX
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Ordinary attacks/mining/tilling should use restrained Fire Devil feedback: brief core pulse, a few orange forge sparks or a short translucent dark-orange trail, while preserving vanilla material/block particles. Do not make every basic action visually equal to the special ability.

======================================================================================
52. SUCCESSFUL HIT / SUCCESSFUL WORK VFX
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Successful confirmed work/hits should add localized feedback at the actual target/block: compact orange-white contact flash, sparse metal/ember sparks, brief core response and normal block debris where relevant. Misses/no-op interactions must not spawn a fake success burst.

======================================================================================
53. CRITICAL / HIGH-VALUE RESULT VFX
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Critical hits or especially valuable successful results may receive a slightly brighter star/core pulse and a modest particle increase, but never auto-trigger the full unique ability unless explicitly designed. Keep special activation visually distinct and readable.

======================================================================================
54. PARTICLE BUDGET AND LIFETIME
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Set explicit budgets. Normal action: roughly single-digit to low-teens custom particles. Special ability: bounded tens, scaled to fixed target cap. Most particles should die within 0.1–0.6 seconds. Never spawn particles every tick merely because the item is held or because a long status/cooldown is active.

======================================================================================
55. ORDINARY-USE SOUND LAYERING
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Ordinary sound should preserve the physical role—blade whoosh, pick impact, soil scrape, etc.—then add a restrained forged-metal/furnace overtone. Avoid stacking five loud sounds on every mundane action. Special ability receives the more elaborate audio signature.

======================================================================================
56. ENVIRONMENTAL SAFETY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. The infernal aesthetic does NOT automatically authorize griefing. By default, never create fire blocks, lava, TNT-like explosions or permanent burning terrain unless the specific ability explicitly requires it—which these designs do not. Cosmetic embers and entity fire status are separate from world fire placement.

======================================================================================
57. WORLD/BLOCK INTERACTION SAFETY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. World/block changes are limited to this item's legitimate rules: RMB on a valid ore block performs a bounded connected-vein extraction. It searches only matching/compatible connected ore blocks, with a hard cap of 32 blocks and a small maximum radius. Blocks are broken through legitimate server loot logic. If a mined ore drop has a valid furnace-smelting result and Silk Touch is not active, the ability may automatically forge-smelt that drop. Silk Touch preserves the ore block; Fortune must not be bypassed or duplicated. Respect block hardness/suitability, crops/farmland safety, loot contexts, world border, chunk availability and protection hooks where the project exposes them. Do not use force-loading or raw setBlockState loops to bypass gameplay systems.

======================================================================================
58. ENTITY FILTERING AND FRIENDLY-FIRE BEHAVIOR
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Respect teams, PvP/friendly-fire, creative/spectator rules, invulnerable entities and caster exclusion for combat abilities. Farming/mining abilities should not damage entities unless explicitly stated. Deduplicate targets per cast so overlapping effect geometry cannot multiply unintended damage.

======================================================================================
59. PERFORMANCE SAFEGUARDS
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Hard-code safe upper bounds for every search, target list, area size and duration. No whole-world scans, no unbounded recursion, no Thread.sleep, no rendering-dependent gameplay and no long-lived unused state. Rate-limit particles/sounds under fast mining or repeated work.

======================================================================================
60. INVALID-USE AND NO-OP BEHAVIOR
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Invalid use must be cheap and predictable. If cooldown is active, target/context is invalid, protection denies action, tool is broken, crop is mature, ore search finds nothing, or no eligible blocks exist, do not consume durability or play full successful VFX. Return/fall back using the correct Minecraft action result.

======================================================================================
61. EDGE CASES AND FAILURE RECOVERY
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Handle edge cases explicitly for this ability, including: use iterative queue/BFS with visited set and hard count/radius limits; stop safely when tool breaks, chunks are unavailable, protection denies a block, or the block changed. Also test chunk boundaries, world border, target changes between validation and execution, dimension change, disconnect, tool break, high latency, offhand, creative mode, and concurrent players. Cleanup must be idempotent and safe.

======================================================================================
62. REQUIRED RESOURCE FILES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Expected resources normally include assets/<modid>/geo/fire_devil_pickaxe.geo.json, animations/fire_devil_pickaxe.animation.json, textures/item/fire_devil_pickaxe.png, item model JSON if renderer requires it, lang entries, optional particle textures and sounds.json entries. Follow the project's actual namespace/path conventions exactly.

======================================================================================
63. LOCALIZATION AND TOOLTIP
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Add en_us and any existing project languages. Tooltip should state the unique mechanic in player-facing terms, e.g. 'MAGMA VEIN / FORGEHEART EXTRACTION' and its main range/area, without implementation jargon. Keep names consistent across registry ID, translation key, advancements/recipes if any.

======================================================================================
64. CODE ARCHITECTURE AND CLASS RESPONSIBILITIES
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Prefer a focused FireDevilPickaxeItem class plus existing/shared model and renderer patterns. Put complex bounded area/target algorithms into small helpers only when that improves clarity. Reuse shared FireDevilToolMaterial, VFX, sound and animation utilities instead of copy-pasting five divergent systems.

======================================================================================
65. JSON/RESOURCE IDENTIFIER VALIDATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Validate every identifier: Java animation trigger strings, geo filename, texture path, namespace, sound ID, particle ID, translation key and JSON schema. Run resource reload where possible. A one-character mismatch that yields missing texture or silent animation means the task is not done.

======================================================================================
66. MODEL GAPS, SEAMS AND Z-FIGHTING QA
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Inspect the final model for unintended holes and seams around central thick socket, two segmented curved pick arms with tapered functional tips, recessed crack channels, square furnace core, long wrapped shaft, collars and cubic pommel. Distinguish deliberate magma channels/recesses from accidental open geometry. Remove z-fighting from coplanar plates, close missing side faces, fix mirrored gaps, and verify there are no zero-size cubes or floating decorative components.

======================================================================================
67. GAMEPLAY TEST MATRIX
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Gameplay QA must cover ordinary behavior plus MAGMA VEIN / FORGEHEART EXTRACTION. Test valid/invalid use, cooldown, durability, low-durability break, enchantments, multiplayer, protection/solid obstacles or block suitability as relevant, repeated use, and concurrency. Verify actual server results, not only pretty animation.

======================================================================================
68. VISUAL TEST MATRIX
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Visual QA: inspect front/back/left/right/top/bottom and 3/4 views, first-person at several FOVs, offhand, third-person movement/actions, GUI, dropped item, item frame, bright daylight and dark environments. Confirm emissive hierarchy, correct working orientation, no camera obstruction, no gaps/z-fighting and coherent animation.

======================================================================================
69. BUILD AND RUNCLIENT VALIDATION
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. Run the actual Gradle wrapper build and then runClient when available. Read compiler/resource/runtime logs, fix errors, reload resources, and repeat until stable. If dedicated-server run is available, verify no client-only renderer/model class causes classloading failure.

======================================================================================
70. FINAL DEFINITION OF DONE
======================================================================================
**Item-specific target:** a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel. The item is DONE only when it strongly matches the supplied concept (a broad symmetrical infernal pickaxe with two black volcanic pick arms curving downward from a massive square furnace socket, orange magma fractures running through the head, a long leather-wrapped shaft, metal collars and a heated square pommel); geometry is clean and connected; UV/texture/emissive layers are polished; first/third/GUI/ground transforms are correct; GeckoLib animations work; ordinary PickaxeItem behavior remains intact; **MAGMA VEIN / FORGEHEART EXTRACTION** behaves exactly as specified with server authority, safe cooldown/cost/networking/performance; no unintended world grief occurs; and build/runtime validation succeeds.

END OF PROMPT.
```

---


# Fire Devil Axe — 70-POINT ULTRA-DETAILED PROMPT

![Fire Devil Axe concept](concept_art/fire_devil_axe.png)

```text
# FIRE DEVIL AXE — MASTER PRODUCTION TASK
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench
# Recommended registry id: fire_devil_axe

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench 3D modeler, Minecraft low-poly artist, pixel texture artist, animator, gameplay programmer, VFX/sound designer, networking engineer, optimization engineer and QA engineer.

This is not a concept-only task. Inspect the actual existing project first, then IMPLEMENT the item and verify it in-game. Use the exact installed Fabric/Yarn/GeckoLib APIs. Do not use Forge, NeoForge, incompatible version examples, imagined methods or pseudocode in place of compiling code.

Shared FIRE DEVIL visual language:
- fractured black volcanic steel / obsidian-like forged metal;
- incandescent orange-red magma fissures with tiny yellow-hot cores;
- square/diamond furnace cores trapped inside heavy forged frames;
- dark heat-blackened leather wrapping;
- stepped brutal architectural plates, bevels and collars;
- restrained sparks, embers and ash rather than permanent screen-filling fire.
The set must look forged by the same infernal civilization, not like five unrelated red recolors.

PRIMARY VISUAL TARGET: a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel.
MANDATORY UNIQUE ABILITY: HELLCLEAVER — One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks.

======================================================================================
1. PROJECT AUDIT AND EXACT VERSION VERIFICATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Before touching code or assets, inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric Loader/API versions, GeckoLib dependency, Java version, package structure, ModItems, ToolMaterial classes, renderers, client initializer, existing Fire Devil tools, sound/particle registries, networking, and any helper utilities. Do not assume an API because an online example looks similar. If the project already contains a working animated AxeItem, treat that implementation as the technical reference while preserving this item's unique visual/gameplay identity. Record exact resource namespace and file conventions before creating anything.

======================================================================================
2. REFERENCE DECOMPOSITION AND VISUAL MEASUREMENT
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Study the supplied per-item concept and the full-set sheet. Decompose the object into measurable masses: thick square head socket, one huge crescent blade with real thickness and inner cutout, hot tapered cutting rim, rear reinforcement, wrapped shaft, collars and core pommel. Note which silhouette features define recognition, which details can be texture-only, which components need depth, where emissive cracks originate, and how the object is expected to connect structurally. Inspect the reference from an imagined front/side/3/4 view and infer hidden rear geometry conservatively rather than inventing unrelated machinery.

======================================================================================
3. SILHOUETTE LOCK BEFORE DETAIL WORK
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Create a flat-color silhouette blockout and judge it before any ornamentation. At normal gameplay distance the item must be recognizable solely from geometry. Do not use cracks, emissive colors or tiny details to hide incorrect proportions. If the silhouette is wrong, stop and correct it before proceeding.

======================================================================================
4. OVERALL PROPORTIONS AND MINECRAFT SCALE
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Establish a consistent Blockbench coordinate system and compare the item with player hand/body scale and the other Fire Devil tools. Preserve the relative visual weight from the reference. The item may be legendary and larger than vanilla, but must remain usable in first person and readable in inventory. Document the final model scale so later transforms do not compensate for arbitrary export scaling.

======================================================================================
5. PRIMARY BLOCKOUT WORKFLOW
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Build only the primary masses first: thick square head socket, one huge crescent blade with real thickness and inner cutout, hot tapered cutting rim, rear reinforcement, wrapped shaft, collars and core pommel. Keep the blockout low complexity and physically connected. Validate working direction and grip orientation now, before UVs and animation. Do not proceed to cracks, rivets, runes or particles until the blockout survives front/back/side/top/3/4 inspection.

======================================================================================
6. SECONDARY FORMS AND STRUCTURAL LAYERING
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Add secondary structural plates, sockets, collars, recesses, ribs and working-edge reinforcement in a hierarchy that makes physical sense. Every visible major plate should either connect to another component or be clearly mounted. Avoid floating decoration and accidental interior holes. Use repeated Fire Devil motifs consistently across the set without copying another tool's silhouette.

======================================================================================
7. SIDE PROFILE AND PHYSICAL THICKNESS
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Give every major working component real side depth. Separate rear structural thickness, middle body plate, recessed inner panel/channel, and thinner working edge where appropriate. The item must not look like a 2D concept image extruded by one pixel. Check side and 3/4 views for believable mass and ensure the hand/shaft connection is structurally thick enough.

======================================================================================
8. BEVELS, EDGES, TIPS AND WORKING SURFACES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Use deliberate low-poly chamfers instead of high-segment bevels. Working tips/edges should transition from thick structural body to narrower edge through a few readable planes. Corners, sockets and pommels may use stepped bevels. Never add dozens of tiny cubes for curvature that will be invisible in gameplay.

======================================================================================
9. MATERIAL HIERARCHY AND READABILITY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Keep four material families visually separable: dark volcanic metal, incandescent magma/emissive cracks, dark wrapped grip, and infernal cores. Use geometry depth plus value contrast—not color alone—to distinguish them. The black body should still be readable in darkness and the orange glow should remain an accent rather than flooding every surface.

======================================================================================
10. BLACK VOLCANIC METAL TEXTURING
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Paint volcanic metal using broad charcoal/blue-black planes, medium-gray chipped bevels, sparse forged pits and controlled scratches. Avoid uniform pure black and avoid noisy rock photographs. Working areas may show brighter abrasion. Recesses can approach near-black, but silhouette edges need enough value separation for Minecraft lighting.

======================================================================================
11. INCANDESCENT MAGMA CRACK DESIGN
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Design magma fractures as stress-driven networks that originate around the core, joints and working edge. Use a hot center hierarchy: tiny pale-yellow/white-orange pixels at peaks, orange core, red-orange falloff, dark red heat halo. Do not draw random equal-brightness scribbles everywhere; secondary cracks must remain subordinate to the principal energy path.

======================================================================================
12. INFERNAL CORE / GEM CONSTRUCTION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Model each infernal core as a physical socket with an inset faceted hot center and surrounding dark frame. The core should look trapped inside forged metal. Give the brightest region a small area so emission feels intense rather than flat. Reuse the same core language across the set while scaling shape/size to this item.

======================================================================================
13. HANDLE, GRIP AND WRAPPING CONSTRUCTION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Construct the grip as dark heat-blackened leather/hide or tightly wrapped material over a rigid shaft/tang. Use diagonal or crossed wrap bands, subtle brown-black value variation, and forged collars. Keep the hand-contact area visually calmer than the head/blade so the grip location remains obvious.

======================================================================================
14. HEAT WEAR, SOOT AND EDGE AGING
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Add restrained heat wear: dark red-brown discoloration near cores and working edges, small soot deposits in recesses, and bright worn metal on exposed bevels. Do not rust the set green/brown or cover everything in dirt. These are maintained infernal artifacts, not abandoned scrap.

======================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Prefer 256x256 texture for this high-detail GeckoLib item unless the existing set uses 128x128. Maintain consistent texel density across all five tools. Allocate more pixels to focal front faces, cores and working edges; allocate fewer to hidden undersides. Tiny details that disappear at inventory scale should be simplified.

======================================================================================
16. UV LAYOUT AND ISLAND PADDING
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Create clean UV islands with padding, logical orientation and minimal distortion. Separate front/back focal faces where unique fracture patterns matter. Mirror only genuinely symmetrical surfaces where duplicated wear is acceptable. Keep emissive orange islands away from unrelated dark islands to prevent filtering/bleeding.

======================================================================================
17. PIXEL-ART TEXTURE PAINTING RULES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Use crisp Minecraft-compatible pixel shading. Do not bake strong environmental highlights from the concept art into the texture. Build depth with edge highlights, plate-to-plate occlusion shadows, hot crack cores and controlled material variation. Avoid blurry photographic gradients and excessive antialiasing.

======================================================================================
18. EMISSIVE-LAYER IMPLEMENTATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Inspect the project for an existing GeckoLib emissive/render-layer solution. If supported, use emission only on core centers, selected magma crack centers and hot working strips. Outer metal, grip and most crack falloff remain normally lit. If no clean emissive system exists, use bright texture values and particles rather than installing a heavy shader dependency solely for this set.

======================================================================================
19. GEOMETRY BUDGET AND OPTIMIZATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Optimize deliberately: geometry for silhouette, thickness, major bevels, sockets, cores and major plates; textures for micro-cracks, scratches, tiny rivets and engraved seams. Remove hidden duplicate cubes, zero-size geometry and unseen internal faces. Normal idle rendering should add negligible cost compared with another GeckoLib item.

======================================================================================
20. GECKOLIB BONE HIERARCHY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Create a small meaningful bone tree: root -> item -> main working assembly/head/blade -> handle -> pommel -> optional FX bones. Sub-bones exist only when animation or organization benefits. Do not create one bone per decorative plate. Use names that are stable, snake_case or project-consistent, and easy to reference in animation JSON.

======================================================================================
21. BONE PIVOTS AND ROTATION ORIGINS
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Place pivots at physical joints: main head/blade pivot near the shaft/hilt connection, handle pivot along the grip axis, pommel at lower connector, cores at their centers, and working sub-parts at actual attachment points. Bad pivots create 'exploding' animation even with correct keyframes, so validate each pivot in Blockbench before export.

======================================================================================
22. ROOT ORIGIN AND HELD-ITEM REFERENCE POINT
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Place root/origin around the natural held-item reference rather than blindly at geometric center. The origin must support first person, third person, GUI and dropped transforms without extreme translations. Follow the same convention as already-working set items when possible to simplify shared renderer logic.

======================================================================================
23. FIRST-PERSON RIGHT-HAND TRANSFORM
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Tune first-person right hand only after the model orientation is correct. The hand must visibly contact the grip, the functional edge must face the correct working/attack direction, and the main head/blade should remain readable without covering the crosshair. Test normal and low/high FOV, idle and action animation.

======================================================================================
24. FIRST-PERSON LEFT/OFFHAND TRANSFORM
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Test offhand/left-hand rendering independently. Do not assume automatic mirroring preserves working direction. Correct mirrored yaw/roll or use display-context-specific transforms so the item does not suddenly face backwards, expose only its thin side, or intersect the camera.

======================================================================================
25. THIRD-PERSON TRANSFORM AND HAND CONTACT
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. In third person, align the player's hand with the actual grip and keep the working end logically forward during attacks/mining/tilling. Test standing, walking, sprinting, jumping, sneaking and action states. Small Minecraft-style clipping is acceptable; gross torso/head penetration or a floating grip is not.

======================================================================================
26. GUI INVENTORY TRANSFORM
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Create a dedicated GUI transform that shows the strongest 3/4 silhouette, the infernal core and emissive fractures. Fit the entire item into the slot without cropping major working geometry. Do not simply reuse first-person transforms.

======================================================================================
27. DROPPED-ITEM AND ITEM-FRAME TRANSFORM
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. For ground/item-frame display, preserve sensible scale and a stable attractive angle. The item should not become building-sized or vanish into a block. Verify item-frame depth so thick GeckoLib geometry does not clip almost entirely through the wall.

======================================================================================
28. IDLE ANIMATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Idle animation should be restrained and loop smoothly for roughly 2.5–4 seconds: a 1–2% core pulse, tiny heat breathing, and at most fractions of a degree of rigid secondary movement. Do not make a forged tool constantly wobble or emit a permanent flame fountain.

======================================================================================
29. EQUIP ANIMATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Equip animation should be short and responsive, around 0.25–0.45 seconds: raise from a slightly lowered pose, tiny heavy overshoot, brief core brightening, settle. Avoid full spins, anime flourishes or animation that delays actual gameplay control.

======================================================================================
30. PRIMARY ATTACK / WORK ANIMATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Design the primary action animation around this item's real role: true axe behavior including axe-effective blocks, stripping/interactions where applicable, heavy melee attributes, enchantments and normal durability. Use anticipation -> fast working/attack motion -> clear impact/contact frame -> physical follow-through -> recovery. If vanilla player-hand motion already supplies the main swing, let GeckoLib add internal inertia and core response instead of doubling root rotation.

======================================================================================
31. SECONDARY INERTIA AND MECHANICAL MOTION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Secondary motion must communicate rigid mass: shaft/hand begins motion, heavy head/blade lags by a few degrees, catches up near impact, then slightly overshoots during recovery. Metal plates do not flex like rubber. Small core/socket counter-rotation can enrich close-up animation without looking mechanical.

======================================================================================
32. MAGMA/CORE PULSE ANIMATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Animate heat as a short energy flow rather than constant maximal glow. A lower core/pommel may brighten first, followed by the main head/core and working crack network. Peak emission aligns with impact or special release, then fades rapidly to idle. Keep ordinary idle dark enough that special activation feels meaningful.

======================================================================================
33. ANIMATION CONTROLLERS AND PRIORITIES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Define controller priority so mutually exclusive actions never fight over root bones. A safe conceptual order is special ability > normal attack/work > equip > idle, with a separate FX controller only if the installed GeckoLib version benefits. Use the exact triggerable-animation API present in the project, not copied syntax from another version.

======================================================================================
34. ANIMATION-EVENT SYNCHRONIZATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Separate animation-timed cosmetics from gameplay confirmation. Whoosh/equip/core pulses can be keyframe-driven. Successful damage, block breaks, crop growth or vein extraction must be triggered by server-authoritative gameplay logic. Damage/work must never depend on render FPS or whether a client skipped an animation frame.

======================================================================================
35. VANILLA GAMEPLAY BASE CLASS AND BEHAVIOR
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Implement the item using the project's real AxeItem (or established custom subclass) so it retains true axe behavior including axe-effective blocks, stripping/interactions where applicable, heavy melee attributes, enchantments and normal durability. Do not replace vanilla tool behavior with a generic Item just to make GeckoLib easier. Preserve tags, interaction semantics, attack/mining attributes and vanilla action results appropriate to Minecraft 1.20.1.

======================================================================================
36. TOOL MATERIAL / COMBAT OR MINING BALANCE
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Reuse an existing FireDevilToolMaterial if present. If absent, derive values from the mod's progression and compare with Netherite and other endgame sets. Keep named constants for durability, mining speed, attack damage and enchantability. Do not use absurd values unless the mod's established progression explicitly requires them.

======================================================================================
37. DURABILITY BEHAVIOR
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Normal durability follows standard item semantics. For the unique ability, follow this item-specific rule: about 5 durability once per released cast, not once per arc or target. Use ItemStack damage APIs compatible with Unbreaking/creative behavior where appropriate. Never perform the full gameplay effect and only afterwards discover the tool should have broken halfway through.

======================================================================================
38. ENCHANTMENTS AND VANILLA COMPATIBILITY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Preserve appropriate vanilla enchantments and loot/interaction semantics. Efficiency/Sharpness/Fortune/Silk Touch/Unbreaking/Mending compatibility depends on item type; do not disable them accidentally. Special abilities must explicitly define how enchantments interact instead of silently duplicating drops or multiplying damage unexpectedly.

======================================================================================
39. UNIQUE ABILITY CONCEPT
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. **HELLCLEAVER** is the mandatory unique mechanic. One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks. This ability is part of the production definition, not an optional idea. Implement it only after ordinary item behavior is correct so the special system cannot hide broken base gameplay.

======================================================================================
40. ABILITY ACTIVATION INPUT AND VALIDATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Activation must be deterministic and context-aware. One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks. Validate the held item, hand/context, cooldown and server-side state before committing. Invalid use must not consume durability or start a fake successful animation. One user input should create one ability execution, not repeated triggers every use tick.

======================================================================================
41. ABILITY TARGETING / AFFECTED REGION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Targeting is strictly bounded: forward fan roughly 9–12 blocks long and about 110–130 degrees wide, represented by three bounded arc sectors with solid-world occlusion. Build the target set once per use with hard numerical limits. Never replace a bounded local calculation with a whole-world scan. Solid collision, block suitability or crop/ore validity must be respected according to this item's design.

======================================================================================
42. SERVER-AUTHORITATIVE ABILITY EXECUTION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. The server is authoritative for every gameplay consequence of HELLCLEAVER: target selection, damage/block/crop changes, cooldown, durability and state transitions. Client-side code may predict harmless visual startup, but cannot decide outcomes. Keep MinecraftClient and renderer classes out of common/server class paths.

======================================================================================
43. ABILITY STATE MACHINE
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Use an explicit, finite state flow rather than scattered booleans. For this ability incorporate the special constraint: one controlled heavy damage instance per valid target, optionally short entity-only burning and modest knockback; no triple-damage from arc overlap. Every active cast/operation must have a clear start, progress/resolve phase and cleanup. World unload, player disconnect or invalid target must not leave stale global state.

======================================================================================
44. ABILITY GAMEPLAY RESOLUTION RULES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Gameplay resolution must follow the exact item-specific promise: One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks. Prevent accidental duplicate effects caused by overlapping samples, repeated ticks or client/server double execution. Preserve normal protection, loot, PvP and block-update semantics rather than bypassing them with raw uncontrolled world mutation.

======================================================================================
45. ABILITY COOLDOWN SEMANTICS
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Cooldown semantics: 8 seconds for Hellcleaver; normal melee and axe block work remain usable during cooldown. Use a named constant and the project's cooldown system. Cooldown should begin only at the correct committed stage. Never let the ability cooldown unintentionally disable unrelated ordinary item actions unless explicitly required by this design.

======================================================================================
46. ABILITY DURABILITY / RESOURCE COST
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Ability cost: about 5 durability once per released cast, not once per arc or target. Apply cost exactly once at the intended successful stage, or per successfully processed block only where this item's definition calls for it. Invalid/no-op actions cost nothing. Stop safely if the item breaks during multi-block work.

======================================================================================
47. ABILITY VFX TIMELINE
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Create a tightly choreographed VFX timeline: head core flares -> crescent edge becomes yellow-hot -> three staggered orange-black crescent ribbons split across the fan -> confirmed targets emit compact sparks/ash -> arcs vanish within fractions of a second. Favor a small number of layered purposeful effects—hot core, emissive path, sparks, ash, contact flash—over hundreds of identical particles. First-person effects must preserve visibility; world-visible effects must make the action understandable to observers.

======================================================================================
48. ABILITY SOUND DESIGN
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Sound identity: deep windup, one massive cleave whoosh with restrained three-part fiery tearing, compact impacts only on confirmed targets. Use layering and pitch variation intentionally, but aggregate repeated multi-target/multi-block events so the action does not produce dozens of maximum-volume identical sounds. Keep ordinary tool sounds recognizable beneath the infernal accent.

======================================================================================
49. ABILITY NETWORKING AND SYNCHRONIZATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Use efficient synchronization. Prefer normal world/entity synchronization or one compact ability event containing origin/direction/seed/positions over one custom packet per particle. The server remains authoritative even if clients reconstruct deterministic visuals from a seed. Avoid trusting client-reported hit lists or block lists.

======================================================================================
50. ABILITY MULTIPLAYER BEHAVIOR
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Test simultaneous multiplayer use. Every player/cast/area operation needs independent state; never store 'current target/current cast' in one global mutable variable. Nearby observers should see important world effects, while camera-only micro-effects may remain local. Handle latency without changing gameplay damage/work result.

======================================================================================
51. NORMAL-USE VFX
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Ordinary attacks/mining/tilling should use restrained Fire Devil feedback: brief core pulse, a few orange forge sparks or a short translucent dark-orange trail, while preserving vanilla material/block particles. Do not make every basic action visually equal to the special ability.

======================================================================================
52. SUCCESSFUL HIT / SUCCESSFUL WORK VFX
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Successful confirmed work/hits should add localized feedback at the actual target/block: compact orange-white contact flash, sparse metal/ember sparks, brief core response and normal block debris where relevant. Misses/no-op interactions must not spawn a fake success burst.

======================================================================================
53. CRITICAL / HIGH-VALUE RESULT VFX
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Critical hits or especially valuable successful results may receive a slightly brighter star/core pulse and a modest particle increase, but never auto-trigger the full unique ability unless explicitly designed. Keep special activation visually distinct and readable.

======================================================================================
54. PARTICLE BUDGET AND LIFETIME
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Set explicit budgets. Normal action: roughly single-digit to low-teens custom particles. Special ability: bounded tens, scaled to fixed target cap. Most particles should die within 0.1–0.6 seconds. Never spawn particles every tick merely because the item is held or because a long status/cooldown is active.

======================================================================================
55. ORDINARY-USE SOUND LAYERING
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Ordinary sound should preserve the physical role—blade whoosh, pick impact, soil scrape, etc.—then add a restrained forged-metal/furnace overtone. Avoid stacking five loud sounds on every mundane action. Special ability receives the more elaborate audio signature.

======================================================================================
56. ENVIRONMENTAL SAFETY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. The infernal aesthetic does NOT automatically authorize griefing. By default, never create fire blocks, lava, TNT-like explosions or permanent burning terrain unless the specific ability explicitly requires it—which these designs do not. Cosmetic embers and entity fire status are separate from world fire placement.

======================================================================================
57. WORLD/BLOCK INTERACTION SAFETY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. World/block changes are limited to this item's legitimate rules: One RMB press performs a fast heavy windup and releases THREE visually distinct molten crescent arcs in a forward fan: left, center and right. The three arcs create width and spectacle, but every entity is deduplicated and can receive damage at most once per cast even when standing in overlapping arcs. The fan is blocked by solid terrain and never breaks or burns blocks. Respect block hardness/suitability, crops/farmland safety, loot contexts, world border, chunk availability and protection hooks where the project exposes them. Do not use force-loading or raw setBlockState loops to bypass gameplay systems.

======================================================================================
58. ENTITY FILTERING AND FRIENDLY-FIRE BEHAVIOR
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Respect teams, PvP/friendly-fire, creative/spectator rules, invulnerable entities and caster exclusion for combat abilities. Farming/mining abilities should not damage entities unless explicitly stated. Deduplicate targets per cast so overlapping effect geometry cannot multiply unintended damage.

======================================================================================
59. PERFORMANCE SAFEGUARDS
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Hard-code safe upper bounds for every search, target list, area size and duration. No whole-world scans, no unbounded recursion, no Thread.sleep, no rendering-dependent gameplay and no long-lived unused state. Rate-limit particles/sounds under fast mining or repeated work.

======================================================================================
60. INVALID-USE AND NO-OP BEHAVIOR
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Invalid use must be cheap and predictable. If cooldown is active, target/context is invalid, protection denies action, tool is broken, crop is mature, ore search finds nothing, or no eligible blocks exist, do not consume durability or play full successful VFX. Return/fall back using the correct Minecraft action result.

======================================================================================
61. EDGE CASES AND FAILURE RECOVERY
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Handle edge cases explicitly for this ability, including: one controlled heavy damage instance per valid target, optionally short entity-only burning and modest knockback; no triple-damage from arc overlap. Also test chunk boundaries, world border, target changes between validation and execution, dimension change, disconnect, tool break, high latency, offhand, creative mode, and concurrent players. Cleanup must be idempotent and safe.

======================================================================================
62. REQUIRED RESOURCE FILES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Expected resources normally include assets/<modid>/geo/fire_devil_axe.geo.json, animations/fire_devil_axe.animation.json, textures/item/fire_devil_axe.png, item model JSON if renderer requires it, lang entries, optional particle textures and sounds.json entries. Follow the project's actual namespace/path conventions exactly.

======================================================================================
63. LOCALIZATION AND TOOLTIP
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Add en_us and any existing project languages. Tooltip should state the unique mechanic in player-facing terms, e.g. 'HELLCLEAVER' and its main range/area, without implementation jargon. Keep names consistent across registry ID, translation key, advancements/recipes if any.

======================================================================================
64. CODE ARCHITECTURE AND CLASS RESPONSIBILITIES
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Prefer a focused FireDevilAxeItem class plus existing/shared model and renderer patterns. Put complex bounded area/target algorithms into small helpers only when that improves clarity. Reuse shared FireDevilToolMaterial, VFX, sound and animation utilities instead of copy-pasting five divergent systems.

======================================================================================
65. JSON/RESOURCE IDENTIFIER VALIDATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Validate every identifier: Java animation trigger strings, geo filename, texture path, namespace, sound ID, particle ID, translation key and JSON schema. Run resource reload where possible. A one-character mismatch that yields missing texture or silent animation means the task is not done.

======================================================================================
66. MODEL GAPS, SEAMS AND Z-FIGHTING QA
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Inspect the final model for unintended holes and seams around thick square head socket, one huge crescent blade with real thickness and inner cutout, hot tapered cutting rim, rear reinforcement, wrapped shaft, collars and core pommel. Distinguish deliberate magma channels/recesses from accidental open geometry. Remove z-fighting from coplanar plates, close missing side faces, fix mirrored gaps, and verify there are no zero-size cubes or floating decorative components.

======================================================================================
67. GAMEPLAY TEST MATRIX
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Gameplay QA must cover ordinary behavior plus HELLCLEAVER. Test valid/invalid use, cooldown, durability, low-durability break, enchantments, multiplayer, protection/solid obstacles or block suitability as relevant, repeated use, and concurrency. Verify actual server results, not only pretty animation.

======================================================================================
68. VISUAL TEST MATRIX
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Visual QA: inspect front/back/left/right/top/bottom and 3/4 views, first-person at several FOVs, offhand, third-person movement/actions, GUI, dropped item, item frame, bright daylight and dark environments. Confirm emissive hierarchy, correct working orientation, no camera obstruction, no gaps/z-fighting and coherent animation.

======================================================================================
69. BUILD AND RUNCLIENT VALIDATION
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. Run the actual Gradle wrapper build and then runClient when available. Read compiler/resource/runtime logs, fix errors, reload resources, and repeat until stable. If dedicated-server run is available, verify no client-only renderer/model class causes classloading failure.

======================================================================================
70. FINAL DEFINITION OF DONE
======================================================================================
**Item-specific target:** a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel. The item is DONE only when it strongly matches the supplied concept (a brutal one-sided crescent execution axe: massive segmented black volcanic blade, bright molten cutting rim, internal orange fracture network, square infernal head socket, long wrapped handle and glowing pommel); geometry is clean and connected; UV/texture/emissive layers are polished; first/third/GUI/ground transforms are correct; GeckoLib animations work; ordinary AxeItem behavior remains intact; **HELLCLEAVER** behaves exactly as specified with server authority, safe cooldown/cost/networking/performance; no unintended world grief occurs; and build/runtime validation succeeds.

END OF PROMPT.
```

---


# Fire Devil Shovel — 70-POINT ULTRA-DETAILED PROMPT

![Fire Devil Shovel concept](concept_art/fire_devil_shovel.png)

```text
# FIRE DEVIL SHOVEL — MASTER PRODUCTION TASK
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench
# Recommended registry id: fire_devil_shovel

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench 3D modeler, Minecraft low-poly artist, pixel texture artist, animator, gameplay programmer, VFX/sound designer, networking engineer, optimization engineer and QA engineer.

This is not a concept-only task. Inspect the actual existing project first, then IMPLEMENT the item and verify it in-game. Use the exact installed Fabric/Yarn/GeckoLib APIs. Do not use Forge, NeoForge, incompatible version examples, imagined methods or pseudocode in place of compiling code.

Shared FIRE DEVIL visual language:
- fractured black volcanic steel / obsidian-like forged metal;
- incandescent orange-red magma fissures with tiny yellow-hot cores;
- square/diamond furnace cores trapped inside heavy forged frames;
- dark heat-blackened leather wrapping;
- stepped brutal architectural plates, bevels and collars;
- restrained sparks, embers and ash rather than permanent screen-filling fire.
The set must look forged by the same infernal civilization, not like five unrelated red recolors.

PRIMARY VISUAL TARGET: a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel.
MANDATORY UNIQUE ABILITY: INFERNAL EXCAVATION — RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square.

======================================================================================
1. PROJECT AUDIT AND EXACT VERSION VERIFICATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Before touching code or assets, inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric Loader/API versions, GeckoLib dependency, Java version, package structure, ModItems, ToolMaterial classes, renderers, client initializer, existing Fire Devil tools, sound/particle registries, networking, and any helper utilities. Do not assume an API because an online example looks similar. If the project already contains a working animated ShovelItem, treat that implementation as the technical reference while preserving this item's unique visual/gameplay identity. Record exact resource namespace and file conventions before creating anything.

======================================================================================
2. REFERENCE DECOMPOSITION AND VISUAL MEASUREMENT
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Study the supplied per-item concept and the full-set sheet. Decompose the object into measurable masses: thick rectangular outer frame, recessed inner spade face, tapered lower working lip, vertical hot fissure, upper socket/core, wrapped shaft, collars and pommel. Note which silhouette features define recognition, which details can be texture-only, which components need depth, where emissive cracks originate, and how the object is expected to connect structurally. Inspect the reference from an imagined front/side/3/4 view and infer hidden rear geometry conservatively rather than inventing unrelated machinery.

======================================================================================
3. SILHOUETTE LOCK BEFORE DETAIL WORK
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Create a flat-color silhouette blockout and judge it before any ornamentation. At normal gameplay distance the item must be recognizable solely from geometry. Do not use cracks, emissive colors or tiny details to hide incorrect proportions. If the silhouette is wrong, stop and correct it before proceeding.

======================================================================================
4. OVERALL PROPORTIONS AND MINECRAFT SCALE
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Establish a consistent Blockbench coordinate system and compare the item with player hand/body scale and the other Fire Devil tools. Preserve the relative visual weight from the reference. The item may be legendary and larger than vanilla, but must remain usable in first person and readable in inventory. Document the final model scale so later transforms do not compensate for arbitrary export scaling.

======================================================================================
5. PRIMARY BLOCKOUT WORKFLOW
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Build only the primary masses first: thick rectangular outer frame, recessed inner spade face, tapered lower working lip, vertical hot fissure, upper socket/core, wrapped shaft, collars and pommel. Keep the blockout low complexity and physically connected. Validate working direction and grip orientation now, before UVs and animation. Do not proceed to cracks, rivets, runes or particles until the blockout survives front/back/side/top/3/4 inspection.

======================================================================================
6. SECONDARY FORMS AND STRUCTURAL LAYERING
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Add secondary structural plates, sockets, collars, recesses, ribs and working-edge reinforcement in a hierarchy that makes physical sense. Every visible major plate should either connect to another component or be clearly mounted. Avoid floating decoration and accidental interior holes. Use repeated Fire Devil motifs consistently across the set without copying another tool's silhouette.

======================================================================================
7. SIDE PROFILE AND PHYSICAL THICKNESS
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Give every major working component real side depth. Separate rear structural thickness, middle body plate, recessed inner panel/channel, and thinner working edge where appropriate. The item must not look like a 2D concept image extruded by one pixel. Check side and 3/4 views for believable mass and ensure the hand/shaft connection is structurally thick enough.

======================================================================================
8. BEVELS, EDGES, TIPS AND WORKING SURFACES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Use deliberate low-poly chamfers instead of high-segment bevels. Working tips/edges should transition from thick structural body to narrower edge through a few readable planes. Corners, sockets and pommels may use stepped bevels. Never add dozens of tiny cubes for curvature that will be invisible in gameplay.

======================================================================================
9. MATERIAL HIERARCHY AND READABILITY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Keep four material families visually separable: dark volcanic metal, incandescent magma/emissive cracks, dark wrapped grip, and infernal cores. Use geometry depth plus value contrast—not color alone—to distinguish them. The black body should still be readable in darkness and the orange glow should remain an accent rather than flooding every surface.

======================================================================================
10. BLACK VOLCANIC METAL TEXTURING
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Paint volcanic metal using broad charcoal/blue-black planes, medium-gray chipped bevels, sparse forged pits and controlled scratches. Avoid uniform pure black and avoid noisy rock photographs. Working areas may show brighter abrasion. Recesses can approach near-black, but silhouette edges need enough value separation for Minecraft lighting.

======================================================================================
11. INCANDESCENT MAGMA CRACK DESIGN
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Design magma fractures as stress-driven networks that originate around the core, joints and working edge. Use a hot center hierarchy: tiny pale-yellow/white-orange pixels at peaks, orange core, red-orange falloff, dark red heat halo. Do not draw random equal-brightness scribbles everywhere; secondary cracks must remain subordinate to the principal energy path.

======================================================================================
12. INFERNAL CORE / GEM CONSTRUCTION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Model each infernal core as a physical socket with an inset faceted hot center and surrounding dark frame. The core should look trapped inside forged metal. Give the brightest region a small area so emission feels intense rather than flat. Reuse the same core language across the set while scaling shape/size to this item.

======================================================================================
13. HANDLE, GRIP AND WRAPPING CONSTRUCTION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Construct the grip as dark heat-blackened leather/hide or tightly wrapped material over a rigid shaft/tang. Use diagonal or crossed wrap bands, subtle brown-black value variation, and forged collars. Keep the hand-contact area visually calmer than the head/blade so the grip location remains obvious.

======================================================================================
14. HEAT WEAR, SOOT AND EDGE AGING
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Add restrained heat wear: dark red-brown discoloration near cores and working edges, small soot deposits in recesses, and bright worn metal on exposed bevels. Do not rust the set green/brown or cover everything in dirt. These are maintained infernal artifacts, not abandoned scrap.

======================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Prefer 256x256 texture for this high-detail GeckoLib item unless the existing set uses 128x128. Maintain consistent texel density across all five tools. Allocate more pixels to focal front faces, cores and working edges; allocate fewer to hidden undersides. Tiny details that disappear at inventory scale should be simplified.

======================================================================================
16. UV LAYOUT AND ISLAND PADDING
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Create clean UV islands with padding, logical orientation and minimal distortion. Separate front/back focal faces where unique fracture patterns matter. Mirror only genuinely symmetrical surfaces where duplicated wear is acceptable. Keep emissive orange islands away from unrelated dark islands to prevent filtering/bleeding.

======================================================================================
17. PIXEL-ART TEXTURE PAINTING RULES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Use crisp Minecraft-compatible pixel shading. Do not bake strong environmental highlights from the concept art into the texture. Build depth with edge highlights, plate-to-plate occlusion shadows, hot crack cores and controlled material variation. Avoid blurry photographic gradients and excessive antialiasing.

======================================================================================
18. EMISSIVE-LAYER IMPLEMENTATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Inspect the project for an existing GeckoLib emissive/render-layer solution. If supported, use emission only on core centers, selected magma crack centers and hot working strips. Outer metal, grip and most crack falloff remain normally lit. If no clean emissive system exists, use bright texture values and particles rather than installing a heavy shader dependency solely for this set.

======================================================================================
19. GEOMETRY BUDGET AND OPTIMIZATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Optimize deliberately: geometry for silhouette, thickness, major bevels, sockets, cores and major plates; textures for micro-cracks, scratches, tiny rivets and engraved seams. Remove hidden duplicate cubes, zero-size geometry and unseen internal faces. Normal idle rendering should add negligible cost compared with another GeckoLib item.

======================================================================================
20. GECKOLIB BONE HIERARCHY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Create a small meaningful bone tree: root -> item -> main working assembly/head/blade -> handle -> pommel -> optional FX bones. Sub-bones exist only when animation or organization benefits. Do not create one bone per decorative plate. Use names that are stable, snake_case or project-consistent, and easy to reference in animation JSON.

======================================================================================
21. BONE PIVOTS AND ROTATION ORIGINS
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Place pivots at physical joints: main head/blade pivot near the shaft/hilt connection, handle pivot along the grip axis, pommel at lower connector, cores at their centers, and working sub-parts at actual attachment points. Bad pivots create 'exploding' animation even with correct keyframes, so validate each pivot in Blockbench before export.

======================================================================================
22. ROOT ORIGIN AND HELD-ITEM REFERENCE POINT
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Place root/origin around the natural held-item reference rather than blindly at geometric center. The origin must support first person, third person, GUI and dropped transforms without extreme translations. Follow the same convention as already-working set items when possible to simplify shared renderer logic.

======================================================================================
23. FIRST-PERSON RIGHT-HAND TRANSFORM
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Tune first-person right hand only after the model orientation is correct. The hand must visibly contact the grip, the functional edge must face the correct working/attack direction, and the main head/blade should remain readable without covering the crosshair. Test normal and low/high FOV, idle and action animation.

======================================================================================
24. FIRST-PERSON LEFT/OFFHAND TRANSFORM
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Test offhand/left-hand rendering independently. Do not assume automatic mirroring preserves working direction. Correct mirrored yaw/roll or use display-context-specific transforms so the item does not suddenly face backwards, expose only its thin side, or intersect the camera.

======================================================================================
25. THIRD-PERSON TRANSFORM AND HAND CONTACT
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. In third person, align the player's hand with the actual grip and keep the working end logically forward during attacks/mining/tilling. Test standing, walking, sprinting, jumping, sneaking and action states. Small Minecraft-style clipping is acceptable; gross torso/head penetration or a floating grip is not.

======================================================================================
26. GUI INVENTORY TRANSFORM
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Create a dedicated GUI transform that shows the strongest 3/4 silhouette, the infernal core and emissive fractures. Fit the entire item into the slot without cropping major working geometry. Do not simply reuse first-person transforms.

======================================================================================
27. DROPPED-ITEM AND ITEM-FRAME TRANSFORM
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. For ground/item-frame display, preserve sensible scale and a stable attractive angle. The item should not become building-sized or vanish into a block. Verify item-frame depth so thick GeckoLib geometry does not clip almost entirely through the wall.

======================================================================================
28. IDLE ANIMATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Idle animation should be restrained and loop smoothly for roughly 2.5–4 seconds: a 1–2% core pulse, tiny heat breathing, and at most fractions of a degree of rigid secondary movement. Do not make a forged tool constantly wobble or emit a permanent flame fountain.

======================================================================================
29. EQUIP ANIMATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Equip animation should be short and responsive, around 0.25–0.45 seconds: raise from a slightly lowered pose, tiny heavy overshoot, brief core brightening, settle. Avoid full spins, anime flourishes or animation that delays actual gameplay control.

======================================================================================
30. PRIMARY ATTACK / WORK ANIMATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Design the primary action animation around this item's real role: true shovel mining and interaction behavior, correct shovel-mineable tags, legitimate drops, enchantments and durability. Use anticipation -> fast working/attack motion -> clear impact/contact frame -> physical follow-through -> recovery. If vanilla player-hand motion already supplies the main swing, let GeckoLib add internal inertia and core response instead of doubling root rotation.

======================================================================================
31. SECONDARY INERTIA AND MECHANICAL MOTION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Secondary motion must communicate rigid mass: shaft/hand begins motion, heavy head/blade lags by a few degrees, catches up near impact, then slightly overshoots during recovery. Metal plates do not flex like rubber. Small core/socket counter-rotation can enrich close-up animation without looking mechanical.

======================================================================================
32. MAGMA/CORE PULSE ANIMATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Animate heat as a short energy flow rather than constant maximal glow. A lower core/pommel may brighten first, followed by the main head/core and working crack network. Peak emission aligns with impact or special release, then fades rapidly to idle. Keep ordinary idle dark enough that special activation feels meaningful.

======================================================================================
33. ANIMATION CONTROLLERS AND PRIORITIES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Define controller priority so mutually exclusive actions never fight over root bones. A safe conceptual order is special ability > normal attack/work > equip > idle, with a separate FX controller only if the installed GeckoLib version benefits. Use the exact triggerable-animation API present in the project, not copied syntax from another version.

======================================================================================
34. ANIMATION-EVENT SYNCHRONIZATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Separate animation-timed cosmetics from gameplay confirmation. Whoosh/equip/core pulses can be keyframe-driven. Successful damage, block breaks, crop growth or vein extraction must be triggered by server-authoritative gameplay logic. Damage/work must never depend on render FPS or whether a client skipped an animation frame.

======================================================================================
35. VANILLA GAMEPLAY BASE CLASS AND BEHAVIOR
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Implement the item using the project's real ShovelItem (or established custom subclass) so it retains true shovel mining and interaction behavior, correct shovel-mineable tags, legitimate drops, enchantments and durability. Do not replace vanilla tool behavior with a generic Item just to make GeckoLib easier. Preserve tags, interaction semantics, attack/mining attributes and vanilla action results appropriate to Minecraft 1.20.1.

======================================================================================
36. TOOL MATERIAL / COMBAT OR MINING BALANCE
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Reuse an existing FireDevilToolMaterial if present. If absent, derive values from the mod's progression and compare with Netherite and other endgame sets. Keep named constants for durability, mining speed, attack damage and enchantability. Do not use absurd values unless the mod's established progression explicitly requires them.

======================================================================================
37. DURABILITY BEHAVIOR
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Normal durability follows standard item semantics. For the unique ability, follow this item-specific rule: one normal durability damage attempt per successfully broken block, stopping if the shovel breaks. Use ItemStack damage APIs compatible with Unbreaking/creative behavior where appropriate. Never perform the full gameplay effect and only afterwards discover the tool should have broken halfway through.

======================================================================================
38. ENCHANTMENTS AND VANILLA COMPATIBILITY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Preserve appropriate vanilla enchantments and loot/interaction semantics. Efficiency/Sharpness/Fortune/Silk Touch/Unbreaking/Mending compatibility depends on item type; do not disable them accidentally. Special abilities must explicitly define how enchantments interact instead of silently duplicating drops or multiplying damage unexpectedly.

======================================================================================
39. UNIQUE ABILITY CONCEPT
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. **INFERNAL EXCAVATION** is the mandatory unique mechanic. RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square. This ability is part of the production definition, not an optional idea. Implement it only after ordinary item behavior is correct so the special system cannot hide broken base gameplay.

======================================================================================
40. ABILITY ACTIVATION INPUT AND VALIDATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Activation must be deterministic and context-aware. RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square. Validate the held item, hand/context, cooldown and server-side state before committing. Invalid use must not consume durability or start a fake successful animation. One user input should create one ability execution, not repeated triggers every use tick.

======================================================================================
41. ABILITY TARGETING / AFFECTED REGION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Targeting is strictly bounded: exactly 25 candidate positions in a face-oriented 5x5x1 plane, with per-block suitability and protection validation. Build the target set once per use with hard numerical limits. Never replace a bounded local calculation with a whole-world scan. Solid collision, block suitability or crop/ore validity must be respected according to this item's design.

======================================================================================
42. SERVER-AUTHORITATIVE ABILITY EXECUTION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. The server is authoritative for every gameplay consequence of INFERNAL EXCAVATION: target selection, damage/block/crop changes, cooldown, durability and state transitions. Client-side code may predict harmless visual startup, but cannot decide outcomes. Keep MinecraftClient and renderer classes out of common/server class paths.

======================================================================================
43. ABILITY STATE MACHINE
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Use an explicit, finite state flow rather than scattered booleans. For this ability incorporate the special constraint: preserve Silk Touch/Fortune/loot/XP where applicable, falling-block updates, chunk safety and protection hooks; do not force-load chunks. Every active cast/operation must have a clear start, progress/resolve phase and cleanup. World unload, player disconnect or invalid target must not leave stale global state.

======================================================================================
44. ABILITY GAMEPLAY RESOLUTION RULES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Gameplay resolution must follow the exact item-specific promise: RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square. Prevent accidental duplicate effects caused by overlapping samples, repeated ticks or client/server double execution. Preserve normal protection, loot, PvP and block-update semantics rather than bypassing them with raw uncontrolled world mutation.

======================================================================================
45. ABILITY COOLDOWN SEMANTICS
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Cooldown semantics: 3 seconds for the mass-excavation action; ordinary single-block shovel mining remains available during cooldown. Use a named constant and the project's cooldown system. Cooldown should begin only at the correct committed stage. Never let the ability cooldown unintentionally disable unrelated ordinary item actions unless explicitly required by this design.

======================================================================================
46. ABILITY DURABILITY / RESOURCE COST
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Ability cost: one normal durability damage attempt per successfully broken block, stopping if the shovel breaks. Apply cost exactly once at the intended successful stage, or per successfully processed block only where this item's definition calls for it. Invalid/no-op actions cost nothing. Stop safely if the item breaks during multi-block work.

======================================================================================
47. ABILITY VFX TIMELINE
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Create a tightly choreographed VFX timeline: spade core flares -> thin orange frame pulse appears across the selected plane -> real block particles remain dominant -> sparse forge sparks sweep center-to-edge. Favor a small number of layered purposeful effects—hot core, emissive path, sparks, ash, contact flash—over hundreds of identical particles. First-person effects must preserve visibility; world-visible effects must make the action understandable to observers.

======================================================================================
48. ABILITY SOUND DESIGN
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Sound identity: one deep shovel impact, a short low forge rumble, and restrained material break feedback rather than 25 repeated loud sounds. Use layering and pitch variation intentionally, but aggregate repeated multi-target/multi-block events so the action does not produce dozens of maximum-volume identical sounds. Keep ordinary tool sounds recognizable beneath the infernal accent.

======================================================================================
49. ABILITY NETWORKING AND SYNCHRONIZATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Use efficient synchronization. Prefer normal world/entity synchronization or one compact ability event containing origin/direction/seed/positions over one custom packet per particle. The server remains authoritative even if clients reconstruct deterministic visuals from a seed. Avoid trusting client-reported hit lists or block lists.

======================================================================================
50. ABILITY MULTIPLAYER BEHAVIOR
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Test simultaneous multiplayer use. Every player/cast/area operation needs independent state; never store 'current target/current cast' in one global mutable variable. Nearby observers should see important world effects, while camera-only micro-effects may remain local. Handle latency without changing gameplay damage/work result.

======================================================================================
51. NORMAL-USE VFX
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Ordinary attacks/mining/tilling should use restrained Fire Devil feedback: brief core pulse, a few orange forge sparks or a short translucent dark-orange trail, while preserving vanilla material/block particles. Do not make every basic action visually equal to the special ability.

======================================================================================
52. SUCCESSFUL HIT / SUCCESSFUL WORK VFX
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Successful confirmed work/hits should add localized feedback at the actual target/block: compact orange-white contact flash, sparse metal/ember sparks, brief core response and normal block debris where relevant. Misses/no-op interactions must not spawn a fake success burst.

======================================================================================
53. CRITICAL / HIGH-VALUE RESULT VFX
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Critical hits or especially valuable successful results may receive a slightly brighter star/core pulse and a modest particle increase, but never auto-trigger the full unique ability unless explicitly designed. Keep special activation visually distinct and readable.

======================================================================================
54. PARTICLE BUDGET AND LIFETIME
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Set explicit budgets. Normal action: roughly single-digit to low-teens custom particles. Special ability: bounded tens, scaled to fixed target cap. Most particles should die within 0.1–0.6 seconds. Never spawn particles every tick merely because the item is held or because a long status/cooldown is active.

======================================================================================
55. ORDINARY-USE SOUND LAYERING
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Ordinary sound should preserve the physical role—blade whoosh, pick impact, soil scrape, etc.—then add a restrained forged-metal/furnace overtone. Avoid stacking five loud sounds on every mundane action. Special ability receives the more elaborate audio signature.

======================================================================================
56. ENVIRONMENTAL SAFETY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. The infernal aesthetic does NOT automatically authorize griefing. By default, never create fire blocks, lava, TNT-like explosions or permanent burning terrain unless the specific ability explicitly requires it—which these designs do not. Cosmetic embers and entity fire status are separate from world fire placement.

======================================================================================
57. WORLD/BLOCK INTERACTION SAFETY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. World/block changes are limited to this item's legitimate rules: RMB on a valid shovel-mineable block excavates a precise 5x5x1 plane centered on the clicked block. The plane follows the clicked face: top/bottom gives XZ, north/south gives XY, east/west gives ZY. Each of the maximum 25 positions is validated independently, and only blocks the shovel can legitimately mine are broken. It is not an explosion and never deletes stone, ores, containers or bedrock just because they are inside the square. Respect block hardness/suitability, crops/farmland safety, loot contexts, world border, chunk availability and protection hooks where the project exposes them. Do not use force-loading or raw setBlockState loops to bypass gameplay systems.

======================================================================================
58. ENTITY FILTERING AND FRIENDLY-FIRE BEHAVIOR
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Respect teams, PvP/friendly-fire, creative/spectator rules, invulnerable entities and caster exclusion for combat abilities. Farming/mining abilities should not damage entities unless explicitly stated. Deduplicate targets per cast so overlapping effect geometry cannot multiply unintended damage.

======================================================================================
59. PERFORMANCE SAFEGUARDS
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Hard-code safe upper bounds for every search, target list, area size and duration. No whole-world scans, no unbounded recursion, no Thread.sleep, no rendering-dependent gameplay and no long-lived unused state. Rate-limit particles/sounds under fast mining or repeated work.

======================================================================================
60. INVALID-USE AND NO-OP BEHAVIOR
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Invalid use must be cheap and predictable. If cooldown is active, target/context is invalid, protection denies action, tool is broken, crop is mature, ore search finds nothing, or no eligible blocks exist, do not consume durability or play full successful VFX. Return/fall back using the correct Minecraft action result.

======================================================================================
61. EDGE CASES AND FAILURE RECOVERY
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Handle edge cases explicitly for this ability, including: preserve Silk Touch/Fortune/loot/XP where applicable, falling-block updates, chunk safety and protection hooks; do not force-load chunks. Also test chunk boundaries, world border, target changes between validation and execution, dimension change, disconnect, tool break, high latency, offhand, creative mode, and concurrent players. Cleanup must be idempotent and safe.

======================================================================================
62. REQUIRED RESOURCE FILES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Expected resources normally include assets/<modid>/geo/fire_devil_shovel.geo.json, animations/fire_devil_shovel.animation.json, textures/item/fire_devil_shovel.png, item model JSON if renderer requires it, lang entries, optional particle textures and sounds.json entries. Follow the project's actual namespace/path conventions exactly.

======================================================================================
63. LOCALIZATION AND TOOLTIP
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Add en_us and any existing project languages. Tooltip should state the unique mechanic in player-facing terms, e.g. 'INFERNAL EXCAVATION' and its main range/area, without implementation jargon. Keep names consistent across registry ID, translation key, advancements/recipes if any.

======================================================================================
64. CODE ARCHITECTURE AND CLASS RESPONSIBILITIES
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Prefer a focused FireDevilShovelItem class plus existing/shared model and renderer patterns. Put complex bounded area/target algorithms into small helpers only when that improves clarity. Reuse shared FireDevilToolMaterial, VFX, sound and animation utilities instead of copy-pasting five divergent systems.

======================================================================================
65. JSON/RESOURCE IDENTIFIER VALIDATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Validate every identifier: Java animation trigger strings, geo filename, texture path, namespace, sound ID, particle ID, translation key and JSON schema. Run resource reload where possible. A one-character mismatch that yields missing texture or silent animation means the task is not done.

======================================================================================
66. MODEL GAPS, SEAMS AND Z-FIGHTING QA
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Inspect the final model for unintended holes and seams around thick rectangular outer frame, recessed inner spade face, tapered lower working lip, vertical hot fissure, upper socket/core, wrapped shaft, collars and pommel. Distinguish deliberate magma channels/recesses from accidental open geometry. Remove z-fighting from coplanar plates, close missing side faces, fix mirrored gaps, and verify there are no zero-size cubes or floating decorative components.

======================================================================================
67. GAMEPLAY TEST MATRIX
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Gameplay QA must cover ordinary behavior plus INFERNAL EXCAVATION. Test valid/invalid use, cooldown, durability, low-durability break, enchantments, multiplayer, protection/solid obstacles or block suitability as relevant, repeated use, and concurrency. Verify actual server results, not only pretty animation.

======================================================================================
68. VISUAL TEST MATRIX
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Visual QA: inspect front/back/left/right/top/bottom and 3/4 views, first-person at several FOVs, offhand, third-person movement/actions, GUI, dropped item, item frame, bright daylight and dark environments. Confirm emissive hierarchy, correct working orientation, no camera obstruction, no gaps/z-fighting and coherent animation.

======================================================================================
69. BUILD AND RUNCLIENT VALIDATION
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. Run the actual Gradle wrapper build and then runClient when available. Read compiler/resource/runtime logs, fix errors, reload resources, and repeat until stable. If dedicated-server run is available, verify no client-only renderer/model class causes classloading failure.

======================================================================================
70. FINAL DEFINITION OF DONE
======================================================================================
**Item-specific target:** a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel. The item is DONE only when it strongly matches the supplied concept (a broad rectangular infernal spade with a thick black forged perimeter, deeply recessed fractured center, vertical incandescent magma core, massive upper socket, long wrapped handle, forged collars and glowing cubic pommel); geometry is clean and connected; UV/texture/emissive layers are polished; first/third/GUI/ground transforms are correct; GeckoLib animations work; ordinary ShovelItem behavior remains intact; **INFERNAL EXCAVATION** behaves exactly as specified with server authority, safe cooldown/cost/networking/performance; no unintended world grief occurs; and build/runtime validation succeeds.

END OF PROMPT.
```

---


# Fire Devil Hoe — 70-POINT ULTRA-DETAILED PROMPT

![Fire Devil Hoe concept](concept_art/fire_devil_hoe.png)

```text
# FIRE DEVIL HOE — MASTER PRODUCTION TASK
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench
# Recommended registry id: fire_devil_hoe

You are a senior Minecraft Fabric 1.20.1 developer, GeckoLib technical specialist, Blockbench 3D modeler, Minecraft low-poly artist, pixel texture artist, animator, gameplay programmer, VFX/sound designer, networking engineer, optimization engineer and QA engineer.

This is not a concept-only task. Inspect the actual existing project first, then IMPLEMENT the item and verify it in-game. Use the exact installed Fabric/Yarn/GeckoLib APIs. Do not use Forge, NeoForge, incompatible version examples, imagined methods or pseudocode in place of compiling code.

Shared FIRE DEVIL visual language:
- fractured black volcanic steel / obsidian-like forged metal;
- incandescent orange-red magma fissures with tiny yellow-hot cores;
- square/diamond furnace cores trapped inside heavy forged frames;
- dark heat-blackened leather wrapping;
- stepped brutal architectural plates, bevels and collars;
- restrained sparks, embers and ash rather than permanent screen-filling fire.
The set must look forged by the same infernal civilization, not like five unrelated red recolors.

PRIMARY VISUAL TARGET: a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel.
MANDATORY UNIQUE ABILITY: ASHEN BLOOM — When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling.

======================================================================================
1. PROJECT AUDIT AND EXACT VERSION VERIFICATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Before touching code or assets, inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric Loader/API versions, GeckoLib dependency, Java version, package structure, ModItems, ToolMaterial classes, renderers, client initializer, existing Fire Devil tools, sound/particle registries, networking, and any helper utilities. Do not assume an API because an online example looks similar. If the project already contains a working animated HoeItem, treat that implementation as the technical reference while preserving this item's unique visual/gameplay identity. Record exact resource namespace and file conventions before creating anything.

======================================================================================
2. REFERENCE DECOMPOSITION AND VISUAL MEASUREMENT
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Study the supplied per-item concept and the full-set sheet. Decompose the object into measurable masses: square socket/core, forward segmented arm, downturned working lip, hot edge strip, long wrapped shaft, collars and pommel. Note which silhouette features define recognition, which details can be texture-only, which components need depth, where emissive cracks originate, and how the object is expected to connect structurally. Inspect the reference from an imagined front/side/3/4 view and infer hidden rear geometry conservatively rather than inventing unrelated machinery.

======================================================================================
3. SILHOUETTE LOCK BEFORE DETAIL WORK
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Create a flat-color silhouette blockout and judge it before any ornamentation. At normal gameplay distance the item must be recognizable solely from geometry. Do not use cracks, emissive colors or tiny details to hide incorrect proportions. If the silhouette is wrong, stop and correct it before proceeding.

======================================================================================
4. OVERALL PROPORTIONS AND MINECRAFT SCALE
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Establish a consistent Blockbench coordinate system and compare the item with player hand/body scale and the other Fire Devil tools. Preserve the relative visual weight from the reference. The item may be legendary and larger than vanilla, but must remain usable in first person and readable in inventory. Document the final model scale so later transforms do not compensate for arbitrary export scaling.

======================================================================================
5. PRIMARY BLOCKOUT WORKFLOW
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Build only the primary masses first: square socket/core, forward segmented arm, downturned working lip, hot edge strip, long wrapped shaft, collars and pommel. Keep the blockout low complexity and physically connected. Validate working direction and grip orientation now, before UVs and animation. Do not proceed to cracks, rivets, runes or particles until the blockout survives front/back/side/top/3/4 inspection.

======================================================================================
6. SECONDARY FORMS AND STRUCTURAL LAYERING
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Add secondary structural plates, sockets, collars, recesses, ribs and working-edge reinforcement in a hierarchy that makes physical sense. Every visible major plate should either connect to another component or be clearly mounted. Avoid floating decoration and accidental interior holes. Use repeated Fire Devil motifs consistently across the set without copying another tool's silhouette.

======================================================================================
7. SIDE PROFILE AND PHYSICAL THICKNESS
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Give every major working component real side depth. Separate rear structural thickness, middle body plate, recessed inner panel/channel, and thinner working edge where appropriate. The item must not look like a 2D concept image extruded by one pixel. Check side and 3/4 views for believable mass and ensure the hand/shaft connection is structurally thick enough.

======================================================================================
8. BEVELS, EDGES, TIPS AND WORKING SURFACES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Use deliberate low-poly chamfers instead of high-segment bevels. Working tips/edges should transition from thick structural body to narrower edge through a few readable planes. Corners, sockets and pommels may use stepped bevels. Never add dozens of tiny cubes for curvature that will be invisible in gameplay.

======================================================================================
9. MATERIAL HIERARCHY AND READABILITY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Keep four material families visually separable: dark volcanic metal, incandescent magma/emissive cracks, dark wrapped grip, and infernal cores. Use geometry depth plus value contrast—not color alone—to distinguish them. The black body should still be readable in darkness and the orange glow should remain an accent rather than flooding every surface.

======================================================================================
10. BLACK VOLCANIC METAL TEXTURING
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Paint volcanic metal using broad charcoal/blue-black planes, medium-gray chipped bevels, sparse forged pits and controlled scratches. Avoid uniform pure black and avoid noisy rock photographs. Working areas may show brighter abrasion. Recesses can approach near-black, but silhouette edges need enough value separation for Minecraft lighting.

======================================================================================
11. INCANDESCENT MAGMA CRACK DESIGN
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Design magma fractures as stress-driven networks that originate around the core, joints and working edge. Use a hot center hierarchy: tiny pale-yellow/white-orange pixels at peaks, orange core, red-orange falloff, dark red heat halo. Do not draw random equal-brightness scribbles everywhere; secondary cracks must remain subordinate to the principal energy path.

======================================================================================
12. INFERNAL CORE / GEM CONSTRUCTION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Model each infernal core as a physical socket with an inset faceted hot center and surrounding dark frame. The core should look trapped inside forged metal. Give the brightest region a small area so emission feels intense rather than flat. Reuse the same core language across the set while scaling shape/size to this item.

======================================================================================
13. HANDLE, GRIP AND WRAPPING CONSTRUCTION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Construct the grip as dark heat-blackened leather/hide or tightly wrapped material over a rigid shaft/tang. Use diagonal or crossed wrap bands, subtle brown-black value variation, and forged collars. Keep the hand-contact area visually calmer than the head/blade so the grip location remains obvious.

======================================================================================
14. HEAT WEAR, SOOT AND EDGE AGING
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Add restrained heat wear: dark red-brown discoloration near cores and working edges, small soot deposits in recesses, and bright worn metal on exposed bevels. Do not rust the set green/brown or cover everything in dirt. These are maintained infernal artifacts, not abandoned scrap.

======================================================================================
15. TEXTURE RESOLUTION AND TEXEL DENSITY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Prefer 256x256 texture for this high-detail GeckoLib item unless the existing set uses 128x128. Maintain consistent texel density across all five tools. Allocate more pixels to focal front faces, cores and working edges; allocate fewer to hidden undersides. Tiny details that disappear at inventory scale should be simplified.

======================================================================================
16. UV LAYOUT AND ISLAND PADDING
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Create clean UV islands with padding, logical orientation and minimal distortion. Separate front/back focal faces where unique fracture patterns matter. Mirror only genuinely symmetrical surfaces where duplicated wear is acceptable. Keep emissive orange islands away from unrelated dark islands to prevent filtering/bleeding.

======================================================================================
17. PIXEL-ART TEXTURE PAINTING RULES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Use crisp Minecraft-compatible pixel shading. Do not bake strong environmental highlights from the concept art into the texture. Build depth with edge highlights, plate-to-plate occlusion shadows, hot crack cores and controlled material variation. Avoid blurry photographic gradients and excessive antialiasing.

======================================================================================
18. EMISSIVE-LAYER IMPLEMENTATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Inspect the project for an existing GeckoLib emissive/render-layer solution. If supported, use emission only on core centers, selected magma crack centers and hot working strips. Outer metal, grip and most crack falloff remain normally lit. If no clean emissive system exists, use bright texture values and particles rather than installing a heavy shader dependency solely for this set.

======================================================================================
19. GEOMETRY BUDGET AND OPTIMIZATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Optimize deliberately: geometry for silhouette, thickness, major bevels, sockets, cores and major plates; textures for micro-cracks, scratches, tiny rivets and engraved seams. Remove hidden duplicate cubes, zero-size geometry and unseen internal faces. Normal idle rendering should add negligible cost compared with another GeckoLib item.

======================================================================================
20. GECKOLIB BONE HIERARCHY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Create a small meaningful bone tree: root -> item -> main working assembly/head/blade -> handle -> pommel -> optional FX bones. Sub-bones exist only when animation or organization benefits. Do not create one bone per decorative plate. Use names that are stable, snake_case or project-consistent, and easy to reference in animation JSON.

======================================================================================
21. BONE PIVOTS AND ROTATION ORIGINS
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Place pivots at physical joints: main head/blade pivot near the shaft/hilt connection, handle pivot along the grip axis, pommel at lower connector, cores at their centers, and working sub-parts at actual attachment points. Bad pivots create 'exploding' animation even with correct keyframes, so validate each pivot in Blockbench before export.

======================================================================================
22. ROOT ORIGIN AND HELD-ITEM REFERENCE POINT
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Place root/origin around the natural held-item reference rather than blindly at geometric center. The origin must support first person, third person, GUI and dropped transforms without extreme translations. Follow the same convention as already-working set items when possible to simplify shared renderer logic.

======================================================================================
23. FIRST-PERSON RIGHT-HAND TRANSFORM
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Tune first-person right hand only after the model orientation is correct. The hand must visibly contact the grip, the functional edge must face the correct working/attack direction, and the main head/blade should remain readable without covering the crosshair. Test normal and low/high FOV, idle and action animation.

======================================================================================
24. FIRST-PERSON LEFT/OFFHAND TRANSFORM
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Test offhand/left-hand rendering independently. Do not assume automatic mirroring preserves working direction. Correct mirrored yaw/roll or use display-context-specific transforms so the item does not suddenly face backwards, expose only its thin side, or intersect the camera.

======================================================================================
25. THIRD-PERSON TRANSFORM AND HAND CONTACT
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. In third person, align the player's hand with the actual grip and keep the working end logically forward during attacks/mining/tilling. Test standing, walking, sprinting, jumping, sneaking and action states. Small Minecraft-style clipping is acceptable; gross torso/head penetration or a floating grip is not.

======================================================================================
26. GUI INVENTORY TRANSFORM
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Create a dedicated GUI transform that shows the strongest 3/4 silhouette, the infernal core and emissive fractures. Fit the entire item into the slot without cropping major working geometry. Do not simply reuse first-person transforms.

======================================================================================
27. DROPPED-ITEM AND ITEM-FRAME TRANSFORM
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. For ground/item-frame display, preserve sensible scale and a stable attractive angle. The item should not become building-sized or vanish into a block. Verify item-frame depth so thick GeckoLib geometry does not clip almost entirely through the wall.

======================================================================================
28. IDLE ANIMATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Idle animation should be restrained and loop smoothly for roughly 2.5–4 seconds: a 1–2% core pulse, tiny heat breathing, and at most fractions of a degree of rigid secondary movement. Do not make a forged tool constantly wobble or emit a permanent flame fountain.

======================================================================================
29. EQUIP ANIMATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Equip animation should be short and responsive, around 0.25–0.45 seconds: raise from a slightly lowered pose, tiny heavy overshoot, brief core brightening, settle. Avoid full spins, anime flourishes or animation that delays actual gameplay control.

======================================================================================
30. PRIMARY ATTACK / WORK ANIMATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Design the primary action animation around this item's real role: ordinary hoe interactions upgraded so valid soil tilling processes an intrinsic 3x3 area on the clicked Y level with vanilla-equivalent validation; this normal tilling has no special-ability cooldown. Use anticipation -> fast working/attack motion -> clear impact/contact frame -> physical follow-through -> recovery. If vanilla player-hand motion already supplies the main swing, let GeckoLib add internal inertia and core response instead of doubling root rotation.

======================================================================================
31. SECONDARY INERTIA AND MECHANICAL MOTION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Secondary motion must communicate rigid mass: shaft/hand begins motion, heavy head/blade lags by a few degrees, catches up near impact, then slightly overshoots during recovery. Metal plates do not flex like rubber. Small core/socket counter-rotation can enrich close-up animation without looking mechanical.

======================================================================================
32. MAGMA/CORE PULSE ANIMATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Animate heat as a short energy flow rather than constant maximal glow. A lower core/pommel may brighten first, followed by the main head/core and working crack network. Peak emission aligns with impact or special release, then fades rapidly to idle. Keep ordinary idle dark enough that special activation feels meaningful.

======================================================================================
33. ANIMATION CONTROLLERS AND PRIORITIES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Define controller priority so mutually exclusive actions never fight over root bones. A safe conceptual order is special ability > normal attack/work > equip > idle, with a separate FX controller only if the installed GeckoLib version benefits. Use the exact triggerable-animation API present in the project, not copied syntax from another version.

======================================================================================
34. ANIMATION-EVENT SYNCHRONIZATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Separate animation-timed cosmetics from gameplay confirmation. Whoosh/equip/core pulses can be keyframe-driven. Successful damage, block breaks, crop growth or vein extraction must be triggered by server-authoritative gameplay logic. Damage/work must never depend on render FPS or whether a client skipped an animation frame.

======================================================================================
35. VANILLA GAMEPLAY BASE CLASS AND BEHAVIOR
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Implement the item using the project's real HoeItem (or established custom subclass) so it retains ordinary hoe interactions upgraded so valid soil tilling processes an intrinsic 3x3 area on the clicked Y level with vanilla-equivalent validation; this normal tilling has no special-ability cooldown. Do not replace vanilla tool behavior with a generic Item just to make GeckoLib easier. Preserve tags, interaction semantics, attack/mining attributes and vanilla action results appropriate to Minecraft 1.20.1.

======================================================================================
36. TOOL MATERIAL / COMBAT OR MINING BALANCE
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Reuse an existing FireDevilToolMaterial if present. If absent, derive values from the mod's progression and compare with Netherite and other endgame sets. Keep named constants for durability, mining speed, attack damage and enchantability. Do not use absurd values unless the mod's established progression explicitly requires them.

======================================================================================
37. DURABILITY BEHAVIOR
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Normal durability follows standard item semantics. For the unique ability, follow this item-specific rule: 3x3 tilling costs durability per successfully transformed soil block; Ashen Bloom uses a small fixed/per-successful-crop cost without charging for mature/invalid crops. Use ItemStack damage APIs compatible with Unbreaking/creative behavior where appropriate. Never perform the full gameplay effect and only afterwards discover the tool should have broken halfway through.

======================================================================================
38. ENCHANTMENTS AND VANILLA COMPATIBILITY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Preserve appropriate vanilla enchantments and loot/interaction semantics. Efficiency/Sharpness/Fortune/Silk Touch/Unbreaking/Mending compatibility depends on item type; do not disable them accidentally. Special abilities must explicitly define how enchantments interact instead of silently duplicating drops or multiplying damage unexpectedly.

======================================================================================
39. UNIQUE ABILITY CONCEPT
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. **ASHEN BLOOM** is the mandatory unique mechanic. When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling. This ability is part of the production definition, not an optional idea. Implement it only after ordinary item behavior is correct so the special system cannot hide broken base gameplay.

======================================================================================
40. ABILITY ACTIVATION INPUT AND VALIDATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Activation must be deterministic and context-aware. When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling. Validate the held item, hand/context, cooldown and server-side state before committing. Invalid use must not consume durability or start a fake successful animation. One user input should create one ability execution, not repeated triggers every use tick.

======================================================================================
41. ABILITY TARGETING / AFFECTED REGION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Targeting is strictly bounded: normal tilling: exact 3x3 same-Y candidate area; Ashen Bloom: exact 5x5 same crop-layer candidate area, valid growable planted crops only. Build the target set once per use with hard numerical limits. Never replace a bounded local calculation with a whole-world scan. Solid collision, block suitability or crop/ore validity must be respected according to this item's design.

======================================================================================
42. SERVER-AUTHORITATIVE ABILITY EXECUTION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. The server is authoritative for every gameplay consequence of ASHEN BLOOM: target selection, damage/block/crop changes, cooldown, durability and state transitions. Client-side code may predict harmless visual startup, but cannot decide outcomes. Keep MinecraftClient and renderer classes out of common/server class paths.

======================================================================================
43. ABILITY STATE MACHINE
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Use an explicit, finite state flow rather than scattered booleans. For this ability incorporate the special constraint: interaction priority is crop growth first when an actual growable crop is clicked, otherwise soil tilling; never place a global item cooldown gate before deciding the path if that would block normal tilling. Every active cast/operation must have a clear start, progress/resolve phase and cleanup. World unload, player disconnect or invalid target must not leave stale global state.

======================================================================================
44. ABILITY GAMEPLAY RESOLUTION RULES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Gameplay resolution must follow the exact item-specific promise: When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling. Prevent accidental duplicate effects caused by overlapping samples, repeated ticks or client/server double execution. Preserve normal protection, loot, PvP and block-update semantics rather than bypassing them with raw uncontrolled world mutation.

======================================================================================
45. ABILITY COOLDOWN SEMANTICS
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Cooldown semantics: 10 seconds for Ashen Bloom only; CRITICAL: even while that cooldown is active, clicking valid soil must still perform normal 3x3 tilling. Use a named constant and the project's cooldown system. Cooldown should begin only at the correct committed stage. Never let the ability cooldown unintentionally disable unrelated ordinary item actions unless explicitly required by this design.

======================================================================================
46. ABILITY DURABILITY / RESOURCE COST
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Ability cost: 3x3 tilling costs durability per successfully transformed soil block; Ashen Bloom uses a small fixed/per-successful-crop cost without charging for mature/invalid crops. Apply cost exactly once at the intended successful stage, or per successfully processed block only where this item's definition calls for it. Invalid/no-op actions cost nothing. Stop safely if the item breaks during multi-block work.

======================================================================================
47. ABILITY VFX TIMELINE
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Create a tightly choreographed VFX timeline: core glows -> warm ember/ash ring spreads across the 5x5 crop patch -> valid plants get tiny upward amber-gold motes representing fertile volcanic ash -> no flames or crop burning. Favor a small number of layered purposeful effects—hot core, emissive path, sparks, ash, contact flash—over hundreds of identical particles. First-person effects must preserve visibility; world-visible effects must make the action understandable to observers.

======================================================================================
48. ABILITY SOUND DESIGN
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Sound identity: soft furnace pulse, low ash/soil sweep and restrained growth chime, explicitly not a combat explosion. Use layering and pitch variation intentionally, but aggregate repeated multi-target/multi-block events so the action does not produce dozens of maximum-volume identical sounds. Keep ordinary tool sounds recognizable beneath the infernal accent.

======================================================================================
49. ABILITY NETWORKING AND SYNCHRONIZATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Use efficient synchronization. Prefer normal world/entity synchronization or one compact ability event containing origin/direction/seed/positions over one custom packet per particle. The server remains authoritative even if clients reconstruct deterministic visuals from a seed. Avoid trusting client-reported hit lists or block lists.

======================================================================================
50. ABILITY MULTIPLAYER BEHAVIOR
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Test simultaneous multiplayer use. Every player/cast/area operation needs independent state; never store 'current target/current cast' in one global mutable variable. Nearby observers should see important world effects, while camera-only micro-effects may remain local. Handle latency without changing gameplay damage/work result.

======================================================================================
51. NORMAL-USE VFX
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Ordinary attacks/mining/tilling should use restrained Fire Devil feedback: brief core pulse, a few orange forge sparks or a short translucent dark-orange trail, while preserving vanilla material/block particles. Do not make every basic action visually equal to the special ability.

======================================================================================
52. SUCCESSFUL HIT / SUCCESSFUL WORK VFX
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Successful confirmed work/hits should add localized feedback at the actual target/block: compact orange-white contact flash, sparse metal/ember sparks, brief core response and normal block debris where relevant. Misses/no-op interactions must not spawn a fake success burst.

======================================================================================
53. CRITICAL / HIGH-VALUE RESULT VFX
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Critical hits or especially valuable successful results may receive a slightly brighter star/core pulse and a modest particle increase, but never auto-trigger the full unique ability unless explicitly designed. Keep special activation visually distinct and readable.

======================================================================================
54. PARTICLE BUDGET AND LIFETIME
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Set explicit budgets. Normal action: roughly single-digit to low-teens custom particles. Special ability: bounded tens, scaled to fixed target cap. Most particles should die within 0.1–0.6 seconds. Never spawn particles every tick merely because the item is held or because a long status/cooldown is active.

======================================================================================
55. ORDINARY-USE SOUND LAYERING
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Ordinary sound should preserve the physical role—blade whoosh, pick impact, soil scrape, etc.—then add a restrained forged-metal/furnace overtone. Avoid stacking five loud sounds on every mundane action. Special ability receives the more elaborate audio signature.

======================================================================================
56. ENVIRONMENTAL SAFETY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. The infernal aesthetic does NOT automatically authorize griefing. By default, never create fire blocks, lava, TNT-like explosions or permanent burning terrain unless the specific ability explicitly requires it—which these designs do not. Cosmetic embers and entity fire status are separate from world fire placement.

======================================================================================
57. WORLD/BLOCK INTERACTION SAFETY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. World/block changes are limited to this item's legitimate rules: When RMB/context-use targets an already planted immature crop, Ashen Bloom instantly matures valid crops in a bounded 5x5 horizontal crop area centered on the clicked plant. It does not harvest, replant, place seeds, hydrate farmland, or create item drops. Already mature crops are skipped. The growth cooldown applies ONLY to Ashen Bloom and must never stop ordinary 3x3 tilling. Respect block hardness/suitability, crops/farmland safety, loot contexts, world border, chunk availability and protection hooks where the project exposes them. Do not use force-loading or raw setBlockState loops to bypass gameplay systems.

======================================================================================
58. ENTITY FILTERING AND FRIENDLY-FIRE BEHAVIOR
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Respect teams, PvP/friendly-fire, creative/spectator rules, invulnerable entities and caster exclusion for combat abilities. Farming/mining abilities should not damage entities unless explicitly stated. Deduplicate targets per cast so overlapping effect geometry cannot multiply unintended damage.

======================================================================================
59. PERFORMANCE SAFEGUARDS
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Hard-code safe upper bounds for every search, target list, area size and duration. No whole-world scans, no unbounded recursion, no Thread.sleep, no rendering-dependent gameplay and no long-lived unused state. Rate-limit particles/sounds under fast mining or repeated work.

======================================================================================
60. INVALID-USE AND NO-OP BEHAVIOR
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Invalid use must be cheap and predictable. If cooldown is active, target/context is invalid, protection denies action, tool is broken, crop is mature, ore search finds nothing, or no eligible blocks exist, do not consume durability or play full successful VFX. Return/fall back using the correct Minecraft action result.

======================================================================================
61. EDGE CASES AND FAILURE RECOVERY
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Handle edge cases explicitly for this ability, including: interaction priority is crop growth first when an actual growable crop is clicked, otherwise soil tilling; never place a global item cooldown gate before deciding the path if that would block normal tilling. Also test chunk boundaries, world border, target changes between validation and execution, dimension change, disconnect, tool break, high latency, offhand, creative mode, and concurrent players. Cleanup must be idempotent and safe.

======================================================================================
62. REQUIRED RESOURCE FILES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Expected resources normally include assets/<modid>/geo/fire_devil_hoe.geo.json, animations/fire_devil_hoe.animation.json, textures/item/fire_devil_hoe.png, item model JSON if renderer requires it, lang entries, optional particle textures and sounds.json entries. Follow the project's actual namespace/path conventions exactly.

======================================================================================
63. LOCALIZATION AND TOOLTIP
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Add en_us and any existing project languages. Tooltip should state the unique mechanic in player-facing terms, e.g. 'ASHEN BLOOM' and its main range/area, without implementation jargon. Keep names consistent across registry ID, translation key, advancements/recipes if any.

======================================================================================
64. CODE ARCHITECTURE AND CLASS RESPONSIBILITIES
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Prefer a focused FireDevilHoeItem class plus existing/shared model and renderer patterns. Put complex bounded area/target algorithms into small helpers only when that improves clarity. Reuse shared FireDevilToolMaterial, VFX, sound and animation utilities instead of copy-pasting five divergent systems.

======================================================================================
65. JSON/RESOURCE IDENTIFIER VALIDATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Validate every identifier: Java animation trigger strings, geo filename, texture path, namespace, sound ID, particle ID, translation key and JSON schema. Run resource reload where possible. A one-character mismatch that yields missing texture or silent animation means the task is not done.

======================================================================================
66. MODEL GAPS, SEAMS AND Z-FIGHTING QA
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Inspect the final model for unintended holes and seams around square socket/core, forward segmented arm, downturned working lip, hot edge strip, long wrapped shaft, collars and pommel. Distinguish deliberate magma channels/recesses from accidental open geometry. Remove z-fighting from coplanar plates, close missing side faces, fix mirrored gaps, and verify there are no zero-size cubes or floating decorative components.

======================================================================================
67. GAMEPLAY TEST MATRIX
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Gameplay QA must cover ordinary behavior plus ASHEN BLOOM. Test valid/invalid use, cooldown, durability, low-durability break, enchantments, multiplayer, protection/solid obstacles or block suitability as relevant, repeated use, and concurrency. Verify actual server results, not only pretty animation.

======================================================================================
68. VISUAL TEST MATRIX
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Visual QA: inspect front/back/left/right/top/bottom and 3/4 views, first-person at several FOVs, offhand, third-person movement/actions, GUI, dropped item, item frame, bright daylight and dark environments. Confirm emissive hierarchy, correct working orientation, no camera obstruction, no gaps/z-fighting and coherent animation.

======================================================================================
69. BUILD AND RUNCLIENT VALIDATION
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. Run the actual Gradle wrapper build and then runClient when available. Read compiler/resource/runtime logs, fix errors, reload resources, and repeat until stable. If dedicated-server run is available, verify no client-only renderer/model class causes classloading failure.

======================================================================================
70. FINAL DEFINITION OF DONE
======================================================================================
**Item-specific target:** a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel. The item is DONE only when it strongly matches the supplied concept (a compact hooked infernal hoe with segmented black forged metal, square furnace socket, orange-hot working edge bending downward, long dark wrapped handle, metal collars and glowing cubic pommel); geometry is clean and connected; UV/texture/emissive layers are polished; first/third/GUI/ground transforms are correct; GeckoLib animations work; ordinary HoeItem behavior remains intact; **ASHEN BLOOM** behaves exactly as specified with server authority, safe cooldown/cost/networking/performance; no unintended world grief occurs; and build/runtime validation succeeds.

END OF PROMPT.
```

---
