# Kitchen v7 image-generation record

Tool: OpenAI built-in image-generation/edit tool.

Mode: whole-room stylised concept/edit with explicit local references. No web
image was used. The source art remains review-only.

## References supplied

| Reference | Purpose | SHA-256 |
|---|---|---|
| `sources/structural-shell-2x.png` | exact 4096 × 1152 room, window and slab geometry | `b894412271ac49011374ab36f250dbfd54b21cd85fd8ace11dd72fbd66664cc3` |
| `review/kitchen-proof-v3-rebuild/sources/approved-style-calibration.png` | approved line density, bevels, material weight and finish | `99efc21c386422683f734d2d8dd559a5bcebba43e933b1a272360965420de7a5` |
| `reference/kitchen-mood/kitchen-mood-01.png` | primary 1950s palette, diner set, checkerboard and cabinet mood | `324a3c48e7c4df044f4fc571680563526c1cf27d1c0709c8ca7b08e7e7588d34` |
| `reference/kitchen-mood/kitchen-mood-07-cooker.png` | cooker construction authority | `a7575cdc4750c66254980fbeaa9ef7af433ca9485d19e8492fe3985ef0e3fff4` |
| `review/kitchen-proof-v3-rebuild/sources/v7-oven-authority.png` | oven/window/detail authority | `0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538` |

The Prime Keeper was **not generated**. It was composited afterward from
`review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png`
(SHA-256 `a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3`).

## Pass 01 — whole-room paint

Final prompt contract:

> Paint one complete 2048 × 576 front-elevation Lighthouse Keeper kitchen over
> the supplied structural shell. Preserve the shell's straight-on elevation,
> two magenta four-pane windows, ceiling/floor slabs, side jambs and empty
> front walk strip. Match the approved calibration's adult-playful modern
> ligne-claire finish: confident organic near-black outline, crisp shapes,
> substantial layered enamel edges and material detail, bright clean fills and
> restrained inner modelling. No cast or floor shadows, no perspective floor,
> no gradients or airbrushed atmosphere. Make a harmonious unfitted 1950s set,
> left to right: low rounded counter-height cream fridge; duck-egg Belfast sink
> cabinet; separate duck-egg kettle cabinet; tall cream gas cooker with four
> black-supported burners, four copper/orange knobs, dark unlit oven window,
> long handle and eye-level grill from the cooker reference; chrome diner table
> and two red chairs under the right window; separate toaster cabinet; separate
> mixer cabinet; cream pedal bin. Add matching decorative wall cupboards only
> above the fridge and the three small cabinets, never over windows or cooker.
> Use copper handles, black-and-white flat checkerboard rows and no royal blue.
> Put no character in the generated art. Leave all appliance lamps unlit.

Result: `sources/kitchen-v7-free-pass-01.png`.

## Pass 02 — shadow and oven correction

> Edit only the supplied whole-room kitchen. Remove every cast/contact shadow
> from wall and floor while preserving material modelling inside objects.
> Change the oven to a closed door with a dark partial-tint window through which
> the complete cavity linework and shelves can be seen; no baked-in glow. Keep
> the eye-level grill, all room geometry, furniture and palette unchanged. Add
> clear copper/orange cooker knobs and visible but unlit lamp hardware. Do not
> add a character.

Result: `sources/kitchen-v7-free-pass-02.png`.

## Pass 03 — cooker controls and status hardware

> Preserve the room exactly. On the cooker control strip, show exactly four
> copper/orange round knobs, then two separate small dark/unlit bezels to their
> right: one heat-indicator bezel and one universal status-lamp bezel. Remove
> any illuminated red or green dots. Ensure the fridge, kettle, toaster and
> mixer each have one small dark/unlit status bezel. Change nothing else.

Result: `sources/kitchen-v7-free-pass-03.png`.

## Pass 04 — fridge scale correction

> Preserve every pixel-level design decision and all objects except the
> refrigerator. Replace only the left cream refrigerator with a low, rounded,
> single-door counter-height 1950s fridge; keep its cream enamel, copper handle
> and unlit status bezel. It must clearly be shorter than the sink worktop and
> leave the wall cupboard above it separate. Do not change the room, cooker,
> windows, cabinets, diner set, props or palette.

Result: `sources/kitchen-v7-free-pass-04-final.png`.

## Pass 05 — missing cabinet-2 wall cupboard

> Preserve the entire supplied kitchen exactly. Add one small matching
> duck-egg wall cupboard in the clear wall gap directly above the kettle
> cabinet, between the left window and cooker. It must have rounded enamel
> construction and one copper handle, remain entirely clear of the window and
> cooker/grill, and align visually with the existing decorative cupboards.
> Change nothing else.

Result and selected final source:
`sources/kitchen-v7-free-pass-05-final.png`.

## Deterministic post-process

`build_review.py` performs aspect normalisation, restores the exact structural
pixels and `#FF00FF`, and composites the unchanged Prime. It does not cut,
segment, re-ink, palette-snap or fabricate any item state.
