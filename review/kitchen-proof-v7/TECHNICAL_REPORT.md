# Kitchen v7 — pre-cut technical report

## Outcome

Kitchen v7 is complete to the explicit **stop-before-cutting** boundary. The
candidate is a freely painted, visually coherent 1950s room rather than a row
of separately generated tiles. It uses the approved calibration's dense,
confident ligne-claire treatment and Frank's cooker reference. The final room
is shown with the unchanged Prime Keeper at native 1:1 scale.

No object, door, interior, mask or state has been cut. No runtime or canonical
asset was changed. The file to approve or reject is:

`outputs/kitchen-v7-free-room-with-prime-precut.png`

| Gate | Result |
|---|---:|
| Final room | `2048 × 576` RGB |
| Prime Keeper | exact `256 × 320` source, composited at 1:1 |
| Keeper sole datum | source y `316` on room y `502` |
| Exact magenta | `38,088` pixels, all and only in eight pane interiors |
| Near-magenta | `0` |
| Window authority | x `622–790` and `1294–1462`, y `106–274` |
| Ceiling / floor slabs | y `0–31` / `544–575` |
| Side jambs | x `0–31` and `2016–2047`, y `208–543` |
| Cutting performed | **No** |
| Production/canon mutation | **No** |

## Visual result against the v7 GO notes

- One harmonious family of glossy duck-egg freestanding cabinets, each with
  its own silhouette and copper handle; there is no fitted continuous run.
- Low rounded cream fridge; Belfast sink cabinet; kettle cabinet; cooker;
  chrome diner table with two red chairs; toaster cabinet; mixer cabinet; and
  cream pedal bin, in the v7 left-to-right order.
- Matching decorative cupboards sit above the fridge and cabinets 2, 3 and 4.
  None overlap a window or the cooker hood.
- Flat two-row black-and-white checkerboard floor; no vanishing point.
- No royal blue kitchen furniture. Blue remains only in the immutable Keeper.
- No cast or contact shadows. Material weight comes from bevels, highlights,
  inner tones, hardware and line detail.
- Both window rectangles are deterministic structural pixels. Furniture and
  cupboards cannot intrude because each complete rectangle is restored after
  generation.
- The cooker follows `reference/kitchen-mood/kitchen-mood-07-cooker.png`: cream
  body, four gas burners under black supports, four copper/orange knobs, long
  copper handle, eye-level grill on metal supports and pull-down grill pan.
- The cooker control strip has two separate unlit dark bezels: the left is the
  red heat indicator target (`indicatorPointPx` after cutting), the right is
  the universal appliance status target (`statusLampPx` after cutting).
- The oven has a closed dark-tinted window with the cavity back, runners and
  shelves visible. No baked-in glow is present.
- The fridge, kettle, toaster and mixer each have a visible unlit status-lamp
  bezel. Sink, table/chairs and bin correctly have none.

## Generation and deterministic finishing

The built-in image-generation tool was used in image-edit mode with five
references: the exact 2× structural shell, the approved style calibration,
the primary kitchen mood image, Frank's cooker reference and the historical
V7 oven authority. `PROMPT_LOG.md` records the prompt set and passes.

The selected paint is pass 05. Deterministic finishing does only this:

1. centre-crop the generated canvas to the exact `2048:576` aspect and resize
   once with Lanczos;
2. restore the top and bottom slabs and both side jambs from the exact shell;
3. restore both complete window rectangles;
4. write the eight pane interiors as hard `#FF00FF` and remove near-magenta
   resampling colours inside the window rectangles;
5. composite the unchanged Prime side-right frame at 1:1, centred at x `250`,
   with its opaque sole datum on walkY `502`;
6. create the calibration comparison sheet.

There is no palette snapping, re-inking, shadow synthesis, segmentation or
cutting. The previous passes remain only as reversible provenance; pass 05 is
the sole selected source.

## Placement implications before the cut

This is the freely painted composition required before stop placement. It
preserves the correct order, scale language and empty walk-in zone, but it is
not represented as exact runtime placement. After approval, objects must be
cut on their painted silhouettes and moved to the section 10b reservation
centres. That distinction is deliberate in the v7 method.

| Runtime part/group | Reservation x | Midpoint | Post-approval operation |
|---|---:|---:|---|
| Low fridge | `378–530` | `454` | Cut body/interior and door; fit uniformly only if the painted envelope exceeds the reservation. |
| Sink cabinet | `622–790` | `706` | Cut as one freestanding cabinet; taps remain below y `274`. |
| Cabinet 2 + kettle | `811–937` | `874` | Cut cabinet and kettle separately; centre both on stop 7. |
| Cooker | `1025–1227` | `1126` | Cut cooker body, oven door and required internal layers; translate right to stop 10. |
| Diner set | `1244–1513` | `1378` | Cut table and each chair separately, then tuck the chairs under the table to fit; do not shrink the complete set as one image. |
| Cabinet 3 + toaster | `1567–1693` | `1630` | Cut separately and centre on stop 16. |
| Cabinet 4 + mixer | `1735–1861` | `1798` | Cut separately and centre on stop 18. |
| Pedal bin | `1945–1987` | `1966` | Cut and uniformly fit to the 0.25 m reservation. |

The cut stage must report actual opaque bounds before any scaling. Uniform
scale is permitted only where the real-size envelope is wrong. Horizontal
translation is the normal operation. No runtime reflow is permitted.

## One-drawing and separate-door contract

The flattened room proves the approved appearance; it is not itself the item
master. After Frank approves the paint, the cut stage must produce one and only
one canonical body drawing per item/tier. State names reference that same body
hash. No independently generated Off, On, Broken or Open full-item redraw may
enter production.

The fridge and oven doors are moving parts, not states:

- cut each door once as a separate RGBA sprite with transparent gutter;
- build the unchanged body with a complete interior beneath it;
- record the door sprite's item-local `hingePx`, `closedPose{x,y,rotationDeg}`
  and any allowed open pose in `movingPartOverlays[]`;
- demonstrate closed and open by transforming the same door bytes;
- demonstrate the cooker's hanging-door fault by rotating/translating that
  same door sprite about the same hinge;
- never use an open or hanging door as a fridge fault. The fridge fault remains
  flashing red status, cold mist and drip/puddle FX.

The explicit stop-before-cutting instruction means item-local hinge and light
coordinates are not fabricated in this report. They must be measured from the
approved cut canvases, entered in `item.json`, and verified to lie within their
declared canvases.

## Required cooker layer stack after approval

Back to front, all registered in the cooker canvas:

1. `engineLight`: no art file. The engine paints warm light in `lightRectPx`;
   absent Off, steady On, random flicker Broken.
2. `cookerBody`: one invariant RGBA drawing. Its complete cavity contains the
   back wall, sides, shelf runners and shelf as line work over partial-alpha
   dark tint so the engine light remains visible through it.
3. `contentsCooking` / `contentsBurnt`: two small sprites at `contentsPx` with
   byte-identical alpha silhouette, outline and registration. Only internal
   colour/detail differs. No contents is the Off state.
4. `ovenDoor`: one sprite. Its glass is partial-alpha dark tint at every pose;
   the same bytes are used closed, open and askew.
5. engine FX: indicator dot at `indicatorPointPx`, status dot at
   `statusLampPx`, smoke at `effectOriginPx`.

No glow or indicator sprite is to be drawn. The partial-alpha glass regions
must remain genuine RGBA after cutting; exact magenta is only for opaque room
apertures, not item glass.

## State recipes Claude can implement

| State | Unchanged art | Replaceable elements |
|---|---|---|
| Cooker Off | body + door in closed pose | no cavity light; no contents; indicator and status bezels unlit |
| Cooker On | same body + same closed door | steady engine light; cooking contents; engine-drawn red heat indicator; steady green status |
| Cooker Broken | same body + same door, transformed askew | flickering engine light; burnt contents; smoke/occasional shake and bang; flashing red status |
| Fridge idle/working | same body + same closed door | steady green status while operating normally |
| Fridge used | same body + same door, transformed open | optional engine light behind the open interior; no body redraw |
| Fridge broken | same body + same closed door | flashing red status; shared cold mist and drip/puddle FX; door unchanged |
| Kettle/toaster/mixer working | same single drawing | steady green status; activity FX/prop only where specified |
| Kettle/toaster/mixer broken | same single drawing | flashing red status plus shared smoke/sparks/shake recipe as appropriate |

The required review composites—Off closed/empty, On closed/cooking/lit, Broken
burnt/askew/flickering/smoking, plus fridge closed/open—are the first output of
the cut stage. Producing them now would either cut the unapproved room or fake
them with redraws, violating one of Frank's two explicit rules.

## Post-approval verification gates

The cut is not complete until all of these pass:

1. each item body has one SHA-256 across all state recipes;
2. the fridge and oven bodies reveal complete interiors when the same door
   sprite is transformed away;
3. closed, open and askew door composites use one door SHA-256 per appliance;
4. cooking and burnt contents have identical alpha and outline masks;
5. `lightRectPx`, `contentsPx`, `hingePx`, `indicatorPointPx`,
   `statusLampPx` and `effectOriginPx` are in bounds and visibly aligned;
6. the engine light is behind body linework, contents and partial-alpha door
   glass; no baked glow or glow sprite exists;
7. every electrical item has one unlit status bezel and non-electrical items
   have none;
8. every cut sprite has transparent safety gutter and no shared-edge alpha;
9. exact magenta remains confined to room-aperture pixels;
10. the assembled room obeys all reservations, midpoint stops, y geometry and
    window exclusions without runtime reflow.

## Boundaries and documentation audit

- No `parts/` directory was created.
- No file under `public/`, `src/`, canonical Keeper art or any prior immutable
  review folder was changed.
- The exact-magenta master route is exercised locally by deterministic source
  and verification; this review does not promote a new runtime art pipeline.
- `docs/SPEC.md` remains the current authority. `docs/CODEX_BRIEF.md` still
  contains historical 1536 × 512 geometry and therefore must not be used to
  override this v7 task.
- README/runtime documentation does not change because this is an unapproved
  review candidate with no product behaviour change.
