# Kitchen V23 approved continuous-run authority

Date: 17 October 2026  
Status: approved visual authority; unpromoted and unwired  
Review: `/keeper-review/kitchen-continuous-run-approved-v23/`

## Approval

Frank marked Image 1 at `x=37.3%, y=56.9%` with “this is correct.” The exact
`2170 × 725` PNG is now the binding full-room visual authority. Its SHA-256 is:

`5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707`

The approved visual treatment is a single full-height, rear-wall fitted run:
all bays share one front plane, one uninterrupted sea-glass worktop and one
common dark base. The toaster/counter area at the approval point is explicitly
correct. The standalone pedal bin and one-person table/chair remain present.

## Authority chain

- V20: immutable fitted-galley visual provenance.
- V21: immutable isolated-asset inventory, including oven tiers, bin and table.
- V22: immutable rejected deterministic room reconstruction; it incorrectly
  treated the earlier kettle lower edge as a shallower cabinet-body datum.
- V23: exact approved Image 1 and current full-room appearance authority.

Any later production extraction, animation-state build or game-scale redraw
must reproduce V23's appearance. Approval does not by itself promote the image
to runtime sprites or Final art.

## Integrity and rebuild

`scripts/build_kitchen_continuous_run_approved_v23.py` only copies the approved
source bytes into the raw and review locations and refuses a source hash or
dimension change. It performs no crop, resize, recolour or redraw. The review's
approval marker is an HTML overlay and is never baked into the raster.

Run:

```sh
python3 scripts/build_kitchen_continuous_run_approved_v23.py
npm run archive:keeper-review
npm run verify:kitchen-continuous-run-approved-v23
npm test
npm run typecheck
npm run build
```

Rollback removes only V23 source/raw/draft/review files, its archive set,
builder, verifier and V23 documentation. V20–V22 remain intact.
