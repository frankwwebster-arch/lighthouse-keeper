#!/usr/bin/env python3
"""Deterministic gates for the Kitchen v14 review candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = json.loads((ROOT / "docs/layout/kitchen_v14_schematic.json").read_text())
MANIFEST = json.loads((HERE / "manifest.json").read_text())


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def alpha_bbox(p: Path):
    im = Image.open(p).convert("RGBA")
    return im.getchannel("A").getbbox()


def main():
    assert SPEC["module"] == [2048, 576]
    items = {i["id"]: i for i in SPEC["items"]}
    exact_units = ("fridge_t1", "cupboard_A1", "sink_cabinet", "dw_slot_cupboard", "cooker_t1", "cupboard_B1", "cupboard_B2")
    for key in exact_units:
        assert items[key]["w"] == 168, f"{key} is not a 1.0 m / 168 px unit"
    assert items["fridge_t1"]["rect"] == [286, 183, 454, 485]
    assert items["runA_worktop"]["rect"] == [454, 317, 958, 348]
    assert items["runB_worktop"]["rect"] == [1126, 317, 1462, 348]
    assert items["runB_endcap_R"]["rect"] == [1462, 317, 1474, 348]
    assert items["cooker_t1"]["rect"] == [958, 149, 1126, 485]
    assert items["window_L"]["rect"] == [622, 106, 790, 274]
    assert items["window_R"]["rect"] == [1294, 106, 1462, 274]
    # Tall pieces satisfy the approved chunky rule: height <= 2 × width.
    for key in ("fridge_t1", "cooker_t1", "dresser", "larder"):
        assert items[key]["h"] <= items[key]["w"] * 2, f"chunky rule failed: {key}"
    # Every schematic item has its exact immutable review canvas.
    for key, item in items.items():
        p = HERE / "parts" / f"{key}.png"
        assert p.exists(), f"missing part {key}"
        assert Image.open(p).size == (item["w"], item["h"]), f"wrong canvas {key}"
        assert MANIFEST["parts"][key]["sha256"] == sha(p)
        assert alpha_bbox(p), f"empty part {key}"
    # Door layers are exact item canvases and retain transparency around the removable leaf.
    for key, size in (("fridge_door", (168,302)), ("cooker_door", (168,336)), ("larder_door", (170,319))):
        p = HERE / "states" / f"{key}.png"; im = Image.open(p).convert("RGBA")
        assert im.size == size
        assert im.getchannel("A").getextrema()[0] == 0, f"{key} is not a separate transparent layer"
    # Complete open bodies exist under each door.
    for key, size in (("fridge_body_open", (168,302)), ("cooker_body_open", (168,336)), ("larder_body_open", (170,319))):
        assert Image.open(HERE / "states" / f"{key}.png").size == size
    room = Image.open(HERE / "outputs/kitchen-v14-assembled-room-1x.png").convert("RGBA")
    assert room.size == (2048,576)
    # Window panes contain exact key magenta; furniture does not cover them.
    for x,y in ((650,140),(740,230),(1320,140),(1420,230)):
        assert room.getpixel((x,y))[:3] == (255,0,255), f"window key lost at {(x,y)}"
    # Review deliverables and range deferral.
    for name in ("kitchen-v14-contact-sheet.png","kitchen-v14-three-scale.png","kitchen-v14-door-light-contents-demos.png"):
        assert (HERE / "outputs" / name).exists()
    assert MANIFEST["range252Deferred"] is True
    assert MANIFEST["runtimeMutation"] is False
    print("Kitchen v14 verification passed: exact canvases, 168 px units, chunky tall items, doors, magenta windows, review sheets")


if __name__ == "__main__":
    main()
