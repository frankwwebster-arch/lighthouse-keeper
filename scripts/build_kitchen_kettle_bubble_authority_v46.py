#!/usr/bin/env python3
"""Build/verify the immutable V46 kitchen kettle from approved Bubble art."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from build_activity_story_ligne_claire_bbq_family_2026_10_21_v1 import (
    CELL,
    DARK_BACK,
    INK,
    VISIBLE_ALPHA,
    backed,
    edge_alpha_pixels,
    normalise,
    visible_bounds,
    write_hashes,
)


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-kettle-bubble-authority-v46"
VERSION = 46
PACK = ROOT / "art/drafts/kitchen-kettle-bubble-authority-2026-10-22-v46"
BUBBLE = ROOT / "art/drafts/activity-story-ligne-claire-tea-toast-2026-10-22-v1/drafts/components/tea-kettle.png"
BROKEN_SOURCE = PACK / "source/kettle-broken-imagegen-source.png"
V45_RAW = ROOT / "art/raw/kitchen-kettle-standalone-2026-10-21-v45"
V45_CONTRACT = ROOT / "art/drafts/kitchen-kettle-standalone-2026-10-21-v45/candidate-catalogue.json"
CREAM_BACK = (247, 236, 204, 255)
CREAM = (246, 229, 183)
LIGHT = (237, 233, 222)
PALE_BLUE = (151, 202, 218)
NAVY = (13, 78, 117)
ORANGE = (232, 139, 45)
GREY = (105, 117, 120)
PALETTE = [INK, CREAM, LIGHT, PALE_BLUE, NAVY, ORANGE, GREY]
EFFECT_NAMES = [
    f"fx-kettle-{state}-steam--{model}-f40.png"
    for state in ("on", "broken")
    for model in ("compact", "regular", "emphatic")
]
BROKEN_EFFECT_DX = 54
BROKEN_EFFECT_DY = -78
DIRECTION = "Use Frank-approved Bubble tea-kettle V2 as the actual intact kitchen kettle."
STATUS = "superseded-unapproved-unpromoted"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def alpha_components(image: Image.Image) -> list[set[tuple[int, int]]]:
    pixels = image.load()
    seen: set[tuple[int, int]] = set()
    result: list[set[tuple[int, int]]] = []
    for y in range(image.height):
        for x in range(image.width):
            if (x, y) in seen or pixels[x, y][3] == 0:
                continue
            group = {(x, y)}
            stack = [(x, y)]
            seen.add((x, y))
            while stack:
                px, py = stack.pop()
                for point in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                    nx, ny = point
                    if 0 <= nx < image.width and 0 <= ny < image.height and point not in seen and pixels[nx, ny][3] > 0:
                        seen.add(point)
                        group.add(point)
                        stack.append(point)
            result.append(group)
    return sorted(result, key=len, reverse=True)


def isolate_groups(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    groups = alpha_components(image)
    if len(groups) != 2:
        raise RuntimeError(f"approved Bubble kettle must contain body plus one detached steam component; found {len(groups)}")
    body = Image.new("RGBA", image.size)
    steam = Image.new("RGBA", image.size)
    source = image.load()
    for x, y in groups[0]:
        body.putpixel((x, y), source[x, y])
    for x, y in groups[1]:
        steam.putpixel((x, y), source[x, y])
    return body, steam


def paste_fitted(dst: Image.Image, sprite: Image.Image, x: int, support_y: int, target: tuple[int, int]) -> None:
    box = sprite.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError("empty state")
    crop = sprite.crop(box)
    crop.thumbnail(target, Image.Resampling.LANCZOS)
    dst.alpha_composite(crop, (x, support_y - crop.height))


def effect_frame(path: Path, frame: int, cell: tuple[int, int]) -> Image.Image:
    strip = Image.open(path).convert("RGBA")
    width, height = cell
    return strip.crop((frame * width, 0, (frame + 1) * width, height))


def contact_sheet(source: Image.Image, off: Image.Image, steam: Image.Image, broken: Image.Image) -> Image.Image:
    titles = ("APPROVED BUBBLE", "OFF / EXACT BODY", "ON / SEPARATE STEAM", "BROKEN CANDIDATE", "OFF / 64PX", "BROKEN / 64PX")
    sheet = Image.new("RGBA", (CELL * 6, 42 + CELL), DARK_BACK)
    draw = ImageDraw.Draw(sheet)
    for index, title in enumerate(titles):
        draw.text((index * CELL + 8, 14), title, fill=CREAM_BACK)
    sheet.alpha_composite(backed(source, CREAM_BACK), (0, 42))
    sheet.alpha_composite(backed(off, CREAM_BACK), (CELL, 42))
    on = off.copy()
    on.alpha_composite(steam)
    sheet.alpha_composite(backed(on, CREAM_BACK), (CELL * 2, 42))
    sheet.alpha_composite(backed(broken, CREAM_BACK), (CELL * 3, 42))
    for column, sprite in ((4, off), (5, broken)):
        small = sprite.resize((64, 64), Image.Resampling.LANCZOS)
        panel = Image.new("RGBA", (CELL, CELL), CREAM_BACK)
        panel.alpha_composite(small, (96, 96))
        sheet.alpha_composite(panel, (CELL * column, 42))
    return sheet


def room_proof(off: Image.Image, broken: Image.Image) -> Image.Image:
    room = Image.open(V45_RAW / "approved-kitchen-counter-room.png").convert("RGBA")
    room = room.resize((room.width * 2, room.height * 2), Image.Resampling.NEAREST)
    support_y = 141 * 2
    paste_fitted(room, off, (84 + 14) * 2, support_y, (56 * 2, 51 * 2))
    paste_fitted(room, off, (168 + 14) * 2, support_y, (56 * 2, 51 * 2))
    on_fx = effect_frame(PACK / "effects/fx-kettle-on-steam--regular-f40.png", 13, (128, 176))
    on_fx = on_fx.resize((20 * 2, 36 * 2), Image.Resampling.LANCZOS)
    room.alpha_composite(on_fx, ((168 + 54) * 2, (141 - 72) * 2))
    paste_fitted(room, broken, (336 + 11) * 2, support_y, (62 * 2, 59 * 2))
    broken_fx = effect_frame(PACK / "effects/fx-kettle-broken-steam--regular-f40.png", 22, (144, 192))
    broken_fx = broken_fx.resize((27 * 2, 42 * 2), Image.Resampling.LANCZOS)
    room.alpha_composite(broken_fx, ((336 + BROKEN_EFFECT_DX) * 2, (141 + BROKEN_EFFECT_DY) * 2))
    return room


def build() -> None:
    for directory in (PACK / "states", PACK / "effects", PACK / "evidence"):
        directory.mkdir(parents=True, exist_ok=True)
    source = Image.open(BUBBLE).convert("RGBA")
    off, steam = isolate_groups(source)
    off_path = PACK / "states/kettle-off.png"
    on_path = PACK / "states/kettle-on.png"
    steam_path = PACK / "states/kettle-approved-steam-isolated.png"
    off.save(off_path, optimize=True)
    off.save(on_path, optimize=True)
    steam.save(steam_path, optimize=True)

    broken_raw = Image.open(BROKEN_SOURCE).convert("RGBA")
    broken, broken_evidence = normalise(broken_raw, PALETTE)
    broken_path = PACK / "states/kettle-broken.png"
    broken.save(broken_path, optimize=True)

    for name in EFFECT_NAMES:
        shutil.copy2(V45_RAW / name, PACK / "effects" / name)

    contact_path = PACK / "evidence/state-family-light-dark-64.png"
    contact_sheet(source, off, steam, broken).save(contact_path, optimize=True)
    room_path = PACK / "evidence/exact-v45-room-retina-proof.png"
    room_proof(off, broken).save(room_path, optimize=True)

    v45 = json.loads(V45_CONTRACT.read_text())
    objects = {}
    for name, path in (("off", off_path), ("on", on_path), ("broken", broken_path)):
        image = Image.open(path).convert("RGBA")
        objects[name] = {
            "file": rel(path),
            "sha256": sha256(path),
            "pixels": list(image.size),
            "bounds": list(visible_bounds(image)),
            "edgeAlphaPixels": edge_alpha_pixels(image),
        }
    manifest = {
        "schema": "lighthouse-keeper/kitchen-kettle-bubble-authority@1",
        "set": SET,
        "version": VERSION,
        "created": "2026-10-22",
        "status": STATUS,
        "direction": DIRECTION,
        "intactAuthority": {"file": rel(BUBBLE), "sha256": sha256(BUBBLE)},
        "brokenSource": {"file": rel(BROKEN_SOURCE), "sha256": sha256(BROKEN_SOURCE), "mode": "built-in precise image edit, then deterministic fixed-palette normalisation"},
        "states": objects,
        "intactGuarantee": {
            "offAndOnByteIdentical": sha256(off_path) == sha256(on_path),
            "bodyPixelsByteIdenticalToApprovedBubble": True,
            "onlyRemovedComponent": "the one detached approved steam plume",
            "approvedSteamPreservedSeparately": {"file": rel(steam_path), "sha256": sha256(steam_path)},
        },
        "brokenNormalisation": {"flatPalette": ["#%02x%02x%02x" % colour for colour in PALETTE], **broken_evidence},
        "preservedV45Contract": {
            "source": {"file": rel(V45_CONTRACT), "sha256": sha256(V45_CONTRACT)},
            "logicalFootprintPixels": v45["geometry"]["logicalFootprintPixels"],
            "supportSurfaceSlots": v45["geometry"]["supportSurfaceSlots"],
            "supportPlaneY": v45["geometry"]["supportPlaneY"],
            "stateRender": v45["geometry"]["stateRender"],
            "brokenBodyAnimation": v45["states"]["broken"]["bodyAnimation"],
            "brokenAssetLock": v45["brokenAssetLock"],
            "countertopOccupancy": v45["countertopOccupancy"],
            "teaInteraction": v45["teaInteraction"],
            "brokenSteamAnchor": {
                "dx": BROKEN_EFFECT_DX,
                "dy": BROKEN_EFFECT_DY,
                "reason": "asset-local placement of the unchanged animated effect; V47 moves it to the fully open top",
            },
            "effectsByteIdentical": [
                {"file": rel(PACK / "effects" / name), "sha256": sha256(PACK / "effects" / name), "sourceSha256": sha256(V45_RAW / name)}
                for name in EFFECT_NAMES
            ],
        },
        "evidence": [
            {"file": rel(contact_path), "sha256": sha256(contact_path)},
            {"file": rel(room_path), "sha256": sha256(room_path)},
        ],
        "registration": {"register": False, "promote": False, "runtimeChanged": False, "approvalRequired": True},
        "rollback": "Discard this V46 directory alone; V45, Bubble V2, production and runtime remain unchanged.",
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_hashes(PACK)
    verify()
    print(f"Built {SET}: exact approved intact body, flat Broken candidate and preserved V45 contract.")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    if manifest["set"] != SET or manifest["status"] != STATUS:
        raise RuntimeError("manifest identity/status mismatch")
    source = Image.open(BUBBLE).convert("RGBA")
    expected_body, expected_steam = isolate_groups(source)
    off = Image.open(PACK / "states/kettle-off.png").convert("RGBA")
    on = Image.open(PACK / "states/kettle-on.png").convert("RGBA")
    steam = Image.open(PACK / "states/kettle-approved-steam-isolated.png").convert("RGBA")
    if list(off.get_flattened_data()) != list(expected_body.get_flattened_data()) or list(on.get_flattened_data()) != list(expected_body.get_flattened_data()):
        raise RuntimeError("intact kitchen body differs from approved Bubble body")
    if list(steam.get_flattened_data()) != list(expected_steam.get_flattened_data()):
        raise RuntimeError("approved steam isolation drift")
    broken = Image.open(PACK / "states/kettle-broken.png").convert("RGBA")
    if broken.size != (CELL, CELL) or edge_alpha_pixels(broken) or manifest["brokenNormalisation"]["transparentGutterPx"] < 20:
        raise RuntimeError("unsafe Broken candidate")
    allowed = set(PALETTE)
    actual = {pixel[:3] for pixel in broken.get_flattened_data() if pixel[3] > VISIBLE_ALPHA}
    if not actual.issubset(allowed):
        raise RuntimeError("Broken candidate contains non-flat palette colours")
    for record in manifest["preservedV45Contract"]["effectsByteIdentical"]:
        if record["sha256"] != record["sourceSha256"] or sha256(ROOT / record["file"]) != record["sha256"]:
            raise RuntimeError("V45 effect drift")
    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(PACK).as_posix()}"
        for path in sorted(PACK.rglob("*"))
        if path.is_file() and path.name != "HASHES.sha256"
    ]
    if (PACK / "HASHES.sha256").read_text().splitlines() != expected_hashes:
        raise RuntimeError("HASHES.sha256 stale")
    print(f"Verified {SET}: exact intact pixels, isolated steam, fixed-palette Broken and V45 behavior hashes.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()


if __name__ == "__main__":
    main()
