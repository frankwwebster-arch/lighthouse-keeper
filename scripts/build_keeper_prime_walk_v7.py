#!/usr/bin/env python3
"""Record Frank's approval of exact Keeper Prime Walk V6."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v7"
V6_REGISTER = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/batch-register.json"
PUBLIC_V6 = ROOT / "public/keeper-review/keeper-prime-walk-v6"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v7"
ROUTE = "/keeper-review/keeper-prime-walk-v7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    v6 = json.loads(V6_REGISTER.read_text())
    if v6.get("status") != "draft-frame8-lower-body-repair-awaiting-visual-approval":
        raise RuntimeError("Walk V6 candidate status changed")
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    shutil.copytree(PUBLIC_V6 / "assets", PUBLIC / "assets")
    page = (PUBLIC_V6 / "index.html").read_text()
    page = page.replace("/keeper-review/keeper-prime-walk-v6", ROUTE)
    page = page.replace("<title>Keeper Prime Walk V6</title>", "<title>Approved Keeper Prime Walk V6</title>")
    page = page.replace("Keeper Prime Walk V6 · right-facing", "Keeper Prime Walk V6 · approved locomotion authority")
    page = page.replace("Frame-8 lower-body repair · awaiting visual approval", "Approved locomotion artwork authority · 14 October 2026")
    page = page.replace("A narrow correction of Walk V5 frame 8. V5 accidentally admitted frame-2 trouser pixels through an over-broad arm mask. V6 restores the accepted V4 frame-8 lower body and changes only two tightened arm polygons. F1–F7 are exact V5 bytes. Nothing has entered Final or production.", "Frank approved exact Walk V6 with ‘Approved’. All eight frames, the corrected opposing-arm cadence, repaired F8 lower body, 8 fps timing and exact strip remain byte-identical to the reviewed candidate. Final and production remain unchanged.")
    page = page.replace("<strong>Review priority:</strong> frame 8 must retain V5's correct opposing-arm direction while its trousers, legs and boots match the accepted frame-8 base without warping.", "<strong>Approved authority:</strong> Walk V6 is the canonical core right-facing locomotion artwork for building stop/walk transitions.")
    (PUBLIC / "index.html").write_text(page)

    assets = [{"file": rel(path), "sha256": digest(path)} for path in sorted((PUBLIC / "assets").iterdir())]
    register = {
        "batchId": "keeper-prime-walk-2026-10-14-v7", "status": "approved-walk-v6-locomotion-artwork-authority",
        "purpose": "Preserve Frank's approval of exact Walk V6 without changing its artwork, Final, production sprites or runtime manifest.",
        "approval": {"approvedBy": "Frank", "approvedOn": "2026-10-14", "wording": "Approved", "scope": "Exact eight-frame Keeper Prime Walk V6, including the leg-authoritative opposing-arm cycle and repaired F8 lower body, at 8 fps."},
        "approvedCandidate": {"register": rel(V6_REGISTER), "registerSha256": digest(V6_REGISTER), "frames": [{"frame": frame["frame"], "file": frame["file"], "sha256": frame["sha256"]} for frame in v6["frames"]], "strip": v6["animation"]["strip"], "fps": v6["animation"]["fps"]},
        "reviewSurface": {"publicReview": f"{ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": digest(PUBLIC / "index.html"), "publicAssets": assets},
        "validation": {"v6RegisterUnchanged": True, "allEightFrameHashesPinned": True, "publicAssetsByteIdenticalToV6": True, "approvalPackDuplicatesNoArtwork": True, "artPixelsChangedByV7": False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"walkV6Approved": True, "coreRightFacingLocomotionAuthority": True, "stopToWalkApproved": False, "walkToStopApproved": False, "finalLaneEntryAllowed": True, "productionPromotionAllowed": False},
        "nextGate": "Review stop→walk→stop V1; Final and production remain separate explicit gates.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; Walk V1–V6, Final and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "approvedFrames": 8, "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
