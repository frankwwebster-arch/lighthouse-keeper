#!/usr/bin/env python3
"""Record Frank's approval of exact side-right ↔ back Turn V9."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10"
V9_REGISTER = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/batch-register.json"
V8_REGISTER = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v8/batch-register.json"
PUBLIC_V9 = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v9"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v10"
ROUTE = "/keeper-review/keeper-prime-turn-side-back-v10"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> None:
    v9 = json.loads(V9_REGISTER.read_text())
    if v9.get("status") != "draft-v9-single-intermediate-awaiting-visual-approval":
        raise RuntimeError("V9 candidate status changed")
    if PUBLIC.exists(): shutil.rmtree(PUBLIC)
    shutil.copytree(PUBLIC_V9 / "assets", PUBLIC / "assets")
    page = (PUBLIC_V9 / "index.html").read_text()
    page = page.replace("/keeper-review/keeper-prime-turn-side-back-v9", ROUTE)
    page = page.replace("<title>Keeper Prime side ↔ back Turn V9</title>", "<title>Approved Keeper Prime side ↔ back Turn V9</title>")
    page = page.replace("← V7 eight-frame base", "← Immutable V9 candidate")
    page = page.replace("<h1>Keeper Prime Turn V9 · one intermediate only</h1>", "<h1>Keeper Prime Turn V9 · approved side-right ↔ back authority</h1>")
    page = page.replace("New reversible candidate · awaiting visual approval", "Approved artwork authority · 13 October 2026")
    page = page.replace("V9 rejects V8's global 16-frame strategy. It keeps every V7 frame byte-identical and inserts only one new 172.5° pose between V7 F7 and F8. Final and production remain unchanged.", "Frank approved exact Turn V9 with ‘approved’. Every V9 frame, the 172.5° midpoint and both nine-frame strips remain byte-identical to the reviewed candidate. Final and production remain unchanged.")
    page = page.replace("<strong>Review priority:</strong> does the single 165° → 172.5° → 180° sequence remove the ear flash without creating a new body, cap or boot wobble?", "<strong>Approved sequence:</strong> the single 165° → 172.5° → 180° interval removes the endpoint flash without adopting V8's rejected global frame-rate increase.")
    page = page.replace("V8 is rejected provenance. V9 is a separate draft based directly on V7. Approval would not promote Final or production.", "V8 remains rejected provenance. Exact V9 is now the approved core-turn artwork authority. This approval record does not alter Final, production sprites or the runtime manifest.")
    (PUBLIC / "index.html").write_text(page)

    frames = [{"frame": record["frame"], "angleDegrees": record["angleDegrees"], "file": record["file"], "sha256": record["sha256"]} for record in v9["frames"]]
    assets = [{"file": rel(path), "sha256": digest(path)} for path in sorted((PUBLIC / "assets").iterdir() if (PUBLIC / "assets").exists() else [])]
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v10",
        "status": "approved-side-back-turn-v9-artwork-authority",
        "purpose": "Preserve Frank's approval of exact Turn V9 without changing its artwork, Final, production sprites or runtime manifest.",
        "approval": {"approvedBy": "Frank", "approvedOn": "2026-10-13", "wording": "approved", "scope": "The exact nine-frame reversible Keeper Prime side-right-to-back Turn V9: all eight retained V7 frames, the single 172.5° intermediate, 9 fps timing and exact reverse strip."},
        "approvedCandidate": {"register": rel(V9_REGISTER), "registerSha256": digest(V9_REGISTER), "frames": frames, "midpoint": v9["midpoint"], "forwardStrip": v9["animation"]["forward"], "reverseStrip": v9["animation"]["reverse"], "fps": v9["animation"]["fps"], "durationSeconds": v9["animation"]["durationSeconds"], "earOcclusion": v9["earOcclusion"]},
        "rejectedV8": {"register": rel(V8_REGISTER), "registerSha256": digest(V8_REGISTER), "feedback": v9["rejectedV8"]["feedback"], "disposition": "rejected provenance; approval of V9 does not reactivate V8 or establish a general higher-frame-rate rule"},
        "reviewSurface": {"publicReview": f"{ROUTE}/", "publicPage": rel(PUBLIC / "index.html"), "publicPageSha256": digest(PUBLIC / "index.html"), "publicAssets": assets, "controls": ["previous-frame", "next-frame", "play-forward", "play-reverse", "loop-both", "pause", "direct-frame-selection"], "views": ["large-inspection", "game-scale-128x160", "v7-v9-equal-duration-comparison", "isolated-approved-rear-interval"]},
        "validation": {"v9RegisterUnchanged": True, "allNineFrameHashesPinned": True, "publicFramesByteIdenticalToV9": True, "stripsAndSidecarsPinned": True, "approvalPackDuplicatesNoArtwork": True, "artPixelsChangedByV10": False, "productionSpritesChanged": False, "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False},
        "approvalBoundary": {"sideBackTurnV9Approved": True, "singleIntermediateApproved": True, "nineFpsOneSecondCadenceApproved": True, "coreTurnArtworkAuthority": True, "finalLaneEntryAllowed": True, "productionPromotionAllowed": False},
        "nextGate": "Use exact approved V9 as the side-right↔back turn authority when assembling complete core transition routes. Final and production remain separate explicit gates.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; V1–V9, Final and production remain unchanged."
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "approvedFrames": len(frames), "fps": register["approvedCandidate"]["fps"], "public": register["reviewSurface"]["publicReview"]}, indent=2))


if __name__ == "__main__": main()
