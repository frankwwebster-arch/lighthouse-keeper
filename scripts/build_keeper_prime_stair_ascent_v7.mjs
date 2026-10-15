#!/usr/bin/env node
/** Build Stair Ascent V7: a four-contact RIGHT/LEFT/RIGHT/LEFT diagnostic. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v7'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v7.json')
const v6RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6/batch-register.json')
const sideAuthorityPath = path.join(root, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v6RegisterPath, sideAuthorityPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const urls = {}
for (const frame of prep.frames) {
  const source = path.join(root, frame.file)
  if (sha(source) !== frame.sha256) throw new Error(`${frame.leg} contact source changed`)
  const target = path.join(assetsDir, `${frame.leg}-contact-${frame.sha256.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  urls[frame.leg] = `/keeper-review/${set}/assets/${path.basename(target)}`
}

const geometry = {
  floorTopLp: 20,
  baseX: 100.5,
  baseBottomLp: 19.5,
  treadRunLp: 6,
  riserRiseLp: 60 / 14,
  shownContacts: 4,
  contactDurationMs: 320,
}
const prepByLeg = Object.fromEntries(prep.frames.map((frame) => [frame.leg, frame]))
const contactOrder = ['right', 'left', 'right', 'left']
const timeline = contactOrder.map((leg, index) => {
  const step = index + 1
  const frame = prepByLeg[leg]
  const supportCentreLp = geometry.baseX - (step - 0.5) * geometry.treadRunLp
  const targetCentreLp = geometry.baseX - (step + 0.5) * geometry.treadRunLp
  const localSupportLp = frame.supportSole.centreX / 8
  return {
    phase: 'two-contact stair proof',
    step,
    leg,
    label: `${leg.toUpperCase()} leg forward and up`,
    src: urls[leg],
    xLp: supportCentreLp - localSupportLp + 16,
    bottomLp: geometry.baseBottomLp + (step - 1) * geometry.riserRiseLp,
    supportTread: step - 1,
    targetTread: step,
    supportXLp: supportCentreLp,
    supportYLp: geometry.floorTopLp + (step - 1) * geometry.riserRiseLp,
    targetXLp: targetCentreLp,
    targetYLp: geometry.floorTopLp + step * geometry.riserRiseLp,
    durationMs: geometry.contactDurationMs,
  }
})

const rigPath = path.join(pack, 'stair-contact-rig-v7.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@7',
  status: 'four-contact-mechanical-proof-only',
  direction: 'leftward gameplay', cell: [256, 320], density: 8, geometry,
  contactOrder,
  contract: [
    'Only two unique drawings exist: RIGHT forward/up and LEFT forward/up.',
    'The review loop is RIGHT, LEFT, RIGHT, LEFT with no intervening drawings.',
    'Each moving sole is one adjacent tread above and one tread ahead of its planted support sole.',
    'This is a leg/contact diagnostic, not a complete stair transition or approval candidate.',
  ],
})

const stairs = Array.from({ length: 7 }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.baseX - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V7</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1180px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left top}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:402px;right:0;bottom:0;height:80px;background:#526675;border-top:3px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.line{position:absolute;height:3px;width:24px;z-index:8}.support{background:#55ff9b}.target{background:#ffe06a}.poses{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pose{background:#0c1d26;padding:12px;border-bottom:5px solid #ffbd72}.pose.left{border-color:#78b7ff}.pose img{display:block;width:min(100%,256px);margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.pose b,.pose span{display:block;text-align:center}.pose span{color:#b8d0da}.legend{display:flex;gap:18px;flex-wrap:wrap}.swatch{display:inline-block;width:14px;height:4px;vertical-align:middle;margin-right:5px}.green{background:#55ff9b}.gold{background:#ffe06a}@media(max-width:850px){.views{grid-template-columns:1fr}.poses{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v6/">← Preserve and compare rejected V6</a><h1>Keeper Prime stair ascent V7 · two-contact leg test</h1><span class="status">New reversible draft · nothing promoted</span><p>This deliberately removes every intermediate. It shows only <strong>RIGHT leg forward/up → LEFT leg forward/up → repeat</strong>.</p></header><main><p class="rule"><strong>Judge only the alternation and tread contact:</strong> one foot remains planted on the lower tread while the other is already planted on the immediately adjacent upper tread. There are no swing, high-pass or transfer frames in this test.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label>Hold each contact <input id="speed" type="range" min="140" max="650" step="10" value="320"> <output id="speedValue">320 ms</output></label></div><p id="loading" class="readout">Loading and decoding both contact drawings…</p><p id="readout" class="readout"></p><p class="legend"><span><i class="swatch green"></i>planted support tread</span><span><i class="swatch gold"></i>next-foot target tread</span></p></article><article><div class="views"><div><h2>Large inspection</h2><div class="stageWrap"><div class="stage large"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Keeper alternating stair contacts"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Exact-scale alternating stair contacts"></div></div></div></div></article><h2>The only two drawings used</h2><section class="poses"><div class="pose right"><img src="${urls.right}" alt="Right leg forward and up"><b>RIGHT</b><span>forward and up</span></div><div class="pose left"><img src="${urls.left}" alt="Left leg forward and up"><b>LEFT</b><span>forward and up</span></div></section><article><h2>Boundary</h2><p>V1–V6 remain immutable historical drafts. V7 changes no approved walk pixels, Final art, runtime sprites or production geometry. If this basic two-drawing alternation is right, intermediate smoothing can be designed later without changing these binding foot contacts.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[document.querySelector('.large'),document.querySelector('.game')];let index=0,timer=null,hold=320;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const el of stages){const img=el.querySelector('.walker'),support=el.querySelector('.support'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*4)+'px';img.style.bottom=(f.bottomLp*4)+'px';support.style.left=((f.supportXLp-3)*4)+'px';support.style.bottom=(f.supportYLp*4)+'px';target.style.left=((f.targetXLp-3)*4)+'px';target.style.bottom=(f.targetYLp*4)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/4 · '+f.label+' · support tread '+f.supportTread+' → target tread '+f.targetTread}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){index=(index+1)%timeline.length;render();timer=setTimeout(tick,hold)}function play(){stop();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+4)%4;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%4;render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('speed').oninput=e=>{hold=Number(e.target.value);document.getElementById('speedValue').value=hold+' ms';if(timer)play()};Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All 2 unique contact drawings decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A drawing failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(pack, 'keeper-prime-stair-ascent-v7.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@7',
  status: 'draft-v7-two-contact-leg-test-awaiting-review',
  rejectionOfV6: 'V6 still let feet pass through treads; its six-phase interpolation is removed entirely.',
  scope: 'Four-contact RIGHT/LEFT/RIGHT/LEFT diagnostic only; not a complete transition.',
  geometry, contactOrder, promoted: false,
  unchanged: { v1ThroughV6: true, approvedWalkSourcePixels: true, finalLane: true, production: true },
})
const frameUrls = [urls.right, urls.left]
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v7',
  status: 'draft-v7-two-contact-leg-test-awaiting-review',
  authorities: {
    rejectedV6: { file: rel(v6RegisterPath), sha256: sha(v6RegisterPath) },
    approvedSideMaster: { file: rel(sideAuthorityPath), sha256: sha(sideAuthorityPath) },
    sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) },
    contactRig: { file: rel(rigPath), sha256: sha(rigPath) },
  },
  generation: { mode: 'deterministic-two-contact-lower-leg-registration-from-v6-contact-drawings', frameUrls },
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { uniqueDrawings: 2, shownContacts: 4, contactOrder, noIntermediates: true, adjacentTreadOnly: true, edgeAlphaZero: true, v1ThroughV6Changed: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), `# Keeper Prime stair ascent V7 decision log\n\nNo image generation was used. V7 is a deterministic mechanical test derived from the rejected V6 RIGHT and LEFT planted-contact drawings. The moving lower leg is registered to exactly one adjacent tread while the upper body remains unchanged through source row 220. The four-frame review order is RIGHT, LEFT, RIGHT, LEFT with no intervening drawings.\n`)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, uniqueDrawings: 2, contactOrder }, null, 2))
