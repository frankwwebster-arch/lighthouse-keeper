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
rear-facing urination proxy, and seated eating with fork and knife. These source
Door opening (side and rear), ladder climbing, and distinct stair ascent/descent
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
  fixed invisible fingertip target; mirror to swap hand and reverse to withdraw.

Production mode is deterministic normalization rather than generative editing:
`author_keeper.py` segments each source pose, applies a shared scale and baseline,
hardens alpha, places it on the 32 × 40 density-4 canvas, and emits the manifest
sidecars and review GIFs.
