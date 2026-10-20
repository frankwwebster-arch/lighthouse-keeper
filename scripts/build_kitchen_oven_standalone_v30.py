#!/usr/bin/env python3
"""Build Oven V30 with a protected foreground dial and dynamic join healing."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-oven-standalone-v30"
BATCH = "kitchen-oven-standalone-2026-10-20-v30"
RAW_DIR = ROOT / "art/raw" / BATCH
DRAFT_DIR = ROOT / "art/drafts" / BATCH
PUBLIC_DIR = ROOT / "public/keeper-review" / SET
TEMPLATE = ROOT / "scripts/templates/kitchen_oven_standalone_v30.html"

V29_BATCH = "kitchen-oven-standalone-2026-10-20-v29"
V29_RAW = ROOT / "art/raw" / V29_BATCH
V29_CATALOGUE = ROOT / "art/drafts" / V29_BATCH / "candidate-catalogue.json"
ROOM_BACKGROUND = ROOT / "art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png"
CABINET_CELL = ROOT / "art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png"
CABINET_APPROVAL = ROOT / "docs/review/kitchen-cabinet-run-v11-approval-2026-10-19.json"
JOIN_CAP = ROOT / "art/raw/kitchen-countertop-join-cap-2026-10-19-v22/countertop-join-cap-template.png"
JOIN_APPROVAL = ROOT / "docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json"

BODY_SIZE = (84, 77)
CELL_SIZE = (92, 85)
ROOM_SIZE = (772, 224)
OVEN_BODY_ORIGIN = (336, 131)
OVEN_CELL_ORIGIN = (332, 127)
CABINET_CELL_ORIGINS = ((164, 130), (416, 130))
CABINET_BODY_BOUNDS = ((168, 134, 168, 74), (420, 134, 168, 74))
JOIN_CAP_ORIGINS = ((324, 134), (408, 134))
JOIN_EDGES = (336, 420)
JOIN_FOCUS_BOX = (316, 126, 440, 154)
DIAL_FOCUS_BOX = (50, 18, 72, 46)
FRAME_COUNT = 40

# Cell-space foreground silhouette.  Only the lower dangling knob overlaps the
# illuminated cavity.  Its socket and wires are already outside V29's cavity
# light mask, so these rows protect precisely the pixels that were recoloured.
DIAL_FOREGROUND_ROWS = (
    (33, 54, 64),
    (34, 54, 65),
    (35, 55, 64),
    (36, 56, 63),
    (37, 56, 63),
    (38, 56, 63),
)

STATE_NAMES = (
    "oven-off.png",
    "oven-on.png",
    "oven-broken.png",
    "oven-broken-cavity-lit.png",
    "oven-broken-warning-lit.png",
    "oven-broken-both-lit.png",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_image(image: Image.Image, name: str) -> Path:
    path = RAW_DIR / name
    image.save(path)
    return path


def copy_asset(source: Path, name: str) -> Path:
    path = RAW_DIR / name
    shutil.copy2(source, path)
    return path


def protect_dangling_dial(cell: Image.Image, dark_cell: Image.Image) -> Image.Image:
    """Restore the foreground dial silhouette from the unlit Broken authority."""
    result = cell.copy()
    for y, x0, x1 in DIAL_FOREGROUND_ROWS:
        for x in range(x0, x1):
            result.putpixel((x, y), dark_cell.getpixel((x, y)))
    return result


def make_strip(frames: list[Image.Image]) -> Image.Image:
    strip = Image.new("RGBA", (CELL_SIZE[0] * len(frames), CELL_SIZE[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.alpha_composite(frame, (index * CELL_SIZE[0], 0))
    return strip


def compose_room(
    background: Image.Image,
    cabinet: Image.Image,
    oven: Image.Image,
    join_cap: Image.Image,
    *,
    heal: bool,
) -> Image.Image:
    """Compose one room. Join pixels are underlays, never appliance artwork."""
    room = background.copy()
    if heal:
        for origin in JOIN_CAP_ORIGINS:
            room.alpha_composite(join_cap, origin)
    for origin in CABINET_CELL_ORIGINS:
        room.alpha_composite(cabinet, origin)
    room.alpha_composite(oven, OVEN_CELL_ORIGIN)
    return room


def main() -> None:
    required = [
        V29_CATALOGUE,
        ROOM_BACKGROUND,
        CABINET_CELL,
        CABINET_APPROVAL,
        JOIN_CAP,
        JOIN_APPROVAL,
        TEMPLATE,
        *[V29_RAW / name for name in STATE_NAMES],
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)

    for directory in (RAW_DIR, DRAFT_DIR, PUBLIC_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    v29_data = json.loads(V29_CATALOGUE.read_text(encoding="utf-8"))
    cells = {name: Image.open(V29_RAW / name).convert("RGBA") for name in STATE_NAMES}
    for name, cell in cells.items():
        if cell.size != CELL_SIZE:
            raise RuntimeError(f"V29 authority {name} changed dimensions")

    dark = cells["oven-broken.png"]
    for name in ("oven-broken-cavity-lit.png", "oven-broken-both-lit.png"):
        cells[name] = protect_dangling_dial(cells[name], dark)

    outputs: list[Path] = [write_image(image, name) for name, image in cells.items()]

    state_strip = Image.new("RGBA", (CELL_SIZE[0] * 3, CELL_SIZE[1]), (0, 0, 0, 0))
    for index, name in enumerate(("oven-off.png", "oven-on.png", "oven-broken.png")):
        state_strip.alpha_composite(cells[name], (index * CELL_SIZE[0], 0))
    outputs.append(write_image(state_strip, "oven-state-family-strip.png"))

    cavity_pattern = v29_data["lighting"]["cavityPattern"]
    warning_pattern = v29_data["lighting"]["warningPattern"]
    if len(cavity_pattern) != FRAME_COUNT or len(warning_pattern) != FRAME_COUNT:
        raise RuntimeError("V29 lighting authority no longer has exactly 40 frames")
    cavity_frames = [cells["oven-broken-cavity-lit.png"] if value else cells["oven-broken.png"] for value in cavity_pattern]
    warning_frames = [cells["oven-broken-warning-lit.png"] if value else cells["oven-broken.png"] for value in warning_pattern]
    outputs.append(write_image(make_strip(cavity_frames), "oven-broken-cavity-flicker-f40.png"))
    outputs.append(write_image(make_strip(warning_frames), "oven-broken-warning-flicker-f40.png"))

    background = Image.open(ROOM_BACKGROUND).convert("RGBA")
    cabinet = Image.open(CABINET_CELL).convert("RGBA")
    join_cap = Image.open(JOIN_CAP).convert("RGBA")
    if background.size != ROOM_SIZE or cabinet.size != (176, 82) or join_cap.size != (24, 12):
        raise RuntimeError("Room, Cabinet V11 or approved V22 join authority changed dimensions")

    outputs.extend(
        [
            copy_asset(ROOM_BACKGROUND, "room-background-exact.png"),
            copy_asset(CABINET_CELL, "cabinet-run-v11-exact.png"),
            copy_asset(JOIN_CAP, "countertop-join-heal-template.png"),
        ]
    )

    room_cells = {
        "off": cells["oven-off.png"],
        "on": cells["oven-on.png"],
        "broken": cells["oven-broken.png"],
        "broken-cavity-lit": cells["oven-broken-cavity-lit.png"],
        "broken-warning-lit": cells["oven-broken-warning-lit.png"],
        "broken-both-lit": cells["oven-broken-both-lit.png"],
    }
    healed_rooms: dict[str, Image.Image] = {}
    raw_rooms: dict[str, Image.Image] = {}
    for state, oven_cell in room_cells.items():
        raw_rooms[state] = compose_room(background, cabinet, oven_cell, join_cap, heal=False)
        healed_rooms[state] = compose_room(background, cabinet, oven_cell, join_cap, heal=True)
        outputs.append(write_image(healed_rooms[state], f"oven-{state}-native-room.png"))

    outputs.extend(
        [
            write_image(raw_rooms["broken"].crop(JOIN_FOCUS_BOX), "oven-join-raw-focus.png"),
            write_image(healed_rooms["broken"].crop(JOIN_FOCUS_BOX), "oven-join-healed-focus.png"),
            write_image(Image.open(V29_RAW / "oven-broken-cavity-lit.png").convert("RGBA").crop(DIAL_FOCUS_BOX), "oven-v29-lit-dial-focus.png"),
            write_image(cells["oven-broken-cavity-lit.png"].crop(DIAL_FOCUS_BOX), "oven-v30-protected-dial-focus.png"),
        ]
    )

    asset_hashes = {path.name: sha256(path) for path in outputs}
    catalogue = {
        "schema": "lighthouse-keeper/kitchen-standalone-state-family@1",
        "set": SET,
        "version": 30,
        "status": "reversible-unapproved-unpromoted",
        "authorities": {
            "v29Catalogue": {"file": str(V29_CATALOGUE.relative_to(ROOT)), "sha256": sha256(V29_CATALOGUE)},
            "approvedCabinet": {"file": str(CABINET_CELL.relative_to(ROOT)), "sha256": sha256(CABINET_CELL)},
            "cabinetApproval": {"file": str(CABINET_APPROVAL.relative_to(ROOT)), "sha256": sha256(CABINET_APPROVAL)},
            "approvedJoinCap": {"file": str(JOIN_CAP.relative_to(ROOT)), "sha256": sha256(JOIN_CAP)},
            "joinApproval": {"file": str(JOIN_APPROVAL.relative_to(ROOT)), "sha256": sha256(JOIN_APPROVAL)},
            "roomBackground": {"file": str(ROOM_BACKGROUND.relative_to(ROOT)), "sha256": sha256(ROOM_BACKGROUND)},
        },
        "sources": {
            "generationMode": "deterministic-existing-pixel-compositing",
            "v29StateHashes": {name: sha256(V29_RAW / name) for name in STATE_NAMES},
        },
        "geometry": {
            **v29_data["geometry"],
            "cabinetBodyBounds": [list(item) for item in CABINET_BODY_BOUNDS],
        },
        "foregroundProtection": {
            "object": "broken dangling dial",
            "sourceState": "oven-broken.png",
            "affectedLitStates": ["oven-broken-cavity-lit.png", "oven-broken-both-lit.png"],
            "cellRows": [list(row) for row in DIAL_FOREGROUND_ROWS],
            "drawOrder": ["broken cavity light", "dangling dial foreground"],
            "dialReceivesCavityLight": False,
        },
        "joinHealing": {
            "method": "approved-v22-countertop-underlay",
            "template": "countertop-join-heal-template.png",
            "templatePixels": list(join_cap.size),
            "sharedEdgeX": list(JOIN_EDGES),
            "destinationOrigins": [list(item) for item in JOIN_CAP_ORIGINS],
            "countertopY": 134,
            "activation": "exact snapped adjacency on the corresponding oven edge",
            "drawOrder": ["room background", "active join underlays", "cabinet neighbours", "standalone oven"],
            "embeddedInOvenSprite": False,
            "embeddedInCabinetSprite": False,
            "leftAndRightIndependent": True,
        },
        "states": v29_data["states"],
        "lighting": {
            **v29_data["lighting"],
            "completeRoomVariants": [f"oven-{name}-native-room.png" for name in room_cells],
            "danglingDialForegroundProtected": True,
        },
        "sfxPlaceholders": v29_data["sfxPlaceholders"],
        "publishedAssets": asset_hashes,
        "boundaries": {
            "v29Changed": False,
            "offChanged": False,
            "onChanged": False,
            "brokenDarkChanged": False,
            "cabinetChanged": False,
            "roomBackgroundChanged": False,
            "finalChanged": False,
            "runtimeChanged": False,
            "promotionPerformed": False,
            "nextAssetStarted": False,
        },
    }
    catalogue_path = DRAFT_DIR / "candidate-catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue, indent=2) + "\n", encoding="utf-8")

    page_path = PUBLIC_DIR / "index.html"
    page_path.write_text(TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))), encoding="utf-8")
    register = {
        "schema": "lighthouse-keeper/reversible-review-batch@1",
        "set": SET,
        "status": "reversible-unapproved-unpromoted",
        "candidate": {
            "catalogue": {"file": str(catalogue_path.relative_to(ROOT)), "sha256": sha256(catalogue_path)},
            "publicShell": {"file": str(page_path.relative_to(ROOT)), "sha256": sha256(page_path)},
        },
        "sources": [
            {"file": str(path.relative_to(ROOT)), "sha256": sha256(path)}
            for path in (V29_CATALOGUE, CABINET_CELL, CABINET_APPROVAL, JOIN_CAP, JOIN_APPROVAL, ROOM_BACKGROUND)
        ],
        "publishedAssets": [
            {
                "source": str(path.relative_to(ROOT)),
                "sourceSha256": sha256(path),
                "publicAssemblyPath": str((PUBLIC_DIR / "assets" / path.name).relative_to(ROOT)),
            }
            for path in outputs
        ],
    }
    (DRAFT_DIR / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n", encoding="utf-8")
    print("Built Kitchen Oven V30: dangling dial protected and both countertop joins dynamically healable")


if __name__ == "__main__":
    main()
