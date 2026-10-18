# Prime Keeper sweep broom V6 prompt log

This immutable review candidate used the built-in `imagegen` mode for new bitmap drawing. No generated image was promoted to production.

## Eight-cell walking sweep

References:

- approved Prime Walk V6 contact sheet;
- Frank-supplied stock-broom action contact sheet;
- Frank-supplied detailed rigid-stock broom authority.

Initial prompt: create exactly eight isolated right-facing Prime Keeper cells in a 4×2 transparent grid; map cells 1–8 to the approved contact/down/passing/up/opposite-contact/down/passing/up gait; keep both legs and boots moving; retain two-hand contact; keep the broom in front; use one straight timber shaft, ferrule, rigid crossbar, separately bound straw bundles and a broad straight working edge; preserve scale, baseline, materials and transparent gutters.

The initial result (`exec-a29ca3d0-1f8d-4778-bc03-4979b478922f.png`) was rejected because its second half did not make the opposite gait phase sufficiently explicit.

Final correction prompt: keep the top row and redraw the bottom row only as the opposite-foot half of the approved cycle—left contact, left down, left passing and left up—while preserving the Prime identity, uninterrupted two-hand broom contact, straight rigid shaft, detailed stock and isolated transparent cells.

Selected result:

- raw: `sources/walking-sweep-eight-phase-raw-contact-sheet.png`
- foreground-isolated: `sources/walking-sweep-eight-phase-transparent-contact-sheet.png`

The generator returned a smooth backdrop despite the transparency request. Apple Vision subject lifting removed only that backdrop; the visible generated Keeper and broom pixels were not repainted by the extraction step.

## Front-held turn

The selected turn sheet was generated against the approved Prime turn-angle sequence and corrected so the broom remains in the Keeper's working space in front of his torso throughout the pivot. In the rear angles the body progressively occludes the broom. At the direct rear frame the remaining broom head/shaft is centred between the boots rather than parked at either side, preventing a side-to-front jump at turn completion.

Selected result:

- raw: `sources/turn-v9-broom-front-centred-raw-contact-sheet.png`
- foreground-isolated: `sources/turn-v9-broom-front-centred-transparent-contact-sheet.png`

Rejected intermediate turn sheets remain as provenance only and are not referenced by the V6 batch register.
