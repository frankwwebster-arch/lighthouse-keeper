# Kitchen Proof V3

Status: **review-only candidate; awaiting Frank.** Nothing in this directory is
canon or runtime art, and the builder does not write outside this versioned
review folder.

This package implements the reissued 26 October V3 kitchen brief at the Prime
Keeper's native scale:

- module `1536 × 576`; world scale `168 px/m`; 14 bays of `84 px`;
- approved Prime cells copied byte-for-byte and composited at `1:1`;
- opaque sole datum `y=316` placed on room `walkY=502`;
- front-on elevation with only the `1/4` top-depth reveal;
- separately assembled fitted kit, slot-in cooker, inserts and loose items;
- exact `#FF00FF` window glass with no near-magenta pixels;
- current 38/38 route proof and D15 42/42 root-motion draft;
- isolation proof for a sink-tap-only amendment.

## Review

Open `review.html` in this directory. Principal outputs are in `outputs/`;
individual engine-facing parts and `item.json` are in `parts/`.

`TECHNICAL_REPORT.md` is the concise technical handoff. `manifest.json` pins
the sources, generated evidence, geometry, test results and known boundary.

## Rebuild and verify

Use the workspace's bundled Pillow runtime:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-proof-v3/build_review.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-proof-v3/verify_review.py
```

The builder retrieves the byte-identical V7 authority from Git commit
`52e94f2a`, verifies SHA-256
`0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538`,
copies the existing Prime sources, and generates the package deterministically.
It does not generate or alter Keeper art.

## Approval boundary

D15's root schedule lands at all four requested centres exactly, but the first
two legs are not animation-complete. Those even-step legs require an approved
F5-to-neutral opposite-foot stop bridge that does not exist in the current
Prime bank. The draft therefore uses the existing F1 bridge pixels as visibly
labelled pose placeholders. They are not approval candidates and must not be
installed in runtime art.

## Documentation audit

The repository authority documents were checked against this package. No
existing document was changed: this is a review-only proof under a task brief
that explicitly supersedes prior geometry for this review. All divergent
geometry and the unresolved D15 phase boundary are recorded in this folder.
