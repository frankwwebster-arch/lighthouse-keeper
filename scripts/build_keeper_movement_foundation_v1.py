#!/usr/bin/env python3
"""Build the reversible root-motion gate and vertical-circulation construction lab."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-movement-foundation-2026-10-14-v1"
GATE = ROOT / "public/keeper-review/keeper-root-motion-gate-v1"
CIRCULATION = ROOT / "public/keeper-review/keeper-vertical-circulation-v1"

AUTHORITIES = {
    "neutral": ROOT / "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png",
    "bridge15": ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f2.png",
    "bridge50": ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f3.png",
    "bridge75": ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f4.png",
    "walkF1": ROOT / "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f1.png",
}

EXPECTED = {
    "neutral": "a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3",
    "bridge15": "e54546ba14b4e5f7f042677f7c5babc83df99943d1bc0a8f482f7188d0c96930",
    "bridge50": "0169b3642905389dfe1846b054ce463653708d971aef7a588f834dcbf8c9714c",
    "bridge75": "9f4192beb8fecbc80de4530725a9431a4df8ad9adc3b86df66ad7159728c2b29",
    "walkF1": "0e80ea65610452c93a1ebe48424dddcc5709a77340b4bc1e93dddff38809e656",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def dump(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2) + "\n")


def gate_page(urls: dict[str, str]) -> str:
    frames = [
        {"pose": "15% bridge", "key": "bridge15"},
        {"pose": "50% bridge", "key": "bridge50"},
        {"pose": "75% bridge", "key": "bridge75"},
        {"pose": "Walk F1 contact", "key": "walkF1"},
        {"pose": "75% bridge", "key": "bridge75"},
        {"pose": "50% bridge", "key": "bridge50"},
        {"pose": "15% bridge", "key": "bridge15"},
        {"pose": "exact stop", "key": "neutral"},
    ]
    payload = {
        "frames": [{**item, "src": urls[item["key"]]} for item in frames],
        "profiles": [
            {"id": "approved", "label": "Current approved bridge · 76 ku", "deltas": [2, 6, 12, 18, 18, 12, 6, 2], "colour": "#70b7ff"},
            {"id": "candidate", "label": "Proposed lattice bridge · 84 ku", "deltas": [3, 7, 13, 19, 19, 13, 7, 3], "colour": "#75e6a7"},
        ],
        "frameMs": 100,
    }
    return GATE_HTML.replace("__PAYLOAD__", json.dumps(payload, separators=(",", ":")))


def circulation_page(spec: dict) -> str:
    return CIRCULATION_HTML.replace("__SPEC__", json.dumps(spec, separators=(",", ":")))


def main() -> None:
    for key, path in AUTHORITIES.items():
        if not path.exists() or digest(path) != EXPECTED[key]:
            raise RuntimeError(f"authority changed: {rel(path)}")

    source_register = ROOT / "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/batch-register.json"
    rig = ROOT / "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json"
    room = ROOT / "docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md"
    for path in (source_register, rig, room):
        if not path.exists():
            raise RuntimeError(f"missing authority: {rel(path)}")

    for directory in (PACK, GATE, CIRCULATION):
        directory.mkdir(parents=True, exist_ok=True)
    assets = GATE / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir()
    urls: dict[str, str] = {}
    published = []
    for key, source in AUTHORITIES.items():
        target = assets / f"{key}-{EXPECTED[key][:16]}.png"
        shutil.copyfile(source, target)
        urls[key] = f"/keeper-review/keeper-root-motion-gate-v1/assets/{target.name}"
        published.append({"key": key, "source": rel(source), "sourceSha256": digest(source), "public": rel(target), "publicSha256": digest(target), "byteIdentical": True})

    geometry = {
        "units": {"kuPerLogicalPixel": 8, "walkingPitchKu": 84, "walkingPitchLogicalPixels": 10.5},
        "floor": {"clearHeightLogicalPixels": 56, "sharedDeckLogicalPixels": 4, "finishedFloorPitchLogicalPixels": 60, "finishedFloorPitchKu": 480},
        "stair": {
            "coreWidthLogicalPixels": 105,
            "coreWidthKu": 840,
            "landingRootMarginLogicalPixels": 10.5,
            "flightRunLogicalPixels": 84,
            "flightRunKu": 672,
            "flightWalkingIntervals": 8,
            "risersPerFlight": 16,
            "riserLogicalPixels": 3.75,
            "riserKu": 30,
            "treadLogicalPixels": 5.25,
            "treadKu": 42,
            "angleDegrees": 35.54,
            "keeperBootLengthLogicalPixels": 8,
            "supportedBootFraction": 0.65625,
            "directionRule": "floor parity alternates bottom-right-to-top-left and bottom-left-to-top-right",
        },
        "ladder": {"vertical": True, "rungPitchLogicalPixels": 7.5, "rungPitchKu": 60, "intervalsPerFloor": 8, "railWidthLogicalPixels": 18, "fullCyclesPerFloor": 4},
        "lift": {"verticalStopPitchLogicalPixels": 60, "verticalStopPitchKu": 480, "doorOpeningLogicalPixels": 44, "entryDepthScale": 0.78, "entryRiseLogicalPixels": 6},
        "keeper": {"standingHeightLogicalPixels": 38, "frontWidthLogicalPixels": 19, "sideWidthLogicalPixels": 13, "maximumStrideWidthLogicalPixels": 24, "bootLengthLogicalPixels": 8},
    }
    dump(PACK / "geometry/keeper-vertical-circulation-v1.json", geometry)

    gate = gate_page(urls)
    circulation = circulation_page(geometry)
    write(GATE / "index.html", gate)
    write(CIRCULATION / "index.html", circulation)

    register = {
        "batchId": "keeper-movement-foundation-2026-10-14-v1",
        "status": "draft-root-motion-and-vertical-circulation-awaiting-review",
        "purpose": "Resolve the horizontal 84-ku root-motion gate and measure ladder, alternating-flight stair and lift transitions before any finished-art animation is drawn.",
        "authorities": {
            "approvedStopWalkStop": {"file": rel(source_register), "sha256": digest(source_register)},
            "approvedConstructionRig": {"file": rel(rig), "sha256": digest(rig)},
            "roomGrid172": {"file": rel(room), "sha256": digest(room)},
        },
        "publishedAssets": published,
        "rootMotionGate": {
            "page": rel(GATE / "index.html"),
            "pageSha256": digest(GATE / "index.html"),
            "approvedDeltasKu": [2, 6, 12, 18, 18, 12, 6, 2],
            "approvedDistanceKu": 76,
            "candidateDeltasKu": [3, 7, 13, 19, 19, 13, 7, 3],
            "candidateDistanceKu": 84,
            "exactApprovedPixels": True,
            "preloadedBeforePlayback": True,
        },
        "verticalCirculation": {"page": rel(CIRCULATION / "index.html"), "pageSha256": digest(CIRCULATION / "index.html"), "geometry": rel(PACK / "geometry/keeper-vertical-circulation-v1.json"), "geometrySha256": digest(PACK / "geometry/keeper-vertical-circulation-v1.json")},
        "routes": ["stairs-continue", "stairs-exit-far", "stairs-exit-near", "ladder-continue", "ladder-exit", "lift-enter", "lift-exit"],
        "validation": {
            "stairRiseMatchesFinishedFloorPitch": geometry["stair"]["risersPerFlight"] * geometry["stair"]["riserKu"] == geometry["floor"]["finishedFloorPitchKu"],
            "stairRunMatchesEightWalkIntervals": geometry["stair"]["flightRunKu"] == 8 * geometry["units"]["walkingPitchKu"],
            "treadAndRiserIntegralKu": True,
            "ladderRiseMatchesFinishedFloorPitch": geometry["ladder"]["intervalsPerFloor"] * geometry["ladder"]["rungPitchKu"] == geometry["floor"]["finishedFloorPitchKu"],
            "liftPitchMatchesFinishedFloorPitch": geometry["lift"]["verticalStopPitchKu"] == geometry["floor"]["finishedFloorPitchKu"],
            "canonicalArtworkChanged": False,
            "productionSpritesChanged": False,
            "runtimeManifestChanged": False,
            "workbenchFinalChanged": False,
        },
        "approvalBoundary": {"geometryApproved": False, "rootMotionCandidateApproved": False, "constructionMotionApproved": False, "finishedArtworkApproved": False, "productionPromotionAllowed": False},
        "rollback": f"Delete only {rel(PACK)}, {rel(GATE)} and {rel(CIRCULATION)}; approved art, Final and runtime remain unchanged.",
    }
    dump(PACK / "batch-register.json", register)
    write(PACK / "HANDOFF.md", HANDOFF)
    write(PACK / "PROMPT_LOG.md", PROMPT_LOG)
    print(json.dumps({"batch": register["batchId"], "gate": rel(GATE / "index.html"), "circulation": rel(CIRCULATION / "index.html"), "stair": geometry["stair"], "ladder": geometry["ladder"]}, indent=2))


HANDOFF = """# Keeper movement foundation V1 handoff

Date: 14 October 2026
Status: draft construction evidence awaiting Frank's review; no finished art and no promotion.

This batch deliberately separates two decisions. The root-motion page compares the exact approved F1 bridge pixels at 76 ku with the proposed 84-ku lattice bridge. The circulation page is a measured mannequin study for alternating stair flights, a straight ladder and lift entry/exit. It does not pretend that construction lines are final Keeper art.

The vertical module is proposed as 56 lp clear room height plus one shared 4 lp structural deck, or 60 lp finished-floor to finished-floor. The stair uses sixteen equal 3.75 lp risers and sixteen 5.25 lp horizontal advances. One flight therefore rises exactly 60 lp and runs exactly 84 lp, which is eight ordinary 10.5 lp walking intervals. A 105 lp stair core leaves a 10.5 lp standing/turning margin at each end.

The ladder has eight 7.5 lp rung intervals per floor. A two-rung gait cycle repeats four times per floor. The lift shares the exact 60 lp stop pitch. All three systems can add or remove a floor without changing any other floor.

Approval of this study would authorize finished-art keyframes in later versioned draft batches. It does not promote the 42-ku root bridge, resize the room, replace the prior 38-lp placeholder stair core or change production.
"""

PROMPT_LOG = """# Prompt/provenance log

No generative image model was used. The root-motion page copies five already approved 256 × 320 PNG authorities byte-for-byte. The circulation page is deterministic browser SVG generated from the documented Keeper measurements and the JSON geometry contract in this batch.
"""

GATE_HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper root-motion Gate 1 V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1480px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #e8b852;background:#18251d;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:6px;align-items:center;flex-wrap:wrap}button{font:inherit;color:white;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.row{display:grid;grid-template-columns:210px minmax(680px,1fr);gap:14px;align-items:center;margin:18px 0}.lane{position:relative;overflow:hidden;border:1px solid #496878;border-radius:8px;background:repeating-conic-gradient(#1b3440 0 25%,#122833 0 50%) 50%/24px 24px}.large{height:330px}.large img{position:absolute;width:256px;height:320px;bottom:5px}.game{height:165px;max-width:760px}.game img{position:absolute;width:128px;height:160px;bottom:2px}.mark{position:absolute;bottom:0;top:0;border-left:1px dashed;opacity:.8}.baseline{position:absolute;left:0;right:0;bottom:5px;border-top:1px solid #e8b852}.game .baseline{bottom:2px}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}.metric{font-size:22px;font-weight:700}.ok{color:#75e6a7}.warn{color:#e8b852}table{border-collapse:collapse;width:100%}th,td{padding:8px;border-bottom:1px solid #2c4a59;text-align:left;font-variant-numeric:tabular-nums}@media(max-width:900px){.row{grid-template-columns:1fr}.pair{grid-template-columns:1fr}.lane{overflow:auto}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Root-motion Gate 1 · exact approved pixels</h1><span class="status">Draft comparison · nothing promoted</span><p>The same five approved Keeper images are used in both rows. Only the root deltas differ.</p></header><main><p class="rule"><strong>Decision:</strong> does the 3, 7, 13, 19 ku bridge look as natural as the approved 2, 6, 12, 18 ku bridge? The proposed route travels exactly one 84-ku / 10.5-lp lattice interval from stop to stop.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox" checked> Loop</label><label>Speed <input id="speed" type="range" min="60" max="300" value="100"> <span id="speedLabel">100 ms</span></label></div><p id="loading" class="readout">Loading and decoding all five unique Keeper frames…</p><div id="largeRows"></div><h2>Exact proposed game scale</h2><div id="gameRows"></div></article><section class="pair"><article><h2>Current approved</h2><div class="metric warn">76 ku · 9.5 lp</div><p>Four-frame acceleration and its exact reverse. It is approved in isolation, but it cannot close one 84-ku room-grid interval.</p></article><article><h2>Candidate</h2><div class="metric ok">84 ku · 10.5 lp</div><p>Identical poses and timing; every half changes by one ku. Start plus stop closes exactly one room-grid interval.</p></article></section><article><h2>Frame evidence</h2><table><thead><tr><th>Frame</th><th>Pose</th><th>Current Δ / cumulative</th><th>Candidate Δ / cumulative</th></tr></thead><tbody id="table"></tbody></table><p>Dashed markers show cumulative root positions. The gold line is the floor contact datum. No pixels are interpolated, redrawn or scaled differently between the rows.</p></article></main><script>
const DATA=__PAYLOAD__;let index=0,timer=null;const buttons=[...document.querySelectorAll('button')],unique=[...new Set(DATA.frames.map(f=>f.src))];
function cumulative(profile,i){return profile.deltas.slice(0,i+1).reduce((a,b)=>a+b,0)}
function makeRows(target,scale,klass){target.innerHTML=DATA.profiles.map(p=>`<div class="row"><div><strong style="color:${p.colour}">${p.label}</strong><div id="${klass}-${p.id}-read" class="readout"></div></div><div class="lane ${klass}" id="${klass}-${p.id}"><div class="baseline"></div><img alt="${p.label}"></div></div>`).join('')}
makeRows(document.getElementById('largeRows'),1,'large');makeRows(document.getElementById('gameRows'),.5,'game');
const table=document.getElementById('table');let sums=[0,0];table.innerHTML=DATA.frames.map((f,i)=>{sums=sums.map((n,p)=>n+DATA.profiles[p].deltas[i]);return `<tr><td>${i+1}</td><td>${f.pose}</td><td>${DATA.profiles[0].deltas[i]} / ${sums[0]} ku</td><td>${DATA.profiles[1].deltas[i]} / ${sums[1]} ku</td></tr>`}).join('');
function render(){DATA.profiles.forEach(p=>{for(const [klass,scale,start] of [['large',1,30],['game',.5,15]]){const lane=document.getElementById(`${klass}-${p.id}`),img=lane.querySelector('img'),x=cumulative(p,index);img.src=DATA.frames[index].src;img.style.left=`${start+x*scale}px`;lane.querySelectorAll('.mark').forEach(n=>n.remove());for(let i=0;i<=index;i++){const m=document.createElement('span');m.className='mark';m.style.left=`${start+cumulative(p,i)*scale}px`;m.style.borderColor=p.colour;lane.append(m)}document.getElementById(`${klass}-${p.id}-read`).textContent=`F${index+1}/8 · ${DATA.frames[index].pose} · Δ ${p.deltas[index]} ku · x ${x} ku`}})}
function pause(){if(timer)clearTimeout(timer);timer=null}function tick(){index=index===7?(document.getElementById('loop').checked?0:7):index+1;render();if(index<7||document.getElementById('loop').checked)timer=setTimeout(tick,Number(document.getElementById('speed').value))}function play(){pause();timer=setTimeout(tick,Number(document.getElementById('speed').value))}
document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{pause();index=(index+7)%8;render()};document.getElementById('next').onclick=()=>{pause();index=(index+1)%8;render()};document.getElementById('restart').onclick=()=>{pause();index=0;render();play()};document.getElementById('speed').oninput=e=>document.getElementById('speedLabel').textContent=`${e.target.value} ms`;
function preloadFrame(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}async function startPlayback(){try{await Promise.all(unique.map(preloadFrame));buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All frames ready · synchronized at both scales';render();play()}catch(error){document.getElementById('loading').textContent=`A frame failed to load; playback remains locked. ${error.message}`}}startPlayback();
</script></body></html>'''

CIRCULATION_HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper vertical circulation V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf6f8;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1600px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #e8b852;background:#18251d;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:6px;align-items:center;flex-wrap:wrap}button,select,input{font:inherit}button,select{color:white;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}.stages{display:grid;grid-template-columns:minmax(700px,1fr) 640px;gap:18px;align-items:start;overflow:auto}.stage{display:block;background:#0c1d26;border:1px solid #496878;border-radius:8px}.large{width:100%;min-width:700px;height:auto}.game{width:620px;height:560px}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.metric{font-size:24px;font-weight:750;color:#75e6a7}table{border-collapse:collapse;width:100%}th,td{padding:7px;border-bottom:1px solid #2c4a59;text-align:left}.pending{color:#ffe09d}@media(max-width:1200px){.stages{grid-template-columns:1fr}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a><h1>Vertical circulation V1 · measured construction motion</h1><span class="status">Mannequin study · no Keeper artwork promoted</span><p>This settles dimensions and route grammar before expensive smooth raster animation is drawn.</p></header><main><p class="rule"><strong>Proposed module:</strong> 56 lp clear room + 4 lp shared structural deck = 60 lp finished-floor pitch. The stage shows true proportions. Select each continue/exit route and step it frame by frame.</p><article><div class="controls"><label>Route <select id="route"></select></label><button id="play">Play</button><button id="pause">Pause</button><button id="prev">← Previous frame</button><button id="next">Next frame →</button><button id="restart">Restart</button><label><input id="loop" type="checkbox" checked> Loop</label><label>Construction fps <input id="fps" type="range" min="6" max="24" value="14"> <span id="fpsLabel">14</span></label></div><p id="readout" class="readout"></p><div class="stages"><div><strong>Large inspection</strong><svg id="large" class="stage large" width="930" height="840" viewBox="-5 -5 155 140" role="img" aria-label="Large construction animation"></svg></div><div><strong>Exact game scale · 4 CSS px per logical px</strong><svg id="game" class="stage game" width="620" height="560" viewBox="-5 -5 155 140" role="img" aria-label="Game-scale construction animation"></svg></div></div></article><section class="cards"><article><div class="metric">60 lp</div><strong>finished-floor pitch</strong><p>56 lp clear height plus one shared 4 lp deck. Lift stops and climb routes repeat this exact amount.</p></article><article><div class="metric">16 × 3.75 lp</div><strong>stair risers</strong><p>Exactly 60 lp rise. Every riser is an integer 30 keeper units.</p></article><article><div class="metric">16 × 5.25 lp</div><strong>stair advances</strong><p>Exactly 84 lp run: eight 10.5-lp walking intervals. The 8-lp boot has 65.6% tread support.</p></article><article><div class="metric">8 × 7.5 lp</div><strong>ladder rung intervals</strong><p>Exactly one floor. Four two-rung climb cycles per storey, with no accumulated phase error.</p></article></section><article><h2>Route grammar included</h2><table><thead><tr><th>System</th><th>Continue higher</th><th>Exit toward room door</th></tr></thead><tbody><tr><th>Alternating stairs</th><td>full flight → landing turn → next flight</td><td>both landing parities; far landing crosses exactly eight walking intervals</td></tr><tr><th>Straight ladder</th><td>climb through floor opening without resetting gait</td><td>land, side-step off, then walk to the door</td></tr><tr><th>Lift</th><td>car repeats exact 60-lp stops</td><td>walk → stop → turn away → enter; exact reverse exit → turn → walk</td></tr></tbody></table><p class="pending">These are construction paths, not final timing or finished Keeper drawings. Approval authorizes the next smooth-art keyframe batches only.</p></article><article><h2>Why the old 38-lp stair placeholder cannot survive</h2><p>A 60-lp rise inside 38 lp would require a very steep 57.7° flight and treads too short for the Keeper's 8-lp boots. The measured 105-lp core holds the 84-lp flight plus a full 10.5-lp standing/turning margin at both ends. The base 172-lp room plus stair core is 277 lp wide; the largest agreed 214-lp room tier plus core is 319 lp and should be handled by camera fit, never by rescaling the Keeper.</p></article></main><script>
const SPEC=__SPEC__;const routes=[
{id:'stairs-continue',label:'Stairs · climb and continue higher',kind:'stairs',frames:88,phase:f=>f<64?'climb first flight':f<72?'turn on landing':'continue onto next flight'},
{id:'stairs-exit-far',label:'Stairs · far landing to room door',kind:'stairsExitFar',frames:104,phase:f=>f<64?'climb to far landing':f<72?'turn toward room': 'walk across landing to room door'},
{id:'stairs-exit-near',label:'Stairs · near landing to room door',kind:'stairsExitNear',frames:76,phase:f=>f<64?'climb reverse flight':f<72?'turn toward room':'single interval to room door'},
{id:'ladder-continue',label:'Ladder · climb and continue higher',kind:'ladderContinue',frames:40,phase:f=>f<32?'climb one floor':'continue through floor opening'},
{id:'ladder-exit',label:'Ladder · climb, dismount and walk',kind:'ladderExit',frames:68,phase:f=>f<32?'climb one floor':f<40?'dismount to landing':'walk toward room door'},
{id:'lift-enter',label:'Lift · walk, stop, turn and enter',kind:'liftEnter',frames:64,phase:f=>f<32?'walk to lift':f<40?'decelerate and stop':f<48?'turn away':f<58?'enter lift':'doors close'},
{id:'lift-exit',label:'Lift · exit, turn and walk',kind:'liftExit',frames:64,phase:f=>f<8?'doors open':f<18?'exit lift':f<26?'turn sideways':f<34?'accelerate':'walk toward room door'}];
const select=document.getElementById('route');select.innerHTML=routes.map(r=>`<option value="${r.id}">${r.label}</option>`).join('');let route=routes[0],frame=0,timer=null;
const E=(name,attrs={},children='')=>`<${name} ${Object.entries(attrs).map(([k,v])=>`${k}="${v}"`).join(' ')}>${children}</${name}>`;const line=(x1,y1,x2,y2,c='#d8edf5',w=1)=>E('line',{x1,y1,x2,y2,stroke:c,'stroke-width':w,'stroke-linecap':'round'});const circle=(x,y,r,c)=>E('circle',{cx:x,cy:y,r,fill:c,stroke:'#061018','stroke-width':.5});
function architecture(kind){let s=`<rect x="0" y="0" width="140" height="125" fill="#0d202a"/>`;for(const y of [10,70,130])s+=`<rect x="0" y="${y}" width="140" height="4" fill="#6d543c"/><line x1="0" y1="${y}" x2="140" y2="${y}" stroke="#d2ab72" stroke-width=".6"/>`;s+=`<rect x="115" y="26" width="22" height="44" fill="#203846" stroke="#7e9aaa"/><text x="126" y="23" text-anchor="middle" fill="#aac2ce" font-size="4">ROOM DOOR</text>`;
if(kind.startsWith('stairs')){for(let flight=0;flight<2;flight++){const baseY=130-flight*60,dir=flight%2===0?-1:1;for(let i=0;i<16;i++){const x=dir<0?94.5-i*5.25:10.5+i*5.25,y=baseY-(i+1)*3.75;s+=line(x,y,x+dir*5.25,y,'#d4ae76',1)+line(x+dir*5.25,y,x+dir*5.25,y+3.75,'#8c6a43',.7)}}s+=line(10.5,70,94.5,70,'#e8c68f',1.2)}
if(kind.startsWith('ladder')){s+=line(12,130,12,0,'#b98c56',2)+line(30,130,30,0,'#b98c56',2);for(let y=130;y>=2;y-=7.5)s+=line(12,y,30,y,'#d4ae76',1.2)}
if(kind.startsWith('lift')){s+=`<rect x="18" y="22" width="38" height="48" rx="2" fill="#172d38" stroke="#9bb4be"/><line x1="37" y1="22" x2="37" y2="70" stroke="#6d8793"/><text x="37" y="18" text-anchor="middle" fill="#aac2ce" font-size="4">LIFT</text>`}return s}
function keeper(x,floorY,phase=0,view='side',scale=1,opacity=1){const bob=Math.sin(phase*Math.PI*2)*.45,hipY=floorY-11.5*scale+bob,headY=floorY-31*scale+bob,leg=Math.sin(phase*Math.PI*2)*4.2*scale,arm=-leg*.8;let s=`<g opacity="${opacity}">`;s+=circle(x,headY,5.2*scale,'#f0dfc1')+`<path d="M ${x-6*scale} ${headY-4*scale} Q ${x} ${headY-9*scale} ${x+6*scale} ${headY-4*scale}" fill="#1974cf" stroke="#061018" stroke-width="${.8*scale}"/>`;s+=`<ellipse cx="${x}" cy="${floorY-19*scale+bob}" rx="${(view==='back'?9.5:6.5)*scale}" ry="${10*scale}" fill="#1673c9" stroke="#061018" stroke-width="${.8*scale}"/><line x1="${x-6*scale}" y1="${floorY-20*scale}" x2="${x+6*scale}" y2="${floorY-20*scale}" stroke="#f3e5c8" stroke-width="${1.5*scale}"/>`;const hipL=x-2.2*scale,hipR=x+2.2*scale;s+=line(hipL,hipY,hipL+leg,floorY-1,'#263858',2.2*scale)+line(hipR,hipY,hipR-leg,floorY-1,'#263858',2.2*scale);s+=line(x-5*scale,floorY-24*scale,x-5*scale+arm,floorY-13*scale,'#1673c9',2*scale)+line(x+5*scale,floorY-24*scale,x+5*scale-arm,floorY-13*scale,'#1673c9',2*scale);s+=circle(hipL+leg,floorY-1,1.2*scale,'#30486f')+circle(hipR-leg,floorY-1,1.2*scale,'#30486f')+'</g>';return s}
function ladderKeeper(x,y,phase,opacity=1){const swing=Math.sin(phase*Math.PI*2)*3.5;let s=keeper(x,y,phase,'back',1,opacity);s+=line(x-5,y-24,x-8,y-31+swing,'#f0b07b',1.8)+line(x+5,y-24,x+8,y-31-swing,'#f0b07b',1.8);return s}
function state(r,f){if(r.kind==='stairs'){if(f<64)return{x:94.5-84*(f/63),y:130-60*(f/63),phase:f/8};if(f<72)return{x:10.5,y:70,phase:0,view:'back'};return{x:10.5+21*((f-72)/15),y:70-15*((f-72)/15),phase:(f-72)/8}}
if(r.kind==='stairsExitFar'){if(f<64)return{x:94.5-84*(f/63),y:130-60*(f/63),phase:f/8};if(f<72)return{x:10.5,y:70,phase:0,view:'back'};return{x:10.5+84*((f-72)/31),y:70,phase:(f-72)/8}}
if(r.kind==='stairsExitNear'){if(f<64)return{x:10.5+84*(f/63),y:130-60*(f/63),phase:f/8};if(f<72)return{x:94.5,y:70,phase:0,view:'back'};return{x:94.5+10.5*((f-72)/3),y:70,phase:(f-72)/8}}
if(r.kind==='ladderContinue'){return{x:21,y:130-75*(f/39),phase:f/8,ladder:true}}
if(r.kind==='ladderExit'){if(f<32)return{x:21,y:130-60*(f/31),phase:f/8,ladder:true};if(f<40)return{x:21+10.5*((f-32)/7),y:70,phase:(f-32)/8,view:'back'};return{x:31.5+63*((f-40)/27),y:70,phase:(f-40)/8}}
if(r.kind==='liftEnter'){if(f<32)return{x:94.5-42*(f/31),y:70,phase:f/8};if(f<40)return{x:52.5-4*(f-32)/7,y:70,phase:0};if(f<48)return{x:48.5,y:70,phase:0,view:'back'};if(f<58){const p=(f-48)/9;return{x:37,y:70-6*p,phase:0,view:'back',scale:1-.22*p,opacity:1-.2*p}}return{x:37,y:64,phase:0,view:'back',scale:.78,opacity:.8,doors:(f-58)/5}}
if(r.kind==='liftExit'){if(f<8)return{x:37,y:64,phase:0,view:'back',scale:.78,opacity:.8,doors:1-f/7};if(f<18){const p=(f-8)/9;return{x:37+11.5*p,y:64+6*p,phase:0,view:'back',scale:.78+.22*p,opacity:.8+.2*p};if(false)return{}}if(f<26)return{x:48.5,y:70,phase:0,view:'back'};if(f<34)return{x:48.5+4*(f-26)/7,y:70,phase:0};return{x:52.5+42*((f-34)/29),y:70,phase:(f-34)/8}}
return{x:94.5,y:130,phase:0}}
function renderSvg(svg){const st=state(route,frame);let s=architecture(route.kind);s+=`<line x1="${st.x}" y1="${st.y}" x2="${st.x}" y2="${st.y-45}" stroke="#75e6a7" stroke-width=".35" stroke-dasharray="1 1"/><circle cx="${st.x}" cy="${st.y}" r="1.2" fill="#75e6a7"/>`;s+=st.ladder?ladderKeeper(st.x,st.y,st.phase,st.opacity??1):keeper(st.x,st.y,st.phase,st.view||'side',st.scale||1,st.opacity??1);if(st.doors!==undefined){const w=19*st.doors;s+=`<rect x="18" y="22" width="${w}" height="48" fill="#315363"/><rect x="${56-w}" y="22" width="${w}" height="48" fill="#315363"/>`}s+=`<text x="3" y="6" fill="#c9e4ee" font-size="4">1 lp = 4 px in exact-scale pane · green = root/floor contact</text>`;svg.innerHTML=s}
function render(){renderSvg(document.getElementById('large'));renderSvg(document.getElementById('game'));const st=state(route,frame);document.getElementById('readout').textContent=`${route.label} · frame ${frame+1}/${route.frames} · ${route.phase(frame)} · root (${st.x.toFixed(2)}, ${st.y.toFixed(2)}) lp`}
function pause(){if(timer)clearTimeout(timer);timer=null}function tick(){frame=frame===route.frames-1?(document.getElementById('loop').checked?0:frame):frame+1;render();if(frame<route.frames-1||document.getElementById('loop').checked)timer=setTimeout(tick,1000/Number(document.getElementById('fps').value))}function play(){pause();timer=setTimeout(tick,1000/Number(document.getElementById('fps').value))}
select.onchange=()=>{pause();route=routes.find(r=>r.id===select.value);frame=0;render();play()};document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{pause();frame=(frame-1+route.frames)%route.frames;render()};document.getElementById('next').onclick=()=>{pause();frame=(frame+1)%route.frames;render()};document.getElementById('restart').onclick=()=>{pause();frame=0;render();play()};document.getElementById('fps').oninput=e=>document.getElementById('fpsLabel').textContent=e.target.value;render();play();
</script></body></html>'''


if __name__ == "__main__":
    main()
