# Prime Keeper expanded animation review V8

Date: 23 October 2026

Status: review candidate. V7 is preserved as rejected evidence.

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v8`

## Correction

V8 responds to the visible inward step where V7 joined its upper and lower
body. Only `rear-work-turn-return-v1` positions 11–31 change.

- Rows 0–213 come byte-for-byte from the V6 moving action source. This keeps
  the complete torso and its single natural ribbed hem instead of cutting the
  torso early.
- Rows 214–230 use the exact approved rear-turn lower body
  `31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35`
  within its x=82–172 source interval and translated by the moving torso's
  measured horizontal registration (−2 to +2 px).
- The retained hem on row 213 and the authority trousers on row 214 have the
  same per-frame outer alpha bounds. There is no horizontal step at either
  side.
- Rows 231–319 use that authority's exact trousers and boots with the same
  per-frame registration.
- No generated, inpainted, rescaled or repainted pixel enters V8.

All other V7 frames, timing and controls are preserved. The page still offers
play, pause, stop, frame stepping, frame selection, browser-local redraft notes
and the sequence sandbox. Every frame retains its own V8 redraft slot.

## Reversibility and verification

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v8/`
- V7/V8 hash map: `corrections.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v8.json`
- Builder: `scripts/build_keeper_prime_morning_drafts_v8.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v8.mjs`

The verifier requires ten sequences / 162 frame occurrences, exactly 21 V8
changes, byte-identical V6 action through row 213, exact per-frame continuity
across rows 213–214, exact translated approved-authority lower-body pixels, transparent
cell-edge gutters, archived hashes, controls and
independent redraft slots.

## Approval boundary

V8 does not approve the rear-task choreography or promote it into the runtime
bank. V1–V7, all canonical art and the installed runtime remain unchanged.
