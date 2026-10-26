# Prime Keeper: installed-bank gaps (paused migration evidence)

> **Paused 26 October 2026:** The gaps below describe the installed Prime bank
> and its historical review queue. They do not authorise new art. Do not resume
> a corrective or missing-animation run until Frank-approved canon references
> populate `/public/art/keeper/canon/` and a reviewed migration decides which
> Prime choreography still applies. Ordinary stair/ladder animation is not
> needed for the hidden inter-floor route.

Updated: 23 October 2026
Machine-readable inventory: `data/keeper_prime_animation_gaps.json`

## Short answer

The movement foundation is no longer waiting outside the game. There are 27
versioned Prime runtime sprites (217 registered frames). The game actively uses
the side idle, walk start/cycle/stop, stair ascent/descent and generic rear-work
loop. Approved front/side/back turns now bridge rear work and seating; TV,
nature TV, armchair nap, reading and piano use side sit → hold → stand; diary
uses turn → back sit → hold → stand → turn.

Historically, Stair Ascent had one open corrective review: V18 normalises the lower beard
across its four unique drawings after a visible contact/passing jump was found.
It preserves the complete approved V16 choreography and changes only two
recorded contact-beard masks. V16 and the current runtime remain immutable
until this correction is explicitly approved.

The last versioned Prime review batch is
`/prime-keeper-animation-drafts-v12` (also served at
`/prime-keeper-animation-drafts`). It contains ten independently redraftable
sequences and 162 frame occurrences. V11 preserves V3's lift omission, brighter
passive front/back jumpers and accurate seated-route title. Frank rejected the
V4 rear-task amendment because detached black fragments returned and its
moving hem was cut across a second fixed hem, then rejected V5 because its hard
waist cut made the result worse, then rejected V6 because the generated lower
jumper still contained two ribbed bands in every affected frame. V7 removed
the duplicate but was rejected because its row-180 join made both side outlines
step inward. V8 corrected the outline but exposed a fixed dark trouser edge
directly beneath the moving hem, recreating a second seam. V9's occlusion was
also rejected because a separate dark waistband line remained visible. V10
removes that incompatible torso/lower-body join: rear-task positions 11–31
begin with the complete approved rear Prime and replace only the V6 action-arm
pixels. The cap, head, beard, torso, stripe, jumper band, trousers, boots,
height and floor registration remain exact authority pixels. V10 was then
rejected because its fixed row-125 arm-transfer boundary visibly cropped the
tops of sleeves and raised hands, while its alignment ghost was mistakenly on
by default. V11 restores complete arm silhouettes using the neutral rear pose
as an exclusion mask, protects every approved head pixel and turns the optional
ghost off by default. V11 was then rejected because the transferred arm layers
retained inner sleeve and jumper edges that broke the torso and cream stripe.
V12 replaces only rear-task positions 11–31 with complete `Cook at counter`
frames 2–8, byte-for-byte, repeated as three work cycles. Because every work
pose is now one intact drawing, there is no arm/torso layer join to break the
jumper. Frank approved all ten V12 animations on 23 October 2026; the external
decision is
`docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json`.
They have not yet replaced or extended the installed runtime sprites. V1–V11
remain immutable, and any later frame amendment must be a new V13 successor.

The next work is not one undifferentiated art list:

1. **Finish consuming installed assets:** ladder and darts still need gameplay
   routes; left seating needs a matching interaction. Turn routing, side
   leisure seating and back diary seating are complete in-game; a complete
   front-seat route is now available for choreography review.
2. **Integrate the approved circulation connectors:** lift entry/ride/exit and
   front-door passage are approved in V12. Visitor greeting is deferred. The
   approved revisions still need prop registration and runtime integration.
3. **Build the core daily-life actions:** food, sleep, bathroom, seated leisure,
   cleaning, diary, lamp, telescope and solo phone use. Visitors are deferred.
4. **Then expand:** outside life excluding pets, mission rooms, expressive
   reactions and, last, costume variants. Pets are deferred.

## Priority list

| Priority | Batch | What is required |
| --- | --- | --- |
| P0 | Installed choreography | **Complete in-game:** action turn controller, side leisure seating and back diary seating. **Approved V12:** front seat route. **Remaining:** runtime binding, left-seat consumer, ladder layout route and darts board ownership. |
| P0 | Circulation connectors | **Approved V12:** lift enter/ride handoff/exit and front-door approach/open/pass-through. **Remaining:** prop registration and runtime wiring; visitor greeting deferred. |
| P1 | Food and kitchen | **Approved V12:** rear cooking. **Remaining:** runtime binding, fridge snack/eat, toast, carry/serve/eat endpoints. |
| P1 | Rest and indoor leisure | **Approved V12:** side leisure sit/hold/stand and front seat route. **Remaining:** runtime deduplication/binding, activity-specific performance/props and bed entry/sleep/exit. |
| P1 | Bathroom | **Approved V12:** rear tooth-brushing. **Remaining:** runtime binding, basin wash, private loo entry/exit and discreet loo performances. |
| P1 | Household and lamp | **Approved V12:** diary turn/sit/hold/stand/return and isolated broom sweep. **Remaining:** runtime deduplication/binding, diary writing performance/prop, hoovers, light/polish lamp and telescope. |
| P1 | Phone and visitors | Call/answer/order pizza, chat, cards and TV together. |
| P2 | Outside and pets | Fishing, gardening/harvest, shop, feed/play with pet. |
| P2 | Unlocked rooms | Aquarium watch/feed, weather, radio, secret computer and gadgets. |
| P2 | Reactions | **Approved V12:** Prime front wave. **Remaining:** runtime binding, bow, dance, sway, shake, wobble, jump, think, flop, spin and shrug. |
| P3 | Variants | Bathrobe, pyjamas, sou'wester, party, swimming/scuba, instruments, sports, seasonal and mood idles. |

## Coverage rule

The machine-readable inventory classifies all 38 interactions currently in
`src/game/config.ts` exactly once. `src/game/primeAnimationCoverage.test.ts`
fails if a gameplay interaction is added or removed without updating this
list. The 44 typed conversational reactions share eleven motion families, so
the reaction batch is counted by motion family rather than by line of dialogue.

## Recommended next batch

Integrate the ten approved V12 sequences first, deduplicating installed turns,
seating and generic rear-work art rather than copying it. Register object planes
and promote only the hash-pinned accepted frames or choreography. Then complete
the P0 ladder/darts/left-seat consumers and continue P1 in this order:
fridge snack/eat, toast and serving; bed entry/sleep/exit; basin and loo;
production held tools; lamp/telescope; then phone. Visitors and pets remain
explicitly deferred. The full next-run handoff is
`docs/PRIME_KEEPER_NEXT_ANIMATION_RUN_HANDOFF_2026-10-23.md`.

The isolation gate withheld four generated sources: snack, bed nap, the
original broom sheet and the first wave. Their adjacent poses shared opaque
pixels, so they were neither cropped nor exported for review. Wave V2 was
rerendered with true gaps and is the six-frame wave now shown. The original
broom source remains quarantined, but Frank approved the separate genuinely
isolated Prime Sweep V2 sequence in V12. Snack and bed still need per-frame
rerendering.

The held-implement feasibility POC is not an exception. It proved the motion
model, but its proxy body art remains excluded. The V12 sweep sequence uses a
separately isolated exact-Prime source and is now approved; hoovering still
requires production-approved Prime held-tool bodies.
