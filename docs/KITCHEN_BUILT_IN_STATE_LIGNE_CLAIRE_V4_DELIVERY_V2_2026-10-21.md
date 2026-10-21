# Kitchen Built-In State Ligne-Claire V4 Delivery V2

Date: 21 October 2026

Review: `/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v2/`

Status: deployed delivery correction for the unchanged immutable V4 evidence;
not approved, registered, promoted, wired or current.

## Fault and correction

The original V4 page requested its archived images through routes that returned
HTTP 307 redirects to `raw.githubusercontent.com`. The image bytes were present
and correct, but the review surface did not display that cross-origin redirect.

Delivery V2 uses a fresh page and asset prefix. Its four evidence paths are
served from the Lighthouse Keeper origin. The server fetches each declared
content-addressed archive object, checks its byte length and SHA-256, then
returns the verified bytes with the correct image content type. A corrupt or
unavailable object fails closed with HTTP 502 rather than displaying unverified
evidence.

The page waits for all four images to decode before showing its ready state and
displays an explicit failure message if decoding fails.

## Immutability

The original V4 page remains byte-for-byte unchanged at SHA-256
`27732340d908aa60e094dae5444ebde2b2eee88f53e1f0b94b5393acd929fcae`.
Delivery V2 reuses the four original content-addressed evidence objects exactly;
it adds no image object and changes no candidate, source, production or runtime
pixel.

The sink remains fixed at its verified room datum `(slot x - 4, 104)`. All
dimensions, alpha, anchors, pivots, collisions, movement locks, repair unlocks,
effect ownership, animation timing and 720-layout healing rules remain those of
V4 and its pinned authorities.

## Verification

```sh
npm run verify:kitchen-built-in-state-ligne-claire-v4-delivery-v2
npm run verify:kitchen-built-in-state-ligne-claire-v4
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

After deployment, the page and each same-origin evidence route must return HTTP
200 without a `Location` header. The returned `X-Review-Archive-Sha256` header
and downloaded SHA-256 must equal the immutable archive declaration.

## Rollback

Rollback is immediate: remove only the Delivery V2 page, its four duplicate
archive path mappings, the targeted same-origin route allow-list entry and this
document. The original V4 pack, page, archive set and every game asset remain
untouched.
