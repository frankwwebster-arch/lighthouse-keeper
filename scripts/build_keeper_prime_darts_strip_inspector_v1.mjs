#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-strip-inspector-v1";
const pack = path.join(root, "art/drafts/keeper-prime-darts-strip-inspector-2026-10-17-v1");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const v2Pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2");
const v2RegisterFile = path.join(v2Pack, "batch-register.json");
const v2Register = JSON.parse(fs.readFileSync(v2RegisterFile, "utf8"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const frameFiles = v2Register.candidate.frames.map((entry) => path.join(root, entry.file));
const stripFile = path.join(root, v2Register.candidate.strip);
for (const file of [...frameFiles, stripFile]) if (!fs.existsSync(file)) throw new Error(`Missing V2 authority: ${rel(file)}`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });

const published = [];
const byHash = new Map();
function publish(file, label) {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`;
  fs.copyFileSync(file, path.join(assets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry);
  published.push(entry);
  return entry;
}

function rgbToHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), delta = max - min;
  let hue = 0;
  if (delta) {
    if (max === r) hue = 60 * (((g - b) / delta) % 6);
    else if (max === g) hue = 60 * ((b - r) / delta + 2);
    else hue = 60 * ((r - g) / delta + 4);
  }
  if (hue < 0) hue += 360;
  return [hue, max ? delta / max : 0, max];
}
function median(values) {
  values.sort((a, b) => a - b);
  return values[Math.floor(values.length / 2)];
}
function paletteMeasurements(file) {
  const png = PNG.sync.read(fs.readFileSync(file));
  if (png.width !== 448 || png.height !== 320) throw new Error(`${rel(file)} is not one 56×40 lp / 8× cell`);
  const groups = { blue: [[], [], []], navy: [[], [], []], cream: [[], [], []] };
  for (let offset = 0; offset < png.data.length; offset += 4) {
    const r = png.data[offset], g = png.data[offset + 1], b = png.data[offset + 2], alpha = png.data[offset + 3];
    if (alpha < 180) continue;
    const [hue, saturation, value] = rgbToHsv(r, g, b);
    let key;
    if (hue >= 195 && hue <= 235 && saturation > 0.5 && value > 0.28) key = "blue";
    else if (hue >= 210 && hue <= 250 && saturation > 0.15 && value >= 0.12 && value < 0.58) key = "navy";
    else if (r > 190 && g > 170 && b > 125 && r - g < 70 && g - b < 100) key = "cream";
    if (key) {
      groups[key][0].push(r); groups[key][1].push(g); groups[key][2].push(b);
    }
  }
  return Object.fromEntries(Object.entries(groups).map(([key, channels]) => [key, {
    medianRgb: channels[0].length ? channels.map(median) : null,
    classifiedPixels: channels[0].length,
  }]));
}

const primePalette = paletteMeasurements(frameFiles[0]);
const colourDistance = (current, authority) => Math.sqrt(current.reduce((sum, value, index) => sum + (value - authority[index]) ** 2, 0));
const frames = frameFiles.map((file, index) => {
  const palette = paletteMeasurements(file);
  const deltas = Object.fromEntries(Object.keys(palette).map((key) => [key, Number(colourDistance(palette[key].medianRgb, primePalette[key].medianRgb).toFixed(2))]));
  return {
    frame: index + 1,
    role: v2Register.candidate.frames[index].role,
    source: rel(file),
    sourceSha256: sha(file),
    url: publish(file, "frame").url,
    exactEndpoint: Boolean(v2Register.candidate.frames[index].exactEndpoint),
    palette,
    paletteDistanceFromPrime: deltas,
  };
});
const strip = publish(stripFile, "registered-strip");
const manifest = {
  schema: "lighthouse-keeper/darts-strip-inspector@1",
  set,
  status: "inspection-only-no-art-change",
  sourceStrip: { ...strip, logicalFrameSize: [56, 40], density: 8, frameCount: 30 },
  exactPrimeFrame: 1,
  primePalette,
  frames,
  colourMethod: "Median RGB among deterministic opaque-pixel classes: saturated uniform blue, dark blue/navy and warm cream. Values diagnose drift but do not define an approval threshold.",
};
const manifestFile = path.join(output, "manifest.json");
writeJson(manifestFile, manifest);

const app = `const MANIFEST_URL='/keeper-review/${set}/manifest.json';let data,index=8;const controls=[...document.querySelectorAll('button,select,input')],selected=document.getElementById('selected'),prime=document.getElementById('prime'),adjacent=document.getElementById('adjacent'),thumbs=document.getElementById('thumbs');function preload(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error('Could not load '+src));i.src=src})}function swatch(name,value,authority,delta){const rgb=value.medianRgb;return '<div class="swatch-card"><i style="background:rgb('+rgb.join(',')+')"></i><div><b>'+name+'</b><br>F'+String(index+1).padStart(2,'0')+' rgb('+rgb.join(', ')+')<br>Prime rgb('+authority.medianRgb.join(', ')+')<br><strong>distance '+delta.toFixed(2)+'</strong> · '+value.classifiedPixels.toLocaleString()+' px</div></div>'}function render(){const f=data.frames[index],prev=data.frames[Math.max(0,index-1)],zoom=+document.getElementById('zoom').value;for(const area of document.querySelectorAll('.detail')){area.style.width=448*zoom+'px';area.style.height=320*zoom+'px'}selected.src=f.url;prime.src=data.frames[0].url;adjacent.src=prev.url;selected.style.width=prime.style.width=adjacent.style.width=448*zoom+'px';selected.style.height=prime.style.height=adjacent.style.height=320*zoom+'px';prime.style.display=document.getElementById('primeGhost').checked?'block':'none';adjacent.style.display=document.getElementById('adjacentGhost').checked?'block':'none';prime.style.opacity=document.getElementById('primeOpacity').value/100;adjacent.style.opacity=document.getElementById('adjacentOpacity').value/100;prime.style.mixBlendMode=document.getElementById('difference').checked?'difference':'normal';document.getElementById('identity').innerHTML='<b>Frame '+String(f.frame).padStart(2,'0')+' / 30</b> · '+f.role+'<br><code>'+f.sourceSha256+'</code>';document.getElementById('palette').innerHTML=Object.keys(f.palette).map(k=>swatch(k,f.palette[k],data.primePalette[k],f.paletteDistanceFromPrime[k])).join('');document.querySelectorAll('.thumb').forEach((b,n)=>b.classList.toggle('active',n===index));document.getElementById('selectedTitle').textContent='Selected F'+String(f.frame).padStart(2,'0')+(f.exactEndpoint?' · exact Prime endpoint':'');document.getElementById('adjacentLabel').textContent=index?'Previous frame F'+String(index).padStart(2,'0'):'Previous frame · same endpoint'}function choose(n){index=Math.max(0,Math.min(data.frames.length-1,n));render()}function buildThumbs(){for(const [n,f] of data.frames.entries()){const b=document.createElement('button');b.className='thumb';b.innerHTML='<img src="'+f.url+'"><span>F'+String(f.frame).padStart(2,'0')+'</span><small>'+f.role.replace('new registered darts core','throw core').replace('approved Prime posture bridge','posture bridge')+'</small>';b.onclick=()=>choose(n);thumbs.appendChild(b)}}document.getElementById('prev').onclick=()=>choose(index-1);document.getElementById('next').onclick=()=>choose(index+1);for(const id of ['zoom','primeGhost','adjacentGhost','primeOpacity','adjacentOpacity','difference'])document.getElementById(id).oninput=render;document.onkeydown=e=>{if(e.key==='ArrowLeft')choose(index-1);if(e.key==='ArrowRight')choose(index+1)};fetch(MANIFEST_URL).then(r=>{if(!r.ok)throw new Error('Manifest '+r.status);return r.json()}).then(async m=>{data=m;document.getElementById('strip').src=m.sourceStrip.url;buildThumbs();await Promise.all([...new Set(m.frames.map(f=>f.url).concat(m.sourceStrip.url))].map(preload));controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All 30 registered cells and the exact V2 strip loaded and decoded.';render()}).catch(e=>document.getElementById('loading').textContent='Inspector locked: '+e.message);`;
fs.writeFileSync(path.join(output, "app.js"), app);

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Darts V2 registered-strip inspector</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1800px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.notice{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.controls{display:flex;gap:9px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled,select:disabled,input:disabled{opacity:.45}.viewport{overflow:auto;max-height:900px;background:#061016;border-radius:8px;padding:12px}.checker{background-color:#16252c;background-image:linear-gradient(45deg,#223943 25%,transparent 25%),linear-gradient(-45deg,#223943 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#223943 75%),linear-gradient(-45deg,transparent 75%,#223943 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.detail{position:relative;border:1px solid #78a5b8;transform-origin:top left}.detail img{position:absolute;inset:0;object-fit:contain;image-rendering:auto}.selected{z-index:3}.prime{z-index:4;filter:hue-rotate(95deg) saturate(1.7)}.adjacent{z-index:2;filter:hue-rotate(285deg) saturate(1.8)}.compare{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}.side img{display:block;width:448px;height:320px;max-width:100%;object-fit:contain}.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(116px,1fr));gap:8px}.thumb{display:grid;grid-template-rows:80px auto auto;padding:6px;text-align:left}.thumb img{width:100%;height:80px;object-fit:contain;background:#07131b}.thumb span{font-weight:800}.thumb small{color:#b6cbd4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.thumb.active{outline:3px solid #72e2a5;background:#20516a}.palette{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.swatch-card{display:flex;gap:10px;background:#0a1a22;border-radius:9px;padding:10px}.swatch-card i{width:64px;min-width:64px;height:64px;border:1px solid #9cb4bd;border-radius:7px}.swatch-card strong{color:#ffe09d}.strip-wrap{overflow-x:auto;background:#061016;padding:10px}.strip{display:block;width:1680px;height:40px;object-fit:fill}.readout{font-variant-numeric:tabular-nums;overflow-wrap:anywhere}code{font-size:12px;color:#bcd2db}@media(max-width:900px){.compare,.palette{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-context-workbench-v3/">← Context Workbench V3</a><h1>Darts V2 registered-strip inspector</h1><span class="status">Inspection only · no pixels changed</span><p>Every one of the 30 inherited V2 registered cells is selectable at exact source resolution and enlarged inspection scales.</p></header><main><p class="notice"><strong>Use this page for colour review:</strong> F01/F30 are the byte-identical Prime side endpoint; F02–F08 and F23–F29 are the approved posture bridge; F09–F22 are the generated throw core. The palette measurements make likely drift visible but do not automatically approve or reject a frame.</p><section class="panel"><div class="controls"><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><select id="zoom" disabled><option value="1">Exact source pixels · 448×320</option><option value="1.5">1.5× source</option><option value="2" selected>2× source · 896×640</option><option value="3">3× source</option></select><label><input id="primeGhost" type="checkbox" disabled> Prime overlay</label><label>Prime opacity <input id="primeOpacity" type="range" min="5" max="95" value="35" disabled></label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame overlay</label><label>Adjacent opacity <input id="adjacentOpacity" type="range" min="5" max="95" value="30" disabled></label><label><input id="difference" type="checkbox" disabled> Difference blend</label></div><p id="loading" class="readout">Loading and decoding all registered cells…</p><p id="identity" class="readout"></p></section><section class="panel"><h2 id="selectedTitle">Selected frame</h2><div class="viewport"><div class="detail checker"><img id="adjacent" class="adjacent"><img id="selected" class="selected"><img id="prime" class="prime"></div></div><p id="adjacentLabel"></p></section><section class="panel"><h2>Selected beside exact Prime endpoint</h2><div class="compare"><div class="side checker"><h3>Selected</h3><img id="selectedSide" alt="Use the main enlarged inspector above"></div><div class="side checker"><h3>Exact Prime F01</h3><img src="${frames[0].url}"></div></div><p>The enlarged overlay above is the authoritative comparison. The fixed endpoint panel remains visible while stepping.</p></section><section class="panel"><h2>Deterministic colour classes</h2><div id="palette" class="palette"></div><p>Distance is Euclidean RGB distance from F01's median in that same class. A larger value is a review flag, not proof of an incorrect colour.</p></section><section class="panel"><h2>All 30 frames</h2><div id="thumbs" class="thumbs"></div></section><section class="panel"><h2>Whole registered V2 strip · one CSS pixel per logical pixel</h2><div class="strip-wrap"><img id="strip" class="strip"></div></section><p class="notice"><strong>Approval boundary:</strong> this inspector does not redraw, correct, approve or promote any frame. Any palette correction must be made later as a new versioned candidate with masks and out-of-scope pixel checks.</p></main><script src="/keeper-review/${set}/app.js"></script><script>document.addEventListener('DOMContentLoaded',()=>{const main=document.getElementById('selected'),side=document.getElementById('selectedSide');new MutationObserver(()=>side.src=main.src).observe(main,{attributes:true,attributeFilter:['src']})})</script></body></html>`;
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-strip-inspector-2026-10-17-v1",
  status: "inspection-only-no-art-change",
  purpose: "Frame-by-frame exact-pixel and deterministic palette inspection of the immutable Darts V2 registered strip.",
  authority: { register: rel(v2RegisterFile), sha256: sha(v2RegisterFile), strip: rel(stripFile), stripSha256: sha(stripFile) },
  manifest: { file: rel(manifestFile), sha256: sha(manifestFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  checks: { frameCount: frames.length, exactCellPx: [448, 320], exactLogicalCell: [56, 40], density: 8, sourceHashesMatchV2: frames.every((frame, index) => frame.sourceSha256 === v2Register.candidate.frames[index].sha256), paletteClasses: ["blue", "navy", "cream"], artPixelsChanged: false },
  publishedAssets: published,
  approvalBoundary: { candidateApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Darts V2/V3 and all authorities remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Darts V2 registered-strip inspector V1\n\nInspection-only evidence for all 30 immutable V2 cells. It adds exact-source zoom, stepping, Prime/adjacent overlays, difference blending, thumbnails, the complete strip and deterministic blue/navy/cream median measurements. It changes no art or approval.\n`);
console.log(JSON.stringify({ set, frames: frames.length, uniqueAssets: published.length, page: rel(pageFile) }, null, 2));
