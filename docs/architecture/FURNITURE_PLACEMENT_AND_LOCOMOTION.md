# Furniture placement and phase-aware locomotion: Phase 1 plan

Date: 14 October 2026. Author: Claude. **Revision 2.** Status: proposal,
awaiting Frank's decisions (section 13). No runtime code, art, register,
manifest, review page, Workbench lane or approved hash is changed by this
document.

- Branch: `claude/furniture-locomotion`. Revision 1 (`fe7a4fc`) started from
  `abe2372`. Revision 2 merges `main` at `db0bbaf`.
- Task source: `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`, "Requested
  architecture deliverable", points 1–8.
- **What changed in revision 2.** Revision 1 proposed re-timing the approved
  start and stop bridges and adding a stop off Walk F5, so that furniture could
  sit on a one-step (84 ku) grid. Codex replied in
  `docs/CODEX_TO_CLAUDE_DOORWAY_GAIT_ALIGNMENT_2026-10-14.md` that Frank's
  priority is to keep the approved locomotion untouched, and that the door
  gives concealed travel space. Codex is right. Two things make it work:
  - Frank decided on 14 October that ladders and stairways are a separate part
    of the lighthouse, never drawn in a room, so every trip into a room starts
    behind a door.
  - A walk that starts out of sight can start anywhere. Planned backwards from
    the furniture, it lands exactly using the approved numbers.

  Revision 1 assumed a visible stairway walk and so missed this. The approved
  walk is now **frozen**, the 84 ku grid is withdrawn, and the remainder policy
  is the door-centred route (section 6). The quantisation proof stays, because
  it still governs walks between two visible points in one room.
- Frank's binding answers (project page, 14 October):
  - plan first;
  - Ralph and Eddie will move furniture themselves, so the rules must guide a
    child gently;
  - furniture snaps to a grid, and some places are impossible for some items;
  - neighbours may shuffle aside while an item is dragged;
  - items can grow when upgraded;
  - the Keeper anchors to the measured centre of the asset;
  - **split steps are never acceptable**: no stretched stride, no shortened
    final step, no snapping;
  - stairways are separate from rooms.

Written for Frank (section 0), Codex (sections 1–9, 12, 13) and the Claude
session that builds Phase 2.

---

## 0. In plain English

1. **The walk stays exactly as approved.** No new numbers, no new drawings.
2. **Every trip into a room is exact.** He always comes in through a door, and
   while he is behind it nobody can see where he started. So the game works
   backwards from the furniture. It picks a hidden starting point exactly the
   right number of steps away, and he walks out already mid-stride and stops
   precisely at the item. Leaving works the same way in reverse: he walks until
   the door hides him completely.
3. **Furniture is free again.** Placement no longer depends on his step length.
   The snap grid for Ralph and Eddie becomes a choice about how easy dragging
   feels (question 8), and an item can stand at any whole art pixel.
4. **One thing still doesn't work:** walking straight from one thing to
   another in the same room, for example cooker to pet bowl. The arithmetic
   from revision 1 still holds for that case. With the approved walk he
   either steps out through the door and back in (4 to 7 seconds in the
   kitchen) or the walk gets changed after all (question 7). Codex and I
   suggest trying the door version in a prototype first.
5. Upgrades, shuffling, door clear areas and the over-full rooms are as before.

---

## 1. One coordinate contract

### 1.1 The units

| Name | Symbol | Definition | Where it is used today |
|---|---|---|---|
| Keeper unit | **ku** | One pixel of the 256 × 320 high-resolution Keeper registration cell (density 8) | Codex's root-motion data (`2, 6, 12, 18`, `21`, `18, 12, 6, 2`), Prime art, review pages |
| Logical pixel | **lp** | One art pixel of the 32 × 40 Keeper cell and of object art; **1 lp = 8 ku** | Studio (`recipe.ts`), dimension datums, catalogue, sprite manifest `w`/`h` |
| Stage unit | **su** | The game's SVG stage, 1200 × 760 (`world.ts`); **1 lp = 4 su** (`PX = 4` in `Sprite.tsx`), so **1 su = 2 ku** | `config.ts` object `x`, `world.ts`, `Actors.tsx`, `floors.tsx` |
| CSS pixel | **css** | What the browser draws after the SVG viewBox scale and camera zoom | Display only |

### 1.2 The rule

- **Every model quantity is an integer in ku:** positions, root deltas,
  footprints, clearances, route distances, hidden origins. A non-integer in
  the model is a test failure. 21 ku per frame is 2.625 lp or 10.5 su, so only
  ku holds the walk exactly.
- **Room-local x** is measured in ku from the room's **door wall** (the wall
  the door is in, `x = 0`), positive into the room. Each room has its own
  origin. There is no continuous lattice through rooms and stairways (Codex
  agrees; stairways are separate, and inter-room travel crosses a hidden
  boundary).
- **Conversion happens at three explicit boundaries and nowhere else:**
  1. *Import:* art and datums in lp are multiplied by 8 when a record is built.
  2. *Render:* `su = roomLeft + ku / 2`. Halves of a stage unit are allowed for
     the Keeper, because Prime art is smooth density-8 art.
  3. *Legacy migration:* today's `config.ts` su positions become room-local ku
     once (section 2.6).
- **The renderer must not re-snap the Keeper.** `Sprite.tsx` rounds every
  sprite's x to whole logical pixels, which would turn 0, 21, 42, 63 ku into
  0, 24, 40, 64 ku: a foot slide of up to 4 ku every frame. Density-8 actors
  bypass that rounding.

### 1.3 Mismatches the contract resolves

| Today | Value | Contract |
|---|---|---|
| Studio room width | 110 lp = 880 ku | A placeholder; room widths are not fixed yet and may be set to the half lp |
| Game interior (`floors.tsx` `CORE.interiorWidth`) | 420 su = 105 lp | Prototype; follows the room records |
| Game walkable interior (`world.ts` `INTERIOR`) | 70–450 su = 95 lp | Replaced by room records (section 2.3) |
| `FLOOR_STEP` | 140 su = 35 lp | Becomes the agreed 56 lp clear height plus Codex's band |
| Studio "positions are whole pixels so the art stays crisp" | lp rounding | Legacy density-4 sprites only; never the Keeper |

### 1.4 Timing is not distance

Distance comes from the root-motion tables; time comes from the approved
**Fast Timing V1** policy: walk and acceleration 10 fps, deceleration 12 fps,
neutral settle 0 ms unless an action needs a beat, turns 16 fps, endpoint hold
625 ms. Action animations keep their own timing. Revision 1's 8 fps durations
are historical.

---

## 2. Furniture placement records

### 2.1 What is measured, and where it comes from

| Field | Meaning | Source of truth |
|---|---|---|
| `useCentre` | The asset's measured centre along the floor. The Keeper's registered anchor stands exactly here | Frank's rule; Codex measures it per tier from the art |
| `useOffset` | Default 0. A genuine interaction-specific offset, declared and measured | Per type and spot (Codex: "centre use is the default") |
| `footprint` | `[left, right]` ku from `useCentre`: the floor span the item occupies | Per tier (Frank: items may grow) |
| `solid` | Intervals the Keeper may not walk into, as `[left, right, topLp]`; empty for back-wall items he passes in front of | Per tier |
| `lane` | `back` (against the back wall, drawn behind him) or `front` (drawn in front, always solid) | Per type |
| `renderAnchor` | Where the art's own pixels sit relative to `useCentre`, in lp | Per tier, from the art |
| `approach` | Allowed arrival facings and the required action facing | Per type |
| `contacts` | Seat 11, surface 19, handle 20 and so on | `data/keeper_object_dimensions.json`; invariant across tiers |
| `effectOrigin`, `bubbleOrigin` | Particle and thought-bubble origins relative to `useCentre` | Per tier |
| `z` | Draw order within its lane | Per type |
| `zone` | Which room zone it may stand in | Per placement |

The Keeper's measured centre is his registered anchor. In the approved
Side-right stop frame the opaque body spans cell x 77–179, centred exactly on
128 = anchor `[16, 40]` × 8 (Appendix A).

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
  footprint: [Ku, Ku]
  solid: { from: Ku; to: Ku; topLp: number }[]
  contacts: Record<string, number> // lp above the floor; equal for every tier
  effectOrigin?: [number, number]
  bubbleOrigin?: [number, number]
}

interface Placement {               // what the save file stores
  object: string
  room: string
  x: Ku                            // useCentre, room-local, on the room's snap grid
  tier: number
}
```

### 2.3 Room records

Each room is data: walls (`[0, width]` ku), each door (its wall x, leaf side,
its **occlusion mask** and its **clear area**), any inner door, and zones.
Movable furniture is never baked into a room plate.

Codex's distinction is adopted. These four things are separate measurements:

1. the **clear area**: layout space no furniture may occupy (Frank's 46 lp);
2. the **aperture**: the visible opening he emerges through;
3. the **occlusion mask**: the foreground leaf, jamb, wall or portal that
   actually hides him;
4. the **hidden pocket**: model space where the controller may start, end,
   turn or transfer him because the masked alpha is zero.

The pocket continues beyond the visible room, clipped at the door wall, so it
is unbounded on that side.

### 2.4 Rendering furniture

Legacy density-4 furniture is placed on whole logical pixels (8 ku), so its
pixel grid stays aligned with the room plate. Smooth density-8 art may use finer
ku placement where close hand contact needs it. The Keeper always stands
exactly at `useCentre`.

### 2.5 Upgrades that grow (agreed with Codex)

Tiers keep their `useCentre`, every contact datum and their approach
semantics; their **footprint may grow**. An asymmetric tier declares an
asymmetric footprint rather than moving the centre. Before an upgrade is
accepted, the validator previews any neighbour shuffle and refuses an
arrangement that can't fit (section 3.4). This replaces "tiers retain
footprint".

### 2.6 Reconciling today's evidence

| Evidence | Finding | Disposition |
|---|---|---|
| `config.ts` `OBJECTS[].x` | One su x per object, no width | Migrated once to room-local ku |
| Catalogue `usePoint(-8,0)` | Keeper 8 lp left of the object anchor | Not an authority; centre by default, measured `useOffset` where truly needed |
| Catalogue proposed locations | Inside the 46 lp door clear area | Re-placed |
| Studio `Spot.dx` per variant | Free lp offsets | Becomes `useOffset` (measured, default 0) |
| Studio `placeX('@table')` "just clear of the nearer edge" | Stop depends on approach side | Retired for furniture: he stops at the centre |
| Living-room armchair in front of the piano | Front item covering a use point | Rejected by the validator (rule 6) |

---

## 3. A placement grid and validator that guides a child

### 3.1 The grid

The grid is a **layout and usability choice**, not a locomotion requirement.
Positions are stored in ku. Centres snap to the room's snap step, measured
from the door wall. My proposal for the step is **4 lp (32 ku)**. It is whole
art pixels, so pixel art stays crisp. At zoom 1 it is 16 css, a clear
"click" as a child drags. An item gets 7 to 15 places in a 64 lp space,
against 27 to 57 at 1 lp. Frank chooses (D8).

### 3.2 Hard rules (the validator)

A placement is legal when, for its current tier:

1. its centre is on the room's snap grid;
2. its footprint lies inside the room walls;
3. its footprint stays out of every door clear area (46 lp at each door, on
   the side the leaf opens);
4. in its lane, it does not overlap another item's footprint;
5. its use point is reachable from the room's door: no `solid` interval
   (including any `front`-lane item) lies between the door and it, except the
   item itself;
6. no `front`-lane item covers any opaque pixel of the Keeper while he
   approaches, stands at or acts at any reachable use point (the studio's
   per-frame cover check, reused);
7. every use point keeps the whole Keeper inside the room (stop pose ±51 ku,
   walking frames up to −86/+105 ku, Appendix A).

### 3.3 Soft rules (shown, never blocking)

- "Room to grow": the item's next tier would not fit where it stands.

### 3.4 How a child is guided (drag, preview, drop)

While an item is dragged, the nearest grid position is computed each frame and
the ghost snaps there:

- **Green, fits:** drop to place.
- **Amber, fits if others shuffle:** neighbours slide aside live along the
  grid (Frank's mechanic). Dropping commits all the moves; one Undo reverses
  them.
- **Grey, can't go here:** shown with a picture and a short reason, such as
  "The door needs this space to open" or "Too big for this gap". The nearest
  place it would fit is suggested.

The shuffle is deterministic:

- neighbours move outward by the fewest grid steps that clear the overlap,
  cascading if needed;
- order is kept, and walls and door clear areas are fixed;
- the smallest total movement wins, with ties going away from the door;
- nothing changes room or is removed;
- if no solution exists, the result is grey.

The same engine runs when an upgrade is bought.

Worked example, the kitchen (catalogue widths: fridge 12, cooker 18, broom 8,
bowl 10 lp): the items need 48 lp of the 64 lp space. A 30 lp double oven
fits (60 lp). A 40 lp professional oven can't (70 lp). The result is grey, with
"Make room: move the pet bowl or the broom to another room."

---

## 4. A route plan, not just a destination

### 4.1 Route classes (Codex's classification, adopted)

| Class | Visible fixed ends | Approved walk alone? |
|---|---|---|
| 1. Hidden door → visible action point | 1 (the target) | **Yes, exact**: backwards-planned ingress (4.2) |
| 2. Visible action point → hidden door | 1 (the start) | **Yes**: walk until fully hidden, no stop (4.3) |
| 3. Hidden door → visible door-control point → hidden | 1 per leg | **Yes**: plan backwards to the contact, act, walk on |
| 4. Hidden door → hidden door | 0 | **Yes**: transfer only at zero alpha |
| 5. Visible action point → visible action point (same room) | 2 | **Only if the gap is exactly `76 + 168n` ku**; otherwise as 2 then 1 (out and back in), or refused while queued (D7) |

An unsupported route **fails closed** with a diagnostic. It never stretches,
shortens or snaps.

### 4.2 Ingress, planned backwards

With target `T` (the use centre), direction `dir = ±1`, and `n ≥ 0` complete
Walk V6 cycles:

```text
S = T − dir × (76 + 168n)
neutral at S (hidden) → start 2, 6, 12, 18 → n × (8 × 21) → stop 18, 12, 6, 2 → neutral at T
```

The deltas sum to `T − S` exactly, by construction. `n` is chosen for
presentation, never to fix a remainder. It is the smallest `n` for which the
neutral at `S`, all four start-bridge frames and Walk F1 are fully masked, so
his first visible state is already mid-stride. With the placeholder door (leaf
covering room-side 0–192 ku, wall clipping x < 0) that means
`S + 38 + 105 ≤ 192`.

Playback starts at the last fully hidden row. Earlier hidden rows exist in
the compiled table for proof but are not played. This is my technical choice;
Codex may prefer to play them while the door opens.

Measured on the kitchen centres used in Appendix B: every arrival is exact
(`S` = 8 or −76 ku, `n` = 2 to 5). The visible part takes 1.8 to 3.8 s at Fast
Timing V1.

### 4.3 Egress

He starts from the exact neutral at the use centre, plays the start bridge and
whole Walk V6 cycles, and continues until the whole composite (body, clothes,
hat, prop, effects) has zero alpha after masking. Then the room actor ends or
transfers. There is no stop and no remainder. With the placeholder door,
walking left he is hidden once `x + 86 ≤ 192` ku. Measured kitchen egresses
take 1.8 to 3.8 s.

### 4.4 Hidden transfers

Costume swap, gait-phase reset, about-turn, room change and stairway hand-over
happen only between two states that both have zero masked alpha for the whole
composite. Appendix A.3 already shows that every walk phase, in both
directions, has at least one fully hidden standard-uniform frame behind the
24 lp leaf alone. That certificate must be rerun for every costume, prop or
tool composite that crosses a door (a keeper-plus-mower is wider).

### 4.5 The plan structure

```ts
interface RoutePlan {
  routeClass: 1 | 2 | 3 | 4 | 5
  legs: Leg[]
  arrival?: { x: Ku; facing: Facing; turn: ClipRef[]; ingress: ClipRef[] }
  totals: { frames: number; ms: number; distanceKu: Ku }
}

type Leg =
  | { kind: 'ingress'; door: string; S: Ku; T: Ku; dir: 1 | -1; cycles: number; firstVisibleRow: number }
  | { kind: 'egress'; door: string; from: Ku; dir: 1 | -1; hiddenAtRow: number }
  | { kind: 'direct'; from: Ku; to: Ku; cycles: number }                 // class 5, only when exact
  | { kind: 'turn'; from: Pose; to: Pose; clips: ClipRef[] }               // zero root motion
  | { kind: 'hidden'; at: string; swapTo?: string; aboutTurn?: boolean }   // zero-alpha transfer
```

---

## 5. A phase-aware locomotion controller

**One timeline drives frame and position.** A route compiles to a frame table.
Each row holds `{ clip, frame, durationMs, dxKu, xKu, phase, leadFoot,
maskedAlpha, events }`. Runtime shows a row's frame at that row's `xKu`, and
position changes only when the frame changes, as in Codex's registers and the
Timing Lab. Durations come from Fast Timing V1; distances never do.

Guarantees, each a test:

- approved frame hashes, order, root deltas and Fast Timing V1 values are
  unchanged;
- every walking row has its authored non-zero delta, with no constant-speed
  substitute and no final snap;
- the visible arrival row is the exact approved neutral at the exact `T`;
- left is the mirror: negated deltas, mirrored frames (mirror-safe art only).

**Changing orders mid-walk** (Codex's policy, which replaces revision 1's
"three frames"). The approved stop exists only from Walk F1, so:

1. queue the new request;
2. continue the exact walk to the next F1, at most 7 frames (0.7 s), or to the
   planned endpoint;
3. play the approved stop if a visible stop is needed;
4. replan, through the door if the route class needs it.

The engine's "give up waiting" never teleports him.

---

## 6. The remainder policy

### 6.1 Measured step lengths (unchanged by Fast Timing V1)

| Quantity | ku | lp |
|---|---:|---:|
| Steady walk, per frame | 21 | 2.625 |
| One step (Walk F1 → F5) | 84 | 10.5 |
| One cycle (8 frames) | 168 | 21 |
| Start bridge `2, 6, 12, 18` | 38 | 4.75 |
| Stop bridge `18, 12, 6, 2` (from Walk F1 only) | 38 | 4.75 |

The planted front boot holds at world x ≈ 202–234 ku from Walk F1 through F5
while the body advances 84 ku, which confirms 21 ku per frame is foot-locked
(Appendix A.2).

### 6.2 The recommendation: door-centred alignment

The leftover distance goes to the **hidden origin** (4.2) or the **hidden
exit** (4.3). Neither is visible, and the approved walk is untouched. This
meets every one of Frank's rules for route classes 1–4, and it lets furniture
sit anywhere on its own snap grid.

### 6.3 The one case it doesn't cover: class 5

For two fixed visible points, a direct walk is `76 + 168n` ku. No three
places in a row can all be joined pairwise: `d(a,c) = d(a,b) + d(b,c) = 152 +
168k`, which is never `76` plus a multiple of 168. Codex agrees with this
proof. Options for same-room trips (D7):

| Option | What it costs |
|---|---|
| **a. Out through the door and back in** (route classes 2 then 1) | Exact with the approved walk. Measured in the kitchen: 4.4–7.2 s per same-room trip, where a direct walk of a step or two would take about 1–2 s if it were possible. It matches the existing rule for costume changes in the same room |
| b. Direct when the gap happens to be exactly `76 + 168n`, otherwise a | Inconsistent: sometimes he walks across, sometimes he goes out |
| c. Revision 1's walk changes (42 ku bridges plus a stop off F5) | Direct walks always work, but this changes approved motion; Frank and Codex have frozen it for now |
| d. Spread the remainder over the walk | Ruled out by Frank (a stretched stride) |

Codex and I recommend **a**, judged by Frank in the visual prototype. Option c
stays documented as the fallback if the door trip feels too slow.

### 6.4 What it costs in placement freedom

Nothing from locomotion. The only constraints are the snap step (D8), the
door clear areas, the walls and the other footprints.

---

## 7. Deterministic tests (Phase 2)

Codex's required proof, merged with revision 1's list. All are pure, with no
clock, DOM or randomness:

1. Approved frame hashes, order, root deltas and Fast Timing V1 values are
   unchanged (read from Codex's registers, never copied).
2. Ingress is computed backwards from `T`; the sum of emitted deltas equals
   `T − S` exactly in integer ku.
3. Every walking row has its authored non-zero delta, with no final snap.
4. The first visible row is already mid-stride; no start-bridge frame is
   visible.
5. The last visible ingress row is the exact neutral at the exact `useCentre`.
6. A hidden transfer is legal only when the masked alpha of the whole
   composite is zero on the rows before and after it.
7. Left routes negate the same table and mirror only mirror-safe art.
8. The density-8 Keeper bypasses whole-lp rendering (21 ku stays 21 ku).
9. The narrowest (F3) and widest (F1, F4, F5) Walk V6 silhouettes, and every
   costume or prop family that crosses the door, pass the occlusion
   certificate.
10. Class 5 routes compile only when the gap is exactly `76 + 168n`;
    otherwise they follow D7 or fail closed with a diagnostic.
11. Identical inputs give byte-identical placements, shuffles and route
    tables; save then load gives identical placements and routes.
12. Footprints never overlap within a lane, never enter a door clear area and
    never leave the room; every use point is reachable from the door.
13. Changing tier never moves `useCentre` or a contact datum; a footprint
    change re-runs the validator.
14. The shuffle is deterministic, keeps order, never crosses walls or doors,
    never changes room, and reports "no fit" instead of overlapping.
15. An interrupted walk continues to the next F1 (at most 7 frames) and never
    teleports.

---

## 8. Debug overlay and the visual prototype

The diagnostic overlay (`?debug=floor` in the studio and the game; never
production art) shows:

- the snap grid, door clear areas, and the occlusion mask outline with a
  mask-on/off toggle;
- footprints (outline), solids (hatched) and the next tier's footprint
  (dashed), with use points and facing arrows;
- `S`, `T`, the route and the first visible row;
- the live gait: `xKu`, clip, frame, gait phase, emitted delta, occlusion
  state (masked alpha count) and **remaining distance**, which must reach
  exactly zero at the visible stop.

**The Phase 2 gate (Codex's).** This is one real room and one doorway mask
(the studio's placeholder door until Codex's door art exists, then rerun),
with at least three furniture centres that are **not** on any step lattice.
It shows complete ingress and egress, and one same-room trip done as D7
decides, at large inspection scale and exact game scale, with the mask
overlay. Frank then decides whether the door-centred approach is enough for
all intended play.

---

## 9. How this fits the code that exists (Phase 3, later)

| File | Today | Becomes |
|---|---|---|
| `src/studio/recipe.ts` | Room 110 lp, door constants, `DOOR_CLEAR`, `Spot`, `Category`/`Variant`, `checkSolids`, the `hide` doorway step, whole-stride walks that **stretch the speed** | Takes positions and walk tables from the new module. The speed stretch goes (it is the stretched stride Frank ruled out). `checkSolids`, the door clear check and the `hide` step's cover check feed the validator and the occlusion certificate |
| `src/game/config.ts` | One su `x` per object | Default placements in room-local ku, plus per-tier geometry |
| `src/game/world.ts` | `route()` returns x waypoints | Route classes; stairway travel is a separate component behind doors |
| `src/ui/Actors.tsx` | `SPEED = 240` su/s, independent of the frame; snaps to the job | Plays the frame table; no snapping |
| `src/ui/floors.tsx` | Zones only; `LivingFurniture` baked into the floor | Room records; furniture drawn from placements |
| `Sprite.tsx` | Rounds x to whole lp | Exempts density-8 actors |

**Phase 2** (after Frank's answers): an isolated module (for example
`src/placement/`) with the types, validator, shuffle, route compiler,
frame-table builder and the tests in section 7. It also includes the
diagnostic prototype page from section 8. It is not wired into the game or
the studio.

---

## 10. Assumptions

- Root motion is applied per frame, not interpolated within a frame.
- Turns have zero root motion.
- Until door art exists, the occlusion mask is the studio placeholder: a 24 lp
  leaf on the room side and a 4 lp jamb, 44 lp tall, both in front of the
  Keeper, with everything behind the door wall clipped. The certificate is
  rerun when real art lands.
- After an activity he stays at the item until the next order; egress begins
  when the next route starts.

---

## 11. What was not done

- No visual verdict on the Timing Lab (no browser in that session).
- No code, art, register or catalogue change.

---

## 12. Conflicts found while reconciling (need an owner)

1. **Rooms that don't fit the 46 lp door rule.** The catalogue's living-room
   back wall (73 lp in a 64 lp space), the bedroom with the en suite partition
   at x = 74, and the weather station (86 lp) don't fit, independent of any
   grid. Room widths are now flexible, which may help (D5).
2. **Living-room armchair in the foreground over the piano** (rule 6).
3. **"Tiers retain footprint" versus growing upgrades:** resolved with Codex
   (2.5).
4. **Catalogue `usePoint(-8,0)` versus the centre rule:** resolved with Codex
   (2.6).
5. **The studio's whole-stride walk varies its speed** (`recipe.ts`). This
   must go when the studio adopts the frame table.

---

## 13. Decisions

Settled on 14 October, by Frank through Codex's note and recorded on the
project page:

- The approved walk stays frozen: no re-timed bridges, no F5 stop, no 84 ku
  grid. Revision 1's D1, D2, D8, D10 and D11 are withdrawn.
- Stairways are separate; rooms have door-local origins.
- Tiers keep their centre and contacts; footprints may grow (revision 1's D9,
  agreed by Codex).
- Legacy furniture is drawn on whole lp, and density-8 art may be finer
  (revision 1's D7, agreed by Codex).

Open for Frank (on the project page):

- **D3.** When an upgrade doesn't fit. *Recommended:* shuffle preview, else
  say what to move.
- **D4.** Dragging. *Recommended:* neighbours slide aside, keep their order,
  one Undo.
- **D5.** Over-full rooms. *Recommended:* Codex narrows the art or splits the
  items; the 46 lp rule stays. Flexible room widths may help.
- **D6.** Changing orders mid-walk. *Recommended (Codex's policy):* he
  finishes to the next stop point (under a second), stops, then goes.
- **D7.** Same-room trips. *Recommended:* out through the door and back in for
  the prototype; revisit if it feels slow.
- **D8.** Snap step for dragging. *Recommended:* 4 lp.
- **Phase 2 go-ahead:** the pure model, tests and the diagnostic prototype.

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
routes (to the front, and away V2) use the same deltas and travel 374 ku.

**A.2 Planted foot** (floor rows y = 314–315, world x = cell x + root x): the
front boot at Walk F1 is at [202, 220]; F2 [205, 233]; F3 [202, 234]; F4
[208, 229]; F5 [210, 234].

**A.3 Body width and door hiding** (opaque bounds relative to the anchor at
x = 128): stop −51…+51; walk F1 −86…+105, F2 −66…+82, F3 −43…+69, F4
−82…+104, F5 −80…+105, F6 −65…+65, F7 −51…+71, F8 −62…+101. For each of the
168 walk phases, walking right and walking left, at least one frame lies fully
behind the occluder: **0 of 168 phases fail**, for the 24 lp leaf alone and
for jamb plus leaf. Height about 298 ku (37.3 lp) is within the 44 lp leaf.

## Appendix B. Kitchen calculations

Use centres (room-local ku, from revision 1's layout, which is not on any
required lattice now): fridge 420, cooker 588, broom 756, bowl 840. Placeholder
door; Fast Timing V1.

| Use centre | Ingress `n` | `S` | Visible ingress | Egress until hidden |
|---:|---:|---:|---:|---:|
| 420 | 2 | 8 | 1.8 s | 1.8 s |
| 588 | 3 | 8 | 2.6 s | 2.6 s |
| 756 | 4 | 8 | 3.4 s | 3.4 s |
| 840 | 5 | −76 | 3.8 s | 3.8 s |

Same-room trips, out through the door and back in: cooker ↔ fridge 4.4 s,
broom ↔ fridge 5.2 s, bowl ↔ fridge 5.6 s, broom ↔ cooker 6.0 s, bowl ↔ cooker
6.4 s, bowl ↔ broom 7.2 s. None of these gaps is `76 + 168n`, so no direct
walk is possible with the approved walk.

Fit with whole-pixel placement (46 lp clear area, 110 lp placeholder room):
the kitchen needs a right edge at 94 lp (fits), and 106 lp with a 30 lp double
oven (fits). It needs 116 lp with a 40 lp professional oven (doesn't fit). The
aquarium needs 92 (fits) and the lair 102 (fits). The living back wall needs
119, the weather station 132 and the bedroom with an inner door 116 against
64 usable (none fit).
