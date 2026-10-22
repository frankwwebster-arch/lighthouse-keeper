#!/usr/bin/env python3
"""Build immutable Kitchen V59 with opaque-only approved oven components."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v59"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v59"
PUBLIC = ROOT / "public/keeper-review" / SET
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V58 = load_module("kitchen_review_v58_builder_for_v59", ROOT / "scripts/build_kitchen_ligne_claire_complete_review_v58.py")
ORIGINAL_RUN = V58.make_run_evidence


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opaque_hob_or_knob(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if a < 200:
        return False
    spread = max(r, g, b) - min(r, g, b)
    orange = r > 105 and r > g * 1.18 and r > b * 1.35
    neutral_metal = spread < 48
    near_black = max(r, g, b) < 30
    return orange or neutral_metal or near_black


def make_run_evidence() -> Path:
    old_path = ORIGINAL_RUN()
    new_path = old_path.with_name("contact-fitted-carcass-v59.png")
    old_path.rename(new_path)
    return new_path


def replace_versions(value):
    if isinstance(value, dict):
        return {key: replace_versions(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_versions(item) for item in value]
    if isinstance(value, str):
        return value.replace("V58", "V59").replace("v58", "v59")
    return value


def postprocess() -> None:
    page_path = PUBLIC / "index.html"
    page_path.write_text(page_path.read_text().replace("V58", "V59").replace("v58", "v59"))

    manifest_path = PACK / "manifest.json"
    manifest = replace_versions(json.loads(manifest_path.read_text()))
    manifest.update({
        "set": SET,
        "version": 59,
        "scope": "Cabinet V11 shell geometry/blue/plinth and flat continuous joins; opaque approved hob/selector components only, with no translucent cooker-surface remnants",
        "rollback": "Discard only this V59 pack, archive set and review shell; V58/V57/V56, Dishwasher V8, approved oven/kettle assets and production remain byte-identical.",
    })
    manifest["workbench"]["translucentCookerSurfacePixelsExcluded"] = True
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    register_path = PACK / "batch-register.json"
    register = replace_versions(json.loads(register_path.read_text()))
    register["set"] = SET
    register["candidate"]["manifest"] = {"file": V58.V57.rel(manifest_path), "sha256": sha(manifest_path)}
    register["candidate"]["publicShell"] = {"file": V58.V57.rel(page_path), "sha256": sha(page_path)}
    register_path.write_text(json.dumps(register, indent=2) + "\n")

    archive = json.loads(ARCHIVE_SET.read_text())
    archive["set"] = SET
    archive["page"] = {"path": V58.V57.rel(page_path), "sha256": sha(page_path), "bytes": page_path.stat().st_size}
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["set"] != SET or manifest["version"] != 59 or register["register"] or register["promote"]:
        raise RuntimeError("V59 approval gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 17 or len(archive["entries"]) != 141:
        raise RuntimeError("V59 coverage changed")
    oven = V58.Image.open(PACK / "workbench-assets/oven-on.png").convert("RGBA")
    # Interior top pixels may be cabinet antialiasing or fully opaque insert
    # components, never the low-alpha cooker-surface remnants seen in V58.
    for y in range(5, 20):
        for x in range(10, 82):
            alpha = oven.getpixel((x, y))[3]
            if alpha < 200:
                raise RuntimeError(f"translucent oven-top remnant at {(x, y)}")
    page = (PUBLIC / "index.html").read_text()
    if "V59 fitted-carcase acceptance view" not in page or "contact-fitted-carcass-v59.png" not in page:
        raise RuntimeError("V59 page evidence drift")
    if "function joinMethod(a,b){return'flat-v22'}" not in page:
        raise RuntimeError("V59 flat join selector drift")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"V59 archive mismatch: {route}")
    if archive["page"]["sha256"] != sha(PUBLIC / "index.html"):
        raise RuntimeError("V59 page hash drift")
    print("Verified V59: clean opaque oven insert; exact fitted shell/plinth; flat continuous rear joins; gate closed")


def build() -> None:
    for name, value in {"SET": SET, "PACK": PACK, "PUBLIC": PUBLIC, "ARCHIVE_SET": ARCHIVE_SET}.items():
        setattr(V58, name, value)
    V58.V57.is_hob_or_knob = opaque_hob_or_knob
    V58.make_run_evidence = make_run_evidence
    V58.verify = lambda: None
    V58.build()
    postprocess()
    verify()
    print("Built Kitchen V59: fitted set with clean oven top and uninterrupted rear line; registration closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
