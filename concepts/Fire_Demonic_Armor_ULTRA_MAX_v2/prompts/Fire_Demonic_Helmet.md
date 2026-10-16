# Fire Demonic Helmet — ULTRA MAXIMUM DETAIL 100-POINT IMPLEMENTATION PROMPT

![Fire Demonic Helmet concept](../concept_art/fire_demonic_helmet.png)

```text
# ITEM: Fire Demonic Helmet
# Likely registry id to FIND first: fire_demonic_helmet
# Minecraft Fabric 1.20.1 + GeckoLib + Blockbench

You are simultaneously acting as:
- senior Minecraft Fabric 1.20.1 mod developer;
- GeckoLib armor/rendering specialist;
- Blockbench character-armor modeler;
- Minecraft low-poly armor concept interpreter;
- pixel-art texture artist;
- technical animator;
- client rendering engineer;
- optimization engineer;
- QA engineer.

THIS IS A PRODUCTION IMPLEMENTATION TASK.

The Fire Demonic armor items are expected to ALREADY EXIST in the mod project or already have intended registry slots. Your first responsibility is to FIND the real existing armor entries/files and modify THOSE exact items in-place.

HARD CONSTRAINTS:
- do not create duplicate items;
- do not create v2 registry IDs;
- do not create parallel placeholder armor sets;
- do not rewrite unrelated systems;
- preserve existing armor stats, ArmorMaterial, slot logic, recipes, tags, set-bonus/effect logic and progression unless a tiny visual integration fix is absolutely required.

Technical target:
- Minecraft Fabric 1.20.1;
- exact installed Yarn mappings;
- exact installed GeckoLib version and armor renderer architecture.

Before implementation, inspect the real dependencies and existing code. Never use Forge / NeoForge APIs, 1.21 examples, or imaginary GeckoLib methods.

FIRE DEMONIC / INFERNAL ARMOR VISUAL BIBLE

The armor must inherit the same civilization and forge language as the Fire Devil toolset:
- primary body material: forged black volcanic steel / obsidian-dark infernal metal;
- secondary body plates: deep burnt crimson-red armor slabs layered over the black core shell;
- emissive accents: orange-red magma fissures with tiny yellow-hot centers only at the brightest stress points;
- structural logic: stepped angular plate architecture, heavy bevels, reinforced borders, sockets, clamps, layered lamellae;
- energy language: contained infernal furnace energy running through seams, reactors, vents and core sockets;
- underlayer: dark charred flexible material in joints and articulation zones;
- visual tone: demonic, heavy, brutal, elite, hell-forged, not sci-fi neon and not a generic bright-red recolor;
- ornament policy: spikes/horns/claws may exist, but only where silhouette benefits; avoid random clutter;
- VFX philosophy: restrained embers, ash, heat shimmer, occasional core pulses; do not cover the wearer in permanent flames;
- readability rule: even without emissive, the silhouette and plate hierarchy must clearly read under Minecraft lighting.

Set-wide power hierarchy:
- HELMET = furnace-crown / demonic predator head and identity anchor.
- CHESTPLATE = main infernal reactor and visual center of mass.
- LEGGINGS = articulated waist/thigh engine distributing heat downward.
- BOOTS = anchored infernal greaves / sabatons grounding the full silhouette.

============================================================================================
1. IMPLEMENTATION POINT 1
============================================================================================
Inspect build.gradle, gradle.properties, settings.gradle, fabric.mod.json, exact Yarn mappings, Fabric
Loader/API, GeckoLib version, Java version, armor registration classes, ArmorMaterial definitions, client
initializer, current armor renderer/provider classes, geo/animation/texture folders, lang entries, recipes and
tags. Determine the real project architecture before creating or modifying any Fire Demonic files.

============================================================================================
2. IMPLEMENTATION POINT 2
============================================================================================
Search the codebase for the real existing item using display name 'Fire Demonic Helmet', likely id
'fire_demonic_helmet', translation keys, recipes, tags and resource references. If naming differs, follow the
actual registry result. Modify THAT exact piece in-place.

============================================================================================
3. IMPLEMENTATION POINT 3
============================================================================================
Preserve the existing registry ID, slot assignment, ArmorMaterial, attribute modifiers, set bonuses, status
effects, repair items, recipes, tags, advancements and gameplay balance. This task is primarily a maximum-
quality visual/model/animation rework, not a rebalance.

============================================================================================
4. IMPLEMENTATION POINT 4
============================================================================================
Primary visual guidance comes from the supplied Fire Demonic concept art plus the following style bible:
FIRE
DEMONIC / INFERNAL ARMOR VISUAL BIBLE

The armor must inherit the same civilization and forge language as the
Fire Devil toolset:
- primary body material: forged black volcanic steel / obsidian-dark infernal metal;
-
secondary body plates: deep burnt crimson-red armor slabs layered over the black core shell;
- emissive accents:
orange-red magma fissures with tiny yellow-hot centers only at the brightest stress points;
- structural logic:
stepped angular plate architecture, heavy bevels, reinforced borders, sockets, clamps, layered lamellae;
-
energy language: contained infernal furnace energy running through seams, reactors, vents and core sockets;
-
underlayer: dark charred flexible material in joints and articulation zones;
- visual tone: demonic, heavy,
brutal, elite, hell-forged, not sci-fi neon and not a generic bright-red recolor;
- ornament policy:
spikes/horns/claws may exist, but only where silhouette benefits; avoid random clutter;
- VFX philosophy:
restrained embers, ash, heat shimmer, occasional core pulses; do not cover the wearer in permanent flames;
-
readability rule: even without emissive, the silhouette and plate hierarchy must clearly read under Minecraft
lighting.

Set-wide power hierarchy:
- HELMET = furnace-crown / demonic predator head and identity anchor.
-
CHESTPLATE = main infernal reactor and visual center of mass.
- LEGGINGS = articulated waist/thigh engine
distributing heat downward.
- BOOTS = anchored infernal greaves / sabatons grounding the full silhouette.

============================================================================================
5. IMPLEMENTATION POINT 5
============================================================================================
Define the whole set as one coherent infernal system before polishing any individual piece. The four items must
share the same black volcanic base metal, burnt-red secondary plates, crack grammar, bevel logic, underlayer
material, core framing and emissive intensity hierarchy.

============================================================================================
6. IMPLEMENTATION POINT 6
============================================================================================
Piece-specific silhouette target for Fire Demonic Helmet: a predatory infernal helmet with massive curved
volcanic horns, a heavy segmented crown, a deep visor slit glowing orange, a layered jaw/face mask, thick temple
and rear-skull armor, and strong forward menace without becoming a giant comedy helmet. Keep this silhouette
readable even in flat gray shading. The model should be recognizable before emissive texture work.

============================================================================================
7. IMPLEMENTATION POINT 7
============================================================================================
Build within a disciplined armor envelope around the player model. Required coverage: crown, forehead, temples,
cheeks, rear skull and face protection while still respecting head rotation and readability. Large accents are
allowed, but they must not become absurdly oversized relative to the character or permanently intersect the
body.

============================================================================================
8. IMPLEMENTATION POINT 8
============================================================================================
Use the actual Minecraft player proportions as the foundation. Model around the real head/torso/arm/leg boxes
and the GeckoLib armor bones used by the project. Do not build on an arbitrary mannequin scale and then hope
transforms fix it.

============================================================================================
9. IMPLEMENTATION POINT 9
============================================================================================
Start with a clean primary blockout using only the largest masses: segmented crown shell, heavy brow, central
vertical crest, full horn assemblies, visor cavity, jaw/face mask, cheek plates, rear skull plates, dark inner
liner, optional small rear fins. Equip the early blockout in-game immediately to verify scale and body alignment
before detailing.

============================================================================================
10. IMPLEMENTATION POINT 10
============================================================================================
After the blockout works, add secondary structural layering: raised borders, recessed plates, clamps, sockets,
lames, collars and protective shells. All large plates must appear mechanically mounted and not float.

============================================================================================
11. IMPLEMENTATION POINT 11
============================================================================================
Tertiary details such as small vents, rivets, fine seam steps, minor spikes and chip damage should be subtle and
come only after the articulation and major silhouette are proven. Most fine detail should remain in texture
rather than excessive cube clutter.

============================================================================================
12. IMPLEMENTATION POINT 12
============================================================================================
Primary black volcanic metal should use broad charcoal / obsidian-dark planes, selective cool dark-gray edge
highlights and forged wear. Avoid both flat pure black and noisy random stone textures.

============================================================================================
13. IMPLEMENTATION POINT 13
============================================================================================
Secondary burnt-red plate material should feel like heat-treated infernal armor slabs layered over the darker
frame. This red material must reinforce the silhouette and plate breakup rather than simply recoloring whole
regions.

============================================================================================
14. IMPLEMENTATION POINT 14
============================================================================================
Magma fissures should appear embedded inside the armor structure, usually along stress seams and core-fed
channels. Use a hierarchy of deep red halo -> orange body -> tiny yellow-hot inner pixels, and never scatter
equally bright cracks everywhere.

============================================================================================
15. IMPLEMENTATION POINT 15
============================================================================================
Infernal core design for Fire Demonic Helmet should prioritize these focal zones: glowing visor slit, horn
roots, central brow ridge, forehead crown plates, cheek structure and rear head protection. Each core or vent
must read as a framed heated chamber rather than a flat orange sticker.

============================================================================================
16. IMPLEMENTATION POINT 16
============================================================================================
At joints and articulation zones, use a dark flexible underlayer—charred leather, demon-forged cloth, scale-
liner or another shadowed flexible material. This prevents rigid plates from seeming to stretch unnaturally.

============================================================================================
17. IMPLEMENTATION POINT 17
============================================================================================
Apply restrained heat discoloration and soot near vents, cores and crack mouths. Let warmth tint adjacent plates
without turning the whole armor muddy. The set should feel hot and controlled, not dirty and messy.

============================================================================================
18. IMPLEMENTATION POINT 18
============================================================================================
Use edge wear sparingly: brighter nicks on exposed bevels, small abrasions on high-contact corners and polished
metal on the most exposed ridges. Avoid procedural speckle noise across all surfaces.

============================================================================================
19. IMPLEMENTATION POINT 19
============================================================================================
Lock a value hierarchy before relying on color: deepest underlayer, dark main shell, medium red plates, bright
fissures, brightest core centers. In grayscale the piece must still read clearly.

============================================================================================
20. IMPLEMENTATION POINT 20
============================================================================================
Prefer 256x256 per piece or a shared atlas size already used by the project. Do not arbitrarily break the
established renderer assumptions. Keep consistent texel density across all four pieces.

============================================================================================
21. IMPLEMENTATION POINT 21
============================================================================================
UV islands should follow plate logic. Prioritize visible front and 3/4 surfaces, keep enough padding around
emissive regions, and mirror symmetrical parts only where duplicate crack patterns will not look obviously fake.

============================================================================================
22. IMPLEMENTATION POINT 22
============================================================================================
Texture painting must remain crisp and Minecraft-friendly. Use deliberate plate separations, restrained
gradients, readable emissive channels and clear silhouette reinforcement. Avoid photorealistic rendering and
overblurred shading.

============================================================================================
23. IMPLEMENTATION POINT 23
============================================================================================
Inspect whether the current GeckoLib armor renderer already supports emissive layers. If yes, use emissive only
for core interiors, major crack centers and critical heat slits. If not, preserve the design with bright texture
values rather than inventing a heavy new shader dependency.

============================================================================================
24. IMPLEMENTATION POINT 24
============================================================================================
Keep geometry efficient. Use geometry for silhouette, horns, pauldron bulk, knee/toe shapes, core sockets and
major bevels. Use texture for tiny cracks, micro-seams and minor wear. Multiple armored players must remain
affordable to render.

============================================================================================
25. IMPLEMENTATION POINT 25
============================================================================================
Remove hidden internal faces, duplicate cubes, abandoned blockout pieces, zero-size cubes and coplanar plate
stacks that will z-fight. Production assets need a clean hierarchy and clean geometry.

============================================================================================
26. IMPLEMENTATION POINT 26
============================================================================================
Inspect the project's exact GeckoLib armor pipeline. Determine whether it uses one full-set geo with bone
visibility, separate geo files per piece, a shared renderer provider, or another approach. Follow the
established working method.

============================================================================================
27. IMPLEMENTATION POINT 27
============================================================================================
Integrate Fire Demonic Helmet through the real armor renderer/provider path already used by the mod. If a shared
full-set geo exists, modify the correct bones and slot visibility. If the project uses per-piece geo files,
update only the correct piece plus shared support files.

============================================================================================
28. IMPLEMENTATION POINT 28
============================================================================================
Create a clean bone hierarchy appropriate to Fire Demonic Helmet. Keep bones meaningful and limited to actual
articulated or organizational regions. Suggested structure should reflect: segmented crown shell, heavy brow,
central vertical crest, full horn assemblies, visor cavity, jaw/face mask, cheek plates, rear skull plates, dark
inner liner, optional small rear fins.

============================================================================================
29. IMPLEMENTATION POINT 29
============================================================================================
Use stable, descriptive bone names that match project style. Avoid default names like Cube1/Group17 in the
shipping asset. Good names make animation and maintenance far easier.

============================================================================================
30. IMPLEMENTATION POINT 30
============================================================================================
Set pivots at real articulation centers: head at skull rotation center; torso at torso origin; shoulders at
shoulder roots; left/right legs at their own pivots; feet aligned to lower leg rotation. Bad pivots are more
harmful than imperfect textures.

============================================================================================
31. IMPLEMENTATION POINT 31
============================================================================================
Attach each geometry region to the correct body bone so vanilla animation already works with zero custom
animation active. Do not parent both legs to one bone, and do not attach independent shoulder pieces to
unrelated bones.

============================================================================================
32. IMPLEMENTATION POINT 32
============================================================================================
Vanilla animation inheritance is the base requirement. Head turning, arm swings, walking, sneaking and jumping
must work correctly even before any custom secondary animation is layered in.

============================================================================================
33. IMPLEMENTATION POINT 33
============================================================================================
Custom secondary animation should be minimal and rigid. For Fire Demonic Helmet: rigid head following with only
subtle emissive pulse and possibly tiny heat-settle in horn/visor components. The armor must never behave like
cloth or jelly.

============================================================================================
34. IMPLEMENTATION POINT 34
============================================================================================
Idle animation should loop smoothly over roughly 2.5–4.5 seconds. Use subtle reactor/visor/vent pulse or
microscopic plate settle. No constant dramatic motion.

============================================================================================
35. IMPLEMENTATION POINT 35
============================================================================================
Walking must preserve precise left-right sync. Plates may have tiny damped lag, but never enough to detach
visibly from the body or clip catastrophically every step.

============================================================================================
36. IMPLEMENTATION POINT 36
============================================================================================
Sprint tests are mandatory because large limb arcs expose clipping. Verify shoulders, thigh plates, knees, toes
and rear structures under faster motion.

============================================================================================
37. IMPLEMENTATION POINT 37
============================================================================================
Sneaking compresses the body. Make sure collars, abdomen plates, waist/faulds and knee geometry survive crouch
without exploding or exposing huge empty gaps.

============================================================================================
38. IMPLEMENTATION POINT 38
============================================================================================
Jumping and falling stretch poses and show underside geometry. Ensure no plate flips inward, floats away or
clips through the torso during landing and airborne motion.

============================================================================================
39. IMPLEMENTATION POINT 39
============================================================================================
Swimming and crawling rotate the entire body horizontally. Test all protrusions, horns, shoulder shells and toe
structures against these orientations so they continue to follow the body correctly.

============================================================================================
40. IMPLEMENTATION POINT 40
============================================================================================
Riding poses bend hips and knees significantly. Test horses, boats and similar contexts where possible. Tassets,
knee plates and boots must remain believable.

============================================================================================
41. IMPLEMENTATION POINT 41
============================================================================================
If the project allows Elytra/back-slot interactions with the chest region, ensure rear armor structures do not
totally break that presentation. Keep compatibility reasonable without rewriting Elytra mechanics.

============================================================================================
42. IMPLEMENTATION POINT 42
============================================================================================
First-person rendering for Fire Demonic Helmet must respect the camera. Helmet internals should not render into
the player's face, and chest/shoulder geometry should not fill the screen. Use the renderer's established
culling/first-person behavior.

============================================================================================
43. IMPLEMENTATION POINT 43
============================================================================================
Third-person front view is a core approval angle. Confirm symmetry, core placement, posture, silhouette width
and general menace. The armor should look elite and heavy without making the player absurdly disproportionate.

============================================================================================
44. IMPLEMENTATION POINT 44
============================================================================================
Third-person rear view needs intentional design: layered back plates, rear vents, calf or heel reinforcement and
complete silhouettes. The backside must never feel forgotten.

============================================================================================
45. IMPLEMENTATION POINT 45
============================================================================================
Side and 3/4 views reveal thickness. Confirm plate depth, horn/pauldron volume, thigh/boot structure and the
presence of actual side walls and back faces instead of hollow shells.

============================================================================================
46. IMPLEMENTATION POINT 46
============================================================================================
Create or update the armor-piece inventory icon or item presentation so the item stack is recognizable at slot
size. If the project uses full 3D item renders, choose a flattering display transform.

============================================================================================
47. IMPLEMENTATION POINT 47
============================================================================================
When held as an item stack, the armor piece must appear readable and reasonably scaled. Do not let the item
model display as a gigantic full-character chunk in first person.

============================================================================================
48. IMPLEMENTATION POINT 48
============================================================================================
Dropped item representation should have sensible scale and angle. The armor piece must not collapse into a tiny
black block or clip halfway underground.

============================================================================================
49. IMPLEMENTATION POINT 49
============================================================================================
In an item frame, the piece should stay centered and readable. Thick geometry should not disappear into the
wall, and horns/spikes should still present attractively.

============================================================================================
50. IMPLEMENTATION POINT 50
============================================================================================
Equip transition may use a brief cosmetic pulse if the project's armor renderer already supports such an effect,
but equipping must remain immediate and functional. Do not introduce long transform sequences.

============================================================================================
51. IMPLEMENTATION POINT 51
============================================================================================
Unequipping must cleanly stop any cosmetic pulse or particle state. No lingering emitters or stuck emissive
behavior after the item is removed.

============================================================================================
52. IMPLEMENTATION POINT 52
============================================================================================
Optional damage-response cosmetics may include a brief reactor flash or tiny spark burst when the wearer takes
damage, but these effects must not change gameplay logic or spam every tick. If no clean hook exists, skip it.

============================================================================================
53. IMPLEMENTATION POINT 53
============================================================================================
Coordinate core pulse timing across the set. The chestplate reactor is the visual leader; helmet, leggings and
boots may echo that pulse at lower intensity. Each piece must also still look correct when worn alone.

============================================================================================
54. IMPLEMENTATION POINT 54
============================================================================================
Heat breathing should be a subtle change in emissive intensity or tiny vent flicker, not a scale pulse of the
whole model. Keep it atmospheric and non-distracting.

============================================================================================
55. IMPLEMENTATION POINT 55
============================================================================================
Ember particles must be sparse. A fully geared player should not permanently shed a storm of particles. Prefer
tiny occasional embers near key vents/cores or only event-based effects.

============================================================================================
56. IMPLEMENTATION POINT 56
============================================================================================
Cosmetic sound hooks, if the project supports them, should be restrained: a soft furnace tick, light metal clink
on equip, or a faint heat hiss. Never attach loud looping fire sounds to worn armor.

============================================================================================
57. IMPLEMENTATION POINT 57
============================================================================================
Test enchantment glint compatibility. The glint must not completely cover emissive cracks or disappear because
of the custom renderer. Use the established renderer path for glint.

============================================================================================
58. IMPLEMENTATION POINT 58
============================================================================================
Armor trims: inspect whether the project's custom armor path already supports vanilla trims. Preserve
compatibility if it already exists. If trims are intentionally unsupported, do not engineer a fragile new system
just for this set.

============================================================================================
59. IMPLEMENTATION POINT 59
============================================================================================
Dyeing compatibility should remain whatever the existing item already does. Fire Demonic armor should generally
keep its fixed infernal identity unless the project already allows dyeing.

============================================================================================
60. IMPLEMENTATION POINT 60
============================================================================================
Durability visualization, if any exists, should stay subtle. Do not create excessive damage variants that
obscure the core design. Small extra chips or dimmer glow are enough if the project already supports visual
wear.

============================================================================================
61. IMPLEMENTATION POINT 61
============================================================================================
Continuity with adjacent pieces is mandatory. The helmet must flow into the chest collar, chest into waist,
leggings into boots. Shared bevel widths, plate density, crack thickness and core framing should prove that the
pieces belong together.

============================================================================================
62. IMPLEMENTATION POINT 62
============================================================================================
Inspect seams between adjacent pieces when worn together. Prevent accidental exposed skin strips at the neck,
waist, thighs or ankles unless intentionally framed by dark underlayer.

============================================================================================
63. IMPLEMENTATION POINT 63
============================================================================================
Allow slight overlap between pieces where useful, but avoid coplanar intersections. Chest abdomen may overlap
the leggings waist; leggings may overlap boot collars; these overlaps need depth separation.

============================================================================================
64. IMPLEMENTATION POINT 64
============================================================================================
Specific clipping-prevention priority for Fire Demonic Helmet: head rotation must remain exact and the horns
must not clip excessively into torso/shoulders during ordinary motion. Test exaggerated poses and solve by
proportion/offset adjustment rather than giant global scale hacks.

============================================================================================
65. IMPLEMENTATION POINT 65
============================================================================================
Decide skin visibility intentionally. If a region is meant to be fully armored, cover it. If the design
deliberately leaves some face or joint area visible, frame it cleanly. Random exposed skin due to gaps is a bug.

============================================================================================
66. IMPLEMENTATION POINT 66
============================================================================================
Any plate that reveals its underside from common angles must have proper inner faces or side walls. Do not rely
on unseen backface culling to hide missing geometry.

============================================================================================
67. IMPLEMENTATION POINT 67
============================================================================================
Perform an explicit gap-prevention pass. Inspect the piece alone and with the full set from all major angles and
extreme poses. Close accidental holes while preserving deliberate vents and recesses.

============================================================================================
68. IMPLEMENTATION POINT 68
============================================================================================
Perform a z-fighting pass. Coplanar plate shells, emissive inserts and overlapping borders are common armor
problems. Offset surfaces meaningfully or consolidate them.

============================================================================================
69. IMPLEMENTATION POINT 69
============================================================================================
Check texture bleeding at mipmapped distance. Orange emissive islands need padding so hot pixels do not leak
onto black metal edges. Fix the UVs rather than hoping filtering hides it.

============================================================================================
70. IMPLEMENTATION POINT 70
============================================================================================
In low light and caves, the armor must not become a pure black blob. Use enough mid-dark edge definition and red
plate separation that the structure remains visible even before the emissive accents draw the eye.

============================================================================================
71. IMPLEMENTATION POINT 71
============================================================================================
In daylight, the emissive accents should still feel hot while the black and red plates remain distinct against
bright terrain and sky. Avoid washed-out oranges or unreadable dark plate stacks.

============================================================================================
72. IMPLEMENTATION POINT 72
============================================================================================
In Nether/lava environments, the armor must still stand out against orange backgrounds. Use value contrast, red-
dark halos and bright core centers so it does not vanish into the environment.

============================================================================================
73. IMPLEMENTATION POINT 73
============================================================================================
If emissive rendering is unavailable or breaks, the base texture must still look complete and thematically
correct using ordinary bright values. The design must not depend entirely on shaders.

============================================================================================
74. IMPLEMENTATION POINT 74
============================================================================================
Keep performance disciplined. Avoid over-boned rigs, giant nested groups, per-tick allocations, uncontrolled
particles and renderer duplication. Several players wearing the set must remain practical.

============================================================================================
75. IMPLEMENTATION POINT 75
============================================================================================
Ensure dedicated-server safety: common armor/item classes must not import or initialize client-only rendering
types. Keep all renderer/provider registration on the client side exactly as the project expects.

============================================================================================
76. IMPLEMENTATION POINT 76
============================================================================================
Ensure client-only classes are isolated. Use the proper Fabric + GeckoLib armor hooks for the exact installed
version, not Forge-specific item extension interfaces.

============================================================================================
77. IMPLEMENTATION POINT 77
============================================================================================
Use the correct existing resource paths for Fire Demonic Helmet. Update only the files genuinely needed: geo,
animations, textures, item model JSON, renderer/provider hooks, lang entries and any existing auxiliary assets.

============================================================================================
78. IMPLEMENTATION POINT 78
============================================================================================
Validate every animation name, loop mode and bone reference. If Java triggers an animation, that animation must
exist exactly in the JSON and target bones that really exist.

============================================================================================
79. IMPLEMENTATION POINT 79
============================================================================================
Validate geo/model JSON, filenames, namespaces, texture paths and casing. Missing textures, invisible geo and
broken resource locations are not acceptable deliverables.

============================================================================================
80. IMPLEMENTATION POINT 80
============================================================================================
Preserve the display name for Fire Demonic Helmet in localization. Add or update only the exact translation key
already used by the project. Do not create competing duplicate lang keys.

============================================================================================
81. IMPLEMENTATION POINT 81
============================================================================================
Tooltip policy: preserve existing functional text and stats. Only add concise flavor text if the project's item
style already uses flavor lines. Do not invent new bonuses or misdescribe mechanics.

============================================================================================
82. IMPLEMENTATION POINT 82
============================================================================================
Keep code architecture tidy. Reuse a shared Fire Demonic armor renderer/model if the project favors that
approach. Create per-piece specific logic only where slot geometry or animation actually requires it.

============================================================================================
83. IMPLEMENTATION POINT 83
============================================================================================
HARD RULE: do not create a duplicate registry entry such as 'fire_demonic_helmet_v2' or any alternate test item.
Modify the existing Fire Demonic Helmet only.

============================================================================================
84. IMPLEMENTATION POINT 84
============================================================================================
HARD RULE: do not register multiple competing renderers or providers for the same piece. Replace or update the
existing path cleanly so only one render path remains active.

============================================================================================
85. IMPLEMENTATION POINT 85
============================================================================================
HARD RULE: do not rewrite unrelated combat, effect, worldgen, tool or general entity systems. Restrict code
edits to Fire Demonic armor visuals and the minimum integration glue required.

============================================================================================
86. IMPLEMENTATION POINT 86
============================================================================================
Test on the standard Steve model in idle, walk, sprint, sneak, jump and combat-adjacent poses. Compare
proportions and coverage with screenshots from front/back/side.

============================================================================================
87. IMPLEMENTATION POINT 87
============================================================================================
Test on Alex/slim where supported. Shoulder, upper-arm and torso-adjacent geometry may need validation to ensure
it does not visibly float or clip more severely on the slim body.

============================================================================================
88. IMPLEMENTATION POINT 88
============================================================================================
Test with several different player skins—light, dark, highly patterned—to expose accidental alpha issues, skin
gaps and holes that a single skin might hide.

============================================================================================
89. IMPLEMENTATION POINT 89
============================================================================================
Test while holding long swords, axes, bows/crossbows, shields and tools if available. Shoulder plates, horns and
chest geometry must not make common combat/utility poses unusable.

============================================================================================
90. IMPLEMENTATION POINT 90
============================================================================================
Equip all four Fire Demonic pieces simultaneously and judge the full silhouette, shared intensity,
neck/waist/ankle seams, overlaps and synchronized heat language. The complete set is the primary hero
composition.

============================================================================================
91. IMPLEMENTATION POINT 91
============================================================================================
Test Fire Demonic Helmet worn by itself. It must still look intentional and complete, and it must not depend on
neighboring pieces to hide glaring gaps or exposed unfinished regions.

============================================================================================
92. IMPLEMENTATION POINT 92
============================================================================================
Test enchanted and unenchanted versions. Glint layering must remain stable and should not produce duplicate
passes or flicker.

============================================================================================
93. IMPLEMENTATION POINT 93
============================================================================================
Test low durability or any HUD/tooltip state associated with wear to ensure the custom visuals do not vanish or
glitch. Do not alter gameplay while testing.

============================================================================================
94. IMPLEMENTATION POINT 94
============================================================================================
Observe another player wearing the armor in multiplayer or simulated observer contexts. Check that geometry
remains attached and that cosmetic effects do not duplicate per viewer.

============================================================================================
95. IMPLEMENTATION POINT 95
============================================================================================
Use resource reload (for example F3+T where applicable) and ensure textures, geo and animation reload correctly
without stale caches or invisible armor.

============================================================================================
96. IMPLEMENTATION POINT 96
============================================================================================
Exit and re-enter the world / relog. Confirm that the armor renderer/provider reinitializes properly and the
piece remains visible and animated after reload.

============================================================================================
97. IMPLEMENTATION POINT 97
============================================================================================
If a dedicated-server run is available, confirm that the server starts with the armor registered and no client-
only classloading crash occurs.

============================================================================================
98. IMPLEMENTATION POINT 98
============================================================================================
Run the real Gradle build and fix compilation issues, mappings mismatches, bad imports and resource processing
errors. A prompt is not complete until the implementation compiles.

============================================================================================
99. IMPLEMENTATION POINT 99
============================================================================================
Run runClient and verify the piece in an actual test world. Fix real in-game problems revealed by lighting,
camera, animation and movement that do not show up in Blockbench preview.

============================================================================================
100. IMPLEMENTATION POINT 100
============================================================================================
DEFINITION OF DONE for Fire Demonic Helmet: the exact existing armor piece has been found and updated in-place;
the result faithfully matches the Fire Demonic concept art and style bible; the silhouette is 'a predatory
infernal helmet with massive curved volcanic horns, a heavy segmented crown, a deep visor slit glowing orange, a
layered jaw/face mask, thick temple and rear-skull armor, and strong forward menace without becoming a giant
comedy helmet'; geometry covers crown, forehead, temples, cheeks, rear skull and face protection while still
respecting head rotation and readability; focal zones (glowing visor slit, horn roots, central brow ridge,
forehead crown plates, cheek structure and rear head protection) are polished; no accidental gaps, z-fighting or
broken UVs remain; animation follows the body correctly; first-person/third-person/item views work; gameplay
logic is preserved; the full set looks coherent; and build + runClient validation succeed.

END OF PROMPT.
```