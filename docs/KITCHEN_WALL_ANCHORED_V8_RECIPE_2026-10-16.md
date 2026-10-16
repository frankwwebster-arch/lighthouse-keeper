# Kitchen V8 wall-anchored asset and room recipe

Date: 16 October 2026  
Status: review-draft construction authority; not approved or wired  
Machine-readable authority: `data/kitchen_wall_anchored_v8_recipe.json`

> Historical porthole note (17 October): V8's illustrated condition underlays
> are rejected. Current construction authority is V10: a true room-wall alpha
> knockout revealing the one global backdrop. See
> `docs/KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_RECIPE_2026-10-17.md`.

## Visual authority and scope

Kitchen V8 uses Kitchen V6 Option B as its immutable asset baseline and Kitchen
Room V7 as its immutable shell baseline. Frank's approved lower-room composition
in `art/source/kitchen-wall-anchored-2026-10-16-v8/frank-approved-wall-anchored-reference.png`
is the visual placement authority. The generated study is reference only; every
candidate pixel is drawn deterministically by
`scripts/build_kitchen_wall_anchored_v8.py`.

V8 changes only:

1. exposed countertop wings on the kettle, toaster, mixer and sink units;
2. the freestanding fridge finish and top;
3. the pedal-bin scale;
4. review-room transforms that anchor assets to the rear wall;
5. the sink-owned porthole frame and its separate condition underlays.

It does not change Keeper art, runtime sprites, manifests, Final assets,
registries or game wiring.

## Coordinate system

- Source density: exactly 4 raster pixels per logical pixel (`lp`).
- Projection: `flat-cutaway-v1`.
- Camera: straight on.
- Horizontal and vertical convergence: exactly `0 lp`.
- Bay: exactly `21 lp` wide.
- Room: exactly `56 lp` high.
- Room width: exactly `4 + 21 × bayCount lp`, for 6–12 bays.
- No runtime depth scaling is permitted.

## Rear-wall anchoring

The room wall meets the floor at `y = 51 lp` from the room top. Every listed
back-wall asset is positioned by its bottom-centre sprite anchor at
`y = 52 lp`:

```text
wall/skirting ends       y = 51 lp
asset foot line          y = 52 lp
foot bedding into floor      1 lp
clear foreground floor       4 lp  (y = 52..56)
```

This is a semantic room anchor, not an arbitrary upward nudge. It makes the
asset read as attached to the rear wall while retaining the complete walkable
foreground strip. The sprite is neither resized nor cropped. Horizontal
placement remains centred in its declared whole bay or bay span.

The rule applies to the bin, fridge, kettle, toaster, cooker, mixer, sink,
table/chair assembly and pet bowl in the review composition. The right-side
cupboard remains owned by the far-wall cap and does not consume a furniture
bay.

## Smooth countertop construction

The selected Option B construction remains authoritative:

- ordinary slab width: `20 lp` inside a `21-lp` cell;
- safety gutter: `0.5 lp` on each side;
- visible top: `1.5 lp`;
- fascia: `2 lp`;
- front and rear edges: horizontal and equal in length;
- body sides: vertical and parallel;
- shear and convergence: `0 lp`.

For the kettle, toaster, mixer and sink, each exposed wing—from the cell-side
counter edge to the appliance silhouette—is an uninterrupted opaque slab.
There may be no transparent pixel, notch, stepped bite, V-gap or inherited
piece of the older moulding anywhere between the rear edge and fascia bottom.
The central appliance pixels retain their V6 character and sit above the
repaired slab.

## Freestanding fridge

- Cell: `21 × 21 lp`.
- Bay occupancy: one whole bay.
- Countertop: none.
- Top: flat bright-white enamel appliance top.
- Standard-state bound: within its existing cell; the complete state family
  may reach `19 × 21 lp` because of effects and feet.
- Required child-recognition cues: one front door, brass pull, two right-side
  hinges, low ventilation grille and two dark feet.
- White palette: `(250,250,239,255)` body,
  `(255,255,250,255)` highlight and `(213,221,222,255)` shadow.
- No countertop wood colour may occur in the top region.

## Pedal bin

- Cell remains `21 × 16 lp`.
- Standard, full and overflowing states must each remain inside a
  `10 × 12-lp` maximum opaque envelope.
- Nominal side gutter: `5.5 lp` per side.
- Alignment: horizontally centred on its bay and bottom-centred on the common
  `52-lp` foot line.
- State content is redrawn/resampled only inside the new envelope; the cell,
  bay ownership and interaction spot do not change.

## Larger transparent sink porthole

The porthole remains a child of `obj_sink` and occupies no independent bay.

- Child cell: `21 × 56 lp`.
- Centre: `(10.5, 14.5) lp` from the child-cell top-left.
- Outer frame diameter: `19 lp`.
- Clear aperture diameter: `14 lp`.
- Side safety gutter: `1 lp`.
- Weather underlay: `z24`.
- Brass frame and glazing highlight: `z26`.
- Sink: `z40`.

The frame PNG contains only the brass frame, outline, bolts and a faint
semi-transparent glazing highlight. The centre of the aperture is alpha zero.
It contains no painted sea, sky, rain or time-of-day pixels.

Condition imagery is a separate sink-owned underlay. The draft proves four
interchangeable conditions: `day`, `sunset`, `night` and `rain`. A future
runtime renderer may swap or animate that underlay without altering the frame
asset. V8 does not perform that wiring.

When the sink moves:

```text
frameDeltaLp == weatherUnderlayDeltaLp == sinkDeltaLp
```

No member of the attached group is rescaled or reshaped.

## Measured cells, bounds and interaction spots

| Item | Cell | Largest V8 bound | Bays | Interaction |
|---|---:|---:|---:|---:|
| pedal bin | 21 × 16 lp | 10 × 12 lp | 1 | 116 ku |
| freestanding fridge | 21 × 21 lp | 19 × 21 lp | 1 | 284 ku |
| kettle unit | 21 × 31 lp | 20 × 31 lp | 1 | 452 ku |
| toaster unit | 21 × 31 lp | 20 × 31 lp | 1 | 620 ku |
| cooker | 21 × 28 lp | 20 × 28 lp | 1 | 788 ku |
| mixer unit | 21 × 31 lp | 20 × 31 lp | 1 | 956 ku |
| sink unit | 21 × 29 lp | 20 × 29 lp | 1 | 1124 ku |
| table/chair | 42 × 28 lp | 40 × 26 lp | 2 | 1292 ku |
| pet bowl | 16 × 8 lp | 12 × 3 lp | 0 | 1440 ku |
| cleaning cupboard | 38 × 56 lp | 34 × 52 lp | far-cap overlay | 1512 ku |

Interaction values remain inherited review metadata; V8 does not register
them in the live game.

## Acceptance checks

- Every declared counter wing is fully opaque across every surface/fascia row.
- The fridge top contains no V6 wood palette pixels and has a bright neutral
  enamel majority.
- Every bin state is at most `10 × 12 lp`.
- Rows `y = 52..56 lp` in the 9-bay composite remain byte-identical to the room
  shell, proving that assets do not occupy the foreground floor.
- The porthole frame is exactly `19 lp` across, stays within its one-bay cell,
  and has an alpha-zero centre.
- Condition underlays fill the aperture, differ from one another and remain
  separate files from the frame.
- Sink, frame and underlay share identical bay translations in bays 2, 5 and 8.
- V6, V7, Keeper, runtime and Final snapshots remain unchanged.
