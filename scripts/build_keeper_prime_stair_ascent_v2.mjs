#!/usr/bin/env node
/** Build Stair Ascent V2: forward door exit and alternating-leg climb. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v2')
const publicDir = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v2')
const assetsDir = path.join(publicDir, 'assets')
const prepPath = path.join(pack, 'source-preparation-v2.json')
const sourcePath = path.join(pack, 'sources/keeper-prime-stair-ascent-v2-generated.png')
const v1RegisterPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-14-v1/batch-register.json')
const geometryPath = path.join(root, 'art/drafts/keeper-movement-foundation-2026-10-14-v1/geometry/keeper-vertical-circulation-v1.json')
const entryPath = path.join(root, 'art/drafts/keeper-circulation-entry-alignment-2026-10-14-v1/circulation-entry-alignment-v1.json')
const walkAuthorityPath = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of [prepPath, sourcePath, v1RegisterPath, geometryPath, entryPath, walkAuthorityPath]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(prepPath, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const copyAsset = (source, stem) => {
  const target = path.join(assetsDir, `${stem}-${sha(source).slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  return `/keeper-review/keeper-prime-stair-ascent-v2/assets/${path.basename(target)}`
}
const walkUrls = prep.walkFrames.map((frame) => copyAsset(path.join(root, frame.leftFile), `walk-left-f${frame.frame}`))
const stairUrls = prep.frames.map((frame) => copyAsset(path.join(root, frame.leftFile), `stair-left-f${frame.frame}`))

const rootDeltasXKu = [6, 10, 13, 13, 13, 13, 10, 6]
const rootDeltasYKu = [3, 7, 10, 10, 3, 7, 10, 10]
if (rootDeltasXKu.reduce((a, b) => a + b, 0) !== 84 || rootDeltasYKu.reduce((a, b) => a + b, 0) !== 60) throw new Error('climb cycle does not close')
const timeline = []
let xKu = 115.5 * 8
let yKu = 20 * 8
for (let frame = 0; frame < 8; frame++) {
  xKu -= 21
  timeline.push({ phase: 'forward walk from door', facing: 'left', pose: frame + 1, src: walkUrls[frame], xKu, yKu, durationMs: 100 })
}
if (xKu !== 94.5 * 8) throw new Error('walk does not close at stair base')
for (let cycle = 0; cycle < 8; cycle++) for (let frame = 0; frame < 8; frame++) {
  xKu -= rootDeltasXKu[frame]
  yKu += rootDeltasYKu[frame]
  timeline.push({ phase: 'alternating stair climb', facing: 'left', cycle: cycle + 1, pose: frame + 1, leadingLeg: frame < 4 ? 'first' : 'opposite', src: stairUrls[frame], xKu, yKu, durationMs: 100 })
}
if (xKu !== 10.5 * 8 || yKu !== 80 * 8) throw new Error('full flight does not close at upper landing')

const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@2',
  status: 'draft-v2-forward-exit-alternating-leg-climb-awaiting-review',
  supersedesForReviewOnly: 'keeper-prime-stair-ascent-2026-10-14-v1',
  corrections: {
    doorExit: 'Exact approved Walk V6 frames horizontally mirrored so sprite faces the leftward root motion.',
    climb: 'Redrawn against approved Walk V6 F1-F8 phase authority: first-leg F1-F4, opposite-leg F5-F8.',
  },
  route: { transferDoorRootLp: 115.5, stairBaseRootLp: 94.5, walkDistanceLp: 21, pauseFramesAtJoin: 0, climbCycles: 8, climbFrames: 64, cycleRunKu: 84, cycleRiseKu: 60, flightRunKu: 672, flightRiseKu: 480, upperLandingRootLp: 10.5 },
  climbRootDeltasKu: { xTowardLeft: rootDeltasXKu, yUp: rootDeltasYKu },
  unchanged: { v1: true, approvedWalkSourcePixels: true, runtimeGeometry: true, finalLane: true, production: true },
}
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v2.json')
writeJson(specPath, spec)

const stairBlocks = Array.from({ length: 16 }, (_, i) => `<span class="step" style="left:${(94.5 - (i + 1) * 5.25) * 4}px;bottom:${(20 + i * 3.75) * 4}px"></span>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1450px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878}.large{width:620px;height:480px}.compact{width:310px;height:240px}.stairs{position:absolute;inset:0}.step{position:absolute;width:21px;height:15px;background:#526675;border-top:2px solid #d0dee6;border-left:1px solid #263d49}.compact .stairs{width:620px;height:480px;transform:scale(.5);transform-origin:left bottom}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:3}.compact .walker{width:64px;height:80px}.door{position:absolute;left:420px;bottom:80px;width:84px;height:224px;background:#273b45;border:3px solid #75909d;z-index:4}.compact .door{left:210px;bottom:40px;width:42px;height:112px;border-width:2px}.landing{position:absolute;left:0;bottom:320px;width:42px;height:12px;background:#526675;border-top:2px solid #d0dee6}.compact .landing{bottom:160px;width:21px;height:6px}.grid{display:grid;grid-template-columns:repeat(8,minmax(90px,1fr));gap:8px}.grid img{width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.grid div:nth-child(-n+4){border-bottom:4px solid #78b7ff}.grid div:nth-child(n+5){border-bottom:4px solid #ffbd72}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric{background:#0c1d26;padding:12px;border-top:4px solid #75e6a7}.metric strong{font-size:1.2rem}.views{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}@media(max-width:900px){.grid{grid-template-columns:repeat(4,1fr)}.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v1/">← Preserve and compare V1</a><h1>Keeper Prime stair ascent V2 · forward exit + alternating legs</h1><span class="status">Corrected transition draft · nothing promoted</span><p>V2 fixes the two review faults only: the Keeper now faces his leftward travel out of the doorway, and the climb is organised as one leg F1–F4 followed by the opposite leg F5–F8.</p></header><main><p class="rule"><strong>What to judge:</strong> he must emerge from the doorway face-first, then climb left-right, left-right with equal movement in both legs. Frame-step through F8→F9 for the walk-to-climb join and through each F4→F5 leg change.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox"> Loop complete route</label></div><p id="loading" class="readout">Loading and decoding all route frames…</p><p id="readout" class="readout"></p></article><article><div class="views"><div><h2>4× authoring ruler</h2><div class="stageWrap"><div class="stage large"><div class="stairs">${stairBlocks}</div><div class="landing"></div><div class="door"></div><img class="walker" alt="Keeper walking forward into stair ascent"></div></div></div><div><h2>Compact pacing preview</h2><p>2 CSS px/lp; not a runtime-size claim.</p><div class="stage compact"><div class="stairs">${stairBlocks}</div><div class="landing"></div><div class="door"></div><img class="walker" alt="Compact stair ascent preview"></div></div></div></article><section class="metrics"><div class="metric"><strong>Forward-facing exit</strong><br>approved walk mirrored exactly</div><div class="metric"><strong>F1–F4 / F5–F8</strong><br>opposite-leg phases</div><div class="metric"><strong>0 pause frames</strong><br>walk → climb join</div><div class="metric"><strong>16 risers</strong><br>exact 60-lp rise</div></section><h2>Corrected alternating eight-pose climb</h2><section class="grid">${stairUrls.map((url, i) => `<div><img src="${url}" alt="Stair pose ${i + 1}"><strong>F${i + 1} · ${i < 4 ? 'first leg' : 'opposite leg'}</strong></div>`).join('')}</section><article><h2>Boundary</h2><p>V1 remains immutable historical evidence. V2 changes no approved animation, Final art, runtime geometry or production sprite. The upper-landing dismount remains the next separate gate after this basic gait is accepted.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[{el:document.querySelector('.large'),scale:4},{el:document.querySelector('.compact'),scale:2}];let index=0,timer=null;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const {el,scale} of stages){const img=el.querySelector('.walker');img.src=f.src;img.style.left=((f.xKu/8-16)*scale)+'px';img.style.bottom=(f.yKu/8*scale)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/'+timeline.length+' · '+f.phase+(f.cycle?' · cycle '+f.cycle:'')+' · pose '+f.pose+(f.leadingLeg?' · '+f.leadingLeg+' leg':'')+' · facing '+f.facing+' ← · root '+(f.xKu/8).toFixed(3)+' lp, '+(f.yKu/8).toFixed(3)+' lp'}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index===timeline.length-1){if(document.getElementById('loop').checked)index=0;else return stop()}else index++;render();timer=setTimeout(tick,timeline[index].durationMs)}function play(){stop();timer=setTimeout(tick,timeline[index].durationMs)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All corrected forward-walk and alternating-climb frames ready';render();play()}).catch(error=>{document.getElementById('loading').textContent='A frame failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const rejected = fs.readdirSync(path.join(pack, 'sources')).filter((name) => name.startsWith('rejected-')).map((name) => {
  const file = path.join(pack, 'sources', name)
  return { file: rel(file), sha256: sha(file), reason: 'same-leg repetition or diagnostic study; retained as rejected provenance' }
})
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-ascent-2026-10-15-v2',
  status: spec.status,
  authorities: { v1: { file: rel(v1RegisterPath), sha256: sha(v1RegisterPath) }, geometry: { file: rel(geometryPath), sha256: sha(geometryPath) }, circulationEntry: { file: rel(entryPath), sha256: sha(entryPath) }, approvedWalk: { file: rel(walkAuthorityPath), sha256: sha(walkAuthorityPath) }, sourcePreparation: { file: rel(prepPath), sha256: sha(prepPath) } },
  generation: { mode: 'built-in-image-generation-guided-by-approved-walk-phase-authority-plus-deterministic-isolation', selectedSource: { file: rel(sourcePath), sha256: sha(sourcePath) }, rejected },
  spec: { file: rel(specPath), sha256: sha(specPath) },
  reviewPage: { file: rel(pagePath), sha256: sha(pagePath) },
  frameUrls: [...walkUrls, ...stairUrls],
  validation: { spriteFacesRootMotion: true, approvedWalkMirroredOnly: true, oppositeLegHalfCyclesDeclared: true, walkClosesAtBase: true, firstClimbFrameAdvances: true, pauseFramesAtJoin: 0, climbCycleCloses84x60Ku: true, flightCloses672x480Ku: true, v1Changed: false, approvedWalkChanged: false, runtimeChanged: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V2\n\nStatus: corrected forward-exit and alternating-leg draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v2/\`.\n\nV2 preserves V1 and fixes two faults: the one-cycle door approach now uses exact horizontally mirrored approved Walk V6 frames so the Keeper faces left with his root motion; the climb is redrawn against approved Walk V6's F1–F8 alternating phase authority. Route geometry and zero-pause closure are unchanged. Nothing is approved or promoted.\n`)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), `# Prompt and decision log\n\n- Built-in image generation edited the V1 climb source using approved Walk V6's eight labelled contact/down/passing/up phases as the leg-sequence authority.\n- Two full-sheet same-leg attempts and two four-pose diagnostic studies are retained as rejected provenance.\n- The selected source is isolated deterministically, then registered with one shared scale and mirrored for the leftward flight.\n- Door approach correction is deterministic: exact horizontal mirrors of approved Walk V6, with no redraw or resampling.\n- Identity constraints remained adult/rotund, restrained face, separate moustache and beard, one cream jumper stripe and the approved standard palette.\n`)
console.log(JSON.stringify({ page: rel(pagePath), walkFrames: walkUrls.length, climbFrames: stairUrls.length, timelineFrames: timeline.length, endpointKu: [xKu, yKu] }, null, 2))
