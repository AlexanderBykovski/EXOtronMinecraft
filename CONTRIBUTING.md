# Contributing to Exotron

Use JDK 17 and the checked-in Gradle wrapper. Preserve the `opusvsexe` identifiers used by saves, recipes and networking.

## Before changing gameplay

Read [agent.md](agent.md), the relevant design notes in [concepts](concepts/), and the [main lore](lore/lore.md). The [Fire Realm lore](lore/Fire%20Biom/LOR.md) is a separate storyline. Existing design notes describe intent; confirm actual behavior in the current code.

Keep rendering and client-only APIs in `src/client/java`. Gameplay, packet validation and persistent state belong in the main source set. Verify a dedicated-server launch when changing code shared by client and server.

## Recipes and generated documentation

Edit recipes in `src/main/resources/data/opusvsexe/recipes`. Do not edit the generated crafting books or `docs/catalog.js` directly.

```sh
python3 docs/generate_catalog.py
python3 scripts/generate_recipe_book.py
python3 scripts/validate_resources.py
python3 docs/validate_docs.py
python3 scripts/generate_recipe_book.py --check
./gradlew build
```

The recipe-book generator retains every authored JSON recipe, preserves 5×5 patterns and reads the three Resonance Forge transformations from Java. Update its translations if recipe types, totals or transformation timings change. Inspect `CRAFTING.md` and `docs/recipes.html` after regeneration.

## Reporting a bug

Include Minecraft, Fabric Loader, Fabric API and Exotron versions; a short reproduction; expected and actual behavior; and relevant `latest.log` or crash-report excerpts. State whether the problem occurs in single-player or on a dedicated server. Remove account tokens, session data and private server addresses from shared logs.

## Pull requests

Explain the player-visible change and how it was checked. Include generated documentation changes with recipe changes. Do not commit saves, runtime account files, caches, compiled output or local environment settings.
