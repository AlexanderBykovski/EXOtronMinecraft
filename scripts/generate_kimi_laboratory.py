#!/usr/bin/env python3
"""Build the deterministic K-17 Minecraft structure template.

The source is deliberately organised by architectural module instead of hand-editing
the binary NBT.  Run from the repository root after changing the plan:

    python3 scripts/generate_kimi_laboratory.py

It writes the same resource into `src/main/resources` and the `pack` mirror.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile
from typing import Iterable

from nbtlib import Compound, File, Int, List, String


WIDTH, HEIGHT, DEPTH = 117, 79, 101
ORIGIN_X, ORIGIN_Y, ORIGIN_Z = 58, 68, 50
ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = (
    ROOT / "src/main/resources/data/opusvsexe/structures/kimi_laboratory/main.nbt",
    ROOT / "pack/data/opusvsexe/structures/kimi_laboratory/main.nbt",
)


@dataclass(frozen=True)
class State:
    name: str
    properties: tuple[tuple[str, str], ...] = ()


AIR = State("minecraft:air")
SHELL = State("opusvsexe:cracked_lab_concrete")
DEEP = State("minecraft:deepslate_tiles")
BRICK = State("minecraft:deepslate_bricks")
PLATING = State("opusvsexe:fortress_plating")
GRATE = State("opusvsexe:lab_floor_grate")
OIL = State("opusvsexe:oil_stain")
GLASS = State("opusvsexe:opus_containment_glass")
MEMORY_GLASS = State("opusvsexe:memory_glass")
IRON = State("minecraft:iron_block")
BARS = State("minecraft:iron_bars")
CHAIN = State("minecraft:chain")
COPPER = State("minecraft:weathered_cut_copper")
GREEN = State("minecraft:green_terracotta")
WHITE = State("minecraft:light_gray_concrete")
TILE = State("minecraft:smooth_quartz")
RUST = State("minecraft:brown_terracotta")
BLACK = State("minecraft:black_concrete")
HAZARD = State("minecraft:yellow_concrete")
WATER = State("minecraft:water")
RUBBLE = State("minecraft:andesite")
MOSS = State("minecraft:mossy_stone_bricks")


def facing(name: str, direction: str) -> State:
    return State(name, (("facing", direction),))


def chest(direction: str = "north") -> State:
    return State("minecraft:chest", (("facing", direction), ("type", "single")))


def ladder(direction: str) -> State:
    return State("minecraft:ladder", (("facing", direction),))


def custom_facing(name: str, direction: str, **extra: str) -> State:
    props = {"facing": direction, **extra}
    return State(name, tuple(sorted(props.items())))


SPAWNER = State("opusvsexe:dormant_spawner", (("active", "true"),))
VAULT = State("opusvsexe:reward_vault", (("open", "false"),))
VAULT_OPEN = State("opusvsexe:reward_vault", (("open", "true"),))


class Lab:
    """Sparse template authoring with local K-17 coordinates."""

    def __init__(self) -> None:
        self.blocks: dict[tuple[int, int, int], tuple[State, dict[str, object] | None]] = {}
        self.notes: list[str] = []

    @staticmethod
    def absolute(x: int, y: int, z: int) -> tuple[int, int, int]:
        return x + ORIGIN_X, y + ORIGIN_Y, z + ORIGIN_Z

    def put(self, x: int, y: int, z: int, state: State, nbt: dict[str, object] | None = None) -> None:
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT and 0 <= z < DEPTH):
            raise ValueError(f"template coordinate outside K-17: {(x, y, z)}")
        self.blocks[(x, y, z)] = (state, nbt)

    def lput(self, x: int, y: int, z: int, state: State, nbt: dict[str, object] | None = None) -> None:
        self.put(*self.absolute(x, y, z), state, nbt)

    def fill(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, state: State) -> None:
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                for x in range(x0, x1 + 1):
                    self.put(x, y, z, state)

    def lfill(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, state: State) -> None:
        self.fill(*self.absolute(x0, y0, z0), *self.absolute(x1, y1, z1), state)

    def room(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int,
             floor: State, wall: State, ceiling: State | None = None, thickness: int = 2) -> None:
        """A sealed, cleared bunker module with a two-block exterior skin."""
        ceiling = ceiling or wall
        self.lfill(x0, y0, z0, x1, y1, z1, AIR)
        self.lfill(x0, y0, z0, x1, y0, z1, floor)
        if y0 > -68:
            self.lfill(x0, y0 - 1, z0, x1, y0 - 1, z1, BRICK)
        self.lfill(x0, y1, z0, x1, y1, z1, ceiling)
        for offset in range(thickness):
            self.lfill(x0 + offset, y0 + 1, z0, x0 + offset, y1 - 1, z1, wall)
            self.lfill(x1 - offset, y0 + 1, z0, x1 - offset, y1 - 1, z1, wall)
            self.lfill(x0, y0 + 1, z0 + offset, x1, y1 - 1, z0 + offset, wall)
            self.lfill(x0, y0 + 1, z1 - offset, x1, y1 - 1, z1 - offset, wall)

    def doorway_x(self, x: int, y: int, z: int, width: int = 3, height: int = 3, depth: int = 3) -> None:
        self.lfill(x, y, z - width // 2, x + depth - 1, y + height - 1, z + width // 2, AIR)

    def doorway_z(self, x: int, y: int, z: int, width: int = 3, height: int = 3, depth: int = 3) -> None:
        self.lfill(x - width // 2, y, z, x + width // 2, y + height - 1, z + depth - 1, AIR)

    def lamp(self, x: int, y: int, z: int, emergency: bool = False) -> None:
        if emergency:
            self.lput(x, y, z, State("minecraft:shroomlight"))
            self.lput(x, y - 1, z, State("minecraft:red_stained_glass"))
        else:
            self.lput(x, y, z, State("minecraft:sea_lantern"))
            self.lput(x, y - 1, z, State("minecraft:iron_trapdoor"))

    def grate_line_x(self, x0: int, x1: int, y: int, z: int) -> None:
        for x in range(x0, x1 + 1):
            self.lput(x, y, z, GRATE)

    def pipe_x(self, x0: int, x1: int, y: int, z: int, state: State) -> None:
        for x in range(x0, x1 + 1):
            self.lput(x, y, z, state)

    def pipe_z(self, x: int, y: int, z0: int, z1: int, state: State) -> None:
        for z in range(z0, z1 + 1):
            self.lput(x, y, z, state)

    def railing_x(self, x0: int, x1: int, y: int, z: int) -> None:
        for x in range(x0, x1 + 1):
            self.lput(x, y, z, BARS)

    def railing_z(self, x: int, y: int, z0: int, z1: int) -> None:
        for z in range(z0, z1 + 1):
            self.lput(x, y, z, BARS)

    def loot(self, x: int, y: int, z: int, table: str, direction: str = "north") -> None:
        self.lput(x, y, z, chest(direction), {"id": "minecraft:chest", "LootTable": f"opusvsexe:chests/kimi_lab/{table}"})

    def vault(self, x: int, y: int, z: int, table: str, locked: bool = False) -> None:
        self.lput(x, y, z, VAULT if locked else VAULT_OPEN,
                  {"id": "opusvsexe:reward_vault", "LootTable": f"opusvsexe:chests/kimi_lab/{table}"})

    def spawner(self, x: int, y: int, z: int, entity: str, *, max_nearby: int = 4,
                spawn_radius: int = 2) -> None:
        self.lput(x, y, z, SPAWNER, {
            "id": "opusvsexe:dormant_spawner",
            "entity_id": f"opusvsexe:{entity}",
            "max_nearby": max_nearby,
            "spawn_radius": spawn_radius,
        })

    def console(self, x: int, y: int, z: int, text: str, direction: str = "north") -> None:
        self.lput(x, y, z, custom_facing("opusvsexe:memory_console", direction, used="false"),
                  {"id": "opusvsexe:memory_console", "memory_text": text})

    def keypad(self, x: int, y: int, z: int, order: int, puzzle: str, direction: str = "north") -> None:
        self.lput(x, y, z, custom_facing("opusvsexe:sequence_keypad", direction, solved="false"),
                  {"id": "opusvsexe:sequence_keypad", "puzzle_id": puzzle, "order": order, "solved": False})


def build_surface(lab: Lab) -> None:
    lab.room(-14, 0, -11, 14, 10, 11, WHITE, SHELL, DEEP)
    # Loading facade, side administration door, generator housing and deliberate roof damage.
    lab.doorway_z(0, 1, 9, width=5, height=4, depth=3)
    lab.doorway_x(-13, 1, -3, width=3, height=3, depth=3)
    lab.lfill(7, 1, -10, 13, 5, -4, RUST)
    lab.lfill(8, 2, -9, 12, 4, -5, AIR)
    lab.lfill(7, 10, -11, 14, 10, -4, AIR)
    for x, z in ((-12, 10), (-7, 10), (8, 10), (13, 7), (13, -2), (7, -10), (-9, -10)):
        lab.lput(x, 1, z, BARS)
    for x in range(-11, 12, 4):
        lab.lput(x, 1, 8, State("minecraft:barrel"))
    for x, z in ((10, -8), (12, -6), (9, -5)):
        lab.lput(x, 1, z, State("minecraft:lightning_rod"))
    lab.lfill(8, 8, -9, 11, 10, -6, SHELL)  # ventilation tower within the +10 silhouette cap
    lab.lfill(9, 9, -8, 10, 10, -7, AIR)
    lab.lput(1, 5, 10, State("minecraft:redstone_lamp"))
    lab.lput(1, 5, 9, State("minecraft:red_stained_glass"))
    for x in range(-12, 14):
        if x % 3 == 0:
            lab.lput(x, 0, -10, MOSS)
            lab.lput(x, 0, 10, State("minecraft:gravel"))
    lab.lfill(-14, 0, 5, 14, 0, 6, GRATE)


def build_access_shaft(lab: Lab) -> None:
    # Offset to the west like the second concept art: it enters the resonator through its side.
    lab.lfill(-14, -60, -6, -2, 5, 6, AIR)
    for y in range(-60, 6):
        for x in range(-14, -1):
            for z in range(-6, 7):
                if x <= -13 or x >= -3 or z <= -5 or z >= 5:
                    lab.lput(x, y, z, PLATING if y < -36 else SHELL)
    # Freight cage, counterweight chains, reliable ladder and buffered landings.
    for y in range(-59, 5):
        lab.lput(-4, y, 3, ladder("east"))
        if y % 3 == 0:
            lab.lput(-9, y, -1, CHAIN)
            lab.lput(-8, y, 1, CHAIN)
    for y in (-59, -49, -40, -27, -14, -5, 0):
        lab.lfill(-12, y, -4, -5, y, -2, DEEP)
        lab.railing_x(-12, -5, y + 1, -4)
        lab.lput(-11, y + 1, -3, facing("opusvsexe:signal_panel", "east"))
        lab.lamp(-12, y + 3, -3, emergency=True)
    lab.lfill(-10, -60, -2, -6, -58, 2, WATER)  # safe basin under the visible deep drop
    lab.lfill(-12, -38, -1, -5, -36, 2, RUBBLE)  # blocked freight lift landing; ladder remains free
    lab.lfill(-13, -13, -2, -1, -9, 2, AIR)      # L1 arrival
    lab.lfill(-13, -26, -2, -1, -22, 2, AIR)     # L2 service exit
    lab.lfill(-13, -39, -2, -1, -35, 2, AIR)     # L3 service exit
    lab.lfill(-13, -58, -2, -1, -54, 2, AIR)     # L4 upper ring entry


def build_level_one(lab: Lab) -> None:
    lab.room(-2, -14, -10, 8, -5, 8, WHITE, GREEN, SHELL)
    lab.room(9, -14, -7, 25, -5, 7, TILE, GREEN, SHELL)
    lab.room(25, -14, -9, 31, -5, 9, TILE, GREEN, SHELL)
    lab.room(31, -14, -8, 39, -5, 10, WHITE, GREEN, SHELL)
    lab.room(8, -14, -22, 25, -5, -8, WHITE, GREEN, SHELL)
    lab.room(9, -14, 10, 30, -5, 28, TILE, GREEN, SHELL)
    lab.room(31, -14, 10, 48, -5, 28, WHITE, GREEN, SHELL)
    lab.room(39, -27, -12, 48, -5, 8, DEEP, SHELL, DEEP)
    # The security checkpoint from art 1: turnstiles, inspection desk and armoured booth.
    lab.doorway_x(7, -13, 0)
    lab.doorway_x(24, -13, 0)
    lab.doorway_x(30, -13, 0)
    lab.doorway_z(35, -13, 8)
    lab.doorway_z(40, -13, 9)
    lab.doorway_x(38, -13, 0)
    for z in (-3, 0, 3):
        lab.lfill(14, -13, z, 14, -12, z + 1, BARS)
        lab.lput(15, -12, z, State("minecraft:heavy_weighted_pressure_plate"))
    lab.lfill(17, -12, -6, 23, -8, -2, GLASS)
    lab.lput(19, -12, -1, facing("opusvsexe:scanner_eye", "south"))
    lab.grate_line_x(10, 24, -14, 0)
    for x in (2, 7, 12, 17, 22, 27, 33, 38, 44):
        lab.lamp(x, -6, 0, emergency=x in (12, 33))
    # Locker/security loop.
    for z in range(-20, -9, 3):
        lab.lput(10, -13, z, State("minecraft:iron_trapdoor"))
        lab.lput(11, -13, z, State("minecraft:iron_trapdoor"))
    lab.loot(21, -13, -19, "security", "south")
    lab.loot(12, -13, -18, "security", "east")
    lab.spawner(23, -13, -12, "haiku_1_5")
    # Office/records/cafeteria loop with not-identical desks and supplies.
    for x, z in ((12, 14), (18, 18), (25, 13), (33, 14), (42, 18)):
        lab.lput(x, -13, z, State("minecraft:dark_oak_slab"))
        lab.lput(x + 1, -13, z, facing("opusvsexe:dead_terminal", "north"))
    for x, z in ((13, 24), (20, 12), (28, 24), (34, 24)):
        lab.loot(x, -13, z, "office", "north")
    lab.console(34, -13, 19, "K-17: access protocol degraded; the research level remains powered.", "west")
    lab.lfill(42, -13, -8, 45, -12, 5, State("minecraft:stone_brick_stairs"))
    lab.grate_line_x(26, 30, -14, 0)


def build_level_two(lab: Lab) -> None:
    lab.room(-30, -27, -3, 31, -17, 3, TILE, GREEN, SHELL)
    lab.room(7, -27, -30, 31, -17, -10, TILE, WHITE, SHELL)
    lab.room(-32, -27, -30, -10, -17, -12, TILE, GREEN, SHELL)
    lab.room(-7, -27, -30, 14, -17, -10, TILE, GREEN, SHELL)
    lab.room(13, -27, 10, 33, -17, 26, TILE, WHITE, SHELL)
    lab.room(-10, -27, 10, 12, -17, 27, TILE, GREEN, SHELL)
    lab.room(-34, -27, 10, -13, -17, 28, TILE, GREEN, SHELL)
    lab.doorway_z(-27, -26, -4)
    lab.doorway_z(15, -26, -10)
    lab.doorway_z(-21, -26, -12)
    lab.doorway_z(4, -26, -10)
    lab.doorway_z(22, -26, 3)
    lab.doorway_z(0, -26, 3)
    lab.doorway_z(-24, -26, 3)
    for x in range(-27, 31, 8):
        lab.lfill(x, -26, -3, x + 1, -22, -3, SHELL)
        lab.lfill(x, -26, 3, x + 1, -22, 3, SHELL)
        lab.lamp(x + 3, -18, 0, emergency=x in (-11, 13))
    lab.grate_line_x(-29, 30, -27, 0)
    # General research tables, glass and secure cabinet.
    for x in (10, 16, 22, 28):
        lab.lfill(x, -26, -25, x + 3, -25, -22, IRON)
        lab.lfill(x, -25, -25, x + 3, -25, -22, State("minecraft:light_gray_carpet"))
    lab.lfill(8, -24, -16, 30, -20, -15, GLASS)
    lab.loot(28, -26, -12, "chemical", "west")
    lab.loot(9, -26, -12, "research", "south")
    lab.spawner(25, -26, -19, "haiku_1_5")
    # Four different specimen tanks, an observation booth and the first cascade vault.
    for index, x in enumerate((-29, -23, -17, -11)):
        lab.lfill(x, -26, -26, x + 3, -20, -22, GLASS)
        lab.lfill(x + 1, -25, -25, x + 2, -22, -23, WATER if index in (0, 2) else AIR)
        lab.lput(x + 1, -19, -24, facing("opusvsexe:signal_panel", "south"))
    lab.lfill(-30, -24, -17, -22, -20, -16, MEMORY_GLASS)
    lab.loot(-31, -26, -14, "research", "east")
    lab.spawner(-17, -26, -19, "haiku_2")
    # Chemical, cold storage and sample archive.
    for x, z in ((-5, -25), (1, -25), (7, -25), (10, -18)):
        lab.lput(x, -26, z, State("minecraft:barrel"))
    lab.loot(-5, -26, -13, "chemical", "south")
    # Medical ward: beds deliberately staggered, nurse station and side storage.
    for x, z, direction in ((15, 13, "east"), (20, 15, "east"), (25, 13, "west"), (30, 18, "west"), (17, 22, "east"), (28, 23, "west")):
        lab.lput(x, -26, z, State("minecraft:white_bed", (("facing", direction), ("part", "foot"), ("occupied", "false"))))
        lab.lput(x + (1 if direction == "east" else -1), -26, z, State("minecraft:white_bed", (("facing", direction), ("part", "head"), ("occupied", "false"))))
    lab.lfill(14, -26, 20, 18, -25, 22, IRON)
    lab.loot(31, -26, 24, "medical", "north")
    lab.loot(16, -26, 24, "medical", "north")
    lab.lput(20, -26, 21, State("minecraft:cauldron"))
    # Data room preserves the four-key memory puzzle but cannot block the route.
    for order, x in enumerate((-7, -2, 3, 8)):
        lab.keypad(x, -26, 14, order, "k17_memory_cascade", "south")
    lab.console(-7, -26, 20, "Memory sequence: observation, containment, signal, archive.", "east")
    lab.console(-2, -26, 20, "The Opus recordings predate the first autonomous response.", "east")
    lab.console(3, -26, 20, "Do not trust a memory that asks to be preserved.", "east")
    lab.console(8, -26, 20, "K-17 research node: sequence closes the isolated vault circuit.", "east")
    lab.vault(9, -26, 24, "memory_vault", locked=True)
    lab.loot(-8, -26, 24, "office", "north")
    # Damaged containment uses a safe crawl-like bypass and one optional cache.
    lab.lfill(-31, -25, 21, -21, -22, 27, RUBBLE)
    lab.lfill(-31, -23, 13, -28, -21, 19, AIR)
    lab.loot(-15, -26, 25, "hidden", "north")
    lab.spawner(-20, -26, 13, "haiku_2")


def build_level_three(lab: Lab) -> None:
    lab.room(-41, -40, -26, -9, -29, -2, DEEP, PLATING, DEEP)
    lab.room(-41, -40, 3, -10, -29, 27, DEEP, PLATING, DEEP)
    lab.room(11, -40, -27, 38, -29, -5, DEEP, PLATING, DEEP)
    lab.room(11, -40, 1, 40, -29, 27, DEEP, PLATING, DEEP)
    lab.room(-8, -40, -28, 1, -29, 14, DEEP, SHELL, DEEP)
    lab.room(-8, -40, 14, 9, -29, 29, DEEP, SHELL, DEEP)
    for x, z in ((-33, -18), (-24, -18), (-15, -18)):
        build_generator(lab, x, -39, z)
    lab.doorway_z(-25, -39, -1)
    lab.doorway_z(-25, -39, 2)
    lab.doorway_z(23, -39, -4)
    lab.doorway_z(23, -39, 0)
    lab.doorway_x(-9, -39, -6)
    lab.doorway_x(8, -39, 20)
    # Pipe and cable logic: every line terminates at a machine, a tank or a service wall.
    lab.pipe_x(-39, -10, -33, -24, COPPER)
    lab.pipe_x(-39, -10, -34, -22, RUST)
    lab.pipe_z(-38, -34, -23, -4, State("minecraft:green_terracotta"))
    lab.pipe_z(-12, -34, 5, 25, BLACK)
    lab.pipe_x(13, 37, -33, -24, COPPER)
    lab.pipe_z(36, -34, -24, -8, RUST)
    lab.pipe_x(13, 39, -33, 5, BLACK)
    for x in (-39, -30, -21, -12, 14, 26, 38):
        lab.lamp(x, -30, -4 if x < 0 else 4, emergency=True)
    for z in range(-25, 13, 6):
        lab.lput(-7, -39, z, WATER)
        lab.lput(-6, -39, z, WATER)
        lab.lput(-5, -39, z, GRATE)
        lab.lput(-1, -39, z, State("minecraft:stone_slab"))
    lab.lfill(-8, -39, -27, -6, -38, 8, WATER)
    lab.lfill(-4, -39, -27, -2, -39, 8, State("minecraft:stone_slab"))
    lab.railing_z(-3, -38, -27, 8)
    lab.lfill(-7, -37, 9, -5, -35, 13, RUBBLE)  # dead-end collapse away from side walkway
    lab.loot(-36, -39, 20, "maintenance", "east")
    lab.loot(-14, -39, 22, "maintenance", "south")
    lab.loot(14, -39, -22, "maintenance", "south")
    lab.loot(37, -39, 21, "maintenance", "west")
    lab.loot(1, -39, 23, "maintenance", "north")
    lab.spawner(-34, -39, -9, "haiku_2")
    lab.spawner(18, -39, 16, "haiku_2")


def build_generator(lab: Lab, x: int, y: int, z: int) -> None:
    lab.lfill(x, y, z, x + 6, y + 3, z + 6, IRON)
    lab.lfill(x + 1, y + 1, z + 1, x + 5, y + 2, z + 5, BLACK)
    lab.lput(x + 3, y + 3, z + 3, State("opusvsexe:flickering_terminal", (("facing", "south"),)))
    lab.lfill(x - 1, y, z - 1, x + 7, y, z - 1, HAZARD)
    lab.lfill(x - 1, y, z + 7, x + 7, y, z + 7, HAZARD)
    lab.railing_x(x - 1, x + 7, y + 1, z - 1)


def build_resonator(lab: Lab) -> None:
    cx, cz = 20, 0
    for y in range(-59, -36):
        for x in range(-7, 48):
            for z in range(-27, 28):
                dx, dz = abs(x - cx), abs(z - cz)
                inside = max(dx, dz) <= 27 and dx + dz <= 45
                inner = max(dx, dz) <= 24 and dx + dz <= 40
                if not inside:
                    continue
                if y in (-59, -37) or not inner:
                    lab.lput(x, y, z, PLATING)
                else:
                    lab.lput(x, y, z, AIR)
    # Three safe rings from art 1, all with handrails; a single broken optional bridge has a detour.
    for y, radius in ((-56, 18), (-49, 15), (-41, 12)):
        for x in range(cx - radius - 2, cx + radius + 3):
            for z in range(cz - radius - 2, cz + radius + 3):
                dx, dz = abs(x - cx), abs(z - cz)
                if max(dx, dz) <= radius + 2 and max(dx, dz) >= radius - 1 and dx + dz <= radius * 2 + 3:
                    lab.lput(x, y, z, DEEP)
                    if max(dx, dz) >= radius + 1:
                        lab.lput(x, y + 1, z, BARS)
    for x in range(-5, 42):
        if x not in (31, 32, 33):
            lab.lput(x, -49, 0, DEEP)
    lab.railing_x(-5, 30, -48, -1)
    lab.railing_x(-5, 30, -48, 1)
    for z in range(-24, 25):
        lab.lput(cx, -49, z, DEEP)
    lab.railing_z(cx - 1, -48, -24, 24)
    lab.railing_z(cx + 1, -48, -24, 24)
    # Machine core: lower pedestal 15x15, column 11x11, crown 13x13 and a damaged upper segment.
    lab.lfill(13, -58, -7, 27, -55, 7, DEEP)
    lab.lfill(15, -55, -5, 25, -39, 5, BLACK)
    for y in range(-54, -39, 3):
        lab.lfill(14, y, -6, 26, y, 6, PLATING)
        lab.lput(20, y + 1, -6, MEMORY_GLASS)
        lab.lput(20, y + 1, 6, MEMORY_GLASS)
        lab.lput(14, y + 1, 0, State("opusvsexe:flickering_terminal", (("facing", "east"),)))
        lab.lput(26, y + 1, 0, State("opusvsexe:flickering_terminal", (("facing", "west"),)))
    lab.lfill(14, -39, -6, 26, -37, 6, PLATING)
    lab.lfill(20, -40, 2, 23, -38, 5, AIR)  # broken crown exposed to the upper cable tray
    for x, z in ((7, 0), (33, 0), (20, -13), (20, 13)):
        lab.lfill(min(x, 20), -49, min(z, 0), max(x, 20), -49, max(z, 0), State("opusvsexe:memory_cable"))
    for x, z, direction, damage in ((20, -25, "south", False), (20, 25, "north", True), (43, 0, "west", False), (-3, 0, "east", True)):
        lab.lfill(x - 3, -50, z - 3, x + 3, -46, z + 3, SHELL if damage else WHITE)
        lab.lfill(x - 2, -49, z - 2, x + 2, -48, z + 2, GLASS)
        lab.lput(x, -49, z, facing("opusvsexe:command_terminal", direction))
        lab.lamp(x, -44, z, emergency=True)
    lab.console(8, -49, -20, "Resonator coupling remains in passive archival mode.", "south")
    lab.loot(43, -56, -4, "maintenance", "west")
    lab.spawner(7, -56, 10, "haiku_2")
    # A single elite warden occupies the deliberately broad lower ring. It has
    # clearance below the middle ring and cannot multiply into a boss pack.
    lab.spawner(7, -56, -10, "haiku_4", max_nearby=1, spawn_radius=0)


def build_level_five(lab: Lab) -> None:
    lab.room(-41, -68, -24, -15, -60, -4, DEEP, PLATING, DEEP)
    lab.room(-14, -68, -24, -3, -60, -9, DEEP, PLATING, DEEP)
    lab.room(14, -68, -26, 38, -60, -2, DEEP, PLATING, DEEP)
    lab.room(-1, -68, 4, 27, -60, 26, DEEP, PLATING, DEEP)
    lab.room(28, -68, 4, 43, -60, 22, DEEP, PLATING, DEEP)
    lab.room(43, -68, 10, 53, -60, 31, DEEP, SHELL, DEEP)
    lab.doorway_x(-16, -67, -14)
    lab.doorway_x(-4, -67, -16)
    lab.doorway_z(25, -67, -3)
    lab.doorway_x(27, -67, 14)
    lab.doorway_x(42, -67, 18)
    # Dense archive but every aisle stays two blocks wide.
    for x in (-38, -33, -28, -23, -18):
        lab.lfill(x, -67, -22, x + 1, -63, -7, State("minecraft:bookshelf"))
    lab.lfill(-29, -67, -14, -25, -67, -11, State("minecraft:dark_oak_slab"))
    lab.loot(-39, -67, -6, "archive", "east")
    lab.loot(-17, -67, -6, "archive", "west")
    lab.vault(-6, -67, -14, "archive")
    lab.console(-8, -67, -20, "Archive K-17: Opus retains observations long after the observers are gone.", "east")
    # Backup reactor deliberately differs from the tall resonator: compact, shielded, red-lit.
    lab.lfill(20, -67, -20, 32, -64, -8, IRON)
    lab.lfill(22, -64, -18, 30, -61, -10, BLACK)
    lab.lput(26, -63, -9, State("opusvsexe:pulsing_core"))
    lab.lfill(17, -67, -24, 35, -67, -23, HAZARD)
    lab.pipe_z(34, -63, -22, -7, COPPER)
    lab.pipe_z(36, -63, -22, -7, COPPER)
    lab.loot(16, -67, -4, "reactor", "north")
    lab.vault(36, -67, -5, "reactor")
    lab.spawner(34, -67, -18, "haiku_1_5")
    # The titan needs a true nine-block headroom. This exhaust bay breaks the
    # low reactor ceiling into the already empty resonator volume above it.
    lab.lfill(32, -60, -6, 36, -57, -2, AIR)
    lab.spawner(34, -67, -4, "haiku_5", max_nearby=1, spawn_radius=0)
    # Controlled collapse, safe low route, and single rare stash.
    for x in range(1, 17):
        lab.lfill(x, -67, 7 + x // 2, x + 2, -64, 11 + x // 2, RUBBLE)
    lab.lfill(-1, -66, 22, 5, -64, 25, AIR)
    lab.loot(24, -67, 24, "hidden", "south")
    lab.lfill(30, -67, 7, 41, -67, 9, WATER)
    lab.lput(31, -67, 15, facing("opusvsexe:dead_terminal", "east"))
    lab.lamp(40, -61, 17, emergency=True)
    # Drainage line to a rising ladder shaft and the concealed outlet.
    lab.lfill(44, -67, 12, 52, -66, 29, WATER)
    lab.lfill(45, -65, 13, 51, -62, 29, AIR)
    for z in range(12, 30):
        lab.lput(47, -67, z, State("minecraft:stone_slab"))
        lab.lput(48, -66, z, BARS)
    lab.lfill(50, -68, 29, 54, 0, 33, AIR)
    for y in range(-67, 1):
        lab.lput(51, y, 30, ladder("east"))
        if y % 5 == 0:
            lab.lput(53, y, 31, SHELL)
    lab.room(48, -1, 34, 56, 3, 44, SHELL, SHELL, SHELL, thickness=1)
    lab.lfill(50, 0, 39, 55, 0, 43, GRATE)
    lab.lfill(52, 1, 42, 55, 2, 43, AIR)
    lab.lput(53, 1, 43, State("minecraft:iron_trapdoor"))
    lab.loot(49, -67, 14, "hidden", "south")
    lab.spawner(45, -67, 19, "haiku_2")


def build_deep_access(lab: Lab) -> None:
    """Protected L4-to-L5 descent; it bypasses the blocked freight lift."""
    lab.lfill(-18, -68, -20, -8, -54, -10, AIR)
    for y in range(-68, -53):
        for x in range(-18, -7):
            for z in range(-20, -9):
                if x <= -17 or x >= -9 or z <= -19 or z >= -11:
                    lab.lput(x, y, z, PLATING)
    for y in range(-67, -53):
        lab.lput(-10, y, -16, ladder("east"))
        if y % 4 == 0:
            lab.lput(-15, y, -18, CHAIN)
    lab.lfill(-16, -68, -18, -10, -68, -12, DEEP)
    lab.lfill(-16, -55, -18, -10, -55, -12, DEEP)
    lab.railing_x(-16, -10, -54, -18)
    # Doorways connect the upper resonator/service shaft and the deep archive.
    lab.lfill(-14, -56, -12, -9, -53, -4, AIR)
    lab.lfill(-13, -56, -11, -6, -56, -5, DEEP)
    lab.railing_x(-13, -6, -55, -11)
    lab.lfill(-18, -67, -18, -14, -64, -12, AIR)


def add_damage_and_final_detail(lab: Lab) -> None:
    # Designed moisture and shallow puddles only; no critical path or block entity is overwritten.
    for x, y, z in ((-8, -13, -8), (26, -13, 7), (30, -26, 2), (-30, -26, -4), (38, -39, 3), (-40, -39, 26), (42, -67, 20)):
        lab.lput(x, y, z, OIL)
    for x, y, z in ((-10, -12, 6), (29, -12, -7), (4, -25, -29), (-33, -25, 12), (-7, -38, -20), (39, -66, 12)):
        lab.lput(x, y, z, MOSS)
    # Deliberately hidden-but-reachable common containers complete the sector loot curve.
    for x, y, z, table, direction in (
        (5, -13, 5, "security", "west"), (21, -13, 5, "security", "south"),
        (15, -13, 26, "office", "north"), (43, -13, 22, "office", "west"),
        (19, -26, -25, "research", "south"), (-4, -26, -20, "chemical", "east"),
        (31, -39, 12, "maintenance", "north"),
    ):
        lab.loot(x, y, z, table, direction)
    # Main connections stay bright enough to read even where the surrounding room is dark.
    for x, y, z in ((-1, -6, 0), (30, -6, 0), (30, -18, 0), (-8, -30, -1), (-6, -42, 0), (-4, -54, 0), (42, -61, 17), (52, -3, 39)):
        lab.lamp(x, y, z, emergency=True)


def build() -> Lab:
    lab = Lab()
    build_surface(lab)
    build_level_one(lab)
    build_level_two(lab)
    build_level_three(lab)
    build_resonator(lab)
    build_level_five(lab)
    build_access_shaft(lab)
    build_deep_access(lab)
    add_damage_and_final_detail(lab)
    return lab


def nbt_value(value: object):
    if isinstance(value, bool):
        from nbtlib import Byte
        return Byte(value)
    if isinstance(value, int):
        return Int(value)
    return String(str(value))


def write_template(lab: Lab, path: Path) -> None:
    palette: list[State] = []
    palette_index: dict[State, int] = {}
    for state, _ in lab.blocks.values():
        if state not in palette_index:
            palette_index[state] = len(palette)
            palette.append(state)
    palette_nbt = List[Compound]([])
    for state in palette:
        entry = Compound({"Name": String(state.name)})
        if state.properties:
            entry["Properties"] = Compound({key: String(value) for key, value in state.properties})
        palette_nbt.append(entry)
    blocks = List[Compound]([])
    for (x, y, z), (state, nbt) in sorted(lab.blocks.items(), key=lambda item: (item[0][1], item[0][2], item[0][0])):
        entry = Compound({
            "pos": List[Int]([Int(x), Int(y), Int(z)]),
            "state": Int(palette_index[state]),
        })
        if nbt:
            entry["nbt"] = Compound({key: nbt_value(value) for key, value in nbt.items()})
        blocks.append(entry)
    root = File({
        "DataVersion": Int(3465),
        "size": List[Int]([Int(WIDTH), Int(HEIGHT), Int(DEPTH)]),
        "palette": palette_nbt,
        "blocks": blocks,
        "entities": List[Compound]([]),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    root.save(path, gzipped=True)


def validate(lab: Lab) -> None:
    states = [state.name for state, _ in lab.blocks.values()]
    counts = {name: states.count(name) for name in set(states)}
    loot_count = sum(1 for _, nbt in lab.blocks.values() if nbt and "LootTable" in nbt)
    spawner_count = counts.get("opusvsexe:dormant_spawner", 0)
    keypad_count = counts.get("opusvsexe:sequence_keypad", 0)
    required = {
        "surface": (0, 0, 0), "security": (18, -14, 0), "decontamination": (28, -14, 0),
        "lab": (0, -27, 0), "generator": (-28, -39, -18), "resonator": (2, -56, 0),
        "archive": (-29, -67, -14), "escape": (53, 1, 43),
    }
    for name, (x, y, z) in required.items():
        state = lab.blocks.get(lab.absolute(x, y, z), (None, None))[0]
        if state is None or state == AIR:
            raise ValueError(f"required K-17 landmark is missing: {name} at {(x, y, z)}")
    if loot_count != 32:
        raise ValueError(f"K-17 container contract is 32, got {loot_count}")
    if spawner_count != 10:
        raise ValueError(f"K-17 encounter contract is 10, got {spawner_count}")
    encounter_ids = [str(nbt["entity_id"]) for state, nbt in lab.blocks.values()
                     if state == SPAWNER and nbt]
    if encounter_ids.count("opusvsexe:haiku_4") != 1 or encounter_ids.count("opusvsexe:haiku_5") != 1:
        raise ValueError("K-17 must contain exactly one Haiku-4 and one Haiku-5 encounter")
    if keypad_count != 4:
        raise ValueError(f"K-17 keypad contract is 4, got {keypad_count}")
    forbidden = {"minecraft:structure_block", "minecraft:jigsaw"}
    if forbidden.intersection(counts):
        raise ValueError("structure markers leaked into K-17")
    print(f"K-17 template: {WIDTH}x{HEIGHT}x{DEPTH}; {len(lab.blocks)} explicit blocks; "
          f"{len(counts)} block types; {loot_count} containers; {spawner_count} encounters; {keypad_count} keypads")


if __name__ == "__main__":
    lab = build()
    validate(lab)
    write_template(lab, OUTPUTS[0])
    copyfile(OUTPUTS[0], OUTPUTS[1])
    for output in OUTPUTS:
        print(output.relative_to(ROOT))
