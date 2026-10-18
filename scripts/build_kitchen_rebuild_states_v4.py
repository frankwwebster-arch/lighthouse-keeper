#!/usr/bin/env python3
"""Build V4 from immutable V3, adding per-effect playback speed controls."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v4"
V3_SET = "kitchen-rebuild-states-2026-10-18-v3"
V3_RAW = ROOT / "art/raw" / V3_SET
V3_DRAFT = ROOT / "art/drafts" / V3_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v4"
ASSETS = PUBLIC / "assets"
FRAMES, CELL = 40, (120, 144)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); image.save(path, optimize=True)


def publish_copy(source: Path, name: str, outputs: dict) -> None:
    for target in (RAW / name, ASSETS / name):
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
    image = Image.open(source); outputs[name] = {"sha256": sha(source), "pixels": list(image.size)}


def wrap_flies() -> Image.Image:
    source = Image.open(V3_RAW / "fx-bin-flies-f40.png").convert("RGBA")
    strip = Image.new("RGBA", (120 * FRAMES, 144))
    for frame in range(FRAMES):
        cell = Image.new("RGBA", CELL)
        cell.alpha_composite(source.crop((frame * 80, 0, frame * 80 + 80, 80)), (20, 60))
        strip.alpha_composite(cell, (frame * 120, 0))
    return strip


def variant(strip: Image.Image, sx: float, sy: float) -> Image.Image:
    output = Image.new("RGBA", strip.size)
    for frame in range(FRAMES):
        cell = strip.crop((frame * 120, 0, frame * 120 + 120, 144)); box = cell.getchannel("A").getbbox()
        if not box: continue
        art = cell.crop(box); w = max(1, min(112, round(art.width * sx))); h = max(1, min(136, round(art.height * sy)))
        art = art.resize((w, h), Image.Resampling.LANCZOS)
        x = max(4, min(116 - w, (box[0] + box[2]) // 2 - w // 2)); y = max(4, min(140 - h, box[3] - h))
        target = Image.new("RGBA", CELL); target.alpha_composite(art, (x, y)); output.alpha_composite(target, (frame * 120, 0))
    return output


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v4.html").read_text()
    cards = "".join(f'<article><h3>{a.title()} · {s.title()}</h3><div class="cell"><img src="assets/{a}-{s}.png" alt="{a} {s}"></div></article>' for a, states in catalogue["states"].items() for s in states)
    options = "".join(f'<option value="{n}">{n.replace("-", " ").title()}</option>' for n in catalogue["effects"])
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__EFFECT_OPTIONS__", options).replace("__CARDS__", cards)


def main() -> None:
    v3 = json.loads(V3_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists(): shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS): directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name in v3["outputs"]: publish_copy(V3_RAW / name, name, outputs)

    effects = json.loads(json.dumps(v3["effects"])); families = json.loads(json.dumps(v3["effectFamilies"]))
    classic = wrap_flies(); fly_models = {"classic": classic, "compact": variant(classic, .82, .88), "emphatic": variant(classic, 1.12, 1.06)}
    names = []
    for model, strip in fly_models.items():
        name = f"bin-broken-flies--{model}"; filename = f"fx-{name}-f40.png"; save(strip, RAW / filename); shutil.copyfile(RAW / filename, ASSETS / filename)
        outputs[filename] = {"sha256": sha(RAW / filename), "pixels": list(strip.size)}; names.append(name)
        effects[name] = {"asset": "bin", "state": "broken", "origin": [-16, 44], "size": [120, 144], "sfx": "kitchen_bin_flies_slow_loop", "family": "bin-broken-flies", "model": model, "file": filename, "frames": 40, "fps": 4, "durationSeconds": 10, "canonicalDurationSeconds": 10, "speedRange": [.1, 4], "reusable": True, "effectOnly": True, "editableTransform": True, "editableSpeed": True, "cellPixels": [120, 144], "crop": [0, 0, 0, 0]}
    families["bin-broken-flies"] = {"models": names, "default": names[0]}
    for meta in effects.values():
        meta["canonicalDurationSeconds"] = 10; meta["speedRange"] = [.1, 4]; meta["editableSpeed"] = True

    catalogue = json.loads(json.dumps(v3)); catalogue.update({"set": SET, "version": 4, "status": "variable-speed-effect-workbench-awaiting-review", "effects": effects, "effectFamilies": families, "outputs": outputs, "media": list(outputs)})
    catalogue["method"]["perEffectPlaybackSpeed"] = True
    catalogue["method"]["canonicalLoopSeconds"] = 10
    catalogue["sourceProvenance"]["immutableV3Parent"] = {"set": V3_SET, "catalogueSha256": sha(V3_DRAFT)}
    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"set": SET, "status": "awaiting-variable-speed-visual-review", "parent": V3_SET, "promotion": "none", "runtimeWiring": "unchanged", "rollback": "Delete V4 only; V3 remains immutable."}, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(families)} families, {len(effects)} models, canonical 10-second loops with per-model speed")


if __name__ == "__main__": main()
