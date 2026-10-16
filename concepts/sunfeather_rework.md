# Sunfeather — rework concept (2026-09-03)

## Source
- Item `opusvsexe:sunfeather` (plain `Item`, Paradise tab). Drop: Sunfinch 1–2.
- Old sprite: plain ivory feather, no family identity, no link to the bird.

## Bird reference (entity texture palette)
- Golds: (242,185,59) light, (218,166,53) body, (202,111,28) bronze shade,
  (161,88,24) deep shadow.
- Accent: pale sky-cyan (191,233,239) wing/belly.

## Concept
A Sunfinch flight feather caught mid-glow: golden vane in the bird's own
golds with bronze barb slits, pale cyan quill (the finch's accent color),
one ruby glint at the vane base for the Paradise family
(ivory marble / sacred gold / ruby). Diagonal pose, quill bottom-left —
reads instantly at 32px next to cloud_fleece (white puff) and
paradise_fruit (round gold).

## Execution
- `scripts/generate_opus_ingredients.py: paint_sunfeather`, in place at
  `textures/item/sunfeather.png`. Old sprite backed up to
  `build/tool_backup/`. No code/model/lang changes (visual-only).
