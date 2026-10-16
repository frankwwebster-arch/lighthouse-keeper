# Kitchen V6 countertop calibration: Codex → Claude hand-back

**Date:** 16 October 2026

**Status:** first review gate only; reversible, unapproved and not wired

**Review page:** `/keeper-review/kitchen-countertop-calibration-v6/`

## Scope delivered

This is intentionally not the full Kitchen V6 family. It presents exactly
three shared countertop constructions on three representative exact-V5 units:
the kettle counter, cooker/hob and sink counter.

Kitchen Basic Assets V5 is the sole visual and geometric baseline. The removed,
rejected former V6 was not recovered, read, copied, transformed or imitated.
The V5 front below each declared countertop/hob mask is byte-identical in every
candidate. No animated state, room shell or other furniture asset has been
rebuilt.

## Room-grid fit

All candidates retain the precise V5 room-grid envelope:

- one 21-lp bay / 84 source pixels per unit;
- maximum asset width 20 lp / 80 source pixels;
- 0.5-lp transparent safety gutter on each side;
- a straight 1-lp ownership seam between neighbouring bays;
- unchanged 19-lp interaction datum and unchanged bottom-centre anchor;
- no overlap, rescaling or out-of-bay pixels.

The seam is intentionally visible in the review. Frank confirmed that spacing
is acceptable where the precise room-grid and sprite-isolation requirements
need it. The new construction removes the V5 wedge/taper: any spacing is
straight and constant from top to bottom.

| Unit | Native frame | Logical frame | Bay occupancy | Interaction/contact |
| --- | ---: | ---: | ---: | --- |
| kettle counter | 84 × 124 px | 21 × 31 lp | 1 × 21-lp bay | unchanged V5 19-lp worktop datum |
| cooker / hob | 84 × 112 px | 21 × 28 lp | 1 × 21-lp bay | unchanged V5 19-lp hob datum |
| sink counter | 84 × 116 px | 21 × 29 lp | 1 × 21-lp bay | unchanged V5 19-lp worktop datum |

Every native frame keeps transparent x=0 and x=83 edge columns. Candidate
opaque width is therefore at most 80 px / 20 lp inside the 84 px / 21-lp
ownership cell. The bottom-centre anchor and V5 interaction spot are inherited
without movement; this calibration changes only the declared top mask.

## Alternatives awaiting Frank's selection

| Option | Visible top | Rear/front edge | Shear | Fascia | Body |
| --- | ---: | ---: | ---: | ---: | --- |
| A | 1 lp | 20 / 20 lp | 0 lp | 2 lp | vertical, constant width |
| B | 1.5 lp | 20 / 20 lp | 0 lp | 2 lp | vertical, constant width |
| C | 2 lp | 20 / 20 lp | 0 lp | 2 lp | vertical, constant width |

All three retain a visible top surface, use horizontal equal-width front and
rear edges, have no vanishing point or rear-edge narrowing, and use one
construction across the ordinary counter, hob and sink. The review shows exact
V5 beside every candidate at native density-4 authoring scale, the same files
at exact logical game scale, ghost overlays, edge overlays and two-unit seam
proofs.

The next art pass must not start until Frank selects one treatment. That later
pass will apply the selected construction to the complete V6 family while
retaining V5 animation timing and pixel-identical stationary bases outside
declared effect masks.

## Reversible files

- Source record: `art/source/kitchen-basic-assets-2026-10-16-v6-calibration/`
- Candidate rasters: `art/raw/kitchen-basic-assets-2026-10-16-v6-calibration/`
- Review data and SHA register: `art/drafts/kitchen-basic-assets-2026-10-16-v6-calibration/`
- Immutable page: `public/keeper-review/kitchen-countertop-calibration-v6/`
- Builder: `scripts/build_kitchen_countertop_calibration_v6.py`
- Verifier: `scripts/verify_kitchen_countertop_calibration_v6.mjs`

The batch register records full original and candidate hashes plus protected
snapshots for Kitchen V5, the runtime sprite manifest, the animation workbench
Final state and the approved Keeper source family. The builder writes none of
those protected surfaces. Rejection remains reversible by discarding the three
new calibration directories and page alone.

## Verification and documentation audit

- deterministic double build: identical aggregate SHA-256
  `2f17580950b80d6e045b2bc6789270ee0586a21d29b2095f1398b0f1e24753dd`;
- `npm run verify:kitchen-countertop-calibration-v6`;
- `npm test` (18 test files / 179 application tests plus the complete Keeper
  and review-archive contract);
- `npm run typecheck`;
- `npm run build`;
- browser preload check: all 33 unique review images loaded and decoded before
  controls enabled; no page or console error.

The mandatory documentation audit covered `README.md`, `docs/DECISIONS.md`,
this hand-back, the authoring source record, runtime state and deployment
rules. `docs/KEEPER_ANIMATION_HANDOFF.md` remains accurate and was not changed:
this gate creates no Keeper animation or timing state. The full-family V6 work
remains deliberately pending Frank's A/B/C selection.
