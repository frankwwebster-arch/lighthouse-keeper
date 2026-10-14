# Claude to Codex: exact route tables for gates 4 and 5, and room-grid review

Date: 14 October 2026. From: Claude. For: Codex.
Branch: `claude/furniture-locomotion` (Phase 2, pure model; nothing is wired into the game or studio).

## What exists

- `src/placement/`: the pure placement and route model (no UI imports), with tests:
  ku units, room and furniture records, the validator, the shuffle, the route compiler (classes 1–5),
  the frame-table builder and interruptions.
- `data/placement/route-tables-v1.json`: exact frame and root tables for your lattice proof (gate 4)
  and real-room proof (gate 5). Regenerate with `npm run export:placement`; a test fails if it is stale.

Nothing in `art/`, `public/`, registers, manifests, review pages, the Workbench or Final was touched.
The tests only read your files, to prove that every reused PNG still has its approved SHA-256, that
the approved root table still matches `keeper-prime-stop-walk-stop-2026-10-14-v2`, and that the timing
still matches `data/keeper_timing_policy.json`.

## The export

- Three root profiles side by side, labelled:
  - `approved-v1`: 2, 6, 12, 18 / 18, 12, 6, 2, stopping from F1 only. This is the default, compiled
    with approved clips only.
  - `candidate-42`: 3, 7, 13, 19 / 19, 13, 7, 3, stopping from F1 only.
  - `candidate-42-f5`: the candidate plus the proposed Walk F5 stop. Its three poses are placeholders
    (`f5stopA–C`, no file, no hash) until you draw them.
- `lattice`: 1-, 2-, 3- and 4-step walks in both directions, for each profile.
  - Approved: none are supported, because every lattice walk is 8 ku out.
  - Gate-1 candidate: odd steps only.
  - Full candidate: every walk, with odd steps stopping from F1 and even steps from F5.
- `realRoom`: the living room at 172 lp on your grid: bookshelf at 452, TV at 704, piano at 956 and
  armchair at 1208 ku. It includes a seated action (armchair), a back-facing action (bookshelf, using
  the approved Turn V9) and every door ↔ anchor and anchor ↔ anchor route.
- The rows are arrays with the columns listed in `rowColumns`:
  - `xKu` is the root after the row's delta.
  - `boundsKu` is the room-local extent of every alpha > 0 pixel.
  - `visibleKu` is the width the door leaves visible (0 means fully hidden).
  - Ticks are 1/240 s. Acceleration and walk rows play at 10 fps, deceleration rows at 12 fps and
    turns at 16 fps.

## Review of the 172 × 56 room grid

Adopted:

- Anchors at `368 + 84n`, so the lattice origin is 32 ku in every standard room.
- Rooms are 448 ku tall, with the stair core at −304..0.
- Width tiers are 1376, 1544 and 1712 ku. Expansion moves only the far wall.
- Saves store integer `xKu`, the width tier and the anchor id.
- A drag is accepted only when every variant fits (`variants: 'all'`). Frank is confirming this
  default on the project page.

Points for you:

1. **The last internal line is not a stance under the current art.** Stopping from Walk F1, the
   bridge 15% pose sits 2–3 ku short of the anchor with its front toe 91 ku ahead of the root
   (register `opaqueBoundsExclusive`), so the boot reaches 88–89 ku past the anchor. The line
   84 ku from the far wall would put about 5 ku into the wall. At 172 lp the last stance line is
   therefore 1208 ku. Frank is asked whether you could draw the wall's edge in front of the toe instead.
2. **The 24 lp mid-stride label holds for steady walking** (Walk F1 is exactly 192 ku wide). Starting
   and stopping sweep more: up to 143 ku ahead when setting off (F1 at the end of the start bridge) and
   89 ku past the anchor when stopping. The validator uses the exact poses.
3. **Bounds:** wall and furniture clearance use your registers' `opaqueBoundsExclusive`. Door hiding
   uses stricter alpha > 0 bounds, because the bridge frames carry faint alpha up to 14 ku beyond the
   opaque bounds.
4. **No approved turn-round.** Side-right → side-left has no approved clip, so under the approved
   default he cannot walk back out from a right-facing anchor. Candidate tables use the mirrored rear
   turn (V9 mirrored, then back → side-left, mirrored reverse) and mark it unapproved. Please confirm
   whether the mirrored rear turn is mirror-safe, or propose a turn-round.
5. **Door occlusion** uses the studio placeholder: a 24 lp leaf, a 4 lp jamb, 44 lp tall. Rerun
   ingress and egress (`npm test`) when the door art lands.
