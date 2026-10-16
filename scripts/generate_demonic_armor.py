#!/usr/bin/env python3
"""Fire Demonic armor VISUAL-ONLY rework (concepts/Fire_Demonic_Armor_ULTRA_MAX_v2).

Hard rules: same registry IDs, same ArmorMaterial/stats/slots/recipes/
set-bonus logic. Only visuals change: layer textures + emissive maps +
item sprites, repainted to the concept-art bible (forged black volcanic
steel, burnt-crimson slabs, magma fissures with yellow-hot centers).
Geometry (LayerDefinition) is kept; existing files are backed up to
concepts/Fire_Demonic_Armor_ULTRA_MAX_v2/backup/ for rollback.

UVs are parsed from the real model sources, so paint always lands on the
faces the game samples (old textures left most islands transparent).
"""
import os
import re
import shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe")
CONCEPTS = os.path.join(ROOT, "concepts", "Fire_Demonic_Armor_ULTRA_MAX_v2", "backup")

HELMET_MODEL = os.path.join(ROOT, "src", "client", "java", "com", "opus", "ember",
                            "client", "model", "FireDemonicHelmetModel.java")
PLATE_MODEL = os.path.join(ROOT, "src", "client", "java", "com", "opus", "ember",
                           "client", "model", "FireDemonicPlateModel.java")
HELMET_LAYER_JAVA = os.path.join(ROOT, "src", "client", "java", "com", "opus", "ember",
                                 "client", "layer", "FireDemonicHelmetLayer.java")
PLATE_LAYER_JAVA = os.path.join(ROOT, "src", "client", "java", "com", "opus", "ember",
                                "client", "layer", "FireDemonicPlateLayer.java")

TEX_HELMET = os.path.join(ASSETS, "textures", "ember", "armor", "fire_demonic_helmet_layer.png")
TEX_HELMET_E = os.path.join(ASSETS, "textures", "ember", "armor", "fire_demonic_helmet_layer_emissive.png")
TEX_PLATE = os.path.join(ASSETS, "textures", "ember", "armor", "fire_demonic_plate_layer.png")
TEX_PLATE_E = os.path.join(ASSETS, "textures", "ember", "armor", "fire_demonic_plate_layer_emissive.png")
ITEM_TEX = {n: os.path.join(ASSETS, "textures", "item", "fire_demonic_%s.png" % n)
            for n in ("helmet", "chestplate", "leggings", "boots")}
ITEM_JSON = {n: os.path.join(ASSETS, "models", "item", "fire_demonic_%s.json" % n)
             for n in ("helmet", "chestplate", "leggings", "boots")}

# ---------------------------------------------------------------- bible
VOLC = (26, 22, 28, 255)
VOLC_DK = (12, 10, 14, 255)
VOLC_HL = (52, 46, 54, 255)
CRIMSON = (138, 30, 26, 255)
CRIMSON_DK = (84, 18, 20, 255)
CRIMSON_HL = (196, 70, 44, 255)
MAGMA = (255, 110, 20, 255)
MAGMA_HL = (255, 200, 90, 255)
MAGMA_WH = (255, 242, 210, 255)
MAGMA_DK = (120, 30, 12, 255)
SOOT = (8, 7, 9, 255)


def role_of(part):
    p = part.lower()
    if any(k in p for k in ("visor", "eye", "reactor", "core", "vent", "crest", "gem", "rune")):
        return "magma"
    if "horn" in p or "claw" in p or "spike" in p or "fang" in p:
        return "horn"
    if any(k in p for k in ("plate", "chest", "head", "helm", "crown", "pauldron", "greave",
                            "sabaton", "boot", "leg", "arm", "shoulder", "shell", "guard",
                            "buckle", "belt", "rib", "gauntlet", "thigh", "knee", "toe",
                            "wrist", "cheek", "jaw", "face")):
        return "crimson"
    return "volcanic"


BOX_RE = re.compile(
    r'addOrReplaceChild\("([^"]+)".*?\.texOffs\(\s*(\d+)\s*,\s*(\d+)\s*\)'
    r'\.addBox\(\s*([-\d.F]+)\s*,\s*([-\d.F]+)\s*,\s*([-\d.F]+)\s*,'
    r'\s*([-\d.F]+)\s*,\s*([-\d.F]+)\s*,\s*([-\d.F]+)', re.S)

PAIR_RE = re.compile(
    r'\.texOffs\(\s*(\d+)\s*,\s*(\d+)\s*\)\.addBox\(\s*([-\d.Ff]+)\s*,\s*([-\d.Ff]+)\s*,'
    r'\s*([-\d.Ff]+)\s*,\s*([-\d.Ff]+)\s*,\s*([-\d.Ff]+)\s*,\s*([-\d.Ff]+)')


def parse_boxes(path):
    # Split per addOrReplaceChild STATEMENT so empty structural parents can
    # never steal the UVs of the next real box (name attribution is exact,
    # and multi-box builders yield every box).
    src = open(path).read()
    out = []
    for stmt in src.split(";"):
        name = re.search(r'addOrReplaceChild\("([^"]+)"', stmt)
        if not name:
            continue
        for m in PAIR_RE.finditer(stmt):
            u, v = int(m.group(1)), int(m.group(2))
            dims = [int(round(float(m.group(i).rstrip("Ff")))) for i in (6, 7, 8)]
            out.append((name.group(1), u, v, *dims))
    return out


def islands(u, v, sx, sy, sz):
    # vanilla box-UV unfolded islands: (x, y, w, h)
    return [
        (u + sz, v, sx, sz),                    # top
        (u + sz + sx, v, sx, sz),               # bottom
        (u, v + sz, sz, sy),                    # west
        (u + sz, v + sz, sx, sy),               # north
        (u + sz + sx, v + sz, sz, sy),          # east
        (u + sz + sx + sz, v + sz, sx, sy),     # south
    ]


def paint_island(d, e, box, role, seed):
    import random
    rnd = random.Random(seed)
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    if role == "magma":
        for yy in range(y, y + h):
            t = (yy - y) / max(1, h - 1)
            if t < 0.35:
                c = MAGMA_WH if rnd.random() < 0.7 else MAGMA_HL
            elif t < 0.7:
                c = MAGMA_HL if rnd.random() < 0.5 else MAGMA
            else:
                c = MAGMA if rnd.random() < 0.5 else MAGMA_DK
            d.line([x, yy, x + w - 1, yy], fill=c)
        e.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255, 255))
    elif role == "horn":
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=VOLC_DK)
        if w >= 2 and h >= 2:
            d.line([x, y, x + w - 1, y], fill=VOLC_HL)
        # ember crack between segments
        if min(w, h) >= 2:
            cx = x + w // 2 + rnd.randrange(-1, 2)
            for yy in range(y, y + h):
                cx = max(x, min(x + w - 1, cx + rnd.randrange(-1, 2)))
                d.point((cx, yy), fill=MAGMA)
                if (yy + seed) % 5 == 0:
                    d.point((cx, yy), fill=MAGMA_HL)
    elif role == "crimson":
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=CRIMSON)
        d.line([x, y, x + w - 1, y], fill=CRIMSON_HL)
        d.line([x, y + h - 1, x + w - 1, y + h - 1], fill=CRIMSON_DK)
        d.line([x, y, x, y + h - 1], fill=CRIMSON_DK)
        if w >= 3 and h >= 3:
            d.rectangle([x + 1, y + 1, x + w - 2, y + h - 2], fill=(118, 26, 24, 255))
        for _ in range(max(1, w * h // 40)):
            px, py = x + rnd.randrange(w), y + rnd.randrange(h)
            d.point((px, py), fill=MAGMA if rnd.random() < 0.4 else CRIMSON_DK)
    else:  # volcanic joint shell
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=VOLC)
        if w >= 2 and h >= 2:
            d.line([x, y, x + w - 1, y], fill=VOLC_HL)
            d.line([x, y + h - 1, x + w - 1, y + h - 1], fill=SOOT)
        for _ in range(max(1, w * h // 60)):
            d.point((x + rnd.randrange(w), y + rnd.randrange(h)), fill=SOOT)


def paint_layer(model_path, out_tex, out_emissive):
    boxes = parse_boxes(model_path)
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    emi = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    e = ImageDraw.Draw(emi)
    seed = 0
    for part, u, v, sx, sy, sz in boxes:
        role = role_of(part)
        for isl in islands(u, v, sx, sy, sz):
            paint_island(d, e, isl, role, seed)
            seed += 1
    img.save(out_tex)
    emi.save(out_emissive)
    print("painted %s (%d boxes)" % (os.path.relpath(out_tex, ROOT), len(boxes)))


def outline(im, color):
    w, h = im.size
    px = im.load()
    seed = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] > 0]
    for x, y in seed:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                px[nx, ny] = color


def item_helmet():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([4, 5, 11, 13], fill=VOLC)          # dome
    d.rectangle([4, 5, 11, 7], fill=CRIMSON)        # crown slab
    d.rectangle([5, 9, 10, 10], fill=MAGMA)         # visor
    d.line([5, 9, 10, 9], fill=MAGMA_WH)
    d.polygon([(4, 5), (2, 0), (4, 0), (6, 5)], fill=VOLC_DK)   # horns
    d.polygon([(11, 5), (13, 0), (11, 0), (9, 5)], fill=VOLC_DK)
    d.point((3, 1), fill=MAGMA)
    d.point((12, 1), fill=MAGMA)
    d.rectangle([6, 13, 9, 14], fill=CRIMSON_DK)    # jaw
    outline(im, SOOT)
    return im


def item_chest():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([3, 2, 12, 13], fill=VOLC)          # torso
    d.rectangle([3, 2, 12, 4], fill=CRIMSON)        # collar slab
    d.rectangle([1, 3, 2, 8], fill=CRIMSON_DK)      # pauldrons
    d.rectangle([13, 3, 14, 8], fill=CRIMSON_DK)
    d.line([6, 5, 6, 11], fill=MAGMA, width=1)      # twin reactor vents
    d.line([9, 5, 9, 11], fill=MAGMA, width=1)
    d.point((6, 5), fill=MAGMA_WH)
    d.point((9, 5), fill=MAGMA_WH)
    d.rectangle([5, 11, 10, 13], fill=CRIMSON)      # waist lamellae
    d.line([5, 12, 10, 12], fill=CRIMSON_DK)
    outline(im, SOOT)
    return im


def item_legs():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x0 in (3, 9):
        d.rectangle([x0, 1, x0 + 3, 13], fill=VOLC)
        d.rectangle([x0, 1, x0 + 3, 3], fill=CRIMSON)
        d.rectangle([x0, 7, x0 + 3, 9], fill=CRIMSON_DK)
        d.point((x0 + 1, 5), fill=MAGMA)
    d.rectangle([3, 0, 12, 1], fill=CRIMSON)        # belt
    outline(im, SOOT)
    return im


def item_boots():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x0 in (3, 9):
        d.rectangle([x0, 6, x0 + 3, 12], fill=VOLC)
        d.rectangle([x0, 6, x0 + 3, 7], fill=CRIMSON)
        d.rectangle([x0, 11, x0 + 4, 13], fill=VOLC_DK)  # sabaton toe
        d.point((x0 + 1, 9), fill=MAGMA)
    outline(im, SOOT)
    return im


BACKUP_FILES = [HELMET_MODEL, PLATE_MODEL, HELMET_LAYER_JAVA, PLATE_LAYER_JAVA,
                TEX_HELMET, TEX_HELMET_E, TEX_PLATE, TEX_PLATE_E,
                *ITEM_TEX.values(), *ITEM_JSON.values()]


def main():
    os.makedirs(CONCEPTS, exist_ok=True)
    for path in BACKUP_FILES:
        if os.path.exists(path):
            dst = os.path.join(CONCEPTS, os.path.basename(path))
            if not os.path.exists(dst):
                shutil.copy2(path, dst)
                print("backup:", os.path.basename(path))
    paint_layer(HELMET_MODEL, TEX_HELMET, TEX_HELMET_E)
    paint_layer(PLATE_MODEL, TEX_PLATE, TEX_PLATE_E)
    for name, painter in (("helmet", item_helmet), ("chestplate", item_chest),
                          ("leggings", item_legs), ("boots", item_boots)):
        painter().save(ITEM_TEX[name])
        print("painted item:", name)


if __name__ == "__main__":
    main()
