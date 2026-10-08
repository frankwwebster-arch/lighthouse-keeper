# Floor and facility design review

Base: `cdb109b2904ce0834fa559760e5d34e1ddc8f4f2`. 71 discussed spaces/variants, including retired garage. All non-runtime numbers are proposals. Frank selected sharp detailed artwork and the original CRT style; coarse exports, the full-width lamp room and stretched TV are rejected. The top lantern cap is inset (95x35 logical), with a wraparound walkway, rather than an ordinary 110-wide floor. Density-4 source images preserve footprints and TV proportions. ON is required for operating devices; passive furniture uses standard art plus actor-layer occupied/seated poses. No progression code changed.

Standard bands: 110 × 35. Plates: 105 × 35. Kitchen base, lamp top, bedroom beneath lamp, other standard floors saved random middle position. Nonstandard previews show their separate proposed footprints. No fixed-height dependency.

## Decision register

- Marine lab: separate floor or aquarium specialization.
- Radio room: separate floor or weather-room expansion; migrate radio without removing activity.
- Greenhouse: garden tier 3 and/or separate facility; avoid double rewards.
- Lift: rear versus side core; current mission at five floors takes precedence over older seven-floor guidance.
- Transport: exact slide clearance and funicular route; no final shafts yet.
- Power: unit budget and zero-gravity costume; numbers are review proposals.
- Bank: capped modest interest rate, interval and grown-up controls undecided; balances never break.
- Bowling/gaming/hot-tub/roof bays: attachment and safe geometry still require review.
- Solar tracker: optional fourth tier discussed; held as separate candidate module.
- Native Codex Canvas tool unavailable; standalone review canvas is delivered, native publication remains outstanding.

## Kitchen / entrance (`kitchen`)

**standard · 110 × 35 logical pixels · fixed base / entrance**

**Layout:** Door left; fridge and range centre; tools and bowl right

**Activities:** Cook; snack; tidy; greet; feed cat

**Dependencies:** none

**Unlock challenge:** Day-one essential, never quiz-gated

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** locked

**Source:** docs/PRODUCTION_ASSET_KIT.md; docs/CODEX_BRIEF.md

**Asset inventory:** plate + structural kit; worktop, wall_shelf, hooks; shared keeper poses and fault/reveal effects are itemized in CSV.

### door

- obj_door: Runtime: Welcome the visitor in; 10 game min; social +22 (need caps apply); proposed specialist perk: greet visitor / 8 min. Old wooden door. Wooden entrance. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (10,0), logical frame 13x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_door_t2: Runtime: Welcome the visitor in; 9 game min; social +28 (need caps apply); proposed specialist perk: greet / 7 min; proposed peek reveals 1 visitor identity. Door with knocker and peephole. Knocker and peephole. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (10,0), logical frame 13x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_door_t3: Runtime: Welcome the visitor in; 7 game min; social +33 (need caps apply); proposed specialist perk: greet / 6 min; proposed visitor patience 30 vs 20 min. Smart door with doorbell camera. Doorbell camera and visitor-wait indicator. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (10,0), logical frame 13x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### fridge

- obj_fridge: PROPOSED, not coded: 4 item slots. Small under-counter fridge. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (30,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fridge_t2: PROPOSED, not coded: 8 item slots. Fridge-freezer. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (30,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fridge_t3: PROPOSED, not coded: 12 item slots. American-style fridge. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (30,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### cooker

- obj_cooker: Runtime: Make toast; 12 game min; hunger +22 (need caps apply); proposed specialist perk: 1 recipe serving / 35 min. Basic oven. Manual single burner/range. ON: 4-frame flame or service motion. Proposed location (53,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_cooker_t2: Runtime: Make toast; 10 game min; hunger +28 (need caps apply); proposed specialist perk: 2 servings / 30 min. Two-oven range. Two clearly marked burner controls. ON: 4-frame flame or service motion. Proposed location (53,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_cooker_t3: Runtime: Make toast; 8 game min; hunger +33 (need caps apply); proposed specialist perk: 3 servings / 25 min. Fancy professional kitchen. Three marked cooking slots and recipe display. ON: 4-frame flame or service motion. Proposed location (53,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### broom

- obj_broom: Runtime: Tidy up; 25 game min; tidiness +40, fun -6 (need caps apply); proposed specialist perk: 40 tidiness / 25 min. Broom. Broom and bristles. ON: 4-frame tool motion. Proposed location (76,0), logical frame 8x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_broom_t2: Runtime: Tidy up; 21 game min; tidiness +50, fun -6 (need caps apply); proposed specialist perk: 50 tidiness / 21 min. Hoover. Hoover body with hose. ON: 4-frame tool motion. Proposed location (76,0), logical frame 8x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_broom_t3: Runtime: Tidy up; 18 game min; tidiness +60, fun -6 (need caps apply); proposed specialist perk: 60 tidiness / 18 min. Robot hoover. Robot cleaner with wheels and automatic status light. ON: 4-frame tool motion. Proposed location (76,0), logical frame 8x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### petbowl

- obj_petbowl: Runtime: Feed the pet; 8 game min; social +8 (need caps apply); proposed specialist perk: 10 pet-care points / 12 min. Plain pet bowl. Plain bowl or simple hand-fed coop. ON: 4-frame feeding. Proposed location (95,0), logical frame 10x5; stable usePoint(-8,0), effectOrigin(0,-5), bubbleOrigin(0,-13), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_petbowl_t2: Runtime: Feed the pet; 7 game min; social +10 (need caps apply); proposed specialist perk: 15 pet-care points / 10 min. Bowl with the pet's name on it. Sturdier vessel with visible larger feed measure. ON: 4-frame feeding. Proposed location (95,0), logical frame 10x5; stable usePoint(-8,0), effectOrigin(0,-5), bubbleOrigin(0,-13), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_petbowl_t3: Runtime: Feed the pet; 6 game min; social +12 (need caps apply); proposed specialist perk: 20 pet-care points / 8 min. Automatic feeder. Automatic feed dispenser and timed indicator. ON: 4-frame feeding. Proposed location (95,0), logical frame 10x5; stable usePoint(-8,0), effectOrigin(0,-5), bubbleOrigin(0,-13), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Living room (`living`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** TV left; shelf centre; piano right; sofa foreground

**Activities:** TV; reading; music; sofa nap

**Dependencies:** none

**Unlock challenge:** Day-one relaxation

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** locked

**Source:** docs/PRODUCTION_ASSET_KIT.md; docs/CODEX_BRIEF.md

**Asset inventory:** plate + structural kit; sofa, rug, sea_chart; shared keeper poses and fault/reveal effects are itemized in CSV.

### tv

- obj_tv: Runtime: Watch TV; 40 game min; fun +30, energy -4 (need caps apply); proposed specialist perk: 30 fun / 40 game min. Old box telly. Charcoal CRT and wooden stand. ON: literal B B SEA wordmark from supplied BBC NEWS reference, NEWS title and newsreader head; Sport football match; Nature animals. Every tier needs all three channel strips; glass always opaque. Proposed location (23,0), logical frame 28x23; stable usePoint(14,0), effectOrigin(8,-18), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tv_t2: Runtime: Watch TV; 34 game min; fun +38, energy -4 (need caps apply); proposed specialist perk: 38 fun / 34 game min. Big flat-screen TV. Flat-screen with same stable stand and larger viewing area. ON: literal B B SEA wordmark from supplied BBC NEWS reference, NEWS title and newsreader head; Sport football match; Nature animals. Every tier needs all three channel strips; glass always opaque. Proposed location (23,0), logical frame 28x23; stable usePoint(14,0), effectOrigin(8,-18), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tv_t3: Runtime: Watch TV; 28 game min; fun +45, energy -4 (need caps apply); proposed specialist perk: 45 fun / 28 game min. Cinema wall with surround sound. Cinema-style screen and two compact speakers within fixed bounds. ON: literal B B SEA wordmark from supplied BBC NEWS reference, NEWS title and newsreader head; Sport football match; Nature animals. Every tier needs all three channel strips; glass always opaque. Proposed location (23,0), logical frame 28x23; stable usePoint(14,0), effectOrigin(8,-18), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### bookshelf

- obj_bookshelf: Runtime: Read a book; 40 game min; fun +26, energy +3 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Wobbly shelf. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (53,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bookshelf_t2: Runtime: Read a book; 34 game min; fun +33, energy +4 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Proper bookcase. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (53,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bookshelf_t3: Runtime: Read a book; 28 game min; fun +39, energy +5 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Library wall with a ladder. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (53,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### piano

- obj_piano: Runtime: Play the piano; 30 game min; fun +30, social +4 (need caps apply); proposed specialist perk: 30 fun and 4 social / 30 min. Old upright piano. Basic upright or small instrument casing. ON: 4-frame keys or bellows. Proposed location (85,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_piano_t2: Runtime: Play the piano; 26 game min; fun +38, social +5 (need caps apply); proposed specialist perk: 38 fun and 5 social / 26 min. Shiny upright piano. Improved keyboard/bellows and sound indicator. ON: 4-frame keys or bellows. Proposed location (85,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_piano_t3: Runtime: Play the piano; 21 game min; fun +45, social +6 (need caps apply); proposed specialist perk: 45 fun and 6 social / 21 min. Grand piano. Performance-ready casing and concert cue; keep frame bounds. ON: 4-frame keys or bellows. Proposed location (85,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bedroom with en suite (`bedroom`)

**standard · 110 × 35 logical pixels · immediately beneath lamp; moves with tower**

**Layout:** Bed left; phone and desk centre; partition at x74; bathroom right

**Activities:** Sleep; call; diary; wash; loo

**Dependencies:** none

**Unlock challenge:** Day-one essentials

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** locked

**Source:** docs/PRODUCTION_ASSET_KIT.md; docs/CODEX_BRIEF.md

**Asset inventory:** plate + structural kit; bedside_table, mirror, privacy_door; shared keeper poses and fault/reveal effects are itemized in CSV.

### bed

- obj_bed: Runtime: morning energy 80 percent; proposed specialist perk: 80 percent morning energy. Creaky single bed. Single bed and blue blanket. ON: 4-frame blanket rise. Proposed location (18,0), logical frame 30x14; stable usePoint(-8,0), effectOrigin(0,-14), bubbleOrigin(0,-22), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bed_t2: Runtime: morning energy 90 percent; proposed specialist perk: 90 percent morning energy. Comfy double bed. Double-style padded headboard within same frame. ON: 4-frame blanket rise. Proposed location (18,0), logical frame 30x14; stable usePoint(-8,0), effectOrigin(0,-14), bubbleOrigin(0,-22), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bed_t3: Runtime: morning energy 100 percent; proposed specialist perk: 100 percent morning energy. Royal four-poster. Four-poster silhouette with energy crest; same footprint. ON: 4-frame blanket rise. Proposed location (18,0), logical frame 30x14; stable usePoint(-8,0), effectOrigin(0,-14), bubbleOrigin(0,-22), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### phone

- obj_phone: Runtime: Phone a friend; 10 game min; social +12 (need caps apply); proposed specialist perk: 12 social / 20 min. Old dial phone. Manual handset or small serving counter. ON: 4-frame serving or ring. Proposed location (54,-20), logical frame 15x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_phone_t2: Runtime: Phone a friend; 9 game min; social +15 (need caps apply); proposed specialist perk: 15 social / 17 min. Cordless phone. Cordless/expanded service with readiness light. ON: 4-frame serving or ring. Proposed location (54,-20), logical frame 15x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_phone_t3: Runtime: Phone a friend; 7 game min; social +18 (need caps apply); proposed specialist perk: 18 social / 14 min. Video phone. Video or group-service screen and visitor cue. ON: 4-frame serving or ring. Proposed location (54,-20), logical frame 15x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### desk

- obj_desk: Runtime: Write in his diary; 20 game min; fun +10, social +6 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Little desk. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (54,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_desk_t2: Runtime: Write in his diary; 17 game min; fun +13, social +8 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Writing bureau. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (54,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_desk_t3: Runtime: Write in his diary; 14 game min; fun +15, social +9 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Inventor's desk. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (54,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (84,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (84,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (84,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (101,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (101,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (101,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Lamp room / inset lantern cap (`lamp`)

**lantern_cap · 95 × 35 logical pixels · always topmost**

**Layout:** Inset glazed iron lantern chamber; lamp centre; wraparound external walkway and telescope; no full-width domestic room

**Activities:** Light and polish lamp; spot ships

**Dependencies:** none

**Unlock challenge:** Day-one ship-safety duty

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** locked

**Source:** docs/PRODUCTION_ASSET_KIT.md; docs/CODEX_BRIEF.md

**Asset inventory:** plate + structural kit; lantern_glass, wrap_rail; shared keeper poses and fault/reveal effects are itemized in CSV.

### telescope

- obj_telescope: Runtime: Look through the telescope; 20 game min; fun +16 (need caps apply); proposed specialist perk: 3 common spotting targets. Brass telescope. Short brass telescope. ON: 4-frame scan. Proposed location (16,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_telescope_t2: Runtime: Look through the telescope; 17 game min; fun +20 (need caps apply); proposed specialist perk: 6 targets with 1 extra zoom step. Big spyglass on a stand. Longer optic on same tripod. ON: 4-frame scan. Proposed location (16,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_telescope_t3: Runtime: Look through the telescope; 14 game min; fun +24 (need caps apply); proposed specialist perk: 9 targets including whale and distant ship. Observatory telescope. Larger lens and spotting finder; stable tripod feet. ON: 4-frame scan. Proposed location (16,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### lamp

- obj_lamp: Runtime: Polish the lamp; 25 game min; tidiness +6 (need caps apply); proposed specialist perk: 4 game hours beam per fuel unit. Oil lamp. Basic: simple manual mechanism and few visible controls. ON: 4-frame lit core. Proposed location (52,0), logical frame 30x35; stable usePoint(-8,0), effectOrigin(0,-35), bubbleOrigin(0,-43), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lamp_t2: Runtime: Polish the lamp; 21 game min; tidiness +8 (need caps apply); proposed specialist perk: 8 game hours beam per fuel unit. Electric lamp. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame lit core. Proposed location (52,0), logical frame 30x35; stable usePoint(-8,0), effectOrigin(0,-35), bubbleOrigin(0,-43), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lamp_t3: Runtime: Polish the lamp; 18 game min; tidiness +9 (need caps apply); proposed specialist perk: full 14.5-hour game night/day cycle beam per charge. Mega beam. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame lit core. Proposed location (52,0), logical frame 30x35; stable usePoint(-8,0), effectOrigin(0,-35), bubbleOrigin(0,-43), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Aquarium (`aquarium`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Tank left/centre; feed station right; clear floor lane

**Activities:** Feed fish; balance habitat; study sea life

**Dependencies:** Fishy Business mission; fish specimens

**Unlock challenge:** Current Fishy Business mission; proposed varied habitat match and tank-balance puzzle

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** runtime hook; ecology mini-game proposal

**Source:** docs/FOR_CODEX.md; docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; habitat_chart, fish_variants, tank_plants; shared keeper poses and fault/reveal effects are itemized in CSV.

### tank

- obj_tank: Runtime: Watch the fish; 25 game min; fun +22, energy +4 (need caps apply); proposed specialist perk: 1 cargo or task slot. Small fish tank. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (23,0), logical frame 38x26; stable usePoint(-8,0), effectOrigin(0,-26), bubbleOrigin(0,-34), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tank_t2: Runtime: Watch the fish; 21 game min; fun +28, energy +5 (need caps apply); proposed specialist perk: 2 cargo or task slots. Big tank. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (23,0), logical frame 38x26; stable usePoint(-8,0), effectOrigin(0,-26), bubbleOrigin(0,-34), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tank_t3: Runtime: Watch the fish; 18 game min; fun +33, energy +6 (need caps apply); proposed specialist perk: 3 cargo or task slots. Wall-sized reef tank. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (23,0), logical frame 38x26; stable usePoint(-8,0), effectOrigin(0,-26), bubbleOrigin(0,-34), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### fishfood

- obj_fishfood: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic fishfood. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (50,0), logical frame 8x12; stable usePoint(-8,0), effectOrigin(0,-12), bubbleOrigin(0,-20), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Workshop (`workshop`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Parts drawers left; workbench centre; test jig right

**Activities:** Repair; choose parts; build inventions

**Dependencies:** breakdowns

**Unlock challenge:** Repair distinct fault types; choose tools; assemble a working mechanism

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: global fault reduction needs playtesting

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; pegboard, tool_rack; shared keeper poses and fault/reveal effects are itemized in CSV.

### repairbench

- obj_repairbench: PROPOSED, not coded: 25 game min per repair. Basic repairbench. Hand tools and pegboard. ON: 4-frame tool jig. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_repairbench_t2: PROPOSED, not coded: 20 game min per repair. Mid-tier repairbench. Powered repair jig. ON: 4-frame tool jig. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_repairbench_t3: PROPOSED, not coded: 15 game min per repair. Top-tier repairbench. Diagnostic display and efficient tool station; do not promise global fault reduction. ON: 4-frame tool jig. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### partsbin

- obj_partsbin: PROPOSED, not coded: 4 item slots. Basic partsbin. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_partsbin_t2: PROPOSED, not coded: 8 item slots. Mid-tier partsbin. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_partsbin_t3: PROPOSED, not coded: 12 item slots. Top-tier partsbin. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### testjig

- obj_testjig: PROPOSED, not coded: 1 completed batch / 30 min. Basic testjig. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_testjig_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier testjig. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_testjig_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier testjig. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Weather station (`weather`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Gauge left; chart centre; radio right; external sensor feed

**Activities:** Forecast; record rain and wind; warn ships

**Dependencies:** none

**Unlock challenge:** Observe weather at distinct times; interpret chart; issue correct warning

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** locked geometry; future forecast simulation proposal

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; forecast_chart, sensor_cable; shared keeper poses and fault/reveal effects are itemized in CSV.

### barometer

- obj_barometer: Runtime: Check the weather; 10 game min; fun +6 (need caps apply); proposed specialist perk: 6 game hours warning. Barometer. One brass dial. ON: 4-frame needle. Proposed location (13,0), logical frame 18x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_barometer_t2: Runtime: Check the weather; 9 game min; fun +8 (need caps apply); proposed specialist perk: 12 game hours warning. Weather instruments. Instrument cluster. ON: 4-frame needle. Proposed location (13,0), logical frame 18x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_barometer_t3: Runtime: Check the weather; 7 game min; fun +9 (need caps apply); proposed specialist perk: 24 game hours warning. Weather computer. Forecast terminal with clear lead-time indicator. ON: 4-frame needle. Proposed location (13,0), logical frame 18x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### radio

- obj_radio: Runtime: Chat on the radio; 20 game min; social +24, fun +6 (need caps apply); proposed specialist perk: 1 signal decoded / 20 min. Crackly radio. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (38,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_radio_t2: Runtime: Chat on the radio; 17 game min; social +30, fun +8 (need caps apply); proposed specialist perk: 2 signals / 17 min. Ship-to-shore radio. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (38,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_radio_t3: Runtime: Chat on the radio; 14 game min; social +36, fun +9 (need caps apply); proposed specialist perk: 3 signals / 14 min. Coastguard radio desk. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (38,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### raingauge

- obj_raingauge: PROPOSED, not coded: one rain reading / 10 min. Basic raingauge. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (65,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### windvane

- obj_windvane: PROPOSED, not coded: one wind direction / 10 min. Basic windvane. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (91,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Marine laboratory (`marine_lab`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Sample shelves left; microscope centre; test sink right

**Activities:** Microscopy; habitat research; water testing

**Dependencies:** aquarium; specimens from fishing or diving

**Unlock challenge:** Match specimens to habitats; examine sample; balance water

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: separate lab or aquarium specialization

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; specimen_jars, habitat_chart; shared keeper poses and fault/reveal effects are itemized in CSV.

### microscope

- obj_microscope: PROPOSED, not coded: resolve 1 sample detail. Basic microscope. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_microscope_t2: PROPOSED, not coded: 2 sample details. Mid-tier microscope. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_microscope_t3: PROPOSED, not coded: 3 details including small plankton. Top-tier microscope. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### sampletank

- obj_sampletank: PROPOSED, not coded: 1 habitat group. Basic sampletank. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_sampletank_t2: PROPOSED, not coded: 2 separately filtered habitat groups. Mid-tier sampletank. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_sampletank_t3: PROPOSED, not coded: 3 habitat groups. Top-tier sampletank. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### waterkit

- obj_waterkit: PROPOSED, not coded: one salinity reading / 10 min. Basic waterkit. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Radio room (`radio_room`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Radio desk centre; signal board left; map right

**Activities:** Decode; rescue calls; relay locations

**Dependencies:** power; aerial

**Unlock challenge:** Repair aerial; decode short signal; relay chart location

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: standalone or weather-room expansion

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; code_chart, headphones; shared keeper poses and fault/reveal effects are itemized in CSV.

### radio

- obj_radio: Runtime: Chat on the radio; 20 game min; social +24, fun +6 (need caps apply); proposed specialist perk: 1 signal decoded / 20 min. Crackly radio. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (16,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_radio_t2: Runtime: Chat on the radio; 17 game min; social +30, fun +8 (need caps apply); proposed specialist perk: 2 signals / 17 min. Ship-to-shore radio. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (16,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_radio_t3: Runtime: Chat on the radio; 14 game min; social +36, fun +9 (need caps apply); proposed specialist perk: 3 signals / 14 min. Coastguard radio desk. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (16,0), logical frame 24x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### signaldecoder

- obj_signaldecoder: PROPOSED, not coded: 1 signal decoded / 20 min. Basic signaldecoder. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (43,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_signaldecoder_t2: PROPOSED, not coded: 2 signals / 17 min. Mid-tier signaldecoder. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (43,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_signaldecoder_t3: PROPOSED, not coded: 3 signals / 14 min. Top-tier signaldecoder. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (43,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### aerial

- obj_aerial: PROPOSED, not coded: 1 signal decoded / 20 min. Basic aerial. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (69,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_aerial_t2: PROPOSED, not coded: 2 signals / 17 min. Mid-tier aerial. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (69,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_aerial_t3: PROPOSED, not coded: 3 signals / 14 min. Top-tier aerial. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (69,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Map and chart room (`map_room`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Chart table centre; map archive left; route pins right

**Activities:** Plot routes; discover islands; chart rocks

**Dependencies:** sightings; boat for routes

**Unlock challenge:** Orient recovered fragments; plot one safe route

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; compass_prop, map_fragments; shared keeper poses and fault/reveal effects are itemized in CSV.

### charttable

- obj_charttable: PROPOSED, not coded: 1 route with 3 waypoints. Basic charttable. Basic: simple manual mechanism and few visible controls. ON: 4-frame route highlight. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_charttable_t2: PROPOSED, not coded: 2 saved routes with 5 waypoints. Mid-tier charttable. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame route highlight. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_charttable_t3: PROPOSED, not coded: 3 saved routes with 7 waypoints. Top-tier charttable. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame route highlight. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### maparchive

- obj_maparchive: PROPOSED, not coded: 1 clue per 20 game min. Basic maparchive. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_maparchive_t2: PROPOSED, not coded: 2 clues per 17 game min. Mid-tier maparchive. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_maparchive_t3: PROPOSED, not coded: 3 clues per 14 game min. Top-tier maparchive. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Observatory (`observatory`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Scope left; star chart centre; moon dial right

**Activities:** Stars; moon phases; direction puzzles

**Dependencies:** night sky; power optional

**Unlock challenge:** Identify constellations; use North Star to find a bearing

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; no fixed height

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; star_chart, moon_phase_tiles; shared keeper poses and fault/reveal effects are itemized in CSV.

### telescope

- obj_telescope: Runtime: Look through the telescope; 20 game min; fun +16 (need caps apply); proposed specialist perk: 3 common spotting targets. Brass telescope. Short brass telescope. ON: 4-frame scan. Proposed location (15,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_telescope_t2: Runtime: Look through the telescope; 17 game min; fun +20 (need caps apply); proposed specialist perk: 6 targets with 1 extra zoom step. Big spyglass on a stand. Longer optic on same tripod. ON: 4-frame scan. Proposed location (15,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_telescope_t3: Runtime: Look through the telescope; 14 game min; fun +24 (need caps apply); proposed specialist perk: 9 targets including whale and distant ship. Observatory telescope. Larger lens and spotting finder; stable tripod feet. ON: 4-frame scan. Proposed location (15,0), logical frame 23x23; stable usePoint(-8,0), effectOrigin(0,-23), bubbleOrigin(0,-31), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### stardial

- obj_stardial: PROPOSED, not coded: one moon/sky bearing reading / 10 min. Basic stardial. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (42,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Library (`library`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Migrated shelf left; reading desk centre; clue cabinet right

**Activities:** Stories; lighthouse history; practical research

**Dependencies:** bookshelf migration

**Unlock challenge:** Recover and sort books; solve a repair using a passage

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; reading_chair, book_props; shared keeper poses and fault/reveal effects are itemized in CSV.

### bookshelf

- obj_bookshelf: Runtime: Read a book; 40 game min; fun +26, energy +3 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Wobbly shelf. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (14,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bookshelf_t2: Runtime: Read a book; 34 game min; fun +33, energy +4 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Proper bookcase. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (14,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bookshelf_t3: Runtime: Read a book; 28 game min; fun +39, energy +5 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Library wall with a ladder. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (14,0), logical frame 20x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### readingdesk

- obj_readingdesk: PROPOSED, not coded: 1 clue per 20 game min. Basic readingdesk. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (39,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_readingdesk_t2: PROPOSED, not coded: 2 clues per 17 game min. Mid-tier readingdesk. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (39,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_readingdesk_t3: PROPOSED, not coded: 3 clues per 14 game min. Top-tier readingdesk. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (39,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Music room (`music`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Piano left; percussion centre; accordion and record player right

**Activities:** Melodies; rhythm; visitor concert

**Dependencies:** piano migration

**Unlock challenge:** Copy melody; identify sounds; perform for visitor

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; music_stand, score_props; shared keeper poses and fault/reveal effects are itemized in CSV.

### piano

- obj_piano: Runtime: Play the piano; 30 game min; fun +30, social +4 (need caps apply); proposed specialist perk: 30 fun and 4 social / 30 min. Old upright piano. Basic upright or small instrument casing. ON: 4-frame keys or bellows. Proposed location (16,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_piano_t2: Runtime: Play the piano; 26 game min; fun +38, social +5 (need caps apply); proposed specialist perk: 38 fun and 5 social / 26 min. Shiny upright piano. Improved keyboard/bellows and sound indicator. ON: 4-frame keys or bellows. Proposed location (16,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_piano_t3: Runtime: Play the piano; 21 game min; fun +45, social +6 (need caps apply); proposed specialist perk: 45 fun and 6 social / 21 min. Grand piano. Performance-ready casing and concert cue; keep frame bounds. ON: 4-frame keys or bellows. Proposed location (16,0), logical frame 25x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### drums

- obj_drums: PROPOSED, not coded: 30 fun and 4 social / 30 min. Basic drums. Basic upright or small instrument casing. ON: 4-frame keys or bellows. Proposed location (43,0), logical frame 20x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drums_t2: PROPOSED, not coded: 38 fun and 5 social / 26 min. Mid-tier drums. Improved keyboard/bellows and sound indicator. ON: 4-frame keys or bellows. Proposed location (43,0), logical frame 20x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drums_t3: PROPOSED, not coded: 45 fun and 6 social / 21 min. Top-tier drums. Performance-ready casing and concert cue; keep frame bounds. ON: 4-frame keys or bellows. Proposed location (43,0), logical frame 20x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### accordion

- obj_accordion: PROPOSED, not coded: 30 fun and 4 social / 30 min. Basic accordion. Basic upright or small instrument casing. ON: 4-frame keys or bellows. Proposed location (66,0), logical frame 18x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_accordion_t2: PROPOSED, not coded: 38 fun and 5 social / 26 min. Mid-tier accordion. Improved keyboard/bellows and sound indicator. ON: 4-frame keys or bellows. Proposed location (66,0), logical frame 18x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_accordion_t3: PROPOSED, not coded: 45 fun and 6 social / 21 min. Top-tier accordion. Performance-ready casing and concert cue; keep frame bounds. ON: 4-frame keys or bellows. Proposed location (66,0), logical frame 18x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### gramophone

- obj_gramophone: PROPOSED, not coded: 30 fun and 4 social / 30 min. Basic gramophone. Basic upright or small instrument casing. ON: 4-frame keys or bellows. Proposed location (87,0), logical frame 16x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gramophone_t2: PROPOSED, not coded: 38 fun and 5 social / 26 min. Mid-tier gramophone. Improved keyboard/bellows and sound indicator. ON: 4-frame keys or bellows. Proposed location (87,0), logical frame 16x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gramophone_t3: PROPOSED, not coded: 45 fun and 6 social / 21 min. Top-tier gramophone. Performance-ready casing and concert cue; keep frame bounds. ON: 4-frame keys or bellows. Proposed location (87,0), logical frame 16x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Artist studio (`artist`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Easel left; mixing table centre; pottery wheel right

**Activities:** Paint; mix colours; pottery; decorate rooms

**Dependencies:** world colour discoveries

**Unlock challenge:** Mix two colours; make visitor picture; fire clay safely

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; kiln powered

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; paint_palette, clay_props, picture_frames; shared keeper poses and fault/reveal effects are itemized in CSV.

### easel

- obj_easel: PROPOSED, not coded: 1 completed batch / 30 min. Basic easel. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_easel_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier easel. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_easel_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier easel. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### potterywheel

- obj_potterywheel: PROPOSED, not coded: 1 completed batch / 30 min. Basic potterywheel. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_potterywheel_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier potterywheel. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_potterywheel_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier potterywheel. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### kiln

- obj_kiln: PROPOSED, not coded: 1 completed batch / 30 min. Basic kiln. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_kiln_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier kiln. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_kiln_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier kiln. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Curated computer room (`computer`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Computer and migrated desk centre; message slots left; printer right

**Activities:** Fictional mail; newspaper; forecasts; research; games

**Dependencies:** power; desk migration

**Unlock challenge:** Order a reply; interpret a headline; research a practical task

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** locked curated content; no live internet

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; mail_cards, newspaper_tiles; shared keeper poses and fault/reveal effects are itemized in CSV.

### computer

- obj_computer: PROPOSED, not coded: 1 clue per 20 game min. Basic computer. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_computer_t2: PROPOSED, not coded: 2 clues per 17 game min. Mid-tier computer. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_computer_t3: PROPOSED, not coded: 3 clues per 14 game min. Top-tier computer. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### desk

- obj_desk: Runtime: Write in his diary; 20 game min; fun +10, social +6 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Little desk. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (42,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_desk_t2: Runtime: Write in his diary; 17 game min; fun +13, social +8 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Writing bureau. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (42,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_desk_t3: Runtime: Write in his diary; 14 game min; fun +15, social +9 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Inventor's desk. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (42,0), logical frame 25x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### printer

- obj_printer: PROPOSED, not coded: 1 completed batch / 30 min. Basic printer. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (70,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_printer_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier printer. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (70,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_printer_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier printer. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (70,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Storage / box room (attic fantasy) (`storage`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Three clear shelving zones; movable boxes foreground

**Activities:** Inspect clutter; search; move and stack boxes

**Dependencies:** none

**Unlock challenge:** Memorize a box field; recover requested part; stack safely

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; never forced above bedroom

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; box_variants, lost_parts; shared keeper poses and fault/reveal effects are itemized in CSV.

### boxrack

- obj_boxrack: PROPOSED, not coded: 4 item slots. Basic boxrack. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boxrack_t2: PROPOSED, not coded: 8 item slots. Mid-tier boxrack. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boxrack_t3: PROPOSED, not coded: 12 item slots. Top-tier boxrack. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### searchchest

- obj_searchchest: PROPOSED, not coded: 1 searchable compartment / 15 min. Basic searchchest. Basic: simple manual mechanism and few visible controls. ON: 4-frame searching. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_searchchest_t2: PROPOSED, not coded: 2 compartments / 13 min. Mid-tier searchchest. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame searching. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_searchchest_t3: PROPOSED, not coded: 3 compartments / 11 min. Top-tier searchchest. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame searching. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Food store / larder (`food_store`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Dry shelves left; cool cabinet centre; basket station right

**Activities:** Store ingredients; plan meals; preserve surplus

**Dependencies:** kitchen; supplies

**Unlock challenge:** Sort food by storage need; prepare varied meal basket

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** discussed system link; room form review

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; food_jars, ingredient_crates; shared keeper poses and fault/reveal effects are itemized in CSV.

### lardershelf

- obj_lardershelf: PROPOSED, not coded: 4 item slots. Basic lardershelf. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lardershelf_t2: PROPOSED, not coded: 8 item slots. Mid-tier lardershelf. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lardershelf_t3: PROPOSED, not coded: 12 item slots. Top-tier lardershelf. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### preserver

- obj_preserver: PROPOSED, not coded: 4 item slots. Basic preserver. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_preserver_t2: PROPOSED, not coded: 8 item slots. Mid-tier preserver. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_preserver_t3: PROPOSED, not coded: 12 item slots. Top-tier preserver. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Dining room (`dining`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Table centre; serving hatch left; dishes right

**Activities:** Meals; table setting; celebrations

**Dependencies:** kitchen; visitors; table migration

**Unlock challenge:** Set correct places; serve varied meal; welcome visitor

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; chairs, cutlery, celebration_bunting; shared keeper poses and fault/reveal effects are itemized in CSV.

### diningtable

- obj_diningtable: PROPOSED, not coded: 12 social / 20 min. Basic diningtable. Manual handset or small serving counter. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_diningtable_t2: PROPOSED, not coded: 15 social / 17 min. Mid-tier diningtable. Cordless/expanded service with readiness light. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_diningtable_t3: PROPOSED, not coded: 18 social / 14 min. Top-tier diningtable. Video or group-service screen and visitor cue. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### servinghatch

- obj_servinghatch: PROPOSED, not coded: 1 recipe serving / 35 min. Basic servinghatch. Manual single burner/range. ON: 4-frame flame or service motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_servinghatch_t2: PROPOSED, not coded: 2 servings / 30 min. Mid-tier servinghatch. Two clearly marked burner controls. ON: 4-frame flame or service motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_servinghatch_t3: PROPOSED, not coded: 3 servings / 25 min. Top-tier servinghatch. Three marked cooking slots and recipe display. ON: 4-frame flame or service motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bank / savings room (`bank`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Counter left; tube centre; safe right; readable account display

**Activities:** Count coins; deposit; withdraw; plan upgrade

**Dependencies:** allowance; persistent savings

**Unlock challenge:** Keep some allowance across days; verify counted receipt

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: capped interest amount and interval; balances never break

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; savings_book, receipt_props; shared keeper poses and fault/reveal effects are itemized in CSV.

### deposittube

- obj_deposittube: PROPOSED, not coded: 1 deposit processed / 10 min. Basic deposittube. Manual coin tube and receipt slot. ON: 4-frame coin transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_deposittube_t2: PROPOSED, not coded: 2 deposits / 8 min. Mid-tier deposittube. Twin-batch deposit mechanism. ON: 4-frame coin transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_deposittube_t3: PROPOSED, not coded: 3 deposits / 6 min. Top-tier deposittube. Triple-batch counter and balance display; no savings loss. ON: 4-frame coin transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### safe

- obj_safe: PROPOSED, not coded: 4 stored crates; money balance unlimited and unaffected. Basic safe. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_safe_t2: PROPOSED, not coded: 8 crates; money unaffected. Mid-tier safe. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_safe_t3: PROPOSED, not coded: 12 crates; money unaffected. Top-tier safe. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### coinscales

- obj_coinscales: PROPOSED, not coded: weigh one coin batch / 10 min. Basic coinscales. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Cinema (`cinema`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Screen left; benches centre; projector right

**Activities:** Fictional films; scene sequencing; adventure replays

**Dependencies:** power; visitors

**Unlock challenge:** Restore projector; order scenes; host screening

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; screen, benches, film_reels; shared keeper poses and fault/reveal effects are itemized in CSV.

### projector

- obj_projector: PROPOSED, not coded: 30 fun / 40 min screening. Basic projector. Charcoal CRT and wooden stand. ON: 4-frame channel flicker. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_projector_t2: PROPOSED, not coded: 38 fun / 34 min. Mid-tier projector. Flat-screen with same stable stand and larger viewing area. ON: 4-frame channel flicker. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_projector_t3: PROPOSED, not coded: 45 fun / 28 min. Top-tier projector. Cinema-style screen and two compact speakers within fixed bounds. ON: 4-frame channel flicker. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### filmarchive

- obj_filmarchive: PROPOSED, not coded: 1 clue per 20 game min. Basic filmarchive. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_filmarchive_t2: PROPOSED, not coded: 2 clues per 17 game min. Mid-tier filmarchive. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_filmarchive_t3: PROPOSED, not coded: 3 clues per 14 game min. Top-tier filmarchive. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Games hall (`games`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** One folding central table; replaceable game surface; wall darts Stations alternate in one central bay; not all displayed at once.

**Activities:** Snooker; table tennis; darts; table football; board games

**Dependencies:** games cabinet migration

**Unlock challenge:** Complete aiming, timing and arithmetic rounds

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: rotate game stations; cannot display all at once

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; cues, balls, paddles, scoreboard; shared keeper poses and fault/reveal effects are itemized in CSV.

### snooker

- obj_snooker: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic snooker. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_snooker_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier snooker. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_snooker_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier snooker. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### tabletennis

- obj_tabletennis: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic tabletennis. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tabletennis_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier tabletennis. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tabletennis_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier tabletennis. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### darts

- obj_darts: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic darts. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_darts_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier darts. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_darts_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier darts. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### tablefootball

- obj_tablefootball: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic tablefootball. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tablefootball_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier tablefootball. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tablefootball_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier tablefootball. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### boardgames

- obj_boardgames: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic boardgames. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boardgames_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier boardgames. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boardgames_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier boardgames. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (55,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Playroom (`playroom`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Pit left; soft obstacles centre; trampoline right

**Activities:** Ball-pit search; soft play; trampoline timing

**Dependencies:** none

**Unlock challenge:** Find clue ball; traverse short course; time bounce

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; colour_balls, padded_blocks; shared keeper poses and fault/reveal effects are itemized in CSV.

### ballpit

- obj_ballpit: PROPOSED, not coded: 1 searchable compartment / 15 min. Basic ballpit. Basic: simple manual mechanism and few visible controls. ON: 4-frame searching. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_ballpit_t2: PROPOSED, not coded: 2 compartments / 13 min. Mid-tier ballpit. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame searching. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_ballpit_t3: PROPOSED, not coded: 3 compartments / 11 min. Top-tier ballpit. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame searching. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### softplay

- obj_softplay: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic softplay. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_softplay_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier softplay. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_softplay_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier softplay. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### trampoline

- obj_trampoline: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic trampoline. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_trampoline_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier trampoline. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_trampoline_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier trampoline. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Imagination / themed room (`imagination`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** One 105x35 interchangeable set; clear movement lane; control pedestal

**Activities:** Six scene puzzles on a reusable stage

**Dependencies:** curated theme unlocks

**Unlock challenge:** Discover theme clue; complete its bespoke puzzle

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: theme selection and reward rules

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; scene_slots; shared keeper poses and fault/reveal effects are itemized in CSV.

### themecontrol

- obj_themecontrol: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic themecontrol. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_themecontrol_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier themecontrol. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_themecontrol_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier themecontrol. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Zero-gravity room (`zero_gravity`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Sealed entrance left; rings centre; padded nets and controls right

**Activities:** Float rings; orbit puzzle; recover floating items; astronaut training

**Dependencies:** observatory; stored power

**Unlock challenge:** Solve orbit sequence; reserve battery power; pass short floating course

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: power unit and costume silhouette

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; rings, padded_nets, floating_lunch; shared keeper poses and fault/reveal effects are itemized in CSV.

### gravitycontrol

- obj_gravitycontrol: PROPOSED, not coded: 10 game min float time per charge. Basic gravitycontrol. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gravitycontrol_t2: PROPOSED, not coded: 20 min per charge. Mid-tier gravitycontrol. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gravitycontrol_t3: PROPOSED, not coded: 30 min per charge. Top-tier gravitycontrol. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### orbitboard

- obj_orbitboard: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic orbitboard. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_orbitboard_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier orbitboard. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_orbitboard_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier orbitboard. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Conservatory (`conservatory`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Plants left; tea bench centre; reading seat right

**Activities:** Tea; read; social visits; tame overgrowth

**Dependencies:** decorative plants; visitors

**Unlock challenge:** Identify plant needs; arrange reading nook; host tea

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; indoor leisure not food greenhouse

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; decorative_plants, reading_seat; shared keeper poses and fault/reveal effects are itemized in CSV.

### teaset

- obj_teaset: PROPOSED, not coded: 12 social / 20 min. Basic teaset. Manual handset or small serving counter. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_teaset_t2: PROPOSED, not coded: 15 social / 17 min. Mid-tier teaset. Cordless/expanded service with readiness light. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_teaset_t3: PROPOSED, not coded: 18 social / 14 min. Top-tier teaset. Video or group-service screen and visitor cue. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### plantstand

- obj_plantstand: PROPOSED, not coded: 3 crop yields / 2 completed game days. Basic plantstand. Ground patch and three crop slots. ON: 2. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_plantstand_t2: PROPOSED, not coded: 6 crop yields / 2 days. Mid-tier plantstand. Raised beds with irrigation line. ON: 2. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_plantstand_t3: PROPOSED, not coded: 9 crop yields / 2 days. Top-tier plantstand. Glass greenhouse and protected crop gauge. ON: 2. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Family-friendly pub / inn (`pub`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Counter left; tables centre; games right; rear guest WC

**Activities:** Lemonade; cocoa; meals; quizzes; dominoes; darts; stories

**Dependencies:** visitors; kitchen

**Unlock challenge:** Prepare drink; solve team quiz; host storytelling

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** review: name; soft drinks only

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; bar_stools, story_cards; shared keeper poses and fault/reveal effects are itemized in CSV.

### drinkcounter

- obj_drinkcounter: PROPOSED, not coded: 12 social / 20 min. Basic drinkcounter. Manual handset or small serving counter. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drinkcounter_t2: PROPOSED, not coded: 15 social / 17 min. Mid-tier drinkcounter. Cordless/expanded service with readiness light. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drinkcounter_t3: PROPOSED, not coded: 18 social / 14 min. Top-tier drinkcounter. Video or group-service screen and visitor cue. ON: 4-frame serving or ring. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### dominoes

- obj_dominoes: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic dominoes. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_dominoes_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier dominoes. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_dominoes_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier dominoes. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### darts

- obj_darts: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic darts. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_darts_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier darts. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_darts_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier darts. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Swimming-pool floor (`pool`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Water ~90 percent; narrow foreground tile edge; ladder right; bathroom annex

**Activities:** Lengths; float; splash; retrieve; gentle rescue

**Dependencies:** boiler; pump; changing annex

**Unlock challenge:** Check water; use ladder; retrieve float; demonstrate rescue

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; bathroom annex preserves large water area

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; water_surface, inflatables, ladder; shared keeper poses and fault/reveal effects are itemized in CSV.

### poolpump

- obj_poolpump: PROPOSED, not coded: clean 1 water bay / 20 min. Basic poolpump. Single manual pump and pipe. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolpump_t2: PROPOSED, not coded: 2 bays / 17 min. Mid-tier poolpump. Two-way pump with visible valve. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolpump_t3: PROPOSED, not coded: 3 bays / 14 min. Top-tier poolpump. Three-way pump with filtering gauge. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### poolheater

- obj_poolheater: PROPOSED, not coded: heat pool for 30 min per charge. Basic poolheater. Pilot flame and one pressure band. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolheater_t2: PROPOSED, not coded: 60 min per charge. Mid-tier poolheater. Larger exchanger and two pressure bands. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolheater_t3: PROPOSED, not coded: 90 min per charge. Top-tier poolheater. Three service circuits and efficiency gauge. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Gym (`gym`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Exercise station left; mat centre; showers in annex right

**Activities:** Exercise; balance; comic flex and headstand

**Dependencies:** exercise equipment migration

**Unlock challenge:** Sequence warm-up; balance course; short varied workout

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** discussed; detailed equipment proposal

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; exercise_mat, balance_beam; shared keeper poses and fault/reveal effects are itemized in CSV.

### exercisebike

- obj_exercisebike: PROPOSED, not coded: 10 energy and 10 fun / 20 min. Basic exercisebike. Manual resistance equipment. ON: 4-frame cycling or lifting. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_exercisebike_t2: PROPOSED, not coded: 13 energy and 13 fun / 17 min. Mid-tier exercisebike. Adjustable resistance indicator. ON: 4-frame cycling or lifting. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_exercisebike_t3: PROPOSED, not coded: 15 energy and 15 fun / 14 min. Top-tier exercisebike. Progress display with efficient activity controls. ON: 4-frame cycling or lifting. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### weights

- obj_weights: PROPOSED, not coded: 10 energy and 10 fun / 20 min. Basic weights. Manual resistance equipment. ON: 4-frame cycling or lifting. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_weights_t2: PROPOSED, not coded: 13 energy and 13 fun / 17 min. Mid-tier weights. Adjustable resistance indicator. ON: 4-frame cycling or lifting. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_weights_t3: PROPOSED, not coded: 15 energy and 15 fun / 14 min. Top-tier weights. Progress display with efficient activity controls. ON: 4-frame cycling or lifting. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Boiler room (`boiler`)

**standard · 110 × 35 logical pixels · saved random middle slot**

**Layout:** Boiler centre; pipes left; gauge and service panel right

**Activities:** Heat; pressure diagnosis; reset and test tap

**Dependencies:** fuel or power; water services

**Unlock challenge:** Read pressure; select pipe/fuse/reset; test hot tap

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Nearest available toilet/wash point within about 3 bands; rear WC may be added after saved random placement. Never disable all essential fixtures.

**Decision/status:** approved idea; failure degrades water, never disables toilets

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; pipe_set, radiator; shared keeper poses and fault/reveal effects are itemized in CSV.

### boiler

- obj_boiler: PROPOSED, not coded: heat 1 connected service bay per charge. Basic boiler. Pilot flame and one pressure band. ON: 4-frame pressure flame. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boiler_t2: PROPOSED, not coded: heat 2 service bays per charge. Mid-tier boiler. Larger exchanger and two pressure bands. ON: 4-frame pressure flame. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boiler_t3: PROPOSED, not coded: heat 3 service bays per charge. Top-tier boiler. Three service circuits and efficiency gauge. ON: 4-frame pressure flame. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### pressuregauge

- obj_pressuregauge: PROPOSED, not coded: one pressure reading / 10 min. Basic pressuregauge. Basic: simple manual mechanism and few visible controls. ON: 4-frame reading. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Hidden underground lair (`lair`)

**underground · 110 × 35 logical pixels · concealed below terrain; revealed only on unlock**

**Layout:** Console left; gadget bench right; concealed rock walls

**Activities:** Gadgets; games; secret discoveries

**Dependencies:** Strange Rumblings mission

**Unlock challenge:** Current mission counts digging, visitors and quiz clues; future bespoke mechanism puzzle proposed

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** runtime hook; terrain reveal only on unlock

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; rock_lining, secret_door; shared keeper poses and fault/reveal effects are itemized in CSV.

### console

- obj_console: Runtime: Use the secret computer; 30 game min; fun +28, energy -4 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Old computer. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_console_t2: Runtime: Use the secret computer; 26 game min; fun +35, energy -4 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Gaming PC. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_console_t3: Runtime: Use the secret computer; 21 game min; fun +42, energy -4 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Supercomputer wall. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### gadgets

- obj_gadgets: Runtime: Tinker with gadgets; 30 game min; fun +24, tidiness -8 (need caps apply); proposed specialist perk: 1 completed batch / 30 min. Workbench. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (50,0), logical frame 28x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gadgets_t2: Runtime: Tinker with gadgets; 26 game min; fun +30, tidiness -8 (need caps apply); proposed specialist perk: 2 batches / 26 min. Gadget bench. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (50,0), logical frame 28x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_gadgets_t3: Runtime: Tinker with gadgets; 21 game min; fun +36, tidiness -8 (need caps apply); proposed specialist perk: 3 batches / 21 min. Robot lab. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (50,0), logical frame 28x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bedroom en suite (`ensuite`)

**subroom · 36 × 35 logical pixels · inside parent; no independent slot**

**Layout:** Within bedroom x74..110; opaque privacy door; basin then loo

**Activities:** Wash; brush teeth; loo

**Dependencies:** bedroom

**Unlock challenge:** Essential from day one

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** locked; no independent stack slot

**Source:** docs/PRODUCTION_ASSET_KIT.md; docs/CODEX_BRIEF.md

**Asset inventory:** plate + structural kit; mirror, privacy_door; shared keeper poses and fault/reveal effects are itemized in CSV.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (10,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (10,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (10,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (27,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (27,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (27,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Pool changing / bathrooms (`pool_changing`)

**service_bay · 66 × 35 logical pixels · rear amenity bay attached to parent**

**Layout:** 66x35 rear annex; cubicle left; basin and loo right

**Activities:** Hidden outfit swap; shower; wash; loo

**Dependencies:** pool

**Unlock challenge:** Included with pool; basic needs never gated

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** proposal footprint; swimming suit reused

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; changing_cubicle, privacy_door; shared keeper poses and fault/reveal effects are itemized in CSV.

### shower

- obj_shower: PROPOSED, not coded: 40 hygiene / 15 min. Basic shower. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_shower_t2: PROPOSED, not coded: 50 hygiene / 13 min. Mid-tier shower. Added mixer/shower control. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_shower_t3: PROPOSED, not coded: 60 hygiene / 11 min. Top-tier shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Gym changing / shower (`gym_changing`)

**service_bay · 66 × 35 logical pixels · rear amenity bay attached to parent**

**Layout:** 66x35 rear annex; shower left; fixtures right

**Activities:** Wash; loo; dress

**Dependencies:** gym

**Unlock challenge:** Included with gym

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** proposal footprint

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; lockers, privacy_door; shared keeper poses and fault/reveal effects are itemized in CSV.

### shower

- obj_shower: PROPOSED, not coded: 40 hygiene / 15 min. Basic shower. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_shower_t2: PROPOSED, not coded: 50 hygiene / 13 min. Mid-tier shower. Added mixer/shower control. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_shower_t3: PROPOSED, not coded: 60 hygiene / 11 min. Top-tier shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (13,0), logical frame 18x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (34,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (53,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Guest toilet (`pub_wc`)

**service_bay · 44 × 35 logical pixels · rear amenity bay attached to parent**

**Layout:** 44x35 rear service bay; privacy screens

**Activities:** Wash; loo

**Dependencies:** pub

**Unlock challenge:** Included with inn

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** proposal footprint

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; privacy_door, mirror; shared keeper poses and fault/reveal effects are itemized in CSV.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Distributed service WC (`service_wc`)

**service_bay · 44 × 35 logical pixels · rear amenity bay attached to parent**

**Layout:** 44x35 rear bay; repeated fixture kit

**Activities:** Wash; loo

**Dependencies:** walking-distance policy

**Unlock challenge:** Add where saved layout exceeds three-band access target

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: placement hook; never all fixtures broken at once

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; privacy_door, pipe_set; shared keeper poses and fault/reveal effects are itemized in CSV.

### basin

- obj_basin: Runtime: Have a wash; 15 game min; hygiene +40 (need caps apply); proposed specialist perk: 40 hygiene / 15 min. Chipped wash basin. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t2: Runtime: Have a wash; 13 game min; hygiene +50 (need caps apply); proposed specialist perk: 50 hygiene / 13 min. Basin with a shower. Added mixer/shower control. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_basin_t3: Runtime: Have a wash; 11 game min; hygiene +60 (need caps apply); proposed specialist perk: 60 hygiene / 11 min. Spa bathroom with rainfall shower. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (12,0), logical frame 15x28; stable usePoint(-8,0), effectOrigin(0,-28), bubbleOrigin(0,-36), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### toilet

- obj_toilet: Runtime: Go to the loo; 8 game min; bladder +70 (need caps apply); proposed specialist perk: 70 bladder / 8 min. Clanky loo. Cistern and plain seat. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t2: Runtime: Go to the loo; 7 game min; bladder +88 (need caps apply); proposed specialist perk: 88 bladder / 7 min. Quiet-flush loo. Quiet-flush cistern with handle indicator. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_toilet_t3: Runtime: Go to the loo; 6 game min; bladder +105 (need caps apply); proposed specialist perk: 105 nominal bladder capped at 100 / 6 min. Heated-seat loo with music. Heated-seat switch and comfort indicator. ON: 4-frame flush. Proposed location (31,0), logical frame 13x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bath / laundry service possibility (`bath`)

**service_bay · 55 × 35 logical pixels · rear amenity bay attached to parent**

**Layout:** Proposed 55x35 utility bay; tub left; washer right Stations alternate in one central bay; not all displayed at once.

**Activities:** Bath; wash clothes

**Dependencies:** boiler; water; possible future laundry

**Unlock challenge:** Diagnose water; sort garments; test service

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed optional systems; do not produce until chosen

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; laundry_basket, pipe_set; shared keeper poses and fault/reveal effects are itemized in CSV.

### bathtub

- obj_bathtub: PROPOSED, not coded: 40 hygiene / 15 min. Basic bathtub. Simple pedestal tap or basic shower. ON: 4-frame water. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bathtub_t2: PROPOSED, not coded: 50 hygiene / 13 min. Mid-tier bathtub. Added mixer/shower control. ON: 4-frame water. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bathtub_t3: PROPOSED, not coded: 60 hygiene / 11 min. Top-tier bathtub. Rainfall head and warm-water status light. ON: 4-frame water. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### washer

- obj_washer: PROPOSED, not coded: 40 tidiness / 25 min. Basic washer. Broom and bristles. ON: 4-frame tool motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_washer_t2: PROPOSED, not coded: 50 tidiness / 21 min. Mid-tier washer. Hoover body with hose. ON: 4-frame tool motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_washer_t3: PROPOSED, not coded: 60 tidiness / 18 min. Top-tier washer. Robot cleaner with wheels and automatic status light. ON: 4-frame tool motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Lift service core (`lift`)

**service_core · 22 × 35 logical pixels · aligned service core; follows saved floor exits**

**Layout:** 22x35 repeatable landing bay; vertical shaft extends with saved stack Stations alternate in one central bay; not all displayed at once.

**Activities:** Fast travel; repair doors

**Dependencies:** current Puffed Out requires five above-ground floors

**Unlock challenge:** Current mission; future safe load and door test

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: rear versus side core; do not create final shaft art

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; landing_door, shaft_segment, indicator; shared keeper poses and fault/reveal effects are itemized in CSV.

### lift

- obj_lift: PROPOSED, not coded: 8 game min per floor or route segment. Basic lift. Simple manual carrier or landing. ON: 4-frame travel. Proposed location (11,0), logical frame 22x34; stable usePoint(-8,0), effectOrigin(0,-34), bubbleOrigin(0,-42), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lift_t2: PROPOSED, not coded: 5 game min per segment. Mid-tier lift. Improved motor/brake and clear floor indicator. ON: 4-frame travel. Proposed location (11,0), logical frame 22x34; stable usePoint(-8,0), effectOrigin(0,-34), bubbleOrigin(0,-42), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_lift_t3: PROPOSED, not coded: 3 game min per segment. Top-tier lift. Fast automatic carrier with route and safety indicator. ON: 4-frame travel. Proposed location (11,0), logical frame 22x34; stable usePoint(-8,0), effectOrigin(0,-34), bubbleOrigin(0,-42), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Ladders / spiral stair core (`stairs`)

**service_core · 10 × 35 logical pixels · aligned service core; follows saved floor exits**

**Layout:** 10x35 repeatable rear access lane Stations alternate in one central bay; not all displayed at once.

**Activities:** Travel upward and downward

**Dependencies:** none

**Unlock challenge:** Basic ladder available; stair upgrade route exercise proposed

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** runtime stairs exist; transport tiers proposed

**Source:** docs/EXPANSION_DESIGN.md; HANDOFF_TO_CLAUDE.md

**Asset inventory:** plate + structural kit; ladder_segment, stair_segment; shared keeper poses and fault/reveal effects are itemized in CSV.

### stairs

- obj_stairs: PROPOSED, not coded: ladder travel 8 min per band both ways. Basic stairs. Simple manual carrier or landing. ON: 4-frame travel. Proposed location (5,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_stairs_t2: PROPOSED, not coded: spiral stair 5 min up and 6 min down. Mid-tier stairs. Improved motor/brake and clear floor indicator. ON: 4-frame travel. Proposed location (5,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_stairs_t3: PROPOSED, not coded: stair with handrail 4 min up and 5 min down. Top-tier stairs. Fast automatic carrier with route and safety indicator. ON: 4-frame travel. Proposed location (5,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Helter-skelter transport (`slide`)

**service_core · 14 × 35 logical pixels · aligned service core; follows saved floor exits**

**Layout:** 14x35 tube segment beside core; one exit each saved floor Stations alternate in one central bay; not all displayed at once.

**Activities:** Fast downward travel; clear jam

**Dependencies:** tower height; dynamic exits

**Unlock challenge:** Plot exit route; test flap; retrieve laundry

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: core clearance and exact wrapping; no final art

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; tube_segment, flap, face_window; shared keeper poses and fault/reveal effects are itemized in CSV.

### slide

- obj_slide: PROPOSED, not coded: down one band in 5 min. Basic slide. Simple manual carrier or landing. ON: 4-frame travel. Proposed location (7,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_slide_t2: PROPOSED, not coded: down one band in 3 min. Mid-tier slide. Improved motor/brake and clear floor indicator. ON: 4-frame travel. Proposed location (7,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_slide_t3: PROPOSED, not coded: down one band in 2 min; every floor still has exit. Top-tier slide. Fast automatic carrier with route and safety indicator. ON: 4-frame travel. Proposed location (7,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bedroom dive / two-door changing bay (`dive`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** Bedroom-local seam x117; hidden x118..130; exit x135; board beyond Stations alternate in one central bay; not all displayed at once.

**Activities:** Hidden change; board dive; sea splash

**Dependencies:** bedroom; safe sea; outfit

**Unlock challenge:** Test doors; demonstrate swimming; choose safe weather

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** locked attachment; playable hook absent; final length review

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; hidden_cubicle, board_support; shared keeper poses and fault/reveal effects are itemized in CSV.

### diveboard

- obj_diveboard: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic diveboard. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_diveboard_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier diveboard. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_diveboard_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier diveboard. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### diveinner

- obj_diveinner: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic diveinner. Basic: simple manual mechanism and few visible controls. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (27,0), logical frame 13x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 1@8fps; broken 1 + shared FX.

### diveouter

- obj_diveouter: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic diveouter. Basic: simple manual mechanism and few visible controls. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (27,0), logical frame 13x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 1@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Kitchen BBQ balcony (`bbq`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 55x35 kitchen-attached bay; grill left; prep shelf right Stations alternate in one central bay; not all displayed at once.

**Activities:** Grill; picnic; feed visitor

**Dependencies:** kitchen; ingredients; safe weather

**Unlock challenge:** Find dry weather; safe ignition; cook varied meal

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved idea; strong wind/lightning blocks regardless tier

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; prep_shelf, visitor_stool; shared keeper poses and fault/reveal effects are itemized in CSV.

### bbq

- obj_bbq: PROPOSED, not coded: 1 recipe serving / 35 min. Basic bbq. Manual single burner/range. ON: 4-frame flame or service motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bbq_t2: PROPOSED, not coded: 2 servings / 30 min. Mid-tier bbq. Two clearly marked burner controls. ON: 4-frame flame or service motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bbq_t3: PROPOSED, not coded: 3 servings / 25 min. Top-tier bbq. Three marked cooking slots and recipe display. ON: 4-frame flame or service motion. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### awning

- obj_awning: PROPOSED, not coded: usable in calm dry weather. Basic awning. Plain exposed fixture. ON: 4-frame deployment. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_awning_t2: PROPOSED, not coded: also usable in light rain. Mid-tier awning. Light-rain cover. ON: 4-frame deployment. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_awning_t3: PROPOSED, not coded: also usable in moderate rain; never lightning/extreme wind. Top-tier awning. Stronger rain seal and status tab; no storm safety bypass. ON: 4-frame deployment. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Gym hot-tub cantilever (`hot_tub`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 55x35 gym-attached platform; tub centre; rail and access left Stations alternate in one central bay; not all displayed at once.

**Activities:** Soak; socialize; winter comfort

**Dependencies:** gym; boiler; pump

**Unlock challenge:** Test heat and pump; select safe temperature

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved idea; structure needs review

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; rail, water_surface; shared keeper poses and fault/reveal effects are itemized in CSV.

### hottub

- obj_hottub: PROPOSED, not coded: 10 fun and 10 energy per 20 min warm soak. Basic hottub. Pilot flame and one pressure band. ON: 4-frame pressure flame. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_hottub_t2: PROPOSED, not coded: 13 fun and 13 energy per 17 min. Mid-tier hottub. Larger exchanger and two pressure bands. ON: 4-frame pressure flame. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_hottub_t3: PROPOSED, not coded: 15 fun and 15 energy per 14 min. Top-tier hottub. Three service circuits and efficiency gauge. ON: 4-frame pressure flame. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### tubpump

- obj_tubpump: PROPOSED, not coded: clean 1 water bay / 20 min. Basic tubpump. Single manual pump and pipe. ON: 4-frame water flow. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tubpump_t2: PROPOSED, not coded: 2 bays / 17 min. Mid-tier tubpump. Two-way pump with visible valve. ON: 4-frame water flow. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tubpump_t3: PROPOSED, not coded: 3 bays / 14 min. Top-tier tubpump. Three-way pump with filtering gauge. ON: 4-frame water flow. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Exterior caged trampoline (`caged_trampoline`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 55x35 playroom bay; spring bed centre; tall safety cage

**Activities:** Timing; comic high bounce

**Dependencies:** playroom; safe weather

**Unlock challenge:** Test cage; land three timed bounces

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: maximum bounce and roof camera hook

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; safety_cage, spring_support; shared keeper poses and fault/reveal effects are itemized in CSV.

### trampoline

- obj_trampoline: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic trampoline. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_trampoline_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier trampoline. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_trampoline_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier trampoline. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Bowling alley telescopic bay (`bowling`)

**extension · 165 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 165x35 bay; release left; pins right

**Activities:** Aim; timing; scoring

**Dependencies:** long horizontal island expansion

**Unlock challenge:** Align lane; roll controlled bowl; count score

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: parent attachment and expansion clearance

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; bowling_ball, pins, lane_markings; shared keeper poses and fault/reveal effects are itemized in CSV.

### bowlinglane

- obj_bowlinglane: PROPOSED, not coded: 10 fun per successful round / 12 min. Basic bowlinglane. Manual game surface and basic score display. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bowlinglane_t2: PROPOSED, not coded: 13 fun / 10 min. Mid-tier bowlinglane. Timing/score assistance with visible control. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_bowlinglane_t3: PROPOSED, not coded: 15 fun / 8 min. Top-tier bowlinglane. Helpful practice/aiming display; skill still required. ON: 4-frame game motion. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### pinsetter

- obj_pinsetter: PROPOSED, not coded: reset 10 pins / 3 min. Basic pinsetter. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_pinsetter_t2: PROPOSED, not coded: 10 pins / 2 min. Mid-tier pinsetter. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_pinsetter_t3: PROPOSED, not coded: 10 pins / 1 min. Top-tier pinsetter. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Expanded kitchen bay (`kitchen_bay`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 55x35 kitchen bay; extra work surfaces and utility seam

**Activities:** Batch meals; visitor cooking

**Dependencies:** kitchen; cooking progression

**Unlock challenge:** Prepare multi-course meal; allocate burners

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed architecture; not replacement for fixed core

**Source:** docs/EXPANSION_DESIGN.md; HANDOFF_TO_CLAUDE.md

**Asset inventory:** plate + structural kit; worktop, serving_hatch; shared keeper poses and fault/reveal effects are itemized in CSV.

### cooker

- obj_cooker: Runtime: Make toast; 12 game min; hunger +22 (need caps apply); proposed specialist perk: 1 recipe serving / 35 min. Basic oven. Manual single burner/range. ON: 4-frame flame or service motion. Proposed location (13,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_cooker_t2: Runtime: Make toast; 10 game min; hunger +28 (need caps apply); proposed specialist perk: 2 servings / 30 min. Two-oven range. Two clearly marked burner controls. ON: 4-frame flame or service motion. Proposed location (13,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_cooker_t3: Runtime: Make toast; 8 game min; hunger +33 (need caps apply); proposed specialist perk: 3 servings / 25 min. Fancy professional kitchen. Three marked cooking slots and recipe display. ON: 4-frame flame or service motion. Proposed location (13,0), logical frame 18x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### fridge

- obj_fridge: PROPOSED, not coded: 4 item slots. Small under-counter fridge. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (32,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fridge_t2: PROPOSED, not coded: 8 item slots. Fridge-freezer. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (32,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fridge_t3: PROPOSED, not coded: 12 item slots. American-style fridge. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (32,0), logical frame 12x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Gaming extension (`gaming_bay`)

**extension · 55 × 35 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 55x35 parent bay; console left; seat right

**Activities:** Curated games; cooperative puzzles

**Dependencies:** computer or living parent

**Unlock challenge:** Solve cooperative puzzle and choose station

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: parent and distinction from lair/games hall

**Source:** docs/EXPANSION_DESIGN.md; HANDOFF_TO_CLAUDE.md

**Asset inventory:** plate + structural kit; game_seat, screen; shared keeper poses and fault/reveal effects are itemized in CSV.

### console

- obj_console: Runtime: Use the secret computer; 30 game min; fun +28, energy -4 (need caps apply); proposed specialist perk: 1 clue per 20 game min. Old computer. Manual book, board or simple computer. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_console_t2: Runtime: Use the secret computer; 26 game min; fun +35, energy -4 (need caps apply); proposed specialist perk: 2 clues per 17 game min. Gaming PC. Indexed storage or improved terminal. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_console_t3: Runtime: Use the secret computer; 21 game min; fun +42, energy -4 (need caps apply); proposed specialist perk: 3 clues per 14 game min. Supercomputer wall. Search interface or clue display; no live internet. ON: 4-frame page or display change. Proposed location (18,0), logical frame 28x22; stable usePoint(-8,0), effectOrigin(0,-22), bubbleOrigin(0,-30), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Lamp-room roof / parachute launch (`roof`)

**extension · 110 × 20 logical pixels · parent-attached bay; integer structural seam**

**Layout:** 110x20 roof; launch hatch; clear lamp beam

**Activities:** Late comic parachute descent

**Dependencies:** maximum tower; wind safety

**Unlock challenge:** Demonstrate safe landing; select calm forecast

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** possible late idea; maximum height and safety decision unresolved

**Source:** docs/EXPANSION_DESIGN.md; HANDOFF_TO_CLAUDE.md

**Asset inventory:** plate + structural kit; roof_hatch, landing_marker; shared keeper poses and fault/reveal effects are itemized in CSV.

### parachutepack

- obj_parachutepack: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic parachutepack. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Garden / raised beds (`garden`)

**island · 55 × 25 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 55x25 patch; three crop slots; fence edge

**Activities:** Grow; harvest; water; dig

**Dependencies:** mission unlock; seed supplies

**Unlock challenge:** Choose sunny site; match seeds; nurture and harvest mixed crop

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** mission design proposed; absent day one in final design

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; soil_tile, crop_stages, fence; shared keeper poses and fault/reveal effects are itemized in CSV.

### garden

- obj_garden: Runtime: Tend the garden; 30 game min; fun +12, energy -6, hygiene -10, tidiness +6 (need caps apply); proposed specialist perk: 3 crop yields / 2 completed game days. Veg patch. Ground patch and three crop slots. ON: 2. Proposed location (19,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_garden_t2: Runtime: Tend the garden; 26 game min; fun +15, energy -6, hygiene -10, tidiness +8 (need caps apply); proposed specialist perk: 6 crop yields / 2 days. Raised beds. Raised beds with irrigation line. ON: 2. Proposed location (19,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_garden_t3: Runtime: Tend the garden; 21 game min; fun +18, energy -6, hygiene -10, tidiness +9 (need caps apply); proposed specialist perk: 9 crop yields / 2 days. Greenhouse. Glass greenhouse and protected crop gauge. ON: 2. Proposed location (19,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### wateringcan

- obj_wateringcan: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic wateringcan. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (42,0), logical frame 8x12; stable usePoint(-8,0), effectOrigin(0,-12), bubbleOrigin(0,-20), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Food greenhouse (`greenhouse`)

**island · 66 × 35 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 66x35 glass house; beds left; irrigation right Stations alternate in one central bay; not all displayed at once.

**Activities:** Protected crops; water; repair glass

**Dependencies:** garden; irrigation

**Unlock challenge:** Balance water; grow varied crop; replace glass panel

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** proposed separate place or garden tier 3 same asset

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; glass_panels, crop_stages; shared keeper poses and fault/reveal effects are itemized in CSV.

### garden

- obj_garden: Runtime: Tend the garden; 30 game min; fun +12, energy -6, hygiene -10, tidiness +6 (need caps apply); proposed specialist perk: 3 crop yields / 2 completed game days. Veg patch. Ground patch and three crop slots. ON: 2. Proposed location (33,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_garden_t2: Runtime: Tend the garden; 26 game min; fun +15, energy -6, hygiene -10, tidiness +8 (need caps apply); proposed specialist perk: 6 crop yields / 2 days. Raised beds. Raised beds with irrigation line. ON: 2. Proposed location (33,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_garden_t3: Runtime: Tend the garden; 21 game min; fun +18, energy -6, hygiene -10, tidiness +9 (need caps apply); proposed specialist perk: 9 crop yields / 2 days. Greenhouse. Glass greenhouse and protected crop gauge. ON: 2. Proposed location (33,0), logical frame 30x18; stable usePoint(-8,0), effectOrigin(0,-18), bubbleOrigin(0,-26), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### irrigation

- obj_irrigation: PROPOSED, not coded: clean 1 water bay / 20 min. Basic irrigation. Single manual pump and pipe. ON: 4-frame water flow. Proposed location (33,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_irrigation_t2: PROPOSED, not coded: 2 bays / 17 min. Mid-tier irrigation. Two-way pump with visible valve. ON: 4-frame water flow. Proposed location (33,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_irrigation_t3: PROPOSED, not coded: 3 bays / 14 min. Top-tier irrigation. Three-way pump with filtering gauge. ON: 4-frame water flow. Proposed location (33,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Orchard (`orchard`)

**island · 88 × 40 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 88x40 terrace; trees in three zones; clear walkway

**Activities:** Fruit; pruning; harvest

**Dependencies:** island expansion; planting

**Unlock challenge:** Identify saplings; plan spacing; harvest seasonal fruit

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved expansion idea; season simulation review

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; tree_stages, fruit_crate; shared keeper poses and fault/reveal effects are itemized in CSV.

### fruittree

- obj_fruittree: PROPOSED, not coded: 3 crop yields / 2 completed game days. Basic fruittree. Ground patch and three crop slots. ON: 2. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fruittree_t2: PROPOSED, not coded: 6 crop yields / 2 days. Mid-tier fruittree. Raised beds with irrigation line. ON: 2. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fruittree_t3: PROPOSED, not coded: 9 crop yields / 2 days. Top-tier fruittree. Glass greenhouse and protected crop gauge. ON: 2. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Jetty / harbour (`jetty`)

**island · 55 × 15 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 55x15 dock; floor plane stable; water below Stations alternate in one central bay; not all displayed at once.

**Activities:** Fish; launch; load supplies

**Dependencies:** mission unlock; shoreline

**Unlock challenge:** Tie knots; select safe tide; catch and identify fish

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** owned repairable; fishing remains reachable

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; bollard, rope, buoy; shared keeper poses and fault/reveal effects are itemized in CSV.

### jetty

- obj_jetty: Runtime: Go fishing; 45 game min; fun +22, hunger +14, energy -6, hygiene -4 (need caps apply); proposed specialist perk: 22 fun and 14 hunger / 45 min. Rickety jetty. Weathered dock and rod support. ON: 4-frame line. Proposed location (27,0), logical frame 55x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_jetty_t2: Runtime: Go fishing; 38 game min; fun +28, hunger +18, energy -6, hygiene -4 (need caps apply); proposed specialist perk: 28 fun and 18 hunger / 38 min. Proper jetty. Reinforced dock and bait stand. ON: 4-frame line. Proposed location (27,0), logical frame 55x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_jetty_t3: Runtime: Go fishing; 31 game min; fun +33, hunger +21, energy -6, hygiene -4 (need caps apply); proposed specialist perk: 33 fun and 21 hunger / 32 min. Harbour with boat shed. Harbour dock with launch fittings. ON: 4-frame line. Proposed location (27,0), logical frame 55x15; stable usePoint(-8,0), effectOrigin(0,-15), bubbleOrigin(0,-23), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Boathouse / indoor dry dock (`boathouse`)

**island · 110 × 50 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 110x50 shore facility; water berth centre; repair bench left; fuel and doors right

**Activities:** Launch; fuel; clean; repair; load; berth upgrades

**Dependencies:** shoreline expansion; boat; weather

**Unlock challenge:** Open inlet; check hull; load supplies; safe practice trip

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved replacement for garage; capacity/fuel tuning proposal

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; indoor_water, buoy, seaweed, cargo; shared keeper poses and fault/reveal effects are itemized in CSV.

### boat

- obj_boat: PROPOSED, not coded: rowing: 30 min shop leg; 1 crate; no fuel. Rowing boat. Rowboat and oars. ON: 4-frame oars. Proposed location (55,0), logical frame 55x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boat_t2: PROPOSED, not coded: tug: 20 min shop leg; 2 crates; 4 legs per tank. Tug. Small tug with engine stack. ON: 4-frame oars. Proposed location (55,0), logical frame 55x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_boat_t3: PROPOSED, not coded: speedboat: 10 min shop leg; 3 crates; 6 legs per tank. Speedboat. Compact speedboat with engine hood; shared waterline. ON: 4-frame oars. Proposed location (55,0), logical frame 55x24; stable usePoint(-8,0), effectOrigin(0,-24), bubbleOrigin(0,-32), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### seadoors

- obj_seadoors: PROPOSED, not coded: one boat bay open/close in 8 min. Basic seadoors. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (87,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_seadoors_t2: PROPOSED, not coded: one bay in 6 min. Mid-tier seadoors. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (87,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_seadoors_t3: PROPOSED, not coded: one bay in 4 min. Top-tier seadoors. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (87,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### fuelpump

- obj_fuelpump: PROPOSED, not coded: 1 tank fill / 10 min. Basic fuelpump. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (98,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fuelpump_t2: PROPOSED, not coded: 1 tank / 8 min. Mid-tier fuelpump. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (98,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_fuelpump_t3: PROPOSED, not coded: 1 tank / 6 min. Top-tier fuelpump. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (98,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### marinebench

- obj_marinebench: PROPOSED, not coded: 25 game min per repair. Basic marinebench. Hand tools and pegboard. ON: 4-frame tool jig. Proposed location (16,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_marinebench_t2: PROPOSED, not coded: 20 game min per repair. Mid-tier marinebench. Powered repair jig. ON: 4-frame tool jig. Proposed location (16,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_marinebench_t3: PROPOSED, not coded: 15 game min per repair. Top-tier marinebench. Diagnostic display and efficient tool station; do not promise global fault reduction. ON: 4-frame tool jig. Proposed location (16,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### berth

- obj_berth: PROPOSED, not coded: one rowing-size berth; 1 repair station. Basic berth. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (55,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_berth_t2: PROPOSED, not coded: one tug-size berth; 2 repair stations. Mid-tier berth. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (55,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_berth_t3: PROPOSED, not coded: one speedboat-size berth; 3 repair stations. Top-tier berth. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (55,-25), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Off-island shop (`shop`)

**destination · 66 × 35 logical pixels · off-island; boat route**

**Layout:** 66x35 destination; shopfront left; landing right

**Activities:** Buy supplies; reserve orders; meet proprietor

**Dependencies:** boat; safe route

**Unlock challenge:** Early route puzzle and first shopping trip

**Breakdowns:** Proprietor-owned; never keeper repair queue. Weather may prevent travel.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** not keeper-owned; no broken or repair state

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; shop_counter, supplies, proprietor; shared keeper poses and fault/reveal effects are itemized in CSV.

### shop

- obj_shop: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic shop. Basic: simple manual mechanism and few visible controls. ON: open doorway/engaged entrance, explicitly delivered at every tier. Proposed location (20,0), logical frame 33x30; stable usePoint(-8,0), effectOrigin(0,-30), bubbleOrigin(0,-38), z40. New tier mechanics and names require review; existing names preserved. States: standard;on; standard 1; on 1.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Chicken coop (`coop`)

**island · 55 × 35 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 55x35 patch; coop left; run right Stations alternate in one central bay; not all displayed at once.

**Activities:** Feed; eggs; tidy; latch repair

**Dependencies:** mission unlock; food

**Unlock challenge:** Build latch; identify feed; care routine with distinct tasks

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved idea; no day-one coop

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; chicken_idle, chicken_peck, straw; shared keeper poses and fault/reveal effects are itemized in CSV.

### coop

- obj_coop: PROPOSED, not coded: 10 pet-care points / 12 min. Basic coop. Plain bowl or simple hand-fed coop. ON: 4-frame feeding. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_coop_t2: PROPOSED, not coded: 15 pet-care points / 10 min. Mid-tier coop. Sturdier vessel with visible larger feed measure. ON: 4-frame feeding. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_coop_t3: PROPOSED, not coded: 20 pet-care points / 8 min. Top-tier coop. Automatic feed dispenser and timed indicator. ON: 4-frame feeding. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### eggtray

- obj_eggtray: PROPOSED, not coded: 4 item slots. Basic eggtray. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_eggtray_t2: PROPOSED, not coded: 8 item slots. Mid-tier eggtray. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_eggtray_t3: PROPOSED, not coded: 12 item slots. Top-tier eggtray. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (27,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. This station replaces the central activity bay when selected; never draw all stations simultaneously. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Outdoor pool / lido (`lido`)

**island · 110 × 45 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 110x45 terrace; large water basin and tiled edge

**Activities:** Swim; float; picnic; gentle rescue

**Dependencies:** boiler; water pump; expanded terrace

**Unlock challenge:** Check water; rescue float; warm pool

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved spectacle idea; footprint proposal

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; water_surface, ladder, changing_cubicle; shared keeper poses and fault/reveal effects are itemized in CSV.

### poolpump

- obj_poolpump: PROPOSED, not coded: clean 1 water bay / 20 min. Basic poolpump. Single manual pump and pipe. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolpump_t2: PROPOSED, not coded: 2 bays / 17 min. Mid-tier poolpump. Two-way pump with visible valve. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolpump_t3: PROPOSED, not coded: 3 bays / 14 min. Top-tier poolpump. Three-way pump with filtering gauge. ON: 4-frame water flow. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### poolheater

- obj_poolheater: PROPOSED, not coded: heat pool for 30 min per charge. Basic poolheater. Pilot flame and one pressure band. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolheater_t2: PROPOSED, not coded: 60 min per charge. Mid-tier poolheater. Larger exchanger and two pressure bands. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_poolheater_t3: PROPOSED, not coded: 90 min per charge. Top-tier poolheater. Three service circuits and efficiency gauge. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Rescue station / helipad (`rescue`)

**island · 110 × 40 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 110x40 cliff terrace; pad centre; equipment left

**Activities:** Prepare equipment; signal; rescue dispatch

**Dependencies:** radio; weather; rescue gear

**Unlock challenge:** Relay location; choose gear; secure terrace

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: rescue vehicle and playable dispatch

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; helipad_marking, helicopter, firstaid_props; shared keeper poses and fault/reveal effects are itemized in CSV.

### rescuewinch

- obj_rescuewinch: PROPOSED, not coded: 1 cargo or task slot. Basic rescuewinch. Basic: simple manual mechanism and few visible controls. ON: 4-frame transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_rescuewinch_t2: PROPOSED, not coded: 2 cargo or task slots. Mid-tier rescuewinch. Mid: sturdier housing; second visible functional control and clear status indicator. ON: 4-frame transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_rescuewinch_t3: PROPOSED, not coded: 3 cargo or task slots. Top-tier rescuewinch. Top: automatic mechanism; readable capacity/output gauge; same anchor and frame bounds. ON: 4-frame transfer. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### rescuecabinet

- obj_rescuecabinet: PROPOSED, not coded: 4 item slots. Basic rescuecabinet. Small four-slot shelves or single chest. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_rescuecabinet_t2: PROPOSED, not coded: 8 item slots. Mid-tier rescuecabinet. Divided eight-slot cabinet with double doors. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_rescuecabinet_t3: PROPOSED, not coded: 12 item slots. Top-tier rescuecabinet. Twelve-slot cabinet with labelled bays; same footprint. ON: 4-frame opening. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Wind turbine (`wind`)

**island · 44 × 70 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 44x70 terrace; mast vertical; stable base

**Activities:** Generate; brake; clear mechanical fault

**Dependencies:** power routing; wind forecast

**Unlock challenge:** Secure foundation; match windy site; route circuit

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved expansion idea; power units proposed

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; foundation, wind_cable; shared keeper poses and fault/reveal effects are itemized in CSV.

### windturbine

- obj_windturbine: PROPOSED, not coded: 10 units per moderate-wind game day. Basic windturbine. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_windturbine_t2: PROPOSED, not coded: 20 units per moderate-wind day. Mid-tier windturbine. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_windturbine_t3: PROPOSED, not coded: 30 units per moderate-wind day. Top-tier windturbine. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Cliff funicular (`funicular`)

**island · 55 × 70 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 55x70 cliff route; two terminal stations

**Activities:** Ride; carry supplies; repair track

**Dependencies:** cliff track to jetty; power

**Unlock challenge:** Align track; test brake; deliver crate

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: island levels and route length

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; track, terminal, carriage; shared keeper poses and fault/reveal effects are itemized in CSV.

### funicular

- obj_funicular: PROPOSED, not coded: 8 game min per floor or route segment. Basic funicular. Simple manual carrier or landing. ON: 4-frame travel. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_funicular_t2: PROPOSED, not coded: 5 game min per segment. Mid-tier funicular. Improved motor/brake and clear floor indicator. ON: 4-frame travel. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_funicular_t3: PROPOSED, not coded: 3 game min per segment. Top-tier funicular. Fast automatic carrier with route and safety indicator. ON: 4-frame travel. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Geothermal heating plant (`geothermal`)

**underground · 110 × 50 logical pixels · concealed below terrain; revealed only on unlock**

**Layout:** 110x50 below new terrace; drill left; exchanger right

**Activities:** Heat; pressure control; steam repair

**Dependencies:** drill; heating pipe network

**Unlock challenge:** Find warm ground; control pressure; test hot tap

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved idea; below terrain not standard stack

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; rock_layers, steam_vent, pipe_set; shared keeper poses and fault/reveal effects are itemized in CSV.

### drill

- obj_drill: PROPOSED, not coded: 1 completed batch / 30 min. Basic drill. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drill_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier drill. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_drill_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier drill. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### heatexchanger

- obj_heatexchanger: PROPOSED, not coded: heat 1 connected service bay per charge. Basic heatexchanger. Pilot flame and one pressure band. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_heatexchanger_t2: PROPOSED, not coded: heat 2 service bays per charge. Mid-tier heatexchanger. Larger exchanger and two pressure bands. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_heatexchanger_t3: PROPOSED, not coded: heat 3 service bays per charge. Top-tier heatexchanger. Three service circuits and efficiency gauge. ON: 4-frame pressure flame. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Sea-life underwater tunnel (`sea_tunnel`)

**underground · 165 × 35 logical pixels · concealed below terrain; revealed only on unlock**

**Layout:** 165x35 below shoreline; glass passage with clear walking lane

**Activities:** Observe wildlife; identify habitats

**Dependencies:** shoreline expansion; seal integrity

**Unlock challenge:** Inspect seals; match species; trace safe exit

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: underwater stage and viewing mechanics

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; glass_segments, sea_creatures, exit_sign; shared keeper poses and fault/reveal effects are itemized in CSV.

### tunnelseals

- obj_tunnelseals: PROPOSED, not coded: usable in calm dry weather. Basic tunnelseals. Plain exposed fixture. ON: 4-frame deployment. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tunnelseals_t2: PROPOSED, not coded: also usable in light rain. Mid-tier tunnelseals. Light-rain cover. ON: 4-frame deployment. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_tunnelseals_t3: PROPOSED, not coded: also usable in moderate rain; never lightning/extreme wind. Top-tier tunnelseals. Stronger rain seal and status tab; no storm safety bypass. ON: 4-frame deployment. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Satellite dish / radio mast (`satellite`)

**island · 66 × 50 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 66x50 terrace; dish centre; support legs and service box

**Activities:** Relay; align; signal puzzles

**Dependencies:** signal network; expanded terrace

**Unlock challenge:** Decode direction; align dish; test message

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved expansion idea; no real internet

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; support_legs, cable; shared keeper poses and fault/reveal effects are itemized in CSV.

### dish

- obj_dish: PROPOSED, not coded: 1 signal decoded / 20 min. Basic dish. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_dish_t2: PROPOSED, not coded: 2 signals / 17 min. Mid-tier dish. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_dish_t3: PROPOSED, not coded: 3 signals / 14 min. Top-tier dish. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### mast

- obj_mast: PROPOSED, not coded: 1 signal decoded / 20 min. Basic mast. Small crackling speaker/aerial. ON: 4-frame signal lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_mast_t2: PROPOSED, not coded: 2 signals / 17 min. Mid-tier mast. Ship-to-shore console and tuned indicator. ON: 4-frame signal lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_mast_t3: PROPOSED, not coded: 3 signals / 14 min. Top-tier mast. Coastguard-style multi-signal console. ON: 4-frame signal lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Workshop testing yard (`testing_yard`)

**island · 110 × 35 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 110x35 terrace; marked test lane; tools left; barriers right

**Activities:** Test inventions; labour-saving machines

**Dependencies:** workshop; island expansion

**Unlock challenge:** Assemble safe mechanism; test fault; demonstrate useful output

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** approved expansion idea; invention scope review

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; safety_barrier, crate_targets; shared keeper poses and fault/reveal effects are itemized in CSV.

### testtrack

- obj_testtrack: PROPOSED, not coded: 1 completed batch / 30 min. Basic testtrack. Manual wheel, printer or assembly bench. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_testtrack_t2: PROPOSED, not coded: 2 batches / 26 min. Mid-tier testtrack. Two-batch fixture or feed tray. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_testtrack_t3: PROPOSED, not coded: 3 batches / 21 min. Top-tier testtrack. Three-batch automated fixture; same anchor. ON: 4-frame tool movement. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### butler

- obj_butler: PROPOSED, not coded: 40 tidiness / 25 min. Basic butler. Broom and bristles. ON: 4-frame tool motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_butler_t2: PROPOSED, not coded: 50 tidiness / 21 min. Mid-tier butler. Hoover body with hose. ON: 4-frame tool motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_butler_t3: PROPOSED, not coded: 60 tidiness / 18 min. Top-tier butler. Robot cleaner with wheels and automatic status light. ON: 4-frame tool motion. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Solar terraces / folding wall array (`solar`)

**island · 110 × 35 logical pixels · island/shore terrace; no tower stack position**

**Layout:** Basic 22x12 rail panel; mid 44x24 folding array; top 110x35 island field

**Activities:** Charge; prioritize lamp/boiler/lift; clear snow; repair glass

**Dependencies:** power cut; forecasts; battery; circuit puzzle

**Unlock challenge:** Find sunny site; repair circuit; route battery to lamp

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** review: tier 4 sun tracker considered optional, not silently removed

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; panel_mount, cable, snow_overlay; shared keeper poses and fault/reveal effects are itemized in CSV.

### solarpanel

- obj_solarpanel: PROPOSED, not coded: 10 stored or generated energy units per clear game day. Basic solarpanel. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_solarpanel_t2: PROPOSED, not coded: 20 energy units per clear day. Mid-tier solarpanel. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_solarpanel_t3: PROPOSED, not coded: 30 energy units per clear day. Top-tier solarpanel. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### battery

- obj_battery: PROPOSED, not coded: 20 energy units stored. Basic battery. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_battery_t2: PROPOSED, not coded: 40 units stored. Mid-tier battery. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_battery_t3: PROPOSED, not coded: 60 units stored. Top-tier battery. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (41,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

### powerrouter

- obj_powerrouter: PROPOSED, not coded: route power to 3 circuits. Basic powerrouter. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_powerrouter_t2: PROPOSED, not coded: 6 circuits. Mid-tier powerrouter. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_powerrouter_t3: PROPOSED, not coded: 9 circuits. Top-tier powerrouter. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (67,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Comic sun-tracking array (`solar_tracker`)

**island · 66 × 35 logical pixels · island/shore terrace; no tower stack position**

**Layout:** 66x35 solar terrace add-on; tracking mount on stable base

**Activities:** Track sun; reset mistaken bright-target tracking

**Dependencies:** solar; tracking decision

**Unlock challenge:** Compare sky targets; calibrate sensor

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed fourth tier; separate optional module pending approval

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; tracking_mount, brightness_targets; shared keeper poses and fault/reveal effects are itemized in CSV.

### suntracker

- obj_suntracker: PROPOSED, not coded: 30 energy units on clear day; manual alignment. Basic suntracker. Small manual panel/battery/motor with one status lamp. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_suntracker_t2: PROPOSED, not coded: 36 units; tracks every 2 game hours. Mid-tier suntracker. Larger working surface and second capacity band. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.
- obj_suntracker_t3: PROPOSED, not coded: 42 units; tracks hourly. Top-tier suntracker. Automatic controller and three output bands. ON: 4-frame status lights. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Castle theme (`castle_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; gate left; toy castle centre

**Activities:** Shield sequence; rescue toy

**Dependencies:** imagination room

**Unlock challenge:** Match heraldry then solve drawbridge sequence

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant; no stack slot

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; banners, castle_backdrop, shield_tiles; shared keeper poses and fault/reveal effects are itemized in CSV.

### drawbridge

- obj_drawbridge: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic drawbridge. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Space-station theme (`space_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; star panel and docking port

**Activities:** Orbit ordering; docking puzzle

**Dependencies:** imagination room

**Unlock challenge:** Place planets then dock toy capsule

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant; distinct from permanent zero-gravity room

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; space_backdrop, planet_tiles; shared keeper poses and fault/reveal effects are itemized in CSV.

### toyairlock

- obj_toyairlock: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic toyairlock. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Pirate-ship theme (`pirate_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; helm left; chart right

**Activities:** Chart clues; knot sequence

**Dependencies:** imagination room

**Unlock challenge:** Plot toy treasure route and tie knot

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; pirate_backdrop, treasure_props; shared keeper poses and fault/reveal effects are itemized in CSV.

### toyhelm

- obj_toyhelm: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic toyhelm. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Jungle theme (`jungle_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; tracks left; vines right

**Activities:** Animal clues; vine path

**Dependencies:** imagination room

**Unlock challenge:** Match tracks then cross short path

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; jungle_backdrop, animal_tracks; shared keeper poses and fault/reveal effects are itemized in CSV.

### vinegate

- obj_vinegate: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic vinegate. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Gentle haunted theme (`haunted_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; puppet box centre

**Activities:** Sound matching; hidden toy

**Dependencies:** imagination room

**Unlock challenge:** Identify silly sound then find puppet

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant; child-friendly

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; haunted_backdrop, comic_ghost; shared keeper poses and fault/reveal effects are itemized in CSV.

### puppetbox

- obj_puppetbox: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic puppetbox. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Arctic-base theme (`arctic_theme`)

**theme · 105 × 35 logical pixels · inside imagination room; interchangeable set**

**Layout:** Same 105x35 set; pretend generator left; ice right

**Activities:** Warmth routing; ice rescue

**Dependencies:** imagination room

**Unlock challenge:** Route pretend heat and rescue toy penguin

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** discussed variant

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; arctic_backdrop, penguin_toy; shared keeper poses and fault/reveal effects are itemized in CSV.

### toyheater

- obj_toyheater: PROPOSED, not coded: one usable interaction; no mechanical reason for tiers. Basic toyheater. Basic: simple manual mechanism and few visible controls. ON: 4-frame use if applicable. Proposed location (15,0), logical frame 22x20; stable usePoint(-8,0), effectOrigin(0,-20), bubbleOrigin(0,-28), z40. New tier mechanics and names require review; existing names preserved. Theme prop remains single-tier; unlock variety instead of cosmetic upgrades. States: standard;on;broken; standard 1; on 4@8fps; broken 1 + shared FX.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

## Garage (superseded) (`garage`)

**retired · 0 × 0 logical pixels · no placement; superseded**

**Layout:** No allocated geometry

**Activities:** Historical idea replaced by water-filled boathouse

**Dependencies:** none

**Unlock challenge:** No unlock; do not implement

**Breakdowns:** Owned interactive machinery: local failure blocks that item, shared 1-pixel casing wobble + smoke + occasional sparks; repair loop 25 game min currently. Essential care always has an alternative. Inventory and savings survive faults.

**Bathroom access:** Shared nearest-fixture rule; boiler failure permits cold washing and leaves toilets usable.

**Decision/status:** retired: boathouse replaces garage

**Source:** docs/EXPANSION_DESIGN.md

**Asset inventory:** plate + structural kit; ; shared keeper poses and fault/reveal effects are itemized in CSV.

**Frank’s changes / additions:**

- [ ] Reviewed
- Notes:

