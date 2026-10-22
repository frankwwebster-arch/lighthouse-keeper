# Prime Keeper expanded animation review V3

Date: 22 October 2026

Status: preserved predecessor. Frank rejected only the rear-task V3 amendment
because two vertical seams remained in the bottom jumper hem. V4 retains the
other V3 feedback corrections and replaces those 21 frames separately.

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v3`

## Purpose

V3 is the reversible response to Frank's first frame-specific review of V2. It
does not overwrite V1, V2, canonical Prime art, approved-source review exports,
runtime sprites or production selectors.

The page retains all per-animation transports, global play/pause/step/stop,
frame rails, stable redraft slots, browser-local notes and the sequence sandbox.
It preloads and decodes every unique frame before enabling playback.

## Corrections

- **Passive front/back jumper colour:** every occurrence of the two reused dark
  endpoint rasters is replaced by one versioned front correction and one
  versioned back correction. Alpha, registration and all non-jumper pixels are
  preserved. Jumper colour ranks are mapped deterministically to the approved
  bright rear turn endpoint (`31dbac4efc00089f…`), whose measured family is
  centred on jumper blue `0,108,230`.
- **Lift entry, ride handoff and exit:** old frame 2 is omitted. The sequence is
  now seven frames; the rear and front passive endpoints use the colour
  corrections above.
- **Cook at counter:** frames 1 and 8 use the corrected passive rear endpoint.
- **Brush teeth at basin:** frames 1 and 8 use the corrected passive rear
  endpoint. Frame 1 is corrected too because it is the same reused raster as
  the cited frame 8.
- **Friendly wave:** frames 1 and 6 use the corrected passive front endpoint.
- **Seated route naming:** `Diary: turn, sit, write, stand and return` is now
  `Turn, sit, hold, stand and return`. No writing motion is claimed.
- **Rear task:** V2 positions 11–31 retain their continuous generated upper-body
  performance, recentered over x=128, but every frame now joins at y=205 to the
  same exact rear-authority waist and legs. This removes the hip squiggles and
  prevents the torso from sliding off the fixed lower body.

## Reversibility and evidence

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v3/`
- Source/draft SHA-256 mapping: `corrections.json`
- Archive register: `batch-register.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v3.json`
- Deterministic builder: `scripts/build_keeper_prime_morning_drafts_v3.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v3.mjs`

The verifier checks the 162-occurrence inventory, the lift omission, the title
change, endpoint alpha identity, bright-jumper medians, identical lower-body
bytes across all 21 rear repairs, cell-edge gutters, unique frame/redraft ids,
archive mappings and review controls.

One image-generation repair study was deliberately rejected because it changed
the Prime Keeper's scale and rendering. No generated study pixels enter V3;
the delivered fixes are deterministic edits of hash-pinned source frames.

## Approval boundary

V3 is a review candidate. The current runtime remains unchanged. Individual
frames can be revised again through their V3 redraft slots; rejection requires
discarding only this V3 correction directory and route.
