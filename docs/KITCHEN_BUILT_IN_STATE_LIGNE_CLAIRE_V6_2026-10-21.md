# Kitchen Built-In State Ligne-Claire V6

Date: 21 October 2026  
Status: immutable reversible review candidate; not approved, registered, promoted or wired

## Purpose

V6 is the sharp-redraw replacement for rejected Kitchen Built-In State Ligne-Claire V4. It changes only the drawing language of the current V41 oven and dishwasher On/Broken assets. Approved fitted-family V3 fridge, sink, cabinets and healing layers remain byte-identical.

The approved `sandwich-tomato` V2 is the primary small-scale calibration. The washing plate and repair tool chest remain co-equal shape and construction references. The supplied original comic panels guide confident near-black contours, flat opaque spot colour, selective detail and small-scale clarity; they do not authorise semantic or geometric redesign.

## Candidate set

The pack contains 17 new candidate files:

- oven On;
- oven Broken, cavity-lit, warning-lit and both-lit;
- both complete 40-frame Broken oven lighting strips at the unchanged 4 fps;
- dishwasher On and Broken bases;
- all four adjacency/healing variants for each dishwasher state.

Each static master is genuinely drawn at 8× native resolution, reduced once with Lanczos, and registered to the matching authority's exact canvas and alpha channel. There is no direct low-resolution RGB remap, texture pass, sharpen filter or pixel-art treatment. Broken appliance construction is authored separately from the closed state.

## Immutable geometry and behaviour

The manifest records source and candidate SHA-256 hashes. Verification requires:

- exact source canvas dimensions and byte-exact alpha for every candidate;
- exact 92 × 85 oven cells, 40 frames and transparent shared frame edges;
- the unchanged sink room datum `(slot x - 4, 104)` in all room proofs;
- byte-identical approved V3 fitted-family files;
- byte-identical V19/V37/V38/V41 movement, healing, interaction, repair and effect contracts;
- unchanged separate drip, water and suds effects;
- no runtime, selector, registration or production changes.

The four room proofs cover On/Broken appliances at both run ends and in an interior position. They retain the existing 720-layout healing process; V6 supplies only replacement RGB drawing language inside the original masks.

## Review delivery

Production review route:

`/keeper-review/kitchen-built-in-state-ligne-claire-v6/`

The page uses root-absolute same-origin asset URLs so Vercel trailing-slash normalisation cannot redirect relative `assets/...` paths to the wrong directory. It preloads and decodes all four unique evidence images before declaring the review ready.

The evidence includes current-versus-candidate contact sheets at inspection and native scale, all dishwasher healing edges, four exact-datum room compositions and samples from both complete 40-frame oven strips.

## Approval boundary and rollback

`batch-register.json` is closed: `register: false`, `promote: false`, and no selector changes. Explicit Frank approval is required before any V6 candidate can become current.

Rollback is immediate: discard only `art/drafts/kitchen-built-in-state-ligne-claire-2026-10-21-v6/` and its review set. Approved V3, rejected V4, the V5 base-method gate, V41 source, production files and runtime remain untouched.

Verification:

```bash
npm run verify:kitchen-built-in-state-ligne-claire-v6
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```
