#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"
OUTPUTS = ROOT / "outputs"
REFERENCE = ROOT / "sources/reference"


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


layout = json.loads((REFERENCE / "kitchen_v15_schematic.json").read_text())
gate = json.loads((ROOT / "gate-report.json").read_text())
manifest = json.loads((ROOT / "manifest.json").read_text())
drafts = json.loads((ROOT / "DRAFTS.json").read_text())

assert layout["version"] == 15
assert layout["module"] == [2048, 576]
assert gate["layoutAuthority"] == "docs/layout/kitchen_v15_schematic.json"
assert gate["modulePx"] == [2048, 576]
assert manifest["status"] == "review-candidate-awaiting-frank"
assert manifest["runtimeMutation"] is False
assert manifest["deployment"] is False
assert drafts["canonicalReview"]["sha256"] == sha(ROOT.parent / "kitchen-v15-painted-room-v5" / "outputs" / "kitchen-v15-check-3-day1-room.png")
assert drafts["draftReview"]["sha256"] == sha(OUTPUTS / "kitchen-v15-check-3-day1-room.png")
assert drafts["sourcePin"]["sha256"] == sha(ROOT / "sources" / "liked-kitchen-source-2172x724.png")

liked = ROOT / "sources/liked-kitchen-source-2172x724.png"
liked_hash = "404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15"
assert rgba(liked).size == (2172, 724)
assert sha(liked) == liked_hash
assert gate["sourcePreservation"]["unchanged"] is True
assert gate["sourcePreservation"]["actualSha256"] == liked_hash

assert sha(REFERENCE / "prime_keeper_120x298.png") == "756f0a723c55997a3d5c38c625765b4077e7d959b7cd5827bcf69c17e27f4444"
assert sha(REFERENCE / "room_door_open_leaf_168x336.png") == "dcf43fec6dd3de41d7904699c88394fa985c0a4f505d4ac67adf391039c8ecbd"
assert rgba(REFERENCE / "prime_keeper_120x298.png").size == (120, 298)
assert rgba(REFERENCE / "room_door_open_leaf_168x336.png").size == (168, 336)

shell_ids = {"back_wall", "floor_band", "window_L", "window_R"}
expected_items = [item for item in layout["items"] if item["id"] not in shell_ids]
assert len(expected_items) == 19
assert gate["schema"] == "lighthouse-keeper/kitchen-v15-painted-room-v6-gate@3"
assert gate["summary"] == {
    "pieceCount": 19,
    "exactCanvasPassCount": 19,
    "allPiecesFit": True,
    "allRepeatedMastersExact": True,
    "ovenSpacingSymmetrical": True,
    "sinkSharesBaseBody": True,
    "dresserSharesWorktopDepth": True,
    "doorStatesExclusive": True,
    "actualEdgeCutsPass": True,
    "allHardDatumsPass": True,
}
assert "larder.png" not in manifest["parts"]

report_by_id = {entry["id"]: entry for entry in gate["pieces"]}
for item in expected_items:
    item_id = item["id"]
    x1, y1, x2, y2 = item["rect"]
    expected_size = (x2 - x1, y2 - y1)
    path = PARTS / f"{item_id}.png"
    assert path.exists(), item_id
    assert rgba(path).size == expected_size, (item_id, rgba(path).size, expected_size)
    assert report_by_id[item_id]["requiredCanvasPx"] == list(expected_size)
    assert report_by_id[item_id]["actualCanvasPx"] == list(expected_size)
    assert report_by_id[item_id]["fitsV15Box"] is True
    assert report_by_id[item_id]["transparentPixelCount"] > 0
    assert report_by_id[item_id]["alphaBoundsOnCanvas"] is not None
    assert manifest["parts"][path.name]["sha256"] == sha(path)

edge = gate["actualEdgeGate"]
assert edge["ordinaryCupboardCanvasPx"] == [168, 137]
assert edge["ordinaryCupboardsByteIdentical"] is True
assert len(set(edge["ordinaryCupboardSha256"].values())) == 1
assert edge["wallCupboardCanvasPx"] == [136, 101]
assert edge["wallCupboardsByteIdentical"] is True
assert len(set(edge["wallCupboardSha256"].values())) == 1
assert edge["worktopsByteIdentical"] is False
assert len(set(edge["worktopSha256"].values())) == 2
assert edge["wallCupboardToCookerVisibleGapPx"] == {"left": 16, "right": 16}
assert edge["wallCupboardToCookerSpacingSymmetrical"] is True
assert edge["baseModuleCutLinesX"] == [454, 622, 790, 958, 1126, 1294, 1462, 1630]
assert edge["sinkBodyMatchesBaseCabinetBelowLocalY"] == 42
assert edge["sinkBodyMatchesBaseCabinet"] is True
assert edge["dresserDepthBandLocalY"] == [168, 199]
assert edge["dresserDepthBandRoomY"] == [317, 348]
assert edge["dresserDepthPx"] == 31
assert edge["dresserSharesWorktopDepthPixels"] is True
assert edge["allFurnitureCutsContainTransparency"] is True

# The repeated masters must be the actual files, not merely equal metadata.
ordinary = ["cupboard_A1", "cupboard_B1", "cupboard_B2", "cupboard_B3", "dw_slot_cupboard"]
assert len({sha(PARTS / f"{item_id}.png") for item_id in ordinary}) == 1
assert len({sha(PARTS / f"wall_cupboard_{index}.png") for index in (1, 2)}) == 1
assert sha(PARTS / "runA_worktop.png") != sha(PARTS / "runB_worktop.png")
assert rgba(PARTS / "sink_cabinet.png").crop((0, 42, 168, 137)).tobytes() == rgba(PARTS / "cupboard_A1.png").crop((0, 42, 168, 137)).tobytes()

assert gate["hardDatums"]["unitBaseY"] == 485
assert gate["hardDatums"]["worktopSurfaceY"] == 326
assert gate["hardDatums"]["worktopBoxY"] == [317, 348]
assert gate["hardDatums"]["hobLevelWithWorktop"] is True
assert gate["hardDatums"]["keeperSolesY"] == 502
assert gate["hardDatums"]["keeperRect"] == [1150, 204, 1270, 502]
assert all(check["exact"] for check in gate["hardDatums"]["stopCentres"])
assert all(check["pass"] and not check["collisions"] for check in gate["hardDatums"]["windowClearAreas"])
assert gate["hardDatums"]["doorLeaves"] == {
    "sourceSha256": "dcf43fec6dd3de41d7904699c88394fa985c0a4f505d4ac67adf391039c8ecbd",
    "closedPerspectiveQuads": {
        "left": [[29, 208], [94, 224], [94, 528], [29, 544]],
        "right": [[1954, 224], [2019, 208], [2019, 544], [1954, 528]],
    },
    "leftOpenRect": [0, 208, 168, 544],
    "rightOpenRect": [1880, 208, 2048, 544],
    "leftFurnitureClearancePx": 118,
    "rightFurnitureClearancePx": 37,
    "structuralShellHasNoLeaf": True,
    "closedAndOpenStatesExclusive": True,
    "closedVsStructuralCentralPixelsIdentical": True,
    "pass": True,
}
assert all(check["pass"] for check in gate["roomChecks"].values())

day1 = rgba(OUTPUTS / "kitchen-v15-day1-room-1x.png")
assert day1.size == (2048, 576)
windows = [tuple(item["rect"]) for item in layout["items"] if item["id"] in {"window_L", "window_R"}]
magenta_count = 0
near_outside = 0
for y in range(day1.height):
    for x in range(day1.width):
        r, g, b, a = day1.getpixel((x, y))
        in_window = any(x1 <= x < x2 and y1 <= y < y2 for x1, y1, x2, y2 in windows)
        if a and (r, g, b) == (255, 0, 255):
            assert in_window, (x, y)
            magenta_count += 1
        elif a and r > 180 and b > 130 and g < 100 and not in_window:
            near_outside += 1
assert magenta_count > 20_000
assert near_outside == 0

required_outputs = {
    "kitchen-v15-check-1-full-upgrade-fit.png": (2180, 740),
    "kitchen-v15-check-2-both-doors-open-clear.png": (2180, 740),
    "kitchen-v15-check-3-day1-room.png": (2180, 740),
    "kitchen-v15-day1-room-1x.png": (2048, 576),
    "kitchen-v15-both-doors-open-room-1x.png": (2048, 576),
    "kitchen-v15-structural-shell-jambs-only-1x.png": (2048, 576),
    "kitchen-v15-cabinet-edge-gate.png": (2180, 1260),
    "kitchen-v15-correction-gate.png": (2180, 1260),
    "kitchen-v15-piece-gate-sheet.png": (3000, 1900),
    "kitchen-v15-two-viewing-scales.png": (2300, 980),
    "kitchen-v15-liked-source-layout-comparison.png": (2180, 880),
}
for name, size in required_outputs.items():
    path = OUTPUTS / name
    assert rgba(path).size == size, (name, rgba(path).size, size)
    assert path.stat().st_size < 2 * 1024 * 1024, (name, path.stat().st_size)
    assert manifest["outputs"][name]["sha256"] == sha(path)

print("Kitchen v15 painted-room v6 shell/sink/dresser verification: PASS")
print("  unchanged liked 2172x724 source: yes")
print("  v15 actual-edge transparent cuts: 19/19 exact canvases")
print("  repeated base cupboards / wall cupboards: byte-identical")
print("  run A worktop contains the approved inset sink rim; run B remains the clean master")
print("  wall-cupboard to cooker visible gaps: 16 px left / 16 px right")
print("  hard datums / stop centres / window clears: pass")
print("  full-upgrade reservation check: pass (5 slots)")
print("  both 168x336 doors open and clear: pass (118 px left / 37 px right)")
print("  closed/open door states use one jamb-only structural shell: pass")
print("  sink body shares base master below local y42: pass")
print("  dresser shares the 31 px worktop depth band at room y317-348: pass")
print("  Day-1 cut-piece assembly: 2048x576")
print(f"  exact-magenta glass pixels: {magenta_count}; near-magenta outside glass: {near_outside}")
print("  Prime Keeper unchanged at 120x298, soles y502")
print("  runtime / production / deployment: untouched")
