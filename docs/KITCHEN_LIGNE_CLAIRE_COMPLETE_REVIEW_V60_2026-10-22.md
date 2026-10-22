# Kitchen Ligne-Claire Complete Review V60 — 22 October 2026

V60 is the active, closed kitchen review candidate at `/keeper-review/kitchen`.
It inherits the complete V59 fitted-carcase correction and changes only the
live-room presentation scale and registration of approved Kettle V47.

## Kettle scale decision

- The kettle remains a countertop accessory anchored to Cabinet A. It is not a
  seventh independently movable kitchen object.
- Frank considered independent movement unnecessary and requested a reduction
  of approximately 20% instead.
- Off and On now render at `46 × 41` native room pixels, compared with
  `56 × 51` in V59. Broken renders at `50 × 47`, compared with `62 × 59`.
- Every state remains centred at x `42` within its supporting 84-pixel bay and
  touches the same support plane at room y `141`.
- Integer destination coordinates avoid adding half-pixel blur at native scale.

The approved V47 PNGs are byte-identical. Only canvas draw rectangles changed.
The smaller presentation therefore does not replace, redraw or resample any
canonical source asset.

## Layer and behaviour preservation

The detached Broken lid keeps its separate hover/vibration transform and uses a
proportionally re-registered pivot. On and Broken steam remain independent,
non-tremoring environmental layers re-registered above the smaller kettle. The
approved motion amplitudes/timing, Off/Subtle/Emphatic modes, independent SFX
toggle, drop-in placeholder replacement and immediate repair stop are unchanged.

The kettle's support relationship, Broken support lock, state transitions and
tea interaction contract are also unchanged. V59 dishwasher/oven/cabinet pixels,
fitted joins and rear-line repair remain byte-identical.

## Approval boundary and rollback

V47 art and its V46 motion/SFX behaviour remain approved. V60's smaller
live-room registration and the inherited V59 fitted-carcase integration remain
unapproved. No production/current selector, runtime, gameplay, collision or
save-state implementation changed. Registration and promotion remain closed.

Reject V60 by discarding only its draft pack, review shell and archive set; V59
and every approved source remain available unchanged.

## Verification

`/usr/bin/python3 scripts/build_kitchen_ligne_claire_complete_review_v60.py --verify`
checks the closed gate, exact source hashes, 18-sheet/142-route archive coverage,
integer-centred draw rectangles, common y141 support plane, detached-lid pivot,
independent steam registration and root-absolute content-addressed delivery.
