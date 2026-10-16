# Fire Demonic armor visual rework + trident / wildlife / radio blast (2026-09-04)

## Demonic Trident LMB = netherite axe
- `DemonicTridentItem` (plain `Item`, melee was 1): attribute modifiers
  MAINHAND +8.0 damage (total 9) / -3.0 speed (total 1.0) = netherite-axe
  1:1, plus `hurtEnemy` durability tick. Thrown projectile untouched.

## Wildlife (verified already-correct, no changes)
- `ParadiseWildlifeSpawner`: IS_FOREST-only biomes (savanna excluded by
  vanilla tag), sunfinch flocks of 3 (crowns + air), grazers in pairs on
  crowns, local caps. `SunfinchEntity`/`CloudGrazerEntity`: BreedGoal +
  TemptGoal + `isFood(PARADISE_FRUIT)` + offspring — breeding with the
  sky-island fruit already works.

## Radio blast visual-only (explosive-blast prompt)
- No mushroom item exists in the mod; the Radio RMB airstrike
  (`ExplosionEntity`, 75 blocks / 150 dmg / 30s effects) is the blast.
- Zero gameplay changes (no code touched). Only
  `textures/entity/nuke.png` repainted (`scripts/generate_nuke_blast.py`):
  white-hot core base, magma fissures, ember pores, scorched rupturing
  shell top. Geo/anim/sound/fuse/damage/cooldowns intact. Old texture in
  `build/tool_backup/nuke.png`. Radio device sprite untouched (it is a
  radio, not a fungus — prompt §4 identity rule).

## Fire Demonic armor visual-only (ULTRA_MAX_v2 prompts + concept art)
- Hard rules kept: IDs, ArmorMaterial/stats, slots, recipes, set bonus,
  geometry (LayerDefinition) all intact.
- Rollback: 16 files (2 model javas, 2 layer javas, 4 layer/emissive
  textures, 4 item sprites + 4 item models) copied to
  `concepts/Fire_Demonic_Armor_ULTRA_MAX_v2/backup/`.
- `scripts/generate_demonic_armor.py` parses real texOffs/addBox from the
  model sources (per-statement split, so empty structural parents can't
  steal UVs) and repaints by part role to the concept bible: volcanic
  black joints, burnt-crimson slabs, magma visor/reactor/vents (also on
  the emissive map), ember-cracked horns. Old layer textures left most
  UV islands transparent (= invisible armor faces); now fully painted.
- Item sprites (16px) redrawn: horned visor helm, reactor-vent chest,
  greaves, sabatons.

## Validation
- `build` green, `validate_resources.py` clean (1191/531/62/70).
- In-game: check armor on player (all 4 pieces + emissive at night),
  trident tooltip shows 9 damage, Radio blast look, wildlife presence.
