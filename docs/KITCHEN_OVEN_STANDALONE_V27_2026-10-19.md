# Kitchen Oven Standalone V27 — fixed registration and intact joins

Date: 19 October 2026
Status: reversible visual-review correction; unapproved, unpromoted and unwired
Review route: `/keeper-review/kitchen-oven-standalone-v27/`

V27 corrects three implementation defects reported in V26 without changing the approved Cabinet V11 asset, room background, Final art or runtime.

## Corrections

1. **One exterior envelope.** V26 independently cropped every generated state to its own alpha bounds before resizing it. Small high-resolution width differences therefore became visible native-pixel movement, especially on the right side from Off to On. V27 uses equal `594 × 619-px` source windows at recorded offsets, then derives On from the exact Off exterior. The Off and On alpha envelopes are byte-identical; only the two declared control/cavity regions may differ.
2. **No rectangular dark patch.** V26 darkened a broad rectangular warning-light region, including ivory fascia pixels. V27 derives a compact saturated-red lamp mask, restores the dormant lamp and fascia from Off, and changes only that mask when the warning lamp flashes. A deterministic gate limits its changed-pixel bounding box to at most `10 × 10 px`.
3. **Visible internal-light flicker.** Broken dark and lit variants now differ across the shaped amber cavity pixels while keeping identical alpha geometry. The review opens in Broken state and starts the irregular 40-frame fault loop automatically. Cavity and red-lamp layers remain independently removable, and presentation speed remains `0.1×–4×` over the canonical 4-fps, ten-second source schedule.
4. **Cabinet pixels are never cleared.** V26's browser compositor cleared the whole `92 × 85-px` oven cell before drawing a light variant. Because the cell includes four-pixel transparent gutters, that operation also erased four pixels of each neighbouring cabinet. V27 precomposes complete native room images for Broken dark, cavity-lit, warning-lit and both-lit variants, then swaps those complete images. The browser performs no `clearRect` operation.

## Geometry and state contract

- logical oven body: `84 × 77 px`;
- isolated cell: `92 × 85 px` with four transparent pixels on every edge;
- native room bounds: x=`336–420`, y=`131–208`;
- Prime interaction anchor: `[378,218]`;
- projection: straight-on flat-cutaway parallel;
- integrated two-ring hob in every state;
- Off: dark cavity and inactive warning lamp;
- On: identical exterior, turned controls, solid red lamp, warm cavity and roasting dish;
- Broken: bottom-hinged door opening straight toward camera, transparent window, blackened roast and one dial hanging on two wires;
- smoke, sparks and flames remain absent from the state art.

## Source and reversibility

The built-in image-generation workflow performed one tightly constrained edit of the V26 high-resolution family against exact Cabinet V11 and the reported defect screenshot. Its output, full normalized prompt, references and SHA-256 values are recorded in `art/source/kitchen-oven-standalone-2026-10-19-v27/generation-provenance.json`. Deterministic equal-window registration and mask construction then produce the native draft files.

V26 remains immutable provenance. Rejecting V27 requires deleting only:

- `art/source/kitchen-oven-standalone-2026-10-19-v27/`;
- `art/raw/kitchen-oven-standalone-2026-10-19-v27/`;
- `art/drafts/kitchen-oven-standalone-2026-10-19-v27/`;
- `public/keeper-review/kitchen-oven-standalone-v27/`;
- the V27 archive manifest, builder, template, verifier, route and documentation entries.

## Verification

`npm run verify:kitchen-oven-standalone-v27` checks exact body/cell/room geometry, transparent gutters, equal fixed source windows, byte-identical Off/On alpha, unchanged Off/On exterior pixels, Broken lighting alpha identity, compact lamp-mask bounds, visible cavity difference, complete 40-frame strip geometry, unmodified pixels outside the oven bounds in every room variant, immutable Cabinet V11 authority hashes, review-page preloading, absence of `clearRect`, archive integrity and unchanged promotion boundaries.

The normal repository build and test suite remain required before delivery. The repository-wide public-payload guard was already above its historical 50 MiB threshold before V27; review media remain content-addressed and outside `public/` after archiving.
