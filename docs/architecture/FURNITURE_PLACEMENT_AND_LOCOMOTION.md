# Furniture placement and phase-aware locomotion: Phase 1 plan

Date: 14 October 2026. Author: Claude. Status: **proposal, awaiting Frank's
decisions** (section 13). No runtime code, art, register, manifest, review page,
Workbench lane or approved hash is changed by this document.

- Branch: `claude/furniture-locomotion`.
- Starting commit: `abe2372` on `main`, a documented successor of `65fe2ec` and
  `cca03dc`. It adds only `CLAUDE.md` and the Phase 1 prompt.
- Task source: `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`, "Requested
  architecture deliverable", points 1–8.
- Frank's binding answers (project page, 14 October): plan first; Ralph and
  Eddie will move furniture themselves, so the rules must guide a child gently;
  furniture snaps to a grid and some places are impossible for some items;
  neighbours may shuffle aside along the grid while an item is dragged; items
  can grow when upgraded; the Keeper anchors to the measured centre of the
  asset; **split steps are never acceptable** (no stretched stride, no shortened
  final step, no snapping), so leftover distance is solved by quantisation.

Written for Frank (section 0), Codex (sections 1–8, 12, 13) and the Claude
session that builds Phase 2.

---

## 0. In plain English

1. **The walk is exact.** Every step moves him 10.5 art pixels, and starting
   and stopping take a fixed distance. So the places he can stop are like the
   squares on a board game, and furniture has to sit on those squares.
2. **With today's walk data the board doesn't work.** Starting plus stopping
   adds 9.5 px, which is not a whole number of steps. The arithmetic (section
   6.2) shows that no three standing places in a row can all be joined by
   whole steps. A kitchen with a fridge, cooker, broom and pet bowl can't work.
   No amount of clever placement fixes this.
3. **Two small changes from Codex fix it completely.** (a) Make starting and
   stopping each cover 5.25 px instead of 4.75 px. That is one extra
   high-resolution pixel on each of the four bridge frames, a change in motion
   numbers only, with no redrawing. (b) Draw one more short stop: stopping off
   the other foot. With both, the floor becomes a grid of places 10.5 px apart,
   and **every place can reach every other place, and the stairs, in whole
   steps, in both directions**. The full kitchen works (section 6.4).
4. **The cost is placement freedom.** In a standard room an item has 2 to 6
   possible places instead of roughly 27 to 57. Gaps between items come in
   10.5 px amounts, so a room loses up to one step's width per gap (section
   6.5).
5. **Growing upgrades are fine.** Each upgrade keeps the same centre, so he
   still stands in the same place. Only the item's width changes. If the bigger
   item doesn't fit, its neighbours slide aside along the grid. If even that
   fails, the game says what to move instead of just refusing (sections 2 and
   3).
6. **One problem exists before any grid.** With the 46 px door rule, the living
   room, bedroom/en suite and weather station furniture in the catalogue is
   wider than the space allowed. Codex or Frank needs to decide how those rooms
   fit (section 12).

---

## 1. One coordinate contract

### 1.1 The units

| Name | Symbol | Definition | Where it is used today |
|---|---|---|---|
| Keeper unit | **ku** | One pixel of the 256 × 320 high-resolution Keeper registration cell (density 8) | Codex's root-motion data (`2, 6, 12, 18`, `21`, `18, 12, 6, 2`), Prime art, review pages |
| Logical pixel | **lp** | One art pixel of the 32 × 40 Keeper cell and of object art; **1 lp = 8 ku** | Studio (`recipe.ts`), dimension datums, catalogue, sprite manifest `w`/`h` |
| Stage unit | **su** | The game's SVG stage, 1200 × 760 (`world.ts`); **1 lp = 4 su** (`PX = 4` in `Sprite.tsx`), so **1 su = 2 ku** | `config.ts` object `x`, `world.ts`, `Actors.tsx`, `floors.tsx` |
| CSS pixel | **css** | What the browser draws after the SVG viewBox scale and camera zoom | Display only |

The Keeper's game-scale box is 128 × 160 css at `PX = 4` and zoom 1, so at zoom
1 one css pixel is 2 ku.

### 1.2 The rule

- **Every model quantity is an integer in ku.** That covers positions, root
  deltas, footprints, grid spots, clearances and route distances. A
  non-integer anywhere in the model is a test failure. 21 ku per frame is 2.625
  lp or 10.5 su, so lp and su can't hold the walk without fractions. ku is the
  only unit that can.
- **Floor-local x** is measured in ku from the room's **door wall** (the wall
  between the stairway and the room, `x = 0` in the studio), positive into the
  room. One floor is one line: stairway, room and any inner room share it.
- **Conversion happens at three explicit boundaries and nowhere else:**
  1. *Import:* art and datums in lp are multiplied by 8 when a record is built.
  2. *Render:* `su = towerInteriorLeft + ku / 2`. Halves of a stage unit are
     allowed for the Keeper, because Prime art is smooth density-8 art, not
     pixel art.
  3. *Legacy migration:* today's `config.ts` su positions become grid spot
     indices once (section 2.5). They are never read again at runtime.
- **The renderer must not re-snap the Keeper.** `Sprite.tsx` rounds every
  sprite's x to whole logical pixels (`Math.round((x - w/2)/PX)*PX`). Applied
  to the walk, that turns the steps 0, 21, 42, 63 ku into 0, 24, 40, 64 ku: a
  foot slide of up to 4 ku (half an art pixel) on every frame. Density-8 actors
  bypass that rounding. Furniture art is placed as in section 2.4.

### 1.3 Mismatches the contract resolves

| Today | Value | Contract |
|---|---|---|
| Studio room width | 110 lp = 880 ku | Authoritative (agreed floor plan) |
| Game interior (`floors.tsx` `CORE.interiorWidth`) | 420 su = 105 lp | Prototype; follows the 110 lp room when Codex's 56 px floors land |
| Game walkable interior (`world.ts` `INTERIOR`) | 70–450 su = 95 lp | Replaced by room records (section 2.3) |
| `FLOOR_STEP` | 140 su = 35 lp | Becomes the agreed 56 lp clear height plus Codex's band |
| Studio "positions are whole pixels so the art stays crisp" | lp rounding | Only for density-4 legacy sprites; never for the Keeper |

---

## 2. Furniture placement records

### 2.1 What is measured, and where it comes from

| Field | Meaning | Source of truth |
|---|---|---|
| `useCentre` | The asset's measured centre along the floor. The Keeper's registered anchor stands exactly here | Frank's rule; Codex measures it per tier from the art |
| `footprint` | `[left, right]` ku from `useCentre`: the floor span the item occupies, art plus any declared breathing space | Per tier (Frank: items may grow) |
| `solid` | Intervals the Keeper may not walk into, as `[left, right, topLp]`; empty for back-wall items he passes in front of | Per tier |
| `lane` | `back` (against the back wall, drawn behind him) or `front` (drawn in front, always solid) | Per type |
| `renderAnchor` | Where the art's own pixels sit relative to `useCentre`: the measured-centre offset inside the sprite, in lp | Per tier, from the art |
| `approach` | Allowed arrival facings (`left`, `right`, `either`) and the required action facing (`side-left`, `side-right`, `front`, `back`) | Per type, from the interaction |
| `contacts` | Seat 11, surface 19, handle 20 and so on | `data/keeper_object_dimensions.json`; invariant across tiers |
| `effectOrigin`, `bubbleOrigin` | Particle and thought-bubble origins, lp relative to `useCentre` | Per tier |
| `z` | Draw order within its lane | Per type |
| `zone` | Which room zone it may stand in (for example bedroom, en suite) | Per placement |

The Keeper's measured centre is his registered anchor. In the approved
Side-right stop frame the opaque body spans cell x 77–179, centred exactly on
128 = anchor `[16, 40]` × 8 (Appendix A). Anchor-to-centre alignment is
therefore an alignment of measured centres, as Frank asked.

### 2.2 Proposed shape (Phase 2 types; written here, not in code)

```ts
type Ku = number // integer, 1/8 logical pixel

interface FurnitureType {
  id: string                       // config.ts ObjectId, e.g. 'cooker'
  lane: 'back' | 'front'
  approach: { arrive: 'left' | 'right' | 'either'; act: 'side-left' | 'side-right' | 'front' | 'back' | 'arrival' }
  tiers: TierGeometry[]            // tier 1 first
}

interface TierGeometry {
  tier: number
  sprite: string
  renderAnchor: [number, number]   // lp inside the sprite that sits on useCentre
  footprint: [Ku, Ku]              // left (negative) and right extent from useCentre
  solid: { from: Ku; to: Ku; topLp: number }[]
  contacts: Record<string, number> // lp above the floor; must equal every other tier's
  effectOrigin?: [number, number]
  bubbleOrigin?: [number, number]
}

interface Placement {               // what the save file stores
  object: string                   // ObjectId
  floor: string
  spot: number                     // grid index: x = spot × 84 ku
  tier: number
}
```

A placement stores a **spot index**, never pixels, so saving and loading
can't drift.

### 2.3 Room records

Each room is data, not a picture. It holds walls (`[0, 880]` ku for a standard
room), each door (its wall x, leaf side, occluder interval and clear area), any
inner door, and its zones. Movable furniture is **never baked into a room
plate** (the handoff's rule). The room plate is walls, floor and fixed fittings
only.

### 2.4 Rendering furniture on the grid

Grid spots fall every 10.5 lp, so every other spot lands on a half art pixel.
Furniture art is density-4 pixel art, so I propose that its sprite is drawn at
the nearest whole logical pixel to `useCentre - renderAnchor`. This keeps the
pixel grid of the furniture aligned with the room plate. The Keeper stays
exactly on the spot. The resulting contact offset is at most 4 ku = 0.5 lp,
which is inside the existing contract ("land within 0.5 logical pixel",
`keeper_object_dimensions.json`). It is deterministic, because the rounding
rule is fixed. If Codex draws furniture as smooth density-8 art, no rounding is
needed. (Decision D7.)

### 2.5 Upgrades that grow: resolving the conflict with Codex

- **Codex's handoff:** "Tier upgrades retain footprint and use points unless a
  reviewed migration says otherwise". The catalogue gives every tier the same
  frame size today.
- **Frank:** some items get larger (oven: single, double, professional).
- **Proposed resolution (flagged for Codex's agreement, D9):** tiers keep their
  `useCentre` and every contact datum; the footprint may differ per tier.
  Because the Keeper stands at `useCentre`, every tier keeps the same standing
  spot and the same animation. That keeps Codex's "one set of animations serves
  every tier", and the oven grows around him. This document is the "reviewed
  migration" the handoff asks for. It replaces only the footprint half of
  Codex's rule.
- Codex draws each tier so that its measured centre is the use centre. A
  double oven grows equally both sides of where he cooks, or declares an
  asymmetric `footprint`; asymmetric growth is allowed.

### 2.6 Reconciling today's evidence

| Evidence | Finding | Disposition |
|---|---|---|
| `config.ts` `OBJECTS[].x` | One su x per object, no width | Migrated once to spot indices; ignored afterwards |
| Catalogue `usePoint(-8,0)` (almost every item) | Keeper 8 lp left of the object anchor | Superseded by Frank's centre rule; side-use offsets, where truly needed, become whole steps (multiples of 84 ku) |
| Catalogue proposed locations (kitchen fridge 30, cooker 53; bedroom bed 18 …) | Inside the 46 lp door clear area | Not kept; re-placed on the grid |
| Catalogue tier frames identical across tiers | Codex's "retain footprint" | Kept until Codex draws a grown tier |
| Studio `Spot.dx` per variant | Free lp offsets | Becomes "0 by default, whole steps otherwise" |
| Studio `placeX('@table')` "just clear of the nearer edge" | Stopping point depends on approach side | Retired for furniture: he stops at the centre spot |
| Dimension datums (seat 11, surface 19 …) | Heights, invariant across tiers | Kept as `contacts` |
| Living-room catalogue: "upgradeable armchair foreground" overlapping the piano | A front-lane item covering another item's use point | Rejected by the validator (section 3.2, rule 6) |

---

## 3. A placement grid and validator that guides a child

### 3.1 The grid

- **Spot pitch: 84 ku = 10.5 lp = 42 su = one Keeper step.** It is the
  smallest pitch that keeps every route whole once the walk changes in
  section 6.3 land. At zoom 1 a spot is 42 css wide, a comfortable finger
  target for Ralph and Eddie.
- **Origin: the door wall, `x = 0`.** Spot `k` is at `84k` ku. One lattice runs
  through the whole floor: stairway, room and inner room. Codex places the
  ladder foot, lift entry and spiral-stair foot on it. I recommend the ladder
  foot at −168 ku (−21 lp), inside the 38 lp stairway. The studio's current
  −27 lp sits off the grid and, measured, costs the kitchen its fourth item
  (Appendix B).
- **Only centres snap.** Widths stay as the art needs (any whole ku). An item
  occupies `useCentre + footprint`, checked as intervals, not as whole cells.

### 3.2 Hard rules (the validator)

A placement is legal when all of these hold, for its current tier:

1. Its centre is on a grid spot.
2. Its footprint lies inside the room walls.
3. Its footprint stays out of every door clear area (46 lp = 368 ku at each
   door, on the side the leaf opens, as the studio already enforces).
4. In its lane, it does not overlap another item's footprint.
5. Its use spot is reachable from the room's door: no `solid` interval
   (including any `front`-lane item) lies between the door and the spot, except
   the item itself.
6. No `front`-lane item covers any opaque pixel of the Keeper while he stands
   at, approaches or acts at any reachable use spot. The studio's per-frame
   cover check is reused.
7. Every use spot keeps the whole Keeper inside the room (stop pose ±51 ku,
   walking frames up to −86/+105 ku, Appendix A).
8. Every grid spot that a route uses is on the lattice. This is automatic once
   rule 1 and the ladder rule hold.

### 3.3 Soft rules (shown, never blocking)

- "Room to grow": the item's next tier would not fit where it stands.
- "A long way round": a placement more than N steps from the door, where N is
  tunable.

### 3.4 How a child is guided (drag, preview, drop)

While an item is dragged, the nearest spot is computed every frame and the
item's ghost snaps there. The ghost shows one of three states:

- **Green, fits:** drop to place.
- **Amber, fits if others shuffle:** neighbours slide aside live, along the
  grid, showing exactly where they would go (Frank's mechanic). Dropping
  commits all the moves together, and one Undo reverses them.
- **Grey, can't go here:** shown with a picture and a short reason. For
  example "The door needs this space to open", "Too big for the gap, try
  here", or "This would block his way to the bed". The ghost also points to
  the nearest spot where it would fit.

Shuffle rules, all deterministic:

1. Neighbours move outward from the dropped item by the fewest whole spots that
   clear the overlap, cascading to the next neighbour if needed.
2. The left-to-right order of items is kept; items never jump over one another.
3. Walls and door clear areas are fixed; nothing is pushed into them.
4. If both "push left" and "push right" solutions exist, the one moving the
   fewest steps in total wins. A tie goes to pushing away from the door.
5. Nothing is ever moved to another room or removed by the shuffle.
6. If no solution exists, the state is grey, with the nearest fitting spot
   suggested.

Worked example, the kitchen on the grid (Appendix B):

| Situation | Result |
|---|---|
| Fridge 12, cooker 18, broom 8, bowl 10 lp | Fits: centres 52.5, 73.5, 94.5, 105 lp (right edge exactly 110) |
| Cooker upgraded to a 30 lp double oven | Fits in place, with no shuffle needed |
| Cooker upgraded to a 40 lp professional oven | Can't fit with all four (70 lp of furniture in a 64 lp space, even without a grid). Grey: "Make room: move the pet bowl or the broom to another room." |

The same engine runs at upgrade time: before an upgrade is bought, the shop
can show whether the bigger item fits as things stand, with the shuffle
preview if it fits after a shuffle (decision D3).

### 3.5 Who uses it

Phase 2 builds the pure validator and shuffle. Codex and I use it first through
the studio. The children's drag-to-place screen is a later feature built on
the same module.

---

## 4. A route plan, not just a destination

A route is compiled once, deterministically, from `(from, to, placements,
layout, outfits)`:

```ts
interface RoutePlan {
  from: Stand                         // { floor, spot, facing, pose }
  to: Stand
  legs: Leg[]
  arrival: { spot: number; facing: Facing; turn: ClipRef[]; ingress: ClipRef[] }
  departure?: { egress: ClipRef[] }   // action → exact stop → (turn) → walk-start
  totals: { frames: number; ms: number; distanceKu: Ku }
}

type Leg =
  | { kind: 'turn'; from: Pose; to: Pose; clips: ClipRef[] }               // zero root motion
  | { kind: 'walk'; floor: string; fromSpot: number; toSpot: number; dir: 'left' | 'right';
      steps: number;                                                       // k ≥ 1 whole steps of 84 ku
      start: 'stop→F1'; stop: 'F1→stop' | 'F5→stop';                       // F1 if k is odd, F5 if k is even
      doors: { door: string; hiddenFrame: number; swapTo?: string }[] }   // occluded lead-in / lead-out
  | { kind: 'climb'; via: 'ladder' | 'spiral' | 'lift'; fromFloor: string; toFloor: string; clips: ClipRef[] }
```

- **Door and stair transfer points** are grid spots: the ladder foot on each
  floor, and so on.
- **Occluded lead-in and lead-out:** each door crossing records the frame on
  which he is fully hidden, where a costume swap happens. Measured: with the
  24 lp leaf alone, every one of the 168 possible walk phases has at least one
  fully hidden walking frame, in both directions (Appendix A.3). The grid
  therefore never has to bend to make a costume change possible.
- **Exact stop anchor:** `toSpot × 84` ku, an integer, reached by the stop
  bridge itself (section 5).
- **Optional turn:** side → front or side → back using the approved turns,
  with zero root motion. Arriving facing the "wrong" side for a side action
  costs a two-turn about-face (side → front → side), never a step.
- **Action ingress and egress:** the universal sequence from
  `docs/RECIPES.md`: `walk → moving stop → optional turn → action`, and back
  through `action → exact stop → reversed walk-start → walk`.

---

## 5. A phase-aware locomotion controller

**One timeline drives both the frame and the position.** The route compiles to
a frame table. Each row holds `{ clip, frame, durationMs, dxKu, xKu, phase,
leadFoot, events }`. Runtime picks the row for the current time and draws that
frame at that row's `xKu`. Position is held for the row and changes only when
the frame changes. This is exactly how Codex's registers and the Timing Lab
already work (`x` per frame, Appendix A.1). Nothing moves between rows, so a
planted foot can't slide between frames.

A walk of `k` steps (84 ku each) compiles to:

| Part | Frames | Root deltas (ku) | Lands on |
|---|---|---|---|
| Start bridge | stop → 15% → 50% → 75% → Walk F1 | 4 deltas summing to 42 (proposed; 38 today) | Walk F1 |
| Steady | `4 × (k − 1)` walk frames | 21 each | Walk F1 if `k − 1` is even, Walk F5 if odd |
| Stop bridge | the matching stop (F1 or F5) | 4 deltas summing to 42, the exact reverse of the start | The exact stop pose, on the spot |

The total is `42 + 84(k − 1) + 42 = 84k` ku: whole steps, every time. The
duration is `4k + 4` frames, so `(k + 1)/2` s at the approved 8 fps.

Guarantees, each a Phase 2 test:

- **Acceleration moves at once:** the first start delta is at least 2 ku.
- **No frame in a walk has zero movement.** Only the deliberate stop holds
  outside the walk have none.
- **Arrival is the exact stop frame at the exact spot.** It is reached by the
  table, not by snapping.
- **Left is the mirror of right:** deltas are negated, frames mirrored, and the
  spot is identical.
- **Timing is separate from distance.** Timing comes from the approved Timing
  Lab profile (walk fps, deceleration fps, settle, turn fps). Changing the fps
  changes when a row shows, never how far it moves.

Changing orders mid-walk (this replaces `Actors.tsx`'s "snap to the job"):

- **Same direction, further or nearer:** recompile the remaining steps. Every
  spot is reachable, so no stop is needed, provided the new target is at least
  one step ahead of the next stop opportunity.
- **Behind him:** carry on to the next F1 or F5 frame (at most 3 frames, under
  0.4 s), play the stop onto that spot, about-face, and walk back.
- **The engine "gives up waiting":** the walk completes. The model never
  teleports him.

---

## 6. The remainder policy: quantisation, with the evidence

### 6.1 Measured step lengths

From Codex's committed registers (Appendix A.1), at 8 fps:

| Quantity | ku | lp | su |
|---|---:|---:|---:|
| Steady walk, per frame | 21 | 2.625 | 10.5 |
| One step (contact to opposite contact, 4 frames, Walk F1 → F5) | 84 | 10.5 | 42 |
| One cycle (8 frames, two steps) | 168 | 21 | 84 |
| Start bridge `2, 6, 12, 18` | 38 | 4.75 | 19 |
| Stop bridge `18, 12, 6, 2` | 38 | 4.75 | 19 |
| Start + stop overhead today | 76 | 9.5 | 38 |
| Approved stop → walk → stop route (2 cycles) | 412 | 51.5 | 206 |

The approved stop exists **only from Walk F1** (`walk-to-stop-right`,
`startPose: walk-right_f1`). The planted front boot measured on the floor rows
holds at world x ≈ 202–234 ku from Walk F1 through F5 while the body advances
84 ku, which confirms that 21 ku per frame is the foot-locked speed (Appendix A.2).

### 6.2 Why today's numbers can't be quantised

With stops only from F1, a spot-to-spot walk is `76 + 168n` ku. Adding a stop
from F5 gives `76 + 84n`.

**Claim:** no three standing places on one floor can all be joined pairwise.
**Proof:** take places `a < b < c` in a row. Then `d(a,c) = d(a,b) + d(b,c)`.
If each distance is `76` plus a multiple of 84, then `d(a,c) = 152 +` a
multiple of 84, which leaves remainder 68 when divided by 84, not 76. So
`d(a,c)` is not walkable. The same holds with the 168 cycle. ∎

This is not a matter of choosing positions cleverly. The overhead (76 ku) is
not a multiple of the step (84 ku). A kitchen needs five standing places (the
ladder foot plus four items), so it can't work. Appendix B shows every kitchen
route failing on today's data.

### 6.3 Options compared

Codex listed four families. Here they are against Frank's rules and the
measurements:

| Option | What it needs | Result | Verdict |
|---|---|---|---|
| **A. Quantise, with re-timed bridges plus an opposite-foot stop** (recommended) | Codex re-times start/stop root motion to 42 ku each (for example `3, 7, 13, 19` and the reverse `19, 13, 7, 3`, at most +1 ku per frame), and draws one new 3-pose bridge from Walk F5 to the same exact stop | Every walk is `84k` ku. Every spot reaches every other spot and the stairs in both directions | Meets every rule. No per-route adjustment, ever |
| B. Re-time only, stop from F1 only | Re-timed numbers, no new art | Walks are `84 + 168n`: only places an odd number of steps apart are joinable. With three or more places, two always share a parity | Fails |
| C. Opposite-foot stop only, no re-time | New bridge, approved numbers kept | `76 + 84n`: the proof in 6.2 applies | Fails |
| D. Hidden-door absorption | Shift him while he is fully hidden by a door | Measured spare room behind the 24 lp leaf: about 80 ku on the narrowest frame (F3), not quite a step. With the 4 lp jamb, 112 ku. But spot-to-spot walks inside a room never pass a door, so it can't fix the main case | Fallback only, for fixed structures (lift, outside), and only after Frank sees it |
| E. Bounded per-frame adjustment | Spread the remainder over the walk's frames | Up to 41 ku of error, about 5 ku per frame over 8 frames | Rejected by Frank (a stretched stride) |
| F. Finer grid (5.25 lp) with stops from the passing poses F3 and F7 as well | Two more bridges, stopping with one foot in the air | Halves the wasted space per gap | Not recommended: awkward stops and twice the art; kept as a future option |

**What Option A costs visually:** each of the eight bridge frames moves at most
1 ku (1/8 art pixel, 0.5 css at game scale) more than today. Codex must
measure the planted foot with the KP rig to confirm it doesn't skate, then put
the new numbers through the Timing Lab or a review page for Frank's approval.
These numbers are approved motion data, so they can't change silently. An
alternative split such as `2, 7, 13, 20` is equally valid; Codex picks whichever
plants better. The new F5 stop is the "two settle variants for the two
lead-foot phases" already listed as P0 item 2 in
`docs/KEEPER_ANIMATION_HANDOFF.md`.

One step is `start + stop` with no steady frames (stop → F1 → stop, 84 ku). It
is the shortest move between neighbouring spots. Codex should check that this
one-step shuffle reads well.

### 6.4 Reachability, proved on the recommended grid

The kitchen on the grid, with the ladder foot at −168 ku. Entries give the
number of whole steps and which stop is used. Every route works both ways (the
left-going walk is the mirror).

| From \ to | Ladder foot | Fridge (420) | Cooker (588) | Broom (756) | Bowl (840) |
|---|---|---|---|---|---|
| Ladder foot (−168) | – | 7, F1 | 9, F1 | 11, F1 | 12, F5 |
| Fridge | 7, F1 | – | 2, F5 | 4, F5 | 5, F1 |
| Cooker | 9, F1 | 2, F5 | – | 2, F5 | 3, F1 |
| Broom | 11, F1 | 4, F5 | 2, F5 | – | 1, F1 |
| Bowl | 12, F5 | 5, F1 | 3, F1 | 1, F1 | – |

The same table on today's data: every one of the 20 routes is impossible
(Appendix B). In general, with Option A **any two grid spots** `i` and `j` on a
floor are `|i − j|` whole steps apart, so the table never has a gap.
Door crossings on these routes always contain a fully hidden frame (A.3).

### 6.5 What it costs in placement freedom (measured)

The places an item's centre can take in a standard 110 lp room with one door
(46 lp clear area):

| Item width (lp) | Whole-pixel placement | On the 10.5 lp grid |
|---:|---:|---:|
| 8 | 57 | 6 |
| 12 | 53 | 5 |
| 15–30 | 35–49 | 4 |
| 38 | 27 | 2 |

Packing: two neighbours must have centres at least half their combined widths
apart, rounded up to a whole step. The loss is up to 10.5 lp per gap, about
5 lp on average. Measured: the kitchen's four items need 94 lp of the room on
whole pixels and exactly 110 lp on the grid. It still fits, with nothing to
spare. The aquarium and lair also fit. A grid anchored 36 ku differently (the
studio's ladder at −27 lp) loses the kitchen's fourth item, which is why the
origin is the door wall.

### 6.6 Rules this places on future art (for Codex)

- Every walk family the Keeper uses in a visible room (pyjamas, smock and so on)
  must share **84 ku per step and 42 ku start and stop bridges**. Speed (fps) is
  free; distance per step is not.
- Every standing transfer point is on the lattice: ladder foot, lift entry,
  spiral-stair foot, inner door approach, cubicle and outside walkway points.
- Side-use offsets, where an action truly needs one, are whole steps.

---

## 7. Deterministic tests (Phase 2)

The handoff's list, plus the guarantees above. All are pure, with no clock, DOM
or randomness:

1. The same inputs give byte-identical placements, shuffles and route tables.
2. Every coordinate is an integer ku, and every use spot is `84k`.
3. Footprints never overlap within a lane. No footprint enters a door clear
   area or leaves the room.
4. Every placed item's use spot is reachable from the door, and from every
   other spot, in both directions.
5. Every compiled walk totals `84k` ku. The sum of `dxKu` equals the
   destination minus the origin.
6. Frame and root motion agree: the start rows are the start bridge frames with
   their deltas, steady rows cycle F1…F8 at 21 ku, and the stop matches the
   lead foot.
7. The first moving row has `dxKu ≥ 1`; no walk row has `dxKu = 0`.
8. The final row is the exact stop frame at the exact spot.
9. A left route is the exact mirror of the right route (negated deltas, same
   frames mirrored).
10. Every door crossing contains a fully hidden frame, checked with the
    measured frame bounds.
11. Save then load gives identical placements (spot indices); legacy saves
    migrate deterministically.
12. Changing tier never moves `useCentre` or any contact datum; a footprint
    change re-runs the validator.
13. The shuffle is deterministic, keeps order, never crosses walls or doors,
    never changes room, and reports "no fit" instead of overlapping.
14. A guard test fails if the walk numbers in the registers stop satisfying
    `start + stop ≡ 0 (mod step)`. A future art change can't silently
    re-break quantisation.
15. Interrupting a walk starts its stop within 3 frames and ends on a grid spot,
    with no teleport.

---

## 8. Debug overlay proposal

A diagnostic layer for the studio and the game (`?debug=floor`), never
production art. It shows:

- **Grid:** every spot as a tick, with its index; door clear areas shaded;
  the ladder foot, lift and door occluders outlined.
- **Footprints:** each item's footprint (outline) and solid intervals (hatched),
  per lane; the next tier's footprint as a dashed outline.
- **Use spots:** a foot marker at each `useCentre` with the arrival facing
  arrow.
- **Route:** each leg as a line, steps as notches every 84 ku, door crossings
  with the hidden frame marked, stop marked F1 or F5.
- **Live gait:** current clip, frame, lead foot, `dxKu` for this frame, `xKu`,
  and **planned remaining ku**. The **residual** is shown and must read 0 at
  every stop. Any other value is a bug.
- **Validator:** each item's state (fits, shuffles, can't), with the reason.

---

## 9. How this fits the code that exists (Phase 3, later)

| File | Today | Becomes |
|---|---|---|
| `src/studio/recipe.ts` | Room 110 lp, door constants, `DOOR_CLEAR`, `Spot`, `Category`/`Variant`, `checkSolids`, whole-stride walks that **stretch the speed** | The studio keeps its format but takes positions, spots and walk tables from the new pure module. The speed stretch (`Math.round(dist/speed·fps/round)`) is removed, because it is the stretched stride Frank ruled out. `checkSolids` and the door clear check are reused by the validator. |
| `src/game/config.ts` | One su `x` per object | Default placements as spot indices, plus per-tier geometry |
| `src/game/world.ts` | `route()` returns x waypoints | Calls the route compiler; stair transfer points come from the lattice |
| `src/ui/Actors.tsx` | `SPEED = 240` su/s, constant, independent of the frame; snaps to the job when the engine ends a walk | Plays the frame table; no snapping |
| `src/ui/floors.tsx` | Zones only, `LivingFurniture` baked into the living floor | Room records; furniture drawn from placements |
| `Sprite.tsx` | Rounds x to whole lp | Exempts density-8 actors |

**Phase 2** (after Frank's answers) is a new isolated module, for example
`src/placement/`, holding the types, grid, validator, shuffle, route compiler,
frame-table builder and the tests in section 7. It has no imports from the UI
and no runtime wiring. It can be built against both the approved numbers
(which demonstrates the failure) and Codex's re-timed proposal.

---

## 10. Assumptions

- Root motion is applied per frame, as in Codex's registers and the Timing Lab;
  it is not interpolated within a frame.
- Turns between side, front and back have zero root motion, as in the approved
  walk → stop → turn route ("root motion stops before turn").
- The door occluder is the open leaf on the room side (24 lp, 44 lp tall),
  plus a 4 lp jamb, both in front of the Keeper (studio `DOOR`). Real door art
  may change these numbers; the hidden-frame test re-checks them.
- The stairway is visible (cutaway), so the stairway-side walk is ordinary
  visible walking, and the ladder foot must be on the lattice.

---

## 11. What was not done

- No visual verdict on the Timing Lab. It is live (HTTP 200), but this session
  had no browser. Its catalogue, model and registers were read instead.
- No foot-plant measurement of the proposed re-timed bridges. That needs
  Codex's rig datums (section 6.3).
- No code, no art, no register or catalogue change.

---

## 12. Conflicts found while reconciling (need an owner)

1. **Rooms that don't fit the 46 lp door rule, with or without a grid**
   (Appendix B): living back wall (TV 28 + bookshelf 20 + piano 25 = 73 lp, in
   a 64 lp space), the bedroom with the en suite partition at x = 74 (two clear
   areas overlap, leaving no space at all), and the weather station (86 lp of
   items). Codex owns layout; Frank owns the rule. (Decision D5.)
2. **Living-room armchair in the foreground over the piano:** a front item
   covering another item's use point. (Rule 6.)
3. **"Tiers retain footprint" versus growing upgrades** (section 2.5,
   decision D9).
4. **Catalogue `usePoint(-8,0)` versus "anchor to the measured centre"**
   (section 2.6). Frank's rule wins; Codex should confirm that no interaction
   needs a non-zero offset.
5. **The studio's whole-stride walk varies speed** (`recipe.ts`). This must go
   when the studio adopts the frame table.

---

## 13. Open decisions

For Frank (product and taste; also on the project page):

- **D1.** Ask Codex for the two walk changes in 6.3 A: re-timed start/stop
  numbers and one new stop off the other foot. *Recommended: yes.* Without
  them, a split-step-free walk can't reach more than two places per room.
- **D2.** Accept the one-step grid (10.5 lp; 2 to 6 places per item per room).
  *Recommended: yes.* The finer half-step grid needs two more awkward stops.
- **D3.** When an upgrade doesn't fit: *recommended:* offer the shuffle
  preview to accept, and if even that fails, say what to move. The
  alternatives are to refuse the sale until there is room, or to sell it and
  store it until there is room.
- **D4.** While dragging, neighbours slide aside live and keep their order.
  *Recommended: yes, with one Undo.* The alternative is to allow items to jump
  past each other.
- **D5.** Rooms that are too full under the door rule (section 12.1).
  *Recommended:* Codex proposes narrower art or a different item split for
  those rooms, and the 46 lp rule stays.
- **D6.** Changing his mind mid-walk: *recommended:* finish the step, stop on
  the nearest spot ahead, then turn back.

For Codex (art and authoring; recorded, not for Frank):

- **D7.** Furniture pixel art is drawn at the nearest whole lp to its centre
  spot (offset ≤ 0.5 lp, inside the contract), or authored as smooth
  density-8 art.
- **D8.** Every visible walk family shares 84 ku steps and 42 ku start and stop
  bridges.
- **D9.** Agree "tiers keep the use centre and contacts; footprint may grow".
- **D10.** Ladder foot at −21 lp (−168 ku); all other transfer points on the
  lattice.
- **D11.** Review the one-step shuffle (stop → F1 → stop) visually.

---

## Appendix A. Measurements

Method: Walk V6 frames
(`art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/`) and the stop →
walk bridge (`art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/`)
were copied into a scratch folder and read with Pillow (alpha ≥ 128). Nothing
in the repository was modified.

**A.1 Root motion as committed** (`keeper-prime-stop-walk-stop-2026-10-14-v1/batch-register.json`,
`rootMotion.route`): 4 stopped holds at x = 0; bridge 15%, 50%, 75%, Walk F1 at
x = 2, 8, 20, 38; Walk F2…F8, F1, F2…F8, F1 at +21 each (x = 59 … 374); stop
75%, 50%, 15%, stop at x = 392, 404, 410, 412; 4 holds. The walk → stop → turn
route (`keeper-prime-walk-stop-turn-front-2026-10-14-v1`) uses the same
deltas, travels 374 ku and stops root motion before the turn. The Timing Lab
model holds `x` per frame.

**A.2 Planted foot** (floor rows y = 314–315, world x = cell x + root x):
front boot at Walk F1 [202, 220]; F2 [205, 233]; F3 [202, 234]; F4 [208, 229];
F5 [210, 234]. The stance boot stays within a few ku while the root advances
84 ku. The bridge frames' sole patches vary by a similar few ku today.

**A.3 Body width and door hiding** (opaque bounds relative to the anchor at
x = 128): stop −51…+51 (centred on the anchor); walk F1 −86…+105, F2 −66…+82,
F3 −43…+69, F4 −82…+104, F5 −80…+105, F6 −65…+65, F7 −51…+71, F8 −62…+101.
For each of the 168 possible walk phases, walking right and walking left, at
least one frame lies fully behind the occluder: **0 of 168 phases fail**, both
for the 24 lp leaf alone (0…192 ku) and for jamb plus leaf (−32…192 ku).
Height about 298 ku (37.3 lp) is within the 44 lp leaf.

## Appendix B. Fit and reachability calculations

Standard room 0…880 ku, door clear area 0…368 ku, items packed in catalogue
order from the door side with zero gap allowed; grid centres at multiples of
84 ku.

| Room (catalogue widths, lp) | Whole pixels: right edge needed | Grid: right edge needed | Space |
|---|---:|---:|---:|
| Kitchen: fridge 12, cooker 18, broom 8, bowl 10 | 94 | 110 | 110 ✓ |
| Kitchen with 30 lp double oven | 106 | 110 | 110 ✓ |
| Kitchen with 40 lp professional oven | 116 | 131 | 110 ✗ |
| Aquarium: tank 38, food 8 | 92 | 109 | 110 ✓ |
| Lair: console 28, bench 28 | 102 | 108.5 | 110 ✓ |
| Living back wall: TV 28, shelf 20, piano 25 | 119 | 138.5 | 110 ✗ |
| Bedroom, inner door at 110 lp as in the studio (bed 30, phone 15, desk 25) | 116 | 128 | 64 ✗ |
| Weather: 18, 24, 22, 22 | 132 | 158 | 110 ✗ |

With the grid shifted by 36 ku (ladder at −27 lp), the kitchen needs 114.5 lp
and fails, which is why the door-wall origin is recommended.

Kitchen reachability on today's data (`76 + 168n` ku): ladder foot −168,
fridge 420, cooker 588, broom 756, bowl 840. None of the 20 ordered pairs is a
whole number of cycles (for example fridge → cooker is 168 ku, and 168 − 76 =
92 is not a multiple of 168). On Option A, each distance is a whole multiple of
84, as tabulated in 6.4.
