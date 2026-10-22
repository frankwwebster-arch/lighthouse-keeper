#!/usr/bin/env python3
"""Build/verify Kitchen Complete Review V46 with V47 kettle motion controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shutil
import struct
import wave
from pathlib import Path

from PIL import Image

import build_kitchen_ligne_claire_complete_review_v43 as base


ROOT = Path(__file__).resolve().parents[1]
VERSION = 46
SET = "kitchen-ligne-claire-complete-review-v46"
PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v46"
PUBLIC = ROOT / "public/keeper-review" / SET
SOURCE_SET = "kitchen-ligne-claire-complete-review-v45"
SOURCE_PACK = ROOT / "art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v45"
SOURCE_PUBLIC = ROOT / "public/keeper-review" / SOURCE_SET
V47_PACK = ROOT / "art/drafts/kitchen-kettle-bubble-authority-2026-10-22-v47"
V47_MANIFEST = V47_PACK / "manifest.json"
V47_APPROVAL = ROOT / "docs/review/kitchen-kettle-bubble-authority-v47-approval-2026-10-22.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_groups(image: Image.Image) -> list[set[tuple[int, int]]]:
    pixels = image.getchannel("A").load()
    seen: set[tuple[int, int]] = set()
    groups: list[set[tuple[int, int]]] = []
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y] == 0 or (x, y) in seen:
                continue
            group = {(x, y)}
            stack = [(x, y)]
            seen.add((x, y))
            while stack:
                px, py = stack.pop()
                for point in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                    nx, ny = point
                    if 0 <= nx < image.width and 0 <= ny < image.height and point not in seen and pixels[nx, ny] > 0:
                        seen.add(point)
                        group.add(point)
                        stack.append(point)
            groups.append(group)
    return sorted(groups, key=len, reverse=True)


def split_broken_layers(source: Path, body_path: Path, lid_path: Path) -> dict:
    image = Image.open(source).convert("RGBA")
    groups = alpha_groups(image)
    if len(groups) != 2:
        raise RuntimeError(f"V47 Broken must contain exactly body and detached lid; found {len(groups)} groups")
    body = Image.new("RGBA", image.size)
    lid = Image.new("RGBA", image.size)
    source_pixels = image.load()
    for target, group in ((body, groups[0]), (lid, groups[1])):
        target_pixels = target.load()
        for x, y in group:
            target_pixels[x, y] = source_pixels[x, y]
    body.save(body_path, optimize=True)
    lid.save(lid_path, optimize=True)
    recomposed = Image.alpha_composite(body, lid)
    if list(recomposed.getdata()) != list(image.getdata()):
        raise RuntimeError("derived V47 body/lid layers do not recompose to the untouched candidate")
    return {
        "source": source.relative_to(ROOT).as_posix(),
        "sourceSha256": sha(source),
        "body": body_path.relative_to(ROOT).as_posix(),
        "bodySha256": sha(body_path),
        "lid": lid_path.relative_to(ROOT).as_posix(),
        "lidSha256": sha(lid_path),
        "recomposesPixelExactly": True,
        "sourcePixels": list(image.size),
        "bodyBounds": list(body.getchannel("A").getbbox() or (0, 0, 0, 0)),
        "lidBounds": list(lid.getchannel("A").getbbox() or (0, 0, 0, 0)),
    }


def write_placeholder_rattle(path: Path) -> None:
    """Write a deliberately replaceable, short mono metal-rattle placeholder."""
    sample_rate = 22050
    duration = 0.24
    rng = random.Random(4701)
    frames = []
    for index in range(round(sample_rate * duration)):
        t = index / sample_rate
        envelope = math.exp(-19 * t)
        strike = (
            math.sin(2 * math.pi * 610 * t)
            + 0.62 * math.sin(2 * math.pi * 1810 * t + 0.4)
            + 0.38 * math.sin(2 * math.pi * 2730 * t + 1.1)
            + 0.18 * rng.uniform(-1, 1)
        )
        value = max(-1.0, min(1.0, strike * envelope * 0.34))
        frames.append(struct.pack("<h", round(value * 32767)))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(b"".join(frames))


def collect_v47() -> tuple[list[dict], list[dict], list[dict]]:
    objects: list[dict] = []
    effects: list[dict] = []
    contracts: list[dict] = []
    manifest = json.loads(V47_MANIFEST.read_text())
    contracts.append({
        "role": "sole approved kettle visual authority; replaces every earlier kettle candidate in this review",
        "file": V47_MANIFEST.relative_to(ROOT).as_posix(),
        "sha256": sha(V47_MANIFEST),
        "approval": V47_APPROVAL.relative_to(ROOT).as_posix(),
        "approvalSha256": sha(V47_APPROVAL),
        "authority": manifest["set"],
    })
    for state in ("off", "on", "broken"):
        source = manifest["states"][state]["file"]
        record = base.record("kettle", f"kettle-{state}.png", source, source, manifest["set"])
        record["selection"] = "approved-visual-authority-v47-unpromoted"
        record["approval"] = V47_APPROVAL.relative_to(ROOT).as_posix()
        record["approvalSha256"] = sha(V47_APPROVAL)
        record["comparisonMode"] = "authority-is-candidate; no superseded kettle candidate offered"
        objects.append(record)

    for state in ("on", "broken"):
        cell = [128, 176] if state == "on" else [144, 192]
        for model in ("compact", "regular", "emphatic"):
            filename = f"fx-kettle-{state}-steam--{model}-f40.png"
            source = V47_PACK / "effects" / filename
            effects.append({
                "family": "kettle",
                "filename": filename,
                "sourceFile": source.relative_to(ROOT).as_posix(),
                "sourceSha256": sha(source),
                "candidateFile": source.relative_to(ROOT).as_posix(),
                "candidateSha256": sha(source),
                "pixels": list(Image.open(source).size),
                "cellPixels": cell,
                "frames": 40,
                "fps": 4,
                "byteExact": True,
                "authority": manifest["set"],
                "anchorAssetId": "kettle",
                "transformSpace": "asset-local",
                "visualAnchorRemainsStaticDuringBodyMotion": True,
            })
    return objects, effects, contracts


def require_replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"expected workbench source fragment missing: {old[:100]}")
    return text.replace(old, new, 1)


def upgrade_page() -> None:
    path = PUBLIC / "index.html"
    page = path.read_text()
    page = require_replace(page, "<title>Kitchen Ligne-Claire Complete Review V46</title>", "<title>Kitchen V47 broken-appliance motion workbench</title>")
    page = require_replace(page, "</style>", """
.motion-controls{background:#122f38;border:1px solid #4f93a0;border-radius:10px;padding:12px;margin-top:12px}.motion-controls label{display:flex;gap:7px;align-items:center}.motion-controls select{min-width:130px}.sfx-drop{display:grid;gap:3px;min-width:250px;border:1px dashed #76c6d1;border-radius:8px;padding:8px 11px;cursor:pointer;background:#0a2028}.sfx-drop.dragging{border-style:solid;background:#16414b}.sfx-drop small{color:var(--muted)}.sfx-drop input{display:none}.kettle-card img{display:block;width:100%;height:230px;object-fit:contain}.contract-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.contract-grid div{border:1px solid var(--line);border-radius:8px;padding:10px;background:#091920}.status-good{color:#79efab}@media(max-width:900px){.contract-grid{grid-template-columns:1fr}}
</style>""")
    page = require_replace(page, '<div class="tags"><span class="tag">V46 immutable complete kitchen review</span><span class="tag">approved V3 fitted family</span><span class="tag">Broken = position locked</span><span class="tag">asset-owned effects</span><span class="tag">reusable 10-second suds</span></div>', '<div class="tags"><span class="tag">V46 immutable kitchen review</span><span class="tag">Kettle Bubble Authority V47 only</span><span class="tag">Broken = position locked</span><span class="tag">separate transform layers</span><span class="tag">independent SFX</span></div>')
    page = require_replace(page, '<h1>Ligne-Claire fitted family · exact V41 movement and healing</h1><p class="lede">V45 preserves the approved V41 movement, locking, snap and healing implementation while substituting the approved fitted-family and oven artwork plus the reversible dishwasher candidate. Broken still locks position; repair still unlocks it; suds remain separate asset-local layers. Nothing on this page is registered or current.</p>', '<h1>Kitchen V47 · broken-appliance vibration workbench</h1><p class="lede">V46 makes Kitchen Kettle Bubble Authority V47 the sole active kettle candidate in the closed kitchen review. Approved/static art and V41 movement, snapping, healing, Broken locking and repair behaviour remain unchanged. Motion is presentation-only: an irregular whole-object tremor, optional component motion, and independent intermittent metal-rattle SFX stop immediately on repair.</p>')
    page = require_replace(page, '<section class="panel"><h2>Candidate dishwasher family · smooth inspection</h2>', '<section class="panel"><h2>Preserved dishwasher family · reusable behaviour comparison</h2>')
    page = require_replace(page, '<section class="panel"><h2>Live native 772 × 224 modular room</h2>', '''<section class="panel"><h2>Sole kettle authority · Bubble V47</h2><p class="rule">No V1 or V42–V46 kettle candidate is selectable here. Off, On and Broken are the approved, hash-pinned V47 visual authority. The derived Broken body and lid layers recompose pixel-for-pixel to that untouched static art; only this V46 motion/SFX presentation remains unapproved.</p><div class="states"><article class="card kettle-card"><h3>Off · exact Bubble body</h3><div class="checker"><img src="/keeper-review/kitchen-ligne-claire-complete-review-v46/assets/kettle--kettle-off.png" alt="V47 kettle off"></div></article><article class="card kettle-card"><h3>On · separate anchored steam</h3><div class="checker"><img src="/keeper-review/kitchen-ligne-claire-complete-review-v46/assets/kettle--kettle-on.png" alt="V47 kettle on"></div></article><article class="card kettle-card"><h3>Broken · detached lid</h3><div class="checker"><img src="/keeper-review/kitchen-ligne-claire-complete-review-v46/assets/kettle--kettle-broken.png" alt="V47 broken kettle with detached lid"></div></article></div></section>

<section class="panel"><h2>Live native 772 × 224 modular room</h2>''')
    page = require_replace(page, '<div class="controls" style="margin-top:10px"><strong>Dishwasher:</strong><button data-state="off" disabled>Off / movable</button><button data-state="on" disabled>On / movable</button><button data-state="broken" disabled aria-pressed="true">Broken / locked</button><button id="reset" disabled>Reset</button><button id="rotate" disabled>Rotate all</button><button id="heal" disabled aria-pressed="true">Healing enabled</button><button id="grid" disabled aria-pressed="true">Grid visible</button><button id="zoom" disabled>Toggle 2×</button></div>', '''<div class="controls" style="margin-top:10px"><strong>Dishwasher:</strong><button data-state="off" disabled>Off / movable</button><button data-state="on" disabled>On / movable</button><button data-state="broken" disabled aria-pressed="true">Broken / locked</button></div><div class="controls" style="margin-top:10px"><strong>Kettle V47:</strong><button data-kettle-state="off" disabled>Off</button><button data-kettle-state="on" disabled>On</button><button data-kettle-state="broken" disabled aria-pressed="true">Broken / locks support</button><button id="reset" disabled>Reset</button><button id="rotate" disabled>Rotate all</button><button id="heal" disabled aria-pressed="true">Healing enabled</button><button id="grid" disabled aria-pressed="true">Grid visible</button><button id="zoom" disabled>Toggle 2×</button></div><div class="controls motion-controls"><strong>Broken motion:</strong><label>Target <select id="motion-target" disabled><option value="kettle" selected>Kettle V47</option><option value="dishwasher">Dishwasher</option></select></label><label>Strength <select id="motion-mode" disabled><option value="off">Off</option><option value="subtle" selected>Subtle</option><option value="emphatic">Emphatic</option></select></label><button id="sfx-toggle" disabled aria-pressed="false">SFX off</button><label id="sfx-drop" class="sfx-drop">Drop replacement SFX here<input id="sfx-file" type="file" accept="audio/*" disabled><small id="sfx-name">placeholder · metal-rattle-placeholder.wav</small></label><span id="motion-readout" class="readout"></span></div>''')
    page = require_replace(page, '<p class="rule">Try dragging the Broken dishwasher, sending it to another bay, dropping another unit onto its bay, or rotating the whole run: every operation which would move it is rejected. Select Off or On to represent repair and unlock it; switch back to Broken to lock its new exact position.</p>', '<p class="rule">Try moving the Broken dishwasher or Kettle V47 support, displacing either with a swap, or rotating the run: the existing Broken lock rejects the operation. Repairing the appliance stops its transform and active sound nodes synchronously, resets it to the static candidate pose, and unlocks movement. Kettle steam is drawn in a non-transforming anchor layer over the open top.</p>')
    page = require_replace(page, '<canvas class="room" id="room" width="772" height="224" aria-label="Modular kitchen demonstrating a position-locked broken dishwasher"></canvas>', '<canvas class="room" id="room" width="772" height="224" aria-label="Modular kitchen demonstrating configurable broken-appliance motion on Kettle V47 and the dishwasher"></canvas>')
    page = require_replace(page, '<section class="panel"><h2>Reusable animation library addition · dishwasher suds</h2>', '''<section class="panel"><h2>Reusable broken-appliance motion contract</h2><div class="contract-grid"><div><strong>Static art stays static</strong><p>Object pixels are never rewritten. Presentation creates a whole-object transform layer and optional named component layers.</p></div><div><strong>Effects keep their own anchor</strong><p>Steam, suds, water and smoke remain asset-local environmental layers and do not inherit body vibration unless explicitly configured.</p></div><div><strong>Repair is synchronous</strong><p>Any non-Broken transition zeros transforms, cancels pending rattle timers, stops active sound nodes and releases the existing movement lock immediately.</p></div></div><p class="rule">The registry accepts a bottom-contact pivot, Off/Subtle/Emphatic transform presets, optional component transforms, an effect anchor policy and an intermittent SFX recipe. Dishwasher uses the whole-object path today; its door can adopt a component layer later without changing the contract.</p></section>

<section class="panel"><h2>Reusable animation library addition · dishwasher suds</h2>''')
    page = require_replace(page, '<a href="/keeper-review/kitchen-kettle-ligne-claire-v1/">Kettle proof</a>', '<strong>Kettle V47 is the sole candidate above</strong>')
    page = require_replace(page, '<p class="warn"><strong>Review boundary:</strong> V42 is an immutable, unapproved integration proof. Approved V41 behaviour, approved V3/V8 art, all source files and all production selectors remain byte-for-byte untouched. Reject by deleting only this V42 pack and route.</p>', '<p class="warn"><strong>Review boundary:</strong> V46 is an immutable, unapproved motion/SFX integration proof. V47 is the approved visual authority and the only kettle offered here, but remains unpromoted and unwired. Approved V41 behaviour, approved V3/V8 art, all source files and all production selectors remain byte-for-byte untouched. Reject by deleting only this V46 pack and route.</p>')

    kettle_contract = {
        "assets": [
            "kettle--kettle-off.png", "kettle--kettle-on.png", "kettle--kettle-broken-body.png", "kettle--kettle-broken-lid.png",
            "kettle--fx-kettle-on-steam--regular-f40.png", "kettle--fx-kettle-broken-steam--regular-f40.png",
        ],
        "states": {"off": {"broken": False}, "on": {"broken": False}, "broken": {"broken": True}},
        "supportAssetId": "cabinetA",
        "supportPlaneY": 141,
        "effectAnchor": {"broken": [27, -78], "inheritsBodyTransform": False},
    }
    page = require_replace(page, "},A='/keeper-review/kitchen-ligne-claire-complete-review-v46/assets/'", "},KETTLE=" + json.dumps(kettle_contract, separators=(",", ":")) + ",A='/keeper-review/kitchen-ligne-claire-complete-review-v46/assets/'")
    page = require_replace(page, "dishState='broken',drag=null,heal=true,showGrid=true,start=performance.now(),layerSerial=1", "dishState='broken',kettleState='broken',motionTarget='kettle',motionMode='subtle',sfxEnabled=false,audioContext=null,sfxBuffer=null,sfxLabel='placeholder · metal-rattle-placeholder.wav',sfxTimer=null,activeSfx=new Set(),renderTime=performance.now(),drag=null,heal=true,showGrid=true,start=performance.now(),layerSerial=1")
    page = require_replace(page, "const names=Object.keys(DATA.publishedAssets)", "const names=[...Object.keys(DATA.publishedAssets),...KETTLE.assets]")

    old_draw = "function drawAsset(id,x,alpha=1,raw=false){if(id==='sink')return drawSink(x,!raw&&heal&&!sinkHasLeft(),alpha);ctx.save();ctx.globalAlpha=alpha;if(kind(id)==='cabinet')ctx.drawImage(imgs[cabinetName(id,neighbours(id),raw||!heal)],x-4,130);else if(id==='oven')ctx.drawImage(imgs['oven-on.png'],x-4,127);else if(id==='fridge')ctx.drawImage(imgs['fridge-standard.png'],x-30,130);else ctx.drawImage(imgs[dishwasherName(dishState,neighbours(id),raw||!heal)],x-7,130);ctx.restore()}"
    new_draw = """function drawAsset(id,x,alpha=1,raw=false){if(id==='sink')return drawSink(x,!raw&&heal&&!sinkHasLeft(),alpha);ctx.save();ctx.globalAlpha=alpha;const pose=id==='dishwasher'?motionPose('dishwasher',renderTime):ZERO_POSE,pivot={x:x+42,y:208};applyPose(pivot,pose);if(kind(id)==='cabinet')ctx.drawImage(imgs[cabinetName(id,neighbours(id),raw||!heal)],x-4,130);else if(id==='oven')ctx.drawImage(imgs['oven-on.png'],x-4,127);else if(id==='fridge')ctx.drawImage(imgs['fridge-standard.png'],x-30,130);else ctx.drawImage(imgs[dishwasherName(dishState,neighbours(id),raw||!heal)],x-7,130);ctx.restore()}
const ZERO_POSE={dx:0,dy:0,angle:0},MOTION={off:{cycle:1,keys:[[0,0,0,0]]},subtle:{cycle:1390,keys:[[0,0,0,0],[.11,.45,-.18,.32],[.29,-.7,.12,-.42],[.43,.2,.28,.18],[.68,-.32,-.2,-.26],[.84,.6,.08,.35],[1,0,0,0]]},emphatic:{cycle:910,keys:[[0,0,0,0],[.08,1.7,-.7,1.15],[.25,-2.2,.45,-1.45],[.39,.8,1.05,.8],[.61,-1.25,-.9,-1.1],[.78,2.1,.25,1.6],[.92,-.7,.55,-.7],[1,0,0,0]]}};
function applianceBroken(id){return id==='kettle'?kettleState==='broken':dishState==='broken'}function motionPose(id,t){if(id!==motionTarget||!applianceBroken(id)||motionMode==='off')return ZERO_POSE;const p=MOTION[motionMode],phase=((t-start)%p.cycle)/p.cycle;let a=p.keys[0],b=p.keys.at(-1);for(let i=1;i<p.keys.length;i++)if(phase<=p.keys[i][0]){a=p.keys[i-1];b=p.keys[i];break}const q=(phase-a[0])/(b[0]-a[0]||1),s=q*q*(3-2*q);return{dx:a[1]+(b[1]-a[1])*s,dy:a[2]+(b[2]-a[2])*s,angle:a[3]+(b[3]-a[3])*s}}function applyPose(pivot,pose){ctx.translate(pivot.x+pose.dx,pivot.y+pose.dy);ctx.rotate(pose.angle*Math.PI/180);ctx.translate(-pivot.x,-pivot.y)}
function kettleRect(state){return state==='broken'?{sx:20,sy:30,sw:216,sh:196,x:pos.cabinetA+11,y:82,w:62,h:59}:{sx:20,sy:53,sw:200,sh:172,x:pos.cabinetA+14,y:90,w:56,h:51}}function drawKettleFrame(image,rect,pose,pivot){ctx.save();applyPose(pivot,pose);ctx.drawImage(image,rect.sx,rect.sy,rect.sw,rect.sh,rect.x,rect.y,rect.w,rect.h);ctx.restore()}function drawKettleSteam(state,t){if(state==='off')return;const cell=state==='broken'?[144,192]:[128,176],im=imgs[`kettle--fx-kettle-${state}-steam--regular-f40.png`],frame=Math.floor((t-start)/250)%40;if(state==='broken')ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+27,63,27,42);else ctx.drawImage(im,frame*cell[0],0,...cell,pos.cabinetA+54,69,20,36)}function drawKettle(t){const rect=kettleRect(kettleState),pivot={x:pos.cabinetA+42,y:141};if(kettleState!=='broken'){drawKettleFrame(imgs[`kettle--kettle-${kettleState}.png`],rect,ZERO_POSE,pivot);drawKettleSteam(kettleState,t);return}const base=motionPose('kettle',t),strength=motionMode==='emphatic'?1:motionMode==='subtle'?.45:0,hover=Math.sin((t-start)/235)*2.2*strength,lid={dx:base.dx+Math.sin((t-start)/91)*1.1*strength,dy:base.dy-hover,angle:base.angle+Math.sin((t-start)/173)*3.4*strength};drawKettleFrame(imgs['kettle--kettle-broken-body.png'],rect,base,pivot);drawKettleFrame(imgs['kettle--kettle-broken-lid.png'],rect,lid,{x:rect.x+22,y:rect.y+18});drawKettleSteam('broken',t)}
function stopSfx(){if(sfxTimer){clearTimeout(sfxTimer);sfxTimer=null}for(const node of activeSfx){try{node.stop()}catch{}try{node.disconnect()}catch{}}activeSfx.clear()}async function ensureSfx(){audioContext??=new AudioContext();if(!sfxBuffer){const response=await fetch(A+'broken-appliance-metal-rattle-placeholder.wav');if(!response.ok)throw new Error('placeholder SFX failed to load');sfxBuffer=await audioContext.decodeAudioData(await response.arrayBuffer())}await audioContext.resume()}async function metalRattle(){if(!sfxEnabled||motionMode==='off'||!applianceBroken(motionTarget))return;await ensureSfx();if(!sfxEnabled||!applianceBroken(motionTarget))return;const source=audioContext.createBufferSource(),gain=audioContext.createGain();source.buffer=sfxBuffer;gain.gain.value=motionMode==='emphatic'?.9:.48;source.connect(gain).connect(audioContext.destination);activeSfx.add(source);source.onended=()=>activeSfx.delete(source);source.start();sfxTimer=setTimeout(metalRattle,motionMode==='emphatic'?480+Math.random()*900:1250+Math.random()*2100)}function syncSfx(){stopSfx();if(sfxEnabled&&motionMode!=='off'&&applianceBroken(motionTarget))sfxTimer=setTimeout(()=>metalRattle().catch(error=>{sfxEnabled=false;syncMotionUi();document.getElementById('sfx-name').textContent='Could not decode audio: '+error.message}),90)}async function replaceSfx(file){if(!file||!file.type.startsWith('audio/'))throw new Error('Drop an audio file');stopSfx();audioContext??=new AudioContext();sfxBuffer=await audioContext.decodeAudioData(await file.arrayBuffer());sfxLabel=`browser-local replacement · ${file.name}`;document.getElementById('sfx-name').textContent=sfxLabel;syncSfx();syncMotionUi()}function syncMotionUi(){document.getElementById('motion-readout').textContent=`${motionTarget} · ${motionMode} · ${applianceBroken(motionTarget)?'Broken / active':'repaired / static'} · ${sfxEnabled?'rattle armed':'silent'}`;document.getElementById('sfx-toggle').textContent=sfxEnabled?'SFX on':'SFX off';document.getElementById('sfx-toggle').setAttribute('aria-pressed',String(sfxEnabled));document.getElementById('sfx-name').textContent=sfxLabel}"""
    page = require_replace(page, old_draw, new_draw)
    page = require_replace(page, "function render(t=performance.now()){if(!ready)return requestAnimationFrame(render);ctx.drawImage", "function render(t=performance.now()){if(!ready)return requestAnimationFrame(render);renderTime=t;ctx.drawImage")
    page = require_replace(page, "drawFrontRepairs(js);if(dishState==='broken')", "drawFrontRepairs(js);drawKettle(t);if(dishState==='broken')")
    page = require_replace(page, "function selectAsset(id){selected=id;document.querySelectorAll('[data-asset]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.asset===id)))}function isLocked(id){return id==='dishwasher'&&dishState==='broken'}", "function selectAsset(id){selected=id;document.querySelectorAll('[data-asset]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.asset===id)))}function isLocked(id){return(id==='dishwasher'&&dishState==='broken')||(id===KETTLE.supportAssetId&&kettleState==='broken')}function lockLabel(id){return id===KETTLE.supportAssetId&&kettleState==='broken'?'cabinetA carries Broken Kettle V47':id}")
    page = require_replace(page, "if(isLocked(id)){lastMessage=`Blocked: ${id} is Broken and fixed at x${old}.`;return false}if(other&&other!==id&&isLocked(other)){lastMessage=`Blocked: x${target} contains Broken ${other}; it cannot be displaced.`;return false}", "if(isLocked(id)){lastMessage=`Blocked: ${lockLabel(id)} is fixed at x${old}.`;return false}if(other&&other!==id&&isLocked(other)){lastMessage=`Blocked: x${target} contains ${lockLabel(other)}; it cannot be displaced.`;return false}")
    page = require_replace(page, "function setState(state){dishState=state;lastMessage=state==='broken'?`Dishwasher became Broken and locked at exact x${pos.dishwasher}.`:`Dishwasher repaired to ${state}; movement unlocked.`;document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)))}", "function setState(state){dishState=state;lastMessage=state==='broken'?`Dishwasher became Broken and locked at exact x${pos.dishwasher}.`:`Dishwasher repaired to ${state}; motion and sound stopped immediately; movement unlocked.`;document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));syncSfx();syncMotionUi()}function setKettleState(state){kettleState=state;lastMessage=state==='broken'?`Kettle V47 became Broken and locked support ${KETTLE.supportAssetId} at x${pos[KETTLE.supportAssetId]}.`:`Kettle V47 repaired to ${state}; motion and sound stopped immediately; support movement unlocked.`;document.querySelectorAll('[data-kettle-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kettleState===state)));syncSfx();syncMotionUi()}")
    page = require_replace(page, "document.querySelectorAll('[data-asset]').forEach(b=>b.onclick=()=>selectAsset(b.dataset.asset));document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>setState(b.dataset.state));", "document.querySelectorAll('[data-asset]').forEach(b=>b.onclick=()=>selectAsset(b.dataset.asset));document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>setState(b.dataset.state));document.querySelectorAll('[data-kettle-state]').forEach(b=>b.onclick=()=>setKettleState(b.dataset.kettleState));document.getElementById('motion-target').onchange=e=>{motionTarget=e.target.value;syncSfx();syncMotionUi()};document.getElementById('motion-mode').onchange=e=>{motionMode=e.target.value;syncSfx();syncMotionUi()};document.getElementById('sfx-toggle').onclick=()=>{sfxEnabled=!sfxEnabled;syncSfx();syncMotionUi()};const sfxFile=document.getElementById('sfx-file'),sfxDrop=document.getElementById('sfx-drop');sfxFile.onchange=()=>replaceSfx(sfxFile.files?.[0]).catch(error=>document.getElementById('sfx-name').textContent=error.message);sfxDrop.ondragover=e=>{e.preventDefault();sfxDrop.classList.add('dragging')};sfxDrop.ondragleave=()=>sfxDrop.classList.remove('dragging');sfxDrop.ondrop=e=>{e.preventDefault();sfxDrop.classList.remove('dragging');replaceSfx(e.dataTransfer.files?.[0]).catch(error=>document.getElementById('sfx-name').textContent=error.message)};")
    page = require_replace(page, "document.querySelectorAll('button').forEach(el=>el.disabled=false);", "document.querySelectorAll('button').forEach(el=>el.disabled=false);for(const id of ['motion-target','motion-mode','sfx-file'])document.getElementById(id).disabled=false;")
    page = require_replace(page, "selectAsset('dishwasher');setState('broken');syncFx()", "selectAsset('dishwasher');setState('broken');setKettleState('broken');motionTarget='kettle';motionMode='subtle';sfxEnabled=false;document.getElementById('motion-target').value=motionTarget;document.getElementById('motion-mode').value=motionMode;syncSfx();syncMotionUi();syncFx()")
    page = require_replace(page, "selectAsset('dishwasher');setState('broken');syncFx();requestAnimationFrame(render)", "selectAsset('dishwasher');setState('broken');setKettleState('broken');syncMotionUi();syncFx();requestAnimationFrame(render)")
    path.write_text(page)


def build() -> None:
    if PACK.exists() or PUBLIC.exists():
        raise RuntimeError("refusing to overwrite immutable Kitchen Complete Review V46")
    if not (SOURCE_PACK / "manifest.json").is_file() or not (SOURCE_PUBLIC / "index.html").is_file():
        raise RuntimeError("complete V45 source review is missing")
    shutil.copytree(SOURCE_PACK, PACK)
    (PUBLIC / "assets").mkdir(parents=True)
    source_register = json.loads((SOURCE_PACK / "batch-register.json").read_text())
    published = []
    for record in source_register["publishedAssets"]:
        name = Path(record["publicAssemblyPath"]).name
        if name.startswith("kettle--") or name == "contact-kettle.png":
            continue
        source = ROOT / record["source"]
        shutil.copy2(source, PUBLIC / "assets" / name)
        published.append({**record, "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}"})

    source_manifest = (SOURCE_PACK / "manifest.json").read_text()
    source_manifest = source_manifest.replace(SOURCE_SET, SET).replace(
        "kitchen-ligne-claire-complete-review-2026-10-22-v45",
        "kitchen-ligne-claire-complete-review-2026-10-22-v46",
    )
    manifest = json.loads(source_manifest)
    manifest["version"] = VERSION
    manifest["objects"] = [record for record in manifest["objects"] if record["family"] != "kettle"]
    manifest["effects"] = [record for record in manifest["effects"] if record["family"] != "kettle"]
    manifest["contracts"] = [record for record in manifest["contracts"] if "kettle" not in record["role"]]
    for directory in (PACK / "candidates", PACK / "effects"):
        for stale in directory.glob("kettle--*"):
            stale.unlink()

    v47_objects, v47_effects, v47_contracts = collect_v47()
    for record in v47_objects:
        target = PACK / "candidates" / f"kettle--{record['filename']}"
        shutil.copy2(ROOT / record["candidateFile"], target)
        shutil.copy2(target, PUBLIC / "assets" / target.name)
        record["reviewFile"] = target.relative_to(ROOT).as_posix()
        record["reviewSha256"] = sha(target)
        published.append({"source": record["reviewFile"], "sourceSha256": record["reviewSha256"], "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{target.name}"})
    for record in v47_effects:
        target = PACK / "effects" / f"kettle--{record['filename']}"
        shutil.copy2(ROOT / record["candidateFile"], target)
        shutil.copy2(target, PUBLIC / "assets" / target.name)
        record["reviewFile"] = target.relative_to(ROOT).as_posix()
        record["reviewSha256"] = sha(target)
        published.append({"source": record["reviewFile"], "sourceSha256": record["reviewSha256"], "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{target.name}"})
    manifest["objects"].extend(v47_objects)
    manifest["effects"].extend(v47_effects)
    manifest["contracts"].extend(v47_contracts)

    previous_pack = base.PACK
    base.PACK = PACK
    try:
        kettle_sheet = base.make_sheets(v47_objects)[0]
    finally:
        base.PACK = previous_pack
    manifest["contactSheets"] = [sheet for sheet in manifest["contactSheets"] if sheet["family"] != "kettle"] + [kettle_sheet]
    shutil.copy2(ROOT / kettle_sheet["file"], PUBLIC / "assets/contact-kettle.png")
    published.append({"source": kettle_sheet["file"], "sourceSha256": kettle_sheet["sha256"], "publicAssemblyPath": f"public/keeper-review/{SET}/assets/contact-kettle.png"})

    components = PACK / "components"
    components.mkdir()
    body_path = components / "kettle-broken-body.png"
    lid_path = components / "kettle-broken-lid.png"
    layers = split_broken_layers(V47_PACK / "states/kettle-broken.png", body_path, lid_path)
    for source, name in ((body_path, "kettle--kettle-broken-body.png"), (lid_path, "kettle--kettle-broken-lid.png")):
        shutil.copy2(source, PUBLIC / "assets" / name)
        published.append({"source": source.relative_to(ROOT).as_posix(), "sourceSha256": sha(source), "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{name}"})
    placeholder_path = PACK / "audio/broken-appliance-metal-rattle-placeholder.wav"
    write_placeholder_rattle(placeholder_path)
    shutil.copy2(placeholder_path, PUBLIC / "assets" / placeholder_path.name)
    published.append({"source": placeholder_path.relative_to(ROOT).as_posix(), "sourceSha256": sha(placeholder_path), "publicAssemblyPath": f"public/keeper-review/{SET}/assets/{placeholder_path.name}"})

    manifest_path = PACK / "manifest.json"
    manifest["scope"] = "closed kitchen review with V47 as the sole kettle candidate and reusable broken-appliance motion/SFX"
    manifest["candidateSelection"] = {
        "kettle": {
            "active": "kitchen-kettle-bubble-authority-v47",
            "activeCandidateCount": 1,
            "supersededCandidatesOffered": [],
            "visualApproval": {"file": V47_APPROVAL.relative_to(ROOT).as_posix(), "sha256": sha(V47_APPROVAL)},
            "promotion": "none",
            "policy": "V47 replaces all pre-existing kettle candidates in this review; immutable predecessor records remain available only as history",
        }
    }
    manifest["brokenApplianceMotion"] = {
        "schema": "lighthouse-keeper/broken-appliance-motion@1",
        "modes": ["off", "subtle", "emphatic"],
        "defaultMode": "subtle",
        "wholeObject": {"type": "irregular-transform", "channels": ["translateX", "translateY", "rotation"], "artPixelsChanged": False},
        "components": {"optional": True, "kettle": {"detachedLid": "hover-vibrate", "layers": layers}},
        "environmentalEffects": {"inheritObjectTransform": False, "kettleBrokenSteam": "anchored over open top"},
        "sfx": {
            "independentToggle": True,
            "defaultEnabled": False,
            "slot": "broken-rattle",
            "placeholder": {"file": placeholder_path.relative_to(ROOT).as_posix(), "sha256": sha(placeholder_path), "label": "replaceable placeholder"},
            "replacement": {"methods": ["drag-and-drop", "file picker"], "scope": "browser-local review session", "canonicalAudioOverwritten": False},
            "playback": "intermittent AudioBufferSourceNode",
        },
        "repair": {"transition": "broken to any non-broken state", "synchronous": True, "zeroTransforms": True, "cancelPendingSfx": True, "stopActiveSoundNodes": True, "releaseMovementLock": True},
        "adopters": {"kettle": "whole object plus detached lid", "dishwasher": "whole object; component layer extension point retained"},
    }
    manifest["workbench"].update({"motionImplementationChanged": True, "approvedStateBehaviourChanged": False, "staticAssetArtChanged": False})
    manifest["workbench"].update({"sourceSet": SOURCE_SET, "sourceManifestSha256": sha(SOURCE_PACK / "manifest.json"), "rootAbsoluteAssetPrefix": f"/keeper-review/{SET}/assets/"})
    manifest["verificationRequired"] += ["motion modes", "component transforms", "static effect anchors", "SFX toggle", "synchronous repair stop"]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (PUBLIC / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
    source_page = (SOURCE_PUBLIC / "index.html").read_text().replace(SOURCE_SET, SET).replace(
        "Kitchen Ligne-Claire Complete Review V45", "Kitchen Ligne-Claire Complete Review V46"
    ).replace("V45 immutable complete kitchen review", "V46 immutable complete kitchen review").replace(
        "All V45 controls are ready.", "All V46 controls are ready."
    )
    (PUBLIC / "index.html").write_text(source_page)
    upgrade_page()
    register = {
        **source_register,
        "set": SET,
        "status": "blocked-pending-explicit-frank-approval",
        "register": False,
        "promote": False,
        "currentSelectorChanges": [],
        "productionWrites": [],
        "candidate": {
            "manifest": {"file": manifest_path.relative_to(ROOT).as_posix(), "sha256": sha(manifest_path)},
            "publicShell": {"file": (PUBLIC / "index.html").relative_to(ROOT).as_posix(), "sha256": sha(PUBLIC / "index.html")},
        },
        "publishedAssets": published,
    }
    (PACK / "batch-register.json").write_text(json.dumps(register, indent=2) + "\n")
    (PACK / "contact-sheet-index.json").write_text(json.dumps({"set": SET, "sheets": manifest["contactSheets"]}, indent=2) + "\n")
    verify()
    print("Built Kitchen Complete Review V46 with V47-only kettle selection and reusable broken-appliance motion.")


def verify() -> None:
    manifest = json.loads((PACK / "manifest.json").read_text())
    if manifest["set"] != SET or manifest["candidateSelection"]["kettle"]["active"] != "kitchen-kettle-bubble-authority-v47":
        raise RuntimeError("V46/V47 selection identity drift")
    kettle_authorities = {record["authority"] for record in manifest["objects"] if record["family"] == "kettle"}
    if kettle_authorities != {"kitchen-kettle-bubble-authority-v47"}:
        raise RuntimeError(f"superseded kettle candidate leaked into V46: {kettle_authorities}")
    if len([record for record in manifest["objects"] if record["family"] == "kettle"]) != 3:
        raise RuntimeError("V46 must expose exactly the V47 Off/On/Broken states")
    layers = manifest["brokenApplianceMotion"]["components"]["kettle"]["layers"]
    source = Image.open(ROOT / layers["source"]).convert("RGBA")
    body = Image.open(ROOT / layers["body"]).convert("RGBA")
    lid = Image.open(ROOT / layers["lid"]).convert("RGBA")
    if list(Image.alpha_composite(body, lid).getdata()) != list(source.getdata()):
        raise RuntimeError("V47 motion layers no longer recompose pixel-exactly")
    for key in ("source", "body", "lid"):
        if sha(ROOT / layers[key]) != layers[f"{key}Sha256"]:
            raise RuntimeError(f"V47 {key} layer hash drift")
    motion = manifest["brokenApplianceMotion"]
    if motion["modes"] != ["off", "subtle", "emphatic"] or not motion["sfx"]["independentToggle"]:
        raise RuntimeError("broken-appliance control contract drift")
    if not all(motion["repair"][key] for key in ("synchronous", "zeroTransforms", "cancelPendingSfx", "stopActiveSoundNodes", "releaseMovementLock")):
        raise RuntimeError("repair no longer stops motion/sound synchronously")
    html = (PUBLIC / "index.html").read_text()
    required = ["Kettle Bubble Authority V47 only", "motion-target", "motion-mode", "SFX off", "Drop replacement SFX here", "sfx-file", "replaceSfx", "broken-appliance-metal-rattle-placeholder.wav", "kettle-broken-lid.png", "drawKettleSteam('broken',t)", "visualAnchorRemainsStaticDuringBodyMotion", "stopSfx()", "setKettleState", "repair"]
    for text in required:
        if text not in html and text not in json.dumps(manifest):
            raise RuntimeError(f"V46 workbench contract missing {text}")
    forbidden = ["/keeper-review/kitchen-kettle-ligne-claire-v1/", "Kettle proof"]
    if any(text in html for text in forbidden):
        raise RuntimeError("superseded kettle candidate remains selectable in V46")
    if manifest["registration"]["register"] or manifest["registration"]["promote"] or manifest["registration"]["productionWrites"]:
        raise RuntimeError("registration gate opened")
    print("Verified Kitchen Complete Review V46: V47-only kettle, pixel-exact layers, three motion modes, replaceable SFX slot and immediate repair stop.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify() if args.verify else build()
