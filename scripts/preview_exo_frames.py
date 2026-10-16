#!/usr/bin/env python3
"""Preview renderer for the EXO-1..4 frames: replicates the GeckoLib 4.4.9 pipeline.

Verified against sources (BakedModelFactory.Builtin, AnimationController,
RenderUtils, GeoEntityRenderer.renderRecursively):
  - bone: updatePivot(-px, py, pz); updateRotation toRadians(-rx, -ry, rz)
  - cube origin: -> (-(ox+w), oy, oz); vertices drawn at stored origin coords
  - bone matrix: T(p') * Rz * Ry * Rx * S * T(-p')   (p' = mirrored pivot)
  - animation rotation: degrees -> radians, NEGATE X and Y, Z unchanged
  - animation value added to the bone's static (initial snapshot) rotation
  - scale keyframe values applied directly (pivot-anchored)
  - loop() animation: time wraps at animation_length; linear interpolation
  - per-face UV dict: v origin is TOP of the texture (uv v is canvas y).

Output: build/preview_exo_frames/<frame>_<pose>_<view>.png and
<frame>_sheet.png (poses x views). Views: front(-Z), side(+X), back(+Z).

Usage: python3 scripts/preview_exo_frames.py [frames...]
"""

from __future__ import annotations

import json
import math
import sys
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build/preview_exo_frames"
ASSETS = ROOT / "src/main/resources/assets/opusvsexe"
TEX = ASSETS / "textures/entity"
ANIM = ASSETS / "animations/entity"

SS = 2  # supersampling
IMG_W = 240
IMG_H = 264
PAD = 6

MAT4_IDENT = None


# ---------------------------------------------------------------------------
# tiny matrix + vector helpers (column-vector convention: M @ v)
# ---------------------------------------------------------------------------


def mat_identity():
    return [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def mat_translation(x, y, z):
    m = mat_identity()
    m[0][3], m[1][3], m[2][3] = x, y, z
    return m


def mat_rot(axis, rad):
    c, s = math.cos(rad), math.sin(rad)
    m = mat_identity()
    if axis == "x":
        m[1][1], m[1][2], m[2][1], m[2][2] = c, -s, s, c
    elif axis == "y":
        m[0][0], m[0][2], m[2][0], m[2][2] = c, s, -s, c
    else:
        m[0][0], m[0][1], m[1][0], m[1][1] = c, -s, s, c
    return m


def mat_scale(sx, sy, sz):
    m = mat_identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def mat_apply(m, v):
    return [
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2] + m[0][3],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2] + m[1][3],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2] + m[2][3],
    ]


# ---------------------------------------------------------------------------
# animation sampling
# ---------------------------------------------------------------------------


def interp_kfs(kfs, t):
    """kfs: {time: {vector: [..]} or [..]}; linear interp (times in seconds)."""
    if not kfs:
        return None

    def val(v):
        return v["vector"] if isinstance(v, dict) and "vector" in v else list(v)

    items = sorted((float(k), val(v)) for k, v in kfs.items())
    if t <= items[0][0]:
        return items[0][1]
    if t >= items[-1][0]:
        return items[-1][1]
    for i in range(len(items) - 1):
        t0, v0 = items[i]
        t1, v1 = items[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return [a + (b - a) * f for a, b in zip(v0, v1)]
    return items[-1][1]


def sample_bones(anims, anim_name, t):
    """Returns {bone_name: (rot[deg-signed], scale[3])} in GeckoLib-processed units."""
    anim = anims.get(anim_name)
    if anim is None:
        return {}
    length = anim.get("animation_length")
    if anim.get("loop") and length and t > length:
        t = t % length
    out = {}
    for bone, tracks in anim.get("bones", {}).items():
        rot = None
        scale = None
        if "rotation" in tracks:
            v = interp_kfs(tracks["rotation"], t)
            if v is not None:
                rot = [math.radians(-v[0]), math.radians(-v[1]), math.radians(v[2])]
        if "scale" in tracks:
            v = interp_kfs(tracks["scale"], t)
            if v is not None:
                scale = list(v)
        if "position" in tracks:
            pass  # unused by our anims
        out[bone] = (rot, scale)
    return out


# ---------------------------------------------------------------------------
# bone matrices
# ---------------------------------------------------------------------------


def compute_matrices(styles, anims, anim_name, t):
    anim_state = sample_bones(anims, anim_name, t)
    mats = {}

    def walk(bone, parent_world):
        p = bone["pivot"]
        p2 = (-p[0], p[1], p[2])
        rx, ry, rz = 0.0, 0.0, 0.0
        sx = sy = sz = 1.0
        st = bone.get("rot")
        if st:
            rx += -math.radians(st[0])
            ry += -math.radians(st[1])
            rz += math.radians(st[2])
        anim_rot, anim_scale = anim_state.get(bone["name"], (None, None))
        if anim_rot:
            rx += anim_rot[0]
            ry += anim_rot[1]
            rz += anim_rot[2]
        if anim_scale:
            sx, sy, sz = anim_scale
        local = mul(mat_translation(*p2),
                    mul(mat_rot("z", rz),
                        mul(mat_rot("y", ry),
                            mul(mat_rot("x", rx),
                                mul(mat_scale(sx, sy, sz), mat_translation(-p2[0], -p2[1], -p2[2]))))))
        world = mul(parent_world, local)
        mats[bone["name"]] = world
        for child in bone.get("children", []):
            walk(child, world)

    roots = [b for b in styles["bones"] if not b.get("parent")]
    for r in roots:
        walk(r, mat_identity())
    return mats


# ---------------------------------------------------------------------------
# cube world quads
# ---------------------------------------------------------------------------


def build_cubes(styles, mats):
    """Returns flat list of (world_quad_corners[4], uv_corner_pairs[4], tex, rgba(avg?))"""
    out = []
    for b in styles["bones"]:
        m = mats[b["name"]]
        for c in b["cubes"]:
            o = c["o"]
            s = c["s"]
            o2 = (-(o[0] + s[0]), o[1], o[2])
            x0, y0, z0 = o2
            x1, y1, z1 = x0 + s[0], y0 + s[1], z0 + s[2]
            for face, (u, v, w, h) in c["uv"].items():
                if face == "north":
                    corn = [(x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0)]
                elif face == "south":
                    corn = [(x1, y1, z1), (x0, y1, z1), (x0, y0, z1), (x1, y0, z1)]
                elif face == "east":
                    corn = [(x1, y1, z0), (x1, y1, z1), (x1, y0, z1), (x1, y0, z0)]
                elif face == "west":
                    corn = [(x0, y1, z1), (x0, y1, z0), (x0, y0, z0), (x0, y0, z1)]
                elif face == "up":
                    corn = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
                else:
                    corn = [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]
                wcorn = [mat_apply(m, [(vx), (vy), (vz)]) for vx, vy, vz in corn]
                uvs = [(u, v), (u + w, v), (u + w, v + h), (u, v + h)]
                out.append((wcorn, uvs))
    return out


# ---------------------------------------------------------------------------
# rasterization
# ---------------------------------------------------------------------------


def view_axes(view):
    """Returns (screen_x_axis, screen_y_axis, depth_axis) mapping world->screen."""
    if view == "front":  # camera at -Z looking +Z
        return (lambda wx, wy, wz: (-wx, wy, wz))
    if view == "back":  # camera at +Z looking -Z
        return (lambda wx, wy, wz: (wx, wy, -wz))
    # side: camera at +X looking -X (screen right = -Z)
    return (lambda wx, wy, wz: (-wz, wy, wx))


def rasterize(frame_name, quads, tex, pose_tag, view, dirpath):
    proj = view_axes(view)
    W, H = IMG_W * SS, IMG_H * SS
    zbuf = [[1e9] * W for _ in range(H)]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    tw, th = tex.size
    samp = tex.load()
    allw = []
    for wcorn, uvs in quads:
        allw += [proj(v[0], v[1], v[2]) for v in wcorn]
    xs = [v[0] for v in allw]
    ys = [v[1] for v in allw]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    span_x = max(1e-6, maxx - minx)
    span_y = max(1e-6, maxy - miny)
    scale = min((W - 2 * PAD * SS) / span_x, (H - 2 * PAD * SS) / span_y)
    offx = (W - span_x * scale) / 2
    offy = (H - span_y * scale) / 2

    def to_screen(p):
        return (offx + (p[0] - minx) * scale, offy + (H - (p[1] - miny) * scale))

    for wcorn, uvs in quads:
        sc = [to_screen(proj(v[0], v[1], v[2])) for v in wcorn]
        sxs = [c[0] for c in sc]
        sys_ = [c[1] for c in sc]
        bx0, bx1 = max(0, int(min(sxs))), min(W - 1, int(max(sxs)) + 1)
        by0, by1 = max(0, int(min(sys_))), min(H - 1, int(max(sys_)) + 1)
        if bx1 < bx0 or by1 < by0:
            continue
        # affine mapping inside the quad: p(s,t) = c0 + s*(c1-c0) + t*(c3-c0)
        c0 = sc[0]
        e1 = (sc[1][0] - c0[0], sc[1][1] - c0[1])
        e2 = (sc[3][0] - c0[0], sc[3][1] - c0[1])
        det = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(det) < 1e-9:
            continue
        u0, v0 = uvs[0]
        uu1 = (uvs[1][0] - u0, uvs[1][1] - v0)
        uu2 = (uvs[3][0] - u0, uvs[3][1] - v0)
        depths = [proj(v[0], v[1], v[2])[2] for v in wcorn]
        d0, de1, de2 = depths[0], depths[1] - depths[0], depths[3] - depths[0]
        for sy_ in range(by0, by1 + 1):
            for sx_ in range(bx0, bx1 + 1):
                dx = sx_ + 0.5 - c0[0]
                dy = sy_ + 0.5 - c0[1]
                s = (dx * e2[1] - dy * e2[0]) / det
                t = (e1[0] * dy - e1[1] * dx) / det
                if -0.001 > s or s > 1.001 or -0.001 > t or t > 1.001:
                    continue
                depth = d0 + de1 * s + de2 * t
                if depth >= zbuf[sy_][sx_]:
                    continue
                ux = u0 + uu1[0] * s + uu2[0] * t
                uy = v0 + uu1[1] * s + uu2[1] * t
                # mirror on east/west faces for the loaded cube: for west use (1-s)
                tx = ux % tw
                ty = uy % th
                rgba = samp[int(tx), int(ty)]
                zbuf[sy_][sx_] = depth
                if rgba[3] == 0:
                    px[sx_, sy_] = (0, 0, 0, 0)
                else:
                    px[sx_, sy_] = rgba
    final = img.resize((IMG_W, IMG_H), Image.NEAREST)
    final.save(dirpath)


def sheet(files, outname):
    """Compose poses(rows) x views(cols) sheet."""
    names = [
        f for f in files
    ]
    cols = 3
    rows = (len(names) + cols - 1) // cols
    sheet_img = Image.new("RGBA", (IMG_W * cols, IMG_H * rows), (255, 255, 255, 255))
    for i, f in enumerate(names):
        im = Image.open(f).convert("RGBA")
        sheet_img.paste(im, ((i % cols) * IMG_W, (i // cols) * IMG_H))
    sheet_img.save(BUILD / outname)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


POSES = {
    "exo_1_sentinel": [("idle", 0.0), ("idle", 1.2), ("walk", 0.45), ("attack", 0.45), ("punch", 0.4),
                       ("slam", 0.62), ("energy_shield_hold", 0.8), ("hurt", 0.3), ("death", 1.6)],
    "exo_2_hunter": [("idle", 0.0), ("idle", 0.7), ("walk", 0.25), ("attack", 0.3), ("punch", 0.27),
                     ("chest_shot", 0.4), ("dash", 0.3), ("hurt", 0.3), ("death", 1.6)],
    "exo_3_vanguard": [("idle", 0.0), ("idle", 1.0), ("walk", 0.35), ("attack", 0.4), ("punch", 0.4),
                       ("slam", 0.62), ("energy_shield_hold", 0.8), ("dash", 0.3), ("death", 1.6)],
    "exo_4_titan": [("idle", 0.0), ("idle", 1.4), ("walk", 0.55), ("attack", 0.47), ("punch", 0.5),
                    ("slam", 0.62), ("energy_shield_hold", 0.8), ("dash", 0.3), ("death", 1.6)],
}


def main(frames=None):
    BUILD.mkdir(parents=True, exist_ok=True)
    frames = frames or list(POSES)
    for fkey in frames:
        styles = json.loads((BUILD / f"styles_{fkey}.json").read_text(encoding="utf-8"))
        anims = json.loads((ANIM / f"{fkey}.animation.json").read_text(encoding="utf-8"))["animations"]
        tex = Image.open(TEX / f"{fkey}.png").convert("RGBA")
        # resolve children for ordered walk
        for b in styles["bones"]:
            b["children"] = [c for c in styles["bones"] if c.get("parent") == b["name"]]
        quads_cache = {}
        files = []
        names = []
        for i, (anim_name, t) in enumerate(POSES[fkey]):
            mats = compute_matrices(styles, anims, anim_name, t)
            quads = build_cubes(styles, mats)
            for view in ("front", "side", "back"):
                fname = f"{fkey}_{anim_name!s}_{view}.png".replace("-", "_")
                rasterize(fkey, quads, tex, f"{anim_name}@{t}", view, BUILD / fname)
            front = f"{BUILD}/{fkey}_{anim_name!s}_front.png".replace("-", "_")
            files.append(front)
            names.append(f"{anim_name}@{t}")
        sheet(files, f"{fkey}_sheet.png")
        print(f"previewed {fkey}: {len(POSES[fkey])} poses x3 views -> {fkey}_sheet.png")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
