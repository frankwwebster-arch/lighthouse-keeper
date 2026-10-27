# Lighthouse Keeper — Upgrade Matrix (DRAFT for Frank, 27 Oct 2026)

Design authority for upgrades once Frank approves it. The live game still reads `data/upgrades.csv`; Claude Code updates that file (and runs `npm run upgrades`) only after approval, room by room as each room's objects exist in the engine.

**Principles (SPEC section 10b):** every interactive item has three tiers. Tier 2 = a better version (faster, more reliable / fewer faults, more satisfying, bigger capacity). **Tier 3 = a wacky British inventor's contraption built out of the original item** (Branestawm / Heath Robinson spirit, slight steampunk: visible gears and pulleys, brass, gauges, flashing bulbs, steam), with a brass maker's name plate, doing something delightful automatically and almost never breaking. Each tier fits its item's reserved slot. Prices follow the current pattern (t1 free, t2 ~15–30, t3 ~35–60 credits) and are placeholders.

Names in CAPITALS are the tier-3 name plates.

## Entrance lobby (ground floor)
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Front door | Old wooden door | Door with knocker and peephole | DOOR-O-MATIC: periscope, bell-pull and pulleys that swing it open for visitors | see visitors sooner; visitors wait longer |
| Washing machine | Twin-tub | Front-loader | LAUNDRY ENGINE: mangle rollers and a pulley line that carries washing out to the line | faster, bigger loads, hangs washing itself |
| Boot rack | Boot rack | Boot-drying rack | BOOT-BUFFING MACHINE: spinning brushes that clean and polish boots | no mud tracked in (less cleaning) |

## Kitchen (first floor) — agreed 27 Oct
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Cooker (double slot) | Old-school cooker with eye-level grill | Cottage range | BAKE-O-MATIC | cooks faster; two dishes at once; posh recipes |
| Fridge (double slot) | Tall fridge-freezer | American-style double-door | FROST ENGINE | holds more; food keeps longer; ice |
| Hot drinks | Brown Betty teapot | Coffee machine (teapot on its warmer) | GRAND ESPRESSO CONTRAPTION | more cheering; quicker |
| Radio | Crackly valve radio | Big wireless | WEATHER ENGINE (aerial mast, small satellite dish, ticker tape) | earlier and clearer storm warnings |
| Toaster | Two-slice toaster | Four-slice toaster | TOAST CATAPULT | faster breakfast; more filling |
| Mixer | Stand mixer | Food processor | BAKING CAROUSEL | baking unlocked / faster |
| Larder | Larder cupboard | Auto-restocking pantry | PANTRY LIFT | fewer shopping trips |
| Dishwasher (new purchase) | Dishwasher | Quiet, fast dishwasher | SELF-LOADER | no washing-up; never stacks up |
| Bin | Pedal bin | Recycling bins | COMPOST ENGINE (pipe 'TO GARDEN') | tidier; feeds the garden |
| Cleaning (behind right door) | Broom | Hoover | Super hoover | tidies faster |

## Living room with dining table (always directly above the kitchen)
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Dining table | Scrubbed pine table | Extending dining table | BANQUETING CAROUSEL: a turning centrepiece that serves each dish | meals more satisfying; visitors stay |
| TV (CRT family) | Old box telly | Big wooden-cabinet colour telly | TELEVISOR: valve-lit cabinet on brass gimbals with twin aerials | more fun per show; film nights |
| Bookshelf | Wobbly shelf | Proper bookcase | LIBRARY ENGINE: rolling ladder and a book-fetching arm | reading hints for quizzes |
| Armchair | Old armchair | Rocking chair | RECLINE-O-MATIC: lever footrest and a tea-holding arm | rest recovers more energy |
| Piano | Old upright piano | Polished upright piano | PIANOLA ENGINE: self-playing with punched paper rolls | visitors ask him to play |

## Bedroom and en-suite (always beneath the lamp room)
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Bed | Creaky single bed | Comfy double bed | SLEEP ENGINE four-poster: canopy, automatic curtains, bedside tea-maker | wakes with more energy |
| Telephone | Old dial phone | Push-button phone | TELEPHONIC EXCHANGE: little switchboard with plugs and lights | ring friends more often; friends arrive sooner |
| Desk | Little desk | Writing bureau | INVENTOR'S DESK: drafting arm, magnifier, sparking gizmos | links to workshop gadgets |
| Basin | Chipped basin | Pedestal basin | BRUSH-O-MATIC: a mirror on a swinging arm and a toothbrush rinser | quicker morning wash |
| Bath | Tin bath | Roll-top bath | BUBBLE ENGINE: bellows that froth the bath | washing cheers him up |
| Shower | Bucket shower | Power shower | RAINMAKER: a spinning brass rose and pipework | quicker, more refreshing |
| Toilet (never seen; sound only) | Clanky loo | Quiet-flush loo | Musical loo (he doesn't want to come out) | joke only |

## Lamp room
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Lamp | Oil lamp | Electric lamp | MEGA BEAM: clockwork-turned giant lens with gears | burns all night; never needs polishing |
| Telescope | Brass telescope | Spyglass on a stand | OBSERVATORY ENGINE: geared telescope with star charts | spotting game sees further and rarer things |

## Outside
| Item | Tier 1 | Tier 2 | Tier 3 contraption | Perk direction |
|---|---|---|---|---|
| Garden shed (outdoor tools) | Lean-to shed | Proper shed | INVENTOR'S SHED: chimney, whirligig and gadget hatch | better tools |
| Lawnmower | Push mower | Petrol mower | MOW-O-MATIC | mows faster |
| Vegetable garden | Veg patch | Raised beds | GREENHOUSE ENGINE: glasshouse with sprinklers | grows faster, even in storms |
| Jetty | Rickety jetty | Proper jetty | JETTY CRANE: winch and hoist for the boat | better fishing; boat trips start here |
| Boat | Rowing boat | Tug | AMPHIBIOUS CONTRAPTION (paddles, propeller, balloon) | quicker trips |

## Later rooms (when built)
| Item | Tier 1 | Tier 2 | Tier 3 contraption |
|---|---|---|---|
| Fish tank | Small fish tank | Big tank | REEF ENGINE (bubbling pipework, feeding chute) |
| Barometer | Barometer | Weather instruments | STORM-PREDICTING ENGINE |
| Workshop bench | Workbench | Gadget bench | ROBOT LAB |
| Computer | Old computer | Gaming computer | SUPERCOMPUTER WALL |

## Changes from Frank's original table
- Removed: 'pet cannot steal from it' (no pet in V1), 'Fancy professional kitchen', 'Lazyboy-style recliner', 'Big flat-screen TV' (breaks the CRT family), 'Grand piano' (too wide and deep for its slot), 'Smart door with doorbell camera', 'Video phone', 'Spa bathroom with rainfall shower', 'Harbour with boat shed' (clashes with the boathouse), 'Greenhouse' as a garden tier (now the tier-3 contraption, still to reconcile with any separate greenhouse facility).
- Pet bowl removed until a pet exists.
- Door moved to the lobby; bedroom basin split into basin, bath and shower to match the en-suite.
- New: hot drinks, radio, toaster, mixer, larder, dishwasher, bin (kitchen); washing machine and boot rack (lobby); dining table (living room); shed and lawnmower (outside).
