#!/usr/bin/env python3
"""Regenerates the daisho item textures (katana.png = Steel Katana/short,
long_katana.png = Long Katana) from explicit pixel row specs.

Design source: concepts/provmt/katana_daisho.md (daisho concept art rework).
Rules: 32x32 RGBA, tip up, edge left, stepped curve, thin irregular hamon,
brass habaki, round iron tsuba, black diamond-wrapped tsuka with brass menuki.
No AA, no gradients, no noise; palette-locked (see PALETTE)."""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "src", "main", "resources", "assets", "opusvsexe", "textures", "item")

PALETTE = {
    ".": (0, 0, 0, 0),
    "K": (15, 15, 18, 255),      # black tsuka-ito wrap
    "I": (35, 36, 39, 255),      # dark iron (tsuba/fuchi/kashira)
    "h": (69, 71, 75, 255),      # iron highlight (top-left rim)
    "d": (23, 24, 26, 255),      # iron shadow (bottom-right rim)
    "g": (59, 61, 67, 255),      # ray-skin underlayer in wrap openings
    "B": (166, 142, 85, 255),    # muted brass
    "b": (119, 101, 59, 255),    # brass shadow
    "L": (194, 175, 124, 255),   # brass highlight
    "S": (95, 100, 108, 255),    # steel dark (spine)
    "M": (139, 144, 152, 255),   # steel mid (blade body)
    "E": (193, 199, 206, 255),   # steel light (cutting edge)
    "W": (243, 245, 247, 255),   # polished silver flash (tip)
    "H": (183, 189, 197, 255),   # hamon line (non-glowing, subtle)
}

# Steel Katana (short, wakizashi role): silhouette y3..y28, blade 15, handle 7.
# One gentle curve step at y11; hamon wave = H pixel in the edge band every 3rd row.
SHORT = [
    (10, "W"),                                    # y3  kissaki
    (10, "ES"),                                   # y4
    (10, "EMS"), (10, "EMS"),                     # y5-6
    (10, "EHS"), (10, "EMS"),                     # y7-8  hamon crest
    (10, "EMMS"), (10, "EMMS"),                   # y9-10 (blade widens to 4 px)
    (11, "EHMS"), (11, "EMMS"),                   # y11-12 (curve step)
    (11, "EHMS"), (11, "EMMS"),                   # y13-14 hamon crest
    (11, "EMMS"), (11, "EMMS"),                   # y15-16
    (11, "EMMS"),                                 # y17 blade base
    (11, "LBbb"),                                 # y18 habaki (brass collar)
    (12, "hId"),                                  # y19 tsuba top
    (11, "hIIId"),                                # y20 tsuba waist (round)
    (12, "IId"),                                  # y21 tsuba bottom
    (12, "IId"),                                  # y22 fuchi
    (12, "KKK"),                                  # y23 tsuka
    (12, "KgK"),                                  # y24 wrap opening
    (12, "KLK"),                                  # y25 menuki (brass)
    (12, "KgK"), (12, "KKK"),                     # y26-27
    (12, "IId"),                                  # y28 kashira
]

# Long Katana: silhouette y0..y31, blade 20, two-hand handle 8, 2 menuki.
LONG = [
    (9, "W"),                                     # y0  kissaki
    (9, "ES"), (9, "ES"),                         # y1-2
    (9, "EMS"), (9, "EMS"),                       # y3-4
    (9, "EHS"), (9, "EMS"),                       # y5-6  hamon crest
    (9, "EMS"), (9, "EMSS"),                      # y7-8  (blade widens to 4 px)
    (10, "EMMS"), (10, "EHMS"),                   # y9-10 (curve step)
    (10, "EMMS"), (10, "EMMS"),                   # y11-12
    (10, "EHMS"), (10, "EMMS"),                   # y13-14 hamon crest
    (10, "EMMS"), (10, "EMSS"),                   # y15-16 (curve step, widen)
    (11, "EMMS"), (11, "EHMS"),                   # y17-18
    (11, "EMMS"),                                 # y19 blade base
    (11, "LBbb"),                                 # y20 habaki
    (12, "hId"),                                  # y21 tsuba top
    (11, "hIIId"),                                # y22 tsuba waist (round)
    (12, "IId"),                                  # y23 tsuba bottom
    (12, "IId"),                                  # y24 fuchi
    (12, "KKK"),                                  # y25 tsuka
    (12, "KgK"),                                  # y26 wrap opening
    (12, "KLK"),                                  # y27 menuki 1
    (12, "KgK"), (12, "KKK"),                     # y28-29
    (12, "KgK"),                                  # y30 wrap opening
    (12, "IId"),                                  # y31 kashira
]


def build(spec, name):
    img = Image.new("RGBA", (32, 32), PALETTE["."])
    for y, (x, pattern) in enumerate(spec):
        for i, ch in enumerate(pattern):
            assert ch in PALETTE, f"{name}: unknown char {ch!r}"
            img.putpixel((x + i, y), PALETTE[ch])
    return img


# Sprite must be diagonal (tip top-right, handle bottom-left) like vanilla
# swords and this mod's own katana_op/refined/gold; vertical -> held wrong.
def shear(img):
    w, h = img.size
    out = Image.new("RGBA", (w, h), PALETTE["."])
    rows = [y for y in range(h) if any(img.getpixel((x, y))[3] > 10 for x in range(w))]
    top, bot = min(rows), max(rows)
    span = max(1, bot - top)
    for y in range(top, bot + 1):
        # tip (top) -> far +x, handle (bottom) -> far -x; ~22 px drift total
        shift = round(22.0 * (bot - y) / span) - 8
        for x in range(w):
            px = img.getpixel((x, y))
            if px[3] > 10 and 0 <= x + shift < w:
                out.putpixel((x + shift, y), px)
    return out


def main():
    os.makedirs(ROOT, exist_ok=True)
    # FLIP_LEFT_RIGHT: daisho art is drawn from top-left to bottom-right, which
    # renders mirrored vs vanilla sword (tip top-right, handle bottom-left) and
    # makes the tsuka face forward in hand; flip to match vanilla orientation.
    # SHEAR: run the blade diagonally (tip top-right) so it sits like a normal
    # sword in hand (the two-axis handheld rotation only "looks right" on a
    # diagonal sprite, as confirmed against katana_op/refined/gold + vanilla).
    katana = build(SHORT, "katana").transpose(Image.FLIP_LEFT_RIGHT)
    katana = shear(katana)
    katana.save(os.path.join(ROOT, "katana.png"))
    long_katana = build(LONG, "long_katana").transpose(Image.FLIP_LEFT_RIGHT)
    long_katana = shear(long_katana)
    long_katana.save(os.path.join(ROOT, "long_katana.png"))
    print("wrote katana.png and long_katana.png (32x32)")


if __name__ == "__main__":
    main()
