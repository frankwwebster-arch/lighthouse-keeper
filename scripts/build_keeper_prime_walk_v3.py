#!/usr/bin/env python3
"""Build the reversible Keeper Prime Walk V3 opposing-arm review draft."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import build_keeper_prime_walk_v1 as base


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v3"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-v3"
SELECTED = PACK / "sources/keeper-prime-walk-8pose-rig-guided.png"
REJECTED_1 = PACK / "sources/rejected-verbal-arm-pass-v1.png"
REJECTED_2 = PACK / "sources/rejected-verbal-arm-pass-v2.png"
REJECTED_3 = PACK / "sources/rejected-single-contact-arm-pass.png"
ADDITIONAL_REJECTS = (
    (PACK / "sources/rejected-bottom-row-arm-pass.png", "four-pose edit retained the same rear-arm depth ordering"),
    (PACK / "sources/rejected-single-f7-guide-pass.png", "single-frame guide retained the near arm in front"),
    (PACK / "sources/rejected-single-marching-pass.png", "marching-language edit retained the original arm ordering"),
    (PACK / "sources/rejected-fresh-rig-sheet-pass.png", "fresh full-sheet render still left the far arm static"),
    (PACK / "sources/rejected-opposite-contact-pass.png", "fresh opposite-contact render retained the near arm in front"),
)
GUIDE = PACK / "sources/rig-arm-overlay.png"
V1_REGISTER = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v1/batch-register.json"
V2_REGISTER = ROOT / "art/drafts/keeper-prime-walk-2026-10-13-v2/batch-register.json"
PUBLIC_PREFIX = "/keeper-review/keeper-prime-walk-v3/assets/"
FEEDBACK = "the arm swing isn't quite right, his left arm remains far more static than the right"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    for required in (SELECTED, REJECTED_1, REJECTED_2, REJECTED_3, *(path for path, _ in ADDITIONAL_REJECTS), GUIDE, V1_REGISTER, V2_REGISTER, PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md"):
        if not required.exists():
            raise RuntimeError(f"missing {rel(required)}")

    base.PACK = PACK
    base.PUBLIC = PUBLIC
    base.RAW = SELECTED
    base.REJECTED_INITIAL = REJECTED_1
    base.REJECTED_BACKGROUND = REJECTED_2
    base.main()

    register_path = PACK / "batch-register.json"
    register = json.loads(register_path.read_text())
    v1_register = json.loads(V1_REGISTER.read_text())
    previous_urls = []
    previous_records = []
    for index, frame in enumerate(v1_register["frames"], 1):
        source = ROOT / frame["file"]
        target = PUBLIC / "assets" / f"previous-v1-frame{index}-{digest(source)[:16]}.png"
        shutil.copyfile(source, target)
        previous_urls.append(f"{PUBLIC_PREFIX}{target.name}")
        previous_records.append({"frame": index, "source": rel(source), "sourceSha256": digest(source), "public": rel(target), "publicSha256": digest(target), "byteIdentical": digest(source) == digest(target)})
    register.update({
        "batchId": "keeper-prime-walk-2026-10-13-v3",
        "status": "draft-opposing-arm-walk-v3-awaiting-visual-approval",
        "purpose": "Correct Walk V1's under-animated far/left arm using the approved Rig Motion V3 as an explicit opposing-arm pose guide while preserving the eight-pose walk contract.",
        "userFeedback": FEEDBACK,
    })
    register["generation"]["mode"] = "built-in-image-generation-identity-preserve-with-approved-rig-arm-overlay"
    register["generation"]["rejectedSources"].append({
        "file": rel(REJECTED_3),
        "sha256": digest(REJECTED_3),
        "reason": "single-contact edit preserved the original arm relationship and was not used",
    })
    register["generation"]["rejectedSources"].extend(
        {"file": rel(path), "sha256": digest(path), "reason": reason}
        for path, reason in ADDITIONAL_REJECTS
    )
    register["generation"]["poseGuide"] = {
        "file": rel(GUIDE),
        "sha256": digest(GUIDE),
        "authority": rel(ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v3/motion/keeper-prime-rig-motion-v3.json"),
        "authoritySha256": digest(ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v3/motion/keeper-prime-rig-motion-v3.json"),
        "nearArmColour": "cyan",
        "farArmColour": "magenta",
        "retainedInFinalPixels": False,
    }
    register["priorCandidates"] = {
        "walkV1": {"register": rel(V1_REGISTER), "sha256": digest(V1_REGISTER), "artworkChanged": False},
        "walkV2RoutingWrapper": {"register": rel(V2_REGISTER), "sha256": digest(V2_REGISTER), "artworkChanged": False},
    }
    register["previousWalkV1FrameComparison"] = previous_records
    register["validation"]["approvedRigOpposingArmGuideUsed"] = True
    register["validation"]["walkV1FilesChanged"] = False
    register["approvalBoundary"] = {
        "walkV3Approved": False,
        "walkStopApproved": False,
        "finalLaneEntryAllowed": False,
        "productionPromotionAllowed": False,
    }
    register["nextGate"] = "Frank visually reviews whether both arms now swing naturally in opposition before any walk-to-stop frames are authored."
    register["rollback"] = f"Delete only {rel(PACK)} and {rel(PUBLIC)}; Walk V1/V2, approved authorities, production sprites, manifests and prior drafts remain unchanged."

    html_path = PUBLIC / "index.html"
    html = html_path.read_text()
    html = html.replace("Keeper Prime Walk V1", "Keeper Prime Walk V3")
    html = html.replace("Walk V1 review draft", "Walk V3 opposing-arm draft")
    html = html.replace("Walk V1 review strip", "Walk V3 opposing-arm strip")
    html = html.replace("Current production versus Walk V1", "Current production versus Walk V3")
    html = html.replace("assets/", PUBLIC_PREFIX)
    comparison = f'''<h2>Walk V1 versus Walk V3 · same frame</h2><article><div class="route-pair"><div><strong>Previous Walk V1</strong><div class="stage game"><img id="previousFrame" src="{previous_urls[0]}" alt="Previous Walk V1 synchronized frame"></div></div><div><strong>Walk V3 arm correction</strong><div class="stage game"><img id="currentCompare" src="{PUBLIC_PREFIX}{next(path.name for path in (PUBLIC / 'assets').iterdir() if path.name.startswith('frame1-'))}" alt="Walk V3 synchronized frame"></div></div></div><p>Both boxes are exact 128 × 160 proposed game size and follow the same frame index.</p></article>'''
    html = html.replace("<h2>Translated walk — begins and ends fully hidden</h2>", comparison + "<h2>Translated walk — begins and ends fully hidden</h2>")
    html = html.replace(
        "Finished-art walk draft · awaiting visual approval",
        "Opposing-arm walk correction · awaiting visual approval",
    )
    html = html.replace(
        "One coherent eight-pose loop derived from the approved Side-right model and Rig Motion V3. Nothing has entered Final or production.",
        "A new eight-pose render guided by the approved Rig Motion V3 opposing arm paths. Walk V1/V2 remain immutable; nothing has entered Final or production.",
    )
    html = html.replace(
        "identity and palette must remain constant while the legs and arms move.",
        "both arms must now swing visibly and naturally in opposition while identity, legs and palette remain constant.",
    )
    previous_json = json.dumps(previous_urls)
    html = html.replace("const frames=", f"const previousFrames={previous_json};const frames=")
    html = html.replace("function show(i){index=", "function show(i){index=")
    html = html.replace("label.textContent=`Frame ${index+1}", "document.getElementById('previousFrame').src=previousFrames[index];document.getElementById('currentCompare').src=frames[index];label.textContent=`Frame ${index+1}")
    html_path.write_text(html)
    register["reviewPage"] = {"file": rel(html_path), "sha256": digest(html_path), "assetPrefix": PUBLIC_PREFIX, "relativeAssetUrls": False}
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"batch": register["batchId"], "frames": 8, "publicPage": rel(html_path), "selectedSourceSha256": digest(SELECTED)}, indent=2))


if __name__ == "__main__":
    main()
