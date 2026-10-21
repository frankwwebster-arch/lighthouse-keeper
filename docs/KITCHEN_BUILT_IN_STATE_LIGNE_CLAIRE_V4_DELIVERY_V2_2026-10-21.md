# Kitchen Built-In State Ligne-Claire V4 Delivery V2

Date: 21 October 2026

Review: `/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v2/`

Status: failed delivery preserved as immutable provenance; superseded by
Delivery V3. It was never approved, registered, promoted, wired or current.

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
displays an explicit failure message if decoding fails. Its relative
`assets/...` URLs resolve incorrectly after Vercel removes the page's trailing
slash, so the live Chromium render correctly displayed the failure state. The
page remains unchanged; Delivery V3 fixes this with root-absolute URLs.

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

Direct requests to each same-origin evidence route returned HTTP 200 without a
`Location` header, and every returned `X-Review-Archive-Sha256` and downloaded
SHA-256 matched the immutable archive declaration. That transport-only check
was insufficient: the required Chromium render then exposed the incorrect
relative URL resolution and displayed the page's explicit failure state.

## Rollback

Delivery V2 is now immutable failed-delivery provenance and is not removed or
rewritten during Delivery V3 rollback. It never changed the original V4 pack,
page, archive set or any game asset.
