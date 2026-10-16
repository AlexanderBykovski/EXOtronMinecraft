# Survivors’ Village — аудит и утверждённый план

## Исходные материалы и границы

- Обязательный текстовый источник: `concepts/structures/survivor_settlement/survivor_settlement_prompt.md` (1739 строк). Он требует полностью оригинальное, живое, обороняемое поселение, а не набор руин.
- Обязательные изображения: `survivor_settlement_art_1.png` и `survivor_settlemen_art_2.png`. Из первого взяты язык собранной из дерева/металла/бетона обороны, тёплый свет, радиорубка, клиника, мастерская, рынок и убежище; из второго — читаемая сверху нерегулярная ограда, южные ворота, центральный костёр, радиомачта, хозяйственные зоны и спокойный ночной свет. Они задают атмосферу и материалы, а не копируемую планировку.
- Лор `lore/lore.md`: мир пережил войну Haiku; Опус может противостоять Haiku. Поэтому поселение людей должно быть поддерживаемым, бережливым и обороняемым, но не принадлежать машине или копировать известные игровые локации.
- Проверка `skills/`: в проекте есть только руководства по моделям, текстурам, VFX и UI; для NBT-worldgen, готовых ванильных блоков и уже зарегистрированных сущностей применимого skill нет.

## Аудит проекта

| Область | Факт | Решение |
|---|---|---|
| Платформа | Fabric Loader 0.19.3, Minecraft 1.20.1, официальные Mojang mappings, Java 17 | Код пишется под существующий Fabric/Java 17 стек. |
| Текущая структура | `survivor_settlement` — jigsaw, template `91×31×91`, одна NBT-деталь, `spacing 52`; 12 Survivor в entities и 3 старых chest-tables | Полная замена на детерминированный template `121×43×101` и terrain-aware custom `Structure`; id остаётся `opusvsexe:survivor_settlement`. Старый pool сохраняется только для уже созданных jigsaw-чанков. |
| Рабочий пример | K-17 уже использует `Structure` + `TemplateStructurePiece`, проверку поверхности, уклона и поворот template | Новый village использует такой же bounded подход, но с более плотной сеткой высот по всему footprint. |
| Жители | `opusvsexe:survivor` уже зарегистрирован как `MobCategory.CREATURE`, умеет торговать, сохраняется в NBT template | В template будут только persistent Survivor, распределённые по ролям и безопасным точкам. Никаких villager, животных, ninja, samurai или Haiku. |
| Враждебные мобы | Haiku относятся к `MobCategory.MONSTER`; в NBT могут создавать их `dormant_spawner` | В template village нет `dormant_spawner` и нет entity кроме Survivor. `spawn_overrides` запрещает естественные monster/creature/ambient/water-спавны внутри pieces, чтобы гарантировать смысл «только выжившие». |
| Блоки | Есть Opus-блоки, `memory_cable`, `lab_floor_grate`; для обитаемой базы достаточны ванильные дерево, бетон, медь, стекло, железо, sandbag-like stairs/slabs/fences | Новые блоки и текстуры не нужны: палитра строит ремонт из доступного материала, без дублирующих registries. |
| Лут | Старые `survivor_settlement_{cartographer,supplies,armory}` существуют; project convention — loot table на chest NBT | Создаются восемь table из prompt (`house`, `food`, `medical`, `workshop`, `warehouse`, `security`, `shelter`, `hidden`) в src и pack. Старые три сохраняются для сохранённых миров, но новым template не используются. |
| Дороги/terrain helpers | Специализированного settlement road helper нет; custom structures уже используют bounded `getBaseHeight` | Фиксированный road graph и фундаменты авторятся в NBT. Java проверяет 7×7 высотную сетку, минимум высоты, поверхность подъёмов и безопасный west-escape участок, не загружая чанки. |

## Утверждённая архитектура

1. Единый NBT остаётся единственным источником обязательной геометрии: при такой деревне это устраняет разрывы jigsaw-улиц, пропавшие здания и неполный периметр.
2. `SurvivorsVillageStructure` выбирает высоту центра, отвергает перепад более 6 блоков на footprint и опасный подпочвенный уровень, затем ставит шаблон с одной из четырёх rotations. Foundation-column и дороги опускаются до нижней границы шаблона; в пересекаемых зданиях и дорогах template очищает растительность/грунт. Так входы не засыпает, а сооружения не висят над небольшой впадиной.
3. Шаблон имеет локальные границы `X −60…+60`, `Z −50…+50`, `Y 0…42`; земля-эталон — `Y=16`. Убежище лежит `Y=1…13`, а верх радиомачты — `Y=40` (24 блока над грунтом).
4. Постоянные жители помещаются в `entities` template, не в ticking-spawner. Все получают `PersistenceRequired`, стоят на полу с двумя блоками headroom и разделены по точкам — 20 Survivor, что соответствует требуемым 12–24 активным NPC.
5. Реализуются все обязательные зоны, целостный irregular-oval perimeter, две открытые проходимые gate, скрытый postern, shelter и выход за стеной. Животный загон остаётся функциональной инфраструктурой без животных: пользовательское ограничение «только выжившие» приоритетнее рекомендованного animal spawn.

## Рабочий план

1. [x] Прочитать prompt, lore, осмотреть оба concept-art, сделать аудит vanilla/Fabric/NBT/entity/loot/worldgen.
2. [x] Утвердить архитектуру без hostile mobs, размеры, terrain contract и источник resident-спавна.
3. [x] Записать точную координатную карту, дороги, периметр, палитру, роли и validation contract.
4. [x] Реализовать template generator, survivor loot и зеркала pack.
5. [x] Реализовать custom terrain-aware type/piece и сменить current worldgen на него.
6. [x] Проверить template, residents, loot, JSON, source/pack mirror, Gradle и чистый server-world.

## Выполненная проверка

- `python3 scripts/generate_survivor_settlement.py`: `121×43×101`, 184843 явных блока, 60 состояний, 35 контейнеров и ровно 20 persistent Survivor; NBT и новые loot/worldgen mirrors совпадают байт-в-байт.
- `python3 scripts/validate_survivor_settlement.py`: подтверждены все обязательные landmark, routes, восемь тематических loot tables, размеры, shell/escape, 20 безопасных resident points, отсутствие `dormant_spawner`/marker и пустые natural-spawn overrides всех категорий.
- `python3 scripts/validate_kimi_laboratory.py` и `python3 scripts/validate_opus_haiku_encounters.py`: пройдены одновременно с KSV contract.
- `JAVA_HOME=/home/shutniko/.jdks/jdk-17.0.20+8 ./gradlew build --console=plain`: успешно.
- Чистый headless universe: `/locate structure opusvsexe:survivor_settlement` нашёл KSV-01 в `[-1664, ~, 4624]`; полный диапазон её 9×9 чанков был force-loaded без template/placement ошибки, а selector подтвердил хотя бы одного созданного `opusvsexe:survivor`. Сервер штатно остановлен, временные worlds удалены.

## Оставшееся ручное подтверждение

Автоматически проверены rotations на уровне template API и фактическое размещение одной свежей ориентации. Перед визуальным релизом остаётся короткий dev-client обход ворот, shelter stair и west exit на всех четырёх rotations; это визуальный, а не ресурсный блокер.

## Неизменяемые ограничения реализации

- Никаких hostile entity NBT, `dormant_spawner`, trial triggers, invisible markers или jigsaw blocks в новом template.
- Никаких copied names, эмблем, флагов, текстов известных франшиз или реальных карт.
- Primary routes — не уже 4, secondary — не уже 2; все обязательные двери имеют проём `1×2` или больше.
- Главные здания и perimeter обслуживают территорию, а не создают декоративную пустоту: у каждого есть интерьер, свет, доступ и тематический loot.
- Служебный legacy pool и прежние loot tables не являются частью нового worldgen и оставлены только для совместимости уже сохранённых chunk-данных.
