#!/usr/bin/env python3
"""Build the Keeper Timing Lab V1 catalogue and timing-only proposal record."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-timing-lab-2026-10-14-v1"
CATALOGUE = ROOT / "public/keeper-timing-lab/catalog.json"
ROUTE_REGISTER = ROOT / "art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1/batch-register.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    for path in [ROUTE_REGISTER, PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md"]:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    route_record = json.loads(ROUTE_REGISTER.read_text())
    phase_map = {
        "approved walk": "walk",
        "approved deceleration": "deceleration",
        "neutral settle": "settle",
        "approved turn to camera": "turn",
        "front hold": "frontHold",
    }
    frames = []
    for index, frame in enumerate(route_record["route"]["framesData"], 1):
        frames.append({
            "id": f"route-f{index}", "src": frame["src"], "phase": phase_map[frame["phase"]],
            "phaseLabel": frame["phase"], "pose": frame["pose"], "dx": frame["dx"], "x": frame["x"],
        })

    baseline = {"walkFps": 8, "decelerationFps": 8, "settleMs": 125, "turnFps": 8, "frontHoldMs": 500}
    recommended = {"walkFps": 8, "decelerationFps": 8, "settleMs": 125, "turnFps": 10, "frontHoldMs": 500}
    catalogue = {
        "version": 1,
        "platformId": "keeper-timing-lab",
        "title": "Keeper Timing Lab",
        "updatedOn": "2026-10-14",
        "principles": {
            "artwork": "Approved frame bytes and frame order are immutable; timing proposals reference them without editing pixels.",
            "timing": "Walk, deceleration, settle, turn and endpoint holds are independently tunable.",
            "approval": "Visual artwork approval and timing-profile approval are separate gates; Final and production remain separate again.",
            "export": "Saved proposals are device-local until exported as JSON and committed as a versioned timing record.",
        },
        "defaults": recommended,
        "presets": [
            {"id": "approved-baseline", "name": "Reviewed V1 timing", "description": "Exact timing shown in the excellent V1 review.", "profile": baseline},
            {"id": "quicker-turn", "name": "Quicker turn · recommended", "description": "Keeps walk, stop and settle unchanged; increases only the turn from 8 to 10 fps.", "profile": recommended},
            {"id": "crisp-turn", "name": "Crisp turn", "description": "A stronger comparison at 12 fps; useful as an upper bound rather than a default.", "profile": {**recommended, "turnFps": 12}},
        ],
        "clips": [{
            "id": "keeper-prime-walk-stop-turn-front-v1",
            "title": "Walk → stop → turn to camera",
            "description": "Approved artwork sequence; timing remains tunable.",
            "outfit": "standard",
            "status": "artwork-excellent-timing-under-review",
            "sourceRegister": rel(ROUTE_REGISTER),
            "sourceRegisterSha256": digest(ROUTE_REGISTER),
            "baseline": baseline,
            "recommended": recommended,
            "frames": frames,
            "distanceHighResolutionPixels": route_record["route"]["distanceHighResolutionPixels"],
            "artworkAuthorities": route_record["authorities"],
            "endpointContract": route_record["endpointContract"],
            "acceptedVisualLimitation": route_record["authorities"]["frontSideTurn"]["acceptedLimitation"],
        }],
        "loopSections": [
            {"id": "all", "label": "Complete route", "phases": ["walk", "deceleration", "settle", "turn", "frontHold"]},
            {"id": "walk", "label": "Walk only", "phases": ["walk"]},
            {"id": "stop", "label": "Walk exit → stopped", "phases": ["deceleration", "settle"]},
            {"id": "stop-turn", "label": "Stopped → full face", "phases": ["settle", "turn"]},
            {"id": "turn", "label": "Turn only", "phases": ["turn"]},
        ],
    }
    dump(CATALOGUE, catalogue)
    register = {
        "batchId": "keeper-timing-lab-2026-10-14-v1",
        "status": "timing-platform-v1-and-quicker-turn-proposal",
        "purpose": "Separate immutable Keeper artwork authority from tunable motion timing and make timing review reusable across core and action routes.",
        "feedback": {"recordedOn": "2026-10-14", "wording": "it's excellent, but the turn could run a little faster - and it's little things like the speed of any given animation that makes me think we need an overall tuning platform, not just building and approving as concrete."},
        "sourceRoute": {"register": rel(ROUTE_REGISTER), "registerSha256": digest(ROUTE_REGISTER), "artworkPixelsChanged": False, "frameOrderChanged": False, "rootMotionChanged": False},
        "timingProposal": {"baseline": baseline, "recommended": recommended, "onlyChangedField": "turnFps", "from": 8, "to": 10, "turnDurationReductionPercent": 20},
        "platform": {"route": "/keeper-timing-lab", "catalogue": rel(CATALOGUE), "catalogueSha256": digest(CATALOGUE), "features": ["phase-specific timing", "baseline-versus-proposal playback", "large-and-game-scale preview", "section loops", "frame stepping", "presets", "device-local saved proposals", "project defaults", "JSON export", "immutable authority display"]},
        "validation": {"sourceRouteUnchanged": True, "approvedArtworkReferencedOnly": True, "timingIndependentOfArtwork": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"routeArtworkAcceptedAsExcellent": True, "recommendedTimingApproved": False, "timingPlatformApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank tunes or approves the 10 fps turn proposal in Keeper Timing Lab; exported settings become the next versioned timing record without changing artwork.",
        "rollback": f"Delete only {rel(PACK)}, {rel(CATALOGUE)} and the timing-lab application files; the V1 route and every approved source authority remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "clips": len(catalogue["clips"]), "defaultTurnFps": recommended["turnFps"], "route": register["platform"]["route"]}, indent=2))


if __name__ == "__main__":
    main()
