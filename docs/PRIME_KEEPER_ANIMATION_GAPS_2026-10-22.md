# Prime Keeper: animation work still required

Date: 22 October 2026
Machine-readable inventory: `data/keeper_prime_animation_gaps.json`

## Short answer

The movement foundation is no longer waiting outside the game. There are 27
versioned Prime runtime sprites (217 registered frames). The game actively uses
the side idle, walk start/cycle/stop, stair ascent/descent and generic rear-work
loop. Approved front/side/back turns now bridge rear work and seating; TV,
nature TV, armchair nap, reading and piano use side sit → hold → stand; diary
uses turn → back sit → hold → stand → turn.

The current versioned review batch is
`/prime-keeper-animation-drafts`. It contains 36 isolated, independently
redraftable frames across lift entry/exit, front-door passage, rear cooking,
rear tooth-brushing and a front wave. These are review-only drafts and have not
entered the runtime bank. Every standing endpoint that has a matching approved
Prime authority is replaced with that exact authority byte-for-byte.

The next work is not one undifferentiated art list:

1. **Finish consuming installed assets:** ladder and darts still need gameplay
   routes; front/left seats need matching interactions. Turn routing, side
   leisure seating and back diary seating are complete.
2. **Review and finish the circulation connectors:** lift entry/ride/exit and
   front-door passage now have V1 review drafts. Visitor greeting is deferred.
   Approved revisions still need prop registration and runtime integration.
3. **Build the core daily-life actions:** food, sleep, bathroom, seated leisure,
   cleaning, diary, lamp, telescope, phone and visitors.
4. **Then expand:** outside life, pets, mission rooms, expressive reactions and,
   last, costume variants.

## Priority list

| Priority | Batch | What is required |
| --- | --- | --- |
| P0 | Installed choreography | **Complete:** action turn controller, side leisure seating and back diary seating. **Remaining:** front/left consumer routes, ladder layout route and darts board ownership. |
| P0 | Circulation connectors | **Review draft:** lift enter/ride handoff/exit and front-door approach/open/pass-through. **Remaining:** feedback revisions, prop registration, runtime wiring; visitor greeting deferred. |
| P1 | Food and kitchen | **Review draft:** rear cooking. **Remaining:** fridge snack/eat, toast, carry/serve/eat endpoints. |
| P1 | Rest and indoor leisure | TV, armchair snooze, reading, piano, bed entry/sleep/exit. Reuse the installed sit/stand foundation. |
| P1 | Bathroom | **Review draft:** rear tooth-brushing. **Remaining:** basin wash, private loo entry/exit and discreet loo performances. |
| P1 | Household and lamp | Diary, production-approved broom/hoovers, light/polish lamp, telescope. |
| P1 | Phone and visitors | Call/answer/order pizza, chat, cards and TV together. |
| P2 | Outside and pets | Fishing, gardening/harvest, shop, feed/play with pet. |
| P2 | Unlocked rooms | Aquarium watch/feed, weather, radio, secret computer and gadgets. |
| P2 | Reactions | **Review draft:** Prime front wave. **Remaining:** bow, dance, sway, shake, wobble, jump, think, flop, spin and shrug. |
| P3 | Variants | Bathrobe, pyjamas, sou'wester, party, swimming/scuba, instruments, sports, seasonal and mood idles. |

## Coverage rule

The machine-readable inventory classifies all 38 interactions currently in
`src/game/config.ts` exactly once. `src/game/primeAnimationCoverage.test.ts`
fails if a gameplay interaction is added or removed without updating this
list. The 44 typed conversational reactions share eleven motion families, so
the reaction batch is counted by motion family rather than by line of dialogue.

## Recommended next batch

Review the five V1 draft sequences first. On approval, register their object
planes and promote only the accepted frames. Then complete the P0 ladder/darts
consumers and continue P1 in this order: fridge snack/eat, toast and serving;
bed entry/sleep/exit; basin and loo; production held tools; lamp/telescope; then
phone. Visitors and pets are explicitly deferred for this batch.

The isolation gate withheld four generated sources: snack, bed nap, broom and
the first wave. Their adjacent poses shared opaque pixels, so they were neither
cropped nor exported for review. Wave V2 was rerendered with true gaps and is
the six-frame wave now shown. The other three remain quarantined in their own
versioned directories for later per-frame rerendering.

The held-implement feasibility POC is not an exception. It proved the motion
model, but its proxy body art remains excluded. Sweeping and hoovering therefore
still require production-approved Prime held-tool bodies.
