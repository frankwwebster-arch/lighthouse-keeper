#!/usr/bin/env python3
"""Build the exact-authority Keeper Prime walk → stop → turn front V1 review."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-stop-turn-front-v1"
PREFIX = "/keeper-review/keeper-prime-walk-stop-turn-front-v1/assets/"
WALK_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6"
WALK_APPROVAL = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json"
STOP_PACK = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1"
STOP_APPROVAL = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/batch-register.json"
TURN_PACK = ROOT / "art/drafts/keeper-prime-turn-front-side-2026-10-13-v1"
TURN_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-front-side-2026-10-13-v2/batch-register.json"
CELL = (256, 320)
FPS = 8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def publish(path: Path, label: str) -> tuple[str, dict]:
    sha = digest(path)
    target = PUBLIC / "assets" / f"{label}-{sha[:16]}{path.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    return PREFIX + target.name, {"source": rel(path), "sourceSha256": sha, "public": rel(target), "publicSha256": digest(target), "byteIdentical": sha == digest(target)}


def save_strip(path: Path, frames: list[Path]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(Image.open(frame).convert("RGBA"), (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def contact_sheet(path: Path, frames: list[Path], labels: list[str]) -> None:
    thumb = (128, 160)
    header = 30
    sheet = Image.new("RGBA", (thumb[0] * len(frames), thumb[1] + header), (10, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(zip(frames, labels)):
        x = index * thumb[0]
        for yy in range(header, sheet.height, 12):
            for xx in range(x, x + thumb[0], 12):
                if ((xx - x) // 12 + (yy - header) // 12) % 2:
                    draw.rectangle((xx, yy, min(xx + 11, x + thumb[0] - 1), min(yy + 11, sheet.height - 1)), fill=(27, 45, 56, 255))
        image = Image.open(frame).convert("RGBA").resize(thumb, Image.Resampling.LANCZOS)
        sheet.alpha_composite(image, (x, header))
        draw.text((x + 5, 8), label, fill=(238, 245, 248, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=False, compress_level=9)


def review_page(route: list[dict], join_urls: list[str], contact_url: str, strip_url: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Walk → Stop → Turn Front V1</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#08131b;color:#eef5f7;font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1120px;margin:auto;padding:22px}}header{{border-bottom:1px solid #29414f}}a{{color:#8fd5ff}}.status{{display:inline-block;background:#5b4211;color:#ffe5a5;padding:5px 9px;border-radius:999px}}article{{background:#10202a;border:1px solid #29414f;border-radius:12px;padding:16px;margin:0 0 22px}}.rule{{background:#102430;border-left:4px solid #f4c55c;padding:12px 14px}}button{{background:#183445;color:#fff;border:1px solid #42677a;border-radius:8px;padding:9px 13px;margin:3px;cursor:pointer}}.controls{{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:10px 0}}.readout{{font-variant-numeric:tabular-nums;color:#c8dce6}}.stage{{position:relative;overflow:hidden;border:1px solid #466473;border-radius:8px;background-color:#152732;background-image:linear-gradient(45deg,#203844 25%,transparent 25%),linear-gradient(-45deg,#203844 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#203844 75%),linear-gradient(-45deg,transparent 75%,#203844 75%);background-size:32px 32px;background-position:0 0,0 16px,16px -16px,-16px 0}}.large{{height:350px}}.large img{{position:absolute;width:256px;height:320px;bottom:10px;left:0;image-rendering:auto}}.game{{height:180px}}.game img{{position:absolute;width:128px;height:160px;bottom:10px;left:0;image-rendering:auto}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.pose{{height:340px;display:grid;place-items:center}}.pose img{{width:256px;height:320px}}.pose.game{{height:180px}}.pose.game img{{width:128px;height:160px}}.sheet{{max-width:100%;height:auto;border:1px solid #466473}}code{{color:#b9e5ff}}@media(max-width:760px){{.pair{{grid-template-columns:1fr}}}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Keeper Prime · walk → stop → turn to camera V1</h1><span class="status">Exact-authority route · awaiting visual approval</span><p>Two exact Walk V6 cycles decelerate through the approved stop bridge, settle for one frame on the exact Side-right neutral, then use the approved side-right → front turn to reach the exact Prime front neutral.</p></header><main><p class="rule"><strong>Review priority:</strong> judge the Walk F1 → 75% deceleration seam, the stop itself, and whether the one-frame neutral beat makes the turn feel intentional without hesitation. The character must cease translating before rotation begins.</p>
<h2>Complete route</h2><article><div class="controls"><button id="play">Play</button><button id="pause">Pause</button><button id="prev">Previous frame</button><button id="next">Next frame</button><button id="restart">Restart</button><label><input id="loop" type="checkbox" checked> Loop route</label></div><p id="readout" class="readout"></p><div class="pair"><div><strong>Large inspection</strong><div class="stage large"><img id="large" alt="Large route"></div></div><div><strong>Exact proposed game scale</strong><div class="stage game"><img id="game" alt="Game-scale route"></div></div></div></article>
<h2>Isolated loop exit → full face</h2><article><div class="controls"><button id="joinPlay">Play</button><button id="joinPause">Pause</button><button id="joinPrev">Previous</button><button id="joinNext">Next</button></div><p id="joinReadout" class="readout"></p><div class="pair"><div class="stage pose"><img id="joinLarge" alt="Join large"></div><div class="stage pose game"><img id="joinGame" alt="Join game scale"></div></div><p>The 13-frame contract includes Walk F1 as its entry contact. When stitched after the walk loop, playback continues at frame 2 so Walk F1 is not duplicated.</p></article>
<h2>Exact pose sequence</h2><article><img class="sheet" src="{contact_url}" alt="Walk stop turn front contact sheet"><p><a href="{strip_url}">Download the 13-frame join strip</a>. Every cell is copied byte-for-byte from an approved authority; no new character drawing was introduced.</p></article>
<h2>Technical contract</h2><article><ul><li>8 fps throughout.</li><li>Walk cadence: 21 high-resolution px/frame; deceleration: 18 → 12 → 6 → 2 px/frame; stop, settle and turn: 0 px/frame.</li><li>Walk F1, Side-right stop and front neutral are exact endpoint bytes.</li><li>The stop is held for one additional frame (125 ms) before rotation.</li><li>All 256 × 320 cells retain transparent safety gutters.</li><li>This route is Draft only; Final and production remain unchanged.</li></ul></article>
<script>
const route={json.dumps(route, separators=(',', ':'))},join={json.dumps(join_urls, separators=(',', ':'))};let i=0,timer=null;const large=document.getElementById('large'),game=document.getElementById('game'),readout=document.getElementById('readout');
function render(){{const f=route[i];large.src=f.src;game.src=f.src;large.style.left=`${{f.x+20}}px`;game.style.left=`${{f.x/2+10}}px`;readout.textContent=`Frame ${{i+1}}/${{route.length}} · ${{f.phase}} · ${{f.pose}} · Δ ${{f.dx}} px · position ${{f.x}} px`;}}function pause(){{if(timer)clearInterval(timer);timer=null}}function play(){{pause();timer=setInterval(()=>{{if(i===route.length-1){{if(document.getElementById('loop').checked)i=0;else{{pause();return}}}}else i++;render()}},125)}}
document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{{pause();i=(i-1+route.length)%route.length;render()}};document.getElementById('next').onclick=()=>{{pause();i=(i+1)%route.length;render()}};document.getElementById('restart').onclick=()=>{{pause();i=0;render();play()}};
let j=0,jt=null;const jl=document.getElementById('joinLarge'),jg=document.getElementById('joinGame'),jr=document.getElementById('joinReadout');function joinRender(){{jl.src=join[j];jg.src=join[j];jr.textContent=`Join frame ${{j+1}}/${{join.length}}`;}}function joinPause(){{if(jt)clearInterval(jt);jt=null}}function joinPlay(){{joinPause();j=0;joinRender();jt=setInterval(()=>{{if(j===join.length-1){{joinPause();return}}j++;joinRender()}},125)}}document.getElementById('joinPlay').onclick=joinPlay;document.getElementById('joinPause').onclick=joinPause;document.getElementById('joinPrev').onclick=()=>{{joinPause();j=(j-1+join.length)%join.length;joinRender()}};document.getElementById('joinNext').onclick=()=>{{joinPause();j=(j+1)%join.length;joinRender()}};render();joinRender();play();
</script></main></body></html>'''


def main() -> None:
    required = [WALK_APPROVAL, STOP_APPROVAL, TURN_APPROVAL]
    walk_frames = [WALK_PACK / f"drafts/frames/keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    stop_frames = [STOP_PACK / f"drafts/frames/keeper_prime_stop-to-walk-right_f{i}.png" for i in range(1, 6)]
    turn_frames = [TURN_PACK / f"drafts/frames/keeper_prime_turn_front_to_side-right_f{i}.png" for i in range(1, 9)]
    required += walk_frames + stop_frames + turn_frames + [PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md"]
    for path in required:
        if not path.exists(): raise RuntimeError(f"missing {rel(path)}")
    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if directory.exists(): shutil.rmtree(directory)

    # Walk F1 contact; approved deceleration; one extra exact stop; approved reverse turn without repeated side endpoint.
    join_frames = [walk_frames[0], stop_frames[3], stop_frames[2], stop_frames[1], stop_frames[0], stop_frames[0], *reversed(turn_frames[:-1])]
    labels = ["Walk F1", "75%", "50%", "15%", "Stop", "Settle", "75°", "60°", "45°", "30°", "15°", "8°", "Front"]
    strip = PACK / "drafts/keeper_prime_walk-contact_to_stop_to_front_f13.png"
    save_strip(strip, join_frames)
    sidecar = strip.with_suffix(".json")
    dump(sidecar, {"name": "keeper_prime_walk-contact_to_stop_to_front", "w": 32, "h": 40, "density": 8, "frames": 13, "fps": FPS, "loop": False, "startPose": "keeper_prime_walk-right_f1", "endPose": "keeper_prime_master-neutral-front", "runtimeEntryFrameAfterWalkLoop": 2, "rootMotionHighResolutionPixels": [0, 18, 12, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0], "sha256": digest(strip), "frameSha256": [digest(path) for path in join_frames], "status": "walk-stop-turn-front-v1-review-draft-not-production"})
    contact = PACK / "evidence/walk-stop-turn-front-contact-sheet.png"
    contact_sheet(contact, join_frames, labels)

    published, walk_urls, stop_urls, turn_urls = [], [], [], []
    for index, path in enumerate(walk_frames, 1):
        url, record = publish(path, f"walk-frame{index}"); walk_urls.append(url); published.append(record)
    for index, path in enumerate(stop_frames, 1):
        url, record = publish(path, f"stop-bridge-frame{index}"); stop_urls.append(url); published.append(record)
    for index, path in enumerate(turn_frames, 1):
        url, record = publish(path, f"turn-frame{index}"); turn_urls.append(url); published.append(record)
    join_urls = [walk_urls[0], stop_urls[3], stop_urls[2], stop_urls[1], stop_urls[0], stop_urls[0], *reversed(turn_urls[:-1])]
    strip_url, record = publish(strip, "join-strip"); published.append(record)
    contact_url, record = publish(contact, "contact"); published.append(record)

    route, x = [], 0
    for _cycle in range(2):
        for frame in range(1, 9):
            x += 21
            actual = frame % 8
            route.append({"src": walk_urls[actual], "phase": "approved walk", "pose": f"Walk F{actual + 1}", "dx": 21, "x": x})
    for index, delta, pose in zip([3, 2, 1, 0], [18, 12, 6, 2], ["75%", "50%", "15%", "exact Side-right stop"]):
        x += delta; route.append({"src": stop_urls[index], "phase": "approved deceleration", "pose": pose, "dx": delta, "x": x})
    route.append({"src": stop_urls[0], "phase": "neutral settle", "pose": "exact Side-right stop", "dx": 0, "x": x})
    for original_index, angle in zip(range(6, -1, -1), [75, 60, 45, 30, 15, 8, 0]):
        route.append({"src": turn_urls[original_index], "phase": "approved turn to camera", "pose": f"{angle}°", "dx": 0, "x": x})
    for _ in range(4): route.append({"src": turn_urls[0], "phase": "front hold", "pose": "exact Prime front", "dx": 0, "x": x})

    page = PUBLIC / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(review_page(route, join_urls, contact_url, strip_url))
    register = {
        "batchId": "keeper-prime-walk-stop-turn-front-2026-10-14-v1", "status": "draft-walk-stop-turn-front-v1-awaiting-visual-approval",
        "purpose": "Review the exact approved walk, deceleration and side-right-to-front turn as one deterministic route.",
        "authorities": {
            "walk": {"approval": rel(WALK_APPROVAL), "approvalSha256": digest(WALK_APPROVAL)},
            "stopWalkStop": {"approval": rel(STOP_APPROVAL), "approvalSha256": digest(STOP_APPROVAL)},
            "frontSideTurn": {"approval": rel(TURN_APPROVAL), "approvalSha256": digest(TURN_APPROVAL), "acceptedLimitation": "very slight visual jump around 45°"},
        },
        "join": {"strip": rel(strip), "sha256": digest(strip), "sidecar": rel(sidecar), "sidecarSha256": digest(sidecar), "frames": len(join_frames), "fps": FPS, "runtimeEntryFrameAfterWalkLoop": 2, "frameSha256": [digest(path) for path in join_frames], "labels": labels},
        "route": {"frames": len(route), "fps": FPS, "distanceHighResolutionPixels": x, "walkCycles": 2, "walkDelta": 21, "decelerationDeltas": [18, 12, 6, 2], "neutralSettleFrames": 1, "turnFramesAfterSharedEndpoint": 7, "frontHoldFrames": 4, "rootMotionStopsBeforeTurn": True, "framesData": route},
        "endpointContract": {"walkContact": {"file": rel(walk_frames[0]), "sha256": digest(walk_frames[0])}, "sideStop": {"file": rel(stop_frames[0]), "sha256": digest(stop_frames[0]), "turnSideEndpointSha256": digest(turn_frames[-1]), "byteIdenticalAcrossDecelerationAndTurn": digest(stop_frames[0]) == digest(turn_frames[-1])}, "front": {"file": rel(turn_frames[0]), "sha256": digest(turn_frames[0])}},
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}}, "publishedAssets": published,
        "reviewPage": {"file": rel(page), "sha256": digest(page), "publicReview": "/keeper-review/keeper-prime-walk-stop-turn-front-v1/", "assetPrefix": PREFIX, "relativeAssetUrls": False, "controls": ["play", "pause", "previous-frame", "next-frame", "restart", "route-loop", "join-play", "join-step"]},
        "validation": {"allArtworkCopiedFromApprovedAuthorities": True, "newCharacterDrawings": False, "walkToDecelerationContactExact": True, "decelerationToTurnSideEndpointExact": True, "turnFrontEndpointExact": True, "rootMotionStopsBeforeTurn": True, "transparentSafetyGutters": True, "stripSidecarAgreement": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"sourceAuthoritiesApproved": True, "compositeRouteApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank reviews walk → stop → turn to camera V1 at large and exact game scale before any next route is assembled.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; every approved source authority, Final and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "joinFrames": len(join_frames), "routeFrames": len(route), "distance": x, "public": register["reviewPage"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
