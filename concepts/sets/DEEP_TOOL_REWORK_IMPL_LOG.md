# Deep Tool (non-katana) Rework — implementation log

Spec: `concepts/sets/DEEP_NON_KATANA_TOOLS_REWORK_PROMPTS_RU.md`
Reference art: `concepts/sets/{opus_arsenal,fire_tools,parthenon_tools,dark_forest_tools}_vanilla.png`

## Status: DONE (all 20 whitelist tools regenerated, validated)

## Scope
Redesigned ONLY the 20 whitelisted non-katana tools across 4 families:
Opus, Fire, Parthenon, Dark Forest (5 tools each: sword/pickaxe/axe/shovel/hoe,
plus opus_warhammer and parthenon_axe=Labrys).

Katanas are FROZEN. Both my generator and edits contain zero katana logic. The
katana files showing "M" in git were pre-existing uncommitted changes from an
earlier session (mtime ~10:58 vs my generated tools ~21:20) — not touched here.

## Pipeline decision
- Source of truth: `scripts/generate_tool_sets.py` (new, replaces the old thin
  `generate_tools_deep.py` approach). It re-authors chunky, concept-faithful
  silhouettes and emits PNG + png.mcmeta + item models + QA sheets.
- It writes ONLY the 20 whitelist items. No Java code, no renderers, no
  registry IDs, no recipes, no creative tabs were changed.

## Design notes
- Resolution: 32x32 master per frame. Item models reference it directly
  (kept `minecraft:item/handheld` so the existing model/display transforms and
  the vanilla parent continue to work — no architecture change). Silhouettes
  were authored to remain readable when halved (16x16).
- Handles are thin (3px) and the HEAD is the dominant mass, matching the
  concept art's proportion (unlike the previous thin-spike output).
- Per-family material logic:
  - Opus: graphite body + cobalt-socket + cyan crystal + blue seams.
  - Fire: charcoal body + bright jagged orange magma vein (deep red shadow →
    orange → sulfur hot), lighter grey working edges, brown handle.
  - Parthenon: ivory body + bronze/gold centre + ruby crystal + Greek-axis
    gold accents (Labrys is the intentionally symmetric double blade).
  - Dark Forest: dark iron + teal/blue-green moss vein + violet socket.
- Emissive animation: ONLY the acc/emissive pixels change per frame. Verified
  programmatically — geometry/alpha mask is identical across frames; only
  6-13 emissive pixels modulate. Outline, handle, material never move.

## Frame counts / frametime (interpolate:false everywhere)
fire=3 (fast ember); others=5.
- opus_warhammer 4, opus_pickaxe 3, opus_axe 3, opus_shovel 4, opus_hoe 3.
- fire_sword 5, fire_pickaxe 4, fire_axe 4, fire_shovel 3, fire_hoe 3.
- parthenon_sword 3, parthenon_pickaxe 3, parthenon_axe 4, parthenon_shovel 3,
  parthenon_hoe 3.
- dark_forest_sword 4, dark_forest_pickaxe 4, dark_forest_axe 3,
  dark_forest_shovel 4, dark_forest_hoe 3.

## Item models
Vanilla handheld for all; volumetric transform preserved ONLY for the two
already-3D tools (opus_warhammer, parthenon_axe/Labrys) so they keep their
existing good read in first/third person.

## Verification
- `scripts/validate_resources.py` passes:
  `Validated 1141 JSON, 531 PNG, 62 OGG and 45 Gecko model/animation pairs.`
- All 20 PNGs alpha-clean (only 0/255 — no gray translucent halo), correct
  frame heights (n*32), correct mcmeta, valid model JSON.
- QA sheets regenerated: `docs/assets/concepts/deep-tool-rework-{sheet,dark,light}-2026-09-02.png`.
- Backup of the pre-change whitelist assets: `build/tool_backup/`.

## Build
Java/JDK is not installed on this host, so `./gradlew build` cannot run here.
No Java sources were modified, so the build is unaffected by these resource
changes. Run locally:
`JAVA_HOME=/path/to/jdk17 ./gradlew build`

## Changed files (whitelist only)
- 20x `src/main/resources/assets/opusvsexe/textures/item/<item>.png`
- 20x `src/main/resources/assets/opusvsexe/textures/item/<item>.png.mcmeta`
- 20x `src/main/resources/assets/opusvsexe/models/item/<item>.json`
- QA sheets under `docs/assets/concepts/`
