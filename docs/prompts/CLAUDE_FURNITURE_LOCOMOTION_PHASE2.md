Continue Lighthouse Keeper: Phase 2 of furniture placement and walking
(the pure placement and route model with its tests; no game or studio
wiring, no art, no review pages).

Start here
1. Pull main, then check out claude/furniture-locomotion (plan revision 3 or
   a documented successor) and merge main into it. Quote both commits.
2. Read CLAUDE.md, then the project page
   (https://claude.ai/artifact/Ehjz6SdSEvsDYLTLWuKZP4; read it with the
   Artifact tool). My answers are saved there and are binding.
3. Read in full docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md
   (revision 3) and docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md.
4. Check how far Codex's review gates have got (the re-timed root-motion
   candidate, the Walk F5 stop bridge, the lattice and real-room proofs) and
   which, if any, I have approved. Record what you find.

Build
- A new isolated module, src/placement/, with no imports from the UI: ku
  types, room records (lattice origin, clear area, aperture, occlusion mask
  and hidden pocket kept separate), keeperUseAnchor records, the validator,
  the shuffle, the route compiler (route classes 1-5) and the frame-table
  builder.
- Root-motion tables are data read from Codex's registers: keep the approved
  table and the candidate table side by side and labelled. Use only what I
  have approved for anything presented as the default; until the F5 stop is
  approved, even-step same-room routes must report "unsupported", never
  improvise.
- The tests in section 7 of the plan, including the proof that the approved
  numbers fail the three-anchor case and the candidate numbers pass it.
- An export of exact frame and root tables for 1-, 2-, 3- and 4-step routes
  and for one real room, so Codex's lattice and real-room review pages can
  use them.
- Never edit Keeper PNGs, registers, manifests, review pages, the Workbench
  or Final, never change approved root motion or timing, and never approve
  or promote anything.

Hand back the branch, commit, changed files, npm test / typecheck / build
results, and anything still open.

How I work
- Anything I need to read, answer or decide goes on the project page (same
  URL; re-read it before every republish so my answers are never wiped). In
  the terminal, give me only the link and one line. I'll say "handed back".
- Stop and update the page if the same error happens twice, the work grows
  beyond Phase 2, or about 10 steps pass without a checkpoint.
- Test with the database off (DATABASE_URL=). Codex works on main: pull
  before you push, and touch none of their directories. Pushes don't deploy;
  only a [deploy] commit does.
