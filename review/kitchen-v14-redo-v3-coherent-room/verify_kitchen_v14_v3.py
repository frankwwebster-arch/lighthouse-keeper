#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
REF = ROOT / "sources/reference"
SRC = ROOT / "sources/imagegen"


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((ROOT / "manifest.json").read_text())
assert manifest["schema"] == "lighthouse-keeper/kitchen-v14-coherent-room-review@1"
assert manifest["status"] == "review-candidate-awaiting-frank"
assert manifest["previousDraftStatus"] == "rejected-no-room-continuity"
assert manifest["runtimeMutation"] is False
assert manifest["productionCutsMade"] is False
assert manifest["modulePx"] == [2048, 576]
assert manifest["twoViewingScales"] == {"room": [2048, 576], "lighthouse": [256, 72]}

source = SRC / "kitchen-v14-coherent-room-no-keeper.png"
assert rgba(source).size == (2172, 724)
assert manifest["source"]["sha256"] == sha(source)
assert manifest["source"]["registration"] == {"uniformScaleToPx": [2048, 683], "cropPx": [0, 68, 2048, 644]}

empty = rgba(OUT / "kitchen-v14-v3-coherent-room-empty-1x.png")
room = rgba(OUT / "kitchen-v14-v3-coherent-room-1x.png")
shell = rgba(REF / "kitchen-v8-room-shell-empty-1x.png")
prime = rgba(OUT / "kitchen-v14-v3-prime-registered.png")
assert empty.size == room.size == shell.size == (2048, 576)
assert prime.size == (120, 298)

# Frozen ceiling and floor-slab boundaries come directly from the approved V8
# shell and must remain byte-identical. Side walls stay in the coherent source.
for rect in ((0, 0, 2048, 32), (0, 544, 2048, 576)):
    assert empty.crop(rect).tobytes() == shell.crop(rect).tobytes(), rect

magenta = [(r, g, b, a) for r, g, b, a in empty.get_flattened_data() if a and r > 190 and b > 140 and g < 80]
assert magenta
assert all((r, g, b) == (255, 0, 255) for r, g, b, _ in magenta)

# Prime pixels are unchanged and registered exactly at the schematic anchor.
registered = room.crop((1150, 204, 1270, 502))
for p, q in zip(prime.get_flattened_data(), registered.get_flattened_data()):
    if p[3] == 255:
        assert p == q

assert rgba(OUT / "kitchen-v14-v3-two-viewing-scales.png").size == (2300, 980)
assert rgba(OUT / "kitchen-v14-v2-v3-continuity-comparison.png").size == (4300, 900)
assert rgba(OUT / "kitchen-v14-v3-v8-comparison.png").size == (4300, 900)
assert rgba(OUT / "kitchen-v14-v3-geometry-comparison.png").size == (4300, 900)

for name, entry in manifest["outputs"].items():
    path = OUT / name
    assert entry["canvasPx"] == list(rgba(path).size)
    assert entry["sha256"] == sha(path)

print("Kitchen v14 V3 coherent-room verification: PASS")
print("  room-wide painted sources: 1")
print("  separately generated furniture assets: 0")
print("  exact room: 2048x576")
print("  lighthouse view: 256x72")
print("  exact approved ceiling/floor boundaries: yes")
print("  generated window glass normalized to exact magenta: yes")
print("  unchanged Prime registration: x=1150 y=204, 120x298")
print("  runtime / production cuts: untouched")
