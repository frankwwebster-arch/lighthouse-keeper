# Kitchen Rebuild V2 amended state family

Date: 18 October 2026

## Outcome

Frank accepted the clean-slate Rebuild V1 direction subject to one correction:
the fridge door must be white so the appliance reads immediately as a fridge.
V2 makes that correction and builds the complete On/Broken family as localized
amendments to V1 rather than rerendering the kitchen.

Review route:

`/keeper-review/kitchen-rebuild-states-v2/`

The page provides three exact 772 × 224 canvases:

1. all eligible assets On;
2. all breakable assets Broken, including the approved broken bin;
3. an interactive intermingled-state mixer with per-asset selectors, standard,
   On, Broken, alternating and random presets.

## On states

- Kettle: static V1 object; small separate steam loop from the spout.
- Toaster: two browned toast tops; separate rising heat loop.
- Oven: steady warm internal light, roasting dish, turned controls and solid red
  indicator; no visible animation is added to the steady state.
- Basin: static V1 object; separate gentle water stream from the spout.

## Broken states

- Fridge: white door attached only at the lower hinge, contents visible through
  the gap, lower-left door corner on the real floor, flat puddle and separate
  slow drip/ripple loop. The low electrical buzz remains sound-only.
- Kettle: lid fully off on the worktop; separate larger steam-cloud loop.
- Toaster: blackened toast; separate connected smoke loop.
- Oven: attached door open/down, dark exposed cavity; separate connected
  billowing smoke and irregular red-indicator/internal-light flicker.
- Bowl: two recognisable smashed halves; no animation.
- Basin: failed outlet; separate forceful upward spray loop.

The table was not included in the requested V2 state list and therefore remains
the exact complete V1 standard table/chair in every preset.

## Animation and sound contract

Every new moving environmental effect is a reusable 40-frame, 4-fps,
ten-second transparent strip with isolated 120 × 144 cells and transparent
shared-edge gutters. The two approved V31 bin strips remain byte-identical.
Named SFX placeholders are stored in the candidate catalogue and exposed on
the page; V2 supplies no audio files.

## Boundaries and verification

V2 changes no Final/runtime file. Rebuild V1, the approved V28/V31 bin family,
and all earlier provenance remain immutable. Rollback means deleting only V2
source/raw/draft/review/archive/builder/verifier/documentation files.

Run:

```sh
npm run verify:kitchen-rebuild-states-v2
```

The gate pins source/output hashes, confirms V1 background/table and non-fridge
standard cells, verifies the white fridge, exact state dimensions, flat puddle,
On/Broken distinctions, 40-frame strip geometry/gutters/variation, native room
proofs, complete media preloading and content-addressed archive coverage.

Documentation audit completed against the delivered V1/V2 geometry, state
catalogue, review route, archive manifest and no-promotion boundary. The focused
gate, 179 repository tests, TypeScript check and production Next.js build pass.
