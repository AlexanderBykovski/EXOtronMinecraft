#!/usr/bin/env python3
"""Focused integrity checks for the static documentation site."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent


class ArchiveParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.fragments: list[str] = []
        self.files: list[str] = []
        self.images_without_alt: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and values.get("href", "").startswith("#"):
            self.fragments.append(values["href"][1:])
        for attribute in ("src", "href"):
            value = values.get(attribute, "")
            if value and not value.startswith(("#", "http:", "https:", "data:")):
                self.files.append(value)
        if tag == "img" and not values.get("alt"):
            self.images_without_alt.append(values.get("src", "unknown"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_catalog() -> dict:
    text = (DOCS / "catalog.js").read_text(encoding="utf-8").strip()
    prefix, suffix = "window.OPUS_CATALOG = ", ";"
    require(text.startswith(prefix) and text.endswith(suffix), "catalog.js wrapper drifted")
    return json.loads(text[len(prefix):-len(suffix)])


def main() -> None:
    parser = ArchiveParser()
    parser.feed((DOCS / "index.html").read_text(encoding="utf-8"))
    require(len(parser.ids) == len(set(parser.ids)), "duplicate HTML ids")
    require(not (set(parser.fragments) - set(parser.ids)), f"broken fragment links: {set(parser.fragments) - set(parser.ids)}")
    missing_files = [path for path in parser.files if not (DOCS / path).exists()]
    require(not missing_files, f"missing local HTML assets: {missing_files}")
    require(not parser.images_without_alt, f"images without alt text: {parser.images_without_alt}")

    catalog = load_catalog()
    recipe_count = len(list((ROOT / "src/main/resources/data/opusvsexe/recipes").glob("*.json")))
    trophy_count = len(list((ROOT / "src/main/resources/assets/opusvsexe/textures/item").glob("trophy_*.png")))
    require(len(catalog["recipes"]) == recipe_count == 153, "recipe catalog drifted")
    require(len(catalog["trophies"]) == trophy_count == 26, "trophy catalog drifted")
    require(len(catalog["entries"]) >= 250, "item/block compendium is unexpectedly incomplete")
    require(len({(entry["kind"], entry["id"]) for entry in catalog["entries"]}) == len(catalog["entries"]), "duplicate compendium entries")
    assembly = next(recipe for recipe in catalog["recipes"] if recipe["id"] == "opus_assembly_table")
    require(assembly["pattern"] == ["GCG", "F#F", "PPP"], "Opus Assembly Table recipe drifted")
    require(assembly["key"]["#"]["id"] == "minecraft:crafting_table", "Opus Assembly Table base key drifted")
    exo_frame = next(recipe for recipe in catalog["recipes"] if recipe["id"] == "exo_assembly_frame")
    require(exo_frame["pattern"] == ["TFMFT", "FESEF", "MSOSM", "FESEF", "TFMFT"],
            "EXO Assembly Frame recipe drifted")
    require(sum(1 for recipe in catalog["recipes"] if "pattern" in recipe and len(recipe["pattern"]) == 5) == 6, "5x5 recipes were truncated")
    require(sum(1 for recipe in catalog["recipes"] if recipe["type"] == "Opus Assembly Table") == 6,
            "assembly recipes have the wrong station type")
    guide = (DOCS / "guide.html").read_text(encoding="utf-8")
    require("Haiku Omega" in guide and "id=\"assembly-table-recipe\"" in guide, "guide highlights drifted")
    missing_catalog_assets = [record["image"] for group in ("recipes", "trophies", "entries") for record in catalog[group]
                              if record.get("image") and not (DOCS / record["image"]).exists()]
    require(not missing_catalog_assets, f"missing generated catalog assets: {missing_catalog_assets[:5]}")
    css = (DOCS / "styles.css").read_text(encoding="utf-8")
    require(css.count("{") == css.count("}"), "unbalanced CSS blocks")
    print(f"DOCS_SITE_OK sections={len(parser.ids)} recipes={recipe_count} trophies={trophy_count} entries={len(catalog['entries'])}")


if __name__ == "__main__":
    main()
