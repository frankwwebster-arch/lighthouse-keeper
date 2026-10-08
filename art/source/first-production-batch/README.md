# First production Pixel batch — source notes

Generated on 8 October 2026 with the built-in ImageGen tool. The existing
`art/background/lighthouse_master_day_pixel.png` concept plate was supplied as
a **style reference only**. No pixels were cropped or sliced from it.

The untouched generated sources in this directory map to the runtime exports:

| Source | Runtime export | Exact export size |
|---|---|---:|
| `tower_stripe_red_source.png` | `art/raw/first-production-batch/tower_stripe_red.png` | 110 × 8 |
| `tower_stripe_white_source.png` | `art/raw/first-production-batch/tower_stripe_white.png` | 110 × 8 |
| `room_kitchen_source.png` | `art/raw/first-production-batch/room_kitchen.png` | 105 × 35 |
| `room_living_source.png` | `art/raw/first-production-batch/room_living.png` | 105 × 35 |
| `room_bedroom_source.png` | `art/raw/first-production-batch/room_bedroom.png` | 105 × 35 |

Run `scripts/build_first_asset_batch.py` with the bundled Codex Python runtime
and Pillow to reproduce the exact-size files in `art/raw/`. The script crops
generated transparent margins, resizes with nearest-neighbour sampling, limits
each asset to 32 colours, and converts edge alpha to hard transparent/opaque
pixels. Then run `npm run sprites` to validate and publish them to
`public/sprites/` through the repository's standard sprite pipeline.

## Prompt set

All prompts requested newly drawn, flat front-on pixel art with dark
`#14243A`-family outlines, centered lighting, no perspective, text, characters,
watermarks, anti-aliasing, blur, or copied pixels.

- `room_kitchen`: warm cream plaster, timber floor/beam, small shelf and hooks;
  architecture and non-interactive dressing only, with clear space for separate
  fridge, cooker, broom, pet bowl and door sprites.
- `room_living`: sea-green plaster, timber floor/beam, framed sea chart and
  restrained nautical trim; no TV, bookshelf, piano, sofa, chair or rug.
- `room_bedroom`: pale-lavender bedroom on the left and sea-glass en-suite on
  the right, divided at about 72% by a partition and open doorway; no bed,
  phone, desk, basin or toilet.
- `tower_stripe_red`: seamless 13.75:1 untapered horizontal shell band in the
  `#C8463C` family, with restrained pixel highlights and a dark lower edge.
- `tower_stripe_white`: matching seamless shell band in the `#F3E7CC` family.

This directory deliberately contains no keeper, object-state, effects,
lamp-room, exterior, extension, or later-floor artwork.
