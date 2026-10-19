# Kitchen Cabinet Run V11 — cabinet-only reset

Date: 19 October 2026

Status: reversible visual-review draft; unapproved, unpromoted and unwired

Review route: `/keeper-review/kitchen-cabinet-run-v11/`

## Why this gate exists

Frank rejected Kitchen Rebuild Modular V10 because its cabinet and appliance
art ignored the required polished style and flat-cutaway projection and read as
unacceptably blocky. V10 remains immutable rejection provenance and is not a
visual authority.

V11 restarts at the structural layer and deliberately builds only one empty
two-cabinet run. No sink, tap, fridge, oven, dishwasher, kettle, toaster, bowl,
state variant or environmental effect belongs to this gate. The sink will be a
standalone asset, like the major white goods. No individual appliance work may
begin until Frank approves the cabinetry.

## Construction

The cabinet is a new high-resolution raster drawn from scratch. The approved
Kitchen V23 room is used only as a style, colour and projection reference; no
historical cabinet pixels are cropped, patched or composited into V11.

The run uses:

- two equal 84-pixel logical bays;
- one continuous 168 × 74-pixel installed body;
- deep storm-blue and marine-blue fronts;
- a pale sea-glass worktop;
- very dark navy outlines and recessed plinth;
- aged-copper cup pulls, knobs and fine hinges;
- a straight-on doll's-house elevation with parallel geometry and no vanishing
  point;
- a high-resolution polished master reduced once with premultiplied-alpha
  Lanczos resampling, rather than a low-resolution procedural redraw.

The native sprite cell is 176 × 82 pixels. Its installed body occupies
`[4,4,172,78]`, leaving a deterministic four-pixel transparent gutter on every
edge.

## Duplication proof

The exact same native cell is composited twice into the empty 772 × 224 room:

- first body origin: `[168,134]`;
- second body origin: `[420,134]`;
- preserved standalone-oven gap: `[336,134,84,74]`.

This proof confirms that two runs of two can be assembled without redrawing the
cabinet. It does not settle the later positions of the standalone sink or
dishwasher.

## Generation record

The final source was produced with the built-in image-generation workflow. The
binding prompt required a transparent, two-bay cabinet-only sprite; polished
hand-rendered pixel art; storm-blue, sea-glass, navy and aged-copper palette;
straight-on parallel projection; a connected worktop/front/plinth; and no
sink, appliance, prop, wall, floor, shadow, text or watermark. The generated
source is preserved at:

`art/source/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-generated-source.png`

## Build and verification

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_cabinet_run_v11.py
npm run archive:keeper-review
npm run verify:kitchen-cabinet-run-v11
```

The verifier pins the source and derived hashes, native dimensions, alpha
gutter, projection metadata, empty oven slot, unchanged room pixels outside the
two cells, literal reuse of one native sprite for both room appearances,
review-media preload contract and archive coverage.

Nothing in Final or runtime changes. Rejection remains reversible by deleting
only the V11 source/raw/draft/review/archive, builder, verifier and this record.
