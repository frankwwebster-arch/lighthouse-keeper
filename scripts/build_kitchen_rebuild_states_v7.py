#!/usr/bin/env python3
"""Build immutable V7 from V6 with an asset-first layered effect workbench."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SET = "kitchen-rebuild-states-2026-10-18-v7"
V6_SET = "kitchen-rebuild-states-2026-10-18-v6"
V6_RAW = ROOT / "art/raw" / V6_SET
V6_DRAFT = ROOT / "art/drafts" / V6_SET / "candidate-catalogue.json"
RAW = ROOT / "art/raw" / SET
DRAFT = ROOT / "art/drafts" / SET
SOURCE = ROOT / "art/source" / SET
PUBLIC = ROOT / "public/keeper-review/kitchen-rebuild-states-v7"
ASSETS = PUBLIC / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_page(catalogue: dict) -> str:
    template = (ROOT / "scripts/templates/kitchen_rebuild_states_v7.html").read_text()
    cards = "".join(
        f'<article><h3>{asset.title()} · {state.title()}</h3>'
        f'<div class="cell"><img src="assets/{asset}-{state}.png" alt="{asset} {state}"></div></article>'
        for asset, states in catalogue["states"].items()
        for state in states
    )
    return template.replace("__DATA__", json.dumps(catalogue, separators=(",", ":"))).replace("__CARDS__", cards)


def main() -> None:
    v6 = json.loads(V6_DRAFT.read_text())
    for directory in (RAW, DRAFT, SOURCE, PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    for directory in (RAW, DRAFT, SOURCE, ASSETS):
        directory.mkdir(parents=True, exist_ok=True)

    for name in v6["outputs"]:
        shutil.copyfile(V6_RAW / name, RAW / name)
        shutil.copyfile(V6_RAW / name, ASSETS / name)

    catalogue = json.loads(json.dumps(v6))
    catalogue.update({"set": SET, "version": 7, "status": "asset-first-multi-layer-workbench-awaiting-review"})
    catalogue["method"].update({
        "assetFirstLayerWorkbench": True,
        "multiInstanceEffects": True,
        "dragDropPlacement": True,
        "perLayerRemoval": True,
    })
    catalogue["sourceProvenance"]["immutableV6Parent"] = {
        "set": V6_SET,
        "catalogueSha256": sha(V6_DRAFT),
    }

    (SOURCE / "source-manifest.json").write_text(json.dumps(catalogue["sourceProvenance"], indent=2) + "\n")
    (DRAFT / "candidate-catalogue.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    (DRAFT / "batch-register.json").write_text(json.dumps({
        "set": SET,
        "status": "awaiting-asset-first-workbench-review",
        "parent": V6_SET,
        "promotion": "none",
        "runtimeWiring": "unchanged",
        "rollback": "Delete V7 only; V6 and all prior immutable evidence remain unchanged.",
    }, indent=2) + "\n")
    (PUBLIC / "index.html").write_text(build_page(catalogue))
    print(f"Built {SET}: {len(catalogue['effectFamilies'])} reusable families, {len(catalogue['effects'])} models, asset-first multi-instance placement")


if __name__ == "__main__":
    main()
