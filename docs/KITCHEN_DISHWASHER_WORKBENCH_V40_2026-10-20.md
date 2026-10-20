# Kitchen Dishwasher Workbench V40

V40 is the reversible correction to Dishwasher V39. It changes only the
dishwasher worktop construction and retains V39's appliance bodies, state
geometry, movable-grid behaviour and reusable suds library.

Review: `/keeper-review/kitchen-dishwasher-workbench-v40/`

## Correction

V39's generated turquoise cap used a heavier dark outline and appeared one
native row too high beside approved Cabinet V11. V40 removes cell rows `4–15`
from each V39 dishwasher state and replaces them with the exact corresponding
`84 × 12 px` Cabinet V11 worktop crop. Every pixel outside those twelve rows is
required to remain byte-identical to the matching V39 state.

The dishwasher now has twelve derived state/edge sprites:

- Off, On and Broken;
- left exposed/right exposed;
- left exposed/right joined;
- left joined/right exposed;
- left joined/right joined.

The live compositor selects the appropriate edge version after every move.
Exposed ends retain the approved rounded Cabinet V11 finish; joined ends use
the exact internal worktop rows before the existing V22 flat or V32 oven join
repair is applied. The appliance remains an independent `84 × 74 px` body with
the same x origin and Prime midpoint.

## Review behaviour retained

All six units remain independently movable and dropping onto an occupied bay
swaps the two bodies. The review still exposes Off, On and Broken controls and
the reusable compact/regular/emphatic dishwasher-suds family. Each suds model
is a separate isolated forty-frame, 4-fps, ten-second strip with multiple
placement, drag, resize, crop, speed and removal controls.

## Source and reversibility

The targeted built-in image edit is retained under
`art/source/kitchen-dishwasher-workbench-2026-10-20-v40/generated/` as visual
source evidence. Final V40 state bodies deliberately inherit exact V39 pixels;
only the deterministic Cabinet V11 worktop substitution ships to review.
V39 remains immutable. V40 does not change approved cabinetry, Final or
runtime assets and performs no promotion.

## Verification

Run:

```sh
npm run verify:kitchen-dishwasher-workbench-v40
```

The verifier checks all twelve state/edge variants against their exact Cabinet
V11 source rows, requires all non-worktop pixels to equal V39, audits the
forty-frame suds gutters, enumerates all 720 six-object arrangements, checks
preload/decode gating and validates the content-addressed review manifest.
