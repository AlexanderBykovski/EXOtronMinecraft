#!/usr/bin/env python3
"""Strict, dependency-free validation for the mod's authored resources."""

from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src/main/resources"
ASSETS = RESOURCES / "assets/opusvsexe"
SHARED_ANIMATIONS = {
    Path("dark_forest/effects.animation.json"),
    Path("dark_forest/mossbound_attacks.animation.json"),
    Path("paradise/angel_attacks.animation.json"),
}


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def validate_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=unique_object)


def validate_png(path: Path) -> None:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("invalid PNG signature")
    offset = 8
    saw_header = False
    saw_end = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload_end = offset + 8 + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            raise ValueError("truncated PNG chunk")
        expected = struct.unpack(">I", data[payload_end:crc_end])[0]
        actual = zlib.crc32(kind + data[offset + 8:payload_end]) & 0xFFFFFFFF
        if expected != actual:
            raise ValueError(f"bad PNG CRC in {kind!r}")
        if kind == b"IHDR":
            width, height = struct.unpack(">II", data[offset + 8:offset + 16])
            if width <= 0 or height <= 0:
                raise ValueError("non-positive PNG dimensions")
            saw_header = True
        if kind == b"IEND":
            saw_end = True
            break
        offset = crc_end
    if not saw_header or not saw_end:
        raise ValueError("incomplete PNG")


def validate_ogg(path: Path) -> None:
    if not path.read_bytes().startswith(b"OggS"):
        raise ValueError("invalid Ogg container signature")


def validate_gecko_pairs() -> int:
    checked = 0
    for animation_path in sorted((ASSETS / "animations").rglob("*.animation.json")):
        relative = animation_path.relative_to(ASSETS / "animations")
        geo_relative = Path(str(relative).replace(".animation.json", ".geo.json"))
        geo_path = ASSETS / "geo" / geo_relative
        animation = validate_json(animation_path)
        validate_keyframe_times(animation_path, animation)
        if not geo_path.exists():
            if relative in SHARED_ANIMATIONS:
                checked += 1
                continue
            raise ValueError(
                f"{animation_path.relative_to(ROOT)} has no matching geometry "
                f"{geo_path.relative_to(ROOT)}"
            )
        geometry = validate_json(geo_path)
        model_bones = {
            bone["name"]
            for model in geometry.get("minecraft:geometry", [])
            for bone in model.get("bones", [])
        }
        animation_bones = {
            bone_name
            for clip in animation.get("animations", {}).values()
            for bone_name in clip.get("bones", {})
        }
        missing = animation_bones - model_bones
        if missing:
            raise ValueError(
                f"{animation_path.relative_to(ROOT)} references missing bones: {sorted(missing)}"
            )
        checked += 1
    return checked


def _channel_times(channel: object) -> list[float]:
    """Keyframe times of one bone channel, in dict- and list-form."""
    times: list[float] = []
    if isinstance(channel, dict):
        for key in channel:
            try:
                times.append(float(key))
            except (TypeError, ValueError):
                continue
    elif isinstance(channel, list):
        for entry in channel:
            if isinstance(entry, dict) and "time" in entry:
                try:
                    times.append(float(entry["time"]))
                except (TypeError, ValueError):
                    continue
    return times


def validate_keyframe_times(animation_path: Path, animation: object) -> None:
    """Fail on two keyframes sharing one tick in a channel.

    Distinct JSON keys such as "0" and "0.0" parse to the same float time;
    newer GeckoLib rejects that with "Invalid keyframe data - multiple
    starting keyframes", which aborts the whole resource reload in-game
    (tofu fonts, null ModelManager state, render crash).
    """
    if not isinstance(animation, dict):
        return
    for clip_name, clip in animation.get("animations", {}).items():
        if not isinstance(clip, dict):
            continue
        for bone_name, channels in clip.get("bones", {}).items():
            if not isinstance(channels, dict):
                continue
            for channel_name, channel in channels.items():
                seen: set[float] = set()
                for time in _channel_times(channel):
                    if time in seen:
                        raise ValueError(
                            f"{animation_path.relative_to(ROOT)} {clip_name}/{bone_name}/"
                            f"{channel_name}: duplicate keyframe time {time:g}s"
                        )
                    seen.add(time)


def main() -> int:
    errors: list[str] = []
    json_files = sorted(RESOURCES.rglob("*.json"))
    png_files = sorted(RESOURCES.rglob("*.png"))
    ogg_files = sorted(RESOURCES.rglob("*.ogg"))

    for validator, paths in ((validate_json, json_files), (validate_png, png_files), (validate_ogg, ogg_files)):
        for path in paths:
            try:
                validator(path)
            except Exception as error:  # report every bad asset in one pass
                errors.append(f"{path.relative_to(ROOT)}: {error}")

    gecko_pairs = 0
    try:
        gecko_pairs = validate_gecko_pairs()
    except Exception as error:
        errors.append(str(error))

    if errors:
        print("Resource validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(json_files)} JSON, {len(png_files)} PNG, "
        f"{len(ogg_files)} OGG and {gecko_pairs} Gecko model/animation pairs."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
