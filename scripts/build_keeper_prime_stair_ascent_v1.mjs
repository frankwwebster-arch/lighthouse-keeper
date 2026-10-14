#!/usr/bin/env node
/** Build the first reversible Keeper Prime walk-to-stair-ascent review. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-14-v1')
const publicDir = path.join(root, 'public/keeper-review/keeper-prime-stair-ascent-v1')
const assetsDir = path.join(publicDir, 'assets')
const preparation = path.join(pack, 'source-preparation-v1.json')
const generatedSource = path.join(pack, 'sources/keeper-prime-stair-ascent-8pose-generated.png')
const magentaSource = path.join(pack, 'sources/keeper-prime-stair-ascent-8pose-magenta.png')
const rejectedSource = path.join(pack, 'sources/rejected-less-varied-stair-ascent.png')
const geometryAuthority = path.join(root, 'art/drafts/keeper-movement-foundation-2026-10-14-v1/geometry/keeper-vertical-circulation-v1.json')
const entryAuthority = path.join(root, 'art/drafts/keeper-circulation-entry-alignment-2026-10-14-v1/circulation-entry-alignment-v1.json')
const walkAuthority = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json')
const walkReview = path.join(root, 'public/keeper-review/keeper-prime-walk-stop-turn-back-v2/index.html')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [preparation, generatedSource, magentaSource, rejectedSource, geometryAuthority, entryAuthority, walkAuthority, walkReview]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
const prep = JSON.parse(fs.readFileSync(preparation, 'utf8'))
const geometry = JSON.parse(fs.readFileSync(geometryAuthority, 'utf8'))
const entry = JSON.parse(fs.readFileSync(entryAuthority, 'utf8'))
fs.mkdirSync(assetsDir, { recursive: true })

const stairUrls = []
for (const record of prep.frames) {
  const source = path.join(root, record.leftFile)
  const target = path.join(assetsDir, `stair-left-f${record.frame}-${sha(source).slice(0, 16)}.png`)
  fs.copyFileSync(source, target)
  stairUrls.push(`/keeper-review/keeper-prime-stair-ascent-v1/assets/${path.basename(target)}`)
}
const walkHtml = fs.readFileSync(walkReview, 'utf8')
const walkUrls = [...new Set([...walkHtml.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/walk-frame([1-8])-[A-Za-z0-9]+\.png/g)].sort((a, b) => Number(a[1]) - Number(b[1])).map((match) => match[0]))]
if (walkUrls.length !== 8) throw new Error(`expected eight approved walk URLs, got ${walkUrls.length}`)

const rootDeltasXKu = [6, 10, 13, 13, 13, 13, 10, 6]
const rootDeltasYKu = [3, 7, 10, 10, 3, 7, 10, 10]
if (rootDeltasXKu.reduce((a, b) => a + b, 0) !== 84 || rootDeltasYKu.reduce((a, b) => a + b, 0) !== 60) throw new Error('climb cycle does not close')
const timeline = []
let xKu = 115.5 * 8
let yKu = 20 * 8
for (let frame = 0; frame < 8; frame++) {
  xKu -= 21
  timeline.push({ phase: 'walk', pose: frame + 1, src: walkUrls[frame], xKu, yKu, durationMs: 100 })
}
if (xKu !== 94.5 * 8) throw new Error('walk does not close at stair base')
for (let cycle = 0; cycle < 8; cycle++) for (let frame = 0; frame < 8; frame++) {
  xKu -= rootDeltasXKu[frame]
  yKu += rootDeltasYKu[frame]
  timeline.push({ phase: 'climb', cycle: cycle + 1, pose: frame + 1, src: stairUrls[frame], xKu, yKu, durationMs: 100 })
}
if (xKu !== 10.5 * 8 || yKu !== 80 * 8) throw new Error('full flight does not close at upper landing')
const spec = {
  schema: 'lighthouse-keeper/prime-stair-ascent@1',
  status: 'draft-finished-art-walk-to-continuous-ascent-awaiting-review',
  direction: 'bottom-right-to-top-left',
  art: { frames: 8, fps: 10, cell: [256, 320], mirroredFromAuthoredRight: true },
  route: {
    transferDoorRootLp: 115.5,
    stairBaseRootLp: 94.5,
    approvedWalkFrames: 8,
    walkDistanceLp: 21,
    pauseFramesAtJoin: 0,
    climbCycles: 8,
    climbFrames: 64,
    cycleRunKu: 84,
    cycleRiseKu: 60,
    flightRunKu: 672,
    flightRiseKu: 480,
    upperLandingRootLp: 10.5,
  },
  climbRootDeltasKu: { xTowardLeft: rootDeltasXKu, yUp: rootDeltasYKu },
  endpointBoundary: 'Ends in continuous climb phase; upper-landing dismount/stop/walk is intentionally not proposed in V1.',
  unchanged: { approvedWalkPixels: true, runtimeGeometry: true, finalLane: true, production: true },
}
const specPath = path.join(pack, 'keeper-prime-stair-ascent-v1.json')
writeJson(specPath, spec)

const stairBlocks = Array.from({ length: 16 }, (_, i) => `<span class="step" style="left:${(94.5 - (i + 1) * 5.25) * 4}px;bottom:${(20 + i * 3.75) * 4}px"></span>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair ascent V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1450px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}article{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.stageWrap{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878}.large{width:620px;height:480px}.compact{width:310px;height:240px}.stairs{position:absolute;inset:0}.step{position:absolute;width:21px;height:15px;background:#526675;border-top:2px solid #d0dee6;border-left:1px solid #263d49}.compact .stairs{width:620px;height:480px;transform:scale(.5);transform-origin:left bottom}.walker{position:absolute;width:128px;height:160px;object-fit:contain;z-index:3}.compact .walker{width:64px;height:80px}.door{position:absolute;left:420px;bottom:80px;width:84px;height:224px;background:#273b45;border:3px solid #75909d;z-index:4}.compact .door{left:210px;bottom:40px;width:42px;height:112px;border-width:2px}.landing{position:absolute;left:0;bottom:320px;width:42px;height:12px;background:#526675;border-top:2px solid #d0dee6}.compact .landing{bottom:160px;width:21px;height:6px}.grid{display:grid;grid-template-columns:repeat(8,minmax(90px,1fr));gap:8px}.grid img{width:100%;background:repeating-conic-gradient(#273640 0 25%,#1b2831 0 50%) 50%/16px 16px}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric{background:#0c1d26;padding:12px;border-top:4px solid #75e6a7}.metric strong{font-size:1.3rem}.views{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}@media(max-width:900px){.grid{grid-template-columns:repeat(4,1fr)}.metrics{grid-template-columns:1fr 1fr}}
</style></head><body><header><a href="/keeper-review/keeper-circulation-entry-alignment-v1/">← Circulation entry construction</a><h1>Keeper Prime stair ascent V1 · walk directly into continuous climb</h1><span class="status">Finished-art transition draft · nothing promoted</span><p>First stair gate only: one exact approved leftward walk cycle enters a new eight-pose climb cycle, repeated across the measured 16-riser flight.</p></header><main><p class="rule"><strong>What to judge:</strong> does Walk F8 hand into the first advancing climb pose without a stop, jump or change of Keeper identity? Then watch whether every boot appears to meet the treads naturally over the complete flight.</p><article><div class="controls"><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox"> Loop complete route</label></div><p id="loading" class="readout">Loading and decoding all route frames…</p><p id="readout" class="readout"></p></article><article><div class="views"><div><h2>4× authoring ruler</h2><div class="stageWrap"><div class="stage large"><div class="stairs">${stairBlocks}</div><div class="landing"></div><div class="door"></div><img class="walker" alt="Keeper walking into stair ascent"></div></div></div><div><h2>Compact pacing preview</h2><p>2 CSS px/lp; not a runtime-size claim.</p><div class="stage compact"><div class="stairs">${stairBlocks}</div><div class="landing"></div><div class="door"></div><img class="walker" alt="Compact stair ascent preview"></div></div></div></article><section class="metrics"><div class="metric"><strong>0 pause frames</strong><br>walk → climb join</div><div class="metric"><strong>16 risers</strong><br>3.75 lp each</div><div class="metric"><strong>84 lp run</strong><br>eight climb cycles</div><div class="metric"><strong>60 lp rise</strong><br>exact floor pitch</div></section><h2>New eight-pose climbing cycle</h2><section class="grid">${stairUrls.map((url, i) => `<div><img src="${url}" alt="Stair pose ${i + 1}"><strong>F${i + 1}</strong></div>`).join('')}</section><article><h2>Boundary and next gate</h2><p>This draft deliberately ends while the Keeper is still climbing. It does not invent the upper-landing dismount. If the walk-to-climb join and repeating gait are accepted, the next separate gate is climb → upper landing → stop → walk, followed by descent and the opposite zigzag parity. No approved art, runtime geometry, Final or production file changes here.</p></article></main><script>
const timeline=${JSON.stringify(timeline)},buttons=[...document.querySelectorAll('button')],stages=[{el:document.querySelector('.large'),scale:4},{el:document.querySelector('.compact'),scale:2}];let index=0,timer=null;const unique=[...new Set(timeline.map(f=>f.src))];function render(){const f=timeline[index];for(const {el,scale} of stages){const img=el.querySelector('.walker');img.src=f.src;img.style.left=((f.xKu/8-16)*scale)+'px';img.style.bottom=((f.yKu/8)*scale)+'px'}document.getElementById('readout').textContent='F'+(index+1)+'/'+timeline.length+' · '+f.phase+(f.cycle?' cycle '+f.cycle:'')+' · pose '+f.pose+' · root '+(f.xKu/8).toFixed(3)+' lp, '+(f.yKu/8).toFixed(3)+' lp'}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(index===timeline.length-1){if(document.getElementById('loop').checked)index=0;else{return stop()}}else index++;render();timer=setTimeout(tick,timeline[index].durationMs)}function play(){stop();timer=setTimeout(tick,timeline[index].durationMs)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=(index-1+timeline.length)%timeline.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%timeline.length;render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};Promise.all(unique.map(preload)).then(()=>{buttons.forEach(b=>b.disabled=false);document.getElementById('loading').textContent='All approved walk and draft climb frames ready';render();play()}).catch(error=>{document.getElementById('loading').textContent='A frame failed to load; playback remains locked. '+error.message});
</script></body></html>`
fs.mkdirSync(publicDir, { recursive: true })
const page = path.join(publicDir, 'index.html')
fs.writeFileSync(page, html)
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-ascent-2026-10-14-v1',
  status: spec.status,
  authorities: {
    geometry: { file: rel(geometryAuthority), sha256: sha(geometryAuthority) },
    circulationEntry: { file: rel(entryAuthority), sha256: sha(entryAuthority) },
    approvedWalk: { file: rel(walkAuthority), sha256: sha(walkAuthority) },
    sourcePreparation: { file: rel(preparation), sha256: sha(preparation) },
  },
  generation: {
    mode: 'built-in-image-generation-with-deterministic-chroma-isolation',
    selectedRawSource: { file: rel(generatedSource), sha256: sha(generatedSource) },
    isolationSource: { file: rel(magentaSource), sha256: sha(magentaSource) },
    rejectedSource: { file: rel(rejectedSource), sha256: sha(rejectedSource), reason: 'less gait variation across the eight requested poses' },
  },
  spec: { file: rel(specPath), sha256: sha(specPath) },
  reviewPage: { file: rel(page), sha256: sha(page) },
  frameUrls: stairUrls,
  validation: { walkClosesAtBase: true, firstClimbFrameAdvances: true, pauseFramesAtJoin: 0, climbCycleCloses84x60Ku: true, flightCloses672x480Ku: true, approvedWalkPixelsChanged: false, runtimeChanged: false, finalChanged: false, productionChanged: false },
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V1\n\nStatus: finished-art walk-to-continuous-ascent draft awaiting Frank's review.\n\nReview: \`/keeper-review/keeper-prime-stair-ascent-v1/\`.\n\nThe route uses one exact approved mirrored Walk V6 cycle from the registered transfer door to the stair base, then immediately enters an advancing eight-pose climb cycle repeated eight times across the exact 16-riser, 84-lp-run, 60-lp-rise flight. There are zero pause frames at the join. The upper-landing dismount is intentionally left for the next gate. Nothing is approved or promoted.\n`)
fs.writeFileSync(path.join(pack, 'PROMPT_LOG.md'), `# Prompt and decision log\n\n- Built-in image generation used the approved Side-right master and Walk V6 arm guide.\n- The first generated eight-pose sheet is retained unchanged. A less varied second render is retained as rejected provenance.\n- A magenta-background extraction pass was requested because the generator did not honor transparent output; deterministic chroma removal isolates the poses.\n- Shared scale and registration are deterministic; no per-frame scaling or creative pixel warp is used.\n- Eight authored right-facing poses are mirrored for the bottom-right-to-top-left flight.\n- Identity constraints: adult restrained face, solid dark rectangular eye, separate moustache and closed mouth, established beard, single pale jumper stripe, fixed palette and rotund body.\n`)
console.log(JSON.stringify({ page: rel(page), frames: stairUrls.length, timelineFrames: timeline.length, endpoint: [xKu, yKu] }, null, 2))
