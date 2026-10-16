# Распределение Haiku-4 / Haiku-5 в Opus-структурах

## Аудит до изменения

По NBT chest-table связаны с Opus следующие active combat locations: K-17 (`kimi_lab/*`), Coddy Workshop (`coddy_workshop/*`), Trial Grounds (`trial_grounds/*`), Data Spire (`data_spire/*`), Abandoned City (`abandoned_city/*`), Frontier Fortress (`frontier_fortress/*`) и Haiku Citadel (`haiku_citadel/*`). Paradise, Moon Fountain и Japanese Settlement имеют самостоятельные loot-линии; Survivor Settlement теперь — зона только людей, поэтому сознательно исключён.

До изменения Fortress уже имела Haiku-4 и Haiku-5, Citadel — Haiku-4; K-17 имела только Haiku-1.5/2. Остальные ранние площадки содержали низшие encounters. Data Spire имеет узкие вертикальные помещения без безопасной authored 4/5-height площадки, поэтому не получает искусственного босса.

## Утверждённая прогрессия

| Структура | Лут-сигнал | Изменение | Причина |
|---|---|---|---|
| K-17 | `reactor`, `archive`, `memory_vault` | +1 Haiku-4 в lower resonator, +1 Haiku-5 в high deep-reactor exhaust bay | ключевая лаборатория Кими и память Опуса; H5 получает реальный 9-block headroom. |
| Coddy Workshop | `coddy`, `armory`, `trophy`, `parts` | +1 Haiku-4 в открытом salvage court | один elite-защитник чертежей, без H5 в T1 workshop. |
| Trial Grounds | `prep_armory`, `reward_vault`, `record_room` | +1 Haiku-4 в reward approach | высокая награда объясняет elite, но не превращает ранний trial в titan arena. |
| Abandoned City | `treasury`, `refinery`, `bunker`, `document` | +1 Haiku-4 у bunker/refinery, +1 Haiku-5 в открытом treasury court | крупная ruined Opus-инфраструктура уже имеет нужный безопасный объём. |
| Haiku Citadel | `approach`, `gallery`, `nave`, `core`, `postboss` | +1 Haiku-5 у core route; существующие H4 остаются | финальная Haiku-локация получает titan, не дублируя Omega altar. |
| Frontier Fortress | `keep_armory`, `command`, `reactor` | без изменения | в её текущем template уже есть оба типа. |

Все новые elite/titan spawners имеют `max_nearby=1` и fixed safe center (`spawn_radius=0`), чтобы один marker не бесконечно создавал четырёх боссов и не помещал большую hitbox в стену. Базовый `DormantSpawnerBlockEntity` проверяется на collision и повторяет попытку в следующий интервал, вместо принудительного спавна в блоке.

## План

1. [x] Инвентаризировать NBT, существующие spawner и loot tables; отсеять не-Opus линии и поселение людей.
2. [x] Добавить collision-safe limit/radius к dormant spawner.
3. [x] Изменить K-17 generator и resource validator.
4. [x] Воспроизводимо дополнить выбранные NBT source+pack и проверить зеркала/свободный объём.

## Результат проверки

- K-17 теперь содержит 10 encounter markers, включая ровно по одному Haiku-4 и Haiku-5; `validate_kimi_laboratory.py` подтверждает headroom и single-boss NBT.
- `validate_opus_haiku_encounters.py` подтвердил пять дополнений в Coddy Workshop, Trial Grounds, Abandoned City и Haiku Citadel, включая 5/9-block authored clearance; source/pack NBT совпадают.
- `DormantSpawnerBlockEntity` теперь ставит моба над marker, проверяет collision, поддерживает ограниченные `max_nearby`/`spawn_radius` и не создаёт titan в стене. Старые NBT без новых полей остаются совместимы с прежними default-значениями.
