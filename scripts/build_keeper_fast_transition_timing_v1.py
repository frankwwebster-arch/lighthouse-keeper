#!/usr/bin/env python3
"""Build the approved Fast Timing V1 transition profile without changing art."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-fast-transition-timing-2026-10-14-v1"
SOURCE_CATALOGUE = ROOT / "public/keeper-timing-lab/catalog.json"
CATALOGUE = ROOT / "public/keeper-timing-lab/catalog-v2.json"
POLICY = ROOT / "data/keeper_timing_policy.json"
ROUTE_REGISTER = ROOT / "art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1/batch-register.json"
RUNTIME_MANIFEST = ROOT / "public/sprites/manifest.json"
WORKBENCH = ROOT / "data/keeper_animation_workbench.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    for path in [SOURCE_CATALOGUE, ROUTE_REGISTER, RUNTIME_MANIFEST, WORKBENCH, PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md"]:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")

    source = json.loads(SOURCE_CATALOGUE.read_text())
    if source.get("version") != 1 or len(source.get("clips", [])) != 1:
        raise RuntimeError("Timing Lab V1 catalogue is not the expected immutable source")

    fast = {"walkFps": 10, "decelerationFps": 12, "settleMs": 0, "turnFps": 16, "frontHoldMs": 625}
    approval = {
        "id": "keeper-fast-transition-timing-v1",
        "name": "Fast Timing V1",
        "status": "approved-transition-authority",
        "approvedOn": "2026-10-14",
        "approvalWording": "approve fast timing v1",
        "designDirection": "Movement between activities should run quickly for a mainly child audience; entertaining action animations remain independently timed and worth savouring.",
        "profile": fast,
        "appliesTo": [
            "steady standard locomotion",
            "walk acceleration",
            "walk deceleration",
            "facing turns",
            "brief transition endpoint holds",
        ],
        "excludes": [
            "action entry",
            "action loops",
            "action exit",
            "comic reactions",
            "prop choreography",
            "activity-specific performance timing",
        ],
        "policy": "Action animation timing is authored and approved per action; it never inherits Fast Timing V1 merely because it follows a transition.",
    }

    policy = {
        "version": 1,
        "policyId": approval["id"],
        "status": "approved-project-timing-policy",
        "approvedOn": approval["approvedOn"],
        "approvalWording": approval["approvalWording"],
        "transitionProfile": fast,
        "transitionScope": approval["appliesTo"],
        "actionTiming": {
            "inheritsTransitionProfile": False,
            "scope": approval["excludes"],
            "rule": approval["policy"],
            "intent": "Action animations should be entertaining to watch and may use slower cadence, anticipation, repetition and comic holds.",
        },
        "runtimeIntegration": {
            "implemented": False,
            "reason": "Keeper Prime authorities remain outside Workbench Final and production; consume this policy when the approved core routes are integrated.",
        },
    }
    dump(POLICY, policy)

    catalogue = json.loads(json.dumps(source))
    catalogue["version"] = 2
    catalogue["updatedOn"] = "2026-10-14"
    catalogue["principles"]["timing"] = "Fast Timing V1 is the project default for locomotion, stopping bridges and turns; action performance timing remains independent."
    catalogue["principles"]["approval"] = "Fast Timing V1 is approved for transitions only. Artwork, Workbench Final, production promotion and every action's timing retain separate gates."
    catalogue["principles"]["export"] = "Repository defaults are authoritative; device-local proposals remain private experiments until exported and explicitly approved."
    catalogue["defaults"] = fast
    catalogue["approvedTransitionProfile"] = approval
    catalogue["projectTimingPolicy"] = {"path": rel(POLICY), "sha256": digest(POLICY)}
    catalogue["presets"] = [
        {
            "id": "fast-transition-v1",
            "name": "Fast Timing V1 · approved",
            "description": "Project standard for brisk walks, stopping bridges and turns. It does not govern action animation timing.",
            "status": "approved",
            "profile": fast,
        },
        source["presets"][0],
        {
            **source["presets"][1],
            "name": "Earlier 10 fps proposal",
            "description": "Superseded review proposal retained as timing history.",
            "status": "superseded",
        },
        {
            **source["presets"][2],
            "name": "Earlier 12 fps comparison",
            "description": "Superseded comparison retained as timing history.",
            "status": "superseded",
        },
    ]
    clip = catalogue["clips"][0]
    clip["description"] = "Approved artwork sequence with approved Fast Timing V1 transition cadence."
    clip["status"] = "artwork-and-fast-transition-timing-approved"
    clip["recommended"] = fast
    clip["timingAuthority"] = approval["id"]

    dump(CATALOGUE, catalogue)

    record = {
        "batchId": "keeper-fast-transition-timing-2026-10-14-v1",
        "status": "approved-transition-timing-authority",
        "purpose": "Pin Frank's approved fast walk/stop/turn cadence while keeping action animations independently paced.",
        "approval": approval,
        "source": {
            "timingLabV1Catalogue": rel(SOURCE_CATALOGUE),
            "timingLabV1CatalogueSha256": digest(SOURCE_CATALOGUE),
            "routeRegister": rel(ROUTE_REGISTER),
            "routeRegisterSha256": digest(ROUTE_REGISTER),
        },
        "candidate": {
            "catalogue": rel(CATALOGUE),
            "catalogueSha256": digest(CATALOGUE),
            "projectTimingPolicy": rel(POLICY),
            "projectTimingPolicySha256": digest(POLICY),
            "profile": fast,
            "baselineDurationMs": 4000,
            "approvedDurationMs": 2995.833333333333,
            "durationReductionPercent": 25.10416666666667,
        },
        "immutableBoundaries": {
            "artworkPixelsChanged": False,
            "frameOrderChanged": False,
            "rootMotionChanged": False,
            "endpointContractChanged": False,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "workbenchFinalChanged": False,
            "actionTimingChanged": False,
        },
        "unchangedAuthorities": {
            "runtimeManifest": rel(RUNTIME_MANIFEST),
            "runtimeManifestSha256": digest(RUNTIME_MANIFEST),
            "workbenchCatalogue": rel(WORKBENCH),
            "workbenchCatalogueSha256": digest(WORKBENCH),
        },
        "promotionBoundary": "This approves the timing profile for locomotion and turns. It does not promote artwork to Workbench Final or production and does not approve any action animation timing.",
        "rollback": f"Delete {rel(PACK)} and {rel(CATALOGUE)}, then point the Timing Lab back to {rel(SOURCE_CATALOGUE)}. No sprite or runtime manifest rollback is required.",
    }
    dump(PACK / "approval-register.json", record)
    print(json.dumps({"batch": record["batchId"], "profile": fast, "catalogue": rel(CATALOGUE)}, indent=2))


if __name__ == "__main__":
    main()
