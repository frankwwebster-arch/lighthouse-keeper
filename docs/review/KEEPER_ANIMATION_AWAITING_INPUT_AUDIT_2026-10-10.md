# Keeper animation awaiting-input corrective audit — 2026-10-10

## Scope and authority

- All 70 animations in `Awaiting new draft review` were checked against
  Frank's immutable 161-review export, not only the 28 cards whose full-redraft
  flag was set.
- The source export remains byte-identical to the supplied
  `keeper-scale-choices (2).json`, SHA-256
  `c19129f8419df2c046f3abb06de9f339f1cd8edb31c2d505dea8e79562d5f486`.
- Frank's saved width and height are production art direction. They are baked
  even for accepted costume clips and full-redraft clips; the former protected
  scale list has been removed. Canonical references still govern identity,
  beard silhouette, anatomy and contact semantics, but do not overrule Frank's
  visual sizing.
- Every awaiting-input card now has a specific read-only Codex response. It
  names the visible, frame, timing, prop or size change actually delivered.
  Generic `Implemented as requested` responses are not used.

## False-completion corrections

- `keeper_bath_enter` and `keeper_bath_exit` were fully re-rendered. The earlier
  response was wrong: the first pass had not materially corrected the eyebrows
  and beard. The replacement eight-pose sources now show the standard eyebrows
  and stepped/ragged side beard, with Frank's 115.5% × 88.5% and 114% × 88%
  sizes respectively.
- `keeper_carry_shopping` was replaced after the previous source was found to
  retain the hand fault. Each of the eight production poses now has exactly two
  arms and two hands, one hand carrying each bag.
- Halloween sizing is no longer overruled: rear is 102% × 89.5%, front is 95%
  × 91.5%, and side is 101% × 88% with its saved horizontal alignment.
- The same saved-size rule now applies to every reviewed clip, including bath,
  pyjamas, Tarzan, press-ups, parachuting and sitting references. Each reviewed
  JSON sidecar records `reviewScale`; verification checks it against all 161
  imported reviews.

## Re-render and extraction pass

New or replacement sources were produced for the bath entry/exit, shopping,
snow clearing, rear crouch family, fishing, hot-drink pour, rear table lean,
vegetable picking, cake placement, platform dive, pyjamas, snooker, sou'wester,
front spaceman, stairs descent, front/rear Tarzan, trampoline and all three
watering views. Final production strips were then visually checked, rather
than treating a new source filename as proof of completion.

The audit also corrected deterministic extraction faults which had cut actors,
mixed neighbouring poses or left fragments in fishing, hot-drink, snooker,
scuba, sawing, record placement and meal placement. The fishing actions are
clean 16-frame sequences with a readable waiting/reeling interval before the
catch; the float and fish sit below foot level. The trampoline now has a true
80-logical-pixel vertical action canvas and a substantially higher jump arc.

## Explicit qualifications

- The speedboat steering wheel and outboard motor remain separate boat/world
  objects. Their keeper clips retain hand contact points so runtime assembly
  does not duplicate those objects.
- The saved -85° anti-gravity viewer rotation remains a comparison aid; four
  calm face-down holds were added without rotating the production coordinate
  system.
- `keeper_swim_costume_down` was not redrawn from the uncertain `head too big?`
  note. The response explains that top-down foreshortening contributes to the
  appearance and asks for an explicit smaller-head request if that was the
  intended instruction.

## Review workflow

The review page can filter `Needs my input`, `Happy`, `Awaiting new draft
review`, `Review later`, `Unreviewed`, or `Has Codex response`. Focused
Previous/Next navigation and the arrow keys remain within the selected filter
and wrap from its final result to its first, so the final card never drops the
reviewer into another category.

### Original-comment identity check

The review pipeline attaches saved state by the exact `keeper_*` animation
name, never by a card's current visible position. The filter retains the same
card objects and only changes which objects are visible; Previous/Next selects
from that filtered object list and then resolves the selected object back to
its stable full-list index.

The verifier parses the data embedded in the generated review page and compares
all 161 keyed records with Frank's immutable export. It requires unique source
names, the identical set of page names, byte-for-byte matching note text,
matching Happy/Review-later decisions, the expected status on the same named
asset, and the exact comment in the same named resolution-table row. The
2026-10-10 audit found zero missing names, extra names, comment/decision
mismatches or status mismatches.

The generated resolution register is
`KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-09.md`; per-card narratives are
stored separately in `keeper-animation-codex-responses-2026-10-09.json` so
Frank's original comments remain immutable.
