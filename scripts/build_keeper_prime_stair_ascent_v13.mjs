#!/usr/bin/env node
/** Build V13: exact V12 contacts with one neutral passing frame per leg. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v13'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v13')
const v12 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v12')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v13.json')
const v12PrepPath = path.join(v12, 'source-preparation-v12.json')
const v12RegisterPath = path.join(v12, 'batch-register.json')
const v12RigPath = path.join(v12, 'stair-contact-rig-v12.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v12PrepPath, v12RegisterPath, v12RigPath, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
const contacts = JSON.parse(fs.readFileSync(v12PrepPath, 'utf8'))
const v12Rig = JSON.parse(fs.readFileSync(v12RigPath, 'utf8'))
const geometry = { ...v12Rig.geometry, shownContacts: 3, framesPerStep: 2, frameDurationMs: 110 }
fs.rmSync(assetsDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const urls = { contact: {}, mid: {} }
const assetRecords = []
function addAsset(sourceFile, stem) {
  const target = path.join(assetsDir, `${stem}-${sha(sourceFile).slice(0, 16)}.png`)
  fs.copyFileSync(sourceFile, target)
  const url = `/keeper-review/${set}/assets/${path.basename(target)}`
  assetRecords.push({ source: rel(sourceFile), sourceSha256: sha(sourceFile), url })
  return url
}
for (const frame of contacts.frames) urls.contact[frame.leg] = addAsset(path.join(root, frame.draft.file), `${frame.leg}-contact`)
for (const frame of prep.frames) urls.mid[frame.movingLeg] = addAsset(path.join(root, frame.draft.file), `${frame.movingLeg}-foot-mid-swing`)

const contactByLeg = Object.fromEntries(contacts.frames.map((frame) => [frame.leg, frame]))
const midByLeg = Object.fromEntries(prep.frames.map((frame) => [frame.movingLeg, frame]))
const supportAt = (tread) => ({
  x: geometry.floorSupportCentreLp - tread * geometry.treadRunLp,
  y: geometry.floorTopLp + tread * geometry.riserRiseLp,
})
function place(source, supportTread) {
  const support = supportAt(supportTread)
  return {
    xLp: support.x - source.supportSole.centreX / 8 + 16,
    bottomLp: support.y - (320 - source.supportSole.y) / 8,
    supportXLp: support.x,
    supportYLp: support.y,
  }
}
function contactFrame(leg, supportTread, frame) {
  const source = contactByLeg[leg]
  const placed = place(source, supportTread)
  const target = supportAt(supportTread + 1)
  const movingXLp = placed.xLp - 16 + source.movingSole.centreX / 8
  const movingYLp = placed.bottomLp + (320 - source.movingSole.y) / 8
  return {
    frame, kind: 'contact', leg, movingLeg: leg,
    label: `${leg.toUpperCase()} foot planted on next tread · opposite arm at full counter-position`,
    src: urls.contact[leg], supportTread, targetTread: supportTread + 1,
    ...placed, targetXLp: target.x, targetYLp: target.y, movingXLp, movingYLp,
    supportClearanceLp: 0, movingClearanceLp: movingYLp - target.y, durationMs: geometry.frameDurationMs,
  }
}
function midFrame(movingLeg, supportTread, frame) {
  const source = midByLeg[movingLeg]
  const placed = place(source, supportTread)
  const target = supportAt(supportTread + 1)
  return {
    frame, kind: 'mid-swing', leg: movingLeg, movingLeg,
    label: `${movingLeg.toUpperCase()} foot passing forward · planted ${source.supportLeg.toUpperCase()} boot locked · arms passing neutral`,
    src: urls.mid[movingLeg], supportTread, targetTread: supportTread + 1,
    ...placed, targetXLp: target.x, targetYLp: target.y,
    supportClearanceLp: 0, durationMs: geometry.frameDurationMs,
  }
}
const timeline = [
  contactFrame('left', 0, 1),
  midFrame('right', 1, 2),
  contactFrame('right', 1, 3),
  midFrame('left', 2, 4),
  contactFrame('left', 2, 5),
]

const rigPath = path.join(pack, 'stair-contact-rig-v13.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@13', status: 'one-mid-swing-per-leg-awaiting-review',
  direction: 'leftward gameplay', cell: [256, 320], density: 8, geometry,
  sequence: ['LEFT contact', 'RIGHT mid-swing', 'RIGHT contact', 'LEFT mid-swing', 'LEFT contact'],
  timeline,
  contract: [
    'Both V12 contact drawings are byte-identical endpoints.',
    'Each half-cycle adds exactly one byte-identical V6 passing drawing.',
    'The planted support sole is registered to the same mathematical tread before and after each passing frame.',
    'Arms travel from one V12 counter-position through the neutral V6 passing pose to the opposite V12 counter-position.',
    'The 14-riser, 7-lp-tread, 98 × 60-lp V12 flight geometry is unchanged.',
  ],
})

const stairs = Array.from({ length: geometry.risers }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.stairBaseRightLp - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const cards = timeline.slice(0, 4).map((frame) => `<div class="pose ${frame.kind}"><img src="${frame.src}" alt="${frame.label}"><b>F${frame.frame} · ${frame.kind === 'contact' ? 'CONTACT' : 'PASSING'}</b><span>${frame.label}</span></div>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V13</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1280px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left top}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:${geometry.stairBaseRightLp * 4}px;right:0;bottom:0;height:${geometry.floorTopLp * 4}px;background:#526675;border-top:3px solid #d0dee6}.landing{position:absolute;left:0;bottom:${geometry.floorTopLp * 4}px;width:${(geometry.stairBaseRightLp-geometry.flightRunLp)*4}px;height:${geometry.flightRiseLp*4}px;background:#526675;border-top:3px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.line{position:absolute;height:3px;width:28px;z-index:8;display:none}.showContacts .line{display:block}.support{background:#55ff9b}.target{background:#ffe06a}.poses{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:12px}.pose{background:#0c1d26;padding:10px;border-bottom:5px solid #ffbd72}.pose.mid-swing{border-color:#75e6a7}.pose img{display:block;width:min(100%,256px);margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.pose b,.pose span{display:block;text-align:center}.pose span{color:#b8d0da;font-size:12px}.legend{display:flex;gap:18px;flex-wrap:wrap}.swatch{display:inline-block;width:14px;height:4px;vertical-align:middle;margin-right:5px}.green{background:#55ff9b}.gold{background:#ffe06a}@media(max-width:900px){.views{grid-template-columns:1fr}.poses{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v12/">← Approved geometry/contact foundation V12</a><h1>Keeper Prime stair ascent V13 · one passing frame per leg</h1><span class="status">New reversible smoothing candidate · nothing promoted</span><p><strong>LEFT contact → RIGHT foot passes → RIGHT contact → LEFT foot passes → LEFT contact.</strong></p></header><main><p class="rule"><strong>Judge the motion:</strong> each foot now travels to the next tread over two frame intervals instead of teleporting in one. The planted boot stays on its tread. Arms move from one opposing extreme, through the neutral passing pose, to the opposite extreme.</p><article><div class="controls"><button id="play" disabled>Play once</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label>Frame speed <input id="speed" type="range" min="70" max="220" step="5" value="110"> <output id="speedValue">110 ms</output></label><label><input id="contacts" type="checkbox" checked> Contact lines</label></div><p id="loading" class="readout">Loading and decoding all four unique drawings…</p><p id="readout" class="readout"></p><p class="legend"><span><i class="swatch green"></i>planted support tread</span><span><i class="swatch gold"></i>next target tread</span></p></article><article><div class="views"><div><h2>Large inspection</h2><div class="stageWrap"><div class="stage large showContacts"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Keeper stair passing sequence"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game showContacts"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Exact-scale stair passing sequence"></div></div></div></div></article><h2>The four unique drawings</h2><section class="poses">${cards}</section><article><h2>Boundary</h2><p>V12's two contact drawings and complete stair geometry remain exact. V13 adds only two exact same-family passing drawings. The generated midpoint studies are retained as rejected provenance and contribute no candidate pixel. Final, runtime and production remain unchanged.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[document.querySelector('.large'),document.querySelector('.game')];let index=0,timer=null,hold=110;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const el of stages){const img=el.querySelector('.walker'),support=el.querySelector('.support'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*4)+'px';img.style.bottom=(f.bottomLp*4)+'px';support.style.left=((f.supportXLp-3.5)*4)+'px';support.style.bottom=(f.supportYLp*4)+'px';target.style.left=((f.targetXLp-3.5)*4)+'px';target.style.bottom=(f.targetYLp*4)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/5 · '+f.label+' · support tread '+f.supportTread+' → target '+f.targetTread}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index>=timeline.length-1)return stop();index++;render();timer=setTimeout(tick,hold)}function play(){stop();if(index>=timeline.length-1)index=0;render();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(timeline.length-1,index+1);render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('speed').oninput=e=>{hold=Number(e.target.value);document.getElementById('speedValue').value=hold+' ms';if(timer)play()};document.getElementById('contacts').onchange=e=>stages.forEach(el=>el.classList.toggle('showContacts',e.target.checked));Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All four unique drawings decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A drawing failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(pack, 'keeper-prime-stair-ascent-v13.json')
const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@13', status: 'draft-v13-one-passing-frame-per-leg-awaiting-review',
  approvalBasis: 'Frank accepted V12 geometry/contact foundation with “yes you’ve got it”.',
  scope: 'Two-step smoothing proof with exactly one passing drawing per leg.', geometry, promoted: false,
  unchanged: { v12ContactsByteIdentical: true, v12GeometryExact: true, finalLane: true, runtimeSprites: true, production: true },
}
writeJson(specPath, spec)
const frameUrls = [...new Set(assetRecords.map((entry) => entry.url))]
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v13', status: spec.status,
  authorities: { approvedV12ContactGate: { file: rel(v12RegisterPath), sha256: sha(v12RegisterPath) }, sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) }, contactRig: { file: rel(rigPath), sha256: sha(rigPath) } },
  generation: { mode: 'exact-v12-contact-reuse-plus-exact-v6-passing-drawings; generated studies rejected', frameUrls },
  assets: assetRecords,
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { uniqueDrawings: 4, shownFrames: 5, passingFramesPerLeg: 1, framesPerStep: 2, v12ContactsByteIdentical: true, v6PassingFramesByteIdentical: true, supportContactRequiredEveryFrame: true, v12GeometryExact: true, edgeAlphaZero: true, priorDraftsChanged: false, finalChanged: false, runtimeSpritesChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, uniqueDrawings: frameUrls.length, geometry }, null, 2))
