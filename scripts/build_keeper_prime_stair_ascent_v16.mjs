#!/usr/bin/env node
/** Build V16: three masked art corrections on the exact V15 full-flight timeline. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-ascent-v16'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const v15 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v15')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v16.json')
const v15RigPath = path.join(v15, 'stair-contact-rig-v15.json')
const v15RegisterPath = path.join(v15, 'batch-register.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v15RigPath, v15RegisterPath, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
const v15Rig = JSON.parse(fs.readFileSync(v15RigPath, 'utf8'))
const v15Register = JSON.parse(fs.readFileSync(v15RegisterPath, 'utf8'))
const geometry = { ...v15Rig.geometry }
fs.rmSync(assetsDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const sources = {
  'contact:left': prep.corrections.left_contact.draft.file,
  'contact:right': prep.corrections.right_contact.draft.file,
  'passing:left': prep.corrections.left_passing.draft.file,
  'passing:right': prep.corrections.right_passing.draft.file,
}
const urls = {}
const assetRecords = []
for (const [key, sourceRel] of Object.entries(sources)) {
  const source = path.join(root, sourceRel)
  const digest = sha(source)
  const stem = key.replace(':', '-')
  const target = path.join(assetsDir, `${stem}-${digest.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  const url = `/keeper-review/${set}/assets/${path.basename(target)}`
  urls[key] = url
  assetRecords.push({ role: key, source: sourceRel, sourceSha256: digest, url })
}

const label = (frame) => {
  if (frame.kind === 'passing' && frame.movingLeg === 'right') return 'RIGHT compact passing · boot lift matched to LEFT'
  if (frame.kind === 'passing') return 'LEFT compact passing · unchanged authority'
  if (frame.movingLeg === 'left') return 'LEFT contact · detached flesh artefact removed'
  return 'RIGHT contact · forward boot toecap restored'
}
const timeline = v15Rig.timeline.map((frame) => {
  const next = { ...frame, src: urls[`${frame.kind}:${frame.movingLeg}`], label: label(frame) }
  if (frame.kind === 'passing' && frame.movingLeg === 'right') {
    next.movingLegMinimumClearanceLp = prep.corrections.right_passing.stairClearance.minimumLp
    next.movingLegPenetratingPixels = prep.corrections.right_passing.stairClearance.penetratingPixels
  }
  return next
})
const rigPath = path.join(pack, 'stair-contact-rig-v16.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@16',
  status: 'three-defect-correction-awaiting-review',
  direction: v15Rig.direction,
  cell: v15Rig.cell,
  density: v15Rig.density,
  geometry,
  uniqueDrawings: 4,
  timeline,
  endpoint: { ...v15Rig.endpoint },
  contract: [
    'The V15 27-frame timeline, placements, root positions, stair geometry and timing remain exact.',
    'RIGHT and LEFT compact-passing moving regions share the same y=270 exclusive lower bound.',
    'RIGHT compact passing has zero stair penetration and at least 1.5 lp clearance.',
    'LEFT contact changes only its measured detached-remnant restoration mask.',
    'RIGHT contact changes only its forward-boot toecap mask; the contact sole row stays exact.',
    'Playback reaches tread 14 and holds; Final, runtime and production remain unchanged.',
  ],
})

const oldByRole = {}
for (const entry of v15Register.assets) {
  if (entry.url.includes('left-contact')) oldByRole['contact:left'] = entry.url
  else if (entry.url.includes('right-contact')) oldByRole['contact:right'] = entry.url
  else if (entry.url.includes('left-passing')) oldByRole['passing:left'] = entry.url
  else if (entry.url.includes('right-passing')) oldByRole['passing:right'] = entry.url
}
const stairs = Array.from({ length: geometry.risers }, (_, index) => { const n = index + 1; return `<span class="step" style="left:${(geometry.stairBaseRightLp - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>` }).join('')
const comparisons = [
  ['RIGHT compact passing', oldByRole['passing:right'], urls['passing:right'], 'Raised-boot lower edge now matches LEFT at source y=270; clearance remains 1.59 lp.'],
  ['LEFT contact', oldByRole['contact:left'], urls['contact:left'], 'Detached flesh-coloured remnant removed; all pixels outside its measured mask are exact.'],
  ['RIGHT contact', oldByRole['contact:right'], urls['contact:right'], 'Forward/left boot receives a complete rounded toecap; sole/contact row remains exact.'],
].map(([name, before, after, note]) => `<article class="compare"><h3>${name}</h3><div><figure><img src="${before}" alt="${name} before"><figcaption>V15 before</figcaption></figure><figure><img src="${after}" alt="${name} V16"><figcaption>V16 candidate</figcaption></figure></div><p>${note}</p></article>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V16</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1280px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left top}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:${geometry.stairBaseRightLp * 4}px;right:0;bottom:0;height:${geometry.floorTopLp * 4}px;background:#526675;border-top:3px solid #d0dee6}.landing{position:absolute;left:0;bottom:${(geometry.floorTopLp + geometry.flightRiseLp) * 4}px;width:${(geometry.stairBaseRightLp - geometry.flightRunLp) * 4}px;height:3px;background:#d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.line{position:absolute;height:3px;width:28px;z-index:8;display:none}.showContacts .line{display:block}.support{background:#55ff9b}.target{background:#ffe06a}.progress{height:8px;background:#1a3542;border-radius:99px;overflow:hidden}.progress span{display:block;height:100%;width:0;background:#75e6a7}.comparisons{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.compare>div{display:grid;grid-template-columns:1fr 1fr;gap:8px}.compare figure{margin:0;text-align:center}.compare img{display:block;width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.compare figcaption{font-size:12px;color:#bdd3dd;margin-top:4px}@media(max-width:900px){.views,.comparisons{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v15/">← V15 full-flight review</a><h1>Keeper Prime stair ascent V16 · three focused corrections</h1><span class="status">New reversible candidate · nothing promoted</span><p><strong>The exact V15 climb now uses corrected RIGHT passing, LEFT contact and RIGHT contact drawings.</strong></p></header><main><p class="rule"><strong>Judge the repeated climb:</strong> RIGHT and LEFT passing boots should now feel equally lifted; the LEFT-contact flesh speck should be gone; the RIGHT-contact forward boot should have a complete toecap.</p><article><div class="controls"><button id="play" disabled>Play full ascent</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart from floor</button><label>Frame speed <input id="speed" type="range" min="70" max="220" step="5" value="110"> <output id="speedValue">110 ms</output></label><label><input id="contacts" type="checkbox"> Contact lines</label></div><p id="loading" class="readout">Loading and decoding all before/after drawings…</p><p id="readout" class="readout"></p><div class="progress"><span id="progress"></span></div></article><article><div class="views"><div><h2>Large full-flight inspection</h2><div class="stageWrap"><div class="stage large"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Keeper V16 complete stair ascent"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Exact-scale V16 stair ascent"></div></div></div></div></article><h2>Focused before/after evidence</h2><section class="comparisons">${comparisons}</section><article><h2>Deterministic boundary</h2><p>All three edits are confined to declared masks. RIGHT/LEFT passing moving regions now share the same lower y=270 boundary; RIGHT passing clears the stair by ${prep.corrections.right_passing.stairClearance.minimumLp.toFixed(2)} lp with zero penetrating pixels. The 27-frame timeline, geometry, root motion and top hold remain exact. Final, runtime and production are unchanged.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},evidence=${JSON.stringify(Object.values(oldByRole))},buttons=[...document.querySelectorAll('button')],stages=[document.querySelector('.large'),document.querySelector('.game')];let index=0,timer=null,hold=110;const unique=[...new Set([...timeline.map(f=>f.src),...evidence])];function render(){const f=timeline[index];for(const el of stages){const img=el.querySelector('.walker'),support=el.querySelector('.support'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*4)+'px';img.style.bottom=(f.bottomLp*4)+'px';support.style.left=((f.supportXLp-3.5)*4)+'px';support.style.bottom=(f.supportYLp*4)+'px';target.style.left=((f.targetXLp-3.5)*4)+'px';target.style.bottom=(f.targetYLp*4)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/27 · '+f.label+(index===26?' · TOP REACHED':'');document.getElementById('progress').style.width=((f.targetTread/14)*100)+'%'}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index>=timeline.length-1)return stop();index++;render();timer=setTimeout(tick,index===timeline.length-1?timeline[index].durationMs:hold)}function play(){stop();if(index>=timeline.length-1)index=0;render();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(timeline.length-1,index+1);render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('speed').oninput=e=>{hold=Number(e.target.value);document.getElementById('speedValue').value=hold+' ms';if(timer)play()};document.getElementById('contacts').onchange=e=>stages.forEach(el=>el.classList.toggle('showContacts',e.target.checked));Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All before/after drawings decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A drawing failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html'); fs.writeFileSync(pagePath, html)
const spec = { schema: 'lighthouse-keeper/prime-stair-ascent@16', status: 'draft-v16-three-defect-correction-awaiting-review', scope: 'Three tightly masked drawing corrections on the exact V15 complete-flight preview.', geometry, promoted: false, unchanged: { v15Timeline: true, rootPositions: true, stairGeometry: true, timing: true, finalLane: true, runtimeSprites: true, production: true } }
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v16.json'); writeJson(specPath, spec)
const frameUrls = assetRecords.map((entry) => entry.url)
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-ascent-2026-10-15-v16',
  status: spec.status,
  authorities: {
    v15FullFlight: { file: rel(v15RegisterPath), sha256: sha(v15RegisterPath) },
    sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) },
    rig: { file: rel(rigPath), sha256: sha(rigPath) },
  },
  generation: { mode: 'two-built-in-image-edit-studies-plus-deterministic-registration-and-three-tight-masks', frameUrls },
  assets: assetRecords,
  spec: { file: rel(specPath), sha256: sha(specPath) },
  reviewPage: { file: rel(pagePath), sha256: sha(pagePath) },
  frameUrls,
  comparisonUrls: Object.values(oldByRole),
  validation: {
    uniqueDrawings: 4,
    timelineFrames: timeline.length,
    contactFrames: timeline.filter((frame) => frame.kind === 'contact').length,
    passingFrames: timeline.filter((frame) => frame.kind === 'passing').length,
    passingMovingBottomExclusive: { right: prep.corrections.right_passing.movingBoundsExclusive[3], left: prep.corrections.left_passing.movingBoundsExclusive[3] },
    rightPassingMinimumClearanceLp: prep.corrections.right_passing.stairClearance.minimumLp,
    passingPenetratingPixels: prep.corrections.right_passing.stairClearance.penetratingPixels + prep.corrections.left_passing.stairClearance.penetratingPixels,
    outsideMaskChanges: ['right_passing', 'left_contact', 'right_contact'].reduce((sum, key) => sum + prep.corrections[key].outsideMaskChangedPixels, 0),
    finalTargetTread: timeline.at(-1).targetTread,
    wrapToBottom: false,
    finalChanged: false,
    runtimeSpritesChanged: false,
    productionChanged: false,
  },
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, passingBottom: register.validation.passingMovingBottomExclusive, rightClearance: register.validation.rightPassingMinimumClearanceLp, outsideMaskChanges: register.validation.outsideMaskChanges }, null, 2))
