# Kitchen coordinated asset families V33–V38

Date: 18 October 2026
Status: complete reversible review drafts; awaiting visual review; unpromoted/unwired
Reviews: `/keeper-review/kitchen-kettle-states-v33/` through `/keeper-review/kitchen-table-states-v38/`

Frank approved the V32 fridge as excellent and authorised the remaining kitchen
sequence. Each successor was drawn as its own coordinated source family, then
normalised into crisp game-scale pixels against the same approved V23/V31
continuous fitted galley. No Final or runtime file changes.

- V33 kettle: standard, on and broken. On uses a small separate spout-steam
  loop. The broken handle has one failed mounting but remains attached; its
  sprung lid, dent and enamel chip are static.
- V34 toaster: standard, on and broken. On has its lever down and both bread
  tops visible, with a separate restrained heat layer. Broken has crooked
  jammed bread, a bent lever and a loosened scorched seam, with no flame,
  smoke, spark or electrical flash.
- V35 oven: standard/off, on and broken. Standard has no light. On has turned
  dials, a red indicator, warm interior light and a readable roasting tin.
  Broken has a static attached askew door; billowing door smoke and two hob
  flames are separate reusable layers.
- V36 mixing bowl: standard and broken. The same painted ceramic construction
  becomes a few large recognisable pieces. No intact bowl is present beneath
  the broken drawing and no animation is required.
- V37 basin: standard/dry, on and broken. A narrow gentle flow and the broken
  tap's upward spray are separate reusable layers; the cracked tilted tap and
  cabinet stay static.
- V38 table: standard and broken. The broken table is its own drawing rather
  than damage placed over the intact sprite. Its front-left leg remains partly
  attached, the damaged foot meets the floor and no animation is required.

Every moving environmental layer is 40 frames at 4 fps for a ten-second loop.
Every frame has transparent gutters; review playback remains locked until all
unique media URLs decode. Each page shows the V21/V23 authority beside the new
standard, every state at 4× inspection scale, and every state in the complete
772 × 224-pixel kitchen at exact game size. The active review lineage remains
exact V5 plus all storm-blue versions from V20 onward. Older cream/brown review
sets stay recoverable under `review-archive/retired/` and are not republished.

Named SFX placeholders are recorded in each candidate catalogue:
`kitchen_kettle_heating_hiss_loop`, `kitchen_kettle_broken_handle_rattle`,
`kitchen_toaster_heating_hum_loop`, `kitchen_toaster_jammed_click`,
`kitchen_oven_on_fan_loop`, `kitchen_oven_broken_smoke_hiss_loop`,
`kitchen_oven_hob_flame_loop`, `kitchen_mixing_bowl_ceramic_break`,
`kitchen_basin_gentle_flow_loop`, `kitchen_basin_broken_spray_loop` and
`kitchen_table_broken_creak`.

## Rebuild and verification

- Build: `/usr/bin/python3 scripts/build_kitchen_asset_families_v33_v38.py`
- Focused gate: `npm run verify:kitchen-asset-families-v33-v38`
- Archive review media: `npm run archive:keeper-review`
- Full gate: `npm test`, `npm run typecheck`, `npm run build`

The six source directories retain the generated concept sheet, its SHA-256 and
the construction prompt summary. Native output and candidate catalogues live in
matching `art/raw/` and `art/drafts/` directories. Rejecting one family requires
discarding only that version's source/raw/draft/review/archive files.

## Verification and documentation audit result

The focused V32 and V33–V38 gates, the 122-set/2,552-reference review archive,
the complete 179-test repository suite, TypeScript and the production Next.js
build all pass. The active reviewer retains exact V5 and V20–V38 only. Its
canonical Keeper shell now factors 109 byte-identical `keeper_walk` lead-in
records through an explicit `leadInRef` fallback; the audit mirror remains
byte-identical, reviewer behaviour is unchanged, and the verified public
payload is 49.93 MiB.

The final documentation audit reconciled README, STATUS, DECISIONS, the V32
approval record, review routes, source/draft/raw paths, archive retention,
named SFX, test commands and the no-promotion boundary. The only unavailable
local check was binding a preview port inside the restricted sandbox; the
production build itself completed successfully and the deployed routes are
verified after delivery.
