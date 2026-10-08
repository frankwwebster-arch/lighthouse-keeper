# Lighthouse Keeper production art style guide

This guide is the working visual contract for new assets. It is based on the
approved original CRT television, the approved inset lantern cap, the full
lighthouse reference and the supplied BBC NEWS reference as adapted into the
`B B SEA` broadcast. New art should be checked against the finished TV at both
logical size and 4× review size before it is proposed for the game.

## The target

The game is a warm, hand-authored pixel illustration with crisp construction,
recognisable silhouettes and a little human imperfection. It is detailed at
the source-pixel level, but never noisy. Objects should look deliberately
drawn rather than like a generic pixel-art filter was applied to a photograph.

The original CRT is the strongest object reference:

- charcoal/navy casing with a warm wooden stand;
- thick, intentional dark outlines and small stepped corners;
- a readable silhouette before interior detail is added;
- compact controls, feet, aerials and other identifying hardware;
- warm cream, brass, timber and muted blue accents;
- opaque screens and glass with no unexplained white or transparent holes.

The lighthouse is assembled from the same language: strong horizontal timber
bands, painted red/cream exterior stripes, charcoal ironwork, brass fittings,
blue glass and restrained highlights. The lantern room is an inset glazed iron
cap with an outside walkway, not a full-width domestic floor.

## Pixel and geometry rules

- Standard floors are **110 × 35 logical px** with a **105 × 35** interior plate.
- The lamp cap is **95 × 35 logical px** and stays inset at the top.
- Detailed production sources use **density 4**: multiply every logical pixel
  and frame dimension by four, then render with nearest-neighbour sampling.
- Keep integer coordinates, integer anchors and integer frame translations.
  Never use fractional raster placement, blur, anti-aliasing or arbitrary
  raster rotation.
- Preserve the approved object's aspect ratio between standard, ON and broken
  states. A state may change its screen, glow or damage, but its casing and
  interaction footprint must not stretch.
- Use hard alpha: pixels are either opaque or transparent unless a deliberately
  authored effect requires otherwise. Do not leave accidental semi-transparent
  fringes around a cutout.
- Every production PNG gets a sidecar describing logical width/height, density,
  frame count/fps, anchor, keeper use point and any effect origin.

## Palette and rendering

Use a small, purposeful palette. These are reference colours, not a mandatory
flat palette:

| Use | Reference |
|---|---|
| deep outline / ink | `#14243a` |
| charcoal hardware | `#23262b` / `#10161c` |
| warm timber | `#6b4423` / `#8a5a2b` |
| cream highlight | `#f3e7cc` |
| brass/light | `#e6b955` |
| sea/glass blue | `#267da0` / `#68a7c5` |
| lighthouse red | `#c8463c` |
| BB Sea news red | `#c80000` |

Use two or three stepped shades for a material: shadow, body and highlight.
Highlights should explain form or a light source. Do not airbrush gradients,
add random one-pixel noise or outline every internal colour patch.

Keep outlines strongest on the outside silhouette. Interior seams can be one
logical pixel and may use a material-dark colour instead of the deepest ink.
Use stair-stepped diagonals and compact clusters; avoid long isolated single
pixels that do not describe a feature.

## Keeper-first scale anchor

The keeper is the first production reference for every room. Do not design a
chair, table, counter, appliance handle or doorway in isolation and then try to
fit the actor afterwards. Start from the existing runtime keeper proportions:

- feet are the floor anchor at `y = 0`;
- visible feet-to-hat envelope is approximately 108 scene units high;
- shoulder/body envelope is approximately 44 units wide;
- head centre is around `y = -80`, torso occupies roughly `y = -64..-26`,
  and legs occupy `y = -30..0`;
- hands, face and the front edge of a device must remain readable at scene
  scale, with no furniture hiding the interaction.

Before making a room set, establish the minimum keeper pose kit: idle/side,
walk, front and rear, reach/use, cook or wash as relevant, and **sit at the
matched table/chair**. Record the hand, face, seat and table-use anchors. The
catalogue's 32 × 40 keeper clips are authoring slots for reusable poses; they
do not license arbitrary rescaling of the runtime actor.

The first keeper review candidate now establishes the intended identity:
compact older keeper, navy cap with a tiny brass badge, blue work jumper with
a cream stripe, large cream beard, dark trousers and boots. Its aligned master
parts and initial clips are the scale reference for subsequent furniture.
Frank approved the identity-preserving walk and initial action set in chat;
the review canvas remains the durable place to inspect and annotate exports.

Side-facing chairs use the six-frame `sit_side` transition and manifest seat
point `(16,29)`; left-facing use is a strict horizontal mirror. Sofas, toilets
and other camera-facing seats use `sit_front` with the same seat point. Getting
up plays the matching strip in reverse. Never redraw or scale the keeper to fit
a chair: position the furniture seat under the shared anchor instead.

Doors use an invisible interaction plane: side opening mirrors for left/right,
rear opening mirrors to swap handle side, and closing reverses the matching
opening strip. Ladder art stays separate from the keeper; the rear climb clip
plays forward/up and reverse/down while runtime movement supplies world Y.
Stairs use distinct side-view ascent and descent cycles, with runtime movement
supplying the diagonal path; mirror either cycle for a left-facing flight.

Furniture approval requires a quick silhouette test with the keeper beside it
and, where relevant, seated at it. Device approval requires a believable hand
reach and a clear standing or seated use position. If the keeper's proportions
make an object unreadable, fix the object layout or pose before adding detail.

## Scale and readability

An asset must read at its actual logical display size, not only when enlarged in
the review canvas. First test the silhouette in a one-colour fill, then add
the minimum detail needed to identify it.

Small lettering is allowed only when it is essential to the design. Use a
hand-authored block glyph (normally 3×5 or 5×5), test it at 1× logical size,
and provide a clear fallback if it cannot be read. The BB Sea example literally
reads `B B SEA`; it does not rely on the viewer inferring a joke from a wave
symbol alone.

## State contract

Every keeper-owned operating device and every delivered upgrade tier has:

1. **standard** — idle, intact and usable-looking;
2. **ON** — visibly engaged, open, lit, deployed or otherwise in use;
3. **broken** — a readable fault with the same stable footprint.

The ON state is not a cosmetic recolour. It must communicate the device
operating: a lit lamp, active screen, turning mechanism, water flow, heating
element, working tool or equivalent. Do not invent ON frames for furniture.
Tables, chairs, shelves and other passive dressing remain standard unless a
real occupied/used state is needed for gameplay; label that state explicitly
instead of calling it ON.

Broken art should identify the damaged component. Prefer one or two strong
fault cues over covering the whole object: a cracked screen, loose cable,
missing pane, dark lamp, jammed mechanism or leaking joint. Shared smoke and
sparks are overlays, not baked into every casing. Attach them using the asset's
`effectOrigin`; do not assume every item breaks at its centre.

The existing broken-item body vibration is a gentle whole-object animation.
Keep it separate from the authored casing frames so it can be tuned globally.

## Animation

Animation should be economical and purposeful:

- usually 2–8 frames, stepped timing and a stated fps;
- use small changes: a mouth, eye, ticker, flame, water ripple, wheel or light;
- preserve the anchor and silhouette in every frame;
- blank or low-motion frames are valid for sparks and intermittent effects;
- do not make four copies of an item when four frames are one animated state;
- inspect the full strip and the actual playback, not only frame one.

For the TV, the casing is shared across all channels. Channel art changes only
the opaque screen content. BB Sea is `B B SEA` with `NEWS` and a newsreader;
Sport is a football match; Nature contains recognisable animals. These are
visual channels, not new gameplay systems.

## Furniture, tables and seated use

Furniture is designed around the keeper's body, not as isolated icons. A table
and chair are a matched pair: align seat height with the tabletop, leave knee
clearance beneath the table, reserve a clear approach path, and keep the chair
within the same floor's walking footprint. The chair back, seat and table edge
must remain readable when the keeper is seated. Provide a seated keeper pose
and hand-to-table/use anchor before approving a dining or work surface. A
chair does not need an ON state; its useful state is normally standard plus a
seated/occupied pose supplied by the actor layer.

## Keeper interaction and anchors

Keep the keeper's feet aligned to the floor and reserve a readable hand/face
area for the task pose. Record:

- bottom-centre object anchor;
- keeper use point;
- effect origin for the likely fault;
- bubble origin for speech or feedback;
- z-order when an overlay must sit above the casing.

Reuse chassis, handles, hinges, screens, timber stands, glass panes and keeper
poses where the construction genuinely matches. Reuse is a consistency tool,
not permission to stretch one object into another.

## Tier design

An upgrade must improve play in a measurable way at basic, mid and top tier:
capacity, duration, effect strength, reliability, reach, throughput or another
real gameplay quantity. Do not make a cosmetic-only tier. Leave an item
single-tier when no worthwhile mechanical improvement exists. Planned art may
inherit a lower-tier chassis temporarily, but must be labelled as pending and
must not imply that a new mechanic is already coded.

## Production and review checklist

Before an asset enters `art/raw/`:

- inspect the source image and remove accidental holes, fringe pixels and
  stretched proportions;
- verify the logical footprint, hard alpha, anchor and nearest-neighbour 4×
  export;
- inspect standard, ON and broken states side by side;
- play every animation and check that its effect is visible at 1×;
- check the object in the full lighthouse scene for scale, z-order and keeper
  alignment;
- add the source/provenance note and mark unresolved product choices clearly;
- run `npm run sprites` and `python scripts/verify_floor_asset_catalogue.py`.

Reject an asset if it is blurry, over-wide, materially inconsistent with the
CRT/lighthouse language, unreadable at logical size, cosmetic-only when labelled
as an upgrade, missing its ON state, dependent on an unresolved product choice,
or cut from a concept plate without an isolated-source record.
