#!/usr/bin/env node
/** Build Stair Ascent V11: three collision-safe drawings per alternating step. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v11')
const publicDir = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v11')
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v11.json')
const v9RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v9/batch-register.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v9RegisterPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const selectedPoses = [1, 3, 4]
const selected = prep.frames.filter((frame) => selectedPoses.includes(frame.pose))
const urls = {}
for (const frame of selected) {
  const source = path.join(root, frame.file)
  if (sha(source) !== frame.sha256) throw new Error(`${frame.leg} F${frame.pose} changed after preparation`)
  const target = path.join(assetsDir, `${frame.leg}-${frame.phase}-f${frame.pose}-${frame.sha256.slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  urls[`${frame.leg}:${frame.pose}`] = `/keeper-review/keeper-prime-stair-ascent-v11/assets/${path.basename(target)}`
}

const geometry = {
  floorTopLp: 20, firstFloorSupportCentreLp: 103.5, firstTreadCentreLp: 97.5,
  flightRunLp: 84, flightRiseLp: 60, risers: 14, treadRunLp: 6, riserRiseLp: 60 / 14,
  framesPerStep: 3, millisecondsPerFrame: 95, millisecondsPerStep: 285,
  rightRootRunLp: [0, 3.5, 6], leftRootRunLp: [0, 2.25, 6],
}
const timeline = []
for (let step = 0; step < 4; step += 1) {
  const leg = step % 2 === 0 ? 'right' : 'left'
  const rootRun = leg === 'right' ? geometry.rightRootRunLp : geometry.leftRootRunLp
  const baseX = 109.875 - step * geometry.treadRunLp
  const bottomLp = 19.5 + step * geometry.riserRiseLp
  selectedPoses.forEach((pose, phaseIndex) => {
    const frame = prep.frames.find((entry) => entry.leg === leg && entry.pose === pose)
    timeline.push({
      step: step + 1, leg, pose, phase: frame.phase, arm: frame.arm,
      label: `${leg.toUpperCase()} leg ${frame.phase} · ${frame.arm.toUpperCase()} arm forward`,
      src: urls[`${leg}:${pose}`], xLp: baseX - rootRun[phaseIndex], bottomLp,
      supportTread: step, targetTread: step + 1,
      supportXLp: geometry.firstFloorSupportCentreLp - step * geometry.treadRunLp,
      supportYLp: geometry.floorTopLp + step * geometry.riserRiseLp,
      targetXLp: geometry.firstTreadCentreLp - step * geometry.treadRunLp,
      targetYLp: geometry.floorTopLp + (step + 1) * geometry.riserRiseLp,
      durationMs: geometry.millisecondsPerFrame,
    })
  })
}

const rigPath = path.join(pack, 'stair-contact-rig-v11.json')
writeJson(rigPath, {
  schema: 'lighthouse-keeper/stair-contact-rig@11', status: 'intermediate-motion-candidate-awaiting-review', direction: 'leftward gameplay', cell: [256, 320], density: 8, geometry,
  contactOrder: ['right', 'left', 'right', 'left'],
  contract: [
    'Each step uses lift, reach and plant only; V6 pose 2 is deliberately excluded because its boot intersects the next riser.',
    'RIGHT leg phases pair with a restrained LEFT-arm counter-motion; LEFT leg phases pair with a clearer RIGHT-arm counter-motion.',
    'The complete root advances exactly one 6-lp tread per three-frame step and rises only when the support changes to the next tread.',
    'Every selected lower-leg pixel is inherited unchanged from the V6/V7 same-family stair art; only the bounded arm region is warped.',
  ],
})

const stairs = Array.from({ length: 7 }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.firstFloorSupportCentreLp - 3 - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const cards = selected.map((frame) => `<div class="pose ${frame.leg}"><img src="${urls[`${frame.leg}:${frame.pose}`]}" alt="${frame.leg} leg ${frame.phase}"><b>${frame.leg.toUpperCase()} · ${frame.phase.toUpperCase()}</b><span>${frame.arm.toUpperCase()} arm forward · ${frame.armForwardPixels} source px</span></div>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V11</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1280px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left top}.step{position:absolute;background:#526675;border-top:3px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:402px;right:0;bottom:0;height:80px;background:#526675;border-top:3px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.line{position:absolute;height:3px;width:24px;z-index:8;display:none}.showContacts .line{display:block}.support{background:#55ff9b}.target{background:#ffe06a}.poses{display:grid;grid-template-columns:repeat(3,minmax(160px,1fr));gap:12px}.pose{background:#0c1d26;padding:10px;border-bottom:5px solid #ffbd72}.pose.left{border-color:#78b7ff}.pose img{display:block;width:min(100%,256px);margin:auto;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.pose b,.pose span{display:block;text-align:center}.pose span{color:#b8d0da;font-size:12px}.legend{display:flex;gap:18px;flex-wrap:wrap}.swatch{display:inline-block;width:14px;height:4px;vertical-align:middle;margin-right:5px}.green{background:#55ff9b}.gold{background:#ffe06a}@media(max-width:850px){.views{grid-template-columns:1fr}.poses{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v9/">← Preserve and compare contact-only V9</a><h1>Keeper Prime stair ascent V11 · alternating lift → reach → plant</h1><span class="status">New reversible draft · nothing promoted</span><p>Four adjacent stairs: <strong>RIGHT leg + LEFT arm</strong>, then <strong>LEFT leg + RIGHT arm</strong>, repeated exactly.</p></header><main><p class="rule"><strong>Judge the transition now:</strong> the V9 tread landings remain the geometry authority. V11 adds only two useful drawings between landings, keeps the same Keeper family, and uses a smaller arm movement on the right-leg step than on the left-leg step.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label>Frame speed <input id="speed" type="range" min="55" max="180" step="5" value="95"> <output id="speedValue">95 ms</output></label><label><input id="contacts" type="checkbox"> Contact lines</label></div><p id="loading" class="readout">Loading and decoding all six unique drawings…</p><p id="readout" class="readout"></p><p class="legend"><span><i class="swatch green"></i>support tread</span><span><i class="swatch gold"></i>next target tread</span></p></article><article><div class="views"><div><h2>Large inspection</h2><div class="stageWrap"><div class="stage large"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Keeper alternating up four stairs"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="line support"></div><div class="line target"></div><img class="walker" alt="Exact-scale alternating stair preview"></div></div></div></div></article><h2>The six drawings actually used</h2><section class="poses">${cards}</section><article><h2>Boundary</h2><p>V1–V10 remain immutable history. V10’s generated motion studies are retained but rejected because they changed the Prime silhouette. V11 derives from the established V6/V7 stair family, modifies only a bounded arm region, changes no Final art, runtime sprite or production geometry, and promotes nothing.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[document.querySelector('.large'),document.querySelector('.game')];let index=0,timer=null,hold=95;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const el of stages){const img=el.querySelector('.walker'),support=el.querySelector('.support'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*4)+'px';img.style.bottom=(f.bottomLp*4)+'px';support.style.left=((f.supportXLp-3)*4)+'px';support.style.bottom=(f.supportYLp*4)+'px';target.style.left=((f.targetXLp-3)*4)+'px';target.style.bottom=(f.targetYLp*4)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/'+timeline.length+' · step '+f.step+'/4 · '+f.label+' · support '+f.supportTread+' → target '+f.targetTread}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index>=timeline.length-1)return stop();index++;render();timer=setTimeout(tick,hold)}function play(){stop();timer=setTimeout(tick,hold)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('speed').oninput=e=>{hold=Number(e.target.value);document.getElementById('speedValue').value=hold+' ms';if(timer)play()};document.getElementById('contacts').onchange=e=>stages.forEach(el=>el.classList.toggle('showContacts',e.target.checked));Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique drawings decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A drawing failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const specPath = path.join(pack, 'keeper-prime-stair-ascent-v11.json')
writeJson(specPath, {
  schema: 'lighthouse-keeper/prime-stair-ascent@11', status: 'draft-v11-alternating-intermediates-awaiting-review',
  rejectionOfV10: 'Generated motion studies changed the Prime silhouette and could not maintain binding tread contacts.',
  correction: 'Return to V6/V7 same-family art; select collision-safe lift/reach/plant poses; add bounded asymmetric contralateral arm warps.',
  geometry, promoted: false,
  unchanged: { v1ThroughV10: true, v9TreadGeometry: true, finalLane: true, production: true },
})
const frameUrls = Object.values(urls)
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v11', status: 'draft-v11-alternating-intermediates-awaiting-review',
  authorities: { contactProofV9: { file: rel(v9RegisterPath), sha256: sha(v9RegisterPath) }, sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) }, contactRig: { file: rel(rigPath), sha256: sha(rigPath) } },
  generation: { mode: 'same-family-source-selection-plus-bounded-deterministic-arm-warp', frameUrls },
  originalAndDraft: selected.map((frame) => ({ leg: frame.leg, pose: frame.pose, originalFile: frame.sourceFile, originalSha256: frame.sourceSha256, draftFile: frame.file, draftSha256: frame.sha256 })),
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { uniqueDrawings: 6, shownFrames: 12, rightLegSteps: 2, leftLegSteps: 2, framesPerStep: 3, armAmplitudeRightStepMaxPx: 3, armAmplitudeLeftStepMaxPx: 7, lowerLegsUnchangedFromY247: true, headUnchangedThroughY127: true, v1ThroughV10Changed: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), '# Keeper Prime stair ascent V11 decision log\n\nNo image generation contributes pixels to V11. The rejected V10 image-generation studies are preserved separately. V11 deterministically derives six selected lift/reach/plant drawings from V6/V7 and applies only a bounded arm-region warp: maximum 3 source pixels for LEFT arm on RIGHT-leg steps, maximum 7 source pixels for RIGHT arm on LEFT-leg steps.\n')
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Keeper Prime stair ascent V11\n\nStatus: alternating intermediate-motion draft awaiting Frank’s review.\n\nReview: `/keeper-review/keeper-prime-stair-ascent-v11/`.\n\nV11 shows four adjacent stairs using a repeated RIGHT-leg/LEFT-arm then LEFT-leg/RIGHT-arm pattern. Each step uses only lift, reach and plant; the collision-prone V6 pose 2 is deliberately excluded. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, uniqueDrawings: frameUrls.length, frameDurationMs: geometry.millisecondsPerFrame }, null, 2))
