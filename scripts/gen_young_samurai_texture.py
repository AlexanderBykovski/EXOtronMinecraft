#!/usr/bin/env python3
"""Regenerates textures/entity/japanese/young_samurai.png (128x128, single atlas).

Design source: concepts/provmt/young_samurai.md. Matches YoungSamuraiModel UV:
- vanilla base parts (head/body/arms/legs) painted fully (skin, indigo kosode, tabi)
- custom parts at their texOffs (hair, sode, collar, obi, hakama, armor, kote,
  shin, sandal, crest, scabbards+tsuka)
Pixel-art rules: nearest-neighbor, hard clusters, no AA/blur/gradients/noise,
consistent top-left light, palette-locked, transparency only where unused."""
import math
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "src", "main", "resources", "assets", "opusvsexe", "textures", "entity", "japanese")

PAL = {
    ".": (0, 0, 0, 0),
    # skin
    "S": (210, 169, 139, 255), "s": (194, 150, 120, 255), "N": (228, 192, 163, 255), "q": (168, 126, 98, 255),
    # hair (near-black blue-gray, no pure black)
    "H": (27, 29, 34, 255), "h": (42, 46, 54, 255), "e": (60, 65, 75, 255),
    # eyes / brows / mouth
    "B": (43, 27, 14, 255), "P": (16, 10, 5, 255), "m": (178, 126, 94, 255),
    # indigo kosode
    "I": (42, 52, 72, 255), "i": (29, 38, 54, 255), "l": (60, 76, 102, 255),
    # inner collar off-white
    "C": (231, 228, 218, 255), "c": (201, 196, 182, 255),
    # hakama charcoal
    "G": (59, 60, 64, 255), "g": (44, 45, 49, 255), "F": (84, 86, 92, 255),
    # lacquered armor (black-brown)
    "A": (41, 31, 27, 255), "a": (59, 46, 38, 255), "Q": (23, 16, 13, 255), "T": (87, 71, 55, 255),
    # iron
    "M": (35, 36, 39, 255), "R": (58, 60, 66, 255), "U": (74, 77, 83, 255),
    # brass
    "O": (166, 142, 85, 255), "o": (119, 101, 59, 255), "Y": (194, 175, 124, 255),
    # cords / leather
    "D": (106, 82, 40, 255), "d": (85, 64, 30, 255),
    # straw sandals
    "W": (181, 164, 118, 255), "w": (124, 111, 76, 255), "V": (207, 195, 158, 255),
    # plain black scabbard
    "K": (18, 19, 22, 255), "k": (35, 38, 43, 255),
}

img = Image.new("RGBA", (128, 128), PAL["."])


def px(x, y, ch):
    assert ch in PAL, ch
    img.putpixel((int(x), int(y)), PAL[ch])


def rect(x, y, w, h, ch):
    for j in range(int(math.ceil(h))):
        for i in range(int(math.ceil(w))):
            px(x + i, y + j, ch)


def faces(u, v, W, H, D):
    """Standard box UV faces for a W x H x D box with texOffs (u, v)."""
    return {
        "top": (u + D, v, W, D), "bottom": (u + D + W, v, W, D),
        "right": (u, v + D, D, H), "front": (u + D, v + D, W, H),
        "left": (u + D + W, v + D, D, H), "back": (u + 2 * D + W, v + D, W, H),
    }


def paint(box, painter):
    for name, (x, y, w, h) in faces(*box).items():
        for j in range(int(math.ceil(h))):
            for i in range(int(math.ceil(w))):
                px(x + i, y + j, painter(name, i, j, int(math.ceil(w)), int(math.ceil(h))))


# ---------------------------------------------------------------- vanilla base
def head_base():
    r = faces(0, 0, 8, 8, 8)
    # top: dark hair with lock streaks
    tx, ty, _, _ = r["top"]
    for j in range(8):
        for i in range(8):
            ch = "H"
            if (i + j) % 4 == 1:
                ch = "h"
            if i in (2, 6) and j > 4:
                ch = "e"
            px(tx + i, ty + j, ch)
    # bottom: neck shadow skin
    bx, by, _, _ = r["bottom"]
    rect(bx, by, 8, 8, "s")
    for i in range(8):
        px(bx + i, by + (3 if i in (3, 4) else 5), "q")
    # back: tied hair, cord hint at center
    bkx, bky, _, _ = r["back"]
    for j in range(8):
        for i in range(8):
            px(bkx + i, bky + j, "H" if (i * 3 + j) % 5 else "h")
    for i in range(2, 6):
        px(bkx + i, bky + 4, "d")
        px(bkx + i, bky + 5, "D")
    # sides: hair upper rows, skin lower (temple + ear)
    for side in ("right", "left"):
        sx, sy, _, _ = r[side]
        for j in range(8):
            for i in range(8):
                ch = "H" if j < 5 else ("S" if j < 6 else "s")
                if j == 5 and i == 3:
                    ch = "s"          # ear
                if j == 6 and i == 3:
                    ch = "q"
                if j == 5 and i == 0:
                    ch = "h"          # sideburn edge
                px(sx + i, sy + j, ch)
    # FRONT FACE — calm, young, focused
    fx, fy = r["front"][0], r["front"][1]
    for j in range(8):
        for i in range(8):
            px(fx + i, fy + j, "S")
    # fringe: full top row + corner tips (controlled hairline)
    for i in range(8):
        px(fx + i, fy + 0, "H")
    for i in (0, 1, 6, 7):
        px(fx + i, fy + 1, "H")
    px(fx + 0, fy + 2, "h"); px(fx + 7, fy + 2, "h")
    # brows: straight, dark
    for i in (1, 2):
        px(fx + i, fy + 2, "B")
    for i in (5, 6):
        px(fx + i, fy + 2, "B")
    # eyes: dark brown 2 px each with near-black pupil, lower lid shade
    px(fx + 1, fy + 3, "B"); px(fx + 2, fy + 3, "P")
    px(fx + 5, fy + 3, "P"); px(fx + 6, fy + 3, "B")
    px(fx + 1, fy + 4, "q"); px(fx + 6, fy + 4, "q")
    # nose + cheek light
    px(fx + 3, fy + 4, "s"); px(fx + 4, fy + 4, "s")
    px(fx + 2, fy + 5, "N"); px(fx + 5, fy + 5, "N")
    # neutral closed mouth
    px(fx + 3, fy + 6, "m"); px(fx + 4, fy + 6, "m")
    px(fx + 3, fy + 7, "s"); px(fx + 4, fy + 7, "s")
    # jaw contour
    px(fx + 0, fy + 6, "s"); px(fx + 7, fy + 6, "s")
    px(fx + 0, fy + 7, "q"); px(fx + 7, fy + 7, "q")
    px(fx + 1, fy + 7, "s"); px(fx + 6, fy + 7, "s")


def body_base():
    def cloth(side, i, j, w, h):
        if side == "front":
            if j < 4:                      # crossed collar on the chest top
                if j == 0:
                    return "C" if 2 <= i <= 5 else "I"
                if j == 1:
                    return "C" if i in (2, 5) else ("c" if i in (3, 4) else "I")
                if j == 2:
                    return "i" if i in (3, 4) else "I"
                return "i" if i in (3, 4) else "I"
            if j in (8, 9):
                return "i"                 # under-obi shadow
            return "l" if (i + j) % 7 == 2 else ("i" if (i * 5 + j) % 11 == 7 else "I")
        if side == "back":
            if j == 0:
                return "C" if 3 <= i <= 4 else "I"
            if j in (8, 9):
                return "i"
            return "i" if (i + 2 * j) % 6 == 3 else "I"
        if side in ("right", "left"):
            return "i" if j % 5 == 4 else ("l" if j % 7 == 1 else "I")
        return "i" if side == "bottom" else "I"
    paint((16, 16, 8, 12, 4), cloth)


def arm_base(u, v):
    def cloth(side, i, j, w, h):
        if side == "top":
            return "I"
        if side == "bottom":
            return "S"                     # palm
        if side in ("front", "back"):
            if j >= 10:
                return "S" if j >= 11 else "s"          # wrist + hand
            if j == 9:
                return "i"                          # cuff
            return "l" if (i + j) % 6 == 1 else "I"
        if side in ("right", "left"):
            if j >= 10:
                return "S"
            return "i" if j % 5 == 4 else "I"
        return "I"
    paint((u, v, 4, 12, 4), cloth)


def leg_base(u, v):
    def cloth(side, i, j, w, h):
        if side == "top":
            return "I"
        if side == "bottom":
            return "w"                     # sandal sole under foot
        if j >= 11:
            return "g"                     # dark tabi ankle
        if side in ("front", "back"):
            return "g" if (i + j) % 6 == 5 else "G"
        if side in ("right", "left"):
            return "g" if j % 5 == 4 else "G"
        return "G"
    paint((u, v, 4, 12, 4), cloth)


# ---------------------------------------------------------------- custom parts
def hair_simple(u, v, W, H, D, tie=False):
    def p(side, i, j, w, h):
        if tie and side in ("front", "back", "left", "right") and j == h - 2:
            return "D"
        if side == "bottom":
            return "H"
        return "h" if (i + 2 * j) % 5 == 2 else ("e" if side == "top" and (i * j) % 7 == 3 else "H")
    paint((u, v, W, H, D), p)


def fringe(u, v):
    def p(side, i, j, w, h):
        if j == 0 and side != "top":
            return "e"
        return "H"
    paint((u, v, 3, 2.8, 1), p)


def sode():
    def p(side, i, j, w, h):
        if side == "top":
            return "D" if j == 0 else "a"
        if side == "bottom":
            return "Q"
        if j % 2 == 0:
            return "Q"                     # plate seams
        if j == h - 1:
            return "a"
        if i == 0:
            return "T"                     # top-left edge light
        return "A" if i < w - 1 else "Q"
    for u in (78, 95):
        paint((u, 16, 4, 5, 4), p)


def collar():
    def p(side, i, j, w, h):
        if side == "front":
            return "C" if j < 2 else "c"
        if side == "top":
            return "C"
        return "c"
    paint((78, 26, 6.8, 3, 1), p)


def chest_armor():
    def p(side, i, j, w, h):
        if side == "top":                  # neckline: dark inner, off-white collar edge, cords
            if 3 <= i <= 5:
                return "c" if j == 0 else "Q"
            return "D" if (i + j) % 4 == 0 else "A"
        if side == "bottom":
            return "Q"
        if side == "front":
            if j == 0:
                return "c" if 3 <= i <= 5 else "D"       # painted collar + neck cords
            if j == 1 and 3 <= i <= 5:
                return "Q"                                # V-neck shadow
            if j % 3 == 2:
                return "Q"                                # plate seams
            if i == 0 or j == 0:
                return "T"
            if i in (1, 4, 7) and j % 3 == 1:
                return "a"
            if i == w - 1 or j == h - 1:
                return "Q"
            return "A"
        if side in ("left", "right"):
            if j % 3 == 2:
                return "Q"
            return "T" if (side == "left" and i == 0) else ("A" if i < w - 1 else "Q")
        if side == "back":
            if j % 3 == 2:
                return "Q"
            if j == 0:
                return "D"
            return "a" if (i + j) % 5 == 2 else "A"
        return "A"
    paint((0, 104, 9, 8, 5), p)


def crest():
    box = faces(112, 10, 3, 3, 0.3)
    fx, fy = box["front"][0], box["front"][1]
    mon = [".O.", "O.O", ".O."]          # original abstract circular mon (brass on lacquer)
    for j in range(3):
        for i in range(3):
            px(fx + i, fy + j, "A" if mon[j][i] == "." else ("Y" if (i, j) == (1, 1) else "O"))
    for name in ("top", "bottom", "right", "left", "back"):
        x, y, w, h = box[name]
        rect(x, y, w, h, "Q")


def obi():
    def p(side, i, j, w, h):
        if side in ("top", "bottom"):
            return "d"
        if j == 0 or j == h - 1:
            return "d"
        if side in ("front", "back"):
            return "D" if (i + j) % 4 else "d"
        return "D" if j % 2 else "d"
    paint((0, 80, 9, 3, 5), p)
    paint((112, 16, 4, 3, 2), lambda side, i, j, w, h: "D" if (i + j) % 3 else "d")


def hakama_panel(u):
    def p(side, i, j, w, h):
        if side == "top":
            return "g"
        if side == "bottom":
            return "G"
        if side in ("front", "back"):
            if j == 0:
                return "g"
            if i % 2 == 1:
                return "g"                 # vertical folds
            return "F" if (i * 3 + j) % 9 == 4 else "G"
        return "g" if i % 2 else "G"
    paint((u, 92, 8, 7, 1), p)


def sleeve(u):
    def p(side, i, j, w, h):
        if side in ("top", "bottom"):
            return "i"
        if j == h - 1:
            return "i"                     # reinforced cuff
        if side in ("front", "back"):
            return "l" if (i + 2 * j) % 7 == 2 else ("i" if i % 3 == 2 else "I")
        return "i" if j % 4 == 3 else "I"
    paint((u, 64, 4, 8, 4), p)


def kote(u):
    def p(side, i, j, w, h):
        if side == "top":
            return "R"
        if side == "bottom":
            return "M"
        if side in ("front", "back"):
            if j in (2, 5):
                return "M"                 # narrow iron plates
            if j == 3:
                return "D"                 # fastening cord
            if j == 0:
                return "R"
            if i == 0:
                return "U"
            return "R" if i == w - 1 else ("k" if (i + j) % 5 == 2 else "M")
        return "M" if j % 3 else "R"
    paint((u, 64, 4, 7, 4), p)


def hakama_leg(u):
    def p(side, i, j, w, h):
        if side == "top":
            return "g"
        if side == "bottom":
            return "G"
        if j == h - 1:
            return "g"                     # hem
        if side in ("front", "back", "left", "right"):
            if i % 2 == 1:
                return "g"
            return "F" if (i + j) % 8 == 3 else "G"
        return "G"
    paint((u, 64, 5, 7, 5), p)


def shin(u, v):
    def p(side, i, j, w, h):
        if side == "top":
            return "g"
        if side == "bottom":
            return "M"
        if j in (1, 4) and side != "top" and side != "bottom":
            return "d"                     # securing straps
        if side in ("front", "back"):
            if i % 2 == 1:
                return "Q"                 # vertical plate seams
            return "R" if (i + j) % 6 == 1 else "M"
        return "Q" if i % 3 == 2 else "M"
    paint((u, v, 5, 5, 5), p)


def sandal(u):
    def p(side, i, j, w, h):
        if side == "top":
            if 2 <= j <= 3:
                return "d"                 # strap band
            return "V" if (i + j) % 2 == 0 else "W"     # woven straw
        if side == "bottom":
            return "w" if (i + j) % 2 else "W"
        return "w"
    paint((u, 77, 5, 1, 6), p)


def sword(u_tsuka, u_saya, tsuka_len, saya_len, menuki_row):
    # tsuka 2 x tsuka_len x 2: black diamond wrap, menuki, iron fuchi/kashira
    def t(side, i, j, w, h):
        if side == "top":
            return "M"                     # fuchi
        if side == "bottom":
            return "M"                     # kashira
        if j == 0:
            return "M"                     # fuchi band on faces
        if j == h - 1:
            return "M"                     # kashira band
        if side in ("front", "back") and j == menuki_row and i == 0:
            return "O"                     # brass menuki
        return "g" if (i + j) % 2 == 0 else "K"
    paint((u_tsuka, 92, 2, tsuka_len, 2), t)

    # saya 2 x saya_len x 2: black lacquer, sageo band, iron koiguchi, brass kojiri
    def s(side, i, j, w, h):
        if side == "top":
            return "M"                     # koiguchi fitting
        if side == "bottom":
            return "o"                     # kojiri end cap
        if j == 2:
            return "D"                     # sageo cord band
        if side in ("front", "back"):
            return "k" if i == 0 else "K"  # lacquer highlight line
        return "K" if i else "k"
    paint((u_saya, 92, 2, saya_len, 2), s)


def main():
    head_base()
    body_base()
    arm_base(40, 16)     # right arm
    arm_base(32, 48)     # left arm
    leg_base(0, 16)      # right leg
    leg_base(16, 48)     # left leg

    hair_simple(56, 0, 9, 3, 9)                 # hair_base
    hair_simple(93, 0, 7, 7, 2, tie=True)       # hair_back
    fringe(112, 0)                              # hair_front_left
    fringe(112, 5)                              # hair_front_right
    hair_simple(56, 16, 1, 5, 4)                # hair_side_left
    hair_simple(67, 16, 1, 5, 4)                # hair_side_right
    hair_simple(93, 10, 3.5, 3, 3.5, tie=True)  # topknot

    collar()
    chest_armor()
    crest()
    sode()
    obi()
    hakama_panel(0)      # front
    hakama_panel(20)     # back
    sleeve(0)            # right
    kote(16)
    sleeve(32)           # left
    kote(48)
    hakama_leg(64)
    shin(104, 64)
    sandal(64)
    hakama_leg(84)
    shin(104, 75)
    sandal(87)
    sword(50, 40, 5, 13, 3)   # katana tsuka / saya
    sword(70, 60, 4, 10, 2)   # wakizashi tsuka / saya

    os.makedirs(ROOT, exist_ok=True)
    out = os.path.join(ROOT, "young_samurai.png")
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
