# Keeper Prime animation-bank audit

**Measured:** 17 October 2026  
**Status:** read-only inventory and redraft queue; nothing in this audit is promoted.

This inventory covers **308** production Keeper animations and technical neutrals. Rig fragments and the static reference sheet are intentionally excluded. Every row retains its exact frame range, geometry, outfit, endpoints, dependencies, current rendering family and transition risks in `data/keeper-prime-animation-bank-audit-v1.json`.

The current production bank is legacy first-batch rendering, not Prime Keeper authority. Historical frames may contribute motion mechanics only. The binding rules are in `docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`.

## Counts

| Group | Count |
|---|---:|
| expression | 9 |
| interaction | 82 |
| locomotion | 101 |
| seated-action | 12 |
| technical-neutral | 73 |
| transition | 31 |
| **Total** | **308** |

### Redraft treatment

| Treatment | Count |
|---|---:|
| excluded-deleted-amendment | 1 |
| full-redraw-user-rejected-family | 27 |
| motion-skeleton-candidate-only | 97 |
| partial-motion-salvage-assessment | 120 |
| prime-redraw-required | 63 |

Legacy endpoint risks: **159**. Strip/sidecar geometry mismatches: **0**. Explicitly rejected/excluded entries: **28**.

## Explicitly rejected or excluded

Swimming, gym and scuba are full-redraw families. `keeper_count_money` must not be regenerated without a new direct instruction.

- `keeper_count_money`
- `keeper_hot_tub`
- `keeper_lift_weights_back`
- `keeper_platform_dive`
- `keeper_pressups_side`
- `keeper_scuba_jetty_dive`
- `keeper_trampoline_front`
- `keeper_ride_bike_front`
- `keeper_scuba_swim_down`
- `keeper_scuba_swim_horizontal`
- `keeper_scuba_swim_up`
- `keeper_scuba_walk_side`
- `keeper_scuba_walk_side_cycle`
- `keeper_scuba_walk_side_start`
- `keeper_scuba_walk_side_stop`
- `keeper_swim_costume_down`
- `keeper_swim_costume_horizontal`
- `keeper_swim_costume_up`
- `keeper_old-school-workout-kit_neutral_prone-side-right`
- `keeper_old-school-workout-kit_neutral_standing-back`
- `keeper_old-school-workout-kit_neutral_standing-front`
- `keeper_scuba_neutral_scuba-standing-side-right`
- `keeper_scuba_neutral_scuba-swim-right`
- `keeper_scuba_neutral_swimming-back`
- `keeper_scuba_neutral_swimming-front`
- `keeper_striped-swimming-costume_neutral_swimming-back`
- `keeper_striped-swimming-costume_neutral_swimming-front`
- `keeper_striped-swimming-costume_neutral_swimming-side-right`

## Inventory by review group

### expression

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_bored` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_dance` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_hungry` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_idle` | 1–4 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | none recorded |
| `keeper_party_dance` | 1–8 @ 4 fps | party-hat | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_party_idle` | 1–4 @ 4 fps | party-hat | standing-front → standing-front | partial-motion-salvage-assessment | costume-route-and-door-occlusion-required |
| `keeper_sad` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_wave_camera` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_yawn` | 1–8 @ 4 fps | standard | standing-rear-right → standing-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |

### interaction

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_aquarium_brush` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_aquarium_net` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_bath_wash` | 1–8 @ 4 fps | mosaic-privacy | sitting-front → sitting-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, seat-height-and-furniture-dependency |
| `keeper_bbq_back` | 1–8 @ 2.5 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_bowling` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_brush_teeth_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | prop-hand-contact-must-be-remeasured |
| `keeper_cake_from_oven_back` | 1–8 @ 4.5 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_carry_cake` | 1–8 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_carry_meal` | 1–8 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_carry_shopping` | 1–8 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_check_instrument_back` | 1–6 @ 6 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_check_instrument_side` | 1–6 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_clear_snow` | 1–8 @ 3.5 fps | winter-coat | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_collect_eggs_back` | 1–8 @ 4 fps | standard | crouching-back → crouching-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_cook_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | prop-hand-contact-must-be-remeasured |
| `keeper_count_money` | 1–8 @ 6 fps | standard | sitting-front → sitting-front | excluded-deleted-amendment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency, must-not-regenerate-without-direct-instruction |
| `keeper_cross` | 1–8 @ 5.5 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_crouch_back` | 1–4 @ 6 fps | standard | standing-back → crouching-back | partial-motion-salvage-assessment | none recorded |
| `keeper_crouch_work_back` | 1–8 @ 4 fps | standard | crouching-back → crouching-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_darts` | 1–14 @ 3 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_dig` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_drink_pint` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_feed_animals` | 1–8 @ 5.5 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_fish_feed_up` | 1–14 @ 5 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_fish_standing` | 1–50 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hammer_back` | 1–8 @ 5 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hammer_side` | 1–8 @ 5 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hoover_basic` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hoover_super` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_drink_drink` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_drink_pour` | 1–10 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_drink_put_down` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_drink_stir` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_tub` | 1–8 @ 4 fps | privacy-foam | sitting-front → sitting-front | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, seat-height-and-furniture-dependency, swimming-family-explicitly-rejected |
| `keeper_lawn_mower_push` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_lean_table_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_lift_weights_back` | 1–8 @ 4 fps | old-school-workout-kit | standing-back → standing-back | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured, gym-family-explicitly-rejected |
| `keeper_machete_side` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_meal_from_oven_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_meal_place_side` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_mechanic_fix` | 1–8 @ 4 fps | mechanic | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_operate_outboard` | 1–8 @ 4 fps | standard | standing-rear-right → standing-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_paint_back` | 1–8 @ 4 fps | artist-smock | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_paint_side` | 1–8 @ 4 fps | artist-smock | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_party_hat_put_on_back` | 1–8 @ 4 fps | party-hat-transition | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_pick_fruit` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_pick_up_low` | 1–8 @ 5 fps | standard | standing-side-right → holding-small-object-side-right | partial-motion-salvage-assessment | none recorded |
| `keeper_pick_vegetable` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_place_cake` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_platform_dive` | 1–10 @ 4 fps | standard | standing-side-right → standing-side-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, swimming-family-explicitly-rejected |
| `keeper_play_drums_back` | 1–8 @ 4 fps | standard | sitting-back → sitting-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_play_drums_front` | 1–8 @ 4 fps | standard | sitting-front → sitting-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_play_guitar` | 1–8 @ 4 fps | standard | play-guitar-acoustic → play-guitar-acoustic | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_play_guitar_flying_v_1967` | 1–8 @ 4 fps | standard | play-guitar-flying-v-1967 → play-guitar-flying-v-1967 | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_play_guitar_gretsch` | 1–8 @ 4 fps | standard | play-guitar-gretsch → play-guitar-gretsch | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_pottery_front` | 1–8 @ 4 fps | artist-smock | sitting-front → sitting-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_pressups_side` | 1–8 @ 4 fps | old-school-workout-kit | prone-side-right → prone-side-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, gym-family-explicitly-rejected |
| `keeper_put_record` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_pyjamas_snore` | 1–6 @ 1 fps | light-blue-pyjamas | lying-side-right → lying-side-right | partial-motion-salvage-assessment | costume-route-and-door-occlusion-required |
| `keeper_reach_high` | 1–5 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | none recorded |
| `keeper_reach_low` | 1–5 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | none recorded |
| `keeper_saw_wood` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_scuba_jetty_dive` | 1–12 @ 4 fps | scuba | scuba-standing-side-right → scuba-swim-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_search_boxes` | 1–8 @ 4 fps | standard | crouching-back → crouching-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_shower_wash` | 1–8 @ 2 fps | mosaic-privacy | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_sow_seeds` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_sweep_broom` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_switch_press_back` | 1–6 @ 4 fps | standard | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_switch_press_side` | 1–6 @ 4 fps | standard | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_table_tennis` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_telescope` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_trampoline_front` | 1–8 @ 7.5 fps | old-school-workout-kit | standing-front → standing-front | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, gym-family-explicitly-rejected |
| `keeper_urinate_back` | 1–6 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_vomit_loo_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_wash_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | prop-hand-contact-must-be-remeasured |
| `keeper_water_plants_back` | 1–8 @ 4 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_water_plants_front` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_water_plants_side` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_weld` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_work_back` | 1–8 @ 3 fps | standard | standing-back → standing-back | partial-motion-salvage-assessment | prop-hand-contact-must-be-remeasured |
| `keeper_write_back` | 1–8 @ 4 fps | standard | sitting-back → sitting-back | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_write_side` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |

### locomotion

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_anti_gravity` | 1–12 @ 4 fps | standard | floating-prone-right → floating-prone-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_artist_smock_walk` | 1–8 @ 4 fps | artist-smock | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_artist_smock_walk_cycle` | 1–9 @ 4 fps | artist-smock | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_artist_smock_walk_start` | 1–5 @ 4 fps | artist-smock | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_artist_smock_walk_stop` | 1–5 @ 4 fps | artist-smock | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_bathrobe_walk` | 1–8 @ 8 fps | cream-bathrobe | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_bathrobe_walk_cycle` | 1–9 @ 8 fps | cream-bathrobe | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_bathrobe_walk_start` | 1–5 @ 8 fps | cream-bathrobe | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_bathrobe_walk_stop` | 1–5 @ 8 fps | cream-bathrobe | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_drive_speedboat` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_halloween_walk_back` | 1–8 @ 4 fps | halloween | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_back_cycle` | 1–9 @ 4 fps | halloween | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_front` | 1–8 @ 4 fps | halloween | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_front_cycle` | 1–9 @ 4 fps | halloween | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_side` | 1–8 @ 4 fps | halloween | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_side_cycle` | 1–9 @ 4 fps | halloween | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_side_start` | 1–5 @ 4 fps | halloween | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_halloween_walk_side_stop` | 1–5 @ 4 fps | halloween | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_knight_walk_back` | 1–8 @ 4 fps | knight | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_knight_walk_back_cycle` | 1–9 @ 4 fps | knight | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_knight_walk_front` | 1–8 @ 4 fps | knight | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_knight_walk_front_cycle` | 1–9 @ 4 fps | knight | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_knight_walk_side` | 1–8 @ 4 fps | knight | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_knight_walk_side_cycle` | 1–9 @ 4 fps | knight | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_knight_walk_side_start` | 1–5 @ 4 fps | knight | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_knight_walk_side_stop` | 1–5 @ 4 fps | knight | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_ladder_climb` | 1–8 @ 4 fps | standard | climbing-back → climbing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_mechanic_walk_back` | 1–8 @ 4 fps | mechanic | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_back_cycle` | 1–9 @ 4 fps | mechanic | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_front` | 1–8 @ 4 fps | mechanic | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_front_cycle` | 1–9 @ 4 fps | mechanic | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_side` | 1–8 @ 4 fps | mechanic | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_side_cycle` | 1–9 @ 4 fps | mechanic | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_side_start` | 1–5 @ 4 fps | mechanic | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_mechanic_walk_side_stop` | 1–5 @ 4 fps | mechanic | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_parachute_drift` | 1–8 @ 4 fps | standard | parachute-open → parachute-open | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_parachute_jump` | 1–9 @ 4 fps | standard | standing-side-right → parachute-open | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_parachute_landing` | 1–10 @ 4 fps | standard | parachute-open → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_party_walk` | 1–8 @ 4 fps | party-hat | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_party_walk_cycle` | 1–9 @ 4 fps | party-hat | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_party_walk_start` | 1–5 @ 4 fps | party-hat | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_party_walk_stop` | 1–5 @ 4 fps | party-hat | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_back` | 1–8 @ 4 fps | pirate | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_back_cycle` | 1–9 @ 4 fps | pirate | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_front` | 1–8 @ 4 fps | pirate | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_front_cycle` | 1–9 @ 4 fps | pirate | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_side` | 1–8 @ 4 fps | pirate | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_side_cycle` | 1–9 @ 4 fps | pirate | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_side_start` | 1–5 @ 4 fps | pirate | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pirate_walk_side_stop` | 1–5 @ 4 fps | pirate | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pyjamas_walk` | 1–8 @ 4 fps | light-blue-pyjamas | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_pyjamas_walk_cycle` | 1–9 @ 4 fps | light-blue-pyjamas | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pyjamas_walk_start` | 1–5 @ 4 fps | light-blue-pyjamas | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_pyjamas_walk_stop` | 1–5 @ 4 fps | light-blue-pyjamas | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_ride_bike_front` | 1–8 @ 4 fps | old-school-workout-kit | sitting-front → sitting-front | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency, gym-family-explicitly-rejected |
| `keeper_row_boat` | 1–8 @ 3 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_scuba_swim_down` | 1–8 @ 4 fps | scuba | swimming-front → swimming-front | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_swim_horizontal` | 1–8 @ 4 fps | scuba | swimming-side-right → swimming-side-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_swim_up` | 1–8 @ 4 fps | scuba | swimming-back → swimming-back | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_walk_side` | 1–8 @ 4 fps | scuba | scuba-standing-side-right → scuba-standing-side-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_walk_side_cycle` | 1–9 @ 4 fps | scuba | scuba-standing-side-right → scuba-standing-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_walk_side_start` | 1–5 @ 4 fps | scuba | scuba-standing-side-right → scuba-standing-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_walk_side_stop` | 1–5 @ 4 fps | scuba | scuba-standing-side-right → scuba-standing-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_slide_side` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_souwester_walk_back` | 1–8 @ 4 fps | souwester | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_back_cycle` | 1–9 @ 4 fps | souwester | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_front` | 1–8 @ 4 fps | souwester | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_front_cycle` | 1–9 @ 4 fps | souwester | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_side` | 1–8 @ 4 fps | souwester | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_side_cycle` | 1–9 @ 4 fps | souwester | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_side_start` | 1–5 @ 4 fps | souwester | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_souwester_walk_side_stop` | 1–5 @ 4 fps | souwester | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_back` | 1–8 @ 4 fps | spaceman | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_back_cycle` | 1–9 @ 4 fps | spaceman | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_front` | 1–8 @ 4 fps | spaceman | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_front_cycle` | 1–9 @ 4 fps | spaceman | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_side` | 1–8 @ 4 fps | spaceman | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_side_cycle` | 1–9 @ 4 fps | spaceman | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_side_start` | 1–5 @ 4 fps | spaceman | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spaceman_walk_side_stop` | 1–5 @ 4 fps | spaceman | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_spiral_stairs` | 1–8 @ 4 fps | standard | standing-rear-right → standing-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_spiral_stairs_down` | 1–8 @ 4 fps | standard | standing-rear-right → standing-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_spiral_stairs_up` | 1–8 @ 4 fps | standard | standing-rear-right → standing-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_stairs_down` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_stairs_up` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_swim_costume_down` | 1–8 @ 4 fps | striped-swimming-costume | swimming-front → swimming-front | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_swim_costume_horizontal` | 1–8 @ 4 fps | striped-swimming-costume | swimming-side-right → swimming-side-right | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_swim_costume_up` | 1–8 @ 4 fps | striped-swimming-costume | swimming-back → swimming-back | full-redraw-user-rejected-family | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_tarzan_walk_back` | 1–8 @ 4 fps | tarzan | standing-back → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_back_cycle` | 1–9 @ 4 fps | tarzan | standing-back → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_front` | 1–8 @ 4 fps | tarzan | standing-front → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_front_cycle` | 1–9 @ 4 fps | tarzan | standing-front → standing-front | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_side` | 1–8 @ 4 fps | tarzan | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_side_cycle` | 1–9 @ 4 fps | tarzan | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_side_start` | 1–5 @ 4 fps | tarzan | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_tarzan_walk_side_stop` | 1–5 @ 4 fps | tarzan | standing-side-right → standing-side-right | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_walk` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_walk_cycle` | 1–9 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | none recorded |
| `keeper_walk_into_lift` | 1–8 @ 4 fps | standard | standing-back → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral |
| `keeper_walk_start` | 1–5 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | none recorded |
| `keeper_walk_stop` | 1–5 @ 8 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | none recorded |

### seated-action

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_eat_seated` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_fish_seated` | 1–41 @ 3 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_nap_seated` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | seat-height-and-furniture-dependency |
| `keeper_party_eat_cake` | 1–8 @ 4 fps | party-hat | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_piano` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_read_front` | 1–8 @ 4 fps | standard | sitting-front → sitting-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, seat-height-and-furniture-dependency |
| `keeper_read_side` | 1–8 @ 4 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, seat-height-and-furniture-dependency |
| `keeper_snooker` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_type_computer` | 1–8 @ 8.5 fps | standard | sitting-side-right → sitting-side-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_video_game` | 1–8 @ 4 fps | standard | sitting-rear-right → sitting-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_watch_movie` | 1–8 @ 4 fps | standard | sitting-rear-right → sitting-rear-right | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_watch_tv` | 1–8 @ 4 fps | standard | sitting-rear-right → sitting-rear-right | partial-motion-salvage-assessment | seat-height-and-furniture-dependency |

### technical-neutral

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_artist-smock_neutral_sitting-front` | 1–1 @ 0 fps | artist-smock | sitting-front → sitting-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_artist-smock_neutral_standing-back` | 1–1 @ 0 fps | artist-smock | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_artist-smock_neutral_standing-front` | 1–1 @ 0 fps | artist-smock | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_artist-smock_neutral_standing-side-left` | 1–1 @ 0 fps | artist-smock | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_artist-smock_neutral_standing-side-right` | 1–1 @ 0 fps | artist-smock | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_cream-bathrobe_neutral_standing-back` | 1–1 @ 0 fps | cream-bathrobe | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_cream-bathrobe_neutral_standing-rear-right` | 1–1 @ 0 fps | cream-bathrobe | standing-rear-right → standing-rear-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_cream-bathrobe_neutral_standing-side-left` | 1–1 @ 0 fps | cream-bathrobe | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_cream-bathrobe_neutral_standing-side-right` | 1–1 @ 0 fps | cream-bathrobe | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_halloween_neutral_standing-back` | 1–1 @ 0 fps | halloween | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_halloween_neutral_standing-front` | 1–1 @ 0 fps | halloween | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_halloween_neutral_standing-side-left` | 1–1 @ 0 fps | halloween | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_halloween_neutral_standing-side-right` | 1–1 @ 0 fps | halloween | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_knight_neutral_standing-back` | 1–1 @ 0 fps | knight | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_knight_neutral_standing-front` | 1–1 @ 0 fps | knight | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_knight_neutral_standing-side-left` | 1–1 @ 0 fps | knight | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_knight_neutral_standing-side-right` | 1–1 @ 0 fps | knight | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_light-blue-pyjamas_neutral_lying-side-right` | 1–1 @ 0 fps | light-blue-pyjamas | lying-side-right → lying-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_light-blue-pyjamas_neutral_standing-back` | 1–1 @ 0 fps | light-blue-pyjamas | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_light-blue-pyjamas_neutral_standing-front` | 1–1 @ 0 fps | light-blue-pyjamas | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_light-blue-pyjamas_neutral_standing-side-left` | 1–1 @ 0 fps | light-blue-pyjamas | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_light-blue-pyjamas_neutral_standing-side-right` | 1–1 @ 0 fps | light-blue-pyjamas | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mechanic_neutral_standing-back` | 1–1 @ 0 fps | mechanic | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mechanic_neutral_standing-front` | 1–1 @ 0 fps | mechanic | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mechanic_neutral_standing-side-left` | 1–1 @ 0 fps | mechanic | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mechanic_neutral_standing-side-right` | 1–1 @ 0 fps | mechanic | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mosaic-privacy_neutral_sitting-front` | 1–1 @ 0 fps | mosaic-privacy | sitting-front → sitting-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_mosaic-privacy_neutral_standing-back` | 1–1 @ 0 fps | mosaic-privacy | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_neutral_crouching-back` | 1–1 @ 0 fps | standard | crouching-back → crouching-back | prime-redraw-required | none recorded |
| `keeper_neutral_holding-small-object-side-right` | 1–1 @ 0 fps | standard | holding-small-object-side-right → holding-small-object-side-right | prime-redraw-required | none recorded |
| `keeper_neutral_sitting-back` | 1–1 @ 0 fps | standard | sitting-back → sitting-back | prime-redraw-required | none recorded |
| `keeper_neutral_sitting-front` | 1–1 @ 0 fps | standard | sitting-front → sitting-front | prime-redraw-required | none recorded |
| `keeper_neutral_sitting-rear-right` | 1–1 @ 0 fps | standard | sitting-rear-right → sitting-rear-right | prime-redraw-required | none recorded |
| `keeper_neutral_sitting-side-right` | 1–1 @ 0 fps | standard | sitting-side-right → sitting-side-right | prime-redraw-required | none recorded |
| `keeper_neutral_standing-back` | 1–1 @ 0 fps | standard | standing-back → standing-back | prime-redraw-required | none recorded |
| `keeper_neutral_standing-front` | 1–1 @ 0 fps | standard | standing-front → standing-front | prime-redraw-required | none recorded |
| `keeper_neutral_standing-side-left` | 1–1 @ 0 fps | standard | standing-side-left → standing-side-left | prime-redraw-required | none recorded |
| `keeper_neutral_standing-side-right` | 1–1 @ 0 fps | standard | standing-side-right → standing-side-right | prime-redraw-required | none recorded |
| `keeper_old-school-workout-kit_neutral_prone-side-right` | 1–1 @ 0 fps | old-school-workout-kit | prone-side-right → prone-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, gym-family-explicitly-rejected |
| `keeper_old-school-workout-kit_neutral_standing-back` | 1–1 @ 0 fps | old-school-workout-kit | standing-back → standing-back | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, gym-family-explicitly-rejected |
| `keeper_old-school-workout-kit_neutral_standing-front` | 1–1 @ 0 fps | old-school-workout-kit | standing-front → standing-front | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, gym-family-explicitly-rejected |
| `keeper_party-hat_neutral_sitting-side-right` | 1–1 @ 0 fps | party-hat | sitting-side-right → sitting-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_party-hat_neutral_standing-back` | 1–1 @ 0 fps | party-hat | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_party-hat_neutral_standing-front` | 1–1 @ 0 fps | party-hat | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_party-hat_neutral_standing-side-left` | 1–1 @ 0 fps | party-hat | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_party-hat_neutral_standing-side-right` | 1–1 @ 0 fps | party-hat | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_pirate_neutral_standing-back` | 1–1 @ 0 fps | pirate | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_pirate_neutral_standing-front` | 1–1 @ 0 fps | pirate | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_pirate_neutral_standing-side-left` | 1–1 @ 0 fps | pirate | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_pirate_neutral_standing-side-right` | 1–1 @ 0 fps | pirate | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_privacy-foam_neutral_sitting-front` | 1–1 @ 0 fps | privacy-foam | sitting-front → sitting-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_scuba_neutral_scuba-standing-side-right` | 1–1 @ 0 fps | scuba | scuba-standing-side-right → scuba-standing-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_neutral_scuba-swim-right` | 1–1 @ 0 fps | scuba | scuba-swim-right → scuba-swim-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_neutral_swimming-back` | 1–1 @ 0 fps | scuba | swimming-back → swimming-back | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_scuba_neutral_swimming-front` | 1–1 @ 0 fps | scuba | swimming-front → swimming-front | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, scuba-family-explicitly-rejected |
| `keeper_souwester_neutral_standing-back` | 1–1 @ 0 fps | souwester | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_souwester_neutral_standing-front` | 1–1 @ 0 fps | souwester | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_souwester_neutral_standing-side-left` | 1–1 @ 0 fps | souwester | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_souwester_neutral_standing-side-right` | 1–1 @ 0 fps | souwester | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_spaceman_neutral_standing-back` | 1–1 @ 0 fps | spaceman | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_spaceman_neutral_standing-front` | 1–1 @ 0 fps | spaceman | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_spaceman_neutral_standing-side-left` | 1–1 @ 0 fps | spaceman | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_spaceman_neutral_standing-side-right` | 1–1 @ 0 fps | spaceman | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_striped-swimming-costume_neutral_swimming-back` | 1–1 @ 0 fps | striped-swimming-costume | swimming-back → swimming-back | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_striped-swimming-costume_neutral_swimming-front` | 1–1 @ 0 fps | striped-swimming-costume | swimming-front → swimming-front | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_striped-swimming-costume_neutral_swimming-side-right` | 1–1 @ 0 fps | striped-swimming-costume | swimming-side-right → swimming-side-right | full-redraw-user-rejected-family | costume-route-and-door-occlusion-required, swimming-family-explicitly-rejected |
| `keeper_tarzan_neutral_standing-back` | 1–1 @ 0 fps | tarzan | standing-back → standing-back | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_tarzan_neutral_standing-front` | 1–1 @ 0 fps | tarzan | standing-front → standing-front | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_tarzan_neutral_standing-side-left` | 1–1 @ 0 fps | tarzan | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_tarzan_neutral_standing-side-right` | 1–1 @ 0 fps | tarzan | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_towel-privacy_neutral_standing-rear-right` | 1–1 @ 0 fps | towel-privacy | standing-rear-right → standing-rear-right | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_towel-privacy_neutral_standing-side-left` | 1–1 @ 0 fps | towel-privacy | standing-side-left → standing-side-left | prime-redraw-required | costume-route-and-door-occlusion-required |
| `keeper_towel-privacy_neutral_standing-side-right` | 1–1 @ 0 fps | towel-privacy | standing-side-right → standing-side-right | prime-redraw-required | costume-route-and-door-occlusion-required |

### transition

| Animation | Frames | Outfit | Start → end | Treatment | Main risks |
|---|---:|---|---|---|---|
| `keeper_artist_smock_sit_front` | 1–6 @ 4.5 fps | artist-smock | standing-front → sitting-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, seat-height-and-furniture-dependency |
| `keeper_artist_smock_turn_back` | 1–6 @ 4 fps | artist-smock | standing-side-right → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_artist_smock_turn_front` | 1–6 @ 4 fps | artist-smock | standing-side-right → standing-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_bath_enter` | 1–8 @ 4 fps | towel-privacy | standing-side-right → sitting-front | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_bath_exit` | 1–8 @ 4 fps | towel-privacy | sitting-front → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_boat_enter` | 1–8 @ 4 fps | standard | standing-side-right → sitting-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_boat_exit` | 1–8 @ 4 fps | standard | sitting-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured, seat-height-and-furniture-dependency |
| `keeper_cake_turn_right` | 1–6 @ 7.5 fps | standard | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_door_open_back` | 1–6 @ 5.5 fps | standard | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_door_open_side` | 1–6 @ 5 fps | standard | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_door_open_side_pyjamas` | 1–6 @ 4 fps | light-blue-pyjamas | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_get_into_bed` | 1–8 @ 3 fps | light-blue-pyjamas | standing-side-right → lying-side-right | partial-motion-salvage-assessment | costume-route-and-door-occlusion-required |
| `keeper_guitar_pickup_acoustic` | 1–12 @ 8 fps | standard | standing-side-right → play-guitar-acoustic | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_guitar_pickup_flying_v_1967` | 1–12 @ 4 fps | standard | standing-side-right → play-guitar-flying-v-1967 | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_guitar_pickup_gretsch` | 1–12 @ 4 fps | standard | standing-side-right → play-guitar-gretsch | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_hot_drink_pickup` | 1–8 @ 4 fps | standard | standing-side-right → standing-side-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_lift_button_front` | 1–8 @ 4 fps | standard | standing-front → standing-front | partial-motion-salvage-assessment | legacy-endpoint-does-not-match-neutral, prop-hand-contact-must-be-remeasured |
| `keeper_party_turn_back` | 1–6 @ 4 fps | party-hat | standing-front → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_pyjamas_turn_back` | 1–6 @ 4 fps | light-blue-pyjamas | standing-front → standing-back | motion-skeleton-candidate-only | costume-route-and-door-occlusion-required |
| `keeper_shower_door_open_bathrobe` | 1–10 @ 4 fps | cream-bathrobe | standing-rear-right → standing-rear-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required, prop-hand-contact-must-be-remeasured |
| `keeper_shower_enter` | 1–8 @ 4 fps | towel-privacy | standing-rear-right → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_shower_enter_bathrobe` | 1–8 @ 4 fps | cream-bathrobe | standing-rear-right → standing-back | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_shower_exit` | 1–8 @ 4 fps | towel-privacy | standing-back → standing-rear-right | motion-skeleton-candidate-only | legacy-endpoint-does-not-match-neutral, costume-route-and-door-occlusion-required |
| `keeper_sit_back` | 1–6 @ 4 fps | standard | standing-back → sitting-back | partial-motion-salvage-assessment | seat-height-and-furniture-dependency |
| `keeper_sit_front` | 1–6 @ 4 fps | standard | standing-front → sitting-front | partial-motion-salvage-assessment | seat-height-and-furniture-dependency |
| `keeper_sit_side` | 1–6 @ 4 fps | standard | standing-side-right → sitting-side-right | partial-motion-salvage-assessment | seat-height-and-furniture-dependency |
| `keeper_sitting_turn_back_to_rear` | 1–4 @ 4 fps | standard | sitting-back → sitting-rear-right | motion-skeleton-candidate-only | seat-height-and-furniture-dependency |
| `keeper_turn_back` | 1–6 @ 10.5 fps | standard | standing-side-right → standing-back | partial-motion-salvage-assessment | none recorded |
| `keeper_turn_front` | 1–6 @ 4 fps | standard | standing-side-right → standing-front | partial-motion-salvage-assessment | none recorded |
| `keeper_turn_left_back` | 1–6 @ 10.5 fps | standard | standing-side-left → standing-back | partial-motion-salvage-assessment | none recorded |
| `keeper_turn_left_front` | 1–6 @ 4 fps | standard | standing-side-left → standing-front | partial-motion-salvage-assessment | none recorded |

## Review order

1. Approve the six Prime seated endpoints, then build stand↔sit transitions for all six directions.
2. Establish one complete standard-outfit action route as the reference implementation: walk → stop → action → exact neutral → walk.
3. Work through standard standing interactions in small object-specific batches.
4. Normalise seated actions against the approved seated authorities.
5. Build costume routes behind door occlusion before costume actions.
6. Redraw swimming, gym and scuba from first principles after their environments and props are fixed.

No action may be approved from an isolated loop.

