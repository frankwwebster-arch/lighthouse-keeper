# Kitchen Oven Standalone V30

Date: 20 October 2026

Status: reversible visual-review draft; unapproved, unpromoted and unwired.

Review page: `/keeper-review/kitchen-oven-standalone-v30/`

## Requested corrections

V29 remains immutable. V30 makes two compositor-only corrections:

1. The dangling Broken-state rotary dial is a foreground object. V29 allowed the
   internal cavity light to recolour the dial's lower face and rim. V30 restores
   that exact silhouette from the unlit Broken authority after applying cavity
   illumination. The cavity continues to flicker behind it.
2. The small wall-coloured V-shaped gaps between the oven top and neighbouring
   cabinet worktops are filled with the already approved V22 countertop join
   pixels. The repair is a background underlay, not part of the oven or cabinet
   sprites.

## Dynamic join rule

- Oven body: `x=336..420`, `y=131..208` in the 772 × 224 room.
- Left cabinet body ends at `x=336`; right cabinet body begins at `x=420`.
- A 24 × 12 approved V22 countertop cap is centred behind each exact shared
  edge at `(324,134)` and `(408,134)`.
- Each side activates independently only when a compatible neighbour has an
  exactly snapped adjacent edge.
- Draw order is room background → active join underlays → cabinet neighbours →
  standalone oven.
- Moving or removing a neighbour removes only its corresponding underlay.
- The oven midpoint and Prime interaction anchor remain `(378,218)`.

This is the same architectural method as the approved sink repair: exact grid
occupancy selects the surface treatment, while the underlying assets remain
independent and immutable.

## Preserved invariants

- Off, On, Broken-dark and Broken-warning-lit state PNGs are byte-identical to
  V29.
- The corrected cavity-lit and both-lit states may differ from V29 only inside
  the declared dangling-dial foreground rows.
- Body `84 × 77`, cell `92 × 85`, four-pixel transparent safety gutter, room
  position, projection, hob, door, fixed shelf and Prime anchor are unchanged.
- The two deterministic 40-frame, 4-fps, ten-second irregular fault schedules
  are unchanged. The cavity and red lamp remain separately removable and
  variable-speed.
- Cabinet V11, the V22 join source, room background, Final art, runtime and
  later kitchen assets are unchanged.
- Smoke remains a separate reusable environmental layer.

## Verification

Run:

```sh
npm run verify:kitchen-oven-standalone-v30
npm run build
```

The V30 verifier rejects state changes outside the foreground-dial silhouette,
transparent-gutter violations, join pixels outside the two declared underlay
boxes, any loss of the cavity animation, authority hash drift, geometry or
Prime-anchor changes, missing review assets and missing content-addressed media.
