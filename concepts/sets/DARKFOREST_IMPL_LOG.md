# Dark Forest toolset — implementation log

## Status: IMPLEMENTED. `./gradlew build` green. Resources + loader harness
(5/5) + wave-walk test green. In-game eyes pending (prompt test matrices).

## Design
Visual language from the 6 concept arts: charcoal fractured plates, cold gray
edges, violet arcane cracks, twisted root handles, 6-petal night flowers with
luminous cores, sparse teal fungus, cube pommels with flower insets. All tip/
horn geometry is stepped axis-aligned (no rotation-convention risk after the
xiphos tip saga). Palette + painters shared in one generator.

## Shared infrastructure (reused, not reinvented)
- `MossboundAttackEntity` +3 lines: `visualOnly` flag (default false — boss
  behavior and its QA contract untouched) + NBT. Ability VFX reuses
  ROOT_SNARE (axe wave), MARKED_STEP (teleport marks), BLOOMFALL (bloom,
  capped 8) with their synced models/animations/particles.
- `com.opus.item.ToolHarvest.breakWithTool`: tool-aware drops (Silk/Fortune),
  Unbreaking/creative, break-stop. XP deliberately NOT replicated (1.20.1
  computes it in protected harvest paths; hardcoding tables would be worse).
- `DarkForestAxeWave`: 11-cell scheduler (ServerTickEvents), per-cast state.

## The five tools (IDs/recipes/langs/tabs preserved; RARE; same tier/stats/
intrinsic/tooltip incl. ToolMarker parity)
- Sword — SHADOW BLOOM STEP: teleport <=10 along clamped look, 0.5 sampling,
  full-box noCollision destination + horizontal wall sweep + landing/void/
  lava-fire-cactus-powdersnow guards; slash 7.0 r=1.0 once per target
  (canHarmPlayer, canBeAffected Darkness 40t); CD 120t; -3 dur.
- Pickaxe — VEINROOT AWAKENING: RMB on harvestable ore (stem family:
  iron_ore/deepslate_iron_ore -> iron); BFS 26-n, radius 8, 128 visited,
  32 broken; CD 80t; normal durability per block.
- Axe — ROOTSNARE CLEAVE: 11x~3 wave (+-1 walk), heightmap follow, wall stop,
  1t/layer, 9.0 once per target, Slowness V 40t (grounded only, immunity
  respected); CD 200t; -5 dur.
- Shovel — NIGHTROOT EXCAVATION: RMB on MINEABLE_WITH_SHOVEL center -> 5x5
  (r=2, 25 max, same Y): tag check + BE skip + border per cell; CD 80t.
- Hoe — NIGHT BLOOM: farmland/growable -> 7x7 pulse (Y+Y+1, Bonemealable
  valid+success roll -> perform, 1 attempt, HAPPY_VILLAGER, capped 8 bloom
  visuals, CD 360t, -2 dur); tillable -> vanilla single-till (super.useOn);
  else PASS. Crops/farmland never touched otherwise.

## Files
NEW: scripts/generate_darkforest.py (framework + 5 tables), 15 assets
(geo/anim/png x5), 17 Java (5 items, 5 models, 5 renderers, ToolHarvest,
DarkForestAxeWave). EDIT: MossboundAttackEntity (+visualOnly),
DarkForestItems x5, DarkForestClient x5, DarkForestLine (wave init),
PlayerAttackMixin x5, whitelist -5 DF, 5 model JSONs (M7). DEL->backup:
5 DF sprites. New tests: WaveWalkTest (60 seeds, 0 violations).

## Verification
- Build green (fixed: FluidTags package, BonemealableBlock name,
  BONE_MEAL_USE name, XP/drop API corrections).
- Validator: 1161 JSON / 55 Gecko pairs. Loader harness 5/5 (26-52 cubes each).
- Jar: all 38 artifacts present; old DF tool sprites absent (armor sprites kept).
- Dead imports removed; old tool classes kept (ToolMarker contract).

## Eyes needed (prompt matrices)
Hold poses x5, swing alternation, teleport safety set (~14 cases), vein
limits, wave shape/root, 5x5 ring-3 guard, bloom crop safety, multiplayer
sync, cooldowns/durability, enchantments (Silk/Fortune/Unbreaking).

## PATCH PASS (2026-09-03, from 6 in-game screenshots)
1. Sword tip (files: generate_darkforest.py TIP table only): rebuilt as a
   taller 5-step pyramid (y19..25.3, +-2.0 -> +-0.45, single-box apex),
   axis-aligned, center-overlapped (no coplanar seam). Root cause of the old
   look: rotated bars splayed past the blade and crossed the center line.
   Verified numerically (monotonic symmetric taper).
2. Axe held backwards (files: generator head tables): ROOT CAUSE — with the
   family yaw (-90) model -X maps to world-backward in first AND third
   person (proven against vanilla axe texture convention: head at +X reads
   forward). Big crescent was authored at -X. FIX: mirrored head across X —
   grand crescent now +X (forward), back blade -X; also matches concept art.
3. Gaps audit (programmatic, all 5 geos): REAL finds fixed — 2 floating guard
   branches (sword, 0.4 gap) extended into the bar; 2 floating pickaxe tip
   crystals (0.6 gap) moved into the beaks. Plus systematic EPS 0.02 volumetric
   overlap in the generator killing every exact-coplanar same-normal contact
   (post-fix audit: 0 floaters, 0 coplanar on all 5). Decorative recesses kept.
4. Hoe rework (files: DarkForestHoeItem, ToolHarvest): till table moved to
   ToolHarvest (ParthenonHoeItem migrated to it, behavior identical). DF hoe:
   priority crop-growth (Bonemealable-valid clicked block -> bounded
   performBonemeal loop to full maturity, no harvest/plant) vs 3x3 till
   (radius 1, 9 max, same-Y, vanilla rules, farm-safe, per-success durability).
   Cooldown GROWTH 200t + durability 1 ONLY on successful growth; till path
   never touches it (separate branches, verified by reading). Mature crops ->
   silent PASS.
Build green throughout; harness re-passed on final geometry; QA sheets
regenerated (axe mirrored correctly).
