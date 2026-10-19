#!/usr/bin/env python3
"""Build Sink Water Workbench V20 with a thin outlet stream and tall comic jets."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-water-workbench-2026-10-19-v20"
V19 = ROOT / "art/raw/kitchen-sink-smooth-join-2026-10-19-v19"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-water-workbench-v20"
ASSETS = PUBLIC / "assets"
CELL = (120, 144)
BASE_OFFSET = (14, 36)
ROOM_EFFECT_ORIGIN = (318, 68)
FRAMES = 40
FPS = 4
DURATION = 10


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def thin_on_frame(source: Image.Image) -> Image.Image:
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    # Compress only the falling column from eight native pixels to the exact
    # four-pixel outlet span. Preserve the animated basin splash unchanged.
    column = source.crop((49, 19, 57, 35)).resize((4, 16), Image.Resampling.NEAREST)
    output.alpha_composite(column, (64, 55))
    output.alpha_composite(source.crop((0, 35, 92, 39)), (14, 71))
    return output


def tall_broken_frame(source: Image.Image) -> Image.Image:
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    # Preserve the approved water drawing and palette, but lengthen the rising
    # jets around their basin contact. The splash remains at exact native scale.
    jets = source.crop((0, 4, 92, 35)).resize((92, 66), Image.Resampling.NEAREST)
    output.alpha_composite(jets, (14, 5))
    output.alpha_composite(source.crop((0, 35, 92, 40)), (14, 71))
    return output


def build_strip(source: Image.Image, transform) -> tuple[Image.Image, list[Image.Image]]:
    strip = Image.new("RGBA", (CELL[0] * FRAMES, CELL[1]), (0, 0, 0, 0))
    frames = []
    for index in range(FRAMES):
        frame = source.crop((index * 92, 0, (index + 1) * 92, 108))
        amended = transform(frame)
        strip.alpha_composite(amended, (index * CELL[0], 0))
        frames.append(amended)
    return strip, frames


def cell_proof(base: Image.Image, effect: Image.Image) -> Image.Image:
    output = Image.new("RGBA", CELL, (0, 0, 0, 0))
    output.alpha_composite(base, BASE_OFFSET)
    output.alpha_composite(effect)
    return output


def room_proof(room: Image.Image, effect: Image.Image) -> Image.Image:
    output = room.copy()
    output.alpha_composite(effect, ROOM_EFFECT_ORIGIN)
    return output


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_sink_water_workbench_v20.html").read_text()
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":")))


def main() -> None:
    for directory in (RAW, DRAFT, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, DRAFT, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    base = Image.open(V19 / "sink-cabinet-standard.png").convert("RGBA")
    room = Image.open(V19 / "cabinet-run-plus-sink-native-room.png").convert("RGBA")
    old_on = Image.open(V19 / "fx-sink-on-water-f40.png").convert("RGBA")
    old_broken = Image.open(V19 / "fx-sink-broken-basin-spouts-f40.png").convert("RGBA")
    on_strip, on_frames = build_strip(old_on, thin_on_frame)
    broken_strip, broken_frames = build_strip(old_broken, tall_broken_frame)

    outputs = {
        "sink-cabinet-v19.png": base,
        "room-v19.png": room,
        "v19-fx-sink-on-water-f40.png": old_on,
        "v19-fx-sink-broken-water-f40.png": old_broken,
        "fx-sink-on-thin-outlet-flow-f40.png": on_strip,
        "fx-sink-broken-tall-comic-jets-f40.png": broken_strip,
        "sink-on-v20-frame-00.png": cell_proof(base, on_frames[0]),
        "sink-broken-v20-frame-00.png": cell_proof(base, broken_frames[0]),
        "room-on-v20-frame-00.png": room_proof(room, on_frames[0]),
        "room-broken-v20-frame-00.png": room_proof(room, broken_frames[0]),
    }
    for name, image in outputs.items():
        save(image, RAW / name)
        shutil.copyfile(RAW / name, ASSETS / name)

    effects = {
        "sink-on-thin-outlet-flow": {
            "state": "on",
            "label": "Thin outlet flow",
            "file": "fx-sink-on-thin-outlet-flow-f40.png",
            "origin": list(ROOM_EFFECT_ORIGIN),
            "size": list(CELL),
            "frames": FRAMES,
            "fps": FPS,
            "durationSeconds": DURATION,
            "sfx": "kitchen_sink_water_gentle_loop",
            "editable": ["enabled", "drag", "resize", "crop", "nudge", "speed"],
        },
        "sink-broken-tall-comic-jets": {
            "state": "broken",
            "label": "Tall comic upward jets",
            "file": "fx-sink-broken-tall-comic-jets-f40.png",
            "origin": list(ROOM_EFFECT_ORIGIN),
            "size": list(CELL),
            "frames": FRAMES,
            "fps": FPS,
            "durationSeconds": DURATION,
            "sfx": "kitchen_sink_pipe_burst_loop",
            "editable": ["enabled", "drag", "resize", "crop", "nudge", "speed"],
        },
    }
    catalogue = {
        "set": SET,
        "version": 20,
        "status": "water-effects-placement-awaiting-visual-review",
        "parent": "kitchen-sink-smooth-join-2026-10-19-v19",
        "base": {
            "file": "sink-cabinet-v19.png",
            "room": "room-v19.png",
            "byteIdenticalToV19": True,
            "baseOffsetInEffectCell": list(BASE_OFFSET),
            "roomSinkOrigin": [332, 104],
        },
        "effects": effects,
        "stateEffect": {"on": "sink-on-thin-outlet-flow", "broken": "sink-broken-tall-comic-jets"},
        "comparison": {
            "on": "v19-fx-sink-on-water-f40.png",
            "broken": "v19-fx-sink-broken-water-f40.png",
            "oldCellPixels": [92, 108],
        },
        "method": {
            "assetFirstSelection": True,
            "effectRemovable": True,
            "dragResizeCropNudge": True,
            "perEffectSpeedRange": [0.1, 4],
            "localPersistence": True,
            "jsonExport": True,
            "canonicalFrames": FRAMES,
            "canonicalFps": FPS,
            "canonicalDurationSeconds": DURATION,
            "effectCellPixels": list(CELL),
            "transparentGutters": True,
        },
        "outputs": {name: sha(RAW / name) for name in outputs},
        "media": list(outputs),
        "boundaries": {
            "v19Changed": False,
            "cabinetOrSinkChanged": False,
            "finalChanged": False,
            "runtimeChanged": False,
            "promotionPerformed": False,
        },
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    register = {
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "parent": catalogue["parent"],
        "files": {
            str(path.relative_to(ROOT)): sha(path)
            for path in [
                V19 / "sink-cabinet-standard.png",
                V19 / "cabinet-run-plus-sink-native-room.png",
                V19 / "fx-sink-on-water-f40.png",
                V19 / "fx-sink-broken-basin-spouts-f40.png",
                catalogue_path,
                *[RAW / name for name in outputs],
            ]
        },
    }
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print("Built Sink Water Workbench V20: thin outlet flow, tall comic jets, movable 40-frame layers")


if __name__ == "__main__":
    main()
