# Глубокий промпт и техническое ТЗ для редизайна инструментов

## Критическое ограничение проекта

**Катаны не переделывать вообще.** Не изменять дизайн, текстуры, модели, анимации, JSON, названия ресурсов, отображение в руках, рецепты, способности и код следующих предметов:

- **katana.png**
- **long_katana.png**
- **katana_op.png**
- **katana_gold.png**
- **katana_refined.png**
- модели **katana.json**, **long_katana.json**, **katana_op.json**, **katana_gold.json**, **katana_refined.json**
- классы и способности катан

Работать только со следующим whitelist из 20 предметов:

| Семейство | Предметы |
|---|---|
| Opus | opus_warhammer, opus_pickaxe, opus_axe, opus_shovel, opus_hoe |
| Огненный Жил | fire_sword, fire_pickaxe, fire_axe, fire_shovel, fire_hoe |
| Парфенон | parthenon_sword, parthenon_pickaxe, parthenon_axe, parthenon_shovel, parthenon_hoe |
| Тёмный лес | dark_forest_sword, dark_forest_pickaxe, dark_forest_axe, dark_forest_shovel, dark_forest_hoe |

Техническая база проекта: Minecraft 1.20.1, Fabric, Java 17, GeckoLib 4.4.9. Большинство item-моделей используют minecraft:item/handheld. У существующих предметов есть png.mcmeta с покадровой анимацией. Не меняй архитектуру и не подключай новый renderer без проверки совместимости с текущим Fabric-клиентом.

---

## Главный copy-paste промпт для другой ИИ

Ты работаешь как lead game artist, pixel-art texture artist, Blockbench modeler и Fabric 1.20.1 technical artist. Выполни глубокий редизайн только 20 предметов из whitelist выше. Катаны полностью заморожены и не должны быть затронуты ни одним действием.

Сначала проведи аудит проекта: найди реальные PNG, png.mcmeta, item JSON, регистрации предметов, рецепты, creative tabs, классы способностей и существующие display-трансформации. Составь таблицу: предмет, текущая текстура, текущая модель, текущий размер, наличие анимации, необходимость изменения Java-кода и итоговый план. До редактирования покажи список файлов, которые разрешено менять, и список файлов, которые запрещено менять. Не переименовывай ресурсы без крайней необходимости.

Создай четыре связанные визуальные семьи, но не своди дизайн к простой смене цвета. Каждый предмет обязан иметь:

1. читаемый силуэт в масштабе 16×16;
2. ясную конструкцию: рабочая часть, крепление, рукоять, навершие;
3. ванильную Minecraft-пиксельную палитру;
4. отдельные слои outline, base, shadow, material detail, highlight и optional emissive;
5. анимацию только там, где она оправдана материалом;
6. корректные отображения GUI, ground, first-person и third-person;
7. игровую проверку после импорта.

Строго запрещены фотореализм, гладкая digital painting-манера, anti-aliasing, blur, мягкие градиенты, случайный шум, тонкие субпиксельные линии, текст, watermark, UI-слоты, руки, персонажи, окружение внутри PNG и декоративные элементы, которые уничтожают функциональный силуэт.

---

## Единый художественный язык

### Силуэт

Сначала создай двухцветный силуэт: почти чёрный outline плюс один базовый цвет. Проверь предмет без деталей. Меч не должен выглядеть копьём, кирка — боевым крюком, топор — щитом, лопата — дверью или бронёй, мотыга — серпом, крюком или киркой, вархаммер — булавой.

Каждый инструмент должен подчиняться визуальной иерархии:

- 55–70% площади — функциональный основной материал;
- 15–25% — тени и конструкционные углубления;
- 5–12% — блики и material accent;
- максимум 5–8% — emissive или магический акцент.

### Сетка и масштаб

Разрабатывай master в 32×32, затем вручную адаптируй в 16×16. Используй nearest-neighbor. Диагонали строй ступеньками 1–2 пикселя. Не оставляй детали, которые при уменьшении превращаются в грязь. После уменьшения сравни предмет с ванильными sword, pickaxe, axe, shovel и hoe.

### Обязательные слои

Рабочий файл каждого предмета должен иметь:

1. GUIDE_SILHOUETTE — временная форма, не экспортировать;
2. OUTLINE — непрерывный почти чёрный контур;
3. BASE_MATERIAL — металл, дерево, камень, обсидиан;
4. SHADOW — нижняя сторона, внутренние углы, под креплениями;
5. MID_DETAIL — швы, кольца, трещины, корни, геометрия;
6. HIGHLIGHT — редкие светлые пиксели на верхней рабочей кромке;
7. EMISSIVE_STATIC — неподвижные магические пиксели;
8. EMISSIVE_ANIMATED — только движущиеся пиксели или короткие каналы;
9. MASK_DEBUG — временная проверка границ и альфа-канала.

Если vanilla item model не поддерживает отдельный слой напрямую, собери стабильный layer0 и только затем добавляй layer1 или animated overlay способом, который реально поддерживается текущим проектом. Не меняй Java renderer ради обычного декоративного свечения.

### Анимированные текстуры

Один кадр должен быть квадратом 16×16 или 32×32, кадры складываются вертикально. Все кадры имеют одинаковый размер, одинаковую геометрию и прозрачный фон. Между кадрами разрешено менять только emissive-пиксели, слабое мерцание кристалла, жар в трещинах или небольшой moss highlight. Outline, рукоять, рабочая форма и базовые тени не должны прыгать.

Используй покадровую анимацию без интерполяции:

~~~json
{
  "animation": {
    "frametime": 4,
    "interpolate": false
  }
}
~~~

Рекомендуемые значения: 2–3 тика для быстрого жара, 4–6 для обычного пульса, 8–12 для редкого магического мерцания. Яркий кадр не должен быть постоянным. Не анимируй весь предмет целиком.

### Модели

Если текущий handheld JSON даёт читаемый результат, оставь его. Для объёма используй простую Blockbench-модель из кубов и плоских панелей:

- shaft;
- head;
- socket;
- grip;
- blade или working_edge;
- small cap.

Не превращай пиксельный предмет в гладкую 3D-скульптуру. Не добавляй GeckoLib для item без проверки client-side pipeline. Любая модель обязана быть протестирована в GUI, на земле, в первой и третьей руке, в обеих руках.

---

# Индивидуальные задания

## 1. opus_warhammer.png — вархаммер Opus

### Глубокий дизайн

Создай тяжёлый технологичный артефакт из тёмного резонансного металла. Главный силуэт: длинная рукоять, крупная прямоугольная hammer head, массивный центральный блок и две короткие ударные грани. Предмет должен выглядеть как молот, а не булава, кирка или современное оружие.

Рукоять: тёмно-графитовая или почти чёрная, с 2–3 коричневыми пиксельными сегментами и металлическими кольцами у головы. Головка: чёрный корпус с серо-стальными верхними плоскостями. В центре — один квадратный cobalt/cyan crystal cluster, занимающий менее 10% площади. Ударные торцы — самые светлые части после кристалла. Швы — короткие cobalt-blue каналы, не сплошные неоновые полосы.

Сделай слой base стабильным и отдельный animated emissive atlas на 4 кадра: dim core, bright core, bright core plus one edge pixel, dim core. Outline, рукоять и металл не двигаются. Для модели используй только shaft, head, core, left_cap, right_cap, grip_cap. В GUI молот занимает 70–80% слота; в first-person не закрывает весь экран.

### Промпт

«Создай opus_warhammer.png для Minecraft Java 1.20.1 в ванильном pixel art. Прозрачный RGBA-фон, master 32×32 с ручной адаптацией в 16×16, жёсткие квадратные пиксели, ступенчатые диагонали и почти чёрный outline. Силуэт тяжёлого молота: длинная тёмная рукоять, большая прямоугольная головка из чёрного металла, две короткие серо-стальные ударные грани, квадратное cobalt-blue/cyan ядро в центре. Добавь редкие синие каналы в швах. Подготовь слои OUTLINE, BASE, SHADOW, DETAIL, HIGHLIGHT, STATIC EMISSIVE и отдельный 4-кадровый EMISSIVE_ANIMATED, где меняется только яркость ядра. Никаких булав, кирок, оружейной футуристики, сглаживания, градиентов, bloom, частиц, текста, рук, фона и 3D-реализма. Сохрани совместимый handheld item model и проверь GUI, ground, first-person и third-person.»

## 2. opus_pickaxe.png — кирка Opus

### Глубокий дизайн

Сделай компактную резонансную кирку: тёмная рукоять, горизонтальная металлическая головка с двумя острыми концами, центральное квадратное крепление и маленький синий кристалл. Рабочая головка должна занимать около 35–40% площади и быть узнаваемой без голубых деталей.

Используй graphite-black body, холодную steel-gray рабочую кромку, тёмно-коричневую рукоять и cobalt socket. Внутри головки допустимы 2–3 cyan pixels как короткий резонансный шов. Левая и правая части могут быть слегка разными по длине, но общий силуэт должен быть сбалансированным.

Создай animated layer на 3 кадра: idle, core bright, edge bright. Рабочие концы не меняются. JSON оставь handheld, если diagonal orientation корректна; объёмная версия допускает только head, socket, shaft и grip.

### Промпт

«Создай opus_pickaxe.png как ванильную Minecraft Java 1.20.1 pixel-art текстуру. Один предмет на прозрачном RGBA-фоне, master 32×32 и финальная версия 16×16, nearest-neighbor. Силуэт компактной кирки с двумя острыми рабочими концами, центральным квадратным socket и длинной тёмной рукоятью. Материалы: graphite metal, серо-стальные кромки, dark brown grip, маленький cobalt-blue crystal, 2–3 cyan pixels внутри металлического шва. Сначала двухцветный силуэт, затем слои outline, base, shadow, detail, highlight, static emissive и 3-кадровый animated emissive atlas; менять только яркость кристалла. Не добавляй крюки, руду, камни, оружейные элементы, bloom, anti-aliasing, текст, фон или гладкий 3D. Совместимый handheld JSON и проверка всех display-режимов.»

## 3. opus_axe.png — топор Opus

### Глубокий дизайн

Создай односторонний топор. Основная часть — широкая металлическая щека справа от рукояти, короткий прямой обух и чистая светлая режущая кромка. Это не лабрис и не двустороннее оружие. Крепление квадратное, с небольшим cobalt socket.

Корпус graphite, тени почти чёрные, рабочая кромка steel-gray. Рукоять тёмная, с двумя кольцами и максимум несколькими коричневыми пикселями. На внутреннем шве — короткая синяя линия. Анимация на 3 кадра: cyan pixel перемещается от socket к верхней части шва, но не пересекает рабочую кромку.

### Промпт

«Создай opus_axe.png в строгом ванильном Minecraft pixel art. Односторонний компактный топор: тёмная графитовая рукоять, квадратное крепление, одна широкая металлическая щека, короткий обух и чистая светло-серая режущая кромка. Материалы: graphite, steel gray, dark brown grip, cobalt socket и редкие cyan pixels во внутреннем шве. Сначала построь узнаваемый axe silhouette, затем добавь слои OUTLINE, BASE, SHADOW, DETAIL, HIGHLIGHT, STATIC EMISSIVE и 3-кадровую покадровую анимацию только синего шва. Не делай двусторонний топор, щит, кирку, sci-fi оружие, внешнее свечение, частицы, текст, фон, blur или 3D-рендер. PNG RGBA, nearest-neighbor, handheld item model, проверка GUI, ground, first-person и third-person.»

## 4. opus_shovel.png — лопата Opus

### Глубокий дизайн

Сделай утилитарную лопату из резонансного металла. Рабочая часть — цельная широкая пластина с плоским верхом, скошенными сторонами и коротким нижним остриём. Она не должна выглядеть щитом, дверью или панелью.

Лопаточная часть занимает 35–40% площади. Корпус graphite, кромка steel-gray, по центру короткий cyan channel, крепление квадратное, рукоять тёмная. Анимация — 4 кадра медленного пульса только центрального канала. Базовый слой полностью стабильный. Если нужен объём, используй одну плоскую extruded plate и простой shaft.

### Промпт

«Создай opus_shovel.png в ванильном Minecraft pixel art. Прозрачный фон, RGBA, 32×32 master и 16×16 final. Нарисуй одну цельную широкую shovel blade с плоским верхом, скошенными сторонами и коротким нижним остриём; длинная тёмная рукоять и квадратное крепление. Материалы: graphite-black metal, steel-gray edge, dark grip, короткий cobalt/cyan channel. Используй чёрный stepped outline, 2–3 тона на материал, крупные pixel clusters. Подготовь слои base, shadow, detail, highlight, static emissive и 4-кадровый slow-pulse atlas только для cyan channel. Не делай щит, дверь, меч, реалистичную панель, bloom, текст, фон, anti-aliasing или 3D. Сохрани handheld JSON и проверь display transformations.»

## 5. opus_hoe.png — мотыга Opus

### Глубокий дизайн

Сделай самую тонкую форму Opus-набора: длинная тёмная рукоять, короткое горизонтальное крепление и один явно загнутый рабочий конец. Рукоять примерно в 2–2,5 раза длиннее головки. Голова не должна выглядеть крюком или киркой.

Материалы: graphite metal, steel working edge, dark grip, маленький cobalt socket. Добавь 1–2 cyan pixels во внутреннем шве. Анимация — 3 кадра редкого пульса только socket. Никаких искр и следов движения.

### Промпт

«Создай opus_hoe.png в стиле ванильного Minecraft pixel art. Тонкая мотыга: длинная тёмная рукоять, короткая металлическая перекладина и один загнутый рабочий конец. Graphite body, steel edge, dark grip, маленький cobalt/cyan socket и 1–2 синих пикселя во внутреннем шве. Сохрани silhouette hoe, не крюка, серпа или кирки. Жёсткий почти чёрный outline, stepped diagonals, 2–3 тона. Подготовь слои outline, base, shadow, detail, highlight, static emissive и 3-кадровый atlas, где пульсирует только socket. Без bloom, частиц, текста, фона, сглаживания, градиентов и 3D-реализма. PNG RGBA, nearest-neighbor, совместимый handheld model.»

---

## 6. fire_sword.png — огненный меч Жил

### Глубокий дизайн

Это обычный меч, не катана. Создай прямой и достаточно широкий меч из обугленного вулканического металла. Лезвие должно иметь чистую режущую кромку, простую гарду, короткую коричневую рукоять и маленькое ember-навершие.

Основа blade — charcoal/obsidian metal. Внутри проходит одна ломаная magma vein: deep red shadow, red-orange midtone и 2–4 ember-yellow highlight pixels. Не делай всю кромку оранжевой. Огонь должен быть встроен в материал, без языков пламени снаружи.

Создай 5-кадровый animated emissive atlas: dark vein, red, orange, bright center, red. Двигай только 1–3 ярких пикселя, не outline и не саму геометрию. frametime 3–4, interpolate false.

### Промпт

«Создай fire_sword.png для Minecraft Java 1.20.1 в ванильном pixel art, это не катана. Прямой компактный sword с широким обугленным graphite/obsidian blade, почти чёрным stepped outline, простой гардой, тёмно-коричневой рукоятью и маленьким ember-навершием. Внутри blade — одна ломаная magma vein: deep red shadow, red-orange midtone, 2–4 ember-yellow highlight pixels. Металл должен оставаться видимым. Подготовь слои outline, base, shadow, detail, highlight, static emissive и вертикальный 5-кадровый animated emissive atlas; менять только яркость нескольких пикселей жилы. Без внешнего пламени, дыма, лавы, bloom, gradients, anti-aliasing, текста, рук, фона и 3D-рендера. RGBA PNG, nearest-neighbor, handheld JSON.»

## 7. fire_pickaxe.png — огненная кирка Жил

### Глубокий дизайн

Создай кирку из вулканического железа: две острые рабочие стороны, центральное крепление и коричневая рукоять. Head должен быть чёрным и тяжёлым, с красно-оранжевыми жилками внутри. Жилы не должны превращать инструмент в две полосы огня.

Рабочие концы — dark steel с небольшими светлыми кромками. Socket — один ember square. Создай 4 кадра: dark, red, orange, dark. Рабочая геометрия, outline и рукоять неподвижны. Модель — vanilla handheld либо простая extruded head.

### Промпт

«Создай fire_pickaxe.png как ванильную Minecraft pixel-art текстуру. Узнаваемая компактная кирка с двумя острыми рабочими концами, central socket и тёмной коричневой рукоятью. Материалы: обугленное graphite/obsidian железо, deep red shadow, red-orange magma cracks, редкие ember-yellow pixels. Сначала чистый silhouette с чёрным outline, затем слои base, shadow, detail, highlight, static emissive и вертикальный 4-кадровый atlas. В animated layer меняются только 1–3 orange pixels внутри трещин. Без внешнего пламени, дыма, лавы, частиц, реализма, текста, anti-aliasing, bloom и 3D. RGBA, nearest-neighbor, handheld item JSON.»

## 8. fire_axe.png — огненный топор Жил

### Глубокий дизайн

Сделай односторонний тяжёлый axe. Широкая клиновидная щека, короткий обух, чистая рабочая кромка и коричневая рукоять. Металл обуглен, но кромка читается. В креплении — маленький ember socket. Red-orange cracks находятся в корпусе, а не снаружи.

Animated atlas на 4 кадра: маленькая горячая точка проходит по одной внутренней трещине. Рабочая кромка не пульсирует целиком. Не добавляй внешний огонь.

### Промпт

«Создай fire_axe.png в ванильном Minecraft pixel art. Односторонний тяжёлый axe: dark brown handle, квадратное крепление, одна широкая клиновидная металлическая щека, короткий обух и чистая режущая кромка. Обугленный graphite metal, deep red cracks, red-orange internal vein, 1–3 ember-yellow pixels в socket. Чёрный outline, плоские ступенчатые тени, ограниченная палитра. Создай слои outline, base, shadow, detail, highlight, static emissive и 4-кадровый animated emissive atlas, где меняется только маленькая hot point внутри blade. Не делай лабрис, щит, кирку, внешнее пламя, дым, bloom, текст, фон, anti-aliasing и 3D. PNG RGBA, nearest-neighbor, handheld model.»

## 9. fire_shovel.png — огненная лопата Жил

### Глубокий дизайн

Рабочая часть — широкая прямоугольная shovel blade с ровным верхом, слегка скошенными боками и рабочим нижним краем. Не делай щит. Blade из тёмного обугленного металла, центральная красно-оранжевая трещина, маленький ember socket в креплении, короткая коричневая рукоять.

Animated atlas на 3 кадра. Меняй только яркость crack; форма лопаты стабильна. Возможная модель — handheld или простая плоская extruded plate.

### Промпт

«Создай fire_shovel.png в ванильном Minecraft Java pixel art. Компактная широкая shovel blade из обугленного чёрно-серого железа, ровный верх, скошенные бока, рабочий нижний край, короткий neck и тёмная коричневая рукоять. В центре blade — одна red-orange magma crack, в socket — маленький ember pixel. Сильный чёрный outline, deep red shadows, 2–3 тона на материал. Подготовь слои outline, base, shadow, detail, highlight, static emissive и 3-кадровый animated atlas с изменением яркости только crack. Без щита, двери, лавы, дыма, bloom, текста, сглаживания, градиентов, фона и 3D-рендера. RGBA PNG, nearest-neighbor, handheld JSON.»

## 10. fire_hoe.png — огненная мотыга Жил

### Глубокий дизайн

Сделай тонкую hoe: длинная тёмно-коричневая рукоять, короткая металлическая голова и один загнутый рабочий конец. Внутренняя сторона крюка тёмно-красная и оранжевая, внешняя сторона остаётся чёрно-серой. Не добавляй длинный пламенный хвост.

Анимация — 3 кадра, один яркий пиксель перемещается по внутренней кромке. Outline и рабочая геометрия стабильны.

### Промпт

«Создай fire_hoe.png как ванильную Minecraft pixel-art текстуру. Тонкая hoe с длинной тёмно-коричневой рукоятью, короткой металлической головкой и одним загнутым рабочим концом. Головка из обугленного чёрно-серого металла, по внутренней режущей кромке короткая red-orange magma vein, один ember pixel в socket. Сохрани форму мотыги, не крюка и не серпа. Создай outline, base, shadow, detail, highlight, static emissive и 3-кадровый animated atlas, где изменяется только яркость жилы. Без внешнего пламени, дыма, lava background, bloom, anti-aliasing, текста и 3D. RGBA, nearest-neighbor, handheld item model.»

---

## 11. parthenon_sword.png — ксифос Парфенона

### Глубокий дизайн

Это обычный меч, не катана. Силуэт — компактный прямой Xiphos с листовидным, но ступенчатым blade, простой бронзово-золотой гардой и коричневой рукоятью. Сделай храмовый характер через материал и симметрию, а не через мелкую историческую филигрань.

Палитра: dark brown outline, ivory blade, muted gold/bronze, один ruby-red crystal. Optional animated ruby — 3 кадра очень слабой пульсации. Ruby не должен занимать больше 3–5 пикселей.

### Промпт

«Создай parthenon_sword.png в ванильном Minecraft pixel art, это не катана. Компактный прямой Xiphos с листовидным ivory blade, тёмным коричневым stepped outline, простой bronze/gold guard, коричневой рукоятью и одним маленьким ruby-red pixel в центре гарды. Ограниченная палитра, 2–3 тона на материал, крупные pixel clusters. Подготовь слои outline, base, shadow, detail, highlight, static ruby emissive и optional 3-кадровый atlas, где меняется только ruby highlight. Без античной реалистичной филиграни, колонн, лаврового фона, текста, bloom, anti-aliasing, watermark и 3D. RGBA PNG, nearest-neighbor, handheld JSON.»

## 12. parthenon_pickaxe.png — кирка Парфенона

### Глубокий дизайн

Создай кирку из ivory stone-metal, бронзы и дерева. Два рабочих конца, простое центральное крепление и маленький ruby. Золотые геометрические пиксели должны быть редкими и не превращать head в орнаментальный герб.

Силуэт кирки должен быть заметен без ruby. Base, shadow и outline не анимируются. Ruby atlas на 3 кадра: dim, bright, dim. Модель — handheld; extruded head разрешена только в простой кубической форме.

### Промпт

«Создай parthenon_pickaxe.png как ванильную Minecraft pixel-art текстуру. Узнаваемая кирка: коричневая деревянная рукоять, светлая ivory/stone-metal головка, два рабочих конца, bronze central socket и один ruby-red pixel. Добавь максимум 2–3 muted-gold geometric pixels. Чёрно-коричневый outline, stepped edges, 2–3 тона на материал, без шумной мраморной текстуры. Подготовь слои outline, base, shadow, detail, highlight, static ruby и 3-кадровый ruby emissive atlas, где меняется только яркость ruby. Без лабрисных лезвий, колонн, фона, текста, сглаживания, bloom и smooth 3D. PNG RGBA, nearest-neighbor, handheld JSON.»

## 13. parthenon_axe.png — лабрис Парфенона

### Глубокий дизайн

Это единственный whitelist-предмет с намеренно двусторонней головой. Создай компактный Labrys с двумя симметричными ivory blades, бронзовым центральным блоком, коричневой рукоятью и ruby в центре. Лезвия должны оставаться рабочими и не сливаться в солнечный диск или щит.

Слои: outline, ivory base, dark ivory shadow, bronze socket, muted gold geometry, ruby emissive. Animated atlas на 4 кадра меняет только ruby и один золотой highlight. Симметрия и режущие кромки неподвижны. Для модели используй простые кубические/плоские части, без гладкой скульптуры.

### Промпт

«Создай parthenon_axe.png в ванильном Minecraft pixel art. Это симметричный двусторонний Labrys: два светлых ivory режущих лезвия, квадратный bronze/gold central block, коричневая рукоять и один ruby-red crystal pixel в центре. Силуэт именно топора, не щита, не солнечного диска и не герба. Ограниченная палитра, тёмный коричневый outline, ivory shadows, muted gold highlights, stepped edges. Создай слои outline, base, shadow, detail, highlight, static ruby и 4-кадровый animated atlas только для ruby/gold accent; лезвия и outline не двигаются. Без барочной детализации, текста, колонн, фона, anti-aliasing, bloom и 3D. RGBA PNG, nearest-neighbor, простая handheld или кубическая item-модель.»

## 14. parthenon_shovel.png — лопата Парфенона

### Глубокий дизайн

Рабочая часть — широкая цельная ivory shovel blade с плоским верхом, скошенными боками и коротким рабочим низом. Бронзовая окантовка только сверху; geometric motif — максимум несколько пикселей. В креплении один ruby. Рукоять коричневая с бронзовым кольцом.

Ruby можно сделать статичным. Если нужна анимация, используй 3 медленных кадра только на ruby. Не делай blade похожей на щит или дверь.

### Промпт

«Создай parthenon_shovel.png как ванильную Minecraft Java pixel-art текстуру. Широкая цельная ivory shovel blade, плоский верх, скошенные стороны, практичный нижний край, тонкая bronze upper rim, коричневая рукоять и маленький ruby-red pixel в креплении. Добавь максимум 2–3 muted-gold geometric pixels, без орнаментального шума. Чёрно-коричневый stepped outline, 2–3 тона на материал. Подготовь слои outline, base, shadow, detail, highlight, ruby и optional 3-кадровую slow ruby animation без движения blade. Не делай щит, дверь, копьё, реалистичный мрамор, текст, фон, anti-aliasing, bloom или 3D. RGBA, nearest-neighbor, handheld JSON.»

## 15. parthenon_hoe.png — мотыга Парфенона

### Глубокий дизайн

Создай тонкую храмовую мотыгу: коричневая рукоять, короткая ivory/bronze головка, один загнутый рабочий конец, небольшой ruby в socket. Ruby и gold — только акценты, не основной материал. Рабочий конец должен быть тонким и функциональным, не декоративным крюком.

Optional animation — 3 кадра ruby. Сохрани прямую рукоять и чёткий silhouette hoe.

### Промпт

«Создай parthenon_hoe.png в ванильном Minecraft pixel art. Узкая hoe с длинной коричневой деревянной рукоятью, короткой ivory/bronze головкой и одним загнутым рабочим концом. В креплении один ruby-red pixel, рядом максимум 1–2 muted-gold geometric pixels. Жёсткий тёмный outline, stepped diagonals, 2–3 тона, прозрачный фон. Подготовь слои outline, base, shadow, detail, highlight, static ruby и optional 3-кадровую slow ruby animation; silhouette неподвижен. Не делай серп, крюк, кирку или орнаментальный символ. Без текста, anti-aliasing, bloom, gradients и 3D-рендера. PNG RGBA, nearest-neighbor, handheld model.»

---

## 16. dark_forest_sword.png — меч Тёмного леса

### Глубокий дизайн

Это обычный меч, не катана. Силуэт узкий, прямой или слегка неровный, с dark iron blade и небольшими thorn pixels у основания. Рукоять — twisted darkwood, но не толстая ветка. Violet flower и blue-green moss — небольшие акценты, не фон.

Рабочая кромка должна оставаться чистой. Animated atlas — 4 кадра слабого violet pulse на маленьком moss/flower node. Шипы, outline, blade и handle не двигаются.

### Промпт

«Создай dark_forest_sword.png в строгом ванильном Minecraft pixel art, это не катана. Узкий обычный sword с тёмно-серым iron blade, почти чёрным outline, немного неровной stepped edge, небольшими thorn pixels у основания, тёмно-коричневой twisted wood grip и 2–3 violet/blue-green moss pixels в гарде. Органические детали не должны закрывать blade. Подготовь слои outline, base, shadow, detail, highlight, static moss emissive и 4-кадровый слабый violet-pulse atlas только для маленького узла. Без лесного фона, тумана, листьев, больших веток, bloom, anti-aliasing, текста и 3D-реализма. PNG RGBA, nearest-neighbor, handheld JSON.»

## 17. dark_forest_pickaxe.png — кирка Тёмного леса

### Глубокий дизайн

Создай кирку с head из dark iron, handle из gloomwood и небольшими root/thorn knots. Рабочие концы короткие, острые и металлические; корни не должны превращать их в ветви. Blue-green moss — на одном внутреннем шве, violet — у socket.

Animated atlas на 4 кадра: dim, one moss bright, two moss bright, dim. Силуэт и рукоять неподвижны. Не добавляй листья, большие ветки, цветы или forest background.

### Промпт

«Создай dark_forest_pickaxe.png как ванильную Minecraft pixel-art текстуру. Компактная кирка с двумя острыми рабочими концами, dark iron head, deep brown gloomwood handle, маленькими root/thorn knots и несколькими blue-green moss/violet pixels. Органика только обрамляет крепление и рукоять, рабочие концы чистые. Используй чёрный outline, graphite shadows, bark-brown midtones, muted plum и teal accents. Подготовь слои outline, base, shadow, detail, highlight, static moss и 4-кадровый animated emissive atlas, где меняется только яркость 3–4 moss pixels. Без леса, листьев, тумана, больших корней, realistic 3D, blur, gradients, текста и bloom. RGBA PNG, nearest-neighbor, handheld model.»

## 18. dark_forest_axe.png — топор Тёмного леса

### Глубокий дизайн

Сделай односторонний топор с широкой dark iron cheek, чистой светлой рабочей кромкой и тонкой root wrapping на креплении. Корни усиливают конструкцию, но не заменяют металл. Violet flower или moss cluster — маленький и расположен в socket.

Animated atlas — 3–4 кадра, меняется только один moss node. Blade, outline, шипы и handle не анимируются.

### Промпт

«Создай dark_forest_axe.png в ванильном Minecraft pixel art. Односторонний axe: широкая тёмно-графитовая металлическая щека, короткий обух, чистая светло-серая режущая кромка, darkwood handle с тонкой root wrapping и маленький violet/blue-green moss node в socket. Сохрани compact axe silhouette, не лабрис и не щит. Ограниченная палитра, почти чёрный outline, ступенчатые края, минимум деталей. Подготовь слои outline, base, shadow, detail, highlight, static moss и 3–4-кадровую анимацию только маленького moss node. Без больших ветвей, растений, тумана, фона, bloom, сглаживания, текста и 3D-рендера. PNG RGBA, nearest-neighbor, handheld JSON.»

## 19. dark_forest_shovel.png — лопата Тёмного леса

### Глубокий дизайн

Создай широкую dark iron shovel blade с слегка асимметричной природной кромкой, но очевидной функцией лопаты. Рукоять gloomwood, одна тонкая root-wrap line, 2–3 blue-green moss pixels в центральной трещине, маленький violet flower cluster у socket.

Animated atlas — 4 кадра slow moss pulse. Blade и корни неподвижны. Не рисуй лист, щит или большую ветвь.

### Промпт

«Создай dark_forest_shovel.png как ванильную Minecraft Java pixel-art текстуру. Широкая shovel blade из dark iron, прямой или слегка скошенный верх, практичный рабочий низ, deep brown gloomwood handle с одной root-wrap line. В blade 2–3 blue-green moss pixels, в socket маленький violet flower cluster. Органические детали маленькие и не превращают предмет в лист или щит. Подготовь слои outline, base, shadow, detail, highlight, static moss и вертикальный 4-кадровый atlas для медленного moss pulse; silhouette не меняется. Без forest background, тумана, листьев, больших корней, bloom, anti-aliasing, gradients, текста и 3D. RGBA PNG, nearest-neighbor, handheld model.»

## 20. dark_forest_hoe.png — мотыга Тёмного леса

### Глубокий дизайн

Сделай тонкую мотыгу с рукоятью из тёмного дерева и короткой iron/thorn head. Один загнутый конец — рабочий. Root wrapping — максимум 2–3 узла. Violet и teal — маленькие акценты на socket и внутренней стороне рабочей части.

Animated atlas — 3 кадра мягкого teal pulse в одном moss pixel. Никаких больших цветков, лозы, ветвей и лесного окружения.

### Промпт

«Создай dark_forest_hoe.png в строгом ванильном Minecraft pixel art. Узкая hoe с длинной тёмно-коричневой wood/root handle, короткой dark iron head и одним загнутым thorn-подобным рабочим концом. Добавь 2–3 маленьких blue-green moss pixels и один muted violet socket pixel. Сохрани тонкий функциональный силуэт hoe, не серпа, крюка или ветки. Используй чёрный outline, stepped edges, ограниченную палитру и крупные pixel clusters. Подготовь слои outline, base, shadow, detail, highlight, static moss и 3-кадровый animated emissive atlas только для одного teal moss pixel. Без больших растений, лесного фона, тумана, glow aura, anti-aliasing, текста, watermark и 3D-реализма. PNG RGBA, nearest-neighbor, handheld model.»

---

# Технический план реализации

## Фаза A — аудит и защита катан

1. Составь список всех 20 разрешённых PNG, JSON и png.mcmeta.
2. Проверь, что ни один файл катан не попал в список изменений.
3. Создай резервную копию whitelist-файлов в отдельной безопасной папке.
4. Проверь регистрации предметов, рецепты, creative tabs и текущие display overrides.
5. Не меняй Java-код, пока новый ресурсный pipeline не проверен.
6. В финальном отчёте явно перечисли изменённые файлы и отдельно подтверди, что катаны не изменялись.

## Фаза B — master и слои

Для каждого предмета создай:

- двухцветный silhouette proof;
- master 32×32;
- финальный 16×16;
- палитру с hex-значениями;
- слои OUTLINE, BASE, SHADOW, DETAIL, HIGHLIGHT, EMISSIVE;
- preview на прозрачном фоне;
- preview на тёмном и светлом фоне;
- таблицу animation frames;
- краткое описание каждого слоя;
- при необходимости простую Blockbench-модель.

## Фаза C — текстуры

Экспортируй PNG RGBA. Не оставляй серые полупрозрачные ореолы по контуру. Проверяй альфа-канал на увеличении 800–1600%. Для обычных текстур используй nearest-neighbor. Для animated PNG высота должна быть равна высоте кадра, умноженной на число кадров. Все кадры выровняй по одной и той же сетке.

## Фаза D — item JSON

По умолчанию используй:

~~~json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "opusvsexe:item/ITEM_ID"
  }
}
~~~

Дополнительные слои добавляй только после проверки, что текущий parent их реально отрисовывает. Не меняй display-трансформации массово. Для каждого JSON отдельно проверь gui, ground, firstperson_righthand, firstperson_lefthand, thirdperson_righthand и thirdperson_lefthand.

## Фаза E — animation

Для каждого animated PNG создай корректный png.mcmeta с frametime и interpolate false. Начинай с медленного пульса и ускоряй только если это действительно нужно. Не делай постоянное яркое мигание: в ванильном Minecraft emissive — редкий акцент, а не большая светящаяся область.

## Фаза F — игровая проверка

Проверь каждый предмет:

- в инвентаре;
- на земле;
- в первой руке;
- в третьем лице;
- в обеих руках;
- у NPC или моба, если он его держит;
- при зачаровании;
- в низком освещении;
- во время анимации;
- после перезапуска клиента;
- рядом с оригинальными катанами, чтобы убедиться, что они не изменились.

## Критерии приёмки

Работа готова только если:

1. Все 20 whitelist-предметов получили новый согласованный дизайн.
2. Ни одна катана не изменена.
3. Каждый предмет узнаваем в размере 16×16.
4. Меч, кирка, молот, топор, лопата и мотыга не путаются.
5. У каждого семейства есть отдельная материальная логика.
6. Слои и animation atlas не ломают базовый силуэт.
7. Нет anti-aliasing, гладких градиентов, лишнего фона, текста и watermark.
8. JSON и png.mcmeta валидны для Minecraft 1.20.1 Fabric.
9. Проверены все display-режимы.
10. Финальный отчёт содержит полный список изменённых файлов и подтверждение защиты катан.

