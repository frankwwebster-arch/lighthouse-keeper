# Kitchen Ligne-Claire Complete Review V46

Date: 22 October 2026

Status: immutable reversible review candidate; not approved, registered,
promoted, selected as current or wired to production/runtime.

Review route: `/keeper-review/kitchen-ligne-claire-complete-review-v46/index.html`

## Outcome

V46 is the complete movable V45 kitchen with only the rejected Dishwasher V1
candidate family replaced by geometry-locked Dishwasher V3. It contains 60
object/state records, 16 separately owned effect records and 16 contact/evidence
sheets. All other object, effect and room-composition bytes are inherited from
V45.

The full-room tool is the required place to judge whether the dishwasher reads
too squat and whether its worktop forms one continuous run. It includes exact
current/candidate ghosts, the invariant control-panel proof, the full-run
worktop ghost, native-size proof and movable room composition.

## Dishwasher correction

The replacement family:

- retains every V41 `98 × 82 px` canvas and alpha byte;
- restores the exact prior component positions and removes the erroneous black
  worktop strip;
- uses one control-panel geometry in Off, On and Broken, with the status lamp
  beside the selector rather than on the door front;
- copies the approved cabinet worktop cap for each matching edge condition;
- changes only the expressly authorised Broken handle angle, with its right
  side hanging more steeply.

V1 and V2 remain immutable rejected provenance. V3 and V46 create new versions
only.

## Behaviour and healing invariants

The V46 page inherits the complete V45/V41 workbench implementation. After
normalising only the immutable set name and ready message, its movement and
healing JavaScript is byte-identical to V45. Bay origins, room layout, anchors,
pivots, collision geometry, drag/snap/swap, Broken-state movement lock, repair
unlock, state transitions, animation timing, asset-local effect ownership and
countertop-healing rules are unchanged.

## Delivery resilience

All review media is content-addressed under `review-archive/objects`; the public
payload contains only the HTML shell. Every image URL is root-absolute through
the same-origin archive route, so Vercel's trailing-slash canonicalisation
cannot rebase it into the wrong directory. Every unique image preloads and
decodes before movement or playback controls are enabled.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v3
npm run verify:kitchen-ligne-claire-complete-review-v46
npm run maintain:keeper-review
npm test
npm run build
```

Browser verification must load the explicit `index.html`, inspect the complete
worktop run at native scale and by ghost, compare all three control panels,
move/swap exact bays, confirm Broken dishwasher movement rejection, repair to
Off or On, move again, and compare healing enabled against raw edges.

## Approval and rollback

The registration gate remains closed. Nothing has been made current and no
approved source, production asset or runtime selector is overwritten. Explicit
approval is still required.

Rollback is immediate: discard only the V46 draft, review shell, archive set,
new archive objects, builder and this record. V45, Dishwasher V3, every approved
authority and all production/runtime files remain byte-for-byte available.

## Documentation audit

README, STATUS, DECISIONS, package verification scripts, route allow-list,
V3/V46 manifests and these delivery records agree on the 60/16/16 inventory,
exact V41 dishwasher geometry, approved-cap continuity, byte-identical
movement/healing implementation, root-absolute delivery, closed registration
gate and immediate rollback boundary. Gameplay and production documentation do
not require changes because neither runtime nor production was modified.
