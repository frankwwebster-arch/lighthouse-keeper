# Prime Keeper morning animation drafts V1

Date: 22 October 2026

Immutable review route: `/prime-keeper-animation-drafts-v1`

This batch remains byte-identical and independently reviewable. The current
expanded review is V2 at `/prime-keeper-animation-drafts-v2` (also served by
`/prime-keeper-animation-drafts`) and is documented in
`docs/PRIME_KEEPER_EXPANDED_ANIMATION_REVIEW_V2_2026-10-22.md`.

## Delivered for review

Five unapproved sequences, 36 frames:

1. Lift entry, ride-neutral handoff and exit — 8 frames.
2. Front-door approach, handle/body action and pass-through — 6 frames.
3. Rear cooking at an invisible counter registration plane — 8 frames.
4. Rear tooth-brushing at an invisible basin registration plane — 8 frames.
5. Friendly front-facing wave — 6 frames.

The page decodes all candidate and authority images before enabling playback.
Each animation has play, pause, stop, previous/next frame, scrub and thumbnail
selection. Global controls act on every player. The sandbox combines and
reverses draft sequences without changing source bytes. Redraft notes are saved
locally against stable IDs such as `cook-counter-v1/frame-04`.

## Binding Prime contract

- Logical cell: 32 × 40.
- Authoring cell: 256 × 320 at 8 pixels per logical pixel.
- Anchor: 128,320; standing cap top y=18; opaque floor y=316.
- Binding authorities are SHA-256-pinned in
  `data/keeper_prime_identity_contract.json`.
- Standard-uniform palette references are jumper blue `0,108,230`, broad band
  `251,232,206`, trousers `63,75,112`, boots `63,74,111`.
- Matching standing endpoints use the exact approved front/back/side authority
  bytes rather than generated approximations.

The deterministic builder colour-locks the generated blue, cream and navy
families toward those measured references while preserving the approved
standard-uniform rendered treatment. No costume was introduced in this batch.
Future costumes must obey Frank's eight-rule ligne-claire direction recorded in
`data/keeper_prime_identity_contract.json`.

## Reversibility and frame replacement

Canonical art, approved reviews and runtime sprites are not overwritten. Each
candidate has its own `art/drafts/keeper-prime-…-2026-10-22-vN/` directory,
immutable generated source hash, normalised draft strip hash and one SHA-256 per
frame. A rejected sequence can be removed by discarding only its draft
directory and review entry; a rejected frame can be regenerated into its stable
redraft slot without changing its neighbours.

## Isolation gate

Every reviewable frame has transparent outer edges and one connected source
ownership range. The build rejected and quarantined these source sheets:

- fridge snack V1 — adjacent reaching/eating poses touched;
- bed daytime nap V1 — seated-to-lying poses overlapped;
- broom sweep V1 — body/broom ownership crossed source gaps;
- wave V0 — two arm poses touched.

Nothing was recovered by cropping, component order or boundary reassignment.
Wave was rerendered as the isolated six-frame V1 candidate. Snack, bed and broom
remain excluded until their affected poses are genuinely rerendered.

## Runtime state

This batch is review-only. Separately, the approved 27-sprite/217-frame runtime
bank now actively binds turns to rear work and seating, side sit/hold/stand to
TV/nature TV/armchair nap/reading/piano, and rear turn/sit/hold/stand/turn to the
diary. Ladder, darts and front/left seating remain installed without a matching
gameplay consumer.

## Verification

```sh
npm run verify:keeper-prime-identity
npm run verify:keeper-prime-runtime
npm run verify:keeper-prime-drafts
npm run typecheck
npm run build
```

The review archive maintenance command must also pass before deployment:

```sh
npm run maintain:keeper-review
```

## Documentation audit

README, the machine-readable animation-gap inventory, this handoff and the
runtime bank were reconciled against the delivered code and generated data on
22 October 2026. The page makes the approval boundary explicit: installed
approved sprites and new unapproved drafts are never presented as the same
state.
