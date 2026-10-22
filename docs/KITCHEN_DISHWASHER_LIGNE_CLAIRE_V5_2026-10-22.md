# Kitchen Dishwasher Ligne-Claire V5

Status: immutable review candidate; not approved, registered, promoted or wired.

Review: `/keeper-review/kitchen-dishwasher-ligne-claire-v5/index.html`

V4 is preserved and rejected. Its proportions improved, but its flat simplified
drawing remained profoundly different from the approved oven, and turquoise
rounded-cap pixels remained visible in the narrow shoulders beneath the shared
worktop overhang.

## Construction

- All 15 Off/On/Broken and join variants retain the exact V41 `98 × 82 px`
  canvas and alpha bytes.
- The approved oven is the primary visual authority for contour weight,
  dimensional warm enamel, blue structure, orange/copper hardware, highlights
  and material hierarchy.
- The three high-resolution state redraws are stored as versioned source
  references and deterministically reduced into the locked V41 envelope.
- The generated redraw contains no worktop. The complete approved Cabinet V3
  worktop is copied exactly through source row `16`, and both narrow shoulders
  below the overhang use exact approved cabinet carcass pixels through row `29`.
- Off changes only control indication. Broken retains the fixed frame/plinth,
  hangs the styled door forward inside the locked footprint and isolates a
  small loose metal component suitable for component-specific vibration.
- Production, selectors, movement locks, repair, collision, room layout and
  gameplay remain unchanged.

Primary evidence is
`art/drafts/kitchen-dishwasher-ligne-claire-2026-10-22-v5/evidence/dishwasher-worktop-run-ghost.png`.
It shows the clean cabinet–dishwasher–oven run before the diagnostic ghost.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v5
```

The verifier checks the closed registration gate, all 15 canvas/alpha pairs,
the exact worktop, both exact under-overhang shoulders, hashes,
content-addressed review objects and root-absolute delivery.

Rollback is deletion of only the V5 draft, public shell and archive-set file.
V1–V4, V41, approvals and production remain immutable.
