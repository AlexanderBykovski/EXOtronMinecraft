#!/usr/bin/env python3
"""Shared toolkit for project GeckoLib asset generators (geo + texture + animations).

Conventions verified against GeckoLib 4.4.9 sources (BakedModelFactory):
- Box-UV face rects identical to vanilla ModelPart unwrap.
- Bedrock -> Java rotation: x and y are NEGATED, z is kept. All builders here take
  JAVA-semantics degrees and convert automatically on output.
- Entities face -Z; the character "front" face of a cube is the NORTH face.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src" / "main" / "resources" / "assets" / "opusvsexe"

FACES = ("up", "down", "east", "north", "west", "south")


def br_rot(jx=0.0, jy=0.0, jz=0.0):
    """Java-semantics degrees -> Bedrock geo/anim values."""
    return [round(-jx, 2), round(-jy, 2), round(jz, 2)]


def face_rects(u, v, w, h, d):
    """Half-open (x, y, w, h) texture rects for a box-UV cube.
    GeckoLib floors cube sizes for UV (BakedModelFactory: Math.floor(uvSize))."""
    w, h, d = int(math.floor(w)), int(math.floor(h)), int(math.floor(d))
    return {
        "up":    (u + d,     v,     w, d),
        "down":  (u + d + w, v,     w, d),
        "east":  (u,         v + d, d, h),
        "north": (u + d,     v + d, w, h),
        "west":  (u + d + w, v + d, d, h),
        "south": (u + d + w + d, v + d, w, h),
    }


def footprint(w, h, d):
    w, h, d = int(math.floor(w)), int(math.floor(h)), int(math.floor(d))
    return 2 * (w + d), d + h


def shelf_pack(cubes, atlas=128, pad=1):
    """Assign texOffs (u, v) per cube. cubes: list of dicts with 'size' (w,h,d).
    Sorts by footprint height (tall first), packs rows left->right. Raises if it can't fit."""
    items = sorted(cubes, key=lambda c: (-footprint(*c["size"])[1], -footprint(*c["size"])[0]))
    x = y = row_h = 0
    for c in items:
        fw, fh = footprint(*c["size"])
        if x + fw > atlas:
            x = 0
            y += row_h + pad
            row_h = 0
        if x + fw > atlas or y + fh > atlas:
            raise RuntimeError(f"UV atlas overflow for {c.get('name')} footprint {fw}x{fh}")
        c["tex"] = (x, y)
        x += fw + pad
        row_h = max(row_h, fh)
    return cubes


class Tex:
    def __init__(self, size=128, palette=None):
        from PIL import Image
        self.img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        self.px = self.img.load()
        self.size = size
        self.pal = palette or {}

    def c(self, key):
        return self.pal[key]

    def set(self, x, y, color):
        if 0 <= x < self.size and 0 <= y < self.size:
            if isinstance(color, str):
                color = self.pal[color]
            self.px[x, y] = color

    def rect(self, r, color):
        x, y, w, h = r
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.set(i, j, color)

    def border(self, r, color, t=1):
        x, y, w, h = r
        self.rect((x, y, w, t), color)
        self.rect((x, y + h - t, w, t), color)
        self.rect((x, y, t, h), color)
        self.rect((x + w - t, y, t, h), color)


def paint_lacquer(tex, r, base, hi, dark, seam, rows=3, border=None, rivets=None,
                  edge_hi=None):
    """Lacquered lamellar panel: base rows, dark seams, top/left light edge."""
    x, y, w, h = r
    tex.rect(r, base)
    for j in range(h):
        m = j % rows
        if m == 0:
            for i in range(w):
                tex.set(x + i, y + j, dark)
        elif m == 1 and edge_hi is not None:
            for i in range(w):
                tex.set(x + i, y + j, hi)
    if edge_hi is None:
        for j in range(h):
            if j % rows == 1:
                tex.set(x, y + j, hi)
    if border:
        tex.border(r, border)
    if rivets:
        for (rx, ry) in rivets:
            tex.set(x + rx, y + ry, rivets if isinstance(rivets, tuple) else None) if False else None
        # rivets given as list of (rx, ry) colors resolved by caller
    return r


def paint_rivets(tex, r, color, step=4, inset=1):
    x, y, w, h = r
    for j in range(inset, h - inset, max(2, h // 3 if h <= 6 else 3)):
        for i in range(inset, w - inset, step):
            tex.set(x + i, y + j, color)


def paint_cloth(tex, r, base, hi, dark, fold_step=4):
    x, y, w, h = r
    tex.rect(r, base)
    for i in range(w):
        m = i % fold_step
        col = hi if m == 0 else (dark if m == fold_step - 1 else base)
        for j in range(h):
            tex.set(x + i, y + j, col)


def paint_metal(tex, r, base, hi, dark, vertical=True):
    x, y, w, h = r
    tex.rect(r, base)
    n = w if vertical else h
    for k in range(n):
        col = hi if k == 0 else (dark if k == n - 1 else base)
        if vertical:
            for j in range(h):
                tex.set(x + k, y + j, col)
        else:
            for i in range(w):
                tex.set(x + i, y + k, col)


def paint_leather(tex, r, base, hi, dark):
    x, y, w, h = r
    tex.rect(r, base)
    tex.border(r, dark)
    for i in range(x + 1, x + w - 1, 2):
        tex.set(i, y + 1, hi)
    if h > 3:
        for i in range(x + 2, x + w - 1, 3):
            tex.set(i, y + h - 2, dark)


def paint_straw(tex, r, base, hi, dark):
    x, y, w, h = r
    tex.rect(r, base)
    for j in range(h):
        for i in range(w):
            if (i // 2 + j) % 3 == 0:
                tex.set(x + i, y + j, dark)
            elif (i + j) % 4 == 0:
                tex.set(x + i, y + j, hi)


def paint_wrap(tex, r, wrap, under, gold=None, period=2):
    """Handle wrap: diagonal diamonds of dark over a lighter underlayer."""
    x, y, w, h = r
    tex.rect(r, under)
    for j in range(h):
        for i in range(w):
            if (i + j) % (period * 2) < period:
                tex.set(x + i, y + j, wrap)
    if gold:
        for j in range(1, h - 1, 3):
            tex.set(x + w // 2, y + j, gold)


# ---------------------------------------------------------------- geo output

def emit_geo(path, identifier, tw, th, bones, visible_bounds=(6, 6, 3.2)):
    data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": identifier,
                "texture_width": tw,
                "texture_height": th,
                "visible_bounds_width": visible_bounds[0],
                "visible_bounds_height": visible_bounds[1],
                "visible_bounds_offset": [0, visible_bounds[2], 0],
            },
            "bones": bones,
        }],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1) + "\n")


def bone(name, pivot, parent=None, jrot=None, cubes=None):
    b = {"name": name, "pivot": [round(v, 3) for v in pivot]}
    if parent:
        b["parent"] = parent
    if jrot and any(jrot):
        b["rotation"] = br_rot(*jrot)
    out = []
    for c in (cubes or []):
        u, v = c["tex"]
        w, h, d = c["size"]
        cu = {
            "origin": [round(q, 3) for q in c["origin"]],
            "size": [round(q, 3) for q in (w, h, d)],
            "uv": [u, v],
        }
        if c.get("inflate"):
            cu["inflate"] = c["inflate"]
        if c.get("mirror"):
            cu["mirror"] = True
        if c.get("jrot") and any(c["jrot"]):
            cu["pivot"] = [round(q, 3) for q in c["cpivot"]]
            cu["rotation"] = br_rot(*c["jrot"])
        out.append(cu)
    if out:
        b["cubes"] = out
    return b


# ------------------------------------------------------------ animations

class AnimBuilder:
    def __init__(self, name, length, loop):
        self.name, self.length, self.loop = name, length, loop
        self.bones = {}

    def bone(self, name, rot=None, pos=None):
        ch = {}
        if rot:
            ch["rotation"] = {f"{t:.2f}".rstrip("0").rstrip("."): br_rot(*v) for t, v in rot}
        if pos:
            ch["position"] = {f"{t:.2f}".rstrip("0").rstrip("."): [round(p[0], 3), round(p[1], 3), round(p[2], 3)]
                              for t, p in pos}
        if ch:
            self.bones[name] = ch
        return self

    def entry(self):
        a = {"animation_length": round(self.length, 3), "bones": self.bones}
        if self.loop:
            a["loop"] = True
        else:
            a["loop"] = False
        return self.name, a


def emit_anims(path, anims):
    data = {"format_version": "1.8.0",
            "animations": dict(anims)}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1) + "\n")


# ------------------------------------------------------------ validation

def validate(geo_bones, anims, tex, cubes, atlas=128):
    errors = []
    # 1. animation bones must exist
    geo_names = {b["name"] for b in geo_bones}
    for name, a in anims.items():
        for b in a["bones"]:
            if b not in geo_names:
                errors.append(f"{name}: animated bone missing in geo: {b}")
    # 2. face rects inside atlas + opaque
    for c in cubes:
        u, v = c["tex"]
        w, h, d = c["size"]
        for face, (x, y, fw, fh) in face_rects(u, v, w, h, d).items():
            if x < 0 or y < 0 or x + fw > atlas or y + fh > atlas:
                errors.append(f"{c['name']}.{face}: rect out of atlas")
                continue
            for j in range(y, y + fh):
                for i in range(x, x + fw):
                    if tex.px[i, j][3] == 0:
                        errors.append(f"{c['name']}.{face}: transparent texel at ({i},{j})")
                        break
                else:
                    continue
                break
    # 3. UV rect overlap between different cubes
    rects = []
    for c in cubes:
        u, v = c["tex"]
        w, h, d = c["size"]
        for face, r in face_rects(u, v, w, h, d).items():
            rects.append((c["name"], face, r))
    for i in range(len(rects)):
        for k in range(i + 1, len(rects)):
            n1, f1, r1 = rects[i]
            n2, f2, r2 = rects[k]
            if n1 == n2:
                continue
            if r1[0] < r2[0] + r2[2] and r2[0] < r1[0] + r1[2] and r1[1] < r2[1] + r2[3] and r2[1] < r1[1] + r1[3]:
                errors.append(f"UV overlap: {n1}.{f1} vs {n2}.{f2}")
    return errors


def seg_box_clearance(p0, p1, box, pad=0.0):
    """2D (x,z) segment vs AABB clearance check for equipment vs body parts."""
    (x0, z0), (x1, z1) = p0, p1
    bx, bz, bw, bd = box
    steps = 24
    for s in range(steps + 1):
        t = s / steps
        x = x0 + (x1 - x0) * t
        z = z0 + (z1 - z0) * t
        if bx - pad <= x <= bx + bw + pad and bz - pad <= z <= bz + bd + pad:
            return False
    return True
