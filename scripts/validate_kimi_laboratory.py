#!/usr/bin/env python3
"""Resource-level contract checks for the generated K-17 structure."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from nbtlib import load


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/main/resources/data/opusvsexe"
PACK = ROOT / "pack/data/opusvsexe"
NBT = SRC / "structures/kimi_laboratory/main.nbt"
SIZE = (117, 79, 101)
ORIGIN = (58, 68, 50)
PASSABLE = {"minecraft:air", "minecraft:water", "minecraft:ladder"}
MARKERS = {"minecraft:structure_block", "minecraft:jigsaw"}
ALLOWED_BE_IDS = {
    "minecraft:chest",
    "opusvsexe:dormant_spawner",
    "opusvsexe:reward_vault",
    "opusvsexe:memory_console",
    "opusvsexe:sequence_keypad",
}


def local(x: int, y: int, z: int) -> tuple[int, int, int]:
    return x + ORIGIN[0], y + ORIGIN[1], z + ORIGIN[2]


def json_file(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def run() -> None:
    if not __debug__:
        raise RuntimeError("this validator must run without Python -O")
    mirror = PACK / "structures/kimi_laboratory/main.nbt"
    assert NBT.read_bytes() == mirror.read_bytes(), "NBT pack mirror differs from source resource"
    root = load(NBT)
    assert tuple(map(int, root["size"])) == SIZE, f"wrong K-17 size: {list(root['size'])}"
    assert int(root["DataVersion"]) == 3465, "template must remain 1.20.1 data version"
    assert not root["entities"], "K-17 must use safe static encounters, not serialized entities"

    palette = root["palette"]
    cells: dict[tuple[int, int, int], tuple[str, dict[str, str], dict | None]] = {}
    loot_tables: list[str] = []
    block_entities: list[tuple[str, dict]] = []
    for entry in root["blocks"]:
        state = palette[int(entry["state"])]
        name = str(state["Name"])
        properties = {str(k): str(v) for k, v in dict(state.get("Properties", {})).items()}
        position = tuple(map(int, entry["pos"]))
        nbt = dict(entry["nbt"]) if "nbt" in entry else None
        cells[position] = (name, properties, nbt)
        if nbt:
            identifier = str(nbt.get("id", ""))
            assert identifier in ALLOWED_BE_IDS, f"unsupported K-17 block entity: {identifier}"
            block_entities.append((identifier, nbt))
            if "LootTable" in nbt:
                loot_tables.append(str(nbt["LootTable"]))

    names = Counter(name for name, _, _ in cells.values())
    assert not MARKERS.intersection(names), "template contains a visible structure/jigsaw marker"
    assert len(loot_tables) == 32, f"expected 32 containers, found {len(loot_tables)}"
    assert names["opusvsexe:dormant_spawner"] == 10, "K-17 must contain exactly 10 encounter markers"
    assert names["opusvsexe:sequence_keypad"] == 4, "memory cascade must contain 4 keypads"
    assert names["minecraft:ladder"] >= 80, "both safety shafts require continuous ladder runs"
    encounter_nbt = [nbt for identifier, nbt in block_entities if identifier == "opusvsexe:dormant_spawner"]
    encounter_ids = [str(nbt.get("entity_id", "")) for nbt in encounter_nbt]
    assert encounter_ids.count("opusvsexe:haiku_4") == 1, "K-17 needs one Haiku-4 encounter"
    assert encounter_ids.count("opusvsexe:haiku_5") == 1, "K-17 needs one Haiku-5 encounter"
    for nbt in encounter_nbt:
        if str(nbt.get("entity_id", "")) in {"opusvsexe:haiku_4", "opusvsexe:haiku_5"}:
            assert int(nbt.get("max_nearby", 0)) == 1 and int(nbt.get("spawn_radius", -1)) == 0, \
                "elite K-17 encounters must be single fixed-center spawns"

    source = (ROOT / "src/main/java/com/opus/registry/ModBlocks.java").read_text(encoding="utf-8")
    registered = {f"opusvsexe:{identifier}" for identifier in __import__("re").findall(r'register\("([a-z0-9_]+)"', source)}
    used_custom = {name for name in names if name.startswith("opusvsexe:")}
    assert used_custom <= registered, f"unregistered custom blocks: {sorted(used_custom - registered)}"

    for table in loot_tables:
        namespace, path = table.split(":", 1)
        assert namespace == "opusvsexe" and path.startswith("chests/kimi_lab/"), f"bad loot reference: {table}"
        source_path = SRC / "loot_tables" / f"{path}.json"
        pack_path = PACK / "loot_tables" / f"{path}.json"
        assert source_path.exists(), f"missing loot table: {source_path}"
        assert source_path.read_bytes() == pack_path.read_bytes(), f"loot mirror differs: {path}"
        json_file(source_path)

    keypads = sorted((str(nbt["puzzle_id"]), int(nbt["order"]))
                     for identifier, nbt in block_entities if identifier == "opusvsexe:sequence_keypad")
    assert keypads == [("k17_memory_cascade", 0), ("k17_memory_cascade", 1),
                       ("k17_memory_cascade", 2), ("k17_memory_cascade", 3)]
    locked_vaults = [(state, nbt) for state, _, nbt in cells.values()
                     if state == "opusvsexe:reward_vault" and nbt and nbt.get("LootTable")]
    assert sum(1 for state, nbt in locked_vaults if state == "opusvsexe:reward_vault") >= 3
    false_vaults = [
        nbt for name, properties, nbt in cells.values()
        if name == "opusvsexe:reward_vault" and properties.get("open") == "false"
    ]
    assert [str(nbt["LootTable"]) for nbt in false_vaults] == ["opusvsexe:chests/kimi_lab/memory_vault"], \
        "only the nearby memory-puzzle vault may start locked"

    def assert_clear(label: str, x: int, y: int, z: int) -> None:
        for dy in (0, 1):
            state = cells.get(local(x, y + dy, z), ("minecraft:void_air", {}, None))[0]
            assert state in PASSABLE, f"{label} lacks two-block clearance at {(x, y + dy, z)}: {state}"

    # Semi-automated primary-route checkpoints. Full playthrough remains a manual dev-client check.
    for point in (
        ("surface entrance", 0, 1, 0),
        ("security exit", 23, -13, 4),
        ("decontamination", 28, -13, 0),
        ("L1 intersection", 35, -13, 5),
        ("L2 main corridor", 0, -26, 0),
        ("L3 service route", -4, -38, 0),
        ("L4 shaft landing", -12, -55, -4),
        ("deep service descent", -11, -62, -16),
        ("archive threshold", -17, -67, -15),
        ("escape outlet", 53, 1, 42),
    ):
        assert_clear(*point)

    structure = json_file(SRC / "worldgen/structure/kimi_laboratory.json")
    structure_set = json_file(SRC / "worldgen/structure_set/kimi_laboratory.json")
    biomes = json_file(SRC / "tags/worldgen/biome/has_kimi_laboratory.json")
    assert structure["type"] == "opusvsexe:deep_neurophysics_lab"
    assert structure_set["placement"] == {
        "type": "minecraft:random_spread", "spacing": 72, "separation": 24,
        "salt": 1625389709, "spread_type": "triangular",
    }
    assert "#minecraft:is_overworld" not in biomes["values"] and len(biomes["values"]) >= 10
    for relative in (
        "worldgen/structure/kimi_laboratory.json",
        "worldgen/structure_set/kimi_laboratory.json",
        "tags/worldgen/biome/has_kimi_laboratory.json",
    ):
        assert (SRC / relative).read_bytes() == (PACK / relative).read_bytes(), f"pack mirror differs: {relative}"
    assert not (SRC / "worldgen/template_pool/kimi_laboratory/start.json").exists(), "legacy jigsaw pool still exists"
    # Legacy jigsaw pieces serialized in worlds before K-17 reference this processor.
    # New worldgen does not reference it, but retaining it keeps those saves loadable.
    assert (SRC / "worldgen/processor_list/lab_degradation.json").read_bytes() == \
           (PACK / "worldgen/processor_list/lab_degradation.json").read_bytes(), "legacy processor mirror differs"

    print("K-17 resource validation passed: "
          f"{len(cells)} blocks, {len(names)} states, {len(loot_tables)} containers, "
          f"{names['opusvsexe:dormant_spawner']} encounters, {len(keypads)} keypads.")


if __name__ == "__main__":
    run()
