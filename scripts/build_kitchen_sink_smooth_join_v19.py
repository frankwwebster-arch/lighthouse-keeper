#!/usr/bin/env python3
"""Build Kitchen Sink V19 with a smooth diagonal and rounded front worktop lip."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path

from PIL import Image

import build_kitchen_sink_angled_join_v18 as v18


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-sink-smooth-join-2026-10-19-v19"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-sink-smooth-join-v19"
ASSETS = PUBLIC / "assets"
V18_RAW = ROOT / "art/raw/kitchen-sink-angled-join-2026-10-19-v18"
V18_FIXTURE = V18_RAW / "sink-fixture-only.png"
V18_STANDARD = V18_RAW / "sink-cabinet-standard.png"
V18_ON = V18_RAW / "fx-sink-on-water-f40.png"
V18_BROKEN = V18_RAW / "fx-sink-broken-basin-spouts-f40.png"

# Sub-pixel left boundary for native worktop rows y=30..42. The regular
# quarter-pixel progression removes V18's three-row staircase. The final two
# samples curl inward and finish with partial coverage comparable to the
# approved V11 worktop's softly rounded right lip.
BOUNDARY_X = (1.00, 1.26, 1.52, 1.77, 2.03, 2.29, 2.55, 2.81, 3.06, 3.32, 3.58, 3.82, 4.55)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def smooth_worktop_join(bay: Image.Image) -> Image.Image:
    output = Image.new("RGBA", v18.v17.v16.CELL, (0, 0, 0, 0))
    source = bay.load()
    target = output.load()
    fixed_anchor_x = 12
    source_anchor_x = 8
    for row, boundary in enumerate(BOUNDARY_X):
        first_x = math.floor(boundary)
        span = fixed_anchor_x - boundary
        for x in range(first_x, fixed_anchor_x + 1):
            coverage = min(1.0, max(0.0, x + 1 - boundary))
            source_x = round((x - boundary) * source_anchor_x / span)
            source_x = min(source_anchor_x, max(0, source_x))
            r, g, b, a = source[source_x, row]
            target[x, 30 + row] = (r, g, b, round(a * coverage))
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
    html = v18.page()
    html = html.replace("/keeper-review/kitchen-sink-angled-join-v18/", "/keeper-review/kitchen-sink-smooth-join-v19/")
    html = html.replace("Kitchen Sink V18 · angled worktop join", "Kitchen Sink V19 · smooth angled join")
    html = html.replace("V18 approved review authority", "V19 reversible smoothing draft")
    html = html.replace(
        '<h1>Angled worktop join and shallow inset basin</h1><p class="lede">The cabinet front remains the exact approved V11 hero geometry. Only the shallow worktop strip changes: its left boundary now follows one small down-right diagonal into the untouched front instead of extending vertically. The basin uses the opposite perspective cue, widening slightly from its narrower rear rim to its wider front lip.</p>',
        '<h1>Smooth angled join with rounded front lip</h1><p class="lede">The V18 direction remains intact, but its coarse three-row steps are replaced by a continuous antialiased down-right edge. The lowest worktop row curls inward with a softly rounded partial-alpha corner matching the finish on the right-hand worktop edge. The approved V11 cabinet face and V18 basin remain unchanged.</p>',
    )
    html = html.replace(
        "V17 remains immutable rejection evidence. V18 changes no approved V11 source, cabinet front, Final art or runtime asset.",
        "V18 remains immutable approved predecessor evidence. V19 changes no approved V11 source, cabinet front, basin, Final art or runtime asset.",
    )
    html = html.replace(
        '<section class="panel"><h2>Deterministic construction · 4× inspection</h2>',
        '<section class="panel"><h2>Approved predecessor and reversible correction · 4×</h2><div class="grid"><div class="card"><h2>V18 approved predecessor</h2><div class="stage checker"><img class="isolated" src="assets/v18-approved-predecessor.png" alt="Immutable approved V18 sink cabinet"></div></div><div class="card"><h2>V19 smoothing draft</h2><div class="stage checker"><img class="isolated" src="assets/sink-cabinet-standard.png" alt="V19 sink cabinet with smooth join and rounded front lip"></div></div></div></section><section class="panel"><h2>Deterministic construction · 4× inspection</h2>',
    )
    html = html.replace("Angled worktop join only", "Smooth join + rounded lip only")
    html = html.replace("worktop-angled-join-only.png", "worktop-smooth-join-only.png")
    html = html.replace("Isolated shallow diagonal worktop join", "Isolated smooth diagonal worktop join with rounded front lip")
    return html


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    DRAFT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    bay = v18.v17.v16.exact_v11_bay()
    fixture = Image.open(V18_FIXTURE).convert("RGBA")
    join = smooth_worktop_join(bay)
    base = v18.v17.v16.standalone_sink(bay, Image.new("RGBA", v18.v17.v16.CELL, (0, 0, 0, 0)))
    sink = apply_exact_replacement(base, join)
    sink.alpha_composite(fixture)
    room = v18.v17.v16.room_proof(sink)
    on = Image.open(V18_ON).convert("RGBA")
    broken = Image.open(V18_BROKEN).convert("RGBA")
    on0 = on.crop((0, 0, *v18.v17.v16.CELL))
    broken0 = broken.crop((0, 0, *v18.v17.v16.CELL))

    outputs = {
        "structural-bay-exact-v11.png": bay,
        "worktop-smooth-join-only.png": join,
        "v18-approved-predecessor.png": Image.open(V18_STANDARD).convert("RGBA"),
        "sink-fixture-only.png": fixture,
        "sink-cabinet-standard.png": sink,
        "sink-cabinet-on-base.png": sink,
        "sink-cabinet-broken-base.png": sink,
        "cabinet-run-plus-sink-native-room.png": room,
        "sink-on-frame-00.png": v18.v17.v16.composite(sink, on0),
        "sink-broken-frame-00.png": v18.v17.v16.composite(sink, broken0),
        "room-sink-on-frame-00.png": v18.v17.v16.room_composite(room, on0),
        "room-sink-broken-frame-00.png": v18.v17.v16.room_composite(room, broken0),
    }
    for name, image in outputs.items():
        v18.v17.v16.save(image, RAW / name)
    shutil.copyfile(V18_ON, RAW / "fx-sink-on-water-f40.png")
    shutil.copyfile(V18_BROKEN, RAW / "fx-sink-broken-basin-spouts-f40.png")
    all_names = [*outputs, "fx-sink-on-water-f40.png", "fx-sink-broken-basin-spouts-f40.png"]
    for name in all_names:
        shutil.copyfile(RAW / name, ASSETS / name)

    catalogue = {
        "set": SET,
        "status": "smooth-join-awaiting-visual-review",
        "construction": {
            "standaloneAsset": True,
            "structuralSource": str(v18.v17.v16.V11.relative_to(ROOT)),
            "structuralSourceSha256": sha(v18.v17.v16.V11),
            "structuralCropExclusive": [88, 4, 172, 78],
            "frontElevationExactV11": True,
            "frontElevationStartsAtCellY": 43,
            "worktopJoinOnlyAboveFrontElevation": True,
            "worktopJoinDirection": "smooth-down-right",
            "worktopBoundaryXByCellRow30To42": list(BOUNDARY_X),
            "roundedFrontLip": True,
            "frontLipBoundaryAlpha": Image.open(RAW / "worktop-smooth-join-only.png").convert("RGBA").getpixel((4, 42))[3] if (RAW / "worktop-smooth-join-only.png").exists() else None,
            "rightWorktopFrontLipReferenceAlpha": bay.getpixel((82, 12))[3],
            "basinFixtureByteIdenticalToV18": True,
            "basinPerspective": {
                "rearRow": {"cellY": 33, "span": [20, 70]},
                "frontRow": {"cellY": 41, "span": [18, 73]},
                "widensTowardFront": True,
            },
            "bodyPixels": list(v18.v17.v16.BODY),
            "cellPixels": list(v18.v17.v16.CELL),
        },
        "states": {"staticBasesByteIdentical": True, "tapAndBasinChangedWhenBroken": False},
        "effects": {
            "onWater": {"source": str(V18_ON.relative_to(ROOT)), "byteIdenticalToV18": True, "frames": v18.v17.v16.FRAME_COUNT, "fps": v18.v17.v16.FPS, "durationSeconds": v18.v17.v16.DURATION, "sfxCue": "kitchen_sink_water_gentle_loop"},
            "brokenWater": {"source": str(V18_BROKEN.relative_to(ROOT)), "byteIdenticalToV18": True, "frames": v18.v17.v16.FRAME_COUNT, "fps": v18.v17.v16.FPS, "durationSeconds": v18.v17.v16.DURATION, "sfxCue": "kitchen_sink_pipe_burst_loop"},
        },
        "outputs": {name: sha(RAW / name) for name in all_names},
        "boundaries": {"v11Changed": False, "v18Changed": False, "cabinetFrontChanged": False, "basinChanged": False, "finalChanged": False, "runtimeChanged": False, "promotionPerformed": False},
    }
    catalogue_path = DRAFT / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n")
    registered = [v18.v17.v16.V11, V18_FIXTURE, V18_STANDARD, V18_ON, V18_BROKEN, v18.v17.v16.BACKGROUND, catalogue_path, *[RAW / name for name in all_names]]
    register = {"set": SET, "status": "reversible-unapproved-unpromoted", "files": {str(path.relative_to(ROOT)): sha(path) for path in registered}}
    (DRAFT / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(page())
    print("Built Kitchen Sink V19: smooth antialiased join, rounded lip, exact V11 front and unchanged V18 basin/effects")


if __name__ == "__main__":
    main()
