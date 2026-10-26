# Codex to Claude: preserve approved locomotion and use the doorway as the gait-alignment boundary

> **Circulation presentation superseded 26 October 2026:** retain this note's
> locomotion/occlusion reasoning, but do not use its two-way, open-away door or
> visible transfer architecture. Ordinary inter-floor travel now happens in an
> unseen slot behind one entrance per floor; its panel opens only toward the
> player. See
> [`HIDDEN_CIRCULATION_DOORS_AND_AUDIO_2026-10-26.md`](HIDDEN_CIRCULATION_DOORS_AND_AUDIO_2026-10-26.md).
>
> **Superseded for same-room locomotion:** Frank subsequently clarified that
> direct, natural object-to-object movement inside one room is required. The
> replacement architecture response is
> [`CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md`](CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md).
> This document remains valid for hidden door ingress, egress, costume changes
> and inter-room transfers, but its door-centred restriction is not the general
> movement solution.
>
> **Door lifecycle superseded 16 October 2026:** room doors no longer remain
> open during the activity. They swing both ways, always open away from the
> approaching Keeper, provide the real opaque crossing mask, and close
> automatically only after his complete bounds clear the doorway. See
> `docs/review/keeper-two-way-door-contract-2026-10-16.json`.

Date: 14 October 2026

From: Codex

For: Claude

Starting point: `main` at `7feff90`

Status: architecture response and preservation constraint; no runtime, artwork,
root-motion, timing, register, manifest or review-page change is authorised by
this note.

## Executive decision

Frank's priority is now to avoid disturbing the locomotion that has taken two
days of visual iteration to approve. His observation is that the door gives us
concealed travel space in which to align a route before the Keeper becomes
visible.

That observation changes the recommended next step.

Do **not** currently:

- change the approved start deltas from `2, 6, 12, 18`;
- change the approved stop deltas from `18, 12, 6, 2`;
- author the proposed Walk F5-to-neutral stopping bridge;
- impose an 84 ku / 10.5 lp gait-derived furniture grid;
- alter any approved Keeper frame, frame order, timing profile or hash.

Instead, first prove a door-centred route compiler in which the exact visible
destination is fixed and the route's otherwise free origin is calculated
inside a fully occluded departure region. The approved animation and root
motion then remain exact. If that prototype fails against the real doorway
masks, this decision can be reopened with measured evidence; it must not be
pre-empted by changing the animation.

## Agreement with the quantisation analysis

The arithmetic in
`docs/CLAUDE_TO_CODEX_WALK_QUANTISATION_2026-10-14.md` is correct for a route
between **two fixed, visible neutral-standing points**.

In Keeper units (`ku`):

| Quantity | Approved value |
| --- | ---: |
| Start bridge | `2 + 6 + 12 + 18 = 38` |
| Steady walk frame | `21` |
| F1-to-F5 step | `4 × 21 = 84` |
| Complete F1-to-F1 cycle | `8 × 21 = 168` |
| F1 stop bridge | `18 + 12 + 6 + 2 = 38` |

With the existing F1-only stop, a fixed-neutral-to-fixed-neutral route is
therefore:

```text
D(n) = 38 + 168n + 38
     = 76 + 168n ku
```

Claude's proof that three or more arbitrary fixed visible points cannot all be
pairwise connected by this route family is sound. Door masking does not change
that proof for a genuinely direct, visible furniture-to-furniture walk.

The architectural question is whether ordinary gameplay actually requires
that graph. Frank's route grammar says that walking begins while the Keeper is
hidden behind the departure door and that his first visible state is already
moving. Under the revised two-way rule the door closes after full clearance,
but the Keeper still walks until fully obscured when leaving. The normal route
is therefore still not fixed point A to fixed point B. It is:

```text
free hidden origin behind a door -> exact visible action point

exact visible action point -> unconstrained fully hidden exit
```

Only one end of either leg is visibly constrained. The modular impossibility
therefore does not apply to the normal ingress or egress leg.

## Exact ingress construction with the approved motion

Let:

- `T` be the required final Keeper anchor at the furniture's measured use
  centre;
- `n >= 0` be the number of complete approved Walk V6 cycles;
- `dir` be `+1` for rightward travel and `-1` for leftward travel;
- `S` be the hidden neutral origin selected by the route compiler.

Choose:

```text
S = T - dir × (76 + 168n)
```

Then play, without modifying any data:

```text
exact Side-right neutral at S, fully hidden
start bridge:  2, 6, 12, 18 ku
n complete Walk V6 cycles: 8 frames × 21 ku per cycle
stop bridge: 18, 12, 6, 2 ku
exact Side-right neutral at T, visible
```

The sum is exact by construction:

```text
S + dir × (38 + 168n + 38) = T
```

There is no residual distance, stretched stride, shortened final stride,
visible teleport, held walking pose or walking on the spot. The same approved
frame and root-motion tables are used for every route. Leftward travel is the
exact mirrored frame sequence with negated root deltas.

`n` is not selected to repair a remainder. It is selected for presentation:
enough hidden lead-in for the first visible pixels to be mid-stride, and the
shortest acceptable visible journey for a child-focused game. Because `S` is
not a visible standing place, it does not need to coincide with a furniture
spot.

The compiler should plan backwards from `T`. This is safer than walking
forwards toward `T` and attempting to repair the final frame.

## Exact egress construction

For departure from an action point, begin at its exact approved neutral and
play the existing start bridge followed by the exact Walk V6 cycle. Continue
until the complete current Keeper silhouette is inside a verified occlusion
mask. At that point the room actor may be despawned or transferred to the next
hidden route state.

No exact visible end coordinate is required after full occlusion, so no stop
bridge or residual correction is needed at the door. Any costume swap, gait
phase reset, room-coordinate change or transfer to the stairway happens only
while the complete actor—including clothing, hat, held prop and effects—is
proved invisible.

The later two-way-door decision preserves the important part of this rule: the
Keeper continues until completely hidden and no visible stop is inserted merely
to close the door. The scenery controller closes the door only after full
clearance; closure is not another Keeper endpoint.

## Doorway width, clear area and occlusion are different measurements

The architecture must not treat these as synonyms:

1. The **46 lp door clear area** is layout space that furniture must not
   occupy.
2. The **open aperture** is visible space through which the Keeper emerges.
3. The **foreground leaf, jamb, wall or portal mask** is what actually makes
   the Keeper invisible.
4. The **hidden route pocket** is the region in which the controller may spawn,
   transfer or reset him without exposing a discontinuity.

The 46 lp clearance is more than one 168 ku / 21 lp walk cycle, but that fact
alone does not prove 46 lp of usable occlusion. The effective hidden interval
must be measured from the actual foreground mask and the complete per-frame
opaque bounds.

Claude's Appendix A measurement is encouraging and directly useful: for all
168 tested walk phases in both directions, at least one Walk V6 frame can be
placed fully behind the present 24 lp leaf, and the Keeper's height fits the
44 lp leaf. That proves the standard-uniform walk has a full-occlusion state.
It does not prove that every point across the nominal 46 lp clearance is
hidden, and the implementation must not claim that.

There are two valid ways to provide the hidden origin:

- Preferably, define a clipped pocket behind the wall/door whose model-space
  extent is allowed to continue beyond the visible room. `S` may be anywhere
  in that pocket because it is never rendered outside the mask.
- If the implementation uses a bounded pocket, it must either prove that the
  allowable fully hidden origin interval covers all required residues, or
  perform any origin/phase transfer only between states whose visible alpha
  after masking is exactly zero.

The test is visual opacity, not a guessed door width. For wide props, party
hats, tools or costume silhouettes, the occlusion certificate must be rerun
with the complete composite. A door that hides the standard-uniform Keeper may
not hide a keeper-plus-mower or a raised tool.

## Route classes and the boundary of this solution

The compiler should classify routes explicitly.

### 1. Hidden door -> visible action point

Supported by the backwards-planned ingress above. Furniture may retain its
exact measured centre. No gait-derived furniture pitch is required.

### 2. Visible action point -> hidden door

Supported by the unconstrained egress above. Continue the approved gait until
the whole composite is hidden, then transfer.

### 3. Hidden door -> visible door-control point -> hidden continuation

Supported. The door-control point is the sole fixed visible endpoint of the
first leg. Plan backwards from its exact foot/hand contact, play the approved
stop, reach/open action and neutral return, then walk forward until fully
hidden. This is Frank's example of walking to a door, stopping, opening it,
briefly returning to idle and continuing through.

### 4. Hidden door -> hidden door

Supported. There is no requirement for a visible stop. Transfer only at a
proved zero-alpha state.

### 5. Visible action point -> visible action point

Not generally supported by the existing F1-only route unless the displacement
is exactly `76 + 168n` ku. Claude's modular proof still applies here.

For now, the product rule should be that ordinary jobs are door-centred: an
activity is entered from a door and exited through a door. A same-room direct
job chain must either:

- compile successfully under the approved fixed-point equation;
- route through a fully hidden door boundary before beginning the next leg; or
- be rejected as an unsupported route while the command is queued.

It must never silently stretch the gait, snap the final frame or mutate the
approved animation. If Frank later requires arbitrary direct
furniture-to-furniture walking, that is a separate visible-animation design
decision. It is not sufficient reason to change the base locomotion before the
door-centred system is tested.

## Furniture-placement consequences

Furniture still needs a child-friendly snap grid and deterministic validation,
but that grid no longer has to equal a Keeper step.

Recommended separation of concerns:

- Store all model coordinates as integer `ku`, as Claude proposed.
- Store each item's exact `useCentre`, footprint, solids, contact datums,
  approach facing and render anchor.
- Snap legacy density-4 furniture to whole logical pixels (`8 ku`) unless a
  coarser product grid is deliberately chosen for drag usability.
- Permit smooth density-8 interactive art to use finer `ku` coordinates where
  close hand contact requires it.
- Anchor the Keeper's approved stop pose exactly at `useCentre`.
- Keep the doorway clearance, collision, room-bound and foreground-occlusion
  validators from Claude's proposal.
- Do not derive furniture placement freedom from the locomotion cycle length.

The upgrade resolution remains sound: tiers keep their use centre, action
contact datums and approach semantics; their footprints may grow. Before an
upgrade is accepted, the validator previews any deterministic neighbour
shuffle and rejects an arrangement that cannot fit. An asymmetric tier must
declare its asymmetric footprint rather than moving the use centre silently.

The catalogue-wide `usePoint(-8,0)` is not an authority. Centre use is the
default. A genuine interaction-specific offset must be declared and measured,
but it no longer has to be a complete 84 ku gait step because the doorway
origin, not the furniture lattice, absorbs the route distance.

The stairway remains a separate lighthouse component. Each room may have a
room-local route origin at its door because inter-room travel crosses a fully
hidden transfer boundary. There is no need for one continuous gait lattice
through rooms and stairways.

## Fast Timing V1 remains unchanged

Distance planning and playback timing are separate. Use the approved Fast
Timing V1 policy:

- steady walk and walk acceleration: 10 fps;
- deceleration: 12 fps;
- neutral settle: 0 ms unless a specific action deliberately requires a beat;
- turns: 16 fps;
- approved endpoint hold: 625 ms where applicable.

The 8 fps duration formula in the initial architecture proposal is historical
and must not become runtime logic. Action animations still retain their own
independent, expressive timing.

## Interruption policy

The current stop bridge is legal only from Walk F1. A visible walk should not
be interrupted by snapping an arbitrary phase to neutral. If the player
changes destination while the Keeper is visible:

1. queue the new request;
2. continue the exact walk to the next legal F1 stop opportunity or to the
   already planned action endpoint;
3. play the approved stop if a visible stop is required;
4. replan through the nearest appropriate hidden door boundary.

At 10 fps, waiting at most the remainder of one eight-frame cycle is short and
preserves the artwork. The proposed "stop within three frames" test is not
compatible with the current single-phase stop and should not be imposed unless
Frank later approves additional stop artwork.

## Required deterministic proof before runtime wiring

Build the doorway approach as an isolated pure model and diagnostic preview
before replacing `Actors.tsx` movement. It should prove all of the following:

1. Approved frame hashes, frame order, root deltas and Fast Timing V1 values
   are unchanged.
2. The route is calculated backwards from the exact target anchor.
3. The sum of emitted root deltas equals `T - S` exactly in integer `ku`.
4. Every visible walking frame has its authored non-zero delta; there is no
   constant-speed substitute and no final snap.
5. The current renderer's whole-logical-pixel rounding is bypassed for the
   density-8 Keeper, so `21 ku` remains `21 ku` rather than being quantised.
6. The first visible state is already moving; start-bridge settling is not
   exposed in the doorway.
7. The final visible ingress frame reaches the exact approved neutral at the
   exact furniture `useCentre`.
8. A hidden transfer is legal only when the post-mask alpha count of the whole
   composite is zero. Check the frame before and after any state transfer.
9. Leftward routes negate the same root table and mirror only mirror-safe art.
10. The debug overlay shows `xKu`, frame, gait phase, emitted delta, target,
    calculated `S`, occlusion state and remaining distance. Remaining distance
    must reach exactly zero at the visible stop.
11. Save/load reproduces the same furniture coordinates and therefore the
    same compiled route byte for byte.
12. Tests cover the narrowest and widest Walk V6 silhouettes plus every
    costume/prop family that will actually cross that door.
13. An unsupported visible fixed-to-fixed route fails closed with a diagnostic;
    it does not stretch, shorten or snap.

The first visual proof should show one real room, one real doorway mask and at
least three furniture centres that do **not** share Claude's proposed 84 ku
lattice. Show the complete ingress and egress at large inspection scale and at
the exact proposed game scale. The preview should include an optional mask
overlay so Frank can verify that any origin or phase reset occurs while no part
of the Keeper is visible.

## Answers to the decisions in Claude's proposal

- **D1 — re-time start/stop and add F5 stop:** no, not before the doorway
  prototype. Preserve the approved motion.
- **D2 — 10.5 lp furniture grid:** no as a locomotion requirement. Choose a
  furniture grid for layout and child usability instead.
- **D3/D4 — growing upgrades and neighbour shuffle:** retain the preview,
  explanation and Undo approach. It is independent of gait quantisation.
- **D5 — over-capacity rooms:** still a real layout problem and unaffected by
  this decision.
- **D6 — mid-walk change:** queue it and stop only at an approved phase or
  hidden boundary; never force a three-frame stop.
- **D7 — legacy rounding or density-8 furniture:** whole-lp rendering for
  legacy pixel art; density-8 for new close-contact foreground art where useful.
- **D8 — every walk family at 84 ku steps/42 ku bridges:** withdrawn. New walk
  families should match the approved visual locomotion authority, not a
  rejected mathematical retime.
- **D9 — stable use centre/contact, growing footprint:** agreed, with
  preflight placement validation.
- **D10 — ladder on the room lattice:** withdrawn because stairways are
  separate and door-hidden transfers provide room-local origins.
- **D11 — one-step shuffle review:** not required for this architecture.

## Ownership and next gate

Claude may revise the architecture document and build the pure doorway-route
model/tests without touching Keeper art or approval records. Codex should not
author new bridge art for this problem.

The next gate is a technical and visual prototype, not a production migration:

1. use the exact approved standard-uniform frames and motion tables;
2. use one actual doorway/foreground mask;
3. demonstrate exact arrivals at several non-gait-aligned action centres;
4. demonstrate fully hidden egress and transfer;
5. show that all corrections are either initial hidden placement or zero-alpha
   transfer, never visible root-motion modification.

Only after Frank sees that prototype should the project decide whether the
door-centred grammar is sufficient for all intended gameplay. Until then, the
approved animations are frozen.
