# Kitchen Dishwasher Ligne-Claire V6

Status: immutable review candidate; not approved, registered, promoted or wired.

Review: `/keeper-review/kitchen-dishwasher-ligne-claire-v6/index.html`

V6 supersedes V5 because its Broken drawing included an unexplained floating
bolt, opened too little and left the handle attached at both ends. This weakened
the established V41 failed-appliance read.

## Correction

- Off and On are byte-identical to V5 across all ten join variants.
- Broken restores a substantially wider-open door: the lower-right hinge has
  failed while the lower-left hinge remains attached.
- The same slender orange/copper handle hangs diagonally from its left mounting
  point, with the right mounting point visibly failed.
- The bolt and its marks are absent from the fresh versioned high-resolution
  redraw before the established Lanczos registration/downsampling.
- The inherited compact/regular/emphatic suds strips remain separate,
  dishwasher-owned forty-frame effects; the regular default provides the large
  soapy floor puddle and repair removes it immediately.
- All 15 V41 `98 × 82 px` canvases and alpha channels remain exact.
- The approved Cabinet V3 worktop through row `16` and both cabinet shoulders
  through row `29` remain exact.
- Production, selectors, movement locks, repair, collision, room layout,
  healing, gameplay and approved/static art remain unchanged.

The Broken source is a precise built-in image edit using the clean V6 image as
visual authority and approved V41 as the structural reference. V5, its source
references and every earlier immutable review remain unchanged.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v6
```

The verifier checks the closed gate, all canvases and alpha channels, exact
worktop/shoulders, Off/On byte identity to V5, the changed Broken reference,
hashes, content-addressed objects and root-absolute delivery.

Rollback is deletion of only the V6 source-reference directory, draft, public
shell and archive-set file.
