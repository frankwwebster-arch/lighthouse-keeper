# Kitchen Proof V3 — technical report

## Result

The requested kitchen, modular kit and comparison evidence are built in this
folder. The render uses the approved Prime Keeper at native `1:1`; no display
transform, redraw or resampling is applied to the room-scale Keeper. The V7
authority was read from Git history and matched its required SHA-256.

| Check | Result |
|---|---:|
| Room | `1536 × 576` |
| 2× proof | `3072 × 1152`, exact nearest-neighbour |
| Tower proof | `384 × 144` |
| Parts | 22 separately delivered and described |
| Exact magenta | 39,200 pixels, confined to eight glass panes |
| Near-magenta | 0 pixels |
| Item pixels above `y=274` in window bays | 0 |
| Keeper source/display scale | `1.0 / 1.0` |
| Sole datum / room walking line | `316 / 502` |
| Worktop and cooker top | both `y=309` |
| Run and cooker plinth | both `y=468–485` |
| Sink isolation delta | 271 pixels, all within the sink insert rectangle |

## Geometry and assembly

The shell, fitted fronts, plinth, worktop, sink insert, appliances, loose
items, Keeper and foreground occluders are separate layers. Worktop runs are
continuous over `x=496–832` and `x=916–1336`; seams occur only at declared bay
joins. The sink is laid over full worktop tiles and does not cut them. The
cooker is an 84-pixel slot-in part with its own hob reveal and plinth. Oven and
dishwasher illumination are transparent overlays whose alpha and composited
deltas remain inside their declared local rectangles.

All front faces are true elevations. Only top depth is revealed at `42 px/m`.
There are no side faces, angled walls, visible ceiling or stairs. The
circulation opening is represented only by its foreground left jamb; the
separate arched exterior door is the brief's specified back-wall door.

## Route results

| Leg | Target | Current 38/38 stop | Error | D15 root stop | Error | D15 phase authority |
|---|---:|---:|---:|---:|---:|---|
| Door → sink, 6 steps | 622 | 698 | +76 | 622 | 0 | **blocked: F5 stop absent** |
| Sink → dishwasher, 2 steps | 790 | 866 | +76 | 790 | 0 | **blocked: F5 stop absent** |
| Dishwasher → cooker, 1 step | 874 | 866 | −8 | 874 | 0 | complete with existing phase |
| Cooker → fridge, 5 steps | 454 | 462 | +8 | 454 | 0 | complete with existing phase |

The D15 numbers prove the proposed root schedule. They do not prove an
approved animation for the two even-step legs: the required opposite-foot
F5-to-neutral stop bridge is absent from the approved bank. The D15 GIF labels
every placeholder frame. No pose was invented to conceal the gap.

## Physical note

The brief's two worktop ratios describe different things. The displayed
front-edge-to-sole separation is `168/298 = 56.38%`, because the keeper stands
forward of the back-wall datum in the 1/4 depth projection. The real height
ratio remains `0.90/1.77 = 50.85%`. This is internally consistent with the
specified projection, but those values should not be treated as the same
measurement in engine documentation.

## Open approval questions

1. Is the assembled ligne-claire room and its 22-part kit approved as the V3
   style/geometry direction?
2. Should a separately versioned Prime candidate task draw the missing
   F5-to-neutral bridge, using approved Prime frames as references, so D15 can
   become phase-valid? This proof cannot authorize that new Keeper art.
