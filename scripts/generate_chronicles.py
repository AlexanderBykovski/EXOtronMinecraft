"""Generate a compact, guided Chronicles tree for the OpusVsExe mod.

The screen contains only meaningful milestones. Individual recipes, fragments,
structures and creatures remain tracked as criteria inside their archive node,
so the player can still complete every part of the mod without a wall of icons.
"""

from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1] / "src/main/resources"
ADV = BASE / "data/opusvsexe/advancements/chronicles"
LANG_DIR = BASE / "assets/opusvsexe/lang"
RECIPES = BASE / "data/opusvsexe/recipes"

for path in ADV.rglob("*.json"):
    path.unlink()
(ADV / "route").mkdir(parents=True, exist_ok=True)


def write(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def display(title_id, description_id, icon, frame="task", toast=False, background=None):
    result = {
        "display": {
            "icon": {"item": icon},
            "title": {"translate": f"advancement.opusvsexe.chronicles.{title_id}.title"},
            "description": {"translate": f"advancement.opusvsexe.chronicles.{description_id}.description"},
            "frame": frame,
            "show_toast": toast,
            "announce_to_chat": False,
            "hidden": False,
        }
    }
    if background:
        # Minecraft 1.20.1 reads the background from DisplayInfo, not the root
        # advancement object. Keeping it here prevents the checkerboard texture.
        result["display"]["background"] = background
    return result


def advancement(parent, title_id, description_id, icon, criteria,
                 frame="task", toast=False, requirements=None, xp=0):
    data = display(title_id, description_id, icon, frame, toast)
    if parent:
        data["parent"] = parent if ":" in parent else f"opusvsexe:{parent}"
    data["criteria"] = criteria
    if requirements is not None:
        data["requirements"] = requirements
    if xp:
        data["rewards"] = {"experience": xp}
    return data


def inventory(item):
    return {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": [item]}]}}


def recipe(recipe_id):
    return {"trigger": "minecraft:recipe_unlocked", "conditions": {"recipe": f"opusvsexe:{recipe_id}"}}


def structure(structure_id):
    return {"trigger": "minecraft:location", "conditions": {"location": {"structure": f"opusvsexe:{structure_id}"}}}


def biome(biome_id):
    return {"trigger": "minecraft:location", "conditions": {"location": {"biome": f"opusvsexe:{biome_id}"}}}


def dimension(dimension_id):
    return {"trigger": "minecraft:changed_dimension", "conditions": {"to": f"opusvsexe:{dimension_id}"}}


def kill(entity_id):
    return {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {"type": f"opusvsexe:{entity_id}"}}}


def tame(entity_id):
    return {"trigger": "minecraft:tame_animal", "conditions": {"entity": {"type": f"opusvsexe:{entity_id}"}}}


def impossible():
    return {"trigger": "minecraft:impossible"}


def all_required(criteria):
    return [[key] for key in criteria]


BACKGROUND = "opusvsexe:textures/gui/advancements/backgrounds/chronicles.png"

# One calm entry point. Any of the three natural discoveries starts the route.
root = display("root", "root", "opusvsexe:core_opus", "task", True, BACKGROUND)
root["criteria"] = {
    "ore_signal": inventory("opusvsexe:opus_ore"),
    "memory_signal": inventory("opusvsexe:memory_fragment_1"),
    "assembly_signal": inventory("opusvsexe:opus_assembly_table"),
}
root["requirements"] = [["ore_signal", "memory_signal", "assembly_signal"]]
write(ADV / "root.json", root)

# The visible main tree is deliberately short. The order forms a readable
# route, while each archive node contains every individual item/action as
# criteria.
nodes = [
    ("route/signal", "chronicles/root", "signal", "signal", "opusvsexe:opus_ore", {}, "task", True, 25),
    ("route/assembly", "chronicles/route/signal", "assembly", "assembly", "opusvsexe:opus_assembly_table", {"table": inventory("opusvsexe:opus_assembly_table")}, "task", True, 50),
    ("route/recipes", "chronicles/route/assembly", "recipes", "recipes", "opusvsexe:core_opus", {}, "goal", True, 500),
    ("route/archive", "chronicles/route/signal", "archive", "archive", "opusvsexe:memory_fragment_15", {}, "goal", True, 500),
    ("route/resonance", "chronicles/route/assembly", "resonance", "resonance", "opusvsexe:resonance_forge", {"forge": inventory("opusvsexe:resonance_forge")}, "task", False, 100),
    ("route/exo_frame", "chronicles/route/resonance", "exo_frame", "exo_frame", "opusvsexe:exo_assembly_frame", {"frame": inventory("opusvsexe:exo_assembly_frame")}, "task", True, 100),
    ("route/exo_models", "chronicles/route/exo_frame", "exo_models", "exo_models", "opusvsexe:exo_5_activation_core", {}, "goal", True, 750),
    ("route/combat", "chronicles/route/signal", "combat", "combat", "opusvsexe:trophy_haiku_omega", {}, "goal", True, 1000),
    ("route/trophies", "chronicles/route/combat", "trophies", "trophies", "opusvsexe:trophy_haiku_omega", {}, "goal", True, 750),
    ("route/mastery", "chronicles/route/trophies", "mastery", "mastery", "opusvsexe:trophy_haiku_omega", {"omega_trophy": inventory("opusvsexe:trophy_haiku_omega")}, "challenge", True, 1500),
]

# Every root without a parent is a real vanilla advancement tab. These tabs
# keep regional content readable and restore the mod's separate worldlines.
tab_roots = [
    ("paradise/root", "paradise_root", "paradise_root", "opusvsexe:paradise_fruit", {"island": structure("paradise_island")}),
    ("fire/root", "fire_root", "fire_root", "opusvsexe:fire_essence", {"realm": dimension("fire_realm")}),
    ("dark_forest/root", "dark_forest_root", "dark_forest_root", "opusvsexe:moonflower_heart", {"forest": biome("dark_forest")}),
    ("settlements/root", "settlements_root", "settlements_root", "opusvsexe:katana", {"settlement": structure("survivor_settlement")}),
    ("expeditions/root", "expeditions_root", "expeditions_root", "opusvsexe:opus_ruins_compass", {"compass": inventory("opusvsexe:opus_ruins_compass")}),
]
for path, title, description, icon, criteria in tab_roots:
    tab = display(title, description, icon, "task", True, BACKGROUND)
    tab["criteria"] = criteria
    write(ADV / f"{path}.json", tab)

recipe_ids = sorted(path.stem for path in RECIPES.glob("*.json"))
recipe_criteria = {recipe_id: recipe(recipe_id) for recipe_id in recipe_ids}

fragment_criteria = {
    f"memory_fragment_{index}": inventory(f"opusvsexe:memory_fragment_{index}")
    for index in range(1, 16)
}

structure_ids = [
    "trial_grounds", "survivor_settlement", "paradise_island", "kimi_laboratory",
    "japanese_settlement", "haiku_citadel", "frontier_fortress", "eternal_colosseum", "data_spire",
    "coddy_workshop", "abandoned_city", "moon_fountain",
]
structure_criteria = {structure_id: structure(structure_id) for structure_id in structure_ids}

biome_criteria = {"dark_forest": biome("dark_forest"), "fire_realm": dimension("fire_realm")}

entities = [
    "haiku_1_5", "haiku_2", "haiku_3", "haiku_4", "haiku_5", "haiku_omega", "haiku_drone", "haiku_drone_plus",
    "fire_slime", "lava_golem", "fire_demon", "ember_slime", "obsidian_golem", "flame_demon",
    "sunfinch", "cloud_grazer", "paradise_wyvern", "angel_boy", "shade_spiderling", "gloom_broodmother",
    "moonwing_bat", "mossbound_enderman", "survivor", "black_ninja", "samurai", "young_samurai",
    "exo_1_sentinel", "exo_2_hunter", "exo_3_vanguard", "exo_4_titan", "exo_5_vengeance",
]
kill_criteria = {entity_id: kill(entity_id) for entity_id in entities}

compass_ids = [
    "opus_ruins_compass", "trial_grounds_expedition_compass", "survivor_settlement_expedition_compass",
    "paradise_expedition_compass", "kimi_laboratory_expedition_compass", "japanese_settlement_expedition_compass",
    "haiku_citadel_expedition_compass", "frontier_fortress_expedition_compass",
    "eternal_colosseum_expedition_compass", "data_spire_expedition_compass",
    "coddy_workshop_expedition_compass", "abandoned_city_expedition_compass",
    "dark_forest_expedition_compass", "moon_fountain_expedition_compass",
]

exo_cores = {f"exo_{index}_core": inventory(f"opusvsexe:exo_{index}_activation_core") for index in range(1, 6)}
trophy_entities = entities[:26]


def trophy_item(entity_id):
    # The registered trophy for the Fire Demon is named after its boss title.
    return "diablo" if entity_id == "fire_demon" else entity_id


nodes += [
    ("paradise/route", "opusvsexe:chronicles/paradise/root", "paradise_route", "paradise_route", "opusvsexe:paradise_fruit", {"island": structure("paradise_island")}, "task", True, 100),
    ("paradise/wyvern", "opusvsexe:chronicles/paradise/route", "paradise_wyvern", "paradise_wyvern", "opusvsexe:paradise_fruit", {"tamed": tame("paradise_wyvern")}, "task", False, 100),
    ("paradise/fast_flight", "opusvsexe:chronicles/paradise/wyvern", "fast_flight", "fast_flight", "opusvsexe:opus_ruins_compass", {"activated": impossible()}, "task", True, 100),
    ("paradise/regalia", "opusvsexe:chronicles/paradise/wyvern", "paradise_regalia", "paradise_regalia", "opusvsexe:parthenon_chestplate", {"forged": inventory("opusvsexe:parthenon_chestplate")}, "goal", True, 250),
    ("fire/veins", "opusvsexe:chronicles/fire/root", "fire_veins", "fire_veins", "opusvsexe:fire_essence", {"essence": inventory("opusvsexe:fire_essence")}, "task", True, 100),
    ("fire/diablo", "opusvsexe:chronicles/fire/veins", "fire_diablo", "fire_diablo", "opusvsexe:trophy_diablo", {"defeated": kill("fire_demon")}, "challenge", True, 300),
    ("dark_forest/guardian", "opusvsexe:chronicles/dark_forest/root", "dark_forest_guardian", "dark_forest_guardian", "opusvsexe:trophy_mossbound_enderman", {"defeated": kill("mossbound_enderman")}, "challenge", True, 300),
    ("dark_forest/rituals", "opusvsexe:chronicles/dark_forest/guardian", "rituals", "rituals", "opusvsexe:moonflower_heart", {}, "goal", True, 500),
    ("dark_forest/vestments", "opusvsexe:chronicles/dark_forest/rituals", "forest_vestments", "forest_vestments", "opusvsexe:moonflower_heart", {"restored": impossible()}, "goal", True, 250),
    ("settlements/survivors", "opusvsexe:chronicles/settlements/root", "settlements_survivors", "settlements_survivors", "opusvsexe:survivor_spawn_egg", {"found": structure("survivor_settlement")}, "task", True, 75),
    ("settlements/japanese", "opusvsexe:chronicles/settlements/survivors", "settlements_japanese", "settlements_japanese", "opusvsexe:katana", {"found": structure("japanese_settlement")}, "task", True, 100),
    ("settlements/warriors", "opusvsexe:chronicles/settlements/japanese", "settlements_warriors", "settlements_warriors", "opusvsexe:trophy_young_samurai", {"defeated": kill("young_samurai")}, "challenge", True, 300),
    ("expeditions/routes", "opusvsexe:chronicles/expeditions/root", "expedition_routes", "expedition_routes", "opusvsexe:opus_ruins_compass", {}, "goal", True, 500),
    ("expeditions/landmarks", "opusvsexe:chronicles/expeditions/routes", "expedition_landmarks", "expedition_landmarks", "opusvsexe:core_opus", {}, "goal", True, 750),
    ("expeditions/worlds", "opusvsexe:chronicles/expeditions/routes", "expedition_worlds", "expedition_worlds", "opusvsexe:core_opus", {}, "goal", True, 300),
]

for path, parent, title, description, icon, criteria, frame, toast, xp in nodes:
    if title == "signal":
        criteria = {
            "ore_signal": inventory("opusvsexe:opus_ore"),
            "memory_signal": inventory("opusvsexe:memory_fragment_1"),
            "assembly_signal": inventory("opusvsexe:opus_assembly_table"),
        }
        requirements = [["ore_signal", "memory_signal", "assembly_signal"]]
    elif title == "recipes":
        criteria = recipe_criteria
        requirements = all_required(criteria)
    elif title == "archive":
        criteria = fragment_criteria
        requirements = all_required(criteria)
    elif title == "structures":
        criteria = structure_criteria
        requirements = all_required(criteria)
    elif title == "biomes":
        criteria = biome_criteria
        requirements = all_required(criteria)
    elif title == "combat":
        criteria = kill_criteria
        requirements = all_required(criteria)
    elif title == "trophies":
        criteria = {entity_id: inventory(f"opusvsexe:trophy_{trophy_item(entity_id)}") for entity_id in trophy_entities}
        requirements = all_required(criteria)
    elif title == "expeditions":
        criteria = {compass_id: inventory(f"opusvsexe:{compass_id}") for compass_id in compass_ids}
        requirements = all_required(criteria)
    elif title == "exo_models":
        criteria = {**exo_cores, "assembled": impossible()}
        requirements = all_required(criteria)
    elif title == "rituals":
        criteria = {
            "haiku_omega": impossible(),
            "reopen_heavens": impossible(),
            "last_bloom": impossible(),
        }
        requirements = all_required(criteria)
    elif title == "expedition_routes":
        criteria = {compass_id: inventory(f"opusvsexe:{compass_id}") for compass_id in compass_ids}
        requirements = all_required(criteria)
    elif title == "expedition_landmarks":
        criteria = structure_criteria
        requirements = all_required(criteria)
    elif title == "expedition_worlds":
        criteria = biome_criteria
        requirements = all_required(criteria)
    else:
        requirements = None
    write(ADV / f"{path}.json", advancement(parent, title, description, icon, criteria,
                                               frame, toast, requirements, xp))

# Keep the two historical IDs used by the built-in QA hooks and old worlds.
# They are hidden compatibility records; the visible progress is the single
# consolidated Rituals milestone above.
for legacy_id, criterion, icon in (
    ("reopen_heavens", "resurrected", "opusvsexe:ruby_halo_shard"),
    ("return_last_bloom", "resurrected", "opusvsexe:moonflower_heart"),
):
    legacy = advancement("chronicles/dark_forest/root", legacy_id, legacy_id, icon,
                         {criterion: impossible()}, "challenge", False, xp=0)
    legacy["display"]["hidden"] = True
    write(ADV / f"{legacy_id}.json", legacy)


names_ru = {
    "root": ("Хроника Опуса", "Откройте параллельную линию мода и пройдите её спокойно, шаг за шагом."),
    "paradise_root": ("Райский остров", "Найдите воздушный остров и откройте небесную ветвь мода."),
    "fire_root": ("Огненное измерение", "Перейдите через портал в живую кальдеру Четырёх жил."),
    "dark_forest_root": ("Тёмный лес", "Войдите в лес вечной луны и найдите его источник."),
    "settlements_root": ("Поселения", "Найдите выживших и познакомьтесь с двумя линиями поселений."),
    "expeditions_root": ("Экспедиции", "Возьмите первый компас и начните картографировать мир мода."),
    "signal": ("Первый сигнал", "Найдите руду Опуса и войдите в новую линию мира."),
    "assembly": ("Станция сборки", "Получите главный производственный узел — стол сборки 5×5."),
    "recipes": ("Производственная матрица", "Соберите все предметы и блоки мода на столах сборки."),
    "archive": ("Память восстановлена", "Соберите все 15 фрагментов и восстановите историю Опуса."),
    "resonance": ("Резонансный цех", "Откройте кузницу и продвинутые материалы мода."),
    "exo_frame": ("Каркас EXO", "Подготовьте раму, в которой пробуждаются модели EXO."),
    "exo_models": ("Коллекция EXO", "Создайте все пять ядер и соберите модель через раму EXO."),
    "expeditions": ("Карта экспедиций", "Настройте и используйте каждый компас маршрутов."),
    "structures": ("Карта мира", "Посетите все отмеченные структуры мода."),
    "biomes": ("Грани реальности", "Посетите Тёмный лес и Огненное измерение."),
    "fast_flight": ("Небо разрывается", "Сидя на виверне, активируйте режим Быстрого полёта."),
    "rituals": ("Ритуалы памяти", "Проведите три главных ритуала: пробуждение, возвращение небес и последний цветок."),
    "combat": ("Архив угроз", "Победите всех уникальных существ и противников мода."),
    "trophies": ("Зал трофеев", "Соберите трофей каждого побеждённого существа."),
    "mastery": ("Полная синхронизация", "Закройте хронику Опуса и завершите параллельную линию."),
    "paradise_route": ("Воздушная экосистема", "Исследуйте остров и добудьте его первый ресурс."),
    "paradise_wyvern": ("Оседлать ветер", "Приручите виверну райским фруктом."),
    "paradise_regalia": ("Регалия Парфенона", "Создайте полный небесный комплект."),
    "fire_veins": ("Четыре жилы", "Добудьте эссенцию живой кальдеры."),
    "fire_diablo": ("Сердце кальдеры", "Победите Диабло и сломайте его ледяную печать."),
    "dark_forest_guardian": ("Хранитель мха", "Победите Мохового эндермена."),
    "forest_vestments": ("Последний цветок", "Завершите восстановление источника Тёмного леса."),
    "settlements_survivors": ("След выживших", "Найдите поселение и поговорите с его жителями."),
    "settlements_japanese": ("Красный мост", "Войдите в Японское поселение."),
    "settlements_warriors": ("Кровавый цветок", "Победите Молодого самурая."),
    "expedition_routes": ("Сеть маршрутов", "Получите и используйте все 14 компасов экспедиций."),
    "expedition_landmarks": ("Атлас руин", "Посетите все структуры мода."),
    "expedition_worlds": ("Две стороны мира", "Посетите Тёмный лес и Огненное измерение."),
}

names_en = {
    "root": ("The Opus Chronicle", "Open the mod's parallel worldline and follow it one calm step at a time."),
    "paradise_root": ("Paradise Island", "Find the airborne island and open the sky branch of the mod."),
    "fire_root": ("The Fire Realm", "Pass through the portal into the living caldera of the Four Veins."),
    "dark_forest_root": ("The Dark Forest", "Enter the eternal moonlight and find its source."),
    "settlements_root": ("Settlements", "Find the survivors and meet both settlement lines."),
    "expeditions_root": ("Expeditions", "Take the first compass and begin mapping the mod's world."),
    "signal": ("The First Signal", "Find Opus ore and enter the new worldline."),
    "assembly": ("Assembly Station", "Obtain the 5x5 Assembly Table, the mod's production hub."),
    "recipes": ("Production Matrix", "Assemble every mod item and block at the assembly stations."),
    "archive": ("Memory Restored", "Collect all 15 fragments and restore the Opus story."),
    "resonance": ("Resonance Workshop", "Unlock the forge and the mod's advanced materials."),
    "exo_frame": ("EXO Frame", "Prepare the frame where EXO models awaken."),
    "exo_models": ("EXO Collection", "Create all five cores and assemble a model through the EXO frame."),
    "expeditions": ("Expedition Map", "Calibrate and use every route compass."),
    "structures": ("World Map", "Visit every marked structure in the mod."),
    "biomes": ("Edges of Reality", "Visit the Dark Forest and the Fire Realm."),
    "fast_flight": ("The Sky Tears Open", "Activate Fast Flight while riding a wyvern."),
    "rituals": ("Memory Rituals", "Complete the three major rituals: awakening, returning the heavens, and the last bloom."),
    "combat": ("Threat Archive", "Defeat every unique creature and enemy in the mod."),
    "trophies": ("Trophy Hall", "Collect the trophy of every creature you defeat."),
    "mastery": ("Full Synchronization", "Complete the Opus Chronicle and finish the parallel worldline."),
    "paradise_route": ("Sky Ecosystem", "Explore the island and harvest its first resource."),
    "paradise_wyvern": ("Ride the Wind", "Tame a wyvern with Paradise Fruit."),
    "paradise_regalia": ("Parthenon Regalia", "Forge the complete sky set."),
    "fire_veins": ("The Four Veins", "Harvest essence from the living caldera."),
    "fire_diablo": ("Caldera Heart", "Defeat Diablo and break its cryoice seal."),
    "dark_forest_guardian": ("Mossbound Guardian", "Defeat the Mossbound Enderman."),
    "forest_vestments": ("The Last Bloom", "Complete the restoration of the Dark Forest source."),
    "settlements_survivors": ("Survivor Trail", "Find the settlement and meet its residents."),
    "settlements_japanese": ("The Vermilion Bridge", "Enter the Japanese Settlement."),
    "settlements_warriors": ("Bloodflower", "Defeat the Young Samurai."),
    "expedition_routes": ("Route Network", "Obtain and use all 14 expedition compasses."),
    "expedition_landmarks": ("Ruin Atlas", "Visit every structure in the mod."),
    "expedition_worlds": ("Two Sides of the World", "Visit the Dark Forest and the Fire Realm."),
}


def add_lang(path, names):
    data = json.loads(path.read_text(encoding="utf-8"))
    for key, (title, description) in names.items():
        data[f"advancement.opusvsexe.chronicles.{key}.title"] = title
        data[f"advancement.opusvsexe.chronicles.{key}.description"] = description
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


add_lang(LANG_DIR / "ru_ru.json", names_ru)
add_lang(LANG_DIR / "en_us.json", names_en)
