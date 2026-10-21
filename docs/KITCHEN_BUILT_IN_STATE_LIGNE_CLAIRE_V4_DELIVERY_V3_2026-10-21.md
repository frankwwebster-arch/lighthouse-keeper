# Kitchen Built-In State Ligne-Claire V4 Delivery V3

Date: 21 October 2026

Review: `/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v3/`

Status: corrected delivery for the unchanged immutable V4 evidence; not
approved, registered, promoted, wired or current.

## Faults and correction

The original V4 page used archive routes which redirected image requests to an
external host that the review surface did not display. Delivery V2 added
same-origin, length- and SHA-256-verified media responses, but retained relative
`assets/...` URLs. Vercel canonicalizes the page URL by removing its trailing
slash, causing those relative URLs to resolve outside the review set. A live
Chromium render caught the resulting broken images.

Delivery V3 uses a new immutable page and asset prefix. Every image and link has
a root-absolute path under
`/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v3/assets/`.
The same-origin server route fetches the declared content-addressed object,
checks byte length and SHA-256, and returns the verified bytes with the correct
content type. The page waits for all four images to decode before showing
`STATIC EVIDENCE READY · 4/4 VERIFIED`.

## Immutability

The original V4 page remains unchanged at SHA-256
`27732340d908aa60e094dae5444ebde2b2eee88f53e1f0b94b5393acd929fcae`.
Failed Delivery V2 remains unchanged at SHA-256
`a484fc99ad9b6a1dfa71708471cef21424ffed6eab4ba7d61bf723a8798b6de9`.
Delivery V3 reuses the four original V4 evidence objects exactly. It adds no
image object and changes no candidate, source, production or runtime pixel.

The sink remains fixed at `(slot x - 4, 104)`. Dimensions, alpha, anchors,
pivots, collisions, movement locks, repair unlocks, effect ownership, animation
timing and 720-layout healing remain unchanged.

## Verification

```sh
npm run verify:kitchen-built-in-state-ligne-claire-v4-delivery-v3
npm run verify:kitchen-built-in-state-ligne-claire-v4
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The deployed page must be rendered in Chromium. A successful render displays
the green `STATIC EVIDENCE READY · 4/4 VERIFIED` badge and visible sheets. Each
image route must return HTTP 200 without a `Location` header; its downloaded
SHA-256 and `X-Review-Archive-Sha256` header must equal the archive declaration.

## Rollback

Remove only the Delivery V3 page, its duplicate archive path mappings, its
same-origin allow-list entry and this document. Original V4, failed Delivery V2,
all artwork and every game/runtime asset remain untouched.
