# Codex → Claude: Kitchen V9 fridge and shelf review hand-back

Date: 17 October 2026  
Status: reversible review draft; unapproved and unwired

## Frank's request and V9 response

Frank accepted the wider V8 kitchen direction, then asked for two bounded
changes: restore dimensional detail to the bright-white fridge, and add a
plant/pots shelf above it which travels with that low furniture element.

V9 responds only to those points. The fridge keeps its approved 21-lp bay,
21-lp cell, 284-ku interaction spot and 52-lp room foot line. Its wooden top
does not return; instead, a layered white enamel lid and a richer inset casing
restore volume. The shelf is a new transparent wall child owned by the fridge,
not room decoration baked into the shell.

## Measured hand-back

| Item | Cell | Opaque bound | Bays | Interaction / ownership |
|---|---:|---:|---:|---|
| dimensional white fridge | 21 × 21 lp | 19.5 × 20.5 lp | 1 | 284 ku; foot line 52 lp |
| plant-and-pots shelf | 21 × 56 lp | 19 × 17 lp | 1 | child of fridge; z26; identical x delta |

The shelf bound begins at `(1,13.5) lp` and ends at `y=30.5 lp`. The fridge
begins at room `y=31 lp`; the layers therefore remain separated. Movement
proofs place the pair in bays 2, 5 and 8 with exact 63-lp jumps.

## Files to continue from

- Machine recipe: `data/kitchen_fridge_shelf_v9_recipe.json`
- Human recipe: `docs/KITCHEN_FRIDGE_SHELF_V9_RECIPE_2026-10-17.md`
- Builder: `scripts/build_kitchen_fridge_shelf_v9.py`
- Verifier: `scripts/verify_kitchen_fridge_shelf_v9.mjs`
- Catalogue and register:
  `art/drafts/kitchen-fridge-shelf-2026-10-17-v9/`
- Source study and exact prompt:
  `art/source/kitchen-fridge-shelf-2026-10-17-v9/`
- Immutable review route: `/keeper-review/kitchen-fridge-shelf-v9/`

## Protection boundary

Do not approve, promote or wire this set from the hand-back. Do not overwrite
V8. If Frank requests another correction, create a fresh versioned review set.
Keeper animations, production sprites, Final art and live manifests have not
changed.

## Verification record

- Deterministic raw/draft/source digest, identical across two rebuilds:
  `0caf31130c39a82ee791627f2031e86e003550d07f0bb04f843cedaad38ed757`.
- Review-page SHA-256, identical across two rebuilds:
  `6bce2143c00ca16828a0f206ff85ed05523009a0fa63f61878f97579704ece36`.
- `node scripts/verify_kitchen_fridge_shelf_v9.mjs`: passed.
- `npm test`: passed, including all Kitchen V1–V9 verifiers and 179 Vitest
  tests across 18 files.
- `npm run build`: passed.
- `npm run typecheck`: passed.
- Content-addressed review archive: 37 V9 review references; the whole archive
  now contains 78 sets, 2,359 references and 1,073 immutable objects. No V9
  review binary remains under `public/keeper-review`.
- Documentation audit: README, decisions, machine recipe, human recipe and this
  hand-back agree on the unchanged 21-lp fridge cell, 52-lp foot line,
  counterless dimensional white-enamel construction, exact 19 × 17-lp shelf
  bound and fridge-child translation rule. No runtime or approval claim changed.
