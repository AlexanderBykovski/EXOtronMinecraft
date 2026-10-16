#!/usr/bin/env python3
"""Basic RPG "player-style" skins for the Black Ninja and the Red Shogun.

Rebuild target (concepts/mobs, both prompt + art): the mobs are rendered on the
REGULAR PLAYER model (PlayerModel/HumanoidModel, vanilla proportions like any
player skin) with custom outer cubes (hood/mask, kabuto/menpo, armor plates...)
instead of the buggy GeckoLib rigs. This script paints the two 128x128 atlases:

    textures/entity/japanese/black_ninja.png   (DarkNinjaModel.BLACK_NINJA_LAYER)
    textures/entity/japanese/samurai.png       (RedShogunModel.SAMURAI_LAYER)

UV rules: vanilla base parts live at their standard 64x64 skin regions; every
custom cube gets its OWN texOffs zone packed into x>=64 of the 128 canvas
(1px padding, disjoint islands). The rect math (faces()) is identical to
vanilla ModelPart for non-mirrored boxes, so the Zones/texOffs tables below
must match the constants in the Java models:
    client/model/WarriorPlayerModel.java
Print output: "... texOffs constants..." lines are COPY-PASTED into Java.

Pixel-art: nearest neighbor, hard clusters, one top-left light, no AA/blur,
palette locked per material. Palettes come from the prompts/art.
"""
import math
import os
from PIL import Image

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
    "src", "main", "resources", "assets", "opusvsexe", "textures", "entity", "japanese"))

# ---------------------------------------------------------------- palettes
PAL = {
    ".": (0, 0, 0, 0),
    # skin (natural light-medium)
    "S": (200, 153, 110, 255), "s": (178, 128, 94, 255), "q": (150, 104, 74, 255), "N": (224, 180, 138, 255),
    # eyes
    "E": (26, 16, 10, 255), "W": (226, 218, 202, 255), "bn": (58, 34, 18, 255),
    # NINJA masonry
    "C0": (35, 38, 46, 255), "C1": (27, 30, 37, 255), "C2": (48, 52, 62, 255), "C3": (62, 68, 80, 255),   # charcoal/blue-gray
    "I0": (30, 34, 51, 255), "I1": (22, 25, 39, 255), "I2": (44, 50, 74, 255),                                  # dark indigo
    "SL": (58, 63, 78, 255), "sl": (42, 46, 58, 255),                                                           # slate
    "L0": (74, 53, 36, 255), "L1": (94, 70, 48, 255), "l2": (52, 36, 24, 255),                                  # leather
    "R0": (122, 104, 74, 255), "r1": (88, 72, 50, 255),                                                         # rope
    "M0": (58, 62, 70, 255), "m1": (38, 41, 47, 255), "M2": (84, 90, 100, 255),                                 # iron
    "ST": (150, 158, 168, 255), "st": (110, 118, 128, 255),                                                     # steel
    "DB": (30, 26, 24, 255),                                                                                    # dark strap
    # SHOGUN masonry
    "R1": (180, 46, 38, 255), "R2": (142, 30, 26, 255), "R3": (104, 18, 16, 255), "R4": (208, 78, 62, 255),    # crimson lacquer
    "IK": (28, 28, 34, 255), "ik": (44, 45, 54, 255), "IK2": (64, 66, 78, 255),                                # iron trim
    "GHD0": (194, 162, 78, 255), "GHD1": (152, 122, 58, 255), "GHD2": (224, 196, 124, 255),                    # antique gold
    "IND0": (44, 52, 80, 255), "IND1": (32, 39, 63, 255), "IND2": (60, 70, 100, 255),                         # indigo cloth
    "CM": (216, 212, 200, 255), "cm": (186, 182, 172, 255),                                                    # cream collar
    "STW": (194, 168, 112, 255), "stw": (150, 126, 82, 255),                                                   # straw
}


def make_img():
    return Image.new("RGBA", (128, 128), PAL["."])


def px(img, x, y, ch):
    img.putpixel((int(x), int(y)), PAL[ch])


def rect(img, x, y, w, h, ch):
    for j in range(int(math.ceil(h))):
        for i in range(int(math.ceil(w))):
            px(img, x + i, y + j, ch)


def faces(u, v, W, H, D):
    """Vanilla ModelPart UV for a non-mirrored W*H*D box at texOffs (u,v)."""
    return {
        "top": (u + D, v, W, D), "bottom": (u + D + W, v, W, D),
        "right": (u, v + D, D, H), "front": (u + D, v + D, W, H),
        "left": (u + D + W, v + D, D, H), "back": (u + 2 * D + W, v + D, W, H),
    }


# ---------------------------------------------------------------- zone packer
class Zones:
    """Row-packed islands in x>=64 (vanilla uses x<64 for the base skin)."""

    def __init__(self):
        self.taken = []
        self.cx, self.cy, self.row_h = 64, 0, 0

    def alloc(self, name, W, H, D):
        # full island span: the faces() layout needs 2W+2D horizontally and H+D vertically
        sw = int(math.ceil(W * 2 + D * 2))
        sh = int(math.ceil(H + D))
        x, y = self.cx, self.cy
        if x + sw > 128:
            self.cy += self.row_h
            self.cx, x, self.row_h = 64, 64, 0
            y = self.cy
        self.row_h = max(self.row_h, sh)
        self.cx = x + sw + 1
        self.taken.append((x, y, sw, sh))
        return (x, y)


def pack_zones(entries):
    """entries: list of (head, W, H, D). Returns {head:(u,v)} and prints java lines."""
    z = Zones()
    out = {}
    for name, W, H, D in entries:
        u, v = z.alloc(name, W, H, D)
        out[name] = (u, v)
    return out


def paint_box(img, zone, W, H, D, painter):
    for face, (x, y, w, h) in faces(*zone, W, H, D).items():
        w, h = int(math.ceil(w)), int(math.ceil(h))
        for j in range(h):
            for i in range(w):
                px(img, int(x) + i, int(y) + j, painter(face, i, j, w, h))


# ================================================================= NINJA
NINJA_Z = {}


def nz(name, W, H, D):
    NINJA_Z[name] = (W, H, D)
    return name


NINJA_CUBES = [
    (nz("hood_main", 9, 4, 9), ()),
]
# assign heads only
NINJA_HEADS = ["hood_main", "hood_side", "hood_back", "mask", "neck_wrap", "jacket", "shoulder_pad",
               "belt", "hip_front", "hip_back", "rope", "pouch", "kunai",
               "saya", "tsuka", "sleeve", "wrap", "bracer", "trouser", "calf"]
NINJA_SIZES = {
    "hood_main": (9.2, 4.2, 9.2), "hood_side": (0.95, 5.1, 8.6), "hood_back": (9.0, 5.1, 1.1),
    "mask": (7.9, 3.7, 0.9),
    "neck_wrap": (6.8, 1.6, 5.0), "jacket": (8.6, 12.3, 4.6), "shoulder_pad": (3.5, 2.7, 1.0),
    "belt": (8.0, 2.5, 4.9), "hip_front": (7.8, 4.6, 0.85), "hip_back": (7.8, 4.6, 0.85),
    "rope": (2.9, 1.8, 2.0), "pouch": (2.2, 3.0, 1.6), "kunai": (1.1, 2.7, 0.95),
    "saya": (2.0, 11.2, 2.0), "tsuka": (2.0, 4.4, 2.0), "sleeve": (4.2, 7.9, 4.2),
    "wrap": (4.4, 5.3, 4.4), "bracer": (4.6, 3.0, 4.6), "trouser": (4.64, 4.7, 4.64),
    "calf": (4.76, 4.7, 4.76),
}
NINJA_ZONES = pack_zones([(h, *NINJA_SIZES[h]) for h in NINJA_HEADS])


# ================================================================ SAMURAI
SAM_HEADS = ["menpo", "bowl", "brim", "shikoro_back", "shikoro_side", "horn", "disc", "sleeve", "kote",
             "cloth", "chest", "sode", "obi", "knot", "kusa_front", "kusa_side",
             "haidate", "suneate", "sandal", "saya", "tsuka", "waki_saya", "waki_tsuka"]
SAM_SIZES = {
    "menpo": (7.5, 3.95, 0.85), "bowl": (9.0, 4.6, 9.0), "brim": (8.0, 1.7, 1.2),
    "shikoro_back": (9.2, 4.7, 1.75), "shikoro_side": (1.0, 4.7, 6.8), "horn": (1.6, 3.0, 0.9),
    "disc": (2.1, 2.1, 0.66), "cloth": (8.5, 12.3, 4.5), "chest": (9.7, 9.5, 5.6),
    "sode": (5.2, 5.8, 5.0), "sleeve": (4.24, 7.5, 4.24), "kote": (4.84, 5.5, 4.84),
    "obi": (8.6, 2.5, 5.3), "knot": (3.8, 2.5, 1.4),
    "kusa_front": (9.0, 6.1, 1.0), "kusa_side": (1.1, 6.1, 5.35), "haidate": (5.1, 4.7, 5.1),
    "suneate": (5.1, 4.7, 5.1), "sandal": (5.2, 1.0, 6.1), "saya": (2.0, 13.8, 2.0),
    "tsuka": (2.0, 6.1, 2.0), "waki_saya": (2.0, 11.3, 2.0), "waki_tsuka": (2.0, 4.4, 2.0),
}
SAM_ZONES = pack_zones([(h, *SAM_SIZES[h]) for h in SAM_HEADS])


# ---------------------------------------------------------------- painters
def cloth(face, i, j, w, h, base, dark, light):
    """Broad cloth with low-contrast vertical folds + top-left light."""
    if j == 0 or (i == 0 and j <= 2):
        return light
    if j == h - 1:
        return dark
    return base


def folds(face, i, j, w, h, base, dark, light, gap=2):
    band = (i % (gap * 2)) < gap
    if j == 0 and not band:
        return light
    if band and j == h - 1:
        return dark
    if band and i % gap == 0 and j > 0:
        return dark
    return base if not band else dark if (i % 4) else dark


# ============================================================ NINJA TEXTURE
def paint_ninja():
    img = make_img()

    # ---- classic vanilla base regions (standard 64x64 skin layout)
    # head
    hz = faces(0, 0, 8, 8, 8)
    # top: hood crown with ring folds
    x, y = hz["top"][:2]
    for j in range(8):
        for i in range(8):
            px(img, x + i, y + j, "C1")
    for r, col in ((1, "C0"), (3, "C2"), (5, "C0"), (7, "C3")):
        for i in range(2, 6):
            px(img, x + i, y + r, col)
    # bottom: hood underside shadow
    x, y = hz["bottom"][:2]
    rect(img, x, y, 8, 8, "C1")
    rect(img, x, y + 6, 8, 2, "DB")
    # back: wrapped hood, crossing tails hint
    x, y = hz["back"][:2]
    for j in range(8):
        for i in range(8):
            px(img, x + i, y + j, "C0" if (i + j) % 3 else "C1")
    for i in range(2, 6):
        px(img, x + i, y + 3, "C2")
        px(img, x + i, y + 4, "C3")
    # sides: cloth with soft folds
    for side in ("right", "left"):
        x, y = hz[side][:2]
        for j in range(8):
            for i in range(8):
                px(img, x + i, y + j, "C1" if (i + j) % 4 == 0 else "C0")
        rect(img, x + 0, y + 6, 8, 2, "C2")
    # front: face — eye slit on brow band, skin below, mask area
    x, y = hz["front"][:2]
    for j in range(8):
        for i in range(8):
            px(img, x + i, y + j, "S" if 2 <= j <= 5 else "C0")
    # eye band: calm dark-brown eyes
    for dx, ex in ((2, 3), (5, 3)):
        for i in range(ex):
            px(img, x + dx + i, y + 3, "W")
            px(img, x + dx + i, y + 4, "W")
        px(img, x + dx, y + 3, "E")
        px(img, x + dx + ex - 1, y + 4, "bn")
    # brows hint + hairline shadow under hood
    rect(img, x, y + 2, 8, 1, "q")
    rect(img, x + 0, y + 2, 8, 1, "q")
    for i in range(8):
        px(img, x + i, y + 2, "q")
    # skin shading + mask seam
    rect(img, x, y + 5, 8, 1, "s")
    rect(img, x, y + 6, 8, 2, "C1")

    # body: base box = uwagi underlayer
    bz = faces(16, 16, 8, 12, 4)
    body = bz["front"]
    for j in range(12):
        for i in range(8):
            px(img, body[0] + i, body[1] + j, "I1")  # indigo seen between jacket gaps
    for face in ("back", "right", "left"):
        fx, fy = bz[face][:2]
        rect(img, fx, fy, bz[face][2], bz[face][3], "I1")
    # right arm base: sleeve underlayer
    az = faces(40, 16, 4, 12, 4)
    rect(img, *az["front"][:2], 4, 12, "I1")
    rect(img, *az["back"][:2], 4, 12, "I1")
    rect(img, *az["right"][:2], 4, 12, "I1")
    rect(img, *az["left"][:2], 4, 12, "I1")
    # left arm
    az = faces(32, 48, 4, 12, 4)
    rect(img, *az["front"][:2], 4, 12, "I1")
    rect(img, *az["back"][:2], 4, 12, "I1")
    rect(img, *az["right"][:2], 4, 12, "I1")
    rect(img, *az["left"][:2], 4, 12, "I1")
    # legs: trousers base (loose charcoal)
    for zone in ((16, 48), (0, 32)):
        lz = faces(*zone, 4, 12, 4)
        for face in ("front", "back", "right", "left"):
            fx, fy = lz[face][:2]
            for j in range(12):
                for i in range(4):
                    px(img, fx + i, fy + j, "C1" if (i + j) % 5 == 0 else "C0")
    # leg top/bottom zones remain but unused visually (covered)

    # ---- custom cubes
    def mask_p(face, i, j, w, h):
        if face != "front":
            return "C1"
        if j == 0:
            return "C0"
        if j >= h - 2:
            return "C1" if i % 5 else "C0"
        return "C0" if (i % 4 == 0 or j % 3 == 0) else "C1"

    paint_box(img, NINJA_ZONES["hood_main"], *NINJA_SIZES["hood_main"],
              lambda f, i, j, w, h: "C0" if (i * 2 + j) % 5 else "C1")
    paint_box(img, NINJA_ZONES["hood_side"], *NINJA_SIZES["hood_side"],
              lambda f, i, j, w, h: "C1" if (i == 0 and j < 2) else "C0")
    paint_box(img, NINJA_ZONES["mask"], *NINJA_SIZES["mask"], mask_p)
    paint_box(img, NINJA_ZONES["neck_wrap"], *NINJA_SIZES["neck_wrap"],
              lambda f, i, j, w, h: "C2" if i == 0 and j <= 1 else ("C1" if j == h - 1 else "C0"))

    def jacket_p(face, i, j, w, h):
        if face == "front":  # crossed V closure with indigo edge
            if j >= 1:
                diag = w - 1 - i - (j * 3 // h)
                if diag <= 1:
                    return "I2" if diag == 0 else "I0"
                if diag <= 2:
                    return "C2"
            return cloth(face, i, j, w, h, "C0", "C1", "C2")
        return cloth(face, i, j, w, h, "C0", "C1", "C2")

    paint_box(img, NINJA_ZONES["jacket"], *NINJA_SIZES["jacket"], jacket_p)
    paint_box(img, NINJA_ZONES["shoulder_pad"], *NINJA_SIZES["shoulder_pad"],
              lambda f, i, j, w, h: "SL" if (i % 2) == 0 and (j % 2) == 0 else "sl")

    def belt_p(face, i, j, w, h):
        if face == "front":
            return "L0" if (i % 3) else "L1"
        return "L0"

    paint_box(img, NINJA_ZONES["belt"], *NINJA_SIZES["belt"], belt_p)
    paint_box(img, NINJA_ZONES["hip_front"], *NINJA_SIZES["hip_front"],
              lambda f, i, j, w, h: "C1" if (i % 6 < 2) else "C0")
    paint_box(img, NINJA_ZONES["hip_back"], *NINJA_SIZES["hip_back"],
              lambda f, i, j, w, h: "C1" if (i % 6 < 2) else "C0")
    paint_box(img, NINJA_ZONES["rope"], *NINJA_SIZES["rope"],
              lambda f, i, j, w, h: "R0" if (i + j) % 2 else "r1")
    paint_box(img, NINJA_ZONES["pouch"], *NINJA_SIZES["pouch"],
              lambda f, i, j, w, h: "L0" if j > 0 else "L1")
    paint_box(img, NINJA_ZONES["kunai"], *NINJA_SIZES["kunai"],
              lambda f, i, j, w, h: "m1" if j > 0 else "M0")

    def saya_p(face, i, j, w, h):
        if j == 0:
            return "M0"
        if j >= h - 1:
            return "m1"
        return "DB" if i == 0 else "IK" if False else "DB"

    paint_box(img, NINJA_ZONES["saya"], *NINJA_SIZES["saya"], saya_p)
    paint_box(img, NINJA_ZONES["tsuka"], *NINJA_SIZES["tsuka"],
              lambda f, i, j, w, h: "L0" if ((i + j) % 4) == 0 else "DB")

    def sleeve_p(face, i, j, w, h):
        if face == "front":  # quilted crosshatch on outer upper arm
            for ii in range(w):
                if j == 0:
                    return "C2"
            return "C1" if (i + j) % 3 else "C0"
        return "C1" if j > h - 3 else "C0"

    paint_box(img, NINJA_ZONES["sleeve"], *NINJA_SIZES["sleeve"], sleeve_p)
    paint_box(img, NINJA_ZONES["wrap"], *NINJA_SIZES["wrap"],
              lambda f, i, j, w, h: "C2" if j % 2 == 0 else "C0")
    paint_box(img, NINJA_ZONES["bracer"], *NINJA_SIZES["bracer"],
              lambda f, i, j, w, h: "M0" if (i % 2 or j % 2) else "M2")
    paint_box(img, NINJA_ZONES["trouser"], *NINJA_SIZES["trouser"],
              lambda f, i, j, w, h: "C1" if (i * 2 + j) % 6 < 2 else "C0")
    paint_box(img, NINJA_ZONES["calf"], *NINJA_SIZES["calf"],
              lambda f, i, j, w, h: "C2" if (j % 2) == 0 else "C0")

    img.save(os.path.join(OUT, "black_ninja.png"))
    return img


# =========================================================== SAMURAI TEXTURE
def paint_samurai():
    img = make_img()

    # head base: mature face + hairline shadow
    hz = faces(0, 0, 8, 8, 8)
    for face in ("front", "right", "left", "back"):
        x, y, w, h = hz[face]
        for j in range(int(h)):
            for i in range(int(w)):
                px(img, int(x) + i, int(y) + j, "s" if (i * 2 + j) % 7 == 0 else "S")
    # front face: calm authority, thick brows, moustache area handled by menpo cube
    x, y = hz["front"][:2]
    for i in range(8):
        px(img, x + i, y + 0, "q")
        px(img, x + i, y + 1, "s")
        px(img, x + i, y + 7, "s")
    # brows
    for ex in (1, 5):
        for i in range(2):
            px(img, x + ex + i, y + 2, "bn")
    # eyes: focused dark brown
    for ex in (1, 5):
        for i in range(2):
            px(img, x + ex + i, y + 3, "W")
        px(img, x + ex, y + 3, "E")
    # nose + cheek shadow
    px(img, x + 3, y + 4, "q")
    px(img, x + 4, y + 4, "q")
    rect(img, x, y + 5, 8, 1, "s")
    # top: kabuto bowl interior (dark iron)
    x, y = hz["top"][:2]
    rect(img, x, y, 8, 8, "IK")
    rect(img, x + 1, y + 1, 6, 6, "ik")
    # bottom: dark under-bowl
    rect(img, *hz["bottom"][:2], 8, 8, "IK")
    # back: hair under the helmet
    x, y = hz["back"][:2]
    for i in range(8):
        px(img, x + i, y, "N")
        px(img, x + i, y + 1, "S")
    # sides: hair at temples
    for side in ("right", "left"):
        x, y, w, h = hz[side]
        for j in range(8):
            for i in range(8):
                px(img, x + i, y + j, "N" if j == 0 else ("S" if (i + j) % 4 else "s"))

    # body base: indigo kosode (visible at neck / under armor)
    bz = faces(16, 16, 8, 12, 4)
    for face in ("front", "back", "right", "left"):
        fx, fy, fw, fh = bz[face]
        for j in range(int(fh)):
            for i in range(int(fw)):
                px(img, int(fx) + i, int(fy) + j, "IND1")
    # cream inner collar + crossed top on front
    fx, fy = bz["front"][:2]
    rect(img, fx, fy, 8, 2, "IND2")
    for i in range(8):
        px(img, fx + i, fy + 0, "CM" if i % 4 < 2 else "IND0")
        px(img, fx + i, fy + 1, "cm" if i % 3 else "CM")
    # arms base: indigo sleeves
    for zone in ((40, 16), (32, 48)):
        az = faces(*zone, 4, 12, 4)
        for face in ("front", "back", "right", "left"):
            fx, fy, fw, fh = az[face]
            for j in range(int(fh)):
                for i in range(int(fw)):
                    px(img, int(fx) + i, int(fy) + j, "IND0" if (i * 2 + j) % 5 else "IND1")
    # legs base: dark trousers
    for zone in ((16, 48), (0, 32)):
        lz = faces(*zone, 4, 12, 4)
        for face in ("front", "back", "right", "left"):
            fx, fy, fw, fh = lz[face]
            for j in range(int(fh)):
                for i in range(int(fw)):
                    px(img, int(fx) + i, int(fy) + j, "IND1" if (i + j) % 4 else "ik")

    def menpo_p(face, i, j, w, h):
        if face != "front":
            return "R3"
        # red-lacquered mask: brow band at j0 => chin shading, vent holes, moustache
        if j == 0:
            return "R4" if i % 3 else "R2"
        if j <= 1:
            for k in (2, 5):
                if abs(i - k) < 1:
                    return "IK"
            return "R2"
        return "R3" if (i * 2 + j) % 5 else "R2"

    paint_box(img, SAM_ZONES["menpo"], *SAM_SIZES["menpo"], menpo_p)

    def bowl_p(face, i, j, w, h):
        # red lacquered bowl: plate seams (vertical black bands) + top rows
        if face == "top":
            return "R3" if (i + j) % 4 else "R2"
        if j == 0:
            return "R4"
        if i % 4 == 0:
            return "IK"
        return "R2" if j > 2 else "R1"

    paint_box(img, SAM_ZONES["bowl"], *SAM_SIZES["bowl"], bowl_p)
    paint_box(img, SAM_ZONES["brim"], *SAM_SIZES["brim"],
              lambda f, i, j, w, h: "IK" if j == 1 else ("R2" if i % 5 else "R3"))

    def shikoro_p(face, i, j, w, h):
        # black-and-red layered plates: alternating rows with iron edges
        if j % 3 == 2:
            return "IK"
        return "R2" if (j // 3) % 2 else "R3"

    paint_box(img, SAM_ZONES["shikoro_back"], *SAM_SIZES["shikoro_back"], shikoro_p)
    paint_box(img, SAM_ZONES["shikoro_side"], *SAM_SIZES["shikoro_side"], shikoro_p)
    paint_box(img, SAM_ZONES["horn"], *SAM_SIZES["horn"],
              lambda f, i, j, w, h: "GHD2" if j == 0 else ("GHD0" if i < w - 1 else "GHD1"))
    paint_box(img, SAM_ZONES["disc"], *SAM_SIZES["disc"],
              lambda f, i, j, w, h: "GHD1" if (i == j or i + j == w - 1) else "GHD0")

    def cloth_p(face, i, j, w, h):
        if face == "front" and j < 3:  # collar again on outer cube
            return "IND2" if (i % 6 < 2) else "IND0"
        return "IND0" if (i + j) % 6 else "IND1"

    paint_box(img, SAM_ZONES["cloth"], *SAM_SIZES["cloth"], cloth_p)

    def chest_p(face, i, j, w, h):
        # lamellar do: five red rows, iron borders, gold rivets
        if face not in ("front", "back", "right", "left"):
            return "R2"
        row = j // 2
        if j % 2 == 1 or row >= 5:
            return "IK" if j % 2 == 1 else "R2"
        if i % 7 == 0 or (j % 6 == 1):
            return "GHD1" if i % 7 == 0 else "R1"
        return "R1" if (i * row) % 3 else "R2"

    paint_box(img, SAM_ZONES["chest"], *SAM_SIZES["chest"], chest_p)
    paint_box(img, SAM_ZONES["sode"], *SAM_SIZES["sode"],
              lambda f, i, j, w, h: "IK" if j % 3 == 2 else ("R1" if (i + j) % 4 else "R2"))
    paint_box(img, SAM_ZONES["sleeve"], *SAM_SIZES["sleeve"],
              lambda f, i, j, w, h: "IND0" if (i * 2 + j) % 5 else "IND1")
    paint_box(img, SAM_ZONES["kote"], *SAM_SIZES["kote"],
              lambda f, i, j, w, h: "IK" if j % 5 == 0 else ("R2" if (i + j) % 4 else "R1"))

    def obi_p(face, i, j, w, h):
        if face == "front":
            return "L1" if i % 4 else "L0"
        return "L1" if j == 0 else "L0"

    paint_box(img, SAM_ZONES["obi"], *SAM_SIZES["obi"], obi_p)
    paint_box(img, SAM_ZONES["knot"], *SAM_SIZES["knot"],
              lambda f, i, j, w, h: "GHD1" if (i + j) % 5 == 0 else "GHD0")
    paint_box(img, SAM_ZONES["kusa_front"], *SAM_SIZES["kusa_front"],
              lambda f, i, j, w, h: "IK" if j % 5 == 4 else ("R2" if (i // 3) % 2 else "R1"))
    paint_box(img, SAM_ZONES["kusa_side"], *SAM_SIZES["kusa_side"],
              lambda f, i, j, w, h: "IK" if j % 5 == 4 else ("R2" if (i // 2) % 2 else "R1"))
    paint_box(img, SAM_ZONES["haidate"], *SAM_SIZES["haidate"],
              lambda f, i, j, w, h: "R2" if j > 2 else ("R1" if i % 2 else "R3"))
    paint_box(img, SAM_ZONES["suneate"], *SAM_SIZES["suneate"],
              lambda f, i, j, w, h: "IK" if i % 4 == 0 else ("R1" if j % 3 else "R2"))
    paint_box(img, SAM_ZONES["sandal"], *SAM_SIZES["sandal"],
              lambda f, i, j, w, h: "STW" if (i + j) % 3 else "stw")

    def saya_p(face, i, j, w, h):
        if j == 0:
            return "GHD1"
        if j >= h - 2:
            return "IK"
        return "IK" if i % 4 == 0 else "R3"

    paint_box(img, SAM_ZONES["saya"], *SAM_SIZES["saya"], saya_p)
    paint_box(img, SAM_ZONES["tsuka"], *SAM_SIZES["tsuka"],
              lambda f, i, j, w, h: "R3" if (i + j) % 4 else "DB")
    paint_box(img, SAM_ZONES["waki_saya"], *SAM_SIZES["waki_saya"],
              lambda f, i, j, w, h: "IK" if j % 5 == 4 or i == 0 else "R3")
    paint_box(img, SAM_ZONES["waki_tsuka"], *SAM_SIZES["waki_tsuka"],
              lambda f, i, j, w, h: "R3" if (i + j) % 4 else "DB")

    img.save(os.path.join(OUT, "samurai.png"))
    return img


if __name__ == "__main__":
    def validate(zones, sizes, img):
        for name, (u, v) in zones.items():
            W, H, D = sizes[name]
            for fname, (x, y, w, h) in faces(u, v, W, H, D).items():
                assert x >= 0 and y >= 0 and x + w <= img.width and y + h <= img.height, \
                    (name, fname, x, y, w, h)
        print(f"zones validated: {len(zones)}")
    ninja = paint_ninja()
    sam = paint_samurai()
    validate(NINJA_ZONES, NINJA_SIZES, ninja)
    validate(SAM_ZONES, SAM_SIZES, sam)
    def fmt(prefix, zones):
        for k in sorted(zones):
            print(f"{prefix}{k.upper()}: texOffs = {zones[k]}")
    print("----- NINJA -----")
    fmt("NINJA_", NINJA_ZONES)
    print("----- SAMURAI -----")
    fmt("SAM_", SAM_ZONES)
    print("saved", os.path.join(OUT, "black_ninja.png"), os.path.join(OUT, "samurai.png"))
