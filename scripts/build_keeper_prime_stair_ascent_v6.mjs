#!/usr/bin/env node
/** Build Stair Ascent V6: fourteen explicit, equally divided stair contacts. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6')
const publicDir = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v6')
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v6.json')
const v5RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v5/batch-register.json')
const v5Page = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v5/index.html')
const archiveIndexPath = path.join(root, 'review-archive/index.json')
const sideAuthorityPath = path.join(root, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, v5RegisterPath, v5Page, archiveIndexPath, sideAuthorityPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
const v5Register = JSON.parse(fs.readFileSync(v5RegisterPath, 'utf8'))
const archiveIndex = JSON.parse(fs.readFileSync(archiveIndexPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const copyAsset = (source, stem) => {
  const target = path.join(assetsDir, `${stem}-${sha(source).slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  return `/keeper-review/keeper-prime-stair-ascent-v6/assets/${path.basename(target)}`
}
const copyArchivedUrl = (url, stem) => {
  const entry = archiveIndex.legacyPaths[url]
  if (!entry) throw new Error(`archive does not resolve ${url}`)
  const source = path.join(root, entry.object)
  if (sha(source) !== entry.sha256) throw new Error(`archive object changed for ${url}`)
  return copyAsset(source, stem)
}

const walkUrls = v5Register.frameUrls.slice(0, 8).map((url, index) => copyArchivedUrl(url, `walk-left-f${index + 1}`))
const legUrls = Object.fromEntries(['left', 'right'].map((leg) => [leg, prep.frames.filter((frame) => frame.leg === leg).map((frame) => copyAsset(path.join(root, frame.leftFile), `${leg}-leg-step-f${String(frame.pose).padStart(2, '0')}`))]))
const guideUrls = Object.fromEntries(['left', 'right'].map((leg) => [leg, copyAsset(path.join(pack, `guides/${leg}-leg-step-guide-v6.png`), `${leg}-leg-contact-authority`)]))

const oldHtml = fs.readFileSync(v5Page, 'utf8')
const oldTimelineMatch = oldHtml.match(/const timeline=(\[.*?\]),buttons=/s)
if (!oldTimelineMatch) throw new Error('V5 timeline missing')
const oldTimeline = JSON.parse(oldTimelineMatch[1])
const walk = oldTimeline.slice(0, 8).map((frame, index) => ({ ...frame, src: walkUrls[index] }))

const geometry = {
  floorTopLp: 20,
  baseX: 94.5,
  baseBottomLp: 19.5,
  flightRunLp: 84,
  flightRiseLp: 60,
  risers: 14,
  treadRunLp: 6,
  riserRiseLp: 60 / 14,
  leftContacts: 7,
  rightContacts: 7,
  posesPerStep: 6,
  climbFrameDurationMs: 60,
}
const rootRun = [0, 0.9, 2, 3.1, 4.6, 6]
const rootRiseFactor = [0, 0, 0, 0, 0, 1]
const phase = ['lift', 'swing', 'high pass', 'adjacent-tread contact', 'weight transfer', 'plant / opposite toe-off']
const timeline = [...walk]
for (let step = 0; step < geometry.risers; step += 1) {
  const leg = step % 2 === 0 ? 'left' : 'right'
  for (let poseIndex = 0; poseIndex < geometry.posesPerStep; poseIndex += 1) {
    const rootRise = rootRiseFactor[poseIndex] * geometry.riserRiseLp
    const supportTread = poseIndex === 5 ? step + 1 : step
    timeline.push({
      phase: 'equal-leg adjacent-tread stair climb', step: step + 1, leg, pose: poseIndex + 1,
      label: `${leg.toUpperCase()} leg · ${phase[poseIndex]}`, src: legUrls[leg][poseIndex],
      xLp: geometry.baseX - step * geometry.treadRunLp - rootRun[poseIndex],
      bottomLp: geometry.baseBottomLp + step * geometry.riserRiseLp + rootRise,
      supportTread,
      contactXLp: geometry.baseX - (supportTread - 0.5) * geometry.treadRunLp,
      contactYLp: geometry.floorTopLp + supportTread * geometry.riserRiseLp,
      targetXLp: geometry.baseX - (step + 0.5) * geometry.treadRunLp,
      targetYLp: geometry.floorTopLp + (step + 1) * geometry.riserRiseLp,
      durationMs: geometry.climbFrameDurationMs,
    })
  }
}

const rig = {
  schema: 'lighthouse-keeper/stair-contact-rig@6', direction: 'leftward gameplay', cell: [256, 320], density: 8,
  geometry, rootRunLp: rootRun, rootRiseFactor,
  cadence: { framesPerStep: 6, millisecondsPerFrame: 60, millisecondsPerStep: 360, priorV5MillisecondsPerStep: 368 },
  contract: [
    'Odd numbered contacts are LEFT leg; even numbered contacts are RIGHT leg.',
    'Each leg owns exactly seven of the fourteen adjacent-tread contacts.',
    'Every step advances exactly 6 lp and rises exactly 60/14 lp; no pose can advance two treads.',
    'F1-F5 remain registered to the lower support tread; F6 transfers the root to the new planted tread.',
    'The source high pass is artwork, not extra root motion; the page never infers travel from the silhouette.',
  ],
}
const rigPath = path.join(pack, 'stair-contact-rig-v6.json')
writeJson(rigPath, rig)

const stairs = Array.from({ length: geometry.risers }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(geometry.baseX - n * geometry.treadRunLp) * 4}px;bottom:${geometry.floorTopLp * 4}px;width:${geometry.treadRunLp * 4}px;height:${n * geometry.riserRiseLp * 4}px"></span>`
}).join('')
const poseCards = ['left', 'right'].flatMap((leg) => legUrls[leg].map((url, index) => `<div class="pose ${leg}"><img src="${url}" alt="${leg} leg stair pose ${index + 1}"><b>${leg.toUpperCase()} ${index + 1}/6</b><span>${phase[index]}</span></div>`)).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V6</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1480px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:24px;align-items:start}.stageWrap{overflow:auto;max-width:100%}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{left:0;bottom:0;top:auto;right:auto;width:620px;height:480px;transform:scale(.25);transform-origin:left bottom}.stairs{position:absolute;inset:0}.step{position:absolute;background:#526675;border-top:2px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:378px;right:0;bottom:0;height:80px;background:#526675;border-top:2px solid #d0dee6}.landing{position:absolute;left:0;bottom:80px;width:42px;height:240px;background:#526675;border-top:2px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.door{position:absolute;left:420px;bottom:80px;width:84px;height:224px;background:#273b45;border:3px solid #75909d;z-index:5}.contact,.target{display:none;position:absolute;height:3px;z-index:8}.contact{background:#55ff9b;box-shadow:0 0 0 1px #063}.target{background:#ffe06a;box-shadow:0 0 0 1px #6b5400}.showContacts .contact,.showContacts .target{display:block}.foregroundBanister{position:absolute;inset:0;z-index:7;pointer-events:none;opacity:.32}.hideBanister .foregroundBanister{display:none}.poses{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:8px}.pose{background:#0c1d26;padding:8px;border-bottom:4px solid #78b7ff}.pose.right{border-color:#ffbd72}.pose img{display:block;width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.pose span{display:block;color:#b8d0da;font-size:12px}.authorityGrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.authorityGrid img{width:100%;background:#0a1117}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric{background:#0c1d26;padding:12px;border-top:4px solid #75e6a7}.metric strong{font-size:1.15rem}.legend{display:flex;gap:18px;flex-wrap:wrap}.swatch{display:inline-block;width:14px;height:4px;vertical-align:middle;margin-right:5px}.green{background:#55ff9b}.gold{background:#ffe06a}@media(max-width:900px){.views{grid-template-columns:1fr}.poses{grid-template-columns:repeat(3,1fr)}.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v5/">← Preserve and compare rejected V5</a><h1>Keeper Prime stair ascent V6 · exact 50/50 alternating contacts</h1><span class="status">New reversible draft · nothing promoted</span><p>V6 replaces the V3–V5 leg artwork. Fourteen explicit adjacent-tread steps alternate LEFT, RIGHT without exception; each step has six drawings but retains the established stair cadence.</p></header><main><p class="rule"><strong>Judge the feet first:</strong> left plants step 1, right plants step 2, then left/right continue through step 14. No boot may pass through a tread and no leg may take two stairs at once.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><button id="cycle" disabled>Loop one LEFT + RIGHT pair</button><label><input id="contacts" type="checkbox"> Contact lines</label><label><input id="banister" type="checkbox" checked> Translucent bannister</label><label>Opacity <input id="opacity" type="range" min="0" max="100" value="32"> <output id="opacityValue">32%</output></label><label><input id="loop" type="checkbox"> Loop full route</label></div><p id="loading" class="readout">Loading and decoding every unique frame…</p><p id="readout" class="readout"></p><p class="legend"><span><i class="swatch green"></i>current support tread</span><span><i class="swatch gold"></i>immediately adjacent target tread</span></p></article><article><div class="views"><div><h2>Large contact inspection · 4 CSS px/lp</h2><div class="stageWrap"><div class="stage large"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="door"></div><div class="contact"></div><div class="target"></div><img class="walker" alt="Keeper walking out and alternating up the stairs"><svg class="foregroundBanister" viewBox="0 0 620 480" aria-hidden="true"><path d="M38 322 L380 82 L392 99 L50 339 Z" fill="#253743" stroke="#8aa0ad" stroke-width="5"/><path d="M54 310 L384 78" stroke="#a8bac4" stroke-width="7" stroke-linecap="round"/></svg></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px per logical px.</p><div class="stage game"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="door"></div><div class="contact"></div><div class="target"></div><img class="walker" alt="Exact-scale stair preview"><svg class="foregroundBanister" viewBox="0 0 620 480" aria-hidden="true"><path d="M38 322 L380 82 L392 99 L50 339 Z" fill="#253743" stroke="#8aa0ad" stroke-width="5"/><path d="M54 310 L384 78" stroke="#a8bac4" stroke-width="7" stroke-linecap="round"/></svg></div></div></div></div></article><section class="metrics"><div class="metric"><strong>7 LEFT + 7 RIGHT</strong><br>exactly equal contacts</div><div class="metric"><strong>6 frames per step</strong><br>smoothness without slower cadence</div><div class="metric"><strong>6 lp × 4.286 lp</strong><br>one adjacent tread only</div><div class="metric"><strong>84 × 60 lp</strong><br>exact flight closure</div></section><h2>Two separately authored six-pose steps</h2><section class="poses">${poseCards}</section><details><summary>Show the binding left/right geometry guides</summary><div class="authorityGrid"><img src="${guideUrls.left}" alt="Left leg six-pose stair guide"><img src="${guideUrls.right}" alt="Right leg six-pose stair guide"></div></details><article><h2>Boundary</h2><p>V1–V5 remain immutable historical drafts. V6 changes no approved walk pixels, Final art, runtime sprites or production geometry. The climb artwork and fourteen-riser stair proposal are review candidates only.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[{el:document.querySelector('.large'),scale:4},{el:document.querySelector('.game'),scale:4}];let index=0,timer=null,cycleOnly=false;const unique=[...new Set(timeline.map(f=>f.src).concat(${JSON.stringify(Object.values(guideUrls))}))];function render(){const f=timeline[index];for(const {el,scale} of stages){const img=el.querySelector('.walker'),line=el.querySelector('.contact'),target=el.querySelector('.target');img.src=f.src;img.style.left=((f.xLp-16)*scale)+'px';img.style.bottom=(f.bottomLp*scale)+'px';if(f.contactXLp!==undefined){line.style.left=((f.contactXLp-3)*scale)+'px';line.style.bottom=(f.contactYLp*scale)+'px';line.style.width=(6*scale)+'px';target.style.left=((f.targetXLp-3)*scale)+'px';target.style.bottom=(f.targetYLp*scale)+'px';target.style.width=(6*scale)+'px'}else{line.style.width='0';target.style.width='0'}}document.getElementById('readout').textContent='F'+(index+1)+'/'+timeline.length+' · '+f.phase+(f.step?' · step '+f.step+'/14 · '+f.leg.toUpperCase()+' leg · pose '+f.pose+'/6 · '+f.label+' · support tread '+f.supportTread:'')};function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){let next=index+1;if(cycleOnly){if(index<8||index>=31)next=8}else if(next>=timeline.length){if(document.getElementById('loop').checked)next=0;else return stop()}index=next;render();timer=setTimeout(tick,timeline[index].durationMs)}function play(){cycleOnly=false;stop();timer=setTimeout(tick,timeline[index].durationMs)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();cycleOnly=false;index=0;render();play()};document.getElementById('cycle').onclick=()=>{stop();cycleOnly=true;index=8;render();timer=setTimeout(tick,timeline[index].durationMs)};document.getElementById('contacts').onchange=e=>stages.forEach(({el})=>el.classList.toggle('showContacts',e.target.checked));document.getElementById('banister').onchange=e=>stages.forEach(({el})=>el.classList.toggle('hideBanister',!e.target.checked));document.getElementById('opacity').oninput=e=>{const value=Number(e.target.value);document.getElementById('opacityValue').value=value+'%';document.querySelectorAll('.foregroundBanister').forEach(el=>el.style.opacity=String(value/100))};Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique frame and guide images decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A frame failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@6', status: 'draft-v6-equal-leg-fourteen-contact-ascent-awaiting-review',
  rejectionOfV5: 'V5 did not divide the work 50/50 and allowed the left boot below the stair surface.',
  correction: { ...geometry, contactOrder: Array.from({ length: 14 }, (_, index) => index % 2 === 0 ? 'left' : 'right'), rootRunLp: rootRun, rootRiseFactor },
  artwork: { separateLeftLegPass: true, separateRightLegPass: true, upperBodyLockedThroughY212: true, transparentCells: true, promoted: false },
  unchanged: { v1ThroughV5: true, approvedWalkSourcePixels: true, finalLane: true, production: true },
}
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v6.json')
writeJson(specPath, spec)
const frameUrls = [...walkUrls, ...legUrls.left, ...legUrls.right, guideUrls.left, guideUrls.right]
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v6', status: spec.status,
  authorities: { rejectedV5: { file: rel(v5RegisterPath), sha256: sha(v5RegisterPath) }, approvedSideMaster: { file: rel(sideAuthorityPath), sha256: sha(sideAuthorityPath) }, sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) }, contactRig: { file: rel(rigPath), sha256: sha(rigPath) } },
  generation: { mode: 'separate-built-in-image-generation-left-and-right-passes-plus-deterministic-registration-upper-body-lock-and-exact-mirror', frameUrls },
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls,
  validation: { leftContacts: 7, rightContacts: 7, adjacentTreadOnly: true, framesPerStep: 6, cadencePreserved: true, upperBodyStable: true, edgeAlphaZero: true, exactFlightClosure: true, v1ThroughV5Changed: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V6\n\nStatus: equal-leg fourteen-contact draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v6/\`.\n\nV6 rejects the V3–V5 climb artwork and preserves all prior evidence. It uses separately authored six-pose left- and right-leg steps, repeated as seven exact LEFT/RIGHT pairs over fourteen adjacent treads. Six 60 ms drawings preserve the prior per-step cadence while smoothing each action. The exact route remains 84 lp run × 60 lp rise. Nothing is approved or promoted.\n`)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, leftContacts: 7, rightContacts: 7, uniqueAssets: frameUrls.length }, null, 2))
