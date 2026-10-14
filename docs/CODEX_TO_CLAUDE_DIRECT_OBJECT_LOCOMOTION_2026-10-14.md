# Codex to Claude: direct object-to-object locomotion and the universal action anchor

Date: 14 October 2026

From: Codex

For: Claude

Starting point: `main` at `db0bbaf`

Status: revised architecture direction after Frank clarified that the Keeper
must be able to move naturally between activities in the same room. This note
authorises analysis and new versioned review candidates only. It does not
approve a root-motion change, new bridge artwork, runtime migration, Final-lane
entry or production promotion.

## Decision that changes the architecture

Direct visible movement between two objects in the same room is a requirement.
The Keeper must not routinely leave and re-enter a room merely to realign his
gait. That would be visibly artificial and would make the room feel like a set
of disconnected activities rather than one coherent space.

The doorway remains useful for:

- beginning a walk while the Keeper is still concealed;
- ending an egress after the complete Keeper is concealed;
- costume and prop-family changes under full occlusion;
- transfers between rooms and the separate stairway.

It is not the primary solution for same-room action-to-action movement.

This note therefore supersedes the architectural recommendation in
`docs/CODEX_TO_CLAUDE_DOORWAY_GAIT_ALIGNMENT_2026-10-14.md`. That earlier note
remains valid technical history and still governs hidden ingress/egress, but
its proposed door-centred restriction is rejected for ordinary same-room
movement.

## Why a grid alone cannot repair the current route

The current approved standard-uniform movement uses:

| Quantity | Approved value |
| --- | ---: |
| Start bridge | `2 + 6 + 12 + 18 = 38 ku` |
| Steady walk frame | `21 ku` |
| F1-to-F5 half-cycle / one step | `4 × 21 = 84 ku` |
| F1-to-F1 cycle | `8 × 21 = 168 ku` |
| Existing F1 stop bridge | `18 + 12 + 6 + 2 = 38 ku` |

With only the existing F1 stop, a fixed visible standing point can reach
another fixed visible standing point only at:

```text
38 + 168n + 38 = 76 + 168n ku
```

No uniform furniture grid can make every pair of three or more points satisfy
that equation. If one grid interval worked, twice that interval would also
have to leave remainder 76 modulo 168, which is impossible.

Adding an opposite-foot F5 stop without changing the bridges would expand the
reachable distances to:

```text
76 + 84n ku
```

That still cannot make all multiples of one grid pitch reachable because the
fixed start-plus-stop overhead is 76 rather than a multiple of the 84 ku step.

There is therefore no furniture-placement trick that preserves all current
motion numbers while also allowing every object-to-object journey. Eight ku of
route distance must be accounted for somewhere.

## Recommended resolution: one 84 ku locomotion lattice

Use one room-local lattice with a pitch of:

```text
84 ku = 10.5 logical pixels = one F1-to-F5 step
```

Every standing interaction anchor in that room lies on this lattice. Make the
start and stop bridge totals 42 ku each:

```text
proposed start: 3, 7, 13, 19 = 42 ku
proposed stop: 19, 13, 7, 3 = 42 ku
```

The exact approved neutral and Walk V6 frames remain unchanged. This proposal
changes only their world-translation schedule. The difference from the
approved start is deliberately distributed across all four moving rows:

| Bridge row | Approved `dx` | Candidate `dx` | Approved cumulative | Candidate cumulative | Cumulative change |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 3 | 2 | 3 | +1 ku |
| 2 | 6 | 7 | 8 | 10 | +2 ku |
| 3 | 12 | 13 | 20 | 23 | +3 ku |
| 4 | 18 | 19 | 38 | 42 | +4 ku |

The per-row velocity change is exactly +1 ku. The largest cumulative position
change is 4 ku, or half one logical pixel, at the endpoint. The acceleration
difference pattern remains exactly `+4, +6, +6`; this is why `3, 7, 13, 19`
is preferred over concentrating the additional motion late.

This is not approved merely because the difference is small. It must be a new
versioned root-motion candidate, compared against the untouched approved route
at large inspection scale and exact game scale.

## The required opposite-foot stop

Author one additional bridge from exact approved Walk V6 F5 to the exact
approved Side-right neutral. It should contain three controlled intermediate
poses between those exact authorities, matching the existing F1 bridge's
length and proposed 42 ku root distance.

It must not be produced by blindly mirroring or swapping legs in the F1 bridge.
The side view has explicit near/far limb ownership, boot overlap, arm
occlusion and weight transfer. Use the KP Rig for limb lengths and contacts,
the exact Walk V6 F5 for the entry pose, and the exact approved neutral for the
endpoint. Preserve a super-smooth source and the transparent registration
gutter.

The reverse may be registered as neutral-to-F5 for phase-aware starts, but the
minimum controller only needs the ordinary neutral-to-F1 start plus phase-aware
F1/F5 stops.

The existing F1 stop bridge remains immutable and recoverable. The F5 bridge
is an addition, not a replacement.

## Proof that every pair of grid points then works

Let two interaction anchors be `k` grid spaces apart, where `k >= 1`.

The route is:

```text
42 ku start
+ 4(k - 1) steady walk frames × 21 ku
+ 42 ku stop
```

Therefore:

```text
distance = 42 + 84(k - 1) + 42
         = 84k ku
```

The stop variant is selected from parity:

| Grid distance | Steady frames after start | Arrival phase | Stop bridge |
| ---: | ---: | --- | --- |
| 1 | 0 | F1 | F1 -> neutral |
| 2 | 4 | F5 | F5 -> neutral |
| 3 | 8 | F1 | F1 -> neutral |
| 4 | 12 | F5 | F5 -> neutral |
| odd `k` | multiple of 8 | F1 | F1 -> neutral |
| even `k` | 4 modulo 8 | F5 | F5 -> neutral |

The same rule works in reverse and for mirrored left travel. There is no
stretched stride, shortened final stride, stationary gait frame, overshoot,
backtracking, door detour or visible snap.

## Universal action-anchor contract

The locomotion grid should simplify action authoring rather than leak room
distance into every action.

Every interactive object declares one or more `keeperUseAnchor` records. A
standard standing anchor contains:

- room-local `xKu`, exactly on the 84 ku lattice;
- floor `y` / foot baseline;
- arrival facing;
- exact named entry pose;
- exact named exit pose;
- outfit and held-prop state;
- object-relative hand, seat, surface or tool contacts;
- permitted left/right mirroring;
- the action's foreground and occlusion rules.

For the common empty-handed case, the complete contract is:

```text
exact locomotion stop neutral at the lattice anchor
-> optional zero-root turn
-> optional sit/crouch/reach or prop-acquisition bridge
-> action entry / loop / exit
-> reverse prop/posture/facing bridge
-> exact same locomotion neutral at the same lattice anchor
```

The action may move the head, torso, hands, feet or complete body as its
performance requires. Its internal poses do not sit on the movement lattice.
Only its registered ingress and egress seam must return to the declared anchor
without residual translation.

This is not an additional aesthetic restriction: exact seam poses, scale,
floor anchor and reversible action routes are already mandatory. The lattice
adds a world-coordinate guarantee to that existing endpoint contract.

### Standing side actions

Stop on the side neutral at `keeperUseAnchor`, perform the action, and return
to the byte-identical side neutral at the same anchor.

### Front- or back-facing actions

Stop on the side neutral at the anchor, use an approved zero-root facing turn,
perform the action, reverse the turn, and recover the same side neutral and
anchor. Turning must not change the grid position.

### Seated actions

The object's standing approach anchor lies on the lattice. The sit bridge
owns the movement from that standing anchor to the measured seat contact and
the stand bridge returns exactly to the same standing anchor. The chair's seat
height and horizontal seat datum remain object-relative; the walk controller
does not infer them.

### Crouched, prone and environment actions

The posture bridge begins from the registered standing anchor and returns to
it. A special environment exit may declare a different named anchor only when
that is an intentional reviewed route, such as a water edge or ladder landing.

### Held-prop and carry routes

An action that ends holding a cake, meal, shopping bags, mug or tool does not
pretend to end empty-handed. It ends on a registered `stand-side+prop` or
`carry-ready+prop` pose at the same lattice anchor. Any visible carry-walk
family must ultimately obey the same 84 ku step and 42 ku bridge geometry, or
must have its own explicitly reviewed route with equivalent endpoints.

Prop acquisition and release stay declared frame events. A held prop never
appears merely because the controller changed clips.

## Furniture and room-layout implications

Only the Keeper interaction centre snaps to the 84 ku lattice. Furniture
width, footprint and artwork do not become 10.5-pixel tiles.

- An item may be any measured width.
- Its footprint may extend asymmetrically around the interaction centre when
  the artwork genuinely requires it.
- Tier upgrades retain the same `keeperUseAnchor`, approach semantics and
  contact datums while their footprints may grow.
- A larger tier runs the placement validator before purchase and may propose a
  deterministic neighbour shuffle with Undo.
- Legacy density-4 furniture may render on the nearest whole logical pixel;
  smooth density-8 art may render at the exact half-pixel lattice position.
- The room's lattice origin is room-local and should be selected against its
  real doorway and required furniture set. It need not continue through the
  separate stairway or other rooms because those transfers are door-hidden.
- A visible door-control standing point belongs on the room lattice if the
  Keeper can walk to it directly from room objects.

The cost is genuine: 10.5 lp is a coarse placement pitch. Before it becomes a
runtime contract, Claude should run the kitchen, living room, bedroom/en-suite,
weather station and every currently over-capacity room through the placement
validator using real measured footprints. A mathematically reachable layout
that cannot physically fit the intended furniture is not acceptable.

If the pitch proves too coarse, that is an explicit product/art decision. It
must not be hidden by silently stretching strides. A finer universal lattice
would require additional visually natural stop phases and possibly shorter
movement bridges, increasing art and review scope.

## Rejected ways to hide the missing 8 ku

Do not distribute a different remainder across each route. That is a stretched
stride and makes the same animation travel differently depending on furniture
placement.

Do not give every action different entry and exit standing points merely to
absorb the mismatch. With an F5 stop but unchanged 38 ku bridges, each action
would need direction-dependent ports separated by 8 ku. That would push
locomotion arithmetic into every sit, stand, turn, prop handover and action
family.

Do not add a universal visible 8 ku neutral shuffle unless the distributed
42/42 candidate fails visual review. A separate one-logical-pixel adjustment
is more likely to read as a foot slide than four tiny changes distributed
through existing moving poses.

Do not solve a same-room route by making the Keeper walk past the object, turn
around or leave through the door and re-enter. These are mathematical workarounds,
not natural character movement.

## Timing remains independent

Fast Timing V1 still governs transition playback:

- walk and acceleration: 10 fps;
- deceleration: 12 fps;
- neutral settle: 0 ms;
- turns: 16 fps;
- endpoint hold: 625 ms where applicable.

Changing root distance does not authorise changing frame bytes, frame order or
fps. Action entry, loops, exits, comic reactions and prop choreography retain
their independently approved performance timing.

## Review sequence and rollback boundary

Proceed one gate at a time.

1. **Root-motion comparison only.** Create a new versioned candidate that uses
   the exact approved F1 bridge pixels twice: current `2, 6, 12, 18` beside
   proposed `3, 7, 13, 19`. Show large and exact game scale, frame stepping,
   ghosted foot/contact overlays and cumulative root positions. Do not alter
   the existing approval record.
2. **Frank reviews the movement.** If the half-pixel cumulative change creates
   visible skate or cadence damage, reject the candidate and retain the
   approved schedule.
3. **Opposite-foot bridge only after gate 2.** Author the F5-to-neutral bridge
   in a separate versioned draft and review it as an isolated stop/start plus
   in a two-grid-space route.
4. **Lattice proof.** Demonstrate exact one-, two-, three- and four-space
   journeys. Include both directions and alternate F1/F5 stops.
5. **Real-room proof.** Show direct object-to-object routes among at least four
   actual furniture anchors, including a seated action and a front/back action.
6. **Only after approval**, Claude may implement the pure placement and route
   model. Runtime integration, Workbench Final and production promotion remain
   later and separate gates.

Rollback is deletion of the new versioned candidates and their new review
pages. Approved Walk V6, stop -> walk -> stop V1, Fast Timing V1, their
immutable review exports and all production art remain byte-identical.

## Deterministic verification requirements

The candidate and later compiler must prove:

1. Every reused PNG hash is the exact approved authority hash.
2. Current and candidate root-motion tables are both retained and labelled.
3. Candidate bridge totals are exactly 42 ku in both directions.
4. Every steady frame remains exactly 21 ku.
5. F1 and F5 stop bridges end on the same exact neutral frame and anchor.
6. The F5 bridge changes nothing outside its declared new draft.
7. The four bridge rows remain inside their cells with transparent gutters.
8. For every tested `k`, emitted distance equals `84k` exactly.
9. Odd `k` selects F1 and even `k` selects F5 deterministically.
10. Left routes negate the same deltas and use only mirror-safe art.
11. No locomotion pose has zero movement and no endpoint is snapped.
12. Turns have zero root motion and preserve the lattice anchor.
13. Every action recipe returns to its declared anchor or explicitly declares
    a reviewed held-prop/environment endpoint.
14. Placement validation rejects overlaps, door-clearance violations,
    unreachable use anchors and unsafe foreground occlusion.
15. Strip, sidecar, root-motion, route and public-review records agree.
16. Approved source, Final, runtime and production hashes remain unchanged
    until Frank gives a later explicit promotion instruction.

## Direct answers to Claude

- Direct same-room movement is required; the door-only hub model is rejected
  as the ordinary route architecture.
- The proposed 42 ku start/stop arithmetic is the correct candidate to test.
- `3, 7, 13, 19` is the preferred split because it preserves the approved
  acceleration shape while adding only 1 ku to each moving row.
- A dedicated F5-to-neutral bridge is required if gate 1 is visually accepted.
- All action families should converge on a universal registered standing or
  carry-ready anchor. Their internal performance remains unconstrained.
- Furniture interaction centres use the 84 ku lattice; artwork widths do not.
- The doorway still handles hidden entry, exit, costume changes and room
  transfer, but not same-room gait arithmetic.
- Nothing is promoted or mutated until Frank has reviewed the root-motion
  comparison, the F5 bridge and real multi-object routes separately.
