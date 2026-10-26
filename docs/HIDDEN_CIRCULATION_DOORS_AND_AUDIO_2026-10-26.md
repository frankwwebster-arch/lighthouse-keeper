# Hidden circulation, room doors and travel audio

Date: 26 October 2026
Status: current design authority

This decision replaces the earlier player-facing stair, ladder, spiral-stair
and visible lift-shaft proposals. Their review pages, geometry and approved
Keeper animation assets remain historical evidence; they are not the target
presentation for ordinary travel between lighthouse floors.

## What the player sees

- The lighthouse remains a straight-on doll's-house cutaway. Stairs, landings,
  a lift car and a lift shaft are never drawn inside the rooms or beside them.
- A narrow concealed circulation slot runs vertically behind the room edge.
  It is architectural negative space, not another visible room module.
- Every ordinary floor has exactly one entrance between that concealed slot
  and its room. There are no doors between width modules.
- The ground floor additionally has the exterior front door. The bedroom is
  the sole ordinary-floor exception: it has one further door into the en-suite
  on its right.
- The closed circulation entrance shows only its slim side jamb. The door
  panel itself is visible only while it opens toward the player.
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
the destination. The lighthouse expansion may widen the tapered building and
pull the island apart, but it does not expose a lift module.

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
