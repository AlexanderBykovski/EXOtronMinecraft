#!/usr/bin/env python3
"""Generates ProjectE EMC data for the OpusVsExe mod.

Strategy (ProjectE auto-maps vanilla shaped/shapeless recipes at runtime,
so those need nothing from us):
  * `values.before` seeds: every opusvsexe item/block with NO crafting recipe
    (ores, mob drops, farmables, trophies, shrine decor ...) gets a hand-picked
    value anchored to ProjectE's canonical scale (iron 256, gold 2048,
    diamond 8192).
  * `conversion` entries: outputs of our custom recipe types
    (`opusvsexe:assembly` 5x5, `opusvsexe:parthenon_forging`), which ProjectE
    cannot derive on its own. Values resolve from ingredients at runtime.
  * Spawn eggs, lore-only keys, music discs and unobtainable blocks are left
    without explicit EMC values, like their vanilla counterparts.

Run:  python3 scripts/generate_projecte_emc.py   (from the project root)
"""
import glob
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "src", "main", "resources", "data")
LANG = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe", "lang", "en_us.json")

CUSTOM_TYPES = ("opusvsexe:assembly", "opusvsexe:parthenon_forging")

# ---------------------------------------------------------------- seeds ----
# Hand-picked EMC for items with no crafting recipe of their own.
SEEDS = {
    # opus chain ground truth (raw derives 1:1 from ore via its recipe;
    # stabilized/resonant derive 1:1 through theirs)
    "opusvsexe:opus_ore": 256,
    "opusvsexe:opus_fragment": 128,
    # farmable foods / drops
    "opusvsexe:paradise_fruit": 32,
    "opusvsexe:cinder_bean": 32,
    "opusvsexe:fire_bean": 32,
    "opusvsexe:sunfeather": 64,
    "opusvsexe:cloud_fleece": 64,
    "opusvsexe:shade_silk": 128,
    "opusvsexe:moonwing_membrane": 256,
    "opusvsexe:ember_essence": 128,
    "opusvsexe:fire_essence": 128,
    # rare mob / boss drops
    "opusvsexe:moonflower_heart": 512,
    "opusvsexe:rootbound_eye": 512,
    "opusvsexe:seraphic_pinions": 512,
    "opusvsexe:ruby_halo_shard": 1024,
    "opusvsexe:ai_tear": 1024,
    "opusvsexe:blazing_trident": 12288,
    # collectible lore fragments (also a compass ingredient)
    **{f"opusvsexe:memory_fragment_{i}": 128 for i in range(1, 16)},
    # wood sets (vanilla log scale)
    "opusvsexe:cinder_log": 32,
    "opusvsexe:ember_log": 32,
    "opusvsexe:gloomwood_log": 32,
    "opusvsexe:paradise_log": 32,
    "opusvsexe:ember_sapling": 32,
    "opusvsexe:gloomwood_sapling": 32,
    "opusvsexe:paradise_sapling": 32,
    "opusvsexe:cinder_leaves": 1,
    "opusvsexe:ember_leaves": 1,
    "opusvsexe:gloomwood_leaves": 1,
    "opusvsexe:paradise_leaves": 1,
    # soils and grasses
    "opusvsexe:fire_soil": 1,
    "opusvsexe:cinder_soil": 1,
    "opusvsexe:moonlit_soil": 1,
    "opusvsexe:paradise_soil": 1,
    "opusvsexe:moonlit_grass": 1,
    "opusvsexe:paradise_grass": 1,
    # stone / decor
    "opusvsexe:ash_block": 1,
    "opusvsexe:cinder_ash": 1,
    "opusvsexe:cinder_crust": 4,
    "opusvsexe:magma_crust": 4,
    "opusvsexe:crimson_ice": 16,
    "opusvsexe:celestial_stone": 4,
    "opusvsexe:fountain_stone": 16,
    "opusvsexe:gilded_marble": 64,
    "opusvsexe:parthenon_marble": 64,
    "opusvsexe:cinder_seal": 16,
    # plants
    "opusvsexe:moonflower": 16,
    "opusvsexe:thorn_fern": 8,
    "opusvsexe:cinder_vine": 8,
    "opusvsexe:fire_vine": 8,
    # shrine decor
    "opusvsexe:angel_dais": 256,
    "opusvsexe:rootbound_pedestal": 256,
    "opusvsexe:seraphic_reliquary": 512,
    "opusvsexe:moon_fountain_core": 1024,
    # trophies: common mobs
    **{t: 256 for t in (
        "opusvsexe:trophy_sunfinch", "opusvsexe:trophy_cloud_grazer",
        "opusvsexe:trophy_shade_spiderling", "opusvsexe:trophy_moonwing_bat",
        "opusvsexe:trophy_ember_slime", "opusvsexe:trophy_fire_slime",
        "opusvsexe:trophy_survivor", "opusvsexe:trophy_samurai")},
    # trophies: elites and lesser haikus
    **{t: 1024 for t in (
        "opusvsexe:trophy_black_ninja", "opusvsexe:trophy_haiku_1_5",
        "opusvsexe:trophy_haiku_2", "opusvsexe:trophy_haiku_3",
        "opusvsexe:trophy_haiku_4", "opusvsexe:trophy_haiku_drone",
        "opusvsexe:trophy_haiku_drone_plus")},
    # trophies: elite guardians
    **{t: 2048 for t in (
        "opusvsexe:trophy_gloom_broodmother", "opusvsexe:trophy_lava_golem",
        "opusvsexe:trophy_obsidian_golem", "opusvsexe:trophy_paradise_wyvern")},
    # trophies: the seven great bosses + diablo
    **{t: 8192 for t in (
        "opusvsexe:trophy_haiku_5", "opusvsexe:trophy_haiku_omega",
        "opusvsexe:trophy_flame_demon",
        "opusvsexe:trophy_angel_boy", "opusvsexe:trophy_mossbound_enderman",
        "opusvsexe:trophy_young_samurai", "opusvsexe:trophy_diablo")},
}

# Items that stay EMC-free (mirrors vanilla: eggs, discs, unobtainables).
IGNORE_EXPLICIT = {
    "opusvsexe:doom_eternal_disc",
    "opusvsexe:cinder_portal",
    "opusvsexe:katana_lore",
    "opusvsexe:hammer_lore",
    "opusvsexe:laser_gun_lore",
    "opusvsexe:light_laser_gun_lore",
    "opusvsexe:heavy_laser_gun_lore",
    "opusvsexe:sky_laser_gun_lore",
    "opusvsexe:radio_lore",
}


def universe():
    lang = json.load(open(LANG, encoding="utf-8"))
    ids = set()
    for key in lang:
        for prefix in ("item.opusvsexe.", "block.opusvsexe."):
            if key.startswith(prefix):
                rest = key[len(prefix):]
                if "." not in rest:
                    ids.add("opusvsexe:" + rest)
    return ids


def load_recipes():
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, "opusvsexe", "recipes", "*.json"))):
        with open(path, encoding="utf-8") as handle:
            out.append((os.path.basename(path), json.load(handle)))
    return out


def ingredient_id(entry):
    if "item" in entry:
        return entry["item"]
    if "tag" in entry:
        return "#" + entry["tag"]
    raise ValueError(f"unsupported ingredient {entry}")


def conversion_for(recipe):
    """Ingredient multiset + output for shaped custom-type recipes."""
    counts: Counter = Counter()
    for row in recipe["pattern"]:
        for symbol in row:
            if symbol == " ":
                continue
            item_id = ingredient_id(recipe["key"][symbol])
            if recipe.get("type") == "opusvsexe:parthenon_forging" \
                    and item_id == "opusvsexe:ruby_halo_shard":
                continue
            counts[item_id] += 1
    result = recipe["result"]
    entry = {"ingredients": dict(counts), "output": result.get("item") or result.get("id")}
    if result.get("count", 1) != 1:
        entry["count"] = result["count"]
    return entry


def main():
    ids = universe()
    recipes = load_recipes()
    vanilla_outputs = set()
    conversions = []
    for name, recipe in recipes:
        rtype = recipe.get("type", "?")
        result = recipe.get("result", {})
        rid = result.get("item") or result.get("id")
        if rtype in ("minecraft:crafting_shaped", "minecraft:crafting_shapeless"):
            if rid and rid.startswith("opusvsexe:"):
                vanilla_outputs.add(rid)
        elif rtype in CUSTOM_TYPES:
            conversions.append(conversion_for(recipe))
    custom_outputs = set()
    for name, recipe in recipes:
        if recipe.get("type") in CUSTOM_TYPES:
            result = recipe.get("result", {})
            rid = result.get("item") or result.get("id")
            if rid and rid.startswith("opusvsexe:"):
                custom_outputs.add(rid)

    # every id must be covered: vanilla recipe, conversion, seed, or ignore
    ignore = {i for i in ids if i.endswith("_spawn_egg")} | IGNORE_EXPLICIT
    uncovered = sorted(i for i in ids
                       if i not in vanilla_outputs and i not in custom_outputs
                       and i not in SEEDS and i not in ignore)
    if uncovered:
        print("UNCOVERED (add seeds or ignore):")
        for item_id in uncovered:
            print("  " + item_id)
        raise SystemExit(1)

    before = {item_id: SEEDS[item_id] for item_id in sorted(SEEDS) if item_id in ids}
    missing_seeds = sorted(set(SEEDS) - ids)
    if missing_seeds:
        print("WARNING: seeds for unknown ids:", missing_seeds)

    doc = {
        "comment": "OpusVsExe EMC: base values for uncraftables + conversions for "
                   "assembly/parthenon_forging recipes. Generated by scripts/generate_projecte_emc.py",
        "values": {
            "before": before,
            "conversion": conversions,
        },
    }
    out_path = os.path.join(DATA, "opusvsexe", "pe_custom_conversions", "generated.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(doc, handle, indent=2)
        handle.write("\n")

    print(f"universe={len(ids)} vanilla={len(vanilla_outputs)} "
          f"custom={len(custom_outputs)} seeds={len(before)} ignore={len(ignore)}")
    print(f"wrote {os.path.relpath(out_path, ROOT)}")


if __name__ == "__main__":
    main()
