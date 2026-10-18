#!/usr/bin/env python3
"""Build V5 from immutable V4, correcting only stale review-boundary copy."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v5"
V4_SET = "kitchen-rebuild-states-2026-10-18-v4"
V4_RAW = ROOT / "art/raw" / V4_SET
V4_DRAFT = ROOT / "art/drafts" / V4_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v5"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publish_copy(source: Path, name: str, outputs: dict) -> None:
    for target in (RAW / name, ASSETS / name):
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
    image = Image.open(source); outputs[name] = {"sha256": sha(source), "pixels": list(image.size)}


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v5.html").read_text()
    cards = "".join(f'<article><h3>{a.title()} · {s.title()}</h3><div class="cell"><img src="assets/{a}-{s}.png" alt="{a} {s}"></div></article>' for a, states in catalogue["states"].items() for s in states)
    options = "".join(f'<option value="{n}">{n.replace("-", " ").title()}</option>' for n in catalogue["effects"])
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__EFFECT_OPTIONS__", options).replace("__CARDS__", cards)


def main() -> None:
    v4 = json.loads(V4_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists(): shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS): directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name in v4["outputs"]: publish_copy(V4_RAW / name, name, outputs)

    catalogue = json.loads(json.dumps(v4)); catalogue.update({"set": SET, "version": 5, "status": "variable-speed-copy-corrected-workbench-awaiting-review", "outputs": outputs, "media": list(outputs)})
    catalogue["sourceProvenance"]["immutableV4Parent"] = {"set": V4_SET, "catalogueSha256": sha(V4_DRAFT)}
    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({"set": SET, "status": "awaiting-variable-speed-visual-review", "parent": V4_SET, "promotion": "none", "runtimeWiring": "unchanged", "rollback": "Delete V5 only; V4 remains immutable."}, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(catalogue['effectFamilies'])} families, {len(catalogue['effects'])} models, exact V4 media with corrected V5 review copy")


if __name__ == "__main__": main()
