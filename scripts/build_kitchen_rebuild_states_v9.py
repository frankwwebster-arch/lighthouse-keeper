#!/usr/bin/env python3
"""Build immutable V9 from V8 with irregular failing-bulb oven timing."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-19-v9"
V8_SET = "kitchen-rebuild-states-2026-10-18-v8"
V8_RAW = ROOT / "art/raw" / V8_SET
V8_DRAFT = ROOT / "art/drafts" / V8_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v9"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v9.html").read_text()
    cards = "".join(
        f'<article><h3>{asset.title()} · {state.title()}</h3>'
        f'<div class="cell"><img src="assets/{asset}-{state}.png" alt="{asset} {state}"></div></article>'
        for asset, states in catalogue["states"].items()
        for state in states
    )
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__CARDS__", cards)


def timed_state_strip(frame: Image.Image, active_frames: set[int]) -> Image.Image:
    """Full-state swap cells have two transparent pixels on every shared edge."""
    strip = Image.new("RGBA", (88 * 40, 124))
    for index in active_frames:
        strip.alpha_composite(frame, (index * 88 + 2, 2))
    return strip


def main() -> None:
    v8 = json.loads(V8_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    for name in v8["outputs"]:
        shutil.copyfile(V8_RAW / name, RAW / name)
        shutil.copyfile(V8_RAW / name, ASSETS / name)

    # Extract the exact complete lit V8 oven from one active full-state cell.
    parent_strip = Image.open(V8_RAW / "fx-oven-broken-cavity-flicker--classic-f40.png").convert("RGBA")
    lit = parent_strip.crop((4 * 88 + 2, 2, 4 * 88 + 86, 122))

    # No short repeating cadence: each ten-second model mixes isolated flashes,
    # uneven dark holds, two/three-frame sputters and an irregular terminal flutter.
    timings = {
        "classic": {2, 6, 7, 13, 19, 22, 23, 24, 31, 35, 38},
        "slow": {1, 4, 10, 11, 16, 21, 22, 29, 33, 34, 35},
        "erratic": {3, 9, 15, 16, 24, 29, 31, 33, 34, 36, 38},
    }
    labels = {"classic": "random", "slow": "sputtering", "erratic": "near-blow"}
    for model, active in timings.items():
        name = f"oven-broken-cavity-flicker--{model}"
        filename = f"fx-{name}-f40.png"
        strip = timed_state_strip(lit, active)
        strip.save(RAW / filename, optimize=True)
        strip.save(ASSETS / filename, optimize=True)

    catalogue = json.loads(json.dumps(v8))
    catalogue.update({"set": SET, "version": 9, "status": "irregular-failing-bulb-timing-awaiting-review"})
    catalogue["method"].update({"irregularFaultTiming": True, "noShortCadenceRepeat": True})
    catalogue["sourceProvenance"]["immutableV8Parent"] = {
        "set": V8_SET,
        "catalogueSha256": sha(V8_DRAFT),
    }
    for model, active in timings.items():
        name = f"oven-broken-cavity-flicker--{model}"
        filename = f"fx-{name}-f40.png"
        image = Image.open(RAW / filename)
        catalogue["outputs"][filename] = {"sha256": sha(RAW / filename), "pixels": list(image.size)}
        catalogue["effects"][name].update({
            "model": labels[model],
            "timingFrames": sorted(active),
            "timingGrammar": "irregular-dark-holds-isolated-flashes-and-short-stutters",
        })

    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "awaiting-irregular-failing-bulb-review",
        "parent": V8_SET,
        "promotion": "none",
        "runtimeWiring": "unchanged",
        "rollback": "Delete V9 only; approved V8 geometry and all earlier evidence remain unchanged.",
    }, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: exact V8 oven geometry with three irregular ten-second failing-bulb timings")


if __name__ == "__main__":
    main()
