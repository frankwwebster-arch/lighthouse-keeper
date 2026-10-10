# Keeper scale audit

This is the permanent, reproducible audit of every keeper sheet against the untouched approved original `keeper_walk`. Frank's saved visual width and height are the production sizing authority; the original remains the identity, anatomy and contact reference. The audit deliberately does **not** use the outer silhouette as character scale except for directly comparable full-body walks that Frank has not visually resized: hats, tools, raised arms, water and furniture can change that box without changing the keeper.

- 191 keeper sheets inspected.
- 173 animation sheets accepted for review; 18 obsolete modular/reference sheets excluded.
- 1475 individual frames measured.
- 81 sheets explicitly rebuilt or anatomy-normalised in this pass.
- 0 unresolved original-comparison failures (the audit command refuses to succeed unless this is zero).
- Canonical upright anatomy: skull top 32.5 logical pixels above the walking floor, shoulders 24.5, hips 14.5, seat contact 11.
- Allowed landmark drift: 0.5 logical pixel; core-width drift: 1 logical pixel. Pose contacts are checked independently from body scale.

## Measurement method

The approved original is printed first in every contact-sheet row. Frank's saved width/height choice is shown at its delivered production size and is never failed for disagreeing with an automatic ratio. Directly comparable walks without a saved visual resize must measure 0.960–1.040 of the original skull-to-sole silhouette; unobscured side walks without a saved visual resize must also remain within 1 logical pixel of its median 20 px-above-floor torso scan, or the command fails. Other upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is recorded as evidence only and cannot overrule Frank's visual sizing.

## Interactive comparison

Open [the sizing and transition review](review.html) to inspect all 173 accepted animations beside the untouched `keeper_walk` authority. Review-state filters cover Needs my input, Happy, Awaiting new draft review, Review later, Unreviewed and Has Codex response. In focused mode Previous/Next and the Left/Right keys stay inside the selected filter and wrap from its final result to its first.
The pinned reference can show standing side/front/back or sitting side/front/back identity ghosts. These fixed ghosts are anatomy comparisons, not a replacement for each reviewed clip's saved production size. In upright standard-cap poses the gold badge crossing the blue skull-top guide is a calibrated visual proxy; tilted, bent, seated, crouched, horizontal, bare-headed and alternate-headwear poses still require anatomical landmarks.
Each card retains precise size, position, rotation, opacity, ghost, frame-step and 1–20fps timing controls. The imported production pass starts those viewer transforms at neutral because accepted geometry and cadence are already baked into the delivered sprite and manifest. Comparison settings remain visual aids until saved/exported as a later review proposal.
Every card has Frank's notes and decision controls plus a read-only Codex response field. Every Awaiting new draft review card has a specific response naming the delivered change; responses also state any genuine qualification rather than implying that an unmade change was completed. Orange cards have unsaved changes; saved happy, new-draft and later-review cards use distinct status colours.
`keeper-scale-choices.json` version 9 exports the complete review register, current review status and Codex response for every animation as well as any new per-card proposals. Export remains blocked while a card has unsaved edits. Import validates exact `keeper_*` names, rejects duplicates/unknown names and safely reconciles stale status-list entries from the matching named review. The page can also prepend matching walks, insert known bridges or freeze a seam with onion skin; every card prints its runtime PNG and authored source-strip filename.
The character-width and character-height sliders each have adjacent −0.5% and +0.5% buttons for precise adjustments. They update the same per-animation values, obey the same 50%–150% limits and become part of the normal Save/export workflow.
Every blue animation-transform slider also has −0.5/+0.5 buttons: degrees for rotation, logical pixels for horizontal/vertical position and percentage points for opacity. They update the same limited, saved and exported values as their sliders.
Each card's frame-control block can play only that reviewed action from frame 1. `Play once` stops on the final frame; `Loop` repeats until paused. This playback choice is inspection-only and does not dirty the review.
At browser widths of 1500px or more, focused mode becomes a widescreen workstation with the pinned canon on the left, a viewport-height animation stage in the centre and a compact two-column control console on the right. Control groups are colour-coded: amber for character size, purple for the ghost, blue for animation transforms, teal for frame navigation and green/red for review decisions and notes.
Review progress is browser-local: changing display zoom or review-state filter saves immediately, and every `Save this review` records that animation as the latest completed card. Reloading restores the focused view and filter. Offline and online browser storage do not synchronise automatically; use Export on one copy and Import review JSON on the other. Saving or advancing from the final result wraps to the first result in that same filter.

## Corrected sheets

- `keeper_anti_gravity` — extended with four calm face-down float frames before the centred back flip; comparison-only rotation was not baked.
- `keeper_artist_smock_sit_front` — new matching-outfit front stand-to-sit transition with the canonical seat datum.
- `keeper_artist_smock_turn_back` — new matching-outfit side-to-rear transition for activity routing.
- `keeper_artist_smock_turn_front` — new matching-outfit side-to-front transition for activity routing.
- `keeper_artist_smock_walk` — new artist-smock locomotion family; every pose is independently height-matched to the corresponding canonical walk frame after frame 4 was identified as undersized in the generated source.
- `keeper_bath_wash` — redrawn and normalised from the standing bare-headed and seated canonical landmarks.
- `keeper_carry_shopping` — frames 1 and 7 replaced with clean adjacent poses so all eight frames carry exactly two bags; cadence reduced to 5fps.
- `keeper_collect_eggs_back` — reuses canonical corrected low rear work anatomy.
- `keeper_crouch_work_back` — redrawn; hands work in front and body width restored.
- `keeper_door_open_side_pyjamas` — clean six-frame side-door redraw in the canonical light-blue pyjama family; handle and floor interaction geometry are unchanged.
- `keeper_drive_speedboat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_eat_seated` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_fish_seated` — extended to 41 frames with a ten-second wait, stable seat contact, longer rod, gradual pull/reel, held catch, ground placement and return to fishing.
- `keeper_fish_standing` — extended to 50 frames with a ten-second wait, stable actor contact, gradual pull/reel, held catch, ground placement and return to fishing.
- `keeper_guitar_pickup_acoustic` — new side-to-rear rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_guitar_pickup_flying_v_1967` — new tier-3 rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_guitar_pickup_gretsch` — new tier-2 rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_halloween_walk_back` — identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_halloween_walk_front` — identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_halloween_walk_side` — identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_hoover_basic` — review-sized tier-2 cleaning loop with its ordinary upright hoover included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_hoover_super` — review-sized tier-3 cleaning loop with its original eccentric super hoover included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_hot_drink_drink` — neighbouring-frame flecks removed while retaining canonical actor, mug and steam.
- `keeper_hot_drink_put_down` — neighbouring-frame flecks removed while retaining the released mug.
- `keeper_hot_tub` — redrawn and normalised by the visible head/shoulder unit rather than the water silhouette.
- `keeper_knight_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_lawn_mower_push` — new baseline-anatomy side walk pushing an included manual reel mower; neighbouring-pose slivers removed; runtime translates the complete unit from behind a foreground shed door.
- `keeper_machete_side` — smooth machete restored from eight isolated grid cells on a 96 px logical long-tool canvas; Frank's saved 127.5% width / 129% height is baked.
- `keeper_meal_place_side` — beard corrected and released plate restored; Frank's original saved 113.5% width / 94% height is now baked.
- `keeper_mechanic_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_nap_seated` — baseline-anatomy side-seated nap loop with closed eyes, clearly reclined head and open mouth; beard silhouette was corrected from a smooth oval to the standard stepped, ragged side-view margin; furniture remains separate.
- `keeper_parachute_drift` — high-resolution eight-pose open-canopy loop, matched to both route hand-offs and baked at the saved 84% width / 122% height.
- `keeper_parachute_landing` — one-shot open-canopy touchdown, compression and canopy-collapse sequence with its entry canvas rebased to the resized drift hand-off.
- `keeper_party_dance` — canonical dance anatomy inherited exactly; party hat is an overlay.
- `keeper_party_eat_cake` — canonical seated-eat anatomy inherited exactly; party hat and cake are overlays.
- `keeper_party_hat_put_on_back` — canonical rear work, raised-arm and leg components recombined; hat overlay only.
- `keeper_party_idle` — canonical front identity inherited exactly; party hat is headwear-only.
- `keeper_party_turn_back` — canonical turn identity inherited exactly; party hat is headwear-only.
- `keeper_party_walk` — canonical side-walk identity inherited exactly; party hat is headwear-only.
- `keeper_piano` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_pirate_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_pirate_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_pirate_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_place_cake` — redrawn for the standard 19 px table datum and a fully straight final pose.
- `keeper_play_drums_back` — normalised to the front drum master with matching seated envelope and 180-degree frame timing.
- `keeper_play_drums_front` — paired front/rear drum master; seated anatomy and frame timing are authoritative.
- `keeper_play_guitar_flying_v_1967` — new tier-3 red 1967 Flying V playing loop at canonical keeper scale.
- `keeper_play_guitar_gretsch` — new tier-2 black Gretsch playing loop at canonical keeper scale.
- `keeper_pressups_side` — redrawn cleanly, then resized to Frank's saved 79% width / 65% height.
- `keeper_put_record` — expanded to a 64 px side-action canvas so the record remains complete through release.
- `keeper_ride_bike_front` — enlarged from its undersized head unit on a 48 px interaction canvas.
- `keeper_row_boat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_scuba_jetty_dive` — new one-shot jetty dive whose endpoint is the exact first horizontal scuba-swim frame.
- `keeper_scuba_swim_down` — redrawn from the approved front swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_horizontal` — redrawn from the approved horizontal swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_up` — redrawn from the approved rear swim anatomy with coherent scuba equipment.
- `keeper_scuba_walk_side` — new matching-outfit jetty locomotion for the scuba route.
- `keeper_search_boxes` — reuses canonical corrected low rear work anatomy.
- `keeper_sit_back` — new canonical rear stand-to-sit transition; final frame is the standard back-to-camera seated comparison ghost.
- `keeper_sit_front` — redrawn and width-normalised against canonical front body.
- `keeper_snooker` — overlapping source poses isolated without fitting actor scale to the cue.
- `keeper_souwester_walk_back` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_souwester_walk_front` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_souwester_walk_side` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_spaceman_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spaceman_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spaceman_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spiral_stairs_down` — frame 4 redrawn to remove an erroneous third hand while preserving the descent cycle.
- `keeper_sweep_broom` — new baseline-anatomy tier-1 cleaning loop with its traditional broom included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_swim_costume_horizontal` — re-rendered on an expanded horizontal canvas; Frank's saved 95.5% width / 100% height is baked.
- `keeper_tarzan_walk_back` — bare-headed identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_tarzan_walk_front` — bare-headed identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_tarzan_walk_side` — bare-headed identity rebuilt against the approved original, then resized to Frank's saved 100% width / 100% height.
- `keeper_walk_into_lift` — intentional depth transition: rear walk scales from 100% to 75%, rises 6 logical pixels, then turns to a full-front neutral pose.
- `keeper_watch_movie` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_watch_tv` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_water_plants_side` — expanded to a 48 px side-action canvas so the watering can and spout remain complete.

## Contact sheets

- [keeper-scale-contact-01.png](../../docs/keeper-scale-audit/keeper-scale-contact-01.png)
- [keeper-scale-contact-02.png](../../docs/keeper-scale-audit/keeper-scale-contact-02.png)
- [keeper-scale-contact-03.png](../../docs/keeper-scale-audit/keeper-scale-contact-03.png)
- [keeper-scale-contact-04.png](../../docs/keeper-scale-audit/keeper-scale-contact-04.png)
- [keeper-scale-contact-05.png](../../docs/keeper-scale-audit/keeper-scale-contact-05.png)
- [keeper-scale-contact-06.png](../../docs/keeper-scale-audit/keeper-scale-contact-06.png)
- [keeper-scale-contact-07.png](../../docs/keeper-scale-audit/keeper-scale-contact-07.png)
- [keeper-scale-contact-08.png](../../docs/keeper-scale-audit/keeper-scale-contact-08.png)
- [keeper-scale-contact-09.png](../../docs/keeper-scale-audit/keeper-scale-contact-09.png)

The frame-by-frame numbers are in `keeper-scale-metrics.json`; the compact per-sheet register is `keeper-scale-summary.csv`. Both are regenerated by `python3 scripts/audit_keeper_scale.py`.
