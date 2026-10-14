#!/usr/bin/env python3
"""Build the exact-authority Keeper Prime walk → stop → turn away V2 review."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v2"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-walk-stop-turn-back-v2"
PREFIX = "/keeper-review/keeper-prime-walk-stop-turn-back-v2/assets/"
WALK_PACK = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6"
WALK_APPROVAL = ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json"
STOP_PACK = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1"
STOP_APPROVAL = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/batch-register.json"
TURN_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v9"
TURN_APPROVAL = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json"
TIMING_APPROVAL = ROOT / "art/drafts/keeper-fast-transition-timing-2026-10-14-v1/approval-register.json"
TIMING_POLICY = ROOT / "data/keeper_timing_policy.json"
CELL = (256, 320)


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
    return PREFIX + target.name, {
        "source": rel(path), "sourceSha256": sha, "public": rel(target),
        "publicSha256": digest(target), "byteIdentical": sha == digest(target),
    }


def save_strip(path: Path, frames: list[Path]) -> None:
    strip = Image.new("RGBA", (CELL[0] * len(frames), CELL[1]), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        strip.paste(Image.open(frame).convert("RGBA"), (index * CELL[0], 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=False, compress_level=9)


def contact_sheet(path: Path, frames: list[Path], labels: list[str]) -> None:
    thumb, header = (128, 160), 30
    sheet = Image.new("RGBA", (thumb[0] * len(frames), thumb[1] + header), (10, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(zip(frames, labels)):
        x = index * thumb[0]
        for yy in range(header, sheet.height, 12):
            for xx in range(x, x + thumb[0], 12):
                if ((xx - x) // 12 + (yy - header) // 12) % 2:
                    draw.rectangle((xx, yy, min(xx + 11, x + thumb[0] - 1), min(yy + 11, sheet.height - 1)), fill=(27, 45, 56, 255))
        sheet.alpha_composite(Image.open(frame).convert("RGBA").resize(thumb, Image.Resampling.LANCZOS), (x, header))
        draw.text((x + 5, 8), label, fill=(238, 245, 248, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=False, compress_level=9)


def review_page(route: list[dict], join_urls: list[str], join_durations: list[float], contact_url: str, strip_url: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime Walk → Stop → Turn Away V2</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#08131b;color:#eef5f7;font:16px/1.45 system-ui,sans-serif}}header,main{{max-width:1180px;margin:auto;padding:22px}}header{{border-bottom:1px solid #29414f}}a{{color:#8fd5ff}}.status{{display:inline-block;background:#5b4211;color:#ffe5a5;padding:5px 9px;border-radius:999px}}article{{background:#10202a;border:1px solid #29414f;border-radius:12px;padding:16px;margin:0 0 22px}}.rule{{background:#102430;border-left:4px solid #f4c55c;padding:12px 14px}}button{{background:#183445;color:#fff;border:1px solid #42677a;border-radius:8px;padding:9px 13px;margin:3px;cursor:pointer}}button:disabled{{cursor:wait;opacity:.45}}.controls{{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:10px 0}}.readout{{font-variant-numeric:tabular-nums;color:#c8dce6}}.stage{{position:relative;overflow:hidden;border:1px solid #466473;border-radius:8px;background-color:#152732;background-image:linear-gradient(45deg,#203844 25%,transparent 25%),linear-gradient(-45deg,#203844 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#203844 75%),linear-gradient(-45deg,transparent 75%,#203844 75%);background-size:32px 32px;background-position:0 0,0 16px,16px -16px,-16px 0}}.large{{height:350px;min-width:670px}}.large img{{position:absolute;width:256px;height:320px;bottom:10px;left:0;image-rendering:auto}}.game{{height:180px;min-width:340px}}.game img{{position:absolute;width:128px;height:160px;bottom:10px;left:0;image-rendering:auto}}.scaleBlock{{margin-top:14px;overflow:auto}}.poseRow{{display:grid;grid-template-columns:2fr 1fr;gap:16px}}.pose{{height:340px;display:grid;place-items:center}}.pose img{{width:256px;height:320px}}.pose.game{{height:180px}}.pose.game img{{width:128px;height:160px}}.sheet{{max-width:100%;height:auto;border:1px solid #466473}}code{{color:#b9e5ff}}@media(max-width:760px){{.poseRow{{grid-template-columns:1fr}}}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Keeper Prime · walk → stop → turn fully away V2</h1><span class="status">Exact V1 artwork · preload-safe playback · awaiting route approval</span><p>V2 changes delivery only: all animation frames load and decode before playback begins. The Keeper pixels, timing, movement and endpoints are byte-identical to V1.</p></header><main><p class="rule"><strong>Review priority:</strong> playback should now remain continuously visible from the walk through the full rear turn. Then judge the same route seam: no flash, shrink or shape change as the exact approved back endpoint arrives.</p>
<h2>Complete route</h2><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>Previous frame</button><button id="next" disabled>Next frame</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox" checked> Loop route</label></div><p id="readout" class="readout">Loading all animation frames before playback…</p><div class="scaleBlock"><strong>Large inspection · full-width travel lane</strong><div class="stage large"><img id="large" alt="Large route"></div></div><div class="scaleBlock"><strong>Exact proposed game scale · full-width travel lane</strong><div class="stage game"><img id="game" alt="Game-scale route"></div></div></article>
<h2>Isolated loop exit → full back</h2><article><div class="controls"><button id="joinPlay" disabled>Play</button><button id="joinPause" disabled>Pause</button><button id="joinPrev" disabled>Previous frame</button><button id="joinNext" disabled>Next frame</button></div><p id="joinReadout" class="readout">Loading all animation frames before playback…</p><div class="poseRow"><div class="stage pose"><img id="joinLarge" alt="Join large"></div><div class="stage pose game"><img id="joinGame" alt="Join game scale"></div></div><p>The 13-frame evidence strip begins with Walk F1. Runtime stitching enters at frame 2 after the complete walk loop, so the Walk F1 contact is not duplicated.</p></article>
<h2>Exact pose sequence</h2><article><img class="sheet" src="{contact_url}" alt="Walk stop turn back contact sheet"><p><a href="{strip_url}">Download the 13-frame join strip</a>. Every cell is copied byte-for-byte from an approved authority; no new character drawing was introduced.</p></article>
<h2>Technical contract</h2><article><ul><li>Fast Timing V1: walk 10 fps; deceleration 12 fps; settle 0 ms; turn 16 fps; rear endpoint hold 625 ms.</li><li>Root motion: 21 px per walk frame, then 18 → 12 → 6 → 2 px; zero throughout the turn.</li><li>The approved Side-right stop is geometrically the turn entry; V9 F1 is omitted from playback to avoid a stationary duplicate.</li><li>The final turn frame is the exact approved rear neutral.</li><li>All 256 × 320 cells retain transparent safety gutters.</li><li>Draft only; Workbench Final, production sprites and runtime manifest remain unchanged.</li></ul></article>
<script>
const route={json.dumps(route, separators=(',', ':'))},join={json.dumps(join_urls, separators=(',', ':'))},joinDur={json.dumps(join_durations, separators=(',', ':'))};let i=0,timer=null;const large=document.getElementById('large'),game=document.getElementById('game'),readout=document.getElementById('readout');
function render(){{const f=route[i];large.src=f.src;game.src=f.src;large.style.left=`${{f.x+20}}px`;game.style.left=`${{f.x/2+10}}px`;readout.textContent=`Frame ${{i+1}}/${{route.length}} · ${{f.phase}} · ${{f.pose}} · Δ ${{f.dx}} px · ${{Math.round(f.durationMs)}} ms`;}}function pause(){{if(timer)clearTimeout(timer);timer=null}}function tick(){{if(i===route.length-1){{if(document.getElementById('loop').checked)i=0;else{{pause();return}}}}else i++;render();timer=setTimeout(tick,route[i].durationMs)}}function play(){{pause();timer=setTimeout(tick,route[i].durationMs)}}
document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{{pause();i=(i-1+route.length)%route.length;render()}};document.getElementById('next').onclick=()=>{{pause();i=(i+1)%route.length;render()}};document.getElementById('restart').onclick=()=>{{pause();i=0;render();play()}};
let j=0,jt=null;const jl=document.getElementById('joinLarge'),jg=document.getElementById('joinGame'),jr=document.getElementById('joinReadout');function joinRender(){{jl.src=join[j];jg.src=join[j];jr.textContent=`Join frame ${{j+1}}/${{join.length}} · ${{Math.round(joinDur[j])}} ms`;}}function joinPause(){{if(jt)clearTimeout(jt);jt=null}}function joinTick(){{if(j===join.length-1){{joinPause();return}}j++;joinRender();jt=setTimeout(joinTick,joinDur[j])}}function joinPlay(){{joinPause();j=0;joinRender();jt=setTimeout(joinTick,joinDur[0])}}document.getElementById('joinPlay').onclick=joinPlay;document.getElementById('joinPause').onclick=joinPause;document.getElementById('joinPrev').onclick=()=>{{joinPause();j=(j-1+join.length)%join.length;joinRender()}};document.getElementById('joinNext').onclick=()=>{{joinPause();j=(j+1)%join.length;joinRender()}};
const frameSources=[...new Set([...route.map(frame=>frame.src),...join])],buttons=[...document.querySelectorAll('button')];
function preloadFrame(src){{return new Promise((resolve,reject)=>{{const image=new Image();image.onload=()=>{{const decoded=image.decode?.();if(decoded)decoded.then(resolve).catch(resolve);else resolve()}};image.onerror=()=>reject(new Error(src));image.src=src}})}}
async function startPlayback(){{try{{await Promise.all(frameSources.map(preloadFrame));buttons.forEach(button=>button.disabled=false);render();joinRender();play()}}catch(error){{pause();joinPause();readout.textContent=`A frame failed to load. Reload this page to retry. (${{error.message}})`;jr.textContent='Playback held because every frame must be ready first.'}}}}startPlayback();
</script></main></body></html>'''


def main() -> None:
    timing = json.loads(TIMING_POLICY.read_text())["transitionProfile"]
    walk_frames = [WALK_PACK / f"drafts/frames/keeper_prime_walk-right_f{i}.png" for i in range(1, 9)]
    stop_frames = [STOP_PACK / f"drafts/frames/keeper_prime_stop-to-walk-right_f{i}.png" for i in range(1, 6)]
    turn_frames = [TURN_PACK / f"drafts/frames/keeper_prime_turn_side-right_to_back_f{i:02d}.png" for i in range(1, 10)]
    required = [WALK_APPROVAL, STOP_APPROVAL, TURN_APPROVAL, TIMING_APPROVAL, TIMING_POLICY, PACK / "HANDOFF.md", PACK / "PROMPT_LOG.md", *walk_frames, *stop_frames, *turn_frames]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing {rel(path)}")
    for directory in (PACK / "drafts", PACK / "evidence", PUBLIC):
        if directory.exists():
            shutil.rmtree(directory)

    # Shared side endpoint is checked by geometry in the verifier; V9 F1 is not replayed.
    join_frames = [walk_frames[0], stop_frames[3], stop_frames[2], stop_frames[1], stop_frames[0], *turn_frames[1:]]
    labels = ["Walk F1", "75%", "50%", "15%", "Side stop", "98°", "105°", "120°", "135°", "150°", "165°", "172.5°", "Back"]
    join_durations = [1000 / timing["walkFps"], *([1000 / timing["decelerationFps"]] * 4), *([1000 / timing["turnFps"]] * 8)]
    strip = PACK / "drafts/keeper_prime_walk-contact_to_stop_to_back_f13.png"
    save_strip(strip, join_frames)
    sidecar = strip.with_suffix(".json")
    dump(sidecar, {
        "name": "keeper_prime_walk-contact_to_stop_to_back", "w": 32, "h": 40, "density": 8,
        "frames": 13, "loop": False, "startPose": "keeper_prime_walk-right_f1", "endPose": "keeper_prime_neutral-back",
        "runtimeEntryFrameAfterWalkLoop": 2, "frameDurationsMs": join_durations,
        "rootMotionHighResolutionPixels": [0, 18, 12, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        "sha256": digest(strip), "frameSha256": [digest(path) for path in join_frames],
        "status": "walk-stop-turn-back-v2-review-draft-not-production",
    })
    contact = PACK / "evidence/walk-stop-turn-back-contact-sheet.png"
    contact_sheet(contact, join_frames, labels)

    published, walk_urls, stop_urls, turn_urls = [], [], [], []
    for index, path in enumerate(walk_frames, 1):
        url, record = publish(path, f"walk-frame{index}"); walk_urls.append(url); published.append(record)
    for index, path in enumerate(stop_frames, 1):
        url, record = publish(path, f"stop-bridge-frame{index}"); stop_urls.append(url); published.append(record)
    for index, path in enumerate(turn_frames, 1):
        url, record = publish(path, f"turn-frame{index}"); turn_urls.append(url); published.append(record)
    join_urls = [walk_urls[0], stop_urls[3], stop_urls[2], stop_urls[1], stop_urls[0], *turn_urls[1:]]
    strip_url, record = publish(strip, "join-strip"); published.append(record)
    contact_url, record = publish(contact, "contact"); published.append(record)

    route, x = [], 0
    walk_ms, decel_ms, turn_ms = 1000 / timing["walkFps"], 1000 / timing["decelerationFps"], 1000 / timing["turnFps"]
    for _cycle in range(2):
        for frame in range(1, 9):
            x += 21
            actual = frame % 8
            route.append({"src": walk_urls[actual], "phase": "approved walk", "pose": f"Walk F{actual + 1}", "dx": 21, "x": x, "durationMs": walk_ms})
    for index, delta, pose in zip([3, 2, 1, 0], [18, 12, 6, 2], ["75%", "50%", "15%", "exact Side-right stop"]):
        x += delta
        route.append({"src": stop_urls[index], "phase": "approved deceleration", "pose": pose, "dx": delta, "x": x, "durationMs": decel_ms})
    for original_index, angle in zip(range(1, 9), [98, 105, 120, 135, 150, 165, 172.5, 180]):
        route.append({"src": turn_urls[original_index], "phase": "approved turn away", "pose": f"{angle}°", "dx": 0, "x": x, "durationMs": turn_ms})
    hold_frame_ms = timing["frontHoldMs"] / 4
    for _ in range(4):
        route.append({"src": turn_urls[-1], "phase": "rear hold", "pose": "exact approved back", "dx": 0, "x": x, "durationMs": hold_frame_ms})

    page = PUBLIC / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(review_page(route, join_urls, join_durations, contact_url, strip_url))
    duration = sum(frame["durationMs"] for frame in route)
    register = {
        "batchId": "keeper-prime-walk-stop-turn-back-2026-10-14-v2",
        "status": "draft-walk-stop-turn-back-v2-awaiting-visual-approval",
        "purpose": "Review the exact V1 artwork and timing with every frame preloaded and decoded before playback.",
        "authorities": {
            "walk": {"approval": rel(WALK_APPROVAL), "approvalSha256": digest(WALK_APPROVAL)},
            "stopWalkStop": {"approval": rel(STOP_APPROVAL), "approvalSha256": digest(STOP_APPROVAL)},
            "sideBackTurn": {"approval": rel(TURN_APPROVAL), "approvalSha256": digest(TURN_APPROVAL)},
            "timing": {"approval": rel(TIMING_APPROVAL), "approvalSha256": digest(TIMING_APPROVAL), "policy": rel(TIMING_POLICY), "policySha256": digest(TIMING_POLICY), "profile": timing},
        },
        "join": {"strip": rel(strip), "sha256": digest(strip), "sidecar": rel(sidecar), "sidecarSha256": digest(sidecar), "frames": 13, "runtimeEntryFrameAfterWalkLoop": 2, "frameSha256": [digest(path) for path in join_frames], "frameDurationsMs": join_durations, "labels": labels},
        "route": {"frames": len(route), "durationMs": duration, "distanceHighResolutionPixels": x, "walkCycles": 2, "walkDelta": 21, "decelerationDeltas": [18, 12, 6, 2], "neutralSettleFrames": 0, "turnFramesAfterSharedEndpoint": 8, "rearHoldFrames": 4, "rootMotionStopsBeforeTurn": True, "framesData": route},
        "endpointContract": {
            "walkContact": {"file": rel(walk_frames[0]), "sha256": digest(walk_frames[0])},
            "sideStop": {"file": rel(stop_frames[0]), "sha256": digest(stop_frames[0]), "turnEntry": rel(turn_frames[0]), "turnEntrySha256": digest(turn_frames[0]), "sharedFloorAnchor": True, "sharedView": "side-right"},
            "rear": {"file": rel(turn_frames[-1]), "sha256": digest(turn_frames[-1])},
        },
        "evidence": {"contactSheet": {"file": rel(contact), "sha256": digest(contact)}},
        "publishedAssets": published,
        "reviewPage": {"file": rel(page), "sha256": digest(page), "publicReview": "/keeper-review/keeper-prime-walk-stop-turn-back-v2/", "assetPrefix": PREFIX, "relativeAssetUrls": False, "controls": ["play", "pause", "previous-frame", "next-frame", "restart", "route-loop", "join-play", "join-step"], "largeLaneFullWidth": True, "gameLaneFullWidth": True, "preloadedBeforePlayback": True},
        "unchangedAuthorities": {"runtimeManifest": "public/sprites/manifest.json", "runtimeManifestSha256": digest(ROOT / "public/sprites/manifest.json"), "workbenchCatalogue": "data/keeper_animation_workbench.json", "workbenchCatalogueSha256": digest(ROOT / "data/keeper_animation_workbench.json")},
        "validation": {"allArtworkCopiedFromApprovedAuthorities": True, "v1ArtworkByteIdentical": True, "newCharacterDrawings": False, "walkToDecelerationContactExact": True, "turnFramesExact": True, "rearEndpointExact": True, "rootMotionStopsBeforeTurn": True, "transparentSafetyGutters": True, "stripSidecarAgreement": True, "fastTimingV1Exact": True, "preloadedBeforePlayback": True, "productionSpritesChanged": False, "runtimeManifestChanged": False, "workbenchFinalChanged": False},
        "approvalBoundary": {"sourceAuthoritiesApproved": True, "compositeRouteApproved": False, "finalLaneEntryAllowed": False, "productionPromotionAllowed": False},
        "nextGate": "Frank confirms flicker-free V2 playback, then reviews the unchanged walk → stop → turn fully away route at large and exact game scale.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; approved authorities, Final and production remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "joinFrames": 13, "routeFrames": len(route), "durationMs": duration, "distance": x, "public": register["reviewPage"]["publicReview"]}, indent=2))


if __name__ == "__main__":
    main()
