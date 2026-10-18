#!/usr/bin/env python3
"""Build immutable V8 from V7 with a coherent slightly-open broken oven."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v8"
V7_SET = "kitchen-rebuild-states-2026-10-18-v7"
V7_RAW = ROOT / "art/raw" / V7_SET
V7_DRAFT = ROOT / "art/drafts" / V7_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v8"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v8.html").read_text()
    cards = "".join(
        f'<article><h3>{asset.title()} · {state.title()}</h3>'
        f'<div class="cell"><img src="assets/{asset}-{state}.png" alt="{asset} {state}"></div></article>'
        for asset, states in catalogue["states"].items()
        for state in states
    )
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__CARDS__", cards)


def burnt_contents(image: Image.Image) -> Image.Image:
    """Char only the roast, preserving the exact tray, cavity and door."""
    result = image.copy()
    pixels = result.load()
    for y in range(81, 91):
        for x in range(19, 58):
            r, g, b, a = pixels[x, y]
            if a and r > 80 and r > g * 1.12 and g < 145:
                value = max(12, min(58, (r + g + b) // 9))
                pixels[x, y] = (value, max(10, value - 7), max(9, value - 11), a)
    return result


def dark_cavity(image: Image.Image) -> Image.Image:
    """Switch the exact On cavity off without changing its geometry."""
    result = image.copy()
    pixels = result.load()
    for y in range(77, 101):
        for x in range(9, 64):
            r, g, b, a = pixels[x, y]
            if a:
                pixels[x, y] = (max(5, r * 18 // 100), max(7, g * 20 // 100), max(9, b * 24 // 100), a)
    return result


def open_door_toward_camera(image: Image.Image, gap_colour: tuple[int, int, int, int]) -> Image.Image:
    """Foreshorten the exact door evenly about its centreline; no side skew."""
    result = image.copy()
    door = image.crop((0, 67, 72, 107)).resize((72, 37), Image.Resampling.NEAREST)
    # A three-pixel horizontal cavity reveal represents only a few degrees of opening.
    # The compressed door then covers the complete prior door footprint, so the
    # shared cabinet body beneath it never becomes transparent or fragmented.
    for y in range(67, 70):
        for x in range(4, 69):
            result.putpixel((x, y), gap_colour)
    result.alpha_composite(door, (0, 70))
    return result


def indicator_off(image: Image.Image, reference: Image.Image) -> Image.Image:
    result = image.copy()
    result.alpha_composite(reference.crop((57, 56, 69, 66)), (57, 56))
    return result


def timed_state_strip(frame: Image.Image, active_frames: set[int]) -> Image.Image:
    """Full-state swap cells have two transparent pixels on every shared edge."""
    strip = Image.new("RGBA", (88 * 40, 124))
    for index in active_frames:
        strip.alpha_composite(frame, (index * 88 + 2, 2))
    return strip


def main() -> None:
    v7 = json.loads(V7_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    for name in v7["outputs"]:
        shutil.copyfile(V7_RAW / name, RAW / name)
        shutil.copyfile(V7_RAW / name, ASSETS / name)

    on = Image.open(V7_RAW / "oven-on.png").convert("RGBA")
    standard = Image.open(V7_RAW / "oven-standard.png").convert("RGBA")
    lit = indicator_off(open_door_toward_camera(burnt_contents(on), (66, 35, 14, 255)), standard)
    unlit = indicator_off(open_door_toward_camera(dark_cavity(burnt_contents(on)), (9, 13, 18, 255)), standard)
    unlit.save(RAW / "oven-broken.png", optimize=True)
    unlit.save(ASSETS / "oven-broken.png", optimize=True)

    timings = {
        "classic": set(range(4, 11)) | set(range(18, 23)) | set(range(31, 35)),
        "slow": set(range(3, 13)) | set(range(25, 32)),
        "erratic": {2, 3, 7, 8, 9, 14, 20, 21, 23, 24, 28, 30, 31, 32, 35},
    }
    for model, active in timings.items():
        name = f"oven-broken-cavity-flicker--{model}"
        filename = f"fx-{name}-f40.png"
        strip = timed_state_strip(lit, active)
        strip.save(RAW / filename, optimize=True)
        strip.save(ASSETS / filename, optimize=True)

    catalogue = json.loads(json.dumps(v7))
    catalogue.update({"set": SET, "version": 8, "status": "coherent-broken-oven-state-swap-awaiting-review"})
    catalogue["method"].update({"fullStateFlickerSwap": True, "brokenOvenDerivedFromOn": True})
    catalogue["sourceProvenance"]["immutableV7Parent"] = {
        "set": V7_SET,
        "catalogueSha256": sha(V7_DRAFT),
    }
    for filename in ["oven-broken.png", *[f"fx-oven-broken-cavity-flicker--{m}-f40.png" for m in timings]]:
        image = Image.open(RAW / filename)
        catalogue["outputs"][filename] = {"sha256": sha(RAW / filename), "pixels": list(image.size)}
    for name in catalogue["effectFamilies"]["oven-broken-cavity-flicker"]["models"]:
        effect = catalogue["effects"][name]
        effect.update({"origin": [334, 96], "size": [88, 124], "cellPixels": [88, 124], "fullStateSwap": True})

    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "awaiting-coherent-broken-oven-review",
        "parent": V7_SET,
        "promotion": "none",
        "runtimeWiring": "unchanged",
        "rollback": "Delete V8 only; V7 and all prior immutable evidence remain unchanged.",
    }, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: On-derived slightly-open broken oven, full-state internal-light swaps, unchanged asset-first workbench")


if __name__ == "__main__":
    main()
