# Codex → Claude: Kitchen final assets V21

**Date:** 17 October 2026

**Base:** commit `2d67163`, Kitchen fitted-galley V20

**Status:** complete final candidate awaiting Frank's visual acceptance

**Review:** `/keeper-review/kitchen-final-assets-v21/`

## Frank's V20 review resolved

- The V20 double oven is retained as Upgrade 1.
- The basic oven is now a compact, narrower, single-door appliance inside the
  unchanged standard cabinet bay, following the functional simplicity of V5.
- A simple standalone pedal bin is included.
- The table for one has exactly one chair and is rebuilt around the exact
  side-right V6 seated geometry.
- A full `193 × 56-lp` room shows every basic asset in situ; a toggle swaps only
  the oven bay to the Upgrade 1 room.

## Binding geometry

- density: `4 source px = 1 lp`;
- cabinet bay: `21 lp = 84 px`;
- rear-wall foot line: `52 lp = 208 px`;
- clear foreground: `4 lp = 16 px`;
- basic oven appliance inset: about `15 lp`, one door;
- pedal bin: `10 × 13 lp`;
- V6 chair support: `7.75 lp`;
- V6 chair depth: `8.625 lp`;
- V6 seat-rim/shin clearance: `0.5 lp`;
- table top: `14.5 lp`, `1.5 lp` thick, `20 lp` span.

The table-height proof composites the exact final V6 seated Keeper between the
chair and table layers. His hands meet the cyan 14.5-lp tabletop datum and the
yellow 7.75-lp support line meets the corrected chair seat.

## Source and build

Three built-in OpenAI image-generation calls produced versioned transparent
sources for the basic oven, bin and table/chair. Their exact prompts and hashes
are in
`art/source/kitchen-final-assets-2026-10-17-v21/IMAGEGEN_PROMPTS.md`.

`scripts/build_kitchen_final_assets_v21.py` performs all normalization and room
assembly. It copies six accepted V20 appearances, retains the V20 oven as the
upgrade, locks the three new assets to measured dimensions, writes the full
room and V6 fit proof, and creates the review page/data/register.

`scripts/verify_kitchen_final_assets_v21.mjs` pins every source and output and
tests the geometry, alpha isolation, fitted-run worktop joins, foreground
channel, oven-only room variation, review copy and archive manifest.

## Delivery boundary

V21 completes the visual asset set but does not overwrite V20 or promote art
into `public/sprites/manifest.json`. Keeper images and animation registers are
unchanged. Promotion/wiring remains a separate explicit step after Frank's
visual acceptance.
