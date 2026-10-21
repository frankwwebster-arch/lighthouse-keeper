# Kitchen Oven Ligne-Claire V8

Date: 21 October 2026  
Status: immutable reversible Oven On mapping gate; exact candidate approved as
the current Oven On visual authority; not promoted or runtime-wired

## Correction

Frank confirmed that V7 preserved the perfect exact visual authority but
trimmed the top of its registered mapping. The cause was V7's over-strict reuse
of the old asset's alpha channel pixel-for-pixel. That old internal silhouette
cut through the new hob contour even though the canvas and outer alpha bounds
were correct.

V8 keeps the exact visual authority unchanged at SHA-256
`0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538`.
It retains the authority's own complete contour and antialiasing while mapping
it inside the current asset's exact `92 × 85` canvas and exact transparent
padding bounds `(4,4)–(88,81)`. The safe source crop includes measured clear
space above the authority's content rather than beginning on a painted row.

The per-pixel alpha is intentionally not copied from the old drawing because
that was the clipping defect. Alpha bounds, canvas, placement and transparent
padding remain exact.

## Scope and safety

V8 remains an Oven On base gate only. It does not propagate Broken, lit or
flicker states and does not touch the dishwasher. `batch-register.json` remains
closed: no registration, promotion, current-selector, runtime, movement,
animation, interaction, repair, healing, timing, anchor, pivot or collision
change is authorised.

Review route:

`/keeper-review/kitchen-oven-ligne-claire-v8/`

The root-absolute page shows the unchanged exact authority followed by the
rejected V7 mapping and top-safe V8 mapping. Both images must decode before the
page declares readiness.

Verify with:

```bash
/usr/bin/python3 scripts/build_kitchen_oven_ligne_claire_v8.py --verify
npm run maintain:keeper-review
```

Rollback is immediate: discard only the V8 draft, review set, builder and this
record. V7 and every earlier source/review version remain immutable.

## Approval

Frank approved the corrected V8 mapping with the word “approved” on 21 October
2026. The external hash-pinned decision is
`docs/review/kitchen-oven-ligne-claire-v8-approval-2026-10-21.json`. That record
makes the exact V8 candidate the current Oven On visual authority without
rewriting this immutable pack, its closed pre-approval register, V41 source art,
Final assets or runtime selectors. Broken/flicker states and the dishwasher are
still outside this approval and remain separate future review gates.
