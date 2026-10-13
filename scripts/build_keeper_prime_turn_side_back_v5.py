#!/usr/bin/env python3
"""Record V4 approval and publish synchronized large/game-scale review controls."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v5"
PRIOR_PACK = ROOT / "art/drafts/keeper-prime-turn-side-back-2026-10-13-v4"
PRIOR_REGISTER = PRIOR_PACK / "batch-register.json"
PUBLIC = ROOT / "public/keeper-review/keeper-prime-turn-side-back-v5"
PUBLIC_ROUTE = "/keeper-review/keeper-prime-turn-side-back-v5"
ASSET_CONTRACT = ROOT / "data/keeper_asset_contract.json"
SPRITE_RENDERER = ROOT / "src/ui/Sprite.tsx"
ANGLES = (90, 98, 105, 120, 135, 150, 165, 180)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_assets(frames: list[Path], comparison: Path, contact: Path) -> dict[str, str]:
    assets = PUBLIC / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True, exist_ok=True)
    sources = {f"frame{index + 1}": path for index, path in enumerate(frames)}
    sources.update({"comparison": comparison, "contact": contact})
    urls: dict[str, str] = {}
    for key, source in sources.items():
        target = assets / f"{key}-{digest(source)[:16]}{source.suffix}"
        shutil.copyfile(source, target)
        urls[key] = target.name
    return urls


def write_page(frames: list[Path], comparison: Path, contact: Path) -> Path:
    urls = copy_assets(frames, comparison, contact)
    asset = lambda key: f"{PUBLIC_ROUTE}/assets/{urls[key]}"
    frames_json = json.dumps([asset(f"frame{index + 1}") for index in range(8)])
    angles_json = json.dumps(list(ANGLES))
    thumbnails = "".join(
        f'<button class="thumb" data-frame="{index}" aria-label="Show frame {index + 1}"><img src="{asset(f"frame{index + 1}")}" alt=""><span>F{index + 1} · {ANGLES[index]}°</span></button>'
        for index in range(8)
    )
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Approved Keeper Prime side ↔ back Turn V4</title><style>:root{{color-scheme:dark;--bg:#0b1218;--panel:#17232d;--line:#40515e;--ink:#edf5fa;--green:#77e3a4;--amber:#efbd58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}header,main{{max-width:1480px;margin:auto;padding:22px}}header{{border-bottom:1px solid var(--line)}}a{{color:#8ed2fa}}.status{{display:inline-block;border:1px solid var(--green);border-radius:999px;padding:5px 10px;color:#a9f3c5}}article{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:14px 0}}.review-grid{{display:grid;grid-template-columns:minmax(330px,1fr) minmax(290px,.72fr);gap:18px;align-items:start}}.large-stage{{width:min(100%,512px);aspect-ratio:4/5;margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/24px 24px}}.large-stage img{{display:block;width:100%;height:100%;object-fit:contain;image-rendering:auto}}.game-wrap{{min-height:230px;display:grid;place-items:center}}.game-stage{{width:128px;height:160px;flex:none;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/8px 8px;outline:1px solid #6f8492}}.game-stage img{{display:block;width:128px;height:160px;object-fit:contain;image-rendering:pixelated}}.controls button,.thumb{{font:inherit;color:var(--ink);background:#111a21;border:1px solid var(--line);border-radius:6px;margin:4px;padding:8px 11px;cursor:pointer}}.controls button:hover,.controls button:focus-visible,.thumb:hover,.thumb:focus-visible{{border-color:#8ed2fa}}.controls .step{{border-color:var(--amber)}}.active{{background:#185f3a!important;border-color:var(--green)!important}}input{{font:inherit;vertical-align:middle}}.frames{{display:grid;grid-template-columns:repeat(8,minmax(82px,1fr));gap:8px;overflow:auto;margin:14px 0}}.thumb{{margin:0;padding:5px}}.thumb img{{display:block;width:100%;aspect-ratio:4/5;object-fit:contain;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/12px 12px}}.thumb span{{display:block;white-space:nowrap}}.wide{{width:100%;background:#101820}}.rule{{border-left:4px solid var(--green);background:#17291f;padding:10px 14px}}.scale-note{{color:#c7d7e0}}@media(max-width:850px){{.review-grid{{grid-template-columns:1fr}}}}</style></head><body><header><a href="/keeper-review/keeper-prime-turn-side-back-v4">← Immutable V4 candidate</a><h1>Keeper Prime Turn V4 · side-right ↔ back</h1><span class="status">Approved artwork authority · 13 October 2026</span><p>Frank approved the exact V4 animation with “Approved.” This page adds review controls and scale views only; every animation frame remains byte-identical to V4.</p></header><main><p class="rule"><strong>Two synchronized views:</strong> the left view is enlarged for inspection. The right view is the proposed game size: 32 × 40 logical pixels rendered by the current game at PX=4, giving an exact 128 × 160 CSS-pixel box.</p><section class="review-grid"><article><h2>Large inspection view</h2><div class="large-stage"><img id="largePlayer" src="{asset('frame1')}" alt="Large approved Keeper turn view"></div></article><article><h2>Proposed in-game size</h2><div class="game-wrap"><div class="game-stage"><img id="gamePlayer" src="{asset('frame1')}" alt="Approved Keeper turn at proposed game size"></div></div><p class="scale-note">Exact display box: 128 × 160 CSS px at the game's current 4 px per logical pixel. Keep browser zoom at 100% for a direct screen-size judgement.</p></article></section><article class="controls"><h2 id="frameLabel">Frame 1 of 8 · 90°</h2><p id="mode">Looping side ↔ back</p><div><button id="previous" class="step">← Previous frame</button><button id="next" class="step">Next frame →</button></div><div><button id="forward">Side → back</button><button id="reverse">Back → side</button><button id="pingpong">Loop both</button><button id="pause">Pause</button></div><label>Frame time <input id="speed" type="range" min="80" max="500" value="125"> <span id="speedValue">125 ms</span></label></article><section class="frames">{thumbnails}</section><h2>Approved V4 evidence</h2><article><img class="wide" src="{asset('comparison')}" alt="Approved F7 to F8 boot comparison and ghost overlay"></article><article><img class="wide" src="{asset('contact')}" alt="All eight approved side-to-back turn frames"></article><h2>Approval boundary</h2><article><p>The exact V4 frames, forward strip, reverse strip, registered standard-uniform palette and rear boot endpoint are approved as a core-turn artwork authority. This page does not alter Final, production sprites or the runtime manifest.</p></article></main><script>const frames={frames_json},angles={angles_json};const large=document.getElementById('largePlayer'),game=document.getElementById('gamePlayer'),label=document.getElementById('frameLabel'),mode=document.getElementById('mode'),speed=document.getElementById('speed'),speedValue=document.getElementById('speedValue');let timer=null,index=0,sequence=[],cursor=0,loop=false;function show(i){{index=(i+frames.length)%frames.length;large.src=frames[index];game.src=frames[index];label.textContent=`Frame ${{index+1}} of ${{frames.length}} · ${{angles[index]}}°`;document.querySelectorAll('[data-frame]').forEach(button=>button.classList.toggle('active',Number(button.dataset.frame)===index));}}function stop(message='Paused'){{if(timer)clearTimeout(timer);timer=null;mode.textContent=message;}}function step(delta){{stop('Paused · frame stepping');show(index+delta);}}function play(seq,repeat,name){{stop();sequence=seq;cursor=0;loop=repeat;mode.textContent=name;const tick=()=>{{show(sequence[cursor]);cursor+=1;if(cursor>=sequence.length){{if(loop)cursor=0;else{{stop('Finished');return}}}}timer=setTimeout(tick,Number(speed.value));}};tick();}}document.getElementById('previous').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('forward').onclick=()=>play([0,1,2,3,4,5,6,7],false,'Playing side → back');document.getElementById('reverse').onclick=()=>play([7,6,5,4,3,2,1,0],false,'Playing back → side');document.getElementById('pingpong').onclick=()=>play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');document.getElementById('pause').onclick=()=>stop();speed.oninput=()=>speedValue.textContent=`${{speed.value}} ms`;document.querySelectorAll('[data-frame]').forEach(button=>button.onclick=()=>{{stop('Paused · selected frame');show(Number(button.dataset.frame));}});show(0);play([0,1,2,3,4,5,6,7,6,5,4,3,2,1],true,'Looping side ↔ back');</script></body></html>'''
    PUBLIC.mkdir(parents=True, exist_ok=True)
    page_path = PUBLIC / "index.html"
    page_path.write_text(page)
    return page_path


def main() -> None:
    prior = json.loads(PRIOR_REGISTER.read_text())
    frames = [ROOT / item["file"] for item in prior["frames"]]
    comparison = ROOT / prior["evidence"]["comparison"]["file"]
    contact = ROOT / prior["evidence"]["contactSheet"]["file"]
    page = write_page(frames, comparison, contact)
    register = {
        "batchId": "keeper-prime-turn-side-back-2026-10-13-v5",
        "status": "approved-side-back-turn-artwork-authority",
        "purpose": "Preserve Frank's approval of exact Turn V4 artwork and add an independently versioned synchronized large/game-scale review surface without changing V4.",
        "approval": {
            "approvedBy": "Frank", "approvedOn": "2026-10-13", "wording": "Approved.",
            "scope": "The exact eight-frame reversible Keeper Prime side-right-to-back Turn V4, including its corrected F8 standard-uniform palette and rear-facing boot construction."
        },
        "approvedCandidate": {
            "register": rel(PRIOR_REGISTER), "registerSha256": digest(PRIOR_REGISTER),
            "frames": [{"frame": index + 1, "file": rel(path), "sha256": digest(path)} for index, path in enumerate(frames)],
            "forwardStrip": prior["animation"]["forward"], "reverseStrip": prior["animation"]["reverse"],
            "palette": prior["palette"], "rearBootChangedMask": prior["bootRedraw"]["changedMask"], "rearBootChangedMaskSha256": prior["bootRedraw"]["changedMaskSha256"]
        },
        "displayContract": {
            "logicalCell": [32, 40], "sourceCell": [256, 320], "sourceDensity": 8,
            "gamePixelsPerLogicalPixel": 4, "gameCssDisplay": [128, 160], "browserZoomForDirectSizeJudgementPercent": 100,
            "assetContract": rel(ASSET_CONTRACT), "assetContractSha256": digest(ASSET_CONTRACT),
            "spriteRenderer": rel(SPRITE_RENDERER), "spriteRendererSha256": digest(SPRITE_RENDERER),
            "method": "The exact density-8 V4 PNG is rendered into the same 32×40 logical box at the game's current PX=4; no review-only character scaling is applied."
        },
        "reviewSurface": {
            "publicReview": f"{PUBLIC_ROUTE}/", "publicPage": rel(page), "publicPageSha256": digest(page),
            "controls": ["previous-frame", "next-frame", "play-forward", "play-reverse", "loop-both", "pause", "frame-time", "direct-frame-selection"],
            "views": ["large-inspection", "game-scale-128x160"], "viewsFrameSynchronized": True
        },
        "validation": {
            "v4RegisterUnchanged": True, "allApprovedFrameHashesPinned": True, "publicFramesByteIdenticalToV4": True,
            "largeAndGameViewsUseSameFrameUrls": True, "artPixelsChangedByV5": False, "productionSpritesChanged": False,
            "runtimeManifestChanged": False, "finalLaneChanged": False, "priorDraftsChanged": False
        },
        "approvalBoundary": {
            "sideBackTurnV4Approved": True, "rearBootEndpointApproved": True, "standardOutfitPaletteApproved": True,
            "coreTurnArtworkAuthority": True, "finalLaneEntryAllowed": True, "productionPromotionAllowed": False
        },
        "nextGate": "Use this synchronized large/game-scale control set for later core-animation reviews. Production promotion remains a separate explicit gate.",
        "rollback": f"Delete only {rel(PACK)} and {rel(PUBLIC)}; immutable V1–V4, approved endpoints and production remain unchanged."
    }
    dump(PACK / "batch-register.json", register)
    print(json.dumps({"batch": register["batchId"], "approvedFrames": len(frames), "gameDisplay": register["displayContract"]["gameCssDisplay"], "public": rel(page)}, indent=2))


if __name__ == "__main__":
    main()
