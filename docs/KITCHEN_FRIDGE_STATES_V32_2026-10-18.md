# Kitchen V32 coordinated fridge state family

Date: 18 October 2026
Status: rejected on detailed deployed-page review; unpromoted/unwired
Review: `/keeper-review/kitchen-fridge-states-v32/`

> Historical note: Frank initially approved V32 from the first visual proof,
> then withdrew that approval after inspecting the deployed page. The old
> fridge/grille remained beneath the replacement and the pool did not meet the
> room's actual floor surface. The later rejection record supersedes the
> approval record; V32 remains immutable provenance and V39 is its replacement.

V32 continues the approved V31 one-asset-at-a-time method with the fridge only.
It draws `standard` and `broken_hinge_failed` together from one coordinated
construction rather than attaching a fault to unrelated standard art. The
standard state is a bright-white enamel undercounter fridge aligned to the
approved V23/V31 21-lp fitted bay, continuous sea-glass worktop and 52-lp foot
line.

The broken top hinge has failed. The same door remains visibly attached to the
lower-right hinge, falls anticlockwise toward the left, and rests its lower-left
corner directly on the floor/puddle contact band. The open cavity includes
sparse unlabelled milk, jar and produce silhouettes so it does not read as
empty. The door and shallow leaked-water pool remain static object pixels.

Only a separate reusable environmental layer moves. It contains a slow falling
drip from the lower door/hinge edge and a restrained pool ripple in a 40-frame,
4-fps, ten-second strip. Every frame has a transparent safety gutter. The
broken state carries the sound-only placeholder
`kitchen_fridge_low_electrical_buzz_loop`; the water layer also names
`kitchen_fridge_water_drip_slow`. There is no smoke, spark, electrical flash or
other visible electrical effect.

The review shows the current V21/V23 fridge beside the new V32 standard state,
both new states isolated at 4× inspection scale, both states in the complete
772 × 224-pixel kitchen at exact game size, and the independent drip/ripple
loop. All unique state/effect URLs preload and decode before playback and sound
controls unlock.

The reversible source lineage lives under
`art/source/kitchen-fridge-states-2026-10-18-v32/`: V1 is the initial family,
V2 adds only generic contents, and selected V3 corrects literal door-floor
contact. Native outputs live under
`art/raw/kitchen-fridge-states-2026-10-18-v32/`; hashes, construction facts and
rollback instructions live under
`art/drafts/kitchen-fridge-states-2026-10-18-v32/`. The deterministic build and
gate are `scripts/build_kitchen_fridge_states_v32.py` and
`scripts/verify_kitchen_fridge_states_v32.mjs`.

## Superseded approval and sequence boundary

V32 changes no Kitchen V20–V31 source, runtime sprite, Final art or gameplay
wiring. Frank initially called the fridge excellent on 18 October 2026, but
later deployed-page inspection exposed the compositing and floor-placement
faults above. `docs/review/kitchen-v32-v38-rejection-2026-10-18.json`
supersedes that approval without deleting its historical record.

## Verification and documentation audit

- Rebuild with the bundled Python runtime using
  `scripts/build_kitchen_fridge_states_v32.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-fridge-states-v32` and
  `npm run verify:review-archive`.
- Full verification: `npm test`, `npm run typecheck` and `npm run build`.
- Documentation audit completed on 18 October 2026 against the source lineage,
  native geometry, review page, catalogue, rollback register, archive policy,
  runtime/Final boundary and fridge-first sequence. README, STATUS and
  DECISIONS record V32's later visual approval and the released asset sequence.
