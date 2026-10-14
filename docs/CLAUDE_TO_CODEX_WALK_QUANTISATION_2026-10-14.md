# Claude to Codex: walk root motion and whole-step furniture placement

Date: 14 October 2026. From: Claude. Starting commit: `130e510` on `main`.

**Status:** for your assessment only. Frank has not decided yet; the question
is open on the project page as D1 and D7. Please don't change any approved
root motion, art or timing because of this note.

The full plan is on branch `claude/furniture-locomotion`:
`docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md` (section 6 and
appendices A–B have the measurements). Nothing of yours was edited; I measured
copies of the Walk V6 and stop → walk frames in a scratch folder.

## Frank's rules this has to meet

- Furniture snaps to a grid, and the Keeper stands at the asset's measured
  centre.
- **No split steps:** no stretched stride, no shortened final step, no snap.
  Leftover distance must be solved by quantisation: every route is whole steps
  plus the fixed start and stop.

## The problem

Units: **ku** = one pixel of the 256 × 320 registration cell (8 ku = 1 logical
px). Fast Timing V1 changes fps only, so these distances are unchanged:

| | ku |
|---|---:|
| Start bridge `2, 6, 12, 18` | 38 |
| Steady walk, per frame | 21 |
| One step, Walk F1 → F5 | 84 |
| One cycle | 168 |
| Stop bridge `18, 12, 6, 2` (exists only from Walk F1) | 38 |

A walk between two standing places is therefore `76 + 168n` ku. Even with a
second stop from F5, it would be `76 + 84n`.

**No three standing places on one floor can all be joined.** Take places
`a < b < c` in a row. Then `d(a,c) = d(a,b) + d(b,c) = 152 + 84k`, which leaves
remainder 68 on division by 84, not 76. So `a → c` can't be walked in whole
steps. This holds whatever the room width or furniture positions; the cause is
that the start + stop overhead (76) is not a multiple of the step (84). A
kitchen with a fridge, cooker, broom and pet bowl fails: 0 of its 20 routes
work.

What is *not* a problem:

- **Door routes.** Each place can be set a whole number of steps from a door.
  Using the Walk V6 opaque bounds (widest F1 −86…+105 ku, narrowest F3 −43…+69
  ku), every one of the 168 possible walk phases has at least one walking frame
  fully hidden behind a 24 lp leaf alone, in both directions. Costume swaps
  never constrain placement.
- **Timing.** Distance per frame is all that matters here; fps is free.

Alternatives already ruled out: spreading the remainder over the stride (Frank
rejected stretched strides), hidden-door absorption (it fixes only walks
through a door, never place to place inside a room), and placing furniture
cleverly (the proof above).

## The proposal (needs Frank's approval before anything changes)

Two changes together make every walk `84k` ku, so a one-step grid (84 ku =
10.5 lp) works and every place reaches every other place in both directions:

1. **Re-time the start and stop root motion to 42 ku each.** Candidates:
   `3, 7, 13, 19` (stop `19, 13, 7, 3`) or `2, 7, 13, 20` (stop `20, 13, 7, 2`),
   at most +1 ku per frame against the approved numbers. Frame bytes, order and
   timing are unchanged, and the stop stays the exact reverse of the start.
2. **A stop off the other foot:** Walk F5 → the exact approved Side-right stop,
   with the same deltas (its reverse can serve as a start into F5). This is the
   "two settle variants for the two lead-foot phases" already listed as P0
   item 2 in `docs/KEEPER_ANIMATION_HANDOFF.md`.

Neither works alone. A re-time alone gives `84 + 168n`, so only places an odd
number of steps apart connect. An F5 stop alone gives `76 + 84n`, and the proof
above still applies.

## What would help from you

- **Foot plant under each candidate re-time,** measured with the KP rig
  datums, or a better 42 ku split. My rough contact-row reading: the stance boot
  holds within a few ku from Walk F1 to F5 at 21 ku/frame, and the bridge sole
  patches already vary by a similar few ku.
- **Whether an F5 → stop bridge is feasible** from the approved authorities,
  and whether the shortest move (stop → F1 → stop, 84 ku, no steady frames)
  reads well as a one-step shuffle.
- **An authoring constraint for later:** every walk family the Keeper uses in
  a visible room (costume walks too) would need the same 84 ku step and 42 ku
  bridges. Speed is free; distance per step is not.

## Other points for you in the plan (section 13)

- **D7:** furniture pixel art is drawn at the nearest whole lp to its grid
  spot (offset ≤ 0.5 lp, inside the 0.5 lp contact tolerance), or authored as
  smooth density-8 art.
- **D9:** tiers keep their use centre and contact datums, but the footprint may
  grow. Frank wants growing upgrades, for example the oven: single, double,
  professional. This would replace "tiers retain footprint". Do you agree?
- **The catalogue `usePoint(-8,0)`** conflicts with Frank's measured-centre
  rule. Does any interaction truly need an offset? If so, it would be a whole
  number of steps.
- **Rooms over capacity under the 46 lp door rule, before any grid:** the
  living room back wall (73 lp of furniture in a 64 lp space), the bedroom with
  the en suite partition at x = 74, and the weather station (86 lp). Frank is
  being asked how these should fit (D5).
- **D10 (ladder foot on the grid) is withdrawn.** Frank decided on 14 October
  that ladders and stairways become a separate part of the lighthouse, never
  drawn inside a room, so every trip between rooms passes through a door. Room
  widths are not fixed yet and can be set to the half pixel.
- **D11:** please review the one-step shuffle visually once it exists.
