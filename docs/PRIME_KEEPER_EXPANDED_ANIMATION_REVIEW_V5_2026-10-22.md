# Prime Keeper expanded animation review V5

Date: 22 October 2026

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v5`

Preserved predecessor: `/prime-keeper-animation-drafts-v4`

## Purpose

V5 is the reversible response to Frank's finding that V4's rear-task repair
still exposed two faults in frames 11–31: detached black fragments reappeared
outside the hips, and the moving jumper hem had been cut across its ribbing so
a second fixed hem remained visible underneath.

V5 preserves every V1–V4 source, review export and route. It changes no
canonical Prime authority, installed runtime sprite, production selector,
timing, frame count, anchor, costume colour, head, beard, cap, cream stripe or
upper action choreography.

## Correction

Only `rear-work-turn-return-v1` positions 11–31 change.

- Each frame is rebuilt from its original hash-pinned V2 action source.
- Rows 0–194 retain the complete recentered action drawing.
- Rows 195–218 retain the source's complete moving ribbed jumper hem and its
  sole lower edge. The action hem therefore occludes the fixed join instead of
  being cut open at row 203 as it was in V4.
- Exact approved rear-authority trousers begin behind the moving hem at row
  219. Their upper waist is selected by navy material, adjacent outline and
  connected central-component ownership; the fixed jumper hem, passive hands
  and detached fragments are not copied.
- Rows 236–319 retain the exact approved rear-authority lower body.
- No generated, inpainted or manually painted pixel enters V5.

The repair is deterministic compositing of existing hash-pinned Prime pixels.
It changes ownership and occlusion only: moving jumper in front, approved
trousers behind.

## Review and reversibility

The page retains per-animation and global play/pause/step/stop controls, frame
rails, stable V5 redraft slots, browser-local notes and the sequence sandbox.
It preloads and decodes every unique V5 and comparison frame before enabling
playback. Selecting a corrected rear-task frame exposes the rejected V4 frame
and V5 candidate side by side with both SHA-256 prefixes.

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v5/`
- V4/V5 SHA-256 map: `corrections.json`
- Archive register: `batch-register.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v5.json`
- Deterministic builder: `scripts/build_keeper_prime_morning_drafts_v5.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v5.mjs`

Rejecting V5 requires discarding only this V5 directory, data manifest and
route. V4 remains byte-addressable and no runtime rollback is required because
these review drafts have not been promoted.

## Verification contract

The verifier checks that:

- the inventory remains ten sequences / 162 frame occurrences;
- exactly 21 frame occurrences differ from V4;
- every unchanged frame remains byte-identical to V4;
- rows 0–194 retain the accepted V4 action drawing exactly;
- every visible moving-hem pixel in rows 195–218 is an exact shifted V2-source
  pixel, with no fixed authority hem in that layer;
- no lower-seam pixel can escape the x=76–180 ownership envelope;
- every visible trouser pixel in rows 219–235 is exact rear-authority data and
  no detached fragment can exist outside x=76–180;
- rows 236–319 match the exact rear authority within the lower-body envelope;
- the moving hem remains animated rather than becoming one frozen block;
- every frame retains a transparent cell-edge safety gutter; and
- source/draft SHA-256 mappings, archive routes, controls, V4/V5 comparison and
  independent redraft slots remain available.

## Approval boundary

V5 is a review candidate. It does not itself approve the rear-task performance
or promote it into the runtime bank. All 21 repaired occurrences remain
independently addressable for further frame-specific feedback.
