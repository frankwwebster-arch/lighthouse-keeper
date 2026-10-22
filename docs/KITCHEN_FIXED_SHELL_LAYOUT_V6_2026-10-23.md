# Kitchen Fixed Shell Layout V6

Date: 23 October 2026

Status: unapproved room-fit review; no runtime or production promotion

Review route: `/keeper-review/kitchen-fixed-shell-layout-v6`

## Why this version exists

V1–V5 repeatedly moved complete appliance pictures. Each picture carried its own worktop end, side cabinet and plinth, so even attractive source renders produced incompatible joins when rearranged. V6 removes that failure mode instead of asking the image model for another redraw.

The visible insert art is derived mechanically from the approved coordinated cabinetry sheet and approved state sheet. Those authorities and the first fitted-run style exemplar remain byte-identical.

## Fixed fitted-kitchen architecture

- One continuous worktop spans room x `84–588` and has outer caps only.
- One continuous plinth owns the y `208` cabinet baseline.
- One fixed carcass declares six identical `84 × 74 px` apertures at x `84, 168, 252, 336, 420, 504`.
- The exact bay centres remain `126, 210, 294, 378, 462, 546`.
- Unit source worktops, source outer side panels and source plinths are excluded from the movable layers.
- Fronts, doors, contents, indicators and leaks move inside the apertures.
- The sink basin/tap is a separately registered cut-in above the fixed top.
- The oven hob is a separately registered overlay above the fixed top and moves with the oven insert.
- No healing artwork is present.

The kettle and toaster retain the V2 grid contract: they belong to distinct cupboard/drawers identities, sit at the exact centre of those worktops and travel when the owning insert moves. Floor objects retain distinct room-section identifiers. Broken fitted units remain locked until repaired.

## State coverage

The review exposes Sink Off/On/Broken, Dishwasher Off/On/Broken, Oven Off/On/Broken and Fridge Standard/Broken. Dishwasher Off is a deterministic dark-lamp derivative of the approved On panel: all three lamp centres remain invariant, and only their fill changes. The Broken dishwasher keeps its flopped-open door and contents; the Broken oven remains ajar with burnt food; the Broken fridge retains the selected hanging door and subtle contents; approved water layers remain attached to their source insert.

## Delivery

The page preloads and decodes one lossless content-addressed atlas before enabling controls. Direct `1×`, `2×` and `4×` canvas rendering uses the same master pixels. The manifest declares the fixed/movable ownership split and pins every approved authority hash.

Build and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_fixed_shell_layout_v6.py
npm run maintain:keeper-review
node scripts/verify_kitchen_fixed_shell_layout_v6.mjs
npm test
```

## Draft-retirement start

The unapproved, unregistered Kitchen Complete Review V43 working-tree pack was the first safe retirement target: it had no external build/document references, while its immutable public review route and content-addressed review evidence remain. Its 116-file, 9.7 MiB source tree is recoverable from git commit `a8f58be9d896bf4cef9d26463dd856d18a254469`; the pre-retirement sorted file/hash-list digest is `aa034787dd3cbd9e1abed1ce0daf6424e43e8ce85f6e1a71ffe782a23d41540b`.

No approved authority, currently used builder input, review decision, public immutable page or content-addressed evidence was deleted. Later cleanup should use the same reference audit and recovery record rather than bulk-deleting kitchen history.

## Boundary

V6 is a reversible review candidate. It does not modify approved Kettle V47, runtime state behavior, vibration/SFX contracts, production sprites or game selectors. Frank still approves or rejects the assembled room.
