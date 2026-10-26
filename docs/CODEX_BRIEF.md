# Lighthouse Keeper — Art Brief (Codex)

Decisions from the 26 October 2026 design session. This is the current standing
authority for all graphics work. It supersedes the former pixel-art brief and
the pixel-style V2–V4 experiments.

## 1. Direction

- Codex produces all game graphics. Makko is no longer used.
- Style: bright, cheerful, colourful 2D illustration, clean dark outlines,
  crisp shapes, saturated sunny colours. Flat colour fills with one simple
  shadow tone per material; no gradients, glossy highlights or airbrushed
  shading. Kid-appealing for ages 7–11, not babyish. Accurate, believable
  architecture with storybook charm. Light texture only. Slightly heavier outer
  silhouette lines, lighter interior lines. Light from the upper left, short
  simple shadows falling right.
- Not pixel art. The 8-bit and 16-bit concepts were tested and rejected: too
  blocky when zoomed in.
- Camera: one flat orthographic side elevation for everything. No perspective,
  vanishing points, foreshortening or curvature. Floors and ceilings are
  horizontal bands, never visible surfaces. Rooms are flat, not boxes. The
  tower is straight-sided with no taper. The island is drawn side-on (level
  ground line, cliff face below); never isometric or top-down.
- Approved layout reference: the Codex flat side-elevation tower (kitchen on
  the ground line, lair underground, two windows per floor, lawns either side,
  jetty).

## 2. Magenta key colour (ABSOLUTE)

- Everything see-through is flat pure magenta `#FF00FF`: sky, sea, all window
  glass, glazed doors, lamp-room glass, boathouse sea arch, lair portholes.
  Frames and glazing bars are drawn; nothing is painted inside the glass.
- No clouds, birds, sun, waves, horizon, islands or ships in foreground art.
  The game draws sky, sea and weather as animated layers.
- Island rock is drawn in full, including below a perfectly level waterline.
- Magenta is used nowhere else. No pink or magenta room colours.

> **Repository pipeline boundary:** the legacy `art/raw/` → `npm run sprites`
> route removes `#FF00FF`, so it is not a valid authoring or preservation route
> for the new tower, island or environment masters. Before production art is
> delivered, add a separate reviewed pipeline (or an explicit source/runtime
> conversion boundary) that retains and verifies the exact-magenta master.
> Never feed the only copy of a new master through the legacy cleanup step.

## 3. Room module grid (ABSOLUTE)

- Module: exactly 1536 × 512 px. Floor slab bottom 32 px, ceiling top 32 px,
  side walls 32 px.
- NO STAIRS are ever drawn; the stairway is hidden inside the tower wall. The
  leftmost module of each floor has one plain wooden door in its LEFT wall.
- Walk-in zone: x = 32–256, in front of the door, always empty floor.
- Bay zone: x = 256–1504, 13 bays of 96 px (numbered 1–13 from the left).
- Windows: two per above-ground module, 192 × 192 px, over bays 4–5 and 10–11,
  sills 160 px above the floor surface. Identical on every floor.
- Extra modules on a floor: joined by a 32 px interior wall with an open
  doorway; no door or walk-in zone.
- Keeper standing height about 250 px.
- Room shells are bare: walls, floor, ceiling, skirting, panelling, doors,
  window frames and listed permanent features only. No furniture, appliances,
  rugs, curtains, pictures, lamps, plants, props, stairs or characters.
- All room modules are made from ONE master module (`module_master.png`) by
  recolouring walls and adding the room's permanent features in code. Every
  other pixel stays identical; verify with a pixel diff.

## 4. Tower and levels

- Exterior: white masonry, bold red horizontal bands repeating every floor,
  stone quoins on both edges, weathered grey stone base at ground level, navy
  trim. On top: a railed gallery across the full width, then a glass lamp room
  (always the same size, centred) with slim dark frames, red domed roof and
  finial. The lamp room is empty: no lamp or lens (supplied separately).
- Grows up to 20 above-ground floors and across to 3 modules wide.
- Order, bottom to top: lair (optional, very bottom, below the waterline) →
  boathouse (optional, at the waterline, sea arch in the right-hand module,
  jetty runs from it) → kitchen and entrance (ground floor, floor exactly on the
  ground line) → interchangeable middle floors → bedroom with en-suite (always
  the top floor) → lamp room.
- Room colours: kitchen cream plaster with honey timber floor and an arched
  front door on the back wall within the walk-in zone; living room sage green
  with lower panelling; bedroom dusty lilac with an en-suite partition near the
  right end; aquarium turquoise; weather station pale blue-grey; lair dark
  stone and old masonry with arched recesses; boathouse rough rock with a stone
  quay. Other middle rooms get distinct cheerful colours, no two adjacent the
  same.
- Day 1: kitchen, living room, bedroom, lamp room. Solid rock below the kitchen.
  The keeper's small wooden rowing boat with outboard is moored at the jetty.

## 5. Modular tower kit (all at native scale)

Save to `/public/art/tower/` with `tower_kit.json` (each piece, size,
bottom-left anchor):

- `module_master.png` and recoloured `module_<room>.png` (1536 × 512).
- `module_boathouse.png`, `module_lair.png` (1536 × 512, same door and window
  positions; lair has small magenta portholes, boathouse has the magenta sea
  arch).
- `wall_left.png`, `wall_right.png` (96 × 512, one floor, exactly one red band
  at the same height so stacking repeats seamlessly); `wall_left_base.png`,
  `wall_right_base.png` (ground-floor versions with the stone base).
- `divider.png` (32 × 512 interior wall with doorway).
- `cap_left.png`, `cap_mid.png` (1536 wide, tiles horizontally),
  `cap_right.png`: cornice and railed gallery.
- `lantern.png`: lamp room, magenta glass, empty.
- Joins must line up perfectly (floor bands, red bands, quoins, gallery). Prove
  it with code-assembled previews: 4 floors × 1 module and 3 floors × 2 modules.

## 6. Island and outdoor plots

- Ground line level with the kitchen floor. Widths in FW (1 FW = 1536 px).
  Plots are level and EMPTY, marked only by surface and low stone edging where
  noted.
- Left of the tower, outwards: play lawn and washing line (1 FW short grass);
  vegetable garden (1 FW raised soil bed, stone edging); greenhouse pad (0.5 FW
  gravel); chicken coop and run (1 FW worn grass and gravel, low stone wall);
  beehive corner (0.5 FW rough grass).
- Right of the tower, outwards: barbecue terrace (1 FW stone flags); shed pad
  (0.5 FW gravel); spare plot (1 FW short grass); stone steps down the cliff to
  a wooden jetty just above the waterline.
- Day 1: only the lawn, vegetable bed and terrace are cleared; the rest is rough
  long grass and rocks.
- Structures (coop, shed, greenhouse, barbecue) are separate sprites, drawn
  later.
- Cliffs: layered grey rock, grass tufts along the top edge. No waves; the game
  adds them.

## 7. Establishing images (zoomable)

- The player's camera cuts between three fixed levels: ROOM (one module fills
  the screen), TOWER and ISLAND. Art must look good at native module scale and
  when shown whole.
- Build `day1_full.png` and `expanded_full.png` by ASSEMBLING full-resolution
  parts in code, never as a single generated picture. Save downscaled previews
  (longest side 2048 px).
- Save `day1.json` and `expanded.json`: image size, ground line y, waterline y,
  tower bounds, every module's position.
- Extract the environment palette (excluding magenta) to
  `/public/art/reference/palette.json`; all later environment and item art snaps
  to it.

## 8. Keeper character (ABSOLUTE)

- Canon files live in `/public/art/keeper/canon/` (approved side idle, front
  idle, walk loop, turns). Never modify or regenerate them.
- Never draw the keeper from a text description. Every new pose starts from a
  canon image as the input reference and changes only the pose.
- Locked design: navy peaked cap with small gold badge; full white beard and
  moustache; pink nose; bright blue knitted jumper with two white chest stripes
  and one on each sleeve, ribbed cuffs and hem; plain navy trousers; chunky navy
  boots; stocky, about 3 heads tall.
- Forbidden: sailor collar (a recurring drift on back and shoulder views),
  scarf, coat, apron, hat changes, glasses, extra stripes, logos, weapons, any
  unrequested object, any change of face, beard or build.
- Palette: extract it from the canon side idle in code into `palette.json`
  (main colours measured: blues `#0560C4`, `#0A57B5`; navies `#263E6B`,
  `#041535`; skin `#ECD1B5`; beard `#FCF1DE`). Snap every new keeper pixel to
  it; report if more than 2% were far off.
- Size: frames 256 px tall, keeper 244–256 px, anchored bottom-centre at the
  feet. Fix size by scaling and padding in code, never by redrawing.
- Animation: 2–4 key poses per action, with motion added by the engine.
  Locomotion loops may use more frames. Every animation starts and ends on the
  neutral standing pose. Props are always separate sprites.
- Not needed: stair animations (stairs are hidden).
- Approval gate: new keeper art goes to `/public/art/keeper/candidates/` with a
  side-by-side comparison against canon. It enters the game only after Frank
  approves.

> **Current repository non-compliance:** this brief requires the canon files to
> live at `/public/art/keeper/canon/`, but that target path is not yet
> populated. Existing approved Keeper Prime assets remain immutable and are not
> silently relabelled as this brief's canon. Do not create new Keeper art until
> Frank-approved references satisfying this section are installed there.

> Existing Prime machine contracts and their hash-pinned authoring,
> normalisation, room-grid and visible-circulation documents remain exact
> evidence for the installed runtime. Their old one-band identity, pixel scale,
> visible stairs and 172 × 56 geometry do not satisfy this brief and cannot be
> used as substitute canon. Leave those pinned files unchanged; this current
> brief and `AGENTS.md` provide their supersession boundary.

## 9. Items (ABSOLUTE)

- Every floor item is exactly 1 bay (96 px) or 2 bays (192 px) wide. Upgraded
  versions (e.g. range oven, 2 bays) are drawn now at final size.
- Minimal states only. Example oven: OFF, ON, INTERIOR LIGHT FLASHING (2
  frames).
- Never draw broken, dirty or alert states into an item. The engine adds overlay
  animations (smoke, exclamation marks, sparkles, drips) on top.
- Batch rule: draw one master per item, then produce every state from it in ONE
  go, changing only the element that differs (e.g. the oven's light). Every
  other pixel identical, verified by pixel diff.
- Output per item: a folder with `master.png`, one PNG per state, and
  `item.json` (states, bay width, anchor bottom-left).
- Before drawing any room's items, list them with base and upgraded bay sizes
  and confirm the fully upgraded layout fits 13 bays per module.
