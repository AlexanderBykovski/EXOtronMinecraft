# Parthenon Xiphos + Celestial Path ability — implementation log

## Status: IMPLEMENTED. `./gradlew build` green (1 pre-fix error, fixed).
Resources + real-loader harness + path-walk test green. In-game eyes pending.

## PART 1 — Xiphos item (registry `opusvsexe:parthenon_sword` preserved)

Reference: celestial straight sword art. Display name stays "Parthenon Xiphos"
(project convention beats the prompt's "Paradise Sword").

### Created
- `scripts/generate_xiphos.py` — same pipeline (M1/M6/M7/M8).
- `geo/paradise/xiphos.geo.json` (1.12.0, 20 bones, 39 cubes; blade 23/35 = 66%).
- `animations/paradise/xiphos.animation.json` (idle/equip/attack/attack_alt/
  lightning_cast/lightning_recover/gem_pulse). attack & attack_alt share
  identical 0-0.1s anticipation so a server trigger landing inside it never snaps.
- `textures/paradise/item/xiphos.png` (256x256, `"uv"`+`uv_size`, M1).
- `ParthenonXiphosItem` (SwordItem + plain GeoAnimatable, M2): same tier/stats
  (ParthenonToolTier, 3, -2.4F), same tier tooltip + 2 new ability lines.
- `ParthenonXiphosModel` (alternating attack/attack_alt by swing parity,
  equip per first-person stack/slot M4/M5, swing trail + whoosh).
- `ParthenonXiphosRenderer`.
- `ParadiseSwordAbility` — path generator + tick scheduler + damage (below).
- QA: `docs/assets/concepts/xiphos-qa-2026-09-03.png` (a tip-sign bug found
  here — mirrored horns diverged; fixed and re-verified).

### Modified / deleted
- `ParadiseItems` (sword swap), `ParadiseClient` (renderer),
  `PlayerAttackMixin` (xiphos branch), `ParadiseLine` (ability init),
  `generate_tool_sets.py` (sword out of sprite whitelist, M11),
  `models/item/parthenon_sword.json` (builtin/entity, M7 display),
  `en_us` + `ru_ru` (ability/cooldown tooltip). Old sprite + mcmeta -> backup.

## PART 2 — Celestial Path ability (RMB, single press, no hold)

- `tryCast` (server): spectator deny, cooldown check, durability-guard
  (no suicide casts), path gen, cast register, cooldown 160t, durability -5
  once, cast anim to all viewers, beacon-activate sound. Creative bypasses
  cost/cooldown.
- Path (non-negotiables enforced + TESTED): 25 steps, random walk in [-2, 2],
  max step 1, 55% keep, center drift at extremes, 35% single-cell protrusions,
  LinkedHashSet dedupe, heightmap MOTION_BLOCKING_NO_LEAVES, wall step-up >3
  stops, void gaps skip.
- Triple per cell: 1 cosmetic `LightningBolt(visualOnly)` with +=0.2 jitter +
  2 particle echoes (END_ROD column + FIREWORK flash) at +2/+4 ticks. No fire,
  no vanilla damage, no terrain damage. Propagation 1 tick/layer (~1.2 s).
- Damage: ONE event per entity per cast (UUID dedupe), 8.0 via
  `damageSources().lightningBolt()`, radius 1.0, caster excluded,
  creative/spectator/invulnerable skipped, restrained knockback. No stun.
- Scheduler: `ServerTickEvents.END_SERVER_TICK`, per-cast state
  (multi-caster safe), dropped on logout/death/dimension-unload. No sleep.
- Audio: cast beacon sound, bolts' own spread thunder, finale impact; no
  75x spam by construction (only ~35 real bolts over ~1.2 s + quiet echoes).
- Recover anim fired at +12t server-side on the currently held xiphos.

## Verification
- Build green (fixed 1 error: `level.random` is RandomSource, not Random).
- Validator: 1147 JSON, 531 PNG, 62 OGG, 48 Gecko pairs.
- Loader harness (real GeckoLib bake): xiphos GEO 39 cubes + all 7 anims with
  correct lengths/loops.
- NEW `PathWalkTest` (60 seeded paths): 0 violations (range/step), 0 flat,
  keep-ratio 0.50 — the §34-37/§116 contract, executed, not asserted by eye.
- Jar contains all 4 classes + 4 assets. No stale refs (power n/a here;
  old sprite gone; tooltip keys in EN+RU).

## Compromises (open, per prompt §121)
- Echoes 2/3 are dense particle columns, not full bolt entities (audio + perf).
- Protrusion branches limited to single extra cells (chains emerge naturally).
- No custom bolt texture/entity; vanilla cosmetic bolt + gold/ivory particles
  carry the Paradise identity.

## Still needs eyes in-game (§130 matrix)
Hold pose, swing parity feel, cast wave shape/triples/propagation, damage UX,
cooldown/durability, multiplayer sync, hills/walls/cliffs/water, reloads.
Display numbers reasoned (M7) — expect one screenshot pass.

## Tip mirror fix (2026-09-04)
- In-game screenshot showed the tip splayed outward (fishtail) instead of
  converging: TIP_L used rot -12, but Minecraft/GeckoLib +Z rotation runs
  opposite to textbook-math CCW, so -12 leans tops outward.
- Fix: TIP_L rot -12 → +12 (mirror() yields -12 on the right; symmetry
  preserved). Rendered projection confirms a centered converging point.
- Revalidated: 1 connected component, loader harness PASS, validator clean.

## Stepped point redesign (2026-09-04)
- Two leaned half-slabs always read as separate prongs with a center notch,
  never as one sharp point. Rebuilt the tip as a single centered stepped
  point (3.8 → 2.6 → 1.6 → 0.7 + gold point cap), zero rotations, symmetric
  by construction. Projection verified: one continuous point, no notch.
- Revalidated: 1 connected component (46 cubes), harness PASS, clean.
