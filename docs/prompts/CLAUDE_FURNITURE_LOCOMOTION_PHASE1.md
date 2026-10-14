# Prompt: furniture placement and walking plan, Phase 1

Paste everything in the box below into a new Claude Code session opened on `/Users/frank/Projects/lighthouse-keeper`.

```text
Continue Lighthouse Keeper: Phase 1 of the furniture placement and phase-aware
walking architecture (the plan only, no runtime code).

Start here
1. Pull main and quote the starting commit (65fe2ec or a documented
   successor). Create a dedicated branch: claude/furniture-locomotion.
2. Read CLAUDE.md and the project page
   (https://claude.ai/artifact/Ehjz6SdSEvsDYLTLWuKZP4; read it with the
   Artifact tool). It is the record of every decision and holds my answers.
3. Read docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md in full. It defines the
   task ("A safe and useful Claude task now" and "Requested architecture
   deliverable", points 1-8) and the collaboration protocol. Then read in full
   the three documents it requires:
   docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md,
   docs/KEEPER_ANIMATION_HANDOFF.md and docs/KEEPER_ANIMATION_WORKBENCH.md.
4. Inputs to reconcile (evidence, not automatic truth):
   data/keeper_object_dimensions.json, docs/KEEPER_OBJECT_DIMENSIONS.md,
   docs/floor-asset-catalogue/, docs/RECIPES.md,
   docs/DOORS_STAIRS_AND_COSTUMES.md, src/game/config.ts, src/game/world.ts,
   src/ui/Actors.tsx and src/ui/floors.tsx. Also read src/studio/recipe.ts:
   the recipe studio's engine already has standing spots, object types with
   tiers, a 46 px door clear area, solid-object checks and whole-stride
   walks. Reconcile with it; don't create a second, conflicting model.
5. Look at the public Timing Lab
   (https://lighthouse-keeper-mu.vercel.app/keeper-timing-lab), and find
   Codex's approved walk root-motion data in the repo: start 2, 6, 12, 18;
   steady 21 per frame; stop 18, 12, 6, 2, in the 256 x 320 registration
   space. You may copy animation assets into the scratchpad to measure them.
   Never edit Keeper PNGs, review drafts, registers, manifests, the Workbench
   or Final animations, and never approve or promote anything.

My answers (binding)
- Phase 1 only: the written plan, with choices laid out for me.
- Ralph and Eddie WILL move furniture themselves (a planned feature), so the
  placement rules must guide a child gently, not just reject.
- Furniture snaps to a grid. Some places will be impossible for some items.
- Some items get larger when upgraded (an oven: single, double,
  professional), so placement must allow for an item growing. Note that this
  differs from Codex's "tiers retain footprint": resolve it in the plan and
  flag it.
- The keeper anchors to the measured centre of the asset.
- Split steps are not acceptable. No stretched strides, no shortened final
  step, no snapping. The leftover-distance policy is quantisation: grid and
  standing spots are placed so every route is whole steps plus the fixed
  start and stop. Prove it with measurements (step length in logical px and
  in stage units, which positions are reachable from each door and from each
  other, in both directions), and say plainly what it costs in placement
  freedom.

Deliverable
docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md on the branch,
covering the handoff's eight points, with options compared, a recommendation
for each, and explicit open decisions. Pure model code and tests are Phase 2
and wait for my approval. Hand back the branch, commit, changed files,
verification results (npm test, typecheck, build) and the open decisions.

How I work (from my global instructions)
- Anything I need to read, answer or decide goes on the project page (same
  URL; re-read it before every republish so my answers are never wiped;
  questions take free text as well as buttons). In the terminal, give me
  only the link and one line. I'll say "handed back".
- Preflight is done: Phase 1 is GREEN with these answers.
- Stop and update the page if the same error happens twice, the work grows
  beyond Phase 1, or about 10 steps pass without a checkpoint.
- Test with the database off (DATABASE_URL= npx next dev). .env.local is the
  live family database.
- Codex works on main at the same time: pull before you push, and touch none
  of their directories.
```
