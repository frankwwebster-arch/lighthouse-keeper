#!/usr/bin/env python3
"""Build Kitchen Sink V18 with one angled worktop join over exact V11 front geometry."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

import build_kitchen_sink_basin_depth_v17 as v17


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-angled-join-2026-10-19-v18"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-angled-join-v18"
ASSETS = PUBLIC / "assets"
V17_RAW = ROOT / "art/raw/kitchen-sink-basin-depth-2026-10-19-v17"
V17_FIXTURE = V17_RAW / "sink-fixture-only.png"
V17_ON = V17_RAW / "fx-sink-on-water-f40.png"
V17_BROKEN = V17_RAW / "fx-sink-broken-basin-spouts-f40.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def angled_worktop_join(bay: Image.Image) -> Image.Image:
    """Return the replacement pixels for the shallow diagonal left worktop edge.

    The rear/top of the slab begins three pixels left of the V11 body. Its edge
    steps right once per three rows until it meets the untouched x=4 front.
    The first nine source pixels are stretched only across this small join area
    so the old vertical V11 end line is replaced rather than left underneath.
    """
    output = Image.new("RGBA", v17.v16.CELL, (0, 0, 0, 0))
    source = bay.load()
    target = output.load()
    starts = (1, 1, 1, 2, 2, 2, 3, 3, 3)
    fixed_anchor_x = 12
    source_anchor_x = 8
    for row, start in enumerate(starts):
        span = fixed_anchor_x - start
        for x in range(start, fixed_anchor_x + 1):
            source_x = round((x - start) * source_anchor_x / span)
            target[x, 30 + row] = source[source_x, row]
    return output


def apply_exact_replacement(base: Image.Image, replacement: Image.Image) -> Image.Image:
    output = base.copy()
    src = replacement.load()
    dst = output.load()
    for y in range(replacement.height):
        for x in range(replacement.width):
            if src[x, y][3]:
                dst[x, y] = src[x, y]
    return output


def page() -> str:
    html = v17.page()
    html = html.replace("/keeper-review/kitchen-sink-basin-depth-v17/", "/keeper-review/kitchen-sink-angled-join-v18/")
    html = html.replace("Kitchen Sink V17 · worktop return and basin depth", "Kitchen Sink V18 · angled worktop join")
    html = html.replace("V17 reversible draft", "V18 reversible draft")
    html = html.replace(
        '<h1>Matching worktop return and inset basin</h1><p class="lede">The front elevation remains one literal approved V11 bay. A two-pixel stepped left worktop return now continues the neighbouring slab line across the join. The basin follows that shallow plane with a narrower rear rim, angled stepped sides, shaded recessed bowl and wider front lip.</p>',
        '<h1>Angled worktop join and shallow inset basin</h1><p class="lede">The cabinet front remains the exact approved V11 hero geometry. Only the shallow worktop strip changes: its left boundary now follows one small down-right diagonal into the untouched front instead of extending vertically. The basin uses the opposite perspective cue, widening slightly from its narrower rear rim to its wider front lip.</p>',
    )
    html = html.replace(
        "V16 remains immutable rejection evidence. V17 changes no approved V11 source, Final art or runtime asset.",
        "V17 remains immutable rejection evidence. V18 changes no approved V11 source, cabinet front, Final art or runtime asset.",
    )
    html = html.replace(
        '<div class="card"><h2>Exact V11 structural bay</h2><div class="stage checker"><img class="bay" src="assets/structural-bay-exact-v11.png" alt="Exact approved V11 right cabinet bay"></div></div>',
        '<div class="card"><h2>Exact V11 structural bay</h2><div class="stage checker"><img class="bay" src="assets/structural-bay-exact-v11.png" alt="Exact approved V11 right cabinet bay"></div></div><div class="card"><h2>Angled worktop join only</h2><div class="stage checker"><img class="isolated" src="assets/worktop-angled-join-only.png" alt="Isolated shallow diagonal worktop join"></div></div>',
    )
    return html


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    bay = v17.v16.exact_v11_bay()
    fixture = Image.open(V17_FIXTURE).convert("RGBA")
    join = angled_worktop_join(bay)
    base = v17.v16.standalone_sink(bay, Image.new("RGBA", v17.v16.CELL, (0, 0, 0, 0)))
    sink = apply_exact_replacement(base, join)
    sink.alpha_composite(fixture)
    room = v17.v16.room_proof(sink)
    on = Image.open(V17_ON).convert("RGBA")
    broken = Image.open(V17_BROKEN).convert("RGBA")
    on0 = on.crop((0, 0, *v17.v16.CELL))
    broken0 = broken.crop((0, 0, *v17.v16.CELL))

    outputs = {
        "structural-bay-exact-v11.png": bay,
        "worktop-angled-join-only.png": join,
        "sink-fixture-only.png": fixture,
        "sink-cabinet-standard.png": sink,
        "sink-cabinet-on-base.png": sink,
        "sink-cabinet-broken-base.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "sink-on-frame-00.png": v17.v16.composite(sink, on0),
        "sink-broken-frame-00.png": v17.v16.composite(sink, broken0),
        "room-sink-on-frame-00.png": v17.v16.room_composite(room, on0),
        "room-sink-broken-frame-00.png": v17.v16.room_composite(room, broken0),
    }
    for name, image in outputs.items():
        v17.v16.save(image, RAW / name)
    shutil.copyfile(V17_ON, RAW / "fx-sink-on-water-f40.png")
    shutil.copyfile(V17_BROKEN, RAW / "fx-sink-broken-basin-spouts-f40.png")
    all_names = [*outputs, "fx-sink-on-water-f40.png", "fx-sink-broken-basin-spouts-f40.png"]
    for name in all_names:
        shutil.copyfile(RAW / name, ASSETS / name)

    catalogue = {
        "set": SET,
        "status": "angled-join-awaiting-visual-review",
        "construction": {
            "standaloneAsset": True,
            "structuralSource": str(v17.v16.V11.relative_to(ROOT)),
            "structuralSourceSha256": sha(v17.v16.V11),
            "structuralCropExclusive": [88, 4, 172, 78],
            "frontElevationExactV11": True,
            "frontElevationStartsAtCellY": 42,
            "worktopJoinOnlyAboveFrontElevation": True,
            "worktopJoinDirection": "down-right",
            "worktopJoinOuterStartsByRow": [1, 1, 1, 2, 2, 2, 3, 3, 3],
            "worktopJoinMeetsBodyAtCellX": 4,
            "basinFixtureByteIdenticalToV17": True,
            "basinPerspective": {
                "rearRow": {"cellY": 33, "span": [20, 70]},
                "frontRow": {"cellY": 41, "span": [18, 73]},
                "widensTowardFront": True,
            },
            "bodyPixels": list(v17.v16.BODY),
            "cellPixels": list(v17.v16.CELL),
        },
        "states": {"staticBasesByteIdentical": True, "tapAndBasinChangedWhenBroken": False},
        "effects": {
            "onWater": {"source": str(V17_ON.relative_to(ROOT)), "byteIdenticalToV17": True, "frames": v17.v16.FRAME_COUNT, "fps": v17.v16.FPS, "durationSeconds": v17.v16.DURATION, "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"source": str(V17_BROKEN.relative_to(ROOT)), "byteIdenticalToV17": True, "frames": v17.v16.FRAME_COUNT, "fps": v17.v16.FPS, "durationSeconds": v17.v16.DURATION, "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "outputs": {name: sha(RAW / name) for name in all_names},
        "boundaries": {"v11Changed": False, "v17Changed": False, "cabinetFrontChanged": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [v17.v16.V11, V17_FIXTURE, V17_ON, V17_BROKEN, v17.v16.BACKGROUND, catalogue_path, *[RAW / name for name in all_names]]
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in registered}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink V18: angled worktop join, exact V11 front and V17 splayed basin")


if __name__ == "__main__":
    main()
