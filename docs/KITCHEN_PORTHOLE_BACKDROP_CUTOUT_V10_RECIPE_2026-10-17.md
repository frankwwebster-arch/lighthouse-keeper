# Kitchen V10 approved-reference family and true-backdrop porthole recipe

Date: 17 October 2026  
Status: review draft; not approved, promoted or wired  
Machine authority: `data/kitchen_porthole_backdrop_cutout_v10_recipe.json`

## Visual authority and V9 rejection

The attached 17 October family sheet that Frank called excellent is V10's sole
visual authority. V9 is immutable rejected provenance only: its fridge was too
flat, its shelf was low-quality and ill-fitting, and its wing-only worktop
repair retained older centre pixels that read as chipped or broken surfaces.

V10 restores the detailed bright-white counterless fridge, rebuilds the shelf
at matching polish, and replaces the complete slab across every state of the
kettle, toaster, mixer and sink units. The slab is a single 20-lp-wide Option-B
construction; the verifier requires an opaque uninterrupted row from raster
x=2 through x=81 in every frame. The units remain inside their exact 21-lp
bays, with the established safety gutters and 52-lp rear-wall foot line.

## Corrected principle

The kitchen does not own a sea, sky, horizon, weather or time-of-day picture.
The porthole is a real opening through the cutaway room wall. The global
lighthouse backdrop—today the scene background and later the layered backdrop
specified in `docs/AMBIENCE_AND_BACKDROP.md`—is drawn beneath the room and is
therefore what the player sees through the opening.

V8's four illustrated condition underlays (`day`, `sunset`, `night`, `rain`)
are rejected for this purpose. V10 neither copies nor replaces them with
another illustration. Its review page uses a CSS checkerboard solely to prove
transparency; that checker is not written into an asset.

## Why the wall must also be cut out

An alpha-clear frame placed over an opaque cream wall still shows the cream
wall. Two sink-owned operations are therefore required:

1. apply a circular alpha knockout to the room-wall layer at the sink-owned
   porthole position; and
2. draw the separate brass ring above that opening.

The immutable V7 shell remains the source. V10 creates derived review shells;
it does not overwrite V7.

## Exact geometry

- Projection: `flat-cutaway-v1`, straight on, with zero convergence.
- Density: 4 raster pixels per logical pixel (`lp`).
- Child cell: `21 × 56 lp`.
- Bay occupancy: one, owned by `obj_sink`.
- Centre in child cell: `(10.5,14.5) lp`.
- Brass outer diameter: exactly `19 lp`.
- Room-wall alpha knockout: exactly `14 lp` diameter.
- Side safety gutter: exactly `1 lp`.
- Frame layer: `z26`.
- Sink layer: `z40`.
- Every aperture pixel: alpha `0`.
- Glazing pixels inside the aperture: none.

The ring may have brass highlights on its own opaque metal. Nothing may cross
the 14-lp opening: no glass shine, reflection, sea, sky, horizon, lighthouse,
rain streak, fog, tint or condition swatch.

## Required rendering stack

```text
z0   global lighthouse backdrop
     (real sky/sea/weather/time layers; never duplicated by the kitchen)

z20  room shell with sink-owned 14-lp circular alpha knockout applied

z26  sink-owned 19-lp brass porthole ring, fully empty in the centre

z40  sink unit
```

The porthole does not read or store weather state. Changing the global backdrop
automatically changes what is visible through every true window opening.

## Movement contract

Because the sink remains movable, a hole permanently baked at bay 7 would be
incorrect. The room renderer must derive the wall knockout from the same sink
transform used for the frame and sink:

```text
wallKnockoutDeltaLp == frameDeltaLp == sinkDeltaLp
```

V10 proves this at bays 2, 5 and 8. Each 2→5 or 5→8 move is exactly 63 lp.
No layer changes scale.

## Preservation boundary

V7, V8 and V9 files remain immutable, but V9 is not copied or accepted as the
V10 visual baseline. V10 writes fresh source, raw and draft paths. Keeper art,
runtime sprites, Final art, live room rendering, registers and manifests remain
untouched. V10 is construction and review evidence only.

## Acceptance checks

- Every pixel inside the declared circular wall opening has alpha zero.
- Every pixel inside the brass-frame opening has alpha zero.
- The complete room remains alpha zero through that aperture.
- V10 outputs contain zero illustrated condition underlays.
- The review HTML references no V8 condition layer.
- Wall opening, ring and sink have identical bay translations.
- The final 4 lp of foreground floor remain byte-identical to V7.
- Every compatible worktop is continuously opaque across the full 20-lp slab
  in every standard, on and broken frame.
- The fridge and shelf remain within their declared one-bay cells.
