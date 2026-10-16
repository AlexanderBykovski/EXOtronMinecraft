# Parthenon Pickaxe + Labrys combat rework — implementation log

## Status: IMPLEMENTED. `./gradlew build` green first try. Resources + loader
harness green for both weapons. In-game eyes check pending (no display here).

## PART 1 — Parthenon Pickaxe (registry `opusvsexe:parthenon_pickaxe` preserved)

Reference: celestial pickaxe art (broad shallow arc, square sun housing,
marble+gilt arms, red tip gems, segmented handle, grip block, pommel).

### Files created
- `scripts/generate_pickaxe.py` — same proven pipeline as the labrys generator
  (M1/M7/M8): BONES table -> geo + 256x256 texture + animations + QA.
- `geo/paradise/pickaxe.geo.json` (1.12.0, 31 bones, 64 cubes; x +-11.6 = 66%
  of height, y -17.8..18).
- `animations/paradise/pickaxe.animation.json` (1.8.0: idle/equip/mine/attack/
  gem_pulse). idle = STATIC hold (M6); mine 0.3s (lag -> strike -> recoil +
  tip flash); gem_pulse 2.2s wave center -> tips -> grip -> pommel.
- `textures/paradise/item/pickaxe.png` (256x256, per-face `"uv"`+`uv_size`, M1).
- `ParthenonPickaxeItem` (PickaxeItem + plain GeoAnimatable, M2):
  same tier/stats as before (ParthenonToolTier, 1, -2.8F), same intrinsic
  Efficiency application + tooltip.
- `ParthenonPickaxeModel` (entityCutoutNoCull; swing-edge trigger picks MINE
  vs ATTACK by crosshair target; equip per first-person stack/slot, M4/M5).
- `ParthenonPickaxeRenderer`.
- QA: `docs/assets/concepts/pickaxe-qa-2026-09-03.png` (silhouette verified:
  arc head, sun housing, crown, segmented handle, pommel).

### RMB skill: Forge Attunement (server-authoritative, no new assets)
- `use()` channels (UseAnim.BOW, 72000). Server `inventoryTick`: while held ->
  Night Vision 60t + Haste V (amp 4, as ordered) refreshed + END_ROD sparkle
  every 10t; NBT `ParthenonAttuneLast` timestamp; after release the same buffs
  refresh at 40t while `gameTime - last <= 200` (10 s tail, as ordered).
- `releaseUsing` after >=10t charge: vanilla BEACON_ACTIVATE + burst.
- Cannot mine while channeling (vanilla use lock) — self-balancing.

### Files modified / deleted
- `ParadiseItems`: PICKAXE swap (1 line + import). `ParadiseClient`: renderer
  registration. `PlayerAttackMixin`: pickaxe branch (attack trigger +
  HAMMER_HIT@1.1 + small burst). `generate_tool_sets.py`: parthenon_pickaxe
  removed from sprite whitelist (M11). `models/item/parthenon_pickaxe.json`:
  builtin/entity + upright display (M7). Old sprite + mcmeta -> backup, deleted.
- Recipe, advancements, langs, creative tab, ParthenonGearQa untouched.

## PART 2 — Labrys combat rework (RMB = BLOCK, power REMOVED)

- Deleted: POWER const/triggerable, `releaseUsing` power (cooldown, shockwave
  particles, HAMMER_ULTIMATE), `power` animation from generator + assets.
- Kept: UseAnim.BLOCK + 72000 -> vanilla `isBlocking()` mechanics live
  (5-tick startup, frontal arc, bypass rules, durability via
  `hurtCurrentlyUsedShield`, axe-disable, projectiles). Names verified in the
  official 1.20.1 layered mappings.
- New animations (generator, baked+verified): block_enter 0.25s, block_idle
  loop 1.5s (STATIC defensive pose, M6), block_hit 0.18s, block_exit 0.2s.
- Triggers (client model, no Minecraft in predicate): use rising edge ->
  block_enter; held +6t -> block_idle loop-triggerable (repeat = no-op);
  release edge -> block_exit. Server: new `ShieldBlockMixin` on
  `LivingEntity.hurtCurrentlyUsedShield` -> `onBlocked` (anim to all viewers +
  4+2 spark supplement + low clang over vanilla SHIELD_BLOCK).
- Attack VFX upgrade (paradise palette, budgets respected): client swing trail
  (8 END_ROD along look + 2 FIREWORK); server hit burst made directional with
  crit scaling (~50% + star burst on falling hits); block impact small and
  ring-less (visually distinct from attack). No AoE, no explosion, no aura.

## Verification
- `./gradlew build` (offline): SUCCESS, zero errors.
- `validate_resources.py`: 1145 JSON, 531 PNG, 62 OGG, 47 Gecko pairs.
- Loader harness (real GeckoLib 4.4.9 bake) on BOTH weapons: cubes baked
  (pickaxe 64, labrys 69), all bones + animations resolve, loop types correct.
- No `power` references left in labrys code; no old-sprite references.
- Jar contains all 8 new/changed classes + 7 assets.

## Still needs eyes in-game
Pickaxe hold pose, mine rhythm vs hand swing, attunement icon/particles,
labrys block pose coverage (20-40% screen), block_hit feel, crit star.
Display numbers are reasoned (M7), expect one screenshot-driven pass.
