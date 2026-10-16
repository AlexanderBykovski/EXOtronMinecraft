#!/usr/bin/env python3
"""Radio RMB blast VISUAL-ONLY rework (explosive-blast prompt).

The Radio item calls an airstrike (ExplosionEntity, 75 blocks, 150 damage);
all of that logic is untouched. Only the blast's look changes:
textures/entity/nuke.png (64x64, sampled across the whole sheet by the
existing box-UV geo) is repainted as an unstable blast-fungus burst —
white-hot core low, magma fissures mid, scorched spore-shell high, ember
pores throughout. Geometry, animation, sounds, timing, damage: intact.
Old texture is backed up to build/tool_backup/.
"""
import os
import random
import shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "opusvsexe",
                   "textures", "entity", "nuke.png")
BACKUP = os.path.join(ROOT, "build", "tool_backup")

WH = (255, 242, 210, 255)
HL = (255, 200, 90, 255)
MAGMA = (255, 110, 20, 255)
RED = (200, 60, 10, 255)
DARKRED = (120, 30, 12, 255)
CRUST = (60, 20, 14, 255)
SOOT = (25, 15, 16, 255)


def main():
    os.makedirs(BACKUP, exist_ok=True)
    dst = os.path.join(BACKUP, "nuke.png")
    if not os.path.exists(dst):
        shutil.copy2(TEX, dst)
        print("backup:", dst)
    rnd = random.Random(137)
    W, H = 64, 64
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # vertical blast gradient: white-hot core (bottom) -> scorched shell (top)
    for y in range(H):
        t = y / (H - 1)
        if t > 0.78:
            c = WH if rnd.random() < 0.75 else HL
        elif t > 0.62:
            c = HL if rnd.random() < 0.5 else MAGMA
        elif t > 0.45:
            c = MAGMA if rnd.random() < 0.5 else RED
        elif t > 0.28:
            c = RED if rnd.random() < 0.5 else DARKRED
        elif t > 0.12:
            c = DARKRED if rnd.random() < 0.6 else CRUST
        else:
            c = CRUST if rnd.random() < 0.7 else SOOT
        d.line([0, y, W - 1, y], fill=c)
    # glowing fissures rising through the burst
    for _ in range(9):
        x = rnd.randrange(2, W - 2)
        y = rnd.randrange(H - 20, H - 2)
        top = rnd.randrange(4, H // 2)
        while y > top:
            d.point((x, y), fill=MAGMA)
            if rnd.random() < 0.4:
                d.point((x, y), fill=HL)
            if rnd.random() < 0.15:
                d.point((x, y), fill=WH)
            x = max(0, min(W - 1, x + rnd.randrange(-1, 2)))
            y -= 1
        # dark halo around the fissure mouth
        d.point((max(0, x - 1), min(H - 1, y + 2)), fill=DARKRED)
    # ember pores / spore sparks, denser toward the hot base
    for _ in range(260):
        x, y = rnd.randrange(W), rnd.randrange(H)
        heat = 1.0 - y / H
        if rnd.random() < 0.25 + heat * 0.6:
            d.point((x, y), fill=WH if rnd.random() < heat * 0.5 else (HL if rnd.random() < 0.5 else MAGMA))
    # scorched blotches up top (rupturing cap shell)
    for _ in range(26):
        x, y = rnd.randrange(W), rnd.randrange(0, 20)
        r = rnd.randrange(1, 4)
        d.ellipse([x - r, y - r, x + r, y + r], fill=SOOT if rnd.random() < 0.7 else CRUST)
    im.save(TEX)
    print("painted:", os.path.relpath(TEX, ROOT))


if __name__ == "__main__":
    main()
