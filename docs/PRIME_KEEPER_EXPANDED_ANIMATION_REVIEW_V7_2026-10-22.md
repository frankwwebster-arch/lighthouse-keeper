# Prime Keeper expanded animation review V7

Date: 22 October 2026

Status: preserved rejected evidence. Frank rejected V7 because its row-180
ownership boundary cut into the moving torso, so the upper and lower side
outlines stepped visibly. V8 replaces only those 21 composites.

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v7`

Preserved predecessor: `/prime-keeper-animation-drafts-v6`

## Purpose

V7 is the reversible response to Frank's rejection of V6 frames 11–31 in
`rear-work-turn-return-v1`. V6 kept the generated action source's lower jumper,
which contains two separately drawn ribbed bands. The lower band therefore read
as a duplicated, independently moving bottom seam throughout the work section.

V7 preserves every V1–V6 source, review export and route. It changes no
canonical Prime authority, installed runtime sprite, production selector,
timing, frame count, anchor, costume colour, head, beard, cap, cream stripe or
upper-arm choreography.

## Correction

Only `rear-work-turn-return-v1` positions 11–31 change.

- Rows 0–179 remain byte-identical to V6, retaining the action head, beard,
  shoulders, stripe and working-arm choreography.
- Rows 180–230 come from the current corrected rear Prime authority
  `e6520aab48100c44aabdb0825c9424dbe35bffb2587b5270898e5214db2038df`.
  Only its centre body interval, x=84–171, is admitted. That interval is inside
  the authority's torso outlines, so passive sleeves, hands and side fragments
  cannot enter the work pose.
- Rows 231–319 use the same authority's exact trousers and boots within the
  established x=70–186 lower-body envelope.
- The generated doubled ribbing is absent: no saturated jumper-blue pixel is
  allowed below the authority hem in rows 214–230.
- No generated, inpainted or manually painted pixel enters the amendment. V7
  is deterministic ownership compositing from hash-pinned V6 action pixels and
  the current corrected rear Prime authority.

## Review and reversibility

The page retains per-animation and global play/pause/step/stop controls, frame
rails, stable V7 redraft slots, browser-local notes and the sequence sandbox.
It preloads and decodes every unique V7 and comparison frame before enabling
playback. Selecting a corrected rear-task frame exposes rejected V6 and V7 side
by side with both SHA-256 prefixes.

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v7/`
- V6/V7 SHA-256 map: `corrections.json`
- Archive register: `batch-register.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v7.json`
- Deterministic builder: `scripts/build_keeper_prime_morning_drafts_v7.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v7.mjs`

Rejecting V7 requires discarding only this V7 directory, data manifest and
route. V6 remains byte-addressable and no runtime rollback is required because
these review drafts have not been promoted.

## Verification contract

The verifier checks that:

- the inventory remains ten sequences / 162 frame occurrences;
- exactly 21 frame occurrences differ from V6;
- every unchanged frame remains byte-identical to V6;
- rows 0–179 remain byte-identical to V6 in every affected frame;
- rows 180–230 contain only exact authority pixels within x=84–171 and are
  transparent outside that interval;
- no passive-hand skin or second blue ribbed band survives in those rows;
- rows 231–319 match the exact corrected rear authority within x=70–186;
- the retained upper action still contains more than ten distinct drawings;
- every frame retains a transparent cell-edge safety gutter; and
- source/draft hashes, archive routes, controls, V6/V7 comparison and
  independent redraft slots remain available.

## Approval boundary

V7 is a review candidate. It does not itself approve the rear-task performance
or promote it into the runtime bank. All 21 repaired occurrences remain
independently addressable for further frame-specific feedback.
