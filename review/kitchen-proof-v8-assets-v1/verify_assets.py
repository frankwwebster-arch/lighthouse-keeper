#!/usr/bin/env python3
"""Acceptance checks for the Kitchen v8 complete Day-1 candidate assets."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_builder():
    spec = importlib.util.spec_from_file_location("kitchen_v8_asset_builder", HERE / "build_assets.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def edge_alpha_is_zero(image: Image.Image) -> bool:
    alpha = image.getchannel("A")
    edges = [
        alpha.crop((0, 0, image.width, 2)),
        alpha.crop((0, image.height - 2, image.width, image.height)),
        alpha.crop((0, 0, 2, image.height)),
        alpha.crop((image.width - 2, 0, image.width, image.height)),
    ]
    return all(edge.getextrema() == (0, 0) for edge in edges)


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    check(manifest["schema"] == "lighthouse-keeper/kitchen-v8-day1-assets@1", "schema drift")
    check(manifest["status"] == "review-candidate", "review status drift")
    check(not manifest["runtimeMutation"] and not manifest["canonMutation"], "production boundary crossed")
    check(not manifest["roomBuilt"], "room assembly crossed the asset boundary")
    check(manifest["standardUnitWidthPx"] == 126, "standard-unit width drift")
    check(manifest["futureRangeWidthPx"] == 252 and not manifest["futureRangeDrawn"], "deferred two-unit range contract drift")
    check(not list((HERE / "outputs").rglob("*range*.png")), "deferred range asset was drawn")

    predecessor = ROOT / manifest["approvedClosedMasterAuthority"] / "manifest.json"
    check(sha256(predecessor) == manifest["predecessorManifestSha256"], "approved v2 predecessor manifest drift")

    for relative, record in manifest["sourceFiles"].items():
        path = HERE / relative
        check(path.is_file(), f"missing source: {relative}")
        check(path.stat().st_size == record["bytes"], f"source byte drift: {relative}")
        check(sha256(path) == record["sha256"], f"source hash drift: {relative}")
        check(list(Image.open(path).size) == record["canvasPx"], f"source canvas drift: {relative}")

    exact_magenta = 0
    near_magenta = 0
    for relative, record in manifest["files"].items():
        path = HERE / relative
        check(path.is_file(), f"missing output: {relative}")
        check(path.stat().st_size == record["bytes"], f"output byte drift: {relative}")
        check(sha256(path) == record["sha256"], f"output hash drift: {relative}")
        image = Image.open(path).convert("RGBA")
        check(list(image.size) == record["canvasPx"], f"output canvas drift: {relative}")
        rgba = iter(image.tobytes())
        for r, g, b, a in zip(rgba, rgba, rgba, rgba):
            if a and (r, g, b) == (255, 0, 255):
                exact_magenta += 1
            elif a and r >= 180 and b >= 180 and g <= 100:
                near_magenta += 1
    check(exact_magenta == 0 and near_magenta == 0, "magenta or near-magenta introduced")

    inherited = {
        "belfast_sink_cabinet-1x.png": "belfast_sink_cabinet-1x.png",
        "painted_dresser-1x.png": "painted_dresser-1x.png",
        "old_school_cooker-1x.png": "small_cream_cooker-1x.png",
    }
    authority_outputs = predecessor.parent / "outputs"
    for candidate, authority in inherited.items():
        check(
            (HERE / "outputs" / candidate).read_bytes() == (authority_outputs / authority).read_bytes(),
            f"praised v2 master changed: {candidate}",
        )

    builder = load_builder()
    for name, size in builder.SPECS.items():
        expected = builder.prepare_asset(HERE / "sources" / "selected" / f"{name}.png", size)
        actual = Image.open(HERE / "outputs" / f"{name}-1x.png").convert("RGBA")
        check(actual.tobytes() == expected.tobytes(), f"non-deterministic selected asset: {name}")
        check(edge_alpha_is_zero(actual), f"transparent safety gutter missing: {name}")

    chair = Image.open(HERE / "outputs/wooden_chair_side-1x.png").convert("RGBA")
    mirrored = Image.open(HERE / "outputs/wooden_chair_side_mirrored-1x.png").convert("RGBA")
    check(mirrored.tobytes() == chair.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes(), "chair mirror is not deterministic")

    expected_state_sizes = {
        "fridge_body_open-1x.png": (126, 180), "fridge_door-1x.png": (126, 180),
        "fridge_closed_registered-1x.png": (126, 180), "cooker_body_open-1x.png": (126, 252),
        "cooker_door-1x.png": (126, 252), "cooker_closed_registered-1x.png": (126, 252),
        "cooker_open_lit_cooking-1x.png": (126, 252), "cooker_open_lit_burnt-1x.png": (126, 252),
        "cooker_oven_light_on-1x.png": (126, 252), "cooker_contents_cooking-1x.png": (80, 34),
        "cooker_contents_burnt-1x.png": (80, 34),
    }
    for filename, size in expected_state_sizes.items():
        image = Image.open(HERE / "outputs/states" / filename).convert("RGBA")
        check(image.size == size, f"state canvas drift: {filename}")
        check(edge_alpha_is_zero(image), f"state safety gutter missing: {filename}")

    door = Image.open(HERE / "outputs/states/cooker_door-1x.png").convert("RGBA")
    glass_alpha = door.getchannel("A").crop((17, 179, 109, 228))
    check(any(0 < value < 255 for value in glass_alpha.tobytes()), "oven glass is not genuinely translucent")

    contents_offset = (23, 193)
    contents_size = Image.open(HERE / "outputs/states/cooker_contents_cooking-1x.png").size
    check(contents_offset[0] + contents_size[0] <= 126 and contents_offset[1] + contents_size[1] <= 252, "oven contents escape cooker canvas")

    for name, bezel in builder.STATUS_BEZELS.items():
        overlay = Image.open(HERE / "outputs/states" / f"{name}_status_on-1x.png").convert("RGBA")
        check(overlay.size == Image.open(HERE / "outputs" / f"{name}-1x.png").size, f"status overlay canvas drift: {name}")
        x, y = bezel["centrePx"]
        r, g, b, a = overlay.getpixel((x, y))
        check(a == 255 and g > r and g > b, f"status overlay is not green at declared bezel: {name}")

    check(len(manifest["items"]) == 12, "Day-1 item inventory count drift")
    for item_id in manifest["items"]:
        item_path = HERE / "items" / item_id / "item.json"
        item = json.loads(item_path.read_text(encoding="utf-8"))
        check(item["schema"] == "lighthouse-keeper/kitchen-item@1", f"item schema drift: {item_id}")
        check(item["id"] == item_id and item["anchor"] == "bottom-left", f"item identity/anchor drift: {item_id}")
        for relative in item["states"].values():
            check((item_path.parent / relative).resolve().is_file(), f"missing item state for {item_id}: {relative}")
    cupboards = json.loads((HERE / "items/painted_base_cupboard/item.json").read_text(encoding="utf-8"))
    check(cupboards["quantity"] == 2 and cupboards["reuseSameBytes"], "matching-cupboard reuse contract drift")
    for item_id in ("cream_larder_fridge", "old_school_cooker", "enamel_electric_kettle", "cream_toaster", "stand_mixer"):
        item = json.loads((HERE / "items" / item_id / "item.json").read_text(encoding="utf-8"))
        check(item["engineDrawsStatusLight"], f"status lamp is not declared engine-drawn: {item_id}")
        check(all("status_on" not in path for path in item["states"].values()), f"review status overlay leaked into production metadata: {item_id}")
    cooker_item = json.loads((HERE / "items/old_school_cooker/item.json").read_text(encoding="utf-8"))
    check(cooker_item["engineDrawsOvenLight"], "oven light is not declared engine-drawn")
    check(all("oven_light" not in path for path in cooker_item["states"].values()), "review oven-light overlay leaked into production metadata")

    print("PASS: Kitchen v8 complete Day-1 candidate assets")
    print("  12 object types; standard unit 126 px; deferred range 252 px and absent")
    print("  praised v2 sink, dresser and cooker inherited byte-for-byte")
    print("  fixed-canvas doors, interiors, oven light, contents and status overlays verified")
    print("  deterministic chair mirror, metadata links, safety gutters and zero magenta")
    print("  no room assembly, runtime promotion, canon mutation or Keeper generation")


if __name__ == "__main__":
    main()
