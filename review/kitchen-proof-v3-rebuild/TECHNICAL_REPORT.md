# Kitchen V3 rebuild — technical report

## Outcome

The approved calibration has been rebuilt as a grid-snapped modular kitchen,
without the rejected V3's schematic treatment and without the calibration's
cast shadows. The source illustrations carry substantial bevels, layered
enamel edges, organic near-black ink, warm internal modelling and detailed
hardware; deterministic processing supplies exact geometry and key colour.

| Gate | Result |
|---|---:|
| Module | `1536 × 576` |
| Bays | `14 × 84 px`, x `328–1504` |
| Production parts | 23 item/run PNGs plus one room shell |
| Exact magenta | 21,624 pixels, confined to eight panes |
| Near-magenta | 0 |
| Item pixels above y=274 in window bays | 0 |
| Worktop runs | x `496–832`, `916–1336` |
| Worktop/cooker top | both y=305 |
| Run/cooker plinth | both y=468–485 |
| Prime Keeper | exact 256×320 source, composited 1:1 |
| Sink isolation delta | 549 pixels, x `581–745`, y `275–319` |

## Art and assembly method

The built-in image workflow produced one high-resolution transparent source
per visually distinct asset. Both the V7 cooker and Frank-approved calibration
were supplied as references. Generated dimensions, transparency and key colour
were never trusted.

The build performs these deterministic steps:

1. discard low-alpha exterior glow and shadow pixels;
2. crop to the hard illustrated silhouette;
3. fit to the exact physical/bay envelope;
4. snap opaque fills to the shared 50-colour `palette_env-v1` set;
5. restore a near-black native-scale silhouette edge;
6. write window panes as hard exact `#FF00FF` rectangles;
7. assemble shell, plinth, fronts, cooker, worktop, inserts, counter items and
   floor items from separate files.

The base worktop tiles remain full opaque rectangles beneath the sink insert.
No worktop knows what is placed on it. Light and moving-door states are
separate overlays. No generated Keeper pixels were used.

## Keeper check

The exact approved rear Prime cell is placed with source y=316 on room y=502
at x=454, 622 and 874. The worktop's displayed top edge is 180 px above his
soles, `180/298 = 60.40%` of his standing height. Major item contours are
2–3 px at native scale against the Keeper's 3–4 px; their visual weight is
compatible, although the smallest internal appliance details necessarily fall
to 1–2 px inside an 84 px bay.

## Physical/specification notes

- The task says `worktop_tile.png` is `84 × 31`, matching y=305–336. Section
  10a-2 of `docs/SPEC.md` still says `84 × 32`. The task explicitly wins, so
  this candidate uses 31 px. The authoritative vertical table in section
  10a-3 also totals 31 px (17 px reveal + 14 px front edge).
- The displayed 60.40% worktop-to-Keeper ratio is not the real-world
  `0.90/1.77 = 50.85%` ratio because screen y includes the specified depth
  projection and walking-line offset. These measurements should remain named
  separately in engine documentation.
- The absolute y values put the worktop top 163 px above the projected unit
  base (`485−322 ≈ 0.97 m` at 168 px/m), while metadata calls it 0.90 m. The
  task's absolute y values were followed. [UNSURE] Frank/Claude may wish to
  clarify whether 0.90 m refers to the cabinet/front datum rather than the
  visible slab top before production promotion.

## Approval boundary

Everything remains in `review/kitchen-proof-v3-rebuild/`. No canon, active
manifest, runtime asset, earlier proof or approved Keeper file was changed.
The full route proof is intentionally absent because the brief defers it until
D15 is decided.
