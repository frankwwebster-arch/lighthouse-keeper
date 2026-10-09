# Keeper scale audit

This is the permanent, reproducible audit of every keeper sheet against the untouched approved original `keeper_walk`. It deliberately does **not** use the outer silhouette as character scale except for the small set of directly comparable full-body walks: hats, tools, raised arms, water and furniture can change that box without changing the keeper.

- 170 keeper sheets inspected.
- 152 animation sheets accepted for review; 18 obsolete modular/reference sheets excluded.
- 1210 individual frames measured.
- 59 sheets explicitly rebuilt or anatomy-normalised in this pass.
- 0 unresolved original-comparison failures (the audit command refuses to succeed unless this is zero).
- Canonical upright anatomy: skull top 32.5 logical pixels above the walking floor, shoulders 24.5, hips 14.5, seat contact 11.
- Allowed landmark drift: 0.5 logical pixel; core-width drift: 1 logical pixel. Pose contacts are checked independently from body scale.

## Measurement method

The approved original is printed first in every contact-sheet row at exactly the same scale as the tested frames. Directly comparable walks must measure 0.960–1.040 of the original skull-to-sole silhouette; unobscured side walks must also remain within 1 logical pixel of its median 20 px-above-floor torso scan, or the command fails. Other upright poses use inferred skull-to-supporting-sole height. Costumes use the face/ear/neck structure to infer the skull under hats and helmets. Seated and crouched poses use the head unit plus shoulder–hip–sole chain. Swimming, press-ups and other horizontal poses use the same articulated chain along the body axis. A skin-colour face proxy is also recorded where visible as a machine-checkable warning signal; it is not allowed to overrule the anatomical method.

## Interactive comparison

Open [the sizing and transition review](review.html) to see every accepted animation at one fixed world scale. It can play actions alone, prepend the matching same-outfit walk, insert known bridge clips, or freeze the exact walk-to-action seam with onion skin.

## Corrected sheets

- `keeper_anti_gravity` — rebuilt as a canonical-scale prone goggle float with frames 3-4 in progressive rotation, a centred back flip and no parachute.
- `keeper_bath_wash` — redrawn and normalised from the standing bare-headed and seated canonical landmarks.
- `keeper_carry_shopping` — hand anatomy redrawn so each frame has exactly two hands attached to the two bag-carrying arms.
- `keeper_collect_eggs_back` — reuses canonical corrected low rear work anatomy.
- `keeper_crouch_work_back` — redrawn; hands work in front and body width restored.
- `keeper_drive_speedboat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_eat_seated` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_fish_standing` — enlarged on a 64 by 56 canvas so the keeper, not the rod and line, determines actor scale.
- `keeper_halloween_walk_back` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_halloween_walk_front` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_halloween_walk_side` — rebuilt against the approved original skull-to-sole scale; cape bulk excluded from core anatomy.
- `keeper_hot_drink_drink` — neighbouring-frame flecks removed while retaining canonical actor, mug and steam.
- `keeper_hot_drink_put_down` — neighbouring-frame flecks removed while retaining the released mug.
- `keeper_hot_tub` — redrawn and normalised by the visible head/shoulder unit rather than the water silhouette.
- `keeper_knight_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_knight_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_machete_side` — smooth machete restored in every frame; 64 px long-tool canvas prevents right-edge clipping without changing keeper scale.
- `keeper_meal_place_side` — standard 19 px table datum; released plate edge restored in frames 7-8 without changing keeper scale.
- `keeper_mechanic_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_mechanic_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
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
- `keeper_pressups_side` — redrawn and body-axis-normalised without shrinking its canonical head/core depth.
- `keeper_put_record` — expanded to a 48 px side-action canvas so the record remains complete in frames 5–7.
- `keeper_ride_bike_front` — enlarged from its undersized head unit on a 48 px interaction canvas.
- `keeper_row_boat` — seated anatomy normalised to the sit-side head and torso unit.
- `keeper_scuba_swim_down` — redrawn from the approved front swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_horizontal` — redrawn from the approved horizontal swim anatomy with coherent scuba equipment.
- `keeper_scuba_swim_up` — redrawn from the approved rear swim anatomy with coherent scuba equipment.
- `keeper_search_boxes` — reuses canonical corrected low rear work anatomy.
- `keeper_sit_front` — redrawn and width-normalised against canonical front body.
- `keeper_snooker` — overlapping source poses isolated without fitting actor scale to the cue.
- `keeper_souwester_walk_back` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_souwester_walk_front` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_souwester_walk_side` — costume headwear excluded; skull, shoulder and sole landmarks normalised.
- `keeper_spaceman_walk_back` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spaceman_walk_front` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spaceman_walk_side` — costume-specific headwear envelope excluded from skull-to-sole scale.
- `keeper_spiral_stairs_down` — frame 4 redrawn to remove an erroneous third hand while preserving the descent cycle.
- `keeper_swim_costume_horizontal` — enlarged on an expanded canvas so horizontal anatomy matches the upright keeper.
- `keeper_tarzan_walk_back` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
- `keeper_tarzan_walk_front` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
- `keeper_tarzan_walk_side` — rebuilt to the approved original bare skull-to-sole scale on the standard 40 px actor canvas.
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

The frame-by-frame numbers are in `keeper-scale-metrics.json`; the compact per-sheet register is `keeper-scale-summary.csv`. Both are regenerated by `python3 scripts/audit_keeper_scale.py`.
