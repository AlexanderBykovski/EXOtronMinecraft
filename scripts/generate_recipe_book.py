#!/usr/bin/env python3
"""Generate aligned, multilingual recipe books from the shipped JSON resources.

No dependencies. Never rewrites game recipes. Use --check in validation jobs.
"""

from __future__ import annotations

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import string

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
TYPES = ["minecraft:crafting_shaped", "minecraft:crafting_shapeless",
         "opusvsexe:assembly", "opusvsexe:parthenon_forging"]
TEXT = {
    "en": {
        "title": "Exotron — complete crafting book",
        "intro": "All 153 JSON recipes shipped in this source snapshot, plus the three Java-defined Resonance Forge conversions. Vanilla Minecraft recipes are outside this book.",
        "grid": "Each letter means one item in that slot; blank slots stay empty. Identical letters mean identical ingredients. Names and resource IDs are listed below each grid. Compact shaped patterns are shown at the top left of the full station grid. Shapeless layouts are examples: ingredient order and position do not matter.",
        "groups": ["Crafting table · shaped · 3×3", "Crafting table · shapeless · 3×3", "Opus Assembly Table · 5×5", "Parthenon Forge · 3×3"],
        "source": "Source", "result": "Result", "legend": "Ingredients", "total": "per craft", "free": "Shapeless recipe — the positions shown are only an example.",
        "catalyst": "Ruby Halo Shard is returned after crafting; it is not consumed.",
        "legacy": "Legacy item: this recipe remains in the supplied source, although this weapon was excluded from the current presentation build. Check that your installed JAR matches this source snapshot.",
        "forge": "Resonance Forge · conversions", "forge_text": "Right-click with flint and steel to switch the forge on. Insert one valid ingredient with right-click; wait 160 ticks (8 seconds at 20 TPS). Collect the output with an empty hand before the next conversion. Each conversion consumes one input and yields one output. Flint and steel switches the forge state; it is not a recipe ingredient.",
        "exo": "EXO assembly", "exo_text": "After crafting an EXO Assembly Frame and an activation core, right-click the frame with the matching core. Assembly takes 60 ticks (3 seconds at 20 TPS), checks space and occupancy, and spawns that EXO. The core is consumed in Survival. This is a block interaction, not an extra crafting-grid recipe.",
        "regen": "Regeneration", "regen_text": "Generated from resource JSON and the Resonance Forge implementation. Do not edit generated grids by hand.",
        "search": "Search recipes or ingredients…", "all": "All stations", "empty": "Empty slot", "any": "any item in tag", "or": "or", "count": "recipes", "print": "Print / save PDF", "view": "Illustrated browser version", "times": "Time", "seconds": "8 seconds at 20 TPS",
    },
    "uk": {
        "title": "Exotron — усі рецепти крафту",
        "intro": "Усі 153 JSON-рецепти з цієї копії вихідного коду та три перетворення Resonance Forge, реалізовані в Java. Звичайні рецепти Minecraft до цього каталогу не входять.",
        "grid": "Літера — один предмет у комірці; порожню комірку треба залишити вільною. Однакові літери означають однакові інгредієнти. Назви та ідентифікатори наведено під схемою. Компактні фігурні рецепти показано в лівому верхньому куті повної сітки станції. Для безформного крафту розкладка умовна: порядок і місце інгредієнтів не важливі.",
        "groups": ["Верстак · фігурний крафт · 3×3", "Верстак · безформний крафт · 3×3", "Opus Assembly Table · 5×5", "Parthenon Forge · 3×3"],
        "source": "Джерело", "result": "Результат", "legend": "Інгредієнти", "total": "на один крафт", "free": "Безформний рецепт — розташування на схемі умовне.",
        "catalyst": "Ruby Halo Shard повертається після крафту й не витрачається.",
        "legacy": "Застарілий предмет: рецепт залишився у наданих вихідниках, хоча цю зброю прибрано з поточної презентаційної збірки. Перевірте відповідність установленого JAR цій копії коду.",
        "forge": "Resonance Forge · перетворення", "forge_text": "Увімкніть кузницю кресалом через ПКМ. Покладіть один придатний інгредієнт через ПКМ та зачекайте 160 тактів (8 секунд за 20 TPS). Заберіть результат порожньою рукою перед наступним перетворенням. Кожне перетворення витрачає один вхідний предмет і дає один вихідний. Кресало перемикає стан кузниці та не входить до рецепта.",
        "exo": "Складання EXO", "exo_text": "Скрафтіть EXO Assembly Frame та ядро активації, потім натисніть ПКМ по рамі відповідним ядром. Складання триває 60 тактів (3 секунди за 20 TPS), перевіряє місце та зайнятість і створює відповідний EXO. У виживанні ядро витрачається. Це взаємодія з блоком, а не додатковий рецепт у сітці.",
        "regen": "Оновлення каталогу", "regen_text": "Схеми створено з JSON ресурсів і реалізації Resonance Forge. Не редагуйте згенеровані сітки вручну.",
        "search": "Пошук рецепта або інгредієнта…", "all": "Усі станції", "empty": "Порожня комірка", "any": "будь-який предмет із теґа", "or": "або", "count": "рецептів", "print": "Друк / зберегти PDF", "view": "Ілюстрована версія для браузера", "times": "Час", "seconds": "8 секунд за 20 TPS",
    },
    "ru": {
        "title": "Exotron — все рецепты крафта",
        "intro": "Все 153 JSON-рецепта из этой копии исходного кода и три превращения Resonance Forge, реализованные в Java. Обычные рецепты Minecraft в этот каталог не входят.",
        "grid": "Буква — один предмет в ячейке; пустую ячейку нужно оставить свободной. Одинаковые буквы означают одинаковые ингредиенты. Названия и идентификаторы приведены под схемой. Компактные фигурные рецепты показаны в левом верхнем углу полной сетки станции. Для бесформенного крафта раскладка условная: порядок и положение ингредиентов не важны.",
        "groups": ["Верстак · фигурный крафт · 3×3", "Верстак · бесформенный крафт · 3×3", "Opus Assembly Table · 5×5", "Parthenon Forge · 3×3"],
        "source": "Источник", "result": "Результат", "legend": "Ингредиенты", "total": "на один крафт", "free": "Бесформенный рецепт — расположение на схеме условное.",
        "catalyst": "Ruby Halo Shard возвращается после крафта и не расходуется.",
        "legacy": "Устаревший предмет: рецепт остался в предоставленных исходниках, хотя это оружие убрано из текущей презентационной сборки. Проверьте соответствие установленного JAR этой копии кода.",
        "forge": "Resonance Forge · превращения", "forge_text": "Включите кузницу огнивом через ПКМ. Положите один подходящий ингредиент через ПКМ и подождите 160 тактов (8 секунд при 20 TPS). Заберите результат пустой рукой перед следующим превращением. Каждое превращение расходует один входной предмет и даёт один выходной. Огниво переключает состояние кузницы и не входит в рецепт.",
        "exo": "Сборка EXO", "exo_text": "Скрафтите EXO Assembly Frame и ядро активации, затем нажмите ПКМ по раме подходящим ядром. Сборка занимает 60 тактов (3 секунды при 20 TPS), проверяет место и занятость и создаёт соответствующий EXO. В выживании ядро расходуется. Это взаимодействие с блоком, а не дополнительный рецепт в сетке.",
        "regen": "Обновление каталога", "regen_text": "Схемы созданы из JSON ресурсов и реализации Resonance Forge. Не редактируйте сгенерированные сетки вручную.",
        "search": "Поиск рецепта или ингредиента…", "all": "Все станции", "empty": "Пустая ячейка", "any": "любой предмет из тега", "or": "или", "count": "рецептов", "print": "Печать / сохранить PDF", "view": "Иллюстрированная версия для браузера", "times": "Время", "seconds": "8 секунд при 20 TPS",
    },
}
LANG = {code: json.loads((RES / f"assets/opusvsexe/lang/{locale}.json").read_text())
        for code, locale in [("en", "en_us"), ("uk", "uk_ua"), ("ru", "ru_ru")]}

# Documentation labels for vanilla ingredients; resource IDs remain authoritative.
VANILLA = {
    "amethyst_shard": ("Аметистовий уламок", "Осколок аметиста"),
    "beacon": ("Маяк", "Маяк"),
    "black_dye": ("Чорний барвник", "Чёрный краситель"),
    "blackstone": ("Чорнокамінь", "Чернит"),
    "blast_furnace": ("Плавильна піч", "Плавильная печь"),
    "blaze_rod": ("Стрижень пломеня", "Огненный стержень"),
    "blue_dye": ("Синій барвник", "Синий краситель"),
    "chest": ("Скриня", "Сундук"),
    "coal": ("Вугілля", "Уголь"),
    "compass": ("Компас", "Компас"),
    "copper_ingot": ("Мідний злиток", "Медный слиток"),
    "crafting_table": ("Верстак", "Верстак"),
    "diamond": ("Діамант", "Алмаз"),
    "diamond_axe": ("Діамантова сокира", "Алмазный топор"),
    "diamond_hoe": ("Діамантова мотика", "Алмазная мотыга"),
    "diamond_pickaxe": ("Діамантове кайло", "Алмазная кирка"),
    "diamond_shovel": ("Діамантова лопата", "Алмазная лопата"),
    "diamond_sword": ("Діамантовий меч", "Алмазный меч"),
    "ender_eye": ("Око Енду", "Око Эндера"),
    "ender_pearl": ("Перлина Енду", "Эндер-жемчуг"),
    "glass": ("Скло", "Стекло"),
    "gold_block": ("Золотий блок", "Золотой блок"),
    "gold_ingot": ("Золотий злиток", "Золотой слиток"),
    "gold_nugget": ("Золотий самородок", "Кусочек золота"),
    "gray_concrete": ("Сірий бетон", "Серый бетон"),
    "ink_sac": ("Чорнильний мішок", "Чернильный мешок"),
    "iron_bars": ("Залізні ґрати", "Железная решётка"),
    "iron_block": ("Залізний блок", "Железный блок"),
    "iron_ingot": ("Залізний злиток", "Железный слиток"),
    "iron_nugget": ("Залізний самородок", "Кусочек железа"),
    "iron_trapdoor": ("Залізний люк", "Железный люк"),
    "leather": ("Шкіра", "Кожа"),
    "magma_block": ("Магмовий блок", "Магмовый блок"),
    "nether_brick": ("Незерська цеглина", "Незерский кирпич"),
    "nether_star": ("Зірка Незеру", "Звезда Незера"),
    "netherite_ingot": ("Незеритовий злиток", "Незеритовый слиток"),
    "oak_planks": ("Дубові дошки", "Дубовые доски"),
    "obsidian": ("Обсидіан", "Обсидиан"),
    "paper": ("Папір", "Бумага"),
    "polished_deepslate": ("Полірований глибинний сланець", "Полированный глубинный сланец"),
    "quartz": ("Незер-кварц", "Незер-кварц"),
    "red_dye": ("Червоний барвник", "Красный краситель"),
    "redstone": ("Редстоуновий пил", "Редстоуновая пыль"),
    "redstone_block": ("Редстоуновий блок", "Редстоуновый блок"),
    "redstone_torch": ("Редстоуновий смолоскип", "Редстоуновый факел"),
    "shield": ("Щит", "Щит"),
    "slime_ball": ("Слиз", "Сгусток слизи"),
    "stick": ("Палиця", "Палка"),
    "stone": ("Камінь", "Камень"),
    "water_bucket": ("Відро води", "Ведро воды"),
}


def title(identifier, language):
    namespace, path = identifier.split(":", 1)
    if namespace == "minecraft" and path in VANILLA and language in ("uk", "ru"):
        return VANILLA[path][0 if language == "uk" else 1]
    lang = LANG[language]
    return lang.get(f"item.{namespace}.{path}", lang.get(f"block.{namespace}.{path}",
                    path.replace("_", " ").replace("/", " / ").title()))


def ingredient(value, language):
    if isinstance(value, list):
        return f" {TEXT[language]['or']} ".join(ingredient(v, language) for v in value)
    if "item" in value:
        return f"{title(value['item'], language)} (`{value['item']}`)"
    return f"{TEXT[language]['any']} `#{value['tag']}`"


def layout(recipe):
    size = 5 if recipe["type"] == "opusvsexe:assembly" else 3
    grid = [[" "] * size for _ in range(size)]
    if "pattern" in recipe:
        assert 0 < len(recipe["pattern"]) <= size
        assert len({len(row) for row in recipe["pattern"]}) == 1
        assert 0 < len(recipe["pattern"][0]) <= size
        raw = recipe["key"]
        symbols = list(dict.fromkeys(c for row in recipe["pattern"] for c in row if c != " "))
        mapping = {c: string.ascii_uppercase[i] for i, c in enumerate(symbols)}
        key = {mapping[c]: raw[c] for c in symbols}
        for y, row in enumerate(recipe["pattern"]):
            for x, c in enumerate(row):
                grid[y][x] = mapping.get(c, " ")
    else:
        assert 0 < len(recipe["ingredients"]) <= size * size
        key, seen = {}, {}
        for i, value in enumerate(recipe["ingredients"]):
            canonical = json.dumps(value, sort_keys=True)
            if canonical not in seen:
                symbol = string.ascii_uppercase[len(seen)]
                seen[canonical] = symbol
                key[symbol] = value
            grid[i // size][i % size] = seen[canonical]
    counts = Counter(c for row in grid for c in row if c != " ")
    return grid, key, counts


def ascii_grid(grid):
    border = "+" + "+".join(["-------"] * len(grid)) + "+"
    lines = [border]
    for row in grid:
        lines.extend(["|" + "|".join(" " * 7 for _ in row) + "|",
                      "|" + "|".join(c.center(7) for c in row) + "|",
                      "|" + "|".join(" " * 7 for _ in row) + "|", border])
    assert len({len(line) for line in lines}) == 1, "unaligned recipe grid"
    assert all(line.isascii() for line in lines)
    return "\n".join(lines)


def load_recipes():
    records = []
    for path in sorted((RES / "data").glob("*/recipes/**/*.json")):
        r = json.loads(path.read_text())
        assert r["type"] in TYPES, f"unhandled recipe type: {path}"
        result = r["result"]
        result_id = result if isinstance(result, str) else result["item"]
        count = 1 if isinstance(result, str) else result.get("count", 1)
        grid, key, counts = layout(r)
        records.append(dict(id=path.stem, source=path.relative_to(ROOT).as_posix(),
                            recipe=r, result=result_id, count=count, grid=grid, key=key, counts=counts,
                            names={lang: title(result_id, lang) for lang in TEXT}))
    return sorted(records, key=lambda r: (TYPES.index(r["recipe"]["type"]), r["id"]))


def conversions():
    path = ROOT / "src/main/java/com/opus/blockentity/ResonanceForgeBlockEntity.java"
    code = path.read_text()
    pairs = re.findall(r"if \(stack\.is\(ModItems\.(\w+)\)\) return new ItemStack\(ModItems\.(\w+)\);", code)
    assert len(pairs) == 3, "Resonance Forge changed: update generator"
    time = int(re.search(r"CRAFT_TIME = (\d+)", code).group(1))
    assert time == 160, "Resonance Forge timing changed: update translations"
    return [("opusvsexe:" + a.lower(), "opusvsexe:" + b.lower()) for a, b in pairs]


def write_markdown(records, pairs, language):
    t = TEXT[language]
    root = language == "uk"
    prefix = "" if root else "../"
    paths = {"en": "docs/CRAFTING.en.md", "uk": "CRAFTING.md", "ru": "docs/CRAFTING.ru.md"}
    nav = " · ".join(f"[{label}]({prefix}{paths[code]})" for code, label in [("en", "English"), ("uk", "Українська"), ("ru", "Русский")])
    out = [f"# {t['title']}", nav, t["intro"], t["grid"],
           f"[{t['view']}]({prefix}docs/recipes.html)"]
    for index, kind in enumerate(TYPES):
        group = [r for r in records if r["recipe"]["type"] == kind]
        out.append(f"## {t['groups'][index]} — {len(group)}")
        for record in group:
            r, grid, key, counts = (record[k] for k in ("recipe", "grid", "key", "counts"))
            out += [f"<a id=\"recipe-{record['id']}\"></a>\n\n### {record['names'][language]}",
                    f"**{t['result']}:** {record['names'][language]} ×{record['count']} · `{record['result']}`"]
            if record["id"] == "laser_gun": out.append("> " + t["legacy"])
            if "pattern" not in r: out.append(t["free"])
            out.append("```text\n" + ascii_grid(grid) + "\n```")
            out.append(f"**{t['legend']} ({t['total']}):**\n\n" + "\n".join(
                f"- **{symbol}** — {ingredient(value, language)} ×{counts[symbol]}"
                for symbol, value in key.items()))
            if "opusvsexe:ruby_halo_shard" in json.dumps(key) and kind == TYPES[3]:
                out.append(t["catalyst"])
            out.append(f"[{t['source']}: `{record['id']}.json`]({prefix}{record['source']})")
    out += [f"## {t['forge']}", t["forge_text"],
            f"| 1 × input | 1 × output | {t['times']} |\n| :--- | :--- | :--- |\n" + "\n".join(
                f"| {title(a, language)} (`{a}`) | {title(b, language)} (`{b}`) | {t['seconds']} |" for a, b in pairs),
            f"[{t['source']}]({prefix}src/main/java/com/opus/blockentity/ResonanceForgeBlockEntity.java)",
            f"## {t['exo']}", t["exo_text"], f"## {t['regen']}", t["regen_text"],
            "```sh\npython3 scripts/generate_recipe_book.py\npython3 scripts/generate_recipe_book.py --check\n```"]
    return "\n\n".join(out) + "\n"


def write_html(records, pairs):
    # Embedding the data keeps the book usable through file:// without a server.
    data = []
    for record in records:
        item = {k: record[k] for k in ["id", "source", "result", "count", "grid", "counts", "names"]}
        item["group"] = TYPES.index(record["recipe"]["type"])
        item["ingredients"] = {s: {lang: ingredient(v, lang) for lang in TEXT} for s, v in record["key"].items()}
        item["icons"] = {}
        for symbol, value in record["key"].items():
            value = value[0] if isinstance(value, list) else value
            identifier = value.get("item", "")
            if identifier.startswith("opusvsexe:"):
                icon = "assets/items/" + identifier.split(":")[1] + ".png"
                if (ROOT / "docs" / icon).is_file(): item["icons"][symbol] = icon
        data.append(item)
    payload = json.dumps(dict(recipes=data, text=TEXT,
                              conversions={lang: [(title(a, lang), title(b, lang)) for a, b in pairs] for lang in TEXT}), ensure_ascii=False).replace("</", "<\\/")
    return HTML.replace("__PAYLOAD__", payload)


HTML = '''<!doctype html>
<html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Exotron — Crafting / Крафти / Крафты</title>
<style>
:root{color-scheme:light;--ink:#102743;--blue:#0067b8;--muted:#57687a;--line:#d8e2ed}
*{box-sizing:border-box}body{margin:0;background:#f3f6fa;color:var(--ink);font:16px/1.55 system-ui,sans-serif}
header{background:var(--ink);color:white;padding:40px max(24px,calc((100vw - 1240px)/2))}h1{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:12px 0 20px}header a{color:#b9ddff}header p{max-width:1000px}
main{max-width:1290px;margin:auto;padding:24px}.tools{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#f3f6faf5;padding:16px 0;z-index:2}
input,select,button{font:inherit;border:1px solid #aabccd;border-radius:6px;padding:10px;background:white;color:var(--ink)}input{flex:1;min-width:220px}button{cursor:pointer}
#cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:20px}.card{background:white;border:1px solid var(--line);border-radius:10px;padding:24px;break-inside:avoid;min-width:0}
.card h2{font-size:23px;line-height:1.25;margin:8px 0 16px}.station{font-size:13px;color:var(--blue);font-weight:700}.result{font-size:14px}.grid{display:grid;grid-template-columns:repeat(var(--n),64px);grid-auto-rows:64px;width:max-content;border:3px solid #586575;margin:22px 0;background:#cad1da}
.slot{border:2px solid;border-color:#eef1f5 #8996a5 #8996a5 #eef1f5;background:#dce2e9;display:flex;align-items:center;justify-content:center;position:relative;font:700 25px ui-monospace,monospace}.slot img{width:42px;height:42px;object-fit:contain;image-rendering:pixelated}.symbol{position:absolute;right:3px;bottom:0;background:#102743e8;color:white;padding:0 3px;font:11px/15px ui-monospace,monospace}
ul{padding-left:20px;font-size:14px}li{margin:7px 0;overflow-wrap:anywhere}code{font-size:12px;overflow-wrap:anywhere}.note{font-size:13px;border-left:3px solid #d39619;padding-left:10px;color:#66470a}a{color:var(--blue)}.source{font-size:12px}#summary{color:var(--muted)}.extra{background:white;border:1px solid var(--line);padding:24px;margin-top:24px;border-radius:10px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid var(--line);text-align:left}
@media(max-width:420px){main{padding:12px}.card{padding:14px}.grid{grid-template-columns:repeat(var(--n),52px);grid-auto-rows:52px}}
@media print{header{background:white;color:var(--ink);padding:0}header a{color:var(--ink)}main{padding:0}.tools,#summary{display:none}#cards{display:block}.card{margin:12px 0;box-shadow:none}.extra{break-inside:avoid}.grid,.slot{print-color-adjust:exact;-webkit-print-color-adjust:exact}a{color:inherit;text-decoration:none}}
</style></head><body>
<header><div>EXOTRON / OPUS VS EXE</div><nav><a href="../README.md">README</a> · <a href="../CRAFTING.md">Markdown · UA</a> · <a href="CRAFTING.en.md">EN</a> · <a href="CRAFTING.ru.md">RU</a></nav><h1 id="title"></h1><p id="intro"></p><p id="help"></p></header>
<main><div class="tools"><input id="search" type="search" aria-label="Search recipes"><select id="station" aria-label="Station"></select><select id="language" aria-label="Language"><option value="uk">Українська</option><option value="en">English</option><option value="ru">Русский</option></select><button id="print" type="button"></button></div><p id="summary" aria-live="polite"></p><div id="cards"></div><section id="extra" class="extra"></section></main>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
const data=JSON.parse(document.querySelector('#data').textContent),byId=id=>document.getElementById(id);let language='uk';
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const format=s=>escape(s).replace(/`([^`]+)`/g,'<code>$1</code>');
function render(){const t=data.text[language],query=byId('search').value.toLocaleLowerCase(),station=byId('station').value;document.documentElement.lang=language;
byId('title').textContent=t.title;byId('intro').textContent=t.intro;byId('help').textContent=t.grid;byId('search').placeholder=t.search;byId('print').textContent=t.print;
const selected=data.recipes.filter(r=>(station===''||Number(station)===r.group)&&JSON.stringify(r).toLocaleLowerCase().includes(query));
byId('cards').innerHTML=selected.map(r=>`<article class="card" id="recipe-${r.id}"><div class="station">${escape(t.groups[r.group])}</div><h2>${escape(r.names[language])}</h2><div class="result">${escape(t.result)}: <strong>${escape(r.names[language])} ×${r.count}</strong><br><code>${escape(r.result)}</code></div>${r.id==='laser_gun'?`<p class="note">${escape(t.legacy)}</p>`:''}${r.group===1?`<p class="note">${escape(t.free)}</p>`:''}<div class="grid" style="--n:${r.grid.length}" role="img" aria-label="${escape(r.names[language])}">${r.grid.flat().map(s=>`<div class="slot" title="${escape(s===' '?t.empty:r.ingredients[s][language].replaceAll('`',''))}">${s===' '?'':r.icons[s]?`<img src="${escape(r.icons[s])}" alt="${escape(s)}"><span class="symbol">${s}</span>`:s}</div>`).join('')}</div><strong>${escape(t.legend)} (${escape(t.total)})</strong><ul>${Object.entries(r.ingredients).map(([s,names])=>`<li><b>${s}</b> — ${format(names[language])} ×${r.counts[s]}</li>`).join('')}</ul>${r.group===3&&JSON.stringify(r.ingredients).includes('opusvsexe:ruby_halo_shard')?`<p class="note">${escape(t.catalyst)}</p>`:''}<a class="source" href="../${r.source}">${escape(t.source)}: ${escape(r.id)}.json</a></article>`).join('');
byId('summary').textContent=`${selected.length} / ${data.recipes.length} ${t.count}`;
byId('extra').innerHTML=`<h2>${escape(t.forge)}</h2><p>${escape(t.forge_text)}</p><table><thead><tr><th>1 × input</th><th>1 × output</th><th>${escape(t.times)}</th></tr></thead><tbody>${data.conversions[language].map(([a,b])=>`<tr><td>${escape(a)}</td><td>${escape(b)}</td><td>${escape(t.seconds)}</td></tr>`).join('')}</tbody></table><h2>${escape(t.exo)}</h2><p>${escape(t.exo_text)}</p><h2>${escape(t.regen)}</h2><p>${escape(t.regen_text)}</p><code>python3 scripts/generate_recipe_book.py</code>`;
}
function stations(){const t=data.text[language],v=byId('station').value;byId('station').innerHTML=`<option value="">${escape(t.all)}</option>`+t.groups.map((s,i)=>`<option value="${i}">${escape(s)}</option>`).join('');byId('station').value=v;}
byId('language').addEventListener('change',e=>{language=e.target.value;stations();render()});byId('search').addEventListener('input',render);byId('station').addEventListener('change',render);byId('print').addEventListener('click',()=>window.print());stations();render();
</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated books are out of date")
    args = parser.parse_args()
    records, pairs = load_recipes(), conversions()
    assert len({r["id"] for r in records}) == len(records)
    assert len(records) == 153, "Recipe count changed: update the introductory text"
    outputs = {ROOT / "CRAFTING.md": write_markdown(records, pairs, "uk"),
               ROOT / "docs/CRAFTING.en.md": write_markdown(records, pairs, "en"),
               ROOT / "docs/CRAFTING.ru.md": write_markdown(records, pairs, "ru"),
               ROOT / "docs/recipes.html": write_html(records, pairs)}
    for path, content in outputs.items():
        if args.check:
            assert path.is_file() and path.read_text() == content, f"Out of date: {path.relative_to(ROOT)}"
        else:
            path.write_text(content, encoding="utf-8")
    counts = Counter(r["recipe"]["type"] for r in records)
    print(f"RECIPE_BOOK_OK recipes={len(records)} conversions={len(pairs)} grids=aligned {dict(counts)}")


if __name__ == "__main__":
    main()
