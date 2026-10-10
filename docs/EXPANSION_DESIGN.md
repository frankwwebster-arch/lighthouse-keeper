# Lighthouse Keeper — expansion, rooms and world ideas

Date: 8 October 2026  
Status: living product-design write-up. It records Frank's locked directions separately from the unbuilt idea backlog so future Claude/Codex sessions do not mistake current placeholder code for the final design.

## Product principles

- Unlock challenges should use varied accomplishments, observation and small puzzles. Repeating the same action many times is tedious and must not be the main progression mechanism.
- The lighthouse is magical. Plausibility should support jokes and readable gameplay, not constrain the tower to realistic engineering.
- Floors should add systems, choices or relationships with other rooms—not merely another isolated clickable object.
- Every upgrade must have a clear, measurable gameplay benefit. Cosmetic changes can communicate or celebrate an improvement, but an object stays single-tier when there is no worthwhile mechanical upgrade.
- Activities remain curated and child-friendly. The computer room does not use live email, news or generative AI.
- Ordinary floors use the common fixed-width production geometry and nearest-neighbour 4× rendering.

## Locked tower layout

- The lamp room is always topmost.
- The bedroom is always immediately below the lamp room.
- The kitchen/entrance remains the ground-floor anchor.
- Other standard floors have no canonical vertical order. When one unlocks, choose a random available position in the middle stack, then persist that order in the save. Do not reshuffle it every night.
- A new insertion may push existing middle floors up or down. Their size and internal layout never change.
- Concept-art taper is decorative only and never controls width, eligibility or order.
- Shell stripe colour is derived from absolute world Y after layout.
- The underground lair remains below ground. Exterior bays and island facilities do not consume standard stack positions.

The current fixed aquarium → weather → lair → lift mission chain, `FLOOR_LEVELS` ordering and Floor 3 diving reservation are interim implementation details. They must be refactored before further standard-floor progression is treated as finished.

## Bedroom, diving board and night ending

The bedroom moves upward as the lighthouse grows, remaining directly beneath the lamp room. Its exterior diving-board/changing-room extension moves with it. The diving board may therefore become extremely high: the keeper can dive the full height of the lighthouse into the sea. Height is a comic reward, not a restriction.

The costume change still happens out of sight between two doors. The Victorian red-and-white swimming costume can be reused for diving and the swimming-pool floor.

At bedtime:

1. The cutaway front closes like a doll's house.
2. The camera pulls back to the full lighthouse.
3. Every domestic window is dark except the bedroom window immediately beneath the lamp.
4. The keeper's face appears on his pillow, perhaps with a yawn, wave, pet or other small variation.
5. The bedroom light clicks off while the lighthouse lamp continues shining.
6. The night recap plays.

## New-floor reveal

Major floor unlocks are held until morning. During the closed-lighthouse night, muffled bumps, sawing and comic crashes may suggest that the tower is rearranging itself.

At dawn:

1. The closed tower rumbles and changes height.
2. Existing middle floors shift to make the saved random slot.
3. The front façade peels open in two dollhouse-like panels.
4. The new room appears with a warm outline, sparkles and two gentle shine pulses.
5. The keeper appears at the stairs and comments on it.
6. A short card introduces the room's objects and new capabilities.

Sample reusable lines:

- “Look! The {room} has appeared!”
- “Well, would you look at that—a {room}!”
- “That definitely wasn't there yesterday.”
- “I wondered what all that banging was!”
- “Another whole floor? This lighthouse has ideas of its own.”
- Grumpy: “Oh good. Another floor to clean.”
- Dreamy: “I think the lighthouse built it while we slept.”

Room-specific lines are encouraged. Only one major reveal should play each morning; extra completed unlocks can wait in a reveal queue.

Use hand-drawn pixel-safe frames or integer translations for the façade. Do not blur or smoothly rotate raster art.

## Furniture migration

When a specialist floor appears, related furniture may move there overnight. The activity remains available; it gains a more capable home.

- Piano → music room. Keeper: “Where's my piano gone?”
- Bookshelf → library.
- Computer/desk → computer room.
- Dining table → dining room.
- Art materials → artist's studio.
- Exercise equipment → gym.
- Games cabinet → games hall.

The vacated room receives useful open space or a smaller replacement rather than looking accidentally empty.

## Candidate floors and challenges

These are approved ideas, not a fixed unlock sequence. Future missions should expose several eligible choices.

### Workshop

Adds repair tools, spare parts and inventions; upgrades can reduce breakdown pressure without eliminating faults.

Challenge: repair different fault categories, identify suitable tools, then assemble and test a small mechanism in the correct order.

### Weather station

Adds forecasts, rain gauge, wind vane and storm warnings.

Challenge: record weather at different times, interpret a simple chart, then warn a ship correctly.

### Aquarium or marine laboratory

Adds sea-creature care, microscope work and habitat knowledge.

Challenge: find creatures through fishing/diving, match them to habitats, then balance a tank.

### Radio room

Adds ship-to-shore communication, signal codes and rescue calls.

Challenge: repair an aerial, decode a short message and relay the correct location.

### Map and chart room

Connects boats, telescope sightings and exploration.

Challenge: collect map fragments, orient them correctly and plot a safe route through rocks.

### Observatory

Adds stars, moon phases and night sightings.

Challenge: spot several constellations and use the North Star in a direction puzzle.

### Library

A cozy room for stories, research, lighthouse history and clues rather than school-like repetition.

Challenge: recover misplaced books, sort them by subject and use information from one to solve a practical problem.

### Music room

Receives the living-room piano and adds drums, accordion, gramophone and comic instruments.

Challenge: copy a short melody, identify sounds and perform a small concert for a visitor.

### Artist's studio

Adds painting, pottery and permanent pictures that can decorate the lighthouse.

Challenge: collect colours from the world, mix simple combinations and make a picture for a visitor.

### Computer room

Uses a fictional, curated computer system. Activities include writing to known characters, reading next-day replies, viewing a game-state newspaper, checking forecasts, researching repairs and playing simple games. There is no live internet, real email or generative AI.

Possible headlines include “MYSTERY FLOOR APPEARS OVERNIGHT” and “LOCAL CAT DENIES STEALING FISH”. Messages can invite visitors, reserve shop items or start missions.

### Storage or box room

Provides the attic fantasy without competing with the bedroom's top position.

Mini-game: briefly inspect a changing field of boxes and clutter, then search, open, move and stack items to find a requested object. Discoveries can supply mission parts, records, maps or jokes.

### Dining room

Supports proper meals, visitors, celebrations and table-setting challenges. The kitchen remains for cooking and quick meals.

### Bank or savings room

A small, reassuring lighthouse bank where the keeper can move credits out of his spending purse and into savings. Saved money earns a modest amount of interest after several completed in-game days, rewarding patience without making waiting more profitable than playing.

The room can include a brass counter, coin scales, deposit tubes, a chunky safe and a savings book that visibly fills with stamps. The account balance, next interest date and expected interest should always be shown plainly. Deposits and withdrawals are allowed without punishment; there are no loans, debt, overdrafts, gambling or real financial products.

Possible activities and challenges:

- Sort and count mixed coins, then check that a deposit receipt is correct.
- Save towards a chosen upgrade, boat part or special outing.
- Compare “spend now” with a small delayed reward.
- Repair a jammed deposit tube or safe mechanism without ever losing the saved balance.
- Unlock the room by keeping some allowance unspent across several days and completing a simple coin-counting puzzle.

Interest should be deliberately modest, capped and based on completed game days rather than the device clock. Grown-ups should be able to tune or disable it. Savings are persistent player data and must never be threatened by the breakdown system; only the room's machinery and animations may break.

### Cinema

A strong rainy-day floor with fictional films, visitor screenings, projector repairs and scene-order puzzles. Later it can replay stylised films of completed lighthouse adventures.

### Games hall

Combines snooker, table tennis, darts, table football and board games. Different game types prevent grind: aiming, timing, arithmetic scoring and memory.

### Playroom

Combines a ball-pit search game, soft-play obstacles and trampoline timing. A caged exterior trampoline may briefly bounce the keeper above the roofline.

### Imagination or themed room

A reusable floor that changes between castle, space station, pirate ship, jungle, haunted room and Arctic-base themes. Themes alter scenery and the mini-game rather than requiring a permanent floor for each one.

### Zero-gravity room

A full late-game floor with a sealed entrance, padded walls and objects drifting around the keeper. It may begin as part of a space-research mission but remains a permanent activity room rather than merely a visual theme.

Activities can include:

- Float through rings or collect drifting objects.
- Play slow-motion zero-gravity ball.
- Put planets or satellites into the correct orbit.
- Recover lunch, tools or the cat's toys from the ceiling.
- Complete comic astronaut training.

The movement can reuse some of the pool's broad swimming language, but needs its own normal-clothes or spacesuit silhouette. Keep pixel motion crisp: integer translations and hand-drawn orientations rather than arbitrary raster rotation.

The room depends on electrical power. A controlled shutdown gently restores gravity; a breakdown makes everything hang for a beat and then fall into padded nets with a comic crash. Storm power loss, solar batteries, the computer room and observatory can all feed its missions.

Unlock challenge: use the observatory, solve a simple orbit/sequence puzzle, reserve enough stored power, then pass a short floating-object training course.

### Conservatory and greenhouse

They serve different purposes and may both exist. The greenhouse is an exterior food-growing facility with crops, irrigation and breakable glass. The conservatory is an indoor leisure floor with decorative plants, tea, reading, visitors and an overgrowth problem if neglected.

### Family-friendly pub or lighthouse inn

A social room serving lemonade, ginger beer, cocoa and large meals. Activities include pub quizzes, darts, dominoes, music nights and visitor stories. Possible names: The Flashing Lantern, The Lamp & Haddock or The Wobbly Gull.

## Swimming-pool floor

The pool is intentionally absurd: roughly 90% of the room is water, with only a narrow tiled walkway, changing cubicle and ladder. The keeper's head and shoulders remain above the waterline; submerged movement is hidden or distorted, keeping animation economical.

Reuse the Victorian swimming costume. Initial clips:

- `swim_idle` — tread water.
- `swim_lengths` — reusable six/eight-frame stroke.
- `swim_splash` — playful loop.
- `swim_float` — mostly static drift.
- `swim_exit` — climb the ladder.
- `pool_rescue` — tow an object or visitor.

Activities include lengths, floating, inflatables, retrieving lost objects and gentle rescue practice. The pool depends on the boiler for heat and the pump for cleanliness. Wind may slosh the water; fish may occasionally peer through an inappropriate glass panel.

The pool includes a proper changing area with toilets, basins and showers. These fixtures count as normal nearby bathroom facilities even when the player is not swimming.

## Bathrooms and walking-distance rule

Do not make the keeper repeatedly climb most of the lighthouse for basic hygiene or bladder needs. Bathrooms are distributed amenities, not scarce progression rewards.

- Bedroom en suite remains the private bathroom.
- Pool changing room includes toilets, basins and showers.
- Gym/hot-tub area can include another shower/changing room.
- Pub/inn needs a guest toilet.
- Large future clusters can receive a small rear service bathroom or WC without consuming an entire standard floor.
- Aim to keep every ordinary floor within roughly three floor bands of a usable toilet and wash point after random placement.
- Commands such as “use the loo” or “wash” should route to the nearest available suitable fixture rather than a single hard-coded object.

Extra fixtures are keeper-owned and may have local plumbing faults, but the fault system should avoid disabling every toilet or wash point simultaneously. Boiler failure affects hot water globally; it does not stop toilets working.

## Boiler room and service dependencies

The boiler supplies hot showers/baths, basin water, pool heat, radiators and possible future laundry/kitchen systems. Its position in the tower does not affect service.

When broken, water activities remain possible but are degraded rather than wholly disabled:

| Activity | Boiler working | Boiler broken |
|---|---|---|
| Shower/bath | Strong hygiene and comfort | Small hygiene gain, fun/energy penalty, shivering reaction |
| Basin wash | Normal hygiene | Reduced hygiene and annoyance |
| Swimming/hot tub | Comfortable | Short cold use or refusal unless necessary |
| Cold-weather sleep | Normal restoration | Reduced restoration until heating returns |

The boiler uses standard/on/broken art: pilot light; active flame/pressure; then shared wobble/smoke/sparks plus a pipe or gauge cue. Repair can ask the player to inspect pressure, choose a reset/pipe/fuse action and test a hot tap. Wrong choices create jokes, not permanent damage.

## Transport through a growing tower

Agreed 9 Oct 2026: transport runs in one continuous stairway separate from the rooms, entered through a door on every room. See `docs/DOORS_STAIRS_AND_COSTUMES.md`.

Progression can be:

1. Ladders — slow both ways.
2. Spiral staircase — better upward movement.
3. Helter-skelter slide wrapped around the stair core — fast, fun downward travel with an exit at every floor.
4. Lift — fast movement both ways once the tower becomes tall.

The slide reads the saved dynamic floor order. Animation can hide the keeper in an opaque tube, show a moving bump and flash his face past small windows. It is keeper-owned and breakable: jammed flaps, blocked tube, wrong-floor exits and trapped laundry provide faults.

## External and island-scale expansions

These are rare spectacle upgrades. They can tear the island apart because they require horizontal, shoreline or underground space. Ordinary floors do not.

- Outdoor pool or lido: tiled basin rises as pipes burst and settle into fountains.
- Boathouse/indoor dry dock: shoreline opens into a protected inlet and water channel running inside the building.
- Greenhouse/orchard: roots push earth plates apart and new soil/grass fills the gap.
- Rescue station/helipad: cliff slides outward into a safe equipment terrace.
- Wind turbine: giant foundation erupts and the turbine unfolds.
- Funicular: split cliff reveals a track to the jetty.
- Geothermal plant: drill, cracks and steam supply heating.
- Sea-life tunnel: shoreline separates around a glass underwater passage.
- Satellite dish/radio mast: support legs force new island terraces outward.
- Workshop testing yard: island expands to test large inventions and labour-saving machines.
- Bowling alley: a long horizontal extension telescopes from the tower.

The expansion initially looks catastrophic, then magic completes it: rock rises, soil fills gaps, grass rolls over it and surprised animals continue as normal.

### Boathouse and indoor dry dock

The boathouse replaces the garage idea. It is a ground/shoreline facility with water coming through large sea doors into an indoor berth, allowing the keeper to start the boat and speed directly out towards the off-island shop.

It connects several existing decisions:

- The shop remains off-island and proprietor-owned, so it never enters the keeper's repair queue.
- The rowing boat → tug → speedboat tiers share one berth and waterline anchor.
- The keeper's boat, boathouse doors, fuel pump and repair equipment are owned assets and may break.
- Weather and sea conditions affect whether departure is sensible or safe.
- The workshop handles small components; the boathouse handles hull, engine and marine repairs.

Boathouse activities:

- Launch the boat and travel to the shop.
- Refuel or recharge it.
- Repair hull, engine, propeller and steering faults.
- Clean salt and seaweed from it.
- Load shopping, rescue equipment or expedition supplies.
- Upgrade the berth as the boat grows from rowing boat to tug to speedboat.

Fuel should create occasional planning rather than a chore before every trip. A visible gauge, sensible capacity and optional reserve can make refuelling meaningful after several journeys or a long mission. Grown-ups can tune costs if it becomes irritating.

The arrival is a major island-tearing spectacle: shoreline rock splits, seawater rushes into a new channel, the boathouse rises around it, doors open and a loose buoy bobs inside. The final terrain heals into a sheltered harbour rather than leaving a broken island.

Possible faults include jammed sea doors, empty fuel tank, blocked propeller, leaking hull and a broken pump. The boat can still be repaired safely inside even when weather prevents sailing.

### Gym hot-tub extension

A deliberately precarious cantilevered platform on the outside wall. The hot tub depends on boiler heat and its pump, is delightful in snow, uncomfortable in a heatwave and alarming from the full-tower view.

### Kitchen BBQ extension

A small exterior balcony/bay attached to the kitchen, with a BBQ, preparation shelf and room for the keeper and a visitor. It is especially appealing on sunny and hot days and supports outdoor meals without becoming a separate floor.

Activities include grilling food, preparing a picnic, feeding visitors and a short cooking-timing challenge. Weather changes its use:

- Sunny/hot: extra fun and social value.
- Light rain: usable with an awning upgrade, but the keeper is reluctant without one.
- Strong wind: unsafe to light.
- Heavy rain or thunderstorm: unavailable.
- Cold weather: possible, but the keeper questions the decision.

It is a keeper-owned breakable asset. Faults include a blocked burner, snapped grill handle or runaway smoke; fire-safety mistakes produce a brief comic flare-up rather than lasting damage.

Unlock challenge: check for a dry weather window, gather ingredients, demonstrate safe lighting and cook several different items for a small outdoor meal.

## Weather and gameplay

How each weather looks and sounds (shared weather keys, backdrop layers and ambience) is in `docs/AMBIENCE_AND_BACKDROP.md`.

Weather changes preferences, safety and room value rather than merely recolouring the scene.

| Weather | Effects |
|---|---|
| Sunny | Outdoor fun bonus; good fishing, gardening, swimming and solar generation |
| Light rain | Keeper prefers indoors; garden waters itself; oilskins enable comfortable outdoor work |
| Heavy rain | Casual outside actions discouraged; leaks/plumbing faults more likely |
| Wind | Better wind power, rougher fishing/boats, loose objects need securing |
| Fog | Telescope impaired; lamp and radio important; ship risk rises |
| Thunderstorm | Unsafe leisure outside; electrical fault pressure and rescue events rise |
| Frost/snow | Frozen pipes, icy paths and snow activities; boats may be unavailable |
| Heatwave | Faster energy/hygiene drain; pool attractive; garden needs water; solar strong |
| Calm | Excellent fishing, weak wind power and possible becalmed ships |

“I would rather stay inside” is a preference that equipment or persistence may overcome. “That is not safe” is a hard block during lightning, extreme wind or dangerous seas. Emergencies can override reluctance only when proper rescue gear exists.

Oilskins, warm clothing, rescue gear and improved boats expand safe conditions. The weather station should forecast tomorrow so the player can plan instead of only reacting.

## Solar panels and power

Solar panels are an exterior energy system, not an ordinary floor. Small panels can unfold from rails/walls like mechanical petals; larger arrays occupy newly formed island terraces.

Suggested tiers:

1. Small balcony panel — powers a few lights.
2. Folding lighthouse array — assists boiler, computer and lift.
3. Island solar field — charges batteries for most systems.
4. Comic sun-tracking array — occasionally follows the wrong bright object.

Sun charges batteries; cloud reduces output; storms can crack glass or cables; snow requires clearing; heat can overheat tracking equipment. Stored energy supports the lamp and selected systems overnight. During shortages, the player chooses priorities such as lamp, boiler, lift, pool, computer or cinema.

Unlock challenge: experience a power cut, inspect a forecast, identify the sunniest site, repair an electrical object and complete a circuit-routing puzzle.

## Prioritisation guidance

Do not implement all ideas as independent floors at once. Prefer connected systems:

- Weather station + radio + solar + boiler create planning and infrastructure.
- Workshop + boathouse + breakdowns create repair, invention and boat-maintenance progression.
- Library + computer + map room create research and discovery.
- Music + art + cinema create creative rainy-day progression.
- Pool + gym/hot tub + diving board reuse the swimming costume and water animation.
- Dining room + food store + kitchen + visitors create preparation and social play.
- Boathouse + off-island shop + weather + radio create a complete travel and supply loop.
- Bank + allowance + shop + upgrades create a gentle saving and long-term-planning loop.

Before implementation, choose a small set of eligible missions and make their order genuinely non-linear. Every new mission should add varied goals and avoid raw repetition counts where a short bespoke challenge would be more enjoyable.

## Wants, thought bubbles and feelings (proposed 10 Oct 2026, not built)

Frank's idea, to be designed properly before it is built.

- **Thought bubbles.** When the keeper wants to do something, a bubble above his head shows it: a small picture of the object (the piano, the kettle) or a generic symbol (a musical note, a fish). Each recipe would name its icon, so every activity can show itself as a want with no extra wiring.
- **Feedback while he does something.** In The Sims, pink hearts rose from a character doing something they liked and minus signs from something they didn't. Our camera is further out, so floating symbols may be too small to read on the iPad. They might work only when the camera is zoomed in on an activity.
- **A "Numskulls" panel.** A sidebar showing what he wants to do inside a funny outline of his brain (or a little control room in his head), next to a gently animated face that shows his mood, from happy to cross. The game already tracks his needs, mood, likes and dislikes, so the panel would read those.
- **Questions to settle:**
  - Does a want come only from needs (hungry → food), or also from his personality (likes the piano)?
  - How many wants show at once?
  - Can tapping a want in the panel order it?
  - Do the symbols and the face need their own art batch from Codex?
