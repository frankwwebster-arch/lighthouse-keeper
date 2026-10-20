# Activity Cloud Composer V7 — generic action symbols

**Status:** immutable, reversible visual-review candidate; not approved or promoted

**Review route:** `/keeper-review/activity-cloud-composer-v7/`

## Outcome

V7 extends the reusable activity-callout vocabulary with seven independent comic marks:

| Component | Family | Intended read |
| --- | --- | --- |
| `symbol-heat-shimmer` | heat | radiant heat distinct from smoke |
| `symbol-pleasant-aroma` | scent | appetising or comforting aroma |
| `symbol-foul-odour` | scent | unpleasant smell without gross imagery |
| `symbol-electrical-arc` | electrical | live power, shock or electrical work |
| `symbol-welding-sparks` | welding | hot-metal contact or welding activity |
| `symbol-exclamation-mark` | notation | surprise, urgency or completion emphasis |
| `symbol-question-mark` | notation | uncertainty, investigation or puzzlement |

These are vocabulary only. V7 does not insert them into Prime Rear Action Choreography V2, change a recipe, claim body compatibility or attach sound.

## Immutable boundary

V7 inherits Composer V6 byte-for-byte:

- all 149 component records and hashes;
- all 15 suggested recipes and the default recipe;
- the complete Prime rear-work body and route;
- review references, notation accents and composer behaviour, except the versioned local-storage key.

The seven additions are new files in a new source set. Composer V6, choreography V1/V2, Final, runtime and Kitchen are not edited.

## Source ownership and rejection record

Six marks share a 1536 × 1024 RGBA source arranged as a strict 3 × 2 grid. Each 512-pixel cell has one declared owner. The accepted source has:

- zero visible pixels on outer or shared ownership lines;
- minimum per-cell source gutters of 99, 97, 93, 111, 115 and 111 pixels;
- zero ambiguous and zero unowned visible pixels.

The first otherwise usable sheet was rejected because several cells left only 41–77 pixels of source gutter, below the binding 80-pixel minimum. Its exact bytes remain under the V7 draft's `rejected/` directory. The question mark uses a separate one-owner RGBA source.

The deterministic builder crops by alpha-greater-than-eight bounds, scales uniformly and centres each owner in a fresh 256 × 256 transparent cell. Every output has at least 20 pixels of transparent gutter, clear outer edges and a pinned SHA-256 value. No builder step repaints, merges or invents pixels.

## Delivery and rollback

The seven review images are content-addressed under `review-archive/objects`; the public review directory contains only HTML and JSON. The page retains preload/decode locking, token inspection, 4–5-element selection, both callout treatments, layer controls and import/export from Composer V6.

Rejecting V7 requires deleting only:

- `art/drafts/activity-cloud-composer-2026-10-20-v7/`;
- `public/keeper-review/activity-cloud-composer-v7/`;
- `review-archive/sets/activity-cloud-composer-v7.json` and its seven V7-only object mappings/files;
- the V7 builder, verifier and documentation references.

Composer V6 remains intact.

## Verification

```bash
npm run verify:activity-cloud-composer-v7
npm run verify:activity-cloud-composer-v6
npm run verify:activity-callout-authoring-standard
npm run typecheck
npm run build
```

The V7 verifier checks parent-byte inheritance, exact component names/families, source geometry, shared-boundary alpha, 80-pixel source gutters, one-owner metadata, 20-pixel output gutters, content hashes, archive mappings, page script syntax, preload/decode declarations and the no-runtime/no-Kitchen/no-deploy boundary.
