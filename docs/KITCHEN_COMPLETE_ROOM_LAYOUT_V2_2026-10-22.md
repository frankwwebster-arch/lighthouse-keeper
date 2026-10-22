# Kitchen Complete Room Layout V2

**Date:** 22 October 2026

**Status:** deployed visual-review workbench; loose-object art, extraction,
positions and state derivation remain unapproved

## Purpose

V2 completes the room-fit foundation by adding toaster, kettle, bin, table and
chair to the exact V1 fitted cabinetry. The five objects were authored together
against the approved cabinetry sheet so their outline, restrained depth,
palette and finish remain one family. They are separately movable in both the
raw-join and join-diagnostic views.

Review route: `/keeper-review/kitchen-complete-room-layout-v2`.

## Immutable inputs

- Kitchen Cabinetry Room Layout V1 remains byte-exact. All fourteen cabinetry
  crops, state mappings, fixed six-bay order mechanics and Broken movement locks
  are inherited without alteration.
- Loose-object source sheet:
  `art/source/kitchen-loose-object-foundation-2026-10-22-v1/loose-object-construction-sheet.png`,
  SHA-256
  `3f7be0874d6a3320d89f5c15e5c467d1f71af58d5ed594530e5aef82a4b2df33`.
- The source is never overwritten. Rebuilding writes only the versioned V2
  draft and review directories.

## Geometry

The review uses the existing `772 × 224` room and these locked room-space
envelopes:

- toaster: `42 × 28 px`, worktop support `y=141`;
- kettle: `38 × 34 px`, worktop support `y=141`—approximately 20% smaller than
  the earlier oversized presentation;
- bin: `32 × 52 px`, floor support `y=208`;
- table: `80 × 58 px`, floor support `y=208`, table-top height `14.5 lp`;
- chair: `35 × 79 px`, floor support `y=208`, seat top exactly `31` room pixels
  / `7.75 lp` above the floor.

Every output is retained at 4× master density with a four-room-pixel
transparent gutter. The renderer draws those masters directly at `1×`, `2×`
or `4×`; it does not enlarge a low-resolution room screenshot.

## Interaction

- Fitted units retain exact 84-pixel drag-and-swap bays and state controls.
- Broken fitted units remain locked until repaired.
- Each loose object is independently selectable and draggable horizontally
  along its declared physical support plane. It cannot drift above or below
  the worktop/floor datum.
- Order, state, loose positions and zoom persist in browser storage.
- Geometry guides expose cabinet bays, the worktop support, the chair-seat line
  and the floor support.

## Review boundary and next gate

This is deliberately the intact loose-object foundation. It does not derive or
approve toaster, kettle or bin On/Broken states, table damage, chair variants,
motion, effects, SFX, collisions or runtime selectors. Approved Kettle V47 and
all existing behaviour remain unchanged. After Frank approves the five
drawings, state work must use these exact bodies and change only named
state-specific parts; it must not regenerate complete objects independently.

Build with
`PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/build_kitchen_complete_room_layout_v2.py`
and verify with `npm run verify:kitchen-complete-room-layout-v2`.
