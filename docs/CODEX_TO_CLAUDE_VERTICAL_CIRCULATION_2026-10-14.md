# Codex to Claude: measured vertical-circulation foundation

Date: 14 October 2026
Status: **versioned construction proposal awaiting Frank's visual approval**. Do not wire it into runtime geometry yet.

## What is ready to review

- Root-motion Gate 1: `/keeper-review/keeper-root-motion-gate-v2/` (clearer
  presentation; V1 remains immutable)
- Stair, ladder and lift construction routes:
  `/keeper-review/keeper-vertical-circulation-v2/` (4× authoring ruler is not
  a fixed runtime screen size; V1 remains immutable)
- Machine-readable geometry: `art/drafts/keeper-movement-foundation-2026-10-14-v1/geometry/keeper-vertical-circulation-v1.json`
- Batch register and hashes: `art/drafts/keeper-movement-foundation-2026-10-14-v1/batch-register.json`

Nothing in this batch changes approved Keeper PNGs, Workbench Final, production sprites, the runtime manifest or room placement logic. The circulation drawings are a deterministic SVG mannequin study, not finished Keeper art.

## Root-motion Gate 1

The comparison follows the route table on `origin/claude/furniture-locomotion` row for row and uses the exact approved neutral, 15%, 50%, 75% and Walk F1 PNG bytes in both rows.

| Profile | Start | Stop | stop-to-stop distance |
| --- | --- | --- | ---: |
| Current approved | 2, 6, 12, 18 ku | 18, 12, 6, 2 ku | 76 ku |
| Candidate | 3, 7, 13, 19 ku | 19, 13, 7, 3 ku | 84 ku |

The candidate changes root translation only. It closes exactly one 84-ku / 10.5-lp placement interval. Both large and exact game-scale panes are synchronized, show cumulative root markers and preload/decode all five unique frame URLs before playback.

No F5 opposite-foot stop was drawn. That remains a later, separately approved art gate if Frank accepts the 84-ku candidate.

## Exact vertical module

The agreed room height is 56 lp of **clear internal height**. `docs/DOORS_STAIRS_AND_COSTUMES.md` explicitly leaves the floor/ceiling thickness for Codex to set before `FLOOR_STEP` is fixed. This proposal reserves one shared 4-lp structural deck between rooms:

| Datum | lp | ku |
| --- | ---: | ---: |
| Clear room height | 56 | 448 |
| Shared structural deck | 4 | 32 |
| Finished-floor to finished-floor pitch | 60 | 480 |

The deck is shared, not added at both the top and bottom of every room. Runtime `FLOOR_STEP` would therefore become 60 lp / 240 screen units at the current 4× stage scale only after approval. Room interiors remain 172 × 56 lp.

## Alternating straight stair

Frank's requested topology is one diagonal flight per storey, alternating direction forever:

- even flight: bottom-right → top-left;
- odd flight: bottom-left → top-right;
- floor insertion adds exactly one flight and flips parity above it;
- the route at a landing either turns into the next flight or walks toward the room door.

The measured flight is:

| Datum | lp | ku |
| --- | ---: | ---: |
| Riser count | 16 | — |
| Each riser | 3.75 | 30 |
| Total rise | 60 | 480 |
| Each tread advance | 5.25 | 42 |
| Total run | 84 | 672 |
| Walking intervals in run | 8 | 8 × 84 |
| Standing/turning margin at each end | 10.5 | 84 |
| Proposed stair-core width | 105 | 840 |
| Flight angle | 35.54° | — |

The Keeper's boot is 8 lp long, so a 5.25-lp tread supports 65.625% of it. That gives a readable cartoon overhang without asking him to balance on a 2–3 lp sliver. His front projection is 19 lp wide; a landing root 10.5 lp from the wall leaves 1 lp of edge clearance when he turns through the front pose.

The old 38-lp stair-core placeholder cannot be production geometry. A 60-lp rise in 38 lp is 57.7°, and any useful riser count leaves treads far too short for an 8-lp boot. The 172-lp room width does not shrink: the 105-lp circulation core sits beside it. Base room plus core is 277 lp; maximum agreed 214-lp room tier plus core is 319 lp. Camera fit should handle the wider whole-tower view; never rescale the Keeper or room contents.

One complete stair gait can use eight art frames and advance two treads: 84 ku horizontally and 60 ku vertically. Repeating it eight times closes one flight with no phase remainder. The construction preview currently samples four motion frames per individual stair contact (64 climb frames per flight); finished art timing remains open.

## Straight ladder

The ladder remains perfectly vertical and can continue through aligned floor openings.

| Datum | Value |
| --- | ---: |
| Rung pitch | 7.5 lp / 60 ku |
| Rung intervals per floor | 8 |
| Total rise | 60 lp / 480 ku |
| Suggested rail width | 18 lp / 144 ku |
| Full two-rung gait cycles per floor | 4 |

The review shows both required routes: continuous climbing past the landing, and climb → land → side dismount → horizontal walk to the room door. The continuous route must not reset limb phase at each storey. An exit may join the horizontal walk only after both feet are established on the landing.

## Lift

Lift stops repeat the exact 60-lp / 480-ku finished-floor pitch. The construction sequence includes:

- room/stair door walk → decelerate → stop at lift;
- zero-root turn fully away;
- depth entry, using the historical lift choreography only as a guide (100% → 78% scale and +6 lp rise);
- doors close only after the figure is inside;
- exact reverse for doors open → depth exit → side turn → stop-to-walk.

Final art may use stronger door occlusion and less visible depth scaling, but its exposed first/last frames must join the approved side neutral and walk bridge exactly.

## Runtime data shape after approval

Keep all values in integer ku. Suggested fixed data:

```json
{
  "floorClearKu": 448,
  "deckKu": 32,
  "floorPitchKu": 480,
  "stairCoreWidthKu": 840,
  "stairFlightRunKu": 672,
  "stairRisers": 16,
  "stairRiserKu": 30,
  "stairTreadKu": 42,
  "landingMarginKu": 84,
  "ladderRungPitchKu": 60,
  "ladderIntervalsPerFloor": 8,
  "liftStopPitchKu": 480
}
```

Route endpoints should be named and parity-aware, for example:

- `stair.landing.near.floor<N>`
- `stair.landing.far.floor<N>`
- `ladder.on.floor<N>` / `ladder.continue.floor<N>`
- `lift.threshold.floor<N>` / `lift.hidden.floor<N>`
- `stairDoor.transfer.floor<N>`

Do not infer stair direction from room identity, because randomly inserted floors change vertical parity. Derive it from the saved tower slot after insertion. A route to the room door from the far stair landing is exactly eight 84-ku horizontal intervals; a near landing is one interval from the transfer anchor in the construction study.

## Verification required when wired

After Frank approves geometry and later finished animation art exists, Claude should add deterministic tests for:

1. every storey rise is exactly 480 ku;
2. stair flight rise closes at 16 × 30 ku;
3. stair flight run closes at 16 × 42 ku and 8 × 84 ku;
4. alternating flight parity survives floor insertion/removal;
5. far-landing exit is an integral horizontal route;
6. ladder rungs close at 8 × 60 ku;
7. lift stops align with every finished floor;
8. continue routes retain gait phase across the floor boundary;
9. exit routes reach a registered horizontal stop/turn/walk endpoint;
10. no runtime scaling changes Keeper identity;
11. room clear dimensions remain 172 × 56 lp at base tier;
12. camera fit includes the 105-lp circulation core at 172, 193 and 214-lp room widths.

Until Frank approves the review pages, retain the current runtime and Claude route tables unchanged.
