#!/usr/bin/env python3
"""Build reversible room-layout review crops from the approved cabinetry sheet.

The approved source is never rewritten.  Each output is a crop of that exact
source with only presentation-background alpha removed outside the declared
module silhouette.  The review renderer maps the declared body rectangle back
to the fixed 84 x 74 logical-pixel game geometry.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png"
STATE_SOURCE = ROOT / "art/drafts/kitchen-cabinetry-state-derivatives-2026-10-22-v1/candidate-v4-red-fault-lights-fridge-leak.png"
OUT = ROOT / "art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1/assets"
PUBLIC = ROOT / "public/keeper-review/kitchen-cabinetry-room-layout-v1/assets"
SOURCE_SHA256 = "898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3"
STATE_SOURCE_SHA256 = "d53b7565558acf6dc5544dde8b415fe50ac9eec1683eb374d996114ad5a902e8"


MODULES = {
    "cupboard": {
        "crop": [64, 135, 503, 528],
        "body": [75, 151, 491, 520],
        "polygon": [(75, 180), (99, 151), (462, 151), (491, 180), (491, 202), (480, 210), (480, 481), (472, 489), (472, 520), (91, 520), (91, 489), (84, 481), (84, 210), (75, 202)],
    },
    "drawers": {
        "crop": [552, 135, 984, 528],
        "body": [564, 151, 972, 520],
        "polygon": [(564, 180), (590, 151), (944, 151), (972, 180), (972, 202), (962, 210), (962, 481), (954, 489), (954, 520), (581, 520), (581, 489), (574, 481), (574, 210), (564, 202)],
    },
    "sink": {
        "crop": [1034, 15, 1471, 528],
        "body": [1044, 151, 1460, 520],
        "polygon": [(1044, 180), (1071, 151), (1433, 151), (1460, 180), (1460, 202), (1450, 210), (1450, 481), (1442, 489), (1442, 520), (1061, 520), (1061, 489), (1054, 481), (1054, 210), (1044, 202)],
        "tapRegion": [1164, 20, 1338, 174],
    },
    "dishwasher": {
        "crop": [64, 548, 503, 968],
        "body": [75, 570, 493, 959],
        "polygon": [(75, 599), (99, 570), (463, 570), (493, 599), (493, 622), (482, 630), (482, 919), (474, 928), (474, 959), (91, 959), (91, 928), (84, 919), (84, 630), (75, 622)],
    },
    "oven": {
        "crop": [542, 540, 994, 968],
        "body": [555, 563, 983, 959],
        "polygon": [(555, 592), (581, 563), (952, 563), (983, 592), (983, 618), (973, 626), (973, 919), (965, 928), (965, 959), (570, 959), (570, 928), (563, 919), (563, 626), (555, 618)],
    },
    "fridge": {
        "crop": [1034, 548, 1471, 968],
        "body": [1044, 570, 1460, 959],
        "polygon": [(1044, 599), (1071, 570), (1433, 570), (1460, 599), (1460, 622), (1450, 630), (1450, 919), (1442, 928), (1442, 959), (1061, 959), (1061, 928), (1054, 919), (1054, 630), (1044, 622)],
    },
}


STATE_MODULES = {
    "sink-on": {
        "crop": [105, 0, 474, 383],
        "body": [116, 102, 461, 372],
        "polygon": [(116, 123), (139, 102), (438, 102), (461, 123), (461, 142), (453, 148), (453, 344), (447, 351), (447, 372), (129, 372), (129, 351), (123, 344), (123, 148), (116, 142)],
        "tapRegion": [230, 14, 360, 137],
    },
    "sink-broken": {
        "crop": [512, 0, 1016, 412],
        "body": [560, 102, 912, 372],
        "polygon": [(560, 123), (583, 102), (889, 102), (912, 123), (912, 142), (904, 148), (904, 344), (898, 351), (898, 372), (574, 372), (574, 351), (567, 344), (567, 148), (560, 142)],
        "tapRegion": [690, 14, 835, 137],
        "waterRegions": [[520, 323, 1005, 403]],
    },
    "dishwasher-on": {
        "crop": [106, 392, 474, 718],
        "body": [117, 403, 461, 708],
        "polygon": [(117, 423), (139, 403), (439, 403), (461, 423), (461, 443), (453, 449), (453, 680), (447, 687), (447, 708), (130, 708), (130, 687), (123, 680), (123, 449), (117, 443)],
    },
    "dishwasher-broken": {
        "crop": [504, 392, 1008, 748],
        "body": [560, 403, 912, 708],
        "polygon": [(560, 423), (582, 403), (890, 403), (912, 423), (912, 443), (904, 449), (904, 681), (898, 688), (898, 708), (574, 708), (574, 688), (567, 681), (567, 449), (560, 443)],
        "waterRegions": [[513, 671, 1000, 739]],
    },
    "oven-off": {
        "crop": [103, 741, 480, 1085],
        "body": [112, 749, 470, 1076],
        "polygon": [(112, 772), (135, 749), (447, 749), (470, 772), (470, 791), (462, 798), (462, 1048), (456, 1055), (456, 1076), (126, 1076), (126, 1055), (119, 1048), (119, 798), (112, 791)],
    },
    "oven-broken": {
        "crop": [551, 741, 976, 1085],
        "body": [560, 749, 912, 1076],
        "polygon": [(560, 772), (583, 749), (889, 749), (912, 772), (912, 791), (904, 798), (904, 1048), (898, 1055), (898, 1076), (574, 1076), (574, 1055), (567, 1048), (567, 798), (560, 791)],
    },
    "fridge-standard": {
        "crop": [103, 1099, 473, 1452],
        "body": [112, 1108, 461, 1443],
        "polygon": [(112, 1131), (135, 1108), (438, 1108), (461, 1131), (461, 1151), (453, 1157), (453, 1415), (447, 1422), (447, 1443), (126, 1443), (126, 1422), (119, 1415), (119, 1157), (112, 1151)],
    },
    "fridge-broken": {
        "crop": [551, 1099, 976, 1500],
        "body": [560, 1108, 912, 1443],
        "polygon": [(560, 1131), (583, 1108), (889, 1108), (912, 1131), (912, 1151), (904, 1157), (904, 1415), (898, 1422), (898, 1443), (574, 1443), (574, 1422), (567, 1415), (567, 1157), (560, 1151)],
        "waterRegions": [[560, 1428, 912, 1490]],
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tap_mask(source: Image.Image, region: list[int]) -> Image.Image:
    x0, y0, x1, y1 = region
    rgb = source.crop(region).convert("RGB")
    seed = Image.new("L", rgb.size, 0)
    pixels = rgb.load()
    target = seed.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = pixels[x, y]
            warm = (r > 150 and r > g * 1.08 and r > b * 1.45) or (r > 180 and g > 110 and b < 130)
            if warm:
                target[x, y] = 255
    near = seed.filter(ImageFilter.MaxFilter(11))
    result = Image.new("L", rgb.size, 0)
    out = result.load()
    near_px = near.load()
    seed_px = seed.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            if not near_px[x, y]:
                continue
            r, g, b = pixels[x, y]
            neutral_outline = max(r, g, b) < 92 and max(r, g, b) - min(r, g, b) < 30
            warm_edge = r > 135 and r > b * 1.35 and r >= g * 0.95
            if seed_px[x, y] or neutral_outline or warm_edge:
                out[x, y] = 255
    result = result.filter(ImageFilter.MaxFilter(3))
    full = Image.new("L", source.size, 0)
    full.paste(result, (x0, y0))
    return full


def water_mask(source: Image.Image, region: list[int]) -> Image.Image:
    x0, y0, x1, y1 = region
    rgb = source.crop(region).convert("RGB")
    seed = Image.new("L", rgb.size, 0)
    pixels = rgb.load()
    target = seed.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = pixels[x, y]
            water = (b > 125 and g > 80 and b > r * 1.08) or (r > 175 and g > 185 and b > 195)
            if water:
                target[x, y] = 255
    near = seed.filter(ImageFilter.MaxFilter(11))
    result = Image.new("L", rgb.size, 0)
    out = result.load()
    near_px = near.load()
    seed_px = seed.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            if not near_px[x, y]:
                continue
            r, g, b = pixels[x, y]
            dark_outline = max(r, g, b) < 95 and b >= r * 0.75
            cool_edge = b > 70 and b >= r * 1.02
            if seed_px[x, y] or dark_outline or cool_edge:
                out[x, y] = 255
    result = result.filter(ImageFilter.MaxFilter(3))
    full = Image.new("L", source.size, 0)
    full.paste(result, (x0, y0))
    return full


def isolate(source: Image.Image, spec: dict) -> tuple[Image.Image, list[int]]:
    mask = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(spec["polygon"], fill=255)
    if "tapRegion" in spec:
        mask = ImageChops.lighter(mask, tap_mask(source, spec["tapRegion"]))
    for region in spec.get("waterRegions", []):
        mask = ImageChops.lighter(mask, water_mask(source, region))
    # A tiny feather preserves antialiasing at the deliberately traced outer edge.
    mask = mask.filter(ImageFilter.GaussianBlur(0.55))
    original_alpha = source.getchannel("A")
    mask = ImageChops.darker(mask, original_alpha)
    isolated = source.copy()
    isolated.putalpha(mask)
    crop = spec["crop"]
    isolated = isolated.crop(crop)
    bx0, by0, bx1, by1 = spec["body"]
    body = [bx0 - crop[0], by0 - crop[1], bx1 - bx0, by1 - by0]
    return isolated, body


def main() -> None:
    assert sha256(SOURCE) == SOURCE_SHA256, "approved cabinetry source bytes changed"
    assert sha256(STATE_SOURCE) == STATE_SOURCE_SHA256, "approved state visual authority bytes changed"
    source = Image.open(SOURCE).convert("RGBA")
    state_source = Image.open(STATE_SOURCE).convert("RGBA")
    OUT.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    assets = {}
    for name, spec in MODULES.items():
        image, body = isolate(source, spec)
        filename = f"{name}-approved-review-crop.png"
        draft_path = OUT / filename
        public_path = PUBLIC / filename
        image.save(draft_path, optimize=True)
        public_path.write_bytes(draft_path.read_bytes())
        assets[name] = {
            "file": filename,
            "sha256": sha256(draft_path),
            "pixels": list(image.size),
            "bodyRect": body,
            "logicalBody": [84, 74],
            "sourceCrop": spec["crop"],
            "maskMethod": "declared outer silhouette; sink tap uses source-colour-connected mask",
            "authority": "approved-cabinetry-foundation",
        }
    for name, spec in STATE_MODULES.items():
        image, body = isolate(state_source, spec)
        filename = f"{name}-approved-review-crop.png"
        draft_path = OUT / filename
        public_path = PUBLIC / filename
        image.save(draft_path, optimize=True)
        public_path.write_bytes(draft_path.read_bytes())
        assets[name] = {
            "file": filename,
            "sha256": sha256(draft_path),
            "pixels": list(image.size),
            "bodyRect": body,
            "logicalBody": [84, 74],
            "sourceCrop": spec["crop"],
            "maskMethod": "declared outer silhouette with source-colour-connected tap/water mask where required",
            "authority": "approved-cabinetry-state-visual-sheet",
        }
    manifest = {
        "schema": "lighthouse-keeper/kitchen-cabinetry-room-layout@1",
        "set": "kitchen-cabinetry-room-layout-2026-10-22-v1",
        "status": "unapproved-room-layout-review",
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": SOURCE_SHA256,
            "changed": False,
        },
        "stateSource": {
            "path": str(STATE_SOURCE.relative_to(ROOT)),
            "sha256": STATE_SOURCE_SHA256,
            "changed": False,
        },
        "room": {
            "logicalPixels": [772, 224],
            "bayWidth": 84,
            "bodySize": [84, 74],
            "bodyTopY": 134,
            "bodyBaselineY": 208,
            "originsX": [84, 168, 252, 336, 420, 504],
            "defaultOrder": ["cupboard", "drawers", "sink", "dishwasher", "oven", "fridge"],
        },
        "assets": assets,
        "states": {
            "sink": {"off": "sink", "on": "sink-on", "broken": "sink-broken"},
            "dishwasher": {"on": "dishwasher-on", "broken": "dishwasher-broken", "offUnavailable": "dark-lamp production extraction is not yet authored"},
            "oven": {"on": "oven", "off": "oven-off", "broken": "oven-broken"},
            "fridge": {"standard": "fridge-standard", "broken": "fridge-broken"},
        },
        "comparison": {
            "raw": "approved review crops with no join treatment",
            "diagnostic": "same crops and positions plus narrow join-only overlay; not approved healing art",
            "bothViewsSynchronized": True,
        },
        "boundaries": {
            "productionChanged": False,
            "runtimeChanged": False,
            "approvedSourceOverwritten": False,
            "stateArtChanged": False,
            "healingApproved": False,
        },
    }
    manifest_path = OUT.parent / "manifest.json"
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    manifest_path.write_bytes(manifest_bytes)
    (PUBLIC.parent / "manifest.json").write_bytes(manifest_bytes)
    print(json.dumps({"manifest": str(manifest_path.relative_to(ROOT)), "assets": assets}, indent=2))


if __name__ == "__main__":
    main()
