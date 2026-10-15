# Codex to Claude: Kitchen Basic Assets V1

Date: 16 October 2026  
Status: **reversible tier-1 draft awaiting Frank's visual review**. Approve,
promote and wire nothing from this batch.

## Review and files

- Review route: `/keeper-review/kitchen-basic-assets-v1/`
- Exact catalogue: `art/drafts/kitchen-basic-assets-2026-10-16-v1/asset-catalogue.json`
- Hash/register record: `art/drafts/kitchen-basic-assets-2026-10-16-v1/batch-register.json`
- High-resolution authored sources and generated visual references:
  `art/source/kitchen-basic-assets-2026-10-16-v1/`
- Logical-pixel drafts: `art/raw/kitchen-basic-assets-2026-10-16-v1/`
- Deterministic builder and verifier: `scripts/build_kitchen_basic_assets_v1.py`

The generated reference sheets are style references only. The builder owns the
exact dimensions, contacts, room widths, frame isolation and review media. No
production sprite, Keeper clip, runtime file, manifest, art register or live
game room was changed.

## Room decision and modular geometry

I propose Frank's preferred **outward-opening room door**. The committed stair
transition construction places the open leaf on the circulation side, away
from the room's furnishing field. This leaves a **4-lp / 32-ku** room-side frame
clear, so bay 1 begins at `x = 32 ku`. The 46 × 56-lp stair-cap source reserves
the historical door-zone canvas: its rightmost 4 lp are the room-side frame and
the remaining 42 lp depict the outward stair-side projection. This proposal
does not approve or alter the stair transition.

The room shell consists of:

| Piece | Logical size | Keeper-unit size | Note |
| --- | ---: | ---: | --- |
| Stair-side cap source | 46 × 56 lp | 368 × 448 ku | 4 lp enters room; door leaf projects outward |
| Repeat A/B/C | 21 × 56 lp each | 168 × 448 ku | Identical join pixels; only quiet plaster/floor variation changes |
| Far-wall cap | 38 × 56 lp canvas | 304 × 448 ku | Carries the 32 × 40-lp cupboard leaf/opening and is always last |

Assemblies for every width from 6 through 12 bays are generated and verified.
The requested compositions are **193 × 56 lp / 1,544 × 448 ku** at 9 bays and
**256 × 56 lp / 2,048 × 448 ku** at 12 bays.

## Measured item bounds and interaction spots

Bounds below are the largest opaque per-frame bounds across every supplied
state, not merely the canvas size. One-bay interactions use the bay centre.
All objects use a bottom-centre bay origin.

| Item | Largest measured bound | Bays | Local interaction offset | 9-bay absolute spot |
| --- | ---: | ---: | ---: | ---: |
| Pedal bin | 18 × 14 lp | 1 | 0 ku | 116 ku |
| Under-counter fridge | 19 × 19 lp | 1 | 0 ku | 284 ku |
| Kettle counter unit | 19 × 30 lp | 1 | 0 ku | 452 ku |
| Toaster counter unit | 19 × 30 lp | 1 | 0 ku | 620 ku |
| Basic oven | 19 × 26 lp | 1 | 0 ku | 788 ku |
| Mixer counter unit | 19 × 30 lp | 1 | 0 ku | 956 ku |
| Sink unit | 19 × 27 lp | 1 | 0 ku | 1,124 ku |
| Table and chair | 38 × 26 lp | 2 | −84 ku (left-bay chair centre) | 1,292 ku |
| Cleaning cupboard/far cap | 34 × 56 lp composite; 32 × 40-lp leaf/opening | 0 | final internal lattice line | 1,460 ku (9 bays); 1,964 ku (12 bays) |
| Pet bowl | 12 × 3 lp | 0; foreground child of table | 0 ku from table origin | 1,376 ku |

The sink dish overlays measure 12 × 5, 12 × 9 and 12 × 12 lp. They share the
sink's origin and do not alter its bay or interaction spot.

The table choice is deliberate: the chair sits at the centre of bay 8, 84 ku
left of the two-bay item origin, while the table extends through bay 9. The
Keeper steps into the back interaction lane to sit, leaving the foreground
walking lane open for the route to the cupboard. The existing `eat_seated`
seat point is 11.61 lp above its sprite bottom, within 0.61 lp of the 11-lp
chair-seat datum; Frank should still judge the visible plate/hand reach.

Frank's later 16 October decision is included: the pet bowl is centred at the
table origin (`x = 1,376 ku` in the nine-bay layout), belongs to the foreground
layer above both table and Keeper, takes no bay and moves with the table. Its
3-lp height leaves the route behind it unobstructed.

## States supplied

- Fridge: standard F1; door-opening F4; broken F4 with ajar/frost cue.
- Kettle unit: standard F1; steam/whistle-shake F4; broken F4.
- Toaster unit: standard F1; toast-pop F4; broken F4 with a short fired-toast
  arc.
- Oven: standard F1; hob-flame F4; broken F4 with smoke and sputtering ring.
- Mixer unit: standard F1; stirring-spoon F4; broken F4 with splatter cue.
- Sink: standard F1; running-tap F4; broken F4 with drip, plus three dish
  overlays.
- Bin: standard, full and overflowing F1 states.
- Pet bowl: empty F1, full F1 and cracked/puddle F4.
- Cleaning cupboard: closed F1, opening F4 and open F1.
- Table and chair: standard F1 only.

Every horizontal four-frame strip has a transparent gutter on both shared cell
edges. The builder fails if a frame touches a shared boundary, exceeds the
declared maximum, changes a shell width or loses the exact 19-lp oven width.

## Required review answers

### 1. Oven clips against a 19-lp door

**Draft answer: they read.** The review overlays both unchanged
`keeper_meal_from_oven_back` and `keeper_cake_from_oven_back` clips against the
exact 19-lp oven door. The rear torso registers with the door; hands, plate and
cake naturally extend outside its silhouette. The rack remains 10 lp above the
floor and the hob/worktop remains 19 lp. Do not widen the oven before Frank's
visual verdict.

### 2. Far-wall cupboard hides the cleaning change

**Draft answer: only at the fully hidden root.** The opaque 32-lp leaf hides the
Keeper's body in both the 9-bay broom and 12-bay basic-hoover demonstrations.
The wide broom/hoover composite can expose a prop tip if the swap is made while
the root is still approaching the opening. The implementation contract must
therefore switch clips only after the complete outgoing composite is behind
the far wall/leaf, and reverse that order on return. This is recorded as a
visible constraint; no Keeper clip or cupboard width was changed to conceal it.

## Twelve-bay reservation only

The 12-bay view contains dashed footprints, not higher-tier art: bin 1; fridge
2; kettle 1; toaster 1; range 2; mixer 1; sink/dishwasher 2; snack counter 1;
dumb waiter 1. The cupboard remains fixed in the far cap after bay 12.

## Approval boundary

Frank's review may accept, reject or request changes to this V1 draft. It does
not place anything in Final, promote art, update any manifest/register, approve
the outward door, modify Keeper animations or wire the live game.

## Documentation audit

Before hand-back I reconciled this note and the generated catalogue against the
latest kitchen brief (including Frank's later foreground pet-bowl decision),
the 172 × 56 room-grid handoff, `data/keeper_object_dimensions.json`, the
actual generated bounds/states, the review preload behaviour and the manual
deployment/archive workflow. `README.md` and `docs/DECISIONS.md` correctly
continue to describe the 46-lp standard-room doorway exclusion and historical
live-game art, because this batch's 4-lp outward-door geometry is an unapproved
kitchen-specific proposal and the live game is unchanged. No release metadata
or project backlog exists that should be advanced for an unapproved art draft.
