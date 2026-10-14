#!/usr/bin/env python3
"""Build clearer V2 review pages without changing the V1 evidence or geometry."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
V1_PACK = ROOT / "art/drafts/keeper-movement-foundation-2026-10-14-v1"
PACK = ROOT / "art/drafts/keeper-movement-foundation-2026-10-14-v2"
GATE = ROOT / "public/keeper-review/keeper-root-motion-gate-v2"
CIRCULATION = ROOT / "public/keeper-review/keeper-vertical-circulation-v2"
V1_CIRCULATION = ROOT / "public/keeper-review/keeper-vertical-circulation-v1/index.html"

FRAME_URLS = {
    "neutral": "/keeper-review/keeper-root-motion-gate-v1/assets/neutral-a172a8a01a387a21.png",
    "bridge15": "/keeper-review/keeper-root-motion-gate-v1/assets/bridge15-e54546ba14b4e5f7.png",
    "bridge50": "/keeper-review/keeper-root-motion-gate-v1/assets/bridge50-0169b3642905389d.png",
    "bridge75": "/keeper-review/keeper-root-motion-gate-v1/assets/bridge75-9f4192beb8fecbc8.png",
    "walkF1": "/keeper-review/keeper-root-motion-gate-v1/assets/walkF1-0e80ea65610452c9.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    v1_register = V1_PACK / "batch-register.json"
    v1_geometry = V1_PACK / "geometry/keeper-vertical-circulation-v1.json"
    for path in (v1_register, v1_geometry, V1_CIRCULATION):
        if not path.exists():
            raise RuntimeError(f"missing V1 authority: {path.relative_to(ROOT)}")

    PACK.mkdir(parents=True, exist_ok=True)
    GATE.mkdir(parents=True, exist_ok=True)
    CIRCULATION.mkdir(parents=True, exist_ok=True)

    payload = {
        "frames": [
            {"pose": "15% bridge", "src": FRAME_URLS["bridge15"]},
            {"pose": "50% bridge", "src": FRAME_URLS["bridge50"]},
            {"pose": "75% bridge", "src": FRAME_URLS["bridge75"]},
            {"pose": "Walk F1 contact", "src": FRAME_URLS["walkF1"]},
            {"pose": "75% bridge", "src": FRAME_URLS["bridge75"]},
            {"pose": "50% bridge", "src": FRAME_URLS["bridge50"]},
            {"pose": "15% bridge", "src": FRAME_URLS["bridge15"]},
            {"pose": "exact stop", "src": FRAME_URLS["neutral"]},
        ],
        "profiles": [
            {"id": "current", "label": "Current", "distance": 76, "deltas": [2, 6, 12, 18, 18, 12, 6, 2], "colour": "#70b7ff"},
            {"id": "candidate", "label": "Grid-perfect candidate", "distance": 84, "deltas": [3, 7, 13, 19, 19, 13, 7, 3], "colour": "#75e6a7"},
        ],
    }
    gate_html = GATE_HTML.replace("__PAYLOAD__", json.dumps(payload, separators=(",", ":")))
    write(GATE / "index.html", gate_html)

    circulation = V1_CIRCULATION.read_text()
    circulation = circulation.replace("Keeper vertical circulation V1", "Keeper vertical circulation V2")
    circulation = circulation.replace("Vertical circulation V1 · measured construction motion", "Vertical circulation V2 · measured construction motion")
    circulation = circulation.replace(
        '<a href="/animation-workbench">← Animation Workbench</a>',
        '<a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-vertical-circulation-v1/">Historical V1</a>',
    )
    circulation = circulation.replace(
        "The stage shows true proportions. Select each continue/exit route and step it frame by frame.",
        "The geometry is proportionally exact. Select each continue/exit route and step it frame by frame.",
    )
    circulation = circulation.replace(
        "Exact game scale · 4 CSS px per logical px",
        "4× authoring scale · not a fixed final screen size",
    )
    # V1's global border-box rule made a nominal 620 × 560 SVG content area
    # two CSS pixels too small in both axes. 622 × 562 leaves an exact
    # 620 × 560 interior for the 155 × 140 viewBox: precisely 4×.
    circulation = circulation.replace(".game{width:620px;height:560px}", ".game{width:622px;height:562px}")
    circulation = circulation.replace("@media(max-width:1200px)", "@media(max-width:1450px)")
    circulation = circulation.replace(
        'aria-label="Game-scale construction animation"',
        'aria-label="Four-times authoring-scale construction animation"',
    )
    circulation = circulation.replace(
        "1 lp = 4 px in exact-scale pane · green = root/floor contact",
        "green = root/floor contact · dashed box = 32 × 40 lp sprite cell",
    )
    circulation = circulation.replace(
        "s+=st.ladder?ladderKeeper(st.x,st.y,st.phase,st.opacity??1):keeper(st.x,st.y,st.phase,st.view||'side',st.scale||1,st.opacity??1);",
        "s+=`<rect x=\"${st.x-16}\" y=\"${st.y-40}\" width=\"32\" height=\"40\" fill=\"none\" stroke=\"#8ed7ff\" stroke-width=\".35\" stroke-dasharray=\"1.5 1\" opacity=\".8\"/>`;s+=st.ladder?ladderKeeper(st.x,st.y,st.phase,st.opacity??1):keeper(st.x,st.y,st.phase,st.view||'side',st.scale||1,st.opacity??1);",
    )
    scale_note = '''<article class="scale-note"><h2>What “4×” means here</h2><p><strong>This is not a promise that the Keeper will appear this many centimetres tall on every device.</strong> The game uses a responsive 1200 × 760 scene (the 300 × 190 logical design stage multiplied by four), then fits that scene to the available phone, tablet or computer viewport. His final on-screen size therefore changes with the device and camera.</p><p>The right pane is only a fixed authoring ruler: 1 logical pixel = 4 CSS pixels at 100% browser zoom. The dashed 32 × 40 lp box is therefore exactly 128 × 160 CSS pixels; the standing body occupies about 38 lp / 152 CSS pixels inside it. Use it to judge proportions against stairs, rungs and doors—not as a literal device preview.</p><div class="ruler"><span></span><b>10 logical px = 40 CSS px at 100% browser zoom</b></div></article>'''
    circulation = circulation.replace("<section class=\"cards\">", scale_note + "<section class=\"cards\">")
    circulation = circulation.replace(
        ".pending{color:#ffe09d}",
        ".pending{color:#ffe09d}.scale-note{border-color:#8ed7ff}.ruler{width:40px;border-left:1px solid #8ed7ff;border-right:1px solid #8ed7ff;border-top:2px solid #8ed7ff;margin-top:18px;padding-top:6px;white-space:nowrap}.ruler b{font-size:12px;color:#c9e4ee}",
    )
    write(CIRCULATION / "index.html", circulation)

    record = {
        "batchId": "keeper-movement-foundation-2026-10-14-v2",
        "status": "presentation-correction-awaiting-review",
        "purpose": "Make the unchanged V1 root-motion and circulation decisions understandable; correct the misleading exact-game-scale label.",
        "v1Authority": {"file": str(v1_register.relative_to(ROOT)), "sha256": digest(v1_register)},
        "geometryAuthority": {"file": str(v1_geometry.relative_to(ROOT)), "sha256": digest(v1_geometry)},
        "pages": {
            "rootMotion": {"file": str((GATE / "index.html").relative_to(ROOT)), "sha256": digest(GATE / "index.html")},
            "verticalCirculation": {"file": str((CIRCULATION / "index.html").relative_to(ROOT)), "sha256": digest(CIRCULATION / "index.html")},
        },
        "unchanged": {
            "rootProfiles": True,
            "frameUrls": True,
            "framePixels": True,
            "timing": True,
            "verticalGeometry": True,
            "routes": True,
            "production": True,
            "approvals": True,
        },
        "scaleLanguage": {
            "removed": "exact game scale",
            "replacement": "4× authoring scale",
            "runtimeReason": "The 1200 × 760 SVG scene responsively fits the available viewport, so CSS pixels per logical pixel are not fixed in play.",
        },
        "rollback": "Delete only the V2 pack and the two V2 public page directories; V1 and all approved/runtime assets remain unchanged.",
    }
    write(PACK / "batch-register.json", json.dumps(record, indent=2) + "\n")
    write(PACK / "HANDOFF.md", """# Keeper movement foundation V2 presentation correction\n\nV2 changes presentation only. Root profiles, approved frame URLs, pixels, timing, vertical geometry and route paths are unchanged from V1. The root page now explains that the user is judging one extra logical pixel of stop-to-stop translation, not new artwork. The circulation page calls its fixed pane a 4× authoring scale and explicitly distinguishes that ruler from the responsive final game display.\n\nNo approval or production state changed.\n""")
    print(json.dumps({"rootMotion": str((GATE / 'index.html').relative_to(ROOT)), "circulation": str((CIRCULATION / 'index.html').relative_to(ROOT))}, indent=2))


GATE_HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper root-motion Gate 1 V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:16px/1.5 system-ui,sans-serif}header,main{max-width:1320px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.hero{background:#18251d;border-left:5px solid #75e6a7;padding:16px 18px;margin:18px 0}.facts,.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.pair{grid-template-columns:1fr 1fr}.fact,article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:14px 0}.fact b,.metric{display:block;font-size:1.35rem}.same{color:#75e6a7}.difference{color:#ffe09d}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:white;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.lane{position:relative;height:325px;overflow:hidden;border:1px solid #496878;border-radius:8px;background:repeating-conic-gradient(#1b3440 0 25%,#122833 0 50%) 50%/24px 24px;margin-top:8px}.lane img{position:absolute;width:256px;height:320px;bottom:4px}.floor{position:absolute;left:0;right:0;bottom:4px;border-top:1px solid #e8b852}.start,.finish{position:absolute;top:0;bottom:0;border-left:2px solid}.start{left:160px;border-color:#fff8}.finish.current{left:236px;border-color:#70b7ff}.finish.candidate{left:244px;border-color:#75e6a7}.labels{position:relative;height:42px;margin-left:160px}.labels span{position:absolute;top:3px;font-size:12px;white-space:nowrap}.labels .startlabel{left:0}.labels .currentlabel{left:76px;color:#70b7ff}.labels .candidatelabel{left:84px;top:21px;color:#75e6a7}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.small{font-size:.9rem;color:#c9e4ee}table{border-collapse:collapse;width:100%}th,td{padding:7px;border-bottom:1px solid #2c4a59;text-align:left;font-variant-numeric:tabular-nums}@media(max-width:760px){.facts,.pair{grid-template-columns:1fr}.lane{overflow:auto}}
</style></head><body><header><a href="/animation-workbench">← Animation Workbench</a> · <a href="/keeper-review/keeper-root-motion-gate-v1/">Historical V1</a><h1>Root-motion Gate 1 V2 · the plain-English comparison</h1><span class="status">Draft technical decision · nothing promoted</span></header><main><div class="hero"><strong>What are you looking at?</strong><p>This is <em>not</em> a redraw and you are not choosing between two Keeper designs. Both rows play the same approved pictures at the same speed. The only question is whether moving him <strong>one logical pixel farther</strong> over the whole start-and-stop feels equally natural.</p><p>If you can barely see a difference, that is expected—and useful. The green version reaches the furniture grid exactly; the blue version stops one logical pixel short.</p></div><section class="facts"><div class="fact"><b class="same">Same</b>Keeper pictures</div><div class="fact"><b class="same">Same</b>frame order and timing</div><div class="fact"><b class="difference">Only change</b>9.5 lp versus 10.5 lp total travel</div></section><article><h2>Watch the feet as he starts and stops</h2><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox" checked> Loop</label><label>Speed <input id="speed" type="range" min="60" max="300" value="100"> <span id="speedLabel">100 ms</span></label></div><p id="loading" class="readout">Loading and decoding the five unique approved frames…</p><div id="rows"></div><div class="labels"><span class="startlabel">start</span><span class="currentlabel">blue ends: 9.5 lp</span><span class="candidatelabel">green ends: 10.5 lp</span></div><p class="small">The vertical lines mark the registered floor anchor (16 lp from the cell's left edge), not the cell edge. The finish lines are eight high-resolution keeper units apart: exactly 1 logical pixel. The movement is enlarged here so that small differences can be inspected.</p></article><section class="pair"><article><h2>Blue · current bridge</h2><div class="metric" style="color:#70b7ff">76 ku = 9.5 lp</div><p>Already visually approved in isolation, but it cannot land on the proposed 10.5-lp furniture lattice.</p></article><article><h2>Green · candidate bridge</h2><div class="metric" style="color:#75e6a7">84 ku = 10.5 lp</div><p>Each half-step gains only one high-resolution unit. The complete bridge lands exactly one lattice interval away.</p></article></section><article><h2>Frame-by-frame numbers</h2><table><thead><tr><th>Frame</th><th>Picture</th><th>Blue Δ / total</th><th>Green Δ / total</th></tr></thead><tbody id="table"></tbody></table></article></main><script>
const DATA=__PAYLOAD__;let index=0,timer=null;const buttons=[...document.querySelectorAll('button')],unique=[...new Set(DATA.frames.map(f=>f.src))];
function cumulative(p,i){return p.deltas.slice(0,i+1).reduce((a,b)=>a+b,0)}
document.getElementById('rows').innerHTML=DATA.profiles.map(p=>`<div><strong style="color:${p.colour}">${p.label} · ${p.distance} ku</strong><span id="${p.id}-read" class="readout"></span><div class="lane" id="${p.id}"><div class="floor"></div><div class="start"></div><div class="finish current"></div><div class="finish candidate"></div><img alt="${p.label} root-motion comparison"></div></div>`).join('');
let sums=[0,0];document.getElementById('table').innerHTML=DATA.frames.map((f,i)=>{sums=sums.map((n,p)=>n+DATA.profiles[p].deltas[i]);return `<tr><td>${i+1}</td><td>${f.pose}</td><td>${DATA.profiles[0].deltas[i]} / ${sums[0]} ku</td><td>${DATA.profiles[1].deltas[i]} / ${sums[1]} ku</td></tr>`}).join('');
function render(){DATA.profiles.forEach(p=>{const x=cumulative(p,index),lane=document.getElementById(p.id),img=lane.querySelector('img');img.src=DATA.frames[index].src;img.style.left=`${32+x}px`;document.getElementById(`${p.id}-read`).textContent=` · F${index+1}/8 · x ${x} ku`;})}
function pause(){if(timer)clearTimeout(timer);timer=null}function tick(){index=index===7?(document.getElementById('loop').checked?0:7):index+1;render();if(index<7||document.getElementById('loop').checked)timer=setTimeout(tick,Number(document.getElementById('speed').value))}function play(){pause();timer=setTimeout(tick,Number(document.getElementById('speed').value))}
document.getElementById('play').onclick=play;document.getElementById('pause').onclick=pause;document.getElementById('prev').onclick=()=>{pause();index=(index+7)%8;render()};document.getElementById('next').onclick=()=>{pause();index=(index+1)%8;render()};document.getElementById('restart').onclick=()=>{pause();index=0;render();play()};document.getElementById('speed').oninput=e=>document.getElementById('speedLabel').textContent=`${e.target.value} ms`;
function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const decoded=image.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};image.onerror=()=>reject(new Error(src));image.src=src})}async function start(){try{await Promise.all(unique.map(preload));buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All approved frames ready · rows synchronized';render();play()}catch(error){document.getElementById('loading').textContent=`A frame failed to load; playback is locked. ${error.message}`}}start();
</script></body></html>'''


if __name__ == "__main__":
    main()
