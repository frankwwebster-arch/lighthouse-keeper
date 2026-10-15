# Kitchen basic assets: drafting scope for Codex

_Claude → Codex, 15 October 2026; revised twice on 16 October after Frank's answers.
Frank asked for the exact scope so Codex can draft the basic (tier-1)
kitchen furniture. This is the test case for Phase 3: snapping furniture to
the grid, moving it, and upgrades that grow. Everything here is a draft for
Frank's review. Approve, promote or wire nothing._

**16 October changes:** the kettle, toaster and mixer each come on their own
one-bay counter unit that upgrades with the appliance. **Nothing overlaps**
(Frank): the bin has its own bay, left of the fridge, and nothing tucks
under another piece. The starting kitchen is 9 bays, mixer included (it is
his cooking counter), and the lighthouse stretches one bay at a time to
12. The cleaning cupboard is always the last thing in the room, set into
the far wall at 90° to the view, and takes no bay. §2 is final apart from
the door clear area, which is your call (§5.3).

Geometry follows `docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md` (agreed),
extended as below. Contact heights follow `data/keeper_object_dimensions.json`.
Names and states follow `docs/CODEX_BRIEF.md`. The object list comes from
Frank's upgrade ledger (claude.ai/artifact/6Nt7f76QCFAP4FCW9kGXC1).

## 1. The width rule: bays of 21 lp

Frank's rule (14 October): an upgrade that grows must be a whole multiple of
the original size, so neighbours shuffle by whole amounts and no step is
ever split. To make that true, every floor-standing item occupies whole
**bays**:

| | lp | ku |
| --- | ---: | ---: |
| One bay (two walking steps) | 21 | 168 |
| Door clear area *Z* | 4, 25 or 46 (§5.3) | 32, 200 or 368 |
| Room width with *n* bays | *Z* + 21*n* | *Z*ku + 168*n* |
| Bay *k* (1-based) spans | | `Zku + 168(k−1)` to `Zku + 168k` |

Every stretch of the lighthouse adds exactly one bay (21 lp), as the agreed
handoff already does. The widest room is **12 bays**: 256, 277 or 298 lp
depending on *Z*. All existing anchors stay on the lattice.

- Draw each item inside its bays. Art may be narrower than its bays (leave
  up to 2 lp each side); it must never be wider.
- Origin is bottom-centre of the item's bays, as now.
- A one-bay item's interaction spot is its bay centre, which is a lattice
  line. A two-bay item's spot is its centre (the line between its bays) or
  10.5 lp either side of it. Declare which.
- An upgrade that grows goes from one bay to two.
- Why 21 lp: the keeper is 38 lp tall, so 1 lp is about 4.7 cm and a bay is
  about a metre of wall. A real oven or under-counter fridge is 60 cm
  (about 13 lp), so one bay is already generous.

## 2. Base layout (9 bays)

The room's width depends on the door (§5.3, your call): with Frank's
preferred outward door and a 4-lp frame, the starting room is 193 lp and
the widest 256 lp; with an inward door it is 214 lp (25-lp zone) or
235 lp (46-lp zone). From the stair-side door to the far wall:

| Bay | Item | Lane |
| ---: | --- | --- |
| — | Door clear area (width per §5.3): no furniture | |
| 1 | Pedal bin | back |
| 2 | Under-counter fridge | back |
| 3 | Kettle unit (stove kettle on its own gas ring) | back |
| 4 | Toaster unit | back |
| 5 | Basic oven | back |
| 6 | Mixer unit (bowl and wooden spoon): his cooking counter | back |
| 7 | Sink unit (cupboard beneath) | back |
| 8–9 | Table for one and chair | back |
| far wall | Cleaning cupboard, door in the end wall (broom inside) | far-wall cap |

The pet bowl no longer goes under the table; Frank is choosing its home
(recommended: the hall at the foot of the stairs, by the cat flap). Draw it
on its own.

**Fixed and movable.** Only the door zone and the cupboard are fixed. Ralph
and Eddie can move every other piece to any bay, so draw nothing that
depends on its neighbour (no shared worktop running across two items, no
splashback that only lines up in this order). The dumb waiter is movable
too (Frank, 16 October).

**The cupboard is always last** (Frank, 16 October). Its door is in the end
wall, at 90° to the view, so it belongs to the far-wall cap and moves with
the wall when the lighthouse stretches. The keeper walks to the last
standing line, opens the door towards the room, appears to walk in behind
it, and comes back out already in the action clip (for example sweeping
or hoovering). When the action ends he walks back in, and comes out in the
standard walk as the door closes behind him. This needs a walk-to-handle
reach; the door leaf hides every costume or prop swap.

**The table must not block the walking line**, because the keeper has to
pass it to reach the cupboard. Arrange the chair so he steps out of the
walking line to sit, as he does for the oven, rather than side-on in it
like the armchair. If `eat_seated` cannot work that way, say so on the
review page.

## 3. What to draw (tier 1 only)

Sizes are the largest the art may be (width × height, lp). Heights are
contact datums that every tier keeps.

| Id (file stem) | What | Bays | Max size | Must hit |
| --- | --- | ---: | --- | --- |
| `room_kitchen` | Room shell: walls, floor and skirting only | | see below | stripes and decks are not part of the room |
| `obj_fridge` | Under-counter fridge | 1 | 21 × 19 | top is a worktop: surface 19, 2 lp thick |
| `obj_kettle` | Counter unit with a single gas ring and a whistling stove kettle | 1 | 21 × 30 | counter 19 |
| `obj_toaster` | Counter unit with a simple toaster | 1 | 21 × 30 | counter 19 |
| `obj_cooker` | Basic oven with a hob | 1 | 21 × 19 (+ splashback to 26) | hob 19; rack 10; oven door ≤ 19 wide (see §5) |
| `obj_mixer` | Counter unit with a mixing bowl and wooden spoon | 1 | 21 × 30 | counter 19 |
| `obj_sink` | Sink unit with a washing-up bowl and tap | 1 | 21 × 27 (tap) | counter 19; cupboard beneath |
| `obj_cupboard` | Cleaning cupboard in the far wall, broom inside | 0 (far-wall cap) | door ≥ 24 × 40 opening | door opens towards the room and hides him (see §5) |
| `obj_table` | Table for one with its chair | 2 | 42 × 26 | table 19, 2 thick, knee clearance ≥ 15, place ≥ 28; chair seat 11, back top 26, clear seat 20 |
| `obj_bin` | Pedal bin | 1 | 21 × 14 | stands on the floor, centred in its bay; later tiers (recycling station, Waste-Manager 3000) fill the bay |
| `obj_petbowl` | Plain pet bowl | on its own (home pending) | 12 × 3 | rim ≤ 3, clear width ≥ 12, scoop target 6 |

The three counter units share one cabinet design and one counter height, so
they read as a run of matching kitchen units. Each unit is drawn together
with its appliance. Frank wants the unit to upgrade alongside the device,
so the cabinet may change style by tier but never width.

**Room shell.** Build `room_kitchen` from pieces so the room can grow
without stretching: a stair-side cap covering the 46-lp door zone, a
21 × 56 repeat section (one per bay; two or three variants are welcome),
and a far-wall cap, which carries the cupboard door. Any whole number of
sections from 9 to 12 must join cleanly. Use the room door from your stair-transition work; don't redraw
it. The front door is not in the kitchen: Frank has put it at the foot of
the stairs (next batch).

**States.** Each object gets `standard` (f1), `on` (f4 at 8 fps) and
`broken` (f4 with the shared wobble, smoke and sparks plus one cue of its
own). Object-specific cues from the ledger:

- Oven: hob flame when on; broken = smoke and a sputtering ring.
- Kettle: steam puff and whistle shake when on.
- Toaster: toast pops when on; broken = fires toast across the room
  (Frank's idea; a short arc is enough).
- Mixer: spoon stirring when on.
- Sink: tap running when on; broken = drip. Add a dirty-dishes overlay at
  three heights (`obj_sink_dishes1..3_f1`), because dishes pile up after
  meals.
- Bin: `standard`, `full`, `overflowing` instead of on/broken.
- Pet bowl: `standard` (empty) and `full`; broken = crack and puddle.
- Cupboard: `standard` (closed), `on` = door opening (f4), plus an open
  still. No broken state: it's architecture.
- Fridge: door opening when on; broken = door ajar and frost puff.
- Table and chair: standard only. Passive furniture doesn't break.

**Existing keeper clips these must fit** (read only; change none):
`meal_from_oven_back`, `cake_from_oven_back`, `hot_drink_pour`, `_stir`,
`_pickup`, `_put_down`, `_drink`, `eat_seated`, `meal_place_side`,
`lean_table_back`, `feed_animals`, `sweep_broom`, `switch_press`.

## 4. Upgrade sizes to reserve (plan only; don't draw)

| Item | Tier 2 | Tier 3 |
| --- | --- | --- |
| Fridge | tall fridge-freezer, 1 bay, ≤ 21 × 46 | American fridge, 2 bays, ≤ 42 × 46 |
| Kettle unit | electric kettle, 1 bay | drinks machine, 1 bay |
| Toaster unit | chrome four-slice, 1 bay | toast-o-matic, 1 bay |
| Oven | two-door oven, 1 bay (stacked) | range, 2 bays |
| Mixer unit | stand mixer, 1 bay | Robo-Cook, 1 bay |
| Sink | double sink with drainer, 1 bay | adds a dishwasher in its own bay beside it |
| Cupboard | fixed, in the far wall; the broom, hoover and robot-hoover dock all live inside | |
| Table | table for two, 2 bays (the visitor sits behind the table, facing out) | moves to the dining room |

When the dining room exists (Frank's answer, 16 October), the table moves
up there and its two bays become a **snack counter with a bar stool** (1
bay) and a **dumb waiter** that sends meals up (1 bay). Frank's design for
the dumb waiter (a later batch): it looks like another kitchen unit, glass
fronted, running all the way up to the ceiling; its working animation shows
the food rising in the little lift and vanishing into a closed top
section. It appears only once the dining room is built, and can stand in
any bay. Fully upgraded,
the kitchen needs exactly 12 bays (bin 1, fridge 2, kettle 1, toaster 1,
range 2, mixer 1, sink and dishwasher 2, snack counter 1, dumb waiter 1),
the widest room. The cupboard takes none.

## 5. Three things to confirm on the review page, not to work around

1. **Oven door width.** `keeper_object_dimensions.json` lists a 24-lp
   minimum oven door, and the oven-approach proxy is 30 × 30. One bay
   allows a 19-lp door, the same as the keeper's back. Show both oven clips
   against a 19-lp door. If they genuinely don't read, say so rather than
   widening the oven.
2. **Cupboard door.** The cleaning-cupboard datum asks for a 32-lp
   opening, and the door is now in the end wall, seen at 90°. Show the
   keeper walking in behind the opening door and coming out with the broom
   (and the basic hoover, for later), at the narrowest and widest rooms. If the leaf
   cannot hide him, say so.

3. **Room door direction: your decision.** Frank prefers the room door
   to open **outward, into the stairwell**, and thinks it may help the
   stair transition. He has left the final call to you. Outward, the room
   keeps only a 4-lp frame clear (lattice origin 32 ku instead of
   368 ku), freeing two bays in every room, and the costume change happens
   behind the leaf on the stair side. Check that an outward leaf fits
   beside the stairs and ladder in the 105-lp core and works with your
   door-exit and stair-entry transitions. If outward doesn't work, the
   fallback is an inward door with a 25-lp clear area (the leaf plus 1 lp),
   provided every costume change and wide composite (keeper plus mower,
   raised tools, party hat) stays hidden; failing both, keep 46 lp. Change
   no approved transition to decide this: propose, and record your choice
   and its clear-area width in your note to Claude. None of the furniture
   drawings depend on it; only the room layouts shift.

## 6. Out of scope

- Tiers 2 and 3, the snack counter and the dumb waiter (sizes reserved
  above only).
- The entrance: front door, doormat, boot pegs and cat flap, at the foot
  of the stairs. That is the next batch.
- Wall items: fuse box and recipe cards. They need a wall rail, which
  comes with Phase 3.
- The BBQ balcony and the expanded kitchen bay.
- Laundry and toolbox. Frank moved laundry to the kitchen, but it has no
  spot yet.
- Any keeper animation change, approval, promotion, manifest or register
  edit, or change to the live game's kitchen. The existing 12 × 24 fridge
  and 18 × 15 cooker stay where they are until Frank promotes the new ones.

## 7. Hand back

- Sources and raw drafts in your usual `art/source/` and `art/raw/`
  review folders, versioned (V1).
- One review page for Frank showing: each item large and at game scale with
  its states; the composed 9-bay starting kitchen with bay lines, the
  lattice and the keeper standing at each spot; and the 12-bay kitchen with the reserved
  tier-3 sizes as dashed outlines.
- A short note back to Claude in `docs/` with each item's measured bounds,
  bays, interaction spots (in ku) and the two answers from §5. Claude will
  turn that into the Phase 3 catalogue.
