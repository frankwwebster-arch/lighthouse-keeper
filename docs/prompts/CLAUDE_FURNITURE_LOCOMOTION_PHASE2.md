Continue Lighthouse Keeper: Phase 2 of furniture placement and walking
(the pure model and its tests; no runtime wiring, no art).

Start here
1. Pull main, then check out claude/furniture-locomotion (commit fe7a4fc or
   a documented successor) and merge main into it. Quote both commits.
2. Read CLAUDE.md, then the project page
   (https://claude.ai/artifact/Ehjz6SdSEvsDYLTLWuKZP4; read it with the
   Artifact tool). My answers to D1-D6 are saved there and are binding.
3. Read docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md in full. It
   is the contract, amended by my answers.
4. Check whether Codex has answered D7-D11 or changed the walk root-motion
   numbers (art/drafts/keeper-prime-*), and record what you find.

Build
- A new isolated module, src/placement/, with no imports from the UI: ku
  types, room records, grid, validator, shuffle, route compiler and
  frame-table builder, as in sections 1-5 of the plan.
- Walk numbers come from one constants table that can hold both Codex's
  approved numbers (38 + 38, stop from F1 only) and the proposed re-timed
  ones (42 + 42, stops from F1 and F5). Tests must show that the approved
  numbers fail the three-spot case and the proposed numbers pass it.
- The tests in section 7 of the plan.
- Never edit Keeper PNGs, registers, manifests, review pages, the Workbench
  or Final, and never approve or promote anything. Don't wire anything into
  the game or the studio; that is Phase 3.

Hand back the branch, commit, changed files, npm test / typecheck / build
results, and anything still open.

How I work
- Anything I need to read, answer or decide goes on the project page (same
  URL; re-read it before every republish so my answers are never wiped). In
  the terminal, give me only the link and one line. I'll say "handed back".
- Stop and update the page if the same error happens twice, the work grows
  beyond Phase 2, or about 10 steps pass without a checkpoint.
- Test with the database off (DATABASE_URL=). Codex works on main: pull
  before you push, and touch none of their directories.
