# Prime Keeper minimal ligne-claire finishing pass V2

**FEASIBILITY TEST — NOT APPROVED PRODUCTION ART**

This pack asks one narrow question: can the approved Prime Keeper receive a
flatter, more rigorously controlled ligne-claire rendering treatment without
changing his construction or rebuilding his motion?

The answer from V2 is **yes technically, but the visual gain is very modest**.
The current Prime Keeper already uses most of the ligne-claire language: clean
silhouette, dark controlled contours, separated colour areas, restrained
facial marks and little texture. V2 makes only a light consolidation pass over
remaining soft modelling and dark ink. It should be judged as a subtle polish
option, not a dramatic conversion or a new design. The stronger V1 flattening
remains preserved in its own immutable draft directory as comparison history.

Nothing in this directory is canonical, Final, runtime or production art. No
production Keeper file, manifest, gameplay code, interaction geometry or
existing review set was modified. Rejection is deletion of this directory.

## Authorities selected before final construction

| Role | Authority | SHA-256 |
|---|---|---|
| Permanent Prime identity, face, front proportions and single-band uniform | `art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png` | `a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e` |
| Approved side-right endpoint; static pose and dimensional authority | `art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png` | `a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3` |
| Approved eight-frame side-right locomotion artwork authority | `art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/keeper_prime_walk-right_f8.png` | `59da79117719ca58368aab22e06520e4fb77dedd88e0fd118ffe80b4910db583` |

Walk V6 was reused exactly for pose order and registration. The artwork-free
V7 record pins Frank's approval. Fast Timing V1 supplies the current approved
10 fps locomotion preview timing. Legacy `public/sprites/keeper_walk.png` and
`art/raw/keeper-first-batch/keeper_walk_f8.png` remain useful historical and
runtime comparisons, but they are not the newer smooth Prime rendering
authority for this test.

Exact snapshots of the three selected images are under `sources/authorities/`.
Their bytes and hashes match the originals.

## Locked construction

- logical cell: 32 × 40;
- density: 8;
- source cell: 256 × 320;
- logical feet anchor: `[16,40]`;
- source anchor and baseline: `[128,320]`;
- coordinate origin: top-left;
- static significant-alpha bounds: `[77,18,179,316)` in both original and test;
- static displayed character size: 102 × 298 source pixels (12.75 × 37.25 logical pixels);
- walk: eight 256 × 320 cells, assembled as a 2048 × 320 strip;
- root-motion authority: 21 logical pixels per second;
- no frame has alpha on a cell edge.

Project-wide anatomical locks remain unchanged: skull-top-to-supporting-sole
32.5 logical pixels; eye line 28.5 above floor; shoulders 24.5; hips 14.5;
side core depth 13; canonical head width 14.5; hand diameter 4; boot length 8;
landmark tolerance 0.5 and core-width tolerance 1 logical pixel. The approved
Prime front additionally records a 111 × 130 source-pixel head envelope and an
85 × 67 beard envelope within a 152 × 298 significant-alpha body box. V2 does
not move any of those regions; every output copies the authority's alpha byte
for byte.

## Treatment

The two built-in image-generation studies in `sources/generated-studies/`
were used only to explore the visual language. They were rejected as geometry
sources because their canvases and silhouettes were not exact.

Final V2 artwork is a deterministic, Prime-specific finishing pass over the
approved pixels. Broad materials retain 72% of their original RGB and move only
28% toward the restricted semantic palette; existing dark drawing receives a
62% deep-navy ink correction. The build does not use edge detection, change
alpha, warp a feature, rescale a cell, alter a pose or generate an intermediate
frame. Limited original modelling and secondary tones remain where they
preserve warmth and readable separation.

## Review order

1. Open `evidence/current-vs-ligne-claire.png` for the exact-scale static proof.
2. Open `evidence/dimensional-comparison.png` and
   `evidence/dimensional-verification.json` for geometry.
3. Inspect `evidence/walk-contact-sheet.png` frame by frame.
4. Inspect `evidence/onion-skin-adjacent.png` for adjacent-pose registration.
5. Play `walk/keeper-prime-ligne-claire-light-pass-walk-preview.webp` or the GIF at the
   approved 10 fps locomotion timing.

Contact is F1, passing is F3 and opposite contact is F5.

## Results

- Static and all eight walk frames have byte-identical alpha to their named
  authorities: zero differing alpha pixels.
- The static pass changes RGB by only 5.17 levels per channel on average;
  77.065% of opaque pixels remain within eight RGB levels of the authority.
  Walk-frame means remain tightly grouped from 5.319 to 5.754 levels, evidence
  that the finish is both light and consistent across the cycle.
- Canvas, cell, density, anchor, baseline, bounds and foot-contact evidence are
  unchanged.
- The test strip slices are byte-identical to the individual test frames.
- All cells retain transparent safety gutters.
- Head, nose, hair, beard, chin, torso, coat/jumper outline, elbows, hands,
  trousers, knees and boots inherit the exact accepted motion drawings, so no
  new line boil or likeness drift is introduced by V2.
- No existing animation was recreated: Walk V6 was reused.

The beard was the most sensitive feature to flatten: removing its modelling
too aggressively makes its stepped silhouette read as a featureless white
mass. The boot/trouser distinction is the second-sensitive area. V2 retains
most of the approved modelling in both regions and only nudges their palette.

## Feasibility assessment

The controlled treatment scales mechanically to other already-approved Prime
frames because it can retain their geometry exactly. Motion remains coherent
and registration-safe. However, the present Prime is already close to ligne
claire, and its soft modelling adds warmth and volume. V2 is intentionally
hard to distinguish at game scale and is not an unambiguous visual upgrade.
The evidence therefore supports continuing with the Keeper as he is unless a
human A/B review clearly prefers this subtle finish. A library-wide migration
is technically feasible but not justified by this proof alone.

If pursued, the safe route is controlled per-material repainting over each
approved authority, not independent frame generation and not a wholesale
redesign. Promotion or approval is outside this pack.

## Rebuild and verify

From the repository root:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 art/drafts/codex-prime-keeper-ligne-claire-walk-test-2026-10-21-v2-light-pass/build.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 art/drafts/codex-prime-keeper-ligne-claire-walk-test-2026-10-21-v2-light-pass/verify.py
```

`build.py` writes only inside this versioned draft directory. `verify.py` is
read-only and fails on authority-hash drift, alpha mismatch, geometry mismatch,
shared-edge alpha, strip/frame disagreement, preview-frame mismatch or output
hash drift.

## Documentation audit

The pack was checked against `AGENTS.md`, `CLAUDE.md`, the Keeper artwork
playbook, scale/interaction contract, Prime restart handoff, animation-bank
normalisation contract, workbench notes and Walk V7 approval record. No
top-level product documentation change is needed: the proof changes no product
state, authority, runtime behaviour, deployment state or backlog decision. This
README, `PROMPT_LOG.md`, `SOURCE_SELECTION.md`, the batch register and the
machine-readable evidence are the complete durable handoff for this isolated
review-only experiment.
