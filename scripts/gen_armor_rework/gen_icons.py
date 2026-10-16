#!/usr/bin/env python3
"""Item icons for all six reworked armor sets (16x16 pixel art, set palettes).
Run from repo root: python3 scripts/gen_armor_rework/gen_icons.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import A, h01, mixc, shadec
from PIL import Image

# palette shortcuts per set: (main, dark, light, trim, accent)
SETS = {
    'fire':        ((46, 46, 54), (30, 30, 37), (66, 66, 78), (26, 22, 31), (216, 67, 21)),
    'fire_demonic': ((26, 26, 28), (14, 14, 16), (51, 51, 58), (92, 22, 22), (232, 118, 20)),
    'briarweave':  ((46, 35, 26), (30, 22, 16), (66, 50, 36), (58, 42, 30), (74, 82, 50)),
    'dark_forest': ((25, 20, 32), (15, 12, 20), (38, 30, 48), (46, 36, 28), (139, 92, 246)),
    'parthenon':   ((232, 226, 212), (206, 198, 182), (244, 241, 232), (201, 168, 92), (255, 244, 214)),
    'aerie_bronze': ((138, 106, 58), (92, 69, 36), (201, 168, 92), (74, 51, 32), (122, 30, 30)),
}

ITEMS = ['helmet', 'chestplate', 'leggings', 'boots']


def canvas():
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    acc = img.load()

    def px(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            acc[x, y] = c

    return img, px


def rect(px, x0, y0, w, h, c):
    for j in range(h):
        for i in range(w):
            px(x0 + i, y0 + j, c)


def edge_shade(px, x0, y0, w, h, main, dk, hi):
    """Block with light top-left edge, dark bottom-right edge."""
    rect(px, x0, y0, w, h, main)
    for i in range(w):
        px(x0 + i, y0, hi)
    for j in range(h):
        px(x0, y0 + j, mixc(hi, main, 0.5))
        px(x0 + w - 1, y0 + j, dk)
    for i in range(w):
        px(x0 + i, y0 + h - 1, dk)


def draw_helmet(px, main, dk, hi, trim, accent):
    edge_shade(px, 4, 3, 8, 7, main, dk, hi)          # dome
    rect(px, 5, 2, 6, 1, hi)                          # crown ridge
    rect(px, 3, 5, 10, 2, trim)                       # brow band
    rect(px, 6, 8, 4, 1, accent)                      # visor slit
    rect(px, 4, 10, 8, 2, trim)                       # cheek/jaw frame
    rect(px, 5, 12, 6, 1, dk)                         # jaw bottom


def draw_chest(px, main, dk, hi, trim, accent):
    edge_shade(px, 3, 3, 10, 8, main, dk, hi)         # torso
    rect(px, 2, 3, 2, 6, trim)                        # shoulders
    rect(px, 12, 3, 2, 6, trim)
    rect(px, 6, 5, 4, 3, accent if accent != trim else mixc(main, hi, 0.5))  # core
    rect(px, 7, 6, 2, 1, shadec(accent, 1.4))
    rect(px, 4, 11, 8, 2, trim)                       # belt
    rect(px, 7, 11, 2, 2, hi)                         # buckle


def draw_legs(px, main, dk, hi, trim, accent):
    edge_shade(px, 4, 2, 3, 7, main, dk, hi)          # left thigh
    edge_shade(px, 9, 2, 3, 7, main, dk, hi)          # right thigh
    rect(px, 3, 3, 10, 1, trim)                       # belt line
    rect(px, 4, 9, 3, 5, mixc(main, dk, 0.4))         # shins
    rect(px, 9, 9, 3, 5, mixc(main, dk, 0.4))
    rect(px, 4, 9, 3, 1, accent)
    rect(px, 9, 9, 3, 1, accent)


def draw_boots(px, main, dk, hi, trim, accent):
    edge_shade(px, 3, 6, 4, 7, main, dk, hi)          # left boot
    edge_shade(px, 9, 6, 4, 7, main, dk, hi)          # right boot
    rect(px, 2, 12, 6, 2, trim)                       # soles
    rect(px, 8, 12, 6, 2, trim)
    rect(px, 3, 6, 4, 1, accent)
    rect(px, 9, 6, 4, 1, accent)


DRAW = {'helmet': draw_helmet, 'chestplate': draw_chest,
        'leggings': draw_legs, 'boots': draw_boots}


def main():
    out = os.path.join(A, 'textures/item')
    os.makedirs(out, exist_ok=True)
    for set_name, pal in SETS.items():
        for piece in ITEMS:
            img, px = canvas()
            DRAW[piece](px, *pal)
            # subtle per-set pixel noise
            p = img.load()
            for y in range(16):
                for x in range(16):
                    c = p[x, y]
                    if c[3] > 0 and h01(x, y, hash(set_name) & 255) > 0.9:
                        p[x, y] = mixc(c, pal[2], 0.35)
            img.save(os.path.join(out, f'{set_name}_{piece}.png'))
    print('24 item icons saved')


if __name__ == '__main__':
    main()
