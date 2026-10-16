#!/usr/bin/env python3
"""Part III visual-only rework: fresh sprites for the 13 remaining items.

Master prompts are VISUAL-ONLY (§17/18/26/28): edit resource files in place,
keep registry IDs, classes and gameplay untouched. Per prompt §2/§8/§14/§16
these small ingredients stay lightweight 2D icons (no forced GeckoLib).

Targets (all 32x32 RGBA unless noted):
  textures/item: shade_silk, moonwing_membrane, moonflower_heart,
    rootbound_eye, briarweave, paradise_fruit, cloud_fleece,
    aerie_bronze_ingot, seraphic_pinions, ruby_halo_shard,
    paradise_sapling, fire_bean
  textures/block/paradise/paradise_sapling.png (32x32 cross)
  textures/block/ember_sapling.png (16x16 cross)
Old PNGs are backed up to build/tool_backup/ before overwrite.
"""
import os
import shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ITEM = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe", "textures", "item")
BLOCK = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe", "textures", "block")
BACKUP = os.path.join(ROOT, "build", "tool_backup")

# ---------------------------------------------------------------- palettes
DF_CHAR = (38, 32, 48, 255)
DF_DEEP = (22, 18, 30, 255)
DF_PURPLE = (122, 88, 180, 255)
DF_PURPLE_LT = (172, 142, 232, 255)
DF_MOON = (212, 236, 250, 255)
DF_THORN = (62, 52, 72, 255)
DF_BARK = (76, 60, 68, 255)
DF_BARK_DK = (44, 34, 42, 255)
DF_LINE = (14, 11, 20, 255)

PAR_IVORY = (240, 234, 214, 255)
PAR_IVORY_SH = (212, 202, 174, 255)
PAR_GOLD = (214, 168, 62, 255)
PAR_GOLD_LT = (246, 220, 140, 255)
PAR_GOLD_DK = (148, 106, 44, 255)
PAR_RUBY = (190, 44, 52, 255)
PAR_RUBY_LT = (242, 122, 122, 255)
PAR_LEAF = (148, 198, 128, 255)
PAR_LEAF_DK = (92, 140, 88, 255)
PAR_LINE = (88, 70, 44, 255)

HELL_CHAR = (24, 18, 20, 255)
HELL_CHAR2 = (48, 32, 30, 255)
HELL_CRUST = (74, 46, 38, 255)
HELL_EMBER = (255, 110, 20, 255)
HELL_HL = (255, 200, 90, 255)
HELL_WH = (255, 242, 212, 255)
HELL_LINE = (8, 6, 8, 255)


def new(size=32):
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def outline(im, color):
    """1px outline around opaque mass (vanilla icon readability)."""
    w, h = im.size
    px = im.load()
    seed = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] > 0]
    for x, y in seed:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                px[nx, ny] = color


def sparkle(d, x, y, color, r=3):
    d.line([x - r, y, x + r, y], fill=color)
    d.line([x, y - r, x, y + r], fill=color)
    d.point((x, y), fill=(255, 255, 255, 255))


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(4))
        d.line([x0, y, x1, y], fill=c)


# ================================================================ DARK FOREST
def paint_shade_silk():
    im, d = new(), None
    im = new()
    d = ImageDraw.Draw(im)
    # folded skein: three stacked rounded bands, charcoal -> purple
    bands = [(8, 9, 24, 13, DF_CHAR), (7, 14, 25, 18, (52, 40, 74, 255)), (8, 19, 24, 23, DF_DEEP)]
    for x0, y0, x1, y1, col in bands:
        d.rounded_rectangle([x0, y0, x1, y1], radius=2, fill=col)
    # moonlit sheen on top band
    d.line([9, 9, 23, 9], fill=DF_MOON)
    d.line([8, 14, 24, 14], fill=DF_PURPLE_LT)
    # fiber striations
    for x in (11, 15, 19, 22):
        d.line([x, 15, x, 17], fill=DF_PURPLE)
    # loose threads curling off bottom-right
    d.line([20, 23, 24, 27], fill=DF_PURPLE_LT)
    d.line([22, 23, 27, 26], fill=DF_CHAR)
    d.line([16, 23, 18, 28], fill=DF_PURPLE)
    outline(im, DF_LINE)
    return im


def paint_moonwing_membrane():
    im = new()
    d = ImageDraw.Draw(im)
    # wing fragment: dark-violet translucent triangle
    d.polygon([(4, 26), (7, 5), (28, 20)], fill=(64, 44, 104, 255))
    d.polygon([(7, 8), (6, 24), (24, 19)], fill=(84, 60, 132, 255))
    # organic veining from base corner
    for x1, y1 in ((24, 18), (18, 10), (12, 8), (20, 22)):
        d.line([5, 25, x1, y1], fill=DF_PURPLE_LT)
    d.line([5, 25, 27, 20], fill=DF_MOON)
    # lunar glow accents
    d.ellipse([19, 15, 22, 18], fill=DF_MOON)
    d.ellipse([12, 17, 14, 19], fill=DF_PURPLE_LT)
    outline(im, DF_LINE)
    return im


def paint_moonflower_heart():
    im = new()
    d = ImageDraw.Draw(im)
    # six petal lobes, deep purple
    import math
    cx, cy = 16, 16
    for i in range(6):
        a = math.pi * i / 3
        px, py = cx + int(9 * math.cos(a)), cy + int(9 * math.sin(a))
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(86, 52, 140, 255))
    # dark organic casing ring
    d.ellipse([8, 8, 24, 24], fill=DF_DEEP)
    d.ellipse([10, 10, 22, 22], fill=(52, 40, 92, 255))
    # luminous magical center
    d.ellipse([12, 12, 20, 20], fill=DF_MOON)
    d.ellipse([14, 14, 18, 18], fill=(255, 255, 255, 255))
    sparkle(d, 23, 8, DF_PURPLE_LT, 2)
    outline(im, DF_LINE)
    return im


def paint_rootbound_eye():
    im = new()
    d = ImageDraw.Draw(im)
    # dark organic mass
    d.ellipse([7, 4, 25, 28], fill=(30, 24, 38, 255))
    # root wraps
    d.line([7, 10, 25, 14], fill=DF_BARK, width=3)
    d.line([7, 22, 25, 18], fill=DF_BARK_DK, width=3)
    d.line([8, 11, 24, 15], fill=DF_THORN)
    # supernatural iris + pupil + glint
    d.ellipse([11, 11, 21, 21], fill=DF_PURPLE)
    d.ellipse([12, 12, 20, 20], fill=(150, 110, 220, 255))
    d.ellipse([14, 14, 18, 18], fill=(10, 8, 16, 255))
    d.point((15, 15), fill=DF_MOON)
    # thorn nubs on rim
    for x, y in ((7, 6), (25, 6), (5, 16), (27, 16), (9, 27), (23, 27)):
        d.point((x, y), fill=DF_THORN)
    outline(im, DF_LINE)
    return im


def paint_briarweave():
    # Briarweave MUST read as woven gloomwood bark: exact log palette —
    # near-black plum base (20,16,31), dark plum strips (48,35,62), mauve
    # highlights (72,52,82), moss-teal accents (42,79,56).
    GLOOM_BASE = (20, 16, 31, 255)
    GLOOM_PLUM = (48, 35, 62, 255)
    GLOOM_MAUVE = (72, 52, 82, 255)
    GLOOM_MOSS = (42, 79, 56, 255)
    GLOOM_MOSS_LT = (86, 138, 104, 255)
    im = new()
    d = ImageDraw.Draw(im)
    # woven bark strips: vertical dark lengths, over/under alternating
    for i in range(4):
        for j in range(4):
            x0, y0 = 5 + i * 6, 5 + j * 6
            col = GLOOM_PLUM if (i + j) % 2 == 0 else GLOOM_BASE
            d.rectangle([x0, y0, x0 + 5, y0 + 5], fill=col)
            d.line([x0, y0, x0 + 5, y0], fill=GLOOM_MAUVE)
            d.line([x0, y0, x0, y0 + 5], fill=GLOOM_BASE)
    # moss-teal binding threads (like the log's moss bands)
    d.line([5, 11, 28, 11], fill=GLOOM_MOSS)
    d.line([5, 22, 28, 22], fill=GLOOM_MOSS)
    d.line([5, 12, 28, 12], fill=GLOOM_MOSS_LT)
    # bark thorns: mauve spikes, moss-lit tip
    for x, y, dx, dy in ((5, 8, -2, -1), (27, 14, 2, -1), (10, 27, -1, 2), (22, 5, 1, -2)):
        d.line([x, y, x + dx, y + dy], fill=GLOOM_MAUVE)
        d.point((x + dx, y + dy), fill=GLOOM_MOSS_LT)
    outline(im, GLOOM_BASE)
    return im


def paint_sunfeather():
    # Sunfeather concept (see concepts/sunfeather_rework.md): a Sunfinch
    # flight feather — golden vane in the bird's own golds (242,185,59 /
    # 218,166,53 / bronze 202,111,28 / deep 161,88,24), pale sky-cyan quill
    # (191,233,239, the finch's wing accent), one ruby glint at the vane
    # base for the Paradise family. Diagonal pose, quill bottom-left.
    GOLD_LT = (242, 185, 59, 255)
    GOLD = (218, 166, 53, 255)
    BRONZE = (202, 111, 28, 255)
    BRONZE_DK = (161, 88, 24, 255)
    QUILL = (191, 233, 239, 255)
    im = new()
    d = ImageDraw.Draw(im)
    # vane: golden leaf around the upper shaft
    d.polygon([(13, 24), (15, 6), (19, 3), (24, 6), (22, 22), (17, 27)], fill=GOLD)
    d.polygon([(15, 20), (16, 8), (19, 5), (22, 8), (20, 20)], fill=GOLD_LT)
    d.line([13, 24, 15, 6], fill=BRONZE, width=2)
    d.line([22, 22, 24, 6], fill=BRONZE)
    # barb slits
    for x0, y0, x1, y1 in ((15, 12, 12, 10), (21, 14, 24, 12), (15, 18, 12, 17)):
        d.line([x0, y0, x1, y1], fill=BRONZE_DK)
    # shaft + cyan quill
    d.line([17, 27, 19, 5], fill=PAR_IVORY)
    d.line([12, 28, 17, 22], fill=QUILL, width=2)
    d.point((12, 28), fill=(255, 255, 255, 255))
    # ruby glint at vane base
    d.ellipse([15, 21, 18, 24], fill=PAR_RUBY)
    d.point((16, 22), fill=PAR_RUBY_LT)
    sparkle(d, 24, 4, GOLD_LT, 2)
    outline(im, PAR_LINE)
    return im


# ================================================================ PARADISE
def paint_paradise_fruit():
    im = new()
    d = ImageDraw.Draw(im)
    # divine apple: pale gold body
    d.ellipse([7, 9, 25, 27], fill=PAR_GOLD)
    d.ellipse([9, 11, 23, 26], fill=PAR_GOLD_LT)
    d.ellipse([10, 17, 22, 26], fill=(232, 190, 100, 255))
    # top indent + stem + leaf
    d.line([16, 9, 16, 5], fill=PAR_GOLD_DK, width=2)
    d.ellipse([17, 4, 24, 9], fill=PAR_LEAF)
    d.line([18, 6, 22, 6], fill=PAR_LEAF_DK)
    # ruby accent + halo sparkle
    d.ellipse([10, 13, 14, 17], fill=PAR_RUBY)
    d.ellipse([11, 13, 12, 15], fill=PAR_RUBY_LT)
    sparkle(d, 22, 20, (255, 255, 255, 255), 2)
    sparkle(d, 6, 6, PAR_GOLD_LT, 2)
    outline(im, PAR_LINE)
    return im


def paint_cloud_fleece():
    im = new()
    d = ImageDraw.Draw(im)
    # heavenly wool puff: overlapping soft circles
    for x, y, r in ((12, 18, 7), (19, 17, 8), (15, 12, 6), (22, 21, 5), (9, 22, 5)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=PAR_IVORY)
    d.ellipse([10, 20, 22, 26], fill=PAR_IVORY_SH)
    # subtle gold warmth on top
    for x, y in ((13, 12), (17, 10), (21, 14), (11, 16)):
        d.point((x, y), fill=PAR_GOLD_LT)
    # stray fibers
    d.line([24, 20, 28, 18], fill=PAR_IVORY)
    d.line([8, 24, 5, 27], fill=PAR_IVORY_SH)
    outline(im, PAR_LINE)
    return im


def paint_aerie_bronze_ingot():
    im = new()
    d = ImageDraw.Draw(im)
    # refined trapezoid ingot
    d.polygon([(6, 24), (10, 10), (22, 10), (26, 24)], fill=(176, 124, 58, 255))
    d.polygon([(8, 22), (11, 12), (21, 12), (24, 22)], fill=(212, 160, 88, 255))
    d.polygon([(11, 12), (21, 12), (19, 10), (13, 10)], fill=PAR_GOLD_LT)
    # sacred stamp: diamond + line
    d.polygon([(16, 15), (18, 18), (16, 21), (14, 18)], fill=PAR_GOLD_DK)
    d.point((16, 18), fill=PAR_GOLD_LT)
    d.line([12, 23, 20, 23], fill=PAR_GOLD_DK)
    outline(im, PAR_LINE)
    return im


def paint_seraphic_pinions():
    im = new()
    d = ImageDraw.Draw(im)
    # three holy feathers fanned
    for dx, tilt in ((-6, -14), (0, 0), (6, 14)):
        cx = 16 + dx
        d.line([cx, 27, cx + tilt // 4, 7], fill=PAR_GOLD, width=2)
        d.polygon([(cx - 3, 26), (cx - 4 + tilt // 4, 8), (cx + tilt // 4, 6),
                   (cx + 4 + tilt // 4, 8), (cx + 3, 26)], fill=PAR_IVORY)
        d.line([cx - 3, 24, cx - 4 + tilt // 4, 10], fill=PAR_IVORY_SH)
        d.point((cx + tilt // 4, 7), fill=PAR_GOLD_LT)
    sparkle(d, 25, 6, PAR_GOLD_LT, 2)
    outline(im, PAR_LINE)
    return im


def paint_ruby_halo_shard():
    im = new()
    d = ImageDraw.Draw(im)
    # sacred ruby fragment with gold celestial framing
    d.polygon([(16, 4), (25, 22), (7, 22)], fill=PAR_RUBY)
    d.polygon([(16, 7), (22, 20), (10, 20)], fill=(214, 70, 78, 255))
    d.polygon([(16, 9), (19, 18), (13, 18)], fill=PAR_RUBY_LT)
    # gold frame along left/right edges
    d.line([16, 4, 7, 22], fill=PAR_GOLD_LT, width=2)
    d.line([16, 4, 25, 22], fill=PAR_GOLD, width=2)
    d.line([7, 22, 25, 22], fill=PAR_GOLD_DK, width=2)
    sparkle(d, 16, 14, (255, 255, 255, 255), 3)
    # halo arc dots
    for x, y in ((9, 7), (23, 7), (6, 12)):
        d.point((x, y), fill=PAR_GOLD_LT)
    outline(im, PAR_LINE)
    return im


def paint_paradise_sapling_item():
    im = new()
    d = ImageDraw.Draw(im)
    # elegant ivory-gold trunk
    d.rectangle([14, 14, 18, 28], fill=PAR_GOLD)
    d.line([14, 14, 14, 28], fill=PAR_GOLD_LT)
    d.line([18, 14, 18, 28], fill=PAR_GOLD_DK)
    # sacred bright crown
    for x, y, r, col in ((16, 9, 6, PAR_LEAF), (9, 13, 4, PAR_LEAF),
                         (23, 13, 4, PAR_LEAF), (16, 6, 3, PAR_GOLD_LT),
                         (12, 10, 2, PAR_IVORY), (20, 10, 2, PAR_IVORY)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.line([9, 13, 23, 13], fill=PAR_LEAF_DK)
    sparkle(d, 25, 5, PAR_GOLD_LT, 2)
    outline(im, PAR_LINE)
    return im


def paint_paradise_sapling_block():
    im = new(32)
    d = ImageDraw.Draw(im)
    # taller trunk for the cross plane
    d.rectangle([14, 12, 18, 31], fill=PAR_GOLD)
    d.line([14, 12, 14, 31], fill=PAR_GOLD_LT)
    d.line([18, 12, 18, 31], fill=PAR_GOLD_DK)
    # fuller ivory-gold crown
    for x, y, r, col in ((16, 10, 8, PAR_LEAF), (7, 14, 5, PAR_LEAF),
                         (25, 14, 5, PAR_LEAF), (11, 6, 4, PAR_GOLD_LT),
                         (21, 6, 4, PAR_GOLD_LT), (16, 4, 3, PAR_IVORY),
                         (10, 11, 2, PAR_IVORY), (22, 11, 2, PAR_IVORY)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.line([6, 14, 26, 14], fill=PAR_LEAF_DK)
    return im


# ================================================================ HELL
def paint_fire_bean():
    im = new()
    d = ImageDraw.Draw(im)
    # lava-fruit pod: charred shell, molten interior glow
    d.ellipse([9, 3, 23, 29], fill=HELL_CHAR)
    d.ellipse([11, 5, 21, 27], fill=HELL_CHAR2)
    # pointed tip
    d.polygon([(13, 5), (19, 5), (16, 1)], fill=HELL_CRUST)
    # molten cracks: dark red halo -> orange core -> hot peaks
    for x in (14, 16, 18):
        d.line([x, 7, x, 26], fill=(120, 30, 12, 255))
    for x in (14, 16, 18):
        d.line([x, 9, x, 24], fill=HELL_EMBER)
    d.line([16, 8, 16, 25], fill=HELL_HL)
    for y in (10, 16, 22):
        d.point((16, y), fill=HELL_WH)
    # crust plates
    for x, y in ((11, 8), (21, 12), (10, 20), (22, 22)):
        d.point((x, y), fill=HELL_CRUST)
    outline(im, HELL_LINE)
    return im


def paint_ember_sapling_block():
    im = new(16)
    d = ImageDraw.Draw(im)
    # charred dark stems
    d.line([8, 15, 8, 6], fill=HELL_CHAR2, width=2)
    d.line([8, 10, 4, 6], fill=HELL_CHAR2)
    d.line([8, 10, 12, 5], fill=HELL_CHAR2)
    # ember-orange glow buds + hellish leaves
    for x, y in ((8, 5), (4, 5), (12, 4), (6, 8), (10, 8)):
        d.point((x, y), fill=HELL_EMBER)
    d.point((8, 4), fill=HELL_WH)
    d.point((12, 3), fill=HELL_HL)
    for x, y in ((3, 7), (13, 6), (5, 9), (11, 9)):
        d.point((x, y), fill=HELL_CRUST)
    return im


TARGETS = [
    ("item", "shade_silk", paint_shade_silk),
    ("item", "moonwing_membrane", paint_moonwing_membrane),
    ("item", "moonflower_heart", paint_moonflower_heart),
    ("item", "rootbound_eye", paint_rootbound_eye),
    ("item", "briarweave", paint_briarweave),
    ("item", "paradise_fruit", paint_paradise_fruit),
    ("item", "cloud_fleece", paint_cloud_fleece),
    ("item", "aerie_bronze_ingot", paint_aerie_bronze_ingot),
    ("item", "seraphic_pinions", paint_seraphic_pinions),
    ("item", "ruby_halo_shard", paint_ruby_halo_shard),
    ("item", "paradise_sapling", paint_paradise_sapling_item),
    ("item", "fire_bean", paint_fire_bean),
    ("item", "sunfeather", paint_sunfeather),
    (os.path.join("block", "paradise", "paradise_sapling"), None, paint_paradise_sapling_block),
    (os.path.join("block", "ember_sapling"), None, paint_ember_sapling_block),
]


def main():
    only = [a for a in os.sys.argv[1:] if not a.startswith("-")]
    os.makedirs(BACKUP, exist_ok=True)
    for sub, name, painter in TARGETS:
        if name is None:
            rel = sub + ".png"
            label = sub
        else:
            rel = os.path.join("item", name + ".png") if sub == "item" else None
            label = name
        if only and label not in only and (name or "") not in only:
            continue
        if sub == "item":
            path = os.path.join(ITEM, name + ".png")
        else:
            path = os.path.join(
                ROOT, "src", "main", "resources", "assets", "opusvsexe", "textures",
                sub + ".png")
        if os.path.exists(path):
            dst = os.path.join(BACKUP, os.path.basename(path))
            if not os.path.exists(dst):
                shutil.copy2(path, dst)
                print("backup:", dst)
        painter().save(path)
        print("painted:", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
