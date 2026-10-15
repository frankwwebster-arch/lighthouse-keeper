# Kitchen basic assets: drafting scope for Codex

_Claude → Codex, 15 October 2026. Frank asked for the exact scope so Codex can
draft the basic (tier-1) kitchen furniture for the 172 × 56 room. This is the
test case for Phase 3: snapping furniture to the grid, moving it, and
upgrades that grow. Everything here is a draft for Frank's review. Approve,
promote or wire nothing._

Geometry follows `docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md` (agreed).
Contact heights follow `data/keeper_object_dimensions.json`. Names and states
follow `docs/CODEX_BRIEF.md`. The object list comes from Frank's upgrade
ledger (claude.ai/artifact/6Nt7f76QCFAP4FCW9kGXC1), as he edited it on
15 October.

## 1. The width rule: bays of 21 lp

Frank's rule (14 October): an upgrade that grows must be a whole multiple of
the original size, so neighbours shuffle by whole amounts and no step is
ever split. To make that true, every floor-standing item occupies whole
**bays**:

| | lp | ku |
| --- | ---: | ---: |
| One bay (two walking steps) | 21 | 168 |
| Bays in the usable field at 172 / 193 / 214 | 6 / 7 / 8 | |
| Bay *k* (1-based) spans | | `368 + 168(k−1)` to `368 + 168k` |

- Draw each item inside its bays. Art may be narrower than its bays (leave
  up to 2 lp each side); it must never be wider.
- Origin is bottom-centre of the item's bays, as now.
- A one-bay item's interaction spot is its bay centre, which is a lattice
  line. A two-bay item's spot is its centre (the line between its bays) or
  10.5 lp either side of it. Declare which.
- An upgrade that grows goes from one bay to two. The base room is full at
  tier 1, so growth needs the wider lighthouse (see §4).
- Why 21 lp: the keeper is 38 lp tall, so 1 lp is about 4.7 cm and a bay is
  about a metre of wall. A real oven or under-counter fridge is 60 cm
  (about 13 lp), so one bay is already generous.

## 2. Base layout at 172 lp (for the mock-up)

From the stair-side door zone towards the far wall:

| Bay | Item | Lane |
| ---: | --- | --- |
| — | Door zone, 46 lp: no furniture | |
| 1 | Under-counter fridge; toaster on its top | back |
| 2 | Basic oven; stove kettle on the hob | back |
| 3 | Sink unit; pedal bin on the open shelf beneath; mixing bowl on its counter | back |
| 4 | Floor-to-ceiling cleaning cupboard (broom inside) | back |
| 5–6 | Table for one and chair; pet bowl under the table | back |

The table goes last because the seated keeper is side-on in the walking
line, like the armchair, so it blocks anything beyond it. At the far end
it blocks nothing. Put the chair on the room side (its seat stance on line
`1124 ku`, 10.5 lp before the table's centre) and the table against the far
wall. The keeper then never has to stop on the line nearest the wall.

The cupboard does not need the far wall. Its door hides him wherever it
stands.

## 3. What to draw (tier 1 only)

Sizes are the largest the art may be (width × height, lp). Heights are
contact datums that every tier keeps.

| Id (file stem) | What | Bays | Max size | Must hit |
| --- | --- | ---: | --- | --- |
| `room_kitchen` | Room shell: walls, floor and skirting only | | see below | stripes and decks are not part of the room |
| `obj_fridge` | Under-counter fridge | 1 | 21 × 19 | top is a worktop: surface 19, 2 lp thick |
| `obj_cooker` | Basic oven with a hob | 1 | 21 × 19 (+ splashback to 26) | hob 19; rack 10; oven door ≤ 19 wide (see §5) |
| `obj_sink` | Sink unit with a washing-up bowl and tap | 1 | 21 × 27 (tap) | counter 19; open shelf beneath for the bin; counter space beside the bowl |
| `obj_cupboard` | Floor-to-ceiling cleaning cupboard, broom inside | 1 | 21 × 52 | door opens towards the room and hides him (see §5) |
| `obj_table` | Table for one with its chair | 2 | 42 × 26 | table 19, 2 thick, knee clearance ≥ 15, place ≥ 28; chair seat 11, back top 26, clear seat 20 |
| `obj_kettle` | Whistling stove kettle | on the hob | 8 × 8 | stands on y = 19 |
| `obj_toaster` | Simple toaster | on the fridge | 8 × 6 | stands on y = 19 |
| `obj_mixer` | Mixing bowl and wooden spoon | on the sink counter | 7 × 5 | stands on y = 19 |
| `obj_bin` | Pedal bin | under the sink | 8 × 10 | stands on the floor inside bay 3 |
| `obj_petbowl` | Plain pet bowl | under the table | 12 × 3 | rim ≤ 3, clear width ≥ 12, scoop target 6 |

**Room shell.** Build `room_kitchen` from pieces so the room can grow
without stretching: a stair-side cap covering the 46-lp door zone, a
21 × 56 repeat section (one per bay; two or three variants are welcome),
and a far-wall cap. Six sections make 172; seven and eight make 193 and
214. Use the room door from your stair-transition work; don't redraw it.

**States.** Each object gets `standard` (f1), `on` (f4 at 8 fps) and
`broken` (f4 with the shared wobble, smoke and sparks plus one cue of its
own). Object-specific cues from the ledger:

- Oven: hob flame when on; broken = smoke and a sputtering ring.
- Kettle: steam puff and whistle shake when on.
- Toaster: toast pops when on; broken = fires toast across the room
  (Frank's idea; a short arc is enough).
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
| Oven | two-door oven, 1 bay (stacked) | range, 2 bays |
| Sink | double sink with drainer, 1 bay | adds a dishwasher in its own bay beside it |
| Table | table for two, 2 bays (the visitor sits behind the table, facing out) | dining table for four: moves to the dining room |
| Cupboard | fixed size; the broom, hoover and robot-hoover dock all live inside | |

Fully upgraded, the kitchen needs 9 bays and the widest lighthouse has 8.
Frank is choosing what gives way (on his project page). Tier-1 art doesn't
depend on the answer.

## 5. Two things to confirm on the review page, not to work around

1. **Oven door width.** `keeper_object_dimensions.json` lists a 24-lp
   minimum oven door, and the oven-approach proxy is 30 × 30. One bay
   allows a 19-lp door, the same as the keeper's back. Show both oven clips
   against a 19-lp door. If they genuinely don't read, say so: the oven
   becomes 2 bays and something else leaves the base kitchen.
2. **Cupboard door.** The cleaning-cupboard datum asks for a 32-lp
   opening. In one bay the door leaf can be up to 21 lp, and while open it
   may overhang the neighbouring bay in the foreground layer. Show
   whether that hides the keeper with the broom (and the basic hoover, for
   later). If it can't, say so; don't widen the cupboard.

## 6. Out of scope

- Tiers 2 and 3 (sizes reserved above only).
- The entrance: front door, doormat, boot rack and cat flap. Frank is
  deciding where the front door goes; that is the next batch.
- Wall items: fuse box and recipe cards. They need a wall rail, which
  comes with Phase 3.
- The BBQ balcony and the expanded kitchen bay.
- Laundry, toolbox and bootrack. Frank moved laundry to the kitchen, but
  it has no spot yet.
- Any keeper animation change, approval, promotion, manifest or register
  edit, or change to the live game's kitchen. The existing 12 × 24 fridge
  and 18 × 15 cooker stay where they are until Frank promotes the new ones.

## 7. Hand back

- Sources and raw drafts in your usual `art/source/` and `art/raw/`
  review folders, versioned (V1).
- One review page for Frank showing: each item large and at game scale with
  its states; the composed 172-lp kitchen with bay lines, the lattice and
  the keeper standing at each spot; and the same room at 214 lp with the
  reserved tier-3 sizes as dashed outlines.
- A short note back to Claude in `docs/` with each item's measured bounds,
  bays, interaction spots (in ku) and the two answers from §5. Claude will
  turn that into the Phase 3 catalogue.
