# Kitchen Oven Standalone V26 — 19 October 2026

## Purpose

V26 is the first clean-slate appliance family after approval of the modular cabinet and exposed-end methodology. It builds one complete standalone oven/hob in three coordinated states rather than amending a cabinet bay or laying a new oven over an old one.

The review route is `/keeper-review/kitchen-oven-standalone-v26/`.

## Exact geometry

- logical oven body: `84 × 77 px`;
- room bounds: `x=336–420`, `y=131–208`;
- transparent cell: `92 × 85 px`, with four transparent pixels on every edge;
- approved cabinet bodies remain at `x=168–336` and `x=420–588`, `y=134–208`;
- Prime interaction anchor remains `(378,218)`.

The oven contains its own hob. It contains no cabinet or countertop pixels. Each native room proof draws the exact approved V11 cabinet cell twice, then draws one complete oven cell into the independent centre slot.

## States

- **Off:** dark cavity, inactive warning light, integrated two-ring hob.
- **On:** solid red indicator, turned controls, warm internal light and visible roasting dish.
- **Broken:** the same oven with its door still attached at the bottom hinge and opening symmetrically toward the camera; the window remains transparent, the roast is burnt and blackened, and one rotary dial hangs from the fascia on exactly two wires.

The Broken base contains no smoke, sparks, flames or electrical flash. Smoke remains a later separate reusable environmental layer.

## Registered Broken lighting

The dark, cavity-lit, warning-lit and both-lit Broken variants all derive from one identical raster. Only RGB values inside recorded cavity and warning-light regions differ; alpha and geometry are identical pixel for pixel. This prevents the door, hob or fascia from jumping when the lights change.

Two deterministic `40-frame`, `4-fps`, ten-second schedules are supplied:

- an irregular failing-bulb cavity flicker with uneven dark holds, isolated flashes, sputters and a terminal flutter;
- a faster, angrier red-warning flicker.

The review page lets either lighting fault be removed independently and varies playback from `0.1×` to `4×`. Named SFX placeholders are recorded for the On fan, Broken low electrical buzz, warning blink, cavity bulb and later smoke hiss.

## Reversibility and generation

The high-resolution three-state source and its Broken-lit companion were created with the built-in image-generation workflow. Their hashes, reference files and full prompt set are recorded in `art/source/kitchen-oven-standalone-2026-10-19-v26/generation-provenance.json`.

V26 is an unapproved, unpromoted review draft. It changes no approved cabinet pixels, room background, Final art or runtime data. No later kitchen asset has begun.

## Documentation audit

README, STATUS, DECISIONS, the package verification commands, the public route and the archive manifest were checked against the delivered files and behaviour on 19 October 2026. They consistently describe V11 as the approved cabinet authority, V25 as the accepted sink-edge correction and V26 as the active unapproved oven gate. Setup, archive/deployment rules, rollback boundaries and the remaining asset sequence are unchanged.
