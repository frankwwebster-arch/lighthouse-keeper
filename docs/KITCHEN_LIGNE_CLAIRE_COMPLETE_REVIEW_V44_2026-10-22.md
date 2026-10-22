# Kitchen Ligne-Claire Complete Review V44

Date: 22 October 2026

Status: immutable reversible review candidate; not approved, registered,
promoted, selected as current or wired to production/runtime.

Review route: `/keeper-review/kitchen-ligne-claire-complete-review-v44/index.html`

## Outcome

V44 is the first verified coordinated pack covering the whole active kitchen
furniture/object inventory while retaining the approved modular movement and
countertop-healing laboratory. It is a review release, not a registration.

The pack contains:

- 50 object/state candidates;
- 16 animation or separately owned effect assets;
- 11 complete family contact sheets with current, candidate, alpha ghost and
  native 64-pixel proof columns;
- exact source and candidate SHA-256 values, canvases, alpha bounds and alpha
  hashes;
- the V41/V42 live six-bay movement, swap, Broken-lock, repair-unlock,
  asset-local suds and countertop-healing implementation.

## Visual authorities and candidates

- Fitted cabinets, fridge, sink and healing layers: approved V3, unchanged.
- Oven On: approved V8, unchanged.
- Oven Broken body: approved V12 authority with the unapproved requested V15
  attached ajar-door candidate and inherited lighting strips.
- Oven Off: unapproved V13 candidate.
- Dishwasher: V1 flat-colour family, including all Off/On/Broken healing-edge
  variants. Its LCD and state lamp are attached to the slanted top control rail
  of the door and move with that door when Broken.
- Table/chair: V3, exact rear-facing one-place geometry.
- Pedal bin: V2, with distinct broken contents and both approved forty-frame
  effect strips unchanged.
- Kettle: V1, retaining V45 high-resolution canvases, logical render sizes,
  support slots, bottom-centre rattle pivot and six forty-frame steam strips.
- Toaster: V4, retaining all three exact `84 × 68` masks and the separate
  forty-frame heat strip.
- Mixing bowl: V1, retaining both exact `84 × 68` masks, intact decoration and
  the large broken ceramic pieces.

All candidates follow the binding taxonomy: one mostly even near-black contour,
real edges only, closed flat local colours, no gradients, shine, glow, hatching
or texture, accurate rather than cute machinery, black only for black material,
and readable construction at 64 pixels.

## Geometry and behaviour invariants

The verifier checks every current/candidate pair for identical canvas and alpha
bounds. Exact source alpha bytes are retained everywhere except the already
approved V8 oven authority, whose deliberately corrected contour retains the
same `92 × 85` canvas and `(4,4)–(88,81)` transparent bounds.

The complete page inherits the V42 script mechanically. After normalising only
the review-set string, it is byte-identical to the approved V41-derived
movement/healing implementation. Therefore V44 changes no:

- bay origins, anchors, pivots, collision geometry or room layout;
- drag preview, exact snap, occupied-bay swap or 720-layout join resolution;
- Broken position lock, displacement rejection or repair unlock;
- effect owner, asset-local transform, frame count, frame order or timing;
- interaction stop, state transition, handling or healing rule.

## Delivery resilience

Every HTML asset URL is root-absolute. The V44 set is admitted by the existing
same-origin content-addressed review-archive route, so Vercel removing a trailing
slash cannot rebase `assets/...` onto the wrong directory. All workbench assets
are preloaded and decoded before controls are enabled.

## Failed internal predecessor

V43 completed its art assembly but its aggregate verifier expected
`candidateSha256` on byte-preserved effects whose source manifests correctly
called the field `preservedSha256`. V43 remains immutable failed provenance.
V44 changes only that aggregate metadata normalisation and is the reviewable
successor.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v1
npm run verify:kitchen-ligne-claire-healing-workbench-v42
npm run verify:kitchen-table-chair-ligne-claire-v3
npm run verify:kitchen-bin-ligne-claire-v2
npm run verify:kitchen-kettle-ligne-claire-v1
npm run verify:kitchen-toaster-ligne-claire-v4
npm run verify:kitchen-mixing-bowl-ligne-claire-v1
npm run verify:kitchen-ligne-claire-complete-review-v44
npm run maintain:keeper-review
npm test
npm run build
```

Browser verification must also exercise an exact-bay move/swap, confirm Broken
dishwasher movement rejection, repair it to Off or On and move it, and compare
healing enabled with raw edges.

## Approval and rollback

`batch-register.json` is closed: `register:false`, `promote:false`, no current
selector changes and no production writes. Explicit approval is required before
any candidate can become current.

Rollback is immediate: discard only the V44 draft, review route, archive set
manifest, builder and this record. Every source, approved authority, production
asset, runtime selector and earlier immutable version remains available and
unchanged.

## Documentation audit

README, STATUS, DECISIONS, package verification scripts, the V44 manifest and
this delivery record agree on the review-only status, the 50/16/11 inventory,
the V41 behaviour inheritance, root-absolute delivery, closed gate and rollback
boundary. No gameplay or production documentation was changed because no
runtime or production change was made.
