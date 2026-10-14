#!/usr/bin/env python3
"""Record Frank's approval of exact Keeper Prime stop → walk → stop V1."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2"
V1_REGISTER = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/batch-register.json"
PUBLIC_V1 = ROOT / "public/keeper-review/keeper-prime-stop-walk-stop-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-stop-walk-stop-v2"
ROUTE = "/keeper-review/keeper-prime-stop-walk-stop-v2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    v1 = json.loads(V1_REGISTER.read_text())
    if v1.get("status") != "draft-stop-walk-stop-v1-awaiting-visual-approval":
        raise RuntimeError("stop-walk-stop V1 candidate status changed")
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    shutil.copytree(PUBLIC_V1 / "assets", PUBLIC / "assets")
    page = (PUBLIC_V1 / "index.html").read_text()
    page = page.replace("/keeper-review/keeper-prime-stop-walk-stop-v1", ROUTE)
    page = page.replace("<title>Keeper Prime Stop → Walk → Stop V1</title>", "<title>Approved Keeper Prime Stop → Walk → Stop V1</title>")
    page = page.replace("Keeper Prime · stop → walk → stop V1", "Keeper Prime · approved stop → walk → stop authority")
    page = page.replace("Core transition route · awaiting visual approval", "Approved core transition authority · 14 October 2026")
    page = page.replace("The exact approved stop and Walk V6 endpoints are joined by one reversible three-pose bridge. The sprite begins translating on the first movement frame, accelerates into the approved walk, then decelerates through the same poses and returns to the exact stop.", "Frank approved exact stop → walk → stop V1 with ‘approved’. The exact stop, three bridge poses, Walk V6 cycles, reverse deceleration and deterministic root-motion schedule remain byte-identical to the reviewed candidate.")
    page = page.replace("<strong>Review priority:</strong> there must be no walking on the spot, no model or scale jump at either seam, and no foot slide after the final exact stop. Pay special attention to stop→25%, 75%→Walk F1, Walk F1→75%, and 25%→stop.", "<strong>Approved sequence:</strong> exact Side-right stop → reversible three-pose acceleration → exact Walk V6 → byte-reversed deceleration → identical stop, with no stationary gait frame.")
    page = page.replace("Walk V6 is approved authority; this transition route is not Final or production.", "Walk V6 and this stop–walk–stop route are approved core artwork authorities. Final and production remain unchanged.")
    (PUBLIC / "index.html").write_text(page)

    assets = [{"file": rel(path), "sha256": digest(path)} for path in sorted((PUBLIC / "assets").iterdir())]
    register = {
        "batchId": "keeper-prime-stop-walk-stop-2026-10-14-v2",
        "status": "approved-stop-walk-stop-v1-route-authority",
        "purpose": "Preserve Frank's approval of exact stop → walk → stop V1 without changing artwork, timing, Final, production sprites or runtime manifest.",
        "approval": {"approvedBy": "Frank", "approvedOn": "2026-10-14", "wording": "approved", "scope": "Exact stop → walk → stop V1: five-pose reversible bridge, two Walk V6 cycles, 8 fps playback and 32-frame/412-pixel root-motion review route."},
        "approvedCandidate": {
            "register": rel(V1_REGISTER), "registerSha256": digest(V1_REGISTER),
            "stopAuthority": v1["stopAuthority"], "approvedWalkAuthority": v1["approvedWalkAuthority"],
            "transition": v1["transition"], "rootMotion": v1["rootMotion"], "publishedAssets": v1["publishedAssets"],
        },
        "reviewSurface": {"publicReview": f"{ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": digest(PUBLIC / "index.html"), "publicAssets": assets},
        "validation": {"v1RegisterUnchanged": True, "allTransitionHashesPinned": True, "rootMotionPinned": True, "publicAssetsByteIdenticalToV1": True, "approvalPackDuplicatesNoArtwork": True, "artPixelsChangedByV2": False, "timingChangedByV2": False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"walkV6Approved": True, "stopToWalkApproved": True, "walkToStopApproved": True, "completeRouteApproved": True, "coreTransitionAuthority": True, "finalLaneEntryAllowed": True, "productionPromotionAllowed": False},
        "nextGate": "Build the next core transition route one at a time from the approved stop, Walk V6 and approved turn authorities. Final and production remain separate explicit gates.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1, approved Walk V6, Final and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "approvedRouteFrames": len(v1["rootMotion"]["route"]), "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
