# Kitchen Oven Ligne-Claire V7

Date: 21 October 2026  
Status: immutable reversible Oven On gate; not registered, promoted or current

## Correction

Frank rejected Kitchen Built-In State Ligne-Claire V6 after confirming that the
earlier high-resolution oven was the correct visual target. V6 did not carry
that drawing through: it created a new scripted approximation and then reduced
the approximation to the native canvas. Its geometry verifier passed because
canvas and alpha were preserved, but it did not verify visual-authority
identity. V6 is therefore rejected in full.

V7 preserves the exact preferred 1305 × 1206 RGBA oven as its primary visual
authority:

`art/source/kitchen-built-in-state-ligne-claire-2026-10-21-v7/oven-on-user-confirmed-visual-authority.png`

SHA-256:
`0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538`

No substitute redraw is allowed downstream. The recovered drawing is mapped to
the current Oven On authority's exact 92 × 85 canvas and its byte-exact alpha
channel. The contact sheet labels the rejected V6 substitute explicitly and
shows the corrected registered mapping beside it.

## Deliberately narrow gate

V7 contains only Oven On. It does not yet propagate the style to Broken,
lighting or flicker states, and it does not touch the dishwasher. This prevents
another state-family sweep from being built from an unverified base mapping.

The gate remains closed:

- `register: false`;
- `promote: false`;
- no selector changes;
- no production or runtime changes;
- anchors, pivots, collisions, movement, animation, interaction, repair,
  healing, timing and state transitions remain unchanged.

After explicit approval of this exact mapping, later state work must derive
from the hash-pinned visual authority rather than reinterpreting it.

## Review and verification

Review route:

`/keeper-review/kitchen-built-in-state-ligne-claire-v7/`

The page uses root-absolute same-origin URLs, preloads and decodes every image,
and shows the recovered authority before the comparison. This retains the
Vercel trailing-slash fix.

Verify with:

```bash
/usr/bin/python3 scripts/build_kitchen_builtin_state_ligne_claire_v7.py --verify
npm run maintain:keeper-review
```

Rollback is immediate: discard only the V7 source, draft, review set, builder
and this delivery record. Existing source, production, approved V3 and all
earlier immutable review packs remain untouched.
