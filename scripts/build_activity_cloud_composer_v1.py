#!/usr/bin/env python3
"""Build the immutable Activity Cloud Composer V1 review candidate."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SET = "activity-cloud-composer-v1"
PACK = ROOT / "art/drafts/activity-cloud-composer-2026-10-19-v1"
SOURCE = PACK / "source/bbq-expansion-generated-v1.png"
COMPONENTS = PACK / "drafts/components"
EVIDENCE = PACK / "evidence"
PUBLIC = ROOT / "public/keeper-review" / SET
ASSETS = PUBLIC / "assets"
V3_PACK = ROOT / "art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3"
V3_CATALOGUE = V3_PACK / "catalogue.json"
V3_PUBLIC_CATALOGUE = ROOT / "public/keeper-review/keeper-prime-back-work-activity-callout-v3/catalogue.json"
V3_REGISTER = V3_PACK / "batch-register.json"
ARCHIVE_INDEX = ROOT / "review-archive/index.json"
PAGE = PUBLIC / "index.html"
CELL = 256
SAFE_GUTTER = 20
SPLIT_X = (520, 1028)
SPLIT_Y = 512
NEW_CELLS = (
    ("bbq-sausages", "bbq", (0, 0, 520, 512)),
    ("bbq-hotdogs", "bbq", (520, 0, 1028, 512)),
    ("bbq-burgers", "bbq", (1028, 0, 1536, 512)),
    ("bbq-ketchup", "bbq", (0, 512, 520, 1024)),
    ("bbq-charcoal", "bbq", (520, 512, 1028, 1024)),
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        path.write_text(json.dumps(value, separators=(",", ":")) + "\n")
    else:
        path.write_text(json.dumps(value, indent=2) + "\n")


def alpha_bounds(image: Image.Image) -> dict:
    alpha = np.asarray(image.getchannel("A")) > 8
    ys, xs = np.where(alpha)
    if not len(xs):
        raise RuntimeError("component has no visible pixels")
    return {
        "minX": int(xs.min()), "minY": int(ys.min()),
        "maxX": int(xs.max()), "maxY": int(ys.max()),
        "opaquePixels": int(alpha.sum()),
    }


def edge_alpha(image: Image.Image) -> int:
    alpha = np.asarray(image.getchannel("A")) > 8
    return int(alpha[0, :].sum() + alpha[-1, :].sum() + alpha[:, 0].sum() + alpha[:, -1].sum())


def gutter(image: Image.Image) -> int:
    b = alpha_bounds(image)
    return min(b["minX"], b["minY"], image.width - 1 - b["maxX"], image.height - 1 - b["maxY"])


def isolate(source: Image.Image, crop: tuple[int, int, int, int]) -> tuple[Image.Image, dict]:
    owned = source.crop(crop)
    pixels = np.asarray(owned).copy()
    pixels[pixels[:, :, 3] <= 8, 3] = 0
    owned = Image.fromarray(pixels)
    bounds = alpha_bounds(owned)
    trimmed = owned.crop((bounds["minX"], bounds["minY"], bounds["maxX"] + 1, bounds["maxY"] + 1))
    available = CELL - SAFE_GUTTER * 2
    scale = min(available / trimmed.width, available / trimmed.height)
    size = (max(1, round(trimmed.width * scale)), max(1, round(trimmed.height * scale)))
    rendered = trimmed.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    canvas.alpha_composite(rendered, ((CELL - size[0]) // 2, (CELL - size[1]) // 2))
    evidence = {
        "sourceCrop": list(crop), "sourceVisiblePixels": bounds["opaquePixels"],
        "registeredBounds": alpha_bounds(canvas), "edgeAlphaPixels": edge_alpha(canvas),
        "transparentGutterPx": gutter(canvas),
        "ownership": {"ownerCount": 1, "ambiguousPixels": 0, "unownedVisiblePixels": 0},
    }
    return canvas, evidence


def boundary_count(source: Image.Image, axis: str, coordinate: int) -> int:
    alpha = np.asarray(source.getchannel("A")) > 8
    return int(alpha[:, coordinate].sum() if axis == "x" else alpha[coordinate, :].sum())


def archive_hash_for_url(index: dict, url: str) -> str:
    entry = index["legacyPaths"].get(url)
    if not entry:
        raise RuntimeError(f"V3 component is missing from archive index: {url}")
    return entry["sha256"]


def build_page() -> str:
    return r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Activity Cloud Composer V1</title>
<style>
:root{color-scheme:dark;--ink:#edf4f7;--muted:#9fb3bd;--panel:#13232e;--line:#36515e;--gold:#f3b54a;--sea:#70d1ca;--danger:#ff8e89}*{box-sizing:border-box}body{margin:0;background:#07141d;color:var(--ink);font:15px/1.45 system-ui,sans-serif}header,main{max-width:1420px;margin:auto;padding:20px}header{border-bottom:1px solid var(--line)}a{color:#c9b5ff}.tags,.row,.actions{display:flex;gap:9px;align-items:center;flex-wrap:wrap}.tag{border:1px solid #b76c7e;border-radius:999px;padding:4px 10px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;margin:16px 0}h1,h2,h3{margin:.1em 0 .6em}h1{font-size:30px}h2{font-size:21px}.grid{display:grid;grid-template-columns:minmax(320px,.75fr) minmax(520px,1.25fr);gap:16px}.fields{display:grid;grid-template-columns:1fr 1fr;gap:12px}.fields label,.stack{display:grid;gap:5px}.wide{grid-column:1/-1}input,select,button,textarea{font:inherit;color:var(--ink);background:#0c1a24;border:1px solid #4b6572;border-radius:7px;padding:9px}button{cursor:pointer}button:hover:not(:disabled){border-color:var(--gold)}button:disabled{opacity:.45;cursor:not-allowed}.primary{background:#6d4e19;border-color:var(--gold)}.danger{border-color:#a45659}.status{padding:10px 12px;border-left:4px solid var(--gold);background:#2a2818}.status.good{border-color:#79d7a4;color:#a5e7bd}.status.bad{border-color:var(--danger);color:#ffb0ab}.previews{display:grid;grid-template-columns:1fr 1fr;gap:12px}.preview-card{background:#0b1923;border:1px solid #294450;border-radius:10px;padding:10px}.stage{height:300px;position:relative;overflow:hidden;background:#213843;border-radius:8px;border-bottom:4px solid #42606b}.actor{position:absolute;width:176px;height:176px;object-fit:contain;left:50%;top:122px;transform:translateX(-50%);image-rendering:auto}.cloud{position:absolute;width:270px;height:155px;left:50%;top:0;transform:translateX(-50%);pointer-events:none}.bubble .cloud::before{content:"";position:absolute;inset:9px 13px 13px;background:rgba(244,239,215,.16);border:3px solid rgba(237,244,247,.7);border-radius:48% 52% 46% 54%}.piece{position:absolute;width:104px;height:104px;left:50%;top:50%;object-fit:contain;transform-origin:center}.asset-target{position:absolute;right:10px;bottom:8px;max-width:46%;padding:5px 8px;background:#07141dcc;border:1px dashed var(--sea);border-radius:7px;color:#b9ece8;font-size:12px}.library-tools{display:grid;grid-template-columns:1fr 180px auto;gap:8px}.library{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:8px;max-height:620px;overflow:auto;margin-top:12px}.token{background:#19303d;border:1px solid #36515e;border-radius:9px;padding:7px;display:grid;gap:5px;text-align:left}.token.selected{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold) inset}.token img{width:100%;aspect-ratio:1;object-fit:contain;background:linear-gradient(45deg,#68808a 25%,transparent 25%),linear-gradient(-45deg,#68808a 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#68808a 75%),linear-gradient(-45deg,transparent 75%,#68808a 75%);background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0}.token small{overflow:hidden;text-overflow:ellipsis}.selected-list{display:grid;gap:8px}.selected-row{display:grid;grid-template-columns:54px 1fr 130px auto auto auto;gap:7px;align-items:center;background:#0b1923;border:1px solid #294450;border-radius:9px;padding:7px}.selected-row img{width:48px;height:48px;object-fit:contain}.counter{font-weight:700;color:var(--gold)}.saved{display:grid;gap:7px}.saved-row{display:flex;justify-content:space-between;gap:8px;align-items:center;border-bottom:1px solid #294450;padding:7px 0}.metric{font-family:ui-monospace,monospace;color:#bdd0d8}.small{color:var(--muted);font-size:13px}.hidden{display:none!important}@media(max-width:900px){.grid,.previews{grid-template-columns:1fr}.fields{grid-template-columns:1fr}.wide{grid-column:auto}.selected-row{grid-template-columns:48px 1fr 110px auto}.selected-row button.move{display:none}}
</style></head><body>
<header><a href="/keeper-review/keeper-prime-back-work-activity-callout-v3/index.html">← Immutable V3 vocabulary</a><h1>Activity Cloud Composer V1</h1><div class="tags"><span class="tag">Review-only tool</span><span class="tag">4–5 owned elements</span><span class="tag">Local drafts + JSON export</span><span class="tag">No runtime promotion</span></div><p>Package the shared activity vocabulary around any labelled household asset. The tool changes recipe metadata only: it never edits the Keeper, source tokens or household asset.</p></header>
<main><p id="loadStatus" class="status">Loading and decoding the complete activity library…</p>
<div class="grid"><section class="panel"><h2>1 · Name and attach</h2><div class="fields">
<label>Activity label<input id="activityLabel" value="Garden BBQ"></label><label>Recipe key<input id="recipeKey" value="garden-bbq"></label>
<label>Household asset label<input id="targetLabel" value="Garden barbecue"></label><label>Household asset ID<input id="targetId" value="outdoor.bbq"></label>
<label>Body compatibility<select id="compatibility"><option value="rear-work-with-context">Rear-work with contextual asset</option><option value="rear-work">Generic rear-work</option><option value="dedicated-pose-required">Dedicated pose required</option></select></label><label>Named SFX cue<input id="sfx" value="bbq-sizzle"></label>
<label class="wide">Notes<textarea id="notes" rows="2" placeholder="Optional implementation note"></textarea></label></div>
<h2 style="margin-top:18px">2 · Package elements</h2><p><span id="selectionCount" class="counter">0/5</span> · choose four or five. The first item is the hero; reorder the package below.</p><div id="selectedList" class="selected-list"></div>
<div class="actions" style="margin-top:12px"><button id="saveLocal" class="primary" disabled>Save local draft</button><button id="exportJson" disabled>Export JSON</button><button id="copyJson" disabled>Copy JSON</button><button id="importJson">Import JSON</button><input id="importFile" type="file" accept="application/json" class="hidden"><button id="reset" class="danger">Reset</button></div><p id="hashReadout" class="metric"></p><p id="validation" class="small"></p>
<h3>Saved on this browser</h3><div id="savedList" class="saved"><p class="small">No saved drafts.</p></div></section>
<section class="panel"><h2>Live 42-frame proof</h2><div class="previews"><article class="preview-card"><h3>Open radial · no bubble</h3><div class="stage"><img id="orbitActor" class="actor" alt="Prime rear-work body"><div id="orbitCloud" class="cloud"></div><span id="orbitTarget" class="asset-target"></span></div></article><article class="preview-card bubble"><h3>Activity bustle · bubble</h3><div class="stage"><img id="bubbleActor" class="actor" alt="Prime rear-work body"><div id="bubbleCloud" class="cloud"></div><span id="bubbleTarget" class="asset-target"></span></div></article></div><div class="actions" style="margin-top:10px"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>◀ Frame</button><button id="next" disabled>Frame ▶</button><label><input id="showBody" type="checkbox" checked> Keeper body</label><label><input id="reducedMotion" type="checkbox"> Reduced motion</label></div><p id="frameReadout" class="metric"></p><p id="compatWarning" class="status hidden"></p><p class="small">Both treatments are generated from the same ordered component package. Body playback is withheld automatically for dedicated-pose recipes.</p>
<h2>Element library</h2><div class="library-tools"><input id="search" placeholder="Search names and families"><select id="family"><option value="all">All families</option></select><button id="clearSelection">Clear selection</button></div><div id="library" class="library"></div></section></div>
<section class="panel"><h2>Export contract</h2><p>Exports contain the household-asset attachment, ordered component hashes, body-compatibility declaration, both presentation treatments, timing, optional SFX and a deterministic recipe SHA-256. They are proposals only until imported into a separately reviewed implementation.</p></section></main>
<script>
const SET='activity-cloud-composer-v1',STORAGE='lighthouse-keeper.activity-cloud-composer-v1';const $=id=>document.getElementById(id);let data=null,selection=[],frame=18,timer=null,bodyFrame=0,hash='';const controls=['saveLocal','exportJson','copyJson','play','pause','prev','next'];
const enc=new TextEncoder();function canonical(value){if(Array.isArray(value))return value.map(canonical);if(value&&typeof value==='object')return Object.fromEntries(Object.keys(value).sort().map(k=>[k,canonical(value[k])]));return value}function canonicalText(value){return JSON.stringify(canonical(value))}async function digest(value){const bytes=await crypto.subtle.digest('SHA-256',enc.encode(canonicalText(value)));return [...new Uint8Array(bytes)].map(v=>v.toString(16).padStart(2,'0')).join('')}
function slug(v){return v.toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,64)}function valid(){return selection.length>=data.composer.minimumElements&&selection.length<=data.composer.maximumElements&&$('activityLabel').value.trim()&&$('recipeKey').value.trim()&&$('targetLabel').value.trim()&&$('targetId').value.trim()}
function baseRecipe(){return{schema:'lighthouse-keeper/activity-cloud-recipe@1',sourceSet:SET,activity:{key:$('recipeKey').value.trim(),label:$('activityLabel').value.trim(),notes:$('notes').value.trim()},appliesTo:{assetId:$('targetId').value.trim(),label:$('targetLabel').value.trim()},bodyCompatibility:$('compatibility').value,elements:selection.map((key,index)=>({asset:key,role:index===0?'primary':'support',order:index,sha256:data.components[key].sha256,sourceSet:data.components[key].sourceSet})),timing:{frames:42,fps:8,quietTailFrames:5},treatments:['orbit','bustle'],sfx:$('sfx').value.trim()?[{cue:$('sfx').value.trim(),kind:'activity-beat'}]:[],ownership:{componentOwnerCount:1,contextBakedIntoKeeper:false}}}
async function refreshHash(){if(!data)return;const recipe=baseRecipe();hash=await digest(recipe);$('hashReadout').textContent=`Recipe SHA-256 · ${hash}`;const ok=valid();$('validation').textContent=ok?'Ready to save or export.':'Add 4–5 elements and complete both activity and household-asset labels.';for(const id of ['saveLocal','exportJson','copyJson'])$(id).disabled=!ok}
function opacityWindow(f,start,hold,end){if(f<start||f>end)return 0;if(f<start+3)return(f-start+1)/3;if(f<=hold)return 1;return Math.max(0,(end-f+1)/Math.max(1,end-hold))}
function parts(treatment){const f=$('reducedMotion').checked?18:frame,positions=[[-60,-18,-14],[58,-20,14],[-54,25,-8],[54,23,9],[0,39,0]];return selection.map((asset,i)=>{const start=i===0?2:5+i*3,o=opacityWindow(f,start,30,36);let [x,y,r]=positions[i];if(treatment==='bustle'){x=Math.round(x*.66);y=Math.round(y*.56+13)}return{asset,x,y,rotate:r+(i===0?Math.sin(f*.25)*3:0),scale:i===0?(treatment==='orbit'?.62:.55):(treatment==='orbit'?.34:.29),opacity:o}}).filter(p=>p.opacity>0)}
function draw(host,treatment){host.innerHTML='';for(const p of parts(treatment)){const img=document.createElement('img');img.className='piece';img.src=data.components[p.asset].src;img.alt=p.asset;img.style.opacity=p.opacity;img.style.transform=`translate(calc(-50% + ${p.x}px),calc(-50% + ${p.y}px)) rotate(${p.rotate}deg) scale(${p.scale})`;host.appendChild(img)}}
function renderPreview(){if(!data)return;const compatible=$('compatibility').value!=='dedicated-pose-required',show=compatible&&$('showBody').checked,b=data.body.frames[bodyFrame%data.body.frames.length].src;for(const id of ['orbitActor','bubbleActor']){$(id).src=b;$(id).hidden=!show}draw($('orbitCloud'),'orbit');draw($('bubbleCloud'),'bustle');for(const id of ['orbitTarget','bubbleTarget'])$(id).textContent=`${$('targetLabel').value.trim()||'Unlabelled asset'} · ${$('targetId').value.trim()||'missing ID'}`;$('frameReadout').textContent=`Callout ${frame+1}/42 at 8 fps · Prime body ${bodyFrame+1}/24 at 4 fps`;$('compatWarning').classList.toggle('hidden',compatible);$('compatWarning').textContent=compatible?'':'Dedicated pose required: activity cloud remains previewable; generic rear-work Keeper is intentionally withheld.'}
function renderSelection(){const host=$('selectedList');host.innerHTML='';selection.forEach((key,i)=>{const row=document.createElement('div');row.className='selected-row';const img=document.createElement('img');img.src=data.components[key].src;img.alt='';const label=document.createElement('span');label.textContent=key;const role=document.createElement('span');role.textContent=i===0?'Hero':'Support';const up=document.createElement('button');up.textContent='↑';up.className='move';up.disabled=i===0;up.onclick=()=>move(i,-1);const down=document.createElement('button');down.textContent='↓';down.className='move';down.disabled=i===selection.length-1;down.onclick=()=>move(i,1);const remove=document.createElement('button');remove.textContent='Remove';remove.onclick=()=>{selection.splice(i,1);updateAll()};row.append(img,label,role,up,down,remove);host.append(row)});$('selectionCount').textContent=`${selection.length}/${data.composer.maximumElements}`;renderLibrary();renderPreview();refreshHash()}
function move(i,d){const j=i+d;[selection[i],selection[j]]=[selection[j],selection[i]];renderSelection()}function toggle(key){const i=selection.indexOf(key);if(i>=0)selection.splice(i,1);else if(selection.length<data.composer.maximumElements)selection.push(key);renderSelection()}
function renderLibrary(){const q=$('search').value.trim().toLowerCase(),family=$('family').value,host=$('library');host.innerHTML='';for(const [key,item] of Object.entries(data.components).sort()){if(family!=='all'&&item.family!==family)continue;if(q&&!`${key} ${item.family}`.toLowerCase().includes(q))continue;const button=document.createElement('button');button.className=`token ${selection.includes(key)?'selected':''}`;button.disabled=!selection.includes(key)&&selection.length>=5;button.onclick=()=>toggle(key);const img=document.createElement('img');img.src=item.src;img.alt=key;const name=document.createElement('small');name.textContent=key;const fam=document.createElement('small');fam.textContent=item.family;button.append(img,name,fam);host.append(button)}}
function updateAll(){renderSelection();renderSaved()}function draftWithHash(){return{...baseRecipe(),recipeSha256:hash}}
function loadSaved(){try{return JSON.parse(localStorage.getItem(STORAGE)||'{}')}catch{localStorage.removeItem(STORAGE);return{}}}function renderSaved(){const saved=loadSaved(),host=$('savedList'),entries=Object.entries(saved);host.innerHTML='';if(!entries.length){host.innerHTML='<p class="small">No saved drafts.</p>';return}for(const [key,value] of entries){const row=document.createElement('div');row.className='saved-row';const label=document.createElement('span');label.textContent=`${value.activity.label} → ${value.appliesTo.label}`;const actions=document.createElement('span');const load=document.createElement('button');load.textContent='Load';load.onclick=()=>applyRecipe(value);const del=document.createElement('button');del.textContent='Delete';del.onclick=()=>{const next=loadSaved();delete next[key];localStorage.setItem(STORAGE,JSON.stringify(next));renderSaved()};actions.append(load,del);row.append(label,actions);host.append(row)}}
function applyRecipe(r){$('activityLabel').value=r.activity?.label||'';$('recipeKey').value=r.activity?.key||'';$('notes').value=r.activity?.notes||'';$('targetLabel').value=r.appliesTo?.label||'';$('targetId').value=r.appliesTo?.assetId||'';$('compatibility').value=r.bodyCompatibility||'rear-work-with-context';$('sfx').value=r.sfx?.[0]?.cue||'';selection=(r.elements||[]).map(e=>e.asset).filter(k=>data.components[k]).slice(0,data.composer.maximumElements);updateAll()}
function download(){const recipe=draftWithHash(),blob=new Blob([JSON.stringify(recipe,null,2)+'\n'],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`activity-cloud-${slug(recipe.activity.key)||'draft'}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)}
function decode(url){return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>img.decode?img.decode().then(resolve,reject):resolve();img.onerror=reject;img.src=url})}
fetch(`/keeper-review/${SET}/catalogue.json`).then(r=>r.json()).then(async d=>{data=d;selection=[...d.defaultRecipe.elements];for(const family of [...new Set(Object.values(d.components).map(v=>v.family))].sort()){const o=document.createElement('option');o.value=family;o.textContent=family;$('family').append(o)}await Promise.all([...new Set([...Object.values(d.components).map(v=>v.src),...d.body.frames.map(v=>v.src)])].map(decode));controls.forEach(id=>$(id).disabled=false);$('loadStatus').textContent='All unique component and Prime body images loaded and decoded. Composer unlocked.';$('loadStatus').classList.add('good');updateAll()}).catch(error=>{$('loadStatus').textContent=`Preload failed; composer remains locked: ${error}`;$('loadStatus').classList.add('bad')});
$('activityLabel').oninput=()=>{if(!$('recipeKey').dataset.edited)$('recipeKey').value=slug($('activityLabel').value);updateAll()};$('recipeKey').oninput=()=>{$('recipeKey').dataset.edited='1';updateAll()};for(const id of ['targetLabel','targetId','compatibility','sfx','notes','showBody','reducedMotion'])$(id).oninput=updateAll;$('search').oninput=renderLibrary;$('family').onchange=renderLibrary;$('clearSelection').onclick=()=>{selection=[];updateAll()};$('play').onclick=()=>{clearInterval(timer);timer=setInterval(()=>{frame=(frame+1)%42;if(frame%2===0)bodyFrame=(bodyFrame+1)%24;renderPreview()},125)};$('pause').onclick=()=>clearInterval(timer);$('prev').onclick=()=>{frame=(frame+41)%42;renderPreview()};$('next').onclick=()=>{frame=(frame+1)%42;renderPreview()};$('saveLocal').onclick=()=>{const saved=loadSaved();saved[$('recipeKey').value.trim()]=draftWithHash();localStorage.setItem(STORAGE,JSON.stringify(saved));renderSaved()};$('exportJson').onclick=download;$('copyJson').onclick=()=>navigator.clipboard.writeText(JSON.stringify(draftWithHash(),null,2)+'\n');$('importJson').onclick=()=>$('importFile').click();$('importFile').onchange=async()=>{try{applyRecipe(JSON.parse(await $('importFile').files[0].text()))}catch(error){$('validation').textContent=`Import failed: ${error}`}};$('reset').onclick=()=>{selection=[...data.defaultRecipe.elements];$('activityLabel').value='Garden BBQ';$('recipeKey').value='garden-bbq';delete $('recipeKey').dataset.edited;$('targetLabel').value='Garden barbecue';$('targetId').value='outdoor.bbq';$('compatibility').value='rear-work-with-context';$('sfx').value='bbq-sizzle';$('notes').value='';frame=18;bodyFrame=0;updateAll()};
</script></body></html>'''


def main() -> None:
    for required in (SOURCE, V3_CATALOGUE, V3_PUBLIC_CATALOGUE, V3_REGISTER, ARCHIVE_INDEX):
        if not required.exists():
            raise RuntimeError(f"missing dependency: {rel(required)}")
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != (1536, 1024):
        raise RuntimeError(f"unexpected source geometry: {source.size}")
    boundary = {
        "verticalBoundaryX520AlphaPixels": boundary_count(source, "x", SPLIT_X[0]),
        "verticalBoundaryX1028AlphaPixels": boundary_count(source, "x", SPLIT_X[1]),
        "horizontalBoundaryY512AlphaPixels": boundary_count(source, "y", SPLIT_Y),
    }
    empty_alpha = int((np.asarray(source.getchannel("A").crop((1028, 512, 1536, 1024))) > 8).sum())
    if any(boundary.values()) or empty_alpha:
        raise RuntimeError(f"source ownership failed: {boundary}, empty={empty_alpha}")

    COMPONENTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    records, paths, published = {}, {}, []
    for name, family, crop in NEW_CELLS:
        image, evidence = isolate(source, crop)
        path = COMPONENTS / f"{name}.png"
        image.save(path)
        if edge_alpha(image) or gutter(image) < 16:
            raise RuntimeError(f"unsafe component: {name}")
        digest = sha(path)
        public = ASSETS / f"{name}-{digest[:16]}.png"
        shutil.copyfile(path, public)
        records[name] = {**evidence, "file": rel(path), "sha256": digest, "family": family, "cellPixels": [CELL, CELL], "sourceSet": SET, "src": f"/keeper-review/{SET}/assets/{public.name}"}
        paths[name] = path
        published.append({"source": rel(path), "sourceSha256": digest, "public": rel(public), "publicAssemblyPath": rel(public), "publicSha256": sha(public), "url": records[name]["src"]})

    atlas = Image.new("RGBA", (CELL * len(paths), CELL), (0, 0, 0, 0))
    for index, name in enumerate(paths):
        atlas.alpha_composite(Image.open(paths[name]).convert("RGBA"), (index * CELL, 0))
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    atlas_path = EVIDENCE / "bbq-expansion-atlas.png"
    atlas.save(atlas_path)
    atlas_digest = sha(atlas_path)
    atlas_public = ASSETS / f"bbq-expansion-atlas-{atlas_digest[:16]}.png"
    shutil.copyfile(atlas_path, atlas_public)
    published.append({"source": rel(atlas_path), "sourceSha256": atlas_digest, "public": rel(atlas_public), "publicAssemblyPath": rel(atlas_public), "publicSha256": sha(atlas_public), "url": f"/keeper-review/{SET}/assets/{atlas_public.name}"})

    v3_public = json.loads(V3_PUBLIC_CATALOGUE.read_text())
    archive = json.loads(ARCHIVE_INDEX.read_text())
    inherited = {}
    for name, item in v3_public["callouts"]["components"].items():
        inherited[name] = {**item, "sha256": archive_hash_for_url(archive, item["src"])}
    new_public = {name: {key: value for key, value in record.items() if key in ("src", "cellPixels", "family", "sourceSet", "sha256")} for name, record in records.items()}
    all_components = {**inherited, **new_public}
    catalogue = {
        "schema": "lighthouse-keeper/activity-cloud-composer@1",
        "set": SET,
        "status": "immutable-reversible-review-tool-not-approved",
        "sourceVocabulary": {"set": v3_public["set"], "catalogue": rel(V3_PUBLIC_CATALOGUE), "catalogueSha256": sha(V3_PUBLIC_CATALOGUE), "register": rel(V3_REGISTER), "registerSha256": sha(V3_REGISTER), "inheritedComponents": len(inherited)},
        "body": v3_public["body"], "route": v3_public["route"], "reviewReferences": v3_public["reviewReferences"],
        "components": all_components,
        "composer": {"minimumElements": 4, "maximumElements": 5, "frames": 42, "fps": 8, "quietTailFrames": 5, "treatments": ["orbit", "bustle"], "localStorageKey": "lighthouse-keeper.activity-cloud-composer-v1", "exportSchema": "lighthouse-keeper/activity-cloud-recipe@1"},
        "defaultRecipe": {"label": "Garden BBQ", "targetAssetLabel": "Garden barbecue", "targetAssetId": "outdoor.bbq", "bodyCompatibility": "rear-work-with-context", "elements": ["bbq-sausages", "bbq-hotdogs", "bbq-burgers", "bbq-ketchup", "bbq-charcoal"], "sfx": "bbq-sizzle"},
    }
    public_catalogue = PUBLIC / "catalogue.json"
    write_json(public_catalogue, catalogue, compact=True)
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(build_page())

    register = {
        "schema": "lighthouse-keeper/activity-cloud-composer-register@1", "set": SET, "status": catalogue["status"],
        "sourceVocabulary": catalogue["sourceVocabulary"],
        "generatedSource": {"file": rel(SOURCE), "sha256": sha(SOURCE), "pixels": list(source.size), "selectedSplitX": list(SPLIT_X), "selectedSplitY": SPLIT_Y, **boundary, "emptySixthCellAlphaPixels": empty_alpha, "cells": [{"asset": name, "family": family, "crop": list(crop)} for name, family, crop in NEW_CELLS]},
        "newComponents": records,
        "catalogue": {"file": rel(public_catalogue), "sha256": sha(public_catalogue), "components": len(all_components), "newComponents": len(records)},
        "page": {"file": rel(PAGE), "sha256": sha(PAGE)},
        "candidate": {"publicShell": {"file": rel(PAGE), "sha256": sha(PAGE)}},
        "atlas": {"file": rel(atlas_path), "sha256": atlas_digest, "cellPixels": [CELL, CELL], "columns": len(paths), "rows": 1, "componentOrder": list(paths), "publishedUrl": f"/keeper-review/{SET}/assets/{atlas_public.name}"},
        "publishedAssets": published,
        "checks": {"sourceBoundariesClear": True, "emptySixthCellClear": True, "componentGuttersClear": True, "componentOwnershipUnambiguous": True, "v3VocabularyUnchanged": True, "primeBodyUnchanged": True, "runtimeChanged": False, "kitchenChanged": False, "deployed": False},
        "approvalBoundary": {"vocabularyApproved": False, "composerApproved": False, "recipeApproved": False, "runtimePromoted": False},
    }
    write_json(PACK / "batch-register.json", register)
    print(json.dumps({"set": SET, "components": len(all_components), "newComponents": len(records), "page": rel(PAGE)}, indent=2))


if __name__ == "__main__":
    main()
