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

Stair ascent has one open corrective review: V18 normalises the lower beard
across its four unique drawings after a visible contact/passing jump was found.
It preserves the complete approved V16 choreography and changes only two
recorded contact-beard masks. V16 and the current runtime remain immutable
until this correction is explicitly approved.

The current versioned review batch is
`/prime-keeper-animation-drafts-v11` (also served at
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
ghost off by default. These V11
corrections remain review-only and have not replaced the installed runtime
sprites. V1–V10 remain
immutable.

The next work is not one undifferentiated art list:

1. **Finish consuming installed assets:** ladder and darts still need gameplay
   routes; left seating needs a matching interaction. Turn routing, side
   leisure seating and back diary seating are complete in-game; a complete
   front-seat route is now available for choreography review.
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
| P0 | Installed choreography | **Complete in-game:** action turn controller, side leisure seating and back diary seating. **Review choreography:** front seat route. **Remaining:** left-seat consumer, ladder layout route and darts board ownership. |
| P0 | Circulation connectors | **Review draft:** lift enter/ride handoff/exit and front-door approach/open/pass-through. **Remaining:** feedback revisions, prop registration, runtime wiring; visitor greeting deferred. |
| P1 | Food and kitchen | **Review draft:** rear cooking. **Remaining:** fridge snack/eat, toast, carry/serve/eat endpoints. |
| P1 | Rest and indoor leisure | **Review choreography:** side leisure sit/hold/stand and front seat route, using byte-exact approved components. **Remaining:** activity-specific performance/props and bed entry/sleep/exit. |
| P1 | Bathroom | **Review draft:** rear tooth-brushing. **Remaining:** basin wash, private loo entry/exit and discreet loo performances. |
| P1 | Household and lamp | **Review choreography:** diary turn/sit/hold/stand/return and isolated broom sweep. **Remaining:** diary writing performance/prop, approval and runtime wiring, hoovers, light/polish lamp and telescope. |
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

Review the ten V9 sequences first. On approval, register object planes and
promote only accepted action frames or accepted composite choreography. Then
complete the P0 ladder/darts/left-seat consumers and continue P1 in this order:
fridge snack/eat, toast and serving; bed entry/sleep/exit; basin and loo;
production held tools; lamp/telescope; then phone. Visitors and pets are
explicitly deferred for this batch.

The isolation gate withheld four generated sources: snack, bed nap, the
original broom sheet and the first wave. Their adjacent poses shared opaque
pixels, so they were neither cropped nor exported for review. Wave V2 was
rerendered with true gaps and is the six-frame wave now shown. The original
broom source remains quarantined, but a separate genuinely isolated Prime Sweep
V2 candidate is now in the V2 review. Snack and bed still need per-frame
rerendering.

The held-implement feasibility POC is not an exception. It proved the motion
model, but its proxy body art remains excluded. The new sweep candidate uses a
separately isolated exact-Prime source and still requires choreography approval;
hoovering still requires production-approved Prime held-tool bodies.
