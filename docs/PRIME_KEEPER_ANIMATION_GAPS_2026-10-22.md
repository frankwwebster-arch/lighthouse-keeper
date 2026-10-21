# Prime Keeper: animation work still required

Date: 22 October 2026
Machine-readable inventory: `data/keeper_prime_animation_gaps.json`

## Short answer

The movement foundation is no longer waiting outside the game. There are 27
versioned Prime runtime sprites (217 registered frames). The game actively uses
the side idle, walk start/cycle/stop, stair ascent/descent and generic rear-work
loop.

The next work is not one undifferentiated art list:

1. **Finish consuming installed assets:** turns, four-way sit/stand, ladder and
   darts need gameplay state-machine choreography, anchors and endpoint tests.
   This requires no new Keeper drawing.
2. **Close the visible circulation gaps:** lift entry/ride/exit and the front
   door entry/exit/greeting route need Prime art and runtime integration.
3. **Build the core daily-life actions:** food, sleep, bathroom, seated leisure,
   cleaning, diary, lamp, telescope, phone and visitors.
4. **Then expand:** outside life, pets, mission rooms, expressive reactions and,
   last, costume variants.

## Priority list

| Priority | Batch | What is required |
| --- | --- | --- |
| P0 | Installed choreography | Front/side/back turn controller; sit → activity → stand controller in four directions; ladder route; darts route. |
| P0 | Circulation connectors | Lift enter/ride/exit; front-door approach/open/hidden handoff/enter/leave; visitor greeting. |
| P1 | Food and kitchen | Fridge snack and eat; cook; toast; carry/serve/eat endpoints. |
| P1 | Rest and indoor leisure | TV, armchair snooze, reading, piano, bed entry/sleep/exit. Reuse the installed sit/stand foundation. |
| P1 | Bathroom | Basin wash, teeth, private loo entry/exit and discreet loo performances. |
| P1 | Household and lamp | Diary, production-approved broom/hoovers, light/polish lamp, telescope. |
| P1 | Phone and visitors | Call/answer/order pizza, chat, cards and TV together. |
| P2 | Outside and pets | Fishing, gardening/harvest, shop, feed/play with pet. |
| P2 | Unlocked rooms | Aquarium watch/feed, weather, radio, secret computer and gadgets. |
| P2 | Reactions | Prime wave, bow, dance, sway, shake, wobble, jump, think, flop, spin and shrug. |
| P3 | Variants | Bathrobe, pyjamas, sou'wester, party, swimming/scuba, instruments, sports, seasonal and mood idles. |

## Coverage rule

The machine-readable inventory classifies all 38 interactions currently in
`src/game/config.ts` exactly once. `src/game/primeAnimationCoverage.test.ts`
fails if a gameplay interaction is added or removed without updating this
list. The 44 typed conversational reactions share eleven motion families, so
the reaction batch is counted by motion family rather than by line of dialogue.

## Recommended next batch

Do **P0 Installed choreography** first. It unlocks turns and sitting across
many later actions without commissioning more artwork. Then build **P0
Circulation connectors** so movement through the current lighthouse no longer
falls back at the lift or front door. After that, the strongest first art batch
is **P1 Food + bathroom + bed**, because those are the keeper's ungated daily
needs and appear most often in ordinary play.

The held-implement feasibility POC is not an exception. It proved the motion
model, but its proxy body art remains excluded. Sweeping and hoovering therefore
still require production-approved Prime held-tool bodies.
