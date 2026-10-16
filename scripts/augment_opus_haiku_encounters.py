#!/usr/bin/env python3
"""Add bounded Haiku-4/5 encounters to authored Opus combat templates.

The selected locations are recorded in
``concepts/opus_haiku_4_5_encounters.md``.  This script is intentionally
idempotent: re-running it updates the same marker rather than duplicating a
spawner, then copies the exact source NBT bytes into the bundled pack mirror.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile

from nbtlib import Compound, File, Int, List, String, load


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/main/resources/data/opusvsexe/structures"
PACK = ROOT / "pack/data/opusvsexe/structures"
SPAWNER_ID = "opusvsexe:dormant_spawner"


@dataclass(frozen=True)
class Encounter:
    entity: str
    pos: tuple[int, int, int]
    note: str
    replace: bool = False


ENCOUNTERS: dict[str, tuple[Encounter, ...]] = {
    "coddy_workshop": (
        Encounter("haiku_4", (30, 1, 17), "open salvage court beside Coddy/armory route"),
    ),
    "trial_grounds": (
        Encounter("haiku_4", (34, 1, 10), "wide reward-vault approach"),
    ),
    "abandoned_city": (
        Encounter("haiku_4", (90, 1, 30), "refinery court beside refinery cache"),
        Encounter("haiku_5", (56, 1, 23), "nine-block treasury court"),
    ),
    "haiku_citadel": (
        # This route already had several Haiku-4 guardians. Upgrading exactly
        # one high-clearance endpoint creates the requested titan without an
        # additional overlapping encounter marker.
        Encounter("haiku_5", (35, 3, 77), "post-core route, replaces one existing Haiku-4", replace=True),
    ),
}


def spawner_state_index(root: File) -> int:
    for index, state in enumerate(root["palette"]):
        if str(state["Name"]) == SPAWNER_ID and dict(state.get("Properties", {})).get("active") == "true":
            return index
    root["palette"].append(Compound({
        "Name": String(SPAWNER_ID),
        "Properties": Compound({"active": String("true")}),
    }))
    return len(root["palette"]) - 1


def spawn_nbt(entity: str) -> Compound:
    return Compound({
        "id": String(SPAWNER_ID),
        "entity_id": String(f"opusvsexe:{entity}"),
        "max_nearby": Int(1),
        "spawn_radius": Int(0),
    })


def update_template(structure: str, encounters: tuple[Encounter, ...]) -> None:
    source = SRC / structure / "main.nbt"
    mirror = PACK / structure / "main.nbt"
    assert source.exists() and mirror.exists(), f"missing template mirror for {structure}"
    assert source.read_bytes() == mirror.read_bytes(), f"source/pack template drift before {structure} edit"
    root = load(source)
    state_index = spawner_state_index(root)
    by_pos = {tuple(map(int, entry["pos"])): entry for entry in root["blocks"]}

    for encounter in encounters:
        entry = by_pos.get(encounter.pos)
        if entry is None:
            entry = Compound({
                "pos": List[Int]([Int(value) for value in encounter.pos]),
                "state": Int(state_index),
                "nbt": spawn_nbt(encounter.entity),
            })
            root["blocks"].append(entry)
            by_pos[encounter.pos] = entry
        else:
            current_state = root["palette"][int(entry["state"])]
            current_name = str(current_state["Name"])
            if current_name != SPAWNER_ID:
                if "nbt" in entry:
                    raise ValueError(f"{structure} target {encounter.pos} is occupied by {current_name}")
            elif not encounter.replace and str(entry.get("nbt", {}).get("entity_id", "")) != f"opusvsexe:{encounter.entity}":
                raise ValueError(f"{structure} target {encounter.pos} unexpectedly contains another encounter")
            entry["state"] = Int(state_index)
            entry["nbt"] = spawn_nbt(encounter.entity)

    root.save(source, gzipped=True)
    copyfile(source, mirror)


def main() -> None:
    for structure, encounters in ENCOUNTERS.items():
        update_template(structure, encounters)
        labels = ", ".join(f"{entry.entity}@{entry.pos}" for entry in encounters)
        print(f"{structure}: {labels}")


if __name__ == "__main__":
    main()
