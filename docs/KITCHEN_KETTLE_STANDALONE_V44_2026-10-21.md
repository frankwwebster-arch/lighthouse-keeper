# Kitchen Kettle Standalone V44

Date: 21 October 2026

Status: reversible visual/behaviour review draft; unapproved, unpromoted and
unwired.

Review: `/keeper-review/kitchen-kettle-standalone-v44/`

V44 supersedes the rejected V43 presentation. V43 displayed a polished
high-resolution concept in development but reduced it to a 44-pixel production
sprite; the reduction lost the enamel finish and made the review page look
materially worse than its source. V44 makes the distinction explicit. It shows
the full-quality concept as review reference and uses an existing
kitchen-native kettle drawing for production without resizing it.

## Production scale and placement

- The intact production kettle is the exact `48 × 34 px` appliance layer from
  the retained Kitchen V5 family, copied into a new V44 source snapshot. No
  scale filter or generated-art reduction touches those pixels.
- The sprite lives in an isolated `64 × 64 px` cell. Intact states occupy x
  `8–55` and y `26–59`; the base therefore still ends at room y `140` when the
  cell uses offset `(10, -53)` from the supporting bay.
- One approved counter bay remains `84 px = 60 cm`. The intact 48-pixel
  handle-to-spout width occupies 57% of a bay. The Broken state reaches 52
  pixels only because its detached handle shard remains with the asset.
- Compatible surface origins remain x `84`, `168`, `336` and `504`: fridge,
  both cabinets and dishwasher. Placement stores `supportAssetId` and
  `surfaceSlotId` and derives the dynamic `make-cup-of-tea` stop at
  `(support origin + 42, 218)`.

The exact `772 × 224 px` room is the placement authority. The review page does
not enlarge a tiny production sprite and present it as source-quality art.
Instead it shows the unchanged full-quality V43 concept separately, labels it
as reference-only, limits isolated production inspection to 2× and provides
the native room directly below.

## States and failure language

- **Off:** exact kitchen-native turquoise enamel kettle pixels, with no effect.
- **On:** byte-identical to Off. Steam remains separate.
- **Broken:** the native casing is visibly destroyed at its authored scale: the
  left handle mount is torn away, the upper handle is rotated and split, one
  handle shard lies detached on the worktop, the lid is displaced, the spout
  tip breaks downward, the body is deeply fractured and a large jagged enamel
  loss exposes dark metal.

Broken uses an eight-frame, `4 fps` body rattle with amplitudes up to three
native pixels. Its base row remains byte-identical and pinned to the support.
The separate Broken effect combines pressure steam, intermittent amber sparks
and small debris pulses. The effect remains owned by `anchorAssetId: kettle`
and stores an asset-local transform. Off/On movement, Broken placement lock,
support-asset lock and repair unlocking remain the V41 contract.

## Source and reversibility

The V44 native source snapshot is:

`art/source/kitchen-kettle-standalone-2026-10-21-v44/native/kettle-native-source.png`

The prior built-in image-generation sources remain unchanged under the V43
source directory and are reused only as source-quality review references and
steam keyframes. The V43 prompts and generation provenance remain authoritative
for those files. No generated kettle painting is used as a production sprite.

V44 has new source, raw, draft, page and archive prefixes. It changes no V41
dishwasher, approved cabinetry, V42/V43 artifact, Final asset or runtime
controller. Rejecting V44 means deleting only its versioned additions and
route. Toaster and mixing-bowl work remains blocked until Frank approves the
kettle.

## Verification

```sh
npm run verify:kitchen-dishwasher-workbench-v41-approval
npm run verify:kitchen-kettle-standalone-v44
npm run typecheck
npm run build
```

The V44 verifier checks the exact 48 × 34 intact bounds and pixel count, Off/On
identity, isolated gutters, y140 seating, 52-pixel Broken debris bound,
base-pinned rattle, forty-frame owned effects, placement locks, dynamic tea
stop, preload/decode gate, route and content-addressed archive.

## Delivery audit

The documentation audit reconciled README, STATUS, DECISIONS, the V43 rejection
record, this record, routes, package scripts, source/draft/raw/archive ownership
and the continuing toaster/bowl hold. The page was exercised through a local
HTTP server with all 18 media files present; every file decoded before controls
unlocked. After integrating current main's review-payload slimming, the archive
contains `190` sets, `4,580` logical references and `2,754` unique objects.
The focused V41–V44 gates, TypeScript check, production build and complete
repository `npm test` all pass (`19` Vitest files / `229` tests); the public
payload is `44.93 MiB`, below the `50 MiB` guard. V44 adds only its HTML shell
to `public/`; all 18 images are content-addressed outside the public payload.
