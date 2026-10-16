# Gear, expedition and Paradise rework — design record

This document is the implementation contract for the 2026-09-01 rework.  It is
written before the mechanical and asset changes so that balance, abilities, and
visual decisions stay connected.

## Guardrails

* **Ember armour is removed.**  Its four item registrations, recipes, models,
  translations and bonuses must not remain accessible.  The separate Fire
  Demonic armour stays: it is a later volcanic end-game set, not a rename of
  Ember.
* The vanilla diamond floor is `3 / 8 / 6 / 3` armour, diamond durability,
  `2.0` toughness and mining level 3.  Every retained armour and tool family
  meets or exceeds that floor; Vein Fire tools keep their already-established
  diamond-level parameters as requested.
* Health is applied through a unique `MAX_HEALTH` attribute modifier, not by a
  coarse potion level.  Thus a fraction of the second, 20-HP health row is
  exact and cannot overwrite a potion supplied by another mod.
* A full suit alone unlocks its set ability.  A single piece may retain a
  narrow thematic passive (such as boots' feather falling); it never grants a
  full-set ability or permanent creative flight by itself.

## Health, armour and ability matrix

The extra-health amount is measured from the **second** vanilla row (20 HP).
Opus reaches exactly two rows total: its Health Boost changes from amplifier 9
(60 max HP) to amplifier 4 (40 max HP).  Its material and its other effects are
otherwise unchanged.

| Set | Base armour | Durability / toughness | Extra HP | Full-set identity and limits |
| --- | --- | --- | --- | --- |
| Shadow Assassin | 20 (diamond distribution) | 36×slot base, 2.0 | +5 (1/4 row) | Night vision and 15% speed; a brief, non-stacking speed/damage modifier.  It is scouting armour, not invisibility. |
| Vein Crust Fire | 20 | 34×slot base, 2.0 | +20/3 (1/3 row) | Fire resistance, lava safety and a short fire-wave active ability with its existing cooldown. |
| Briarweave | 20 | 34×slot base, 2.0 | +10 (1/2 row) | Clears poison and gives a modest regeneration pulse.  It protects an explorer in the undergrowth without duplicating Vestments' mobility. |
| Aerie Bronze | 20 | 34×slot base, 2.0 | +10 (1/2 row) | Slow Falling, water breathing and Feather Falling II boots.  This is the accessible aerial-exploration set. |
| Dark Forest Vestments | 20 | 38×slot base, 2.5 | +15 (3/4 row) | Night vision, Speed II, Strength I and Dolphin's Grace II; aimed twilight-step remains its 2.5-second cooldown active ability. |
| Parthenon Regalia | unchanged diamond-equivalent 20 | unchanged 33×slot base, 2.0 | +15 (3/4 row) | Keeps intrinsic Protection III, chestpiece flight and the aimed Hurricane (15 s cooldown).  Health is made explicit in the shared modifier system. |
| Fire Demonic | 25 | 41×slot base, 3.5 | +20/3 (5/6 row) | Fire resistance, Strength I, Regeneration I and controlled flight granted only to a complete living suit.  It is the strongest non-Opus vitality set but remains below two full rows. |
| Opus | unchanged | unchanged | +20 (one full second row) | Existing resonant movement, regeneration, resistance, haste, water affinity and rage remain unchanged; only the health ceiling is reduced from three rows to two. |

The exact fractional values preserve the intended progression while avoiding an
illusory "half heart" from potion rounding.  Removing a suit removes only the
modifier/effects that this suit itself applied and caps current health to the
new maximum.

## Tool and sword matrix

**Vein Fire is deliberately excluded from stat changes.**  Its level-3 tier,
1800 durability, 9 mining speed and Furnace Touch / Fire Aspect identity stay
as they are.  It is still included in the texture pass below.

| Family | Tier / combat direction | Special behaviour |
| --- | --- | --- |
| Opus pickaxe, axe, shovel, hoe, warhammer and katanas | Existing late-game Opus tier is retained; the warhammer remains the slow heavy option and katanas remain the fast precision options. | No new stacking passive: their existing distinct weapon abilities remain the source of power. |
| Dark Forest sword and tools | Level 3, 1800 durability, 9 mining speed, +3 tier damage.  Sword 7 damage/1.6 attack speed; axe 9/1.0; pickaxe 4/1.2; shovel 4.5/1.0; hoe 1/4.0. | Intrinsic Haste III while held is retained, with normal enchantment compatibility. |
| Parthenon sword and tools | Level 3, 1800 durability, 9 mining speed, +3 tier damage.  Sword 7 damage/1.6; axe 8/1.0; pickaxe 4/1.2; shovel 4.5/1.0; hoe 1/4.0. | Tools retain intrinsic Efficiency IV; the sword stays a clean combat weapon rather than silently gaining a mining enchantment. |

## Paradise ecology and rare wildlife

* A Paradise Sapling accepts ordinary bone meal whenever its generated crown
  has room.  Bone meal has the vanilla sapling-style 45% success roll, rather
  than a hidden custom item requirement.
* Paradise leaves use the oak-apple loot condition: 0.5% base chance for a
  Paradise Fruit, with the same Fortune growth (`0.005 + 0.001 × level`, capped
  at 1.0).  Shears and Silk Touch preserve the leaves and do not also yield a
  fruit.
* Natural wildlife becomes an Overworld-wide rare ambient event.  Sunfinches
  may settle on a tree canopy or appear in clear sky.  Cloud Grazers require a
  leaf canopy below their feet.  Paradise Wyverns may appear above a canopy or
  in open sky in the cloud band (Y=112–160), and receive a persistent aerial
  roaming goal that keeps untamed adults in that band.  Spawn weights are low
  (Sunfinch 2, Grazer 1, Wyvern 1), group size is one, and validation prevents
  underground, water, enclosed and non-leaf Grazer spawns.

## Expedition compasses and Survivor stock

Every registered data-driven structure receives a distinct Expedition Compass:
Trial Grounds, Survivor Settlement, Paradise Island, Moon Fountain, Kimi
Laboratory, Japanese Settlement, Haiku Citadel, Frontier Fortress, Eternal
Colosseum, Data Spire, Coddy Workshop, and Abandoned City.  A compass locks to
the nearest structure of its own one-entry structure tag; none use a broad
"any Opus ruin" fallback.

Survivors roll one of four supply roles when their trades are first created:

* **Scout:** bread, torches and the surface exploration routes.
* **Archivist:** paper, lanterns and laboratory/citadel routes.
* **Quartermaster:** iron, food and fortress/colosseum routes.
* **Wayfinder:** maps, compasses and the remaining difficult routes.

Each role has a guaranteed useful survival offer, a different rotating set of
three compasses, and no duplicate offers.  Across an ordinary settlement the
complete route catalogue is therefore available without every Survivor having
the same inventory.

## Tool-art pipeline

The first-stage material/silhouette reference is
[`tool-family-reference-2026-09-01.png`](assets/concepts/tool-family-reference-2026-09-01.png),
generated with the built-in image-generation workflow.  It is a concept sheet,
not an in-game asset.  The companion weapon study is
[`weapon-family-reference-2026-09-02.png`](assets/concepts/weapon-family-reference-2026-09-02.png).

### Individual silhouette cards

Each named item has a distinct card below before it is translated into pixels;
this prevents the five tool types in a family from becoming the same diagonal
stick with a recolour.

| Item(s) | 16×16 art concept and identifying pixels |
| --- | --- |
| Opus warhammer | A compact 5×4 gunmetal striking block around a violet core; a short, dark wrapped handle and one magenta pommel pixel make it feel heavy rather than like an axe. |
| Opus pickaxe | Forked two-prong head cut from violet crystal; one bright facet sits at the join, with the dark shaft deliberately longer than either prong. |
| Opus axe | Broad, squared crystal wedge with a stepped rear edge; the single pink rivet anchors it to the gunmetal handle. |
| Opus shovel | Narrow crystalline spade, pointed at the upper-right and shaded dark along the lower edge. |
| Opus hoe | Open hook with a one-pixel break under the tip so it is never mistaken for a pickaxe. |
| Vein Fire sword | Straight charcoal blade with only a thin ember seam—orange is an accent, never a glowing full blade. |
| Vein Fire pickaxe | Asymmetric blackstone pick head with one orange furnace crack at the socket. |
| Vein Fire axe | Heavy chipped volcanic wedge; the orange fracture terminates inside the head instead of becoming a smooth flame. |
| Vein Fire shovel | Rounded dark spade with a warmer, worn top rim and a single ember at its neck. |
| Vein Fire hoe | Lean dark hook, with the ember point placed at the bend for a readable farming silhouette. |
| Dark Forest sword | Thorned violet blade with a quiet cyan rune at the guard; the cutting edge remains straight enough to read as a sword. |
| Dark Forest pickaxe | Thorn-like opposing prongs around a cyan socket, on a muted gloomwood grip. |
| Dark Forest axe | Leaf/axe hybrid wedge, its lower edge darker and one cyan knot near the haft. |
| Dark Forest shovel | Moonlit pointed spade; cyan is limited to the neck instead of an oversized glow. |
| Dark Forest hoe | Curved briar hook with a darker inner curve, visually separate from the pickaxe prongs. |
| Parthenon Xiphos | Ivory straight blade, aged-gold crossguard and a small turquoise inset; white highlights are sparse to keep it stone rather than chrome. |
| Parthenon pickaxe | Marble-and-gold fork with the turquoise inset placed where the two prongs meet. |
| Parthenon labrys | Broad twin-sided marble axe head, but condensed to a single readable Minecraft wedge at icon scale. |
| Parthenon shovel | Cream marble spade, gold collar and turquoise neck pixel, with the silhouette kept no wider than a vanilla shovel. |
| Parthenon hoe | Gold-rimmed marble hook; its pale outer rim contrasts with a darker gold inner edge. |
| Steel katana | Slim stepped steel edge, black wrap and muted brass guard; shorter length communicates the one-handed version. |
| Long katana | The same material language with a longer continuous blade path and grip, not an enlarged or rotated ordinary katana. |
| Opus katana | Violet crystalline blade with a restrained pale magenta edge and a dark wrapped handle. |
| Gold katana | Deep gold blade/body progression, orange-gold guard inset and a brown shadow to prevent flat yellow noise. |
| Refined katana | Silver-lilac blade with one cool cyan refinement point; it is the cleanest, least thorned Opus katana. |

The final sprites follow these non-negotiable vanilla constraints:

1. One transparent **16×16** PNG per named sword, pickaxe, axe, shovel and hoe.
2. A 1-pixel near-black outline, 3–5 material colours plus one controlled
   highlight; never smooth gradients, photoreal shading, text or baked glow.
3. The canonical diagonal handheld silhouette: grip at lower-left, working
   end upper-right.  Sword blades stay straight, pick heads form a readable T,
   axes a wedge, shovels a rounded spade, and hoes an open hook.
4. Each family is identified through material rather than a different shape
   language: Opus violet crystal/gunmetal; Vein Fire charcoal/ember; Dark
   Forest gloomwood/thorned violet with one cyan gem; Parthenon marble/gold
   with a cyan inset.
5. Every tool model uses `minecraft:item/handheld`; this preserves Minecraft's
   held-item transform in first person, third person and on armour stands.

The concept sheet was used only to select material hierarchy and silhouette;
the supplied final icons are deliberately hand-authored at the target pixel
resolution for the Minecraft style.  The final nearest-neighbour inspection
sheet is [`vanilla-tool-texture-sheet-2026-09-02.png`](assets/concepts/vanilla-tool-texture-sheet-2026-09-02.png).
