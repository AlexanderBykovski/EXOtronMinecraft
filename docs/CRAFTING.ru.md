# Exotron — все рецепты крафта

[English](../docs/CRAFTING.en.md) · [Українська](../CRAFTING.md) · [Русский](../docs/CRAFTING.ru.md)

Все 153 JSON-рецепта из этой копии исходного кода и три превращения Resonance Forge, реализованные в Java. Обычные рецепты Minecraft в этот каталог не входят.

Буква — один предмет в ячейке; пустую ячейку нужно оставить свободной. Одинаковые буквы означают одинаковые ингредиенты. Названия и идентификаторы приведены под схемой. Компактные фигурные рецепты показаны в левом верхнем углу полной сетки станции. Для бесформенного крафта раскладка условная: порядок и положение ингредиентов не важны.

[Иллюстрированная версия для браузера](../docs/recipes.html)

## Верстак · фигурный крафт · 3×3 — 61

<a id="recipe-abandoned_city_compass"></a>

### Экспедиционный компас заброшенного города

**Результат:** Экспедиционный компас заброшенного города ×1 · `opusvsexe:abandoned_city_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сломанный корпус ЭКС (`opusvsexe:broken_exo_hull`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `abandoned_city_compass.json`](../src/main/resources/data/opusvsexe/recipes/abandoned_city_compass.json)

<a id="recipe-altar_heart"></a>

### Сердце Алтаря

**Результат:** Сердце Алтаря ×1 · `opusvsexe:altar_heart`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×4
- **B** — Слеза ИИ (`opusvsexe:ai_tear`) ×4
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `altar_heart.json`](../src/main/resources/data/opusvsexe/recipes/altar_heart.json)

<a id="recipe-briarweave"></a>

### Терноткань

**Результат:** Терноткань ×2 · `opusvsexe:briarweave`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Теневая нить (`opusvsexe:shade_silk`) ×4
- **B** — Мембрана лунокрыла (`opusvsexe:moonwing_membrane`) ×2
- **C** — Железный слиток (`minecraft:iron_ingot`) ×2
- **D** — Бревно сумрачного дерева (`opusvsexe:gloomwood_log`) ×1

[Источник: `briarweave.json`](../src/main/resources/data/opusvsexe/recipes/briarweave.json)

<a id="recipe-briarweave_boots"></a>

### Сапоги из терноткани

**Результат:** Сапоги из терноткани ×1 · `opusvsexe:briarweave_boots`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×4

[Источник: `briarweave_boots.json`](../src/main/resources/data/opusvsexe/recipes/briarweave_boots.json)

<a id="recipe-briarweave_chestplate"></a>

### Туника из терноткани

**Результат:** Туника из терноткани ×1 · `opusvsexe:briarweave_chestplate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×8

[Источник: `briarweave_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/briarweave_chestplate.json)

<a id="recipe-briarweave_helmet"></a>

### Капюшон из терноткани

**Результат:** Капюшон из терноткани ×1 · `opusvsexe:briarweave_helmet`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×5

[Источник: `briarweave_helmet.json`](../src/main/resources/data/opusvsexe/recipes/briarweave_helmet.json)

<a id="recipe-briarweave_leggings"></a>

### Поножи из терноткани

**Результат:** Поножи из терноткани ×1 · `opusvsexe:briarweave_leggings`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×7

[Источник: `briarweave_leggings.json`](../src/main/resources/data/opusvsexe/recipes/briarweave_leggings.json)

<a id="recipe-broken_exo_hull"></a>

### Сломанный корпус ЭКС

**Результат:** Сломанный корпус ЭКС ×1 · `opusvsexe:broken_exo_hull`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×8
- **B** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1

[Источник: `broken_exo_hull.json`](../src/main/resources/data/opusvsexe/recipes/broken_exo_hull.json)

<a id="recipe-coddy_workshop_compass"></a>

### Экспедиционный компас мастерской Кодди

**Результат:** Экспедиционный компас мастерской Кодди ×1 · `opusvsexe:coddy_workshop_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Резонансный Опус (`opusvsexe:resonant_opus`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `coddy_workshop_compass.json`](../src/main/resources/data/opusvsexe/recipes/coddy_workshop_compass.json)

<a id="recipe-core_crate"></a>

### Ящик с ядром

**Результат:** Ящик с ядром ×1 · `opusvsexe:core_crate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — любой предмет из тега `#minecraft:planks` ×8
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `core_crate.json`](../src/main/resources/data/opusvsexe/recipes/core_crate.json)

<a id="recipe-core_opus"></a>

### Ядро Опуса

**Результат:** Ядро Опуса ×1 · `opusvsexe:core_opus`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Резонансный Опус (`opusvsexe:resonant_opus`) ×8
- **B** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1

[Источник: `core_opus.json`](../src/main/resources/data/opusvsexe/recipes/core_opus.json)

<a id="recipe-core_opus_block"></a>

### Блок ядра Опуса

**Результат:** Блок ядра Опуса ×1 · `opusvsexe:core_opus_block`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ядро Опуса (`opusvsexe:core_opus`) ×9

[Источник: `core_opus_block.json`](../src/main/resources/data/opusvsexe/recipes/core_opus_block.json)

<a id="recipe-dark_forest_axe"></a>

### Топор Тёмного леса

**Результат:** Топор Тёмного леса ×1 · `opusvsexe:dark_forest_axe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×3
- **B** — Палка (`minecraft:stick`) ×2

[Источник: `dark_forest_axe.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_axe.json)

<a id="recipe-dark_forest_compass"></a>

### Компас Тёмного леса

**Результат:** Компас Тёмного леса ×1 · `opusvsexe:dark_forest_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сердце луноцвета (`opusvsexe:moonflower_heart`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `dark_forest_compass.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_compass.json)

<a id="recipe-dark_forest_hoe"></a>

### Мотыга Тёмного леса

**Результат:** Мотыга Тёмного леса ×1 · `opusvsexe:dark_forest_hoe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×2
- **B** — Палка (`minecraft:stick`) ×2

[Источник: `dark_forest_hoe.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_hoe.json)

<a id="recipe-dark_forest_pickaxe"></a>

### Кирка Тёмного леса

**Результат:** Кирка Тёмного леса ×1 · `opusvsexe:dark_forest_pickaxe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×3
- **B** — Палка (`minecraft:stick`) ×2

[Источник: `dark_forest_pickaxe.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_pickaxe.json)

<a id="recipe-dark_forest_shovel"></a>

### Лопата Тёмного леса

**Результат:** Лопата Тёмного леса ×1 · `opusvsexe:dark_forest_shovel`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×1
- **B** — Палка (`minecraft:stick`) ×2

[Источник: `dark_forest_shovel.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_shovel.json)

<a id="recipe-dark_forest_sword"></a>

### Меч Тёмного леса

**Результат:** Меч Тёмного леса ×1 · `opusvsexe:dark_forest_sword`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терноткань (`opusvsexe:briarweave`) ×2
- **B** — Палка (`minecraft:stick`) ×1

[Источник: `dark_forest_sword.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_sword.json)

<a id="recipe-data_spire_compass"></a>

### Экспедиционный компас шпиля данных

**Результат:** Экспедиционный компас шпиля данных ×1 · `opusvsexe:data_spire_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Слеза ИИ (`opusvsexe:ai_tear`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `data_spire_compass.json`](../src/main/resources/data/opusvsexe/recipes/data_spire_compass.json)

<a id="recipe-demonic_trident"></a>

### Демонический трезубец

**Результат:** Демонический трезубец ×1 · `opusvsexe:demonic_trident`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×3
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×2
- **C** — Незеритовый слиток (`minecraft:netherite_ingot`) ×1

[Источник: `demonic_trident.json`](../src/main/resources/data/opusvsexe/recipes/demonic_trident.json)

<a id="recipe-eternal_colosseum_compass"></a>

### Экспедиционный компас Вечного Колизея

**Результат:** Экспедиционный компас Вечного Колизея ×1 · `opusvsexe:eternal_colosseum_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `eternal_colosseum_compass.json`](../src/main/resources/data/opusvsexe/recipes/eternal_colosseum_compass.json)

<a id="recipe-fire_axe"></a>

### Огненный топор Жил

**Результат:** Огненный топор Жил ×1 · `opusvsexe:fire_axe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×3
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×2

[Источник: `fire_axe.json`](../src/main/resources/data/opusvsexe/recipes/fire_axe.json)

<a id="recipe-fire_boots"></a>

### Ботинки из жильной коры

**Результат:** Ботинки из жильной коры ×1 · `opusvsexe:fire_boots`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Жильная кора (`opusvsexe:magma_crust`) ×4

[Источник: `fire_boots.json`](../src/main/resources/data/opusvsexe/recipes/fire_boots.json)

<a id="recipe-fire_chestplate"></a>

### Кираса из жильной коры

**Результат:** Кираса из жильной коры ×1 · `opusvsexe:fire_chestplate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Жильная кора (`opusvsexe:magma_crust`) ×8

[Источник: `fire_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/fire_chestplate.json)

<a id="recipe-fire_helmet"></a>

### Шлем из жильной коры

**Результат:** Шлем из жильной коры ×1 · `opusvsexe:fire_helmet`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Жильная кора (`opusvsexe:magma_crust`) ×5

[Источник: `fire_helmet.json`](../src/main/resources/data/opusvsexe/recipes/fire_helmet.json)

<a id="recipe-fire_hoe"></a>

### Огненная мотыга Жил

**Результат:** Огненная мотыга Жил ×1 · `opusvsexe:fire_hoe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×2
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×2

[Источник: `fire_hoe.json`](../src/main/resources/data/opusvsexe/recipes/fire_hoe.json)

<a id="recipe-fire_leggings"></a>

### Поножи из жильной коры

**Результат:** Поножи из жильной коры ×1 · `opusvsexe:fire_leggings`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Жильная кора (`opusvsexe:magma_crust`) ×7

[Источник: `fire_leggings.json`](../src/main/resources/data/opusvsexe/recipes/fire_leggings.json)

<a id="recipe-fire_pickaxe"></a>

### Огненная кирка Жил

**Результат:** Огненная кирка Жил ×1 · `opusvsexe:fire_pickaxe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×3
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×2

[Источник: `fire_pickaxe.json`](../src/main/resources/data/opusvsexe/recipes/fire_pickaxe.json)

<a id="recipe-fire_portal"></a>

### Прорыв в пространстве

**Результат:** Прорыв в пространстве ×1 · `opusvsexe:fire_portal`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Обсидиан (`minecraft:obsidian`) ×4
- **B** — Магмовый блок (`minecraft:magma_block`) ×4
- **C** — Огненный стержень (`minecraft:blaze_rod`) ×1

[Источник: `fire_portal.json`](../src/main/resources/data/opusvsexe/recipes/fire_portal.json)

<a id="recipe-fire_shovel"></a>

### Огненная лопата Жил

**Результат:** Огненная лопата Жил ×1 · `opusvsexe:fire_shovel`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×1
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×2

[Источник: `fire_shovel.json`](../src/main/resources/data/opusvsexe/recipes/fire_shovel.json)

<a id="recipe-fire_sword"></a>

### Огненный меч Жил

**Результат:** Огненный меч Жил ×1 · `opusvsexe:fire_sword`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Эссенция Жил (`opusvsexe:fire_essence`) ×2
- **B** — Огненный стержень (`minecraft:blaze_rod`) ×1

[Источник: `fire_sword.json`](../src/main/resources/data/opusvsexe/recipes/fire_sword.json)

<a id="recipe-frontier_fortress_compass"></a>

### Экспедиционный компас пограничной крепости

**Результат:** Экспедиционный компас пограничной крепости ×1 · `opusvsexe:frontier_fortress_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `frontier_fortress_compass.json`](../src/main/resources/data/opusvsexe/recipes/frontier_fortress_compass.json)

<a id="recipe-haiku_citadel_compass"></a>

### Экспедиционный компас цитадели Хайку

**Результат:** Экспедиционный компас цитадели Хайку ×1 · `opusvsexe:haiku_citadel_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ядро Хаику (`opusvsexe:haiku_core`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `haiku_citadel_compass.json`](../src/main/resources/data/opusvsexe/recipes/haiku_citadel_compass.json)

<a id="recipe-haiku_core"></a>

### Ядро Хаику

**Результат:** Ядро Хаику ×1 · `opusvsexe:haiku_core`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×4
- **B** — Слеза ИИ (`opusvsexe:ai_tear`) ×4
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `haiku_core.json`](../src/main/resources/data/opusvsexe/recipes/haiku_core.json)

<a id="recipe-japanese_settlement_compass"></a>

### Экспедиционный компас японского поселения

**Результат:** Экспедиционный компас японского поселения ×1 · `opusvsexe:japanese_settlement_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стальная катана (`opusvsexe:katana`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `japanese_settlement_compass.json`](../src/main/resources/data/opusvsexe/recipes/japanese_settlement_compass.json)

<a id="recipe-katana"></a>

### Стальная катана

**Результат:** Стальная катана ×1 · `opusvsexe:katana`

```text
+-------+-------+-------+
|       |       |       |
|       |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×2
- **B** — Палка (`minecraft:stick`) ×1
- **C** — Кожа (`minecraft:leather`) ×1

[Источник: `katana.json`](../src/main/resources/data/opusvsexe/recipes/katana.json)

<a id="recipe-kimi_laboratory_compass"></a>

### Экспедиционный компас лаборатории Кими

**Результат:** Экспедиционный компас лаборатории Кими ×1 · `opusvsexe:kimi_laboratory_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент памяти #4 (`opusvsexe:memory_fragment_4`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `kimi_laboratory_compass.json`](../src/main/resources/data/opusvsexe/recipes/kimi_laboratory_compass.json)

<a id="recipe-long_katana"></a>

### Длинная катана

**Результат:** Длинная катана ×1 · `opusvsexe:long_katana`

```text
+-------+-------+-------+
|       |       |       |
|       |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Алмаз (`minecraft:diamond`) ×2
- **B** — Стальная катана (`opusvsexe:katana`) ×1

[Источник: `long_katana.json`](../src/main/resources/data/opusvsexe/recipes/long_katana.json)

<a id="recipe-moon_fountain_compass"></a>

### Компас Лунного фонтана

**Результат:** Компас Лунного фонтана ×1 · `opusvsexe:moon_fountain_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `moon_fountain_compass.json`](../src/main/resources/data/opusvsexe/recipes/moon_fountain_compass.json)

<a id="recipe-opus_assembly_table"></a>

### Стол сборки Опуса

**Результат:** Стол сборки Опуса ×1 · `opusvsexe:opus_assembly_table`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   E   |   E   |   E   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Золотой слиток (`minecraft:gold_ingot`) ×2
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Обшивка крепости (`opusvsexe:fortress_plating`) ×2
- **D** — Верстак (`minecraft:crafting_table`) ×1
- **E** — Полированный глубинный сланец (`minecraft:polished_deepslate`) ×3

[Источник: `opus_assembly_table.json`](../src/main/resources/data/opusvsexe/recipes/opus_assembly_table.json)

<a id="recipe-opus_axe"></a>

### Топор из Опуса

**Результат:** Топор из Опуса ×1 · `opusvsexe:opus_axe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×3
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_axe.json`](../src/main/resources/data/opusvsexe/recipes/opus_axe.json)

<a id="recipe-opus_boots"></a>

### Ботинки из Опуса

**Результат:** Ботинки из Опуса ×1 · `opusvsexe:opus_boots`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×2
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_boots.json`](../src/main/resources/data/opusvsexe/recipes/opus_boots.json)

<a id="recipe-opus_chestplate"></a>

### Нагрудник из Опуса

**Результат:** Нагрудник из Опуса ×1 · `opusvsexe:opus_chestplate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×2
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×5
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `opus_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/opus_chestplate.json)

<a id="recipe-opus_helmet"></a>

### Шлем из Опуса

**Результат:** Шлем из Опуса ×1 · `opusvsexe:opus_helmet`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×3
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_helmet.json`](../src/main/resources/data/opusvsexe/recipes/opus_helmet.json)

<a id="recipe-opus_hoe"></a>

### Мотыга из Опуса

**Результат:** Мотыга из Опуса ×1 · `opusvsexe:opus_hoe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×2
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_hoe.json`](../src/main/resources/data/opusvsexe/recipes/opus_hoe.json)

<a id="recipe-opus_leggings"></a>

### Поножи из Опуса

**Результат:** Поножи из Опуса ×1 · `opusvsexe:opus_leggings`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |   B   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×3
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×4

[Источник: `opus_leggings.json`](../src/main/resources/data/opusvsexe/recipes/opus_leggings.json)

<a id="recipe-opus_pickaxe"></a>

### Кирка из Опуса

**Результат:** Кирка из Опуса ×1 · `opusvsexe:opus_pickaxe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×3
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_pickaxe.json`](../src/main/resources/data/opusvsexe/recipes/opus_pickaxe.json)

<a id="recipe-opus_ruins_compass"></a>

### Компас руин Опуса

**Результат:** Компас руин Опуса ×1 · `opusvsexe:opus_ruins_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент памяти #1 (`opusvsexe:memory_fragment_1`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `opus_ruins_compass.json`](../src/main/resources/data/opusvsexe/recipes/opus_ruins_compass.json)

<a id="recipe-opus_shovel"></a>

### Лопата из Опуса

**Результат:** Лопата из Опуса ×1 · `opusvsexe:opus_shovel`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×2

[Источник: `opus_shovel.json`](../src/main/resources/data/opusvsexe/recipes/opus_shovel.json)

<a id="recipe-paradise_compass"></a>

### Компас Острова-Рая

**Результат:** Компас Острова-Рая ×1 · `opusvsexe:paradise_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Райский плод (`opusvsexe:paradise_fruit`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `paradise_compass.json`](../src/main/resources/data/opusvsexe/recipes/paradise_compass.json)

<a id="recipe-parthenon_forge"></a>

### Кузня Парфенона

**Результат:** Кузня Парфенона ×1 · `opusvsexe:parthenon_forge`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Золотой слиток (`minecraft:gold_ingot`) ×4
- **B** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×4
- **C** — Верстак (`minecraft:crafting_table`) ×1

[Источник: `parthenon_forge.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_forge.json)

<a id="recipe-pulsing_core"></a>

### Пульсирующее ядро

**Результат:** Пульсирующее ядро ×1 · `opusvsexe:pulsing_core`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Резонансный Опус (`opusvsexe:resonant_opus`) ×4
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `pulsing_core.json`](../src/main/resources/data/opusvsexe/recipes/pulsing_core.json)

<a id="recipe-raw_opus"></a>

### Необработанный Опус

**Результат:** Необработанный Опус ×4 · `opusvsexe:raw_opus`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Руда Опуса (`opusvsexe:opus_ore`) ×4

[Источник: `raw_opus.json`](../src/main/resources/data/opusvsexe/recipes/raw_opus.json)

<a id="recipe-raw_opus_block"></a>

### Блок необработанного Опуса

**Результат:** Блок необработанного Опуса ×1 · `opusvsexe:raw_opus_block`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Необработанный Опус (`opusvsexe:raw_opus`) ×9

[Источник: `raw_opus_block.json`](../src/main/resources/data/opusvsexe/recipes/raw_opus_block.json)

<a id="recipe-resonant_opus"></a>

### Резонансный Опус

**Результат:** Резонансный Опус ×4 · `opusvsexe:resonant_opus`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×4

[Источник: `resonant_opus.json`](../src/main/resources/data/opusvsexe/recipes/resonant_opus.json)

<a id="recipe-resonant_opus_block"></a>

### Блок резонансного Опуса

**Результат:** Блок резонансного Опуса ×1 · `opusvsexe:resonant_opus_block`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Резонансный Опус (`opusvsexe:resonant_opus`) ×9

[Источник: `resonant_opus_block.json`](../src/main/resources/data/opusvsexe/recipes/resonant_opus_block.json)

<a id="recipe-stabilized_opus"></a>

### Стабилизированный Опус

**Результат:** Стабилизированный Опус ×4 · `opusvsexe:stabilized_opus`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Необработанный Опус (`opusvsexe:raw_opus`) ×4

[Источник: `stabilized_opus.json`](../src/main/resources/data/opusvsexe/recipes/stabilized_opus.json)

<a id="recipe-stabilized_opus_block"></a>

### Блок стабилизированного Опуса

**Результат:** Блок стабилизированного Опуса ×1 · `opusvsexe:stabilized_opus_block`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×9

[Источник: `stabilized_opus_block.json`](../src/main/resources/data/opusvsexe/recipes/stabilized_opus_block.json)

<a id="recipe-survivor_settlement_compass"></a>

### Экспедиционный компас поселения выживших

**Результат:** Экспедиционный компас поселения выживших ×1 · `opusvsexe:survivor_settlement_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент памяти #3 (`opusvsexe:memory_fragment_3`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `survivor_settlement_compass.json`](../src/main/resources/data/opusvsexe/recipes/survivor_settlement_compass.json)

<a id="recipe-trial_grounds_compass"></a>

### Экспедиционный компас испытательных земель

**Результат:** Экспедиционный компас испытательных земель ×1 · `opusvsexe:trial_grounds_expedition_compass`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Фрагмент памяти #2 (`opusvsexe:memory_fragment_2`) ×4
- **B** — Компас (`minecraft:compass`) ×1

[Источник: `trial_grounds_compass.json`](../src/main/resources/data/opusvsexe/recipes/trial_grounds_compass.json)

<a id="recipe-welding_bench"></a>

### Сварочный стол

**Результат:** Сварочный стол ×1 · `opusvsexe:welding_bench`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×6
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×2
- **C** — Пульсирующее ядро (`opusvsexe:pulsing_core`) ×1

[Источник: `welding_bench.json`](../src/main/resources/data/opusvsexe/recipes/welding_bench.json)

## Верстак · бесформенный крафт · 3×3 — 72

<a id="recipe-amber_pillar"></a>

### Янтарная Опора

**Результат:** Янтарная Опора ×2 · `opusvsexe:amber_pillar`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Янтарный блок Хаику (`opusvsexe:haiku_amber_block`) ×1
- **B** — Полированный глубинный сланец (`minecraft:polished_deepslate`) ×1

[Источник: `amber_pillar.json`](../src/main/resources/data/opusvsexe/recipes/amber_pillar.json)

<a id="recipe-arena_gate"></a>

### Ворота арены

**Результат:** Ворота арены ×1 · `opusvsexe:arena_gate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железная решётка (`minecraft:iron_bars`) ×1
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `arena_gate.json`](../src/main/resources/data/opusvsexe/recipes/arena_gate.json)

<a id="recipe-blueprint_table"></a>

### Стол чертежей

**Результат:** Стол чертежей ×1 · `opusvsexe:blueprint_table`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Дубовые доски (`minecraft:oak_planks`) ×1
- **B** — Бумага (`minecraft:paper`) ×1
- **C** — Чернильный мешок (`minecraft:ink_sac`) ×1
- **D** — Стекло памяти (`opusvsexe:memory_glass`) ×1

[Источник: `blueprint_table.json`](../src/main/resources/data/opusvsexe/recipes/blueprint_table.json)

<a id="recipe-broken_resonance_forge"></a>

### Сломанная резонансная кузница

**Результат:** Сломанная резонансная кузница ×1 · `opusvsexe:broken_resonance_forge`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Камень (`minecraft:stone`) ×1
- **B** — Необработанный Опус (`opusvsexe:raw_opus`) ×1
- **C** — Плавильная печь (`minecraft:blast_furnace`) ×1

[Источник: `broken_resonance_forge.json`](../src/main/resources/data/opusvsexe/recipes/broken_resonance_forge.json)

<a id="recipe-citadel_vein"></a>

### Жила цитадели

**Результат:** Жила цитадели ×2 · `opusvsexe:citadel_vein`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Кусочек железа (`minecraft:iron_nugget`) ×1
- **B** — Ядро Хаику (`opusvsexe:haiku_core`) ×1
- **C** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1

[Источник: `citadel_vein.json`](../src/main/resources/data/opusvsexe/recipes/citadel_vein.json)

<a id="recipe-colosseum_concrete"></a>

### Бетон Колизея

**Результат:** Бетон Колизея ×4 · `opusvsexe:colosseum_concrete`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Серый бетон (`minecraft:gray_concrete`) ×1
- **B** — Кусочек железа (`minecraft:iron_nugget`) ×1
- **C** — Ядро Хаику (`opusvsexe:haiku_core`) ×1

[Источник: `colosseum_concrete.json`](../src/main/resources/data/opusvsexe/recipes/colosseum_concrete.json)

<a id="recipe-colosseum_wall"></a>

### Стена Колизея

**Результат:** Стена Колизея ×2 · `opusvsexe:colosseum_wall`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Бетон Колизея (`opusvsexe:colosseum_concrete`) ×1
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×1

[Источник: `colosseum_wall.json`](../src/main/resources/data/opusvsexe/recipes/colosseum_wall.json)

<a id="recipe-combat_beacon"></a>

### Боевой маяк

**Результат:** Боевой маяк ×1 · `opusvsexe:combat_beacon`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Маяк (`minecraft:beacon`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1

[Источник: `combat_beacon.json`](../src/main/resources/data/opusvsexe/recipes/combat_beacon.json)

<a id="recipe-command_terminal"></a>

### Командный терминал

**Результат:** Командный терминал ×1 · `opusvsexe:command_terminal`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Терминал волны (`opusvsexe:wave_terminal`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Слеза ИИ (`opusvsexe:ai_tear`) ×1

[Источник: `command_terminal.json`](../src/main/resources/data/opusvsexe/recipes/command_terminal.json)

<a id="recipe-cracked_lab_concrete"></a>

### Потрескавшийся лабораторный бетон

**Результат:** Потрескавшийся лабораторный бетон ×4 · `opusvsexe:cracked_lab_concrete`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Камень (`minecraft:stone`) ×1
- **B** — Кусочек железа (`minecraft:iron_nugget`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `cracked_lab_concrete.json`](../src/main/resources/data/opusvsexe/recipes/cracked_lab_concrete.json)

<a id="recipe-dark_forest_boots"></a>

### Сапоги Тёмного леса

**Результат:** Сапоги Тёмного леса ×1 · `opusvsexe:dark_forest_boots`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сапоги из терноткани (`opusvsexe:briarweave_boots`) ×1
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1

[Источник: `dark_forest_boots.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_boots.json)

<a id="recipe-dark_forest_chestplate"></a>

### Облачение Тёмного леса

**Результат:** Облачение Тёмного леса ×1 · `opusvsexe:dark_forest_chestplate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Туника из терноткани (`opusvsexe:briarweave_chestplate`) ×1
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1
- **C** — Сердце луноцвета (`opusvsexe:moonflower_heart`) ×1

[Источник: `dark_forest_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_chestplate.json)

<a id="recipe-dark_forest_helmet"></a>

### Корона Тёмного леса

**Результат:** Корона Тёмного леса ×1 · `opusvsexe:dark_forest_helmet`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Капюшон из терноткани (`opusvsexe:briarweave_helmet`) ×1
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1

[Источник: `dark_forest_helmet.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_helmet.json)

<a id="recipe-dark_forest_leggings"></a>

### Поножи Тёмного леса

**Результат:** Поножи Тёмного леса ×1 · `opusvsexe:dark_forest_leggings`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Поножи из терноткани (`opusvsexe:briarweave_leggings`) ×1
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1

[Источник: `dark_forest_leggings.json`](../src/main/resources/data/opusvsexe/recipes/dark_forest_leggings.json)

<a id="recipe-data_conduit"></a>

### Канал передачи данных

**Результат:** Канал передачи данных ×2 · `opusvsexe:data_conduit`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Медный слиток (`minecraft:copper_ingot`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `data_conduit.json`](../src/main/resources/data/opusvsexe/recipes/data_conduit.json)

<a id="recipe-dead_terminal"></a>

### Мёртвый терминал

**Результат:** Мёртвый терминал ×1 · `opusvsexe:dead_terminal`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Канал передачи данных (`opusvsexe:data_conduit`) ×1

[Источник: `dead_terminal.json`](../src/main/resources/data/opusvsexe/recipes/dead_terminal.json)

<a id="recipe-dormant_spawner"></a>

### Спящий спавнер

**Результат:** Спящий спавнер ×1 · `opusvsexe:dormant_spawner`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железная решётка (`minecraft:iron_bars`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×1

[Источник: `dormant_spawner.json`](../src/main/resources/data/opusvsexe/recipes/dormant_spawner.json)

<a id="recipe-energy_barrier"></a>

### Барьер

**Результат:** Барьер ×2 · `opusvsexe:energy_barrier`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железная решётка (`minecraft:iron_bars`) ×1
- **B** — Стекло (`minecraft:glass`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `energy_barrier.json`](../src/main/resources/data/opusvsexe/recipes/energy_barrier.json)

<a id="recipe-energy_barrier_blue"></a>

### Синий барьер

**Результат:** Синий барьер ×2 · `opusvsexe:energy_barrier_blue`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Барьер (`opusvsexe:energy_barrier`) ×1
- **B** — Синий краситель (`minecraft:blue_dye`) ×1

[Источник: `energy_barrier_blue.json`](../src/main/resources/data/opusvsexe/recipes/energy_barrier_blue.json)

<a id="recipe-energy_barrier_red"></a>

### Красный барьер

**Результат:** Красный барьер ×2 · `opusvsexe:energy_barrier_red`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Барьер (`opusvsexe:energy_barrier`) ×1
- **B** — Красный краситель (`minecraft:red_dye`) ×1

[Источник: `energy_barrier_red.json`](../src/main/resources/data/opusvsexe/recipes/energy_barrier_red.json)

<a id="recipe-energy_beam"></a>

### Энергетический стержень

**Результат:** Энергетический стержень ×2 · `opusvsexe:energy_beam`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Барьер (`opusvsexe:energy_barrier`) ×1
- **B** — Осколок аметиста (`minecraft:amethyst_shard`) ×1
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1

[Источник: `energy_beam.json`](../src/main/resources/data/opusvsexe/recipes/energy_beam.json)

<a id="recipe-energy_relay"></a>

### Энергоузел

**Результат:** Энергоузел ×1 · `opusvsexe:energy_relay`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Медный слиток (`minecraft:copper_ingot`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `energy_relay.json`](../src/main/resources/data/opusvsexe/recipes/energy_relay.json)

<a id="recipe-fire_demonic_boots"></a>

### Сапоги огненного демона

**Результат:** Сапоги огненного демона ×1 · `opusvsexe:fire_demonic_boots`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ботинки из жильной коры (`opusvsexe:fire_boots`) ×1
- **B** — Эссенция Жил (`opusvsexe:fire_essence`) ×4

[Источник: `fire_demonic_boots.json`](../src/main/resources/data/opusvsexe/recipes/fire_demonic_boots.json)

<a id="recipe-fire_demonic_chestplate"></a>

### Кираса огненного демона

**Результат:** Кираса огненного демона ×1 · `opusvsexe:fire_demonic_chestplate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Кираса из жильной коры (`opusvsexe:fire_chestplate`) ×1
- **B** — Эссенция Жил (`opusvsexe:fire_essence`) ×4

[Источник: `fire_demonic_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/fire_demonic_chestplate.json)

<a id="recipe-fire_demonic_helmet"></a>

### Рогатый шлем огненного демона

**Результат:** Рогатый шлем огненного демона ×1 · `opusvsexe:fire_demonic_helmet`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Шлем из жильной коры (`opusvsexe:fire_helmet`) ×1
- **B** — Эссенция Жил (`opusvsexe:fire_essence`) ×4

[Источник: `fire_demonic_helmet.json`](../src/main/resources/data/opusvsexe/recipes/fire_demonic_helmet.json)

<a id="recipe-fire_demonic_leggings"></a>

### Поножи огненного демона

**Результат:** Поножи огненного демона ×1 · `opusvsexe:fire_demonic_leggings`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Поножи из жильной коры (`opusvsexe:fire_leggings`) ×1
- **B** — Эссенция Жил (`opusvsexe:fire_essence`) ×4

[Источник: `fire_demonic_leggings.json`](../src/main/resources/data/opusvsexe/recipes/fire_demonic_leggings.json)

<a id="recipe-flickering_terminal"></a>

### Мерцающий терминал

**Результат:** Мерцающий терминал ×1 · `opusvsexe:flickering_terminal`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Мёртвый терминал (`opusvsexe:dead_terminal`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Редстоуновая пыль (`minecraft:redstone`) ×1

[Источник: `flickering_terminal.json`](../src/main/resources/data/opusvsexe/recipes/flickering_terminal.json)

<a id="recipe-force_field_projector"></a>

### Проектор силового поля

**Результат:** Проектор силового поля ×1 · `opusvsexe:force_field_projector`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Энергетический стержень (`opusvsexe:energy_beam`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Железный блок (`minecraft:iron_block`) ×1

[Источник: `force_field_projector.json`](../src/main/resources/data/opusvsexe/recipes/force_field_projector.json)

<a id="recipe-fortress_plating"></a>

### Обшивка крепости

**Результат:** Обшивка крепости ×2 · `opusvsexe:fortress_plating`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный блок (`minecraft:iron_block`) ×1
- **B** — Незерский кирпич (`minecraft:nether_brick`) ×1
- **C** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1

[Источник: `fortress_plating.json`](../src/main/resources/data/opusvsexe/recipes/fortress_plating.json)

<a id="recipe-gravity_anchor"></a>

### Гравитационный якорь

**Результат:** Гравитационный якорь ×1 · `opusvsexe:gravity_anchor`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Обсидиан (`minecraft:obsidian`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1

[Источник: `gravity_anchor.json`](../src/main/resources/data/opusvsexe/recipes/gravity_anchor.json)

<a id="recipe-haiku_amber_block"></a>

### Янтарный блок Хаику

**Результат:** Янтарный блок Хаику ×1 · `opusvsexe:haiku_amber_block`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ядро Хаику (`opusvsexe:haiku_core`) ×1
- **B** — Золотой блок (`minecraft:gold_block`) ×1
- **C** — Слеза ИИ (`opusvsexe:ai_tear`) ×1

[Источник: `haiku_amber_block.json`](../src/main/resources/data/opusvsexe/recipes/haiku_amber_block.json)

<a id="recipe-hazard_emitter"></a>

### Излучатель опасности

**Результат:** Излучатель опасности ×1 · `opusvsexe:hazard_emitter`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Редстоуновый факел (`minecraft:redstone_torch`) ×1
- **B** — Железный слиток (`minecraft:iron_ingot`) ×1
- **C** — Эссенция Жил (`opusvsexe:fire_essence`) ×1

[Источник: `hazard_emitter.json`](../src/main/resources/data/opusvsexe/recipes/hazard_emitter.json)

<a id="recipe-heavy_laser_gun"></a>

### Тяжёлая лазерная пушка

**Результат:** Тяжёлая лазерная пушка ×1 · `opusvsexe:heavy_laser_gun`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Лёгкая лазерная пушка (`opusvsexe:light_laser_gun`) ×1
- **B** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1
- **C** — Железный блок (`minecraft:iron_block`) ×1
- **D** — Редстоуновый блок (`minecraft:redstone_block`) ×1

[Источник: `heavy_laser_gun.json`](../src/main/resources/data/opusvsexe/recipes/heavy_laser_gun.json)

<a id="recipe-katana_gold"></a>

### Золотая катана

**Результат:** Золотая катана ×1 · `opusvsexe:katana_gold`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Необработанный Опус (`opusvsexe:raw_opus`) ×1
- **B** — Золотой слиток (`minecraft:gold_ingot`) ×2
- **C** — Железный слиток (`minecraft:iron_ingot`) ×1

[Источник: `katana_gold.json`](../src/main/resources/data/opusvsexe/recipes/katana_gold.json)

<a id="recipe-katana_op"></a>

### Катана-OP

**Результат:** Катана-OP ×1 · `opusvsexe:katana_op`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **B** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1
- **C** — Железный слиток (`minecraft:iron_ingot`) ×2

[Источник: `katana_op.json`](../src/main/resources/data/opusvsexe/recipes/katana_op.json)

<a id="recipe-katana_refined"></a>

### Очищенная катана Опуса

**Результат:** Очищенная катана Опуса ×1 · `opusvsexe:katana_refined`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Золотая катана (`opusvsexe:katana_gold`) ×1
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `katana_refined.json`](../src/main/resources/data/opusvsexe/recipes/katana_refined.json)

<a id="recipe-katana_stand"></a>

### Стойка для катаны

**Результат:** Стойка для катаны ×1 · `opusvsexe:katana_stand`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Дубовые доски (`minecraft:oak_planks`) ×1
- **B** — Палка (`minecraft:stick`) ×1
- **C** — Кусочек золота (`minecraft:gold_nugget`) ×1

[Источник: `katana_stand.json`](../src/main/resources/data/opusvsexe/recipes/katana_stand.json)

<a id="recipe-lab_floor_grate"></a>

### Лабораторная решётка

**Результат:** Лабораторная решётка ×4 · `opusvsexe:lab_floor_grate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×4
- **B** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `lab_floor_grate.json`](../src/main/resources/data/opusvsexe/recipes/lab_floor_grate.json)

<a id="recipe-laser_gun"></a>

### Лазерная пушка

**Результат:** Лазерная пушка ×1 · `opusvsexe:laser_gun`

> Устаревший предмет: рецепт остался в предоставленных исходниках, хотя это оружие убрано из текущей презентационной сборки. Проверьте соответствие установленного JAR этой копии кода.

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Необработанный Опус (`opusvsexe:raw_opus`) ×1
- **B** — Железный слиток (`minecraft:iron_ingot`) ×2
- **C** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **D** — Незер-кварц (`minecraft:quartz`) ×1

[Источник: `laser_gun.json`](../src/main/resources/data/opusvsexe/recipes/laser_gun.json)

<a id="recipe-light_laser_gun"></a>

### Лёгкая лазерная пушка

**Результат:** Лёгкая лазерная пушка ×1 · `opusvsexe:light_laser_gun`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Лазерная пушка (`opusvsexe:laser_gun`) ×1
- **B** — Необработанный Опус (`opusvsexe:raw_opus`) ×1
- **C** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **D** — Незер-кварц (`minecraft:quartz`) ×1

[Источник: `light_laser_gun.json`](../src/main/resources/data/opusvsexe/recipes/light_laser_gun.json)

<a id="recipe-marsh_filter"></a>

### Болотный фильтр

**Результат:** Болотный фильтр ×1 · `opusvsexe:marsh_filter`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железная решётка (`minecraft:iron_bars`) ×1
- **B** — Ведро воды (`minecraft:water_bucket`) ×1
- **C** — Кабель памяти (`opusvsexe:memory_cable`) ×1

[Источник: `marsh_filter.json`](../src/main/resources/data/opusvsexe/recipes/marsh_filter.json)

<a id="recipe-memory_cable"></a>

### Кабель памяти

**Результат:** Кабель памяти ×4 · `opusvsexe:memory_cable`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Медный слиток (`minecraft:copper_ingot`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Стекло памяти (`opusvsexe:memory_glass`) ×1

[Источник: `memory_cable.json`](../src/main/resources/data/opusvsexe/recipes/memory_cable.json)

<a id="recipe-memory_console"></a>

### Консоль памяти

**Результат:** Консоль памяти ×1 · `opusvsexe:memory_console`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стекло памяти (`opusvsexe:memory_glass`) ×1
- **B** — Канал передачи данных (`opusvsexe:data_conduit`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `memory_console.json`](../src/main/resources/data/opusvsexe/recipes/memory_console.json)

<a id="recipe-memory_glass"></a>

### Стекло памяти

**Результат:** Стекло памяти ×4 · `opusvsexe:memory_glass`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стекло (`minecraft:glass`) ×1
- **B** — Осколок аметиста (`minecraft:amethyst_shard`) ×1
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1

[Источник: `memory_glass.json`](../src/main/resources/data/opusvsexe/recipes/memory_glass.json)

<a id="recipe-memory_sludge"></a>

### Осадок памяти

**Результат:** Осадок памяти ×2 · `opusvsexe:memory_sludge`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сгусток слизи (`minecraft:slime_ball`) ×1
- **B** — Стекло памяти (`opusvsexe:memory_glass`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `memory_sludge.json`](../src/main/resources/data/opusvsexe/recipes/memory_sludge.json)

<a id="recipe-oil_stain"></a>

### Масляное пятно

**Результат:** Масляное пятно ×2 · `opusvsexe:oil_stain`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Уголь (`minecraft:coal`) ×1
- **B** — Сгусток слизи (`minecraft:slime_ball`) ×1
- **C** — Чёрный краситель (`minecraft:black_dye`) ×1

[Источник: `oil_stain.json`](../src/main/resources/data/opusvsexe/recipes/oil_stain.json)

<a id="recipe-omega_frame"></a>

### Рама Омеги

**Результат:** Рама Омеги ×1 · `opusvsexe:omega_frame`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный блок (`minecraft:iron_block`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×1

[Источник: `omega_frame.json`](../src/main/resources/data/opusvsexe/recipes/omega_frame.json)

<a id="recipe-opus_containment_glass"></a>

### Сдерживающее стекло Опуса

**Результат:** Сдерживающее стекло Опуса ×4 · `opusvsexe:opus_containment_glass`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Стекло (`minecraft:glass`) ×2
- **B** — Незер-кварц (`minecraft:quartz`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `opus_containment_glass.json`](../src/main/resources/data/opusvsexe/recipes/opus_containment_glass.json)

<a id="recipe-opus_warhammer"></a>

### Боевой молот из Опуса

**Результат:** Боевой молот из Опуса ×1 · `opusvsexe:opus_warhammer`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |   D   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Железный блок (`minecraft:iron_block`) ×1
- **D** — Палка (`minecraft:stick`) ×2

[Источник: `opus_warhammer.json`](../src/main/resources/data/opusvsexe/recipes/opus_warhammer.json)

<a id="recipe-phase_gate"></a>

### Фазовые врата

**Результат:** Фазовые врата ×1 · `opusvsexe:phase_gate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Обсидиан (`minecraft:obsidian`) ×1
- **B** — Эндер-жемчуг (`minecraft:ender_pearl`) ×1
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1

[Источник: `phase_gate.json`](../src/main/resources/data/opusvsexe/recipes/phase_gate.json)

<a id="recipe-phased_barrier"></a>

### Фазовый барьер

**Результат:** Фазовый барьер ×1 · `opusvsexe:phased_barrier`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Синий барьер (`opusvsexe:energy_barrier_blue`) ×1
- **B** — Эндер-жемчуг (`minecraft:ender_pearl`) ×1
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1

[Источник: `phased_barrier.json`](../src/main/resources/data/opusvsexe/recipes/phased_barrier.json)

<a id="recipe-pulse_turret"></a>

### Импульсная турель

**Результат:** Импульсная турель ×1 · `opusvsexe:pulse_turret`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный блок (`minecraft:iron_block`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `pulse_turret.json`](../src/main/resources/data/opusvsexe/recipes/pulse_turret.json)

<a id="recipe-radio"></a>

### Рация

**Результат:** Рация ×1 · `opusvsexe:radio`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×1
- **B** — Медный слиток (`minecraft:copper_ingot`) ×1
- **C** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **D** — Кабель памяти (`opusvsexe:memory_cable`) ×1

[Источник: `radio.json`](../src/main/resources/data/opusvsexe/recipes/radio.json)

<a id="recipe-reinforced_opus_block"></a>

### Усиленный блок Опуса

**Результат:** Усиленный блок Опуса ×1 · `opusvsexe:reinforced_opus_block`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Ядро Опуса (`opusvsexe:core_opus`) ×9

[Источник: `reinforced_opus_block.json`](../src/main/resources/data/opusvsexe/recipes/reinforced_opus_block.json)

<a id="recipe-resonance_forge"></a>

### Резонансная кузница

**Результат:** Резонансная кузница ×1 · `opusvsexe:resonance_forge`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сломанная резонансная кузница (`opusvsexe:broken_resonance_forge`) ×1
- **B** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1
- **C** — Железный блок (`minecraft:iron_block`) ×1
- **D** — Плавильная печь (`minecraft:blast_furnace`) ×1

[Источник: `resonance_forge.json`](../src/main/resources/data/opusvsexe/recipes/resonance_forge.json)

<a id="recipe-reward_vault"></a>

### Сундук наград

**Результат:** Сундук наград ×1 · `opusvsexe:reward_vault`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сундук (`minecraft:chest`) ×1
- **B** — Усиленный блок Опуса (`opusvsexe:reinforced_opus_block`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `reward_vault.json`](../src/main/resources/data/opusvsexe/recipes/reward_vault.json)

<a id="recipe-scanner_eye"></a>

### Глаз-сканер

**Результат:** Глаз-сканер ×1 · `opusvsexe:scanner_eye`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Око Эндера (`minecraft:ender_eye`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Стекло памяти (`opusvsexe:memory_glass`) ×1

[Источник: `scanner_eye.json`](../src/main/resources/data/opusvsexe/recipes/scanner_eye.json)

<a id="recipe-scorched_concrete"></a>

### Обожжённый бетон

**Результат:** Обожжённый бетон ×4 · `opusvsexe:scorched_concrete`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Чернит (`minecraft:blackstone`) ×1
- **B** — Жильная кора (`opusvsexe:magma_crust`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `scorched_concrete.json`](../src/main/resources/data/opusvsexe/recipes/scorched_concrete.json)

<a id="recipe-sealed_bulkhead"></a>

### Герметичная переборка

**Результат:** Герметичная переборка ×1 · `opusvsexe:sealed_bulkhead`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный блок (`minecraft:iron_block`) ×1
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×1
- **C** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1

[Источник: `sealed_bulkhead.json`](../src/main/resources/data/opusvsexe/recipes/sealed_bulkhead.json)

<a id="recipe-sealed_hatch"></a>

### Герметичный люк

**Результат:** Герметичный люк ×1 · `opusvsexe:sealed_hatch`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный блок (`minecraft:iron_block`) ×1
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×1
- **C** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1
- **D** — Железный люк (`minecraft:iron_trapdoor`) ×1

[Источник: `sealed_hatch.json`](../src/main/resources/data/opusvsexe/recipes/sealed_hatch.json)

<a id="recipe-sequence_keypad"></a>

### Клавиатура последовательности

**Результат:** Клавиатура последовательности ×1 · `opusvsexe:sequence_keypad`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×1
- **B** — Редстоуновая пыль (`minecraft:redstone`) ×1
- **C** — Канал передачи данных (`opusvsexe:data_conduit`) ×1

[Источник: `sequence_keypad.json`](../src/main/resources/data/opusvsexe/recipes/sequence_keypad.json)

<a id="recipe-shadow_boots"></a>

### Тёмные ботинки

**Результат:** Тёмные ботинки ×1 · `opusvsexe:shadow_boots`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Теневая нить (`opusvsexe:shade_silk`) ×2
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `shadow_boots.json`](../src/main/resources/data/opusvsexe/recipes/shadow_boots.json)

<a id="recipe-shadow_chestplate"></a>

### Тёмный нагрудник

**Результат:** Тёмный нагрудник ×1 · `opusvsexe:shadow_chestplate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Теневая нить (`opusvsexe:shade_silk`) ×6
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `shadow_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/shadow_chestplate.json)

<a id="recipe-shadow_helmet"></a>

### Тёмный капюшон

**Результат:** Тёмный капюшон ×1 · `opusvsexe:shadow_helmet`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Теневая нить (`opusvsexe:shade_silk`) ×4
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `shadow_helmet.json`](../src/main/resources/data/opusvsexe/recipes/shadow_helmet.json)

<a id="recipe-shadow_leggings"></a>

### Тёмные поножи

**Результат:** Тёмные поножи ×1 · `opusvsexe:shadow_leggings`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Теневая нить (`opusvsexe:shade_silk`) ×5
- **B** — Оплетённый корнями глаз (`opusvsexe:rootbound_eye`) ×1
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `shadow_leggings.json`](../src/main/resources/data/opusvsexe/recipes/shadow_leggings.json)

<a id="recipe-shield_node"></a>

### Узел щита

**Результат:** Узел щита ×1 · `opusvsexe:shield_node`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Щит (`minecraft:shield`) ×1
- **B** — Ядро Опуса (`opusvsexe:core_opus`) ×1
- **C** — Пульсирующее ядро (`opusvsexe:pulsing_core`) ×1

[Источник: `shield_node.json`](../src/main/resources/data/opusvsexe/recipes/shield_node.json)

<a id="recipe-signal_panel"></a>

### Сигнальная панель

**Результат:** Сигнальная панель ×1 · `opusvsexe:signal_panel`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Кабель памяти (`opusvsexe:memory_cable`) ×1
- **B** — Железный слиток (`minecraft:iron_ingot`) ×1
- **C** — Необработанный Опус (`opusvsexe:raw_opus`) ×1

[Источник: `signal_panel.json`](../src/main/resources/data/opusvsexe/recipes/signal_panel.json)

<a id="recipe-sky_laser_gun"></a>

### Небесная лазерная пушка

**Результат:** Небесная лазерная пушка ×1 · `opusvsexe:sky_laser_gun`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Тяжёлая лазерная пушка (`opusvsexe:heavy_laser_gun`) ×1
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1
- **C** — Слеза ИИ (`opusvsexe:ai_tear`) ×1
- **D** — Звезда Незера (`minecraft:nether_star`) ×1

[Источник: `sky_laser_gun.json`](../src/main/resources/data/opusvsexe/recipes/sky_laser_gun.json)

<a id="recipe-tank_trap"></a>

### Противотанковая ловушка

**Результат:** Противотанковая ловушка ×2 · `opusvsexe:tank_trap`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Железный слиток (`minecraft:iron_ingot`) ×3
- **B** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1

[Источник: `tank_trap.json`](../src/main/resources/data/opusvsexe/recipes/tank_trap.json)

<a id="recipe-titan_plate"></a>

### Пластина памяти Титана

**Результат:** Пластина памяти Титана ×1 · `opusvsexe:titan_plate`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Незеритовый слиток (`minecraft:netherite_ingot`) ×1
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1
- **C** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×1

[Источник: `titan_plate.json`](../src/main/resources/data/opusvsexe/recipes/titan_plate.json)

<a id="recipe-trial_trigger"></a>

### Триггер испытания

**Результат:** Триггер испытания ×1 · `opusvsexe:trial_trigger`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Редстоуновый блок (`minecraft:redstone_block`) ×1
- **B** — Пульсирующее ядро (`opusvsexe:pulsing_core`) ×1
- **C** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×1

[Источник: `trial_trigger.json`](../src/main/resources/data/opusvsexe/recipes/trial_trigger.json)

<a id="recipe-wave_terminal"></a>

### Терминал волны

**Результат:** Терминал волны ×1 · `opusvsexe:wave_terminal`

Бесформенный рецепт — расположение на схеме условное.

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Глаз-сканер (`opusvsexe:scanner_eye`) ×1
- **B** — Медный слиток (`minecraft:copper_ingot`) ×1
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×1

[Источник: `wave_terminal.json`](../src/main/resources/data/opusvsexe/recipes/wave_terminal.json)

## Opus Assembly Table · 5×5 — 6

<a id="recipe-exo_1_activation_core"></a>

### Ядро активации EXO-1

**Результат:** Ядро активации EXO-1 ×1 · `opusvsexe:exo_1_activation_core`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   D   |   C   |   D   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сломанный корпус ЭКС (`opusvsexe:broken_exo_hull`) ×10
- **B** — Пульсирующее ядро (`opusvsexe:pulsing_core`) ×4
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×3
- **D** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×2

[Источник: `exo_1_activation_core.json`](../src/main/resources/data/opusvsexe/recipes/exo_1_activation_core.json)

<a id="recipe-exo_2_activation_core"></a>

### Ядро активации EXO-2

**Результат:** Ядро активации EXO-2 ×1 · `opusvsexe:exo_2_activation_core`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |   B   |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   C   |   D   |   A   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   C   |   E   |   C   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   A   |   D   |   C   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |   B   |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Сломанный корпус ЭКС (`opusvsexe:broken_exo_hull`) ×8
- **B** — Фрагмент Опуса (`opusvsexe:opus_fragment`) ×6
- **C** — Резонансный Опус (`opusvsexe:resonant_opus`) ×4
- **D** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×2
- **E** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `exo_2_activation_core.json`](../src/main/resources/data/opusvsexe/recipes/exo_2_activation_core.json)

<a id="recipe-exo_3_activation_core"></a>

### Ядро активации EXO-3

**Результат:** Ядро активации EXO-3 ×1 · `opusvsexe:exo_3_activation_core`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   C   |   D   |   C   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   C   |   B   |   C   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×8
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×5
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×5
- **D** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×1

[Источник: `exo_3_activation_core.json`](../src/main/resources/data/opusvsexe/recipes/exo_3_activation_core.json)

<a id="recipe-exo_4_activation_core"></a>

### Ядро активации EXO-4

**Результат:** Ядро активации EXO-4 ×1 · `opusvsexe:exo_4_activation_core`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   C   |       |   D   |       |   C   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Резонансный Опус (`opusvsexe:resonant_opus`) ×8
- **B** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×4
- **C** — Ядро Опуса (`opusvsexe:core_opus`) ×4
- **D** — Слеза ИИ (`opusvsexe:ai_tear`) ×1

[Источник: `exo_4_activation_core.json`](../src/main/resources/data/opusvsexe/recipes/exo_4_activation_core.json)

<a id="recipe-exo_5_activation_core"></a>

### Ядро активации EXO-5

**Результат:** Ядро активации EXO-5 ×1 · `opusvsexe:exo_5_activation_core`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   A   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   C   |   B   |   C   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   A   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|       |   A   |       |   A   |       |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×8
- **B** — Резонансный Опус (`opusvsexe:resonant_opus`) ×7
- **C** — Слеза ИИ (`opusvsexe:ai_tear`) ×4

[Источник: `exo_5_activation_core.json`](../src/main/resources/data/opusvsexe/recipes/exo_5_activation_core.json)

<a id="recipe-exo_assembly_frame"></a>

### Рама сборки ЭКС

**Результат:** Рама сборки ЭКС ×1 · `opusvsexe:exo_assembly_frame`

```text
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   D   |   E   |   D   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   C   |   E   |   F   |   E   |   C   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   B   |   D   |   E   |   D   |   B   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
|       |       |       |       |       |
|   A   |   B   |   C   |   B   |   A   |
|       |       |       |       |       |
+-------+-------+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Пластина памяти Титана (`opusvsexe:titan_plate`) ×4
- **B** — Обшивка крепости (`opusvsexe:fortress_plating`) ×8
- **C** — Стекло памяти (`opusvsexe:memory_glass`) ×4
- **D** — Энергоузел (`opusvsexe:energy_relay`) ×4
- **E** — Стабилизированный Опус (`opusvsexe:stabilized_opus`) ×4
- **F** — Ядро Опуса (`opusvsexe:core_opus`) ×1

[Источник: `exo_assembly_frame.json`](../src/main/resources/data/opusvsexe/recipes/exo_assembly_frame.json)

## Parthenon Forge · 3×3 — 14

<a id="recipe-aerie_bronze_boots"></a>

### Сапоги из небесной бронзы

**Результат:** Сапоги из небесной бронзы ×1 · `opusvsexe:aerie_bronze_boots`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×4

[Источник: `aerie_bronze_boots.json`](../src/main/resources/data/opusvsexe/recipes/aerie_bronze_boots.json)

<a id="recipe-aerie_bronze_chestplate"></a>

### Кираса из небесной бронзы

**Результат:** Кираса из небесной бронзы ×1 · `opusvsexe:aerie_bronze_chestplate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×8

[Источник: `aerie_bronze_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/aerie_bronze_chestplate.json)

<a id="recipe-aerie_bronze_helmet"></a>

### Шлем из небесной бронзы

**Результат:** Шлем из небесной бронзы ×1 · `opusvsexe:aerie_bronze_helmet`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×5

[Источник: `aerie_bronze_helmet.json`](../src/main/resources/data/opusvsexe/recipes/aerie_bronze_helmet.json)

<a id="recipe-aerie_bronze_ingot"></a>

### Слиток небесной бронзы

**Результат:** Слиток небесной бронзы ×4 · `opusvsexe:aerie_bronze_ingot`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   E   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Солнечное перо (`opusvsexe:sunfeather`) ×4
- **B** — Облачное руно (`opusvsexe:cloud_fleece`) ×1
- **C** — Медный слиток (`minecraft:copper_ingot`) ×2
- **D** — Золотой слиток (`minecraft:gold_ingot`) ×1
- **E** — Райский плод (`opusvsexe:paradise_fruit`) ×1

[Источник: `aerie_bronze_ingot.json`](../src/main/resources/data/opusvsexe/recipes/aerie_bronze_ingot.json)

<a id="recipe-aerie_bronze_leggings"></a>

### Поножи из небесной бронзы

**Результат:** Поножи из небесной бронзы ×1 · `opusvsexe:aerie_bronze_leggings`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   A   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×7

[Источник: `aerie_bronze_leggings.json`](../src/main/resources/data/opusvsexe/recipes/aerie_bronze_leggings.json)

<a id="recipe-parthenon_axe"></a>

### Лабрис Парфенона

**Результат:** Лабрис Парфенона ×1 · `opusvsexe:parthenon_axe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   C   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   D   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×2
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмазный топор (`minecraft:diamond_axe`) ×1
- **D** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_axe.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_axe.json)

<a id="recipe-parthenon_boots"></a>

### Сапоги Парфенона

**Результат:** Сапоги Парфенона ×1 · `opusvsexe:parthenon_boots`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   C   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   D   |       |   D   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **B** — Алмаз (`minecraft:diamond`) ×2
- **C** — Сапоги из небесной бронзы (`opusvsexe:aerie_bronze_boots`) ×1
- **D** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×2

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_boots.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_boots.json)

<a id="recipe-parthenon_chestplate"></a>

### Крылатая кираса Парфенона

**Результат:** Крылатая кираса Парфенона ×1 · `opusvsexe:parthenon_chestplate`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |   C   |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×4
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмаз (`minecraft:diamond`) ×3
- **D** — Кираса из небесной бронзы (`opusvsexe:aerie_bronze_chestplate`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_chestplate.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_chestplate.json)

<a id="recipe-parthenon_helmet"></a>

### Ореол Парфенона

**Результат:** Ореол Парфенона ×1 · `opusvsexe:parthenon_helmet`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Алмаз (`minecraft:diamond`) ×3
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×2
- **D** — Шлем из небесной бронзы (`opusvsexe:aerie_bronze_helmet`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_helmet.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_helmet.json)

<a id="recipe-parthenon_hoe"></a>

### Мотыга Парфенона

**Результат:** Мотыга Парфенона ×1 · `opusvsexe:parthenon_hoe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   C   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   D   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×1
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмазная мотыга (`minecraft:diamond_hoe`) ×1
- **D** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_hoe.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_hoe.json)

<a id="recipe-parthenon_leggings"></a>

### Поножи Парфенона

**Результат:** Поножи Парфенона ×1 · `opusvsexe:parthenon_leggings`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |   C   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   A   |       |   A   |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×4
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмаз (`minecraft:diamond`) ×2
- **D** — Поножи из небесной бронзы (`opusvsexe:aerie_bronze_leggings`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_leggings.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_leggings.json)

<a id="recipe-parthenon_pickaxe"></a>

### Кирка Парфенона

**Результат:** Кирка Парфенона ×1 · `opusvsexe:parthenon_pickaxe`

```text
+-------+-------+-------+
|       |       |       |
|   A   |   B   |   A   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   C   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   D   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×2
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмазная кирка (`minecraft:diamond_pickaxe`) ×1
- **D** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_pickaxe.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_pickaxe.json)

<a id="recipe-parthenon_shovel"></a>

### Лопата Парфенона

**Результат:** Лопата Парфенона ×1 · `opusvsexe:parthenon_shovel`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   B   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   C   |   D   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **B** — Алмазная лопата (`minecraft:diamond_shovel`) ×1
- **C** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×1
- **D** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_shovel.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_shovel.json)

<a id="recipe-parthenon_sword"></a>

### Ксифос Парфенона

**Результат:** Ксифос Парфенона ×1 · `opusvsexe:parthenon_sword`

```text
+-------+-------+-------+
|       |       |       |
|       |   A   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   C   |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |   D   |       |
|       |       |       |
+-------+-------+-------+
```

**Ингредиенты (на один крафт):**

- **A** — Позолоченный мрамор Парфенона (`opusvsexe:gilded_marble`) ×1
- **B** — Рубиновый осколок ореола (`opusvsexe:ruby_halo_shard`) ×1
- **C** — Алмазный меч (`minecraft:diamond_sword`) ×1
- **D** — Слиток небесной бронзы (`opusvsexe:aerie_bronze_ingot`) ×1

Ruby Halo Shard возвращается после крафта и не расходуется.

[Источник: `parthenon_sword.json`](../src/main/resources/data/opusvsexe/recipes/parthenon_sword.json)

## Resonance Forge · превращения

Включите кузницу огнивом через ПКМ. Положите один подходящий ингредиент через ПКМ и подождите 160 тактов (8 секунд при 20 TPS). Заберите результат пустой рукой перед следующим превращением. Каждое превращение расходует один входной предмет и даёт один выходной. Огниво переключает состояние кузницы и не входит в рецепт.

| 1 × input | 1 × output | Время |
| :--- | :--- | :--- |
| Необработанный Опус (`opusvsexe:raw_opus`) | Стабилизированный Опус (`opusvsexe:stabilized_opus`) | 8 секунд при 20 TPS |
| Стабилизированный Опус (`opusvsexe:stabilized_opus`) | Резонансный Опус (`opusvsexe:resonant_opus`) | 8 секунд при 20 TPS |
| Резонансный Опус (`opusvsexe:resonant_opus`) | Ядро Опуса (`opusvsexe:core_opus`) | 8 секунд при 20 TPS |

[Источник](../src/main/java/com/opus/blockentity/ResonanceForgeBlockEntity.java)

## Сборка EXO

Скрафтите EXO Assembly Frame и ядро активации, затем нажмите ПКМ по раме подходящим ядром. Сборка занимает 60 тактов (3 секунды при 20 TPS), проверяет место и занятость и создаёт соответствующий EXO. В выживании ядро расходуется. Это взаимодействие с блоком, а не дополнительный рецепт в сетке.

## Обновление каталога

Схемы созданы из JSON ресурсов и реализации Resonance Forge. Не редактируйте сгенерированные сетки вручную.

```sh
python3 scripts/generate_recipe_book.py
python3 scripts/generate_recipe_book.py --check
```
