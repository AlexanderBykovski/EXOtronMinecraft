<p align="center"><img src="src/main/resources/assets/opusvsexe/icon.png" alt="Exotron" width="112"></p>

# Exotron

**A world after artificial intelligence.** A story-driven adventure mod for **Minecraft Java 1.20.1 · Fabric**, also known as **Opus Vs EXE**. Explore the aftermath of the Great War, recover a metal that remembers the past, and turn abandoned technology against the machines that inherited the world.

**English** · [Українська](README.uk.md) · [Русский](README.ru.md)

[CurseForge](https://www.curseforge.com/minecraft/mc-mods/exotron-beta) · [Modrinth](https://modrinth.com/mod/exotron-beta) · [Planet Minecraft](https://www.planetminecraft.com/mod/exotron-beta/) · [BuiltByBit](https://builtbybit.com/resources/exotron.127909/) · [Report an issue](https://github.com/Irisko007/Exotron/issues)

![Mossbound at the Moon Fountain — an actual in-game screenshot](docs/assets/screenshots/mossbound.png)

> **Beta · source version 1.0.0.** This repository contains the supplied development source snapshot. A separately published JAR may have a different set of enabled content. The generated crafting book documents this repository exactly, including recipes retained for compatibility.

## What is in the mod?

| Route | What you explore | What you work toward |
| :--- | :--- | :--- |
| Opus and Haiku | Laboratories, ruined cities, fortresses, the citadel and colosseum | Refined Opus, machine-tier progression and Haiku Omega |
| Fire Realm | Volcanic terrain, ember trees and the Four Veins | Vein equipment, Diablo and his explosive Demonic Trident |
| Paradise Island | A sky island, wildlife and the Parthenon | Wyvern riding, celestial equipment and Angel Boy |
| Dark Forest | Gloomwood, Moonflowers and the Moon Fountain | Living forest equipment and Mossbound |
| Settlements | Survivor and Japanese settlements | Trading, exploration, samurai encounters and equipment |

- Five pilotable **EXO frames** with energy, equipment bays and individual abilities.
- Haiku machines, regional creatures and bosses with phases, attack warnings and repeat-summon mechanics.
- Weapons and tools with active abilities, armor set bonuses, material upgrades and custom 3D models.
- **Opus Assembly Table 5×5**, **Parthenon Forge 3×3** and the **Resonance Forge** refinement chain.
- Memory Fragments, exploration compasses, collectible trophies and the **Mod Chronicles** progression screen.
- Client/server source separation and an optional JEI integration for custom stations and recipe transfer.

<p><img src="docs/assets/screenshots/diablo.png" alt="Diablo in the Fire Realm" width="49%"> <img src="docs/assets/screenshots/angel-boy.png" alt="Angel Boy at the Parthenon" width="49%"></p>

## The story

Brothers Kimi and Coddy discover **Opus**, a metal capable of preserving memories. Kimi uses it to create Haiku, an artificial intelligence that learns to reproduce the metal and improve its own body. Fear, betrayal and the death of its creators lead to the Great War.

The player arrives among the remains: unfinished EXO designs, machines, scattered memories and places that still carry the war's traces. The main story is in [lore/lore.md](lore/lore.md). The Fire Realm has its own [parallel storyline](lore/Fire%20Biom/LOR.md).

## Installation

Use **Minecraft Java Edition 1.20.1** with Fabric. The requirements below are read from this source's `fabric.mod.json` and `gradle.properties`.

| Component | Requirement |
| :--- | :--- |
| Minecraft | Java Edition **1.20.1** |
| Java | **17 or newer** at runtime; **JDK 17** for the documented build |
| Fabric Loader | **0.19.5 or newer** |
| Fabric API | **0.92.12+1.20.1 or newer compatible 1.20.1 build**; install separately |
| GeckoLib | **4.4.9**, embedded by the Gradle build through `include` |
| JEI | Optional; integration compiles against **15.49.0.200** |

1. Install the Fabric profile for Minecraft 1.20.1.
2. Download the Exotron JAR and a compatible Fabric API JAR. Put both into the instance's `mods` folder.
3. Start the Fabric profile. Use the same mod versions on the client and server when playing together.
4. Check **Options → Controls** for key conflicts, especially `L` and the EXO ability keys.

For a downloaded release, its own dependency metadata takes precedence. The remapped JAR built here embeds GeckoLib; do not add a second copy unless a particular published package requires it. Fabric's [installation guide](https://docs.fabricmc.net/players/installing-mods) explains how to locate the instance's `mods` folder.

## First steps and controls

Find Opus materials and Memory Fragments while exploring structures. Refine **Raw → Stabilized → Resonant → Core Opus** in an active Resonance Forge. Build the 5×5 assembly table, then work toward EXO activation cores and an assembly frame. The Fire Realm, Paradise Island and Dark Forest offer their own equipment routes.

| Default key | Action |
| :---: | :--- |
| **L** | Open **Mod Chronicles**: added achievements and progression |
| **F / G / H / J** | EXO abilities 1 / 2 / 3 / ultimate, when supported by the frame |
| **R** | Open EXO equipment bays |
| **B** | EXO resonance punch |
| **V** | Equipment ability: armor shockwave / hurricane / shadow step, depending on equipment |

Keys can be changed in Controls. Equipment, energy and cooldown requirements still apply. **Demonic Trident** drops from Diablo: hold use to charge, release to throw; it explodes on impact and its projectile returns to the owner.

## Every crafting recipe

| Format | Languages | Contents |
| :--- | :--- | :--- |
| [CRAFTING.md](CRAFTING.md) | Ukrainian | Complete aligned crafting grids |
| [CRAFTING.en.md](docs/CRAFTING.en.md) | English | Same recipes and ingredient counts |
| [CRAFTING.ru.md](docs/CRAFTING.ru.md) | Russian | Same recipes and ingredient counts |
| [recipes.html](docs/recipes.html) | Switch between all three | Illustrated grids, search, station filter and print / PDF |

**153 JSON recipes:** 61 shaped, 72 shapeless, 6 assembly recipes and 14 Parthenon recipes. The book also includes all **three Resonance Forge conversions** and explains EXO assembly. Ordinary recipes use a 3×3 grid; assembly recipes retain the complete 5×5 pattern. Each symbol occupies one slot, with ingredient IDs and quantities below it. A Ruby Halo Shard used in Parthenon forging is returned after crafting.

The existing [illustrated field guide](docs/index.html) and [progression guide](docs/guide.html) are also included. Open these HTML files locally after cloning or downloading the repository. Historical guide entries can describe content retained in the source rather than enabled in a specific published build.

## Build from source

Install **JDK 17** and make sure `JAVA_HOME` points to it. The Gradle wrapper downloads **Gradle 8.10.2**; the first build needs internet access to resolve Minecraft, Fabric, GeckoLib and the compile-only JEI API.

```sh
git clone https://github.com/Irisko007/Exotron.git
cd Exotron
chmod +x gradlew
./gradlew build
```

On Windows, use `gradlew.bat build`. Output: **`build/libs/opusvsexe-1.0.0.jar`**. The `-sources.jar` is for developers and is not the playable mod.

```sh
./gradlew runClient       # development client
./gradlew runServer       # development dedicated server; accept its EULA first
```

Resource and documentation checks require **Python 3.10+** and no extra packages:

```sh
python3 scripts/validate_resources.py
python3 docs/validate_docs.py
python3 scripts/generate_recipe_book.py --check
```

After changing recipe resources, regenerate both catalogs:

```sh
python3 docs/generate_catalog.py
python3 scripts/generate_recipe_book.py
```

Some optional asset-generation scripts use additional Python tools; they are not required for the Gradle build.

## Project layout

```text
src/main/java/       Gameplay, registries, entities, stations, networking
src/client/java/     Rendering, screens, key bindings, JEI integration
src/main/resources/ Models, textures, animation, audio, recipes, worldgen
docs/               Field guides and generated crafting books
lore/               Main canon and the Fire Realm storyline
scripts/            Asset generators and resource/document checks
pack/               Additional authored data-pack resources
concepts/           Preserved design and implementation notes
gradle/             Gradle wrapper
```

The mod ID and Java namespaces remain **`opusvsexe` / `com.opus`** for compatibility. Regeneration scripts use `src/main/resources` as their recipe source; the build packages that resource tree.

## About the project and contributions

Exotron was made by a **team of students** as a practical Java project. Entities, equipment, interfaces and separate gameplay systems gave us a way to work with classes, inheritance, encapsulation and communication between components. That experience with organizing a larger project is useful beyond Java too.

For bugs, [open an issue](https://github.com/Irisko007/Exotron/issues) with the Minecraft/Fabric/mod versions, reproduction steps and a relevant log excerpt. See [CONTRIBUTING.md](CONTRIBUTING.md) before changing code or generated catalogs.

## License and credits

The supplied source tree contains the **CC0-1.0** [LICENSE](LICENSE), and the same identifier in the mod metadata; both are preserved here. Individual third-party assets and dependencies retain their own notices. See [CREDITS.md](CREDITS.md), including the difference between the source license metadata and the public distribution listing.

Exotron is an independent Minecraft mod project, not an official Mojang or Microsoft product.
