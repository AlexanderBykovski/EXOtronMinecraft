#!/usr/bin/env bash
# Преобразование звуков Омеги из приложенных файлов (~Downloads) в OGG.
# Использование: bash conver_omega_sounds.sh /path/to/source/audio
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
SRC="${1:-}"
OUT="$ROOT/src/main/resources/assets/opusvsexe/sounds"
if [[ -z "$SRC" || ! -d "$SRC" ]]; then
    printf 'usage: %s /path/to/source/audio\n' "$0" >&2
    exit 2
fi
mkdir -p "$OUT"

conv() {
    local name="$1" src="$2" out="$3"
    ffmpeg -y -loglevel error -i "$SRC/$src" -c:a libvorbis -q:a 6 -ac 1 -ar 44100 "$OUT/$out"
    printf "ok %-25s -> %s\n" "$src" "$out"
}

conv haiku_omega_death  "Haiku_omega_death.mp3" haiku_omega_death.ogg
conv omega_ring_wave    "omega_ring_wave.wav"   omega_ring_wave.ogg
conv omega_slash        "omega_slash.mp3"       omega_slash.ogg
conv altar_heart_loop   "altar heart.mp3"       altar_heart_loop.ogg
conv sky_laser_warn     "sky_laser_warn.mp3"    sky_laser_warn.ogg
conv sky_laser_omega    "sky_laser_omega.mp3"   sky_laser_omega.ogg

echo "done -> $OUT"
