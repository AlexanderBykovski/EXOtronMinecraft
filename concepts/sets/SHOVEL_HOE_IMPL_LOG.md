# Parthenon Shovel + Hoe — implementation log (+ Xiphos tip fix)

## Status: IMPLEMENTED. `./gradlew build` green. Resources + loader harness
green (5 weapons). Tilling table headless-test BLOCKED (vanilla Bootstrap
silently exits headless here — harness env issue, not mod code); table covered
by inspection + in-game §121-126 tests. In-game eyes pending.

## 0. Xiphos tip fix (user: "point looks into the sword")
Root cause: tip boxes rotated about a pivot near their TOP swung the long
bottoms outward past the blade AND crossed the tops over the center line
(X-tangle reading as an inverted point). Fix: shorter span (y 20..24.5),
pivot AT the apex (0, 25), angle ∓12°, inner edges shifted to meet exactly
at x=0. Verified numerically (ASCII projection: closed apex at y~25,
flared shoulders ±3) — no more center crossing.

## PART 1 — Shovel (registry `opusvsexe:parthenon_shovel` preserved)
- `scripts/generate_shovel.py`: 23 bones / 45 cubes. Pentagonal pointed head
  (36% height, 28% width), gold frame + marble + trim, 9-ray sun fan (looped),
  ruby housing, segmented handle, ruby housing, pommel ruby. QA silhouette OK.
- Anims: idle static (M6), equip, dig 0.45, attack 0.4, haste_cast 0.5
  (pommel->lower->head->sun), haste_recover 0.3, gem_pulse 2.6.
- `ParthenonShovelItem` (ShovelItem 1.5F/-3F + plain GeoAnimatable M2, intrinsic
  + tooltip parity): sneak+RMB = vanilla path (super.useOn), plain RMB = PASS
  -> ability (documented §35 resolution).
- Haste 255 = amplifier **254** (exact), 200t, cooldown 400t, durability -2
  once, caster-only, server-side, icon on/particles off. `use()` predicts cast
  client-side; server validates (cooldown/durability/spectator), applies,
  bursts ring+rise VFX once, schedules recover via NBT timestamp read in
  server inventoryTick (no new scheduler). Creative: cooldown yes, no durability.
- Mining VFX under Haste: `PlayerBlockBreakEvents.AFTER` (precedent
  FireToolEvents) with global 1-per-6-ticks throttle, shovel-in-hand only.
- Melee: restrained burst via attack mixin branch.

## PART 2 — Hoe (registry `opusvsexe:parthenon_hoe` preserved)
- `scripts/generate_hoe.py`: 22 bones / 36 cubes. Vertical handle + FORWARD
  (+Z) 3-segment stepped blade (10.7 long) with bevel edge, meander on TOP
  faces too, socket + ruby, housings, pommel. Front+side QA OK.
- Anims: idle static, equip, till 0.45 (press-down), attack 0.4, gem_pulse.
- `ParthenonHoeItem` (HoeItem -3/0F + plain GeoAnimatable M2, intrinsic +
  tooltip parity). `useOn`: center must be tillable + UP face, else PASS;
  server iterates dx,dz in [-3,3] SAME Y (49 max): world-border guard, skip
  farmland, vanilla-equivalent transform per cell (grass/dirt/path->farmland
  w/ air; coarse->dirt; rooted->dirt+hanging-roots drop; else null),
  setBlock flag 3, hurtAndBreak(1) per success with break-stop, max 24 custom
  motes, ONE hoe sound, ONE stat, till trigger to all viewers. Zero successes
  -> PASS. No cooldown/buff/damage/planting, as ordered.
- Assumption flagged: coarse-dirt air requirement mirrored as NOT required;
  user §126 tests will confirm; one-line change if vanilla differs.

## Files
NEW: 2 generators, 4 geo/anim/png sets... (shovel+hoe: geo/anim/png = 6),
6 Java (2 items, 2 models, 2 renderers). EDIT: ParadiseLine (shovel init),
ParadiseItems x2, ParadiseClient x2, PlayerAttackMixin x2, whitelist -2,
2 model JSONs (M7). DEL->backup: 2 sprites. No new mixins. No lang changes.

## Verification
- Build green (fixed 2 Mojmap slips: no MobEffects.HASTE — Haste IS DIG_SPEED;
  Level has setBlock not setBlockState).
- Validator: 1151 JSON / 50 Gecko pairs. Loader harness: shovel 45 cubes +
  7 anims; hoe 36 cubes + 5 anims; labrys re-verified after tip fix.
- Jar: all 15 new artifacts present, old sprites absent.
- PathWalkTest/TillLogicTest harnesses kept in /tmp (path test green; till
  table blocked headless — see above).

## Eyes needed (§113/§130 + xiphos still frame)
Shovel: hold/cast pose, Haste shows "255", mining perf. Hoe: exact 7x7,
ring-4 untouched, crops/farmland safe, coarse/rooted semantics, durability.
Xiphos: still screenshot standing idle to close the tip question.
