#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "manifest.json").read_text())
schema = json.loads((ROOT / "sources/reference/kitchen_v14_schematic.json").read_text())
items = {i["id"]: i for i in schema["items"]}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert manifest["status"] == "review-candidate-awaiting-frank"
assert manifest["runtimeMutation"] is False
assert manifest["rejectedV14ArtworkReused"] is False
assert manifest["modulePx"] == [2048, 576]
assert manifest["twoViewingScales"] == {"room": [2048, 576], "lighthouse": [256, 72]}

for item_id, entry in manifest["parts"].items():
    path = ROOT / "parts" / f"{item_id}.png"
    im = Image.open(path).convert("RGBA")
    expected = items[item_id]
    assert list(im.size) == [expected["w"], expected["h"]], (item_id, im.size)
    assert entry["canvasPx"] == list(im.size)
    assert entry["rectPx"] == expected["rect"]
    assert entry["sha256"] == sha(path)
    if item_id not in {"back_wall", "floor_band", "window_L", "window_R"}:
        assert im.getchannel("A").getbbox(), f"empty {item_id}"
        # Items never use the environment's reserved technical magenta.
        assert all(not (r == 255 and g == 0 and b == 255 and a) for r, g, b, a in im.get_flattened_data()), item_id

for name, entry in manifest["states"].items():
    path = ROOT / "states" / name
    assert entry["sha256"] == sha(path)
    assert entry["canvasPx"] == list(Image.open(path).size)

for name, size in {
    "kitchen-v14-redo-assembled-room-1x.png": (2048, 576),
    "kitchen-v14-redo-shell-empty-1x.png": (2048, 576),
}.items():
    assert Image.open(ROOT / "outputs" / name).size == size

# Tall-item chunky rule: height is no more than twice width.
for item_id in ("fridge_t1", "cooker_t1", "dresser", "larder"):
    w, h = Image.open(ROOT / "parts" / f"{item_id}.png").size
    assert h <= 2 * w, (item_id, w, h)

# The Keeper is unchanged except approved uniform registration/canvas padding.
keeper = Image.open(ROOT / "parts/prime_keeper.png").convert("RGBA")
assert keeper.size == (120, 298)
assert keeper.getchannel("A").getbbox() == (9, 0, 111, 298)

print("Kitchen v14 redo verification: PASS")
print(f"  exact parts: {len(manifest['parts'])}")
print(f"  state layers: {len(manifest['states'])}")
print("  room view: 2048x576")
print("  lighthouse view: 256x72 (12.5%)")
print("  rejected c9c3f6c6 artwork reused: no")
