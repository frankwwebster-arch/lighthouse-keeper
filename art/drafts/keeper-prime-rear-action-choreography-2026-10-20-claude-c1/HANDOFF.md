# Claude C1 bubble choreography: model-test handoff

Claude Code's answer to `claude-code-model-test-pack/CLAUDE_CODE_MODEL_TEST_PROMPT.md`.
A draft for comparison with Codex's V2. Nothing is approved, promoted or deployed.

## Files

| File | What it is |
| --- | --- |
| `build.mjs` | Generates every frame from keyframed staging. `node build.mjs` |
| `verify.mjs` | Checks the brief (below). `node verify.mjs` |
| `metrics.mjs` | Shared geometry: visible-pixel bounds, overlap, bubble bounds |
| `catalogue.json` | C1 data in V2's shape, plus `treatment`, `contacts`, `supports`, `metrics` |
| `compare-v2.json` | V2's bubble timelines remapped onto pack files, measured the same way |
| `review.html` | Side-by-side player (C1 and V2 in sync) with Frank's verdict form |
| `answers.json` | Frank's saved verdict (written by the review page) |
| `pack` | Symlink to the V2 model-test pack. Read only; every picture comes from it |

Local preview: serve this directory (`python3 -m http.server -d .`) and open
`review.html`. Frank reviews the published copy on claude.ai.

## Staging rules

- **Origin.** The connector mouth is cloud-local (182, 193), under the head at
  x 182. Three trail circles pop from the cap on frames 0–2 while the scalloped
  bubble scales up from that point. The hero (frames 1–5) and each support
  (A 4–8, B 6–10, C 8–12) are born at the mouth and fly out on curved paths.
- **Lanes.** Supports live in fixed lanes: A upper left (-84, -26), B upper
  right (84, -28), C lower right (86, 34). The hero sits at (0, 16), scale 0.7.
- **One visitor at a time.** Supports visit the hero in turn (A ~13–20, B ~18–26,
  C ~23–30), each with a story move: flips, a tip, three hammer strikes, a
  spin, a scrub, a stack. Touches are declared in `contacts`; outside them no
  two pictures cover more than 7% of the smaller one (BBQ), 0% elsewhere.
- **Resolution.** Supports fold into the hero (or return to the head for
  washing-up tools) by frame 32, the result bursts out, and hero and result
  settle side by side: hero (-44, 16, 0.62), result (48, 6, 0.64).
- **Quiet tail.** Frames 37–41 hold one still picture with every symbol at 0.
- **Ticks and stars.** All separate instances on the symbol layer: a speed tick
  per moving picture (rotated onto its real velocity; the drawn streak points
  up-right, so rotation = travel angle + 35.5°), a star at every touch, landing
  sparks, rising heat or soap loops, wrench orbit ticks, a burst and three
  glints. 20–22 instances per story, at most 6 on any one frame.
- **Reduced motion.** No travel, spin or scale: pictures fade in where they
  live and swap to their touch pose while invisible; punctuation is static; no
  speed ticks; the bubble only fades in. It ends on the same quiet picture as
  full motion.

## Layer separation

Body, hero/result, supports, symbols and treatment marks are separate arrays or
fields in every frame and separate switches on the page. `treatment` holds the
bubble scale and opacity and the three trail circles; the scalloped outline is
drawn by the page from `scallopPath()` in `review.html`. SFX cues keep V2's
owners and kinds, re-timed to C1's beats.

## Checks (`node verify.mjs`, 3,021 pass)

Pack and every protected path unchanged (git status and every manifest hash);
all 52 sequence frames byte-exact Prime bodies with V2's timing; every picture
a pack asset; 42 frames at 8 fps per story and mode; five-layer roles on every
frame; quiet tail still and silent in both modes and identical between them;
no picture leaves the bubble; undeclared covering at most 10%; hero and
supports born within 20 px of the connector; each support travels at least
150 px; at least 15 separate ticks and stars, 4 speed ticks and 5 stars per
story; reduced motion never moves, spins or scales a visible picture.

## Measured against V2 (full motion)

| Story | Frames with >25% covering, C1 / V2 | Separate ticks and stars, C1 / V2 |
| --- | --- | --- |
| Garden BBQ | 13 / 23 | 21 / 9 |
| Sandwich | 17 / 10 | 20 / 8 |
| Washing up | 12 / 16 | 22 / 9 |
| General repair | 18 / 20 | 21 / 9 |

C1's covering frames are its declared touches (stacking, scrubbing, folding).
The sandwich stack covers by design, which is why it is higher than V2's.

## Boundary

Written only inside this directory. Not touched: the pack, V1, V2, Prime
authority, runtime, Final, Kitchen, registers, manifests, package.json and
deployment configuration. Not deployed.
