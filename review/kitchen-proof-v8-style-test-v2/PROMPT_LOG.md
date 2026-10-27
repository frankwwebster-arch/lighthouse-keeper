# Kitchen v8 Step 1 v2 — image-generation record

Tool: OpenAI built-in image-generation/edit tool.

Modes: `stylized-concept` for the inherited sink/dresser sources and
`precise-object-edit` for the cooker correction.

## References

| File | Role | SHA-256 |
|---|---|---|
| `review/kitchen-proof-v8-style-test/manifest.json` | immutable rejected predecessor | `96e1d8b6cc04b8e68309c550361899fbc6e2449bc786c00fa89241521006e0ef` |
| `review/kitchen-proof-v3-rebuild/sources/v7-oven-authority.png` | line/style authority | `0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538` |
| `reference/kitchen-mood/kitchen-mood-07-cooker.png` | old-school gas cooker, hood and grill subject reference | `a7575cdc4750c66254980fbeaa9ef7af433ca9485d19e8492fe3985ef0e3fff4` |
| `review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png` | exact 1:1 scale comparison; never generated | `a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3` |

## Inherited pieces

The selected Belfast sink (`sources/sink-pass-02-final.png`) and painted
dresser (`sources/dresser-pass-02-final.png`) are unchanged from v1. Their
prompts and provenance remain in the predecessor folder.

## Corrected cooker prompt contract

> Derive a single old-school British cream gas cooker from the supplied cooker
> photograph and the approved Kitchen v8 line/style family. Fill one exact
> standard-unit boundary, not the previous narrow slot. Include four burners,
> exactly four copper/orange control knobs, one small dark unlit status bezel,
> a raised eye-level hood/grill with tray and handle, and a lower oven with a
> copper handle and dark glass. Use confident near-black outlines, warm cream
> enamel, cobalt/navy structure and restrained copper accents. Straight-on
> orthographic game-asset view on transparent alpha, with no room, floor,
> character, text, external shadow, pink or magenta. Do not draw the future
> two-unit range.

Selected source: `sources/cooker-old-school-grill-pass-01-final.png`.

## Deterministic preparation

`build_style_test.py` removes exterior alpha below 32, crops the silhouette,
reduces it uniformly into the exact `126 × 252` canvas, preserves a two-pixel
transparent safety gutter and rebuilds the review sheets. It does not redraw,
stretch, palette-snap, promote or mutate the Prime Keeper.
