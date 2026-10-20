# Kitchen Standalone Oven V28 — perspective and fixed-shelf correction

Date: 20 October 2026  
Status: reversible, unapproved, unpromoted review draft

## Purpose

V28 retains Oven V27's approved coordinated Off, On and Broken design while
correcting the two issues identified during installed review:

- the hob now uses the shallow, near-parallel flat-cutaway projection of the
  approved Cabinet V11 worktop; and
- the burnt roast and roasting dish in Broken remain on the fixed interior
  shelf at the same height as the On-state dish. The bottom-hinged door opens
  straight toward the camera as a separate foreground flap and carries no
  oven contents.

## Locked geometry

- logical body: `84 × 77 px`
- isolated cell: `92 × 85 px`, with a transparent four-pixel gutter
- installed body: `x=336–420`, `y=131–208` in the `772 × 224 px` room
- Prime interaction anchor: `(378,218)`
- adjacent Cabinet V11 runs and room background: unchanged authorities

The deterministic builder may replace only body rows `0–15` in every state
for the shallow hob and body rectangle `x=8–75`, `y=26–66` in Broken variants
for the fixed-shelf correction. Verification rejects every V27 pixel change
outside those declared regions.

## State and motion contract

Off, On and Broken retain V27's state meanings. Broken still has the
straight-toward-camera transparent door, blackened roast, and failed dial on
two wires. The cavity and red warning lamp retain V27's independent irregular
40-frame, 4-fps, ten-second schedules, can be removed independently and can be
previewed at `0.1×–4×`. Every combination swaps a complete precomposed room
image; no browser canvas clearing can damage neighbouring cabinets.

Smoke remains a separate reusable environmental effect. No smoke, sparks or
electrical flash is baked into the oven.

## Review and verification

Review route: `/keeper-review/kitchen-oven-standalone-v28/`

Run:

```sh
python3 scripts/build_kitchen_oven_standalone_v28.py # requires Pillow
npm run archive:keeper-review:set -- art/drafts/kitchen-oven-standalone-2026-10-20-v28/batch-register.json HEAD
npm run verify:kitchen-oven-standalone-v28
```

The verifier checks source and authority hashes, exact dimensions and gutters,
the two allowed edit regions, V27 lighting schedules, identical Off/On alpha,
complete-room neighbour preservation, archive integrity, preloading and the
absence of `clearRect` compositing.

## Boundary

V27 remains immutable approved state-family provenance. V28 has not been
approved or promoted into Final/runtime, and no later kitchen asset is started
by this batch.
