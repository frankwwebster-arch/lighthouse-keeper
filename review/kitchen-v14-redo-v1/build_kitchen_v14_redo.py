#!/usr/bin/env python3
"""Assemble the Kitchen v14 redo from painted raster sources only.

Code in this file is deliberately limited to cropping, uniform scaling,
padding, placement, masking/alpha, assembly and review-sheet annotation.
It does not draw any room or item artwork.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources" / "imagegen"
REF = ROOT / "sources" / "reference"
PARTS = ROOT / "parts"
STATES = ROOT / "states"
OUT = ROOT / "outputs"
SCHEMATIC = json.loads((REF / "kitchen_v14_schematic.json").read_text())
ITEMS = {item["id"]: item for item in SCHEMATIC["items"]}
RESAMPLE = Image.Resampling.LANCZOS
INK = (24, 35, 42, 255)
PAPER = (245, 240, 221, 255)
MUTED = (171, 191, 194, 255)
GOLD = (220, 164, 66, 255)


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def alpha_bbox(im: Image.Image) -> tuple[int, int, int, int]:
    alpha = im.getchannel("A")
    bbox = alpha.point(lambda p: 255 if p >= 8 else 0).getbbox()
    if not bbox:
        raise ValueError("empty alpha")
    return bbox


def fit_cover(im: Image.Image, size: tuple[int, int], margin: int = 3) -> Image.Image:
    """Trim transparency, uniformly scale, centre-crop overflow, then pad."""
    im = im.crop(alpha_bbox(im))
    iw, ih = im.size
    tw, th = size
    inner_w = max(1, tw - 2 * margin)
    inner_h = max(1, th - 2 * margin)
    scale = max(inner_w / iw, inner_h / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    im = im.resize((nw, nh), RESAMPLE)
    left = max(0, (nw - inner_w) // 2)
    top = max(0, (nh - inner_h) // 2)
    im = im.crop((left, top, left + inner_w, top + inner_h))
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(im, (margin, margin))
    return canvas


def fit_contain(im: Image.Image, size: tuple[int, int], margin: int = 0) -> Image.Image:
    im = im.crop(alpha_bbox(im))
    iw, ih = im.size
    tw, th = size
    scale = min((tw - 2 * margin) / iw, (th - 2 * margin) / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    im = im.resize((nw, nh), RESAMPLE)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(im, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def save(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    im = Image.new("RGBA", size, (228, 226, 216, 255))
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(204, 207, 202, 255))
    return im


def build_parts() -> dict[str, Image.Image]:
    shell = rgba(REF / "kitchen-v8-room-shell-empty-1x.png")
    sources = {
        "base": rgba(SRC / "base-cupboard-v14.png"),
        "sink": rgba(SRC / "sink-cabinet-v14.png"),
        "fridge_body": rgba(SRC / "fridge-body-open-v14.png"),
        "fridge_door": rgba(SRC / "fridge-door-v14.png"),
        "cooker_body": rgba(SRC / "cooker-body-open-v14.png"),
        "cooker_door": rgba(SRC / "cooker-door-v14.png"),
        "larder_body": rgba(SRC / "larder-body-open-v14.png"),
        "larder_door": rgba(SRC / "larder-door-v14.png"),
        "dresser": rgba(SRC / "dresser-v14.png"),
        "wall": rgba(SRC / "wall-cupboard-v14.png"),
        "teapot": rgba(SRC / "teapot-v14.png"),
        "toaster": rgba(SRC / "toaster-v14.png"),
        "mixer": rgba(SRC / "mixer-v14.png"),
        "clock": rgba(SRC / "clock-v14.png"),
        "calendar": rgba(SRC / "calendar-v14.png"),
    }

    parts: dict[str, Image.Image] = {}
    for item_id in ("back_wall", "floor_band", "window_L", "window_R"):
        x0, y0, x1, y1 = ITEMS[item_id]["rect"]
        parts[item_id] = shell.crop((x0, y0, x1, y1))

    parts["clock"] = fit_cover(sources["clock"], (60, 60), 2)
    parts["calendar"] = fit_cover(sources["calendar"], (60, 70), 2)
    base = fit_cover(sources["base"], (168, 137), 3)
    for item_id in ("cupboard_A1", "dw_slot_cupboard", "cupboard_B1", "cupboard_B2"):
        parts[item_id] = base.copy()
    parts["sink_cabinet"] = fit_cover(sources["sink"], (168, 137), 3)
    wall = fit_cover(sources["wall"], (136, 101), 3)
    parts["wall_cupboard_1"] = wall.copy()
    parts["wall_cupboard_2"] = wall.copy()

    # The selected generator output is stored as an exact 2x authoring master.
    work_src = rgba(SRC / "worktop-v14.png")
    parts["runA_worktop"] = fit_cover(work_src, (504, 31), 1)
    parts["runB_worktop"] = fit_cover(work_src, (336, 31), 1)
    parts["runB_endcap_R"] = parts["runA_worktop"].crop((492, 0, 504, 31))

    fridge_body = fit_cover(sources["fridge_body"], (168, 302), 3)
    fridge_door_local = fit_cover(sources["fridge_door"], (150, 270), 2)
    fridge_door = Image.new("RGBA", (168, 302), (0, 0, 0, 0))
    fridge_door.alpha_composite(fridge_door_local, (9, 20))
    fridge = fridge_body.copy()
    fridge.alpha_composite(fridge_door)
    parts["fridge_t1"] = fridge

    cooker_body = fit_cover(sources["cooker_body"], (168, 336), 3)
    cooker_door_local = fit_cover(sources["cooker_door"], (150, 82), 2)
    # Preserve generated glass artwork while making the dark pane transmissive.
    data = list(cooker_door_local.get_flattened_data())
    cooker_door_local.putdata([
        (r, g, b, min(a, 170)) if a and b > r * 0.9 and b > g * 0.9 and r < 90 else (r, g, b, a)
        for r, g, b, a in data
    ])
    cooker_door = Image.new("RGBA", (168, 336), (0, 0, 0, 0))
    cooker_door.alpha_composite(cooker_door_local, (9, 238))
    cooker = cooker_body.copy()
    cooker.alpha_composite(cooker_door)
    parts["cooker_t1"] = cooker

    larder_body = fit_cover(sources["larder_body"], (170, 319), 3)
    larder_door_local = fit_cover(sources["larder_door"], (154, 286), 2)
    larder_door = Image.new("RGBA", (170, 319), (0, 0, 0, 0))
    larder_door.alpha_composite(larder_door_local, (8, 18))
    larder = larder_body.copy()
    larder.alpha_composite(larder_door)
    parts["larder"] = larder

    parts["dresser"] = fit_cover(sources["dresser"], (213, 336), 3)
    parts["teapot"] = fit_cover(sources["teapot"], (44, 36), 2)
    parts["toaster"] = fit_cover(sources["toaster"], (52, 34), 2)
    parts["mixer"] = fit_cover(sources["mixer"], (64, 59), 2)

    keeper = rgba(REF / "keeper-prime-2x.png").crop((77, 18, 179, 316))
    parts["prime_keeper"] = fit_contain(keeper, (120, 298), 0)

    for item_id, im in parts.items():
        save(im, PARTS / f"{item_id}.png")

    save(fridge_body, STATES / "fridge_body_open.png")
    save(fridge_door, STATES / "fridge_door.png")
    save(cooker_body, STATES / "cooker_body_open.png")
    save(cooker_door, STATES / "cooker_door.png")
    save(larder_body, STATES / "larder_body_open.png")
    save(larder_door, STATES / "larder_door.png")
    save(fit_contain(rgba(SRC / "contents-cooking-v14.png"), (80, 38), 1), STATES / "contents_cooking.png")
    save(fit_contain(rgba(SRC / "contents-burnt-v14.png"), (80, 38), 1), STATES / "contents_burnt.png")
    return parts


def paste_rect(room: Image.Image, part: Image.Image, rect: list[int]) -> None:
    x0, y0, x1, y1 = rect
    if part.size != (x1 - x0, y1 - y0):
        raise AssertionError((part.size, rect))
    room.alpha_composite(part, (x0, y0))


def assemble_room(parts: dict[str, Image.Image]) -> Image.Image:
    room = rgba(REF / "kitchen-v8-room-shell-empty-1x.png")
    order = [
        "clock", "calendar", "wall_cupboard_1", "wall_cupboard_2",
        "cupboard_A1", "sink_cabinet", "dw_slot_cupboard",
        "cupboard_B1", "cupboard_B2", "runA_worktop", "runB_worktop",
        "runB_endcap_R", "fridge_t1", "cooker_t1", "dresser", "larder",
        "teapot", "toaster", "mixer", "prime_keeper",
    ]
    for item_id in order:
        paste_rect(room, parts[item_id], ITEMS[item_id]["rect"])
    return room


def card(sheet: Image.Image, image: Image.Image, xy: tuple[int, int], title: str, subtitle: str = "") -> None:
    x, y = xy
    d = ImageDraw.Draw(sheet)
    d.rounded_rectangle((x - 10, y - 48, x + image.width + 10, y + image.height + 42), radius=10, fill=(33, 46, 55, 255), outline=(87, 108, 113, 255), width=2)
    sheet.alpha_composite(image, (x, y))
    d.text((x, y - 38), title, font=font(22, True), fill=PAPER)
    if subtitle:
        d.text((x, y + image.height + 10), subtitle, font=font(16), fill=MUTED)


def build_two_scale(room: Image.Image) -> Image.Image:
    sheet = Image.new("RGBA", (2300, 980), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((44, 28), "KITCHEN v14 REDO · TWO VIEWING SCALES", font=font(36, True), fill=PAPER)
    d.text((44, 76), "Painted-image sources only · exact schematic assembly · review candidate", font=font(20), fill=MUTED)
    card(sheet, room, (120, 160), "ROOM VIEW · exact 1:1 · 2048 × 576")
    small = room.resize((256, 72), RESAMPLE)
    card(sheet, small, (1022, 830), "LIGHTHOUSE VIEW · exact 12.5% · 256 × 72", "Fine panels vanish by design; cream appliances, duck-egg runs and copper accents still read.")
    return sheet


def build_comparison(room: Image.Image) -> Image.Image:
    v8_room = rgba(REF / "kitchen-v8-room-furnished-1x.png")
    v8_assets = rgba(REF / "kitchen-v8-complete-day1-assets-1x.png")
    sheet = Image.new("RGBA", (4300, 1900), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((46, 26), "KITCHEN v14 REDO · REQUIRED v8 COMPARISON", font=font(38, True), fill=PAPER)
    d.text((46, 78), "New room and approved v8 room proof are shown at the same exact 1:1 scale.", font=font(21), fill=MUTED)
    card(sheet, room, (70, 160), "NEW v14 REDO · painted assets · exact 1:1")
    card(sheet, v8_room, (2180, 160), "APPROVED v8 ROOM PROOF · exact 1:1")
    v8_scaled = v8_assets.resize((2300, 1050), RESAMPLE)
    card(sheet, v8_scaled, (70, 870), "APPROVED v8 PIECES · exact 1:1 lineup reference")
    mini = room.resize((256, 72), RESAMPLE)
    card(sheet, mini, (3030, 1030), "NEW v14 · LIGHTHOUSE VIEW · 12.5%", "Readable: cream fridge/cooker, duck-egg cabinet run, dresser and larder. Fine handles and panels intentionally disappear.")
    return sheet


def build_contact(parts: dict[str, Image.Image]) -> Image.Image:
    ids = [i["id"] for i in SCHEMATIC["items"]]
    cols, cell_w, cell_h = 5, 390, 410
    rows = (len(ids) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w + 60, rows * cell_h + 130), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 24), "KITCHEN v14 REDO · EXACT-CANVAS CONTACT SHEET", font=font(34, True), fill=PAPER)
    d.text((30, 70), "All visible item art is painted; code only registers and assembles.", font=font(18), fill=MUTED)
    for idx, item_id in enumerate(ids):
        im = parts[item_id]
        col, row = idx % cols, idx // cols
        x, y = 30 + col * cell_w, 110 + row * cell_h
        d.rounded_rectangle((x, y, x + cell_w - 20, y + cell_h - 18), radius=12, fill=(33, 46, 55, 255), outline=(87, 108, 113, 255), width=2)
        max_w, max_h = cell_w - 56, cell_h - 110
        scale = min(max_w / im.width, max_h / im.height, 1.5)
        preview = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), RESAMPLE)
        bg = checker(preview.size)
        bg.alpha_composite(preview)
        sheet.alpha_composite(bg, (x + (cell_w - 20 - preview.width) // 2, y + 48))
        d.text((x + 14, y + 12), item_id, font=font(19, True), fill=PAPER)
        d.text((x + 14, y + cell_h - 54), f"PASS · exact {im.width} × {im.height} px", font=font(16), fill=GOLD)
    return sheet


def rotate_layer(layer: Image.Image, angle: float, hinge: tuple[int, int]) -> Image.Image:
    # Rotation is a review-only moving-part demonstration.
    bbox = alpha_bbox(layer)
    part = layer.crop(bbox)
    rotated = part.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    canvas = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    x = max(0, min(layer.width - rotated.width, hinge[0] - rotated.width // 2))
    y = max(0, min(layer.height - rotated.height, hinge[1] - rotated.height // 2))
    canvas.alpha_composite(rotated, (x, y))
    return canvas


def demo_panel(body: Image.Image, door: Image.Image, mode: str, contents: Image.Image | None = None) -> Image.Image:
    panel = body.copy()
    if mode != "open" and contents is not None:
        panel.alpha_composite(contents, ((panel.width - contents.width) // 2, int(panel.height * 0.72)))
    if mode == "closed":
        panel.alpha_composite(door)
    elif mode == "askew":
        panel.alpha_composite(rotate_layer(door, -18, (panel.width // 2, panel.height - 8)))
    return panel


def build_demos() -> Image.Image:
    sheet = Image.new("RGBA", (3260, 980), (17, 27, 34, 255))
    d = ImageDraw.Draw(sheet)
    d.text((40, 24), "KITCHEN v14 REDO · DOOR / LIGHT / CONTENTS CONTRACT", font=font(34, True), fill=PAPER)
    d.text((40, 68), "One fixed body + one moving door; engine light sits behind glass; food is a separate sprite.", font=font(18), fill=MUTED)
    groups = [
        ("FRIDGE", rgba(STATES / "fridge_body_open.png"), rgba(STATES / "fridge_door.png"), None),
        ("COOKER", rgba(STATES / "cooker_body_open.png"), rgba(STATES / "cooker_door.png"), fit_contain(rgba(STATES / "contents_cooking.png"), (80, 38))),
        ("LARDER", rgba(STATES / "larder_body_open.png"), rgba(STATES / "larder_door.png"), None),
    ]
    x = 44
    for name, body, door, contents in groups:
        for j, mode in enumerate(("closed", "open", "askew")):
            im = demo_panel(body, door, mode, contents)
            scale = min(250 / im.width, 590 / im.height)
            im = im.resize((round(im.width * scale), round(im.height * scale)), RESAMPLE)
            card(sheet, im, (x, 170), f"{name} · {mode.upper()}")
            x += im.width + 38
        x += 30
    d.text((44, 900), "Review-only poses: fixed body pixels do not change. Askew uses only transform of the same door sprite.", font=font(18), fill=MUTED)
    return sheet


def build_manifest(parts: dict[str, Image.Image]) -> None:
    manifest = {
        "schema": "lighthouse-keeper/kitchen-v14-redo-review@1",
        "status": "review-candidate-awaiting-frank",
        "runtimeMutation": False,
        "rejectedV14ArtworkReused": False,
        "modulePx": SCHEMATIC["module"],
        "walkYPx": 502,
        "twoViewingScales": {"room": [2048, 576], "lighthouse": [256, 72]},
        "paintMethod": "OpenAI built-in image generation; code limited to crop/uniform-scale/pad/place/mask/assemble/verify",
        "approvedShellReuse": "sources/reference/kitchen-v8-room-shell-empty-1x.png",
        "parts": {},
        "states": {},
    }
    for item_id, im in parts.items():
        path = PARTS / f"{item_id}.png"
        manifest["parts"][item_id] = {
            "canvasPx": list(im.size),
            "rectPx": ITEMS[item_id]["rect"],
            "sha256": sha(path),
        }
    for path in sorted(STATES.glob("*.png")):
        manifest["states"][path.name] = {"canvasPx": list(rgba(path).size), "sha256": sha(path)}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    for directory in (PARTS, STATES, OUT):
        directory.mkdir(parents=True, exist_ok=True)
    parts = build_parts()
    room = assemble_room(parts)
    save(room, OUT / "kitchen-v14-redo-assembled-room-1x.png")
    save(rgba(REF / "kitchen-v8-room-shell-empty-1x.png"), OUT / "kitchen-v14-redo-shell-empty-1x.png")
    save(build_two_scale(room), OUT / "kitchen-v14-redo-two-viewing-scales.png")
    save(build_comparison(room), OUT / "kitchen-v14-redo-v8-comparison.png")
    save(build_contact(parts), OUT / "kitchen-v14-redo-contact-sheet.png")
    save(build_demos(), OUT / "kitchen-v14-redo-door-light-contents-demos.png")
    build_manifest(parts)


if __name__ == "__main__":
    main()
