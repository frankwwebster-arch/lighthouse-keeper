# Kitchen Kettle Standalone V45

Date: 21 October 2026

Status: reversible visual/behaviour review draft; unapproved, unpromoted and
unwired.

Review: `/keeper-review/kitchen-kettle-standalone-v45/`

V45 supersedes rejected V44. V44 fixed placement but replaced the polished
concept language with a tiny kitchen-native redraw. Frank judged the concept
references good and the production assets poor by comparison. V45 therefore
makes the approved-looking concept pixels the production pixels rather than a
separate aspirational reference.

## Production masters and scale

- Off is isolated directly from the first kettle in the V43 concept family.
  Its complete `588 × 540 px` component is preserved without resizing inside
  a `652 × 604 px` transparent master.
- On is byte-identical to Off. Its steam remains a separate asset-owned layer.
- Broken is isolated directly from the stronger V43 Broken concept. Its
  complete `976 × 928 px` component is preserved without resizing inside a
  `1040 × 992 px` transparent master.
- Every master retains a 32-source-pixel transparent gutter. Alpha below
  `18/255` is removed deterministically; no enamel, brass, outline or damage
  pixels at or above that threshold are repainted or resampled.

Raster resolution and room footprint are independent. Metadata draws intact
states at `56 × 51` logical pixels and Broken at `62 × 59` logical pixels. One
approved counter bay remains `84 px = 60 cm`, so the intact kettle occupies
67% of the bay and Broken occupies 74%. Both fit on one bay with clearance.
Their base ends at bottom-exclusive room y141, visually resting on the
approved worktop's y140 row. Review canvases and proofs use a `1544 × 448`
backing for the exact `772 × 224` logical room.

## Placement and tea interaction

Compatible origins remain x `84`, `168`, `336` and `504`: fridge, cabinet A,
cabinet B and dishwasher. Placement stores `supportAssetId`, `surfaceSlotId`
and the kettle-local position. `make-cup-of-tea` resolves the Keeper stop from
the current support midpoint at `(origin + 42, 218)` and is available only in
Off and On.

Broken keeps the V41 lock contract. Direct kettle movement, swaps that would
displace it and movement of its current support are rejected until repair.
Moving an unlocked support carries its locally anchored kettle; moving the
kettle never carries cabinetry.

## Broken motion and effects

The Broken master visibly has a torn and twisted handle, open lid, displaced
spout cap, deep crushed panel, large jagged rupture exposing dark metal,
fractures and scorching. Its eight-frame `7 fps` body transform reaches three
logical pixels and ±4.1°, pivoted on the bottom-centre support contact with no
vertical displacement. The kettle therefore rattles violently while its base
remains pinned.

On and Broken use separate 40-frame, 4 fps high-resolution steam families.
Broken also emits intermittent amber sparks and small debris. Every effect
declares `anchorAssetId: kettle`, `transformSpace: asset-local`, its applicable
state and a separately editable local transform. Removing or editing an effect
does not alter the kettle master.

## Source and reversibility

The image-generation sources and exact prompts remain immutable under:

`art/source/kitchen-kettle-standalone-2026-10-20-v43/generated/`

V45 regenerates no concept art. Its builder deterministically selects, crops,
pads and publishes those existing sources. V45 has new source, raw, draft,
page and archive prefixes and changes no V41 dishwasher, approved cabinetry,
V42–V44 artifact, Final asset or runtime controller. Rejecting V45 means
deleting only its versioned additions and route. Toaster and mixing-bowl work
remains blocked until Frank approves the kettle.

## Verification

```sh
npm run verify:kitchen-dishwasher-workbench-v41-approval
npm run verify:kitchen-kettle-standalone-v45
npm run typecheck
npm run build
npm test
```

The V45 verifier proves that the production masters' RGBA components equal
the selected concept-source pixels after the documented alpha threshold. It
also checks source/master dimensions, 32-pixel gutters, Off/On identity,
logical bay ratios, y140 support contact, high-resolution effect cells and
frame isolation, meaningful animation, V41 locks, dynamic tea stops,
preload/decode gating, route and content-addressed archive integrity.

## Delivery audit

The documentation audit reconciled README, STATUS, DECISIONS, this record,
V44's rejection status, routes, package scripts, source/draft/raw/archive
ownership and the continuing toaster/bowl hold. The local review was rendered
through the real Next.js route with all 15 media files present and reached
“All V45 production media decoded.” The archive now contains `191` sets,
`4,595` logical references and `2,766` unique objects; the public payload is
`44.95 MiB`, below the `50 MiB` guard. V45 adds only its HTML shell to
`public/`; all 15 PNGs are content-addressed outside the public payload.

The V41 approval gate, immutable V44 gate, V45 gate, TypeScript check,
production build and complete repository `npm test` pass. Vitest reports `19`
files and `229` tests. The final deployment commit and live URL/hash check are
recorded in the delivery history rather than changing this immutable draft
after review begins.
