# Kitchen Dishwasher Ligne-Claire V4

Status: immutable review candidate; not approved, registered, promoted or wired.

Review: `/keeper-review/kitchen-dishwasher-ligne-claire-v4/index.html`

V3 is preserved and rejected: its measurements improved, but it still read as
a separately designed appliance beside the approved oven and cabinets. V4 is
judged first as a member of the full cabinet–dishwasher–oven run.

## Construction

- All 15 Off/On/Broken and join variants retain the exact V41 `98 × 82 px`
  canvas and alpha bytes.
- The full matching Cabinet V3 countertop assembly is copied byte-for-byte
  through source row `16`, including the dark underside/front return omitted
  by V3.
- The face uses the oven family's warm enamel, long slender copper handle
  rhythm and compact fascia hierarchy. Blue side stiles and the plinth retain
  the fitted-cabinet construction.
- Off/On vary only their indicators. Broken preserves the stationary carcass
  and uses the same handle weight on the detached door.
- Production pixels are deterministic 16× masters reduced with LANCZOS and
  then registered to the exact V41 alpha. The image-generation study is art
  direction only and is never inserted into a sprite.

Primary evidence is
`art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v4/evidence/dishwasher-worktop-run-ghost.png`:
it shows the clean fitted run before the diagnostic alpha ghost. Rejection is
reversible by discarding only the V4 draft, public shell and archive-set file.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v4
```

The verifier checks the closed registration gate, all 15 canvas/alpha pairs,
the complete worktop assembly for every edge state, hashes, content-addressed
review objects and root-absolute delivery.
