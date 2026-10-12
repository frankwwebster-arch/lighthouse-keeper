#!/usr/bin/env python3
"""Build the separate Draft/Final Keeper animation workbench catalogue."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "public/sprites/manifest.json"
V2 = ROOT / "art/drafts/keeper-full-face-standard-turn-redraw-2026-10-12-v2"
PUBLIC = ROOT / "public/keeper-animation-workbench"
DATA_PATH = ROOT / "data/keeper_animation_workbench.json"
APPROVAL_WORDING = "I am very happy with your V2."


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def runtime_asset(name: str, manifest: dict) -> dict:
    record = manifest[name]
    if isinstance(record, str):
        raise RuntimeError(f"runtime asset {name} has legacy string metadata")
    path = ROOT / "public/sprites" / record["file"]
    image = Image.open(path)
    density = record.get("density", 1)
    expected = (record["w"] * density * record.get("frames", 1), record["h"] * density)
    if image.size != expected:
        raise RuntimeError(f"runtime asset {name} disagrees with manifest: {image.size} != {expected}")
    return {
        "id": f"runtime:{name}",
        "name": name,
        "file": f"/sprites/{record['file']}",
        "sha256": sha256(path),
        "w": record["w"],
        "h": record["h"],
        "frames": record.get("frames", 1),
        "fps": record.get("fps", 0),
        "density": density,
        "anchor": record.get("anchor", [round(record["w"] / 2), record["h"]]),
        "startPose": record.get("startPose"),
        "endPose": record.get("endPose"),
        "outfit": record.get("outfit", "standard"),
        "loop": record.get("loop", False),
        "mirrorSafe": record.get("mirrorSafe", False),
        "source": "production-runtime-context",
        "immutable": True,
    }


def final_turn_asset(name: str) -> dict:
    source = V2 / "drafts" / name / f"{name}_f6.png"
    sidecar_path = V2 / "drafts" / name / f"{name}_f6.json"
    sidecar = json.loads(sidecar_path.read_text())
    image = Image.open(source)
    expected = (sidecar["w"] * sidecar["density"] * sidecar["frames"], sidecar["h"] * sidecar["density"])
    if image.size != expected:
        raise RuntimeError(f"approved V2 asset {name} disagrees with sidecar")
    digest = sha256(source)
    target = PUBLIC / "assets/final" / f"{name}-v2-{digest[:16]}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return {
        "id": f"final:{name}:v2",
        "name": name,
        "file": f"/keeper-animation-workbench/assets/final/{target.name}",
        "sha256": digest,
        "w": sidecar["w"],
        "h": sidecar["h"],
        "frames": sidecar["frames"],
        "fps": sidecar["fps"],
        "density": sidecar["density"],
        "anchor": sidecar["anchor"],
        "startPose": sidecar["startPose"],
        "endPose": sidecar["endPose"],
        "outfit": "standard",
        "loop": sidecar["loop"],
        "mirrorSafe": sidecar.get("mirrorSafe", False),
        "source": rel(source),
        "sourceSidecar": rel(sidecar_path),
        "sourceSidecarSha256": sha256(sidecar_path),
        "immutable": True,
    }


def final_item(name: str, direction: str) -> dict:
    left = direction == "left"
    return {
        "id": f"{name}-v2-final",
        "lane": "final",
        "name": name,
        "title": "Turn left profile to front" if left else "Turn right profile to front",
        "description": "Approved V2 complete moving-model redraw with an exact canonical front endpoint.",
        "assetId": f"final:{name}:v2",
        "timeline": [{"id": f"frame-{index + 1}", "frame": index} for index in range(6)],
        "sectionLoops": [],
        "overallLoop": False,
        "transitionPolicy": "required",
        "transitionReason": "Standard-uniform movement remains visible; walk, stop, turn and arrival must read as one continuous route.",
        "transitionRoute": [
            {
                "id": "walk",
                "label": "Walk",
                "assetId": "runtime:keeper_walk_cycle",
                "frames": list(range(8)),
                "repeats": 2,
                "mirror": left,
            },
            {
                "id": "stop",
                "label": "Stop",
                "assetId": "runtime:keeper_walk_stop",
                "frames": list(range(5)),
                "repeats": 1,
                "mirror": left,
            },
            {
                "id": "turn",
                "label": "Turn",
                "assetId": f"final:{name}:v2",
                "frames": list(range(6)),
                "repeats": 1,
                "mirror": False,
            },
            {
                "id": "arrive",
                "label": "Front idle",
                "assetId": "runtime:keeper_neutral_standing-front",
                "frames": [0],
                "repeats": 4,
                "mirror": False,
                "fps": 4,
            },
        ],
        "approval": {
            "approvedBy": "Frank",
            "approvedOn": "2026-10-12",
            "wording": APPROVAL_WORDING,
            "scope": "Approved for the workbench Final lane; canonical runtime promotion remains a separate decision.",
        },
        "sourceDraft": rel(V2),
        "tags": ["standard", "turn", "front-endpoint", "approved-v2"],
    }


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    required_runtime = [
        "keeper_walk_cycle",
        "keeper_walk_stop",
        "keeper_neutral_standing-front",
    ]
    assets = [runtime_asset(name, manifest) for name in required_runtime]
    assets.extend(final_turn_asset(name) for name in ("keeper_turn_front", "keeper_turn_left_front"))
    catalogue = {
        "version": 1,
        "platformId": "keeper-animation-workbench",
        "title": "Keeper Animation Workbench",
        "updatedOn": "2026-10-12",
        "separateFrom": "/keeper-review/",
        "principles": {
            "final": "Approved, immutable source strips. Editing begins by copying an item to Draft.",
            "draft": "Non-destructive playback recipes may copy, remove and reorder frame references or repeat selected sections without changing source PNGs.",
            "transitions": "Every visible same-costume action must carry an inspectable walk → stop → optional turn → action/recovery route. Door-hidden costume changes are explicitly exempt.",
        },
        "lanes": {
            "final": [
                final_item("keeper_turn_front", "right"),
                final_item("keeper_turn_left_front", "left"),
            ],
            "draft": [],
        },
        "assets": assets,
        "storage": {
            "drafts": "browser-local under keeper-animation-workbench:v1; export/import JSON is the portable handoff",
            "final": "repository catalogue only; browser tools never mutate Final records",
        },
        "featureContract": {
            "frameOperations": ["copy", "remove", "move-left", "move-right"],
            "playback": ["play", "pause", "restart", "overall-loop", "section-loop"],
            "transitionPreview": True,
            "transitionPolicies": ["required", "door-hidden"],
            "futureSafe": "Timeline entries use stable IDs and asset/frame references; approved PNG bytes remain immutable.",
        },
        "provenance": {
            "v2Register": rel(V2 / "batch-register.json"),
            "v2RegisterSha256": sha256(V2 / "batch-register.json"),
            "runtimeManifest": rel(MANIFEST_PATH),
            "runtimeManifestSha256": sha256(MANIFEST_PATH),
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
        },
    }
    write_json(DATA_PATH, catalogue)
    write_json(PUBLIC / "catalog.json", catalogue)
    print(json.dumps({
        "platform": catalogue["platformId"],
        "finalCount": len(catalogue["lanes"]["final"]),
        "draftCount": len(catalogue["lanes"]["draft"]),
        "publicCatalogue": rel(PUBLIC / "catalog.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
