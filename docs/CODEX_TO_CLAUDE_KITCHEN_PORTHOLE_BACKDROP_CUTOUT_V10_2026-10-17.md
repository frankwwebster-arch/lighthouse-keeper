# Codex → Claude: Kitchen V10 approved-reference family hand-back

Date: 17 October 2026  
Status: reversible review draft; unapproved and unwired

## Frank's correction

The porthole must reveal the lighthouse's actual sea/sky backdrop and inherit
its weather and time naturally. The kitchen must not provide an illustrated
proxy.

## V10 response

- Rejected V9 as visual authority and returned to Frank's approved attached
  family sheet.
- Restored the detailed white fridge and replaced the shelf with a polished,
  correctly fitted one-bay child.
- Rebuilt each compatible worktop as one full-width slab in every state; no old
  centre segment remains between separately repaired wings.
- Removed every kitchen-owned condition underlay from the new version.
- Removed the faint glazing highlight from inside the opening.
- Kept the 19-lp brass ring as a separate sink-owned layer.
- Added a true 14-lp circular alpha knockout through the room-wall layer.
- Proved the completed room remains transparent at the aperture.
- Proved that wall knockout, frame and sink share the same bay transform at
  bays 2, 5 and 8.
- Used only a CSS checkerboard as technical alpha evidence on the review page;
  no checker, sea, sky or weather proxy is stored in a V10 PNG.

## Exact hand-back

| Item | Measurement | Ownership / role |
|---|---:|---|
| brass frame | 21 × 56-lp cell; 19-lp outer; 14-lp empty centre | sink child, z26 |
| room-wall knockout | 14-lp circular alpha opening | derived from sink transform at room layer |
| fridge | 21 × 21-lp cell; detailed white enamel; no brown top | one bay; foot line 52 lp |
| fridge shelf | 21 × 56-lp cell; ≤19-lp opaque width | fridge child; same x delta |
| kettle/toaster/mixer/sink slabs | 20-lp continuous slab in every frame | 21-lp cells; Option B |
| sink | corrected full-slab V10 object | z40; same x delta |

Required relation:

```text
wallKnockoutDeltaLp == frameDeltaLp == sinkDeltaLp
```

## Files to continue from

- Machine recipe: `data/kitchen_porthole_backdrop_cutout_v10_recipe.json`
- Human recipe:
  `docs/KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_RECIPE_2026-10-17.md`
- Builder: `scripts/build_kitchen_porthole_backdrop_cutout_v10.py`
- Verifier: `scripts/verify_kitchen_porthole_backdrop_cutout_v10.mjs`
- Catalogue and register:
  `art/drafts/kitchen-porthole-backdrop-cutout-2026-10-17-v10/`
- Immutable review route:
  `/keeper-review/kitchen-porthole-backdrop-cutout-v10/`

## Protection boundary

Do not wire, approve or promote V10 from this note. Runtime implementation must
apply the knockout in the room layer; merely drawing the transparent ring over
an opaque wall is insufficient. V7–V9 remain immutable historical sets;
Keeper, Final, production sprites and live manifests remain unchanged.

## Verification record

- Content commit: `4ab8315`.
- Production trigger: `a362356` (`[deploy]`).
- `npm test`: 18 test files and 179 tests passed, together with every kitchen
  and Keeper deterministic pretest.
- Review archive: V10 media is content-addressed; no public review binary is
  committed under the route.
- Live check: the production review route returned HTTP 200 and the archived
  refrigerator resolved as `image/png`, exactly `84 × 84` raster pixels.
- Documentation audit: README, decision history, background-window contract,
  V8 historical note, V10 recipe and this hand-back all agree that V9 is
  rejected, V10 is review-only, and nothing is approved, promoted or wired.
