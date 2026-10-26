# Hidden circulation, room doors and travel audio

Date: 26 October 2026
Status: current travel/occlusion/audio authority; room and door geometry is
owned by `docs/CODEX_BRIEF.md`

This decision replaces the earlier player-facing stair, ladder, spiral-stair
and visible lift-shaft proposals. Their review pages, geometry and approved
Keeper animation assets remain historical evidence; they are not the target
presentation for ordinary travel between lighthouse floors.

The later 26 October graphics brief supersedes this document's earlier narrow
pixel-module, tapered-shell and no-en-suite assumptions. Production room art is
straight-sided and uses the exact 1536 × 512 master-module grid.

## What the player sees

- The lighthouse remains a straight-on doll's-house cutaway. Stairs, landings,
  a lift car and a lift shaft are never drawn inside the rooms or beside them.
- The hidden stairway runs vertically inside the tower wall. It is never a
  visible room module, recess or shaft.
- The leftmost 1536 × 512 module on every floor has one identical plain wooden
  door in its LEFT wall. Its empty walk-in zone is always x=32–256. Extra width
  modules join through an open doorway in a 32 px divider and never gain
  another stair door or walk-in zone.
- The ground floor additionally has its arched exterior front door on the back
  wall within the walk-in zone. The top-floor bedroom includes an en-suite
  partition near its right end; the new production module is wide enough for
  it. The V4 pixel experiment's no-en-suite decision is rejected history.
- In the straight-on elevation the closed left-wall stair door stays visually
  minimal and flat; its panel becomes visible only while it opens toward the
  player. Do not introduce an inset, recess or perspective surface.
- The open panel is flat, opaque foreground scenery. Layer order is
  `room shell -> Keeper -> open door panel`, so it completely covers the
  Keeper as he crosses. It must not introduce an angled wall, floor, ceiling,
  recess or other perspective cue.

## Hidden travel and costume changes

For stair travel, the Keeper walks behind the open departure door, becomes
fully occluded, travels between floors off-stage, and emerges through the
destination door. No upstairs/downstairs body animation is shown.

When the lift is unlocked, it occupies the same unseen circulation slot. The
room entrance changes only through a subtly more engineered jamb treatment;
the lift car, shaft and machinery remain off-stage. The Keeper walks into the
entrance, changes costume inside the hidden lift when required, and emerges at
the destination. The lighthouse expansion may widen the straight-sided tower
and pull the island apart, but it does not expose a lift module.

## Stair-travel sound placeholder

The stable placeholder id is `footsteps_stone_stairwell`. It is seeded in the
Recipe Studio sound library by `data/studio/sound_placeholders.json`. Until a
real file is uploaded under that id, the Studio plays its normal deterministic
placeholder blip; no synthetic production footstep file has been added.

Audio brief:

- measured Keeper bootfalls on worn stone steps;
- a short, enclosed tower echo with a little vertical resonance;
- warm and architectural, not cavernous, frightening or exaggerated;
- no voices, music, stair creaks or lift machinery in this cue.

Playback contract:

1. Start only after the departure door has completely hidden the Keeper.
2. Keep one uninterrupted cadence across intermediate floors; do not restart
   the sound at every floor boundary.
3. Let duration and footfall count follow the number of floors crossed.
4. Stop before the destination door opens and the Keeper reappears.
5. Do not play it for same-floor walking, the doorway crossing itself or lift
   travel.
6. Stop immediately if travel is cancelled, replaced or force-completed.

A future lift sound, if wanted, is a separate cue. This decision does not
invent one.

## Current implementation boundary

The sound placeholder is available for upload and preview in `/studio`, but
the playable game does not yet have its shared runtime audio engine or the new
hidden-circulation state. Current visible stair movement and the dashed lift
shaft are temporary runtime stand-ins, not design authority.

When runtime travel is rebuilt, `src/ui/Actors.tsx` is the current owner of the
`stairs-up`, `stairs-down` and `lift` motion boundary. The eventual audio
service should start this cue on entry to either stair motion, preserve it
across consecutive floor segments, and stop it on walk, idle, lift, arrival,
interruption, pause, hidden browser tab or unmount. Do not attach the cue to a
Keeper sprite sheet: it belongs to the off-stage travel state.
