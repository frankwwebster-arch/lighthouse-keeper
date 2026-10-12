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
CORE = ROOT / "art/drafts/keeper-prime-core-transitions-2026-10-12-v1"
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


def draft_asset(name: str) -> dict:
    matches = sorted((CORE / "drafts").glob(f"{name}_f*.png"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one Keeper Prime Draft strip for {name}, found {len(matches)}")
    source = matches[0]
    sidecar_path = source.with_suffix(".json")
    sidecar = json.loads(sidecar_path.read_text())
    image = Image.open(source)
    expected = (sidecar["w"] * sidecar["density"] * sidecar["frames"], sidecar["h"] * sidecar["density"])
    if image.size != expected:
        raise RuntimeError(f"Keeper Prime Draft asset {name} disagrees with its sidecar")
    digest = sha256(source)
    target = PUBLIC / "assets/draft" / f"{name}-kp-v1-{digest[:16]}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return {
        "id": f"draft:{name}:kp-v1",
        "name": name,
        "file": f"/keeper-animation-workbench/assets/draft/{target.name}",
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
        "immutable": False,
    }


def final_item(name: str, direction: str) -> dict:
    left = direction == "left"
    return {
        "id": f"{name}-v2-final",
        "lane": "final",
        "name": name,
        "title": "Turn left profile to front" if left else "Turn right profile to front",
        "description": "Historical V2 approval retained immutably. Live route review later rejected its joins; it is not the Keeper Prime transition foundation.",
        "assetId": f"final:{name}:v2",
        "timeline": [{"id": f"frame-{index + 1}", "frame": index} for index in range(6)],
        "sectionLoops": [],
        "overallLoop": False,
        "transitionPolicy": "required",
        "transitionReason": "Every action begins with walk, stop and any required facing turn. The game engine extends only the walk from world placement.",
        "transitionRoute": [
            {
                "id": "walk",
                "role": "walk",
                "label": "Walk (runtime length)",
                "assetId": "runtime:keeper_walk_cycle",
                "frames": list(range(8)),
                "repeats": 1,
                "mirror": left,
                "distanceMode": "runtime-placement",
                "entryOcclusion": "door-right" if left else "door-left",
            },
            {
                "id": "stop",
                "role": "stop",
                "label": "Stop",
                "assetId": "runtime:keeper_walk_stop",
                "frames": list(range(5)),
                "repeats": 1,
                "mirror": left,
            },
            {
                "id": "turn",
                "role": "action",
                "label": "Action: turn",
                "assetId": f"final:{name}:v2",
                "frames": list(range(6)),
                "repeats": 1,
                "mirror": False,
            },
        ],
        "approval": {
            "approvedBy": "Frank",
            "approvedOn": "2026-10-12",
            "wording": APPROVAL_WORDING,
            "scope": "Approved for the workbench Final lane; canonical runtime promotion remains a separate decision.",
        },
        "sourceDraft": rel(V2),
        "tags": ["standard", "turn", "front-endpoint", "approved-v2", "historical", "superseded-route-foundation"],
    }


def segment(identifier: str, role: str, label: str, asset: str, frames: list[int], motion: list[float] | None = None, *, start_pose: str | None = None, end_pose: str | None = None) -> dict:
    value = {
        "id": identifier, "role": role, "label": label,
        "assetId": f"draft:{asset}:kp-v1", "frames": frames,
        "repeats": 1, "mirror": False,
    }
    if motion is not None:
        value["motion"] = motion
    if start_pose:
        value["startPose"] = start_pose
    if end_pose:
        value["endPose"] = end_pose
    return value


def keeper_prime_drafts() -> list[dict]:
    walk_frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4]
    walk_motion = [1.0] * len(walk_frames)
    stop_frames = [0, 1, 2, 3]
    stop_motion = [0.8, 0.55, 0.3, 0.0]
    start_frames = [3, 2, 1, 0]
    start_motion = [0.0, 0.3, 0.55, 0.8]
    restart_walk = [4, 3, 2, 1, 0, 7, 6, 5, 4]

    walk = segment("walk", "walk", "Walk — continuous root motion", "keeper_prime_walk_cycle", walk_frames, walk_motion, start_pose="standing-side-right", end_pose="standing-side-right")
    stop = segment("stop", "stop", "Decelerate to exact stop", "keeper_prime_walk_stop", stop_frames, stop_motion, start_pose="standing-side-right", end_pose="standing-side-right")
    hold = segment("stop-hold", "stop", "Exact Keeper Prime side stop", "keeper_prime_walk_stop", [3], [0.0], start_pose="standing-side-right", end_pose="standing-side-right")
    start = segment("walk-start", "stop", "Exact reverse: stop to walk", "keeper_prime_walk_stop", start_frames, start_motion, start_pose="standing-side-right", end_pose="walking-side-right")
    resume = segment("walk-resume", "walk", "Walk away — continuous root motion", "keeper_prime_walk_cycle", restart_walk, [1.0] * len(restart_walk), start_pose="walking-side-right", end_pose="standing-side-right")

    def item(identifier: str, title: str, description: str, asset: str, frames: list[int], route: list[dict], tags: list[str]) -> dict:
        return {
            "id": f"{identifier}-kp-v1-draft",
            "lane": "draft",
            "name": identifier,
            "title": title,
            "description": description,
            "assetId": f"draft:{asset}:kp-v1",
            "timeline": [{"id": f"{identifier}-frame-{index + 1}", "frame": frame} for index, frame in enumerate(frames)],
            "sectionLoops": [],
            "overallLoop": False,
            "transitionPolicy": "required",
            "transitionReason": "Keeper Prime Draft V1. Root motion continues through deceleration; shared stop/action endpoints are exact pixels.",
            "transitionRoute": route,
            "sourceDraft": rel(CORE),
            "tags": ["keeper-prime", "core-transition", "awaiting-approval", *tags],
            "updatedAt": "2026-10-12T00:00:00Z",
        }

    turn_front = segment("turn-front", "turn", "Turn to exact Keeper Prime full face", "keeper_prime_turn_front", list(range(6)), [0.0] * 6, start_pose="standing-side-right", end_pose="standing-front")
    turn_back = segment("turn-back", "turn", "Turn until completely back-facing", "keeper_prime_turn_back", list(range(6)), [0.0] * 6, start_pose="standing-side-right", end_pose="standing-back")
    sit = segment("sit", "action", "Sit from exact stop", "keeper_prime_sit_side", list(range(6)), [0.0] * 6, start_pose="standing-side-right", end_pose="sitting-side-right")
    stand = segment("stand", "action", "Exact reverse: sit to stop", "keeper_prime_stand_side", list(range(6)), [0.0] * 6, start_pose="sitting-side-right", end_pose="standing-side-right")

    return [
        item("keeper_prime_walk_to_stop", "1. Walk → stop", "A moving walk decelerates into the one exact Keeper Prime side stop; there are no stationary walking frames.", "keeper_prime_walk_stop", stop_frames, [walk, stop], ["walk", "stop"]),
        item("keeper_prime_stop_to_walk", "2. Stop → walk", "The exact stop reverses the same four transition frames, then joins a temporally reversed walk phase while root motion accelerates.", "keeper_prime_walk_stop", start_frames, [hold, start, resume], ["stop", "walk-start"]),
        item("keeper_prime_walk_turn_front", "3. Walk → stop → full face", "Walk, decelerate to the shared stop, then turn to the byte-identical Keeper Prime front selected from V2 frame 6.", "keeper_prime_turn_front", list(range(6)), [walk, stop, turn_front], ["turn", "front", "exact-endpoint"]),
        item("keeper_prime_walk_turn_back", "4. Walk → stop → fully away", "Walk, decelerate to the shared stop, then turn until the Keeper is completely back-facing.", "keeper_prime_turn_back", list(range(6)), [walk, stop, turn_back], ["turn", "back", "exact-endpoint"]),
        item("keeper_prime_walk_stop_sit", "5. Walk → stop → sit", "Walk and decelerate to the exact side stop before the seated action begins.", "keeper_prime_sit_side", list(range(6)), [walk, stop, sit], ["sit", "seated"]),
        item("keeper_prime_sit_stop_walk", "6. Sit → stop → walk", "Stand uses the exact reverse of the sit frames, lands on the shared stop, then reverses the stop transition and walks away.", "keeper_prime_stand_side", list(range(6)), [stand, hold, start, resume], ["stand", "walk-start", "exact-reverse"]),
    ]


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    required_runtime = [
        "keeper_walk_cycle",
        "keeper_walk_stop",
        "keeper_neutral_standing-front",
    ]
    assets = [runtime_asset(name, manifest) for name in required_runtime]
    assets.extend(final_turn_asset(name) for name in ("keeper_turn_front", "keeper_turn_left_front"))
    draft_names = (
        "keeper_prime_walk_cycle", "keeper_prime_walk_stop", "keeper_prime_turn_front",
        "keeper_prime_turn_back", "keeper_prime_sit_side", "keeper_prime_stand_side",
        "keeper_prime_neutral_standing-back",
    )
    assets.extend(draft_asset(name) for name in draft_names)
    draft_items = keeper_prime_drafts()
    catalogue = {
        "version": 1,
        "platformId": "keeper-animation-workbench",
        "title": "Keeper Animation Workbench",
        "updatedOn": "2026-10-12",
        "separateFrom": "/keeper-review/",
        "principles": {
            "final": "Approved, immutable source strips. Editing begins by copying an item to Draft.",
            "draft": "Non-destructive playback recipes may copy, remove and reorder frame references or repeat selected sections without changing source PNGs.",
            "transitions": "Every action must carry an inspectable walk → stop → optional facing turn → action ingress and a compatible action → stop → walk egress. Root motion continues through stop/start; the engine varies only walking distance from world placement.",
        },
        "lanes": {
            "final": [
                final_item("keeper_turn_front", "right"),
                final_item("keeper_turn_left_front", "left"),
            ],
            "draft": draft_items,
        },
        "assets": assets,
        "storage": {
            "drafts": "repository Keeper Prime proposals plus browser-local edits under keeper-animation-workbench:v2; export/import JSON is the portable handoff",
            "final": "repository catalogue only; browser tools never mutate Final records",
        },
        "featureContract": {
            "frameOperations": ["copy", "remove", "move-left", "move-right"],
            "playback": ["play", "pause", "restart", "overall-loop", "section-loop"],
            "transitionPreview": True,
            "transitionPolicies": ["required"],
            "ingressStages": ["walk", "moving-stop", "optional-turn", "action"],
            "egressStages": ["action", "exact-stop", "reversed-walk-start", "walk"],
            "coreReviewRoutes": ["walk-to-stop", "stop-to-walk", "walk-stop-turn-front", "walk-stop-turn-back", "walk-stop-sit", "sit-stop-walk"],
            "rootMotionPreview": "Per-frame motion continues through stop/start; no walking-on-the-spot preview frames.",
            "walkExtension": {
                "owner": "game-engine",
                "strategy": "deterministic-runtime-placement",
                "workbenchPreviewCycles": 1,
                "startVisibility": "hidden-behind-door",
                "firstVisibleState": "walking-mid-stride",
            },
            "futureSafe": "Timeline entries use stable IDs and asset/frame references; approved PNG bytes remain immutable.",
        },
        "provenance": {
            "v2Register": rel(V2 / "batch-register.json"),
            "v2RegisterSha256": sha256(V2 / "batch-register.json"),
            "keeperPrimeCoreRegister": rel(CORE / "batch-register.json"),
            "keeperPrimeCoreRegisterSha256": sha256(CORE / "batch-register.json"),
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
