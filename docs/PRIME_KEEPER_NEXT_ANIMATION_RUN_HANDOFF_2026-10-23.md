# Prime Keeper: next animation run handoff

Checkpoint: 23 October 2026

Purpose: the authoritative starting point for the next standard-uniform Prime
Keeper animation run. A fresh Codex task must be able to continue from this
file without reconstructing decisions from chat history.

## Read these first

1. `AGENTS.md` and `docs/DEPLOYMENT.md`.
2. `docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json` —
   Frank's hash-pinned approval of all ten animations on the V12 page.
3. `data/keeper_prime_animation_drafts_v12.json` — the exact approved frame
   order, timing, endpoints, per-frame redraft slots and asset hashes.
4. `docs/PRIME_KEEPER_EXPANDED_ANIMATION_REVIEW_V12_2026-10-23.md` — the final
   rear-task construction and verification boundary.
5. `data/keeper_prime_animation_gaps.json` — the ordered remaining work.
6. `docs/PRIME_KEEPER_RESTART_HANDOFF_2026-10-17.md` when older Prime movement
   authorities or historical decisions are needed.

When an approval or rejection record exists in `docs/review/`, it outranks a
status string embedded in a pre-approval immutable manifest. Never infer the
current verdict from a filename or old page label.

## Exact Prime Keeper contract

The character remains the adult, restrained, slightly rotund approved Prime
Keeper: blue cap, white beard and separate moustache, solid dark rectangular
eyes without glints, readable closed mouth, bright blue standard jumper with
one broad pale band, storm-blue trousers and matching boots. Do not make him
younger, cuter, slimmer, taller, rougher or more expressive by default.

Geometry and registration:

- logical cell: 32 × 40 px;
- authoring cell: 256 × 320 px at 8 px per logical pixel;
- anchor: x128, y320;
- cap top: y18;
- opaque floor datum: y316;
- every actor, garment, prop, effect and detached pixel must remain wholly
  inside its declared cell with a transparent safety gutter at every shared
  edge.

Approved standard-uniform colour locks:

- jumper blue: RGB 0, 108, 230;
- jumper cream: RGB 251, 232, 206;
- trousers: RGB 63, 75, 112;
- boots: RGB 63, 74, 111.

V12 review-facing authorities:

- front: `287c42001ae5c757ee93f46ae0d627e8e1511dbdabae6d11739348ea411e809c`;
- back: `e6520aab48100c44aabdb0825c9424dbe35bffb2587b5270898e5214db2038df`;
- side-right: `a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3`.

The front and back hashes above are the feedback-corrected review references;
the side-right hash is the unchanged approved authority. The canonical source
hashes remain in the V12 manifest and must not be overwritten.

## Binding visual direction

Frank's ligne-claire direction remains exact:

1. one even line weight everywhere;
2. a line only where there is a real edge — no hatching or texture strokes;
3. every area closed and filled with one flat colour;
4. no gradients, shine or glow; at most one rare flat shadow tone;
5. show the object's own colour under even daylight;
6. draw objects accurately, like Hergé's cars and machines, simplifying by
   leaving detail out rather than making them cute;
7. preserve clarity at 64 px; and
8. use black only where the thing is black, with marks drawn in the same line.

Jumper and boots must match the Prime authorities in every standard-uniform
frame. A different outfit needs its own consistent construction and palette;
it is not permission to drift the body, face or proportions.

## What this run achieved and Frank approved

Frank approved all ten complete animations on the V12 page: 162 frame
occurrences at the exact hashes in the approval record.

| Sequence | Frames | Approved result |
| --- | ---: | --- |
| Lift entry, ride handoff and exit | 7 | Pointless intermediate removed; corrected bright jumper; walking-back to standing-front handoff. |
| Front-door approach, open and pass through | 6 | Complete side-right approach and passage route. |
| Cook at counter | 8 | Corrected bright jumper endpoints; seven intact rear cooking poses plus return. |
| Brush teeth at basin | 8 | Corrected bright final jumper; complete rear basin loop. |
| Friendly wave to camera | 6 | Corrected bright front endpoints; clean isolated front wave. |
| Collect broom, sweep and recover | 11 | Isolated complete Keeper/broom action candidate accepted as shown. |
| Side leisure: sit, hold and stand | 15 | Approved-component side-facing seating choreography. |
| Turn, sit, hold, stand and return | 31 | Approved-component rear seating route. It is intentionally named for what it shows; writing and a diary prop are not present. |
| Front seat consumer route | 29 | Complete side-right → front seat → side-right choreography. |
| Rear task: turn, work and return | 41 | Final V12 route with intact cooking poses replacing the failed layered work section. |

The immutable live review remains:

- current route: `https://lighthouse-keeper-mu.vercel.app/prime-keeper-animation-drafts`;
- exact V12 route: `https://lighthouse-keeper-mu.vercel.app/prime-keeper-animation-drafts-v12`.

Every frame keeps a stable `redraftSlot`. The review page retains per-animation
play, pause, stop, previous/next, direct frame selection, global controls,
optional Prime ghost, browser-local frame notes and the sequence-combination
sandbox. Approval does not remove the ability to redraft an individual frame:
any later amendment must create V13 or another new version and preserve V12.

## Corrections and lessons that must not be repeated

- V3 fixed the passive front/back jumper colour, removed the redundant lift
  frame and renamed the seated rear route to describe the motion it actually
  contains.
- Rear-task V4 reintroduced detached black fragments and two competing jumper
  seams.
- V5's hard waist cut made the join worse.
- V6 still contained two ribbed jumper bands.
- V7 removed the duplicate band but stepped both side outlines inward.
- V8 exposed a fixed dark trouser edge below the moving hem.
- V9 still showed a separate dark waistband line.
- V10 abandoned the incompatible torso/lower-body splice and retained the
  approved body, but its row-125 arm boundary cropped sleeves and raised hands.
- V11 restored the complete arms and disabled the default ghost, but the arm
  layers retained their old inner sleeve and jumper boundaries. Those lines
  broke the torso and cream stripe.
- V12 stopped compositing separate arms and torso. Rear-task positions 11–31
  are complete cooking frames 2–8, reused byte-for-byte as three seven-frame
  work cycles. This is the approved solution.

General lesson: exact alignment cannot reconcile two structurally different
drawings. Do not splice a generated torso to authority legs, overlay arms that
still contain torso boundaries, or solve a bad join by accumulating masks and
seams. Reuse a complete approved pose where possible; otherwise redraw one
coherent full-frame Prime pose from the approved authorities.

## Approval and runtime boundary

V12 is now an approved review authority. This checkpoint records the decision
without rewriting the immutable V12 manifest, frames, strips or page.

This documentation change does not install the ten sequences into the runtime
animation bank. Runtime integration must be a new, versioned delivery with its
own frame isolation, metadata, endpoint, binding and gameplay tests. Audit for
deduplication first:

- side leisure and rear diary seating already use installed component routes;
- front seating source is installed but lacks a matching gameplay consumer;
- the game already has a generic rear-work loop;
- lift, door, cooking, tooth-brushing, wave and the approved broom route need
  explicit packaging and/or gameplay bindings rather than duplicate art; and
- the diary approval covers a hold route, not a writing performance.

Do not report an approved sequence as “in the game” until the runtime registry,
state machine, object/prop anchors and actual gameplay consumer have all been
verified.

## Ordered next animation run

Pets and visitors remain skipped, per Frank's direction. Work in this order:

1. **Integrate the approved V12 batch safely.** Map each accepted sequence to
   existing runtime clips or add a new versioned sprite only where genuinely
   absent. Bind lift, front door, cooker, basin, wave and broom consumers.
   Preserve the exact V12 frame hashes and do not duplicate already-installed
   seating or turn art.
2. **Finish already-installed consumers.** Add the ladder route when its layout
   is available; bind darts with board/dart ownership; bind the approved front
   seat route; add left seating only when an actual interaction needs it.
3. **Food and kitchen.** Redraw isolated fridge-open/take-snack/eat frames;
   create toast, carry, serve and eat endpoints. The overlapped snack source is
   choreography evidence only and must not be cropped into production cells.
4. **Bed and rest.** Create complete bed entry, sleep/nap loop and exit. The
   overlapped bed source must be rerendered as isolated full poses.
5. **Bathroom.** Build basin washing and discreet loo entry, performance and
   exit routes; reuse the approved tooth-brushing route where appropriate.
6. **Desk, housework and lamp room.** Add real diary-writing hand motion and a
   separately owned diary/pen; desk tidy; basic/upgraded hoover; lamp light and
   polish; telescope use. Held-tool proxy bodies remain motion evidence only.
7. **Solo phone and reactions.** Build phone call/order/answer, then bow, dance,
   sway, shake, wobble, jump, think, flop, spin and shrug. Wave is complete.
8. **Outside and unlocked rooms, excluding pets/visitors.** Fishing, gardening,
   shopping, aquarium, weather, radio, secret computer and gadgets.
9. **Costumes last.** Bathrobe, pyjamas, sou'wester, swimming/scuba,
   instruments, sports, seasonal and mood variants only after the standard
   Prime action grammar is stable.

## Required method for the next run

1. Start from the exact facing authority and fixed dimensions above.
2. Treat historical or rejected frames as choreography evidence only.
3. Prefer complete coherent body drawings; keep props/effects separately owned
   wherever gameplay needs independent positioning or state.
4. Register floor, root, head, beard, jumper band and garment colours before
   accepting motion polish.
5. Keep every proposal in a new versioned draft directory. Record original and
   candidate hashes and expose predecessor/candidate comparison.
6. Preload and decode all unique frames before enabling playback.
7. Verify cell dimensions, transparent gutters, ownership, palette, endpoints,
   frame metadata and strip geometry deterministically.
8. Review at enlarged, gameplay and literal scale with pause, stop, frame-step,
   ghost and per-frame redraft notes.
9. Record Frank's decision externally under `docs/review/`; never rewrite an
   immutable approval authority.
10. Promote only under a separately authorised integration task, then verify
    the actual in-game route end to end.

## Verification commands

```sh
npm run verify:keeper-prime-drafts
npm run verify:review-archive
npm run typecheck
npm run build
```
