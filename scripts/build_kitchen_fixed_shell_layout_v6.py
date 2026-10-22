#!/usr/bin/env python3
"""Build Kitchen Fixed Shell Layout V6 from approved raster authorities.

This builder deliberately does not redraw the kitchen.  It separates the
approved fitted-unit pixels into a fixed, continuous carcass/worktop and
movable functional inserts.  The split is deterministic and reversible.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-fixed-shell-2026-10-23-v6"
OUT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-fixed-shell-layout-v6"
TEMPLATE = ROOT / "scripts/templates/kitchen_fixed_shell_layout_v6.html"
GRID = ROOT / "data/kitchen_room_grid_contract_v2.json"
FOUNDATION = ROOT / "art/drafts/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png"
STATE_SHEET = ROOT / "art/drafts/kitchen-cabinetry-state-derivatives-2026-10-22-v1/candidate-v4-red-fault-lights-fridge-leak.png"
ROOM_SET = ROOT / "art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1"
V4 = ROOT / "art/drafts/kitchen-complete-room-layout-2026-10-22-v4"
ATLAS_NAME = "kitchen-fixed-shell-atlas-v6.png"
MASTER_BODY = (420, 370)
MASTER_RUN = (2520, 370)
GUTTER = 8

EXPECTED = {
    FOUNDATION: "898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3",
    STATE_SHEET: "d53b7565558acf6dc5544dde8b415fe50ac9eec1683eb374d996114ad5a902e8",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(image: Image.Image, body: list[int]) -> tuple[Image.Image, list[int]]:
    """Scale a review crop while retaining its declared body registration."""
    x, y, w, h = body
    sx, sy = MASTER_BODY[0] / w, MASTER_BODY[1] / h
    scaled = image.resize((round(image.width * sx), round(image.height * sy)), Image.Resampling.LANCZOS)
    return scaled, [round(x * sx), round(y * sy), *MASTER_BODY]


def alpha_masked(image: Image.Image, mask: Image.Image) -> Image.Image:
    result = image.copy()
    result.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
    return result


def fitted_insert(image: Image.Image, body: list[int], name: str) -> Image.Image:
    """Keep only functional insert pixels; discard each source's own shell."""
    bx, by, bw, bh = body
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    # The aperture is shared by every bay.  The fixed run supplies all rails,
    # plinths and countertop pixels around it.
    draw.rectangle((bx + 30, by + 54, bx + bw - 30, by + 340), fill=255)

    if name.startswith("sink"):
        # Retain the tap above the worktop and the flood below the carcass.
        draw.rectangle((bx + 92, 0, bx + 328, by + 100), fill=255)
    if name.endswith("broken"):
        # Broken doors and leaks can leave the aperture, while the fixed shell
        # will still overpaint its own rails and worktop.
        draw.rectangle((0, by + 250, image.width, image.height), fill=255)
    return alpha_masked(image, mask)


def stretch_horizontal(strip: Image.Image, width: int, left: int, right: int) -> Image.Image:
    result = Image.new("RGBA", (width, strip.height), (0, 0, 0, 0))
    result.alpha_composite(strip.crop((0, 0, left, strip.height)), (0, 0))
    middle = strip.crop((left, 0, strip.width - right, strip.height)).resize(
        (width - left - right, strip.height), Image.Resampling.LANCZOS
    )
    result.alpha_composite(middle, (left, 0))
    result.alpha_composite(strip.crop((strip.width - right, 0, strip.width, strip.height)), (width - right, 0))
    return result


def build_fixed_layers(cupboard: Image.Image, body: list[int]) -> tuple[Image.Image, Image.Image, Image.Image]:
    bx, by, bw, bh = body
    unit = cupboard.crop((bx, by, bx + bw, by + bh))

    # One worktop, with one pair of end caps.  There are no internal end bevels.
    worktop = stretch_horizontal(unit.crop((0, 0, bw, 70)), MASTER_RUN[0], 36, 36)

    # One carcass run.  The plinth is continuous; each internal divider is the
    # exact same mirrored approved rail sample, not two overlapping unit ends.
    backing = Image.new("RGBA", MASTER_RUN, (7, 87, 161, 255))
    carcass = Image.new("RGBA", MASTER_RUN, (0, 0, 0, 0))
    plinth = stretch_horizontal(unit.crop((0, 338, bw, bh)), MASTER_RUN[0], 30, 30)
    carcass.alpha_composite(plinth, (0, 338))

    rail_half = unit.crop((13, 67, 25, 338))
    divider = Image.new("RGBA", (24, rail_half.height), (0, 0, 0, 0))
    divider.alpha_composite(rail_half.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (0, 0))
    divider.alpha_composite(rail_half, (12, 0))
    for edge in range(0, MASTER_RUN[0] + 1, MASTER_BODY[0]):
        x = max(0, min(MASTER_RUN[0] - divider.width, edge - divider.width // 2))
        carcass.alpha_composite(divider, (x, 67))
    return backing, carcass, worktop


def hob_overlay(oven: Image.Image, body: list[int]) -> Image.Image:
    """Extract only burners and orange control from the approved oven top."""
    bx, by, bw, _ = body
    crop = oven.crop((bx, by, bx + bw, by + 72)).convert("RGBA")
    rgb = crop.convert("RGB")
    seed = Image.new("L", crop.size, 0)
    out = seed.load()
    pix = rgb.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b = pix[x, y]
            dark_burner = max(r, g, b) < 130 and abs(r - g) < 38
            orange_control = r > 135 and r > g * 1.18 and b < 100
            if dark_burner or orange_control:
                out[x, y] = 255
    mask = seed.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.45))
    return alpha_masked(crop, mask)


def sink_overlay(sink: Image.Image, body: list[int]) -> Image.Image:
    """Keep the registered basin lip, tap and state water above the worktop."""
    bx, by, bw, _ = body
    rgb = sink.convert("RGB")
    seed = Image.new("L", sink.size, 0)
    out, pix = seed.load(), rgb.load()
    x0, x1 = bx + 58, bx + bw - 58
    y1 = by + 42
    for y in range(max(0, by - 180), min(sink.height, y1)):
        for x in range(max(0, x0), min(sink.width, x1)):
            r, g, b = pix[x, y]
            cream = r > 145 and g > 115 and b > 72 and not (g > r * 1.18 and b > r * 1.18)
            orange = r > 135 and r > g * 1.16 and b < 115
            water = b > 135 and b > r * 1.18 and b > g * 1.03
            outline = max(r, g, b) < 82
            if cream or orange or water or outline:
                out[x, y] = 255
    mask = seed.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.4))
    return alpha_masked(sink, mask)


def build_dishwasher_off(on_image: Image.Image, body: list[int]) -> Image.Image:
    """Create the missing dark-lamp state without moving the approved controls."""
    result = on_image.copy()
    bx, by, _, _ = body
    draw = ImageDraw.Draw(result)
    # Coordinates are in the normalized approved control panel.  All three
    # lamp centres are invariant across Off, On and Broken.
    for cx in (82, 119, 156):
        draw.ellipse((bx + cx - 9, by + 70 - 9, bx + cx + 9, by + 70 + 9), fill=(38, 43, 43, 255), outline=(4, 13, 18, 255), width=4)
        draw.ellipse((bx + cx - 4, by + 66 - 4, bx + cx + 2, by + 72), fill=(111, 119, 115, 255))
    return result


def main() -> None:
    for path, digest in EXPECTED.items():
        assert sha256(path) == digest, f"approved authority changed: {path}"

    room_manifest = json.loads((ROOM_SET / "manifest.json").read_text())
    v4 = json.loads((V4 / "manifest.json").read_text())
    grid = json.loads(GRID.read_text())
    assets: dict[str, tuple[Image.Image, dict]] = {}
    normalized_sources: dict[str, tuple[Image.Image, list[int]]] = {}

    for name, record in room_manifest["assets"].items():
        source = Image.open(ROOM_SET / "assets" / record["file"]).convert("RGBA")
        normalized, body = normalize(source, record["bodyRect"])
        normalized_sources[name] = (normalized, body)
        assets[name] = (
            fitted_insert(normalized, body, name),
            {"bodyRect": body, "logicalBody": [84, 74], "authority": record["authority"]},
        )

    dishwasher_on, dishwasher_body = assets["dishwasher-on"]
    # Off is derived before the shell mask is applied so the same registered
    # lamp centres are guaranteed.  Re-normalize the approved On crop.
    record = room_manifest["assets"]["dishwasher-on"]
    raw_on, raw_body = normalize(Image.open(ROOM_SET / "assets" / record["file"]).convert("RGBA"), record["bodyRect"])
    off = fitted_insert(build_dishwasher_off(raw_on, raw_body), raw_body, "dishwasher-off")
    assets["dishwasher-off"] = (off, {"bodyRect": raw_body, "logicalBody": [84, 74], "authority": "deterministic dark-lamp derivative of approved dishwasher On"})

    cupboard_raw, cupboard_body = normalize(
        Image.open(ROOM_SET / "assets" / room_manifest["assets"]["cupboard"]["file"]).convert("RGBA"),
        room_manifest["assets"]["cupboard"]["bodyRect"],
    )
    backing, carcass, worktop = build_fixed_layers(cupboard_raw, cupboard_body)
    oven_raw, oven_body = normalize(
        Image.open(ROOM_SET / "assets" / room_manifest["assets"]["oven"]["file"]).convert("RGBA"),
        room_manifest["assets"]["oven"]["bodyRect"],
    )
    hob = hob_overlay(oven_raw, oven_body)
    sink_overlays = {
        name: sink_overlay(*normalized_sources[name])
        for name in ("sink", "sink-on", "sink-broken")
    }

    v4_atlas = Image.open(V4 / "assets" / v4["atlas"]["file"]).convert("RGBA")
    loose: dict[str, tuple[Image.Image, dict]] = {}
    for name, record in v4["looseAssets"].items():
        x, y, w, h = record["atlasRect"]
        image = v4_atlas.crop((x, y, x + w, y + h))
        loose[name] = (image, {key: value for key, value in record.items() if key not in {"file", "atlasRect", "sha256"}})

    items: list[tuple[str, str, Image.Image, dict]] = [
        ("fixedLayers", "carcass-backing", backing, {"logicalSize": [504, 74], "bodyOrigin": [84, 134], "drawOrder": "before inserts"}),
        ("fixedLayers", "carcass-run", carcass, {"logicalSize": [504, 74], "bodyOrigin": [84, 134]}),
        ("fixedLayers", "worktop-run", worktop, {"logicalSize": [504, 14], "bodyOrigin": [84, 134]}),
        ("overlays", "hob", hob, {"logicalSize": [84, 14], "bodyOffset": [0, 0]}),
    ]
    for name, image in sink_overlays.items():
        body = normalized_sources[name][1]
        items.append(("overlays", name, image, {"bodyRect": body, "logicalBody": [84, 74], "role": "sink cut-in above fixed worktop"}))
    items += [("assets", name, image, record) for name, (image, record) in assets.items()]
    items += [("looseAssets", name, image, record) for name, (image, record) in loose.items()]

    width = max(image.width for _, _, image, _ in items) + GUTTER * 2
    height = sum(image.height + GUTTER for _, _, image, _ in items) + GUTTER
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sections = {"fixedLayers": {}, "overlays": {}, "assets": {}, "looseAssets": {}}
    y = GUTTER
    for section, name, image, record in items:
        atlas.alpha_composite(image, (GUTTER, y))
        sections[section][name] = {**record, "file": ATLAS_NAME, "atlasRect": [GUTTER, y, image.width, image.height]}
        y += image.height + GUTTER

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(parents=True, exist_ok=True)
    atlas_path = OUT / "assets" / ATLAS_NAME
    atlas.save(atlas_path, optimize=True)
    (PUBLIC / "assets" / ATLAS_NAME).write_bytes(atlas_path.read_bytes())

    manifest = {
        "schema": "lighthouse-keeper/kitchen-fixed-shell-layout@6",
        "set": SET,
        "status": "unapproved-fixed-shell-review",
        "visualAuthorities": {
            "foundation": {"path": str(FOUNDATION.relative_to(ROOT)), "sha256": EXPECTED[FOUNDATION], "changed": False},
            "states": {"path": str(STATE_SHEET.relative_to(ROOT)), "sha256": EXPECTED[STATE_SHEET], "changed": False},
            "firstRenderExemplar": {
                "path": "art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png",
                "sha256": "bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2",
                "changed": False,
            },
        },
        "architecture": {
            "fixed": ["one continuous worktop", "one six-bay carcass run", "one continuous plinth", "six exact grid apertures"],
            "movable": ["fronts", "doors", "contents", "indicator states", "water effects", "sink insert", "hob overlay"],
            "internalEndBevels": False,
            "healingOverlay": False,
            "sourceUnitShellPixelsExcluded": True,
        },
        "room": room_manifest["room"],
        "roomGrid": grid,
        "countertopOwnership": grid["countertopObjectOwnership"],
        "states": {
            "sink": {"off": "sink", "on": "sink-on", "broken": "sink-broken"},
            "dishwasher": {"off": "dishwasher-off", "on": "dishwasher-on", "broken": "dishwasher-broken"},
            "oven": {"off": "oven-off", "on": "oven", "broken": "oven-broken"},
            "fridge": {"standard": "fridge-standard", "broken": "fridge-broken"},
        },
        "fixedLayers": sections["fixedLayers"],
        "overlays": sections["overlays"],
        "assets": sections["assets"],
        "looseAssets": sections["looseAssets"],
        "looseGeometry": {**v4["looseGeometry"], "defaultPositions": None, "countertopPositionStorage": "supporting cabinet identity only"},
        "atlas": {"file": ATLAS_NAME, "sha256": sha256(atlas_path), "pixels": list(atlas.size), "drawingCount": len(items), "uniqueImageRequests": 1, "lossless": True},
        "boundaries": {"productionChanged": False, "runtimeChanged": False, "approvedSourceOverwritten": False, "candidateReviewOnly": True},
    }
    payload = (json.dumps(manifest, indent=2) + "\n").encode()
    (OUT / "manifest.json").write_bytes(payload)
    (PUBLIC / "manifest.json").write_bytes(payload)
    (PUBLIC / "index.html").write_text(TEMPLATE.read_text())
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "architecture": manifest["architecture"]}, indent=2))


if __name__ == "__main__":
    main()
