# Kitchen v14 V3 — coherent-room review candidate

V1 and V2 are rejected. Their furniture was generated as separate objects and
assembled afterward, so the result read as a collection of assets rather than
one designed kitchen.

V3 reverses that production order. The entire kitchen was painted by the
built-in image generator as one complete room-wide scene. Cabinet language,
worktop continuity, heights, materials, line weight and light were solved
together in that single painting. Code does not draw or restyle furniture.

The build step is limited to permitted registration work: uniform scaling,
cropping, magenta-by-mask recolouring, placement of the approved ceiling and
floor-slab boundary bands, and compositing the unchanged Prime Keeper at the
schematic anchor. The room-wide side walls, windows and furniture remain one
unbroken painting. No runtime assets have been cut, promoted or deployed.

Review in this order:

- `outputs/kitchen-v14-v2-v3-continuity-comparison.png`
- `outputs/kitchen-v14-v3-v8-comparison.png`
- `outputs/kitchen-v14-v3-geometry-comparison.png`
- `outputs/kitchen-v14-v3-two-viewing-scales.png`
- `outputs/kitchen-v14-v3-coherent-room-1x.png`

Status: **review candidate awaiting Frank**. Stop before component extraction,
runtime integration, canon promotion or deployment.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v3-coherent-room/build_kitchen_v14_v3.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v3-coherent-room/verify_kitchen_v14_v3.py
```
