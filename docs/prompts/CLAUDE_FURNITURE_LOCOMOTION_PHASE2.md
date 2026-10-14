Continue Lighthouse Keeper: Phase 2 of furniture placement and walking
(the pure model, its tests and a diagnostic doorway prototype; no game or
studio wiring, no art).

Start here
1. Pull main, then check out claude/furniture-locomotion (revision 2 of the
   plan or a documented successor) and merge main into it. Quote both commits.
2. Read CLAUDE.md, then the project page
   (https://claude.ai/artifact/Ehjz6SdSEvsDYLTLWuKZP4; read it with the
   Artifact tool). My answers to D3-D8 are saved there and are binding.
3. Read in full docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md
   (revision 2) and docs/CODEX_TO_CLAUDE_DOORWAY_GAIT_ALIGNMENT_2026-10-14.md.
   The approved walk is frozen: never change the start, stop or walk deltas,
   frames, order or Fast Timing V1, and never ask Codex for new bridge art.
4. Check for any newer Codex note, door art or occlusion mask, and record
   what you find.

Build
- A new isolated module, src/placement/, with no imports from the UI: ku
  types, room records with clear area, aperture, occlusion mask and hidden
  pocket kept separate, the validator, the shuffle, the route compiler
  (route classes 1-5, ingress planned backwards from the target, egress until
  zero masked alpha) and the frame-table builder.
- Root motion and Fast Timing V1 are read from Codex's registers and
  catalogue, never copied by hand.
- The tests in section 7 of the plan.
- The diagnostic prototype page from section 8: one room, the placeholder
  door mask, at least three furniture centres that are not on any step
  lattice, complete ingress and egress, and one same-room trip as I decided
  in D7, at large inspection scale and exact game scale, with a mask overlay
  and the debug readout. Use Codex's approved frames read-only.
- Never edit Keeper PNGs, registers, manifests, review pages, the Workbench
  or Final, and never approve or promote anything.

Hand back the branch, commit, changed files, npm test / typecheck / build
results, the prototype link (deploy only with npm run deploy if I ask), and
anything still open.

How I work
- Anything I need to read, answer or decide goes on the project page (same
  URL; re-read it before every republish so my answers are never wiped). In
  the terminal, give me only the link and one line. I'll say "handed back".
- Stop and update the page if the same error happens twice, the work grows
  beyond Phase 2, or about 10 steps pass without a checkpoint.
- Test with the database off (DATABASE_URL=). Codex works on main: pull
  before you push, and touch none of their directories. Pushes don't deploy;
  only a [deploy] commit does.
