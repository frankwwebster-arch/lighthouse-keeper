# Keeper scale audit

This is the permanent, reproducible audit of every keeper sheet against the untouched approved original `keeper_walk`. It deliberately does **not** use the outer silhouette as character scale except for the small set of directly comparable full-body walks: hats, tools, raised arms, water and furniture can change that box without changing the keeper.

- 187 keeper sheets inspected.
- 169 animation sheets accepted for review; 18 obsolete modular/reference sheets excluded.
- 1348 individual frames measured.
- 76 sheets explicitly rebuilt or anatomy-normalised in this pass.
- 0 unresolved original-comparison failures (the audit command refuses to succeed unless this is zero).
- Canonical upright anatomy: skull top 32.5 logical pixels above the walking floor, shoulders 24.5, hips 14.5, seat contact 11.
- Allowed landmark drift: 0.5 logical pixel; core-width drift: 1 logical pixel. Pose contacts are checked independently from body scale.

## Measurement method

The approved original is printed first in every contact-sheet row at exactly the same scale as the tested frames. Directly comparable walks must measure 0.960–1.040 of the original skull-to-sole silhouette; unobscured side walks must also remain within 1 logical pixel of its median 20 px-above-floor torso scan, or the command fails. Other upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is also recorded where visible as a machine-checkable warning signal; it is not allowed to overrule the anatomical method.

## Interactive comparison

Open [the sizing and transition review](review.html) to see a dedicated untouched `keeper_walk` scale-authority panel followed by all 169 accepted animations in one filename-ordered gallery, with no search or filters required. A focused one-animation view provides a much larger stage, Previous/Next buttons, progress and filename status, and Left/Right arrow-key navigation without rebuilding cards or losing in-progress edits. It keeps a compact canonical reference pinned beside the reviewed card; choose standing or one sitting canon. The sitting endpoint's measured 9.75 × 6.5 face proxy exactly matches the standing reference frame, making it the sitting height/proportion authority. In upright standard-cap poses, the gold badge crossing the blue skull-top guide is a calibrated visual proxy; use anatomical landmarks for tilted, bent, seated, crouched, horizontal, bare-headed or alternate-headwear poses. The display-size slider magnifies gallery stages, or the focused reviewed stage, from 1× to 12× without changing the art or its relative scale; the pinned reference remains at a compact 2×. Each animation has independent 50%–150% character-width and character-height proposal sliders plus horizontal and vertical position controls, applied only to the reviewed action while the reference, rulers, ghost, approach walk and bridges remain unchanged. Earlier uniform size choices migrate to both axes. Comparison ghosts automatically use the canonical front, side or rear sitting endpoint for seated poses and the standing walk reference otherwise. Per-card controls can override that reference with the canonical standing side, standing facing-front, standing back-to-camera, sitting side, sitting front or sitting back figure, mirror, rotate and reset the ghost, move it alongside on a wider stage, rotate and reposition every frame of the reviewed animation around its fixed review anchor, and fade only that animation. The facing-front ghost is the neutral arms-down first frame of `keeper_wave_camera`, from which the exact-canonical-identity party idle is also derived. The back-to-camera standing ghost is the final frame of `keeper_turn_back`: the audited standard-outfit rear endpoint at the same 32 × 40 canvas, [16, 40] feet anchor and 38-pixel height as the standing authority. The sitting-back ghost is the final frame of `keeper_sit_back`, with the same [16, 29] seat point as the front and side sitting standards. Flying and swimming clips initially place the bottom of the first-frame figure on the red floor line so their size is easier to compare; manual position changes are explicit saved proposals. Pausing resets every card to its action's first frame. Per-card Previous/Next frame buttons pause globally, select action-only mode and step without wrapping from frame 1 through the final frame; frame inspection does not dirty the saved review. A separate 1–20fps proposed game-speed slider, 0.5fps buttons, authored-speed reset and live cycle-duration readout preview the reviewed action without changing approach-walk or bridge timing. Every card has a free-text production-notes field, mutually exclusive happy, full-re-draft and re-review-later decisions, a `Save this review` button and saved/unsaved status. `Save & re-review later` records the reminder immediately and advances to the next clip in focused mode; the reminder can be removed when that card is revisited. Saving persists notes, the decision, width, height, proposed runtime FPS, reviewed-animation rotation and position, ghost mirror, rotation and position controls, opacity and approval in the browser. Orange cards have unsaved changes, saved-and-happy cards are green, saved re-draft cards are red, saved re-review cards are blue, the summary counts progress, and export refuses to proceed while edits remain unsaved. `keeper-scale-choices.json` version 8 contains independent width/height/position/FPS production proposals, notes, re-draft requests, re-review reminders and the complete saved review/approval register. Accepted `animationFps` values belong in each clip's source JSON sidecar and generated runtime manifest, not in the PNG pixels. Comparison settings remain visual aids and do not alter production art. The page can also prepend the matching same-outfit walk, insert known bridge clips, or freeze the exact walk-to-action seam with onion skin. Every card prints its runtime PNG and authored source-strip filename.
The character-width and character-height sliders each have adjacent −0.5% and +0.5% buttons for precise adjustments. They update the same per-animation values, obey the same 50%–150% limits and become part of the normal Save/export workflow.
Every blue animation-transform slider also has −0.5/+0.5 buttons: degrees for rotation, logical pixels for horizontal/vertical position and percentage points for opacity. They update the same limited, saved and exported values as their sliders.
Each card's frame-control block can play only that reviewed action from frame 1. `Play once` stops on the final frame; `Loop` repeats until paused. This playback choice is inspection-only and does not dirty the review.
At browser widths of 1500px or more, focused mode becomes a widescreen workstation with the pinned canon on the left, a viewport-height animation stage in the centre and a compact two-column control console on the right. Control groups are colour-coded: amber for character size, purple for the ghost, blue for animation transforms, teal for frame navigation and green/red for review decisions and notes.
Review progress is browser-local: changing display zoom saves it immediately, and every `Save this review` records that animation as the latest completed card. Reloading then restores the zoom, opens focused mode and selects the filename-ordered animation immediately after the most recently saved card (or remains on the final card when it was last).

## Corrected sheets

- `keeper_anti_gravity` — rebuilt as a canonical-scale prone goggle float with frames 3-4 in progressive rotation, a centred back flip and no parachute.
- `keeper_artist_smock_sit_front` — new matching-outfit front stand-to-sit transition with the canonical seat datum.
- `keeper_artist_smock_turn_back` — new matching-outfit side-to-rear transition for activity routing.
- `keeper_artist_smock_turn_front` — new matching-outfit side-to-front transition for activity routing.
- `keeper_artist_smock_walk` — new artist-smock locomotion family; every pose is independently height-matched to the corresponding canonical walk frame after frame 4 was identified as undersized in the generated source.
- `keeper_bath_wash` — redrawn and normalised from the standing bare-headed and seated canonical landmarks.
- `keeper_carry_shopping` — hand anatomy redrawn so each frame has exactly two hands attached to the two bag-carrying arms.
- `keeper_collect_eggs_back` — reuses canonical corrected low rear work anatomy.
- `keeper_crouch_work_back` — redrawn; hands work in front and body width restored.
- `keeper_door_open_side_pyjamas` — clean six-frame side-door redraw in the canonical light-blue pyjama family; handle and floor interaction geometry are unchanged.
- `keeper_drive_speedboat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_eat_seated` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_fish_standing` — enlarged on a 64 by 56 canvas so the keeper, not the rod and line, determines actor scale.
- `keeper_guitar_pickup_acoustic` — new side-to-rear rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_guitar_pickup_flying_v_1967` — new tier-3 rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_guitar_pickup_gretsch` — new tier-2 rack pickup and return-to-play transition; prop handoff occurs on frame 6.
- `keeper_halloween_walk_back` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_halloween_walk_front` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_halloween_walk_side` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_hoover_basic` — new canonical-height tier-2 cleaning loop with its ordinary upright hoover included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_hoover_super` — new canonical-height tier-3 cleaning loop with its original eccentric super hoover included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_hot_drink_drink` — neighbouring-frame flecks removed while retaining canonical actor, mug and steam.
- `keeper_hot_drink_put_down` — neighbouring-frame flecks removed while retaining the released mug.
- `keeper_hot_tub` — redrawn and normalised by the visible head/shoulder unit rather than the water silhouette.
- `keeper_knight_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_lawn_mower_push` — new canonical-height side walk pushing an included manual reel mower; runtime translates the complete unit from behind a foreground shed door.
- `keeper_machete_side` — smooth machete restored in every frame; 64 px long-tool canvas prevents right-edge clipping without changing keeper scale.
- `keeper_meal_place_side` — standard 19 px table datum; released plate edge restored in frames 7-8 without changing keeper scale.
- `keeper_mechanic_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_nap_seated` — canonical side-seated nap loop with closed eyes, clearly reclined head and open mouth; beard silhouette was corrected from a smooth oval to the standard stepped, ragged side-view margin; body height matches the standard sitting endpoint and furniture remains separate.
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
- `keeper_pressups_side` — redrawn and body-axis-normalised without shrinking its canonical head/core depth.
- `keeper_put_record` — expanded to a 48 px side-action canvas so the record remains complete in frames 5–7.
- `keeper_ride_bike_front` — enlarged from its undersized head unit on a 48 px interaction canvas.
- `keeper_row_boat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_scuba_swim_down` — redrawn from the approved front swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_horizontal` — redrawn from the approved horizontal swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_up` — redrawn from the approved rear swim anatomy with coherent scuba equipment.
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
- `keeper_sweep_broom` — new canonical-height tier-1 cleaning loop with its traditional broom included; runtime swaps tools only while fully hidden by the cupboard door.
- `keeper_swim_costume_horizontal` — enlarged on an expanded canvas so horizontal anatomy matches the upright keeper.
- `keeper_tarzan_walk_back` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
- `keeper_tarzan_walk_front` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
- `keeper_tarzan_walk_side` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
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
