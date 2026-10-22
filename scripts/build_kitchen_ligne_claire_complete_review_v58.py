#!/usr/bin/env python3
"""Build immutable Kitchen V58, refining the V57 fitted-carcass proof."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-ligne-claire-complete-review-v58"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v58"
PUBLIC = ROOT / "public/keeper-review" / SET
ARCHIVE_SET = ROOT / "review-archive/sets" / f"{SET}.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V57 = load_module("kitchen_review_v57_builder_for_v58", ROOT / "scripts/build_kitchen_ligne_claire_complete_review_v57.py")
ORIGINAL_UPDATE_PAGE = V57.update_page


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_cupboard_hardware(shell: Image.Image) -> None:
    """Keep carcass blues but omit orange hinges/knobs belonging to cupboard doors."""
    pixels = shell.load()
    width, height = shell.size

    def orange(pixel):
        r, g, b, a = pixel
        return a and r > 115 and r > g * 1.14 and r > b * 1.35

    targets = [(x, y) for y in range(18, min(71, height)) for x in range(width) if orange(pixels[x, y])]
    for x, y in targets:
        replacement = None
        for distance in range(1, 14):
            for candidate_y in (y - distance, y + distance):
                if 18 <= candidate_y < min(71, height) and not orange(pixels[x, candidate_y]) and pixels[x, candidate_y][3]:
                    replacement = pixels[x, candidate_y]
                    break
            if replacement:
                break
        if replacement:
            pixels[x, y] = replacement


def fitted_dishwasher(source: Image.Image, suffix: str, state: str) -> Image.Image:
    cabinet = Image.open(PACK / "workbench-assets" / V57.cabinet_for_suffix(suffix)).convert("RGBA")
    remove_cupboard_hardware(cabinet)
    out = Image.new("RGBA", source.size, (0, 0, 0, 0))
    out.alpha_composite(cabinet, (3, 0))
    V57.overlay_exact(out, source, (18, 20, 80, 71) if state != "broken" else (16, 20, 82, 78))
    return out


def fitted_oven(source: Image.Image) -> Image.Image:
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-le-re.png").convert("RGBA")
    remove_cupboard_hardware(cabinet)
    out = cabinet.copy()
    sp = source.load()
    op = out.load()
    # Explicit component windows prevent the rejected glossy cooker surface
    # and corner flashes from leaking into the common Cabinet V11 worktop.
    component_windows = ((17, 5, 44, 18), (48, 5, 75, 18), (76, 4, 88, 20))
    for x0, y0, x1, y1 in component_windows:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if V57.is_hob_or_knob(sp[x, y]):
                    op[x, y] = sp[x, y]
    V57.overlay_exact(out, source, (4, 20, 88, 71))
    return out


def make_run_evidence() -> Path:
    font = ImageFont.load_default()
    sheet = Image.new("RGBA", (1370, 760), (250, 244, 224, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), "PRIMARY ACCEPTANCE VIEW - one Cabinet V11 carcass / flat joins / shared plinth", fill=(5, 24, 36), font=font)
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-lj-rj.png").convert("RGBA")
    oven = Image.open(PACK / "workbench-assets/oven-on.png").convert("RGBA")
    cap = Image.open(PACK / "workbench-assets/countertop-join-cap-template.png").convert("RGBA").crop((0, 0, 16, 12))
    for row, state in enumerate(("off", "on", "broken")):
        dishwasher = Image.open(PACK / "workbench-assets" / f"dishwasher-{state}-lj-rj.png").convert("RGBA")
        native = V57.checker((340, 92), 6)
        # Exact live-room geometry: bay origins 20, 104, 188.
        native.alpha_composite(cabinet, (16, 5))
        native.alpha_composite(dishwasher, (97, 5))
        native.alpha_composite(oven, (184, 5))
        native.alpha_composite(cap, (96, 9))
        native.alpha_composite(cap, (180, 9))
        enlarged = native.resize((1360, 368), Image.Resampling.NEAREST)
        y = 45 + row * 235
        sheet.alpha_composite(enlarged.crop((0, 0, 1360, 205)), (5, y))
        draw.text((18, y + 208), state.upper(), fill=(5, 24, 36), font=font)
    path = PACK / "evidence/contact-fitted-carcass-v58.png"
    sheet.save(path, optimize=True)
    return path


def update_page(published_hashes: dict[str, str]) -> None:
    ORIGINAL_UPDATE_PAGE(published_hashes)
    page_path = PUBLIC / "index.html"
    page = page_path.read_text().replace("V57", "V58").replace("v57", "v58")
    page = page.replace(
        "function joinMethod(a,b){return a.kind==='oven'||b.kind==='oven'?'oven-triangle':'flat-v22'}",
        "function joinMethod(a,b){return'flat-v22'}",
    )
    page = page.replace("contact-fitted-carcass-v57.png", "contact-fitted-carcass-v58.png")
    page = page.replace(
        "the approved oven supplies its insert, and exact Cabinet V11 pixels supply both shells",
        "the approved oven supplies its insert, and Cabinet V11 supplies both shell geometries and colours",
    )
    page_path.write_text(page)


def replace_versions(value):
    if isinstance(value, dict):
        return {key: replace_versions(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_versions(item) for item in value]
    if isinstance(value, str):
        return value.replace("V57", "V58").replace("v57", "v58")
    return value


def postprocess() -> None:
    manifest_path = PACK / "manifest.json"
    manifest = replace_versions(json.loads(manifest_path.read_text()))
    manifest.update({
        "set": SET,
        "version": 58,
        "scope": "Cabinet V11 shell geometry/blue/plinth around dishwasher and oven inserts; cupboard hardware excluded; flat join repair with continuous dark rear edge",
        "rollback": "Discard only this V58 pack, archive set and review shell; V57/V56, Dishwasher V8, approved oven/kettle assets and production remain byte-identical.",
    })
    manifest["workbench"].update({
        "ovenJoinMethod": "same flat Cabinet V11 join as every fitted module",
        "cupboardHardwareExcludedFromApplianceShells": True,
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    register_path = PACK / "batch-register.json"
    register = replace_versions(json.loads(register_path.read_text()))
    register["set"] = SET
    register["candidate"]["manifest"] = {"file": V57.rel(manifest_path), "sha256": sha(manifest_path)}
    register["candidate"]["publicShell"] = {"file": V57.rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html")}
    register_path.write_text(json.dumps(register, indent=2) + "\n")

    archive = json.loads(ARCHIVE_SET.read_text())
    archive["set"] = SET
    archive["page"] = {"path": V57.rel(PUBLIC / "index.html"), "sha256": sha(PUBLIC / "index.html"), "bytes": (PUBLIC / "index.html").stat().st_size}
    ARCHIVE_SET.write_text(json.dumps(archive, indent=2) + "\n")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    register = json.loads((PACK / "batch-register.json").read_text())
    archive = json.loads(ARCHIVE_SET.read_text())
    if manifest["set"] != SET or manifest["version"] != 58 or register["register"] or register["promote"]:
        raise RuntimeError("V58 approval gate changed")
    if len(manifest["objects"]) != 60 or len(manifest["contactSheets"]) != 17 or len(archive["entries"]) != 141:
        raise RuntimeError("V58 coverage changed")
    cabinet = Image.open(PACK / "workbench-assets/cabinet-a-le-re.png").convert("RGBA")
    oven = Image.open(PACK / "workbench-assets/oven-on.png").convert("RGBA")
    if oven.crop((4, 71, 88, 78)).tobytes() != cabinet.crop((4, 71, 88, 78)).tobytes():
        raise RuntimeError("V58 oven plinth is not exact Cabinet V11")
    for state in ("off", "on"):
        dishwasher = Image.open(PACK / "workbench-assets" / f"dishwasher-{state}-le-re.png").convert("RGBA")
        if dishwasher.crop((7, 71, 91, 78)).tobytes() != cabinet.crop((4, 71, 88, 78)).tobytes():
            raise RuntimeError(f"V58 dishwasher {state} plinth drift")
        side_pixels = list(dishwasher.crop((7, 18, 18, 71)).convert("RGB").getdata()) + list(dishwasher.crop((80, 18, 91, 71)).convert("RGB").getdata())
        if any(r > 115 and r > g * 1.14 and r > b * 1.35 for r, g, b in side_pixels):
            raise RuntimeError(f"cupboard hinge hardware leaked into dishwasher {state}")
    page = (PUBLIC / "index.html").read_text()
    if "function joinMethod(a,b){return'flat-v22'}" not in page or "contact-fitted-carcass-v58.png" not in page:
        raise RuntimeError("V58 flat fitted join/page drift")
    if "oven-triangle" in page.split("function joinMethod", 1)[1].split("function joins", 1)[0]:
        raise RuntimeError("oven-specific join survived in active selector")
    for route, item in archive["entries"].items():
        if not route.startswith(f"/keeper-review/{SET}/assets/") or sha(ROOT / item["object"]) != item["sha256"]:
            raise RuntimeError(f"V58 archive mismatch: {route}")
    if archive["page"]["sha256"] != sha(PUBLIC / "index.html"):
        raise RuntimeError("V58 page hash drift")
    print("Verified V58: fitted Cabinet V11 shells; no cupboard hardware; flat continuous joins; matching plinth; gate closed")


def build() -> None:
    for name, value in {"SET": SET, "PACK": PACK, "PUBLIC": PUBLIC, "ARCHIVE_SET": ARCHIVE_SET}.items():
        setattr(V57, name, value)
    V57.fitted_dishwasher = fitted_dishwasher
    V57.fitted_oven = fitted_oven
    V57.make_run_evidence = make_run_evidence
    V57.update_page = update_page
    V57.verify = lambda: None
    V57.build()
    postprocess()
    verify()
    print("Built Kitchen V58: flat fitted joins and clean shared appliance carcasses; registration closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
