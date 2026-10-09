# Keeper costume-route audit

Audit date: 2026-10-09. Authority: the 182-sheet keeper batch, its JSON
sidecars, `data/keeper_asset_contract.json` and the 164-card transition review.
This audit excludes the standard blue uniform and treats privacy coverings as
transition states rather than ordinary wearable costumes.

## Outcome

The new artist-smock family is the first activity outfit with a complete basic
route: side walk, side-to-front turn, side-to-back turn and front sit/stand,
followed by the existing side/rear painting and front pottery loops. Its walk
is frame-by-frame height-matched to `keeper_walk`; frame 4 was explicitly
corrected after being identified as undersized.

The next production priority is not another collection of isolated activity
loops. It is the small set of matching-outfit bridges below. Reversing a named
one-shot supplies its exit only where the endpoint is identical.

| Outfit/state | Existing coverage | Still needed | Priority |
|---|---|---|---|
| Artist smock | side walk; turn front/back; sit front; paint side/back; pottery front | no new core bridge; validate pottery and easel object contacts in-game | complete basic route |
| Light-blue pyjamas | side walk; turn rear; side door; bed entry; snore | side-to-front turn only if future front-facing bedroom actions use this outfit | P2 |
| Cream bathrobe | side walk; shower-door reach; rear shower entry | matching side-to-rear turn so the walk reaches the shower actions without a snap | P0 |
| Party hat | front idle; side walk; rear turn; seated cake; dance | side-to-front turn and matching side sit/stand; reuse them for dance and cake routes | P0 |
| Mechanic | side/front/back walks; side repair loop | side-to-front and side-to-back turns; no sit until a seated mechanic task exists | P1 |
| Old-school workout kit | weights rear; press-ups side; exercise bike front; trampoline front | side/front/back walk, side-to-front/rear turns, front bike mount/dismount and stand-to-floor press-up entry/exit | P0 family |
| Winter coat | side snow-clearing loop | side walk first; add a rear turn only if a rear winter task is approved | P0 |
| Striped swimming costume | horizontal/up/down swimming | pool-edge water entry and exit; land walking is unnecessary if changing remains hidden | P0 special entry |
| Scuba | horizontal/up/down swimming | dive/water entry and exit linked to equipment change; ordinary corridor walk is unnecessary | P0 special entry |
| Sou'wester/oilskins | side/front/back walks | side-to-front and side-to-back turns before weather-room actions are attached | P1 |
| Knight, pirate, spaceman, Halloween, Tarzan | side/front/back walks only | shared pose plan per costume: side-to-front turn, side-to-back turn, side/front sit only when an actual activity requires it | P2; activity-led |
| Towel privacy | bath/shower entry and exit | none as a free-walking family; transitions must remain within the bathroom occlusion route | intentionally limited |
| Mosaic privacy / privacy foam | bath, shower and hot-tub wash loops | dedicated matching entry/exit at the fixture; never expose as a walking outfit | intentionally limited |
| Party-hat transition | rear hat reveal only | no corridor route; gameplay costume change remains hidden behind a foreground door | flavour/reference only |

## Minimum next animation batch

1. `keeper_bathrobe_turn_back` (reversible).
2. `keeper_party_turn_front` (reversible) and `keeper_party_sit_side`
   (reversible).
3. `keeper_workout_walk_side`, `keeper_workout_walk_front`,
   `keeper_workout_walk_back`, matching front/rear turns, bike mount/dismount,
   and press-up lower/rise.
4. `keeper_winter_coat_walk`.
5. Swimming-costume pool entry/exit and scuba water entry/exit.
6. Mechanic and sou'wester turns when their room routes are implemented.

The novelty three-view walking families should not receive generic sit/turn
bulk work until a concrete activity needs it. This keeps each new sheet tied to
a playable route and avoids producing costume variants that never appear.

## Current machine inventory

- 17 non-standard outfit/state labels across 57 accepted sheets.
- 18 accepted states currently have no same-outfit walk; 13 of those are
  deliberate water/privacy/fixture states, while the winter coat and four
  workout-kit activities are the genuine locomotion gap.
- The artist-smock route contributes four new bridge/locomotion sheets.
- Every multi-frame sheet remains authored at 4fps by default; game code may
  override a clip's manifest FPS without altering its PNG.
