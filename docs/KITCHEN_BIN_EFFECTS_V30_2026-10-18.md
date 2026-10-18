# Kitchen V30 taller bin stench cloud

Date: 18 October 2026  
Status: complete effect review draft; awaiting visual confirmation; unpromoted/unwired  
Review: `/keeper-review/kitchen-bin-effects-v30/`

V30 responds to the V29 miasma being too subtle. It preserves the approved V28
bin and room PNGs, the V29 fly strip, the V29 miasma colour palette, and the
40-frame/4-fps ten-second timing exactly. Only the miasma silhouette changes.

The replacement is one continuous, overlapping translucent cloud rather than
separate cartoon puffs. It rises to y=3 in its 80 × 80 px cell, compared with
y=18–22 in V29, and uses roughly four times the opaque pixel area. Broken
edges, negative holes and slow five-frame shape changes keep it atmospheric.
Its narrow throat remains connected to the overflowing bin opening in every
frame. The bin object itself does not animate.

Native review outputs live under
`art/raw/kitchen-bin-effects-2026-10-18-v30/`. The reversible catalogue and
rollback register live under
`art/drafts/kitchen-bin-effects-2026-10-18-v30/`. The deterministic visual
recipe is recorded in
`art/source/kitchen-bin-effects-2026-10-18-v30/DESIGN.md` and
`scripts/build_kitchen_bin_effects_v30.py`.

## Verification and documentation audit

- Rebuild with the bundled Python runtime using
  `scripts/build_kitchen_bin_effects_v30.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-bin-effects-v30` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- Documentation audit completed on 18 October 2026. README, STATUS and
  DECISIONS identify V30 as a one-change miasma successor. Runtime, Final art
  and canonical V20–V29 assets remain unchanged.
