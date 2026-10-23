# Kitchen Fixed Shell Layout V9

Date: 23 October 2026

Status: unapproved complete-front and perspective review; no runtime promotion

Review route: `/keeper-review/kitchen-fixed-shell-layout-v9`

## Correction

V8's shared worktop was correct, but its cupboard and drawer masks began too
low. The exposed backing between the worktop and their first functional panel
looked like a blue fascia and cropped the top of the top drawer/door outline.

V9 removes that region completely. It does not recolour it or insert another
rail. For the standard cupboard and drawers, the complete approved functional
front is shifted `10` master pixels upward. Its upper outline begins at body
row `50`, exactly where the shared worktop ends. Row `49` remains empty and row
`50` is verified opaque across more than 400 of the 420 master pixels.

The two exposed run ends now use `34`-master-pixel tapered side planes with
visible top and plinth recession. The planes stay within the fixed run; no bay,
front, object centre or Keeper anchor moves.

## Retained contract

- Fitted bodies: exactly `84 × 74 px`.
- Origins: `84, 168, 252, 336, 420, 504`.
- Centres: `126, 210, 294, 378, 462, 546`.
- Worktop support: `y=141`.
- Cabinet floor support: `y=208`.
- Keeper stop/turn plane: `y=218`.
- Sink: V8 geometry mask; no source countertop pixels.
- Internal joins: one narrow ink seam, no blue divider fill.
- Kettle/toaster ownership, broken locks and appliance states: unchanged.
- Healing layer: absent.

## Rebuild and verification

```sh
/usr/bin/python3 scripts/build_kitchen_fixed_shell_layout_v9.py
npm run maintain:keeper-review
node scripts/verify_kitchen_fixed_shell_layout_v9.mjs
npm test
```

The V9 verifier directly checks the transparent row above each standard front,
the fully occupied first front row beneath the worktop, the widened/tapered end
planes, all approved authority hashes, exact grid/state contracts, one archived
atlas, review JavaScript and same-origin delivery route.

## Boundary

V9 remains reversible review evidence. It changes no approved source, runtime
asset, game selector, state behaviour, Kettle V47 motion/audio contract or
deployment architecture. V6–V8 remain immutable comparison evidence. Frank
still approves or rejects the assembled room.
