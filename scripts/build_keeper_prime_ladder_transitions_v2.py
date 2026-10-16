#!/usr/bin/env python3
"""Build Ladder Transition V2 without changing any V1 artwork bytes."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1_SET = "keeper-prime-ladder-transitions-v1"
SET = "keeper-prime-ladder-transitions-v2"
V1_PACK = ROOT / "art/drafts/keeper-prime-ladder-transitions-2026-10-16-v1"
PACK = ROOT / "art/drafts/keeper-prime-ladder-transitions-2026-10-16-v2"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"

V1_SPEC_FILE = V1_PACK / "keeper-prime-ladder-transitions-v1.json"
V1_REGISTER_FILE = V1_PACK / "batch-register.json"
V1_PAGE_FILE = ROOT / "public/keeper-review" / V1_SET / "index.html"
SPEC_FILE = PACK / "keeper-prime-ladder-transitions-v2.json"
PAGE_FILE = PUBLIC / "index.html"

TURN_MS = 50
CLIMB_MS = 150
LADDER_ASSETS = {
    "contactA",
    "passingA",
    "contactB",
    "passingB",
    "mount",
    "dismountRight",
    "dismountLanded",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


for required in (V1_SPEC_FILE, V1_REGISTER_FILE, V1_PAGE_FILE):
    if not required.exists():
        raise FileNotFoundError(required)

v1_spec = json.loads(V1_SPEC_FILE.read_text())
v1_register = json.loads(V1_REGISTER_FILE.read_text())
spec = copy.deepcopy(v1_spec)
spec["set"] = SET
spec["timing"] = {
    "turnFrameDurationMs": TURN_MS,
    "turnFps": 1000 / TURN_MS,
    "climbFrameDurationMs": CLIMB_MS,
    "climbFps": 1000 / CLIMB_MS,
    "decision": "faster mounting/landing turns and substantially slower rung-to-rung climbing",
}
spec["layering"] = {
    "orderBackToFront": ["ladder", "central-rung-body-occluder", "keeper", "floor", "door", "guides"],
    "centralRungOccluderWidthLp": 12,
    "centralRungOccluderHeightLp": 38,
    "purpose": "prevent central rung segments flashing through transparent gaps while the Keeper turns or climbs; side rails remain visible",
}

PACK.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

old_to_new_url: dict[str, str] = {}
published: list[dict[str, object]] = []
for entry in v1_register["publishedAssets"]:
    source = ROOT / entry["source"]
    if not source.exists():
        raise FileNotFoundError(source)
    digest = sha256(source)
    if digest != entry["sourceSha256"]:
        raise ValueError(f"V1 source drift: {source}")
    filename = Path(entry["published"]).name
    target = ASSETS / filename
    shutil.copyfile(source, target)
    new_url = f"/keeper-review/{SET}/assets/{filename}"
    old_to_new_url[entry["url"]] = new_url
    published.append({
        "source": relative(source),
        "sourceSha256": digest,
        "published": relative(target),
        "url": new_url,
        "bytes": source.stat().st_size,
        "byteIdenticalToV1": True,
    })

for route in spec["routes"].values():
    for frame in route["frames"]:
        frame["src"] = old_to_new_url[frame["src"]]
        source_frame = frame["sourceFrame"]
        if source_frame.startswith("turn"):
            frame["durationMs"] = TURN_MS
        elif source_frame in LADDER_ASSETS:
            frame["durationMs"] = CLIMB_MS
        if abs(frame["xLp"] - 104) <= 7 and (
            source_frame.startswith("turn")
            or source_frame == "back"
            or source_frame in LADDER_ASSETS
        ):
            frame["ladderOcclusion"] = "central-body"

write_json(SPEC_FILE, spec)

html = V1_PAGE_FILE.read_text()
html = html.replace("Keeper Prime ladder transitions V1", "Keeper Prime ladder transitions V2")
html = html.replace(
    "Prime-derived finished-art proposal for approach, exact eight-rung ascent, continuous climbing and a controlled upper-landing dismount.",
    "Timing and layering correction of V1: faster turns, slower climbing, and no central-rung flash through the Keeper. Every character pixel is unchanged.",
)
html = html.replace(
    "Four exact mirrored left/right gait cycles close the storey without phase remainder. The lower door is 84 lp—eight walking intervals—from the ladder.",
    "Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns now run at 20 fps and climbing at 6.67 fps; V1 artwork and geometry are unchanged.",
)
html = html.replace(
    ".rail,.rung{position:absolute;background:#bd925b;border:1px solid #65482b;z-index:2}",
    ".rail,.rung{position:absolute;background:#bd925b;border:1px solid #65482b;z-index:2}.rungOccluder{position:absolute;background:linear-gradient(#173440,#102833);background-repeat:no-repeat;z-index:3}",
)
old_architecture = "function architecture(world,scale,frame){world.innerHTML='';const add=(className,left,top,width,height)=>{const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e};const offset=frame.ladderOffsetLp||0;add('rail',95,4,1.5,112);add('rail',111.5,4,1.5,112);for(let y=3.5+offset;y<=116;y+=7.5)add('rung',95,y,18,1);add('floor',0,116,172,16);add('floor',0,56,95,4);add('floor',113,56,59,4);if(routeId==='approach'||routeId==='full')add('door',8,68,24,48);if(routeId==='exit'||routeId==='full')add('door',158,8,14,48)}"
new_architecture = "function architecture(world,scale,frame){world.innerHTML='';const add=(className,left,top,width,height)=>{const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e};const offset=frame.ladderOffsetLp||0;add('rail',95,4,1.5,112);add('rail',111.5,4,1.5,112);for(let y=3.5+offset;y<=116;y+=7.5)add('rung',95,y,18,1);if(frame.ladderOcclusion==='central-body'){const top=frame.rootYLp-38,shield=add('rungOccluder',frame.xLp-6,top,12,38);shield.style.backgroundSize=`100% ${132*scale}px`;shield.style.backgroundPosition=`0 ${-top*scale}px`}add('floor',0,116,172,16);add('floor',0,56,95,4);add('floor',113,56,59,4);if(routeId==='approach'||routeId==='full')add('door',8,68,24,48);if(routeId==='exit'||routeId==='full')add('door',158,8,14,48)}"
if old_architecture not in html:
    raise ValueError("V1 architecture function changed")
html = html.replace(old_architecture, new_architecture)
html = html.replace(
    "<section class=\"metrics\"><article><b>60 lp / 480 ku</b>finished-floor pitch</article>",
    "<section class=\"metrics\"><article><b>20 fps</b>faster turn cadence</article><article><b>6.67 fps</b>slower climb cadence</article><article><b>60 lp / 480 ku</b>finished-floor pitch</article>",
)
html = html.replace(
    "First inspect the camera-follow gait for equal left/right work. Then inspect the approach join, the uninterrupted floor crossing, and whether the rightward top dismount reads as weight transfer rather than sliding.",
    "First inspect the bottom turn: central rungs must stay behind the Keeper with no flash, while both side rails remain visible. Then judge the faster turn, the slower climb, the uninterrupted floor crossing and the top dismount. Hand/foot rung contact remains the accepted V1 tolerance.",
)
html, count = re.subn(
    r"const SPEC=.*?;\nconst routeSelect=",
    lambda _: "const SPEC=" + json.dumps(spec, separators=(",", ":")) + ";\nconst routeSelect=",
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    raise ValueError("could not replace embedded V1 spec")
PAGE_FILE.write_text(html)

(PACK / "HANDOFF.md").write_text(
    """# Keeper Prime ladder transitions V2

V2 changes no Keeper, ladder-contact, walk, bridge or turn pixels. It adds a narrow central-rung occlusion layer between the ladder and Keeper only while their bodies overlap, so rungs cannot flash through changing transparent gaps while the rails remain visible. Turns change from 62.5 ms to 50 ms per frame; contact, passing, mount and dismount frames change to 150 ms. Hand/foot-to-rung geometry remains V1 exactly. Nothing is promoted.

Review: `/keeper-review/keeper-prime-ladder-transitions-v2/`.
"""
)

register = {
    "schema": "lighthouse-keeper/review-batch@1",
    "batchId": "keeper-prime-ladder-transitions-2026-10-16-v2",
    "status": "draft-awaiting-visual-review",
    "purpose": "Correct V1 bottom-turn rung flicker and tune turn/climb cadence without changing artwork or geometry.",
    "authorities": {
        "v1Spec": {"file": relative(V1_SPEC_FILE), "sha256": sha256(V1_SPEC_FILE)},
        "v1Register": {"file": relative(V1_REGISTER_FILE), "sha256": sha256(V1_REGISTER_FILE)},
        "v1Page": {"file": relative(V1_PAGE_FILE), "sha256": sha256(V1_PAGE_FILE)},
    },
    "spec": {"file": relative(SPEC_FILE), "sha256": sha256(SPEC_FILE)},
    "reviewPage": {"file": relative(PAGE_FILE), "sha256": sha256(PAGE_FILE), "publicReview": f"/keeper-review/{SET}/", "preloadsAllUniqueFrames": True},
    "publishedAssets": published,
    "changes": {
        "artworkPixelsChanged": False,
        "geometryChanged": False,
        "rungContactChanged": False,
        "turnFrameDurationMs": [62.5, TURN_MS],
        "climbFrameDurationMs": [95, CLIMB_MS],
        "centralRungOcclusionLayerAdded": True,
    },
    "validation": {"productionChanged": False, "runtimeChanged": False, "finalChanged": False},
    "approvalBoundary": {"candidateApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
    "rollback": f"Delete only {relative(PACK)} and {relative(PUBLIC)}; V1, approved sources, Final, runtime and production remain unchanged.",
}
write_json(PACK / "batch-register.json", register)

print(json.dumps({
    "page": relative(PAGE_FILE),
    "routes": {key: len(value["frames"]) for key, value in spec["routes"].items()},
    "turnMs": TURN_MS,
    "climbMs": CLIMB_MS,
    "publishedAssets": len(published),
}, indent=2))
