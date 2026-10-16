"""Move vanilla-shaped/shapeless mod recipes onto the 5x5 assembly table."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/data/opusvsexe/recipes"
SKIP = {"opus_assembly_table.json"}

for path in sorted(ROOT.glob("*.json")):
    if path.name in SKIP:
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("type") in {"minecraft:crafting_shaped", "minecraft:crafting_shapeless"}:
        data["type"] = "opusvsexe:assembly"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
