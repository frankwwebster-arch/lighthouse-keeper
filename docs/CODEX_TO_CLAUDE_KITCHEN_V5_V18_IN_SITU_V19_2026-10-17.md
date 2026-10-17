# Codex → Claude: Kitchen V19 exact V5 in-situ comparison

Date: 17 October 2026  
Status: review-only comparison; no asset is approved, promoted or wired

## Decision recorded

Frank rejected the three V18 calibration units and said V5 was better. V18 is
kept intact as rejection evidence. V17 remains the complete byte-exact V5
rollback and the sole full-family draft authority.

V19 answers one narrow review question: how do the exact V5 kettle, cooker and
sink look in precisely the same neutral, measured room used for V18?

Review: `/keeper-review/kitchen-v5-v18-in-situ-comparison-v19/`. The public
page shows the requested exact V5 room clean and with measured guides. The
rejected V18 composite is retained in the raw comparison record and verifier,
not placed ahead of the requested V5 views.

## Composition contract

- Canvas: `63 × 56 lp` / `252 × 224 px` at 4 px/lp.
- Three adjacent bays: `21 lp` / `84 px` each.
- Bay x origins: `0`, `84`, `168 px`.
- Rear wall/floor junction: `51 lp` / `204 px`.
- Asset foot line: `52 lp` / `208 px`.
- Clear foreground channel: `4 lp` / `16 px`, rows `208…223`.
- Every source raster is used at native size, without scaling, repainting or
  silhouette adjustment.
- Both variants call the unchanged
  `scripts/build_kitchen_countertop_gate_v18.py::neutral_room_context`
  function. The room pixels and positions are therefore identical.

## Exact sources

| Unit | Exact V5 SHA-256 | Rejected V18 SHA-256 |
|---|---|---|
| Kettle counter | `bc296bff87334d769aadccd75e749f4edd0221853f1d52eae90ab04270552b3c` | `add806a1f9f84e0865a473082972d05421c6a04e6c4482a0da46f58065a67e3c` |
| Cooker / hob | `a6183f51f506957fb77c79ef5dfddc82c287dfa781838fe099944f76cf303034` | `67942103f64aa4ed8fb42c4fc3db2223ee0af0986d653305aeb5ddbe48bff437` |
| Sink counter | `31ca919a515f05ac51c2850092df8501c9574c05013ea5a88ea5aca5e3d40f2a` | `8f1c1f6fd9d8fb6ecd566c873affc7c34853eaabbdc78261c57b4763cc48522a` |

## Binding verification

Run:

```sh
npm run verify:kitchen-v5-v18-in-situ-v19
```

The test pins every source and output SHA, checks the exact 252 × 224-px room
geometry, proves that the two variants share the same background wherever
neither source contributes alpha, and verifies that neither version enters the
final 4-lp foreground channel. The standard review-archive verifier also
requires all review PNGs to be content-addressed and absent from `public/`.

## Protected scope

V19 changes no runtime sprite, manifest, object register, Keeper animation,
Final asset, V5/V17/V18 source raster or live-game wiring. Any later redraw
requires a new versioned gate; V19 itself is immutable once published.
