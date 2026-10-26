# Lighthouse establishing-shot drafts — 26 October 2026

These two generated images are rejected historical layout drafts for the
foreground lighthouse and island. They remain measured review evidence, but
they are neither current visual direction nor approved runtime art. Frank
rejected their sterile rectangular/apartment-block character in favour of the
original concept's warm tapered lighthouse, rich distant-island backdrop and
magical island-splitting expansion. The current circulation, door and sound
authority is `docs/HIDDEN_CIRCULATION_DOORS_AND_AUDIO_2026-10-26.md`.

The later V3 pixel-style test is documented in
`docs/LIGHTHOUSE_PIXEL_STYLE_TEST_2026-10-26.md`. It does not rehabilitate
either rejected establishing shot or alter the binding hidden-circulation
contract; its Concept C intentionally preserves the Day 1 image as a failure
control.

## Files

- Day 1: `public/art/reference/day1.png`
- Day 1 geometry: `public/art/reference/day1.json`
- Fully expanded: `public/art/reference/expanded.png`
- Fully expanded geometry: `public/art/reference/expanded.json`
- Repeatable geometry measurement: `node tools/measure-reference-art.cjs`

Coordinates use a top-left origin. Tower bounds are inclusive and cover the
lamp room, gallery and exterior shell down to the measured ground line.

## Binding layout decisions

- The view is a straight-on orthographic doll's-house cutaway. Back walls are
  flat panels; floors are horizontal bands; side and partition walls are
  vertical bands. The island is a side elevation, not an isometric ground
  plane.
- Day 1 has two enclosed floors: the ground-floor kitchen/entrance and the
  top-floor bedroom/en-suite. The lamp room sits above them. There is no Day 1
  living-room floor or underground room.
- The expanded tower has exactly 20 enclosed floors above ground, with three
  equal room modules on every floor. It also has a three-module boathouse at
  the waterline and a three-module lair below it.
- There is one circulation entrance per floor between a narrow concealed
  vertical slot and that floor's room. No stair, landing, lift car or shaft is
  visible. There are no doors between width modules. The bedroom alone has a
  second door into the en-suite on its right, and the ground-floor exterior
  entrance is separate.
- A closed circulation entrance shows only its slim side jamb. Its flat opaque
  door panel appears only while opening toward the player and becomes the
  foreground occluder (`room shell -> Keeper -> open door panel`). Stair
  travel and, after its upgrade, lift travel happen entirely behind it.
- Hidden stair travel owns the replaceable sound placeholder
  `footsteps_stone_stairwell`: Keeper boots on worn stone with a short enclosed
  tower echo. It starts after full departure occlusion and stops before the
  destination entrance opens; it never plays for the lift.
- Magenta is reserved for the removed sky/sea layers and glass/open-water
  apertures.

## Measured geometry

| Draft | Canvas | Ground line | Waterline | Tower bounds |
| --- | ---: | ---: | ---: | --- |
| Day 1 | 1672 x 941 | y=571 | y=705 | x=576..962, y=0..571 |
| Expanded | 1024 x 1536 | y=1225 | y=1388 | x=305..717, y=0..1225 |

## Known non-compliance — do not promote unchanged

The built-in image generator produced strong composition drafts, but the
following brief requirements remain unresolved:

- The apparent magenta is not byte-exact `#FF00FF`. Neither PNG contains an
  exact key pixel; both use a visually similar range of magentas. Production
  chroma-key art needs deterministic colour normalisation and edge cleanup.
- Both roof finials touch the top canvas edge, so the complete tower silhouette
  lacks the requested breathing room.
- In Day 1, the outdoor ground edge is measured at y=571 while the visible
  kitchen floor sits higher; they do not yet share one exact horizontal line.
- The expanded outdoor surfaces do not distinguish every requested plot and
  width clearly enough. The five left plots and three right plots need a
  deterministic layout pass.
- Several expanded middle floors use peach/coral hues close to pink, contrary
  to the no-pink room-wall rule.
- The lamp room and module geometry are stylistically related across the two
  canvases but are not pixel-identical in size.

These limitations are recorded deliberately. The PNGs may still help explain
the rejected orthographic experiment, but they must not be used as composition,
door-layout or production foreground authority.
