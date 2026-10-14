#!/usr/bin/env python3
"""Build the shared door-to-stair/lift approach alignment review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "art/drafts/keeper-circulation-entry-alignment-2026-10-14-v1"
PUBLIC = ROOT / "public/keeper-review/keeper-circulation-entry-alignment-v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SPEC = {
    "schema": "lighthouse-keeper/circulation-entry-alignment@1",
    "status": "draft-construction-choreography-awaiting-review",
    "units": {"kuPerLp": 8, "stepLp": 10.5, "fullStrideLp": 21},
    "sharedGeometry": {
        "circulationCoreWidthLp": 105,
        "transferDoorCentreLp": 115.5,
        "floorYLp": 70,
        "landingRootMarginLp": 10.5,
    },
    "stair": {
        "baseRootLp": 94.5,
        "doorToBaseLp": 21,
        "doorToBaseKu": 168,
        "walkStepIntervals": 2,
        "fullWalkCycles": 1,
        "visibleWalkFrames": 8,
        "pauseFramesAtJoin": 0,
        "firstClimbFrameAdvances": True,
        "flightEndRootLp": 10.5,
        "flightRunLp": 84,
        "flightRiseLp": 60,
        "risers": 16,
        "treadLp": 5.25,
        "riserLp": 3.75,
        "direction": "bottom-right-to-top-left",
    },
    "lift": {
        "thresholdRootLp": 31.5,
        "doorToThresholdLp": 84,
        "doorToThresholdKu": 672,
        "walkStepIntervals": 8,
        "fullWalkCycles": 4,
        "openingLeftLp": 9.5,
        "openingWidthLp": 44,
        "buttonLp": [42, 43.5],
        "fixedRootPhases": ["stop", "right-hand button press", "turn fully away", "depth-only entry"],
        "f5StopDependency": "not-drawn-not-approved",
    },
    "boundaries": {
        "approvedPixelsChanged": False,
        "runtimeGeometryChanged": False,
        "approvalChanged": False,
        "constructionOnly": True,
    },
}


HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper circulation entry alignment V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7f9;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#132921;padding:13px 15px}.warning{border-left:4px solid #e8b852;background:#2a2518;padding:13px 15px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button,select,input{font:inherit}button,select{color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled,select:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.stages{display:grid;grid-template-columns:minmax(620px,1fr) minmax(620px,1fr);gap:18px;align-items:start;overflow:auto}.stage{display:block;background:#0c1d26;border:1px solid #496878;border-radius:8px;height:auto}.wide{width:100%;min-width:620px}.exact{width:580px;max-width:none}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px}.metric{font-size:25px;font-weight:750;color:#75e6a7}.small{font-size:13px;color:#b9ced7}table{border-collapse:collapse;width:100%}th,td{padding:8px;border-bottom:1px solid #2c4a59;text-align:left}.yes{color:#75e6a7}.pending{color:#ffe09d}@media(max-width:1250px){.stages{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-vertical-circulation-v2/">← Vertical circulation V2</a><h1>Circulation entry alignment V1 · door → stairs or lift</h1><span class="status">Shared construction geometry · nothing promoted</span><p>One registered transfer doorway, two progression alternatives, and no arbitrary approach distances.</p></header><main><p class="rule"><strong>Stair rule:</strong> the visible walk begins while the Keeper is still partly hidden by the doorway, runs for exactly one complete eight-frame walk cycle, lands at the stair base, and goes straight into climb frame 1. There is no stop pose, no idle beat and no duplicated root frame at the join.</p><section class="cards"><div class="panel"><div class="metric">x = 115.5 lp</div><strong>shared doorway root</strong><p>Fixed transfer anchor for both routes.</p></div><div class="panel"><div class="metric">21 lp</div><strong>door → stair base</strong><p>Two steps; one complete walk cycle.</p></div><div class="panel"><div class="metric">0 pause frames</div><strong>walk → stair join</strong><p>The first climb frame already advances.</p></div><div class="panel"><div class="metric">84 lp</div><strong>door → lift centre</strong><p>Eight steps; four complete strides.</p></div></section><section class="panel"><div class="controls"><label>Route <select id="route" disabled><option value="stair">Walk → immediate stair climb</option><option value="lift">Walk → stop → button → lift entry</option></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox"> Loop for inspection</label><label>Speed <input id="speed" type="range" min="40" max="180" value="76"> <span id="speedLabel">76 ms</span></label></div><p id="loading" class="readout">Checking construction media before playback…</p><p id="readout" class="readout"></p></section><section class="stages"><article class="panel"><h2>Large choreography inspection</h2><p class="small">Green marks the registered endpoint. On the stair route, the white ghost is the last walk root and orange marks climb frame 1.</p><svg id="large" class="stage wide" viewBox="0 0 145 84" role="img" aria-label="Large circulation entry choreography"></svg></article><article class="panel"><h2>Exact 4× authoring ruler</h2><p class="small">145 × 84 logical pixels at exactly four CSS pixels per logical pixel. Runtime screen scale remains responsive.</p><svg id="exact" class="stage exact" width="580" height="336" viewBox="0 0 145 84" role="img" aria-label="Exact-scale circulation entry choreography"></svg></article></section><article class="panel"><h2>Why the stair begins at x=94.5 lp</h2><p>The measured 105-lp core needs a 10.5-lp standing/root margin at each end. Therefore its bottom-right flight root is exactly <strong>105 − 10.5 = 94.5 lp</strong>. Placing the transfer doorway at x=115.5 lp puts that base exactly 21 lp—one full two-step walk cycle—away. Moving the stair itself would break its matched 84-lp flight run and landing margin; registering the doorway correctly solves the join without distorting the staircase.</p></article><p class="warning"><strong>Separate lift-art dependency:</strong> the lift route stops after eight step intervals, so finished lift pixels still need the undrawn Walk F5 → neutral stop bridge. The stair route does not stop: its one full walk cycle hands directly into climb frame 1 and therefore does not depend on that bridge.</p><article class="panel"><h2>Deterministic joins</h2><table><thead><tr><th>Route</th><th>Measured approach</th><th>Required join</th></tr></thead><tbody><tr><td>Stairs</td><td>115.5 → 94.5 lp = 21 lp</td><td class="yes">walk F8 → climb F1; zero pause; climb F1 advances</td></tr><tr><td>Lift</td><td>115.5 → 31.5 lp = 84 lp</td><td>F5 stop bridge → neutral → right-hand press → fixed-root turn/entry</td></tr></tbody></table></article><article class="panel"><h2>Decision boundary</h2><p>This construction proposal changes no approved Keeper artwork, Final lane, production sprite, runtime coordinate, stair asset, lift asset or approval record. The earlier circulation and lift-only pages remain unchanged evidence.</p></article></main><script>
const SPEC=__SPEC__;const REVIEW_MEDIA=[];const ROUTES={stair:{frames:72,label:'Walk → immediate stair climb'},lift:{frames:86,label:'Walk → stop → button → lift entry'}};let route='stair',frame=0,timer=null;const controls=[...document.querySelectorAll('button,select')];const E=(n,a={},c='')=>`<${n} ${Object.entries(a).map(([k,v])=>`${k}="${v}"`).join(' ')}>${c}</${n}>`;const line=(x1,y1,x2,y2,c='#d8edf5',w=1,d='')=>E('line',{x1,y1,x2,y2,stroke:c,'stroke-width':w,'stroke-linecap':'round','stroke-dasharray':d});const circle=(x,y,r,c,s='#061018')=>E('circle',{cx:x,cy:y,r,fill:c,stroke:s,'stroke-width':.5});const clamp=n=>Math.max(0,Math.min(1,n));const ease=n=>{n=clamp(n);return n*n*(3-2*n)};
function stairState(f){if(f<8)return{x:115.5-21*((f+1)/8),y:70,gait:f/8,kind:'walk',advance:true};const p=(f-7)/64;return{x:94.5-84*p,y:70-60*p,gait:(f-8)/8,kind:'climb',advance:true}}
function liftState(f){let x=31.5,gait=0,reach=0,turn=0,depth=0,doors=0,lit=false;if(f<32){x=115.5-73.5*ease(f/31);gait=f/8}else if(f<40){x=42-10.5*ease((f-32)/7);gait=4+(f-32)/16}else if(f<44){}else if(f<52){reach=ease((f-44)/4);if(f>48)reach=ease((51-f)/3);lit=f>=47}else if(f<60){reach=1-ease((f-52)/4);doors=ease((f-52)/7);lit=f<56}else if(f<68){doors=1;turn=ease((f-60)/7)}else if(f<78){doors=1;turn=1;depth=ease((f-68)/9)}else{turn=1;depth=1;doors=1-ease((f-78)/7)}return{x,y:70,gait,kind:'lift',reach,turn,depth,doors,lit,advance:f<40}}
function phase(){if(route==='stair')return frame<8?'one complete visible walk cycle':frame===8?'climb frame 1 · already advancing':'continuous stair climb';if(frame<32)return'walk from doorway';if(frame<40)return'decelerate to lift centre';if(frame<44)return'settled stop';if(frame<52)return'right-hand button press';if(frame<60)return'doors open; hand retracts';if(frame<68)return'turn fully away';if(frame<78)return'depth-only entry';return'doors close after occlusion'}
function architecture(st){let s=`<rect width="145" height="84" fill="#0d202a"/><rect x="0" y="70" width="145" height="4" fill="#6d543c"/><line x1="0" y1="70" x2="145" y2="70" stroke="#d2ab72" stroke-width=".6"/>`;s+=`<rect x="104.5" y="26" width="22" height="44" fill="#203846" stroke="#7e9aaa"/><text x="115.5" y="23" text-anchor="middle" fill="#aac2ce" font-size="3.7">TRANSFER DOOR</text>`;if(route==='stair'){for(let i=0;i<16;i++){const x=94.5-i*5.25,y=70-(i+1)*3.75;s+=line(x,y,x-5.25,y,'#d4ae76',1)+line(x-5.25,y,x-5.25,y+3.75,'#8c6a43',.7)}s+=line(94.5,12,94.5,74,'#75e6a7',.35,'1 1')+circle(94.5,70,1.1,'#75e6a7','#75e6a7');s+=line(94.5,77.5,115.5,77.5,'#75e6a7',.5)+`<text x="105" y="82" text-anchor="middle" fill="#75e6a7" font-size="3">21 lp · 2 steps · 1 walk cycle</text>`;if(frame>=7&&frame<=9){s+=circle(94.5,70,1.8,'none','#ffffff')+circle(94.5-84/64,70-60/64,1.5,'#e8b852','#e8b852')+line(94.5,70,94.5-84/64,70-60/64,'#e8b852',.7)}}else{s+=`<rect x="9.5" y="22" width="44" height="48" rx="2" fill="#162f3b" stroke="#9bb4be"/><rect x="12.5" y="25" width="38" height="45" fill="#0b1920"/><text x="31.5" y="18" text-anchor="middle" fill="#aac2ce" font-size="4">LIFT · 44 lp</text><rect x="39.5" y="39" width="5" height="9" rx=".8" fill="#243f4d" stroke="#9bb4be" stroke-width=".5"/><circle cx="42" cy="43.5" r="1.25" fill="${st.lit?'#ffd45c':'#6f8790'}" stroke="#07131b" stroke-width=".4"/>`;s+=line(31.5,10,31.5,74,'#75e6a7',.35,'1 1')+circle(31.5,70,1.1,'#75e6a7','#75e6a7');s+=line(31.5,77.5,115.5,77.5,'#75e6a7',.5)+`<text x="73.5" y="82" text-anchor="middle" fill="#75e6a7" font-size="3">84 lp · 8 steps · 4 full strides</text>`;const leaf=22*(1-st.doors);if(leaf>0){s+=`<rect x="9.5" y="22" width="${leaf}" height="48" fill="#315363"/><rect x="${53.5-leaf}" y="22" width="${leaf}" height="48" fill="#315363"/>`}}return s}
function keeper(st){const scale=1-.22*(st.depth||0),baseY=st.y-6*(st.depth||0),bob=Math.sin(st.gait*Math.PI*2)*.32,x=st.x,headY=baseY-31*scale+bob,wide=(6.5+3*(st.turn||0))*scale,leg=Math.sin(st.gait*Math.PI*2)*4.2*scale,arm=-leg*.7*(1-(st.reach||0)),hipY=baseY-11.5*scale+bob,opacity=1-.2*(st.depth||0);let s=`<g opacity="${opacity}">`;s+=circle(x,headY,5.2*scale,'#f0dfc1')+`<path d="M ${x-6*scale} ${headY-4*scale} Q ${x} ${headY-9*scale} ${x+6*scale} ${headY-4*scale}" fill="#1974cf" stroke="#061018" stroke-width="${.8*scale}"/>`;s+=`<ellipse cx="${x}" cy="${baseY-19*scale+bob}" rx="${wide}" ry="${10*scale}" fill="#1673c9" stroke="#061018" stroke-width="${.8*scale}"/><line x1="${x-6*scale}" y1="${baseY-20*scale}" x2="${x+6*scale}" y2="${baseY-20*scale}" stroke="#f3e5c8" stroke-width="${1.5*scale}"/>`;s+=line(x-2.2*scale,hipY,x-2.2*scale+leg,baseY-1,'#263858',2.2*scale)+line(x+2.2*scale,hipY,x+2.2*scale-leg,baseY-1,'#263858',2.2*scale);s+=circle(x-2.2*scale+leg,baseY-1,1.2*scale,'#30486f')+circle(x+2.2*scale-leg,baseY-1,1.2*scale,'#30486f');const sy=baseY-24*scale;if((st.reach||0)>0){const r=st.reach,ex=x+(5+3.8*r)*scale,ey=sy+(7-4.5*r)*scale,hx=x+(5+6*r)*scale,hy=baseY-(13+13.5*r)*scale;s+=line(x+5*scale,sy,ex,ey,'#1673c9',2*scale)+line(ex,ey,hx,hy,'#f0b07b',1.8*scale)+circle(hx,hy,1.15*scale,'#f0b07b')}else{s+=line(x+5*scale,sy,x+5*scale-arm,baseY-13*scale,'#1673c9',2*scale)}s+=line(x-5*scale,sy,x-5*scale+arm,baseY-13*scale,'#1673c9',2*scale)+'</g>';return s}
function renderSvg(svg){const st=route==='stair'?stairState(frame):liftState(frame);let s=architecture(st)+keeper(st);if(route==='lift'&&frame>=78){const leaf=22*(1-st.doors);s+=`<rect x="9.5" y="22" width="${leaf}" height="48" fill="#315363"/><rect x="${53.5-leaf}" y="22" width="${leaf}" height="48" fill="#315363"/>`}s+=`<text x="3" y="6" fill="#c9e4ee" font-size="3.2">${route==='stair'?'walk F8 joins climb F1 with no held root':'stop / press / turn / entry share one horizontal root'}</text>`;svg.innerHTML=s}
function render(){const st=route==='stair'?stairState(frame):liftState(frame);renderSvg(document.getElementById('large'));renderSvg(document.getElementById('exact'));document.getElementById('readout').textContent=`${ROUTES[route].label} · frame ${frame+1}/${ROUTES[route].frames} · ${phase()} · root (${st.x.toFixed(2)}, ${st.y.toFixed(2)}) lp`}
function pause(){if(timer)clearTimeout(timer);timer=null}function tick(){const end=ROUTES[route].frames-1;if(frame===end){if(!document.getElementById('loop').checked){pause();return}frame=0}else frame++;render();timer=setTimeout(tick,Number(document.getElementById('speed').value))}function play(){pause();timer=setTimeout(tick,Number(document.getElementById('speed').value))}document.getElementById('route').onchange=e=>{pause();route=e.target.value;frame=0;render();play()};document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{pause();frame=(frame-1+ROUTES[route].frames)%ROUTES[route].frames;render()};document.getElementById('next').onclick=()=>{pause();frame=(frame+1)%ROUTES[route].frames;render()};document.getElementById('restart').onclick=()=>{pause();frame=0;render();play()};document.getElementById('speed').oninput=e=>document.getElementById('speedLabel').textContent=`${e.target.value} ms`;
function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}async function startPlayback(){try{await Promise.all(REVIEW_MEDIA.map(preload));controls.forEach(c=>c.disabled=false);document.getElementById('loading').textContent='Construction vectors ready · no external frame media required';render();play()}catch(error){document.getElementById('loading').textContent=`Playback locked: ${error.message}`}}startPlayback();
</script></body></html>'''


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=False)
    PUBLIC.mkdir(parents=True, exist_ok=False)
    spec_path = PACK / "circulation-entry-alignment-v1.json"
    spec_path.write_text(json.dumps(SPEC, indent=2) + "\n")
    page = PUBLIC / "index.html"
    page.write_text(HTML.replace("__SPEC__", json.dumps(SPEC, separators=(",", ":"))))
    authority_files = {
        "verticalCirculationGeometry": "art/drafts/keeper-movement-foundation-2026-10-14-v1/geometry/keeper-vertical-circulation-v1.json",
        "primeConstructionRig": "art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json",
    }
    preserved_files = {
        "verticalCirculationV1": "public/keeper-review/keeper-vertical-circulation-v1/index.html",
        "verticalCirculationV2": "public/keeper-review/keeper-vertical-circulation-v2/index.html",
        "liftEntryV1": "public/keeper-review/keeper-lift-entry-alignment-v1/index.html",
    }
    register = {
        "schema": "lighthouse-keeper/review-batch@1",
        "batchId": "keeper-circulation-entry-alignment-2026-10-14-v1",
        "status": SPEC["status"],
        "authorities": {key: {"file": rel, "sha256": digest(ROOT / rel)} for key, rel in authority_files.items()},
        "preservedEvidence": {key: {"file": rel, "sha256": digest(ROOT / rel)} for key, rel in preserved_files.items()},
        "spec": {"file": str(spec_path.relative_to(ROOT)), "sha256": digest(spec_path)},
        "reviewPage": {"file": str(page.relative_to(ROOT)), "sha256": digest(page)},
        "validation": {
            "sharedDoorAnchor": True,
            "stairWholeWalkCycle": True,
            "stairJoinHasZeroPauseFrames": True,
            "firstClimbFrameAdvances": True,
            "liftWholeStrideClosure": True,
            "approvedPixelsChanged": False,
            "runtimeChanged": False,
            "approvalChanged": False,
        },
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "HANDOFF.md").write_text("""# Keeper circulation entry alignment V1\n\nStatus: draft construction choreography awaiting Frank's review.\n\nThe shared transfer-door root is x=115.5 lp. The stair base remains at its measured x=94.5 lp, exactly one 21-lp full walk cycle away. Walk F8 hands directly into an already-advancing climb F1 with zero pause frames. The alternative lift threshold is x=31.5 lp, exactly 84 lp/four full strides from the same doorway; its final art still requires the separate F5 stop bridge.\n\nNothing is approved or wired. Review: `/keeper-review/keeper-circulation-entry-alignment-v1/`.\n""")
    print(page.relative_to(ROOT))


if __name__ == "__main__":
    main()
