#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'keeper-prime-seated-six-view-v1'
const pack = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1')
const sourceDir = path.join(pack, 'sources/generated')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'keeper-seat-v1-'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, data) => fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`)

const authorities = {
  front: path.join(root, 'art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png'),
  sideRight: path.join(root, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f01.png'),
  rearRight: path.join(root, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f05.png'),
  back: path.join(root, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png'),
}
const legacy = {
  front: path.join(root, 'art/raw/keeper-first-batch/keeper_neutral_sitting-front_f1.png'),
  sideRight: path.join(root, 'art/raw/keeper-first-batch/keeper_neutral_sitting-side-right_f1.png'),
  rearRight: path.join(root, 'art/raw/keeper-first-batch/keeper_neutral_sitting-rear-right_f1.png'),
  back: path.join(root, 'art/raw/keeper-first-batch/keeper_neutral_sitting-back_f1.png'),
}
const generated = {
  front: path.join(sourceDir, 'keeper-prime-seated-front-generated.png'),
  sideRight: path.join(sourceDir, 'keeper-prime-seated-side-right-generated.png'),
  rearRight: path.join(sourceDir, 'keeper-prime-seated-rear-right-generated.png'),
  back: path.join(sourceDir, 'keeper-prime-seated-back-generated.png'),
}
for (const file of [...Object.values(authorities), ...Object.values(legacy), ...Object.values(generated)]) {
  if (!fs.existsSync(file)) throw new Error(`missing authority ${rel(file)}`)
}
fs.mkdirSync(frameDir, { recursive: true })
fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

function bounds(png, threshold = 0) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (png.data[(y * png.width + x) * 4 + 3] <= threshold) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  if (maxX < 0) throw new Error('empty PNG')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 }
}
function cleanSource(source, id) {
  const png = PNG.sync.read(fs.readFileSync(source))
  for (let i = 0; i < png.data.length; i += 4) {
    if (png.data[i + 3] <= 16) png.data[i] = png.data[i + 1] = png.data[i + 2] = png.data[i + 3] = 0
  }
  const b = bounds(png)
  const cropped = new PNG({ width: b.width, height: b.height })
  PNG.bitblt(png, cropped, b.minX, b.minY, b.width, b.height, 0, 0)
  const file = path.join(tempDir, `${id}-cropped.png`)
  fs.writeFileSync(file, PNG.sync.write(cropped))
  return { file, bounds: b }
}
function registerFrame(source, id) {
  const clean = cleanSource(source, id)
  const targetHeight = 264
  const targetWidth = Math.round(clean.bounds.width * targetHeight / clean.bounds.height)
  if (targetWidth > 232) throw new Error(`${id} is too wide for safety gutter: ${targetWidth}px`)
  const scaledFile = path.join(tempDir, `${id}-scaled.png`)
  const ffmpeg = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', clean.file, '-vf', `scale=${targetWidth}:${targetHeight}:flags=lanczos,format=rgba`, '-frames:v', '1', scaledFile])
  if (ffmpeg.status !== 0) throw new Error(`ffmpeg failed for ${id}: ${ffmpeg.stderr}`)
  const scaled = PNG.sync.read(fs.readFileSync(scaledFile))
  for (let i = 0; i < scaled.data.length; i += 4) if (scaled.data[i + 3] <= 3) scaled.data[i] = scaled.data[i + 1] = scaled.data[i + 2] = scaled.data[i + 3] = 0
  const b = bounds(scaled)
  const cell = new PNG({ width: 256, height: 320 })
  const dx = Math.round(127.5 - (b.minX + b.maxX) / 2)
  const dy = 315 - b.maxY
  PNG.bitblt(scaled, cell, 0, 0, scaled.width, scaled.height, dx, dy)
  const output = path.join(frameDir, `keeper_prime_neutral_sitting-${id}_f01.png`)
  fs.writeFileSync(output, PNG.sync.write(cell))
  return { id, output, source, sourceBounds: clean.bounds, registeredBounds: bounds(cell), resampling: 'LANCZOS', targetHeight }
}
function mirror(sourceRecord, id) {
  const source = PNG.sync.read(fs.readFileSync(sourceRecord.output))
  const mirrored = new PNG({ width: source.width, height: source.height })
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const si = (y * source.width + x) * 4
    const di = (y * source.width + (source.width - 1 - x)) * 4
    mirrored.data[di] = source.data[si]; mirrored.data[di + 1] = source.data[si + 1]; mirrored.data[di + 2] = source.data[si + 2]; mirrored.data[di + 3] = source.data[si + 3]
  }
  const output = path.join(frameDir, `keeper_prime_neutral_sitting-${id}_f01.png`)
  fs.writeFileSync(output, PNG.sync.write(mirrored))
  return { id, output, source: sourceRecord.output, mirrorOf: sourceRecord.id, registeredBounds: bounds(mirrored), resampling: 'none-exact-pixel-mirror', targetHeight: sourceRecord.targetHeight }
}

const front = registerFrame(generated.front, 'front')
const back = registerFrame(generated.back, 'back')
const sideRight = registerFrame(generated.sideRight, 'side-right')
const sideLeft = mirror(sideRight, 'side-left')
const rearRight = registerFrame(generated.rearRight, 'rear-right')
const rearLeft = mirror(rearRight, 'rear-left')
const frames = [front, rearLeft, sideLeft, back, sideRight, rearRight]

for (const frame of frames) {
  const pose = `sitting-${frame.id}`
  writeJson(frame.output.replace(/\.png$/, '.json'), {
    schema: 'lighthouse-keeper/sprite-sidecar@draft-1', w: 32, h: 40, frames: 1, fps: 0, density: 8,
    anchor: [16, 40], seatPoint: [16, 29], seatHeightLp: 11, floorBottomPixel: 315,
    startPose: pose, endPose: pose, pose, assetRole: 'draft-neutral-endpoint',
    mirrorOf: frame.mirrorOf ? `sitting-${frame.mirrorOf}` : null,
    productionPromotionAllowed: false,
  })
}

const contactSheet = new PNG({ width: 256 * frames.length, height: 320 })
frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame.output)), contactSheet, 0, 0, 256, 320, index * 256, 0))
const contactSheetFile = path.join(evidenceDir, 'keeper-prime-seated-six-view-v1.png')
fs.writeFileSync(contactSheetFile, PNG.sync.write(contactSheet))

const publishedByHash = new Map()
const publishedAssets = []
function publish(file, role) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const ext = path.extname(file)
  const name = `${role}-${digest.slice(0, 16)}${ext}`
  fs.copyFileSync(file, path.join(assetsDir, name))
  const record = { role, source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` }
  publishedByHash.set(digest, record); publishedAssets.push(record); return record
}
const frameRecords = Object.fromEntries(frames.map((frame) => [frame.id, publish(frame.output, `seat-${frame.id}`)]))
const authorityRecords = Object.fromEntries(Object.entries(authorities).map(([id, file]) => [id, publish(file, `standing-${id}`)]))
const legacyRecords = Object.fromEntries(Object.entries(legacy).map(([id, file]) => [id, publish(file, `legacy-seat-${id}`)]))

const geometry = {
  schema: 'lighthouse-keeper/seated-foundation@1', set, status: 'draft-awaiting-frank',
  cell: { logical: [32, 40], pixels: [256, 320], density: 8, anchorLp: [16, 40] },
  sharedDatums: { seatPointLp: [16, 29], seatHeightAboveFloorLp: 11, floorOpaqueMaximumY: 315, transparentSafetyGutterMinimumPx: 4 },
  directions: frames.map((frame) => ({ id: frame.id, pose: `sitting-${frame.id}`, image: rel(frame.output), sha256: sha(frame.output), registeredBounds: frame.registeredBounds, mirrorOf: frame.mirrorOf ?? null })),
  interpretation: 'angled views are rear-left and rear-right three-quarter seats for screen/furniture-facing activities',
  futureMotionGate: 'After endpoint approval, build standing-to-sitting and sitting-to-standing clips that land byte-exactly on these endpoints; action loops inherit the same first/last pose.',
}
const geometryFile = path.join(pack, 'keeper-prime-seated-six-view-v1.json')
writeJson(geometryFile, geometry)

const registerFile = path.join(pack, 'batch-register.json')
const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-seated-six-view-2026-10-16-v1', status: 'draft-seated-foundation-awaiting-frank',
  purpose: 'Establish six smooth Prime Keeper seated endpoint authorities before animating stand-to-sit and sit-to-stand transitions.',
  stairDescentApproval: { wording: "I'm fine with it", approvedCandidate: 'keeper-prime-stair-descent-2026-10-16-v2', acceptedLimitation: 'slight visible overstride', futureSceneryMitigation: 'two newel posts, foreground balustrade and continuous handrail may partly mask feet without changing stored tread/riser geometry' },
  authorities: Object.fromEntries(Object.entries(authorities).map(([id, file]) => [id, { file: rel(file), sha256: sha(file), immutable: true }])),
  historicalSeatedReferences: Object.fromEntries(Object.entries(legacy).map(([id, file]) => [id, { file: rel(file), sha256: sha(file), role: 'pose-and-seat-geometry-only', immutable: true }])),
  generatedSources: Object.fromEntries(Object.entries(generated).map(([id, file]) => [id, { file: rel(file), sha256: sha(file), role: 'built-in-image-edit-output' }])),
  geometry: { file: rel(geometryFile), sha256: sha(geometryFile) },
  evidence: { contactSheet: { file: rel(contactSheetFile), sha256: sha(contactSheetFile) } },
  frames: geometry.directions,
  publishedAssets,
  deterministicRegistration: { sourceAlphaThresholdRemovedAtOrBelow: 16, resampling: 'LANCZOS', registeredCellPixels: [256, 320], targetVisibleHeightPixels: 264, registeredBottomPixel: 315, leftViews: 'exact horizontal mirrors after registration' },
  boundaries: { canonicalRawChanged: false, approvedPrimeAuthoritiesChanged: false, historicalDraftsChanged: false, finalChanged: false, runtimeChanged: false, productionChanged: false, endpointApprovalGranted: false, transitionAnimationApprovalGranted: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; all authorities and earlier drafts remain untouched.`,
}
writeJson(registerFile, register)

const pageFile = path.join(publicDir, 'index.html')
const cards = frames.map((frame) => `<article><h3>${frame.id.replaceAll('-', ' ')}</h3><div class="cell cardCell"><span class="seatLine"></span><span class="floorLine"></span><img src="${frameRecords[frame.id].url}" alt="Prime Keeper seated ${frame.id}"></div></article>`).join('')
const data = frames.map((frame) => ({ id: frame.id, src: frameRecords[frame.id].url, bounds: frame.registeredBounds, sha256: sha(frame.output) }))
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime seated six-view V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1380px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px 14px}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.stageGrid{display:grid;grid-template-columns:minmax(800px,1fr) 220px;gap:24px;align-items:start}.inspection{position:relative;width:768px;height:960px;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/48px 48px;overflow:hidden}.inspection img,.game img,.cell img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:2}.guide{position:absolute;left:0;right:0;z-index:4;pointer-events:none}.seatGuide{top:72.5%;border-top:3px solid #ffca55}.floorGuide{bottom:1.25%;border-top:3px solid #62e0aa}.guideLabel{position:absolute;left:8px;font-weight:700;text-shadow:0 1px 3px #000}.seatLabel{top:calc(72.5% - 25px);color:#ffda7a}.floorLabel{bottom:2%;color:#8df2c4}.chair{position:absolute;left:25%;top:72.5%;width:50%;height:9%;border:3px solid #a67945;background:#6b4a2a;z-index:1;opacity:.8}.chair:before{content:'';position:absolute;left:0;bottom:100%;width:10%;height:135%;background:#6b4a2a;border:3px solid #a67945}.game{position:relative;width:32px;height:40px;background:#17303b;margin:16px auto}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee;min-height:3em}.cards{display:grid;grid-template-columns:repeat(3,minmax(250px,1fr));gap:14px}.cards article{background:#0c1d26;border:1px solid #2c4a59;border-radius:10px;padding:12px}.cards h3{text-transform:capitalize;margin:.1em 0 .6em}.cell{position:relative;width:256px;height:320px;margin:auto;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/16px 16px}.cardCell .seatLine{position:absolute;left:0;right:0;top:232px;border-top:1px solid #ffca55;z-index:3}.cardCell .floorLine{position:absolute;left:0;right:0;top:316px;border-top:1px solid #62e0aa;z-index:3}.metrics{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:12px}.metric b{display:block;color:#75e6a7;font-size:22px}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.compare article{background:#0c1d26;padding:12px;border-radius:10px}.compare img{width:100%;max-height:320px;object-fit:contain;background:#17303b}@media(max-width:1100px){.stageGrid{grid-template-columns:1fr}.cards{grid-template-columns:repeat(2,1fr)}.inspection{width:768px}}@media(max-width:820px){.inspection{width:100%;height:auto;aspect-ratio:4/5}.cards,.compare,.metrics{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-descent-v2/">← Approved Stair Descent V2 review</a><h1>Keeper Prime seated six-view V1</h1><span class="status">Foundation draft · no animation or production promotion</span><p>Six seated endpoints derived from Prime Keeper: direct front, direct back, either profile and rear three-quarter to either side. Approving these locks the targets for the stand ↔ sit animations.</p></header><main><p class="rule"><strong>Look for:</strong> one Keeper identity, equal registered height, stable cap/head size, the same rotund body, flat boots, and believable contact with the 11-lp seat line. The angled views are deliberately rear three-quarter—the useful view for TVs, games and furniture-facing actions.</p><section class="panel"><div class="controls"><button id="prev" disabled>← Previous view</button><button id="next" disabled>Next view →</button><button id="play" disabled>Rotate views</button><button id="pause" disabled>Pause</button><label><input id="chairToggle" type="checkbox" checked> Show neutral seat block</label></div><p id="loading" class="readout">Loading and decoding all six registered endpoint images…</p><p id="readout" class="readout"></p></section><section class="panel stageGrid"><div><h2>Large inspection</h2><div class="inspection"><div class="chair"></div><span class="guide seatGuide"></span><span class="guide floorGuide"></span><span class="guideLabel seatLabel">seat datum · y 29 lp · 11 lp above floor</span><span class="guideLabel floorLabel">registered floor / anchor</span><img id="large" alt="Selected seated Prime Keeper view"></div></div><div><h2>Exact game raster</h2><p>32 × 40 logical pixels, shown here at literal 1:1.</p><div class="game"><img id="game" alt="Exact game-scale seated Prime Keeper"></div><p>The runtime may display this logical raster at the game camera’s chosen zoom; this is the unscaled logical asset footprint.</p></div></section><section class="panel"><h2>All six registered views</h2><div class="cards">${cards}</div></section><section class="metrics"><div class="panel metric"><b>6 endpoints</b>front, back, two profiles, two rear angles</div><div class="panel metric"><b>11 lp</b>seat height above floor</div><div class="panel metric"><b>256 × 320</b>8× registered review cell</div><div class="panel metric"><b>exact mirrors</b>left pair introduces no redraw drift</div></section><section class="panel"><h2>Authority comparison</h2><p>These show the immutable approved standing authority beside the historical seated pose reference. Prime identity/rendering comes from the former; only seat mechanics came from the latter.</p><div class="compare"><article><h3>Prime front authority</h3><img src="${authorityRecords.front.url}"></article><article><h3>Historical front seat geometry</h3><img src="${legacyRecords.front.url}"></article><article><h3>Prime back authority</h3><img src="${authorityRecords.back.url}"></article></div></section><p class="warn"><strong>Approval boundary:</strong> this page asks only whether the six seated endpoint drawings are right. It does not approve the intervening stand/sit frames, an action animation, Final art, runtime sprites or production promotion.</p></main><script>
const views=${JSON.stringify(data)};const unique=[...new Set([...views.map(v=>v.src),${JSON.stringify([...Object.values(authorityRecords), ...Object.values(legacyRecords)].map(x=>x.url))}])];let index=0,timer=null;const large=document.getElementById('large'),game=document.getElementById('game'),controls=[...document.querySelectorAll('button')];function render(){const v=views[index];large.src=game.src=v.src;document.getElementById('readout').textContent=(index+1)+' / '+views.length+' · '+v.id.replaceAll('-',' ')+' · bounds '+JSON.stringify(v.bounds)+' · SHA-256 '+v.sha256}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){index=(index+1)%views.length;render();timer=setTimeout(tick,900)}document.getElementById('prev').onclick=()=>{stop();index=(index+views.length-1)%views.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%views.length;render()};document.getElementById('play').onclick=()=>{stop();tick()};document.getElementById('pause').onclick=stop;document.getElementById('chairToggle').onchange=e=>document.querySelector('.chair').style.display=e.target.checked?'block':'none';function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const d=im.decode?.();d?d.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}Promise.all(unique.map(preload)).then(()=>{controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique comparison images decoded before controls were enabled.';render()}).catch(e=>document.getElementById('loading').textContent='Review locked: '+e.message)
</script></body></html>`
fs.writeFileSync(pageFile, html)

register.publicPage = { file: rel(pageFile), sha256: sha(pageFile) }
writeJson(registerFile, register)
fs.rmSync(tempDir, { recursive: true, force: true })
console.log(JSON.stringify({ set, frames: frames.map((x) => ({ id: x.id, bounds: x.registeredBounds, sha256: sha(x.output) })), review: rel(pageFile) }, null, 2))
