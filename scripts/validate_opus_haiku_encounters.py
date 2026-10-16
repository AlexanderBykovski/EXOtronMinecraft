#!/usr/bin/env python3
"""Validate bounded Haiku-4/5 additions in active Opus combat structures."""

from __future__ import annotations

from pathlib import Path

from nbtlib import load


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/main/resources/data/opusvsexe/structures"
PACK = ROOT / "pack/data/opusvsexe/structures"
EXPECTED = {
    "coddy_workshop": (("haiku_4", (30, 1, 17), 5, 1),),
    "trial_grounds": (("haiku_4", (34, 1, 10), 5, 1),),
    "abandoned_city": (("haiku_4", (90, 1, 30), 5, 1), ("haiku_5", (56, 1, 23), 9, 2)),
    "haiku_citadel": (("haiku_5", (35, 3, 77), 9, 2),),
}


def cells(path: Path) -> dict[tuple[int, int, int], tuple[str, dict | None]]:
    root = load(path)
    palette = root["palette"]
    out = {}
    for entry in root["blocks"]:
        state = palette[int(entry["state"])]
        out[tuple(map(int, entry["pos"]))] = (str(state["Name"]), dict(entry["nbt"]) if "nbt" in entry else None)
    return out


def run() -> None:
    if not __debug__:
        raise RuntimeError("this validator must run without Python -O")
    for structure, encounters in EXPECTED.items():
        source = SRC / structure / "main.nbt"
        mirror = PACK / structure / "main.nbt"
        assert source.read_bytes() == mirror.read_bytes(), f"template mirror differs: {structure}"
        template = cells(source)
        for entity, pos, height, radius in encounters:
            name, nbt = template.get(pos, ("", None))
            assert name == "opusvsexe:dormant_spawner" and nbt, f"missing {entity} marker in {structure} at {pos}"
            assert str(nbt.get("entity_id", "")) == f"opusvsexe:{entity}", f"wrong entity at {structure} {pos}"
            assert int(nbt.get("max_nearby", 0)) == 1 and int(nbt.get("spawn_radius", -1)) == 0, \
                f"{structure} {entity} must be a single fixed-center encounter"
            x, y, z = pos
            for yy in range(y + 1, y + height + 1):
                for zz in range(z - radius, z + radius + 1):
                    for xx in range(x - radius, x + radius + 1):
                        assert template.get((xx, yy, zz), ("minecraft:void_air", None))[0] == "minecraft:air", \
                            f"{structure} {entity} lacks authored clearance at {(xx, yy, zz)}"

    fortress = cells(SRC / "frontier_fortress/main.nbt")
    existing = [str(nbt.get("entity_id", "")) for name, nbt in fortress.values()
                if name == "opusvsexe:dormant_spawner" and nbt]
    assert "opusvsexe:haiku_4" in existing and "opusvsexe:haiku_5" in existing, \
        "Frontier Fortress must retain its existing Haiku-4/5 progression"
    print("Opus Haiku encounter validation passed: 5 bounded additions; Frontier Fortress already retains Haiku-4/5.")


if __name__ == "__main__":
    run()
