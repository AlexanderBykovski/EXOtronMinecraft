#!/usr/bin/env python3
"""Validate geo/animation/texture consistency for a list of asset triplets."""
import json, sys, math, struct

def validate(geo_path, anim_path, tex_path):
    with open(geo_path, encoding='utf-8') as handle:
        geo = json.load(handle)['minecraft:geometry'][0]
    desc = geo['description']
    tw, th = desc['texture_width'], desc['texture_height']
    bones = {b['name']: b for b in geo['bones']}
    errors = []
    with open(tex_path, 'rb') as handle:
        header = handle.read(24)
    if len(header) < 24 or not header.startswith(b'\x89PNG\r\n\x1a\n'):
        errors.append(f"texture {tex_path}: invalid PNG header")
    else:
        actual_width, actual_height = struct.unpack('>II', header[16:24])
        if (actual_width, actual_height) != (tw, th):
            errors.append(
                f"texture {tex_path}: {actual_width}x{actual_height}, expected {tw}x{th}"
            )
    # uv bounds
    for b in geo['bones']:
        parent = b.get('parent')
        if parent and parent not in bones:
            errors.append(f"bone {b['name']}: missing parent {parent}")
        for c in b.get('cubes', []):
            if not isinstance(c.get('uv'), list) or len(c['uv']) != 2:
                continue  # per-face uv dict or other extended form: out of scope here
            u, v = c['uv']
            w, h, d = c['size']
            need_w, need_h = 2 * (w + d), d + h
            if u + need_w > tw + 0.01 or v + need_h > th + 0.01:
                errors.append(f"bone {b['name']}: uv ({u},{v}) + {need_w}x{need_h} exceeds {tw}x{th}")
            if u < -0.01 or v < -0.01:
                errors.append(f"bone {b['name']}: negative uv")
    # animations
    if anim_path:
        with open(anim_path, encoding='utf-8') as handle:
            anims = json.load(handle)['animations']
        for aname, anim in anims.items():
            for bone_name in anim.get('bones', {}):
                if bone_name not in bones:
                    errors.append(f"anim {aname}: bone '{bone_name}' not in geo")
            length = anim.get('animation_length', 0)
            for bone_name, channels in anim.get('bones', {}).items():
                for ch, track in channels.items():
                    times = []
                    items = track if isinstance(track, list) else (track or {})
                    for t in items:
                        if isinstance(items, list):
                            if not isinstance(t, dict) or 'time' not in t:
                                continue
                            t = t['time']
                        try:
                            tv = float(t)
                        except (TypeError, ValueError):
                            errors.append(f"anim {aname}/{bone_name}/{ch}: bad time key {t}")
                            continue
                        times.append(tv)
                        if tv > length + 0.01:
                            errors.append(f"anim {aname}/{bone_name}/{ch}: key {t}s > length {length}s")
                    # distinct JSON keys ("0" vs "0.0") can share one float
                    # time; GeckoLib >= 4.8 aborts the whole resource reload
                    # on that ("multiple starting keyframes").
                    seen = set()
                    for tv in times:
                        if tv in seen:
                            errors.append(f"anim {aname}/{bone_name}/{ch}: duplicate keyframe time {tv:g}s")
                        seen.add(tv)
            # loop continuity for looping anims: first/last rotation keys should match mod 360
            if anim.get('loop'):
                for bone_name, channels in anim.get('bones', {}).items():
                    rot = channels.get('rotation') or {}
                    if not isinstance(rot, dict) or not rot:
                        continue
                    keys = sorted(rot.keys(), key=float)
                    first, last = rot[keys[0]], rot[keys[-1]]
                    if not (isinstance(first, list) and isinstance(last, list)):
                        continue  # eased/catmullrom key dicts carry no plain vector here
                    for i in range(3):
                        diff = abs(first[i] - last[i]) % 360
                        if min(diff, 360 - diff) > 1.0:
                            errors.append(f"anim {aname}/{bone_name}: loop discontinuity axis {i}: {first[i]} vs {last[i]}")
                            break
    print(('FAIL ' if errors else 'OK   ') + geo_path.split('/')[-1])
    for e in errors:
        print('   -', e)
    return not errors

if __name__ == '__main__':
    ok = True
    for triplet in sys.argv[1:]:
        geo, anim, tex = triplet.split(',')
        ok &= validate(geo, anim if anim != '-' else None, tex)
    sys.exit(0 if ok else 1)
