"""Create the second-pass recipes for craftable equipment and utility blocks.

Boss trophies, memory fragments, natural ore and spawn eggs intentionally stay
non-craftable: they are progression gates and exploration rewards.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/data/opusvsexe/recipes"


def item(name: str) -> dict:
    return {"item": name if ":" in name else f"opusvsexe:{name}"}


def write_shapeless(recipe_id: str, result: str, ingredients: list[str], count: int = 1) -> None:
    data = {
        # Small recipes are also valid in a normal 3x3 crafting table. Larger
        # recipes remain exclusive to the Opus Assembly Table.
        "type": "minecraft:crafting_shapeless" if len(ingredients) <= 9 else "opusvsexe:assembly",
        "group": "opusvsexe:assembly",
        "ingredients": [item(ingredient) for ingredient in ingredients],
        "result": {"item": result if ":" in result else f"opusvsexe:{result}", **({"count": count} if count != 1 else {})},
    }
    (ROOT / f"{recipe_id}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CRAFTS: dict[str, tuple[str, list[str], int]] = {
    # Opus weapons and the ranged arsenal.
    "katana_op": ("katana_op", ["core_opus", "stabilized_opus", "minecraft:iron_ingot", "minecraft:iron_ingot"], 1),
    "katana_gold": ("katana_gold", ["raw_opus", "minecraft:gold_ingot", "minecraft:gold_ingot", "minecraft:iron_ingot"], 1),
    "katana_refined": ("katana_refined", ["katana_gold", "resonant_opus", "core_opus"], 1),
    "opus_warhammer": ("opus_warhammer", ["titan_plate", "core_opus", "minecraft:iron_block", "minecraft:stick", "minecraft:stick"], 1),
    "laser_gun": ("laser_gun", ["raw_opus", "minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:redstone", "minecraft:quartz"], 1),
    "light_laser_gun": ("light_laser_gun", ["laser_gun", "raw_opus", "minecraft:redstone", "minecraft:quartz"], 1),
    "heavy_laser_gun": ("heavy_laser_gun", ["light_laser_gun", "stabilized_opus", "minecraft:iron_block", "minecraft:redstone_block"], 1),
    "sky_laser_gun": ("sky_laser_gun", ["heavy_laser_gun", "resonant_opus", "ai_tear", "minecraft:nether_star"], 1),
    "radio": ("radio", ["minecraft:iron_ingot", "minecraft:copper_ingot", "minecraft:redstone", "memory_cable"], 1),
    "titan_plate": ("titan_plate", ["minecraft:netherite_ingot", "resonant_opus", "opus_fragment"], 1),

    # Shadow armour: a stealth branch based on drops from the Dark Forest.
    "shadow_helmet": ("shadow_helmet", ["shade_silk", "shade_silk", "shade_silk", "shade_silk", "rootbound_eye", "core_opus"], 1),
    "shadow_chestplate": ("shadow_chestplate", ["shade_silk", "shade_silk", "shade_silk", "shade_silk", "shade_silk", "shade_silk", "rootbound_eye", "core_opus"], 1),
    "shadow_leggings": ("shadow_leggings", ["shade_silk", "shade_silk", "shade_silk", "shade_silk", "shade_silk", "rootbound_eye", "core_opus"], 1),
    "shadow_boots": ("shadow_boots", ["shade_silk", "shade_silk", "rootbound_eye", "core_opus"], 1),

    # Laboratory and expedition construction materials.
    "cracked_lab_concrete": ("cracked_lab_concrete", ["minecraft:stone", "minecraft:iron_nugget", "raw_opus"], 4),
    "lab_floor_grate": ("lab_floor_grate", ["minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot", "raw_opus"], 4),
    "opus_containment_glass": ("opus_containment_glass", ["minecraft:glass", "minecraft:glass", "minecraft:quartz", "raw_opus"], 4),
    "scorched_concrete": ("scorched_concrete", ["minecraft:blackstone", "magma_crust", "raw_opus"], 4),
    "oil_stain": ("oil_stain", ["minecraft:coal", "minecraft:slime_ball", "minecraft:black_dye"], 2),
    "fortress_plating": ("fortress_plating", ["minecraft:iron_block", "minecraft:nether_brick", "stabilized_opus"], 2),
    "memory_glass": ("memory_glass", ["minecraft:glass", "minecraft:amethyst_shard", "resonant_opus"], 4),
    "omega_frame": ("omega_frame", ["minecraft:iron_block", "core_opus", "opus_fragment"], 1),
    "citadel_vein": ("citadel_vein", ["minecraft:iron_nugget", "haiku_core", "stabilized_opus"], 2),
    "tank_trap": ("tank_trap", ["minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot", "titan_plate"], 2),
    "data_conduit": ("data_conduit", ["minecraft:copper_ingot", "minecraft:redstone", "raw_opus"], 2),
    "memory_cable": ("memory_cable", ["minecraft:copper_ingot", "minecraft:redstone", "memory_glass"], 4),
    "signal_panel": ("signal_panel", ["memory_cable", "minecraft:iron_ingot", "raw_opus"], 1),
    "memory_sludge": ("memory_sludge", ["minecraft:slime_ball", "memory_glass", "raw_opus"], 2),
    "hazard_emitter": ("hazard_emitter", ["minecraft:redstone_torch", "minecraft:iron_ingot", "fire_essence"], 1),
    "marsh_filter": ("marsh_filter", ["minecraft:iron_bars", "minecraft:water_bucket", "memory_cable"], 1),

    # Terminals, stations and encounter infrastructure.
    "dead_terminal": ("dead_terminal", ["minecraft:iron_ingot", "minecraft:redstone", "data_conduit"], 1),
    "flickering_terminal": ("flickering_terminal", ["dead_terminal", "core_opus", "minecraft:redstone"], 1),
    "blueprint_table": ("blueprint_table", ["minecraft:oak_planks", "minecraft:paper", "minecraft:ink_sac", "memory_glass"], 1),
    "broken_resonance_forge": ("broken_resonance_forge", ["minecraft:stone", "raw_opus", "minecraft:blast_furnace"], 1),
    "resonance_forge": ("resonance_forge", ["broken_resonance_forge", "stabilized_opus", "minecraft:iron_block", "minecraft:blast_furnace"], 1),
    "katana_stand": ("katana_stand", ["minecraft:oak_planks", "minecraft:stick", "minecraft:gold_nugget"], 1),
    "scanner_eye": ("scanner_eye", ["minecraft:ender_eye", "core_opus", "memory_glass"], 1),
    "pulse_turret": ("pulse_turret", ["minecraft:iron_block", "minecraft:redstone", "core_opus"], 1),
    "wave_terminal": ("wave_terminal", ["scanner_eye", "minecraft:copper_ingot", "resonant_opus"], 1),
    "command_terminal": ("command_terminal", ["wave_terminal", "core_opus", "ai_tear"], 1),
    "memory_console": ("memory_console", ["memory_glass", "data_conduit", "core_opus"], 1),
    "arena_gate": ("arena_gate", ["minecraft:iron_bars", "fortress_plating", "core_opus"], 1),
    "phase_gate": ("phase_gate", ["minecraft:obsidian", "minecraft:ender_pearl", "resonant_opus"], 1),
    "sealed_bulkhead": ("sealed_bulkhead", ["minecraft:iron_block", "fortress_plating", "titan_plate"], 1),
    "sealed_hatch": ("sealed_hatch", ["minecraft:iron_block", "fortress_plating", "titan_plate", "minecraft:iron_trapdoor"], 1),
    "shield_node": ("shield_node", ["minecraft:shield", "core_opus", "pulsing_core"], 1),
    "gravity_anchor": ("gravity_anchor", ["minecraft:obsidian", "core_opus", "titan_plate"], 1),
    "combat_beacon": ("combat_beacon", ["minecraft:beacon", "core_opus", "titan_plate"], 1),
    "trial_trigger": ("trial_trigger", ["minecraft:redstone_block", "pulsing_core", "titan_plate"], 1),
    "reward_vault": ("reward_vault", ["minecraft:chest", "reinforced_opus_block", "core_opus"], 1),
    "dormant_spawner": ("dormant_spawner", ["minecraft:iron_bars", "core_opus", "opus_fragment"], 1),

    # Colosseum and barrier kit.
    "reinforced_opus_block": ("reinforced_opus_block", ["core_opus"] * 9, 1),
    "haiku_amber_block": ("haiku_amber_block", ["haiku_core", "minecraft:gold_block", "ai_tear"], 1),
    "amber_pillar": ("amber_pillar", ["haiku_amber_block", "minecraft:polished_deepslate"], 2),
    "colosseum_concrete": ("colosseum_concrete", ["minecraft:gray_concrete", "minecraft:iron_nugget", "haiku_core"], 4),
    "colosseum_wall": ("colosseum_wall", ["colosseum_concrete", "fortress_plating"], 2),
    "energy_barrier": ("energy_barrier", ["minecraft:iron_bars", "minecraft:glass", "core_opus"], 2),
    "energy_barrier_red": ("energy_barrier_red", ["energy_barrier", "minecraft:red_dye"], 2),
    "energy_barrier_blue": ("energy_barrier_blue", ["energy_barrier", "minecraft:blue_dye"], 2),
    "energy_beam": ("energy_beam", ["energy_barrier", "minecraft:amethyst_shard", "resonant_opus"], 2),
    "force_field_projector": ("force_field_projector", ["energy_beam", "core_opus", "minecraft:iron_block"], 1),
    "phased_barrier": ("phased_barrier", ["energy_barrier_blue", "minecraft:ender_pearl", "resonant_opus"], 1),
    "sequence_keypad": ("sequence_keypad", ["minecraft:iron_ingot", "minecraft:redstone", "data_conduit"], 1),
    "energy_relay": ("energy_relay", ["minecraft:copper_ingot", "minecraft:redstone", "core_opus"], 1),
}


for recipe_id, (result, ingredients, count) in CRAFTS.items():
    write_shapeless(recipe_id, result, ingredients, count)

print(f"Generated {len(CRAFTS)} additional 5x5 assembly recipes")
