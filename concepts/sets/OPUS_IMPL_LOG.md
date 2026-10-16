# Opus set — GeckoLib 3D rework (master prompts v1)

Source: `concepts/Opus_And_Existing_Items_Master_Prompts_v1/Opus_Weapons_And_Existing_Items_Master_Prompts.md`.
Generator: `scripts/generate_opus.py` (single source of truth, M8). Lessons M1/M6/M7/M11 applied.

## Scope decision
- 3D + abilities: `katana_op`, `katana_gold`, `katana_refined`, `opus_warhammer`,
  `opus_pickaxe`, `opus_axe`, `opus_shovel`, `opus_hoe` (ids unchanged, ModTier.OPUS stats unchanged).
- 3D, NO new ability (prompt §25/26): settlement `katana` (= Steel Katana),
  `long_katana` — `JapaneseKatanaItem` converted to GeoAnimatable in place,
  `executeTechnique` untouched.
- Visual-only ingredients (`shade_silk`, `moonwing_membrane`, `moonflower_heart`,
  `rootbound_eye`, `briarweave`, `paradise_fruit`, `cloud_fleece`,
  `aerie_bronze_ingot`, `seraphic_pinions`, `ruby_halo_shard`, saplings/pods):
  intentionally left as sprites; functional code untouched per master rule.

## Abilities (all server-authoritative, bounded)
- Katana-OP/Gold/Refined: logic preserved 1:1 from old `KatanaItem`
  (OPUS forward slash 14.0F/24t cd 50 / GOLD ground wave 12.0F/22t cd 100 /
  REFINED 12-blade ring cd 120) via `KatanaSlashEntity`.
- Warhammer Shockwave: `CombatEffects.shockwave(6.0, 16.0, 2.8, launch)` +
  Slowness II 5s on valid targets, cd 100. No terrain damage.
- Pickaxe Azure Vein Resonance: `ToolHarvest.collectVein` (32/8/128) +
  `breakWithTool`, blue VFX, cd 120. No smelt (Opus is not fire).
- Axe Crosscut Arc (`OpusAxeArc`): instant corridor L12 / half-width 2 /
  height 2.5, ClipContext occlusion, 9.0 dmg once per target, knockback,
  whiff = visuals + 20t cd only, hit = cd 100 + 2 durability.
- Shovel Prism Trench: 3x3x1 by clicked face, shovel-mineable only, cd 60.
- Hoe Growth Lattice: 3x3 till (vanilla `ToolHarvest.tillTransform` rules) +
  5x5 bloom (radius 2, max 25, 16 bonemeal attempts); bloom cd 200 NEVER
  blocks tilling (checked only on the bloom path). Settlement/Paradise/Fire
  hoe pattern reused.

## Assets
- `geo/opus/*.geo.json` (8), `geo/settlement/{katana,long_katana}.geo.json`,
  matching `animations/` + `textures/{opus,settlement}/item/*.png` (256px).
- EPS 0.01 volumetric overlap everywhere; gap audit: all touching contacts
  EPS-covered, 0 floaters (connected sockets/collars/cores by construction).
- Item JSONs `models/item/{katana_op,katana_gold,katana_refined,opus_*,katana,long_katana}.json`
  = `builtin/entity` + M7 display (third [0,∓90,12], first [0,∓90,25],
  gui 0.45, ground 0.4).
- Old sprites backed up to `build/tool_backup/`, PNGs deleted.
- Whitelists cleaned: `generate_tool_sets.py` (opus entries removed),
  `generate_tool_set_32.py` (katanas + opus family removed) — regen-safe.

## Code
- New `com.opus.opus.item`: `OpusKatanaItem` (Kind OPUS/GOLD/REFINED),
  `OpusWarhammerItem`, `OpusPickaxeItem`, `OpusAxeItem` + `OpusAxeArc`,
  `OpusShovelItem`, `OpusHoeItem` — plain `GeoAnimatable` (M2), manual
  fireTrigger routing (M4), per-perspective state (M5), static idle + fx
  pulse ≤1.04 (M6).
- `ModItems`: same IDs/tiers/stats/tooltip keys, classes swapped.
- `JapaneseKatanaItem`: GeoAnimatable in place, technique + cooldowns kept.
- `PlayerAttackMixin`: onStrike branches for all 8 opus + japanese katanas.
- Client `com.opus.opus.client.OpusClient.init()` (10 renderers) wired into
  `OpusVsExeClient`; swing→attack/work + equip triggers per model.
- Lang EN/RU: `opus_warhammer/pickaxe/axe/shovel/hoe.ability` added;
  katana + hammer lore keys reused.

## Validation (2026-09-03)
- `compileJava` + `compileClientJava`: clean.
- `./gradlew build`: green. `validate_resources.py`: 1191 JSON, 531 PNG,
  62 OGG, 70 Gecko pairs (was 60, +10 opus/settlement).
- Loader harness (real GEO_GSON + BakedModelFactory + BakedAnimations):
  10/10 PASS, bones + anims verified per asset.
- In-game check still needed: hand fit, first-person, GUI, abilities,
  Haiku opus-only message, Sunfinch/Cloud Grazer spawns.

## Gap fix pass (2026-09-03, second iteration)
- Connectivity audit (contact graph over EPS-inflated boxes, face + volume
  contact) found TRUE structural gaps in my own opus models; older sets
  (Paradise / Dark Forest / Vein Fire) deliberately NOT touched:
  - all 5 katanas: 3 components (blade floated 0.5–0.7 above guard, guard
    0.5 above handle). Fixed: shaft extended up into guard (top y=2.0),
    new `neck` cube with energy strip bridges guard top into blade bottom.
  - axe/hoe/pickaxe/shovel: pommel floated 0.2 below handle shaft.
    Fixed: pommel body extended up to overlap shaft bottom.
  - warhammer was already 1 component.
- After regen: all 10 models = 1 connected component, 0 floaters,
  harness re-run 10/10 PASS, build green.

## Part III visual-only ingredients (2026-09-03)
- New generator `scripts/generate_opus_ingredients.py` repaints all 13 in
  place (IDs/classes/gameplay untouched per prompt §17/18/26/28; 2D icons
  per §2/§8/§14/§16, NOT GeckoLib):
  Dark Forest — `shade_silk`, `moonwing_membrane`, `moonflower_heart`,
  `rootbound_eye`, `briarweave`; Paradise — `paradise_fruit`,
  `cloud_fleece`, `aerie_bronze_ingot`, `seraphic_pinions`,
  `ruby_halo_shard`, `paradise_sapling` (item sprite + block cross
  texture); Hell — `fire_bean` = Ember Kapok Pod item sprite,
  `ember_sapling` = Ember Kapok Sapling block cross texture (16px).
- Old PNGs backed up to `build/tool_backup/`. QA contact sheet reviewed
  at 8x (`/tmp/opus_ingredients_qa.png`): silhouettes readable,
  family palettes consistent; briarweave thorn tips toned down after review.
- Validator still clean (same PNG count, contents replaced).

## All-sets gap fix + Sunfeather/briarweave/wall (2026-09-04)
- Connectivity audit over EVERY tool geo (face + volume contact):
  Paradise xiphos (3 comp: blade/guard/handle split) + shovel (2 comp:
  sun medallion floated 0.1 in front of the marble plate); Dark Forest
  all 5 (sword was 4 comp — blade/guard/handle/pommel all split; shovel
  panel foot + pommel; hoe beak_mid spikes + pommel; axe/pickaxe pommel);
  Vein Fire all 5 (sword blade floated 1.2 over guard; 4× pommel 0.2 gap).
- Fixes (generator-side, M8): blade bases / shafts extended INTO their
  neighbors, new neck/ricasso bridges (veinfire sword, DF sword),
  DF shovel panel foot reaches into the flower, DF hoe spikes reach into
  the mid body, paradise sun medallion back embedded into the plate,
  xiphos blade base + collar overlap the guard, all pommels overlap
  shaft bottoms. After regen: 15/15 = 1 component, 0 floaters.
- Sunfeather: concept in `concepts/sunfeather_rework.md` (Sunfinch golds +
  cyan quill + ruby glint), sprite repainted in place, old backed up.
- Briarweave: redesigned to exact gloomwood-log palette (near-black plum
  weave, mauve edges, moss-teal binding like the log's moss bands).
- Colosseum Wall: hardness/blast were already nether-brick 2.0/6.0 with
  correct-tool requirement; sound switched METAL → NETHER_BRICKS so it
  fully mirrors vanilla Nether Bricks.
- Validation: `build` green, validator clean, generic loader harness
  (real GEO_GSON bake + anim-bone cross-check) 25/25 PASS across
  paradise/dark_forest/fire/opus/settlement tool geos.
