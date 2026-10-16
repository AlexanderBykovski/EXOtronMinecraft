# Survivors’ Village — финальная координатная схема KSV-01

## Система координат и terrain contract

- NBT: `121×43×101`; абсолютные template coordinates получаются как `(localX + 60, localY + 16, localZ + 50)`.
- Локальные оси: `+X` восток, `+Z` юг. Опорный уровень земли/дорог — `Y=16`; фундамент идёт до `Y=0`; максимум радиомачты `Y=40`.
- Java-anchor — центр communal square. Генерация допускается, только если сетка `7×7` с шагом 18 блоков имеет перепад не более 6; поверхности центра, south gate, north gate и west exit также должны укладываться в ±3 от центра. Шаблон не сканирует и не force-loads chunk.
- Ротация `NONE`, `CLOCKWISE_90`, `CLOCKWISE_180`, `COUNTERCLOCKWISE_90`; pivot `(60, 0, 50)`. Block facing, двери, beds, chest facing, stairs и NBT entities поворачиваются vanilla template системой.

## План сверху: обязательные зоны

| Зона | Local bounds / центр | Содержание и доступ |
|---|---|---|
| Main gate | `X −10…+10, Z +43…+50` | 5-wide открытый проезд, две башни, gate court, search booth, sandbag steps, тёплые и красный тревожный свет; дорога ведёт к square. |
| Service gate | `X −6…+6, Z −50…−43` | 3-wide северный проход, компактная площадка, путь к quarantine и command. |
| Postern | `X −60…−56, Z +9…+14` | скрытая западная калитка и узкая тропа за perimeter; не заменяет tunnel exit. |
| Perimeter / towers | irregular oval: `X −59…+59, Z −48…+48` | ломаная смесь spruce palisade, stone rubble, concrete, iron/copper repair panels; башни NE `(+48,−34)`, NW `(-48,−32)`, SE `(+47,+33)`, SW `(-47,+31)`, пятая у north gate. Стены 6 high, внутренний fighting step, нет незапланированных щелей. |
| Communal square | `X −13…+13, Z −13…+13` | 27×27 repaired cobble/gravel, firepit, pump, notice-board без текста, benches, covered meeting corner, 5 primary exits. |
| Command/radio | `X −11…+11, Z −38…−21`; mast `(0,−29)` | двухэтажная command house с coordination, map/radio/battery rooms, roof maintenance platform; mast `Y=17…40`, cable to generator. |
| Clinic | `X +18…+39, Z −10…+9` | triage, ward, exam, wash, storage, isolation; east door и rear service door, medical chest. |
| Market | `X −42…−18, Z −10…+11` | 6 разных canvas/wood stalls с covered aisle, food/tools/fabric/supply/trader points, drainage и lamps. |
| Warehouse | `X −43…−20, Z +17…+35` | receiving, two-block aisles, food/tools shelves, secure room, loft and loading access toward gate. |
| Canteen | `X −10…+11, Z +20…+35` | stoves, serving counter, tables, benches, water and firewood, rear waste route. |
| Workshop | `X +18…+42, Z +16…+35` | forge, workbench, tool wall, repair pit, scrap yard and water barrel; connected but separate from generator. |
| Generator shed | `X +33…+46, Z +30…+42` | fuel/battery/exhaust/cable board on concrete base, fence and maintenance clearance. |
| Residential + barracks | houses across north/east (`−16…+42, −20…−41`) | six visibly distinct houses, barracks A `(+19…+39,−39…−25)`, B `(-38…-19,−39…−25)`, clear entrances on secondary paths. |
| Farm + greenhouse | `X −45…−17, Z −45…−23` | 21×11 repaired greenhouse, 3 irregular fields, seed shed, compost, herb plot, irrigation that ends before roads. |
| Quarantine | `X +19…+31, Z −48…−38` | separated 2-bed hut and fenced wash yard near service gate. |
| Animal/utility + sanitation | pen `X −49…−30, Z +32…+46`; sanitation `X +44…+55, Z +10…+27` | pen/tough/feed shelter is empty by policy; latrines, handwash and enclosed refuse are distant from well, crops, clinic and kitchen. |
| Water | pump `(0,0)`, rain tanks at clinic, kitchen, greenhouse | stone rim/pump/drainage around square; gutters/barrels/pipes follow roofs and poles. |
| Underground shelter | `X −21…+21, Z −15…+16, Y 1…13` | stair + vestibule at `(0,+15)`, communal chamber, bunk room, food/water, medical alcove, ventilation/battery, secure supplies; sealed 2-block shell. |
| Escape tunnel | from `(-20,5,+4)` to west exit `(-59,16,+2)` | 3×3 supported route, upward stepped slope, maintenance alcove, shaft, concealed hatch outside perimeter. |

## Дороги и foundations

- Primary roads: `south gate → square`, `square → north/service`, and five 5-wide arms to command, clinic, market, workshop, residences. Material: coarse dirt, gravel, cobble fragments, packed mud, repaired slabs; gutters never cross floor-height entryways.
- Secondary paths are 2–3 wide and join every house, farm, tower, warehouse, utilities, postern and shelter. No random dead ends except deliberate hidden postern route.
- Для каждой дороги, стены, gate, tower и здания generator emits foundation columns from local `Y=0…15`. Building volume and road heads clear tree/ground collision to local `Y=23`; the validated 6-block terrain envelope therefore cannot leave a door buried or a foundation floating.

## Палитра и визуальный язык

- Structural: spruce/oak logs and planks, stripped spruce, dark oak, stone/cobble/cracked stone bricks, andesite, gray/light gray concrete.
- Repairs: weathered/exposed cut copper, iron bars/trapdoors, chains, brown terracotta, mixed slabs/stairs, muted green/gray wool/carpets.
- Lighting: lanterns and campfire, limited redstone-lamp warning at gate/mast; no redstone clocks and no light spam.
- Industrial detail: `opusvsexe:memory_cable` runs generator → command → clinic → square/workshop; `lab_floor_grate` only workshop pit and drainage. This is salvage infrastructure, not a Haiku facility.

## Residents — only this entity type

The NBT `entities` list contains exactly 20 persistent `opusvsexe:survivor`: leader/radio (2), medic (2), mechanic/cook/storekeeper/trader (4), farm/utility (3), gate/tower/warehouse watch (5), household residents (4). Equipment varies only among safe vanilla/Opus-compatible tools; every point is on a clear floor and distributed through accessible buildings/roads. No animal or hostile entity is authored. JSON spawn-overrides use empty lists for natural monster, creature, ambient and water categories inside the structure pieces.

## Implementation checklist

1. [x] Coordinates, rotation pivot, terrain range, mandatory zones, road graph, foundations and NPC policy fixed.
2. [x] Author reproducible NBT generator and the eight loot tables.
3. [x] Add village custom Structure/Piece/registry and worldgen data; retain legacy jigsaw pool only for old saves.
4. [x] Validate geometry, entities, loot, no-hostile contract, mirrors, JSON, compile and fresh-world placement.

## Реализованный validation contract

- Surface structure-set: `spacing 64`, `separation 24`, `salt 155746213`, triangular. Кодек размещает только на допустимой 7×7 высотной сетке и сохраняет 8 блоков до world minimum Y.
- 35 chest containers с восьмью таблицами: `house`, `food`, `medical`, `workshop`, `warehouse`, `security`, `shelter`, `hidden`.
- В template есть центральный campfire, mast top, clinic bed, greenhouse glass, generator core, quarantine bed, shelter crate и exterior escape hatch; validator проверяет их по конкретным координатам.
- Четыре gate/postern маршрута, square, command, clinic, market, workshop, shelter и exit имеют двухблочную clearance-проверку. Все 20 resident floor/headroom points проверяются до записи NBT.

## Known deliberate trade-off

This release prefers one deterministic authored village over random optional jigsaw houses. It guarantees all required services, perimeter closure, shelter and circulation every time; visual variety is carried by six non-identical houses, wall repair pattern, market stalls and terrain-aware site selection rather than unsafe recursion.
