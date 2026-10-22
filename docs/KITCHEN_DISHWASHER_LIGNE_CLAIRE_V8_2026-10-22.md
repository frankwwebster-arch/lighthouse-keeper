# Kitchen Dishwasher Ligne-Claire V8 — 22 October 2026

## Status

Immutable review candidate. Not approved, registered, promoted or wired.

## Why V8 exists

V7 fixed the duplicate worktop, but still shrank the complete glossy
high-resolution reference into the `98 × 82 px` game cell. That carried bright
cyan shine strokes into both cabinet-blue side rails and softened sub-pixel
linework. Its cream fascia and door also remained too wide and too close to the
worktop beside the approved oven.

## V8 construction

- retains all 15 exact V41 canvases and byte-exact alpha channels;
- retains the exact approved worktop and both cabinet-side shoulders;
- rebuilds visible appliance pixels as density-16 game art with deliberate
  one- and two-pixel native contours rather than mechanically shrinking the
  full generated reference;
- removes high-luminance cyan shine from the vertical side rails;
- insets the fascia and door to native x `19..79` inside the 84-pixel bay;
- lowers the fascia to native y `21..31.5`;
- aligns dishwasher control centres at y `25.5` with the approved oven's
  measured y `25.4`;
- keeps the lower-right Broken hinge failed, lower-left hinge attached, door
  visibly open and slender handle hanging from its left boss;
- keeps suds as a separate dishwasher-owned forty-frame floor effect.

The V7 image-generation references are copied byte-for-byte into the V8 source
directory as reversible art-direction provenance. V8 does not overwrite them
and does not use their glossy outer rails as production pixels.

## Review and verification

- Standalone: `/keeper-review/kitchen-dishwasher-ligne-claire-v8/`
- Integrated: `/keeper-review/kitchen`
- Verify: `npm run verify:kitchen-dishwasher-ligne-claire-v8`

The verifier rejects canvas/alpha drift, worktop or shoulder drift, unchanged
V7 candidates, a return of bright cyan rail flashes, archive mismatches or an
opened registration gate.

Rollback is deletion of the V8 source, draft pack, archive set and review shell
only. V1–V7, V41, approved assets and production remain untouched.
