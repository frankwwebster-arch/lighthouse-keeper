# Prime Keeper expanded animation review V4

Date: 22 October 2026

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v4`

Preserved predecessor: `/prime-keeper-animation-drafts-v3`

## Purpose

V4 is the reversible response to Frank's finding that rear-task frames 11–31
still contained two vertical seams in the bottom of the jumper. V3 had removed
the loose hip squiggles but had replaced only a central rectangle of the hem,
leaving the two sides of that rectangle visible.

V4 preserves every V1–V3 source, review export and route. It changes no
canonical Prime authority, installed runtime sprite, production selector,
timing, frame count, anchor, costume colour, head, beard, cap, cream stripe,
action pose or upper-body choreography.

## Correction

Only `rear-work-turn-return-v1` positions 11–31 change.

- Each frame is rebuilt from its original hash-pinned V2 action source, rather
  than from the rejected V3 composite.
- The complete upper action drawing through row 203 is retained and recentered
  over the fixed x=128 root exactly as before.
- Rows 204–227 use the central blue body run and contiguous dark outline from
  approved rear authority `31dbac4efc00089f…`. Its passive hands are excluded.
- Rows 228–319 use the exact authority lower body.
- The resulting hem is one closed continuous component. No black hip fragment,
  passive-hand fragment or rectangular join seam remains.
- All 21 repaired frames share identical authority-locked pixels from row 204
  downward while retaining their individual upper-body performance.

The repair is deterministic compositing of existing hash-pinned Prime pixels.
No generated, inpainted or manually painted pixel enters V4.

## Review and reversibility

The page retains per-animation and global play/pause/step/stop controls, frame
rails, stable V4 redraft slots, browser-local notes and the sequence sandbox.
It preloads and decodes every unique V4 and comparison frame before enabling
playback. Selecting a corrected rear-task frame exposes its rejected V3 source
and V4 draft side-by-side with both SHA-256 prefixes.

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v4/`
- V3/V4 SHA-256 map: `corrections.json`
- Archive register: `batch-register.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v4.json`
- Deterministic builder: `scripts/build_keeper_prime_morning_drafts_v4.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v4.mjs`

Rejecting V4 requires discarding only this V4 directory, data manifest and
route. V3 remains byte-addressable and no runtime rollback is required because
these review drafts have not been promoted.

## Verification contract

The verifier checks that:

- the inventory remains ten sequences / 162 frame occurrences;
- exactly 21 frame occurrences differ from V3;
- every unchanged frame remains byte-identical to V3;
- every visible pixel from rows 204–227 is an exact authority pixel and no hip
  or passive-hand fragment exists outside the declared central body envelope;
- rows 228–319 match the exact rear authority;
- all 21 lower-body blocks are byte-identical;
- every frame retains a transparent cell-edge safety gutter;
- source/draft SHA-256 mappings and archive routes resolve; and
- the review controls, V3/V4 comparison and independent redraft slots remain
  available.

## Approval boundary

V4 is a review candidate. It does not itself approve the rear-task performance
or promote it into the runtime bank. All 21 repaired occurrences remain
independently addressable for further frame-specific feedback.
