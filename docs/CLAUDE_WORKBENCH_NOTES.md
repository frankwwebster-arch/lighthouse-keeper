# Claude's notes: the shared workbench

Date: 11 October 2026. Written by Claude for the next Claude session (and readable by Codex). Frank will paste Codex's handover note into a new prompt; start there and with this file.

## What this work is

One **workbench** where Frank can:
- review every asset Codex makes (animations, rooms, furniture, backdrop);
- have Claude and Codex each propose how activities play (recipes);
- amend anything by eye;
- send it back for Claude and Codex to review **independently**;
- approve it.

The approved results become what the game plays. Frank calls it absolutely integral to the whole project.

Two tools exist today and overlap:

| | Codex's keeper reviewer | Claude's recipe studio |
|---|---|---|
| Address | `/keeper-review` (`public/keeper-review/`), also `docs/keeper-scale-audit/review.html` | `/studio` (`src/studio/`, `src/app/studio/`) |
| Does | Review every animation (scale, ghosts, frames, fps, size proposals, notes, decisions), drafts against canonical art, **Hand back to Codex** | Assemble activities from clips (recipes and macros), object types and variants, doors and costume changes, sounds, solid-object checks, pixel join checks with bridges, route, ghosts, evening light |
| Saves to | browser, then `keeper_review_handoffs` (a database queue that Codex reads) | `studio_docs`, `studio_sounds` (database); drafts are files in `data/studio/` |
| Planned next | `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md`, sections 1–8. **Sections 5 and 6 (routines, triggers, context preview) duplicate the recipe studio.** | the shared review loop (versions, hand-back into the repo, independent reviews) |

## Decided: build our own (Frank, 11 October 2026)

No existing platform does the whole job, so we build our own thin workbench. These were considered:
- Unity's Animator, Godot's AnimationTree, Rive, Spine;
- Unreal's Smart Objects;
- LDtk and Tiled;
- SyncSketch, ShotGrid (Flow), ftrack, Frame.io;
- Aseprite.

**Borrow their proven ideas:**
- named states and transitions with explicit "finish this before moving on" rules (Unity, Rive);
- objects that declare their own spots and behaviours (Smart Objects; we already do this);
- notes pinned to an exact frame, numbered versions, and a simple status flow of needs review → changes requested → approved (SyncSketch, ShotGrid);
- LDtk as a possible ready-made room-layout editor later, rather than writing one.

## How to proceed (in this order; do not skip to building)

1. **Read** Codex's handover (pasted by Frank), this file, and then, in full:
   - `docs/RECIPES.md` and `docs/DECISIONS.md`;
   - `docs/KEEPER_ANIMATION_HANDOFF.md`;
   - `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md`;
   - `docs/FOR_CODEX.md` and `docs/DOORS_STAIRS_AND_COSTUMES.md`;
   - `docs/AMBIENCE_AND_BACKDROP.md` and `docs/BACKGROUND_ELEMENTS.md`.
2. **Explore what is built, in detail, before planning:**
   - Run both tools in a browser. Use a dev server with the database off: `DATABASE_URL= npx next dev -p 3123`. `.env.local` points at the **live** database with the family's real players, so never test against it.
   - Read the code paths end to end:
     - `src/studio/*` (`recipe.ts` is the pure engine; `Studio.tsx` the screen);
     - `src/app/api/studio/*`;
     - `public/keeper-review/index.html` and its drafts;
     - `src/app/api/keeper-review-handoffs`;
     - `scripts/keeper-contract.ts` (the pose and neutral contract that `npm test` enforces);
     - `scripts/sprites.ts` (sidecars to the manifest).

     Codex's hand-back monitor script (`scripts/keeper_review_handoff_monitor.py`) is **not relevant** to this work (Frank, 11 Oct): don't design around it.
   - Trace each data flow: art sidecars → manifest → studio; reviewer → hand-back queue → Codex; studio edits → `studio_docs` (they never reach the repo today).
   - List every overlap, gap and contradiction between the two tools.
3. **Plan, as a senior tools developer at a game studio.**
   - Architecture: one app, shared engine and renderer, a single source of truth.
   - Data model: assets, variants, recipes, versions, reviews, annotations, requests, hand-backs.
   - A UI map written from Frank's side of the screen.
   - How Codex and Claude each extend it without stepping on each other.
   - Migration of both tools' existing data, with nothing lost.
   - Phased delivery, each phase usable on its own.

   Present the plan to Frank in plain English.
4. **Ask Frank questions one at a time, in his preferred format** (below), before building anything. Record each answer in this file and in `docs/DECISIONS.md`.
5. Build in reviewable phases. Each one: tests, a production build, a headless browser check, commit, push to `main`, confirm the Vercel deploy is READY, then tell Frank what to try.

## How Frank wants questions

- **One question at a time**, with the AskUserQuestion tool.
- 2–4 options, **the recommended one first, marked "(Recommended)"**, each with a one-line plain-English consequence.
- No jargon in the question. Frank is not a developer; ask about outcomes ("Where should your edits be saved?"), not mechanisms ("DB vs git?").
- When his answer is free text, read it carefully: it often adds a new rule. Fold it in and confirm briefly.
- Don't ask what can be decided sensibly. Decide it, and say so.

## Principles for this build

- **One tool, one truth.** One workbench, not two. The repo is the permanent record. Every version is kept and every action can be undone. Nothing ever overwrites canonical art or Frank's evidence files; Codex's draft, hash and promotion rules stay.
- **What you see is what the game plays.** Use the same engine (`src/studio/recipe.ts`) and the same sprites and metadata as the game. No second renderer.
- **For a non-technical user:**
  - plain words, no ids or JSON in the main view (they stay in "details");
  - a clear "what needs me" inbox and a status on everything;
  - one obvious next step, autosave, and an obvious Hand back;
  - nothing destructive without a clear undo;
  - large clear controls, readable at a glance.
- **Both agents can amend it.** Formats are documented (`docs/RECIPES.md` and successors), tests guard every contract, and ownership is split so changes don't collide. Codex owns the asset review side; Claude owns recipes, the engine, the checks and the game wiring; shared formats change only by agreement.
- **Independent review means independent.** Neither agent sees the other's review before writing its own. Frank sees both side by side.
- **Scale.** 325+ keeper sheets and growing; rooms, furniture and backdrop to come. Lists need search, filters and "next" navigation that doesn't slow down.
- **Security:** don't raise PINs or authentication. Frank doesn't want it for this private family game (see memory).

## State of play (11 October 2026)

**Built in the studio:**
- recipes and macros; object types with variants and an every-variant check;
- walk-through doors with the costume changing behind the open door, and a door clear area;
- whole-stride walks and whole-round loops;
- pixel join checks with Look, Bridges and Note for Codex;
- solid and cover checks against real frame pixels;
- the sound library (placeholders, drag-and-drop, trim, volume), and sounds from clip sidecars;
- route lines, ghosts, the evening light;
- in-game animation speed tweaks (Grown-ups).

**Known gaps in the studio:**
- Frank's edits stay in the database (no versions, no hand-back into the repo);
- no review records and no annotations;
- the studio asks for a PIN (Frank may want it gone: ask);
- poses lack held props (asked of Codex);
- object types come from `data/studio/categories`, not from sidecars;
- no ambience page and no lamp sequence preview;
- the game does not play recipes yet.

**Codex's side:**
- the reviewer and its hand-back queue;
- the neutral and bridge contract;
- the `KEEPER_REVIEW_WORKBENCH_BUILD` prompt (not yet run as of writing; check). It should be changed so sections 5 and 6 build on the studio. Frank has a suggested message.

**Paused, separate tasks** (not part of this work): non-linear floor progression (Frank: a brand-new task later); thought bubbles and the feelings panel (proposal in `docs/EXPANSION_DESIGN.md`).

## Questions likely to need Frank (refine after exploring; ask one at a time)

1. Where the workbench lives: one app in this repo at one address, or a separate site. Recommend one app here.
2. Where Frank's edits are saved for good. Options:
   - the website writes them straight into the repo (needs a GitHub token in Vercel);
   - they wait in a database hand-back queue that Claude or Codex pulls into the repo at the start of their next task.

   Weigh them after exploring; don't assume either.
3. Who proposes first for each new activity (Claude, Codex or either), and how "in turn" works.
4. How independent reviews are shown to Frank, and what "approve" does next.
5. What Frank uses it on: the Mac only, or the iPad too.
6. Remove the studio's PIN? (Likely yes, given Frank's view.)
7. The first delivery's scope: which tabs and which parts of the loop come first.
