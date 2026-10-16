# Parthenon Labrys — implementation log

Reference: attached divine double-bladed axe art.
Registry id PRESERVED: `opusvsexe:parthenon_axe` (recipe, advancements,
ParthenonGearQa recipe list, all 5 lang names already "Parthenon Labrys").

## Status: IMPLEMENTED, resources verified. Java compile NOT run on this host (no JDK).

## Files created
- `scripts/generate_labrys.py` — single source of truth: BONES table ->
  geo + 256x256 texture + animations + QA sheets. Re-running regenerates all
  three asset kinds consistently (bone names cannot drift).
- `src/main/resources/assets/opusvsexe/geo/paradise/labrys.geo.json`
  (format 1.12.0, 26 bones, 69 cubes; Y-up, origin at grip y=0,
  head y 8..19 / +-10.7, handle to y -16).
- `src/main/resources/assets/opusvsexe/animations/paradise/labrys.animation.json`
  (format 1.8.0: idle/equip/attack/power/gem_pulse).
- `src/main/resources/assets/opusvsexe/textures/paradise/item/labrys.png`
  (256x256, per-face UV, alpha 0/255 only).
- `src/main/java/com/opus/paradise/item/ParthenonLabrysItem.java`
  (AxeItem + GeoItem; stats identical to before: ParthenonToolTier, 5.0F, -3.0F).
- `src/client/java/com/opus/paradise/client/model/ParthenonLabrysModel.java`
  (entityCutoutNoCull; client-side swing/equip prediction on render thread).
- `src/client/java/com/opus/paradise/client/renderer/ParthenonLabrysRenderer.java`
- QA: `docs/assets/concepts/labrys-qa-2026-09-03.png`,
  `labrys-texture-2026-09-03.png`, `labrys-key-zoom.png`.

## Files modified
- `ParadiseItems`: PARTHENON_AXE now `new ParthenonLabrysItem(... EPIC)` (1 line + import).
- `ParadiseClient`: `BuiltinItemRendererRegistry.register(PARTHENON_AXE, renderer::renderByItem)`.
- `PlayerAttackMixin`: labrys branch -> `onStrike` (server anim trigger + HAMMER_HIT + impact particles).
- `models/item/parthenon_axe.json`: parent `builtin/entity`, axe-diagonal display
  (thirdperson [0,-90,55], firstperson [0,-90,25] — hand grips lower handle,
  decorated +Z face outward, crosshair free).
- `scripts/generate_tool_sets.py`: `parthenon_axe` REMOVED from WHITELIST so the
  sprite pipeline can never overwrite the 3D assets.

## Files deleted (backed up to build/tool_backup/)
- `textures/item/parthenon_axe.png` + `.png.mcmeta` (flat sprite replaced by 3D).

## Animation trigger architecture (GeckoLib 4.4.9, verified against its sources)
- `main` controller: idle loop default; equip/attack/power as triggerableAnims.
  Predicate yields while a triggered anim plays.
- `fx` controller: gem_pulse loop (staggered ruby breathing).
- Attack: client prediction (model sees local swing rising edge via
  DataTickets.ITEMSTACK + getAttackAnim) + server trigger from the attack mixin
  (AnimTriggerPacket to tracking clients). Re-trigger of the same RawAnimation
  is a no-op in AnimationController, so no snap when both fire.
- Equip: client model triggers when a new stack appears in first person.
- Power: right-click charge (UseAnim.BLOCK pose), release -> server cooldown 40,
  HAMMER_ULTIMATE, END_ROD+FIREWORK burst; purely cosmetic, damage untouched.
- Sounds: KATANA_SWING@0.55 (swing), HAMMER_HIT (hit), HAMMER_ULTIMATE (power)
  — all pre-existing events, no new audio. Particles: vanilla END_ROD/ENCHANT/
  FIREWORK only. No new registries of any kind.

## Verification done here
- `scripts/validate_resources.py`: 1143 JSON, 531 PNG, 62 OGG, 46 Gecko pairs — clean.
- Programmatic: all animation bones exist in geo (26/26), all parents resolve,
  no zero-size cubes, all face UVs inside 256 bounds, all 5 Java animation-name
  constants match JSON, geo 1.12.0 / anim 1.8.0.
- Every GeckoLib symbol used was confirmed present in geckolib-4.4.9-sources.jar
  from the Gradle cache; every Mojmap symbol (ItemDisplayContext constants,
  UseAnim.BLOCK, LivingEntity.getAttackAnim) confirmed in the official 1.20.1
  layered mappings (loom.mappings.1_20_1.layered).
- QA renders inspected: silhouette (double crescent + crown + segmented handle
  + pommel), Greek-key meander on border strips, ruby faces (dark shell, scarlet
  core, pink highlight).

## MUST still be done on a machine with JDK 17
DONE HERE (JDK found at ~/.jdks/jdk-17.0.20+8):
`./gradlew build` -> BUILD SUCCESSFUL; jar contains all labrys classes/assets.
In-game matrix still needs eyes: inventory / hands / persons / dropped / attack /
air-swing / sneak / enchanted glint / F3+T (display tuning pass expected).

## Post-build crash fix (2026-09-03)
Symptom: launch failed at compileJava.
Root cause: `ParthenonLabrysItem implements GeoItem` without the two abstract
SingletonGeoAnimatable members. The in-project precedent (DemonicTridentItem)
implements plain GeoAnimatable, which has no such members — but plain
GeoAnimatable cannot server-sync triggers, so GeoItem was kept and the contract
completed instead:
- `createRenderer(Consumer)` no-op + `getRenderProvider()` returning `() -> null`,
  documented: Fabric renders via BuiltinItemRendererRegistry (ParadiseClient),
  RenderProvider is a Forge-side hook never touched on this loader. A main/client
  split-source-set layout forbids referencing the client renderer from the item.
Boot check: mod init clean ("OpusVsExe mod initialized"), zero mixin/GeckoLib/
paradise errors; only pre-existing "No data fixer" noise. Full client boot to
title was impossible from the build shell (no DISPLAY/Wayland) — needs a desktop
run by the user.

## World-load crash fix (2026-09-03, crash-2026-09-03_12.46.37-client.txt)
Symptom: entering a world crashed the render thread (knock-on NPE in
LevelRenderer: null shader after a failed resource reload in Recovery mode).
Root cause, from the report's reload section:
`GeckoLibException: opusvsexe:geo/paradise/labrys.geo.json: Error loading model file`
caused by `NullPointerException: ...UVUnion.isBoxUV()... "uvUnion" is null`.
My generator wrote per-face UVs under a `"faces"` key; GeckoLib 4.4.9's Cube
deserializer only reads `"uv"`, which must be an OBJECT of per-face entries in
per-face mode (`"uv": {north: {uv:[...], uv_size:[...]}, ...}`) — a bare
`"faces"` key is silently ignored, leaving uvUnion null.
Fix: `scripts/generate_labrys.py` now emits the Bedrock-correct `"uv"` object
(incl. `uv_size`, which FaceUV also requires); assets regenerated.
Proof beyond static checks: headless harness `/tmp/labrys_test/LabrysLoadTest`
runs GeckoLib 4.4.9's REAL `JsonUtil.GEO_GSON` deserialization +
`BakedModelFactory.constructGeoModel` + `BakedAnimationsAdapter` over the
assets: GEO baked (69 cubes, all key bones), all 5 animations parsed with
correct lengths (idle 60t, equip 8t, attack 9t, power 18t, gem_pulse 40t) and
loop types. Negative control (one cube reverted to `"faces"`) reproduces the
exact in-game NPE, so the harness is faithful. `./gradlew build` green again;
user must relaunch (I cannot render without a display).

## Hotbar-render crash fix (2026-09-03, crash-2026-09-03_12.56.40-client.txt)
Symptom: entering a world with the labrys in the hotbar crashed in
`ItemRenderer.handler$zdn000$geckolib$itemModelHook` ("Rendering item"):
`RenderProvider.of(stack)` returned null.
Root cause: GeckoLib 4.4.9's Fabric `MixinItemRenderer` calls
`RenderProvider.of(stack).getCustomRenderer()` for EVERY item render, and
`RenderProvider.of` returns `getRenderProvider().get()` for any `GeoItem`.
My `() -> null` provider (added for the compile fix) NPE'd there. The provider
cannot exist in this split main/client layout, so the correct architecture —
same as the working DemonicTridentItem — is plain `GeoAnimatable` + vanilla
baked-model path (`builtin/entity` + `BuiltinItemRendererRegistry`), which the
mixin leaves alone (`DEFAULT` provider -> no-op -> vanilla continues).
Change: `ParthenonLabrysItem implements GeoAnimatable`; trigger routing
(`SingletonGeoAnimatable.triggerAnim`) inlined as `fireTrigger` using public
`GeckoLibNetwork.sendToTrackingEntityAndSelf` + `AnimTriggerPacket`
(server) and direct manager trigger (client). `GeoItem.getOrAssignId/getId`
are static and still used. `./gradlew build` green; resources re-validated.

## Hold-pose fix (2026-09-03, from in-game screenshot)
Two complaints, two root causes:
1. Cyclic first-person sway (tilt left, rise back right) = the `idle`
   animation's weapon rotation ([-1.2,0,0.6] loop). Fixed: `idle` is now a
   STATIC hold (neutral keys only, zero motion). The sole living detail is the
   fx-controller gem micro-pulse (scale 1.03, no positional motion). Motion now
   happens only on LMB (attack), RMB-charge (power) and equip.
2. Third-person diagonal lay = display z-rotation 55, inherited from vanilla
   `handheld` (correct for diagonal-painted sprites, wrong for an upright 3D
   model). Fixed: third-person rotations to [0,-90,12]/[0,90,-12] so the
   handle stands vertical with the head up and the decorated +Z face outward.
   First-person angle [0,-90,25] kept (vanilla axe feel, no complaint about it).
Verified: load-test harness green on new assets, `./gradlew build` green,
resources re-validated. Needs user's eyes in-game.

## Equip-spam fix (2026-09-03, first-person rocking between two tilted frames)
Symptom: the axe rocked left-right every frame in first person (amplitude
matched equip's -18deg start, not idle — idle was already static).
Root cause: `setCustomAnimations` runs for EVERY render context each frame.
The hotbar (GUI perspective) draws the same ItemStack objects as the hand, and
the old `else` branch reset `lastFirstPersonStack` to EMPTY on every GUI
render; the following first-person render then saw EMPTY != stack and
retriggered EQUIP — every single frame, so the 0.4s flourish never settled.
Fix: GUI renders never touch equip state (branch removed); re-selecting the
identical stack is detected via the hotbar slot index instead. Result: the
weapon is fully static in hand; motion only on LMB (attack), RMB-charge
(power) and genuine equip. `./gradlew build` green.

## Known compromises
- Per-keyframe easing strings omitted (Bedrock 1.8.0 compat); easing is baked
  through keyframe timing (slow anticipation -> explosive strike).
- No emissive texture layer (project has no item emissive pipeline); ruby glow
  is faked with scale-flash keyframes + particles, per spec fallback.
- Remote players' air-swings don't animate the model (their entity hits do via
  server trigger); local prediction covers the wielder fully.
- First/third-person display numbers are reasoned from the trident precedent +
  the previous axe tuning, not eyeballed in-game yet — expect one tuning pass.
