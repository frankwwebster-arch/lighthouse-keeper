#!/usr/bin/env python3
"""Build a reversible oven-context walk/stop/turn-away review page."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-object-approach-oven-2026-10-14-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-object-approach-oven-v1"
TURN_APPROVAL = ROOT / "art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v3/batch-register.json"
ROOT_GATE = ROOT / "art/drafts/keeper-movement-foundation-2026-10-14-v2/batch-register.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    for path in (TURN_APPROVAL, ROOT_GATE):
        if not path.exists():
            raise RuntimeError(f"missing authority: {path.relative_to(ROOT)}")

    base = "/keeper-review/keeper-prime-walk-stop-turn-back-v2/assets/"
    urls = {
        "neutral": base + "stop-bridge-frame1-a172a8a01a387a21.png",
        "bridge15": base + "stop-bridge-frame2-e54546ba14b4e5f7.png",
        "bridge50": base + "stop-bridge-frame3-0169b3642905389d.png",
        "bridge75": base + "stop-bridge-frame4-9f4192beb8fecbc8.png",
        "walkF1": base + "walk-frame1-0e80ea65610452c9.png",
        "walkF2": base + "walk-frame2-2b8e91de747b527d.png",
        "walkF3": base + "walk-frame3-b376254e9c29da38.png",
        "walkF4": base + "walk-frame4-982646b0b0e6f3f9.png",
        "walkF5": base + "walk-frame5-545e7338151e6e5a.png",
        "walkF6": base + "walk-frame6-17d007eee75c2e86.png",
        "walkF7": base + "walk-frame7-dbf5b3849624cec7.png",
        "walkF8": base + "walk-frame8-cf8c53e7ffa703a5.png",
        "turn98": base + "turn-frame2-e1dc020aabfe8f3b.png",
        "turn105": base + "turn-frame3-34028d8821a7272a.png",
        "turn120": base + "turn-frame4-0d278363a0e7e4f1.png",
        "turn135": base + "turn-frame5-f827ac61f45aaaa4.png",
        "turn150": base + "turn-frame6-fe06522abd0cd55c.png",
        "turn165": base + "turn-frame7-d55afae023051e29.png",
        "turn172": base + "turn-frame8-bb530610cf0e17bf.png",
        "back": base + "turn-frame9-31dbac4efc00089f.png",
    }
    pose_order = [
        ("bridge15", "accelerate", "15% bridge", 100),
        ("bridge50", "accelerate", "50% bridge", 100),
        ("bridge75", "accelerate", "75% bridge", 100),
        ("walkF1", "accelerate", "Walk F1 contact", 100),
        ("walkF2", "walk", "Walk F2", 100),
        ("walkF3", "walk", "Walk F3", 100),
        ("walkF4", "walk", "Walk F4", 100),
        ("walkF5", "walk", "Walk F5", 100),
        ("walkF6", "walk", "Walk F6", 100),
        ("walkF7", "walk", "Walk F7", 100),
        ("walkF8", "walk", "Walk F8", 100),
        ("walkF1", "walk", "Walk F1 contact", 100),
        ("bridge75", "decelerate", "75% bridge", 1000 / 12),
        ("bridge50", "decelerate", "50% bridge", 1000 / 12),
        ("bridge15", "decelerate", "15% bridge", 1000 / 12),
        ("neutral", "stop", "exact Side-right stop", 1000 / 12),
        ("turn98", "turn", "98°", 62.5),
        ("turn105", "turn", "105°", 62.5),
        ("turn120", "turn", "120°", 62.5),
        ("turn135", "turn", "135°", 62.5),
        ("turn150", "turn", "150°", 62.5),
        ("turn165", "turn", "165°", 62.5),
        ("turn172", "turn", "172.5°", 62.5),
        ("back", "turn", "exact approved back", 62.5),
        ("back", "hold", "ready at oven", 625),
    ]
    profiles = {
        "candidate": [3, 7, 13, 19] + [21] * 8 + [19, 13, 7, 3] + [0] * 9,
        "approved": [2, 6, 12, 18] + [21] * 8 + [18, 12, 6, 2] + [0] * 9,
    }
    frames = [
        {"src": urls[key], "phase": phase, "pose": pose, "durationMs": duration}
        for key, phase, pose, duration in pose_order
    ]
    payload = {
        "frames": frames,
        "profiles": {
            "candidate": {"label": "Grid-perfect candidate", "deltasKu": profiles["candidate"], "totalKu": sum(profiles["candidate"])},
            "approved": {"label": "Current approved root distance", "deltasKu": profiles["approved"], "totalKu": sum(profiles["approved"])},
        },
        "room": {"widthLp": 172, "heightLp": 56},
        "oven": {"centreLp": 120, "widthLp": 30, "heightLp": 30, "label": "OVEN PLACEHOLDER"},
        "targetRootKu": 960,
        "candidateStartRootKu": 708,
        "anchorKu": 128,
    }

    PACK.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    page = PAGE.replace("__PAYLOAD__", json.dumps(payload, separators=(",", ":")))
    write(PUBLIC / "index.html", page)

    register = {
        "batchId": "keeper-object-approach-oven-2026-10-14-v1",
        "status": "draft-asset-context-root-motion-awaiting-review",
        "purpose": "Show the proposed 42-ku bridge in a complete walk, stop and approved turn-away flow at an opaque 30-lp oven placeholder.",
        "authorities": {
            "approvedWalkStopTurnAway": {"file": str(TURN_APPROVAL.relative_to(ROOT)), "sha256": digest(TURN_APPROVAL)},
            "rootMotionGateV2": {"file": str(ROOT_GATE.relative_to(ROOT)), "sha256": digest(ROOT_GATE)},
        },
        "reviewPage": {"file": str((PUBLIC / "index.html").relative_to(ROOT)), "sha256": digest(PUBLIC / "index.html")},
        "asset": {"kind": "opaque-placeholder", "label": "oven", "footprintLp": [30, 30], "centreLp": 120, "artAuthority": False},
        "route": {
            "roomLp": [172, 56],
            "startRootKu": 708,
            "targetRootKu": 960,
            "candidateDistanceKu": 252,
            "candidateDistanceLp": 31.5,
            "currentDistanceKu": 244,
            "currentMissKu": 8,
            "currentMissLp": 1,
            "candidateDeltasKu": profiles["candidate"],
            "approvedDeltasKu": profiles["approved"],
            "frameCount": len(frames),
            "finishedFacing": "back-to-camera",
            "pixelsReusedExactly": True,
            "preloadedBeforePlayback": True,
        },
        "validation": {
            "candidateClosesThreeLatticeIntervals": sum(profiles["candidate"]) == 3 * 84,
            "candidateEndsAtAssetAnchor": 708 + sum(profiles["candidate"]) == 960,
            "currentStopsOneLogicalPixelShort": 960 - (708 + sum(profiles["approved"])) == 8,
            "turnRootMotionZero": all(delta == 0 for delta in profiles["candidate"][16:]),
            "canonicalArtworkChanged": False,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "approvalChanged": False,
        },
        "rollback": "Delete only this V1 pack and public page. All approved art, prior reviews, Final and production remain unchanged.",
    }
    write(PACK / "batch-register.json", json.dumps(register, indent=2) + "\n")
    write(PACK / "HANDOFF.md", """# Keeper object approach: oven V1\n\nThis is an asset-context review of the already proposed candidate-42 root motion. It uses the exact approved walk, stop-bridge and Turn V9 pixels. The opaque 30 × 30 logical-pixel oven is a layout placeholder, not proposed oven artwork.\n\nThe default route travels three 10.5-lp lattice intervals: 42 ku acceleration, one 168-ku walk cycle and 42 ku deceleration, then turns on a fixed root to the exact approved rear endpoint. The comparison toggle shows the current approved 38/38-ku bridges stopping exactly 1 lp short from the same origin. Nothing is promoted.\n""")
    print(json.dumps({"page": str((PUBLIC / 'index.html').relative_to(ROOT)), "frames": len(frames), "candidateKu": sum(profiles["candidate"])}, indent=2))


PAGE = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper oven approach V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1480px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.profile{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.profile button.on{outline:3px solid #75e6a7;background:#183d2a}.stageWrap{overflow:auto;padding-bottom:5px}.stage{position:relative;overflow:hidden;border:1px solid #496878;border-radius:8px;background:linear-gradient(#17313e 0 75%,#293a35 75% 100%)}.full{width:690px;height:226px}.detail{width:962px;height:450px}.floor{position:absolute;left:0;right:0;bottom:0;background:#75583d;border-top:2px solid #d3ae75}.full .floor{height:8px}.detail .floor{height:16px}.asset{position:absolute;bottom:0;background:#6d737b;border:3px solid #dbe1e7;color:white;display:flex;align-items:flex-start;justify-content:center;text-align:center;font-weight:800;letter-spacing:.06em;padding-top:8px}.asset:before{content:'';position:absolute;inset:14% 14% 46%;border:2px solid #cbd1d6}.asset:after{content:'';position:absolute;left:18%;right:18%;bottom:18%;height:6%;background:#d8dde1}.target{position:absolute;top:0;bottom:0;border-left:2px dashed #75e6a7}.target span{position:absolute;top:5px;left:5px;color:#9af1ba;white-space:nowrap;font-size:12px}.keeper{position:absolute;bottom:0;image-rendering:auto;z-index:2}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.key{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.key div{border-top:4px solid;padding:8px;background:#0c1d26}.accelerate{border-color:#70b7ff!important}.walk{border-color:#8ed7ff!important}.decelerate,.stop{border-color:#e8b852!important}.turn,.hold{border-color:#c696ff!important}.note{color:#c9e4ee}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.metric{font-size:1.5rem;font-weight:800;color:#75e6a7}.phasebar{display:flex;height:8px;overflow:hidden;border-radius:99px;background:#213844;margin:10px 0}.phasebar span{display:block}.phasebar .p-accelerate{background:#70b7ff}.phasebar .p-walk{background:#8ed7ff}.phasebar .p-decelerate,.phasebar .p-stop{background:#e8b852}.phasebar .p-turn,.phasebar .p-hold{background:#c696ff}@media(max-width:760px){.key,.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-root-motion-gate-v2/">← Root-motion Gate V2</a><h1>Oven approach V1 · walk → stop → turn fully away</h1><span class="status">Asset-context draft · nothing promoted</span><p>The oven is deliberately an opaque block. Every Keeper image is exact approved artwork; only the candidate root translation remains under review.</p></header><main><p class="rule"><strong>What to judge:</strong> he should approach at a brisk natural pace, decelerate onto the green oven interaction line without skating, stop cleanly, then turn on the spot until his back faces the player and he is ready to use the oven.</p><article><div class="profile"><button id="candidateProfile" class="on" disabled>Grid-perfect candidate · lands exactly</button><button id="approvedProfile" disabled>Current approved distance · 1 lp short</button></div><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox"> Loop for inspection (restarts from origin)</label></div><p id="loading" class="readout">Loading and decoding every unique approved frame…</p><p id="readout" class="readout"></p><div class="phasebar" id="phasebar"></div><div class="key"><div class="accelerate"><strong>1 · Start walking</strong><br>42-ku acceleration</div><div class="walk"><strong>2 · Full stride</strong><br>one eight-frame cycle</div><div class="decelerate"><strong>3 · Stop</strong><br>42-ku deceleration</div><div class="turn"><strong>4 · Face oven</strong><br>exact approved rear turn</div></div></article><article><h2>Full 172 × 56 lp room · exact 4× authoring ruler</h2><p class="note">The 30 × 30 lp oven block sits on the rear wall. The Keeper finishes on its centre interaction anchor. This is an authoring ruler, not a fixed device size.</p><div class="stageWrap"><div class="stage full" id="fullStage"><div class="floor"></div><div class="asset">OVEN<br>30 × 30 lp</div><div class="target"><span>oven interaction root</span></div><img class="keeper" alt="Keeper approaching the oven"></div></div></article><article><h2>Large 8× inspection · approach and turn</h2><div class="stageWrap"><div class="stage detail" id="detailStage"><div class="floor"></div><div class="asset">OVEN<br>PLACEHOLDER</div><div class="target"><span>exact target</span></div><img class="keeper" alt="Large Keeper oven approach inspection"></div></div></article><section class="metrics"><article><div class="metric">31.5 lp</div><strong>candidate travel</strong><p>Three exact 10.5-lp lattice intervals.</p></article><article><div class="metric">1 lp short</div><strong>current comparison</strong><p>Same start and pixels; only the existing root schedule changes.</p></article><article><div class="metric">0 root motion</div><strong>during turn</strong><p>His floor anchor remains fixed from stop through the rear endpoint.</p></article></section><article><h2>Boundary</h2><p>The grey oven is only a scale and placement proxy. It is not oven artwork and cannot be promoted. This page changes no approved PNG, timing authority, Final lane, sprite manifest or runtime logic.</p></article></main><script>
const DATA=__PAYLOAD__;let profile='candidate',index=0,timer=null;const buttons=[...document.querySelectorAll('button')],unique=[...new Set(DATA.frames.map(f=>f.src))];
const stages=[{el:document.getElementById('fullStage'),scale:4,leftLp:0},{el:document.getElementById('detailStage'),scale:8,leftLp:60}];
function cumulative(i){return DATA.profiles[profile].deltasKu.slice(0,i+1).reduce((a,b)=>a+b,0)}
function configureStage({el,scale,leftLp}){const oven=el.querySelector('.asset'),target=el.querySelector('.target'),floor=el.querySelector('.floor');oven.style.left=`${(DATA.oven.centreLp-DATA.oven.widthLp/2-leftLp)*scale}px`;oven.style.width=`${DATA.oven.widthLp*scale}px`;oven.style.height=`${DATA.oven.heightLp*scale}px`;target.style.left=`${(DATA.oven.centreLp-leftLp)*scale}px`;floor.style.width=`${DATA.room.widthLp*scale}px`}
stages.forEach(configureStage);
const phaseWidths={accelerate:4,walk:8,decelerate:3,stop:1,turn:8,hold:1};document.getElementById('phasebar').innerHTML=Object.entries(phaseWidths).map(([phase,n])=>`<span class="p-${phase}" style="flex:${n}"></span>`).join('');
function render(){const f=DATA.frames[index],xKu=DATA.candidateStartRootKu+cumulative(index),targetGap=(DATA.targetRootKu-xKu)/8;stages.forEach(({el,scale,leftLp})=>{const img=el.querySelector('.keeper');img.src=f.src;img.style.width=`${32*scale}px`;img.style.height=`${40*scale}px`;img.style.left=`${(xKu/8-16-leftLp)*scale}px`});document.getElementById('readout').textContent=`${DATA.profiles[profile].label} · F${index+1}/${DATA.frames.length} · ${f.phase} · ${f.pose} · root ${xKu} ku · ${targetGap.toFixed(1)} lp before target`;document.querySelectorAll('.key div').forEach(x=>x.style.opacity=x.classList.contains(f.phase)||(f.phase==='stop'&&x.classList.contains('decelerate'))||(f.phase==='hold'&&x.classList.contains('turn'))?'1':'.45')}
function pause(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index===DATA.frames.length-1){if(document.getElementById('loop').checked)index=0;else{pause();return}}else index++;render();timer=setTimeout(tick,DATA.frames[index].durationMs)}function play(){pause();timer=setTimeout(tick,DATA.frames[index].durationMs)}function choose(next){pause();profile=next;index=0;document.getElementById('candidateProfile').classList.toggle('on',profile==='candidate');document.getElementById('approvedProfile').classList.toggle('on',profile==='approved');render();play()}
document.getElementById('candidateProfile').onclick=()=>choose('candidate');document.getElementById('approvedProfile').onclick=()=>choose('approved');document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{pause();index=(index-1+DATA.frames.length)%DATA.frames.length;render()};document.getElementById('next').onclick=()=>{pause();index=(index+1)%DATA.frames.length;render()};document.getElementById('restart').onclick=()=>{pause();index=0;render();play()};
function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}async function start(){try{await Promise.all(unique.map(preload));buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All approved frames ready · candidate shown by default';render();play()}catch(error){document.getElementById('loading').textContent=`A frame failed to load; playback remains locked. ${error.message}`}}start();
</script></body></html>'''


if __name__ == "__main__":
    main()
