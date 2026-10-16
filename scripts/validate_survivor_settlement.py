#!/usr/bin/env python3
"""Resource-level contract for the no-hostile KSV-01 settlement."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from nbtlib import load


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/main/resources/data/opusvsexe"
PACK = ROOT / "pack/data/opusvsexe"
NBT = SRC / "structures/survivor_settlement/main.nbt"
SIZE = (121, 43, 101)
GROUND_Y = 16
ORIGIN = (60, 0, 50)
THEMES = {"house", "food", "medical", "workshop", "warehouse", "security", "shelter", "hidden"}
FORBIDDEN_BLOCKS = {
    "opusvsexe:dormant_spawner", "opusvsexe:trial_trigger",
    "minecraft:structure_block", "minecraft:jigsaw",
}
SPAWN_CATEGORIES = {
    "monster", "creature", "ambient", "axolotls", "underground_water_creature",
    "water_creature", "water_ambient", "misc",
}


def local(x: int, y: int, z: int) -> tuple[int, int, int]:
    return x + ORIGIN[0], y, z + ORIGIN[2]


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def run() -> None:
    if not __debug__:
        raise RuntimeError("this validator must run without Python -O")
    mirror = PACK / "structures/survivor_settlement/main.nbt"
    assert NBT.read_bytes() == mirror.read_bytes(), "KSV template source/pack mirrors differ"
    root = load(NBT)
    assert tuple(map(int, root["size"])) == SIZE, f"wrong KSV size: {list(root['size'])}"
    assert int(root["DataVersion"]) == 3465, "KSV must target the 1.20.1 data version"

    palette = root["palette"]
    cells: dict[tuple[int, int, int], tuple[str, dict[str, str], dict | None]] = {}
    loot_tables: list[str] = []
    for entry in root["blocks"]:
        block = palette[int(entry["state"])]
        name = str(block["Name"])
        properties = {str(key): str(value) for key, value in dict(block.get("Properties", {})).items()}
        nbt = dict(entry["nbt"]) if "nbt" in entry else None
        cells[tuple(map(int, entry["pos"]))] = (name, properties, nbt)
        if nbt and "LootTable" in nbt:
            assert str(nbt.get("id", "")) == "minecraft:chest", "KSV loot must live in ordinary chests"
            loot_tables.append(str(nbt["LootTable"]))

    names = Counter(name for name, _, _ in cells.values())
    assert not FORBIDDEN_BLOCKS.intersection(names), "settlement contains a hostile/marker block"
    assert len(loot_tables) == 35, f"expected 35 settlement containers, got {len(loot_tables)}"
    actual_themes = {table.removeprefix("opusvsexe:chests/survivors_village_") for table in loot_tables}
    assert THEMES <= actual_themes, f"missing settlement loot themes: {sorted(THEMES - actual_themes)}"
    for theme in THEMES:
        relative = f"loot_tables/chests/survivors_village_{theme}.json"
        assert (SRC / relative).read_bytes() == (PACK / relative).read_bytes(), f"loot mirror differs: {theme}"
        read_json(SRC / relative)

    entities = list(root["entities"])
    assert len(entities) == 20, f"expected 20 residents, got {len(entities)}"
    for entity in entities:
        nbt = entity["nbt"]
        assert str(nbt.get("id", "")) == "opusvsexe:survivor", "only Survivor may be serialized in KSV"
        assert int(nbt.get("PersistenceRequired", 0)) == 1, "each resident must persist"
        x, y, z = map(int, entity["blockPos"])
        assert cells.get((x, y - 1, z), ("minecraft:air", {}, None))[0] != "minecraft:air", \
            f"resident at {(x, y, z)} has no floor"
        assert cells.get((x, y, z), ("minecraft:air", {}, None))[0] == "minecraft:air", \
            f"resident at {(x, y, z)} intersects furniture"
        assert cells.get((x, y + 1, z), ("minecraft:air", {}, None))[0] == "minecraft:air", \
            f"resident at {(x, y, z)} lacks headroom"

    def clear(label: str, x: int, y: int, z: int) -> None:
        for dy in (0, 1):
            name = cells.get(local(x, y + dy, z), ("minecraft:air", {}, None))[0]
            assert name == "minecraft:air", f"{label} route is blocked at {(x, y + dy, z)} by {name}"

    for checkpoint in (
        ("main gate", 0, 17, 47), ("square", 0, 17, 10), ("command", 0, 17, -22),
        ("clinic", 24, 17, -9), ("market", -18, 17, 0), ("workshop", 23, 17, 17),
        ("service gate", 0, 17, -44), ("shelter", 0, 4, 0), ("escape exit", -59, 17, 3),
    ):
        clear(*checkpoint)

    # Sentinel blocks prove the complete mandatory programme exists, without
    # trusting a free-form building name in a binary template.
    sentinels = {
        "central fire": (0, 17, 0, "minecraft:campfire"),
        "radio mast": (0, 40, -29, "minecraft:redstone_lamp"),
        "clinic ward": (20, 17, -5, "minecraft:white_bed"),
        "market": (-40, 21, -9, "minecraft:green_wool"),
        "greenhouse": (-35, 22, -41, "minecraft:glass"),
        "generator": (36, 17, 34, "minecraft:iron_block"),
        "quarantine": (21, 17, -45, "minecraft:white_bed"),
        "shelter": (-17, 3, 12, "minecraft:chest"),
        "escape hatch": (-59, 19, 3, "minecraft:iron_trapdoor"),
    }
    for label, (x, y, z, expected) in sentinels.items():
        actual = cells.get(local(x, y, z), ("minecraft:air", {}, None))[0]
        assert actual == expected, f"missing {label}: expected {expected}, got {actual}"

    structure = read_json(SRC / "worldgen/structure/survivor_settlement.json")
    structure_set = read_json(SRC / "worldgen/structure_set/survivor_settlement.json")
    assert structure["type"] == "opusvsexe:survivors_village"
    assert set(structure["spawn_overrides"]) == SPAWN_CATEGORIES
    assert all(value == {"bounding_box": "piece", "spawns": []}
               for value in structure["spawn_overrides"].values()), "natural mobs must be disabled inside KSV pieces"
    assert structure_set["placement"] == {
        "type": "minecraft:random_spread", "spacing": 32, "separation": 8,
        "salt": 155746213, "spread_type": "triangular",
    }
    for relative in ("worldgen/structure/survivor_settlement.json",
                     "worldgen/structure_set/survivor_settlement.json"):
        assert (SRC / relative).read_bytes() == (PACK / relative).read_bytes(), f"worldgen mirror differs: {relative}"

    print("KSV-01 resource validation passed: "
          f"{len(cells)} blocks, {len(names)} states, {len(loot_tables)} containers, {len(entities)} survivors, 0 hostile markers.")


if __name__ == "__main__":
    run()
