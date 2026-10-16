# Kitchen flat-cutaway projection and layering contract

**Date:** 16 October 2026

**Status:** superseded historical authority. It explains the numeric contract
used for Kitchen V5, but Frank's visual review found that its top-surface and
5-lp floor allowances still produced too much perspective. New work must use
`KITCHEN_FLAT_ELEVATION_PROJECTION_SPEC_V2_2026-10-16.md`. It does not approve
or promote any existing kitchen art.

**Applies to:** the kitchen room shell, tier-1 kitchen furniture, their review
composites and the later reusable room/asset authoring system.

**Does not apply to:** a physically rotating door leaf, the deliberate lift
depth transition, stairs, ladders or outdoor scenes.

## 1. Visual objective

The lighthouse is presented as an illustrated doll's-house cutaway viewed
straight on. It is not a perspective-rendered room and it is not a theatre
stage.

The required look is:

- predominantly frontal and orthographic;
- readable as a shallow room through floor, overlap and layer order;
- stable enough that movable furniture can be snapped to bays without changing
  shape or size;
- compatible with the fixed-scale Keeper and deterministic interaction grid;
- gently dimensional, without conspicuous vanishing lines, tapered cupboards
  or exaggerated top surfaces.

The practical shorthand for drawing is:

> Draw the functional front elevation first. Add only enough top or exposed
> side surface to make its volume readable. Never distort the functional front
> face.

## 2. Normative projection model

The kitchen uses `flat-cutaway-v1`.

### 2.1 Required rules

1. The camera is straight-on.
2. All architectural and furniture verticals remain vertical.
3. Corresponding horizontal edges remain horizontal and parallel.
4. There is no vanishing point.
5. The Keeper remains at canonical scale everywhere in the room.
6. An asset remains the same rendered size in every bay.
7. No raster asset is scaled continuously at runtime because of room depth.
8. Navigation, collisions, snap positions and interaction points remain in the
   unprojected logical-pixel/Keeper-unit coordinate system.
9. Depth is conveyed primarily by layer order, overlap, the visible floor band,
   shallow contact shadows and small top surfaces.
10. Perspective is never manufactured by raising, shrinking, narrowing or
    tapering a complete asset.

### 2.2 Explicitly superseded rules

For kitchen and standard-room asset authoring, do **not** apply the earlier
proposal of:

- a rear wall drawn at 96% of the open-front scale;
- an asset rear face drawn at 99% of its front-face scale;
- a calculated projection distance or per-depth raster scale;
- independent perspective estimates for individual objects.

`docs/KEEPER_ROOM_PERSPECTIVE_PROPOSAL_2026-10-14.md` and Oven Approach V7 are
retained as historical review evidence. They are not the current kitchen
projection authority.

## 3. Coordinate and room constants

| Datum | Required value |
| --- | ---: |
| Logical unit | 1 logical pixel (`lp`) |
| Keeper unit conversion | 1 lp = 8 ku |
| Kitchen authoring density | 4 source pixels per lp |
| Standard room height | 56 lp |
| Furniture bay width | 21 lp / 168 ku |
| Visible floor band | 5 lp |
| Standard worktop/hob/table contact | 19 lp above the Keeper foot line |
| Chair/seat contact | 11 lp above the Keeper foot line |
| Keeper visible standing height | approximately 38 lp |

The kitchen-basic-assets brief currently defines a 4-lp door datum plus whole
21-lp bays: 193 lp for nine bays and 256 lp for twelve bays. This projection
specification does not alter those horizontal dimensions.

### 3.1 Floor treatment

- Draw a restrained **5-lp visible floor band** across the room.
- The band is a shallow doll's-house depth cue, not a stage or a second
  coordinate system.
- Do not add a separate raised front lip unless a later room-shell review asks
  for one explicitly.
- Floorboards or tiles may run horizontally or use very mild repeated detail;
  they must not converge towards a vanishing point.
- Floor-standing object anchors and the Keeper foot anchor use one stable screen
  floor line in composed interaction reviews.
- The floor band must not cause an object to be lifted above, sunk below or
  scaled relative to that line.

This resolves the oven-proxy problem: the old 30-lp proxy looked almost as tall
as the approximately 38-lp Keeper. The basic cooker body should instead obey
its 19-lp hob datum, with only its declared splashback allowed to reach 26 lp.
The correction is object proportion, not forced perspective.

## 4. Asset drawing rules

### 4.1 Functional front face

The functional front face is authoritative for:

- width and height;
- doors, drawers, controls and openings;
- handles and hinges;
- interaction/contact points;
- state changes and animation alignment;
- collision and bay occupancy.

It must be a true front elevation. Rectangular structures remain rectangular.
A cabinet, fridge, cooker, sink unit or cupboard must not become a trapezoid.

### 4.2 Allowed dimensional cues

| Asset class | Maximum visible top surface | Exposed side surface |
| --- | ---: | --- |
| Back-wall cabinet, cooker, fridge, sink unit | 0–2 lp | Normally none; only on a genuinely exposed end |
| Counter appliance attached to its unit | 0–2 lp | Only enough to describe its casing |
| Freestanding table | 2–3 lp | Permitted if both side edges stay parallel |
| Small bowl, kettle, toaster or mixer | Shape-dependent | May use ellipses/curves, without global convergence |
| Wall-mounted object | 0 lp | None unless physical thickness is essential |

Top surfaces use a shallow orthographic/oblique construction:

- the rear edge remains the same width as the front edge;
- left and right edges remain parallel;
- no horizontal narrowing towards the rear;
- no more than the limits above;
- one consistent light direction and one consistent shallow depth direction.

End faces must be omitted between adjacent units. They may appear only at the
exposed end of an independent object, and must not increase its declared bay
footprint.

### 4.3 Scale and proportions

- The Keeper is the world ruler. Do not resize him to fit furniture.
- Do not enlarge a cooker, table or cupboard merely to fill its transparent
  cell.
- Do not shrink a rear-wall object because it is notionally farther away.
- Respect `data/keeper_object_dimensions.json` and
  `data/keeper_asset_contract.json` for contact heights.
- Preserve declared whole-bay occupancy and transparent safety gutters.
- An effect or open door may require a larger cell; enlarge the transparent
  cell rather than shrinking the object.

### 4.4 Colour, outline and lighting

- Use the established smooth, anti-aliased kitchen style at the declared source
  density.
- Keep outer contours and internal line weights consistent across the family.
- Use local value changes to describe planes; do not use perspective gradients.
- Use small grounding/contact shadows only. Avoid long cast shadows that imply
  an unmodelled light or depth geometry.
- State animation must not change the base object's palette, apparent scale,
  outline weight or perspective.

## 5. Kitchen-specific construction

### 5.1 Back-wall run

The fridge, kettle unit, toaster unit, cooker, mixer unit and sink unit are
predominantly frontal assets. Each remains independently movable and must not
depend on its neighbour's pixels.

- All counter units share the exact 19-lp worktop/hob contact datum.
- Worktop thickness is consistent across the family.
- Adjacent units align without requiring a shared baked worktop.
- The fridge remains visibly freestanding where specified by the kitchen brief.
- The cooker body remains materially shorter than the Keeper; its splashback is
  not part of the body-height comparison.
- Open doors, steam, smoke, water and other state effects remain isolated in the
  asset's declared cell and safety gutter.

### 5.2 Table and chair

The table is allowed slightly more visible top surface than the back-wall run,
but it still uses parallel, non-converging edges.

Maintain the established composition:

1. chair/background layer;
2. Keeper layer;
3. table/apron foreground layer.

The seat contact remains 11 lp and the dining surface remains 19 lp above the
Keeper foot line. The apron may occlude the thighs; the boots must remain
legible where the approved seated pose requires them.

### 5.3 Small floor objects

The bin and pet bowl use the same flat room coordinate system.

- Their bottom contact is stable across all states.
- Full, overflowing, cracked or puddle states must not shift the base object.
- The pet bowl may remain a foreground child of the table, but this is a layer
  role, not a perspective scale.

### 5.4 Cleaning cupboard and doors

A stationary closed cupboard or architectural door face is a front-elevation
rectangle. A moving hinged leaf is the sole ordinary-room exception to the
constant screen-width rule:

- its real height and leaf dimensions remain invariant;
- its hinge point remains fixed;
- closed/edge-on presentation is a thin vertical edge;
- projected width increases as the leaf physically rotates through 90 degrees;
- fully open presentation is an opaque rectangular panel;
- there is no trapezoidal deformation, gradient depth or whole-leaf scaling;
- the real leaf supplies Keeper/tool/costume occlusion.

Door rotation is object motion, not room perspective.

## 6. Layering contract

Depth is categorical. A suggested ordering is:

| Role | Relative order |
| --- | ---: |
| Room wall and floor | 10 |
| Recesses and behind-Keeper architecture | 20 |
| Back-wall furniture | 30–40 |
| Keeper | 50 |
| Table apron or declared foreground furniture part | 60 |
| Small declared foreground child | 70 |
| Open door leaf / genuine occluder | 80 |
| Effects that must appear in front | 90, only when explicitly declared |

The numbers may be mapped to the existing renderer, but their ordering must be
preserved. Do not create perceived depth by scaling the same object between
layers.

## 7. Metadata contract

The next draft should record the room projection once and keep asset-specific
exceptions explicit. A suitable structure is:

```json
{
  "projection": {
    "id": "flat-cutaway-v1",
    "runtimeDepthScaling": false,
    "vanishingPoint": null,
    "horizontalConvergenceLp": 0,
    "floorBandLp": 5,
    "maxBackWallTopRevealLp": 2,
    "maxFreestandingTopRevealLp": 3,
    "keeperScale": 1
  }
}
```

Each asset record should include at minimum:

```json
{
  "supportAnchorLp": [10.5, 21],
  "interactionPointsLp": {
    "worktop": [10.5, 2]
  },
  "layerRole": "back-wall-furniture",
  "bayOccupancy": 1,
  "topRevealLp": 1.5,
  "hasPerspectiveConvergence": false,
  "runtimeScaleByDepth": false
}
```

Use the real cell and contact coordinates for each object; the example values
do not override the asset contract.

## 8. Required review presentation

Create a fresh versioned review candidate. Do not rewrite Kitchen V1–V4 or any
canonical/runtime art.

The review must show:

1. each isolated asset and every state at a large inspection scale;
2. each asset at **4× authoring scale**, labelled as such rather than “exact
   physical game size”;
3. the complete nine-bay kitchen with the 5-lp floor band;
4. the same asset moved between at least three bays with no scaling or shape
   change;
5. the Keeper beside every major asset at unchanged scale;
6. interaction overlays for worktop/hob/table at 19 lp and seat at 11 lp;
7. the table/seat and cupboard/door layer stacks;
8. the twelve-bay reservation without stretching any repeated module;
9. a front-elevation guide proving verticals and horizontals remain parallel;
10. a toggle showing any shallow top/side cue separately from the functional
    front face.

The page must preload and decode all unique moving-frame URLs before enabling
playback or controls.

## 9. Deterministic acceptance tests

The verifier must fail if any of the following occurs:

- a furniture state changes its support anchor or base footprint;
- an asset changes scale when placed in another bay;
- a declared rectangular front face tapers or converges;
- a top surface exceeds its class limit;
- any kitchen object introduces runtime depth scaling;
- worktop, hob, table or seat contacts miss their declared Keeper datums;
- an animated state changes unchanged out-of-scope pixels without declaration;
- an asset, effect or detached component touches a shared cell edge;
- strip geometry and sidecar geometry disagree;
- room repeat modules fail to join at any supported bay count;
- foreground/background ordering contradicts the declared layer role;
- a door's actual height or hinge datum changes during rotation;
- a review URL begins playback before all unique frames decode;
- any draft overwrites V1–V4, canonical art, runtime sprites or production
  manifests.

Also record original and candidate SHA-256 values and prove a byte-identical
rebuild.

## 10. Approval boundary

This specification approves the **projection method**, not any kitchen image.
Kitchen V1–V4 remain reversible review provenance. The next task must produce a
new versioned candidate and present it for Frank's visual approval. Nothing may
enter Final, runtime or production without his explicit approval.

## Ready-to-paste task instruction

> Continue the Lighthouse Keeper kitchen-basic-assets work in
> `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on `main`. Read
> `AGENTS.md`, `docs/CLAUDE_TO_CODEX_KITCHEN_BASIC_ASSETS_2026-10-15.md`,
> `docs/KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md`,
> `docs/KEEPER_ASSET_SCALE.md` and `data/keeper_object_dimensions.json` before
> changing anything. Treat `flat-cutaway-v1` as the projection authority:
> straight-on camera, parallel verticals/horizontals, no vanishing point, no
> runtime depth scaling, constant Keeper and asset scale, a restrained 5-lp
> floor band, back-wall top reveals no greater than 2 lp and freestanding-table
> top reveal no greater than 3 lp. The earlier 4% room / 1% asset convergence
> proposal is historical evidence only and must not seed the new drawings.
> Preserve Kitchen V1–V4 unchanged and build a new reversible versioned
> candidate. Show isolated assets, complete nine- and twelve-bay compositions,
> three-position no-rescale proofs, fixed Keeper contact overlays and declared
> layer stacks. Add deterministic checks for parallel geometry, contact datums,
> constant scale, cell gutters, unchanged pixels, modular joins, metadata and
> archive hashes. Promote or wire nothing without Frank's explicit approval.
