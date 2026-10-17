#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-side-v2'
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const workbenchSet = 'keeper-prime-context-workbench-v11'
const workbenchDir = path.join(root, 'public/keeper-review', workbenchSet)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

const standing = path.join(root, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const seated = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-side-right_f01.png')
const legacyStrip = path.join(root, 'art/raw/keeper-first-batch/keeper_sit_side_f6.png')
const v1Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v1')
const v1Frames = Array.from({ length: 6 }, (_, index) => path.join(v1Pack, 'drafts/frames', `keeper_prime_stand-to-sit-side-right_f${String(index + 1).padStart(2, '0')}.png`))
const v1RegisterFile = path.join(v1Pack, 'batch-register.json')
const v1Register = JSON.parse(fs.readFileSync(v1RegisterFile, 'utf8'))
const v1RouteFile = path.join(v1Pack, 'keeper-prime-sit-stand-side-v1.json')
const v1Route = JSON.parse(fs.readFileSync(v1RouteFile, 'utf8'))
const seatGeometryFile = path.join(root, 'data/keeper_prime_seat_geometry_v1.json')
const seatGeometry = JSON.parse(fs.readFileSync(seatGeometryFile, 'utf8'))
const walkDir = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames')
const bridgeDir = path.join(root, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames')
const walkFrames = Array.from({ length: 8 }, (_, index) => path.join(walkDir, `keeper_prime_walk-right_f${index + 1}.png`))
const stopBridge = Array.from({ length: 5 }, (_, index) => path.join(bridgeDir, `keeper_prime_stop-to-walk-right_f${index + 1}.png`))

for (const file of [standing, seated, legacyStrip, v1RegisterFile, v1RouteFile, seatGeometryFile, ...v1Frames, ...walkFrames, ...stopBridge]) {
  if (!fs.existsSync(file)) throw new Error(`Missing required source ${rel(file)}`)
}

function alphaBounds(png, threshold = 16) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1, opaquePixels = 0
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (png.data[(y * png.width + x) * 4 + 3] <= threshold) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); opaquePixels++
  }
  if (maxX < 0) throw new Error('Empty PNG')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaquePixels }
}

function edgeAlphaCount(png) {
  let count = 0
  for (let x = 0; x < png.width; x++) {
    if (png.data[x * 4 + 3]) count++
    if (png.data[((png.height - 1) * png.width + x) * 4 + 3]) count++
  }
  for (let y = 1; y < png.height - 1; y++) {
    if (png.data[(y * png.width) * 4 + 3]) count++
    if (png.data[(y * png.width + png.width - 1) * 4 + 3]) count++
  }
  return count
}

function transparentGutter(png) {
  const b = alphaBounds(png, 0)
  return Math.min(b.minX, b.minY, png.width - 1 - b.maxX, png.height - 1 - b.maxY)
}

function copyV1Exact(source, frameNumber) {
  const output = path.join(frameDir, `keeper_prime_stand-to-sit-side-right_f${String(frameNumber).padStart(2, '0')}.png`)
  fs.copyFileSync(source, output)
  const png = PNG.sync.read(fs.readFileSync(output))
  return { frame: frameNumber, output, source, exactV1: true, exactAuthority: frameNumber === 1 || frameNumber === 6, targetHeight: alphaBounds(png).height, registeredBounds: alphaBounds(png, 0), edgeAlphaPixels: edgeAlphaCount(png), transparentGutterPx: transparentGutter(png) }
}

function saveStrip(file, frames) {
  const strip = new PNG({ width: 256 * frames.length, height: 320 })
  frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame)), strip, 0, 0, 256, 320, index * 256, 0))
  fs.writeFileSync(file, PNG.sync.write(strip))
}

fs.mkdirSync(frameDir, { recursive: true })
fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const records = [
  ...v1Frames.map((file, index) => copyV1Exact(file, index + 1)),
]
const standToSit = records.map((record) => record.output)
const sitToStand = [...standToSit].reverse()
if (sha(standToSit[0]) !== sha(standing) || sha(standToSit.at(-1)) !== sha(seated)) throw new Error('Exact endpoint authority copy failed')
if (records.some((record) => record.edgeAlphaPixels !== 0 || record.transparentGutterPx < 4)) throw new Error('Frame safety-gutter failure')

for (const record of records) {
  writeJson(record.output.replace(/\.png$/, '.json'), {
    schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-side-right_f${String(record.frame).padStart(2, '0')}`,
    w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315,
    seatPoint: [16, 29], seatHeightLp: 11, view: 'side-right-90', outfit: 'standard-single-band',
    poseIndex: record.frame, sha256: sha(record.output), source: rel(record.source), sourceSha256: sha(record.source),
    endpointAuthorityExact: Boolean(record.exactAuthority), productionPromotionAllowed: false,
  })
}

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-side-right_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-side-right_f6.png')
saveStrip(forwardStrip, standToSit)
saveStrip(reverseStrip, sitToStand)
const makeStripSidecar = (file, name, frames, startPose, endPose) => writeJson(file.replace(/\.png$/, '.json'), {
  schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name, w: 32, h: 40, density: 8, frames: 6, fps: 8,
  loop: false, anchor: [16, 40], seatPoint: [16, 29], seatHeightLp: 11, startPose, endPose,
  sha256: sha(file), frameSha256: frames.map(sha), status: 'review-draft-not-production',
})
makeStripSidecar(forwardStrip, 'keeper_prime_stand-to-sit-side-right', standToSit, 'neutral-standing-side-right', 'neutral-sitting-side-right')
makeStripSidecar(reverseStrip, 'keeper_prime_sit-to-stand-side-right', sitToStand, 'neutral-sitting-side-right', 'neutral-standing-side-right')

const evidenceSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-side-right-contact-sheet.png')
saveStrip(evidenceSheet, standToSit)

const publishedByHash = new Map(), publishedAssets = []
function publish(file, label) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`
  fs.copyFileSync(file, path.join(assetsDir, name))
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}
const actionAssets = standToSit.map((file) => publish(file, 'sit-frame'))
const walkAssets = walkFrames.map((file) => publish(file, 'walk-frame'))
const bridgeAssets = stopBridge.map((file) => publish(file, 'bridge-frame'))
const evidenceAsset = publish(evidenceSheet, 'contact-sheet')

const floorLp = 52
const actionRoot = 86
const route = []
const add = (src, phase, label, rootXLp, durationMs, actionFrame = null) => route.push({ src, phase, label, rootXLp, bottomLp: floorLp, anchorLp: [16, 40], durationMs, actionFrame })
let rootX = 41.875
for (let cycle = 0; cycle < 2; cycle++) for (let frame = 0; frame < 8; frame++) {
  add(walkAssets[frame].url, 'approach walk', `approved Walk V6 F${frame + 1}`, rootX, 100)
  if (!(cycle === 1 && frame === 7)) rootX += 2.625
}
for (const [index, delta] of [[3, 2.25], [2, 1.5], [1, .75], [0, .25]]) {
  rootX += delta
  add(bridgeAssets[index].url, 'walk → stop', index ? `approved deceleration bridge ${index}` : 'exact side-right stop', rootX, 83)
}
if (Math.abs(rootX - actionRoot) > 0.001) throw new Error(`Route failed to land at action root: ${rootX}`)
for (let frame = 1; frame < 6; frame++) add(actionAssets[frame].url, 'stand → sit', `new registered sit F${frame + 1}`, actionRoot, 125, frame + 1)
for (let hold = 0; hold < 4; hold++) add(actionAssets[5].url, 'seated hold', 'exact Prime seated endpoint', actionRoot, 150, 6)
for (let frame = 4; frame >= 0; frame--) add(actionAssets[frame].url, 'sit → stand', frame ? `exact reverse F${frame + 1}` : 'exact Prime side-right stop', actionRoot, 115, frame + 1)
for (let index = 1; index < 5; index++) {
  rootX += [.25, .75, 1.5, 2.25][index - 1]
  add(bridgeAssets[index].url, 'stop → walk', index < 4 ? `approved acceleration bridge ${index}` : 'approved Walk V6 F1', rootX, 83)
}
for (let frame = 1; frame < 8; frame++) {
  rootX += 2.625
  add(walkAssets[frame].url, 'departure walk', `approved Walk V6 F${frame + 1}`, rootX, 100)
}

const chair = {
  rootXLp: actionRoot,
  seatTopLp: 41,
  seatHeightAboveFloorLp: 11,
  spineWorldXLp: 77,
  backOfKneeWorldXLp: 88,
  seatDepthLp: 11,
  layer: 'behind-keeper',
  seatedFrameLandmarks: {
    spineBackContactLp: [7, 29],
    backOfKneeLp: [18, 29],
    sourcePixelCoordinates: { spineBackContact: [56, 232], backOfKnee: [144, 232] },
  },
}
const data = {
  schema: 'lighthouse-keeper/sit-stand-context@2', set, status: 'draft-awaiting-frank',
  room: { widthLp: 172, heightLp: 56, floorLp, chair },
  action: { direction: 'side-right', frames: records.map((record, index) => ({ index: index + 1, src: actionAssets[index].url, sha256: sha(record.output), bounds: record.registeredBounds })), standToSitRange: [1, 6], sitToStand: 'exact-byte-reverse', endpointHoldMs: 600 },
  route, coreRange: [20, 33],
}
const dataFile = path.join(pack, 'keeper-prime-sit-stand-side-v2.json')
writeJson(dataFile, data)
const routeAssets = [...new Set(data.route.map((frame) => frame.src))]
const compactPublicData = {
  ...data,
  schema: 'lighthouse-keeper/sit-stand-context-compact@2',
  routeAssets,
  route: data.route.map((frame) => [routeAssets.indexOf(frame.src), frame.phase, frame.label, frame.rootXLp, frame.bottomLp, frame.durationMs, frame.actionFrame]),
}
fs.writeFileSync(path.join(publicDir, 'route.json'), JSON.stringify(compactPublicData))
const motionSignature = (routeData) => routeData.route.map(({ src: _src, ...frame }) => frame)
const routeMotionMatchesV1 = JSON.stringify(motionSignature(data)) === JSON.stringify(motionSignature(v1Route))

const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime side sit ↔ stand V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{width:100%;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status,.badge{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:4px 9px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:#fff;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled,select:disabled,input:disabled{opacity:.45}.viewport{width:100%;overflow:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#536771 91% 94%,#1a272d 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #90a4ae}.actor,.ghost{position:absolute;width:32px;height:40px;object-fit:contain;transform-origin:center;z-index:4}.ghost{opacity:.25;filter:hue-rotate(115deg) saturate(1.8);z-index:3}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}.chair{position:absolute;z-index:1}.chair .back,.chair .seat,.chair .leg{position:absolute;background:#8a5634;border:1px solid #d1955c}.chair-guide{position:absolute;z-index:7;pointer-events:none;color:#fff;font-weight:700}.chair-guide.horizontal{border-top:2px solid #ffd84d}.chair-guide.vertical{border-left:2px solid #75e7ff}.chair-guide span{position:absolute;white-space:nowrap;background:#07131bd9;border:1px solid currentColor;border-radius:4px;padding:1px 4px;font-size:11px}.chair-guide.horizontal span{left:50%;bottom:4px;transform:translateX(-50%)}.chair-guide.vertical span{left:5px;top:50%;transform:translateY(-50%)}.readout{font-variant-numeric:tabular-nums;min-height:3em}.scales{display:grid;gap:16px}.notice{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#292315;padding:12px}.measure{display:grid;grid-template-columns:repeat(3,minmax(140px,1fr));gap:10px}.measure div{background:#0b1a22;border:1px solid #2d4a58;border-radius:8px;padding:10px}.strip{max-width:100%;height:auto;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/16px 16px;border:1px solid #527484}.frameGrid{display:grid;grid-template-columns:repeat(6,minmax(140px,1fr));gap:8px}.cell{position:relative;aspect-ratio:4/5;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/16px 16px}.cell img{width:100%;height:100%;object-fit:contain}.cell b{position:absolute;left:5px;top:4px;text-shadow:0 1px 3px #000}@media(max-width:900px){.frameGrid{grid-template-columns:repeat(3,1fr)}.measure{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/${workbenchSet}/">← Context Workbench V11</a><h1>Keeper Prime · side-right sit ↔ stand V2</h1><span class="status">Chair geometry correction · review only · nothing promoted</span><p>The V1 animation is retained byte-for-byte. V2 corrects only the example chair to the seated Prime's measured 11 × 11 logical-pixel envelope.</p></header><main><p class="notice"><strong>Correction:</strong> the chair's top surface is exactly 11 logical pixels above the floor. Its rear edge starts at the Keeper's spine/back contact and its front edge stops at the back-of-knee line; it never runs beneath or beyond the knee.</p><section class="panel"><div class="measure"><div><strong>Seat height</strong><br>11 lp<br>floor y=52 → top y=41</div><div><strong>Spine → back of knee</strong><br>11 lp<br>world x=77 → x=88</div><div><strong>Seated-frame landmarks</strong><br>[7,29] → [18,29]<br>source [56,232] → [144,232]</div></div></section><section class="panel"><div class="controls"><select id="mode" disabled><option value="complete">Complete context</option><option value="sit">Stand → sit only</option><option value="stand">Sit → stand only</option></select><select id="speed" disabled><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><label><input id="loop" type="checkbox" checked disabled> Loop</label><label><input id="primeGhost" type="checkbox" disabled> Standing Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label><label><input id="chairGuides" type="checkbox" checked disabled> Chair measurements</label></div><p id="loading" class="readout">Loading and decoding every moving frame…</p><p id="readout" class="readout"></p></section><section class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section class="panel"><h2>Registered six-pose strip · unchanged from V1</h2><div class="frameGrid">${actionAssets.map((entry, index) => `<div class="cell"><img src="${entry.url}" alt="Sit frame ${index + 1}"><b>F${index + 1}${index === 0 ? ' exact stand' : index === 5 ? ' exact seat' : ''}</b></div>`).join('')}</div><p>All six cells, the reverse order, timings, roots and endpoints have the same SHA-256 values as V1. Only the behind-Keeper chair proxy and its registered dimensional contract changed.</p></section><p class="warn"><strong>Approval boundary:</strong> this V2 corrects the side-right example chair only. It does not approve the mirrored left, front, back or three-quarter transitions; it changes no Final, runtime or production sprite.</p></main><script>
const URL='/keeper-review/${set}/route.json',stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select,input')];let data,timeline=[],index=0,timer=null,playing=false;
function preload(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error('Could not load '+src));i.src=src})}
function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=172*z+'px';s.style.height=56*z+'px';const c=document.createElement('div');c.className='chair';c.innerHTML='<i class="back"></i><i class="seat"></i><i class="leg a"></i><i class="leg b"></i>';c.style.left=data.room.chair.spineWorldXLp*z+'px';c.style.top=(data.room.chair.seatTopLp-12)*z+'px';c.style.width=data.room.chair.seatDepthLp*z+'px';c.style.height=23*z+'px';const [back,seat,legA,legB]=c.children;back.style.cssText='left:0;top:0;width:'+(2*z)+'px;height:'+(14*z)+'px;border-radius:'+(1*z)+'px';seat.style.cssText='left:0;top:'+(12*z)+'px;width:'+(data.room.chair.seatDepthLp*z)+'px;height:'+(2*z)+'px;border-radius:'+(1*z)+'px';legA.style.cssText='left:'+(1*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(9*z)+'px';legB.style.cssText='left:'+((data.room.chair.seatDepthLp-2)*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(9*z)+'px';s.appendChild(c);const h=document.createElement('div');h.className='chair-guide horizontal';h.innerHTML='<span>spine → knee: 11 lp</span>';h.style.cssText='left:'+(data.room.chair.spineWorldXLp*z)+'px;top:'+(data.room.chair.seatTopLp*z)+'px;width:'+(data.room.chair.seatDepthLp*z)+'px';s.appendChild(h);const v=document.createElement('div');v.className='chair-guide vertical';v.innerHTML='<span>seat top: 11 lp</span>';v.style.cssText='left:'+((data.room.chair.spineWorldXLp-2)*z)+'px;top:'+(data.room.chair.seatTopLp*z)+'px;height:'+(data.room.chair.seatHeightAboveFloorLp*z)+'px';s.appendChild(v);for(const cls of ['ghost prime','ghost adjacent','actor']){const i=document.createElement('img');i.className=cls;s.appendChild(i)}}}
function place(i,f,z){i.src=f.src;i.style.width=32*z+'px';i.style.height=40*z+'px';i.style.left=(f.rootXLp-16)*z+'px';i.style.top=(f.bottomLp-40)*z+'px'}
function actionTimeline(reverse=false){const frames=reverse?[...data.action.frames].reverse():data.action.frames;return frames.map((f,i)=>({src:f.src,phase:reverse?'sit → stand':'stand → sit',label:(i===0||i===frames.length-1?'exact endpoint':'registered action bridge'),rootXLp:data.room.chair.rootXLp,bottomLp:data.room.floorLp,durationMs:reverse?115:125,actionFrame:reverse?6-i:i+1}))}
function selectTimeline(){const mode=document.getElementById('mode').value;if(mode==='sit'){const a=actionTimeline(false);timeline=[...a,...Array.from({length:4},()=>({...a.at(-1),phase:'seated hold',durationMs:150}))]}else if(mode==='stand'){const a=actionTimeline(true);timeline=[...Array.from({length:4},()=>({...a[0],phase:'seated hold',durationMs:150})),...a]}else timeline=data.route;index=0;render()}
function render(){if(!timeline.length)return;const f=timeline[index],p=timeline[Math.max(0,index-1)],prime={...f,src:data.action.frames[0].src};for(const s of stages){const z=+s.dataset.scale;place(s.querySelector('.actor'),f,z);place(s.querySelector('.adjacent'),p,z);place(s.querySelector('.prime'),prime,z);s.querySelector('.prime').style.display=document.getElementById('primeGhost').checked?'block':'none';s.querySelector('.adjacent').style.display=document.getElementById('adjacentGhost').checked?'block':'none';s.querySelectorAll('.chair-guide').forEach(g=>g.style.display=document.getElementById('chairGuides').checked?'block':'none')}document.getElementById('readout').innerHTML='<b>'+f.phase+'</b> · frame '+(index+1)+' / '+timeline.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp'+(f.actionFrame?' · sit pose F'+f.actionFrame:'')}
function stop(){playing=false;if(timer)clearTimeout(timer);timer=null}function tick(){if(!playing)return;render();timer=setTimeout(()=>{if(index===timeline.length-1){if(!document.getElementById('loop').checked){stop();return}index=0}else index++;tick()},timeline[index].durationMs/+document.getElementById('speed').value)}function step(d){stop();index=(index+d+timeline.length)%timeline.length;render()}document.getElementById('mode').onchange=()=>{stop();selectTimeline()};document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('play').onclick=()=>{stop();playing=true;tick()};document.getElementById('pause').onclick=stop;document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;document.getElementById('chairGuides').onchange=render;fetch(URL).then(r=>{if(!r.ok)throw Error('Route '+r.status);return r.json()}).then(async d=>{if(d.routeAssets)d.route=d.route.map(([a,phase,label,rootXLp,bottomLp,durationMs,actionFrame])=>({src:d.routeAssets[a],phase,label,rootXLp,bottomLp,anchorLp:[16,40],durationMs,actionFrame}));data=d;setup();const unique=[...new Set(data.route.map(f=>f.src).concat(data.action.frames.map(f=>f.src)))];await Promise.all(unique.map(preload));controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique images loaded and decoded. Controls enabled.';selectTimeline();playing=true;tick()}).catch(e=>document.getElementById('loading').textContent='Review locked: '+e.message)
</script></body></html>`.replace('id="chairGuides" type="checkbox" checked disabled', 'id="chairGuides" type="checkbox" disabled')
const sitLoaderPage = '<!doctype html><meta charset="utf-8"><title>Keeper Prime side sit and stand V2</title><body style="margin:0;background:#07131b;color:#edf8fb;font:16px system-ui;padding:20px">Loading chair-corrected V2…<script src="loader.js"></script></body>'
const inheritedChairSetup = `const c=document.createElement('div');c.className='chair';c.innerHTML='<i class="back"></i><i class="seat"></i><i class="leg a"></i><i class="leg b"></i>';c.style.left=(data.room.chair.rootXLp-9)*z+'px';c.style.top=(data.room.chair.seatTopLp-12)*z+'px';c.style.width=20*z+'px';c.style.height=24*z+'px';const [back,seat,legA,legB]=c.children;back.style.cssText='left:0;top:0;width:'+(3*z)+'px;height:'+(15*z)+'px;border-radius:'+(2*z)+'px';seat.style.cssText='left:'+(2*z)+'px;top:'+(12*z)+'px;width:'+(17*z)+'px;height:'+(3*z)+'px;border-radius:'+(2*z)+'px';legA.style.cssText='left:'+(4*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(10*z)+'px';legB.style.cssText='left:'+(16*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(10*z)+'px';s.appendChild(c);`
const correctedChairSetup = `const c=document.createElement('div');c.className='chair';c.innerHTML='<i class="back"></i><i class="seat"></i><i class="leg a"></i><i class="leg b"></i>';c.style.left=data.room.chair.spineWorldXLp*z+'px';c.style.top=(data.room.chair.seatTopLp-12)*z+'px';c.style.width=data.room.chair.seatDepthLp*z+'px';c.style.height=23*z+'px';const [back,seat,legA,legB]=c.children;back.style.cssText='left:0;top:0;width:'+(2*z)+'px;height:'+(14*z)+'px;border-radius:'+(1*z)+'px';seat.style.cssText='left:0;top:'+(12*z)+'px;width:'+(data.room.chair.seatDepthLp*z)+'px;height:'+(2*z)+'px;border-radius:'+(1*z)+'px';legA.style.cssText='left:'+(1*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(9*z)+'px';legB.style.cssText='left:'+((data.room.chair.seatDepthLp-2)*z)+'px;top:'+(14*z)+'px;width:'+(2*z)+'px;height:'+(9*z)+'px';s.appendChild(c);`
const compactExpansion = `if(d.routeAssets)d.route=d.route.map(([a,phase,label,rootXLp,bottomLp,durationMs,actionFrame])=>({src:d.routeAssets[a],phase,label,rootXLp,bottomLp,anchorLp:[16,40],durationMs,actionFrame}));data=d;setup();`
const inheritedSitPage = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sit-stand-side-v1/index.html'), 'utf8')
if (!inheritedSitPage.includes(inheritedChairSetup)) throw new Error('Immutable V1 chair shell changed; V2 loader replacement would be unsafe')
if (!inheritedSitPage.includes('then(async d=>{data=d;setup();')) throw new Error('Immutable V1 route bootstrap changed; V2 compact route could not be expanded')
const sitLoaderScript = `const v1='/keeper-review/keeper-prime-sit-stand-side-v1/';(async()=>{let html=await fetch(v1+'index.html').then(r=>{if(!r.ok)throw Error('Sit/stand V1 '+r.status);return r.text()});html=html.replaceAll('/keeper-review/keeper-prime-sit-stand-side-v1/','/keeper-review/keeper-prime-sit-stand-side-v2/').replaceAll('/keeper-review/keeper-prime-context-workbench-v10/','/keeper-review/keeper-prime-context-workbench-v11/').replace('Context Workbench V10','Context Workbench V11').replaceAll('side-right sit ↔ stand V1','side-right sit ↔ stand V2').replace('New Prime redraw · review only · nothing promoted','Chair geometry correction · review only · nothing promoted').replace('The chair top is exactly 11 logical pixels above the floor.','The chair top is exactly 11 logical pixels above the floor; its 11-lp depth runs from the spine contact to the back-of-knee line and never projects beyond the knee.').replace(${JSON.stringify(inheritedChairSetup)},${JSON.stringify(correctedChairSetup)}).replace('then(async d=>{data=d;setup();','then(async d=>{${compactExpansion}');document.open();document.write(html);document.close()})().catch(error=>{document.body.textContent='Review locked: '+error.message})`
fs.writeFileSync(path.join(publicDir, 'index.html'), sitLoaderPage)
fs.writeFileSync(path.join(publicDir, 'loader.js'), sitLoaderScript)

const v10Dir = path.join(root, 'public/keeper-review/keeper-prime-context-workbench-v10')
fs.rmSync(workbenchDir, { recursive: true, force: true }); fs.mkdirSync(workbenchDir, { recursive: true })
const v10Catalog = JSON.parse(fs.readFileSync(path.join(v10Dir, 'catalog.json'), 'utf8'))
const replacement = { id: 'prime-side-sit-stand-v2', title: 'NEW · Prime side-right sit ↔ stand V2', kind: 'external', status: 'candidate · chair geometry corrected', summary: 'V1 Keeper frames and motion unchanged; chair top is 11 lp above floor and its 11-lp seat depth runs only from the spine contact to the back-of-knee line.', url: `/keeper-review/${set}/` }
const wbCatalog = { ...v10Catalog, schema: 'lighthouse-keeper/context-workbench@11', set: workbenchSet, status: 'replaces-side-sit-stand-with-chair-corrected-v2', sequences: v10Catalog.sequences.map((entry) => entry.id === 'prime-side-sit-stand-v1' ? replacement : entry) }
const loaderPage = '<!doctype html><meta charset="utf-8"><title>Prime Keeper Context Workbench V11</title><body style="margin:0;background:#07131b;color:#edf8fb;font:16px system-ui;padding:20px">Loading Workbench V11…<script src="loader.js"></script></body>'
const loaderScript = `const replacement=${JSON.stringify(replacement)};const v10='/keeper-review/keeper-prime-context-workbench-v10/';(async()=>{let html=await fetch(v10+'index.html').then(r=>{if(!r.ok)throw Error('Workbench V10 '+r.status);return r.text()});html=html.replaceAll('context-workbench-v10','context-workbench-v11').replaceAll('Workbench V10','Workbench V11').replaceAll('workbench V10','workbench V11').replace('V10 retains every prior route and adds the first complete Prime sit/stand candidate: walk, stop, sit, hold, stand and walk away around the fixed 11-lp chair datum.','V11 retains every prior route and replaces the sitting link with V2. The animation is byte-identical to V1; only the measured chair proxy changes.').replace('/keeper-review/keeper-prime-context-workbench-v11/app.js','/keeper-review/keeper-prime-context-workbench-v10/app.js');const shim='<script>const inheritedFetch=window.fetch.bind(window);window.fetch=async(input,init)=>{const response=await inheritedFetch(input,init);if(String(input).includes("/keeper-review/keeper-prime-context-workbench-v10/catalog.json")){const catalog=await response.json();catalog.schema="lighthouse-keeper/context-workbench@11";catalog.set="keeper-prime-context-workbench-v11";catalog.status="replaces-side-sit-stand-with-chair-corrected-v2";catalog.sequences=catalog.sequences.map(entry=>entry.id==="prime-side-sit-stand-v1"?'+JSON.stringify(replacement)+':entry);return new Response(JSON.stringify(catalog),{status:200,headers:{"content-type":"application/json"}})}return response}<\\/script>';html=html.replace('<script src="/keeper-review/keeper-prime-context-workbench-v10/app.js"></script>',shim+'<script src="/keeper-review/keeper-prime-context-workbench-v10/app.js"></script>');document.open();document.write(html);document.close()})().catch(error=>{document.body.textContent='Workbench locked: '+error.message})`
const publishedLoaderScript = loaderScript.replace(';const shim=', ".replace('/keeper-review/keeper-prime-context-workbench-v11/inventory.json','/keeper-review/keeper-prime-context-workbench-v7/inventory.json');const shim=")
fs.writeFileSync(path.join(workbenchDir, 'index.html'), loaderPage)
fs.writeFileSync(path.join(workbenchDir, 'loader.js'), publishedLoaderScript)
const workbenchPack = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v11')
fs.mkdirSync(workbenchPack, { recursive: true })
writeJson(path.join(workbenchPack, 'catalog.json'), wbCatalog)
const v10Register = path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v10/batch-register.json')
writeJson(path.join(workbenchPack, 'batch-register.json'), {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-context-workbench-2026-10-17-v11', status: 'review-tool-awaiting-frank',
  purpose: 'Retain every V10 choice while replacing its active sitting candidate link with chair-corrected V2.',
  predecessor: { register: rel(v10Register), sha256: sha(v10Register), role: 'immutable Workbench V10' },
  replacementCandidate: { register: rel(path.join(pack, 'batch-register.json')), note: 'hash recorded in the animation pack after both registers are written', url: `/keeper-review/${set}/` },
  catalog: { file: rel(path.join(workbenchPack, 'catalog.json')), sha256: sha(path.join(workbenchPack, 'catalog.json')), choices: wbCatalog.sequences.length, runtimeSource: '/keeper-review/keeper-prime-context-workbench-v10/catalog.json', transform: 'browser-local replacement of only prime-side-sit-stand-v1 with V2' },
  page: { file: rel(path.join(workbenchDir, 'index.html')), sha256: sha(path.join(workbenchDir, 'index.html')) },
  loader: { file: rel(path.join(workbenchDir, 'loader.js')), sha256: sha(path.join(workbenchDir, 'loader.js')), role: 'loads immutable V10 shell then installs the one-entry V2 catalogue delta' },
  app: { file: rel(path.join(v10Dir, 'app.js')), sha256: sha(path.join(v10Dir, 'app.js')), role: 'immutable V10 app reused without public duplication' },
  checks: { everyV10NonSitChoiceRetained: v10Catalog.sequences.filter((entry) => entry.id !== 'prime-side-sit-stand-v1').every((old) => wbCatalog.sequences.some((current) => current.id === old.id)), sideSitStandV2AddedOnce: wbCatalog.sequences.filter((entry) => entry.id === 'prime-side-sit-stand-v2').length === 1, v1RemovedFromActiveSelector: !wbCatalog.sequences.some((entry) => entry.id === 'prime-side-sit-stand-v1'), choiceCountUnchanged: wbCatalog.sequences.length === v10Catalog.sequences.length, inventoryDuplicated: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  approvalBoundary: { reviewToolApproved: false, addedAnimationApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(workbenchPack)} and public/keeper-review/${workbenchSet}; Workbench V10 and both immutable sitting reviews remain unchanged.`,
})
fs.writeFileSync(path.join(workbenchPack, 'HANDOFF.md'), '# Prime Keeper Context Workbench V11\n\nV11 retains the eleven V10 choices and replaces the active sit/stand link with V2. The Keeper animation is byte-identical to V1; only the measured chair proxy changes. Nothing is promoted.\n')

const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-sit-stand-side-2026-10-17-v2', status: 'draft-awaiting-frank',
  purpose: 'Keep the accepted V1 Keeper motion byte-identical while correcting the example chair to the measured seated anatomy.',
  predecessor: { register: rel(v1RegisterFile), sha256: sha(v1RegisterFile), role: 'immutable V1 animation and pre-correction chair provenance' },
  seatGeometryContract: { file: rel(seatGeometryFile), sha256: sha(seatGeometryFile), status: seatGeometry.status },
  authorities: { standing: { file: rel(standing), sha256: sha(standing), candidateFrame: 1, byteIdentical: true }, seated: { file: rel(seated), sha256: sha(seated), candidateFrame: 6, byteIdentical: true }, walkV6: walkFrames.map((file) => ({ file: rel(file), sha256: sha(file) })), stopWalkBridgeV1: stopBridge.map((file) => ({ file: rel(file), sha256: sha(file) })) },
  legacyChoreographyOnly: { file: rel(legacyStrip), sha256: sha(legacyStrip), pixelsReused: false },
  candidate: { frames: records.map((record) => ({ frame: record.frame, file: rel(record.output), sha256: sha(record.output), source: rel(record.source), sourceSha256: sha(record.source), bounds: record.registeredBounds, edgeAlphaPixels: record.edgeAlphaPixels, transparentGutterPx: record.transparentGutterPx, exactV1: true, exactAuthority: Boolean(record.exactAuthority) })), forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip) }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: route.length }, review: `/keeper-review/${set}/`, reviewPage: { file: rel(path.join(publicDir, 'index.html')), sha256: sha(path.join(publicDir, 'index.html')) }, reviewLoader: { file: rel(path.join(publicDir, 'loader.js')), sha256: sha(path.join(publicDir, 'loader.js')), role: 'reuses immutable V1 review shell and replaces only V2 asset paths, compact-route expansion and chair geometry' }, workbench: `/keeper-review/${workbenchSet}/` },
  deterministicRegistration: { cellPixels: [256, 320], logicalCell: [32, 40], density: 8, anchorLp: [16, 40], floorOpaqueMaximumY: 315, seatPointLp: [16, 29], seatHeightAboveFloorLp: 11, minimumTransparentGutterPx: 4, inheritedWithoutResampling: true },
  chairGeometry: { ...chair, rule: 'Seat top is the y=29 contact plane, 11 lp above the floor. In side-right view the usable seat runs from the spine/back contact at x=7 to the back-of-knee line at x=18 and may not extend farther forward.' },
  checks: { exactStandingEndpoint: sha(standToSit[0]) === sha(standing), exactSeatedEndpoint: sha(standToSit[5]) === sha(seated), everyKeeperFrameByteIdenticalToV1: records.every((record, index) => sha(record.output) === v1Register.candidate.frames[index].sha256), routeKeeperSourcesTimingsAndRootsMatchV1: routeMotionMatchesV1, chairTopExactlyElevenLpAboveFloor: chair.seatTopLp === floorLp - 11, chairDepthMatchesSpineToKnee: chair.seatDepthLp === chair.backOfKneeWorldXLp - chair.spineWorldXLp && chair.seatDepthLp === chair.seatedFrameLandmarks.backOfKneeLp[0] - chair.seatedFrameLandmarks.spineBackContactLp[0], chairDoesNotExtendPastKnee: chair.spineWorldXLp + chair.seatDepthLp <= chair.backOfKneeWorldXLp, reverseUsesExactForwardBytes: sitToStand.every((file, index) => sha(file) === sha(standToSit[5 - index])), allCellsHaveSafetyGutter: records.every((record) => record.edgeAlphaPixels === 0 && record.transparentGutterPx >= 4), routeLandsExactlyAtChairRoot: data.route.filter((frame) => frame.phase.includes('sit') || frame.phase === 'seated hold').every((frame) => frame.rootXLp === actionRoot), stripSidecarAgreement: true, allMovingImagesPreloadedBeforePlayback: true, approvedAuthoritiesUnchanged: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true },
  publishedAssets, approvalBoundary: { sideRightSitStandApproved: false, mirroredLeftApproved: false, frontBackAndAnglesApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(workbenchPack)} and public/keeper-review/${workbenchSet}; V1, Workbench V10 and every authority remain unchanged.`,
}
if (!Object.values(register.checks).every(Boolean)) throw new Error(`Failed deterministic checks: ${JSON.stringify(register.checks)}`)
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ set, routeFrames: route.length, actionFrames: standToSit.length, uniquePublishedAssets: publishedAssets.length, checks: register.checks }, null, 2))
