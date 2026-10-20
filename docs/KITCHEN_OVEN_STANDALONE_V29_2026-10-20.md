# Kitchen Standalone Oven V29 — Broken shelf-height correction

Date: 20 October 2026
Status: reversible, unapproved, unpromoted review draft

## Purpose

V29 corrects only the Broken oven contents after V28 placed them too high.
The blackened roast and roasting dish remain on a fixed interior shelf, but
are lowered behind the unchanged open door. The door therefore occludes the
lower tray naturally; no oven contents are attached to or carried by it.

Off and On are byte-identical to V28. The approved V27 state-family design,
V28 shallow hob, exact body envelope, installed position and Prime interaction
anchor are retained.

## Locked geometry

- logical body: `84 × 77 px`
- isolated cell: `92 × 85 px`, with a transparent four-pixel gutter
- installed body: `x=336–420`, `y=131–208` in the `772 × 224 px` room
- Prime interaction anchor: `(378,218)`
- V29 edit region: Broken body `x=14–69`, `y=35–50` only
- complete open door, hob, exterior, cabinets and room background: V28 bytes

The dark and lit Broken variants use the same registered content patch. The
dark version applies one fixed RGB scale rather than V28's geometry-dependent
lit/dark pixel delta, preventing the former high roast from reappearing as a
ghost during the fault loop.

## Smoke workflow

Smoke is not baked into the oven. It is added only after the static Broken
state is approved, as a separate reusable ten-second environmental layer.
The existing `/keeper-review/kitchen-rebuild-states-v9/` workbench still
provides three animated oven-smoke models with drag, resize, crop, speed and
remove controls. It currently contains the older pre-modular oven and is
therefore reference-only for placement. The next effects-workbench revision
must load the approved standalone oven unchanged before final smoke placement.

The oven's internal cavity and red warning light remain independent,
removable 40-frame, 4-fps, ten-second fault layers with `0.1×–4×` presentation
speed. Their schedules are inherited unchanged from V28/V27.

## Review and verification

Review route: `/keeper-review/kitchen-oven-standalone-v29/`

Run:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_oven_standalone_v29.py
npm run archive:keeper-review:set -- art/drafts/kitchen-oven-standalone-2026-10-20-v29/batch-register.json HEAD
npm run verify:kitchen-oven-standalone-v29
```

The verifier checks all authority/source hashes, exact dimensions and gutters,
byte-identical Off/On states, the sole allowed Broken edit patch, unchanged
lighting schedules, complete-room neighbour preservation, archive integrity,
media preloading and the absence of browser `clearRect` compositing.

## Boundary

V27 remains the approved state-family authority. V28 remains immutable
perspective-correction provenance. V29 is not approved or promoted into
Final/runtime, and no later kitchen asset is started by this batch.
