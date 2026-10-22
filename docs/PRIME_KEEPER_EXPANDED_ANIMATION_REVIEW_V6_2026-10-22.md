# Prime Keeper expanded animation review V6

Date: 22 October 2026

Status: **rejected and preserved**. Frank found that frames 11–31 still contain
two separately drawn ribbed bands at the bottom of the jumper. V7 supersedes
this review without overwriting it.

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v6`

Preserved predecessor: `/prime-keeper-animation-drafts-v5`

## Purpose

V6 is the reversible response to Frank's rejection of V5's rear-task repair.
V5 removed the doubled hem but introduced a harsher horizontal waist cut and
an unstable moving-hem/fixed-trouser handoff. It improved one still image while
making the complete motion worse.

V6 preserves every V1–V5 source, review export and route. It changes no
canonical Prime authority, installed runtime sprite, production selector,
timing, frame count, anchor, costume colour, head, beard, cap, cream stripe or
upper action choreography.

## Correction

Only `rear-work-turn-return-v1` positions 11–31 change.

- Each frame is rebuilt from its original hash-pinned V2 action source.
- Rows 0–194 retain the complete recentered action drawing byte-for-byte.
- Rows 195–230 retain the source's complete lower torso, ribbed jumper hem and
  natural trouser join. The horizontal registration eases from the upper-body
  correction to zero over those rows, so the torso meets the fixed root without
  a hard cut or second seam.
- In rows 214–230, only the centre-owned contiguous source run survives. This
  removes the detached black side runs without repainting the body.
- The taper reaches zero at row 230. Exact approved rear-authority trousers and
  boots begin at row 231, where source and authority share the same outer and
  crotch-split geometry.
- No generated, inpainted or manually painted pixel enters V6.

The repair is deterministic compositing of existing hash-pinned Prime pixels.
It changes registration and ownership only: source action through the natural
waist join, approved lower body below the matching split.

## Review and reversibility

The page retains per-animation and global play/pause/step/stop controls, frame
rails, stable V6 redraft slots, browser-local notes and the sequence sandbox.
It preloads and decodes every unique V6 and comparison frame before enabling
playback. Selecting a corrected rear-task frame exposes the rejected V5 frame
and V6 candidate side by side with both SHA-256 prefixes.

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v6/`
- V5/V6 SHA-256 map: `corrections.json`
- Archive register: `batch-register.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v6.json`
- Deterministic builder: `scripts/build_keeper_prime_morning_drafts_v6.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v6.mjs`

Rejecting V6 requires discarding only this V6 directory, data manifest and
route. V5 remains byte-addressable and no runtime rollback is required because
these review drafts have not been promoted.

## Verification contract

The verifier checks that:

- the inventory remains ten sequences / 162 frame occurrences;
- exactly 21 frame occurrences differ from V5;
- every unchanged frame remains byte-identical to V5;
- rows 0–194 retain the accepted V5 action drawing exactly;
- every visible pixel in rows 195–230 is an exact V2-source pixel under the
  recorded row-wise taper;
- rows 214–230 contain exactly one centre-owned alpha run, so detached hip
  fragments cannot survive;
- row 230 already matches the authority's alpha geometry before the handoff;
- rows 231–319 match the exact rear authority within the lower-body envelope;
- the tapered source hem remains animated rather than becoming a frozen block;
- every frame retains a transparent cell-edge safety gutter; and
- source/draft SHA-256 mappings, archive routes, controls, V5/V6 comparison and
  independent redraft slots remain available.

## Approval boundary

V6 is rejected review evidence. It was never approved or promoted into the
runtime bank. Its 21 amended occurrences remain byte-addressable for comparison
with V7.
