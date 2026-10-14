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
- `public/keeper-review` contains HTML and small JSON only. It must not contain
  PNG, GIF, JPEG, WebP or AVIF review media.
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
`public/keeper-review`. Before committing the batch, run:

```sh
npm run archive:keeper-review
npm test
npm run typecheck
npm run build
```

The archive command is additive: it preserves old objects, stores new bytes
only once, updates manifests and removes deployable public copies. Do not hand
edit objects or hashes. Never reuse an existing review directory for a new
proposal.

## Deterministic safeguards

`npm test` verifies that:

- every manifest hash exists and matches its object's full filename;
- every legacy path appears in exactly one set and in the global index;
- immutable review-page bytes still match their archived page hash;
- no archived media remains physically under `public/keeper-review`;
- the real `public/` payload remains below 50 MiB;
- historical sprite/reviewer verifiers still read the exact archived bytes;
- known routes resolve and unknown archive paths fail closed.

After the movement-foundation review batch, 579 legacy paths resolve to the
same 246 unique objects. They represent 72.71 MiB of logical review media while
the unique store remains 44.71 MiB; `public/` is 43.04 MiB.
