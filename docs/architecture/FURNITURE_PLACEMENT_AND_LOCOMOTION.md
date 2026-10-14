# Furniture placement and phase-aware locomotion: Phase 1 plan

Date: 14 October 2026. Author: Claude. **Revision 3.** Status: proposal,
awaiting Frank's decisions (section 13) and Codex's review gates (section 8).
No runtime code, art, register, manifest, review page, Workbench lane or
approved hash is changed by this document.

- Branch: `claude/furniture-locomotion`.
  - Revision 1: `fe7a4fc`, from `abe2372`.
  - Revision 2: `99312f3`.
  - Revision 3: merges `main` at `d77f998`.
- Task source: `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`, "Requested
  architecture deliverable", points 1–8.
- **History.**
  - Revision 1 proposed a one-step (84 ku) lattice for interaction anchors,
    made possible by re-timing the start and stop bridges to 42 ku and adding a
    stop off Walk F5.
  - Revision 2 followed Codex's door-centred note
    (`docs/CODEX_TO_CLAUDE_DOORWAY_GAIT_ALIGNMENT_2026-10-14.md`). That kept the
    approved walk frozen and sent same-room trips out through the door.
  - Frank then made **direct same-room movement a requirement**. Codex's note
    `docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md` supersedes the
    door-centred restriction and recommends the revision 1 lattice. It prefers
    `3, 7, 13, 19`, requires a new Walk F5 → neutral bridge, adds a universal
    action-anchor contract, and sets a gated review sequence.
  - Revision 3 adopts that. It keeps revision 2's hidden-origin ingress and
    zero-alpha egress for doors.
- Frank's binding answers (project page, 14 October):
  - plan first;
  - Ralph and Eddie will move furniture themselves, so the rules must guide a
    child gently;
  - furniture snaps to a grid, and some places are impossible for some items;
  - neighbours may shuffle aside while an item is dragged;
  - items can grow when upgraded;
  - the Keeper anchors to the measured centre of the asset;
  - **split steps are never acceptable**;
  - stairways are separate from rooms;
  - **he walks directly between things in the same room**.

Written for Frank (section 0), Codex (sections 1–9, 12, 13) and the Claude
session that builds Phase 2.

---

## 0. In plain English

1. **He walks straight between things in a room.** To make that possible
   without split steps, the places where he stands to use furniture sit on
   squares one step apart (10.5 art pixels). The furniture itself can be any
   width; only his standing spot snaps.
2. **Two small walk changes make every square reachable from every other
   square**, in whole steps, both ways:
   - starting and stopping each move one high-resolution pixel per frame
     further (half an art pixel in total);
   - a new stop drawing, stopping off the other foot.
3. **Codex shows you each change first**, in order. Nothing is approved
   automatically, and the approved walk stays untouched until you say so:
   - the re-timed start and stop next to today's;
   - then the new stop;
   - then walks of one to four squares;
   - then a real room.
4. **Doors still help.** He comes into a room from a hidden start behind the
   door and leaves until the door hides him. Costume changes still happen
   there.
5. **The cost is room width.** On the grid, each room needs 1.5 to 19.5 art
   pixels more width than free placement. The kitchen, en suite, aquarium and
   lair fit in today's 110 px; the living room, bedroom and weather station
   need wider rooms either way (question 2).

---

## 1. One coordinate contract

### 1.1 The units

| Name | Symbol | Definition | Where it is used today |
|---|---|---|---|
| Keeper unit | **ku** | One pixel of the 256 × 320 high-resolution Keeper registration cell (density 8) | Codex's root-motion data, Prime art, review pages |
| Logical pixel | **lp** | One art pixel of the 32 × 40 Keeper cell and of object art; **1 lp = 8 ku** | Studio (`recipe.ts`), dimension datums, catalogue, sprite manifest |
| Stage unit | **su** | The game's SVG stage, 1200 × 760; **1 lp = 4 su**, so **1 su = 2 ku** | `config.ts`, `world.ts`, `Actors.tsx`, `floors.tsx` |
| CSS pixel | **css** | What the browser draws after viewBox scale and camera zoom | Display only |

### 1.2 The rule

- **Every model quantity is an integer in ku.** A non-integer is a test
  failure. 21 ku per frame is 2.625 lp or 10.5 su; only ku holds it exactly.
- **Room-local x** is measured in ku from the room's door wall. Each room has
  its own lattice origin, chosen against its doorway and furniture
  (section 3.1). No lattice runs through the stairway or between rooms, because
  those transfers are door-hidden.
- **Conversion happens at three explicit boundaries:**
  1. *Import:* lp × 8.
  2. *Render:* `su = roomLeft + ku / 2`; halves of a stage unit are allowed for
     density-8 art.
  3. *Legacy migration:* `config.ts` su → room-local ku, once.
- **The renderer must not re-snap the Keeper.** `Sprite.tsx` rounds x to whole
  lp, which would turn 0, 21, 42, 63 ku into 0, 24, 40, 64 ku: up to 4 ku of
  foot slide per frame. Density-8 actors bypass it.

### 1.3 Mismatches the contract resolves

| Today | Value | Contract |
|---|---|---|
| Studio room width | 110 lp | A placeholder; room widths are flexible to the half lp (section 3.5) |
| Game interior (`CORE.interiorWidth`) | 420 su = 105 lp | Follows the room records |
| Game walkable interior (`INTERIOR`) | 70–450 su | Replaced by room records |
| `FLOOR_STEP` | 140 su = 35 lp | Becomes the agreed 56 lp clear height plus Codex's band |

### 1.4 Timing is not distance

Distance comes from root-motion tables; time comes from **Fast Timing V1**:
walk and acceleration 10 fps, deceleration 12 fps, settle 0 ms, turns 16 fps,
endpoint hold 625 ms. Action animations keep their own timing. Changing root
distance never authorises changing frame bytes, order or fps.

---

## 2. Furniture placement records and the action-anchor contract

### 2.1 Fields

| Field | Meaning | Source of truth |
|---|---|---|
| `keeperUseAnchor` | Where he stands to use it: room-local `xKu` **on the 84 ku lattice**, floor baseline, arrival facing, named entry and exit poses, outfit and held-prop state | Per type and tier (invariant across tiers) |
| `useCentre` | The asset's measured centre. By Frank's rule the default anchor is the lattice point at the item's measured centre, so items are placed by their centre | Codex measures from the art |
| `footprint` | `[left, right]` ku around the anchor; may be asymmetric; may grow with tier | Per tier |
| `solid` | Intervals he may not walk into, `[left, right, topLp]` | Per tier |
| `lane` | `back` (behind him) or `front` (in front, always solid) | Per type |
| `renderAnchor` | Where the art's pixels sit relative to the anchor, in lp | Per tier |
| `contacts` | Seat 11, surface 19, handle 20 and so on, object-relative | `data/keeper_object_dimensions.json`; invariant across tiers |
| `effectOrigin`, `bubbleOrigin`, `z`, `zone` | As named | Per tier or type |

### 2.2 The universal action-anchor contract (Codex's, adopted)

Every action begins and ends at its object's `keeperUseAnchor`:

```text
exact locomotion stop neutral at the anchor
→ optional zero-root turn
→ optional sit / crouch / reach or prop-acquisition bridge
→ action entry / loop / exit
→ reverse prop / posture / facing bridge
→ exact same neutral at the same anchor
```

- An action's internal poses are free. Only its ingress and egress seams return
  to the anchor, with no residual translation.
- **Seated:** the standing anchor is on the lattice. The sit bridge owns the
  move to the seat contact, and the stand bridge returns exactly.
- **Front or back:** use approved zero-root turns.
- **Crouched, prone, environment:** they begin and end at the anchor. A
  different named exit anchor (water edge, ladder landing) is allowed only as a
  reviewed route.
- **Held props:** an action ending with a cake, mug or bags ends on a
  registered `stand-side+prop` or `carry-ready+prop` pose at the same anchor.
  Any visible carry-walk family must obey the same 84 ku step and 42 ku bridges,
  or have its own reviewed route with equivalent endpoints.

### 2.3 Shape (Phase 2 types; written here, not in code)

```ts
type Ku = number // integer

interface TierGeometry {
  tier: number
  sprite: string
  renderAnchor: [number, number]
  footprint: [Ku, Ku]                 // around the anchor
  solid: { from: Ku; to: Ku; topLp: number }[]
  contacts: Record<string, number>    // equal for every tier
  effectOrigin?: [number, number]
  bubbleOrigin?: [number, number]
}

interface KeeperUseAnchor {
  id: string                          // 'use', 'seat' …
  offsetSteps: number                 // 0 by default; whole 84 ku steps from the placement point
  facing: 'left' | 'right'
  entryPose: string
  exitPose: string
  outfit?: string
  prop?: string
}

interface Placement {                  // what the save file stores
  object: string
  room: string
  spot: number                        // lattice index: xKu = room.origin + 84 × spot
  tier: number
}
```

### 2.4 Room records

Each room is data: walls (`[0, width]` ku, width flexible to 4 ku),
`latticeOrigin` (0–83 ku), each door, any inner door, and zones. Codex's four
door measurements are kept separate:

1. the **clear area**: no furniture, Frank's 46 lp;
2. the **aperture**: the visible opening;
3. the **occlusion mask**: what actually hides him;
4. the **hidden pocket**: where he may start, end or transfer at zero masked
   alpha, unbounded beyond the door wall.

A visible door-control standing point is on the room lattice if he can walk to
it directly from furniture.

### 2.5 Upgrades that grow (agreed with Codex)

Tiers keep the same `keeperUseAnchor`, approach semantics and contact datums;
footprints may grow, asymmetrically if declared. A larger tier runs the
validator before purchase and may propose a deterministic shuffle with Undo.

### 2.6 Reconciling today's evidence

| Evidence | Disposition |
|---|---|
| `config.ts` `OBJECTS[].x` (one su x, no width) | Migrated once to spot indices |
| Catalogue `usePoint(-8,0)` | Not an authority; the anchor is the centre unless a measured offset of whole steps is declared |
| Catalogue proposed locations inside the 46 lp clear area | Re-placed |
| Studio `Spot.dx` per variant | Becomes `offsetSteps` |
| Studio `placeX('@table')` "just clear of the nearer edge" | Retired for furniture |
| Living-room armchair in front of the piano | Rejected by validator rule 6 |
| Only the TV has real object art (28 × 23 lp, matching the catalogue) | Catalogue frame widths are the best measured footprints today; refit when art lands |

---

## 3. Placement grid and validator

### 3.1 The grid

- **Lattice pitch: 84 ku = 10.5 lp = one step.** Only Keeper anchors snap;
  furniture widths and art do not become tiles.
- **Origin per room:** `latticeOrigin` (0–83 ku from the door wall) is chosen
  against the room's door and furniture set. Measured, the origin changes
  whether the kitchen fits in 110 lp (Appendix B).
- The child's drag snaps an item's anchor to lattice points. At zoom 1 that is
  42 css, a comfortable finger step.

### 3.2 Hard rules (the validator)

1. The anchor is on the lattice.
2. The footprint lies inside the room walls.
3. The footprint stays out of every door clear area.
4. Within its lane, it doesn't overlap another footprint.
5. The anchor is reachable from the door and from every other anchor: no
   `solid` interval between them, except the item itself.
6. No `front`-lane item covers any opaque Keeper pixel while he walks to,
   stands at or acts at any reachable anchor.
7. Every anchor keeps the whole Keeper inside the room (stop ±51 ku, walking
   −86/+105 ku, Appendix A).

### 3.3 Soft rule

"Room to grow": the next tier wouldn't fit as things stand.

### 3.4 How a child is guided

- **Green, fits:** drop to place.
- **Amber, fits if others shuffle:** neighbours slide aside live along the
  lattice; one Undo.
- **Grey, can't go here:** a picture and a short reason, with the nearest
  fitting spot suggested.

The shuffle moves neighbours outward by the fewest lattice steps and keeps
their order. Walls and door clear areas are fixed. The smallest total move
wins, with ties going away from the door. Nothing changes room. The same engine
runs at upgrade time.

### 3.5 What the grid costs in room width (Codex's requested check)

Catalogue frame widths, the 46 lp clear area at each door, the best lattice
origin and the best item order (Appendix B):

| Room | Min width, free placement | Min width, on the grid | Grid cost | Fits 110 lp on the grid? |
|---|---:|---:|---:|---|
| Kitchen | 94 | 102 | 8 | yes |
| Kitchen with 30 lp double oven | 106 | 107.5 | 1.5 | yes |
| Kitchen with 40 lp professional oven | 116 | 123.5 | 7.5 | no (not even free) |
| Living, including the armchair | 143 | 162.5 | 19.5 | no (not even free) |
| Bedroom, with its inner door to the en suite | 162 | 167 | 5 | no (not even free) |
| En suite | 74 | 81 | 7 | yes |
| Aquarium | 92 | 100.5 | 8.5 | yes |
| Weather station | 132 | 141.5 | 9.5 | no (not even free) |
| Lair | 102 | 105.5 | 3.5 | yes |

These are minimum widths with items touching. Real layouts want breathing room,
and children want choice; each extra 10.5 lp of room width gives every item one
more possible place.

---

## 4. Route classes

| Class | Construction |
|---|---|
| 1. Hidden door → anchor | Planned **backwards** from the anchor `T` to a hidden origin `S = T − dir × 84k` (with the 42 ku bridges), choosing `k` so that the start bridge and Walk F1 are fully masked. The first visible state is mid-stride |
| 2. Anchor → hidden door | Start bridge, then whole walk until the whole composite has zero masked alpha; transfer there. No stop |
| 3. Hidden door → door-control point → hidden | As 1 to the control anchor, act, then as 2 |
| 4. Hidden door → hidden door | Transfer only at zero alpha |
| 5. **Anchor → anchor, same room** | **Direct:** `42 + 84(k − 1) + 42 = 84k` ku for anchors `k` lattice steps apart. Stop from F1 when `k` is odd, from F5 when `k` is even |

Until the F5 bridge is approved, class 5 works only for odd `k`. The compiler
reports even-`k` routes as unsupported and never improvises.

Hidden transfers (costume, phase reset, about-turn, room change) happen only
between two states with zero masked alpha for the whole composite. With the
placeholder 24 lp leaf, every walk phase in both directions has at least one
fully hidden standard-uniform frame (Appendix A.3). Rerun it for every costume,
prop or tool composite.

```ts
type Leg =
  | { kind: 'ingress'; door: string; S: Ku; T: Ku; dir: 1 | -1; steps: number; firstVisibleRow: number }
  | { kind: 'egress'; door: string; from: Ku; dir: 1 | -1; hiddenAtRow: number }
  | { kind: 'direct'; from: Ku; to: Ku; steps: number; stop: 'F1' | 'F5' }
  | { kind: 'turn'; from: Pose; to: Pose; clips: ClipRef[] }               // zero root motion
  | { kind: 'hidden'; at: string; swapTo?: string; aboutTurn?: boolean }
```

---

## 5. A phase-aware locomotion controller

One frame table drives frame and position. Each row is `{ clip, frame,
durationMs, dxKu, xKu, phase, leadFoot, maskedAlpha, events }`. Position
changes only when the frame changes. Every walking row carries its authored
non-zero delta, the arrival row is the exact neutral at the exact anchor, and
left is the mirror (negated deltas, mirror-safe art only).

**Root-motion tables are data, read from Codex's registers.** The approved
table (`2, 6, 12, 18` / `18, 12, 6, 2`, stop from F1) and any candidate table
(`3, 7, 13, 19` / `19, 13, 7, 3`, stops from F1 and F5) are both kept and
labelled. The compiler uses whichever Frank has approved.

**Changing orders mid-walk.** He continues to the next legal stop phase: the
next F1 or F5 once both stops exist (at most 3 frames, 0.3 s), or the next F1
before then (at most 7 frames). He stops there and replans. With the 42 ku
bridges, every F1/F5 stop from an anchor lands on another lattice point, so the
replanned route is always whole steps. He never teleports.

---

## 6. The remainder policy

### 6.1 Measured step lengths

| Quantity | ku | lp |
|---|---:|---:|
| Steady walk, per frame | 21 | 2.625 |
| One step (Walk F1 → F5) | 84 | 10.5 |
| One cycle | 168 | 21 |
| Approved start / stop bridge | 38 / 38 | 4.75 / 4.75 |
| Candidate start / stop bridge | 42 / 42 | 5.25 / 5.25 |

The planted front boot holds at world x ≈ 202–234 ku from Walk F1 to F5 while
the body advances 84 ku (Appendix A.2).

### 6.2 Why the approved numbers can't serve direct same-room walks

A direct walk with approved numbers is `76 + 168n` (or `76 + 84n` with an F5
stop). For three anchors in a row, `d(a,c) = d(a,b) + d(b,c) = 152 + 84m`,
which leaves remainder 68 on division by 84, not 76. No placement fixes this;
Codex agrees. Eight ku of route distance must be accounted for somewhere.

### 6.3 The recommendation: quantisation on an 84 ku anchor lattice

Codex and I recommend, together:

1. the candidate bridges `3, 7, 13, 19` / `19, 13, 7, 3`;
2. one new Walk F5 → neutral bridge;
3. the 84 ku anchor lattice.

The candidate keeps the approved acceleration shape (increments `+4, +6, +6`)
and adds exactly 1 ku to each moving row. The largest cumulative change is
4 ku (half an art pixel) at the bridge's end. The F5 bridge is drawn from the
KP rig between the exact Walk V6 F5 and the exact neutral. It must not be a
leg-swapped copy of the F1 bridge.

Rejected, by Codex and me:

- a different remainder per route (a stretched stride);
- direction-dependent action ports 8 ku apart;
- a universal visible 8 ku shuffle;
- walking past and turning back;
- detouring through the door.

The door detour also measured 4.4–7.2 s per same-room trip in revision 2.

### 6.4 If Frank rejects the re-timed bridges

The approved walk then supports direct walks only between anchors exactly
`76 + 168n` ku apart. Every room could have at most two mutually reachable
anchors, which fails the requirement. The next options are additional stop
phases with shorter bridges (more art) or a coarser product decision. That is
for Frank and Codex, never a silent stretch.

---

## 7. Deterministic tests

Codex's 16 requirements, merged with the earlier list:

1. Every reused PNG hash is the exact approved authority.
2. Approved and candidate root-motion tables are both retained and labelled.
3. Candidate bridge totals are exactly 42 ku in both directions; steady frames
   stay 21 ku.
4. F1 and F5 stops end on the same exact neutral and anchor.
5. For every tested `k`, emitted distance equals `84k`. Odd `k` selects F1 and
   even `k` selects F5.
6. Left routes negate the same deltas, using mirror-safe art only.
7. No locomotion row has zero movement, and no endpoint is snapped.
8. Turns have zero root motion and keep the anchor.
9. Every action recipe returns to its declared anchor, or declares a reviewed
   held-prop or environment endpoint.
10. Door ingress is planned backwards with an exact sum; the first visible row
    is mid-stride; hidden transfers occur only at zero masked alpha (narrowest
    and widest Walk V6 frames, and every costume or prop composite).
11. The density-8 Keeper bypasses whole-lp rendering.
12. The validator rejects overlaps, door-clearance violations, unreachable
    anchors and unsafe foreground occlusion.
13. Tier changes never move an anchor or contact datum; footprint changes
    re-run validation.
14. The shuffle is deterministic, keeps order, never crosses walls or doors and
    never changes room.
15. Identical inputs give byte-identical placements and routes; save and load
    round-trip exactly.
16. Interrupted walks stop at the next legal phase and land on the lattice.
17. Approved source, Final, runtime and production hashes are unchanged until
    Frank promotes.

---

## 8. Review gates and the debug overlay

**Gates (Codex's sequence; Frank reviews each separately):**

1. **Root motion only.** A new versioned candidate with the exact approved F1
   bridge pixels twice: current `2, 6, 12, 18` beside `3, 7, 13, 19`. Large and
   game scale, frame stepping, foot-contact overlays, cumulative positions.
   *Codex.*
2. **Frank reviews the movement.** If it skates, the candidate is rejected and
   the approved schedule kept.
3. **The F5 → neutral bridge**, in its own versioned draft, reviewed alone and
   in a two-step route. *Codex.*
4. **Lattice proof:** exact 1-, 2-, 3- and 4-step journeys, both directions,
   alternating F1/F5 stops.
5. **Real-room proof:** direct routes among at least four real anchors,
   including a seated action and a front- or back-facing action.
6. Pure placement and route model in the game code (Phase 2), then runtime
   integration later.

My route compiler and validator are pure and touch no art. They can produce the
exact frame and root tables that gates 4 and 5 display. Whether Phase 2 starts
in parallel with gates 1–3 or after gate 5 is Frank's call (D9).

**Debug overlay** (`?debug=floor`, diagnostic only): lattice ticks with indices
and origin; door clear areas and the occlusion mask with an on/off toggle;
footprints, solids and next-tier outlines; anchors with facing; the route with
step notches and F1/F5 stop marks; and the live gait readout: `xKu`, frame,
phase, emitted delta, active root table, masked alpha and **remaining distance,
which must be exactly 0 at every stop**.

---

## 9. How this fits the code that exists (Phase 3, later)

| File | Today | Becomes |
|---|---|---|
| `src/studio/recipe.ts` | Room 110 lp, door constants, `DOOR_CLEAR`, `Spot`, `Category`/`Variant`, `checkSolids`, `hide`, whole-stride walks that **stretch the speed** | Takes anchors, rooms and walk tables from the new module. The speed stretch goes. `checkSolids`, the door clear check and the `hide` cover check feed the validator |
| `src/game/config.ts` | One su `x` per object | Default placements as spot indices, plus tier geometry |
| `src/game/world.ts` | x waypoints | Route classes; stairway separate behind doors |
| `src/ui/Actors.tsx` | `SPEED = 240`, frame-independent; snaps to the job | Plays the frame table; no snapping |
| `src/ui/floors.tsx` | Zones; `LivingFurniture` baked in | Room records; furniture from placements |
| `Sprite.tsx` | Rounds x to whole lp | Exempts density-8 actors |

---

## 10. Assumptions

- Root motion applies per frame, not interpolated.
- Turns have zero root motion.
- Until door art exists, the occlusion mask is the studio placeholder: a 24 lp
  leaf and a 4 lp jamb, 44 lp tall, with everything behind the door wall
  clipped.
- Catalogue frame widths stand in for footprints until object art exists.
- After an activity he stays at the anchor until the next order.

## 11. What was not done

- No visual verdict on the Timing Lab or any review page from this session.
- No code, art, register or catalogue change.

## 12. Conflicts found while reconciling

1. **Over-full rooms:** living, bedroom with en suite, weather station, and the
   kitchen with a professional oven don't fit 110 lp even with free placement.
   Room widths are now flexible (D5).
2. **Living-room armchair in front of the piano** (rule 6).
3. **"Tiers retain footprint":** resolved (2.5).
4. **Catalogue `usePoint(-8,0)`:** resolved (2.6).
5. **The studio's speed-stretching walk** must go when the studio adopts the
   frame table.

## 13. Decisions

Settled on 14 October:

- **By Frank:** direct same-room movement is required; stairways are separate;
  the approved walk changes only through Codex's gated reviews.
- **With Codex:** tiers keep anchors and contacts while footprints may grow;
  legacy furniture renders on whole lp, and density-8 art may sit on the
  half-lp lattice.

Open for Frank (project page):

- **D3.** When an upgrade doesn't fit. *Recommended:* shuffle preview, else say
  what to move.
- **D4.** Dragging. *Recommended:* neighbours slide aside, keep their order,
  one Undo.
- **D5.** Room widths. *Recommended:* size each room to fit its furniture on
  the grid, plus breathing room, with Codex judging the look (Appendix B gives
  the minimums).
- **D6.** Changing orders mid-walk. *Recommended:* carry on to the next legal
  stop, stop, then go.
- **D9.** Phase 2 timing. *Recommended:* build the pure model now in parallel
  with Codex's gates 1–3, with both root tables, so it can supply exact route
  tables for gates 4–5; nothing is wired in.

Open for Codex: gates 1, 3, 4 and 5; real furniture footprints as art lands;
the door's occlusion mask.

---

## Appendix A. Measurements

Method: Walk V6 frames and the stop → walk bridge frames were copied into a
scratch folder and read with Pillow (alpha ≥ 128). Nothing in the repository
was modified.

**A.1 Root motion as committed**
(`keeper-prime-stop-walk-stop-2026-10-14-v1/batch-register.json`): 4 holds at
0; bridge to Walk F1 at x = 2, 8, 20, 38; Walk at +21 each to 374; stop at
392, 404, 410, 412; 4 holds. The walk → stop → turn routes (to the front, and
away V2) use the same deltas.

**A.2 Planted foot** (rows y = 314–315, world x): the front boot at Walk F1 is
at [202, 220]; F2 [205, 233]; F3 [202, 234]; F4 [208, 229]; F5 [210, 234].

**A.3 Body width and door hiding** (relative to anchor x = 128): stop −51…+51;
walk F1 −86…+105, F2 −66…+82, F3 −43…+69, F4 −82…+104, F5 −80…+105, F6
−65…+65, F7 −51…+71, F8 −62…+101. Of 168 walk phases in each direction,
**0 lack a fully hidden frame** behind the 24 lp leaf alone. Height about
298 ku fits the 44 lp leaf.

## Appendix B. Fit and timing calculations

**Room fit** (section 3.5): catalogue widths; a 46 lp clear area at each door
(two for the bedroom with its inner door); items touching. The best of 84
lattice origins and every item order was searched; room widths are rounded up
to 4 ku. Best grid layouts (anchor centres, lp from the door wall):

- kitchen: cooker 55, fridge 76, broom 86.5, bowl 97 (width 102);
- double-oven kitchen: broom 50, fridge 60.5, cooker 81.5, bowl 102.5 (width
  107.5);
- en suite: basin 53.5, toilet 74.5 (width 81);
- aquarium: tank 65, food 96.5 (width 100.5);
- lair: console 60, bench 91.5 (width 105.5).

With the origin fixed at the door wall instead of chosen, the kitchen needs
110 lp exactly; with the studio ladder's old offset (36 ku), it needs 114.5 lp.

**Same-room trip through the door** (revision 2, for the record, Fast Timing
V1): 4.4–7.2 s in the kitchen, against about 1–2 s for a direct walk of a
step or two.
