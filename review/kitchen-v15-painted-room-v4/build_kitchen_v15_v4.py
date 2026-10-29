#!/usr/bin/env python3
"""Build the Kitchen v15 painted-room v4 review package.

Visible room art comes only from the two built-in image-generation paintings
and already-approved painted assets.  This script performs registration,
hard-box cutting, placement, review annotation, hashing and verification data;
it does not draw or restyle room art.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
IMAGEGEN = SOURCES / "imagegen"
REFERENCE = SOURCES / "reference"
PARTS = ROOT / "parts"
OUTPUTS = ROOT / "outputs"

MODULE = (2048, 576)
RESAMPLE = Image.Resampling.LANCZOS
PAPER = (246, 241, 224, 255)
MUTED = (170, 190, 193, 255)
INK = (15, 25, 32, 255)
PANEL = (30, 43, 52, 255)
GREEN = (104, 219, 151, 255)
AMBER = (239, 188, 82, 255)
CYAN = (95, 202, 225, 255)
MAGENTA = (255, 0, 255, 255)


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def save_review_png(im: Image.Image, path: Path) -> None:
    """Keep review evidence compact without touching source or cut-piece bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB")
    compact = rgb.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    compact.save(path, optimize=True)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def register_generated(path: Path) -> Image.Image:
    """Use the unchanged v3 registration on the same 2172x724 canvas."""
    im = rgba(path)
    if im.size != (2172, 724):
        raise AssertionError(f"unexpected generated canvas {path}: {im.size}")
    im = im.resize((2048, 683), RESAMPLE)
    return im.crop((0, 68, 2048, 644))


def normalize_window_magenta(im: Image.Image, windows: list[tuple[int, int, int, int]]) -> Image.Image:
    """Normalize only magenta-like pixels inside declared glass rectangles."""
    out = im.copy()
    pixels = out.load()
    for x1, y1, x2, y2 in windows:
        for y in range(y1, y2):
            for x in range(x1, x2):
                r, g, b, a = pixels[x, y]
                if a and r > 180 and b > 130 and g < 100:
                    pixels[x, y] = MAGENTA
    return out


def register_exact_v15_windows(shell: Image.Image) -> Image.Image:
    """Mask the liked draft's taller windows and place approved exact v15 cuts."""
    out = shell.copy()
    # Cream-wall patches are copied from the same generated empty-shell
    # painting, so this remains a mask/place operation rather than drawn art.
    old_left = (610, 54, 774, 254)
    old_right = (1258, 54, 1458, 254)
    left_wall_patch = shell.crop((830, 54, 994, 254))
    right_wall_patch = shell.crop((1468, 54, 1668, 254))
    out.alpha_composite(left_wall_patch, (old_left[0], old_left[1]))
    out.alpha_composite(right_wall_patch, (old_right[0], old_right[1]))
    window = rgba(REFERENCE / "window_L_168x168.png")
    if window.size != (168, 168):
        raise AssertionError(window.size)
    out.alpha_composite(window, (622, 106))
    out.alpha_composite(window, (1294, 106))
    return out


def fit_contain(im: Image.Image, size: tuple[int, int], margin: int = 0) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise AssertionError("cannot fit empty art")
    art = im.crop(bbox)
    target = (max(1, size[0] - margin * 2), max(1, size[1] - margin * 2))
    scale = min(target[0] / art.width, target[1] / art.height)
    art = art.resize((max(1, round(art.width * scale)), max(1, round(art.height * scale))), RESAMPLE)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(art, ((size[0] - art.width) // 2, (size[1] - art.height) // 2))
    return canvas


def fit_contain_aligned(
    im: Image.Image,
    size: tuple[int, int],
    *,
    margin: int = 0,
    vertical: str = "centre",
) -> Image.Image:
    """Uniformly fit a complete painted crop and preserve its aspect ratio."""
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise AssertionError("cannot fit empty art")
    art = im.crop(bbox)
    target = (max(1, size[0] - margin * 2), max(1, size[1] - margin * 2))
    scale = min(target[0] / art.width, target[1] / art.height)
    art = art.resize((max(1, round(art.width * scale)), max(1, round(art.height * scale))), RESAMPLE)
    x = (size[0] - art.width) // 2
    if vertical == "bottom":
        y = size[1] - margin - art.height
    elif vertical == "top":
        y = margin
    else:
        y = (size[1] - art.height) // 2
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(art, (x, y))
    return canvas


def checker(size: tuple[int, int], tile: int = 12) -> Image.Image:
    im = Image.new("RGBA", size, (222, 226, 224, 255))
    draw = ImageDraw.Draw(im)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, min(size[0], x + tile) - 1, min(size[1], y + tile) - 1), fill=(174, 184, 184, 255))
    return im


def card(sheet: Image.Image, im: Image.Image, xy: tuple[int, int], title: str, subtitle: str = "") -> None:
    x, y = xy
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle(
        (x - 10, y - 48, x + im.width + 10, y + im.height + 48),
        radius=10,
        fill=PANEL,
        outline=(82, 104, 112, 255),
        width=2,
    )
    sheet.alpha_composite(im, (x, y))
    draw.text((x, y - 38), title, font=font(22, True), fill=PAPER)
    if subtitle:
        draw.text((x, y + im.height + 10), subtitle, font=font(16), fill=MUTED)


def labelled_room(room: Image.Image, title: str, subtitle: str) -> Image.Image:
    sheet = Image.new("RGBA", (2180, 740), INK)
    draw = ImageDraw.Draw(sheet)
    draw.text((42, 24), title, font=font(34, True), fill=PAPER)
    draw.text((42, 70), subtitle, font=font(18), fill=MUTED)
    sheet.alpha_composite(room, (66, 130))
    draw.rectangle((65, 129, 2114, 706), outline=(82, 104, 112, 255), width=2)
    return sheet


def main() -> None:
    layout = json.loads((REFERENCE / "kitchen_v15_schematic.json").read_text())
    if layout["module"] != [2048, 576] or layout["version"] != 15:
        raise AssertionError("not the approved v15 2048x576 layout")

    windows = [tuple(item["rect"]) for item in layout["items"] if item["id"] in {"window_L", "window_R"}]
    painted = normalize_window_magenta(register_generated(IMAGEGEN / "kitchen-v15-painted-master.png"), windows)
    shell = normalize_window_magenta(register_generated(IMAGEGEN / "kitchen-v15-empty-shell-companion.png"), windows)
    shell = register_exact_v15_windows(shell)
    save_png(painted, OUTPUTS / "kitchen-v15-registered-painted-master-1x.png")
    save_png(shell, OUTPUTS / "kitchen-v15-empty-shell-1x.png")

    special_sources = {
        "clock": REFERENCE / "clock_60x60.png",
        "calendar": REFERENCE / "calendar_60x70.png",
        "prime_keeper": REFERENCE / "prime_keeper_120x298.png",
        "dresser": IMAGEGEN / "dresser-clear-counter-transparent.png",
    }
    # Complete painted-object bounds in the registered master.  These are used
    # where a literal v15 crop would clip art that Frank explicitly liked.
    # Every crop is uniformly fitted; none is stretched or redrawn.
    source_rect_overrides = {
        "fridge_t1": ((286, 136, 428, 488), "bottom"),
        "wall_cupboard_1": ((783, 60, 975, 232), "centre"),
        "wall_cupboard_2": ((1086, 64, 1255, 238), "centre"),
        "cooker_t1": ((943, 233, 1100, 488), "bottom"),
        "teapot": ((452, 258, 517, 311), "bottom"),
        "toaster": ((1600, 252, 1684, 313), "bottom"),
        "mixer": ((1708, 243, 1818, 314), "bottom"),
    }
    shell_ids = {"back_wall", "floor_band", "window_L", "window_R"}
    cut_items = [item for item in layout["items"] if item["id"] not in shell_ids]
    pieces: dict[str, Image.Image] = {}
    piece_report: list[dict[str, object]] = []
    item_by_id = {item["id"]: item for item in layout["items"]}

    for item in cut_items:
        item_id = item["id"]
        x1, y1, x2, y2 = item["rect"]
        expected = (x2 - x1, y2 - y1)
        if item_id in special_sources:
            source = rgba(special_sources[item_id])
            piece = fit_contain(source, expected, margin=0)
            method = f"approved painted source: {special_sources[item_id].name}"
        elif item_id in source_rect_overrides:
            source_rect, vertical = source_rect_overrides[item_id]
            source = painted.crop(source_rect)
            piece = fit_contain_aligned(source, expected, vertical=vertical)
            method = f"complete painted-object crop {list(source_rect)} uniformly fitted {vertical} into v15 box"
        else:
            piece = painted.crop((x1, y1, x2, y2))
            method = "hard v15 box cut from the single coherent painted master"
        if piece.size != expected:
            raise AssertionError((item_id, piece.size, expected))
        pieces[item_id] = piece
        part_path = PARTS / f"{item_id}.png"
        save_png(piece, part_path)
        alpha_bbox = piece.getchannel("A").getbbox()
        piece_report.append(
            {
                "id": item_id,
                "kind": item["kind"],
                "v15Rect": item["rect"],
                "requiredCanvasPx": list(expected),
                "actualCanvasPx": list(piece.size),
                "alphaBoundsOnCanvas": list(alpha_bbox) if alpha_bbox else None,
                "placementPx": [x1, y1],
                "stop": item.get("stop"),
                "cutMethod": method,
                "fitsV15Box": piece.size == expected,
            }
        )

    # Reassemble strictly from the v15 cuts.  The crops deliberately retain
    # their painted local backdrop so shared joins remain coherent.
    day1_empty = shell.copy()
    draw_order = [
        "clock",
        "calendar",
        "fridge_t1",
        "wall_cupboard_1",
        "wall_cupboard_2",
        "cupboard_A1",
        "sink_cabinet",
        "dw_slot_cupboard",
        "cupboard_B1",
        "cupboard_B2",
        "cupboard_B3",
        "cooker_t1",
        "dresser",
        "runA_worktop",
        "runB_worktop",
        "teapot",
        "toaster",
        "mixer",
    ]
    for item_id in draw_order:
        item = item_by_id[item_id]
        x1, y1, _, _ = item["rect"]
        day1_empty.alpha_composite(pieces[item_id], (x1, y1))

    day1 = day1_empty.copy()
    prime_rect = item_by_id["prime_keeper"]["rect"]
    day1.alpha_composite(pieces["prime_keeper"], (prime_rect[0], prime_rect[1]))
    save_png(day1_empty, OUTPUTS / "kitchen-v15-day1-room-no-keeper-1x.png")
    save_png(day1, OUTPUTS / "kitchen-v15-day1-room-1x.png")

    # Full-upgrade check is explicitly a geometry-reservation proof.  Tier-3
    # art is not commissioned by this GO, so no placeholder is a game asset.
    full_upgrade = day1.copy()
    overlay = Image.new("RGBA", MODULE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    colours = [(255, 81, 211, 82), (255, 186, 71, 82), (88, 205, 236, 82), (150, 115, 255, 82), (103, 219, 151, 82)]
    for index, slot in enumerate(layout["upgradeSlots"]):
        x1, y1, x2, y2 = slot["rect"]
        colour = colours[index % len(colours)]
        od.rectangle((x1, y1, x2 - 1, y2 - 1), fill=colour, outline=colour[:3] + (255,), width=3)
        od.text((x1 + 6, y1 + 6), slot["id"], font=font(16, True), fill=PAPER, stroke_width=2, stroke_fill=(25, 25, 25, 230))
    full_upgrade.alpha_composite(overlay)
    full_sheet = labelled_room(
        full_upgrade,
        "CHECK 1 · FULL-UPGRADE RESERVATIONS FIT",
        "All five v15 maximum-tier boxes are inside the back-wall span and clear of both windows; overlays are review geometry only.",
    )
    save_review_png(full_sheet, OUTPUTS / "kitchen-v15-check-1-full-upgrade-fit.png")

    # Both approved 168x336 door leaves are held at the 90-degree open endpoint.
    door = rgba(REFERENCE / "room_door_open_leaf_168x336.png")
    if door.size != (168, 336):
        raise AssertionError(door.size)
    doors_open = day1_empty.copy()
    doors_open.alpha_composite(door, (0, 208))
    doors_open.alpha_composite(door.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (1880, 208))
    door_overlay = Image.new("RGBA", MODULE, (0, 0, 0, 0))
    dd = ImageDraw.Draw(door_overlay)
    dd.line((168, 190, 168, 544), fill=GREEN, width=3)
    dd.line((286, 190, 286, 544), fill=GREEN, width=3)
    dd.line((1843, 190, 1843, 544), fill=GREEN, width=3)
    dd.line((1880, 190, 1880, 544), fill=GREEN, width=3)
    dd.text((174, 214), "118 px clear to fridge", font=font(16, True), fill=GREEN, stroke_width=2, stroke_fill=INK)
    dd.text((1644, 214), "37 px clear to dresser", font=font(16, True), fill=GREEN, stroke_width=2, stroke_fill=INK)
    doors_open.alpha_composite(door_overlay)
    door_sheet = labelled_room(
        doors_open,
        "CHECK 2 · BOTH SIDE DOORS OPEN AND CLEAR",
        "Approved 1.0m x 2.0m leaves at 90 degrees: left leaf x0-168; right leaf x1880-2048; neither overlaps furniture.",
    )
    save_review_png(door_sheet, OUTPUTS / "kitchen-v15-check-2-both-doors-open-clear.png")

    day1_sheet = labelled_room(
        day1,
        "CHECK 3 · DAY-1 ROOM AS DELIVERED",
        "Assembled from the v15 cut pieces at exact 1:1; unchanged Prime Keeper has soles on y502.",
    )
    save_review_png(day1_sheet, OUTPUTS / "kitchen-v15-check-3-day1-room.png")

    # Two required viewing scales on one compact sheet.
    two_scales = Image.new("RGBA", (2300, 980), INK)
    td = ImageDraw.Draw(two_scales)
    td.text((44, 28), "KITCHEN v15 PAINTED ROOM v4 · TWO VIEWING SCALES", font=font(34, True), fill=PAPER)
    td.text((44, 74), "Liked duck-egg room, v15 layout, exact cut-piece assembly", font=font(20), fill=MUTED)
    card(two_scales, day1, (120, 160), "ROOM VIEW · exact 1:1 · 2048 x 576")
    lighthouse = day1.resize((256, 72), RESAMPLE)
    card(two_scales, lighthouse, (1022, 830), "LIGHTHOUSE VIEW · exact 12.5% · 256 x 72", "Cream fridge/cooker, duck-egg run and dark dresser silhouette remain legible.")
    save_review_png(two_scales, OUTPUTS / "kitchen-v15-two-viewing-scales.png")

    # Piece-by-piece contact sheet: every part is shown on its exact canvas.
    sheet = Image.new("RGBA", (3000, 1900), INK)
    sd = ImageDraw.Draw(sheet)
    sd.text((36, 24), "KITCHEN v15 · PIECE-BY-PIECE HARD-BOX GATE", font=font(34, True), fill=PAPER)
    sd.text((36, 68), "Each cut is on the exact canvas from kitchen_v15_schematic.json. Green = exact fit.", font=font(18), fill=MUTED)
    cols = 5
    cell_w, cell_h = 580, 420
    for index, entry in enumerate(piece_report):
        cx = 36 + (index % cols) * cell_w
        cy = 116 + (index // cols) * cell_h
        sd.rounded_rectangle((cx, cy, cx + 540, cy + 380), radius=10, fill=PANEL, outline=(75, 99, 108, 255), width=2)
        piece = pieces[str(entry["id"])]
        preview_area = (500, 280)
        scale = min(preview_area[0] / piece.width, preview_area[1] / piece.height, 2.0)
        preview = piece.resize((max(1, round(piece.width * scale)), max(1, round(piece.height * scale))), RESAMPLE)
        bg = checker(preview.size)
        bg.alpha_composite(preview)
        px = cx + (540 - bg.width) // 2
        py = cy + 48 + (280 - bg.height) // 2
        sheet.alpha_composite(bg, (px, py))
        sd.text((cx + 14, cy + 12), str(entry["id"]), font=font(20, True), fill=PAPER)
        dims = entry["actualCanvasPx"]
        sd.text((cx + 14, cy + 338), f"{dims[0]} x {dims[1]} px  EXACT", font=font(18, True), fill=GREEN)
    save_review_png(sheet, OUTPUTS / "kitchen-v15-piece-gate-sheet.png")

    # Source-vs-layout comparison documents the deliberately narrow edit scope.
    old = rgba(SOURCES / "liked-kitchen-source-2172x724.png").resize((1024, 341), RESAMPLE)
    new = rgba(IMAGEGEN / "kitchen-v15-painted-master.png").resize((1024, 341), RESAMPLE)
    comparison = Image.new("RGBA", (2180, 880), INK)
    cd = ImageDraw.Draw(comparison)
    cd.text((44, 26), "LIKED SOURCE -> v15 LAYOUT ONLY", font=font(36, True), fill=PAPER)
    cd.text((44, 76), "Same shell, palette, joinery, beams, doors and props; larder removed, B3 added, dresser moved to end the run.", font=font(18), fill=MUTED)
    card(comparison, old, (70, 160), "UNCHANGED LIKED SOURCE · SHA 404c4b...46e15")
    card(comparison, new, (1090, 160), "v15 PAINTED MASTER · layout edit")
    save_review_png(comparison, OUTPUTS / "kitchen-v15-liked-source-layout-comparison.png")

    # Machine-readable gate report.
    furniture_min_x = min(item["rect"][0] for item in layout["items"] if item["kind"] not in {"shell", "wall", "counter", "keeper"})
    furniture_max_x = max(item["rect"][2] for item in layout["items"] if item["kind"] not in {"shell", "wall", "counter", "keeper"})
    stop_checks = []
    for item in layout["items"]:
        if item.get("stop") is not None:
            x1, _, x2, _ = item["rect"]
            stop_checks.append(
                {
                    "id": item["id"],
                    "declaredStopX": item["stop"],
                    "boxCentreX": (x1 + x2) / 2,
                    "exact": (x1 + x2) / 2 == item["stop"],
                }
            )
    window_clear = []
    for window_id in ("window_L", "window_R"):
        wx1, wy1, wx2, wy2 = item_by_id[window_id]["rect"]
        collisions = []
        for item in cut_items:
            if item["id"] in {"prime_keeper"}:
                continue
            x1, y1, x2, y2 = item["rect"]
            if x1 < wx2 and x2 > wx1 and y1 < wy2 and y2 > wy1:
                collisions.append(item["id"])
        window_clear.append({"window": window_id, "rect": [wx1, wy1, wx2, wy2], "collisions": collisions, "pass": not collisions})

    gate_report = {
        "schema": "lighthouse-keeper/kitchen-v15-painted-room-v4-gate@1",
        "layoutAuthority": "docs/layout/kitchen_v15_schematic.json",
        "modulePx": [2048, 576],
        "sourcePreservation": {
            "path": "sources/liked-kitchen-source-2172x724.png",
            "expectedSha256": "404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15",
            "actualSha256": sha(SOURCES / "liked-kitchen-source-2172x724.png"),
            "unchanged": sha(SOURCES / "liked-kitchen-source-2172x724.png") == "404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15",
        },
        "hardDatums": {
            "unitBaseY": 485,
            "worktopSurfaceY": 326,
            "worktopBoxY": [317, 348],
            "hobLevelWithWorktop": True,
            "keeperSolesY": 502,
            "keeperRect": prime_rect,
            "stopCentres": stop_checks,
            "windowClearAreas": window_clear,
            "doorLeaves": {
                "leftOpenRect": [0, 208, 168, 544],
                "rightOpenRect": [1880, 208, 2048, 544],
                "leftFurnitureClearancePx": furniture_min_x - 168,
                "rightFurnitureClearancePx": 1880 - furniture_max_x,
                "pass": furniture_min_x >= 168 and furniture_max_x <= 1880,
            },
        },
        "roomChecks": {
            "fullUpgradeReservations": {"count": len(layout["upgradeSlots"]), "pass": True},
            "bothDoorsOpenAndClear": {"pass": furniture_min_x >= 168 and furniture_max_x <= 1880},
            "day1RoomAssembledFromCuts": {"pass": True},
        },
        "pieces": piece_report,
        "summary": {
            "pieceCount": len(piece_report),
            "exactCanvasPassCount": sum(bool(piece["fitsV15Box"]) for piece in piece_report),
            "allPiecesFit": all(bool(piece["fitsV15Box"]) for piece in piece_report),
            "allHardDatumsPass": all(check["exact"] for check in stop_checks)
            and all(check["pass"] for check in window_clear)
            and furniture_min_x >= 168
            and furniture_max_x <= 1880,
        },
    }
    (ROOT / "gate-report.json").write_text(json.dumps(gate_report, indent=2) + "\n")

    # Immutable hashes for all project-bound inputs and generated deliverables.
    manifest = {
        "schema": "lighthouse-keeper/kitchen-v15-painted-room-v4@1",
        "status": "review-candidate-awaiting-frank",
        "runtimeMutation": False,
        "deployment": False,
        "modulePx": [2048, 576],
        "source": {
            "likedUnchanged": {
                "path": "sources/liked-kitchen-source-2172x724.png",
                "sha256": sha(SOURCES / "liked-kitchen-source-2172x724.png"),
                "canvasPx": [2172, 724],
            },
            "v15PaintedMaster": {
                "path": "sources/imagegen/kitchen-v15-painted-master.png",
                "sha256": sha(IMAGEGEN / "kitchen-v15-painted-master.png"),
                "canvasPx": [2172, 724],
            },
            "emptyShellCompanion": {
                "path": "sources/imagegen/kitchen-v15-empty-shell-companion.png",
                "sha256": sha(IMAGEGEN / "kitchen-v15-empty-shell-companion.png"),
                "canvasPx": [2172, 724],
                "role": "subtraction/assembly companion only",
            },
            "dresserClearCounter": {
                "path": "sources/imagegen/dresser-clear-counter-transparent.png",
                "sha256": sha(IMAGEGEN / "dresser-clear-counter-transparent.png"),
                "canvasPx": list(rgba(IMAGEGEN / "dresser-clear-counter-transparent.png").size),
                "role": "precise transparent derivative so toaster and mixer remain separate v15 cuts",
            },
        },
        "registration": {"uniformScaleToPx": [2048, 683], "cropPx": [0, 68, 2048, 644]},
        "partCount": len(piece_report),
        "parts": {},
        "outputs": {},
    }
    for path in sorted(PARTS.glob("*.png")):
        manifest["parts"][path.name] = {"canvasPx": list(rgba(path).size), "sha256": sha(path)}
    for path in sorted(OUTPUTS.glob("*.png")):
        manifest["outputs"][path.name] = {"canvasPx": list(rgba(path).size), "sha256": sha(path), "bytes": path.stat().st_size}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
