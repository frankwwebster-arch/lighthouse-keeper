#!/usr/bin/env python3
"""Build V6 from immutable V5, adding reversible per-family effect switches."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v6"
V5_SET = "kitchen-rebuild-states-2026-10-18-v5"
V5_RAW = ROOT / "art/raw" / V5_SET
V5_DRAFT = ROOT / "art/drafts" / V5_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v6"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publish_copy(source: Path, name: str, outputs: dict) -> None:
    for target in (RAW / name, ASSETS / name):
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
    image = Image.open(source); outputs[name] = {"sha256": sha(source), "pixels": list(image.size)}


def publish_image(image: Image.Image, name: str, outputs: dict) -> None:
    for target in (RAW / name, ASSETS / name):
        target.parent.mkdir(parents=True, exist_ok=True); image.save(target, optimize=True)
    outputs[name] = {"sha256": sha(RAW / name), "pixels": list(image.size)}


def draw_burnt_tray(image: Image.Image) -> Image.Image:
    image = image.copy(); draw = ImageDraw.Draw(image)
    draw.polygon([(10, 78), (64, 78), (69, 85), (7, 85)], fill=(8, 10, 12, 255), outline=(3, 5, 7, 255))
    draw.line([(13, 80), (62, 80)], fill=(54, 45, 38, 255), width=1)
    draw.polygon([(24, 74), (31, 71), (48, 72), (57, 76), (53, 81), (27, 80), (20, 77)], fill=(19, 17, 16, 255), outline=(5, 6, 7, 255))
    draw.point((29, 74), fill=(92, 69, 45, 255)); draw.point((46, 76), fill=(71, 55, 40, 255)); draw.point((36, 79), fill=(118, 83, 45, 255))
    return image


def warning_overlay(on_oven: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", (120, 144))
    overlay.alpha_composite(on_oven.crop((58, 52, 72, 68)), (76, 76))
    return overlay


def cavity_overlay(on_oven: Image.Image, broken_oven: Image.Image) -> Image.Image:
    lit = broken_oven.copy()
    for y in range(63, 91):
        source_y = y + 10
        for x in range(7, 71):
            pixel = on_oven.getpixel((x, source_y))
            if pixel[3]: lit.putpixel((x, y), pixel)
    lit = draw_burnt_tray(lit)
    overlay = Image.new("RGBA", (120, 144))
    overlay.alpha_composite(lit.crop((7, 63, 71, 91)), (25, 87))
    return overlay


def timed_strip(frame: Image.Image, active_frames: set[int]) -> Image.Image:
    strip = Image.new("RGBA", (4800, 144))
    for index in active_frames: strip.alpha_composite(frame, (index * 120, 0))
    return strip


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v6.html").read_text()
    cards = "".join(f'<article><h3>{a.title()} · {s.title()}</h3><div class="cell"><img src="assets/{a}-{s}.png" alt="{a} {s}"></div></article>' for a, states in catalogue["states"].items() for s in states)
    options = "".join(f'<option value="{n}">{n.replace("-", " ").title()}</option>' for n in catalogue["effects"])
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__EFFECT_OPTIONS__", options).replace("__CARDS__", cards)


def main() -> None:
    v5 = json.loads(V5_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists(): shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS): directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name in v5["outputs"]: publish_copy(V5_RAW / name, name, outputs)

    effects = json.loads(json.dumps(v5["effects"])); families = json.loads(json.dumps(v5["effectFamilies"]))
    old_models = families.pop("oven-broken-flicker")["models"]
    for name in old_models:
        filename = effects.pop(name)["file"]; outputs.pop(filename)
        for directory in (RAW, ASSETS): (directory / filename).unlink()

    broken = draw_burnt_tray(Image.open(V5_RAW / "oven-broken.png").convert("RGBA"))
    publish_image(broken, "oven-broken.png", outputs)

    on_oven = Image.open(V5_RAW / "oven-on.png").convert("RGBA")
    warning_timings = {
        "classic": set(range(0, 8)) | set(range(11, 19)) | set(range(22, 31)) | set(range(34, 40)),
        "rapid": {0, 1, 3, 5, 6, 8, 10, 11, 13, 15, 16, 18, 20, 21, 23, 25, 26, 28, 30, 31, 33, 35, 36, 38},
        "angry": {0, 1, 2, 4, 5, 9, 10, 11, 12, 16, 17, 19, 20, 21, 25, 26, 27, 31, 32, 34, 35, 36},
    }
    warning_frame = warning_overlay(on_oven)
    warning_models = []
    for model, frames in warning_timings.items():
        name = f"oven-broken-warning-flicker--{model}"; filename = f"fx-{name}-f40.png"
        publish_image(timed_strip(warning_frame, frames), filename, outputs); warning_models.append(name)
        effects[name] = {"asset": "oven", "state": "broken", "origin": [318, 74], "size": [120, 144], "sfx": "kitchen_oven_broken_warning_flicker_loop", "family": "oven-broken-warning-flicker", "model": model, "file": filename, "frames": 40, "fps": 4, "durationSeconds": 10, "canonicalDurationSeconds": 10, "speedRange": [.1, 4], "reusable": False, "effectOnly": True, "editableTransform": False, "lockedToObject": True, "editableSpeed": True, "cellPixels": [120, 144], "crop": [0, 0, 0, 0]}
    families["oven-broken-warning-flicker"] = {"models": warning_models, "default": warning_models[0]}

    light = cavity_overlay(on_oven, broken)
    timings = {
        "classic": set(range(4, 11)) | set(range(18, 23)) | set(range(31, 35)),
        "slow": set(range(3, 13)) | set(range(25, 32)),
        "erratic": {2, 3, 7, 8, 9, 14, 20, 21, 23, 24, 28, 30, 31, 32, 35},
    }
    cavity_models = []
    for model, frames in timings.items():
        name = f"oven-broken-cavity-flicker--{model}"; filename = f"fx-{name}-f40.png"
        publish_image(timed_strip(light, frames), filename, outputs); cavity_models.append(name)
        effects[name] = {"asset": "oven", "state": "broken", "origin": [318, 74], "size": [120, 144], "sfx": "kitchen_oven_broken_internal_light_flicker_loop", "family": "oven-broken-cavity-flicker", "model": model, "file": filename, "frames": 40, "fps": 4, "durationSeconds": 10, "canonicalDurationSeconds": 10, "speedRange": [.1, 4], "reusable": False, "effectOnly": True, "editableTransform": False, "lockedToObject": True, "editableSpeed": True, "cellPixels": [120, 144], "crop": [0, 0, 0, 0]}
    families["oven-broken-cavity-flicker"] = {"models": cavity_models, "default": cavity_models[0]}

    enabled = {family: family != "fridge-broken-drip" for family in families}
    catalogue = json.loads(json.dumps(v5)); catalogue.update({"set": SET, "version": 6, "status": "switchable-layered-effect-workbench-awaiting-review", "outputs": outputs, "media": list(outputs), "effects": effects, "effectFamilies": families, "effectEnabledDefaults": enabled})
    catalogue["method"]["perEffectFamilyEnabled"] = True
    catalogue["sourceProvenance"]["immutableV5Parent"] = {"set": V5_SET, "catalogueSha256": sha(V5_DRAFT)}
    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"set": SET, "status": "awaiting-switchable-effect-visual-review", "parent": V5_SET, "promotion": "none", "runtimeWiring": "unchanged", "rollback": "Delete V6 only; V5 remains immutable."}, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(catalogue['effectFamilies'])} switchable families, {len(catalogue['effects'])} models, layered oven smoke/warning/cavity effects")


if __name__ == "__main__": main()
