# Kitchen V29 quieter bin effects

Date: 18 October 2026  
Status: complete effect review draft; awaiting visual confirmation; unpromoted/unwired  
Review: `/keeper-review/kitchen-bin-effects-v29/`

V29 preserves all approved V28 bin artwork byte-for-byte. The standard bin,
overflowing bin, standard room proof and broken room proof retain their exact
V28 SHA-256 values. Only the two separate reusable environmental layers change.

The greenish stench is now built from restrained, translucent, irregular
vapour ribbons rather than rounded cloud puffs. It remains visibly connected
to the bin opening in every frame. The three flies use slow shallow paths and
muted wings. Both layers are 40-frame strips at 4 fps, so the full loop lasts
10 seconds before repeating. The bin object itself has no animated pixels.
The fly layer retains the placeholder SFX cue
`kitchen_bin_flies_slow_loop`.

Native review outputs live under
`art/raw/kitchen-bin-effects-2026-10-18-v29/`. The reversible catalogue and
rollback register live under
`art/drafts/kitchen-bin-effects-2026-10-18-v29/`. The deterministic visual
recipe is recorded in
`art/source/kitchen-bin-effects-2026-10-18-v29/DESIGN.md` and
`scripts/build_kitchen_bin_effects_v29.py`.

## Verification and documentation audit

- Rebuild with the bundled Python runtime using
  `scripts/build_kitchen_bin_effects_v29.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-bin-effects-v29` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- Documentation audit completed on 18 October 2026. README, STATUS and
  DECISIONS distinguish approved V28 object pixels from the V29-only effect
  revision. Runtime, Final art and canonical V20–V28 assets remain unchanged.
