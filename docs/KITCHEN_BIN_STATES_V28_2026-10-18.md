# Kitchen V28 bin state family and environmental effects

Date: 18 October 2026
Status: complete state/effect review draft; awaiting visual confirmation; unpromoted/unwired
Review: `/keeper-review/kitchen-bin-states-v28/`

V28 restarts the breakable kitchen-asset process one item at a time. It draws
the narrow turquoise pedal bin from scratch as one coordinated two-state
family: `standard` and `broken_overflowing`. The standard shell, scale,
centreline, orange pedal and floor contact are shared. The broken state changes
the lid and contents and adds a restrained rubbish spill extending into the
room. The bin object remains static. Its environmental impact is supplied by
two independent reusable overlays: a slow green miasma and slowly orbiting
flies. Each is a 24-frame loop at 4 fps, lasting six seconds, and is anchored to
the bin opening without changing the object sprite. The fly layer carries the
placeholder SFX cue `kitchen_bin_flies_slow_loop`.

The review shows both isolated sprites at 4× inspection scale and each state in
the exact 772 × 224 px V26 room. Each sprite occupies a 72 × 72 px transparent
interaction cell with a safety gutter and a common baseline. V27 is retained
unchanged as rejected provenance; it is not a visual or timing authority for
V28.

Generated source, first-pass source, prompts and SHA-256 pins live under
`art/source/kitchen-bin-states-2026-10-18-v28/`. Native review sprites and room
composites and reusable effect strips live under
`art/raw/kitchen-bin-states-2026-10-18-v28/`. The draft
catalogue and rollback register live under
`art/drafts/kitchen-bin-states-2026-10-18-v28/`.

## Verification and documentation audit

- Rebuild with the bundled Python runtime using
  `scripts/build_kitchen_bin_states_v28.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-bin-states-v28` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- Documentation audit completed on 18 October 2026. README, STATUS and
  DECISIONS now identify V27 as rejected provenance and V28 as the current
  static bin gate. No runtime, Final art or canonical kitchen asset is changed.
