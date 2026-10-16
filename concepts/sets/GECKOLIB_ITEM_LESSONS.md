# GeckoLib-предметы: выученные ошибки (читать ПЕРЕД каждым новым оружием)

Проект: Fabric 1.20.1 + GeckoLib 4.4.9 + split source sets (src/main + src/client).
Нарушение любого пункта уже роняло игру минимум один раз.

## M1. Per-face UV — только под ключом `"uv"` (geo)
Десериализатор кубов GeckoLib читает ТОЛЬКО `"uv"`. В per-face режиме это ОБЪЕКТ:
`"uv": {"north": {"uv": [x1,y1,x2,y2], "uv_size": [w,h]}, ...}`.
Ключ `"faces"` молча игнорируется → `uvUnion == null` → NPE `UVUnion.isBoxUV()`
→ краш перезагрузки ресурсов → краш входа в мир. `uv_size` обязателен тоже.

## M2. Предмет — plain `GeoAnimatable`, НЕ `GeoItem`
Fabric-миксин `MixinItemRenderer.itemModelHook` вызывает
`RenderProvider.of(stack).getCustomRenderer()` для КАЖДОГО рендера; `of()` для
`GeoItem` возвращает `getRenderProvider().get()`. Провайдера не может
существовать при split-раскладе (рендерер в src/client, предмет в src/main) →
NPE в хотбаре. Правильно (прецедент DemonicTridentItem): plain `GeoAnimatable` +
ванильный путь `builtin/entity` + `BuiltinItemRendererRegistry`.

## M3. У `GeoItem` два абстрактных метода
`createRenderer(Consumer)` + `getRenderProvider()` (через SingletonGeoAnimatable).
Заглушка `() -> null` компилируется, но падает по M2. Не implement'ить GeoItem.

## M4. Триггеры вместо провайдера
`SingletonGeoAnimatable.triggerAnim` недоступен без GeoItem. Маршрутизация
вручную (`fireTrigger`): клиент — прямой `manager.tryTriggerAnimation`,
сервер — `GeckoLibNetwork.sendToTrackingEntityAndSelf(new AnimTriggerPacket(
getClass().toString(), id, controller, anim), player)`. Конструктор:
`GeckoLibNetwork.registerSyncedAnimatable(this)`. ID стаков:
статические `GeoItem.getOrAssignId(stack, ServerLevel)` (сервер, в
inventoryTick) / `GeoItem.getId(stack)`. Повторный триггер той же анимации —
no-op (проверено по исходникам AnimationController), снапа нет.

## M5. Состояние триггеров — строго per-perspective
GUI/хотбар рисуют ТЕ ЖЕ объекты ItemStack, что и рука, каждый кадр.
Любая мутация first-person стейта из GUI-рендера = equip/атака каждый кадр
(вечное качание). GUI-рендеры не трогают стейт; повторный выбор того же стака —
по индексу слота хотбара.

## M6. Idle — статичный холд
Оружие в руке не дрейфует/не качается. Единственная жизнь — микропульс
самоцветов scale ~1.03 на отдельном fx-контроллере (без смещения).
Движение только по действию: ЛКМ / ПКМ / equip.

## M7. Display-трансформы: ванильный handheld — для диагональных спрайтов
Углы `[0,∓90,55]` кладут ВЕРТИКАЛЬНУЮ 3D-модель диагональю 55°. Вертикальным
моделям: третье лицо `[0,∓90,12]`, первое `[0,∓90,25]` (топорный feel),
GUI ~0.45, ground ~0.4. Проверять по скриншотам игрока.

## M8. Единый источник правды — генератор
geo + текстура + анимации из одной таблицы костей (имена не расходятся).
После генерации: программная сверка кости(anim)⊆кости(geo), UV в границах,
имена анимаций Java↔JSON.

## M9. Харнес реального загрузчика — обязателен
`/tmp/labrys_test/LabrysLoadTest` (держать!): настоящий `GEO_GSON` +
`BakedModelFactory.constructGeoModel` + `BakedAnimationsAdapter` по новым
ассетам + негативный контроль (ломаный куб обязан дать ТОТ ЖЕ NPE, что в игре).

## M10. JDK и порядок проверок
JDK: `~/.jdks/jdk-17.0.20+8`, всегда `export JAVA_HOME...`. Порядок:
`compileJava` → `compileClientJava` → правки → `build` → validator →
харнес → отчёт. Никогда не заявлять «JDK нет», не проверив `~/.jdks`.
Клиент из build-shell не стартует (нет DISPLAY) — только init-проверка по логу;
мир/рука — глазами пользователя по скринам.

## M11. Сохранение ID и поведения
Registry-ID, рецепт, ачивки, ланги, креатив-таб не трогать. Новый класс встаёт
1:1 на старый (те же Tier/урон/скорость/тултип/intrinsic). Старый спрайт —
в бэкап и удалить; whitelist-генератор спрайтов (`generate_tool_sets.py`)
почистить от ID, иначе перегенерация затрет 3D-ассеты.
