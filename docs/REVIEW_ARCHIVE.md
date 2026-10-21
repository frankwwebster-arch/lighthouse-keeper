# Keeper review archive

The Keeper's review pages keep their historical URLs and immutable HTML, while
their heavy images and GIFs are stored once by SHA-256 outside the Vercel
deployment payload.

## Current contract

- `review-archive/objects/<first-two-hash-characters>/<sha256>.<ext>` contains
  each unique review object exactly once.
- `review-archive/sets/<review-set>.json` maps each historical public path to
  its immutable object.
- `review-archive/index.json` is the production redirect index and records the
  measured counts and byte savings.
- `/keeper-review/<set>/assets/<name>` and `/keeper-review/drafts/<name>` return
  short-lived temporary redirects to the declared external object URL. The
  route stays replaceable if the external host changes.
- `public/keeper-review` contains HTML, JavaScript and JSON smaller than 24 KiB.
  PNG, GIF, JPEG, WebP and AVIF review media is always archived; JSON and
  JSON.GZ at or above 24 KiB is archived as review data. Historical URLs for
  both media and data resolve through the archive routes.
- The one larger public exception is
  `activity-cloud-composer-v6/catalogue.json`. Its exact SHA-256 is pinned by
  the maintenance scripts because immutable approval verifiers read that
  shared contract directly and pin their own bytes.
- `public/sprites` is deliberately not archived because the running game reads
  it directly.

The external host is GitHub's raw-content endpoint over the public repository.
The object filename is the complete SHA-256. Do not use jsDelivr for this
archive: it refuses uncached objects when the repository package exceeds
50 MB. Animation review pages must preload and decode all moving-frame URLs
before playback, so the redirect/download hop can never appear as a blank or
stale animation frame.

## Normal authoring workflow

Review builders can continue assembling a new versioned page under
`public/keeper-review`. Before committing the batch, run the maintenance gate:

```sh
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The maintenance command runs the archive sweep and then the verifier. The
archive is additive: it preserves old objects, stores new bytes only once,
updates manifests, proves the object and both manifest entries match, and only
then removes the deployable public copy. It ignores unrelated untracked archive
objects, so one task cannot absorb another task's draft evidence. Repeating the
command with unchanged inputs is byte-for-byte idempotent. Do not hand edit
objects or hashes. Never reuse an existing review directory for a new proposal.

## Deterministic safeguards

`npm test` verifies that:

- every manifest hash exists and matches its object's full filename;
- every legacy path appears in exactly one set and in the global index;
- immutable review-page bytes still match their archived page hash;
- no archiveable media or oversized review data remains physically under
  `public/keeper-review`;
- every required literal review payload URL in retained HTML resolves either
  to a small public file or to an archived object (three optional V8-V10
  inventory hyperlinks remain intentionally unpublished because their version
  gates forbid duplicated inventory files);
- the real `public/` deployment payload remains below 50 MiB, with a diagnostic
  that lists the largest offenders and explicitly excludes repository size,
  `review-archive/` and `art/drafts/`;
- historical sprite/reviewer verifiers still read the exact archived bytes;
- known routes resolve and unknown archive paths fail closed.

As verified on 21 October 2026, 4,562 legacy paths across 189 sets resolve to
2,742 unique objects. They represent 339.19 MiB of logical review evidence;
the retained unique store is 188.61 MiB. The clean-checkout `public/` payload
is 44.9008 MiB: 5.0992 MiB below the unchanged 50 MiB guard. Runtime
`public/sprites` is 36.9977 MiB and remains deliberately untouched.
