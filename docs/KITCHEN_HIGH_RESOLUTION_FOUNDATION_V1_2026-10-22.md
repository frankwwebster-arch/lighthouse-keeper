# Kitchen high-resolution foundation V1

**Decision date:** 22 October 2026
**Status:** cabinetry/appliance visual foundation approved; production crops,
state variants, registration and runtime remain gated

## Approved coordinated cabinetry foundation

Frank approved the exact six-module construction sheet on 22 October 2026:

`art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png`

It is the byte-exact `1536 × 1024` RGBA
`exec-e3c53515-09df-45b2-b5f3-0cf65cc185b9.png`, SHA-256
`898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3`.
The sheet draws cupboard, drawers, sink, dishwasher, oven and the basic
undercounter fridge together. This is the fixed visual/body foundation for the
fitted family. Its approval ends the practice of independently redrawing a
complete appliance for each state.

The next gated stage must derive Off, On and Broken art from these exact bodies.
Doors, contents, indicator fills and environmental effects live in separately
registered layers; the approved body pixels do not move or get regenerated.
Loose objects—kettle, toaster, bowl and bin—follow as a separate coordinated
family after the fitted state system is stable.

The sheet is a visual construction authority, not a production atlas. Its dark
presentation background/halo is not game art, its grid is not a declaration of
logical crop bounds, and no runtime selector changed. Exact production
extraction, transparent isolation, logical geometry and native-size proofs have
their own review gate. The approval is pinned at
`docs/review/kitchen-cabinetry-foundation-v1-approval-2026-10-22.json`.
The exact approved sheet and the original fitted-run authority are available
together at `/keeper-review/kitchen` (immutable versioned route
`/keeper-review/kitchen-cabinetry-foundation-v1/index.html`). The preceding
`/keeper-review/kitchen-high-resolution-foundation-v1/index.html` page remains
unchanged as historical evidence.

## Why the earlier candidate path stops here

Kitchen Complete Review V60 and its predecessors flattened high-resolution art
into native `1×` room rasters before display. Enlarging the `772 × 224` canvas
therefore enlarged a thumbnail rather than revealing retained detail. Later
compositing also mixed complete cabinet shells with appliance frames, producing
double-dark stiles, dirty hinge regions, inconsistent worktop undersides and a
damaged-looking hob.

Frank has explicitly restarted the kitchen as an entirely new high-resolution
art programme. V60 remains immutable provenance, but it is no longer the active
visual direction.

## Primary review view

Frank selected the exact first fitted-run render as the primary visual,
composition and style exemplar:

`art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png`

It is the byte-exact `exec-b28bb76f-bdd9-4d95-bae6-4d25ab665468.png`
generation: `2203 × 714`, SHA-256
`bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2`.
It now appears first and alone as the visual candidate at
`/keeper-review/kitchen`. Its centred, rear-set sink, coherent fitted-run
relationships, relative visual presence, retained sharpness, warmth and
restrained three-dimensional modelling are the baseline. Later state atlases
are diagnostic exploration, not the main view and not competing candidates.

This selection does not turn the complete render into a crop-ready sprite
sheet. In particular, its tall fridge is not the basic game fridge and its
displayed module widths do not replace the fixed game geometry. Production
extraction/redrawing must keep the basic fridge undercounter, obey the existing
footprints and retain the exemplar's dimensional warmth without turning it
into glossy mobile-game icon art. The exact render is preserved unchanged so
those adaptations cannot silently damage the chosen sink, style or composition.

The latest coordinated Off/On/Broken exploration remains preserved at
`art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-complete-state-family-atlas-v5-strict-ligne-claire.png`.
It is useful only for state inventory: undercounter fridge treatment, detached
broken components, contents, burnt toast, broken bin and separately authored
effects. It is not the active visual authority and must not be presented ahead
of the selected first render.

## Revised kitchen visual target

The exact first render supersedes the earlier strict-flat interpretation for
the kitchen. `exec-036d9986-abce-4f47-9e6a-2896bc245f8e.png` was strongly
ligne-claire aligned and mechanically disciplined, but its schematic flatness
made the kitchen too harsh and removed too much of the desired depth.

The target is adult cinematic ligne claire: the warmth and dimensional presence
of a Tintin feature film, not the cute or toy-like finish of a children's game.
Production art therefore preserves:

1. clear disciplined black contours with near-consistent weight;
2. lines only for real edges and useful mechanical separations;
3. observationally accurate adult proportions and mechanisms;
4. closed colour shapes with restrained two- or three-tone modelling;
5. subtle highlights, recesses, bevels and contact shadows where they describe
   real form;
6. immediate clarity at 64 pixels;
7. separate, disciplined action marks and environmental effects;
8. the first render's warmth, depth and visual generosity.

It rejects candy-plastic gloss, bloom, texture noise, hatching, inflated forms,
mascot proportions, caricature and anything cute, juvenile or toy-like. The
action-imagery recipe remains useful for edge discipline, clear construction
and effect separation, but it no longer overrides the first render's restrained
three-dimensional modelling in this kitchen programme.

## Geometry does not change

High resolution changes source density, not game size. The existing logical
geometry remains binding:

- room: `772 × 224` logical pixels;
- fitted bay: `84` logical pixels wide;
- base body: `84 × 74` logical pixels;
- normal fitted cell: `92 × 82` with four-pixel gutters;
- base baseline: room y `208`;
- current worktop support plane: room y `141`;
- basic fridge: one-bay undercounter appliance, not the later tall upgrade;
- Kettle V47 room footprint: `46 × 41` Off/On and `50 × 47` Broken.

The complete machine-readable authority is
`data/kitchen_high_resolution_asset_contract_v1.json`.

## Zoom-safe production rule

Every production master carries at least eight source pixels per logical pixel.
That supports a `4×` gameplay zoom on a `2×` display without magnifying a `1×`
thumbnail. The renderer sizes its backing surface from logical viewport × zoom
× device-pixel ratio and draws from the high-resolution master directly. A
native-size PNG may exist as a review thumbnail only.

## Structural perspective healing

Movable units still require geometry to respond to their neighbours. The new
foundation therefore retains healing as occupancy-derived construction rather
than raster repair. At every placement change, the renderer derives the
continuous worktop top/front/rear edges, exposed side faces, perspective end
caps and plinth from the current contiguous bays and renders that structure at
master scale before drawing the modules. It never lays join caps, backfills,
cleanup sprites or oven triangles over finished art.

## Broken animation is authored with the art

Every powered appliance delivers a dark indicator housing in its body plus a
separate, same-canvas RGBA indicator component. On lights and Broken blinking
lights are never recovered later by colour selection from a flattened image.
The default Broken indicator loop is a deterministic irregular 40-frame,
8-fps step sequence.

Component motion is separate again: fridge/dishwasher/oven doors, dishwasher
handle, oven dial, toaster lever, kettle lid, bin lid and sink handle each have
named transform layers where applicable. Smoke, steam, suds, leaks and stink
remain post-hoc environmental effects with explicit anchors; flies are excluded
from the kitchen language. Every Broken family therefore has visible motion
even if an environmental effect is disabled. Repair cancels indicator timers,
transforms and SFX synchronously.

## Reversibility

Nothing in this foundation changes approved Kettle V47 files, approved V46
motion/SFX behaviour, historical review pages, runtime assets, selectors or
production sprites. The approved construction sheet is preserved byte-exactly
in separate draft and source directories. Rejecting it requires discarding only
those directories and its external approval record; canonical runtime and
historical art remain untouched.
