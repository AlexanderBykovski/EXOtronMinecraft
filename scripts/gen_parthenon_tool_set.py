#!/usr/bin/env python3
"""Parthenon celestial tool set — angelic rework (pickaxe, labrys, shovel, hoe).

Same visual language as the Angelic Sword (gen_parthenon_xiphos.py): identical
palette, ruby gem, dark charcoal grip, gold wrap rings, gold pommel and the
4-frame divine shimmer. Each tool keeps its own functional silhouette.

Approach A (2D pixel art + vanilla handheld model + display transforms) —
the project has NO custom item renderer; GeckoLib is entity-only.

Dry-run (ASCII, writes nothing):
    python3 scripts/gen_parthenon_tool_set.py --dump
Write assets:
    python3 scripts/gen_parthenon_tool_set.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image  # noqa: E402
import gen_parthenon_set_common as C

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/resources/assets/opusvsexe/textures/item"
MODELS = ROOT / "src/main/resources/assets/opusvsexe/models/item"
FRAMETIME = 5
N_FRAMES = 4

GB = C.GOLD_BRIGHT
GM = C.GOLD_MID
GD = C.GOLD_DEEP
EH = C.EDGE_HI
LI = C.LIGHT
MI = C.MID
CO = C.COOL
DE = C.DEEP

# Shared handle axis — IDENTICAL director to the sword's blade so the grip +
# gem + pommel land in the same screen spot for every member of the set.
GUARD = (14.0, 18.0)        # blade/guard base (same as sword)
HANDLE_AXIS = (14.0, 18.0, 30.0, 4.0)   # handle drawn at s<0 (down-left)
P_S = -0.62                 # pommel point along axis


class Axis:
    def __init__(self, gx, gy, tx, ty):
        self.gx, self.gy = gx, gy
        self.tx, self.ty = tx, ty
        dx, dy = tx - gx, ty - gy
        self.len = math.hypot(dx, dy)
        self.ux, self.uy = dx / self.len, dy / self.len
        self.evx, self.evy = -self.uy, self.ux

    def p(self, s, o):
        return self.gx + (self.tx - self.gx) * s + self.evx * o, \
            self.gy + (self.ty - self.gy) * s + self.evy * o


def shared_tail(g):
    """Handle + wrap rings + ruby gem + pommel (full set-consistency)."""
    ax = Axis(*HANDLE_AXIS)
    C.draw_handle(g, ax)
    gcx, gcy = ax.p(0.05, 0.0)
    C.draw_gem(g, gcx, gcy)
    p_x, p_y = ax.p(P_S, 0.0)
    C.draw_pommel(g, p_x, p_y)


# =====================================================================
# 1. PICKAXE — long horizontal mining head: pointed tip + celestial chisel
# Connector at ~(14,15); head spans the top half, slight downward curve.
# =====================================================================
def paint_pickaxe(g):
    # LEFT pointed arm (drops lower-left)
    C.quad(g, (14, 11), (14, 16), (5, 17), (5, 14), MI)
    C.quad(g, (5, 14), (5, 17), (2, 19), (2, 13), CO)
    g.px(1, 16, EH); g.px(1, 15, EH); g.px(1, 14, EH)
    # RIGHT chisel arm (wider, bright edge)
    C.quad(g, (14, 11), (14, 16), (28, 10), (28, 5), LI)
    C.quad(g, (28, 10), (28, 5), (30, 3), (30, 11), EH)
    # central socket around the connector
    C.quad(g, (11, 9), (11, 17), (16, 13), (16, 13), GM)
    C.quad(g, (12, 9), (12, 17), (13, 10), (13, 16), GD)
    shared_tail(g)
    C.outline(g)


# =====================================================================
# 2. LABRYS (kept identity) — twin symmetric blades + centre hub
# Hub/connector at ~(14,15); blades sweep up-left and up-right.
# =====================================================================
def paint_labrys(g):
    hx, hy = 14.0, 15.0
    for s in (1, -1):
        # blade body (hub out and up)
        C.quad(g, (hx, hy - 2), (hx, hy + 1), (hx - 11 * s, hy - 3 - 4), (hx - 11 * s, hy - 3), LI)
        # bright cutting edge (outer)
        C.quad(g, (hx - 11 * s, hy - 3), (hx - 11 * s, hy - 3 - 4),
               (hx - 12 * s, hy - 2), (hx - 12 * s, hy), EH)
        # face shading
        C.quad(g, (hx - 5 * s, hy - 1), (hx - 5 * s, hy - 4),
               (hx - 8 * s, hy - 2 - 1), (hx - 8 * s, hy), CO)
    # central hub + gold collar
    C.quad(g, (hx - 2, hy - 2), (hx + 2, hy - 2), (hx + 2, hy + 2), (hx - 2, hy + 2), GM)
    C.quad(g, (hx - 2, hy + 2), (hx + 2, hy + 2), (hx + 2, hy + 3), (hx - 2, hy + 3), GD)
    shared_tail(g)
    C.outline(g)


# =====================================================================
# 3. SHOVEL — centred excavation blade with a central raised ridge
# Blade top at y=4; connects down to the connector at ~(14,15).
# =====================================================================
def paint_shovel(g):
    C.quad(g, (9, 4), (9, 12), (21, 12), (21, 4), MI)          # blade upper
    C.quad(g, (9, 12), (21, 12), (20, 19), (10, 19), CO)       # lower taper
    C.quad(g, (6, 4), (6, 12), (9, 12), (9, 4), EH)            # left rim
    C.quad(g, (24, 4), (24, 12), (21, 12), (21, 4), EH)        # right rim
    # central raised ridge + slim gold energy line
    C.quad(g, (14.2, 4), (14.2, 19), (15.8, 19), (15.8, 4), LI)
    C.quad(g, (14.6, 5), (14.6, 18), (15.4, 18), (15.4, 5), GD)
    g.px(15, 19, EH); g.px(15, 20, EH); g.px(14, 20, EH)       # brightest tip
    shared_tail(g)
    C.outline(g)


# =====================================================================
# 4. HOE — offset horizontal cultivation blade + folded-wing support
# Support across the top; farming blade hangs down on the right.
# Connector at ~(14,15) meet the support bar.
# =====================================================================
def paint_hoe(g):
    # horizontal support bar (upper region)
    C.quad(g, (9, 9), (9, 14), (30, 12), (30, 9), MI)          # support top
    C.quad(g, (9, 14), (9, 16), (30, 14), (30, 12), CO)        # support underside
    C.quad(g, (30, 9), (30, 12), (31, 12.5), (31, 8.5), EH)    # bright far edge
    # folded-wing geometry on the upper-left support
    C.quad(g, (9, 9), (9, 6), (16, 5), (16, 8), GD)
    C.quad(g, (9, 6), (9, 4), (14, 3), (14, 6), GM)
    # farming blade hanging down on the right
    C.quad(g, (23, 12), (23, 20), (30, 22), (30, 14), LI)
    C.quad(g, (23, 20), (30, 22), (31, 23), (31, 21), EH)
    C.quad(g, (23, 20), (23, 12), (25, 13), (25, 19), CO)
    # gold reinforcement along the support
    C.quad(g, (18, 9), (18, 14), (22, 13), (22, 9), GM)
    shared_tail(g)
    C.outline(g)


PAINTERS = {
    "parthenon_pickaxe": paint_pickaxe,
    "parthenon_axe": paint_labrys,
    "parthenon_shovel": paint_shovel,
    "parthenon_hoe": paint_hoe,
}


def build(name):
    g = C.Grid()
    PAINTERS[name](g)
    return g


def render_frame(base, f):
    return C.render_frame(base, f, N_FRAMES)


def write_model(name):
    model = {
        "parent": "minecraft:item/handheld",
        "textures": {"layer0": f"opusvsexe:item/{name}"},
        "display": C.VOLUME_DISPLAY if name in ("parthenon_axe",) else {
            "gui": {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [0.62, 0.62, 0.62]},
            "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
            "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4, 0.5], "scale": [0.95, 0.95, 0.95]},
            "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.62, 0.62, 0.62]},
            "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.62, 0.62, 0.62]},
            "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
            "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [0.75, 0.75, 0.75]},
            "head": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1.0, 1.0, 1.0]},
        },
    }
    (MODELS / f"{name}.json").write_text(json.dumps(model, indent=2))
    print("wrote", MODELS / f"{name}.json")


def main():
    write = "--dump" not in sys.argv
    for name in PAINTERS:
        base = build(name)
        if not write:
            print(f"=== {name} frame0 ===")
            base.dump()
            continue
        atlas = Image.new("RGBA", (C.SIZE, C.SIZE * N_FRAMES), (0, 0, 0, 0))
        for f in range(N_FRAMES):
            fr = render_frame(base, f)
            for y in range(C.SIZE):
                for xi in range(C.SIZE):
                    c = fr.c[y][xi]
                    if c != C.T:
                        atlas.putpixel((xi, y + f * C.SIZE), c)
        atlas.save(ITEMS / f"{name}.png")
        print("wrote", ITEMS / f"{name}.png")
        (ITEMS / f"{name}.png.mcmeta").write_text(
            json.dumps({"animation": {"frametime": FRAMETIME, "interpolate": False}}, indent=2))
        print("wrote", ITEMS / f"{name}.png.mcmeta")
        write_model(name)


if __name__ == "__main__":
    main()
