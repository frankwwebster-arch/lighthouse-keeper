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
  permanent redirects to the declared external object URL.
- `public/keeper-review` contains HTML and small JSON only. It must not contain
  PNG, GIF, JPEG, WebP or AVIF review media.
- `public/sprites` is deliberately not archived because the running game reads
  it directly.

The initial external host is jsDelivr over the public GitHub repository. The
object filename is the complete SHA-256, redirects are cached for one year and
the host can be replaced through regenerated manifests without changing the
evidence bytes.

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

At migration, 550 legacy paths became 246 unique objects. The old review media
represented 70.27 MiB per deployment; `public/` is now 43.01 MiB.
