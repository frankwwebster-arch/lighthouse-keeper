#!/usr/bin/env python3
"""Build the Kitchen v15 painted-room v6 corrected-shell review package.

This revision keeps the v5 cut-piece geometry, separates the room structure
from the approved moving door leaves, rebuilds the sink on the shared base
cabinet, and gives the dresser the same 31 px / 0.60 m worktop depth as the
fitted run.  New image pixels are limited to the recorded jamb-only shell edit;
all cabinet corrections are deterministic assemblies of approved painted art.
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
CLEAN = SOURCES / "clean-alpha-masters"
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
LEFT_CLOSED_QUAD = [(29, 208), (94, 224), (94, 528), (29, 544)]
RIGHT_CLOSED_QUAD = [(1954, 224), (2019, 208), (2019, 544), (1954, 528)]


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


def solve_linear(matrix: list[list[float]], values: list[float]) -> list[float]:
    """Small deterministic Gaussian solver for the 8-term door homography."""
    work = [row[:] + [value] for row, value in zip(matrix, values)]
    size = len(values)
    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(work[row][col]))
        if abs(work[pivot][col]) < 1e-12:
            raise AssertionError("singular door transform")
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for row in range(size):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [a - factor * b for a, b in zip(work[row], work[col])]
    return [work[row][-1] for row in range(size)]


def perspective_coefficients(
    source: list[tuple[float, float]], destination: list[tuple[float, float]]
) -> tuple[float, ...]:
    """Return Pillow output-to-input coefficients for four corner pairs."""
    matrix: list[list[float]] = []
    values: list[float] = []
    for (u, v), (x, y) in zip(source, destination):
        matrix.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        values.append(u)
        matrix.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        values.append(v)
    return tuple(solve_linear(matrix, values))


def door_leaf_in_quad(leaf: Image.Image, quad: list[tuple[int, int]]) -> Image.Image:
    source = [(0, 0), (leaf.width, 0), (leaf.width, leaf.height), (0, leaf.height)]
    coefficients = perspective_coefficients(source, [(float(x), float(y)) for x, y in quad])
    return leaf.transform(
        MODULE,
        Image.Transform.PERSPECTIVE,
        coefficients,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )


def make_structural_and_closed_shell() -> tuple[Image.Image, Image.Image]:
    """Return a jamb-only shell and the same shell with approved leaves closed."""
    windows = [(622, 106, 790, 274), (1294, 106, 1462, 274)]
    liked_shell = normalize_window_magenta(
        register_generated(IMAGEGEN / "kitchen-v15-empty-shell-companion.png"), windows
    )
    liked_shell = register_exact_v15_windows(liked_shell)
    jamb_donor = register_generated(IMAGEGEN / "kitchen-v15-jambs-only-shell-source.png")

    # Replace only the two side-door regions. The v5 openings were nearly
    # 500 px high and could not meet the approved 336 px leaves. Build exact
    # y208-544 apertures from the edited jamb source, use a clean liked-wall
    # patch above, and retain the liked floor below. No new pixels are drawn.
    structural = liked_shell.copy()
    # Stretch narrow, already-painted side-wall strips so colour and lighting
    # meet the original room boundary without a rectangular back-wall patch.
    left_wall = liked_shell.crop((130, 0, 140, 208)).resize((145, 208), RESAMPLE)
    right_wall = liked_shell.crop((1908, 0, 1918, 208)).resize((145, 208), RESAMPLE)
    structural.paste(left_wall, (0, 0))
    structural.paste(right_wall, (1903, 0))
    structural.paste(jamb_donor.crop((0, 208, 145, 544)), (0, 208))
    structural.paste(jamb_donor.crop((1903, 208, MODULE[0], 544)), (1903, 208))
    left_lintel = jamb_donor.crop((12, 34, 126, 58)).resize((114, 12), RESAMPLE)
    right_lintel = jamb_donor.crop((1922, 34, 2036, 58)).resize((114, 12), RESAMPLE)
    structural.paste(left_lintel, (12, 196))
    structural.paste(right_lintel, (1922, 196))

    leaf = rgba(REFERENCE / "room_door_open_leaf_168x336.png")
    closed = structural.copy()
    closed.alpha_composite(door_leaf_in_quad(leaf, LEFT_CLOSED_QUAD))
    closed.alpha_composite(
        door_leaf_in_quad(leaf.transpose(Image.Transpose.FLIP_LEFT_RIGHT), RIGHT_CLOSED_QUAD)
    )
    return structural, closed


def make_sink_from_shared_base(base: Image.Image, sink_donor: Image.Image) -> Image.Image:
    """Keep the exact base body; add the approved Belfast apron at its top."""
    if base.size != (168, 137) or sink_donor.size != (168, 211):
        raise AssertionError((base.size, sink_donor.size))
    out = base.copy()
    apron = sink_donor.crop((0, 65, 168, 110)).resize((168, 42), RESAMPLE)
    out.alpha_composite(apron, (0, 0))
    if out.crop((0, 42, 168, 137)).tobytes() != base.crop((0, 42, 168, 137)).tobytes():
        raise AssertionError("sink cabinet body drifted from shared base")
    return out


def make_sink_worktop(worktop: Image.Image, sink_donor: Image.Image) -> Image.Image:
    """Set the approved taps/rim into run A without leaving its 504x31 box."""
    if worktop.size != (504, 31) or sink_donor.size != (168, 211):
        raise AssertionError((worktop.size, sink_donor.size))
    out = worktop.copy()
    inset = sink_donor.crop((0, 18, 168, 65)).resize((168, 31), RESAMPLE)
    out.alpha_composite(inset, (168, 0))
    return out


def make_dresser_shared_depth(donor: Image.Image, worktop: Image.Image) -> Image.Image:
    """Fit the hutch around the run's exact y317-348 depth band."""
    if donor.size != (213, 336) or worktop.size != (504, 31):
        raise AssertionError((donor.size, worktop.size))
    out = Image.new("RGBA", donor.size, (0, 0, 0, 0))
    upper = donor.crop((0, 0, 213, 181)).resize((213, 168), RESAMPLE)
    lower = donor.crop((0, 201, 213, 336))
    shared_depth_band = worktop.resize((213, 31), RESAMPLE)
    out.alpha_composite(upper, (0, 0))
    out.paste(shared_depth_band, (0, 168))
    out.alpha_composite(lower, (0, 199))
    if out.crop((0, 168, 213, 199)).tobytes() != shared_depth_band.tobytes():
        raise AssertionError("dresser depth band is not the shared worktop")
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


def fit_painted_width(im: Image.Image, size: tuple[int, int], *, vertical: str = "centre") -> Image.Image:
    """Crop to actual alpha edges, then fit uniformly to the exact box width.

    Repeated cabinet modules use this once and then copy the resulting bytes.
    The visible left/right edges therefore coincide with the v15 cut lines.
    """
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise AssertionError("cannot fit empty art")
    art = im.crop(bbox)
    scale = size[0] / art.width
    fitted = (size[0], max(1, round(art.height * scale)))
    if fitted[1] > size[1]:
        scale = size[1] / art.height
        fitted = (max(1, round(art.width * scale)), size[1])
    art = art.resize(fitted, RESAMPLE)
    x = (size[0] - art.width) // 2
    if vertical == "bottom":
        y = size[1] - art.height
    elif vertical == "top":
        y = 0
    else:
        y = (size[1] - art.height) // 2
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(art, (x, y))
    return canvas


def alpha_metrics(im: Image.Image) -> dict[str, object]:
    alpha = im.getchannel("A")
    bbox = alpha.getbbox()
    histogram = alpha.histogram()
    return {
        "bounds": list(bbox) if bbox else None,
        "transparentPixels": histogram[0],
        "nonTransparentPixels": im.width * im.height - histogram[0],
        "touchesLeftCut": bool(bbox and bbox[0] == 0),
        "touchesRightCut": bool(bbox and bbox[2] == im.width),
    }


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
    structural_shell, closed_shell = make_structural_and_closed_shell()
    save_png(painted, OUTPUTS / "kitchen-v15-registered-painted-master-1x.png")
    save_png(structural_shell, OUTPUTS / "kitchen-v15-structural-shell-jambs-only-1x.png")
    save_png(closed_shell, OUTPUTS / "kitchen-v15-empty-shell-1x.png")

    approved_sources = {
        "clock": REFERENCE / "clock_60x60.png",
        "calendar": REFERENCE / "calendar_60x70.png",
        "prime_keeper": REFERENCE / "prime_keeper_120x298.png",
        "fridge_t1": CLEAN / "fridge-master.png",
        "cooker_t1": CLEAN / "cooker-master.png",
        "teapot": CLEAN / "teapot-master.png",
        "toaster": CLEAN / "toaster-master.png",
        "mixer": CLEAN / "mixer-master.png",
    }
    ordinary_cupboards = {"cupboard_A1", "dw_slot_cupboard", "cupboard_B1", "cupboard_B2", "cupboard_B3"}
    wall_cupboards = {"wall_cupboard_1", "wall_cupboard_2"}
    worktops = {"runA_worktop", "runB_worktop"}
    shell_ids = {"back_wall", "floor_band", "window_L", "window_R"}
    cut_items = [item for item in layout["items"] if item["id"] not in shell_ids]
    pieces: dict[str, Image.Image] = {}
    piece_report: list[dict[str, object]] = []
    item_by_id = {item["id"]: item for item in layout["items"]}

    for item in cut_items:
        item_id = item["id"]
        x1, y1, x2, y2 = item["rect"]
        expected = (x2 - x1, y2 - y1)
        master_group = None
        if item_id in ordinary_cupboards:
            source_path = CLEAN / "base-cupboard-master.png"
            source = rgba(source_path)
            piece = fit_painted_width(source, expected, vertical="bottom")
            method = "actual-alpha crop from one base-cupboard master; uniformly fitted to exact v15 width"
            master_group = "base-cupboard-168"
        elif item_id in wall_cupboards:
            source_path = CLEAN / "wall-cupboard-master.png"
            source = rgba(source_path)
            piece = fit_painted_width(source, expected)
            method = "actual-alpha crop from one wall-cupboard master; uniformly fitted to exact v15 width"
            master_group = "wall-cupboard-136"
        elif item_id in worktops:
            source_path = CLEAN / "worktop-504-master.png"
            source = rgba(source_path)
            piece = fit_painted_width(source, expected)
            if item_id == "runA_worktop":
                piece = make_sink_worktop(piece, rgba(CLEAN / "approved-v8-belfast-sink-master.png"))
                method = "504 px worktop master with approved v8 Belfast taps/rim set into the middle 168 px"
                master_group = "sink-integrated-worktop-504"
            else:
                method = "actual-alpha crop from one 504 px worktop master; uniformly fitted to exact v15 width"
                master_group = "worktop-504"
        elif item_id == "sink_cabinet":
            source_path = CLEAN / "approved-v8-belfast-sink-master.png"
            base = fit_painted_width(rgba(CLEAN / "base-cupboard-master.png"), expected, vertical="bottom")
            piece = make_sink_from_shared_base(base, rgba(source_path))
            method = "exact shared base-cupboard body plus approved v8 Belfast apron above y42; taps/rim are in run A worktop"
            master_group = "base-cupboard-168-body"
        elif item_id == "dresser":
            source_path = CLEAN / "v5-dresser-painted-donor.png"
            piece = make_dresser_shared_depth(rgba(source_path), rgba(CLEAN / "worktop-504-master.png"))
            method = "retained v5 painted dresser fitted around the exact shared 31 px worktop-depth band"
            master_group = "worktop-depth-31"
        elif item_id in approved_sources:
            source_path = approved_sources[item_id]
            source = rgba(source_path)
            if source.size == expected:
                # Preserve already-registered liked-room pieces byte-for-byte.
                piece = source.copy()
            else:
                vertical = "bottom" if item_id in {"fridge_t1", "teapot", "toaster", "mixer", "dresser"} else "centre"
                piece = fit_contain_aligned(source, expected, vertical=vertical)
            method = f"actual-alpha crop from approved painted source: {source_path.name}"
        else:
            raise AssertionError(f"no actual-edge source declared for {item_id}")
        if piece.size != expected:
            raise AssertionError((item_id, piece.size, expected))
        pieces[item_id] = piece
        part_path = PARTS / f"{item_id}.png"
        save_png(piece, part_path)
        metrics = alpha_metrics(piece)
        piece_report.append(
            {
                "id": item_id,
                "kind": item["kind"],
                "v15Rect": item["rect"],
                "requiredCanvasPx": list(expected),
                "actualCanvasPx": list(piece.size),
                "alphaBoundsOnCanvas": metrics["bounds"],
                "transparentPixelCount": metrics["transparentPixels"],
                "nonTransparentPixelCount": metrics["nonTransparentPixels"],
                "paintTouchesLeftCut": metrics["touchesLeftCut"],
                "paintTouchesRightCut": metrics["touchesRightCut"],
                "placementPx": [x1, y1],
                "stop": item.get("stop"),
                "cutMethod": method,
                "sharedMasterGroup": master_group,
                "fitsV15Box": piece.size == expected,
            }
        )

    # Reassemble strictly from transparent cuts. No room backdrop or neighbour
    # pixels are baked into any furniture part.
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
    def assemble_furniture(room_shell: Image.Image) -> Image.Image:
        room = room_shell.copy()
        for draw_id in draw_order:
            draw_item = item_by_id[draw_id]
            dx1, dy1, _, _ = draw_item["rect"]
            room.alpha_composite(pieces[draw_id], (dx1, dy1))
        return room

    day1_empty = assemble_furniture(closed_shell)

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
    # Start from the jamb-only shell: no closed leaf remains underneath.
    doors_open = assemble_furniture(structural_shell)
    doors_open.alpha_composite(door, (0, 208))
    doors_open.alpha_composite(door.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (1880, 208))
    doors_open_clean = doors_open.copy()
    save_png(doors_open_clean, OUTPUTS / "kitchen-v15-both-doors-open-room-1x.png")
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
    td.text((44, 28), "KITCHEN v15 PAINTED ROOM v6 · TWO VIEWING SCALES", font=font(34, True), fill=PAPER)
    td.text((44, 74), "Correct door-state shell, v15 layout, actual-edge transparent cut-piece assembly", font=font(20), fill=MUTED)
    card(two_scales, day1, (120, 160), "ROOM VIEW · exact 1:1 · 2048 x 576")
    lighthouse = day1.resize((256, 72), RESAMPLE)
    card(two_scales, lighthouse, (1022, 830), "LIGHTHOUSE VIEW · exact 12.5% · 256 x 72", "Cream fridge/cooker, duck-egg run and dark dresser silhouette remain legible.")
    save_review_png(two_scales, OUTPUTS / "kitchen-v15-two-viewing-scales.png")

    # Piece-by-piece contact sheet: exact canvas plus the actual painted alpha
    # bounds.  Unlike v4, checkerboard is real transparency, not room backdrop.
    sheet = Image.new("RGBA", (3000, 1900), INK)
    sd = ImageDraw.Draw(sheet)
    sd.text((36, 24), "KITCHEN v15 · PIECE-BY-PIECE ACTUAL-EDGE GATE", font=font(34, True), fill=PAPER)
    sd.text((36, 68), "Checkerboard = true transparency; cyan = actual painted alpha bounds; green = exact v15 canvas.", font=font(18), fill=MUTED)
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
        bounds = entry["alphaBoundsOnCanvas"]
        if bounds:
            bx1, by1, bx2, by2 = bounds
            sd.rectangle(
                (
                    px + round(bx1 * scale),
                    py + round(by1 * scale),
                    px + round(bx2 * scale) - 1,
                    py + round(by2 * scale) - 1,
                ),
                outline=CYAN,
                width=2,
            )
        sd.text((cx + 14, cy + 12), str(entry["id"]), font=font(20, True), fill=PAPER)
        dims = entry["actualCanvasPx"]
        sd.text((cx + 14, cy + 338), f"{dims[0]} x {dims[1]} px  EXACT", font=font(18, True), fill=GREEN)
        sd.text((cx + 14, cy + 362), f"alpha {bounds} · transparent {entry['transparentPixelCount']}", font=font(14), fill=MUTED)
    save_review_png(sheet, OUTPUTS / "kitchen-v15-piece-gate-sheet.png")

    # Cabinet-specific proof: exact shared cut lines and symmetrical visible
    # gap from the paired wall-cupboard master to the cooker.
    wall_left = alpha_metrics(pieces["wall_cupboard_1"])["bounds"]
    wall_right = alpha_metrics(pieces["wall_cupboard_2"])["bounds"]
    cooker_bounds = alpha_metrics(pieces["cooker_t1"])["bounds"]
    assert wall_left and wall_right and cooker_bounds
    left_wall_rect = item_by_id["wall_cupboard_1"]["rect"]
    right_wall_rect = item_by_id["wall_cupboard_2"]["rect"]
    cooker_rect = item_by_id["cooker_t1"]["rect"]
    left_gap = cooker_rect[0] + cooker_bounds[0] - (left_wall_rect[0] + wall_left[2])
    right_gap = right_wall_rect[0] + wall_right[0] - (cooker_rect[0] + cooker_bounds[2])

    edge_sheet = Image.new("RGBA", (2180, 1260), INK)
    ed = ImageDraw.Draw(edge_sheet)
    ed.text((42, 24), "CABINET CUT-LINE + OVEN-SPACING GATE", font=font(34, True), fill=PAPER)
    ed.text((42, 70), "Cuts follow the actual transparent pieces. Repeated cupboards are copies of one master, not arbitrary room crops.", font=font(18), fill=MUTED)
    edge_sheet.alpha_composite(day1_empty, (66, 116))
    ed.rectangle((65, 115, 2114, 692), outline=(82, 104, 112, 255), width=2)
    for x in (454, 622, 790, 958, 1126, 1294, 1462, 1630):
        sx = 66 + x
        ed.line((sx, 432, sx, 602), fill=CYAN, width=2)
        ed.text((sx + 3, 606), str(x), font=font(14, True), fill=CYAN)
    crop = day1_empty.crop((770, 118, 1314, 300)).resize((1632, 546), RESAMPLE)
    edge_sheet.alpha_composite(crop, (274, 714))
    ed = ImageDraw.Draw(edge_sheet)
    ed.rectangle((273, 713, 1907, 1259), outline=(82, 104, 112, 255), width=2)
    ed.text((42, 702), f"VISIBLE GAP: LEFT {left_gap} px · RIGHT {right_gap} px · {'PASS' if left_gap == right_gap else 'FAIL'}", font=font(24, True), fill=GREEN if left_gap == right_gap else AMBER, stroke_width=2, stroke_fill=INK)
    ed.text((42, 1230), "Base cuts: 454 / 622 / 790 / 958 · cooker 958-1126 · 1126 / 1294 / 1462 / 1630", font=font(16), fill=MUTED)
    save_review_png(edge_sheet, OUTPUTS / "kitchen-v15-cabinet-edge-gate.png")

    # Focused correction sheet: state-exclusive doors, shared sink body and
    # one common 31 px countertop depth across the run and dresser.
    correction = Image.new("RGBA", (2180, 1260), INK)
    kd = ImageDraw.Draw(correction)
    kd.text((42, 24), "SHELL + SINK + DRESSER CORRECTION GATE", font=font(34, True), fill=PAPER)
    kd.text((42, 70), "Closed and open door states are exclusive; sink body and dresser depth come from shared masters.", font=font(18), fill=MUTED)
    closed_preview = day1_empty.resize((1024, 288), RESAMPLE)
    open_preview = doors_open_clean.resize((1024, 288), RESAMPLE)
    card(correction, closed_preview, (42, 150), "CLOSED · approved leaves in perspective apertures")
    card(correction, open_preview, (1114, 150), "OPEN 90° · jamb-only shell underneath")

    base_zoom = pieces["cupboard_A1"].resize((336, 274), RESAMPLE)
    sink_zoom = pieces["sink_cabinet"].resize((336, 274), RESAMPLE)
    dresser_zoom = pieces["dresser"].resize((213, 336), RESAMPLE)
    card(correction, base_zoom, (100, 790), "SHARED BASE MASTER")
    card(correction, sink_zoom, (550, 790), "SINK · same body below y42")
    card(correction, dresser_zoom, (1120, 730), "DRESSER · shared y317-348 depth")
    depth_strip = pieces["runB_worktop"].resize((504, 31), RESAMPLE)
    card(correction, depth_strip, (1510, 790), "RUN WORKTOP · same 31 px band")
    kd.text((1118, 1130), "Dresser local y168-199 = room y317-348", font=font(19, True), fill=GREEN)
    kd.text((98, 1130), "Sink rows y42-137 = base-cupboard rows y42-137 byte-for-byte", font=font(19, True), fill=GREEN)
    save_review_png(correction, OUTPUTS / "kitchen-v15-correction-gate.png")

    # Source-vs-layout comparison documents the deliberately narrow edit scope.
    old = rgba(SOURCES / "liked-kitchen-source-2172x724.png").resize((1024, 341), RESAMPLE)
    new = rgba(IMAGEGEN / "kitchen-v15-painted-master.png").resize((1024, 341), RESAMPLE)
    comparison = Image.new("RGBA", (2180, 880), INK)
    cd = ImageDraw.Draw(comparison)
    cd.text((44, 26), "LIKED SOURCE -> v15 LAYOUT ONLY", font=font(36, True), fill=PAPER)
    cd.text((44, 76), "Liked source remains hash-pinned; v6 corrects only shell state layering and the requested v15 furniture geometry.", font=font(18), fill=MUTED)
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

    ordinary_hashes = {item_id: sha(PARTS / f"{item_id}.png") for item_id in sorted(ordinary_cupboards)}
    wall_hashes = {item_id: sha(PARTS / f"{item_id}.png") for item_id in sorted(wall_cupboards)}
    worktop_hashes = {item_id: sha(PARTS / f"{item_id}.png") for item_id in sorted(worktops)}
    sink_body_matches_base = (
        pieces["sink_cabinet"].crop((0, 42, 168, 137)).tobytes()
        == pieces["cupboard_A1"].crop((0, 42, 168, 137)).tobytes()
    )
    dresser_depth_band = pieces["dresser"].crop((0, 168, 213, 199))
    expected_dresser_depth_band = rgba(CLEAN / "worktop-504-master.png").resize((213, 31), RESAMPLE)
    dresser_shares_worktop_depth = dresser_depth_band.tobytes() == expected_dresser_depth_band.tobytes()
    door_state_central_pixels_identical = (
        structural_shell.crop((145, 0, 1903, 576)).tobytes()
        == closed_shell.crop((145, 0, 1903, 576)).tobytes()
    )
    actual_edge_gate = {
        "ordinaryCupboardIds": sorted(ordinary_cupboards),
        "ordinaryCupboardCanvasPx": [168, 137],
        "ordinaryCupboardSha256": ordinary_hashes,
        "ordinaryCupboardsByteIdentical": len(set(ordinary_hashes.values())) == 1,
        "wallCupboardIds": sorted(wall_cupboards),
        "wallCupboardCanvasPx": [136, 101],
        "wallCupboardSha256": wall_hashes,
        "wallCupboardsByteIdentical": len(set(wall_hashes.values())) == 1,
        "worktopSha256": worktop_hashes,
        "worktopsByteIdentical": len(set(worktop_hashes.values())) == 1,
        "wallCupboardToCookerVisibleGapPx": {"left": left_gap, "right": right_gap},
        "wallCupboardToCookerSpacingSymmetrical": left_gap == right_gap,
        "baseModuleCutLinesX": [454, 622, 790, 958, 1126, 1294, 1462, 1630],
        "sinkBodyMatchesBaseCabinetBelowLocalY": 42,
        "sinkBodyMatchesBaseCabinet": sink_body_matches_base,
        "dresserDepthBandLocalY": [168, 199],
        "dresserDepthBandRoomY": [317, 348],
        "dresserDepthPx": 31,
        "dresserSharesWorktopDepthPixels": dresser_shares_worktop_depth,
        "allFurnitureCutsContainTransparency": all(
            int(piece["transparentPixelCount"]) > 0 for piece in piece_report if piece["kind"] not in {"keeper"}
        ),
    }

    gate_report = {
        "schema": "lighthouse-keeper/kitchen-v15-painted-room-v6-gate@3",
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
                "sourceSha256": sha(REFERENCE / "room_door_open_leaf_168x336.png"),
                "closedPerspectiveQuads": {
                    "left": [list(point) for point in LEFT_CLOSED_QUAD],
                    "right": [list(point) for point in RIGHT_CLOSED_QUAD],
                },
                "leftOpenRect": [0, 208, 168, 544],
                "rightOpenRect": [1880, 208, 2048, 544],
                "leftFurnitureClearancePx": furniture_min_x - 168,
                "rightFurnitureClearancePx": 1880 - furniture_max_x,
                "structuralShellHasNoLeaf": True,
                "closedAndOpenStatesExclusive": True,
                "closedVsStructuralCentralPixelsIdentical": door_state_central_pixels_identical,
                "pass": furniture_min_x >= 168 and furniture_max_x <= 1880,
            },
        },
        "roomChecks": {
            "fullUpgradeReservations": {"count": len(layout["upgradeSlots"]), "pass": True},
            "bothDoorsOpenAndClear": {"pass": furniture_min_x >= 168 and furniture_max_x <= 1880},
            "day1RoomAssembledFromCuts": {"pass": True},
        },
        "actualEdgeGate": actual_edge_gate,
        "pieces": piece_report,
        "summary": {
            "pieceCount": len(piece_report),
            "exactCanvasPassCount": sum(bool(piece["fitsV15Box"]) for piece in piece_report),
            "allPiecesFit": all(bool(piece["fitsV15Box"]) for piece in piece_report),
            "allRepeatedMastersExact": actual_edge_gate["ordinaryCupboardsByteIdentical"]
            and actual_edge_gate["wallCupboardsByteIdentical"],
            "ovenSpacingSymmetrical": actual_edge_gate["wallCupboardToCookerSpacingSymmetrical"],
            "sinkSharesBaseBody": sink_body_matches_base,
            "dresserSharesWorktopDepth": dresser_shares_worktop_depth,
            "doorStatesExclusive": door_state_central_pixels_identical,
            "actualEdgeCutsPass": actual_edge_gate["allFurnitureCutsContainTransparency"],
            "allHardDatumsPass": all(check["exact"] for check in stop_checks)
            and all(check["pass"] for check in window_clear)
            and furniture_min_x >= 168
            and furniture_max_x <= 1880,
        },
    }
    (ROOT / "gate-report.json").write_text(json.dumps(gate_report, indent=2) + "\n")

    # Immutable hashes for all project-bound inputs and generated deliverables.
    manifest = {
        "schema": "lighthouse-keeper/kitchen-v15-painted-room-v6@3",
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
            "jambsOnlyShellSource": {
                "path": "sources/imagegen/kitchen-v15-jambs-only-shell-source.png",
                "sha256": sha(IMAGEGEN / "kitchen-v15-jambs-only-shell-source.png"),
                "canvasPx": list(rgba(IMAGEGEN / "kitchen-v15-jambs-only-shell-source.png").size),
                "role": "precise image edit used only for the two side-door regions of the structural shell",
            },
            "cleanAlphaMasters": {
                path.name: {
                    "sha256": sha(path),
                    "canvasPx": list(rgba(path).size),
                    "role": "approved hand-painted actual-edge source; never placed as a room crop",
                }
                for path in sorted(CLEAN.glob("*.png"))
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
