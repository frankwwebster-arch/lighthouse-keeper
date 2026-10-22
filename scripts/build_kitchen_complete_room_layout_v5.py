#!/usr/bin/env python3
"""Build the reversible Kitchen Complete Room Layout V5 review.

V5 replaces V4's incompatible legacy healing strips with one normalized,
high-resolution countertop interface family.  It keeps the approved V1/V4
authorities immutable, retains rejected generated attempts, and changes
countertop loose objects from slot ownership to supporting-unit ownership.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-countertop-interface-2026-10-22-v5"
OUT = ROOT / "art/drafts" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-complete-room-layout-v5"
FOUNDATION = OUT / "source/cabinetry-foundation-interface-hob-sink-corrected.png"
STATES = OUT / "source/cabinetry-states-interface-hob-sink-corrected.png"
REJECTED_FOUNDATION = OUT / "source/cabinetry-foundation-interface-candidate.png"
REJECTED_STATES = OUT / "source/cabinetry-states-interface-candidate.png"
SUPERSEDED_FOUNDATION = OUT / "source/cabinetry-foundation-interface-hob-corrected.png"
SUPERSEDED_STATES = OUT / "source/cabinetry-states-interface-hob-corrected.png"
V4 = ROOT / "art/drafts/kitchen-complete-room-layout-2026-10-22-v4"
V4_MANIFEST_SHA256 = "6340d9cddddabd430872af08dd2b6672b38f08cd2cedad4256016512f164c4f6"
GRID = ROOT / "data/kitchen_room_grid_contract_v2.json"
TEMPLATE = ROOT / "scripts/templates/kitchen_complete_room_layout_v5.html"
ATLAS_NAME = "kitchen-complete-room-atlas-v5.png"
GUTTER = 8
BODY_MASTER = (420, 370)

EXPECTED = {
    FOUNDATION: "4b7c25ef2ea006225f465360479b73fac3ea2ab02650ea471a1fdb6f5fd35032",
    STATES: "6ab62d05bbc0fa7b24357abddbca8e5828ae0bb5a34a90b7dc79f88358721d10",
    REJECTED_FOUNDATION: "54de8e9b70e75ec1ca034e0555ceb855afa901b5b2ea0e9d5952ffe5636bd586",
    REJECTED_STATES: "babd01621ebb25fc2787b9ae23e292bd4863530aaf8366b15b70da81442c116b",
    SUPERSEDED_FOUNDATION: "e598617b257ffbf2899dc9393e86d89a39db0677f9b3faf066efff5b623bbf75",
    SUPERSEDED_STATES: "18b35f2faea27124113d77d9ec913cc9a06ea5cf6dd9299dcb60349d898335c9",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body_polygon(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    return [(x0 + 5, y0), (x1 - 5, y0), (x1, y0 + 5), (x1, y1), (x0, y1), (x0, y0 + 5)]


FOUNDATION_SPECS = {
    "cupboard": {"crop": [70, 140, 505, 528], "body": [78, 148, 499, 520]},
    "drawers": {"crop": [552, 140, 984, 528], "body": [558, 148, 979, 520]},
    "sink": {"crop": [1032, 14, 1465, 528], "body": [1039, 148, 1460, 520], "tap": [1160, 18, 1342, 174]},
    "dishwasher": {"crop": [70, 552, 505, 962], "body": [78, 562, 499, 954]},
    "oven": {"crop": [552, 545, 984, 962], "body": [559, 562, 980, 954]},
    "fridge": {"crop": [1032, 552, 1465, 962], "body": [1039, 562, 1460, 954]},
}

STATE_SPECS = {
    "sink-on": {"crop": [108, 12, 466, 382], "body": [116, 98, 458, 376], "tap": [228, 18, 348, 122], "water": [[244, 20, 320, 205]]},
    "sink-broken": {"crop": [512, 12, 968, 398], "body": [560, 98, 910, 376], "tap": [680, 18, 808, 122], "water": [[512, 110, 968, 398]]},
    "dishwasher-on": {"crop": [108, 394, 466, 718], "body": [116, 400, 458, 712]},
    "dishwasher-broken": {"crop": [512, 394, 968, 734], "body": [560, 400, 910, 712], "water": [[512, 642, 968, 734]]},
    "oven-off": {"crop": [108, 736, 466, 1086], "body": [116, 750, 458, 1080]},
    "oven-broken": {"crop": [552, 736, 920, 1086], "body": [560, 750, 910, 1080]},
    "fridge-standard": {"crop": [108, 1094, 466, 1452], "body": [116, 1102, 458, 1446]},
    "fridge-broken": {"crop": [552, 1094, 920, 1504], "body": [560, 1102, 910, 1446], "water": [[552, 1400, 920, 1504]]},
}

for spec in FOUNDATION_SPECS.values():
    spec["polygon"] = body_polygon(*spec["body"])
for spec in STATE_SPECS.values():
    spec["polygon"] = body_polygon(*spec["body"])


def connected_colour_mask(source: Image.Image, region: list[int], kind: str) -> Image.Image:
    x0, y0, x1, y1 = region
    rgb = source.crop(region).convert("RGB")
    seed = Image.new("L", rgb.size, 0)
    pixels = rgb.load()
    target = seed.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = pixels[x, y]
            if kind == "tap":
                selected = (r > 150 and r > g * 1.08 and r > b * 1.45) or (r > 180 and g > 105 and b < 135)
            else:
                selected = (b > 135 and g > 75 and b > r * 1.12) or (r > 170 and g > 185 and b > 195)
            if selected:
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
            dark = max(r, g, b) < 95
            related = r > 130 and r > b * 1.3 if kind == "tap" else b > 70 and b >= r
            if seed_px[x, y] or dark or related:
                out[x, y] = 255
    result = result.filter(ImageFilter.MaxFilter(3))
    full = Image.new("L", source.size, 0)
    full.paste(result, (x0, y0))
    return full


def isolate_and_normalize(source: Image.Image, spec: dict) -> tuple[Image.Image, list[int]]:
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).polygon(spec["polygon"], fill=255)
    if spec.get("tap"):
        mask = ImageChops.lighter(mask, connected_colour_mask(source, spec["tap"], "tap"))
    for region in spec.get("water", []):
        mask = ImageChops.lighter(mask, connected_colour_mask(source, region, "water"))
    mask = mask.filter(ImageFilter.GaussianBlur(0.55))
    isolated = source.copy()
    isolated.putalpha(mask)
    crop = spec["crop"]
    isolated = isolated.crop(crop)
    bx0, by0, bx1, by1 = spec["body"]
    body = [bx0 - crop[0], by0 - crop[1], bx1 - bx0, by1 - by0]
    sx = BODY_MASTER[0] / body[2]
    sy = BODY_MASTER[1] / body[3]
    resized = isolated.resize((round(isolated.width * sx), round(isolated.height * sy)), Image.Resampling.LANCZOS)
    normalized_body = [round(body[0] * sx), round(body[1] * sy), BODY_MASTER[0], BODY_MASTER[1]]
    return resized, normalized_body


def connector(source: Image.Image, body: list[int], sample_x: int) -> Image.Image:
    x = body[0] + sample_x
    return source.crop((x - 15, body[1], x + 15, body[1] + 65))


def transition(left: Image.Image, right: Image.Image) -> Image.Image:
    result = Image.new("RGBA", (30, 65), (0, 0, 0, 0))
    result.alpha_composite(left.crop((0, 0, 15, 65)), (0, 0))
    result.alpha_composite(right.crop((15, 0, 30, 65)), (15, 0))
    return result


def main() -> None:
    for path, digest in EXPECTED.items():
        assert sha256(path) == digest, f"candidate bytes changed: {path}"
    assert sha256(V4 / "manifest.json") == V4_MANIFEST_SHA256, "V4 manifest changed"
    v4 = json.loads((V4 / "manifest.json").read_text())
    grid = json.loads(GRID.read_text())
    foundation = Image.open(FOUNDATION).convert("RGBA")
    states = Image.open(STATES).convert("RGBA")
    candidates: dict[str, tuple[Image.Image, dict]] = {}
    (OUT / "candidates").mkdir(parents=True, exist_ok=True)

    for name, spec in FOUNDATION_SPECS.items():
        image, body = isolate_and_normalize(foundation, spec)
        candidate_path = OUT / "candidates" / f"{name}.png"
        image.save(candidate_path, optimize=True)
        candidates[name] = (image, {"bodyRect": body, "logicalBody": [84, 74], "authority": "unapproved-interface-foundation-v5"})
    for name, spec in STATE_SPECS.items():
        image, body = isolate_and_normalize(states, spec)
        candidate_path = OUT / "candidates" / f"{name}.png"
        image.save(candidate_path, optimize=True)
        candidates[name] = (image, {"bodyRect": body, "logicalBody": [84, 74], "authority": "unapproved-interface-states-v5"})

    standard_join = connector(candidates["cupboard"][0], candidates["cupboard"][1]["bodyRect"], 210)
    oven_join = connector(candidates["oven"][0], candidates["oven"][1]["bodyRect"], 42)
    joins = {
        "standard-standard": standard_join,
        "standard-oven": transition(standard_join, oven_join),
        "oven-standard": transition(oven_join, standard_join),
    }

    v4_atlas = Image.open(V4 / "assets" / v4["atlas"]["file"]).convert("RGBA")
    canonical_images = {}
    for name, record in v4["assets"].items():
        x, y, w, h = record["atlasRect"]
        canonical_images[name] = v4_atlas.crop((x, y, x + w, y + h))
    loose_images = {}
    for name, record in v4["looseAssets"].items():
        x, y, w, h = record["atlasRect"]
        loose_images[name] = v4_atlas.crop((x, y, x + w, y + h))

    items: list[tuple[str, str, Image.Image, dict]] = []
    for name, image in canonical_images.items():
        predecessor = v4["assets"][name]
        record = {
            "bodyRect": predecessor["bodyRect"],
            "logicalBody": predecessor["logicalBody"],
            "authority": predecessor["authority"],
        }
        items.append(("canonicalAssets", name, image, record))
    for name, (image, record) in candidates.items():
        items.append(("assets", name, image, record))
    for name, image in loose_images.items():
        record = {key: value for key, value in v4["looseAssets"][name].items() if key not in {"atlasRect", "file"}}
        items.append(("looseAssets", name, image, record))
    for name, image in joins.items():
        items.append(("interfaceAssets", name, image, {"logicalSize": [6, 13], "role": "master-resolution internal worktop connector"}))

    atlas_width = max(image.width for _, _, image, _ in items) + GUTTER * 2
    atlas_height = sum(image.height + GUTTER for _, _, image, _ in items) + GUTTER
    atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))
    sections = {"canonicalAssets": {}, "assets": {}, "looseAssets": {}, "interfaceAssets": {}}
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
        "schema": "lighthouse-keeper/kitchen-complete-room-layout@5",
        "set": SET,
        "status": "unapproved-countertop-interface-and-cabinet-owned-objects",
        "approvedAuthoritiesPreserved": {
            "foundation": v4["source"],
            "states": v4["stateSource"],
            "changed": False,
        },
        "candidateSources": {
            "foundation": {"path": str(FOUNDATION.relative_to(ROOT)), "sha256": EXPECTED[FOUNDATION]},
            "states": {"path": str(STATES.relative_to(ROOT)), "sha256": EXPECTED[STATES]},
            "rejectedHobColourAttempts": [
                {"path": str(REJECTED_FOUNDATION.relative_to(ROOT)), "sha256": EXPECTED[REJECTED_FOUNDATION]},
                {"path": str(REJECTED_STATES.relative_to(ROOT)), "sha256": EXPECTED[REJECTED_STATES]},
            ],
            "supersededBeforeStraightSinkDatum": [
                {"path": str(SUPERSEDED_FOUNDATION.relative_to(ROOT)), "sha256": EXPECTED[SUPERSEDED_FOUNDATION]},
                {"path": str(SUPERSEDED_STATES.relative_to(ROOT)), "sha256": EXPECTED[SUPERSEDED_STATES]},
            ],
        },
        "deliveryPredecessor": {"set": v4["set"], "manifestSha256": V4_MANIFEST_SHA256, "v4Changed": False},
        "room": v4["room"],
        "states": v4["states"],
        "canonicalAssets": sections["canonicalAssets"],
        "assets": sections["assets"],
        "looseAssets": sections["looseAssets"],
        "interfaceAssets": sections["interfaceAssets"],
        "roomGrid": grid,
        "countertopOwnership": grid["countertopObjectOwnership"],
        "looseGeometry": {
            **v4["looseGeometry"],
            "defaultPositions": None,
            "defaultSlotAssignments": grid["floorSlots"]["defaultAssignments"],
            "countertopPositionStorage": "supporting cabinet identity only",
        },
        "countertopInterface": {
            "bodyMasterPixels": list(BODY_MASTER),
            "allBodyRectsExact": True,
            "internalEdges": "square; no baked exposed-end bevels",
            "joinSelection": "standard-standard, standard-oven or oven-standard from current neighbours",
            "legacyV22V32HealingUsed": False,
            "approved": False,
        },
        "atlas": {
            "file": ATLAS_NAME,
            "sha256": sha256(atlas_path),
            "pixels": list(atlas.size),
            "drawingCount": len(items),
            "uniqueImageRequests": 1,
            "lossless": True,
        },
        "boundaries": {
            "productionChanged": False,
            "runtimeChanged": False,
            "approvedSourceOverwritten": False,
            "candidateReviewOnly": True,
        },
    }
    payload = (json.dumps(manifest, indent=2) + "\n").encode()
    (OUT / "manifest.json").write_bytes(payload)
    (PUBLIC / "manifest.json").write_bytes(payload)
    (PUBLIC / "index.html").write_text(TEMPLATE.read_text())
    print(json.dumps({"set": SET, "atlas": manifest["atlas"], "owners": manifest["countertopOwnership"]["defaultOwners"]}, indent=2))


if __name__ == "__main__":
    main()
