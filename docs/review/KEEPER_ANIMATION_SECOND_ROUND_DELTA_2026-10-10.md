# Keeper animation second-round delta — 2026-10-10

## Immutable review evidence

- First round: `frank-keeper-animation-review-2026-10-09.json`, SHA-256 `c19129f8419df2c046f3abb06de9f339f1cd8edb31c2d505dea8e79562d5f486`.
- Second round: `frank-keeper-animation-review-2026-10-10.json`, SHA-256 `e72a6ddf3e7c30e3093195b5044ebd2b9d9af62ba94c9e493158af49b1e7ace7`.
- The supplied second export is retained byte-for-byte. Its contents are review data, never executable instructions. All joins use the exact `keeper_*` name; list position and display order are not used.
- The second export contains 167 named reviews and 173 status rows. Canonical state derived from each named review is 96 Happy, 68 Awaiting new draft review, 3 Review later and 6 Unreviewed.
- Four stale status-list entries disagree with the corresponding named review flags: `keeper_anti_gravity`, `keeper_bath_exit`, `keeper_count_money` and `keeper_nap_seated`. The generated page safely uses the named review flags; the immutable source export is not edited.

## Exact semantic delta

The first and second exports differ semantically for 31 animations:

`keeper_anti_gravity`, `keeper_bath_enter`, `keeper_bath_exit`, `keeper_carry_shopping`, `keeper_clear_snow`, `keeper_collect_eggs_back`, `keeper_count_money`, `keeper_crouch_work_back`, `keeper_darts`, `keeper_drink_pint`, `keeper_drive_speedboat`, `keeper_eat_seated`, `keeper_fish_feed_up`, `keeper_fish_seated`, `keeper_fish_standing`, `keeper_guitar_pickup_acoustic`, `keeper_guitar_pickup_flying_v_1967`, `keeper_guitar_pickup_gretsch`, `keeper_hot_drink_pickup`, `keeper_hot_drink_pour`, `keeper_lawn_mower_push`, `keeper_lean_table_back`, `keeper_lift_button_front`, `keeper_lift_weights_back`, `keeper_machete_side`, `keeper_meal_from_oven_back`, `keeper_meal_place_side`, `keeper_mechanic_walk_front`, `keeper_nap_seated`, `keeper_operate_outboard`, `keeper_parachute_drift`.

Four were status-only acceptances and were not regenerated: `keeper_anti_gravity`, `keeper_count_money`, `keeper_drink_pint`, `keeper_drive_speedboat`.

The other 27 were regenerated from the second-round review data. `keeper_parachute_landing` was also regenerated solely to preserve its exact resized drift-to-landing entry hand-off; it is not an additional review delta.

## Cropping and source-overlap correction

Every one of the 191 review-source sheets now passes a permanent per-frame lateral-gutter check: no opaque pixel touches a registered frame's left or right edge. This prevents runtime pixels from crossing into the adjacent frame.

The final changed strips were also inspected for fragments just inside a cell. `keeper_clear_snow`, `keeper_darts` and `keeper_machete_side` required new isolated grid sources because their earlier one-row generated sources painted long props over neighbouring poses. `keeper_lawn_mower_push` was recoverable deterministically by retaining only its connected actor/tool pose. The dart production strip has 14 frames, released darts only in frames 11–13, a clean neutral frame 14 and no frame 15.

## Workflow and documentation audit

The review page imports a version-9 review JSON by exact animation name, rejects unknown or duplicate names, preserves complete notes, derives status from the named review flags, and keeps Codex responses generated and read-only. Offline and online browser storage do not synchronise automatically: transfer progress with Export on one copy and Import review JSON on the other.

The documentation audit reconciled the review counts, 1,475-frame audit total, immutable export hashes, offline transfer behaviour, source provenance, generated resolution register and permanent verifier. No historical accepted/unchanged animation was regenerated.
