#!/usr/bin/env python3
"""Build Kitchen Sink Basin Depth V17 over exact V11 structural geometry."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_kitchen_sink_cabinet_extension_v16 as v16


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-basin-depth-2026-10-19-v17"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-basin-depth-v17"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_with_depth() -> Image.Image:
    source = Image.open(v16.V15_SINK).convert("RGBA")
    output = Image.new("RGBA", v16.CELL, (0, 0, 0, 0))
    src = source.load()
    dst = output.load()
    for y in range(v16.CELL[1]):
        for x in range(v16.CELL[0]):
            r, g, b, a = src[x, y]
            if a < 8:
                continue
            keep = y < 30
            if 30 <= y <= 32 and 28 <= x <= 64:
                # Preserve the tap base and dark outline, but never copy the
                # rejected V15 worktop into the exact V11 shell.
                keep = (r >= 55 and r > g * 1.18 and g > b * 1.05) or (r < 70 and g < 70 and b < 70)
            elif 33 <= y <= 41 and 17 <= x <= 75:
                # Restore the complete perspective basin: narrower rear rim,
                # stepped side returns, shaded bowl and wider bright front lip.
                keep = r >= 145 and g >= 135 and b >= 120
                if 40 <= x <= 52 and 34 <= y <= 38 and b > r * 1.05:
                    keep = True
            if keep:
                dst[x, y] = (r, g, b, a)
    return output


def worktop_left_return(bay: Image.Image) -> Image.Image:
    """Add only the two-pixel stepped return that mates to the previous run."""
    output = Image.new("RGBA", v16.CELL, (0, 0, 0, 0))
    source = bay.load()
    target = output.load()
    # Relative worktop rows 0..12. The return steps one pixel left, then two,
    # before returning to the exact 84-pixel front elevation below the slab.
    starts = {0: 4, 1: 3, **{row: 2 for row in range(2, 11)}, 11: 3, 12: 4}
    for row, start in starts.items():
        for x in range(start, 4):
            target[x, 30 + row] = source[0, row]
    return output


def page() -> str:
    html = v16.page()
    html = html.replace("/keeper-review/kitchen-sink-cabinet-extension-v16/", "/keeper-review/kitchen-sink-basin-depth-v17/")
    html = html.replace("Kitchen Sink V16 · exact cabinet extension", "Kitchen Sink V17 · worktop return and basin depth")
    html = html.replace("V16 reversible draft", "V17 reversible draft")
    html = html.replace("<h1>Sink as an exact cabinet extension</h1><p class=\"lede\">The sink remains a completely separate asset, but its entire cabinet shell is now one literal approved V11 bay. Only the inset basin and intact tap amend those structural pixels. The adjoining worktop, fascia, doors, rails and plinth therefore share exact geometry.</p>", "<h1>Matching worktop return and inset basin</h1><p class=\"lede\">The front elevation remains one literal approved V11 bay. A two-pixel stepped left worktop return now continues the neighbouring slab line across the join. The basin follows that shallow plane with a narrower rear rim, angled stepped sides, shaded recessed bowl and wider front lip.</p>")
    html = html.replace("V15 remains immutable rejection evidence. V16 changes", "V16 remains immutable rejection evidence. V17 changes")
    html = html.replace("<h2>Sink fixture only</h2>", "<h2>Perspective basin + tap only</h2>")
    html = html.replace("Isolated basin and intact tap fixture", "Isolated perspective basin and intact tap fixture")
    return html


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    bay = v16.exact_v11_bay()
    fixture = fixture_with_depth()
    worktop_return = worktop_left_return(bay)
    sink = v16.standalone_sink(bay, Image.new("RGBA", v16.CELL, (0, 0, 0, 0)))
    sink.alpha_composite(worktop_return)
    sink.alpha_composite(fixture)
    room = v16.room_proof(sink)
    on = Image.open(v16.V15_ON).convert("RGBA")
    broken = Image.open(v16.V15_BROKEN).convert("RGBA")
    on0 = on.crop((0, 0, *v16.CELL))
    broken0 = broken.crop((0, 0, *v16.CELL))
    outputs = {
        "structural-bay-exact-v11.png": bay,
        "worktop-left-return.png": worktop_return,
        "sink-fixture-only.png": fixture,
        "sink-cabinet-standard.png": sink,
        "sink-cabinet-on-base.png": sink,
        "sink-cabinet-broken-base.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "sink-on-frame-00.png": v16.composite(sink, on0),
        "sink-broken-frame-00.png": v16.composite(sink, broken0),
        "room-sink-on-frame-00.png": v16.room_composite(room, on0),
        "room-sink-broken-frame-00.png": v16.room_composite(room, broken0),
    }
    for name, image in outputs.items():
        v16.save(image, RAW / name)
    shutil.copyfile(v16.V15_ON, RAW / "fx-sink-on-water-f40.png")
    shutil.copyfile(v16.V15_BROKEN, RAW / "fx-sink-broken-basin-spouts-f40.png")
    all_names = [*outputs, "fx-sink-on-water-f40.png", "fx-sink-broken-basin-spouts-f40.png"]
    for name in all_names:
        shutil.copyfile(RAW / name, ASSETS / name)

    catalogue = {
        "set": SET,
        "status": "inset-basin-depth-awaiting-visual-review",
        "construction": {
            "standaloneAsset": True,
            "structuralSource": str(v16.V11.relative_to(ROOT)),
            "structuralSourceSha256": sha(v16.V11),
            "structuralCropExclusive": [88, 4, 172, 78],
            "structuralPixelsExactV11": True,
            "frontElevationExactV11": True,
            "worktopLeftReturnPixels": 2,
            "worktopReturnOnlyAboveFrontElevation": True,
            "fixtureAndReturnAreOnlyAmendments": True,
            "bodyPixels": list(v16.BODY),
            "cellPixels": list(v16.CELL),
            "basinPerspective": {"rearRim": "narrower", "sideReturns": "step-out-toward-player", "bowl": "shaded-recess", "frontLip": "wider-brighter"},
        },
        "states": {"staticBasesByteIdentical": True, "tapAndBasinChangedWhenBroken": False},
        "effects": {
            "onWater": {"source": str(v16.V15_ON.relative_to(ROOT)), "byteIdenticalToV16": True, "frames": v16.FRAME_COUNT, "fps": v16.FPS, "durationSeconds": v16.DURATION, "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"source": str(v16.V15_BROKEN.relative_to(ROOT)), "byteIdenticalToV16": True, "frames": v16.FRAME_COUNT, "fps": v16.FPS, "durationSeconds": v16.DURATION, "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "outputs": {name: sha(RAW / name) for name in all_names},
        "boundaries": {"v11Changed": False, "v16Changed": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [v16.V11, v16.V15_SINK, v16.V15_ON, v16.V15_BROKEN, v16.BACKGROUND, catalogue_path, *[RAW / name for name in all_names]]
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in registered}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink V17: exact V11 front with two-pixel worktop return and perspective inset basin")


if __name__ == "__main__":
    main()
