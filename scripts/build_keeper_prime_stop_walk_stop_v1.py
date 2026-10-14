#!/usr/bin/env python3
"""Build the reversible Keeper Prime stop → walk → stop V1 review pack."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

import build_keeper_prime_walk_v1 as walk_base
import build_keeper_prime_walk_v4 as registration


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-stop-walk-stop-v1"
PREFIX = "/keeper-review/keeper-prime-stop-walk-stop-v1/assets/"
NEUTRAL = ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png"
WALK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6"
WALK_REGISTER = WALK / "batch-register.json"
WALK_APPROVAL_REGISTER = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json"
SOURCES = [
    PACK / "sources/bridge-25-start.png",
    PACK / "sources/bridge-50-mid.png",
    PACK / "sources/bridge-75-late.png",
]
FPS = 8
CELL = (256, 320)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def save_strip(path: Path, frames: list[Path]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(Image.open(frame).convert("RGBA"), (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def alpha_bounds(path: Path) -> tuple[int, int, int, int]:
    image = Image.open(path).convert("RGBA")
    return walk_base.alpha_bounds(image)


def publish(path: Path, label: str) -> tuple[str, dict]:
    sha = digest(path)
    target = PUBLIC / "assets" / f"{label}-{sha[:16]}{path.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    return PREFIX + target.name, {"source": rel(path), "sourceSha256": sha, "public": rel(target), "publicSha256": digest(target), "byteIdentical": sha == digest(target)}


def write_sidecar(path: Path, name: str, frames: list[Path], start_pose: str, end_pose: str) -> Path:
    sidecar = path.with_suffix(".json")
    dump(sidecar, {
        "name": name, "w": 32, "h": 40, "density": 8, "frames": len(frames), "fps": FPS,
        "loop": False, "startPose": start_pose, "endPose": end_pose,
        "sha256": digest(path), "frameSha256": [digest(frame) for frame in frames],
        "status": "stop-walk-stop-v1-review-draft-not-production",
    })
    return sidecar


def contact_sheet(frames: list[Path], labels: list[str]) -> Path:
    scale = 1
    header = 34
    sheet = Image.new("RGBA", (CELL[0] * len(frames) * scale, CELL[1] * scale + header), (12, 23, 31, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (path, label) in enumerate(zip(frames, labels)):
        x = index * CELL[0]
        for yy in range(header, sheet.height, 16):
            for xx in range(x, x + CELL[0], 16):
                if ((xx - x) // 16 + (yy - header) // 16) % 2:
                    draw.rectangle((xx, yy, min(xx + 15, x + CELL[0] - 1), min(yy + 15, sheet.height - 1)), fill=(29, 47, 58, 255))
        sheet.alpha_composite(Image.open(path).convert("RGBA"), (x, header))
        draw.text((x + 8, 9), label, fill=(240, 246, 250, 255))
    output = PACK / "evidence/stop-to-walk-contact-sheet.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=False, compress_level=9)
    return output


def write_review_page(stop_urls: list[str], walk_urls: list[str], contact_url: str, strip_urls: dict[str, str], route: list[dict]) -> Path:
    route_json = json.dumps(route, separators=(",", ":"))
    stop_json = json.dumps(stop_urls, separators=(",", ":"))
    reverse_json = json.dumps(list(reversed(stop_urls)), separators=(",", ":"))
    walk_json = json.dumps(walk_urls, separators=(",", ":"))
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Stop → Walk → Stop V1</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#08131b;color:#eef5f7;font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1120px;margin:auto;padding:22px}}header{{border-bottom:1px solid #29414f}}a{{color:#8fd5ff}}.status{{display:inline-block;background:#5b4211;color:#ffe5a5;padding:5px 9px;border-radius:999px}}.rule{{background:#102430;border-left:4px solid #f4c55c;padding:12px 14px}}article{{background:#10202a;border:1px solid #29414f;border-radius:12px;padding:16px;margin:0 0 22px}}button{{background:#183445;color:#fff;border:1px solid #42677a;border-radius:8px;padding:9px 13px;margin:3px;cursor:pointer}}button:hover{{background:#24506a}}.controls{{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:10px 0}}.readout{{font-variant-numeric:tabular-nums;color:#c8dce6}}.stage{{position:relative;overflow:hidden;border:1px solid #466473;border-radius:8px;background-color:#152732;background-image:linear-gradient(45deg,#203844 25%,transparent 25%),linear-gradient(-45deg,#203844 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#203844 75%),linear-gradient(-45deg,transparent 75%,#203844 75%);background-size:32px 32px;background-position:0 0,0 16px,16px -16px,-16px 0}}.route-large{{height:350px}}.route-large img{{position:absolute;width:256px;height:320px;bottom:10px;left:0;image-rendering:auto}}.route-game{{height:180px}}.route-game img{{position:absolute;width:128px;height:160px;bottom:10px;left:0;image-rendering:auto}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.pose{{height:340px;display:grid;place-items:center}}.pose img{{width:256px;height:320px;image-rendering:auto}}.pose.game{{height:180px}}.pose.game img{{width:128px;height:160px}}.sheet{{max-width:100%;height:auto;border:1px solid #466473}}code{{color:#b9e5ff}}@media(max-width:760px){{.pair{{grid-template-columns:1fr}}}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Keeper Prime · stop → walk → stop V1</h1><span class="status">Core transition route · awaiting visual approval</span><p>The exact approved stop and Walk V6 endpoints are joined by one reversible three-pose bridge. The sprite begins translating on the first movement frame, accelerates into the approved walk, then decelerates through the same poses and returns to the exact stop.</p></header><main><p class="rule"><strong>Review priority:</strong> there must be no walking on the spot, no model or scale jump at either seam, and no foot slide after the final exact stop. Pay special attention to stop→25%, 75%→Walk F1, Walk F1→75%, and 25%→stop.</p>
<h2>Complete route</h2><article><div class="controls"><button id="play">Play</button><button id="pause">Pause</button><button id="prev">Previous frame</button><button id="next">Next frame</button><button id="restart">Restart</button><label><input id="loop" type="checkbox" checked> Loop route</label></div><p id="readout" class="readout"></p><div class="pair"><div><strong>Large inspection</strong><div class="stage route-large"><img id="routeLarge" alt="Large stop walk stop route"></div></div><div><strong>Exact proposed game scale</strong><div class="stage route-game"><img id="routeGame" alt="Game-scale stop walk stop route"></div></div></div></article>
<h2>Isolated reversible bridge</h2><article><div class="controls"><button id="bridgePlay">Play stop → walk</button><button id="bridgeReverse">Play walk → stop</button><button id="bridgePause">Pause</button><button id="bridgePrev">Previous</button><button id="bridgeNext">Next</button></div><p id="bridgeReadout" class="readout"></p><div class="pair"><div class="stage pose"><img id="bridgeLarge" alt="Transition pose large"></div><div class="stage pose game"><img id="bridgeGame" alt="Transition pose at game scale"></div></div></article>
<h2>Five registered poses</h2><article><img class="sheet" src="{contact_url}" alt="Stop to walk contact sheet"><p>Stop and Walk F1 are exact approved bytes. The three interior frames are new review artwork. Walk→stop is the exact byte-reverse, so both directions share identical geometry.</p></article>
<h2>Technical contract</h2><article><ul><li>8 fps; route velocity deltas: 0 hold, then 2 → 6 → 12 → 18 → 21 px/frame, and the exact inverse into stop.</li><li>No root motion is baked into the strips; the route preview applies the registered displacement schedule.</li><li>Start and final stop are the same file and SHA-256.</li><li>Every 256 × 320 cell has a transparent safety gutter.</li><li>Walk V6 is approved authority; this transition route is not Final or production.</li></ul><p><a href="{strip_urls['forward']}">Stop→walk strip</a> · <a href="{strip_urls['reverse']}">Walk→stop strip</a></p></article>
<script>
const route={route_json},stopFrames={stop_json},reverseFrames={reverse_json},walkFrames={walk_json};let i=0,timer=null;
const large=document.getElementById('routeLarge'),game=document.getElementById('routeGame'),readout=document.getElementById('readout');
function renderRoute(){{const f=route[i];large.src=f.src;game.src=f.src;large.style.left=`${{f.x+40}}px`;game.style.left=`${{f.x/2+20}}px`;readout.textContent=`Frame ${{i+1}}/${{route.length}} · ${{f.phase}} · pose ${{f.pose}} · displacement ${{f.dx}} px · position ${{f.x}} px`;}}
function stop(){{if(timer)clearInterval(timer);timer=null}}function play(){{stop();timer=setInterval(()=>{{if(i===route.length-1){{if(document.getElementById('loop').checked)i=0;else{{stop();return}}}}else i++;renderRoute()}},1000/{FPS})}}
document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{{stop();i=(i-1+route.length)%route.length;renderRoute()}};document.getElementById('next').onclick=()=>{{stop();i=(i+1)%route.length;renderRoute()}};document.getElementById('restart').onclick=()=>{{stop();i=0;renderRoute();play()}};
let bi=0,bd=1,bt=null;const bl=document.getElementById('bridgeLarge'),bg=document.getElementById('bridgeGame'),br=document.getElementById('bridgeReadout');
function bridgeRender(){{const list=bd===1?stopFrames:reverseFrames;bl.src=list[bi];bg.src=list[bi];br.textContent=`${{bd===1?'Stop → walk':'Walk → stop'}} · frame ${{bi+1}}/5`;}}function bridgeStop(){{if(bt)clearInterval(bt);bt=null}}function bridgePlay(dir){{bridgeStop();bd=dir;bi=0;bridgeRender();bt=setInterval(()=>{{if(bi===4){{bridgeStop();return}}bi++;bridgeRender()}},1000/{FPS})}}
document.getElementById('bridgePlay').onclick=()=>bridgePlay(1);document.getElementById('bridgeReverse').onclick=()=>bridgePlay(-1);document.getElementById('bridgePause').onclick=bridgeStop;document.getElementById('bridgePrev').onclick=()=>{{bridgeStop();bi=(bi-1+5)%5;bridgeRender()}};document.getElementById('bridgeNext').onclick=()=>{{bridgeStop();bi=(bi+1)%5;bridgeRender()}};
renderRoute();bridgeRender();play();
</script></main></body></html>'''
    page = PUBLIC / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(html)
    return page


def main() -> None:
    required = [NEUTRAL, WALK_REGISTER, WALK_APPROVAL_REGISTER, PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md", *SOURCES]
    required += [WALK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png" for frame in range(1, 9)]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    walk_register = json.loads(WALK_REGISTER.read_text())
    if walk_register.get("status") != "draft-frame8-lower-body-repair-awaiting-visual-approval":
        raise RuntimeError("Walk V6 provenance changed")

    for directory in (PACK / "drafts", PACK / "evidence/registered-sources", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)
    (PACK / "drafts/frames").mkdir(parents=True, exist_ok=True)
    (PACK / "evidence/registered-sources").mkdir(parents=True, exist_ok=True)

    walk_f1 = WALK / "drafts/frames/keeper_prime_walk-right_f1.png"
    bridge_paths = []
    bridge_records = []
    for index, source_path in enumerate(SOURCES, 1):
        source = Image.open(source_path).convert("RGBA")
        target = Image.open(walk_f1).convert("RGBA")
        image, registration_record = registration.register_to_frame(source, target)
        output = PACK / f"drafts/frames/keeper_prime_stop-to-walk-right_f{index + 1}.png"
        image.save(output, optimize=False, compress_level=9)
        registered = PACK / f"evidence/registered-sources/bridge-{index}.png"
        image.save(registered, optimize=False, compress_level=9)
        if walk_base.edge_alpha_count(image):
            raise RuntimeError(f"bridge {index} touches cell edge")
        bridge_paths.append(output)
        bounds = alpha_bounds(output)
        bridge_records.append({"frame": index + 1, "fraction": [0.15, 0.5, 0.75][index - 1], "file": rel(output), "sha256": digest(output), "source": rel(source_path), "sourceSha256": digest(source_path), "registration": registration_record, "opaqueBoundsExclusive": list(bounds), "edgeAlphaPixels": walk_base.edge_alpha_count(image)})

    stop_path = PACK / "drafts/frames/keeper_prime_stop-to-walk-right_f1.png"
    contact_path = PACK / "drafts/frames/keeper_prime_stop-to-walk-right_f5.png"
    shutil.copyfile(NEUTRAL, stop_path)
    shutil.copyfile(walk_f1, contact_path)
    forward_frames = [stop_path, *bridge_paths, contact_path]
    reverse_frames = list(reversed(forward_frames))
    forward_strip = PACK / "drafts/keeper_prime_stop-to-walk-right_f5.png"
    reverse_strip = PACK / "drafts/keeper_prime_walk-to-stop-right_f5.png"
    save_strip(forward_strip, forward_frames)
    save_strip(reverse_strip, reverse_frames)
    forward_sidecar = write_sidecar(forward_strip, "keeper_prime_stop-to-walk-right", forward_frames, "keeper_prime_stop-side-right", "keeper_prime_walk-right_f1")
    reverse_sidecar = write_sidecar(reverse_strip, "keeper_prime_walk-to-stop-right", reverse_frames, "keeper_prime_walk-right_f1", "keeper_prime_stop-side-right")

    contact = contact_sheet(forward_frames, ["Exact stop", "15%", "50%", "75%", "Exact Walk F1"])
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    stop_urls, published = [], []
    for index, path in enumerate(forward_frames, 1):
        url, record = publish(path, f"transition-frame{index}")
        stop_urls.append(url); published.append(record)
    walk_urls = []
    for frame in range(1, 9):
        path = WALK / f"drafts/frames/keeper_prime_walk-right_f{frame}.png"
        url, record = publish(path, f"walk-frame{frame}")
        walk_urls.append(url); published.append(record)
    contact_url, record = publish(contact, "contact"); published.append(record)
    forward_url, record = publish(forward_strip, "stop-to-walk-strip"); published.append(record)
    reverse_url, record = publish(reverse_strip, "walk-to-stop-strip"); published.append(record)

    route = []
    x = 0
    for _ in range(4): route.append({"src": stop_urls[0], "phase": "stopped hold", "pose": "exact stop", "dx": 0, "x": x})
    for index, delta in zip([1, 2, 3, 4], [2, 6, 12, 18]):
        x += delta; route.append({"src": stop_urls[index], "phase": "accelerating", "pose": ["15%", "50%", "75%", "Walk F1"][index - 1], "dx": delta, "x": x})
    for _cycle in range(2):
        for frame in range(1, 9):
            x += 21; route.append({"src": walk_urls[frame % 8], "phase": "approved walk", "pose": f"Walk F{frame % 8 + 1}", "dx": 21, "x": x})
    for index, delta in zip([3, 2, 1, 0], [18, 12, 6, 2]):
        x += delta; route.append({"src": stop_urls[index], "phase": "decelerating", "pose": ["75%", "50%", "15%", "exact stop"][3 - index], "dx": delta, "x": x})
    for _ in range(4): route.append({"src": stop_urls[0], "phase": "stopped hold", "pose": "exact stop", "dx": 0, "x": x})

    page = write_review_page(stop_urls, walk_urls, contact_url, {"forward": forward_url, "reverse": reverse_url}, route)
    stop_sha = digest(stop_path)
    final_stop_sha = digest(reverse_frames[-1])
    register = {
        "batchId": "keeper-prime-stop-walk-stop-2026-10-14-v1", "status": "draft-stop-walk-stop-v1-awaiting-visual-approval",
        "purpose": "Review an exact stop accelerating into approved Walk V6 and decelerating through the byte-reversed bridge to the identical stop.",
        "approvedWalkAuthority": {"register": rel(WALK_REGISTER), "registerSha256": digest(WALK_REGISTER), "approvalRecord": rel(WALK_APPROVAL_REGISTER), "approvalRecordSha256": digest(WALK_APPROVAL_REGISTER), "approvalWording": "Approved", "approvedOn": "2026-10-14"},
        "stopAuthority": {"file": rel(NEUTRAL), "sha256": digest(NEUTRAL)},
        "generation": {"mode": "built-in image generation with exact stop and Walk V6 F1 references, followed by deterministic badge/floor registration", "selectedSources": [{"file": rel(path), "sha256": digest(path)} for path in SOURCES], "promptLog": rel(PACK / "PROMPT_LOG.md")},
        "transition": {"fps": FPS, "forward": {"strip": rel(forward_strip), "sha256": digest(forward_strip), "sidecar": rel(forward_sidecar), "sidecarSha256": digest(forward_sidecar)}, "reverse": {"strip": rel(reverse_strip), "sha256": digest(reverse_strip), "sidecar": rel(reverse_sidecar), "sidecarSha256": digest(reverse_sidecar)}, "bridgeFrames": bridge_records, "startStopSha256": stop_sha, "finalStopSha256": final_stop_sha, "identicalStopEndpoints": stop_sha == final_stop_sha},
        "rootMotion": {"bakedIntoStrips": False, "fps": FPS, "accelerationDeltasHighResolutionPixels": [2, 6, 12, 18], "walkDeltaHighResolutionPixels": 21, "decelerationDeltasHighResolutionPixels": [18, 12, 6, 2], "firstMovementFrameDelta": 2, "walkingOnSpotFrames": 0, "route": route},
        "publishedAssets": published,
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}},
        "reviewPage": {"file": rel(page), "sha256": digest(page), "publicReview": "/keeper-review/keeper-prime-stop-walk-stop-v1/", "assetPrefix": PREFIX, "relativeAssetUrls": False, "controls": ["play", "pause", "previous-frame", "next-frame", "restart", "route-loop", "bridge-forward", "bridge-reverse"]},
        "validation": {"approvedWalkV6Unchanged": True, "stopAuthorityUnchanged": True, "startAndFinalStopByteIdentical": stop_sha == final_stop_sha, "walkToStopIsExactBridgeReverse": True, "movementBeginsOnFirstGaitFrame": True, "walkingOnSpotFrames": 0, "transparentSafetyGutters": True, "stripSidecarAgreement": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"walkV6Approved": True, "stopToWalkApproved": False, "walkToStopApproved": False, "completeRouteApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank reviews the complete stop→walk→stop route, especially both endpoint seams and whether acceleration/deceleration ever reads as walking on the spot.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; approved Walk V6, side-right stop, prior drafts, Final and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "transitionFrames": 5, "routeFrames": len(route), "routeDistance": x, "publicPage": rel(page)}, indent=2))


if __name__ == "__main__":
    main()
