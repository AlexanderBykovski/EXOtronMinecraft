You are implementing a complete large modular structure for an existing Minecraft Fabric 1.20.1 mod.

Follow every applicable instruction from the `skills/` directory.

Read and strictly follow the project lore from `lore.md`.

Save every concept, plan, coordinate, structure-piece description, palette, implementation decision, TODO item, validation result, and unresolved question inside the `concepts/` directory.

Do not rely on image understanding. The complete design is described textually below.

Do not stop after research or planning. After inspecting the project and recording the plan, implement the complete settlement, world generation, modular buildings, roads, defensive perimeter, residents, loot integration, and validation.

# PRIMARY OBJECTIVE

Create a complete original fortified settlement called the Survivors’ Village.

Suggested registry identifier:

- `survivors_village`

Use another identifier only if required by the project’s naming conventions.

The settlement belongs to a dangerous post-catastrophe world.

It is not an abandoned ruin. It is a functioning, inhabited community created by survivors from:

- Abandoned rural houses.
- Salvaged timber.
- Corrugated sheet metal.
- Concrete fragments.
- Sandbags.
- Industrial equipment.
- Repaired glass.
- Canvas.
- Old electrical equipment.
- Repurposed storage containers.
- Agricultural materials.

The settlement must appear:

- Inhabited.
- Defensible.
- Improvised.
- Organized.
- Resource-conscious.
- Tense but hopeful.
- Repaired rather than clean.
- Built gradually over several years.

# ORIGINALITY REQUIREMENT

Create the complete location from scratch.

Do not copy:

- Rookie Village.
- Skadovsk.
- Rostok.
- Yanov Station.
- Any S.T.A.L.K.E.R. settlement.
- Fallout settlements.
- Metro settlements.
- The Walking Dead settlements.
- Existing Minecraft villages.
- Downloaded structure packs.
- Marketplace maps.
- Other mods.

Do not use copyrighted:

- Faction emblems.
- Settlement names.
- Signs.
- Flags.
- Logos.
- Graffiti.
- Map layouts.

The broad post-catastrophe survival theme is allowed, but the final settlement must have an original layout and architectural identity.

# TARGET EXPERIENCE

The Survivors’ Village must feel like a real community rather than a collection of random houses.

The player must be able to understand:

- How residents enter and leave.
- How the village is defended.
- Where food is produced.
- Where water is obtained.
- Where sick people are treated.
- Where tools are repaired.
- Where supplies are stored.
- Where residents sleep.
- Where leaders coordinate the settlement.
- Where traders work.
- Where people gather.
- Where residents hide during an attack.
- How waste is handled.
- How the village can be evacuated.

The village should support approximately:

- 20–35 residents visually.
- 12–24 active NPCs depending on performance and existing entity systems.
- 25–40 minutes of initial exploration.
- Repeated visits without becoming inconvenient to navigate.

# PROJECT AUDIT

Before implementation, inspect:

1. Fabric Loader version.
2. Yarn mappings version.
3. Java version.
4. Existing structure registration.
5. Existing jigsaw implementation.
6. Existing NBT structures.
7. Existing procedural structures.
8. Existing village or road-generation helpers.
9. Existing custom blocks.
10. Existing survivor or NPC entities.
11. Existing professions.
12. Existing trade systems.
13. Existing loot tables.
14. Existing factions or reputation systems.
15. Existing biome tags.
16. Existing structure sets.
17. Existing processors.
18. Existing data generation.
19. Existing sounds and ambience.
20. Existing furniture blocks.
21. Existing electrical or generator blocks.
22. Existing quest or interaction systems.

Record findings inside:

- `concepts/survivors_village_audit.md`

Do not stop after the audit.

# RECOMMENDED IMPLEMENTATION ARCHITECTURE

Use the project’s existing world-generation architecture when suitable.

Preferred approach:

- Hybrid modular settlement.
- Deterministic critical core.
- Jigsaw or weighted variants for buildings.
- Procedurally generated or modular defensive perimeter.
- Terrain-aware roads.
- Fixed mandatory functional zones.
- Weighted optional decoration.
- Terrain-adapted foundations.

The following components must be guaranteed:

- Main gate.
- Secondary service gate.
- Defensive wall.
- At least four watchtowers.
- Central square.
- Command and radio building.
- Clinic.
- Workshop.
- Generator shed.
- Market.
- Warehouse.
- Communal kitchen.
- At least one barracks.
- Multiple houses.
- Water source.
- Food-production area.
- Underground shelter.
- Emergency exit.
- Road connection between all mandatory areas.

Optional structures may vary.

# SETTLEMENT SIZE

Recommended complete maximum footprint:

- Width: approximately 121 blocks.
- Length: approximately 101 blocks.
- Maximum normal building height: 12 blocks.
- Radio mast height: approximately 18–24 blocks.
- Underground shelter depth: approximately 10–16 blocks.

Target local bounds:

- X: −60 to +60.
- Z: −50 to +50.
- Surface variation: preferably no more than 10 blocks across the central build area.

The outer perimeter should form an irregular oval rather than a perfect square.

Approximate interior radii:

- East–west radius: 54 blocks.
- North–south radius: 44 blocks.

Use the center of the communal square as local origin:

- X = 0.
- Z = 0.
- Y = terrain-adjusted settlement reference height.

Document all final coordinates inside:

- `concepts/survivors_village_layout.md`

# ORIENTATION

Define:

- Positive X = east.
- Negative X = west.
- Positive Z = south.
- Negative Z = north.

Preferred placement:

- Main gate: south.
- Service gate: north.
- Emergency postern: west.
- Farms and greenhouse: northwest.
- Workshop and generator: southeast.
- Clinic: east.
- Warehouse: southwest.
- Command house: north of central square.
- Residential zone: north and northeast.
- Market: west of central square.
- Animal pen: southwest or western edge.
- Quarantine hut: near the northern service gate but separated from housing.
- Waste area: outside or near the downwind edge.
- Shelter entrance: close to the center but not directly inside the command house.

Support structure rotation if reliable.

Every road, gate, building orientation, escape tunnel, and marker must rotate consistently.

# WORLD-GENERATION CONDITIONS

Generate in the Overworld unless the lore defines a different dimension.

Preferred biomes:

- Plains.
- Forest.
- Birch forest.
- Taiga.
- Sparse woodland.
- Meadow.
- Mod-specific temperate wasteland biomes.

Avoid:

- Oceans.
- Deep oceans.
- Rivers through the central square.
- Beaches.
- Tiny islands.
- Dense jungle unless a dedicated variant is implemented.
- Deserts unless a dedicated palette variant is implemented.
- Ice spikes.
- Extremely steep mountain peaks.
- Terrain with excessive vertical variation.
- Locations where the shelter would cross the world minimum Y.

Before generation, validate:

- Sufficient mostly continuous terrain.
- Acceptable average slope.
- No large lake inside the footprint.
- No ravine cutting through the mandatory core.
- No excessive terrain removal.
- Valid shelter depth.
- Valid emergency-exit destination.
- All required pieces fit inside the structure bounds.

Do not force-load chunks.

Do not perform unbounded terrain scans.

# RARITY

The village should be uncommon but discoverable.

Suggested starting structure-set values:

- Spacing: 56–72 chunks.
- Separation: 18–28 chunks.
- Unique salt not used elsewhere.

Adjust according to the existing project’s structure density.

If the settlement is a major progression location, use the project’s established placement or quest system instead of uncontrolled random generation.

# TERRAIN ADAPTATION

The village must follow terrain without producing floating or buried buildings.

Calculate:

- Central reference height.
- Height under every mandatory building.
- Height under gates.
- Height along the main road.
- Height around the perimeter.

Use these rules:

- Central square variation: ideally no more than 2 blocks.
- Main-building foundation correction: up to 4 blocks.
- Secondary house correction: up to 5 blocks.
- Perimeter may step gradually.
- Road slope: preferably no steeper than one block vertically per two horizontal blocks.
- Stairs or slabs must be used at controlled height changes.
- Never create vertical road cliffs.
- Never bury doors.
- Never leave foundations floating.

Foundation styles:

- Stone rubble foundation.
- Timber stilts for small uneven sections.
- Retaining walls.
- Filled packed-earth base.
- Concrete footing under industrial buildings.

Reject generation if correction would require destroying an unreasonable amount of terrain.

# VEGETATION HANDLING

Inside the settlement footprint:

- Remove trees intersecting buildings, roads, walls, or fields.
- Preserve selected trees in intentional courtyards.
- Remove floating leaves.
- Remove trunks passing through roofs.
- Preserve surrounding forest to conceal and frame the settlement.
- Add stumps near cleared areas.
- Add stacked firewood near homes and workshop.
- Avoid clearing a perfect circular boundary.

Do not modify vegetation far outside the structure bounds.

# MASTER LAYOUT

The settlement contains these zones:

1. Southern main gate.
2. Main approach road.
3. Central communal square.
4. Command and communications zone.
5. Market and warehouse zone.
6. Medical zone.
7. Workshop and power zone.
8. Residential zone.
9. Food-production zone.
10. Animal and utility zone.
11. Quarantine zone.
12. Defensive perimeter.
13. Underground shelter.
14. Emergency evacuation route.

Every zone must connect to the road network.

# ROAD NETWORK

Create a clear hierarchical road system.

Primary roads:

- Main gate to central square.
- Central square to command building.
- Central square to workshop.
- Central square to clinic.
- Central square to market.
- Central square to residential zone.
- Central square to service gate.

Primary width:

- 5 blocks where possible.
- Minimum 4 blocks at narrow points.

Secondary paths:

- 2–3 blocks wide.
- Connect houses, farms, towers, storage and utility areas.

Road materials:

- Coarse dirt.
- Packed mud if available.
- Gravel.
- Cobblestone fragments.
- Stone slabs.
- Repaired paving near central square.
- Wooden walkways over wet ground.

Road details:

- Drainage channels.
- Wheel ruts.
- Repaired sections.
- Muddy edges.
- Small puddles.
- Stepping slabs.
- Directional visual cues.

Do not use a random maze of paths.

Do not place decoration in the center of mandatory walkways.

# DEFENSIVE PERIMETER

Construct an irregular fortified wall around the village.

The wall must look gradually assembled from available materials.

Use a controlled mixture of:

- Vertical logs.
- Stripped logs.
- Heavy planks.
- Corrugated metal.
- Cracked concrete sections.
- Stone rubble.
- Sandbags.
- Iron bars.
- Chains.
- Existing project wire or barricade blocks.
- Earth berms.

Recommended wall dimensions:

- Total height: 5–7 blocks.
- Minimum solid lower section: 3 blocks.
- Internal fighting step or walkway: 1–2 blocks wide where practical.
- Foundation depth: 1–3 blocks depending on terrain.

Wall variation:

- Timber palisade segments.
- Patched sheet-metal segments.
- Concrete checkpoint segments.
- Reinforced corner sections.
- Repair scaffolding.
- Small observation slits.
- Exterior obstacle fields.

The wall must not become:

- A perfect castle wall.
- A uniform medieval palisade.
- A modern military fortress.
- A solid concrete megabase.

# OUTER OBSTACLES

Add restrained defensive obstacles outside selected wall sections:

- Wooden stakes.
- Czech-hedgehog-like block constructions.
- Sandbag positions.
- Ditches.
- Rubble.
- Wire-like fences if the mod provides them.
- Warning markers without readable copyrighted text.

Do not completely prevent ordinary player access.

The main gate must remain the obvious intended entrance.

# MAIN GATE

Recommended total module:

- Width: 17–21 blocks.
- Depth: 9–13 blocks.
- Tower height: 10–13 blocks.
- Clear gate opening: 5 blocks wide and 4–5 blocks high.

Required features:

- Two reinforced gate towers.
- Main double gate.
- Search booth.
- Sandbag positions.
- Elevated guard platforms.
- Interior gate courtyard.
- Exterior approach barriers.
- Warm lamps.
- Emergency red lamp.
- Small storage alcove.
- Defensive firing steps.
- Road passing cleanly through the center.

The gate must be functional visually.

Do not create doors that cannot open unless they are permanently shown open.

If the project has a large-door system, use it.

Otherwise build a believable permanently open or simple vanilla-compatible gate.

# SECONDARY SERVICE GATE

Recommended dimensions:

- Width: 9–13 blocks.
- Clear opening: 3 blocks.
- One compact guard platform.
- Vehicle or cart access.
- Nearby quarantine route.
- Reinforced internal bar.
- Less decorative than the main gate.

# EMERGENCY POSTERN

Create one narrow concealed pedestrian exit.

Requirements:

- Located on west or northwest wall.
- 1–2 block-wide opening.
- Hidden behind storage, vegetation, or a small utility structure.
- Connected to a narrow internal path.
- Connected to an external escape trail.
- Does not replace the underground shelter exit.

# WATCHTOWERS

Create at least four towers.

Suggested positions:

- Southeast perimeter.
- Southwest perimeter.
- Northeast perimeter.
- Northwest perimeter.

Possible fifth tower:

- Near service gate or radio side.

Recommended dimensions:

- Base: 7×7 blocks.
- Platform height: 8–10 blocks.
- Total height: 11–14 blocks.
- Usable ladder or stairs.
- Roof or partial cover.
- Sandbag parapet.
- Warm lamp.
- Observation openings.
- Small supply crate.
- Clear view above the wall.

Every tower must:

- Reach the terrain correctly.
- Avoid floating supports.
- Provide safe player access.
- Have railings.
- Connect visually to the wall.

# CENTRAL COMMUNAL SQUARE

Recommended size:

- Approximately 25×25 blocks.

Required features:

- Repaired stone and gravel paving.
- Communal bonfire or firepit.
- Stone or metal fire surround.
- Benches.
- Water pump or well access.
- Notice-board shape with abstract papers.
- Central lamp posts.
- Gathering area.
- Small covered meeting corner.
- Road connections in at least five directions.
- Drainage.
- Crates or supply distribution point.
- Enough clear space for NPC movement.

Keep at least:

- 3 blocks of clearance around the fire.
- 4–5-block-wide primary routes through the square.

Do not use readable text on the notice board unless the project has its own document system.

# COMMAND AND RADIO HOUSE

Suggested position:

- North of central square.
- Approximately X −10 to +10.
- Z −30 to −14.

Recommended footprint:

- 21×15 blocks.
- Two floors.
- Height: 10–12 blocks excluding antenna.

Ground floor:

- Entry checkpoint.
- Coordination room.
- Map table.
- Storage.
- Small weapon locker if lore-compatible.
- Leader’s office.
- Radio-equipment room.
- Rear emergency exit.

Upper floor:

- Observation room.
- Radio desk.
- Battery storage.
- Signal equipment.
- Small sleeping room for duty staff.
- Roof access.

Roof:

- Radio mast.
- Antennas.
- Cables.
- Lightning protection.
- Signal lamp.
- Maintenance platform.

Use abstract maps and papers. Do not copy real maps or faction symbols.

# RADIO MAST

Recommended height:

- 18–24 blocks above local terrain.

Construction:

- Narrow lattice-like support.
- Cross braces.
- Multiple antenna shapes.
- Cable connection to command house.
- Red warning light at top.
- Stable foundation.
- Ladder only if safe and intended.

Do not create a modern cellular tower.

Do not place hundreds of fences causing rendering problems.

# CLINIC

Suggested position:

- East of central square.

Recommended footprint:

- 19×15 blocks.
- One floor.
- Optional small attic storage.

Required rooms:

1. Reception and triage.
2. Three-bed ward.
3. Examination room.
4. Medicine storage.
5. Wash area.
6. Herb and drying shelf.
7. Small isolation room.
8. Rear service entrance.

Required details:

- Beds.
- Privacy dividers.
- Cabinets.
- Sink or washbasin.
- Water container.
- Shelves.
- Worktable.
- Warm clean lighting.
- Patched but more hygienic walls.
- Medical loot container.
- Clear NPC path.

Do not include graphic gore.

# QUARANTINE HUT

Place near the northern service gate and away from central housing.

Recommended footprint:

- 11×9 blocks.
- Small fenced yard.
- Two beds.
- Observation window.
- Wash station.
- Separate storage.
- Exterior warning light.
- Controlled road connection.

Do not use real biohazard logos unless the project has an original symbol system.

# WORKSHOP

Suggested position:

- Southeast quadrant.

Recommended footprint:

- 21×17 blocks.
- Height: 7–9 blocks.

Required areas:

- Main workbench.
- Forge or furnace corner.
- Tool wall.
- Spare-parts shelves.
- Metalworking table.
- Woodworking table.
- Repair pit or floor grate.
- Ventilation hood.
- Material storage.
- Rear scrap yard.
- Fire-safety water barrel.
- Workshop loot container.

The workshop must appear used but organized.

# GENERATOR SHED

Place directly beside or behind the workshop.

Recommended footprint:

- 13×11 blocks.

Include:

- One or two generator assemblies.
- Fuel storage.
- Battery bank.
- Exhaust pipe.
- Ventilation.
- Cable distribution board.
- Protected maintenance clearance.
- Concrete or stone foundation.
- Fence separating it from the public road.
- Fire-resistant wall behind exhaust.

Do not create a constantly ticking redstone clock.

Lighting can be static unless an existing power system supports state changes.

# POWER DISTRIBUTION

Show cables running from the generator area toward:

- Command house.
- Clinic.
- Central square.
- Workshop.
- Market.
- Selected residential buildings.
- Gate lamps.

Cable routes must:

- Follow poles.
- Follow walls.
- Cross roads above player height.
- Terminate at plausible buildings.
- Avoid random disconnected cable pieces.

Use existing project cable blocks if available.

# MARKET

Suggested position:

- West of central square.

Recommended area:

- 23×17 blocks.

Include:

- Four to seven patched canvas stalls.
- Food stall.
- Tools and parts stall.
- Clothing or fabric stall.
- General supply stall.
- Secure trader booth.
- Storage crates.
- Weighing table.
- Covered central walkway.
- Rain drainage.
- Warm lamps.

Maintain clear movement between stalls.

# WAREHOUSE

Suggested position:

- Southwest quadrant near market and main gate.

Recommended footprint:

- 23×17 blocks.
- Height: 8 blocks.

Required zones:

- Receiving area.
- Food storage.
- Tool storage.
- Locked secure room.
- Shelving aisles.
- Loading door.
- Inventory desk.
- Rear service entrance.
- Small loft or upper storage.
- Guarded rare-loot container if appropriate.

Aisles must be at least 2 blocks wide.

# COMMUNAL KITCHEN AND CANTEEN

Recommended footprint:

- 19×15 blocks.

Include:

- Cooking stoves.
- Preparation tables.
- Water storage.
- Food shelves.
- Serving counter.
- Dining tables.
- Benches.
- Chimney.
- Firewood storage.
- Rear waste exit.
- Warm lighting.
- Accessible main entrance.

Do not place the kitchen directly beside latrines, quarantine, or fuel storage.

# BARRACKS

Create at least two barracks variants.

Barracks A:

- Footprint: 19×13.
- 8–12 beds.
- Central stove.
- Personal lockers.
- Weapon or equipment rack if appropriate.
- Drying clothes.
- Small table.
- Rear window.

Barracks B:

- Footprint: 17×13.
- 6–10 beds.
- Slightly different roof.
- Side storage room.
- Exterior covered porch.

Beds and furniture must not block the central aisle.

# FAMILY HOUSES

Generate approximately six houses selected from at least four variants.

Suggested variants:

1. Small timber cottage: 11×9.
2. Patched plaster house: 13×11.
3. Salvaged-metal extension house: 15×11.
4. Two-family house: 17×13.
5. Raised-foundation house for uneven terrain: 11×11.
6. Damaged but repaired rural house: 13×13.

Every house should contain:

- Entrance.
- Stove or safe heat source.
- Sleeping area.
- Table.
- Storage.
- Window.
- Light.
- Personal clutter.
- Clear walking space.

Some may contain:

- Tiny garden.
- Covered porch.
- Firewood stack.
- Water barrel.
- Tool bench.
- Clothesline.

Do not duplicate the exact same furniture arrangement.

# FOOD PRODUCTION

Northwestern agricultural zone must include:

- Greenhouse.
- Fenced vegetable fields.
- Compost area.
- Tool shed.
- Water barrels.
- Irrigation channels where practical.
- Seed storage.
- Small herb plot.

# GREENHOUSE

Recommended footprint:

- 21×11 blocks.
- Height: 6 blocks.

Construction:

- Repaired glass.
- Timber or metal frame.
- Several patched opaque roof sections.
- Central 3-block-wide path.
- Crop beds on both sides.
- Water supply.
- Tool chest.
- Warm lamps only if supported.
- Ventilation panels.

Do not create perfect modern glass architecture.

# VEGETABLE FIELDS

Create several irregular plots.

Possible crops:

- Wheat.
- Carrots.
- Potatoes.
- Beetroot.
- Existing mod crops.

Use existing project crop balance.

Requirements:

- Fences.
- Paths.
- Water access.
- Compost.
- Scarecrow-like original structure if appropriate.
- No farmland under buildings.
- No water flowing into roads.

# WATER SYSTEM

Provide at least two reliable-looking water sources:

1. Central deep well or pump.
2. Rainwater collection system.

Optional:

- Elevated storage tank.
- Purification shed.
- Backup barrels.

The well must include:

- Stone or concrete rim.
- Pump or winch.
- Drainage.
- Bucket area.
- Safe barrier.

Rainwater system:

- Roof gutters represented visually.
- Storage barrels or tanks.
- Pipes into clinic, kitchen or greenhouse.
- Overflow drainage.

Do not create random water sources inside houses.

# ANIMAL PEN

Recommended area:

- 17×15 blocks.

Include:

- Strong fence.
- Small shelter.
- Water trough.
- Feed storage.
- Double gate.
- Drainage.
- Clear separation from crop fields.

Only spawn animals if the project permits it and performance remains acceptable.

# SANITATION AND WASTE

Place latrines and waste area near the settlement edge, away from:

- Well.
- Kitchen.
- Clinic.
- Residential center.
- Crops.

Create:

- Two or three latrine stalls.
- Handwashing barrel.
- Small drainage trench.
- Ash or waste pit.
- Enclosed refuse area.
- Compost separated from dangerous waste.

Keep the implementation non-graphic.

# UNDERGROUND SHELTER

Create a reinforced storm and attack shelter beneath or near the central settlement.

Recommended entrance:

- Concrete stairwell or heavy hatch near the central square.
- Not directly inside the command building.
- Protected by sandbags and reinforced walls.

Recommended shelter bounds:

- Width: 35–43 blocks.
- Length: 25–31 blocks.
- Depth: 10–16 blocks below terrain.
- Ceiling height: 4–6 blocks.

Required rooms:

1. Entrance stairwell.
2. Airlock-like security vestibule.
3. Main communal shelter.
4. Bunk room.
5. Food storage.
6. Water storage.
7. Medical alcove.
8. Ventilation room.
9. Generator or battery room.
10. Secure emergency supplies.
11. Escape-tunnel entrance.

The shelter must remain separate from natural caves unless a controlled breach is intentionally designed.

# SHELTER CONSTRUCTION

Use:

- Reinforced concrete.
- Stone.
- Iron doors.
- Heavy supports.
- Pipes.
- Ventilation ducts.
- Warm emergency lighting.
- Storage racks.
- Bunk beds.
- Drainage.

External shell thickness:

- 2–3 blocks.

Prevent:

- Surface water leakage.
- Cave flooding.
- Exposed rooms.
- Dead-end mandatory route.
- Escape tunnel being cut off by terrain.

# ESCAPE TUNNEL

Create an underground escape route from the shelter.

Recommended:

- Width: 3 blocks.
- Height: 3 blocks.
- Length: 45–75 blocks.
- Slight upward slope.
- Occasional support beams.
- One maintenance alcove.
- One ventilation shaft.
- One concealed exterior exit beyond the perimeter.

Possible exterior exit:

- Small concrete hatch.
- Drainage outlet.
- Collapsed utility shed.
- Root-covered bunker door.

Validate destination terrain before placement.

# BUILDING MATERIAL PALETTE

Audit existing mod blocks first.

Preferred materials:

Wood:

- Spruce logs.
- Stripped spruce logs.
- Dark oak.
- Oak.
- Weathered custom planks if present.
- Trapdoors.
- Fences.
- Slabs.
- Stairs.

Concrete and masonry:

- Stone bricks.
- Cracked stone bricks.
- Mossy stone bricks.
- Cobblestone.
- Andesite.
- Polished andesite.
- Gray concrete.
- Light gray concrete.
- Bricks.
- Mud bricks where appropriate.

Metal:

- Iron blocks.
- Iron bars.
- Iron trapdoors.
- Chains.
- Cut copper.
- Exposed copper.
- Weathered copper.
- Brown terracotta.
- Existing rusted-metal blocks.

Fabric:

- Wool.
- Carpets.
- Existing canvas blocks.
- Muted banners without copyrighted symbols.

Defensive:

- Logs.
- Sand-colored blocks.
- Walls.
- Fences.
- Chains.
- Existing sandbag and wire blocks.

Roads:

- Coarse dirt.
- Gravel.
- Cobblestone.
- Packed mud.
- Stone slabs.
- Path blocks.

# CUSTOM BLOCK POLICY

Do not create duplicate blocks already present in the project.

Only add a custom block when:

- It is required repeatedly.
- It has a clear functional or visual purpose.
- Vanilla blocks cannot represent it adequately.
- It can be fully textured, registered and tested.

Possible reusable additions:

- Corrugated rusted metal panel.
- Sandbag block and corner.
- Reinforced survivor wall.
- Patched window.
- Canvas awning.
- Warm industrial lantern.
- Cable segment.
- Radio console.
- Water tank.
- Generator casing.
- Notice board.

Directional blocks must support correct rotation and mirroring.

# MODULAR PIECE SYSTEM

Recommended mandatory pieces:

- `village_core_square`
- `main_gate`
- `service_gate`
- `watchtower`
- `wall_timber`
- `wall_metal`
- `wall_concrete`
- `wall_corner`
- `command_house`
- `clinic`
- `workshop`
- `generator_shed`
- `market`
- `warehouse`
- `canteen`
- `barracks_a`
- `barracks_b`
- `greenhouse`
- `quarantine_hut`
- `shelter_entrance`
- `shelter_core`
- `escape_tunnel`
- `escape_exit`

Weighted house pools:

- Small house: weight 4.
- Medium house: weight 4.
- Two-family house: weight 2.
- Raised house: weight 2.
- Repaired damaged house: weight 2.

Decorative lot pools:

- Firewood lot.
- Water-barrel lot.
- Small garden.
- Scrap pile.
- Empty reserve lot.
- Covered storage.
- Clothesline yard.
- Livestock utility lot.

# JIGSAW RULES

If using jigsaw:

- Critical structures must use guaranteed connectors.
- Optional lots may use weighted pools.
- Roads must terminate correctly.
- No jigsaw block may remain visible.
- No connector may open directly into a wall.
- Building entrances must face roads.
- Towers must face outward.
- Gate pieces must align with approach roads.
- Shelter pieces must use rigid underground projection.
- Surface paths may use terrain matching.
- Buildings must use appropriate foundation handling.

Set a strict maximum depth.

Do not allow recursive road expansion beyond settlement bounds.

# PROCEDURAL PERIMETER

If the perimeter is generated procedurally:

1. Build a deterministic irregular oval polygon or stepped ellipse.
2. Reserve gate openings.
3. Reserve tower foundations.
4. Sample terrain height along the wall.
5. Limit vertical changes per segment.
6. Add retaining supports.
7. Select weighted wall variants.
8. Connect internal fighting steps where practical.
9. Verify closure of the complete perimeter.
10. Ensure no unintended gaps larger than one block remain.

Do not generate the wall as a perfect circle.

# STRUCTURE MARKERS

If using markers, define and document:

- `resident_spawn`
- `guard_spawn`
- `medic_spawn`
- `trader_spawn`
- `mechanic_spawn`
- `farmer_spawn`
- `animal_spawn`
- `loot_common`
- `loot_food`
- `loot_medical`
- `loot_tools`
- `loot_security`
- `loot_rare`
- `light_warm`
- `light_emergency`
- `road_connector`
- `wall_connector`
- `shelter_connector`
- `escape_connector`

Process all markers safely.

Remove all marker blocks.

Log unknown markers during development.

# RESIDENT INTEGRATION

Inspect existing NPC systems.

Preferred order:

1. Existing survivor NPC entities.
2. Existing faction NPCs.
3. Existing configurable human entities.
4. Vanilla villagers only if they fit the lore.
5. Static empty village if no suitable system exists.

Do not create a new complex human AI framework solely for this structure.

Suggested roles:

- Village leader.
- Two to four guards.
- Medic.
- Mechanic.
- Radio operator.
- Trader.
- Cook.
- Two farmers.
- Storekeeper.
- General survivors.

Spawn limits must be configurable.

Do not spawn all NPCs in one room.

Validate:

- Valid ground.
- Headroom.
- Door access.
- Navigation.
- Persistence.
- Chunk reload.
- Multiplayer synchronization.
- No suffocation inside furniture.

# GUARD POSITIONS

Suggested guard locations:

- Main gate.
- Service gate.
- Two active watchtowers.
- Central square patrol.
- Warehouse or command house.

Do not fill every tower permanently if performance is limited.

# NPC NAVIGATION

Maintain:

- Doors at least one block wide and two blocks high.
- Main roads at least four blocks wide.
- Secondary paths at least two blocks wide.
- No carpets or trapdoors causing repeated navigation failure.
- No unavoidable one-block drops.
- No fence traps.
- No unreachable beds.
- No unreachable workstations.
- No blocked stairs.

# LOOT TABLES

Create thematic loot tables following project conventions:

- `chests/survivors_village_house`
- `chests/survivors_village_food`
- `chests/survivors_village_medical`
- `chests/survivors_village_workshop`
- `chests/survivors_village_warehouse`
- `chests/survivors_village_security`
- `chests/survivors_village_shelter`
- `chests/survivors_village_hidden`

Do not place overpowered guaranteed loot.

Public containers should contain low-value supplies.

Secure containers may contain better resources.

Do not make villagers’ essential food storage completely lootable if the project has settlement-protection mechanics.

# LIGHTING

Daytime:

- Settlement remains naturally lit.
- Interiors use restrained lamps.
- Workshops have brighter task lighting.
- Clinic is cleanly illuminated.

Night:

- Warm lanterns along primary paths.
- Main gate illuminated.
- Central fire visible.
- Command house radio room lit.
- Clinic entrance clearly visible.
- Towers use small lamps.
- Perimeter remains mostly dark.

Avoid:

- Excessive torches on every block.
- Modern bright street lighting.
- Hidden exposed light blocks.
- Redstone clocks for flickering.

# AMBIENCE

Use existing sound systems if available.

Possible ambience:

- Central bonfire.
- Generator hum.
- Radio static.
- Hammering.
- Distant conversation.
- Animal sounds.
- Wind through metal.
- Gate creaking.
- Water pump.
- Evening insects.
- Watchtower bell or alarm only if original and supported.

Do not add copyrighted audio.

# DAMAGE AND MAINTENANCE BALANCE

This is an inhabited settlement.

Recommended visual condition:

- 70% maintained but aged.
- 20% visibly patched.
- 8% damaged but usable.
- 2% actively under repair.

Do not make every roof collapsed.

Every required building must remain functional.

Use damage mostly for:

- Patched roof sections.
- Replaced wall materials.
- Cracked plaster.
- Rust.
- Boarded unused windows.
- Temporary braces.
- Scaffolding.
- Salvaged doors.

# PERFORMANCE

Requirements:

- Do not force-load chunks.
- Do not scan an unlimited terrain area.
- Keep structure selection deterministic.
- Limit block entities.
- Avoid ticking decorative blocks.
- Limit NPC count.
- Limit animal count.
- Avoid active redstone clocks.
- Use bounded generation.
- Use chunk-aware piece placement.
- Cache immutable palettes.
- Prevent pieces from generating twice.
- Avoid excessive fences and complex block models where simpler blocks work.
- Do not spawn particles continuously across the village.

# DEVELOPMENT PHASES

## PHASE 1 — AUDIT

Inspect the entire relevant project architecture.

Record findings.

Do not stop.

## PHASE 2 — FINAL LAYOUT

Finalize:

- Village bounds.
- Terrain requirements.
- Mandatory building coordinates.
- Road graph.
- Perimeter path.
- Gate positions.
- Tower positions.
- Shelter depth.
- Escape route.
- Modular pools.
- Rotation behavior.

Record exact results.

Do not stop.

## PHASE 3 — CORE GENERATION

Implement:

- Registration.
- Placement validation.
- Terrain anchor.
- Central square.
- Main road.
- Mandatory buildings.
- Perimeter.
- Gates.
- Towers.
- Shelter.

Compile before proceeding.

## PHASE 4 — MODULAR VARIANTS

Implement:

- Houses.
- Barracks.
- Wall variants.
- Decorative lots.
- Market variants.
- Road details.
- Foundation types.
- Biome palette adjustments if required.

## PHASE 5 — FUNCTIONAL CONTENT

Implement:

- Residents.
- Profession markers.
- Loot tables.
- Beds.
- Workstations.
- Agriculture.
- Water.
- Lighting.
- Shelter supplies.
- Ambience hooks.

## PHASE 6 — VALIDATION

Test many seeds and terrain types.

# REQUIRED VALIDATION

Verify:

1. Village generates naturally.
2. Village generates only in allowed biomes.
3. Village does not generate in oceans.
4. Central square is navigable.
5. Main gate connects to the primary road.
6. Service gate connects correctly.
7. Perimeter closes completely.
8. Towers reach the ground.
9. Buildings do not float.
10. Doors are not buried.
11. Roads do not form cliffs.
12. Houses face roads.
13. Every mandatory building exists.
14. Clinic interior is accessible.
15. Command house is accessible.
16. Workshop and generator are separate but connected.
17. Market has clear aisles.
18. Warehouse aisles remain navigable.
19. Beds remain accessible.
20. Greenhouse crops generate correctly.
21. Water does not flood roads.
22. Shelter remains sealed.
23. Escape tunnel reaches the surface.
24. Exit is outside the perimeter.
25. NPC spawn positions are safe.
26. NPCs can navigate major routes.
27. Loot tables resolve correctly.
28. No jigsaw or structure blocks remain.
29. No unknown markers remain.
30. Rotation works if supported.
31. Generation is deterministic for the same seed.
32. Performance remains acceptable.
33. No unrelated project files were changed.

# TERRAIN TESTS

Test at least:

- Plains.
- Forest.
- Birch forest.
- Taiga.
- Gentle hills.
- Terrain near a small cave.
- Terrain near a pond.
- Multiple chunk alignments.
- Multiple rotations if supported.
- Multiple seeds.

Reject invalid terrain gracefully rather than producing a broken village.

# BUILD VALIDATION

Run:

- `./gradlew build`

Run the development client if possible:

- `./gradlew runClient`

Use structure-location or placement commands during development where appropriate.

Fix every:

- Compilation error.
- Registry error.
- Codec error.
- JSON error.
- Missing pool.
- Missing NBT file.
- Missing processor.
- Missing loot table.
- Invalid block identifier.
- Floating building.
- Buried doorway.
- Broken road.
- Wall gap.
- NPC suffocation.
- Fluid leak.
- Runtime exception.

# FINAL COMPLETION REQUIREMENTS

Before declaring completion:

1. Confirm the settlement is original.
2. Confirm it is not copied from S.T.A.L.K.E.R. or another game.
3. Confirm all mandatory zones exist.
4. Confirm all roads connect.
5. Confirm the perimeter closes.
6. Confirm both gates work.
7. Confirm the shelter is complete.
8. Confirm the escape route reaches a safe exterior point.
9. Confirm buildings adapt to terrain.
10. Confirm residents spawn correctly if supported.
11. Confirm loot tables work.
12. Confirm performance is acceptable.
13. Confirm all documentation is updated.
14. Report all created and modified files.
15. Report all tests performed.
16. Report remaining limitations honestly.

Do not leave:

- Placeholder buildings.
- Empty interiors.
- Floating foundations.
- Buried entrances.
- Unconnected roads.
- Open jigsaw connectors.
- Visible structure blocks.
- Visible jigsaw blocks.
- Unprocessed markers.
- TODO-only systems.
- Missing loot tables.
- Unregistered blocks.
- Excessive NPC spawns.
- Copyrighted symbols.
- Copied settlement layouts.
- Compilation errors.
- Runtime errors.

The task is complete only when the Survivors’ Village is fully implemented, inhabited where supported, naturally generated, terrain-adapted, navigable, defensible, visually detailed, performant, and verified in Minecraft Fabric 1.20.1.
