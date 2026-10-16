# Ready-to-paste prompt: rebuild Kitchen V6 from V5

Work in `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on current remote
`main`.

Before changing anything, read completely:

- `AGENTS.md`
- `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md`
- `docs/KEEPER_ANIMATION_HANDOFF.md`
- `docs/KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md`
- `docs/CLAUDE_TO_CODEX_KITCHEN_BASIC_ASSETS_2026-10-15.md`
- `docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V5_2026-10-16.md`
- `docs/DEPLOYMENT.md`

## Provenance and authority

Use Kitchen Basic Assets V5 as the sole visual and geometric starting point:

- review: `/keeper-review/kitchen-basic-assets-v5/`
- source: `art/source/kitchen-basic-assets-2026-10-16-v5/`
- raw draft art: `art/raw/kitchen-basic-assets-2026-10-16-v5/`
- draft records: `art/drafts/kitchen-basic-assets-2026-10-16-v5/`
- builder: `scripts/build_kitchen_basic_assets_v5.py`

An earlier flat-elevation V6 was explicitly rejected and removed. Do not
recover, copy, transform or imitate it. Its failure was that it flattened away
the readable countertops, reduced the illustration quality, produced weak and
inconsistent counter treatments, and made the animations look especially
rough. It is rejected provenance only.

V5 is not approved or production art, but it is the preferred visual baseline.
The new candidate must be a fresh, versioned and reversible V6. Do not overwrite
V5, any earlier draft, canonical art, runtime sprites, Final art, manifests or
immutable review exports. Promote nothing without Frank's explicit approval.

## Objective

Keep the character, warmth, polish, volume and visible countertop surfaces of
V5. Correct the excessive or inconsistent perspective by redrawing the
problematic geometry only.

The key distinction is:

> The countertops must remain visibly present. The cabinet and appliance bodies
> beneath them must not taper, lean or change width.

This is a straight-on illustrated doll's-house view with a very shallow,
consistent oblique cue—not a completely flat elevation and not a perspective
room with converging furniture.

## First gate: countertop construction study

Do not redraw the whole kitchen immediately. First make a small review-only
calibration page using exact V5 art for three representative units:

1. a normal counter unit, preferably the kettle or toaster unit;
2. the cooker/hob;
3. the sink.

For each unit, keep the V5 front face and appliance detail and show no more than
three carefully drawn alternatives for the countertop geometry. All
alternatives must:

- retain a clearly visible shallow top surface;
- keep the front cabinet's left and right sides perfectly vertical;
- keep front and rear countertop edges horizontal and equal in width;
- use one common top-surface depth, shear direction, slab thickness, outline
  weight and highlight treatment across all three units;
- use no vanishing-point convergence and no rear-edge narrowing;
- show how two neighbouring units meet without a wedge, angled gap, double
  outline or change of height;
- be shown at native 4x authoring scale and exact logical game scale;
- include V5 beside each option and a ghost/edge overlay.

The likely useful range is a 1–2 lp visible top surface. Do not treat that range
as permission to improvise independently per unit: choose one shared
construction. Stop after publishing this calibration gate and ask Frank to
select the treatment before applying it to the complete family.

## Geometry contract after the calibration is selected

Preserve V5's accepted measured layout unless a conflict is demonstrated:

- 56-lp room height;
- 21-lp furniture bays and existing transparent safety gutters;
- 19-lp worktop, hob and table contact datum;
- 11-lp chair seat contact;
- 193-lp nine-bay and 256-lp twelve-bay room widths;
- V5 object heights, interaction spots, anchors, bay occupancy and draw order;
- V5's five-lp restrained floor band;
- the established right-side-wall cupboard, fixed right hinge and opaque open
  leaf behaviour.

For the fridge, kettle unit, toaster unit, cooker, mixer unit and sink unit:

- the structural front is a true rectangle;
- outer body sides are vertical and parallel;
- body width is identical at top and bottom;
- every counter/hob edge meets the same 19-lp datum;
- the chosen top plane is constructed identically on every compatible unit;
- countertop colour, thickness, outline and highlight are consistent across
  the whole run;
- internal neighbouring ends do not expose independent side faces;
- a genuine exposed end may have one restrained end face, but it must not alter
  bay occupancy or create a taper;
- appliances may retain curved self-volume, but their perspective must not
  dictate a different countertop angle;
- the fridge remains recognisably freestanding;
- the cooker must remain materially shorter than the Keeper.

Do not solve geometry by resizing, narrowing, vertically compressing or
re-rendering whole V5 assets. Redraw only the countertop, side silhouette or
small adjoining pixels that are necessary. Preserve the good V5 fronts,
details, palette, line weight, highlights and smooth antialiasing.

The table may retain a slightly larger visible top than the back-wall run, but
its front/rear edges must remain parallel, its two side edges must use the same
construction, and its V5 chair/Keeper/table layer order must remain unchanged.

## Animation quality contract

V5's animation content and timing are the baseline. The new V6 must not
re-render the complete unit for each frame.

For every animated state:

- derive one finished, approved-in-batch base unit from the standard frame;
- reuse that exact base in every frame of `on`, `broken`, open or effect states;
- allow changes only inside a declared effect or moving-part mask;
- keep the cabinet, countertop, outline, feet, handles and stationary hardware
  pixel-identical across frames unless that specific part is the declared
  moving mechanism;
- never resample, resize, shift, sharpen or recolour the base between frames;
- keep animation effects clean, smooth and stylistically matched to the V5
  source rather than using crude geometric marks;
- keep palette, apparent scale, alpha edge quality and outline weight stable;
- preserve the declared transparent gutter in every cell and every frame.

Add a deterministic unchanged-pixel test comparing every animated frame with
its standard base outside the declared mask. Also verify that counterpart units
use the same countertop geometry and colour values—not merely something that
looks approximately similar.

## Review requirements

Build a new immutable V6 review set and show:

- V5 and new V6 side by side for every asset and state;
- the complete counter run, not only isolated objects;
- two adjacent ordinary units with seam guides;
- countertop-height, front-edge and rear-edge guides across the entire run;
- frame stepping and looping for every animation;
- a difference/ghost overlay that reveals any base-object movement;
- exact logical game scale as well as large inspection scale;
- the same Keeper reference beside every major asset without resizing him;
- the nine-bay room and the modular 6–12-bay room shells;
- original and candidate SHA-256 values;
- explicit confirmation that V5, runtime art, Final art and approved Keeper
  animation files are unchanged.

Preload and decode every unique frame before enabling playback. Archive review
media through the repository's content-addressed review archive. Do not place
committed review binaries directly under `public/keeper-review`.

## Deterministic verification

At minimum test:

- exact cell and strip/sidecar geometry;
- transparent safety gutters and no shared-edge alpha;
- stable anchors, contact datums and interaction spots;
- vertical body sides and constant body width;
- one selected countertop construction across every compatible unit;
- equal front/rear top-edge lengths and no convergence;
- exact 19-lp counter/hob datum across the assembled run;
- identical stationary pixels across animation frames outside declared masks;
- stable palette and alpha bounds across frames;
- room assembly dimensions and whole-bay snapping;
- review manifest/object hashes and page preload behaviour;
- no changes to production, Final or approved Keeper assets.

Run the complete reviewer and sprite contract, update the relevant handoff and
decision documents, commit and push the finished review batch to remote
`main`, and deploy once using the repository's `[deploy]` workflow. Leave the
new V6 as an unapproved reversible draft and give Frank the production review
link. Do not promote or wire it into the game.

