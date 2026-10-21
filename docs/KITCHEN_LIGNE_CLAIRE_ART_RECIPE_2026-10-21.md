# Lighthouse Keeper kitchen ligne-claire art recipe

Date: 21 October 2026

Status: binding recipe for the reversible Kitchen Ligne-Claire Sweep V1 review
candidate. It does not approve, register, promote or wire any asset.

## Purpose

Translate the existing Lighthouse Keeper kitchen into a classic European
ligne-claire drawing language while leaving the game object itself unchanged.
Each current asset is the sole authority for what the object is and how it
works. The approved `sandwich-tomato` V2 is the closest small-object finish
reference. Frank's six supplied original comic panels supply secondary guidance
for furniture, architecture, material shorthand, contour rhythm and the balance
between busy functional detail and quiet colour fields.

The references define a visual grammar. They do not authorise copying a panel,
character, room, prop arrangement, lettering or story beat into the game.

## 1. Preserve before drawing

Lock the source canvas and semantic contract before changing colour or line.

- Preserve exact pixel dimensions, canvas size and RGBA alpha channel.
- Preserve exact alpha bounds, transparent padding and the location of every
  opaque or partially transparent pixel.
- Preserve position, perspective, proportions, orientation and footprint.
- Preserve doors, drawers, shelves, handles, hinges, appliances, surfaces,
  contents, controls and every other functional part.
- Preserve filenames, identifiers, state names, anchors, pivots, attachment
  points, collision bodies, interaction stops, support slots and layering.
- Preserve all animation frames, frame order, frame count, timing, transforms,
  state transitions, movement locks, effect ownership, interaction and healing.
- Change drawing language only. If a proposed mark changes what the object is,
  how it reads mechanically or where it occupies space, reject it.

## 2. Contour recipe

Use exact tomato-V2 ink `#051824` as the normal contour colour.

- Outer silhouettes are continuous, confident and mostly even in weight.
- At native game scale, use one decisive pixel for ordinary assets. Larger
  concept masters may use a proportionate two-pixel internalised contour, but
  the contour must never grow into a sticker rim.
- Keep contours inside the inherited alpha silhouette; never expand the
  footprint to make room for linework.
- Interior lines are fewer than the source's tonal boundaries. Keep only lines
  which explain construction, articulation, overlap, control, opening or state.
- Corners may soften slightly in the line, but geometry stays square, parallel
  or round wherever the current asset says it is.
- Avoid hatching, cross-hatching, repeated texture marks and decorative noise.

## 3. Form and projection

- Use the existing straight-on flat-cutaway parallel projection.
- Keep verticals vertical and shared horizontal datums continuous.
- Describe depth with overlap, a shallow top plane, an opening edge or one
  decisive interior line—not with tonal modelling.
- Keep scale relationships literal: one-bay bodies, worktop depth, door size,
  handle position, appliance seating and floor contact do not drift.
- Prefer a clear complete silhouette and readable negative spaces at game size.

## 4. Spot-colour recipe

Use flat, opaque, non-dithered spot colours. The shared palette begins with the
exact tomato-V2 six-colour calibration:

| Role | Colour |
| --- | --- |
| Near-black ink | `#051824` |
| Deep red | `#c32b37` |
| Tomato red | `#e84833` |
| Coral secondary | `#f57e6a` |
| Warm cream | `#f6e5b7` |
| Leaf green | `#399437` |

The kitchen extends it only where a material requires a durable semantic role:

| Role | Colour |
| --- | --- |
| Warm ivory | `#faf4e0` |
| Pale metal | `#d9ded3` |
| Mid metal | `#aebbb9` |
| Charcoal | `#5c6c6f` |
| Deep storm blue | `#1d4562` |
| Storm blue | `#235b85` |
| Blue secondary | `#2d779d` |
| Sea-glass | `#53b1b5` |
| Pale sea-glass | `#6dc9c2` |
| Water blue | `#4099c2` |
| Aged copper | `#d36f2d` |
| Brass/gold | `#e7a638` |
| Warm brown | `#905231` |
| Wood/copper secondary | `#b56636` |
| Olive | `#737d4c` |
| Pale green | `#adc284` |

Rules:

- Give one material one dominant colour and, only where readability needs it,
  one darker or lighter secondary colour.
- Use local colour rather than lighting colour: blue cabinetry stays blue,
  enamel stays cream, copper stays copper and silver fronts stay pale metal.
- Use red, green and amber sparingly for active indicators and fault grammar.
- Preserve state differences, but do not add dramatic lighting to sell them.
- Never use gradients, glossy white streaks, reflected shine, airbrush,
  painterly modelling, texture noise, bloom, haze, ambient occlusion or cast
  shadows.

## 5. Detail budget

Follow the supplied panels' rhythm: broad quiet fields carry the object, and a
small cluster of exact marks explains function.

- Keep recognisable handles, hinges, knobs, burners, displays, vents, taps,
  seams and contents.
- Remove incidental tonal edges which do not explain construction.
- At small scale, keep the most diagnostic feature first: kettle handle and
  spout, toaster slot and lever, oven hob and door, sink basin and tap, bin lid
  and pedal.
- Do not invent ornament, labels, lettering, scenery or narrative props.
- Do not simplify so far that two different states or appliances become
  interchangeable.

## 6. Material shorthand

- Enamel and ceramic: one warm cream field, ink edge, at most one restrained
  secondary plane; no white glare.
- Painted cabinetry: storm-blue face, sea-glass worktop, ink construction lines,
  copper hardware; no bevel shading.
- Metal appliance fronts: pale metal field, charcoal/ink openings, minimal blue
  secondary; no brushed texture.
- Timber: one warm brown/orange field with an ink edge; no grain unless one short
  line is essential to explain a break.
- Glass/open cavities: deep ink or storm-blue void with one clear frame line;
  transparency remains exactly where the current alpha/state declares it.
- Water, steam, smoke, smell, sparks and suds remain separate owned effects.
  They are not baked into the furniture merely to complete an illustration.

## 7. State-family recipe

- Build Off/Standard, On and Broken from the same locked construction.
- Unchanged casing and furniture geometry must remain registered identically.
- On adds only the current functional evidence: indicator, contents, control
  position or separately owned effect.
- Broken preserves the current mechanical story—same hinge side, same door,
  same detached piece, same spill, same damaged part and same floor contact.
- Full-state lighting strips receive the same colour/ink translation frame by
  frame; their timing and geometry remain unchanged.
- Effect-only strips are inherited byte-for-byte unless a separate visual gate
  explicitly redraws them.

## 8. Review and rejection test

Every candidate must be shown beside its exact current source, on transparency,
at inspection scale and at native scale. Reject a candidate if any of the
following is true:

- canvas, alpha bytes, bounds, padding, anchors, pivots or collisions differ;
- a door, drawer, shelf, handle, hinge, appliance, surface or content changes;
- perspective, proportions, orientation, footprint or floor/support contact
  changes;
- a state loses or gains a functional cue;
- the contour reads as a thick sticker rim;
- glossy highlights, gradients, texture, scenery, text or a cast shadow appear;
- a full-state animation changes timing, registration or frame isolation;
- an effect becomes detached from its owner;
- the candidate has been registered, selected as current, copied to Final or
  wired before Frank's explicit approval.

Rollback is immediate: discard only the versioned sweep directory and its
review route. All source, approved, production and runtime bytes remain in
place.

## 9. Seascape and island extension

Frank's five additional original seascape panels extend this same grammar to
the lighthouse's most important exterior environment. This section records the
world direction only; it does not add sea, sky, cliff or boat pixels to the
kitchen-furniture sweep.

### Water

- Begin with one flat sea field, normally a restrained blue or blue-green.
- Describe the surface with separated near-horizontal ink strokes and small
  hooked wave contours. Vary length and spacing, not contour weight.
- Use denser, shorter marks near rocks, wakes and shore contact; keep open-water
  passages comparatively quiet.
- White water is an explicit flat white/cream shape bounded by ink. It is not a
  soft glow, mist brush or field of random bright specks.
- A wake has a clear causal origin at the moving hull and widens behind it. A
  wave breaking on rock wraps the rock plane rather than floating in front.
- Create depth by overlap, changing line density, smaller distant wave marks and
  clear horizon separation—not by gradients, blur or atmospheric haze.

### Rocks, cliffs and islands

- Build cliffs from a few large interlocking planes with confident outer
  silhouettes. Interior fracture lines explain mass and direction.
- Keep the darkest rock notes in crevices, undercuts and overlaps; avoid tonal
  modelling across every surface.
- Distant rocks use fewer interior marks and a lighter flat local colour while
  retaining a readable silhouette.
- Vegetation appears as contained green masses with selective edge notation,
  not stippled texture or noise.
- Lighthouse, castle, jetty and harbour architecture keeps parallel, legible
  construction even when the terrain around it is irregular.

### Sky and weather

- The ordinary sky is one quiet flat field. Cloud banks are broad cream shapes
  with sparse ink contours and, at most, one restrained secondary sky colour.
- Birds are a few purposeful ink marks scaled by distance; never a repeated
  texture stamp.
- Rain, spray, fog, cloud and storm colour stay on separate controllable layers
  so the existing ambience/weather system remains authoritative.
- Storm intensity comes from wave shape, overlap, spray silhouettes and cadence,
  not bloom, dark vignettes or airbrushed atmosphere.

### Boats and maritime objects

- Hull, gunwale, seats, oars, ropes, fittings and waterline remain mechanically
  explicit and consistently registered.
- Use clean local colours and one decisive contour; do not use glossy hull
  reflections or water-colour shading.
- Preserve every gameplay anchor, collision, attachment point and motion path.
  Spray, wake and foam are independent owned effects, never baked into a hull
  merely to improve a still image.

### Motion grammar

- Animate reusable water on long, low-amplitude loops whose first and last
  frames join without a visible pulse.
- Keep moving wave marks inside declared cells with transparent gutters.
- Separate base sea, near-shore turbulence, object wakes, rock spray and weather
  so speed and visibility can follow game state independently.
- Reject any loop which reads as boiling texture, moving wallpaper or a global
  shimmer disconnected from wind, shore or vessel motion.
