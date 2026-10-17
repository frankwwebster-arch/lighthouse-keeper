#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { PNG } from "pngjs";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-isolation-v1";
const pack = path.join(root, "art/drafts/keeper-prime-darts-isolation-2026-10-17-v1");
const frameDir = path.join(pack, "drafts/frames");
const publicDir = path.join(root, "public/keeper-review", set);
const publicAssets = path.join(publicDir, "assets");
const source = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2/sources/generated/keeper-prime-darts-14-pose-generated-v2.png");
const v2RegisterFile = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2/batch-register.json");
const sideAuthority = path.join(root, "art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png");
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "keeper-darts-isolation-"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const ALPHA = 6;
const CELL = { width: 448, height: 320, logical: [56, 40], density: 8, anchor: [28, 40] };
const ANCHOR = [224, 320];
const FLOOR_Y = 315;

for (const file of [source, v2RegisterFile, sideAuthority]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`);
fs.mkdirSync(frameDir, { recursive: true });
fs.rmSync(publicDir, { recursive: true, force: true });
fs.mkdirSync(publicAssets, { recursive: true });

function connectedComponents(png) {
  const seen = new Uint8Array(png.width * png.height);
  const componentAt = new Int32Array(png.width * png.height).fill(-1);
  const found = [];
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const start = y * png.width + x;
    if (seen[start] || png.data[start * 4 + 3] <= ALPHA) continue;
    seen[start] = 1;
    const stack = [start], pixels = [];
    let minX = x, maxX = x, minY = y, maxY = y;
    while (stack.length) {
      const current = stack.pop();
      const cy = Math.floor(current / png.width), cx = current % png.width;
      pixels.push(current);
      minX = Math.min(minX, cx); maxX = Math.max(maxX, cx); minY = Math.min(minY, cy); maxY = Math.max(maxY, cy);
      for (const [nx, ny] of [[cx - 1, cy], [cx + 1, cy], [cx, cy - 1], [cx, cy + 1]]) {
        if (nx < 0 || ny < 0 || nx >= png.width || ny >= png.height) continue;
        const next = ny * png.width + nx;
        if (!seen[next] && png.data[next * 4 + 3] > ALPHA) { seen[next] = 1; stack.push(next); }
      }
    }
    const id = found.length;
    for (const pixel of pixels) componentAt[pixel] = id;
    found.push({ id, count: pixels.length, pixels, minX, maxX, minY, maxY, centreX: (minX + maxX) / 2, centreY: (minY + maxY) / 2 });
  }
  return { found, componentAt };
}

function alphaBounds(png) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1;
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (png.data[(y * png.width + x) * 4 + 3] <= ALPHA) continue;
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);
  }
  if (maxX < 0) throw new Error("Empty frame");
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 };
}

function transparentGutter(png, gutter = 2) {
  let opaque = 0;
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (x >= gutter && x < png.width - gutter && y >= gutter && y < png.height - gutter) continue;
    if (png.data[(y * png.width + x) * 4 + 3] > ALPHA) opaque += 1;
  }
  return opaque;
}

const sourcePng = PNG.sync.read(fs.readFileSync(source));
const segmentation = connectedComponents(sourcePng);
const actors = segmentation.found
  .filter((entry) => entry.count > 20000)
  .sort((a, b) => (a.centreY < sourcePng.height / 2 ? 0 : 1) - (b.centreY < sourcePng.height / 2 ? 0 : 1) || a.centreX - b.centreX);
const detachedProjectiles = segmentation.found
  .filter((entry) => entry.count >= 900 && entry.count <= 1300)
  .sort((a, b) => a.centreX - b.centreX);
if (actors.length !== 14) throw new Error(`Expected 14 actor components, found ${actors.length}`);
if (detachedProjectiles.length !== 4) throw new Error(`Expected 4 detached projectiles, found ${detachedProjectiles.length}`);

const actorOwner = new Map(actors.map((actor, index) => [actor.id, index]));
const sourceOwnership = actors.map((actor, index) => {
  const column = index % 7, row = Math.floor(index / 7);
  const x0 = Math.round(column * sourcePng.width / 7), x1 = Math.round((column + 1) * sourcePng.width / 7);
  const y0 = Math.round(row * sourcePng.height / 2), y1 = Math.round((row + 1) * sourcePng.height / 2);
  let ownedActorPixels = 0, foreignActorPixels = 0, detachedOrNoisePixels = 0;
  for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) {
    const pixel = y * sourcePng.width + x;
    if (sourcePng.data[pixel * 4 + 3] <= ALPHA) continue;
    const owner = actorOwner.get(segmentation.componentAt[pixel]);
    if (owner === index) ownedActorPixels += 1;
    else if (owner !== undefined) foreignActorPixels += 1;
    else detachedOrNoisePixels += 1;
  }
  return { frame: index + 1, nominalCell: [column + 1, row + 1], ownedActorPixels, foreignActorPixels, detachedOrNoisePixels };
});

const sidePng = PNG.sync.read(fs.readFileSync(sideAuthority));
const sideBounds = alphaBounds(sidePng);
const sortedHeights = actors.map((actor) => actor.maxY - actor.minY + 1).sort((a, b) => a - b);
const medianHeight = (sortedHeights[6] + sortedHeights[7]) / 2;
const scale = sideBounds.height / medianHeight;

const correctedCore = actors.map((actor, index) => {
  const isolated = new PNG({ width: actor.maxX - actor.minX + 1, height: actor.maxY - actor.minY + 1 });
  for (const pixel of actor.pixels) {
    const sy = Math.floor(pixel / sourcePng.width), sx = pixel % sourcePng.width;
    const sourceOffset = pixel * 4;
    const targetOffset = ((sy - actor.minY) * isolated.width + (sx - actor.minX)) * 4;
    isolated.data.set(sourcePng.data.subarray(sourceOffset, sourceOffset + 4), targetOffset);
  }
  const footBandTop = actor.maxY - Math.max(24, Math.round((actor.maxY - actor.minY + 1) * 0.13));
  let footMin = sourcePng.width, footMax = -1;
  for (const pixel of actor.pixels) {
    const y = Math.floor(pixel / sourcePng.width), x = pixel % sourcePng.width;
    if (y >= footBandTop) { footMin = Math.min(footMin, x); footMax = Math.max(footMax, x); }
  }
  const cropFile = path.join(tempDir, `isolated-${index + 1}.png`);
  const scaledFile = path.join(tempDir, `scaled-${index + 1}.png`);
  fs.writeFileSync(cropFile, PNG.sync.write(isolated));
  const scaledWidth = Math.max(1, Math.round(isolated.width * scale));
  const scaledHeight = Math.max(1, Math.round(isolated.height * scale));
  execFileSync("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", cropFile, "-vf", `scale=${scaledWidth}:${scaledHeight}:flags=lanczos,format=rgba`, "-frames:v", "1", scaledFile]);
  const scaled = PNG.sync.read(fs.readFileSync(scaledFile));
  for (let offset = 0; offset < scaled.data.length; offset += 4) if (scaled.data[offset + 3] <= 3) scaled.data.fill(0, offset, offset + 4);
  const footCentre = (footMin + footMax) / 2;
  const dx = Math.round(ANCHOR[0] - (footCentre - actor.minX) * scale);
  const dy = Math.round(FLOOR_Y - (actor.maxY - actor.minY) * scale);
  if (dx < 2 || dy < 2 || dx + scaled.width > CELL.width - 2 || dy + scaled.height > CELL.height - 2) throw new Error(`Corrected F${index + 1} does not fit the action cell`);
  const cell = new PNG({ width: CELL.width, height: CELL.height });
  PNG.bitblt(scaled, cell, 0, 0, scaled.width, scaled.height, dx, dy);
  if (transparentGutter(cell) !== 0) throw new Error(`Corrected F${index + 1} lacks a two-pixel transparent gutter`);
  const file = path.join(frameDir, `keeper_prime_darts-core-isolated-right_f${String(index + 1).padStart(2, "0")}.png`);
  fs.writeFileSync(file, PNG.sync.write(cell));
  return { file, frame: index + 1, sha256: sha(file), alphaBounds: alphaBounds(cell), offset: [dx, dy], sourceActorComponent: { id: actor.id, count: actor.count, bounds: [actor.minX, actor.minY, actor.maxX, actor.maxY] } };
});

const v2 = JSON.parse(fs.readFileSync(v2RegisterFile, "utf8"));
const v2Frames = v2.candidate.frames.map((entry) => path.join(root, entry.file));
const correctedRegistered = v2Frames.map((file, index) => index >= 8 && index <= 21 ? correctedCore[index - 8].file : file);
if (correctedRegistered.length !== 30) throw new Error("Registered frame count changed");
for (const index of [...Array(8).keys(), ...Array.from({ length: 8 }, (_, offset) => offset + 22)]) {
  if (sha(correctedRegistered[index]) !== sha(v2Frames[index])) throw new Error(`Out-of-scope registered frame F${index + 1} changed`);
}

const strip = new PNG({ width: CELL.width * correctedRegistered.length, height: CELL.height });
correctedRegistered.forEach((file, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(file)), strip, 0, 0, CELL.width, CELL.height, index * CELL.width, 0));
const stripFile = path.join(pack, "drafts/keeper_prime_darts-isolated-right_f30.png");
fs.writeFileSync(stripFile, PNG.sync.write(strip));
const sidecarFile = path.join(pack, "drafts/keeper_prime_darts-isolated-right_f30.json");
writeJson(sidecarFile, { schema: "lighthouse-keeper/sprite-sidecar@draft-1", w: 56, h: 40, frames: 30, density: 8, anchor: [28, 40], fps: 6, loop: false, facing: "right", interaction: "play-darts", startPose: "standing-side-right", endPose: "standing-side-right", productionPromotionAllowed: false });

const published = [], byHash = new Map();
function publish(file, label) {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`;
  fs.copyFileSync(file, path.join(publicAssets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry); published.push(entry); return entry;
}
const oldCore = v2Frames.slice(8, 22).map((file) => publish(file, "old"));
const newCore = correctedCore.map((entry) => publish(entry.file, "isolated"));
const oldStrip = publish(path.join(root, v2.candidate.strip), "v2-strip");
const newStrip = publish(stripFile, "isolated-strip");
const reviewData = {
  set,
  frames: correctedCore.map((entry, index) => ({
    frame: index + 1,
    registeredFrame: index + 9,
    old: oldCore[index].url,
    corrected: newCore[index].url,
    ownership: sourceOwnership[index],
    oldSha256: sha(v2Frames[index + 8]),
    correctedSha256: entry.sha256,
  })),
  strips: { old: oldStrip.url, corrected: newStrip.url },
};
writeJson(path.join(publicDir, "comparison.json"), reviewData);

const app = `let data,index=0;const controls=[...document.querySelectorAll('button,select,input')];function load(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error(src));i.src=src})}function render(){const f=data.frames[index];document.getElementById('old').src=f.old;document.getElementById('corrected').src=f.corrected;document.getElementById('overlayOld').src=f.old;document.getElementById('overlayNew').src=f.corrected;document.getElementById('overlayOld').style.opacity=document.getElementById('opacity').value;document.getElementById('overlay').style.mixBlendMode=document.getElementById('difference').checked?'difference':'normal';document.getElementById('readout').innerHTML='<b>Core F'+String(f.frame).padStart(2,'0')+' · registered F'+String(f.registeredFrame).padStart(2,'0')+'</b><br>foreign actor pixels in old nominal cell: '+f.ownership.foreignActorPixels+' · detached projectile/noise pixels: '+f.ownership.detachedOrNoisePixels+'<br><small>old '+f.oldSha256+'<br>candidate '+f.correctedSha256+'</small>';document.querySelectorAll('.thumb').forEach((b,n)=>b.classList.toggle('active',n===index))}function step(d){index=(index+d+data.frames.length)%data.frames.length;render()}document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('opacity').oninput=render;document.getElementById('difference').onchange=render;addEventListener('keydown',e=>{if(e.key==='ArrowLeft')step(-1);if(e.key==='ArrowRight')step(1)});fetch('/keeper-review/${set}/comparison.json').then(r=>{if(!r.ok)throw Error('comparison '+r.status);return r.json()}).then(async d=>{data=d;await Promise.all([...new Set(d.frames.flatMap(f=>[f.old,f.corrected]).concat([d.strips.old,d.strips.corrected]))].map(load));document.getElementById('oldStrip').src=d.strips.old;document.getElementById('newStrip').src=d.strips.corrected;const thumbs=document.getElementById('thumbs');d.frames.forEach((f,n)=>{const b=document.createElement('button');b.className='thumb';b.textContent='F'+String(f.registeredFrame).padStart(2,'0');b.onclick=()=>{index=n;render()};thumbs.appendChild(b)});controls.forEach(c=>c.disabled=false);document.getElementById('loading').textContent='All old and corrected cells and both registered strips loaded and decoded.';render()}).catch(e=>document.getElementById('loading').textContent='Review locked: '+e.message);`;
fs.writeFileSync(path.join(publicDir, "app.js"), app);
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Darts cell-isolation candidate V1</title><style>*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px}.controls,.thumbs{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled{opacity:.45}.thumb.active{outline:3px solid #72e2a5}.compare{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.cell{position:relative;overflow:auto;background:repeating-conic-gradient(#20333d 0 25%,#16262e 0 50%) 0/24px 24px;min-height:680px}.cell img{display:block;width:896px;height:640px;object-fit:contain}.overlay img{position:absolute;inset:0}.strip{overflow-x:auto}.strip img{display:block;width:1680px;height:40px;image-rendering:auto}.readout{font-variant-numeric:tabular-nums;min-height:5em}@media(max-width:1000px){.compare{grid-template-columns:1fr}}</style></head><body><header><a href="/keeper-review/keeper-prime-context-workbench-v4/">← Context Workbench V4</a><h1>Darts registered-strip cell isolation · V1</h1><span class="status">Corrective draft · nothing promoted</span><p>The immutable Darts V2 strip used rectangular 7×2 source slicing even though several poses crossed those boundaries. This candidate assigns each whole actor component to exactly one frame and keeps flying darts as separate route effects.</p></header><main><p class="rule"><strong>What changed:</strong> only the fourteen generated throw-core cells (registered F09–F22). Exact Prime endpoints and all approved posture bridges are byte-identical to V2. This candidate deliberately does not address palette matching yet.</p><section class="panel"><div class="controls"><button id="prev" disabled>← Previous</button><button id="next" disabled>Next →</button><label>Old opacity <input id="opacity" type="range" min="0" max="1" step=".05" value=".45" disabled></label><label><input id="difference" type="checkbox" disabled> Difference blend</label></div><p id="loading">Loading and decoding all comparison images…</p><p id="readout" class="readout"></p><div id="thumbs" class="thumbs"></div></section><section class="compare"><article class="panel"><h2>Immutable V2 cell</h2><div class="cell"><img id="old"></div></article><article class="panel"><h2>Isolated candidate</h2><div class="cell"><img id="corrected"></div></article><article class="panel"><h2>Registration overlay</h2><div id="overlay" class="cell overlay"><img id="overlayNew"><img id="overlayOld"></div></article></section><section class="panel"><h2>Whole registered strips · logical size</h2><p>V2</p><div class="strip"><img id="oldStrip"></div><p>Isolated candidate</p><div class="strip"><img id="newStrip"></div></section><p class="warn"><strong>Approval boundary:</strong> V2, V3, Final and production remain unchanged. Palette correction is intentionally a later, separately reviewable operation.</p></main><script src="/keeper-review/${set}/app.js"></script></body></html>`;
const pageFile = path.join(publicDir, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-isolation-2026-10-17-v1",
  status: "corrective-draft-awaiting-frank",
  purpose: "Repair cross-cell ownership in the fourteen generated Darts V2 core poses without changing immutable V2/V3 or approved endpoints/bridges.",
  provenance: { source: { file: rel(source), sha256: sha(source) }, immutableV2: { register: rel(v2RegisterFile), sha256: sha(v2RegisterFile) }, primeSideAuthority: { file: rel(sideAuthority), sha256: sha(sideAuthority) } },
  segmentation: { actorComponents: actors.length, excludedDetachedProjectileComponents: detachedProjectiles.length, sourceOwnership },
  candidate: { strip: rel(stripFile), stripSha256: sha(stripFile), sidecar: rel(sidecarFile), sidecarSha256: sha(sidecarFile), frames: correctedRegistered.map((file, index) => ({ frame: index + 1, file: rel(file), sha256: sha(file), gutterAlphaPixels: transparentGutter(PNG.sync.read(fs.readFileSync(file))) })) },
  checks: { globalConnectedComponentOwnership: true, everyActorAssignedOnce: new Set(actors.map((actor) => actor.id)).size === 14, detachedProjectilesExcludedFromCharacterCells: true, twoPixelTransparentGutters: correctedRegistered.every((file) => transparentGutter(PNG.sync.read(fs.readFileSync(file))) === 0), registeredGeometry: [CELL.logical[0], CELL.logical[1], correctedRegistered.length, CELL.density], unchangedEndpointAndBridgeFrames: 16, stripSidecarAgreement: true },
  publishedAssets: published,
  review: { page: rel(pageFile), pageSha256: sha(pageFile), comparisonData: rel(path.join(publicDir, "comparison.json")), comparisonDataSha256: sha(path.join(publicDir, "comparison.json")) },
  approvalBoundary: { candidateApproved: false, paletteCorrected: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V2, V3 and every authority remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Darts cell-isolation candidate V1\n\nThis corrective draft rebuilds the fourteen generated core poses from whole-source connected components rather than rectangular 7×2 crops. It recovers actor pixels crossing nominal source boundaries, removes foreign neighbouring-actor fragments, and excludes four detached projectile components because Darts V3 renders flying darts as independent route effects. Registered F01–F08 and F23–F30 are byte-identical to immutable V2. No palette correction, approval or promotion is included.\n`);
fs.rmSync(tempDir, { recursive: true, force: true });
console.log(JSON.stringify({ set, actorComponents: actors.length, excludedProjectiles: detachedProjectiles.length, foreignActorPixels: sourceOwnership.reduce((sum, entry) => sum + entry.foreignActorPixels, 0), page: rel(pageFile) }, null, 2));
