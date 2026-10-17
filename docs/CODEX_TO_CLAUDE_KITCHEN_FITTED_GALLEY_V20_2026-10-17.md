# Codex → Claude: Kitchen fitted galley V20

**Date:** 17 October 2026  
**Status:** new reversible appearance/construction gate awaiting Frank  
**Review:** `/keeper-review/kitchen-fitted-galley-v20/`

## Decision carried forward

Frank identified the fundamental problem with V5–V19: complete cabinet sprites
placed beside each other read as disconnected dolls-house furniture. V20 starts
a different fitted-galley family and does not promote any art. Frank then
removed from the review tools. V1–V4 and V6–V19 public routes and active archive
entries are gone, but their art trees, page bytes, manifests and media objects
remain retained offline. V5 remains the sole public old-family reference and
V20 remains the current replacement gate.

The approved-for-review direction is:

- storm-blue fronts;
- pale sea-glass worktop;
- aged-copper hardware;
- dark navy outlines;
- occasional coral-red accents;
- straight-on rectangular cabinet architecture;
- rounded illustrative depth concentrated in countertop objects.

## What V20 contains

1. A transparent six-appearance sheet: undercounter fridge, oven/grill, kettle,
   toaster, mixing bowl/spoon and sink/faucet.
2. A `63 × 56-lp` room proof containing kettle, oven/grill and sink as one
   uninterrupted three-bay fitted run.
3. A measured recipe and a deterministic verifier.

The three-bay proof is exact at `252 × 224 px`: three `84-px` bays, rear-wall
foot line y=`208 px`, and rows `208–223` retained as a `4-lp` foreground walking
channel.

## Physical prop calibration

`60 cm = 21 lp`, so `1 lp = 2.857142857 cm`.

| Prop | Real width | Exact conversion | V20 target | Measured V20 appearance |
|---|---:|---:|---:|---:|
| Kettle | 18 cm | 6.3 lp | about 7 lp | 28 px / 7 lp |
| Toaster | 28 cm | 9.8 lp | about 10 lp | 37 px / 9.25 lp |

The toaster remains within the intended approximate ten-lp envelope; any final
overlay can be standardized at exactly 40 px after visual acceptance.

## Source and output identities

- `art/source/kitchen-fitted-galley-2026-10-17-v20/isolated-six-appearance-source.png`
  - SHA-256 `971cb7d0047c380fbdf1561a06e8d64dcef1e6b20327ec0c0263ebaa49c9db81`
- `art/source/kitchen-fitted-galley-2026-10-17-v20/three-bay-fitted-run-source.png`
  - SHA-256 `b1af0ccf926adb6b24b0596eeeac056ff1b32ab14e7ab87560ee7ba44fad3b9a`
- `art/raw/kitchen-fitted-galley-2026-10-17-v20/isolated-six-appearance-grid.png`
  - `324 × 240 px`, SHA-256 `2348325e75d82f09116914b774de084e19d2f52728d19db3edb4e1aaacb9a88d`
- `art/raw/kitchen-fitted-galley-2026-10-17-v20/three-bay-fitted-room.png`
  - `252 × 224 px`, SHA-256 `5730e51c07c3c0baa38fbc537fc542179ea427bf0870eff0576e6fad5d8a7a57`

The isolated source was generated in one regular `2 × 3` layout. The builder
extracts visible alpha from each slot, scales each appearance to an exact
`84-px` width and places it in a `108 × 120-px` transparent review cell. The
joined proof is uniformly scaled—not stretched—to exactly `252 px` wide and
registered to the y=`208 px` foot line.

## Generation provenance

OpenAI image generation was used in new-generation mode. The isolated source
prompt requested six coherent storm-blue/sea-glass/copper front-elevation
appearances with transparent gutters. The final in-situ prompt preserved the
original approximately seven-lp kettle and changed only the sink assembly:
shorter practical faucet/taps and a smaller centred basin. It explicitly locked
the equal bays, continuous run, room, palette and orthographic construction.

The generated images were then copied into the repository and normalized only
by the deterministic Pillow builder. Originals remain in the local generated
image store; project-bound copies are the source of record above.

## Construction authority

The six isolated images answer “what does each appearance look like?” The
three-bay proof answers “how is it built?” Future production art must therefore
use shared run-wide worktop/highlight/fascia/plinth layers and end caps only at
the complete run's ends. It must not tile the isolated cards as complete pieces
of furniture.

The binding recipe is
[`KITCHEN_FITTED_GALLEY_V20_RECIPE_2026-10-17.md`](KITCHEN_FITTED_GALLEY_V20_RECIPE_2026-10-17.md).

## Verification and boundary

Run:

```bash
npm run verify:kitchen-fitted-galley-v20
npm test
```

The V20 verifier pins source/output hashes, exact room and bay dimensions,
transparent cell gutters, kettle/toaster scale, clear foreground floor and
cyan worktop continuity across both internal three-bay joins.

Nothing is approved, promoted or wired. V20 changes no Keeper animation,
register, manifest, Final art or live-game asset. Exact layered modules,
animation states, shelves, bin, porthole, cupboard and complete room remain
future gates after this fitted-galley direction is accepted. The obsolete
kitchen builders/verifiers remain only as historical source code; they are no
longer active npm commands and the retired outputs are not deployment inputs.

Retired review pages and per-set manifests live at
`review-archive/retired/kitchen-v1-v4-v6-v19/`. Their media objects remain in
the content-addressed object store but have no active legacy-path entry, so the
review resolver cannot publish them.
