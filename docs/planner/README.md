# Room Planner mirror (read-only, for Codex)

The source of truth for rooms, pieces, upgrades, reference images, draft history and Frank's feedback is the **Room Planner** artifact (https://claude.ai/artifact/KAvqrmWsYootZJLmEz22kL). Frank works there; Claude copies it here. **Never edit these files.** Ask for changes with a note in `docs/SPEC.md` section 19.

- `pieces.json`: every piece. **Ignore any piece with `inGame: false`**: it is kept for reference only and must not be painted, cut or briefed. Fields: `room` (place), `shape` (standard shape key, below), `status` (idea, layout, briefed, drafting, review, approved), `about`, `tiers` (1–3; tier 3 is the contraption name plate, `unlocks` = themed room), `perk`, `finish` + `swatch` (shell finishes only), `refs` (reference images), `drafts` (newest first by `date`: `image` = repo path, `verdict` keep / mixed / reject, `notes`, `pins` = Frank's pinned likes and dislikes, `x`/`y` as fractions of the image's width and height), `brief` (the next-round brief built from that feedback).
- `rooms.json`: each room's `bays` (9 standard), `windows`, `rightDoor` (none / cupboard / wc), `leftLabel`, finishes (`floorFinish`, `wallFinish`, `ceilingFinish` = piece ids) and `items` (`t` = shape key, `x` = left edge in px, `y` for free wall items, `piece` = piece id, `reserve` = upgrade space reserved above, `counter` = tall piece with a counter at worktop height).
- Shape keys: `f-<height>-<bays>` floor pieces (heights: tall 336 px = 2.0 m, work 168 = 1.0 m, appl 151 = 0.9 m, table 128 = 0.76 m, bench 84 = 0.5 m; widths 1–3 bays of 168 px); `p-floor` 84 × 84 floor prop; `d-s` 44 × 36, `d-m` 64 × 60, `d-l` 84 × 84 desktop pieces (stand on the surface beneath); `w-cup1` 136 × 101 / `w-cup2` 304 × 101 wall cupboards at y 140–241; `w-sm` 60 × 60, `w-md` 100 × 90 wall items; `w-sh1` / `w-sh2` shelves; `c-h2` 336 × 110 ceiling-hung at y 40.
- Geometry and rules: `docs/SCHEMATIC_METHOD.md`.

## Handing drafts back (Codex → Claude → planner)
Every review folder Codex delivers must include `DRAFTS.json`, one entry per draft image:

```json
[{"piece": "kitchen-fridge", "tier": 1, "label": "Redo v4 fridge", "path": "review/<folder>/<file>.png"}]
```

`piece` is an id from `pieces.json` (a whole-room painting uses the room piece, e.g. `kitchen-room`; the shell uses `shell-fixed`; a finish uses its finish id). Claude files each draft into the planner, where Frank gives his verdict and pins notes; the next brief comes from those notes.
