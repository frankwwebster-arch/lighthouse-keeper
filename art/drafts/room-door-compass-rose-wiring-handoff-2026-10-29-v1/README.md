# Ordinary room door — approved wiring handoff

Frank approved this compass-rose room door, its true scale, and the automatic crossing choreography on 29 October 2026. This directory is the cloud-accessible handoff for Claude Code.

The approval is for an **ordinary room door**. Decorative and stained-glass designs do not apply to kitchen cabinetry, the cupboard of myriads, or other cupboards. Those doors remain opaque monotone and match their surrounding cabinetry.

## Files

| File | Use |
|---|---|
| `assets/room-door-compass-rose-room-168x336.png` | Runtime room-view leaf, exactly 1 m × 2 m at 168 px/m |
| `assets/room-door-compass-rose-lighthouse-20x40.png` | Reviewed lighthouse-view mip |
| `assets/room-door-compass-rose-paint-source-337x674.png` | Painted high-resolution source; not the runtime-size asset |
| `review/room-door-compass-rose-correct-scale-v3.mp4` | Approved behaviour reference only; never use as runtime art |
| `door-runtime-contract.json` | Machine-readable geometry, state, collision and rendering contract |
| `CLAUDE_CODE_PROMPT.md` | Ready implementation brief |
| `manifest.json` | Immutable SHA-256 values |
| `verify_handoff.py` | Dependency-free integrity and PNG-dimension verifier |

The larger APNG review proof is deliberately not committed: it exceeded the repository's review-image limit. The small MP4 contains the same 128-frame proof.

## Non-negotiable geometry

- Room scale: 168 px/m.
- Door leaf: 168 × 336 px, exactly 1 m wide and 2 m tall.
- Prime Keeper: unchanged at 120 × 298 px with 298 px opaque height. Never resize him at room scale.
- Keeper-to-door height ratio: 298/336 = 0.8869047619; head clearance is 38 px.
- Open endpoint: exactly 90° from closed, with the full face parallel to the player/camera.
- The leaf opens toward stage front into the gutter, clear of the cabinet-depth plane.
- Left door: hinge on outer/left edge, handle on free/right edge. Mirror both for a right-hand **room-door** variant; never show hinges on both sides.

## Automatic crossing contract

1. The Keeper approaches and stops outside the swept volume.
2. The door opens automatically to 90° in about 0.72 seconds.
3. The leaf becomes stationary and remains a stage-front foreground occluder.
4. The Keeper crosses behind it and through the doorway.
5. The game waits until his complete bounds clear the swept volume plus a safety margin.
6. The door closes automatically in about 0.72 seconds.

The leaf must never pass through the Keeper. Opening or closing is forbidden while his bounds intersect the swept volume. A held-open state is an explicit scripted override only. The Keeper has no hand-on-handle animation.

Render order while open: room shell and frame → Keeper → open leaf and jamb → later foreground overlays.

## Integration points

The existing studio has useful semantics but placeholder visuals:

- `src/studio/recipe.ts` currently defines placeholder logical door dimensions and already treats an open leaf as a foreground solid and cover.
- `src/studio/StageView.tsx` draws the leaf as an SVG rectangle.
- `src/studio/recipe.test.ts` tests closed-door rejection, hidden crossing, coverage and open-leaf collision.

Preserve those semantics, introduce one explicit conversion between logical stage units and room-art pixels, replace the drawn rectangle with the painted asset, and add a real automatic door state machine. Do not blindly paste 168 and 336 into a logical-unit model.

Locate and wire the actual game room renderer as well as the studio preview. A studio-only implementation is incomplete.

The implementation must not redraw the door in SVG, CSS or canvas. Code may transform, mask, position and animate the supplied painted PNG.

## Acceptance

- Asset and mip dimensions and hashes pass `verify_handoff.py`.
- Keeper remains exactly 120 × 298 at room scale.
- Door reaches 90°, becomes stationary, and only then admits the Keeper.
- Door never intersects the Keeper and closes only after full clearance.
- Stationary open leaf fully occludes the Keeper at the hidden crossing point.
- Handed variants have one hinge edge and the handle on the free edge.
- Room and lighthouse captures are both reviewed.
- Existing collision/coverage tests remain green and gain sweep-lock and delayed-auto-close tests.
- The actual game flow, not just the studio, is tested.

This handoff does not authorize kitchen-cabinet changes, new art generation, or modification of the approved Prime Keeper.
