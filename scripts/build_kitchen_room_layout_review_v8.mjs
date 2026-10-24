#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const VERSION = 'v8'
const PREVIOUS = 'v7'
const V7_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v7/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v8/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v8/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v8'
const V7_PAGE = 'public/keeper-review/kitchen-room-layout-v7/index.html'
const V7_REGISTER_FILE = `${V7_DIR}/extraction-register.json`
const V7_REGISTER_SHA256 = 'eef929ce4e6f7f1d7f8fafc406de6d90605af6a74b37a35eeb5f855af0379a8a'
const PAD = 8

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const blank = (width, height) => new PNG({ width, height })
const clone = png => PNG.sync.read(PNG.sync.write(png, { colorType: 6 }))
const writePng = (file, png) => {
  const bytes = PNG.sync.write(png, { colorType: 6 })
  fs.writeFileSync(file, bytes)
  return { bytes, sha256: sha256(bytes), dimensions: [png.width, png.height] }
}
const pixelOffset = (png, x, y) => (y * png.width + x) * 4
const clearPixel = (png, x, y) => png.data.fill(0, pixelOffset(png, x, y), pixelOffset(png, x, y) + 4)
const copyPixel = (source, target, sx, sy, dx, dy) => {
  if (sx < 0 || sy < 0 || dx < 0 || dy < 0 || sx >= source.width || sy >= source.height || dx >= target.width || dy >= target.height) return
  const si = pixelOffset(source, sx, sy)
  if (!source.data[si + 3]) return
  source.data.copy(target.data, pixelOffset(target, dx, dy), si, si + 4)
}
function components(image) {
  const seen = new Uint8Array(image.width * image.height), result = []
  for (let start = 0; start < seen.length; start += 1) {
    if (seen[start] || !image.data[start * 4 + 3]) continue
    const pixels = [start]
    seen[start] = 1
    for (let head = 0; head < pixels.length; head += 1) {
      const p = pixels[head], x = p % image.width, y = Math.floor(p / image.width)
      for (let dy = -1; dy <= 1; dy += 1) for (let dx = -1; dx <= 1; dx += 1) {
        if (!dx && !dy) continue
        const xx = x + dx, yy = y + dy
        if (xx < 0 || yy < 0 || xx >= image.width || yy >= image.height) continue
        const next = yy * image.width + xx
        if (!seen[next] && image.data[next * 4 + 3]) { seen[next] = 1; pixels.push(next) }
      }
    }
    result.push(pixels)
  }
  return result.sort((a, b) => b.length - a.length)
}
function keepLargest(image) {
  const result = blank(image.width, image.height)
  const largest = components(image)[0]
  for (const p of largest) image.data.copy(result.data, p * 4, p * 4, p * 4 + 4)
  return result
}
function trim(image) {
  let minx = image.width, miny = image.height, maxx = -1, maxy = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[pixelOffset(image, x, y) + 3]) {
    minx = Math.min(minx, x); miny = Math.min(miny, y); maxx = Math.max(maxx, x); maxy = Math.max(maxy, y)
  }
  if (maxx < 0) throw new Error('Cannot trim empty image')
  const out = blank(maxx - minx + 1 + PAD * 2, maxy - miny + 1 + PAD * 2)
  for (let y = miny; y <= maxy; y += 1) for (let x = minx; x <= maxx; x += 1) copyPixel(image, out, x, y, x - minx + PAD, y - miny + PAD)
  return out
}
const contactRow = image => {
  let row = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[pixelOffset(image, x, y) + 3]) row = y
  return row
}
function insidePolygon(x, y, points) {
  let inside = false
  for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
    const [xi, yi] = points[i], [xj, yj] = points[j]
    if (((yi > y) !== (yj > y)) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside
  }
  return inside
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V7_REGISTER_FILE) !== V7_REGISTER_SHA256) throw new Error('Kitchen V7 register changed')
const v7 = JSON.parse(fs.readFileSync(V7_REGISTER_FILE, 'utf8'))
const outputs = {}

for (const [id, source] of Object.entries(v7.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V7 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { ...source, file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, inheritedByteIdenticalFromV7: true }
}
function replaceOutput(id, png, metadata) {
  const filename = `${id}-native.png`
  const written = writePng(path.join(OUT, filename), png)
  fs.writeFileSync(path.join(PUBLIC, filename), written.bytes)
  outputs[id] = {
    ...outputs[id], file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`,
    dimensions: written.dimensions, sha256: written.sha256, inheritedByteIdenticalFromV7: false,
    predecessorSha256: v7.outputs[id]?.sha256, ...metadata,
  }
}

const toaster = trim(keepLargest(readPng(v7.outputs['toaster-broken'].file)))
replaceOutput('toaster-broken', toaster, {
  contactRow: contactRow(toaster), anchorX: Math.round(toaster.width / 2), detachedDebrisRemoved: 2,
  correction: 'two detached black/brown countertop splodges removed; main broken toaster pixels unchanged and re-registered to its own feet',
})

const bowlRaw = keepLargest(readPng(v7.outputs['bowl-broken'].file))
const hangingPanel = [[93, 32], [117, 32], [120, 44], [131, 41], [129, 58], [137, 66], [128, 83], [103, 83], [102, 69], [90, 58], [96, 49]]
for (let y = 0; y < bowlRaw.height; y += 1) for (let x = 0; x < bowlRaw.width; x += 1) if (insidePolygon(x + 0.5, y + 0.5, hangingPanel)) clearPixel(bowlRaw, x, y)
const bowl = trim(bowlRaw)
replaceOutput('bowl-broken', bowl, {
  contactRow: contactRow(bowl), anchorX: Math.round(bowl.width / 2), detachedDebrisRemoved: 2,
  hangingFrontPanelRemoved: true,
  correction: 'both loose debris pieces and the large unstriped hanging front panel removed; the front wall now contains a genuine transparent jagged break',
})

const broken = readPng(v7.outputs['fitted-overlay-broken'].file)
const waterLike = (png, x, y) => {
  const i = pixelOffset(png, x, y), r = png.data[i], g = png.data[i + 1], b = png.data[i + 2], a = png.data[i + 3]
  return a && g > 140 && b > 175 && b > r + 20
}
for (let y = 248; y < broken.height; y += 1) for (let x = 0; x < broken.width; x += 1) if (waterLike(broken, x, y)) clearPixel(broken, x, y)
replaceOutput('fitted-overlay-broken', broken, {
  correction: 'dishwasher/fridge source-row leak pixels removed; broken water is owned only by the sink-gush and sink-centred floor-puddle layers',
})

const floorSource = readPng(v7.outputs['broken-floor-water'].file)
const floorWater = blank(floorSource.width, floorSource.height)
for (let y = 10; y < floorSource.height; y += 1) for (let x = 360; x <= 760; x += 1) copyPixel(floorSource, floorWater, x, y, x, y)
replaceOutput('broken-floor-water', floorWater, {
  correction: 'puddle clipped to the walking plane below the sink; the source-row horizontal line and water beneath oven/fridge are removed',
  sinkOwned: true,
})

for (const id of ['dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3']) {
  const source = readPng(v7.outputs[id].file), clean = blank(source.width, source.height)
  const red = []
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    const i = pixelOffset(source, x, y), r = source.data[i], g = source.data[i + 1], b = source.data[i + 2], a = source.data[i + 3]
    if (a && r > 140 && r > g * 1.35 && r > b * 1.35) red.push([x, y])
  }
  const cx = red.reduce((sum, p) => sum + p[0], 0) / red.length, cy = red.reduce((sum, p) => sum + p[1], 0) / red.length
  for (let y = Math.floor(cy - 10); y <= Math.ceil(cy + 10); y += 1) for (let x = Math.floor(cx - 10); x <= Math.ceil(cx + 10); x += 1) {
    const i = pixelOffset(source, x, y), r = source.data[i], g = source.data[i + 1], b = source.data[i + 2]
    const paper = r > 170 && g > 160 && b > 125
    if ((x - cx) ** 2 + (y - cy) ** 2 <= 95 && !paper) copyPixel(source, clean, x, y, x, y)
  }
  replaceOutput(id, clean, { correction: 'only the fixed red lens and its dark rim remain; moving cream source rectangles removed', fixedLensCentre: [Number(cx.toFixed(2)), Number(cy.toFixed(2))] })
}

const ovenGlow = blank(broken.width, broken.height)
for (let y = 174; y <= 229; y += 1) for (let x = 944; x <= 1110; x += 1) {
  const dx = (x - 1027) / 83, dy = (y - 201.5) / 27.5
  if (dx * dx + dy * dy > 1) continue
  const sourceIndex = pixelOffset(broken, x, y), alpha = broken.data[sourceIndex + 3]
  const luminance = broken.data[sourceIndex] * .2126 + broken.data[sourceIndex + 1] * .7152 + broken.data[sourceIndex + 2] * .0722
  if (!alpha || luminance > 95) continue
  const edge = Math.max(0, 1 - Math.sqrt(dx * dx + dy * dy))
  const i = pixelOffset(ovenGlow, x, y)
  ovenGlow.data[i] = 255; ovenGlow.data[i + 1] = 145; ovenGlow.data[i + 2] = 18; ovenGlow.data[i + 3] = Math.round(42 + edge * 92)
}
replaceOutput('oven-broken-cavity-light', ovenGlow, {
  correction: 'cavity-only translucent amber glow; no food, tray, handle, door or fascia pixels',
  animation: 'irregular opacity flicker in review shell',
})

const onWater = readPng(v7.outputs['fitted-overlay-on'].file)
const gushFrames = []
for (let frame = 0; frame < 3; frame += 1) {
  const gush = blank(onWater.width, onWater.height)
  const streamOffsets = frame === 0 ? [-4, 0, 4] : frame === 1 ? [-5, -1, 3, 6] : [-3, 1, 5]
  for (let y = 42; y <= 96; y += 1) for (let x = 540; x <= 575; x += 1) {
    if (!onWater.data[pixelOffset(onWater, x, y) + 3]) continue
    for (const dx of streamOffsets) copyPixel(onWater, gush, x, y, x + dx, y)
  }
  const splashShift = frame === 0 ? 0 : frame === 1 ? 2 : -2
  for (let y = 87; y <= 98; y += 1) for (let x = 520; x <= 625; x += 1) if (onWater.data[pixelOffset(onWater, x, y) + 3]) {
    copyPixel(onWater, gush, x, y, x + splashShift, y)
    if (frame === 1) copyPixel(onWater, gush, x, y, x - 2, y + (y < 96 ? 1 : 0))
  }
  const id = `sink-broken-gush-${frame + 1}`
  const filename = `${id}-native.png`, written = writePng(path.join(OUT, filename), gush)
  fs.writeFileSync(path.join(PUBLIC, filename), written.bytes)
  outputs[id] = {
    file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, dimensions: written.dimensions, sha256: written.sha256,
    source: v7.outputs['fitted-overlay-on'].file, sourceSha256: v7.outputs['fitted-overlay-on'].sha256,
    role: 'sink-owned animated broken-state gush', frame: frame + 1, scaleApplied: false, resamplingApplied: false,
  }
  gushFrames.push(outputs[id])
}

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v7/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V7 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const register = {
  ...v7,
  schema: 'lighthouse-keeper/kitchen-native-assets@8', status: 'review-only-unapproved-v8-broken-state-ownership-correction', createdOn: '2026-10-25',
  predecessor: { register: V7_REGISTER_FILE, sha256: V7_REGISTER_SHA256 },
  corrections: {
    toaster: 'detached countertop splodges removed; own feet establish support',
    bowl: 'debris and hanging unstriped panel removed; transparent front-wall break',
    sink: 'three-frame tap-outlet gush plus sink-centred walking-plane puddle',
    dishwasher: 'fixed lens-only overlays pulse without cream rectangles or translation',
    oven: 'cavity-only translucent glow flickers; prior food/door overlay removed',
    waterOwnership: 'no broken-overlay leak below dishwasher/fridge and no puddle below oven/fridge',
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V7_PAGE, 'utf8')
page = page
  .replace('<title>Kitchen V7 · corrected sink flow and transparent chair slats</title>', '<title>Kitchen V8 · corrected broken-state ownership and animation</title>')
  .replace('<h1>Corrected sink flow and transparent chair slats</h1>', '<h1>Corrected broken-state ownership and animation</h1>')
  .replace('V6 remains immutable predecessor evidence. V7 changes only the ON water effect and the chair alpha mask: water now falls from the curved tap outlet and stays inside the basin, while the rear-chair gaps are transparent. The approved fitted units and V6 layout remain byte-identical.', 'V7 remains immutable predecessor evidence. V8 keeps its ON sink and chair corrections, then repairs only the broken-state layers: debris-free counter assets, a genuinely open broken bowl, sink-owned gush and puddle, fixed dishwasher lenses and cavity-only oven flicker. The approved fitted-unit bodies and room layout remain byte-identical.')
  .replaceAll('/keeper-review/kitchen-room-layout-v7/assets/', '/keeper-review/kitchen-room-layout-v8/assets/')
  .replace("const ROOT='/keeper-review/kitchen-room-layout-v8/assets/',V='?v=7';", "const ROOT='/keeper-review/kitchen-room-layout-v8/assets/',V='?v=8';")
  .replace('V7 corrected loose family · native source pixels', 'V8 corrected loose family · native source pixels')
  .replace('V7 inherits the approved fitted base byte-for-byte from V4; only the separate ON water effect changes.', 'V8 inherits the approved fitted base byte-for-byte from V4; only separate fault/effect layers change.')
  .replace('Reject V7 by discarding only its page, route and V7 native correction directory. V1–V6 and live 84 × 74 gameplay remain unchanged.', 'Reject V8 by discarding only its page, route and V8 native correction directory. V1–V7 and live 84 × 74 gameplay remain unchanged.')
  .replace("'OFF: locked fitted base and V7 corrected loose bodies.'", "'OFF: locked fitted base and V8 corrected loose bodies.'")
  .replace("'V7 starting layout restored.'", "'V8 starting layout restored.'")
  .replace("'Ready: V7 sink water and rear-chair transparency corrected.'", "'Ready: V8 broken-state ownership and animations corrected.'")
  .replace("broken:'toaster-broken-native.png'},contacts:{off:96,on:117,broken:123},anchors:{off:66,on:68,broken:80}", `broken:'toaster-broken-native.png'},contacts:{off:96,on:117,broken:${outputs['toaster-broken'].contactRow}},anchors:{off:66,on:68,broken:${outputs['toaster-broken'].anchorX}}`)
  .replace("broken:'bowl-broken-native.png'},contacts:{standard:116,broken:93},anchors:{standard:69,broken:81}", `broken:'bowl-broken-native.png'},contacts:{standard:116,broken:${outputs['bowl-broken'].contactRow}},anchors:{standard:69,broken:${outputs['bowl-broken'].anchorX}}`)

page = page.replace('<img id="runBroken" hidden alt="BROKEN overlays">', '<img id="runBroken" hidden alt="BROKEN overlays"><img class="sinkGush g1" hidden alt="Broken tap gush frame one"><img class="sinkGush g2" hidden alt="Broken tap gush frame two"><img class="sinkGush g3" hidden alt="Broken tap gush frame three">')
page = page.replace("warnings:['dishwasher-warning-1-native.png','dishwasher-warning-2-native.png','dishwasher-warning-3-native.png']};", "warnings:['dishwasher-warning-1-native.png','dishwasher-warning-2-native.png','dishwasher-warning-3-native.png'],sink:['sink-broken-gush-1-native.png','sink-broken-gush-2-native.png','sink-broken-gush-3-native.png']};")
page = page.replace("document.querySelectorAll('.warningLight').forEach(i=>i.hidden=state!=='broken');", "document.querySelectorAll('.warningLight,.sinkGush').forEach(i=>i.hidden=state!=='broken');")
page = page.replace("document.querySelectorAll('.warningLight').forEach((i,n)=>i.src=ROOT+FITTED.warnings[n]+V);", "document.querySelectorAll('.warningLight').forEach((i,n)=>i.src=ROOT+FITTED.warnings[n]+V);document.querySelectorAll('.sinkGush').forEach((i,n)=>i.src=ROOT+FITTED.sink[n]+V);")

page = page.replace(/\.camera\.broken \.w1\{animation:blinkA.*?@keyframes ovenBlink\{0%,25%,60%,100%\{opacity:1\}26%,59%\{opacity:0\}\}/, '.camera.broken .w1{animation:blinkA 2.5s steps(1,end) infinite}.camera.broken .w2{animation:blinkB 3s steps(1,end) infinite}.camera.broken .w3{animation:blinkC 3.5s steps(1,end) infinite}.camera.broken .ovenLight{animation:ovenBlink 2.3s steps(1,end) infinite}.camera.broken .g1{animation:gush1 .36s steps(1,end) infinite}.camera.broken .g2{animation:gush2 .36s steps(1,end) infinite}.camera.broken .g3{animation:gush3 .36s steps(1,end) infinite}@keyframes blinkA{0%,45%,100%{opacity:.35}46%,80%{opacity:1}}@keyframes blinkB{0%,28%,72%,100%{opacity:1}29%,71%{opacity:.35}}@keyframes blinkC{0%,55%,100%{opacity:.35}56%,88%{opacity:1}}@keyframes ovenBlink{0%,18%,44%,47%,73%,100%{opacity:0}19%,43%,48%,72%{opacity:1}}@keyframes gush1{0%,32%{opacity:1}33%,100%{opacity:0}}@keyframes gush2{0%,32%,66%,100%{opacity:0}33%,65%{opacity:1}}@keyframes gush3{0%,65%{opacity:0}66%,100%{opacity:1}}')

const extraCss = '.assetProof,.effectProof{height:190px;display:grid;place-items:center;overflow:hidden;background:#fdfaea}.assetProof img{max-height:175px;max-width:100%}.effectProof{position:relative}.effectProof img{position:absolute;width:1368px;height:284px;left:-900px;top:-90px;max-width:none}'
page = page.replace('</style>', `${extraCss}</style>`)
const proof = `<section class="panel"><h2>V7 predecessor ↔ V8 broken-state draft</h2><p>Only separate broken-state assets and effects differ. The approved fitted-unit bodies, V7 ON sink, chair transparency, room geometry, pace lattice and gameplay remain unchanged.</p><div class="comparison"><article><h3>Counter assets</h3><div class="comparisonPair"><figure><figcaption>V7 · debris-driven support</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v7/assets/toaster-broken-native.png?v=7"></div></figure><figure><figcaption>V8 · toaster feet on worktop</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v8/assets/toaster-broken-native.png?v=8"></div></figure><figure><figcaption>V7 · bowl panel and debris</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v7/assets/bowl-broken-native.png?v=7"></div></figure><figure><figcaption>V8 · open break, no debris</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v8/assets/bowl-broken-native.png?v=8"></div></figure></div></article><article><h3>Oven fault light</h3><div class="comparisonPair"><figure><figcaption>V7 · food/door overlay</figcaption><div class="effectProof"><img src="/keeper-review/kitchen-room-layout-v7/assets/fitted-overlay-broken-native.png?v=7"><img src="/keeper-review/kitchen-room-layout-v7/assets/oven-broken-cavity-light-native.png?v=7"></div></figure><figure><figcaption>V8 · cavity glow only</figcaption><div class="effectProof"><img src="/keeper-review/kitchen-room-layout-v8/assets/fitted-overlay-broken-native.png?v=8"><img src="/keeper-review/kitchen-room-layout-v8/assets/oven-broken-cavity-light-native.png?v=8"></div></figure></div></article></div></section>`
page = page.replace(/<section class="panel"><h2>V6 predecessor ↔ V7 draft<\/h2>.*?<\/section>(?=<section class="panel"><h2>Scale registration<\/h2>)/s, proof)
page = page.replace(/const predecessorProofUrls=\[[^;]+;/, "const predecessorProofUrls=['/keeper-review/kitchen-room-layout-v7/assets/toaster-broken-native.png?v=7','/keeper-review/kitchen-room-layout-v7/assets/bowl-broken-native.png?v=7','/keeper-review/kitchen-room-layout-v7/assets/fitted-overlay-broken-native.png?v=7','/keeper-review/kitchen-room-layout-v7/assets/oven-broken-cavity-light-native.png?v=7'];")
page = page.replaceAll('Kitchen V7', 'Kitchen V8')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@8', version: 8, createdOn: '2026-10-25',
  status: 'review-only-awaiting-broken-state-review', reviewRoute: '/keeper-review/kitchen-room-layout-v8/', supersedesReview: '/keeper-review/kitchen-room-layout-v7/',
  authority: { document: 'docs/KITCHEN_ASSET_AUTHORITY.md', contract: 'data/kitchen_asset_contract_v1.json', roomGrid: 'data/kitchen_room_grid_contract_v2.json', lockedFittedBaseSha256: outputs['fitted-units-static'].sha256 },
  nativeAssets: { register: `${OUT}/extraction-register.json`, registerSha256: hash(`${OUT}/extraction-register.json`), predecessorRegister: V7_REGISTER_FILE, predecessorRegisterSha256: V7_REGISTER_SHA256, scaleAppliedToKitchenArt: false, downscalingApplied: false, resamplingApplied: false, colourTransformApplied: false },
  corrections: register.corrections,
  boundary: { runtimeChanged: false, gameplayChanged: false, approvedFittedUnitsChanged: false, roomGridChanged: false, rollback: 'Rejecting V8 discards only its route, page and V8 native correction directory. V1-V7, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.' },
}
fs.writeFileSync('data/kitchen_room_layout_review_v8.json', `${JSON.stringify(record, null, 2)}\n`)
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v8/HANDOFF.md', '# Kitchen Room Layout Review V8\n\nV8 is a reversible review-only broken-state correction derived from immutable V7. It removes toaster and bowl debris from support registration, removes the bowl\'s hanging unstriped front panel, assigns all broken water to a three-frame tap gush and sink-centred floor puddle, reduces dishwasher warning assets to fixed lenses, and replaces the oven food/door crop with a cavity-only flicker. Approved fitted bodies, V7 ON/chair corrections, exact pace grid, gameplay and runtime art remain unchanged.\n')
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v8/PROMPT_LOG.md', '# Kitchen V8 edit record\n\nA built-in image-edit draft was explored for the broken bowl but rejected because its 1536 × 1024 output would require forbidden downscaling and materially changed the approved line treatment. Final V8 outputs use deterministic 1:1 native-pixel alpha/layer edits to immutable V7 inputs. No final asset is scaled, resampled or colour-transformed.\n')
console.log(`Built Kitchen V8 with ${Object.keys(outputs).length} native outputs and ${gushFrames.length} sink-gush frames.`)
