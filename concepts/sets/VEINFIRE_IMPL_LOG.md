# Vein Fire toolset — implementation log

## Status: IMPLEMENTED. `./gradlew build` green. Resources + loader harness
(5/5) + fan-walk test green. In-game eyes pending (prompt QA matrices).

## Design
Visual language from the 6 concept arts: black volcanic metal, magma
fissures (red halo -> orange -> yellow-white peaks), diamond infernal cores,
wrapped grips, glowing cubic pommels. Stepped axis-aligned tips/horns only.
Registry IDs `fire_*` ("Vein Fire ..." names) preserved with recipes/langs/
tabs; tier/stats/props preserved (incl. sword Fire Aspect II + ignite,
pickaxe Furnace-Touch tooltip, fireResistant props).

## Shared infrastructure (reused)
- `FireToolEvents.scheduleSmelt` extracted public: the vein ability feeds it
  broken positions; the next-tick rewrite smelts raw drops (Fortune kept,
  Silk Touch ore-blocks have no recipe -> preserved). No duplication.
- EMBER/ASH custom particles + FIRE_CHARGE/FIREBALL_LAUNCH/FIRE_EXPLODE/
  BONE_MEAL_USE/HOE_TILL/GRAVEL_BREAK sounds: all pre-existing, no new assets.
- `ToolHarvest` (drops/XP-note/durability) + `tillTransform` table shared with hoes.

## The five abilities (all server-authoritative)
- Sword INFERNAL BRAND: 16x3 broad wave (heightmap, wall-stop), 5.0 once per
  target + brand; +20t entity-only eruption 6.0 on branded targets. CD 160t,
  -4 dur. Scheduler in FireSwordAbility (per-cast state).
- Pickaxe MAGMA VEIN: RMB on harvestable ore -> BFS (stem family, r8,
  128 visited, 32 kept) -> ToolHarvest each + scheduleSmelt. CD 120t.
- Axe HELLCLEAVER: 3 arcs (0/+-40 deg, 10 long, +-1 walk each), shared dedupe,
  9.0 once, terrain-stop, no block damage. CD 160t, -5 dur. FireAxeFan scheduler.
- Shovel EXCAVATION: face-oriented 5x5x1 (XZ/XY/ZY by clicked face, r2, 25 max):
  MINEABLE_WITH_SHOVEL + BE skip + border per cell. CD 60t.
- Hoe 3x3 till (shared table, farm-safe, per-success durability) + ASHEN BLOOM
  5x5 maturation (Bonemealable loop to full, no harvest, mature skipped,
  growth-only CD 200t + -2, till path never gated).

## Files
NEW: scripts/generate_veinfire.py, 15 assets (fire/ namespace), 17 Java
(5 items, 5 models, 5 renderers, FireSwordAbility, FireAxeFan). EDIT:
FireItems x3 (axe/shovel/hoe; sword/pickaxe classes replaced in place),
FireClient x5, FireLine (2 scheduler inits), PlayerAttackMixin x5,
FireToolEvents (scheduleSmelt), whitelist -5 fire, 5 model JSONs (M7),
en_us+ru_ru (+7 tooltip keys). DEL->backup: 5 fire sprites.

## Verification
- Build green (fixed: mod-vs-vanilla sound names, registry ctor shapes,
  template leftovers, missing MAX_LATERAL, BonemealableBlock/MobEffects names
  — all compiler-caught, zero silent).
- Validator: 1171 JSON / 60 Gecko pairs. Loader harness 5/5 (17-32 cubes,
  correct lengths/loops). FanWalkTest 60 seeds clean. Jar: all 37 present.
- New tests kept: FanWalkTest. Old: PathWalkTest still green (untouched code).

## Eyes needed
Hold poses, swing parity, brand wave/eruption readability, vein limits +
smelt results, fan shape/dedupe, face-plane excavation, bloom maturation,
multiplayer sync, cooldowns/durability, Silk/Fortune/Unbreaking.
