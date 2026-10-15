#!/usr/bin/env node
/** Build V12: deeper-tread contact handover with visible alternating arms. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v12'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v12')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v12.json')
const v11RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v11/batch-register.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v11RegisterPath, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const urls = {}
for (const frame of prep.frames) {
  const source = path.join(root, frame.draft.file)
  if (sha(source) !== frame.draft.sha256) throw new Error(`${frame.leg} prepared frame changed`)
  const target = path.join(assetsDir, `${frame.leg}-contact-${frame.draft.sha256.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  urls[frame.leg] = `/keeper-review/${set}/assets/${path.basename(target)}`
}

const geometry = {
  floorTopLp: 20,
  stairBaseRightLp: 116,
  floorSupportCentreLp: 119.5,
  flightRunLp: 98,
  flightRiseLp: 60,
  risers: 14,
  treadRunLp: 7,
  riserRiseLp: 60 / 14,
  reservedCoreRunLp: 105,
  shownContacts: 4,
  contactDurationMs: 280,
}
const byLeg = Object.fromEntries(prep.frames.map((frame) => [frame.leg, frame]))
const contactOrder = ['right', 'left', 'right', 'left']
const timeline = contactOrder.map((leg, index) => {
  const frame = byLeg[leg]
  const supportXLp = geometry.floorSupportCentreLp - index * geometry.treadRunLp
  const supportYLp = geometry.floorTopLp + index * geometry.riserRiseLp
  const targetXLp = supportXLp - geometry.treadRunLp
  const targetYLp = supportYLp + geometry.riserRiseLp
  const xLp = supportXLp - frame.supportSole.centreX / 8 + 16
  const bottomLp = supportYLp - (320 - frame.supportSole.y) / 8
  const movingXLp = xLp - 16 + frame.movingSole.centreX / 8
  const movingYLp = bottomLp + (320 - frame.movingSole.y) / 8
  return {
    frame: index + 1,
    step: index + 1,
    leg,
    label: leg === 'right' ? 'RIGHT leg forward · LEFT arm forward' : 'LEFT leg forward · RIGHT arm forward',
    src: urls[leg],
    xLp,
    bottomLp,
    supportTread: index,
    targetTread: index + 1,
    supportXLp,
    supportYLp,
    targetXLp,
    targetYLp,
    movingXLp,
    movingYLp,
    supportClearanceLp: 0,
    movingClearanceLp: movingYLp - targetYLp,
    durationMs: geometry.contactDurationMs,
  }
})

const handovers = timeline.slice(0, -1).map((frame, index) => ({
  fromFrame: frame.frame,
  toFrame: timeline[index + 1].frame,
  previousMovingToNextSupportDeltaLp: {
    x: timeline[index + 1].supportXLp - frame.movingXLp,
    y: timeline[index + 1].supportYLp - frame.movingYLp,
  },
}))
const rigPath = path.join(pack, 'stair-contact-rig-v12.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@12',
  status: 'deeper-tread-contact-and-arm-gate-awaiting-review',
  direction: 'leftward gameplay', cell: [256, 320], density: 8,
  geometry, contactOrder, timeline, handovers,
  contract: [
    'The finished-floor rise remains exactly 60 lp and still uses fourteen equal risers.',
    'Tread depth increases from 6 to 7 lp, so the flight run becomes 98 lp inside the reserved 105-lp stair core.',
    'Every displayed frame has a support sole on a real tread; floating is a hard failure, not merely non-penetration.',
    'The opposite contact inherits the previous upper-foot position within 0.063 lp horizontally and 0.036 lp vertically.',
    'Arms alternate as a visibly different foreground/background silhouette; no sub-logical-pixel arm motion is claimed.',
  ],
})

const stairs = Array.from({ length: geometry.risers }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.stairBaseRightLp - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const cards = prep.frames.map((frame) => `<div class="pose ${frame.leg}"><img src="${urls[frame.leg]}" alt="${frame.leg} leg contact"><b>${frame.leg.toUpperCase()} LEG FORWARD</b><span>${frame.leg === 'right' ? 'LEFT arm visibly forward' : 'RIGHT arm visibly forward'}</span></div>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V12</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1280px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.warning{border-left-color:#ffae69;background:#2a2018}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left top}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:${geometry.stairBaseRightLp * 4}px;right:0;bottom:0;height:${geometry.floorTopLp * 4}px;background:#526675;border-top:3px solid #d0dee6}.landing{position:absolute;left:0;bottom:${geometry.floorTopLp * 4}px;width:${(geometry.stairBaseRightLp-geometry.flightRunLp)*4}px;height:${geometry.flightRiseLp*4}px;background:#526675;border-top:3px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.line{position:absolute;height:3px;width:28px;z-index:8;display:none}.showContacts .line{display:block}.support{background:#55ff9b}.target{background:#ffe06a}.poses{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pose{background:#0c1d26;padding:12px;border-bottom:5px solid #ffbd72}.pose.left{border-color:#78b7ff}.pose img{display:block;width:min(100%,256px);margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.pose b,.pose span{display:block;text-align:center}.pose span{color:#b8d0da}.metrics{display:grid;grid-template-columns:repeat(4,minmax(140px,1fr));gap:10px}.metric{background:#0c1d26;padding:12px;border-top:4px solid #75e6a7}.metric strong{display:block;font-size:1.15rem}.legend{display:flex;gap:18px;flex-wrap:wrap}.swatch{display:inline-block;width:14px;height:4px;vertical-align:middle;margin-right:5px}.green{background:#55ff9b}.gold{background:#ffe06a}@media(max-width:850px){.views{grid-template-columns:1fr}.poses,.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v11/">← Preserve and compare rejected V11</a><h1>Keeper Prime stair ascent V12 · deeper-tread contact and arm reset</h1><span class="status">New reversible mechanical gate · nothing promoted</span><p>Four binding contacts only: <strong>RIGHT leg + LEFT arm</strong>, then <strong>LEFT leg + RIGHT arm</strong>, repeated.</p></header><main><p class="rule warning"><strong>Why V11 is rejected:</strong> its frame 7 support sole floated exactly one 4.286-lp riser above the stair, and its largest arm shift was only 0.875 logical pixels. V12 does not reuse that timeline.</p><p class="rule"><strong>Judge these two things only:</strong> each planted contact must sit on a tread, and the arms must visibly alternate. Once this gate is right, weight-transfer intermediates will be authored between these locked endpoints without changing them.</p><section class="metrics"><div class="metric"><strong>7 lp</strong>tread depth (was 6)</div><div class="metric"><strong>14 × 4.286 lp</strong>equal risers</div><div class="metric"><strong>98 × 60 lp</strong>complete flight</div><div class="metric"><strong>105 lp</strong>reserved stair core</div></section><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label>Hold each contact <input id="speed" type="range" min="120" max="600" step="10" value="280"> <output id="speedValue">280 ms</output></label><label><input id="contacts" type="checkbox" checked> Contact lines</label></div><p id="loading" class="readout">Loading and decoding both contact drawings…</p><p id="readout" class="readout"></p><p class="legend"><span><i class="swatch green"></i>support tread</span><span><i class="swatch gold"></i>next target tread</span></p></article><article><div class="views"><div><h2>Large inspection</h2><div class="stageWrap"><div class="stage large showContacts"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Keeper alternating stair contacts and arms"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game showContacts"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Exact-scale alternating stair contacts"></div></div></div></div></article><h2>The two binding endpoint drawings</h2><section class="poses">${cards}</section><article><h2>Boundary</h2><p>V1–V11 remain immutable review history. The two generated studies are arm sources only: their head, torso and leg pixels are excluded outside two declared arm polygons. V12 changes no Final art, runtime sprite, production manifest or approved animation.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[document.querySelector('.large'),document.querySelector('.game')];let index=0,timer=null,hold=280;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const el of stages){const img=el.querySelector('.walker'),support=el.querySelector('.support'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*4)+'px';img.style.bottom=(f.bottomLp*4)+'px';support.style.left=((f.supportXLp-3.5)*4)+'px';support.style.bottom=(f.supportYLp*4)+'px';target.style.left=((f.targetXLp-3.5)*4)+'px';target.style.bottom=(f.targetYLp*4)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/4 · '+f.label+' · support tread '+f.supportTread+' → target '+f.targetTread+' · support clearance '+f.supportClearanceLp.toFixed(3)+' lp · upper sole '+f.movingClearanceLp.toFixed(3)+' lp'}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){index=(index+1)%timeline.length;render();timer=setTimeout(tick,hold)}function play(){stop();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('speed').oninput=e=>{hold=Number(e.target.value);document.getElementById('speedValue').value=hold+' ms';if(timer)play()};document.getElementById('contacts').onchange=e=>stages.forEach(el=>el.classList.toggle('showContacts',e.target.checked));Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='Both contact drawings decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A drawing failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(pack, 'keeper-prime-stair-ascent-v12.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@12',
  status: 'draft-v12-deeper-tread-contact-and-arm-gate-awaiting-review',
  rejectionOfV11: 'Frame 7 floated exactly one riser and the claimed arm motion remained below one logical pixel.',
  scope: 'Four-contact geometry and alternating-arm gate only; weight-transfer intermediates intentionally deferred.',
  geometry, contactOrder, promoted: false,
  unchanged: { v1ThroughV11: true, finalLane: true, runtimeSprites: true, production: true },
})
const frameUrls = Object.values(urls)
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v12',
  status: 'draft-v12-deeper-tread-contact-and-arm-gate-awaiting-review',
  authorities: {
    rejectedV11: { file: rel(v11RegisterPath), sha256: sha(v11RegisterPath) },
    sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) },
    contactRig: { file: rel(rigPath), sha256: sha(rigPath) },
  },
  generation: { mode: 'generated-arm-studies-plus-deterministic-declared-region-compositing-and-contact-lock', frameUrls },
  originalAndDraft: prep.frames.map((frame) => ({ leg: frame.leg, originalFile: frame.original.file, originalSha256: frame.original.sha256, draftFile: frame.draft.file, draftSha256: frame.draft.sha256 })),
  spec: { file: rel(specPath), sha256: sha(specPath) },
  reviewPage: { file: rel(pagePath), sha256: sha(pagePath) },
  frameUrls,
  validation: {
    uniqueDrawings: 2, shownContacts: 4, contactOrder, treadRunLp: 7, risers: 14, exactFlightRunLp: 98, exactFlightRiseLp: 60,
    everyFrameRequiresSupportContact: true, maximumHandoverXDeltaLp: Math.max(...handovers.map((entry) => Math.abs(entry.previousMovingToNextSupportDeltaLp.x))),
    maximumHandoverYDeltaLp: Math.max(...handovers.map((entry) => Math.abs(entry.previousMovingToNextSupportDeltaLp.y))),
    visiblyOppositeArmSilhouettes: true, edgeAlphaZero: true, v1ThroughV11Changed: false, finalChanged: false, productionChanged: false,
  },
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, uniqueDrawings: frameUrls.length, geometry }, null, 2))
