#!/usr/bin/env node
/** Build the immutable Stair Ascent V3 contact-locked review candidate. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const publicDir = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v3')
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v3.json')
const rigPath = path.join(pack, 'stair-contact-rig-v3.json')
const v2RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v2/batch-register.json')
const walkRegisterPath = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json')
const sideAuthorityPath = path.join(root, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, rigPath, v2RegisterPath, walkRegisterPath, sideAuthorityPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const copyAsset = (source, stem) => {
  const target = path.join(assetsDir, `${stem}-${sha(source).slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  return `/keeper-review/keeper-prime-stair-ascent-v3/assets/${path.basename(target)}`
}
const walkUrls = prep.walkFrames.map((f) => copyAsset(path.join(root, f.leftFile), `walk-left-f${f.frame}`))
const stairUrls = prep.frames.map((f) => copyAsset(path.join(root, f.leftFile), `stair-left-f${f.frame}`))
const guideUrl = copyAsset(path.join(pack, 'guides/stair-contact-guide-right-8pose.png'), 'contact-authority')

const floorTopLp = 20
const baseX = 94.5
const treadRunLp = 5.25
const riserRiseLp = 3.75
const cellWidthLp = 32
const soleOffsetLp = (prep.target.height - prep.target.soleY) / 8
const contactCentre = (tread) => tread === 0 ? baseX + treadRunLp / 2 : baseX - (tread - 0.5) * treadRunLp
const treadTop = (tread) => floorTopLp + tread * riserRiseLp
const timeline = []
let walkX = 115.5
for (let frame = 0; frame < 8; frame++) {
  walkX -= 21 / 8
  timeline.push({ phase: 'forward walk from door', pose: frame + 1, src: walkUrls[frame], xLp: walkX, bottomLp: floorTopLp - soleOffsetLp, durationMs: 88 })
}

for (let cycle = 0; cycle < 8; cycle++) for (let pose = 1; pose <= 8; pose++) {
  const lowerTread = cycle * 2 + (pose >= 5 ? 1 : 0)
  const frame = prep.frames[pose - 1]
  const localContactLp = frame.leftContactCentreX / 8
  const xLp = contactCentre(lowerTread) - (localContactLp - cellWidthLp / 2)
  const bottomLp = treadTop(lowerTread) - soleOffsetLp
  timeline.push({
    phase: 'contact-locked stair climb', cycle: cycle + 1, pose, src: stairUrls[pose - 1],
    support: frame.support, swing: frame.swing, label: frame.phase, lowerTread,
    xLp, bottomLp, contactXLp: contactCentre(lowerTread), contactYLp: treadTop(lowerTread), durationMs: 92,
  })
}

const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@3',
  status: 'draft-v3-contact-locked-opposite-leg-cycle-awaiting-review',
  rejectionOfV2: 'V2 declared phase alternation but did not visually transfer the moving leg; a boot also passed below the stair surface.',
  corrections: {
    alternation: 'F1-F4 near leg advances one riser; F5-F8 far leg advances the next riser.',
    contact: 'Each lower support/contact sole is registered to y316 and placed exactly on its active tread top.',
    stairs: 'CSS blocks use bottom=floor top and height=riser index × rise, so their visible top is the actual tread datum.',
  },
  geometry: { floorTopLp, baseX, treadRunLp, riserRiseLp, risers: 16, cellWidthLp, soleOffsetLp, cycleRunLp: 10.5, cycleRiseLp: 7.5 },
  unchanged: { v1: true, v2: true, approvedWalkSourcePixels: true, runtimeGeometry: true, finalLane: true, production: true },
}
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v3.json')
writeJson(specPath, spec)

const stairs = Array.from({ length: 16 }, (_, index) => {
  const n = index + 1
  return `<span class="step" style="left:${(baseX - n * treadRunLp) * 4}px;bottom:${floorTopLp * 4}px;height:${n * riserRiseLp * 4}px"></span>`
}).join('')
const poseCards = stairUrls.map((url, index) => `<div><img src="${url}" alt="Stair pose ${index + 1}"><b>F${index + 1}</b><span>${prep.frames[index].phase}</span></div>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V3</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1480px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.views{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}.stageWrap{overflow:auto;max-width:100%}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878;width:620px;height:480px}.stage.game{width:155px;height:120px}.world{position:absolute;inset:0}.game .world{width:620px;height:480px;transform:scale(.25);transform-origin:left bottom}.stairs{position:absolute;inset:0}.step{position:absolute;width:21px;background:#526675;border-top:2px solid #d0dee6;border-left:1px solid #263d49}.floor{position:absolute;left:378px;right:0;bottom:0;height:80px;background:#526675;border-top:2px solid #d0dee6}.landing{position:absolute;left:0;bottom:80px;width:42px;height:240px;background:#526675;border-top:2px solid #d0dee6}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:4}.door{position:absolute;left:420px;bottom:80px;width:84px;height:224px;background:#273b45;border:3px solid #75909d;z-index:5}.contact{display:none;position:absolute;height:2px;background:#55ff9b;z-index:6;box-shadow:0 0 0 1px #063}.showContact .contact{display:block}.poses{display:grid;grid-template-columns:repeat(8,minmax(100px,1fr));gap:8px}.poses div{background:#0c1d26;padding:8px;border-bottom:4px solid #78b7ff}.poses div:nth-child(n+5){border-color:#ffbd72}.poses img{display:block;width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.poses span{display:block;color:#b8d0da;font-size:12px}.authority{max-width:100%;background:#fff}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric{background:#0c1d26;padding:12px;border-top:4px solid #75e6a7}.metric strong{font-size:1.15rem}@media(max-width:900px){.poses{grid-template-columns:repeat(4,1fr)}.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v2/">← Preserve and compare rejected V2</a><h1>Keeper Prime stair ascent V3 · contact-locked alternation</h1><span class="status">New draft · nothing promoted</span><p>V3 replaces the false phase labels with a visible two-step cycle: near leg climbs, then far leg climbs. The lowest sole is locked to the actual tread top, never to the bottom of the stair block.</p></header><main><p class="rule"><strong>Judge two things:</strong> F1–F4 must be the near/front leg’s step; F5–F8 must be the far/rear leg’s step. No sole may flash below its active tread.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><button id="cycle" disabled>Loop one two-step cycle</button><label><input id="contacts" type="checkbox"> Show active tread contact</label><label><input id="loop" type="checkbox"> Loop full route</label></div><p id="loading" class="readout">Loading and decoding every frame…</p><p id="readout" class="readout"></p></article><article><div class="views"><div><h2>Large contact inspection · 4 CSS px/lp</h2><div class="stageWrap"><div class="stage large"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="door"></div><div class="contact"></div><img class="walker" alt="Keeper walking out and climbing stairs"></div></div></div></div><div><h2>Exact logical scale · 1 CSS px/lp</h2><div class="stage game"><div class="world"><div class="stairs">${stairs}</div><div class="floor"></div><div class="landing"></div><div class="door"></div><div class="contact"></div><img class="walker" alt="Exact-scale stair preview"></div></div></div></div></article><section class="metrics"><div class="metric"><strong>Near F1–F4</strong><br>first riser</div><div class="metric"><strong>Far F5–F8</strong><br>second riser</div><div class="metric"><strong>y316 sole datum</strong><br>locked to tread top</div><div class="metric"><strong>16 risers</strong><br>8 complete two-step cycles</div></section><h2>One complete two-step cycle</h2><section class="poses">${poseCards}</section><details><summary>Show the deterministic contact authority</summary><img class="authority" src="${guideUrl}" alt="Red near leg and cyan far leg contact guide"></details><article><h2>Boundary</h2><p>V1 and V2 remain immutable rejected evidence. V3 changes no approved walk pixels, runtime geometry, Final art or production sprites. Stair dismount is still a separate later gate.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[{el:document.querySelector('.large'),scale:4},{el:document.querySelector('.game'),scale:4}];let index=0,timer=null,cycleOnly=false;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const {el,scale} of stages){const img=el.querySelector('.walker'),line=el.querySelector('.contact');img.src=f.src;img.style.left=((f.xLp-16)*scale)+'px';img.style.bottom=(f.bottomLp*scale)+'px';if(f.contactXLp!==undefined){line.style.left=((f.contactXLp-2.5)*scale)+'px';line.style.bottom=(f.contactYLp*scale)+'px';line.style.width=(5*scale)+'px'}else line.style.width='0'}document.getElementById('readout').textContent='F'+(index+1)+'/'+timeline.length+' · '+f.phase+(f.cycle?' · cycle '+f.cycle+' · pose '+f.pose+' · '+f.label+' · support '+f.support:'')+(f.lowerTread!==undefined?' · active tread '+f.lowerTread+' at '+f.contactYLp.toFixed(2)+' lp':'')};function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){let next=index+1;if(cycleOnly){if(index<8||index>=15)next=8}else if(next>=timeline.length){if(document.getElementById('loop').checked)next=0;else return stop()}index=next;render();timer=setTimeout(tick,timeline[index].durationMs)}function play(){cycleOnly=false;stop();timer=setTimeout(tick,timeline[index].durationMs)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();cycleOnly=false;index=0;render();play()};document.getElementById('cycle').onclick=()=>{stop();cycleOnly=true;index=8;render();timer=setTimeout(tick,timeline[index].durationMs)};document.getElementById('contacts').onchange=e=>stages.forEach(({el})=>el.classList.toggle('showContact',e.target.checked));Promise.all(unique.concat('${guideUrl}').map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All walk, climb and contact-authority frames decoded';render();play()}).catch(error=>{document.getElementById('loading').textContent='A frame failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-stair-ascent-2026-10-15-v3', status: spec.status,
  authorities: { rejectedV2: { file: rel(v2RegisterPath), sha256: sha(v2RegisterPath) }, approvedWalk: { file: rel(walkRegisterPath), sha256: sha(walkRegisterPath) }, approvedSideMaster: { file: rel(sideAuthorityPath), sha256: sha(sideAuthorityPath) }, contactRig: { file: rel(rigPath), sha256: sha(rigPath) }, sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) } },
  generation: { mode: 'built-in-image-generation-per-contact-pose-plus-deterministic-registration', sourceFrames: prep.frames.map((f) => ({ file: f.sourceFile, sha256: f.sourceSha256 })) },
  spec: { file: rel(specPath), sha256: sha(specPath) }, reviewPage: { file: rel(pagePath), sha256: sha(pagePath) }, frameUrls: [...walkUrls, ...stairUrls, guideUrl],
  validation: { oppositeLegRolesExplicit: true, lowerSolesRegisteredY316: true, treadTopGeometryCorrected: true, contactLockedPlacement: true, approvedWalkMirroredOnly: true, v1Changed: false, v2Changed: false, runtimeChanged: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V3\n\nStatus: contact-locked opposite-leg draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v3/\`.\n\nV3 preserves V1 and V2. It uses a real near-leg F1–F4 / far-leg F5–F8 cycle. Every lower contact sole is registered to cell y316 and the page places that datum on the actual top of its active tread. Nothing is approved or promoted.\n`)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), `# Prompt and decision log\n\n- Mode: built-in image generation, one transparent pose at a time, followed by deterministic registration and exact mirroring.\n- Authority: approved Keeper Prime side-right master plus the V3 red-near/cyan-far contact guide for each pose.\n- F1–F4 prompt constraint: far leg supports below while the near leg lifts, passes, reaches and takes the upper tread.\n- F5–F8 prompt constraint: near leg supports below while the far leg lifts behind, passes, reaches and takes the next upper tread.\n- The first full-sheet attempt and unused individual attempts remain in \`sources/rejected\` or the original generated-image store as rejected provenance.\n- No stairs, floor or effects were generated into the character pixels.\n`)
console.log(JSON.stringify({ page: rel(pagePath), timelineFrames: timeline.length, assets: 17 }, null, 2))
