# Keeper first production batch

`keeper-turnaround-source.png` is the untouched image-generation study used to
settle the keeper's identity: navy cap, blue work jumper, cream stripe and
beard, dark trousers and boots. It uses the approved CRT as its rendering
reference and the lighthouse master image as its world/palette reference.

`keeper-walk-generated-source.png` is the identity-preserving eight-pose walk
source derived directly from that turnaround. The authoring script detects the
eight transparent poses, applies one shared scale, aligns every boot to the
same baseline, hardens alpha and exports the exact runtime strip.

The same identity-locked process supplies further generated sources:
turning from camera to rear, a reusable rear-facing arm-work loop, side and
front sit-down transitions, seated piano/instrument playing, a discreet
rear-facing urination proxy, and seated eating with fork and knife. Door
opening (side and rear), ladder climbing, and distinct stair ascent/descent
sources extend the same movement kit. Side/rear switch-reaching sources add a
fixed fingertip target for reuse across buttons and controls. These source
sheets remain untouched beside the turnaround. The rejected earlier simplified
action strips are preserved in `replaced-simplified/`; the quieter first rear-
work loop is preserved in `replaced-motion-v1/` for provenance only.

`author_keeper.py` is the deterministic production source. It redraws the
keeper on the locked 32 x 40 logical canvas at density 4, with hard alpha and
integer coordinates. Run it with the bundled workspace Python:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/source/keeper-first-batch/author_keeper.py
npm run sprites
python3 scripts/build_floor_asset_catalogue.py
```

The batch supplies aligned front/back master parts and these production clips:
idle; a right-facing eight-frame walk; turn to rear; rear arm-work; cooking,
washing and brushing aliases of that arm-work; side and front sit-downs;
piano/instrument playing; a separate urination proxy; and seated eating.
Left walk, left sit and left-facing seated eating are exact horizontal mirrors.
Get-up replays the relevant sit strip in reverse. The manifest records those
mirror/reverse rules plus the seat and hand-use points so furniture can be
aligned without redrawing the keeper.

Side door use mirrors for a left-hand door and both door-opening clips reverse
for closing. Ladder descent reverses the climb sequence. Stairs deliberately
use separate up/down cycles because descending needs a more upright balance and
different leading-foot placement; both stair cycles mirror for left travel.
Switch use follows the same economy: one side pose mirrors left/right, while the
rear pose mirrors to swap hands. Both reverse from pressed position to idle.
Their fingertips now share the authoritative Y=17 datum. Parachute jump,
platform dive, gardening, animal feeding, shopping, boating and offset TV
watching extend the same production set. Airborne frames expand to 48 × 56 for the dive
or 48 × 84 for parachute deployment, but retain the keeper's scale.

The `docs/floor-asset-catalogue/keeper-*-preview.gif` files are enlarged
previews made from the exact production frames; they are not separate artwork.
Turn and sit previews ping-pong only to demonstrate their reversible contracts.

The generated study is reference material, not a runtime sprite. The authored
PNGs in `art/raw/keeper-first-batch/` are the review candidates.

## Generation provenance

The generated sheets were made with the built-in image generator in referenced-
image/edit mode, using the approved turnaround as the identity lock. Prompt set:

- `keeper-turn-back-generated-source.png` — exact same keeper, six evenly spaced
  frames from side/three-quarter to full rear, fixed feet and centre, transparent.
- `keeper-work-back-generated-source.png` — exact same rear-facing keeper, eight
  frames of broad rhythmic two-arm work at an imaginary waist-high surface.
- `keeper-sit-side-generated-source.png` — exact same right-facing keeper, six
  frames from standing to an invisible side-on chair, designed to mirror/reverse.
- `keeper-sit-front-generated-source.png` — exact same front-facing keeper, six
  frames sitting back onto an invisible sofa/toilet, designed to reverse.
- `keeper-piano-generated-source.png` — exact same rear three-quarter keeper,
  eight seated frames playing an invisible keyboard/instrument, transparent.
- `keeper-loo-stand-generated-source.png` — exact same fully clothed rear-facing
  keeper, six discreet restroom frames with both hands held low in front.
- `keeper-eat-seated-generated-source.png` — exact same side-seated keeper,
  eight frames moving a fork from table height to mouth while a knife stays low.
- `keeper-door-side-generated-source.png` — six side-view frames reaching,
  turning an invisible handle, pulling and stepping through; mirror/reverse safe.
- `keeper-door-back-generated-source.png` — six rear-view frames of the same
  invisible-handle opening action; mirror handle side and reverse to close.
- `keeper-ladder-generated-source.png` — eight rear-view hand-over-hand frames
  with alternating boots on invisible rungs; reverse for descent.
- `keeper-stairs-up-generated-source.png` — eight right-facing high-knee ascent
  frames for diagonal runtime translation; mirror for left-rising stairs.
- `keeper-stairs-down-generated-source.png` — eight right-facing careful descent
  frames with upright balance; mirror for left-descending stairs.
- `keeper-switch-side-generated-source.png` — six right-facing reach frames with
  one fixed invisible fingertip target; mirror left and reverse to withdraw.
- `keeper-switch-back-generated-source.png` — six rear reach frames with one
  fixed invisible fingertip target at the same height as the side press; mirror
  to swap hand and reverse to withdraw.
- `keeper-parachute-jump-generated-source.png` — nine right-facing frames from
  take-off through pack opening, pilot chute and round red-and-cream canopy
  deployment, ending in an upright hanging pose with taut suspension lines.
- `keeper-dive-costume-turnaround-source.png` — identity-locked front, side and
  rear reference in a full-length red-and-white striped bathing costume, bare
  headed and barefoot.
- `keeper-platform-dive-generated-source.png` — ten right-facing launch,
  streamline and rotation frames in that costume, ending near-vertical and
  head-first with straight outstretched arms; no platform, water or splash.
- `keeper-dig-generated-source.png` — eight right-facing spade poses covering
  drive, boot press, lever, lift and return, with soil kept separate.
- `keeper-feed-animals-generated-source.png` — eight right-facing poses that
  lower a scoop to one near-floor point; bowl and animal remain separate.
- `keeper-sow-seeds-generated-source.png` — eight right-facing pouch-and-scatter
  poses with the soil bed kept separate.
- `keeper-pick-vegetable-generated-source.png` — eight low harvest poses ending
  with one generic carrot; garden bed and plant remain separate.
- `keeper-pick-fruit-generated-source.png` — eight high harvest poses ending
  with one generic red fruit; branch/tree and basket remain separate.
- `keeper-carry-shopping-generated-source.png` — eight right-facing walk-cycle
  poses carrying two consistent grocery bags; mirror for left travel.
- `keeper-row-boat-generated-source.png` — eight seated two-oar rowing poses;
  hull, seat, rowlocks and water remain separate.
- `keeper-drive-speedboat-generated-source.png` — eight seated helm poses with
  hands held at one invisible wheel point; boat and dashboard remain separate.
- `keeper-operate-outboard-generated-source.png` — eight rear-three-quarter
  tiller-control poses; motor, boat, water and wake remain separate.
- `keeper-watch-tv-generated-source.png` — eight seated rear-three-quarter
  right-looking poses; mirror left, with chair and screen kept separate.
- `keeper-weld-generated-source.png` — eight right-facing torch poses with
  protective goggles and gloves; metal workpiece and bench remain separate.
- `keeper-saw-wood-generated-source.png` — eight right-facing push-pull hand-saw
  poses; timber and sawhorse remain separate and align to one contact point.
- `keeper-wave-generated-source.png` — eight front-facing greeting poses from
  neutral through a broad friendly wave and back.
- `keeper-yawn-generated-source.png` — eight sleepy front-three-quarter poses
  with hand-to-mouth yawn and full-body stretch.
- `keeper-pyjamas-walk-light-blue-generated-source.png` — eight right-facing
  walk poses in light powder-blue pyjamas, cream piping and slippers; mirror left.
- `keeper-pyjamas-turn-back-light-blue-generated-source.png` — six matching pyjama poses
  from front to rear; reverse to face camera.
- `keeper-get-into-bed-light-blue-generated-source.png` — eight isolated right-side bed
  entry poses; bed, mattress, pillow and blanket remain separate. The rejected
  overlapping ten-frame attempt is preserved under `replaced-bed-v1/`.
- `keeper-snore-light-blue-generated-source.png` — six matching horizontal breathing and
  snoring poses without bed or floating Z effects.
- `keeper-swim-costume-horizontal-generated-source.png` — eight right-facing
  breaststroke poses in the red-and-white costume; mirror left.
- `keeper-swim-costume-up-generated-source.png` and
  `keeper-swim-costume-down-generated-source.png` — eight rear/up and
  front/down directional swim poses respectively.
- `keeper-scuba-horizontal-generated-source.png`, `keeper-scuba-up-generated-source.png`
  and `keeper-scuba-down-generated-source.png` — the same directional coverage
  in the locked navy wetsuit, mask, regulator, yellow tank and fins.
- `keeper-party-idle-generated-source.png`, `keeper-party-walk-generated-source.png`
  and `keeper-party-turn-back-generated-source.png` — normal uniform with a
  blue dotted cardboard cone hat, covering idle, mirrored walk and turn.
- `keeper-souwester-walk-side-generated-source.png`,
  `keeper-souwester-walk-back-generated-source.png` and
  `keeper-souwester-walk-front-generated-source.png` — full mustard-yellow
  sou'wester hat, toggle-fastened oilskin coat and trousers with navy sea boots;
  eight-frame side, direct rear and direct front walks. Mirror side for left.
- `keeper-dance-generated-source.png` — eight front-facing poses with side
  steps, knee bends, raised arms and a playful heel lift in one smooth loop.
- `keeper-play-guitar-generated-source.png` — eight standing front-right poses
  with a consistent warm-brown acoustic guitar, chord changes and down/up strums.
- `keeper-play-drums-front-generated-source.png` and
  `keeper-play-drums-back-generated-source.png` — matching eight-frame seated
  strike loops with sticks; drum kit and stool remain separate object assets.
- `keeper-watch-movie-generated-source.png` — eight reclined rear-right poses
  with a striped popcorn tub and hand-to-mouth loop; seating and screen separate.
- `keeper-clear-snow-generated-source.png` — eight right-facing shovel poses in
  a padded dark teal duffle coat, cream scarf and gloves; mirror left, with snow
  banks and spray kept separate.
- `keeper-crouch-work-back-generated-source.png` — eight direct-rear crouched
  poses using the established alternating back-work arm rhythm at ground level.
- `keeper-cake-from-oven-back-generated-source.png` — eight direct-rear poses
  crouching to an unseen oven, withdrawing a cake on a dark tray and standing
  with it level; quilted oven mitts, tray and cake are part of the actor clip.
- `keeper-cake-turn-right-generated-source.png` — six connected poses turning
  from the retrieval end pose to right-facing carry; mirror for the left turn.

The 9 October interaction expansion adds 67 untouched generated source sheets.
Their filenames follow the action directly: fish feeding and aquarium care;
hammering, reading, writing and table inspection; telescope, records, painting,
pottery and box searching; meal service and money; games and exercise; bathing,
showering and hot-tub use; fishing, watering and egg collection; lift, bicycle,
spiral-stair and slide movement; and side/back/front walks for knight,
spaceman, pirate, Tarzan, Halloween and mechanic outfits plus mechanic repair.
The corresponding runtime names and mirror/application rules are indexed in
`docs/KEEPER_ANIMATIONS.md`. The aquarium brush and side-hammer sheets are the
clean regenerated versions; the rejected foamy brush and welding-contaminated
hammer studies were never copied into this source directory. The corrected box
search ends with both arms reaching forward on the far side of the torso; its
hands-behind-body predecessor is retained in `replaced-search-boxes-v1/` only.

The replaced navy pyjama source files remain in this directory as historical
inputs, but production uses only the `light-blue` files above. The built-in
image generator was run in referenced-image mode: recolour only the pyjama
fabric and slippers to powder blue while preserving pose, proportions, cream
piping and transparency; for the sou'wester, preserve the canonical keeper and
draw isolated full-body walks in the specified oilskins from side, rear and
front views with identical scale and baseline. The music and cinema prompts
preserve the same identity and uniform, request eight isolated transparent
poses, keep stationary furniture/instruments separate where appropriate, and
lock repeated props, seat points, strike points and screen sightlines across
the loop. The snow prompt adds only the thick winter outfit and held shovel,
leaving ground snow/effects separate; the crouched prompt preserves the rear
uniform and adapts the approved back-work rhythm to a fixed low contact point.
The cake prompt pair locks the same golden sponge, dark tray, cream mitts and
hand positions across a rear oven retrieval and a mirror-safe carrying turn;
oven casing, rack and door remain separate.

`keeper-carry-cake-generated-source.png` and
`keeper-carry-meal-generated-source.png` extend those serving sequences with
eight-frame right-facing walks. Both use the canonical gait and 48 × 40 tray
canvas, mirror for left travel, and keep the established cake or plated meal
level at the shared `(34,20)` carry point.

`keeper-place-cake-generated-source.png` matches the existing plated-meal
placement logic: lower to the fixed invisible tabletop, release, withdraw the
hands and finish upright. The cake design is locked across oven retrieval,
turn, walking and placement: two golden sponge layers, a visible red jam
filling, white top icing and one centred red cherry. Superseded plain-sponge
sources are retained under `replaced-cake-design-v1/`.

The plated-meal placement source was also corrected so the released plate and
food remain at the fixed table point while the keeper withdraws his hands and
straightens. Its disappearing-plate predecessor is retained under
`replaced-meal-place-v1/`.

The fitness trio was regenerated in referenced-image edit mode as a matched
old-school workout set: blue headband, white sleeveless vest, blue shorts,
white socks and blue-and-white trainers. Trampoline and rear weight-lifting
retain their approved motion. The press-up source was redrawn at canonical
head, hand and foot scale, with the horizontal body spanning the extended
64 × 40 frame instead of being reduced to a miniature figure. The superseded
uniform sheets are retained under `replaced-fitness-uniform-v1/`.

The front bicycle study was replaced with an actor-only stationary
exercise-bike loop in the same old-school workout kit. The keeper grips two
invisible fixed handlebar points and pedals around an invisible crank; all bike
hardware is a separate object aligned through manifest hand, seat and pedal
points. The superseded road-bike sheet is retained under
`replaced-bicycle-v1/`.

Production mode is deterministic normalization rather than generative editing:
`author_keeper.py` segments each source pose, applies a shared scale and baseline,
hardens alpha, places it on a density-4 contract canvas, and emits the manifest
sidecars and review GIFs. Most clips use 32 × 40; dive and parachute poses use
larger transparent contract canvases at the identical character scale. The
hand-saw strip uses a 40 × 40 extended side-tool canvas for its full stroke.
Bed entry and snoring use a 48 × 40 canvas for the horizontal body.
Press-ups use an extended horizontal canvas and enforce a minimum
52-logical-pixel visible head-to-toe length in every production frame on a
64 × 40 canvas. Horizontal costume and scuba swimming likewise use 64 × 48;
only vertical swimming retains the centred 48 × 48 canvas. Rear weightlifting
uses 48 × 56 so raised arms and the barbell add space rather than shrinking the
keeper.
Vertical swim clips use a centred 48 × 48 canvas; horizontal swim uses 64 × 48.
Party and sou'wester
headwear use a 32 × 48 canvas so headwear never shrinks the keeper. Guitar and
movie clips use 48 × 40 for their horizontal extent; raised drumsticks use
32 × 48 without shrinking the seated body. Snow clearing also uses 48 × 40 for
the full shovel stroke; cake retrieval and carrying use 48 × 40 for the tray.
The expanded clips add 40-pixel-wide fish-tank/tabletop actions, 48-pixel-wide
long-prop actions, centred 48 × 48 anti-gravity motion, and 32 × 48 costume
walks. Bath/shower prompts require towel coverage on entry/exit and an opaque
blue mosaic/foam band on every wash frame. All generation used the built-in
image generator in referenced-image mode; runtime creation is deterministic
normalization only.
