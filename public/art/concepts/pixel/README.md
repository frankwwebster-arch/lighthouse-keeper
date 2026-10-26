# Lighthouse pixel-style comparison V4

Status: review-only style experiment; awaiting Frank's verdict. Nothing in
this package is approved canon, runtime art or production art. Its review page
may be published without promoting a candidate into the game.

V4 compares two authored pixel densities with one deliberately weak code-only
control. It responds to Frank's direction that the tower must immediately read
as a classic lighthouse: alternating deep-red and warm-white masonry, a slight
continuous exterior taper around fixed rectangular rooms, a broader
gallery/lantern silhouette and a believable but completely invisible
stair-sized circulation pocket between the shell and the left room jamb.

The cutaway remains a flat, straight-on doll's house. Rooms have no inset depth
or visible side planes. No stair, landing, shaft or lift car appears. Every
floor uses the same closed circulation-door mark in the same local position:
one pixel-equivalent hairline edge and one pixel-equivalent warm handle, with no visible
panel, frame, recess or perspective surface. The ground floor separately has
its exterior door. The bedroom en-suite is omitted because its partition and
second door are not believable at this one-module width.

## Concepts

| Concept | Native output | Enforced structure | Viewing output |
| --- | --- | --- | --- |
| A — generated 16-bit | 2304 × 1080, exactly 32 colours | 384 × 128 rooms, 48 px windows, 8 px wall/floor bands, 24 px bays, 62 px Keeper | exact nearest-neighbour ×3 |
| B — generated 8-bit | 1152 × 540, exactly 16 colours | 192 × 64 rooms, 24 px windows, 4 px wall/floor bands, 12 px bays, 31 px Keeper | exact nearest-neighbour ×6 |
| C — code-only legacy control | 2304 × 1080, exactly 32 colours | no architectural redraw | exact nearest-neighbour ×3 |

A and B have three identical flat room modules plus an empty lamp room. Their
island layer is also code-enforced on a six-module canvas: one level ground
line, fully visible one-module bed, lawn and terrace spans outside the shell, a
front-facing cliff, side-profile steps and jetty, rough edge ground and sea
breathing room. No visible paving or soil top planes remain. All sky, sea and glazing are exact
`#FF00FF`; final PNGs are fully opaque and contain no anti-aliased pixel grid.

Concept C is intentionally not a compliant proposal. Its source,
`public/art/reference/day1.png`, is a rejected historical draft rather than an
approved smooth reference. A code-only conversion honestly retains three
failures:

- two room floors rather than the test's three;
- visible stair flights and stair recesses rather than concealed circulation;
- no exact 384 × 128 room-module geometry, which cannot be recovered without
  redrawing the source.

The requested `public/art/keeper/canon/` directory does not exist. The build
therefore uses the exact approved 256 × 320 side-right idle authority at
`review-archive/objects/a1/a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3.png`.
It is converted in code to the candidate's grid, palette and hard alpha.

## Files and packaging

- `manifest-v4.json` is the current machine-readable authority for source/output
  hashes, exact geometry, palette counts, Keeper placement and known breaks.
- `PROMPTS-v2.md` records the generated-source prompt chain shared by V2–V4.
- `/keeper-review/lighthouse-pixel-style-v4/` is the current same-size visual review.
- The immutable V2/V3 reviews and their manifests remain as superseded evidence.
  V2's nominal outdoor plots were partly covered by the tapered shell. V3 fixed
  those widths but retained a visually heavy stair jamb and a cramped bedroom
  en-suite strip. V4 changes only those deterministic room marks.
- Generated inputs remain reversible under
  `art/drafts/lighthouse-pixel-style-test-2026-10-26-v2/sources/`. V1 source
  passes are explicitly superseded, not overwritten.

Large PNGs initially build under
`public/keeper-review/lighthouse-pixel-style-v4/assets/`. The mandatory review
maintenance step moves them into immutable content-addressed
`review-archive/objects/` storage while preserving those stable review URLs.
This keeps the live `public/` payload below its 50 MiB ceiling. The package
entrypoint, manifest and documentation remain in this directory as requested.

## Rebuild and verify

Python 3 needs Pillow and NumPy. In the Codex workspace, use the bundled Python
runtime returned by the workspace-dependency helper.

```sh
python3 scripts/build_lighthouse_pixel_concepts_v4.py
python3 scripts/verify_lighthouse_pixel_concepts_v4.py
npm run maintain:keeper-review
python3 scripts/verify_lighthouse_pixel_concepts_v4.py
```

The first verification proves the freshly built files. The second proves that
the same bytes resolve from the immutable archive after the public copies have
been removed.
