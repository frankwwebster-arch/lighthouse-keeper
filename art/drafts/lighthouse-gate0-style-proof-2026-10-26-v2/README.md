# Gate 0 style proof V2 — room-depth correction

Status: **candidate — awaiting Frank's A/B decision**.

This is the fresh, reversible successor to V1 for the conditional Gate 0
decision in `LIGHTHOUSE_SPEC_v2_DRAFT.md`. It applies Frank's
`room_depth_rule.png` without changing V1, any canon asset, runtime binding or
active manifest.

Open `review.html` and choose:

- **A — high-resolution pixel illustration:** authored at 768 × 256 and
  delivered by exact nearest-neighbour 2× to 1536 × 512.
- **B — smooth flat-colour illustration:** drawn at 1536 × 512 with smooth
  antialiased contours, flat fills and restrained shadow tones.

Both candidates use the same approved geometry and room-depth model:

- 1536 × 512 delivered module;
- 13 bays of 96 px;
- walk-in zone x=32–256;
- floor surface y=480;
- 192 × 192 windows over bays 4–5 and 10–11;
- identical exact `#FF00FF` pane masks;
- a logical plan with furniture in the back ~70% of room depth and locomotion
  only in the front ~30%;
- a strict orthographic front elevation: vertical back wall, no angled side
  walls and no floor plane seen from above;
- a flat front walking strip at y=480–511;
- furniture projected against the back wall on whole 96/192 px bay footprints;
- the Keeper registered at y=480 and composited in front of that furniture;
- the circulation opening represented only by a narrow x=32–48 jamb at the
  front-left cut edge — no back-wall door panel, door leaf, knob or stairs.

The illustrative Day-1 kitchen run is fridge (bays 1–2), cooker (3), worktop
(4–5), sink (6–7), dresser (8–9) and bin (10). Bays 11–13 remain open. These
are style-proof drawings, not promoted production item masters.

The approved side/front/back Prime frames are identity references only. The
two candidate Keeper redraws are not canon and are not promoted anywhere.

## Known identity boundary

The approved Prime images supplied by the repository have one broad white
torso band. The proposed reboot prose describes two separate chest stripes.
This style proof preserves the approved reference rather than deciding that
Gate 3 identity detail. The A/B decision is about rendering style, not canon
promotion.

## Generated-source boundary

Two initial full-room generations are retained under `sources/` as rejected
provenance. They were not used as the proof because they introduced a
perspective floor and non-key window panes. The final rooms use deterministic
shared geometry and the transparent candidate Keeper renders.

## Rebuild and verify

Use the bundled workspace Python with Pillow:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/drafts/lighthouse-gate0-style-proof-2026-10-26-v2/build_review.py

/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/drafts/lighthouse-gate0-style-proof-2026-10-26-v2/verify_review.py
```

The verifier checks source/output hashes, dimensions, 13-bay geometry metadata,
whole-bay furniture footprints, exact 2× delivery for A, identical
exact-magenta aperture masks, absence of near-magenta pixels, the flat floor
boundary, the jamb-only door representation and the intended palette
distinction.

## Documentation audit

Completed on 26 October 2026. Existing repository documentation remains
unchanged because this package is an unapproved A/B candidate and therefore
does not supersede `AGENTS.md`, `docs/CODEX_BRIEF.md` or any runtime contract.
The new room-depth rule, candidate status, rebuild commands, known Keeper
stripe boundary and non-canon/non-runtime scope are recorded entirely inside
this fresh versioned folder.
