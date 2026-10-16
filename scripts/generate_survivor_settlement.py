#!/usr/bin/env python3
"""Author the deterministic, inhabited Survivors' Village (KSV-01).

The layout and every fixed coordinate live in
``concepts/survivors_village_layout.md``.  Keep this generator as the source
of truth; the compressed NBT files it emits are build artefacts mirrored into
the standalone pack.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile

from nbtlib import Byte, Compound, Double, File, Float, Int, List, String


WIDTH, HEIGHT, DEPTH = 121, 43, 101
ORIGIN_X, GROUND_Y, ORIGIN_Z = 60, 16, 50
DATA_VERSION = 3465
ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = (
    ROOT / "src/main/resources/data/opusvsexe/structures/survivor_settlement/main.nbt",
    ROOT / "pack/data/opusvsexe/structures/survivor_settlement/main.nbt",
)
LOOT_THEMES = ("house", "food", "medical", "workshop", "warehouse", "security", "shelter", "hidden")


@dataclass(frozen=True)
class State:
    name: str
    properties: tuple[tuple[str, str], ...] = ()


def state(name: str, **properties: str) -> State:
    return State(name, tuple(sorted(properties.items())))


AIR = State("minecraft:air")
DIRT = State("minecraft:dirt")
COARSE = State("minecraft:coarse_dirt")
GRAVEL = State("minecraft:gravel")
COBBLE = State("minecraft:cobblestone")
STONE = State("minecraft:stone_bricks")
CRACKED = State("minecraft:cracked_stone_bricks")
ANDESITE = State("minecraft:andesite")
MOSSY = State("minecraft:mossy_stone_bricks")
SPR_LOG = state("minecraft:spruce_log", axis="y")
OAK_LOG = state("minecraft:oak_log", axis="y")
STRIPPED = state("minecraft:stripped_spruce_log", axis="y")
PLANK = State("minecraft:spruce_planks")
DARK_PLANK = State("minecraft:dark_oak_planks")
OAK_PLANK = State("minecraft:oak_planks")
GRAY = State("minecraft:gray_concrete")
LIGHT_GRAY = State("minecraft:light_gray_concrete")
BROWN = State("minecraft:brown_terracotta")
COPPER = State("minecraft:weathered_cut_copper")
EXPOSED_COPPER = State("minecraft:exposed_cut_copper")
IRON = State("minecraft:iron_block")
BARS = State("minecraft:iron_bars")
CHAIN = State("minecraft:chain")
GLASS = State("minecraft:glass")
PANE = State("minecraft:glass_pane")
GREEN_WOOL = State("minecraft:green_wool")
GRAY_WOOL = State("minecraft:gray_wool")
WHITE_WOOL = State("minecraft:white_wool")
LAB_GRATE = State("opusvsexe:lab_floor_grate")
MEMORY_CABLE = state("opusvsexe:memory_cable", facing="north")
DATA_CONDUIT = state("opusvsexe:data_conduit", facing="north")
WATER = state("minecraft:water", level="0")


def slab(name: str = "minecraft:spruce_slab") -> State:
    return state(name, type="bottom", waterlogged="false")


def stair(name: str, facing: str) -> State:
    return state(name, facing=facing, half="bottom", shape="straight", waterlogged="false")


def fence(name: str = "minecraft:spruce_fence") -> State:
    return State(name)


def trapdoor(facing: str = "north") -> State:
    return state("minecraft:iron_trapdoor", facing=facing, half="bottom", open="false", powered="false", waterlogged="false")


def chest(facing: str = "north") -> State:
    return state("minecraft:chest", facing=facing, type="single", waterlogged="false")


def door(facing: str, half: str, hinge: str = "left") -> State:
    return state("minecraft:spruce_door", facing=facing, half=half, hinge=hinge, open="false", powered="false")


class Village:
    def __init__(self) -> None:
        self.blocks: dict[tuple[int, int, int], tuple[State, dict[str, object] | None]] = {}
        self.entities: list[dict[str, object]] = []

    @staticmethod
    def absolute(x: int, y: int, z: int) -> tuple[int, int, int]:
        return x + ORIGIN_X, y, z + ORIGIN_Z

    def put(self, x: int, y: int, z: int, block: State, nbt: dict[str, object] | None = None) -> None:
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT and 0 <= z < DEPTH):
            raise ValueError(f"KSV-01 coordinate outside template: {(x, y, z)}")
        self.blocks[(x, y, z)] = (block, nbt)

    def lput(self, x: int, y: int, z: int, block: State, nbt: dict[str, object] | None = None) -> None:
        self.put(*self.absolute(x, y, z), block, nbt)

    def fill(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, block: State) -> None:
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                for x in range(x0, x1 + 1):
                    self.put(x, y, z, block)

    def lfill(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, block: State) -> None:
        self.fill(*self.absolute(x0, y0, z0), *self.absolute(x1, y1, z1), block)

    def foundation(self, x0: int, z0: int, x1: int, z1: int, top: State = COBBLE) -> None:
        """A bounded support column for the accepted ±3 terrain envelope."""
        self.lfill(x0, 0, z0, x1, GROUND_Y - 1, z1, ANDESITE)
        self.lfill(x0, GROUND_Y, z0, x1, GROUND_Y, z1, top)

    def clear(self, x0: int, z0: int, x1: int, z1: int, top: int) -> None:
        self.lfill(x0, GROUND_Y + 1, z0, x1, top, z1, AIR)

    def road_rect(self, x0: int, z0: int, x1: int, z1: int) -> None:
        self.foundation(x0, z0, x1, z1, COARSE)
        self.clear(x0, z0, x1, z1, GROUND_Y + 4)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                selector = (x * 17 + z * 31) % 11
                material = GRAVEL if selector in (0, 1, 7) else (COBBLE if selector == 5 else COARSE)
                self.lput(x, GROUND_Y, z, material)
                if selector == 9:
                    self.lput(x, GROUND_Y, z, slab("minecraft:stone_slab"))

    def building(self, x0: int, z0: int, x1: int, z1: int, height: int, *,
                 wall: State = PLANK, floor: State = DARK_PLANK, roof: State = PLANK) -> None:
        roof_y = GROUND_Y + height
        self.foundation(x0, z0, x1, z1, floor)
        self.clear(x0, z0, x1, z1, min(HEIGHT - 1, roof_y + 3))
        for y in range(GROUND_Y + 1, roof_y):
            self.lfill(x0, y, z0, x1, y, z0, wall)
            self.lfill(x0, y, z1, x1, y, z1, wall)
            self.lfill(x0, y, z0, x0, y, z1, wall)
            self.lfill(x1, y, z0, x1, y, z1, wall)
        self.lfill(x0, roof_y, z0, x1, roof_y, z1, roof)
        # Repaired roofs: sparse patches are intentional, never a collapsed building.
        for x in range(x0 + 2, x1, 5):
            patch_z = z0 + 1 + ((x - x0) * 3) % max(1, z1 - z0 - 1)
            self.lput(x, roof_y + 1, patch_z, COPPER if (x + z1) % 2 else BROWN)

    def doorway(self, x: int, z: int, facing: str, hinge: str = "left") -> None:
        self.lput(x, GROUND_Y + 1, z, door(facing, "lower", hinge))
        self.lput(x, GROUND_Y + 2, z, door(facing, "upper", hinge))

    def window(self, x: int, z: int, y: int = GROUND_Y + 3) -> None:
        self.lput(x, y, z, PANE)
        self.lput(x, y + 1, z, PANE)

    def loot(self, x: int, z: int, table: str, facing: str = "north") -> None:
        self.lput(x, GROUND_Y + 1, z, chest(facing), {
            "id": "minecraft:chest",
            "LootTable": f"opusvsexe:chests/survivors_village_{table}",
        })

    def bed(self, x: int, z: int, facing: str, color: str = "green") -> None:
        dx, dz = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}[facing]
        self.lput(x, GROUND_Y + 1, z, state(f"minecraft:{color}_bed", facing=facing, part="foot", occupied="false"))
        self.lput(x + dx, GROUND_Y + 1, z + dz,
                  state(f"minecraft:{color}_bed", facing=facing, part="head", occupied="false"))

    def lantern(self, x: int, y: int, z: int, hanging: bool = False) -> None:
        self.lput(x, y, z, state("minecraft:lantern", hanging="true" if hanging else "false", waterlogged="false"))

    def survivor(self, x: int, z: int, variant: int, item: str | None = None) -> None:
        ax, ay, az = self.absolute(x, GROUND_Y + 1, z)
        nbt: dict[str, object] = {
            "id": "opusvsexe:survivor",
            "Variant": variant,
            "PersistenceRequired": True,
            "Health": 20.0,
        }
        if item:
            nbt["HandItems"] = [{"id": item, "Count": 1}, {}]
            nbt["HandDropChances"] = [0.0, 0.0]
        self.entities.append({
            "pos": (ax + 0.5, ay, az + 0.5),
            "blockPos": (ax, ay, az),
            "nbt": nbt,
        })


def road_network(v: Village) -> None:
    # Five-block primary spine and branches; the smaller spurs are two or three blocks.
    v.road_rect(-2, -50, 2, 50)
    v.road_rect(-42, -2, 42, 2)
    v.road_rect(-12, -13, 12, 13)
    v.road_rect(-2, -38, 2, -13)
    v.road_rect(11, -2, 18, 2)
    v.road_rect(-18, -2, -11, 2)
    v.road_rect(10, 2, 14, 35)
    v.road_rect(-14, 2, -10, 35)
    v.road_rect(-45, -24, -16, -22)
    v.road_rect(14, -24, 17, -10)
    v.road_rect(39, -24, 42, 15)
    v.road_rect(-49, 35, -30, 37)
    v.road_rect(31, 35, 46, 38)
    v.road_rect(-59, 10, -42, 12)


def wall_material(x: int, z: int) -> State:
    options = (SPR_LOG, STRIPPED, PLANK, BROWN, COPPER, GRAY, COBBLE)
    return options[(x * 13 + z * 7) % len(options)]


def perimeter(v: Village) -> None:
    vertices = [(-55, -46), (-28, -49), (1, -48), (29, -47), (54, -38), (59, -17),
                (58, 12), (53, 38), (36, 47), (10, 49), (-16, 47), (-40, 45),
                (-56, 34), (-59, 13), (-58, -15)]

    def is_gate(x: int, z: int) -> bool:
        return (z >= 43 and -4 <= x <= 4) or (z <= -43 and -2 <= x <= 2) or (x <= -56 and 9 <= z <= 14)

    def wall_cell(x: int, z: int) -> None:
        if is_gate(x, z):
            return
        material = wall_material(x, z)
        v.lfill(x, 0, z, x, GROUND_Y + 3, z, material)
        v.lput(x, GROUND_Y + 4, z, fence("minecraft:spruce_fence") if material in (SPR_LOG, STRIPPED, PLANK) else BARS)
        v.lput(x, GROUND_Y + 5, z, slab("minecraft:spruce_slab"))
        # An inward fighting step, interrupted at hard corners by tower modules.
        inward_x = x - 1 if abs(x) > abs(z) else x
        inward_z = z - 1 if abs(z) >= abs(x) else z
        v.lput(inward_x, GROUND_Y + 3, inward_z, slab("minecraft:stone_slab"))

    for (x0, z0), (x1, z1) in zip(vertices, vertices[1:] + vertices[:1]):
        steps = max(abs(x1 - x0), abs(z1 - z0))
        for index in range(steps + 1):
            x = round(x0 + (x1 - x0) * index / steps)
            z = round(z0 + (z1 - z0) * index / steps)
            wall_cell(x, z)

    main_gate(v)
    service_gate(v)
    postern(v)
    for x, z in ((48, -34), (-48, -32), (47, 33), (-47, 31), (8, -46)):
        watchtower(v, x, z)


def watchtower(v: Village, cx: int, cz: int) -> None:
    v.foundation(cx - 3, cz - 3, cx + 3, cz + 3, COBBLE)
    v.clear(cx - 3, cz - 3, cx + 3, cz + 3, GROUND_Y + 13)
    for x, z in ((cx - 2, cz - 2), (cx + 2, cz - 2), (cx - 2, cz + 2), (cx + 2, cz + 2)):
        v.lfill(x, GROUND_Y + 1, z, x, GROUND_Y + 9, z, STRIPPED)
    v.lfill(cx - 3, GROUND_Y + 9, cz - 3, cx + 3, GROUND_Y + 9, cz + 3, PLANK)
    for x in range(cx - 3, cx + 4):
        v.lput(x, GROUND_Y + 10, cz - 3, fence())
        v.lput(x, GROUND_Y + 10, cz + 3, fence())
    for z in range(cz - 2, cz + 3):
        v.lput(cx - 3, GROUND_Y + 10, z, fence())
        v.lput(cx + 3, GROUND_Y + 10, z, fence())
    v.lfill(cx - 3, GROUND_Y + 12, cz - 3, cx + 3, GROUND_Y + 12, cz + 3, PLANK)
    for y in range(GROUND_Y + 1, GROUND_Y + 10):
        v.lput(cx - 2, y, cz, state("minecraft:ladder", facing="east", waterlogged="false"))
    v.lput(cx, GROUND_Y + 10, cz, chest("north"), {"id": "minecraft:chest", "LootTable": "opusvsexe:chests/survivors_village_security"})
    v.lantern(cx + 2, GROUND_Y + 10, cz, hanging=True)


def main_gate(v: Village) -> None:
    v.foundation(-10, 42, 10, 50, COBBLE)
    v.clear(-10, 42, 10, 50, GROUND_Y + 13)
    v.road_rect(-2, 42, 2, 50)
    for cx in (-7, 7):
        v.lfill(cx - 2, GROUND_Y + 1, 43, cx + 2, GROUND_Y + 9, 49, BROWN)
        v.lfill(cx - 2, GROUND_Y + 10, 43, cx + 2, GROUND_Y + 10, 49, PLANK)
        v.lantern(cx, GROUND_Y + 7, 44, hanging=True)
        v.lput(cx, GROUND_Y + 4, 46, BARS)
    # Permanently open five-wide passage: no fake closed doors blocking the road.
    for x in range(-2, 3):
        v.lput(x, GROUND_Y + 6, 47, CHAIN)
    v.lput(0, GROUND_Y + 8, 47, state("minecraft:redstone_lamp", lit="true"))
    v.loot(-7, 45, "security", "east")
    v.loot(7, 45, "security", "west")


def service_gate(v: Village) -> None:
    v.foundation(-6, -50, 6, -42, COBBLE)
    v.clear(-6, -50, 6, -42, GROUND_Y + 10)
    v.road_rect(-1, -50, 1, -42)
    for x in (-5, 5):
        v.lfill(x - 1, GROUND_Y + 1, -49, x + 1, GROUND_Y + 7, -43, GRAY)
        v.lantern(x, GROUND_Y + 6, -45, hanging=True)
    v.lput(0, GROUND_Y + 7, -46, BARS)
    v.loot(5, -46, "security", "west")


def postern(v: Village) -> None:
    v.road_rect(-60, 10, -54, 13)
    v.lfill(-58, GROUND_Y + 1, 10, -57, GROUND_Y + 4, 13, AIR)
    v.lput(-58, GROUND_Y + 5, 11, trapdoor("east"))
    v.lput(-56, GROUND_Y + 2, 13, BROWN)


def central_square(v: Village) -> None:
    v.foundation(-13, -13, 13, 13, COBBLE)
    v.clear(-13, -13, 13, 13, GROUND_Y + 5)
    for x in range(-13, 14):
        for z in range(-13, 14):
            selector = (x * 5 + z * 11) % 9
            material = STONE if selector in (0, 4) else (GRAVEL if selector in (1, 2) else COBBLE)
            v.lput(x, GROUND_Y, z, material)
    # Fire, safe three-block clearance and non-text notice-board.
    v.lfill(-1, GROUND_Y, -1, 1, GROUND_Y, 1, STONE)
    v.lput(0, GROUND_Y + 1, 0, state("minecraft:campfire", facing="north", lit="true", signal_fire="false", waterlogged="false"))
    for x, z in ((-5, -3), (5, -3), (-5, 4), (5, 4)):
        v.lfill(x - 1, GROUND_Y + 1, z, x + 1, GROUND_Y + 1, z, slab("minecraft:spruce_slab"))
    v.lfill(-10, GROUND_Y + 1, -7, -10, GROUND_Y + 4, -4, STRIPPED)
    v.lfill(-12, GROUND_Y + 4, -7, -8, GROUND_Y + 4, -4, PLANK)
    v.lput(-10, GROUND_Y + 2, -5, State("minecraft:lectern"))
    v.lfill(5, GROUND_Y + 1, 7, 7, GROUND_Y + 2, 9, STONE)
    v.lput(6, GROUND_Y + 3, 8, state("minecraft:lightning_rod", facing="up"))
    v.lput(6, GROUND_Y + 1, 8, WATER)
    for x, z in ((-11, -11), (11, -11), (-11, 11), (11, 11)):
        v.lfill(x, GROUND_Y + 1, z, x, GROUND_Y + 3, z, STRIPPED)
        v.lantern(x, GROUND_Y + 4, z, hanging=True)


def command_house(v: Village) -> None:
    v.building(-11, -38, 11, -21, 10, wall=DARK_PLANK, floor=OAK_PLANK, roof=PLANK)
    v.doorway(0, -21, "south")
    v.doorway(9, -30, "east", "right")
    v.window(-5, -38); v.window(5, -38); v.window(-11, -31); v.window(11, -31)
    # Coordination / radio / battery desks and the private rear duty room.
    for x, z in ((-6, -33), (-2, -33), (3, -33), (7, -33)):
        v.lput(x, GROUND_Y + 1, z, State("minecraft:cartography_table"))
        v.lput(x, GROUND_Y + 2, z, State("minecraft:lever"))
    v.lfill(-8, GROUND_Y + 1, -25, -4, GROUND_Y + 1, -25, PLANK)
    v.loot(8, -35, "security", "west")
    v.loot(-8, -35, "hidden", "east")
    v.lfill(-2, GROUND_Y + 2, -28, 2, GROUND_Y + 2, -28, MEMORY_CABLE)
    for y in range(GROUND_Y + 11, 41):
        v.lput(0, y, -29, BARS if y % 3 else IRON)
        if y % 4 == 0:
            v.lput(1, y, -29, CHAIN)
    v.lput(0, 40, -29, state("minecraft:redstone_lamp", lit="true"))
    v.lantern(-8, GROUND_Y + 8, -24, hanging=True)
    v.lantern(8, GROUND_Y + 8, -24, hanging=True)


def clinic(v: Village) -> None:
    v.building(18, -10, 39, 9, 7, wall=LIGHT_GRAY, floor=STONE, roof=GRAY)
    v.doorway(24, -10, "north")
    v.doorway(37, 5, "east", "right")
    # Triage divider, ward, exam and wash area; all beds retain a free central aisle.
    v.lfill(25, GROUND_Y + 1, -7, 25, GROUND_Y + 4, 5, WHITE_WOOL)
    v.lfill(31, GROUND_Y + 1, -7, 31, GROUND_Y + 4, 5, WHITE_WOOL)
    for x, z, facing in ((20, -5, "east"), (20, 0, "east"), (20, 5, "east")):
        v.bed(x, z, facing, "white")
    v.lput(34, GROUND_Y + 1, -5, State("minecraft:brewing_stand"))
    v.lput(35, GROUND_Y + 1, -5, State("minecraft:cauldron"))
    v.lput(35, GROUND_Y + 1, 4, State("minecraft:barrel"))
    v.loot(36, 6, "medical", "west")
    v.lantern(22, GROUND_Y + 6, -2, hanging=True)
    v.lantern(34, GROUND_Y + 6, -2, hanging=True)


def market(v: Village) -> None:
    v.foundation(-42, -10, -18, 11, COARSE)
    v.clear(-42, -10, -18, 11, GROUND_Y + 7)
    v.road_rect(-42, -2, -18, 2)
    stalls = [(-40, -9, "food", GREEN_WOOL), (-34, 5, "house", GRAY_WOOL),
              (-28, -9, "workshop", BROWN), (-22, 5, "house", WHITE_WOOL),
              (-22, -9, "security", GREEN_WOOL), (-40, 5, "food", GRAY_WOOL)]
    for index, (x, z, loot, awning) in enumerate(stalls):
        v.lfill(x, GROUND_Y + 1, z, x + 5, GROUND_Y + 1, z, PLANK)
        v.lfill(x, GROUND_Y + 1, z, x, GROUND_Y + 5, z + 5, STRIPPED)
        v.lfill(x + 5, GROUND_Y + 1, z, x + 5, GROUND_Y + 5, z + 5, STRIPPED)
        v.lfill(x, GROUND_Y + 5, z, x + 5, GROUND_Y + 5, z + 5, awning)
        v.loot(x + 2, z + 1, loot, "south" if z < 0 else "north")
        v.lantern(x + 2, GROUND_Y + 4, z + 2, hanging=True)
        if index % 2 == 0:
            v.lput(x + 1, GROUND_Y + 1, z + 3, State("minecraft:barrel"))


def warehouse(v: Village) -> None:
    v.building(-43, 17, -20, 35, 8, wall=PLANK, floor=OAK_PLANK, roof=GRAY)
    v.doorway(-32, 17, "north")
    v.doorway(-42, 29, "west", "right")
    # Two-wide storage aisles, secure side room, receiving desk and loft suggestion.
    for x in (-40, -36, -28, -24):
        v.lfill(x, GROUND_Y + 1, 21, x + 1, GROUND_Y + 3, 31, State("minecraft:barrel"))
    v.lfill(-26, GROUND_Y + 1, 19, -21, GROUND_Y + 4, 24, IRON)
    v.doorway(-26, 25, "south")
    v.loot(-40, 19, "warehouse", "south")
    v.loot(-30, 19, "warehouse", "south")
    v.loot(-23, 22, "security", "west")
    v.lantern(-34, GROUND_Y + 7, 27, hanging=True)


def canteen(v: Village) -> None:
    v.building(-10, 20, 11, 35, 7, wall=PLANK, floor=DARK_PLANK, roof=BROWN)
    v.doorway(0, 20, "north")
    for x in (-7, -4, -1):
        v.lput(x, GROUND_Y + 1, 23, State("minecraft:smoker"))
        v.lput(x, GROUND_Y + 1, 24, State("minecraft:barrel"))
    v.lfill(2, GROUND_Y + 1, 23, 8, GROUND_Y + 1, 23, PLANK)
    for z in (27, 31):
        v.lfill(-6, GROUND_Y + 1, z, 6, GROUND_Y + 1, z, slab())
    v.loot(8, 33, "food", "west")
    v.lput(-8, GROUND_Y + 4, 34, state("minecraft:campfire", facing="north", lit="true", signal_fire="true", waterlogged="false"))
    v.lantern(0, GROUND_Y + 6, 27, hanging=True)


def workshop_and_generator(v: Village) -> None:
    v.building(18, 16, 42, 35, 8, wall=BROWN, floor=STONE, roof=COPPER)
    v.doorway(23, 16, "north")
    v.doorway(42, 28, "east", "right")
    v.lput(22, GROUND_Y + 1, 20, State("minecraft:crafting_table"))
    v.lput(26, GROUND_Y + 1, 20, State("minecraft:anvil"))
    v.lput(30, GROUND_Y + 1, 20, State("minecraft:blast_furnace"))
    v.lfill(34, GROUND_Y, 20, 38, GROUND_Y, 24, LAB_GRATE)
    v.lfill(34, GROUND_Y + 1, 20, 38, GROUND_Y + 1, 20, BARS)
    for x in (20, 24, 28, 32, 36, 40):
        v.lput(x, GROUND_Y + 2, 32, state("minecraft:iron_trapdoor", facing="south", half="bottom", open="false", powered="false", waterlogged="false"))
    v.loot(39, 33, "workshop", "west")
    v.lantern(25, GROUND_Y + 7, 23, hanging=True)
    v.lantern(36, GROUND_Y + 7, 28, hanging=True)

    v.building(33, 30, 46, 42, 6, wall=GRAY, floor=STONE, roof=IRON)
    v.doorway(40, 30, "north")
    for x in (35, 39, 43):
        v.lfill(x, GROUND_Y + 1, 34, x + 2, GROUND_Y + 3, 37, IRON)
        v.lput(x + 1, GROUND_Y + 4, 36, DATA_CONDUIT)
    v.lfill(34, GROUND_Y + 1, 40, 45, GROUND_Y + 1, 40, State("minecraft:barrel"))
    v.lfill(35, GROUND_Y + 6, 38, 44, GROUND_Y + 6, 38, MEMORY_CABLE)
    v.loot(44, 40, "workshop", "west")
    # Plausible aerial cable routes: generator → command/clinic/square/workshop.
    for x in range(12, 34):
        v.lput(x, GROUND_Y + 7, 34, MEMORY_CABLE)
    for z in range(-29, 35):
        if z % 2 == 0:
            v.lput(12, GROUND_Y + 7, z, MEMORY_CABLE)
    for x in range(12, 19):
        v.lput(x, GROUND_Y + 7, -2, MEMORY_CABLE)


def barracks(v: Village, x0: int, z0: int, x1: int, z1: int, variant: str) -> None:
    v.building(x0, z0, x1, z1, 7 if variant == "A" else 6,
               wall=PLANK if variant == "A" else DARK_PLANK, floor=OAK_PLANK, roof=BROWN if variant == "A" else COPPER)
    v.doorway((x0 + x1) // 2, z1, "south")
    for index, z in enumerate(range(z0 + 2, z1 - 2, 3)):
        v.bed(x0 + 2, z, "east", "green" if index % 2 == 0 else "gray")
        v.bed(x1 - 2, z, "west", "green" if index % 2 else "gray")
    v.lput((x0 + x1) // 2, GROUND_Y + 1, (z0 + z1) // 2, State("minecraft:campfire"))
    v.loot(x1 - 2, z0 + 2, "house", "west")
    v.lantern((x0 + x1) // 2, GROUND_Y + 6, z0 + 3, hanging=True)


def house(v: Village, x0: int, z0: int, width: int, depth: int, variant: int) -> None:
    x1, z1 = x0 + width - 1, z0 + depth - 1
    palettes = ((PLANK, DARK_PLANK, BROWN), (LIGHT_GRAY, OAK_PLANK, COPPER),
                (BROWN, PLANK, GRAY), (DARK_PLANK, OAK_PLANK, PLANK),
                (PLANK, STONE, COPPER), (GRAY, DARK_PLANK, BROWN))
    wall, floor, roof = palettes[variant % len(palettes)]
    v.building(x0, z0, x1, z1, 5 + variant % 3, wall=wall, floor=floor, roof=roof)
    v.doorway((x0 + x1) // 2, z1, "south", "right" if variant % 2 else "left")
    v.window(x0, z0 + depth // 2)
    v.window(x1, z0 + depth // 2)
    v.bed(x0 + 2, z0 + 2, "east", "green" if variant % 2 else "gray")
    v.lput(x1 - 2, GROUND_Y + 1, z0 + 2, State("minecraft:smoker"))
    v.lfill(x0 + 2, GROUND_Y + 1, z1 - 2, x1 - 2, GROUND_Y + 1, z1 - 2, slab())
    v.loot(x1 - 2, z1 - 2, "house", "west")
    if variant % 2 == 0:
        v.lfill(x0 - 1, GROUND_Y + 1, z1 + 1, x0 + 2, GROUND_Y + 1, z1 + 1, STRIPPED)
    else:
        v.lput(x0 - 1, GROUND_Y + 1, z0 + 1, State("minecraft:barrel"))
    v.lantern((x0 + x1) // 2, GROUND_Y + 4, z1 - 1, hanging=True)


def farm_and_utilities(v: Village) -> None:
    # Greenhouse: repaired glass under a timber/copper frame, never a pristine modern volume.
    v.foundation(-45, -45, -25, -35, DIRT)
    v.clear(-45, -45, -25, -35, GROUND_Y + 8)
    for x in range(-45, -24):
        for z in range(-45, -34):
            edge = x in (-45, -25) or z in (-45, -35)
            v.lput(x, GROUND_Y, z, DIRT)
            if edge:
                v.lfill(x, GROUND_Y + 1, z, x, GROUND_Y + 5, z, STRIPPED)
    v.lfill(-45, GROUND_Y + 6, -45, -25, GROUND_Y + 6, -35, GLASS)
    for x in range(-43, -26, 4):
        v.lput(x, GROUND_Y + 6, -40, COPPER)
    for x in range(-43, -27):
        for z in (-43, -42, -38, -37):
            v.lput(x, GROUND_Y, z, state("minecraft:farmland", moisture="7"))
            crop = "minecraft:carrots" if (x + z) % 2 else "minecraft:wheat"
            v.lput(x, GROUND_Y + 1, z, state(crop, age="7"))
    v.lfill(-44, GROUND_Y, -40, -26, GROUND_Y, -40, WATER)
    v.loot(-27, -36, "food", "west")
    v.lantern(-35, GROUND_Y + 5, -40, hanging=True)

    for x0, z0, x1, z1, crop in ((-45, -32, -33, -24, "minecraft:wheat"),
                                  (-31, -32, -18, -24, "minecraft:potatoes")):
        v.foundation(x0, z0, x1, z1, DIRT)
        v.clear(x0, z0, x1, z1, GROUND_Y + 3)
        for x in range(x0 + 1, x1):
            for z in range(z0 + 1, z1):
                if z == (z0 + z1) // 2:
                    v.lput(x, GROUND_Y, z, WATER)
                else:
                    v.lput(x, GROUND_Y, z, state("minecraft:farmland", moisture="7"))
                    v.lput(x, GROUND_Y + 1, z, state(crop, age="7"))
        for x in range(x0, x1 + 1):
            v.lput(x, GROUND_Y + 1, z0, fence())
            v.lput(x, GROUND_Y + 1, z1, fence())
    v.building(-23, -32, -17, -25, 4, wall=PLANK, floor=DARK_PLANK, roof=BROWN)
    v.doorway(-20, -25, "south")
    v.loot(-18, -30, "workshop", "west")
    v.lfill(-49, GROUND_Y, -44, -47, GROUND_Y + 1, -42, State("minecraft:composter"))

    # Empty animal pen by explicit policy; it still has trough, feed storage and drainage.
    v.foundation(-49, 32, -30, 46, DIRT)
    v.clear(-49, 32, -30, 46, GROUND_Y + 5)
    for x in range(-49, -29):
        for z in (32, 46):
            v.lput(x, GROUND_Y + 1, z, fence("minecraft:oak_fence"))
    for z in range(33, 46):
        for x in (-49, -30):
            v.lput(x, GROUND_Y + 1, z, fence("minecraft:oak_fence"))
    v.lfill(-43, GROUND_Y + 1, 37, -37, GROUND_Y + 1, 38, WATER)
    v.building(-48, 34, -43, 40, 4, wall=PLANK, floor=DARK_PLANK, roof=BROWN)
    v.doorway(-45, 40, "south")
    v.loot(-44, 35, "food", "west")

    # Sanitation: deliberately far from water, food, clinic and residential center.
    for x in (45, 49, 53):
        v.building(x, 6, x + 2, 11, 4, wall=PLANK, floor=COARSE, roof=BROWN)
        v.doorway(x + 1, 11, "south")
        v.lput(x + 1, GROUND_Y + 1, 8, State("minecraft:cauldron"))
    v.lfill(45, GROUND_Y, 13, 55, GROUND_Y, 15, COARSE)
    v.lfill(47, GROUND_Y + 1, 13, 53, GROUND_Y + 2, 15, BROWN)
    v.lput(44, GROUND_Y + 1, 13, State("minecraft:barrel"))


def quarantine(v: Village) -> None:
    v.building(19, -48, 31, -39, 5, wall=LIGHT_GRAY, floor=STONE, roof=GRAY)
    v.doorway(25, -39, "south")
    v.bed(21, -45, "east", "white")
    v.bed(21, -42, "east", "white")
    v.lput(28, GROUND_Y + 1, -45, State("minecraft:cauldron"))
    v.loot(29, -42, "medical", "west")
    for x in range(19, 32):
        v.lput(x, GROUND_Y + 1, -49, fence())
    v.lput(25, GROUND_Y + 5, -39, state("minecraft:redstone_lamp", lit="true"))


def shelter(v: Village) -> None:
    # Full reinforced shell, then an interior with one-cell partitions and doorways.
    v.lfill(-21, 1, -15, 21, 13, 16, GRAY)
    v.lfill(-19, 3, -13, 19, 11, 14, AIR)
    v.lfill(-19, 2, -13, 19, 2, 14, STONE)
    v.lfill(-19, 12, -13, 19, 12, 14, IRON)
    # Rooms: communal, bunk, storage/medical, ventilation/battery.
    v.lfill(-6, 3, -13, -6, 11, 3, STONE)
    v.lfill(-6, 3, 3, -6, 11, 14, STONE)
    v.lfill(7, 3, -13, 7, 11, 5, STONE)
    v.lfill(7, 3, 7, 7, 11, 14, STONE)
    for x, z in ((-6, -5), (-6, 8), (7, -4), (7, 10)):
        v.lfill(x, 5, z, x, 7, z + 1, AIR)
    for x in (-16, -12, -2, 1, 10, 14):
        v.bed(x, -8 if x < 0 else -5, "east", "gray")
    v.lfill(-17, 3, 5, -9, 5, 10, State("minecraft:barrel"))
    v.lput(11, 3, 8, State("minecraft:brewing_stand"))
    v.lput(12, 3, 8, State("minecraft:cauldron"))
    v.lfill(10, 3, -9, 16, 5, -3, IRON)
    v.lfill(11, 6, -8, 15, 6, -8, MEMORY_CABLE)
    v.lput(-17, 3, 12, chest("east"), {"id": "minecraft:chest", "LootTable": "opusvsexe:chests/survivors_village_shelter"})
    v.lput(-14, 3, 12, chest("east"), {"id": "minecraft:chest", "LootTable": "opusvsexe:chests/survivors_village_hidden"})
    for x, z in ((-16, -10), (-2, -10), (12, -10), (-14, 11), (2, 11), (15, 11)):
        v.lantern(x, 10, z, hanging=True)

    # Protected 13-block surface stair: it reaches the actual shelter floor,
    # rather than ending at the roof slab above the rooms.
    v.lfill(-2, 3, 2, 2, GROUND_Y + 2, 15, AIR)
    for index in range(14):
        y = GROUND_Y - index
        z = 15 - index
        v.lfill(-2, y, z, 2, y + 2, z, AIR)
        v.lfill(-2, y - 1, z, 2, y - 1, z, STONE)
        v.lfill(-1, y, z, 1, y, z, stair("minecraft:stone_brick_stairs", "north"))
    v.lput(0, GROUND_Y + 1, 15, trapdoor("north"))


def escape_tunnel(v: Village) -> None:
    # A 3×3 protected tunnel, rising one block every three horizontal blocks.
    for index, x in enumerate(range(-21, -60, -1)):
        floor_y = min(GROUND_Y, 5 + index // 3)
        for z in range(1, 6):
            for y in range(floor_y - 1, min(HEIGHT, floor_y + 4)):
                edge = z in (1, 5) or y in (floor_y - 1, floor_y + 3)
                v.lput(x, y, z, STONE if edge else AIR)
        v.lput(x, floor_y, 3, stair("minecraft:stone_brick_stairs", "west"))
        if index % 8 == 0:
            v.lput(x, floor_y + 2, 2, STRIPPED)
            v.lput(x, floor_y + 2, 4, STRIPPED)
            v.lantern(x, floor_y + 2, 3, hanging=True)
    v.lfill(-60, GROUND_Y, 1, -57, GROUND_Y + 2, 5, MOSSY)
    v.lfill(-59, GROUND_Y + 1, 3, -58, GROUND_Y + 2, 3, AIR)
    v.lput(-59, GROUND_Y + 3, 3, trapdoor("west"))


def residents(v: Village) -> None:
    # 20 dispersed persistent people: leadership, service roles, guards and households.
    placements = [
        (-2, -30, "minecraft:spyglass"), (4, -27, "minecraft:compass"),
        (22, -3, "minecraft:glass_bottle"), (34, 2, "minecraft:iron_axe"),
        (24, 22, "minecraft:iron_pickaxe"), (38, 34, "minecraft:iron_pickaxe"),
        (-34, -6, "minecraft:bread"), (-28, 7, "minecraft:leather"),
        (-33, 27, "minecraft:iron_axe"), (-2, 29, "minecraft:bread"),
        (-20, -23, "minecraft:iron_sword"), (24, -30, "minecraft:shield"),
        (47, 33, "minecraft:bow"), (-47, 31, "minecraft:bow"),
        (-4, 45, "minecraft:shield"), (7, -46, "minecraft:shield"),
        (-11, -15, None), (15, -15, None), (45, -4, "minecraft:iron_axe"), (43, 0, None),
    ]
    for variant, (x, z, item) in enumerate(placements):
        v.survivor(x, z, variant, item)


def build() -> Village:
    v = Village()
    road_network(v)
    perimeter(v)
    central_square(v)
    command_house(v)
    clinic(v)
    market(v)
    warehouse(v)
    canteen(v)
    workshop_and_generator(v)
    barracks(v, 15, -39, 35, -26, "A")
    barracks(v, 38, -37, 55, -25, "B")
    for variant, (x, z, width, depth) in enumerate(((-17, -20, 11, 10), (42, -20, 13, 10),
                                                       (42, -7, 14, 12), (44, 16, 11, 11),
                                                       (-56, -10, 11, 10), (-56, 17, 10, 10))):
        house(v, x, z, width, depth, variant)
    farm_and_utilities(v)
    quarantine(v)
    shelter(v)
    escape_tunnel(v)
    residents(v)
    return v


def nbt_value(value: object):
    if isinstance(value, bool):
        return Byte(value)
    if isinstance(value, int):
        return Int(value)
    if isinstance(value, float):
        return Float(value)
    return String(str(value))


def entity_nbt(value: object):
    if isinstance(value, dict):
        return Compound({str(key): entity_nbt(part) for key, part in value.items()})
    if isinstance(value, list):
        if not value:
            return List[Compound]([])
        if isinstance(value[0], dict):
            return List[Compound]([entity_nbt(part) for part in value])
        if isinstance(value[0], float):
            return List[Float]([Float(part) for part in value])
        return List[Int]([Int(part) for part in value])
    return nbt_value(value)


def write_template(v: Village, path: Path) -> None:
    palette: list[State] = []
    index: dict[State, int] = {}
    for block, _ in v.blocks.values():
        if block not in index:
            index[block] = len(palette)
            palette.append(block)
    palette_nbt = List[Compound]([])
    for block in palette:
        entry = Compound({"Name": String(block.name)})
        if block.properties:
            entry["Properties"] = Compound({key: String(value) for key, value in block.properties})
        palette_nbt.append(entry)
    blocks = List[Compound]([])
    for (x, y, z), (block, nbt) in sorted(v.blocks.items(), key=lambda item: (item[0][1], item[0][2], item[0][0])):
        entry = Compound({"pos": List[Int]([Int(x), Int(y), Int(z)]), "state": Int(index[block])})
        if nbt:
            entry["nbt"] = Compound({key: nbt_value(value) for key, value in nbt.items()})
        blocks.append(entry)
    entities = List[Compound]([])
    for entity in v.entities:
        pos = entity["pos"]
        block_pos = entity["blockPos"]
        entities.append(Compound({
            "pos": List[Double]([Double(pos[0]), Double(pos[1]), Double(pos[2])]),
            "blockPos": List[Int]([Int(block_pos[0]), Int(block_pos[1]), Int(block_pos[2])]),
            "nbt": entity_nbt(entity["nbt"]),
        }))
    root = File({
        "DataVersion": Int(DATA_VERSION),
        "size": List[Int]([Int(WIDTH), Int(HEIGHT), Int(DEPTH)]),
        "palette": palette_nbt,
        "blocks": blocks,
        "entities": entities,
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    root.save(path, gzipped=True)


def validate(v: Village) -> None:
    names = [block.name for block, _ in v.blocks.values()]
    hostile = {"opusvsexe:dormant_spawner", "opusvsexe:trial_trigger", "minecraft:structure_block", "minecraft:jigsaw"}
    if hostile.intersection(names):
        raise ValueError(f"forbidden settlement block(s): {sorted(hostile.intersection(names))}")
    if len(v.entities) != 20 or {entity["nbt"]["id"] for entity in v.entities} != {"opusvsexe:survivor"}:
        raise ValueError("KSV-01 must contain exactly 20 Survivor entities and no other entity type")
    loot = [nbt["LootTable"] for _, nbt in v.blocks.values() if nbt and "LootTable" in nbt]
    required = {"house", "food", "medical", "workshop", "warehouse", "security", "shelter", "hidden"}
    present = {entry.rsplit("_", 1)[-1] for entry in loot}
    if not required <= present:
        raise ValueError(f"missing village loot themes: {sorted(required - present)}")
    checkpoints = {
        "main gate": (0, GROUND_Y + 1, 47), "square": (0, GROUND_Y + 1, 10),
        "command": (0, GROUND_Y + 1, -22), "clinic": (24, GROUND_Y + 1, -9),
        "market": (-18, GROUND_Y + 1, 0), "workshop": (23, GROUND_Y + 1, 17),
        "service gate": (0, GROUND_Y + 1, -44), "shelter": (0, 4, 0),
        "escape exit": (-59, GROUND_Y + 1, 3),
    }
    for name, (x, y, z) in checkpoints.items():
        cell = v.blocks.get(v.absolute(x, y, z), (AIR, None))[0]
        if cell != AIR:
            raise ValueError(f"route checkpoint {name} is blocked by {cell.name}")
    print(f"KSV-01 template: {WIDTH}x{HEIGHT}x{DEPTH}; {len(v.blocks)} explicit blocks; "
          f"{len(set(names))} states; {len(loot)} containers; {len(v.entities)} survivors.")


if __name__ == "__main__":
    village = build()
    validate(village)
    write_template(village, OUTPUTS[0])
    copyfile(OUTPUTS[0], OUTPUTS[1])
    for theme in LOOT_THEMES:
        source_loot = ROOT / f"src/main/resources/data/opusvsexe/loot_tables/chests/survivors_village_{theme}.json"
        pack_loot = ROOT / f"pack/data/opusvsexe/loot_tables/chests/survivors_village_{theme}.json"
        copyfile(source_loot, pack_loot)
    for relative in ("worldgen/structure/survivor_settlement.json",
                     "worldgen/structure_set/survivor_settlement.json"):
        copyfile(ROOT / "src/main/resources/data/opusvsexe" / relative,
                 ROOT / "pack/data/opusvsexe" / relative)
    for output in OUTPUTS:
        print(output.relative_to(ROOT))
