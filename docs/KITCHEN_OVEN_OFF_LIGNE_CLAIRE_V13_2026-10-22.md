# Kitchen Oven Off Ligne-Claire V13

Status: immutable reversible review candidate; not approved, promoted or wired.

Review route: `/keeper-review/kitchen-oven-off-ligne-claire-v13/`

## Decision

V13 adds the missing intact Off member without redrawing the oven. It starts
from the exact approved V8 On master, removes the cavity and warning-lamp
illumination deterministically, then registers those two lighting regions into
the exact approved V8 native image. Approved V8 On and approved V12 Broken are
copied byte-for-byte into the review family evidence.

The image-generation workflow was considered, but the edit is a bounded state
change with exact source pixels and masks. A generative redraw would add drift,
so none was used.

## Hard invariants

- Canvas remains `92 × 85`; alpha bounds remain `(4,4)–(88,81)`.
- Alpha, transparent padding, silhouette, perspective, proportions, controls,
  burners, countertop, handle, door, tray, roast, plinth and datum are exact V8.
- Zero pixels differ from V8 On outside the cavity mask
  `[16,34]–[78,65]` and warning-lamp mask `[70,20]–[80,31]`.
- The Off cavity and warning lamp are dark; the oven is intact rather than
  Broken.
- No animation, timing, anchor, pivot, collision, movement, interaction,
  handling, repair or healing process changed.
- V8, V12, source, production, Final and runtime files remain untouched.

## Review and approval gate

The review page presents the approved V8 On, V13 Off and approved V12 Broken
as one family, a live On/Off opacity ghost and a complete current-versus-
candidate Off contact sheet. All image URLs are root-absolute and every image
is decoded before the opacity control is enabled, so Vercel's slashless route
cannot break relative asset resolution.

`batch-register.json` is closed with `register:false`, `promote:false` and no
selector changes. Explicit approval is required before V13 can become an
approved visual authority. Rollback is immediate by discarding only this V13
pack, builder, review route and delivery record.

## Verification

```sh
npm run verify:kitchen-oven-broken-ligne-claire-v12-approval
npm run verify:kitchen-oven-off-ligne-claire-v13
npm run maintain:keeper-review
npm test
npm run build
```

## Documentation audit

README, STATUS, DECISIONS, package scripts and this record agree that V8 On and
V12 Broken are approved visual authorities, while V13 Off is a fresh closed
review candidate. No production selector or runtime behaviour changed.
