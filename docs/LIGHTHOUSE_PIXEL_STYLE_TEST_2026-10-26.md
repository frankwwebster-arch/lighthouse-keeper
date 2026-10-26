# Lighthouse pixel-style test V4 — 26 October 2026

Status: rejected; retained as immutable historical evidence.

This reversible comparison tested two authored pixel densities against one
deliberately weak code-only control. Frank rejected both pixel candidates as
too blocky when zoomed in. The current authority, `docs/CODEX_BRIEF.md`, uses
non-pixel illustration and a straight-sided tower with no taper. No candidate
amended canon, runtime art or production art.

## Review package

- Visual review: `/keeper-review/lighthouse-pixel-style-v4/`
- Package notes: `public/art/concepts/pixel/README.md`
- Machine-readable geometry and hashes:
  `public/art/concepts/pixel/manifest-v4.json`
- Generated-source provenance:
  `public/art/concepts/pixel/PROMPTS-v2.md`
- Builder: `scripts/build_lighthouse_pixel_concepts_v4.py`
- Verifier: `scripts/verify_lighthouse_pixel_concepts_v4.py`

| Concept | Method | Native result | Purpose |
| --- | --- | --- | --- |
| A | generated source plus deterministic 16-bit enforcement | 2304 × 1080; exactly 32 colours; 384 × 128 modules; 62 px Keeper | richer SNES-like candidate |
| B | generated source plus deterministic 8-bit enforcement | 1152 × 540; exactly 16 colours; 192 × 64 modules; 31 px Keeper | coarser NES/GBC-like candidate |
| C | code-only conversion of rejected `public/art/reference/day1.png` | 2304 × 1080; exactly 32 colours | failure control for naive pixelation |

All viewing exports are exact integer nearest-neighbour enlargements. A and B
have pure `#FF00FF` sky, sea and glass, hard alpha before Keeper composition,
fully opaque final pixels, equal flat rooms and no visible interior stair or
lift architecture.

## Why V4 exists

This section records the historical reasoning at the time of the test. It is
not current production direction.

Frank rejected the earlier rectangular result because it had lost the feeling
of a lighthouse. The tapered V2 correction restored the identity, and V3 fixed
the outdoor widths. Frank then found that V3's broad brown stair jambs were too
visually assertive and that its en-suite strip could not fit believably inside
one room module. V4 preserves the V3 lighthouse and island while guaranteeing:

- alternating deep-red and warm-white masonry bands;
- a subtle exterior taper around fixed rectangular room modules;
- a wider gallery and more recognisable domed lantern crown;
- a plausible stair-sized pocket inside the left shell, completely concealed
  from the cutaway;
- the exact same stairway entrance on every floor, at the same local position;
- only one pixel-equivalent hairline edge and one pixel-equivalent handle when closed,
  with no visible panel, broad jamb, recess or perspective cue;
- no bedroom en-suite partition or extra door at one-module width;
- a six-module native canvas with a fully visible one-module bed, lawn and
  terrace measured from the real tapered-shell edges;
- rough edge ground beyond the plots and visible magenta sea margin beyond the
  boat.

The ground floor separately retains an exterior door. The test-specific scene
contains three equal room floors plus the empty lamp room; it does not rewrite
the measured two-floor history of the rejected Day 1 establishing-shot draft.
An en-suite can return only in a future layout wide enough to house it without
compressing the bedroom or introducing a perspective-bearing internal box.

The deterministic island pass removes all inherited outdoor perspective. The
bed, lawn and terrace are measured one-module spans attached to one level
ground line; the cliff, stone steps, jetty and boat are side profiles with no
visible ground, paving or soil top planes. The immutable V2 and V3 reviews
remain as superseded evidence rather than being rewritten.

## Deliberately retained control failures

Concept C is not an approved smooth-art baseline. Its rejected historical
source has:

1. two room floors instead of the test's three;
2. visible stair flights/recesses instead of the concealed circulation slot;
3. non-modular room geometry that a code-only whole-frame conversion cannot
   turn into exact 384 × 128 modules without becoming a redraw.

Those failures remain visible and are recorded in the manifest. They are the
point of the control, not accidental omissions.

## Validation and boundaries

The dedicated verifier checks source/output hashes, native dimensions, exact
palette counts, pure-magenta glass, equal module geometry, tapered-shell and
hidden-pocket metadata, identical local stair-door edge/handle geometry and
colours across all three floors, absence of the former en-suite strip, measured
outdoor spans, fully side-profile outdoor presentation, Keeper height, and
pixel-identical nearest-neighbour viewing exports.

Large review PNGs are content-addressed under `review-archive/objects/` after
the standard maintenance pass; the review URLs and package manifest remain
stable while `public/` stays below its 50 MiB deployment guard.

No candidate has been promoted or wired into runtime. Publishing the review
page did not change that status. The immutable page's “awaiting verdict” label
is a frozen pre-rejection snapshot. The magenta
background is technical isolation for this style test, not a reversal of the
current preference for the original concept's warm atmosphere and distant
island detail when the separate animated background layers are composed.
