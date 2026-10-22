# Prime Keeper expanded animation review V2

Date: 22 October 2026

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v2`

Preserved predecessor: `/prime-keeper-animation-drafts-v1`

## Delivered for review

V2 has ten reversible sequences and 163 frame occurrences. It carries all five
V1 sequences unchanged and adds:

1. Collect broom, sweep and recover — 11 isolated frames.
2. Side leisure: sit, hold and stand — 15 frame occurrences.
3. Diary: turn, sit, hold, stand and return — 31 frame occurrences.
4. Front seat consumer route — 29 frame occurrences.
5. Rear task: turn, work and return — 41 frame occurrences.

The four longer choreography previews are not new drawings. Every occurrence
is a byte-exact copy of a frame already in the approved Prime animation
catalogue; only order, direction, duration and repeated holds are proposed for
review. The sweep is a separate isolated action candidate and remains
unapproved. None of these sequences has been promoted to the runtime bank.

## Prime identity and colour gate

All sequences retain the binding 32 × 40 logical / 256 × 320 authoring Prime
contract, 8 px per logical pixel and standing anchor 128,320. The broom uses a
384 × 320 prop-safe cell while retaining the body anchor at 128,320. Canonical
front, back and side-right authorities and the measured jumper, cream band,
trouser and boot colours are shown on the page before the candidates.

The generated fridge-snack retry was rejected before entering the repository:
although isolated, it subtly changed Prime's proportions and therefore failed
the exact-identity gate. The bed source remains quarantined for overlapping
poses. The original broom sheet also remains rejected history; V2 uses the
independently isolated sweep source instead.

## Review controls and redrafting

The page preloads and decodes all 166 unique image URLs (163 occurrences plus
three canonical authorities) before enabling transport controls. Every
sequence and the combined sandbox supports play, pause, stop/reset,
previous/next frame, scrubbing and direct frame selection. The sandbox can add,
reorder, reverse and remove any sequence without changing source bytes.

Every occurrence has a stable `sequence/frame-NN` redraft slot. Frame-specific
notes are kept in the browser and can be copied for feedback. Source art,
canonical art, V1 files and runtime sheets remain untouched; rejection is
reversible by discarding the V2 draft directory or replacing only a named frame
slot in a later version.

## Deterministic sources

- `data/keeper_prime_animation_drafts_v2.json` is the checked review manifest.
- `scripts/build_keeper_prime_morning_drafts_v2.mjs` reconstructs or verifies
  every frame, hash, composition record and strip.
- `art/drafts/keeper-prime-*-choreography-2026-10-22-v*/` contains versioned
  composition manifests, isolated occurrence files and review strips.
- `review-archive/sets/keeper-prime-morning-drafts-v2.json` maps deployed URLs
  to content-addressed evidence objects.

The builder rejects changed V1 hashes, missing approved sources, non-320 px
frames, any opaque outer cell edge, duplicate redraft slots or an unexpected
sequence/frame inventory.

## Verification

```sh
npm run verify:keeper-prime-drafts
npm run maintain:keeper-review
npm run typecheck
npm run build
npm test
```

## Documentation audit

README, the approved-library handoff, the V1 record and the machine-readable
gap inventory were reconciled with V2 on 22 October 2026. Current documentation
distinguishes approved source art, proposed choreography, unapproved action art
and runtime promotion; no review candidate is described as production-ready.
