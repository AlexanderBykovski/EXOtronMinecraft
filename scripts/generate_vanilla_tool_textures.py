#!/usr/bin/env python3
"""Hand-authored 16×16 vanilla-style sprites for every held melee/tool item.

The generated concepts are deliberately used only as material references.  This
script contains the final pixel silhouettes so the game gets readable Minecraft
tools, not down-scaled concept art.  Run from the repository root:

    python3 scripts/generate_vanilla_tool_textures.py
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
PREVIEW = ROOT / "docs/assets/concepts/vanilla-tool-texture-sheet-2026-09-02.png"
SIZE = 16
TRANSPARENT = (0, 0, 0, 0)

# All families use one pixel of nearly-black outline; the four coloured entries
# are shadow, body, light, and signature respectively.  The short palette is a
# core vanilla constraint, not a renderer limitation.
FAMILIES = {
    "opus": {
        "outline": (29, 22, 39, 255), "handle": (42, 34, 51, 255),
        "shadow": (73, 39, 104, 255), "body": (119, 61, 164, 255),
        "light": (184, 109, 224, 255), "accent": (242, 153, 255, 255),
    },
    "fire": {
        "outline": (30, 22, 19, 255), "handle": (68, 45, 30, 255),
        "shadow": (76, 64, 57, 255), "body": (112, 103, 91, 255),
        "light": (165, 150, 127, 255), "accent": (239, 102, 36, 255),
    },
    "forest": {
        "outline": (25, 22, 34, 255), "handle": (61, 49, 43, 255),
        "shadow": (57, 43, 83, 255), "body": (90, 68, 129, 255),
        "light": (126, 102, 167, 255), "accent": (101, 222, 220, 255),
    },
    "parthenon": {
        "outline": (68, 58, 43, 255), "handle": (196, 179, 146, 255),
        "shadow": (161, 132, 73, 255), "body": (222, 192, 103, 255),
        "light": (248, 238, 211, 255), "accent": (78, 201, 210, 255),
    },
}

KATANAS = {
    "katana": ((26, 27, 31, 255), (66, 69, 75, 255), (137, 143, 151, 255), (219, 225, 229, 255), (178, 145, 77, 255)),
    "long_katana": ((24, 25, 29, 255), (66, 69, 75, 255), (144, 150, 158, 255), (231, 235, 238, 255), (176, 143, 75, 255)),
    "katana_op": ((29, 22, 39, 255), (70, 39, 104, 255), (126, 67, 171, 255), (209, 132, 245, 255), (238, 158, 255, 255)),
    "katana_gold": ((54, 42, 24, 255), (114, 79, 31, 255), (184, 133, 48, 255), (249, 210, 103, 255), (230, 104, 44, 255)),
    "katana_refined": ((31, 30, 44, 255), (73, 69, 96, 255), (145, 134, 174, 255), (221, 209, 243, 255), (121, 233, 240, 255)),
}


class Sprite:
    def __init__(self):
        self.cells = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    def pixel(self, x, y, colour):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.cells[y][x] = colour

    def line(self, x0, y0, x1, y1, colour):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.pixel(x0, y0, colour)
            if x0 == x1 and y0 == y1:
                return
            twice = 2 * err
            if twice >= dy:
                err += dy
                x0 += sx
            if twice <= dx:
                err += dx
                y0 += sy

    def points(self, points, colour):
        for x, y in points:
            self.pixel(x, y, colour)

    def render(self, outline):
        image = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
        for y in range(SIZE):
            for x in range(SIZE):
                if self.cells[y][x] is None:
                    continue
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ox, y + oy
                    if 0 <= nx < SIZE and 0 <= ny < SIZE and self.cells[ny][nx] is None:
                        image.putpixel((nx, ny), outline)
        for y in range(SIZE):
            for x in range(SIZE):
                if self.cells[y][x] is not None:
                    image.putpixel((x, y), self.cells[y][x])
        return image


def add_handle(sprite, p, end=(8, 9), long=False):
    start = (2, 14) if long else (3, 14)
    sprite.line(*start, *end, p["handle"])
    # Three intentional knots make a grip rather than a plain diagonal stick.
    sprite.points([(4, 13), (6, 11), (7, 10)], p["shadow"])
    sprite.pixel(start[0] - 1, start[1], p["accent"])


def make_tool(family, kind):
    p = FAMILIES[family]
    s = Sprite()
    if kind == "sword":
        add_handle(s, p, (7, 10))
        s.points([(5, 11), (6, 11), (6, 10), (7, 10), (7, 9), (8, 9), (8, 8),
                  (9, 8), (9, 7), (10, 7), (10, 6), (11, 6), (11, 5), (12, 5),
                  (12, 4), (13, 3)], p["body"])
        s.points([(6, 10), (7, 9), (8, 8), (9, 7), (10, 6), (11, 5), (12, 4)], p["light"])
        s.points([(5, 10), (6, 9), (7, 8)], p["shadow"])
        s.points([(4, 11), (5, 10), (6, 12)], p["accent"])
    elif kind == "pickaxe":
        add_handle(s, p, (9, 8))
        s.points([(7, 7), (8, 6), (9, 5), (10, 4), (11, 4), (12, 4), (13, 5),
                  (12, 5), (11, 5), (10, 6), (9, 7), (8, 8), (7, 8), (6, 8)], p["body"])
        s.points([(8, 6), (9, 5), (10, 4), (11, 4)], p["light"])
        s.points([(11, 5), (10, 6), (9, 7), (7, 8)], p["shadow"])
        s.pixel(9, 7, p["accent"])
    elif kind == "axe":
        add_handle(s, p, (8, 9))
        s.points([(7, 8), (8, 7), (9, 6), (10, 5), (10, 4), (11, 4), (12, 4),
                  (13, 5), (13, 6), (12, 7), (11, 8), (10, 8), (9, 9), (8, 9)], p["body"])
        s.points([(10, 4), (11, 4), (12, 5), (12, 6)], p["light"])
        s.points([(8, 8), (9, 8), (10, 7), (11, 7)], p["shadow"])
        s.pixel(10, 6, p["accent"])
    elif kind == "shovel":
        add_handle(s, p, (9, 8))
        s.points([(9, 8), (10, 7), (11, 6), (12, 5), (13, 5), (13, 6), (12, 7),
                  (11, 8), (10, 9), (9, 9), (8, 9)], p["body"])
        s.points([(11, 6), (12, 5), (13, 5)], p["light"])
        s.points([(9, 9), (10, 9), (11, 8)], p["shadow"])
        s.pixel(11, 7, p["accent"])
    elif kind == "hoe":
        add_handle(s, p, (9, 8))
        s.points([(8, 7), (9, 6), (10, 5), (11, 4), (12, 4), (13, 4), (13, 5),
                  (12, 5), (11, 5), (10, 6), (9, 7), (9, 8)], p["body"])
        s.points([(11, 4), (12, 4), (13, 4)], p["light"])
        s.points([(9, 7), (10, 6)], p["shadow"])
        s.pixel(10, 5, p["accent"])
    else:
        raise ValueError(kind)
    return s.render(p["outline"])


def make_warhammer():
    p = FAMILIES["opus"]
    s = Sprite()
    add_handle(s, p, (8, 9), long=True)
    s.points([(8, 8), (9, 7), (9, 6), (10, 5), (11, 5), (12, 5), (13, 6), (13, 7),
              (12, 8), (11, 8), (10, 8), (9, 9)], p["body"])
    s.points([(10, 5), (11, 5), (12, 6)], p["light"])
    s.points([(9, 8), (10, 8), (11, 7)], p["shadow"])
    s.points([(10, 6), (11, 6)], p["accent"])
    return s.render(p["outline"])


def make_katana(name, long=False):
    outline, shadow, body, light, accent = KATANAS[name]
    s = Sprite()
    # A stepped, one-pixel edge reads as a katana without abandoning vanilla's
    # diagonal held-item orientation.
    grip_start = (2, 14) if long else (3, 14)
    s.line(*grip_start, 7, 10, shadow)
    s.points([(4, 13), (6, 11)], outline)
    s.points([(6, 10), (7, 10), (7, 9), (8, 9), (8, 8), (9, 8), (9, 7), (10, 7),
              (10, 6), (11, 6), (11, 5), (12, 5), (12, 4), (13, 3)], body)
    s.points([(7, 9), (8, 8), (9, 7), (10, 6), (11, 5), (12, 4)], light)
    s.points([(5, 11), (6, 10), (6, 9), (7, 8)], shadow)
    s.points([(5, 12), (6, 11), (7, 10)], accent)
    if long:
        s.points([(9, 7), (10, 6), (11, 5)], body)
    return s.render(outline)


ASSETS = {
    "opus_warhammer": make_warhammer,
    "opus_pickaxe": lambda: make_tool("opus", "pickaxe"),
    "opus_axe": lambda: make_tool("opus", "axe"),
    "opus_shovel": lambda: make_tool("opus", "shovel"),
    "opus_hoe": lambda: make_tool("opus", "hoe"),
    "fire_sword": lambda: make_tool("fire", "sword"),
    "fire_pickaxe": lambda: make_tool("fire", "pickaxe"),
    "fire_axe": lambda: make_tool("fire", "axe"),
    "fire_shovel": lambda: make_tool("fire", "shovel"),
    "fire_hoe": lambda: make_tool("fire", "hoe"),
    "dark_forest_sword": lambda: make_tool("forest", "sword"),
    "dark_forest_pickaxe": lambda: make_tool("forest", "pickaxe"),
    "dark_forest_axe": lambda: make_tool("forest", "axe"),
    "dark_forest_shovel": lambda: make_tool("forest", "shovel"),
    "dark_forest_hoe": lambda: make_tool("forest", "hoe"),
    "parthenon_sword": lambda: make_tool("parthenon", "sword"),
    "parthenon_pickaxe": lambda: make_tool("parthenon", "pickaxe"),
    "parthenon_axe": lambda: make_tool("parthenon", "axe"),
    "parthenon_shovel": lambda: make_tool("parthenon", "shovel"),
    "parthenon_hoe": lambda: make_tool("parthenon", "hoe"),
    "katana": lambda: make_katana("katana"),
    "long_katana": lambda: make_katana("long_katana", long=True),
    "katana_op": lambda: make_katana("katana_op"),
    "katana_gold": lambda: make_katana("katana_gold"),
    "katana_refined": lambda: make_katana("katana_refined"),
}


def save_preview(images):
    columns, cell = 5, 96
    rows = (len(images) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell, rows * cell), (28, 28, 32, 255))
    for index, image in enumerate(images):
        x, y = (index % columns) * cell, (index // columns) * cell
        sheet.alpha_composite(image.resize((64, 64), Image.Resampling.NEAREST), (x + 16, y + 16))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW)


def write_handheld_models():
    """Remove oversized bespoke transforms and use Minecraft's tool transform."""
    for name in ASSETS:
        model = {
            "parent": "minecraft:item/handheld",
            "textures": {"layer0": f"opusvsexe:item/{name}"},
        }
        (MODELS / f"{name}.json").write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")


def main():
    images = []
    for name, build in ASSETS.items():
        image = build()
        assert image.size == (16, 16) and image.mode == "RGBA"
        image.save(ITEMS / f"{name}.png")
        images.append(image)
    write_handheld_models()
    save_preview(images)
    print(f"wrote {len(images)} 16x16 vanilla tool sprites/models and {PREVIEW.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
