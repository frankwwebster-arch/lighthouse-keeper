# Kitchen Countertop Join Cap V22 — 19 October 2026

## Purpose

V21 successfully concealed the pale wall between adjacent cabinet bodies, but
the two sprites' independent softened worktop end contours remained visible on
top of one another. At inspection scale they formed a wide jagged staircase.
V22 replaces that composite artefact without amending either source asset.

Review route: `/keeper-review/kitchen-countertop-join-cap-v22/`

## Layer order

1. room background;
2. dynamic cabinet-body backfill;
3. exact independently movable V11 and V19 sprites;
4. dynamic twelve-row countertop join cap; and
5. optional single soft angled seam.

The source room, approved V11 two-bay run, complete V19 sink and V21 comparison
room are copied byte-for-byte into the review set.

## Countertop cap

The cap covers world rows 134–145 only. Each row colour is derived
deterministically from clean, already-composited countertop pixels away from
the basin and away from the join on both exact sprites. At the default fit it
spans x=328–343, underlapping each logical cabinet body by eight pixels so the
two old end contours are completely covered.

The default treatment contains no seam and therefore restores uninterrupted
horizontal worktop bands. The alternate treatment adds one anti-aliased,
low-contrast down-right seam from the sink's rear projection to its front lip.
It does not expose the former pair of overlapping staircases.

## Semi-dynamic rule

The existing V21 body mask and the V22 cap use the same live neighbour gap.
They remain active from six pixels of overlap through eight pixels of
separation. Both switch off beyond that range rather than forming a floating
bridge between deliberately separated furniture.

## Review interaction

The page compares V21, V22 seamless and V22 soft-seam treatments at six times
native scale. Its native-room sandbox lets Frank drag the sink, enter exact X,
switch treatment, vary the maximum small-gap threshold and show logical bounds.

## Boundaries

V22 is the approved review authority but remains reversible and unpromoted.
V11, V19, V20, V21, the room background, Final art and runtime remain
unchanged. The approval does not authorise runtime or Final promotion.

## Approval

Frank approved the exact seamless V22 treatment and the layered join method on
19 October 2026. The immutable decision record is
`docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json`.
Approval establishes the review authority and future modular-join method; it
does not promote artwork into Final or wire the treatment into runtime.
