You are implementing a complete large underground structure for an existing Minecraft Fabric 1.20.1 mod.

Follow every applicable instruction from the `skills/` directory.

Read and strictly follow the project lore from `lore.md`.

Store every concept, plan, architectural decision, room description, coordinate, palette, TODO item, implementation note, validation result, and unresolved question inside the `concepts/` directory.

Do not rely on image understanding. The complete visual and technical specification is written below.

Do not stop after research, planning, or writing documentation. After inspecting the project and recording the plan, implement the complete structure, world generation, resources, loot integration, and validation.

# PRIMARY OBJECTIVE

Create a huge original underground research laboratory for Minecraft Fabric 1.20.1.

Working concept name:

- Deep Neurophysics Complex K-17

Suggested registry identifier:

- `deep_neurophysics_lab`
- or another identifier consistent with the project’s naming conventions.

The facility is an abandoned late-Soviet underground scientific and industrial complex.

Its atmosphere may be broadly inspired by the oppressive underground laboratories found in post-disaster Eastern European science-fiction games, including the general mood of Laboratory X16 from S.T.A.L.K.E.R.: Shadow of Chernobyl.

However, do not reproduce:

- The exact X16 layout.
- Recognizable X16 rooms.
- Exact story scenes.
- Exact puzzles.
- Exact machinery.
- Exact signs.
- Exact colors and textures.
- Exact enemy placement.
- Exact documents.
- Any S.T.A.L.K.E.R. logos or faction symbols.
- Any copyrighted names inside the implementation.

The final structure must be an original location with its own architecture, navigation, machinery, environmental storytelling, room hierarchy, and progression.

# TARGET EXPERIENCE

The structure must feel:

- Huge.
- Deep underground.
- Abandoned.
- Oppressive.
- Industrial.
- Scientific.
- Dangerous.
- Damp.
- Structurally damaged.
- Logically planned.
- Difficult to navigate without becoming a random maze.
- Visually distinct on every level.
- Suitable for exploration lasting approximately 25–45 minutes on the first visit.

The player must repeatedly feel that the complex continues deeper than expected.

The structure must combine:

- Narrow institutional corridors.
- Large industrial halls.
- Laboratories.
- Offices.
- Medical rooms.
- Maintenance areas.
- Vertical shafts.
- Catwalks.
- Flooded tunnels.
- Collapsed sectors.
- A huge central machine chamber.
- A sealed archive.
- A hidden emergency escape route.

# REQUIRED IMPLEMENTATION APPROACH

First inspect the project.

Determine:

1. Fabric Loader version.
2. Yarn mappings version.
3. Java version.
4. Existing world-generation architecture.
5. Existing structure classes.
6. Existing NBT structures.
7. Existing jigsaw pools.
8. Existing procedural-generation helpers.
9. Existing custom blocks.
10. Existing entities.
11. Existing loot tables.
12. Existing biome tags.
13. Existing structure sets.
14. Existing data-generation system.
15. Existing registration utilities.
16. Existing test infrastructure.

Use the project’s established structure system whenever it is suitable.

Preferred implementation order:

1. Existing project structure framework.
2. Hybrid deterministic modular structure.
3. NBT/jigsaw pieces if the project already supports them.
4. Custom procedural `Structure` and `StructurePiece` implementation if necessary.

Do not create one enormous unmaintainable method containing thousands of block placements.

Do not create one massive monolithic NBT file if it causes:

- Editing difficulty.
- Chunk-boundary issues.
- Excessive memory use.
- Fragile generation.
- Poor rotation support.
- Unmanageable data size.

# RECOMMENDED HYBRID GENERATION SYSTEM

Use a deterministic modular main structure with optional room variants.

The critical path must always generate successfully.

Recommended division:

- Surface entrance module.
- Vertical access shaft modules.
- Level 1 main module.
- Level 1 optional side-room modules.
- Level 2 laboratory modules.
- Level 3 utility modules.
- Level 4 central chamber modules.
- Level 5 archive and containment modules.
- Drainage tunnel modules.
- Emergency exit module.
- Damage and decay processors.
- Loot and encounter markers.

The primary route must use fixed connections and verified coordinates.

Optional side rooms may use weighted variants.

Random generation must never remove:

- Required stairs.
- Required ladders.
- Required doors.
- Required bridges.
- Required switches.
- Required access shafts.
- Required boss or objective chamber.
- Required exit.
- Required loot required for progression.

# COORDINATE SYSTEM

Use a clear local coordinate system for the complete facility.

Define:

- Positive X = east.
- Negative X = west.
- Positive Z = south.
- Negative Z = north.
- Local Y = height relative to the surface entrance anchor.

Use the center of the main surface building as approximately:

- Local X = 0.
- Local Z = 0.
- Local Y = surface level.

Recommended complete maximum bounding box:

- Width: approximately 117 blocks.
- Length: approximately 101 blocks.
- Depth below surface: approximately 68 blocks.
- Surface height: approximately 10 blocks above terrain.
- Total possible height: approximately 78 blocks.

Target horizontal bounds:

- X: −58 to +58.
- Z: −50 to +50.

Target vertical bounds:

- Y: −68 to +10 relative to the entrance surface.

These values may be adjusted slightly to fit the project’s structure system, but record every final coordinate in `concepts/deep_neurophysics_lab_layout.md`.

# WORLD-GENERATION CONDITIONS

Generate only in the Overworld unless the lore explicitly requires another dimension.

Preferred terrain:

- Mainland.
- Forests.
- Taiga.
- Plains.
- Hills.
- Sparse wooded regions.
- Abandoned industrial-themed biomes if the mod provides them.

Avoid:

- Oceans.
- Deep oceans.
- Rivers directly beneath the entrance.
- Beaches.
- Tiny islands.
- Extremely steep peaks.
- Locations where the underground structure would cross the dimension minimum Y.
- Locations where most of the laboratory would be exposed to the surface.

Use an appropriate heightmap such as the project’s established surface heightmap.

Before generation, validate:

- Sufficient vertical depth.
- Minimum-Y safety margin of at least 8 blocks.
- Surface slope around the entrance.
- No excessive fluid intersection.
- Valid chunk-generator context.
- Complete bounding-box containment.

Do not load chunks manually during world generation.

Do not scan an unbounded region.

Keep all position checks deterministic and limited.

# RARITY AND SPACING

The laboratory must be rare.

Use the existing structure-set conventions.

Suggested initial random-spread values:

- Spacing: 72 chunks.
- Separation: 24 chunks.
- Salt: choose one unique constant that is not used elsewhere in the project.

Adjust these values if the project has an established rarity scale.

Record the final values and reasoning.

Do not make the laboratory appear near every settlement.

If the project uses exclusion zones, prevent obvious overlap with other very large structures where practical.

# STRUCTURE ROTATION

Support horizontal rotation if the selected architecture supports it safely:

- North.
- South.
- East.
- West.

All local offsets, doors, corridors, pipes, room connections, loot markers, and escape tunnels must rotate correctly.

If reliable rotation would make the structure significantly more fragile, use a fixed orientation and document the limitation instead of implementing broken rotation.

# SURFACE ENTRANCE

Create a ruined service building above the main shaft.

Recommended footprint:

- 29 blocks wide.
- 23 blocks long.
- 9 blocks high.

Required features:

- Flat reinforced-concrete roof.
- Partially collapsed roof corner.
- Small ventilation tower.
- Rusted exterior railings.
- Broken perimeter fence.
- Loading platform.
- Freight-door facade.
- Administrative side entrance.
- Concrete stairs.
- Drainage channel.
- Abandoned crates.
- Cable reels.
- Overgrown cracks.
- Small generator housing.
- Exterior red emergency lamp.
- Elevator machinery room.
- Main freight-elevator shaft.
- Emergency stairwell.

The building must appear insignificant compared with the facility beneath it.

Do not construct a giant obvious laboratory tower.

# SURFACE MATERIALS

Use existing mod blocks where appropriate.

Possible vanilla fallback palette:

- Gray concrete.
- Light gray concrete.
- Smooth stone.
- Stone bricks.
- Cracked stone bricks.
- Polished andesite.
- Andesite.
- Iron blocks.
- Iron bars.
- Iron trapdoors.
- Heavy weighted pressure plates.
- Cut copper.
- Exposed cut copper.
- Weathered cut copper.
- Brown terracotta.
- Mossy stone bricks.
- Coarse dirt.
- Gravel.
- Dead bushes.
- Vines where biome-appropriate.

Do not use random materials merely to add visual noise.

# VERTICAL ACCESS CORE

Create one continuous vertical access system connecting all five underground levels.

Recommended shaft dimensions:

- Outer shaft: 13×13 blocks.
- Inner elevator opening: approximately 5×5 blocks.
- Emergency stairwell: minimum clear width of 3 blocks.
- Utility gap for pipes and cables: 2–3 blocks.
- Shaft wall thickness: minimum 2 blocks.

Required components:

- Broken freight elevator.
- Usable maintenance ladders.
- Emergency stairs or alternating landings.
- Elevator doors at every level.
- Cable counterweights.
- Machinery alcoves.
- Red emergency lights.
- Numbered floor identity through color and architecture, not readable text.
- Occasional blocked landings.
- At least one alternate route around a blocked shaft section.

Never require an impossible jump to continue.

Prevent fatal unavoidable drops.

If a deep drop is visible, provide:

- Railings.
- Broken but readable barriers.
- Ladders.
- Water emergency basin.
- Intermediate platform.
- Alternative stair route.

# LEVEL 1: SECURITY AND ADMINISTRATION

Vertical range:

- Approximately Y −14 to Y −5.

Recommended bounds:

- X −38 to +38.
- Z −30 to +30.

Primary identity:

- Institutional.
- Administrative.
- Controlled access.
- Faded green paint.
- Dirty white tile.
- Steel security doors.

Required rooms:

1. Elevator arrival lobby.
2. Security checkpoint.
3. Guard booth.
4. Decontamination corridor.
5. Locker room.
6. Staff changing room.
7. Administrative office.
8. Records office.
9. Briefing room.
10. Small cafeteria.
11. Restrooms.
12. Security equipment room.
13. Emergency stair landing.
14. Side maintenance corridor.

# LEVEL 1 PRIMARY ROUTE

Required progression:

1. Player exits the access shaft.
2. Enters the security lobby.
3. Passes through a damaged checkpoint.
4. Crosses the decontamination corridor.
5. Reaches the main administrative intersection.
6. Finds the downward access toward Level 2.

Provide at least two loops:

- Security booth loop.
- Locker and office loop.

Avoid one long featureless corridor.

# SECURITY CHECKPOINT

Recommended size:

- 17×15 blocks.
- Ceiling height: 5 blocks.

Include:

- Reinforced entrance door.
- Three block-built turnstile-like barriers.
- Guard booth with reinforced glass.
- Inspection desk.
- Metal detector-like frame.
- Lockers.
- Emergency lamp.
- Drainage grate.
- Broken camera-like decorative blocks.
- Barricade remnants.
- One optional security loot container.

Do not use readable copyrighted Soviet signs.

Use abstract faded warning panels and geometric hazard markings.

# DECONTAMINATION CORRIDOR

Recommended dimensions:

- Width: 7 blocks.
- Length: 19 blocks.
- Height: 5 blocks.

Include:

- Two sealed-door frames.
- Ceiling nozzles.
- Wall pipes.
- Floor drains.
- Observation window.
- Control panel.
- Stained tile.
- Broken final door.
- Small puddles.
- Flickering lighting pattern.

Maintain at least a 3-block clear walking path.

# LEVEL 2: SCIENTIFIC AND MEDICAL SECTOR

Vertical range:

- Approximately Y −27 to Y −17.

Recommended bounds:

- X −42 to +42.
- Z −34 to +34.

Primary identity:

- Sterile laboratory architecture corrupted by decay.
- White tiles.
- Faded institutional green.
- Observation glass.
- Stainless-steel-like surfaces.
- Chemical storage.
- Specimen containment.

Required rooms:

1. Main laboratory corridor.
2. General research laboratory.
3. Specimen laboratory.
4. Observation booth.
5. Chemical storage.
6. Cold-storage room.
7. Medical ward.
8. Operating or examination room.
9. Staff preparation room.
10. Data processing room.
11. Sample archive.
12. Sanitation room.
13. Damaged containment room.
14. Access to service stairs.

# MAIN LABORATORY CORRIDOR

Recommended dimensions:

- Width: 7 blocks.
- Length: 45–55 blocks.
- Height: 6 blocks.

Break the corridor into segments using:

- Door frames.
- Ceiling beams.
- Observation windows.
- Pipe intersections.
- Floor drains.
- Collapsed sections.
- Lighting changes.
- Small waiting areas.

Do not create a single uninterrupted tunnel.

# GENERAL RESEARCH LABORATORY

Recommended dimensions:

- 25×21 blocks.
- Height: 7 blocks.

Include:

- Central worktables.
- Wall cabinets.
- Sinks.
- Drainage.
- Ceiling utility frame.
- Glass partition.
- Broken instruments.
- Cable bundles.
- Chemical shelves.
- Floor debris.
- One secure cabinet.
- One optional loot container.
- Multiple entry points where logical.

# SPECIMEN LABORATORY

Recommended dimensions:

- 23×19 blocks.
- Height: 8 blocks.

Include:

- Three to five block-built containment tanks.
- Thick reinforced-glass walls.
- Dark liquid or empty variants.
- Maintenance pipes.
- Floor drains.
- Observation booth.
- Steel worktables.
- Broken tank variant.
- Emergency shutter.
- Control console.
- Cable conduits.
- Quarantine doorway.

Use existing mod containment or laboratory blocks if available.

Do not place graphic gore.

Environmental storytelling must come from:

- Broken glass.
- Open restraints.
- Damaged drains.
- Abandoned equipment.
- Emergency lighting.
- Barricaded doors.

# MEDICAL WARD

Recommended dimensions:

- 21×17 blocks.
- Height: 6 blocks.

Include:

- Four to eight beds.
- Privacy dividers.
- Medicine cabinets.
- Examination table.
- Sink.
- Small nurse station.
- Damaged ceiling.
- Bloodless or extremely restrained evidence of evacuation.
- Medical loot table.
- Side storage.

Do not make every bed identical.

# LEVEL 3: INDUSTRIAL UTILITIES

Vertical range:

- Approximately Y −40 to Y −29.

Recommended bounds:

- X −48 to +48.
- Z −38 to +38.

Primary identity:

- Loud industrial machinery.
- Rusted steel.
- Pipes.
- Pumps.
- Catwalks.
- Cable galleries.
- Flooding.
- Lower visibility.
- Warmer emergency lighting.

Required rooms:

1. Generator hall.
2. Transformer room.
3. Boiler room.
4. Pump station.
5. Water-treatment room.
6. Cable gallery.
7. Workshop.
8. Spare-parts storage.
9. Fuel or coolant storage.
10. Flooded maintenance corridor.
11. Service elevator.
12. Access route to Level 4.

# GENERATOR HALL

Recommended dimensions:

- 33×25 blocks.
- Clear height: 12 blocks.

Include:

- Two or three large generator assemblies.
- Turbine-like block structures.
- Thick intake and output pipes.
- Catwalks.
- Stairs.
- Yellow-black safety edges.
- Control booth.
- Overhead cable trays.
- Suspended maintenance crane.
- Red emergency lighting.
- Coolant channels.
- Floor grates.
- One damaged generator.
- One partially functional generator.
- Multiple routes around machinery.

Maintain minimum:

- 3-block-wide primary route.
- 2-block-wide catwalks.
- 2-block-high player clearance everywhere.

# PIPE SYSTEM

Use consistent pipe color logic:

- Dark red-brown: heat or steam.
- Weathered copper: coolant.
- Faded green: water.
- Dark gray: ventilation.
- Black: cables.
- Mustard yellow: hazardous pressure line.

Do not connect pipes randomly.

Each visible pipe should appear to travel between plausible machinery or disappear through a wall, floor, or ceiling service route.

Use:

- Existing custom pipe blocks.
- Walls.
- Fences.
- Copper blocks.
- Trapdoors.
- Stairs.
- Slabs.
- Custom models already present in the mod.

# FLOODED MAINTENANCE AREA

Recommended corridor dimensions:

- Width: 7–9 blocks.
- Length: 35–50 blocks.
- Height: 6 blocks.

Include:

- Ankle-deep or waist-deep water sections.
- Raised side walkway.
- Drainage grates.
- Rusted pipes.
- Broken ceiling.
- Exposed cables.
- Maintenance ladders.
- Pump alcove.
- Collapsed dead end.
- Hidden supply niche.
- Water flowing from a damaged wall.
- Connection to Level 5 drainage route.

Keep at least one reliable navigable route.

Do not flood redstone or functional blocks unless intentionally protected.

# LEVEL 4: NEURO-RESONATOR CHAMBER

Vertical range:

- Approximately Y −59 to Y −40.

Recommended chamber bounds:

- Approximately 55×55 blocks.
- Internal clear height: 23–27 blocks.

This is the facility’s primary landmark.

The player must immediately understand that this chamber is the central purpose of the entire laboratory.

# CHAMBER SHAPE

Use:

- Large cylindrical or octagonal chamber.
- Reinforced concrete shell.
- Multiple wall buttresses.
- Deep central shaft.
- Three circular or octagonal catwalk rings.
- Four radial bridges.
- Control booths.
- Cable bundles.
- Vertical machine core.
- Service staircases.
- Ladders.
- Maintenance platforms.
- Emergency lights.
- Observation windows.

Use stepped block geometry to approximate circles.

Do not use impossible smooth cylindrical geometry.

# CENTRAL MACHINE CORE

Recommended dimensions:

- Main core footprint: 11×11 blocks.
- Height: approximately 25 blocks.
- Lower base: 15×15 blocks.
- Upper crown: 13×13 blocks.

Required construction:

- Heavy lower pedestal.
- Central vertical column.
- Repeating machine segments.
- Dark reinforced panels.
- Narrow green-white observation lights.
- Cable connection points.
- Four radial conduits.
- Maintenance hatches.
- Internal dark cavity.
- Broken upper segment.
- Multiple external braces.

The machine must look engineered, not like a magical altar.

Do not use runes or fantasy crystals.

# CATWALK RINGS

Create three main rings:

1. Lower ring near machine base.
2. Middle ring near central controls.
3. Upper ring near cable distribution.

Recommended walkway width:

- 3 blocks.

Railings:

- Minimum 1 block high.
- Broken only in carefully selected optional locations.
- Never remove railings along the mandatory route without an alternate safety path.

Connect rings using:

- Two main staircases.
- One emergency ladder.
- Four radial bridges.
- One partially collapsed bridge with a safe detour.

# CONTROL BOOTHS

Create four control areas around the chamber:

- North observation booth.
- South power-control station.
- East monitoring booth.
- West maintenance-control booth.

Each booth should contain:

- Consoles.
- Indicator lights.
- Reinforced glass.
- Cable conduits.
- Chairs or workstations.
- Emergency controls.
- Storage.
- Distinct damage state.

Do not require functional puzzles unless the project already has an interaction system suitable for them.

# OPTIONAL POWER-RESTORATION PROGRESSION

Only implement this mechanic if it fits the project.

Possible sequence:

1. Player reaches Level 3 generator hall.
2. Activates or repairs a power-control block.
3. Level 4 emergency lights change state.
4. Selected doors unlock.
5. Central machine begins low-intensity animation or sound.
6. Access to Level 5 opens.

Requirements:

- Server-authoritative state.
- Persistent state after chunk reload.
- No fragile vanilla redstone network spanning unloaded chunks.
- Use block entities or structure-state storage only if an existing system supports it.
- Provide a fallback route if the interaction system is not implemented.

Do not create an enormous new puzzle framework solely for this structure.

# LEVEL 5: ARCHIVE, REACTOR, AND CONTAINMENT

Vertical range:

- Approximately Y −68 to Y −60.

Recommended bounds:

- X −42 to +42.
- Z −32 to +32.

Primary identity:

- Oldest and most restricted layer.
- Low ceilings in archives.
- Heavy blast doors.
- Red emergency lighting.
- Severe structural damage.
- Drainage water.
- Dense records storage.
- Hidden escape route.

Required rooms:

1. Sealed archive.
2. Secure records vault.
3. Emergency reactor or backup power chamber.
4. Collapsed containment sector.
5. Drainage control room.
6. Hidden storage.
7. Escape-tunnel entrance.
8. Final maintenance intersection.
9. Deep shaft access.
10. Emergency exit route.

# SEALED ARCHIVE

Recommended dimensions:

- 27×21 blocks.
- Height: 6 blocks.

Include:

- Dense shelving.
- Filing cabinets.
- Storage crates.
- Microfilm or data-terminal-like props.
- Secure central cabinet.
- Collapsed shelves.
- Reading table.
- Reinforced inner vault.
- Rare archive loot.
- One hidden document cache represented through project items, if available.

Maintain narrow but navigable aisles.

Do not fill every aisle with debris.

# EMERGENCY REACTOR ROOM

Recommended dimensions:

- 25×25 blocks.
- Height: 11 blocks.

Include:

- Compact backup reactor.
- Cooling pipes.
- Shielded walls.
- Two maintenance platforms.
- Control console.
- Damaged coolant channel.
- Red lighting.
- Warning-striped floor edge.
- Heavy door.
- Side maintenance route.
- Exhaust shaft.

The reactor must be visually distinct from the Level 4 resonator.

# COLLAPSED CONTAINMENT SECTOR

Recommended dimensions:

- 29×23 blocks before damage.
- Approximately 25–35% visibly collapsed.

Include:

- Broken wall.
- Rock intrusion.
- Bent support columns.
- Partial ceiling collapse.
- Damaged containment doors.
- Rubble slopes.
- Exposed reinforcement.
- One dead end.
- One crawl-like side route with normal Minecraft clearance.
- One optional rare loot location.

Never allow random damage processing to destroy the only required path.

# EMERGENCY ESCAPE ROUTE

Create a hidden exit path from Level 5.

Route:

1. Archive or drainage intersection.
2. Narrow maintenance passage.
3. Drainage tunnel.
4. Rising ladder shaft.
5. Horizontal escape tunnel.
6. Small concealed surface outlet 60–100 blocks from the main entrance.

The outlet may appear as:

- Concrete drainage opening.
- Collapsed utility shed.
- Hidden ventilation structure.
- Rusted service hatch.

Ensure the exit rotates correctly with the structure.

Do not generate the outlet inside midair, water, or solid uncarved terrain without creating a valid opening.

# BLOCK PALETTE

Audit existing mod blocks first.

Prefer existing project blocks that already represent:

- Concrete.
- Painted concrete.
- Laboratory tile.
- Rusted steel.
- Pipes.
- Cable trays.
- Industrial lamps.
- Reinforced glass.
- Laboratory furniture.
- Computers.
- Generators.
- Vents.
- Doors.
- Warning panels.
- Grates.

Do not recreate duplicate blocks with different names.

Vanilla fallback palette:

Structural concrete:

- Gray concrete.
- Light gray concrete.
- Smooth stone.
- Polished andesite.
- Andesite.
- Stone bricks.
- Cracked stone bricks.
- Deepslate tiles for deep structural reinforcement.

Interior tile:

- Smooth quartz.
- Quartz slabs.
- Diorite.
- Polished diorite.
- White concrete.
- Light gray concrete.

Painted lower walls:

- Green terracotta.
- Green concrete.
- Cyan terracotta in small quantities.
- Mossy stone variants for moisture damage.

Rust:

- Exposed copper.
- Weathered copper.
- Cut copper.
- Brown terracotta.
- Granite.
- Polished granite.
- Brown concrete.
- Dark oak details.

Industrial metal:

- Iron blocks.
- Iron bars.
- Chains.
- Hoppers.
- Cauldrons.
- Anvils.
- Iron trapdoors.
- Heavy weighted pressure plates.

Glass:

- Tinted glass.
- Gray stained glass.
- Light gray stained glass.
- Iron bars around selected windows.

Hazard markings:

- Yellow concrete.
- Yellow terracotta.
- Black concrete.
- Blackstone.

Lighting:

- Redstone lamps.
- End rods hidden inside fixtures.
- Sea lanterns concealed behind trapdoors or custom diffusers.
- Red stained glass around emergency lamps.
- Existing project lamps preferred.

# CUSTOM BLOCK CREATION

Do not automatically create dozens of new decorative blocks.

Only add a custom block when:

1. The required function or silhouette cannot be represented adequately.
2. No equivalent exists in the project.
3. The block will be reused throughout the laboratory.
4. It fits the mod’s architecture.
5. Its texture and model can be completed fully.

Possible minimal reusable additions if truly necessary:

- Cracked laboratory tile.
- Faded green wall panel.
- Rusted reinforced panel.
- Industrial floor grate.
- Reinforced observation glass.
- Ceiling fluorescent fixture.
- Red emergency lamp.
- Large pipe block family.
- Cable-tray block.
- Laboratory console.
- Containment glass frame.

If adding directional blocks, implement:

- Correct placement state.
- Rotation.
- Mirroring.
- Blockstate JSON.
- Item model.
- Loot table.
- Pick-block behavior.
- Waterlogging where appropriate.
- Datagen integration.
- Texture validation.

# ARCHITECTURAL RULES

All rooms must follow these minimums:

- Primary corridor clear width: 3–5 blocks.
- Secondary corridor clear width: minimum 2 blocks.
- Primary room ceiling: 5–8 blocks.
- Industrial hall ceiling: 10–14 blocks.
- Catwalk width: minimum 2 blocks, preferably 3.
- Door opening: minimum 2 blocks high and 1 block wide.
- Major blast door: 3–5 blocks wide and 4–5 blocks high.
- Stair clearance: minimum 2 blocks.
- Ladder landing: minimum 2×2 blocks.
- Railings: minimum 1 block high.
- Wall thickness: normally 2 blocks.
- Floor thickness between levels: normally 2–3 blocks.
- External bunker shell: 2–4 blocks.

Avoid one-block-thick external walls around the entire structure.

The facility must not be easily exposed by a small cave opening.

# NAVIGATION DESIGN

Create a clear primary route using visual landmarks.

Landmarks:

- Surface freight shaft.
- Green Level 1 corridors.
- White laboratory Level 2.
- Orange-rust industrial Level 3.
- Massive circular Level 4 chamber.
- Red-lit Level 5 archive and reactor.
- Water-filled escape route.

Use recurring directional cues:

- Pipe colors.
- Floor stripe direction.
- Light color.
- Door-frame type.
- Ceiling architecture.
- Room scale.
- Damage intensity.

Do not rely entirely on readable signs.

Provide:

- At least one loop on each major level.
- Optional side rooms.
- Shortcuts that reconnect to the main route.
- One or two collapsed dead ends with rewards.
- Clear transitions between levels.
- No random corridor maze.

# DECAY AND DAMAGE SYSTEM

Create controlled variants:

- Intact.
- Damp.
- Rusted.
- Partially collapsed.
- Flooded.
- Emergency-lit.
- Overgrown surface variant.

Recommended damage distribution:

- 45% worn but structurally intact.
- 25% moisture damage.
- 15% heavy rust.
- 10% partial collapse.
- 5% severe special damage.

These values are visual guidance, not a requirement for global random replacement.

Critical route protection:

Never damage:

- Required stairs.
- Required ladders.
- Required door openings.
- Required bridges.
- Required interaction blocks.
- Required loot containers.
- Structural markers.
- Escape route.
- Player spawn or entrance area.

Use processor lists or protected-position masks where appropriate.

# CAVE INTERSECTION

The laboratory may intersect caves, but the result must remain believable.

Rules:

- Maintain the reinforced outer shell.
- Seal most unintended cave openings.
- Permit a small number of deliberate breaches.
- Add rubble around breaches.
- Add reinforcement beams.
- Prevent water or lava from flooding the entire structure unexpectedly.
- Replace dangerous fluid sources around critical rooms when necessary and safe.
- Do not erase huge natural cave regions outside the structure.
- Do not write blocks outside the known bounding area unnecessarily.

# WATER HANDLING

Flooding must be deliberate.

Use water only in:

- Maintenance tunnels.
- Pump room.
- Drainage routes.
- Selected damaged laboratories.
- Lower collapsed containment sector.

Do not flood:

- Main entrance.
- Entire central chamber.
- Required redstone or block-entity systems.
- Archive loot.
- Mandatory ladders.
- Primary control booths.

Validate fluid containment after generation.

# LIGHTING

Use layered lighting:

Level 1:

- Cold green-white fluorescent lighting.
- Occasional red emergency lamps.

Level 2:

- Dirty white laboratory lighting.
- Flickering gaps.
- Dark specimen rooms.

Level 3:

- Warm industrial lights.
- Red emergency lamps.
- Deep pipe shadows.

Level 4:

- Sparse white-green machine lights.
- Red perimeter emergency lamps.
- Dark lower shaft.

Level 5:

- Mostly red emergency lighting.
- Very dark archives.
- Small reactor highlights.
- Minimal escape-route lighting.

Avoid over-lighting.

Allow dark spaces, but ensure required navigation remains possible.

Do not spawn visually exposed light blocks unless the project intentionally uses them.

# LOOT DESIGN

Inspect existing project loot tables and items.

Create separate loot tables such as:

- `chests/deep_lab_security`
- `chests/deep_lab_office`
- `chests/deep_lab_medical`
- `chests/deep_lab_chemical`
- `chests/deep_lab_maintenance`
- `chests/deep_lab_archive`
- `chests/deep_lab_reactor`
- `chests/deep_lab_hidden`

Suggested loot themes:

Security:

- Basic weapons if consistent with the mod.
- Ammunition or tools if present.
- Armor scraps.
- Keys or access items only if an access system exists.

Office:

- Paper.
- Books.
- Maps.
- Low-value supplies.
- Lore documents represented by existing systems.

Medical:

- Food or healing items.
- Potions.
- Bandages if present.
- Rare medical supplies.

Chemical:

- Bottles.
- Brewing materials.
- Mod-specific reagents.
- Protective equipment.

Maintenance:

- Iron.
- Copper.
- Redstone.
- Tools.
- Repair materials.
- Industrial components.

Archive:

- Rare lore item.
- High-value technical component.
- Research material.
- Unique but non-essential collectible.

Reactor:

- Rare energy material.
- High-tier crafting component.
- Dangerous industrial resource.

Do not place guaranteed overpowered loot in ordinary rooms.

Do not hardcode item identifiers before checking registration.

Use loot tables rather than inserting fixed item stacks into every chest.

# LOOT PLACEMENT

Recommended approximate counts across the complete facility:

- Common containers: 18–28.
- Uncommon containers: 6–10.
- Rare containers: 2–4.
- Hidden containers: 2–5.

Do not place all containers in plain sight.

Use:

- Lockers.
- Cabinets.
- Crates.
- Toolboxes.
- Medical cabinets.
- Secure archive storage.
- Maintenance niches.

Ensure block entities receive loot tables correctly during generation.

# ENTITY AND ENCOUNTER INTEGRATION

Inspect existing mod entities.

Use only lore-compatible existing entities.

Do not create new mobs unless explicitly required.

Possible encounter zones:

- Surface entrance.
- Security sector.
- Damaged laboratory.
- Generator hall.
- Flooded maintenance tunnel.
- Central chamber.
- Archive.
- Escape route.

Keep spawn placement away from walls and inside valid navigation space.

Do not permanently fill every room with enemies.

Use environmental silence between encounters.

If using spawners or scripted encounters:

- Follow existing project systems.
- Avoid uncontrolled infinite spawning.
- Persist completion state if necessary.
- Validate multiplayer behavior.
- Do not make required doors permanently inaccessible.

# AMBIENCE

Use existing project sound blocks or ambient systems if available.

Possible ambience:

- Distant machinery hum.
- Water dripping.
- Electrical buzzing.
- Metal creaking.
- Pipe knocking.
- Generator vibration.
- Low central-machine resonance.
- Occasional alarm pulse.
- Water movement.
- Ventilation noise.

Do not add copyrighted audio.

Do not create a new complex sound engine solely for this structure.

# STRUCTURE MARKERS

If using NBT structure markers, define a documented marker vocabulary.

Possible markers:

- `loot_security`
- `loot_office`
- `loot_medical`
- `loot_chemical`
- `loot_maintenance`
- `loot_archive`
- `loot_reactor`
- `loot_hidden`
- `mob_common`
- `mob_industrial`
- `mob_lab`
- `mob_deep`
- `light_emergency`
- `damage_minor`
- `damage_major`
- `water_source`
- `power_control`
- `escape_exit`

Process every marker safely.

Replace marker blocks after processing.

Log unknown markers during development.

Do not leave structure blocks or jigsaw markers visible in the generated world.

# PROCEDURAL HELPER ARCHITECTURE

If using Java procedural generation, create reusable helpers rather than raw repetitive calls.

Possible helpers:

- `buildRoomShell`
- `buildCorridor`
- `buildDoorFrame`
- `buildBlastDoor`
- `buildTileWall`
- `buildConcreteWall`
- `buildPipeRun`
- `buildCableTray`
- `buildCatwalk`
- `buildRailing`
- `buildStaircase`
- `buildLadderShaft`
- `buildGenerator`
- `buildContainmentTank`
- `buildConsole`
- `buildLockerRow`
- `buildLabTable`
- `buildCeilingLight`
- `buildEmergencyLight`
- `buildDrain`
- `buildRubble`
- `buildCollapsedWall`
- `placeLootContainer`
- `placeEncounterMarker`

Each helper must:

- Accept local coordinates.
- Respect rotation.
- Stay inside its declared bounds.
- Avoid unnecessary chunk lookups.
- Use deterministic random input.
- Avoid mutable global state.

# CLASS ORGANIZATION

Follow project conventions.

A possible organization:

- `DeepNeurophysicsLabStructure`
- `DeepNeurophysicsLabPiece`
- `DeepLabLayout`
- `DeepLabPalette`
- `DeepLabRooms`
- `DeepLabDecorators`
- `DeepLabMarkers`
- `DeepLabProcessors`
- `DeepLabRegistration`

Do not create excessive abstraction if the project uses a simpler pattern.

Do not put all generation logic in the registration class.

# RESOURCE ORGANIZATION

Use the actual mod ID.

Potential resource locations:

- `data/<mod_id>/worldgen/structure/deep_neurophysics_lab.json`
- `data/<mod_id>/worldgen/structure_set/deep_neurophysics_lab.json`
- `data/<mod_id>/tags/worldgen/biome/has_structure/deep_neurophysics_lab.json`
- `data/<mod_id>/worldgen/template_pool/...`
- `data/<mod_id>/structures/deep_neurophysics_lab/...`
- `data/<mod_id>/loot_tables/chests/deep_lab_*.json`

Only create files appropriate to the selected generation method.

Do not create unused duplicate JSON and Java registrations.

# PERFORMANCE REQUIREMENTS

The structure is large, so generation must be optimized.

Requirements:

- Never scan the entire world.
- Never force-load chunks.
- Never perform unbounded flood fill.
- Never search recursively without strict limits.
- Avoid thousands of individual block-state allocations.
- Cache immutable block palettes.
- Keep random generation deterministic.
- Divide work into structure pieces aligned reasonably with chunks.
- Use bounding-box checks.
- Prevent repeated decoration.
- Avoid excessive block entities.
- Avoid hundreds of ticking blocks.
- Prefer static decorative blocks.
- Keep particles and ambient effects localized.
- Do not create active redstone clocks throughout the facility.

A generated laboratory must not create continuous server lag.

# CHUNK BOUNDARIES

Every piece must:

- Know its bounding box.
- Place blocks only when allowed by the current generation region.
- Avoid duplicate generation at piece edges.
- Connect cleanly across chunk boundaries.
- Preserve doors, floors, pipes, and corridors crossing boundaries.
- Avoid missing walls caused by incorrect clipping.

Test the complete structure across many chunk alignments.

# DEVELOPMENT PHASES

Execute the work in this order.

## PHASE 1 — AUDIT

1. Inspect project structure.
2. Read `skills/`.
3. Read `lore.md`.
4. Find existing world-generation implementations.
5. Find existing mod blocks and entities.
6. Find loot-table conventions.
7. Determine the correct Fabric/Yarn APIs.
8. Record findings in `concepts/deep_neurophysics_lab_audit.md`.

Do not stop after this phase.

## PHASE 2 — ARCHITECTURE

1. Finalize dimensions.
2. Finalize anchor position.
3. Finalize level bounds.
4. Define primary path.
5. Define optional branches.
6. Define rotation policy.
7. Define module boundaries.
8. Define palette.
9. Define protected critical positions.
10. Record the final plan.

Do not stop after this phase.

## PHASE 3 — CORE GENERATION

1. Register the structure type if needed.
2. Register structure pieces if needed.
3. Implement surface-position validation.
4. Implement anchor calculation.
5. Implement modular layout.
6. Implement bounding boxes.
7. Implement rotation.
8. Generate the outer shell.
9. Generate the vertical access core.
10. Confirm the structure can generate without decoration.

Run build checks before continuing.

## PHASE 4 — LEVEL IMPLEMENTATION

Implement and validate separately:

1. Surface entrance.
2. Level 1.
3. Level 2.
4. Level 3.
5. Level 4.
6. Level 5.
7. Escape tunnel.
8. Surface outlet.

After each level:

- Check coordinates.
- Check connections.
- Check player clearance.
- Check bounding boxes.
- Check chunk clipping.
- Check rotation.

## PHASE 5 — DECORATION

Add:

- Pipes.
- Cables.
- Machinery.
- Furniture.
- Glass.
- Lighting.
- Rust.
- Moisture.
- Controlled rubble.
- Flooding.
- Containers.
- Encounter markers.

Do not decorate before confirming navigation.

## PHASE 6 — WORLDGEN DATA

Add:

- Structure JSON.
- Structure set.
- Biome tags.
- Processor lists.
- Template pools if used.
- Loot tables.
- Language entries.
- Datagen integration.

## PHASE 7 — VALIDATION

Perform complete verification.

# REQUIRED AUTOMATED OR SEMI-AUTOMATED TESTS

Where possible, create GameTests or development validation utilities for:

1. Structure registration.
2. Structure serialization.
3. Generation without exceptions.
4. Stable deterministic layout from the same seed.
5. Valid bounding box.
6. No placement below minimum Y.
7. Complete primary route.
8. Correct vertical connections.
9. Correct loot-table identifiers.
10. No unknown blocks.
11. No remaining structure markers.
12. Rotation consistency.
13. No mandatory path blocked by processors.
14. Escape tunnel connection.
15. Surface entrance connection.
16. Chunk-boundary placement.

If automatic pathfinding validation is impractical, create a documented manual route checklist.

# MANUAL PRIMARY-ROUTE CHECKLIST

Verify that a player can travel without commands from:

1. Surface entrance.
2. Security checkpoint.
3. Decontamination corridor.
4. Level 1 central intersection.
5. Level 2 main laboratory corridor.
6. Specimen sector.
7. Service stairs.
8. Level 3 generator hall.
9. Flooded maintenance route.
10. Level 4 upper catwalk.
11. Level 4 central control ring.
12. Access to Level 5.
13. Archive.
14. Reactor area.
15. Drainage tunnel.
16. Emergency ladder.
17. Hidden surface exit.

Verify the reverse route where intended.

# VISUAL VALIDATION

Inspect:

- Surface silhouette.
- Each level independently.
- Corridor repetition.
- Room-scale variation.
- Lighting.
- Pipe continuity.
- Cable continuity.
- Catwalk safety.
- Water containment.
- Damage placement.
- Material transitions.
- Central-chamber silhouette.
- View from upper catwalk.
- View from lower shaft.
- Escape-route readability.

Remove obvious copy-pasted repetition.

Use variants for:

- Corridor damage.
- Pipe arrangement.
- Light failures.
- Furniture position.
- Debris.
- Door state.
- Ceiling damage.

# BUILD VALIDATION

Run:

- `./gradlew build`

Run the development client if the environment permits:

- `./gradlew runClient`

Generate multiple worlds or use structure-location commands to test several placements.

Test at least:

- Flat terrain.
- Forest.
- Hills.
- Near caves.
- Near aquifers.
- Different chunk alignments.
- Different rotations if supported.
- Different seeds.

Fix every:

- Compilation error.
- Registry error.
- Codec error.
- JSON error.
- Missing block.
- Missing loot table.
- Missing template pool.
- Invalid processor.
- Bounding-box error.
- Chunk clipping error.
- Fluid leak.
- Broken path.
- Lighting issue.
- Runtime exception.

# FINAL COMPLETION REQUIREMENTS

Before declaring completion:

1. Confirm that the structure is original.
2. Confirm that it does not reproduce X16.
3. Confirm that every level generates.
4. Confirm that all main rooms exist.
5. Confirm that the primary route is navigable.
6. Confirm that all vertical links work.
7. Confirm that the central resonator chamber is complete.
8. Confirm that the emergency exit reaches the surface.
9. Confirm that loot tables work.
10. Confirm that no markers remain.
11. Confirm that the structure remains inside world limits.
12. Confirm that generation is deterministic.
13. Confirm that generation does not force-load chunks.
14. Confirm that performance is acceptable.
15. Confirm that existing mod blocks are reused where appropriate.
16. Confirm that unrelated files were not modified.
17. Update the documentation in `concepts/`.
18. Report every created and modified file.
19. Report all tests performed.
20. Report any remaining limitations honestly.

Do not leave:

- Placeholder rooms.
- Empty major halls.
- Temporary debug blocks.
- Structure blocks visible in the world.
- Jigsaw blocks visible in the world.
- TODO-only implementations.
- Broken loot references.
- Missing textures.
- Unregistered blocks.
- Unreachable rooms.
- Mandatory parkour.
- Unsealed fluid leaks.
- Monolithic unreadable generator code.
- Copyrighted names or copied level layouts.

The task is complete only when the complete multi-level laboratory is implemented, registered, generated naturally, navigable, visually detailed, performant, and successfully tested in Minecraft Fabric 1.20.1.
