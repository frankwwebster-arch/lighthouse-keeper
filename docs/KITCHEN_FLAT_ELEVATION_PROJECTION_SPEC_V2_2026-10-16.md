# Kitchen flat-elevation projection contract V2

**Date:** 16 October 2026  
**Status:** active visual-authoring authority; it approves the method, not any
individual kitchen image.  
**Supersedes:** `KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md` for new
kitchen and standard-room furniture. The earlier document remains historical
provenance explaining why V5 was built as it was.

## Decision

Kitchen V5 complied numerically with `flat-cutaway-v1`, but Frank rejected its
visual result because the combined top plane, outline, bevel and highlight
still read as excessive perspective. The room also read as a theatre platform
because its floor treatment contained several stacked horizontal bands.

The replacement projection is `flat-elevation-v2`:

> Rear-wall furniture is an illustrated front elevation attached to the wall.
> Depth comes from the Keeper passing in front, not from seeing the tops of
> everything.

## Invariants retained from V5

- straight-on doll's-house camera;
- vertical and horizontal edges remain parallel;
- no vanishing point or runtime depth scaling;
- constant Keeper and object scale in every bay;
- 4 source pixels per logical pixel (`lp`);
- 56-lp room height, 21-lp bay width and 4-lp door datum;
- 193-lp nine-bay and 256-lp twelve-bay review rooms;
- 19-lp worktop/hob/table contact and 11-lp seat contact;
- accepted asset cells, anchors, interaction spots, layer roles and cupboard
  lifecycle;
- transparent safety gutters and isolated animated states.

## V2 visual limits

| Surface or asset class | Visible planar top reveal |
| --- | ---: |
| Fridge and ordinary rear-wall cabinet/counter | 0 lp |
| Freestanding table | 0 lp |
| Cooker/hob functional cue | at most 0.5 lp |
| Sink/basin functional cue | at most 0.5 lp |
| Wall-mounted planar object | 0 lp |
| Curved kettle, bin, bowl or rounded appliance casing | natural self-volume |
| Physically rotating door leaf | projected width from its fixed hinge |

For planar furniture:

1. show the functional front only;
2. use a flat vertical nosing or apron when thickness must be readable;
3. do not draw a rear edge, diagonal corner, exposed side return or top-plane
   gradient;
4. do not taper, narrow or shrink the front face;
5. do not introduce depth by scaling the complete asset.

Curved objects are not flattened into symbols. Their curves, highlights and
self-shadow may describe their own shape, provided they do not impose a room
vanishing point.

## Floor treatment

- The visible floor cue is exactly **2 lp**.
- It has one wall/floor boundary or skirting line and one shallow colour band.
- It has no front fascia, raised lip, repeated theatre rails or converging
  boards.
- Keeper feet and every floor-standing object retain one stable foot line.
- The room remains 56 lp high; reducing the floor cue does not move or resize
  the Keeper or furniture.

## Doors and genuine rotation

The side-wall cupboard/room door remains the exception. A real rectangular
leaf may change projected width as it rotates around a fixed hinge. Its true
height, hinge location, palette and opacity remain invariant. This is object
motion, not room perspective.

## Required review evidence

Every new candidate must provide:

1. isolated assets and all states at density-4 inspection scale;
2. exact logical game-scale room evidence;
3. the prior candidate and new candidate side by side;
4. the same raster in three bays with no scale change;
5. unchanged Keeper scale beside each major asset;
6. 19-lp worktop/table and 11-lp seat guides;
7. table, Keeper and cupboard layer proofs;
8. complete nine- and twelve-bay layouts;
9. parallel-edge overlays;
10. preloaded and decoded moving media before controls enable.

## Deterministic acceptance checks

The verifier must reject:

- a rear-wall or table top reveal above 0 lp;
- a sink/cooker micro-reveal above 0.5 lp;
- any front floor fascia or a floor band other than 2 lp;
- a tapered front, diagonal planar corner or exposed planar side return;
- asset scale changes between bays;
- changes to accepted cell geometry, anchors, contact datums or cupboard hinge;
- changes outside each declared flattening mask for inherited V5 assets;
- opaque pixels on shared cell edges;
- strip/sidecar geometry disagreement;
- missing source/candidate SHA-256 evidence;
- review playback or controls before all unique images decode;
- writes to Final, runtime sprites, production manifests or any earlier draft.

## Current candidate

Kitchen Basic Assets V6 is the first `flat-elevation-v2` candidate. It is a
reversible review draft and changes no runtime or approved Keeper art. V5 is
retained intact as rejected visual provenance. V6 requires Frank's explicit
visual approval before any promotion or game wiring.
