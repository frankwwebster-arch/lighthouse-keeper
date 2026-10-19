# Activity Cloud Composer V5 — household, leisure and repair vocabulary

Date: 19 October 2026

Status: immutable, reversible review candidate; not approved or promoted; review page publicly reachable after an unrelated concurrent deployment

## Outcome

V5 preserves Composer V4's 86 selectable components, six deterministic musical-notation accents, Prime rear-work body, full approved walk → stop → turn → rear-work → rear-neutral route, default recipe and timing contract exactly. It adds 60 independently selectable callout elements across eggs, toast, bathroom, rest, reading, pottery, writing, pet care, fishing, exercise, tabletop games and repair.

The review tool is at `/keeper-review/activity-cloud-composer-v5/index.html`. It still supports arbitrary four- or five-element packages attached to a labelled household asset, plus local save and JSON import/export. Fifteen suggested packages provide editable starting points; loading one never changes the underlying components.

## New activity coverage

- collecting eggs and making toast;
- discreet, family-safe loo and bath callouts;
- armchair naps and adventure reading (book, pirate ship, dragon, treasure chest and castle);
- pottery wheel, moulding hands, wet clay and finished vase;
- writing and stationery;
- pet feeding and affection cues;
- fishing;
- exercise;
- playing cards and board games;
- boat-hull repair, outboard work, petrol filling, tyre pumping, tool work, varnishing and battery leads.

Loo, bath, nap, reading, fishing, exercise and tabletop games are marked `dedicated-pose-required`. Their callout vocabulary can be reviewed and packaged now, but the generic standing rear-work body is automatically withheld. This avoids implying that V5 has approved body choreography for those activities.

## Separation and reversibility

- No callout object, household context, prop or icon is baked into the Keeper.
- Body, component package, notation layer and SFX cue remain independently switchable metadata/layers.
- V5 lives only in `art/drafts/activity-cloud-composer-2026-10-19-v5/`, `public/keeper-review/activity-cloud-composer-v5/` and its content-addressed review objects.
- Rejecting V5 requires deleting only those V5 paths and archive references. V1–V4 and every Prime authority remain byte-identical.
- No Kitchen file, runtime asset, Final asset or production route is changed.

## Deterministic ownership gate

The ten accepted 1536×1024 source sheets use an exact 3×2 ownership grid. The builder rejects visible alpha above the project threshold on outer edges or at x=512, x=1024 or y=512. Every declared crop is then isolated into a fresh 256×256 transparent cell and must pass:

- one owner;
- zero ambiguous pixels;
- zero unowned visible pixels;
- zero shared-edge alpha;
- at least 16 transparent pixels between visible content and every cell edge;
- exact SHA-256 agreement among draft component, catalogue record, public review reference and archive object.

Run:

```bash
npm run verify:activity-cloud-composer-v5
```

The generation method, exact accepted prompts and source mapping are in `art/drafts/activity-cloud-composer-2026-10-19-v5/PROMPT_LOG.md`. The complete hash and ownership register is `art/drafts/activity-cloud-composer-2026-10-19-v5/batch-register.json`.

## Approval boundary

V5 asks only whether this broader component vocabulary and composer workflow are useful. It does not approve a suggested recipe, dedicated body pose, runtime wiring, Kitchen amendment or sound effect.

No deployment was initiated for V5. After V5 commit `a4c179c7` reached `main`, the concurrent Kitchen V27 work created deployment commit `19cc2a7f`, which included V5 as an ancestor and therefore made the review page publicly reachable. This incidental publication did not promote V5, change Final/runtime assets or authorise any V5 content for the game.
