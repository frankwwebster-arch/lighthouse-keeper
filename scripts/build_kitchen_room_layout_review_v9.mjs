#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const V8_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v8/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v9/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v9/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v9'
const V8_PAGE = 'public/keeper-review/kitchen-room-layout-v8/index.html'
const V8_REGISTER = `${V8_DIR}/extraction-register.json`
const V8_REGISTER_SHA256 = '3178c24438ab520ba10142196aef85149602e26764e00daff51b0a147d664ce2'
const PAD = 8

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const blank = (width, height) => new PNG({ width, height })
const offset = (png, x, y) => (y * png.width + x) * 4
const clear = (png, x, y) => png.data.fill(0, offset(png, x, y), offset(png, x, y) + 4)
const copyPixel = (source, target, sx, sy, dx, dy) => {
  const si = offset(source, sx, sy)
  if (!source.data[si + 3]) return
  source.data.copy(target.data, offset(target, dx, dy), si, si + 4)
}
const writePng = (file, png) => {
  const bytes = PNG.sync.write(png, { colorType: 6 })
  fs.writeFileSync(file, bytes)
  return { bytes, sha256: sha256(bytes), dimensions: [png.width, png.height] }
}
function insidePolygon(x, y, points) {
  let inside = false
  for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
    const [xi, yi] = points[i], [xj, yj] = points[j]
    if (((yi > y) !== (yj > y)) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside
  }
  return inside
}
function trim(image) {
  let minx = image.width, miny = image.height, maxx = -1, maxy = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[offset(image, x, y) + 3]) {
    minx = Math.min(minx, x); miny = Math.min(miny, y); maxx = Math.max(maxx, x); maxy = Math.max(maxy, y)
  }
  const out = blank(maxx - minx + 1 + PAD * 2, maxy - miny + 1 + PAD * 2)
  for (let y = miny; y <= maxy; y += 1) for (let x = minx; x <= maxx; x += 1) copyPixel(image, out, x, y, x - minx + PAD, y - miny + PAD)
  return out
}
const contactRow = image => {
  let row = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[offset(image, x, y) + 3]) row = y
  return row
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V8_REGISTER) !== V8_REGISTER_SHA256) throw new Error('Kitchen V8 register changed')
const v8 = JSON.parse(fs.readFileSync(V8_REGISTER, 'utf8'))
const outputs = {}
for (const [id, source] of Object.entries(v8.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V8 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { ...source, file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, inheritedByteIdenticalFromV8: true }
}
function replaceOutput(id, png, metadata) {
  const filename = `${id}-native.png`, written = writePng(path.join(OUT, filename), png)
  fs.writeFileSync(path.join(PUBLIC, filename), written.bytes)
  outputs[id] = {
    ...outputs[id], file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`,
    dimensions: written.dimensions, sha256: written.sha256, predecessorSha256: v8.outputs[id].sha256,
    inheritedByteIdenticalFromV8: false, ...metadata,
  }
}

const bowlRaw = readPng(v8.outputs['bowl-broken'].file)
const frontLeftPanel = [[8, 48], [29, 52], [42, 48], [56, 55], [69, 50], [81, 61], [84, 82], [8, 82]]
for (let y = 0; y < bowlRaw.height; y += 1) for (let x = 0; x < bowlRaw.width; x += 1) if (insidePolygon(x + .5, y + .5, frontLeftPanel)) clear(bowlRaw, x, y)
const bowl = trim(bowlRaw)
replaceOutput('bowl-broken', bowl, {
  contactRow: contactRow(bowl), anchorX: Math.round(bowl.width / 2), frontLeftPanelRemoved: true,
  correction: 'the remaining striped front-left shell panel is removed as transparent loss; no detached debris is introduced',
})

const v8Water = readPng(v8.outputs['broken-floor-water'].file), floorWater = blank(v8Water.width, v8Water.height)
for (let y = 0; y < v8Water.height; y += 1) for (let x = 360; x <= 640; x += 1) copyPixel(v8Water, floorWater, x, y, x, y)
replaceOutput('broken-floor-water', floorWater, {
  sinkOwned: true, correction: 'walking-plane puddle ends at local x=640 beneath the sink and cannot extend under the dishwasher, oven or fridge',
})

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v8/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V8 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const register = {
  ...v8,
  schema: 'lighthouse-keeper/kitchen-native-assets@9',
  status: 'review-only-unapproved-v9-final-broken-bowl-and-water-ownership-correction',
  predecessor: { register: V8_REGISTER, sha256: V8_REGISTER_SHA256 },
  corrections: {
    ...v8.corrections,
    bowl: 'remaining striped front-left shell panel removed; transparent material loss with no detached debris',
    floorWater: 'puddle clipped to the sink footprint and excluded from dishwasher, oven and fridge footprints',
    reviewShell: 'version label and reversible-boundary copy corrected',
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V8_PAGE, 'utf8')
page = page
  .replace('<title>Kitchen V8 · corrected broken-state ownership and animation</title>', '<title>Kitchen V9 · final broken bowl and sink-water correction</title>')
  .replace('<h1>Corrected broken-state ownership and animation</h1>', '<h1>Final broken bowl and sink-water correction</h1>')
  .replace('V7 remains immutable predecessor evidence. V8 keeps its ON sink and chair corrections, then repairs only the broken-state layers: debris-free counter assets, a genuinely open broken bowl, sink-owned gush and puddle, fixed dishwasher lenses and cavity-only oven flicker. The approved fitted-unit bodies and room layout remain byte-identical.', 'V8 remains immutable predecessor evidence. V9 removes the last striped front-left panel from the broken bowl, confines floor water to the sink footprint, and corrects the review-shell version labels. All other V8 artwork and behaviour remain byte-identical.')
  .replaceAll('/keeper-review/kitchen-room-layout-v8/assets/', '/keeper-review/kitchen-room-layout-v9/assets/')
  .replace("const ROOT='/keeper-review/kitchen-room-layout-v9/assets/',V='?v=8';", "const ROOT='/keeper-review/kitchen-room-layout-v9/assets/',V='?v=9';")
  .replace('Review-only V6', 'Review-only V9')
  .replace('V8 corrected loose family · native source pixels', 'V9 corrected loose family · native source pixels')
  .replace('V8 inherits the approved fitted base byte-for-byte from V4; only separate fault/effect layers change.', 'V9 inherits the approved fitted base byte-for-byte from V4; only the separate bowl and sink-puddle alpha masks change from V8.')
  .replace('Reject V7 by discarding only its page, route and native correction outputs. V1–V6 and live 84 × 74 gameplay remain unchanged.', 'Reject V9 by discarding only its page, route and V9 native correction directory. V1–V8 and live 84 × 74 gameplay remain unchanged.')
  .replace("'OFF: locked fitted base and V8 corrected loose bodies.'", "'OFF: locked fitted base and V9 corrected loose bodies.'")
  .replace("'V8 starting layout restored.'", "'V9 starting layout restored.'")
  .replace("'Ready: V8 broken-state ownership and animations corrected.'", "'Ready: V9 broken bowl and sink-owned water corrected.'")
  .replace("contacts:{standard:116,broken:81},anchors:{standard:69,broken:65}", `contacts:{standard:116,broken:${outputs['bowl-broken'].contactRow}},anchors:{standard:69,broken:${outputs['bowl-broken'].anchorX}}`)

const proof = `<section class="panel"><h2>V8 predecessor ↔ V9 final correction</h2><p>Only the broken bowl alpha and sink-owned walking-plane puddle differ. Approved fitted bodies, all animations, room geometry, pace lattice and gameplay remain unchanged.</p><div class="comparison"><article><h3>Broken bowl</h3><div class="comparisonPair"><figure><figcaption>V8 · front-left panel remains</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v8/assets/bowl-broken-native.png?v=8"></div></figure><figure><figcaption>V9 · panel removed</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v9/assets/bowl-broken-native.png?v=9"></div></figure></div></article><article><h3>Sink-owned floor water</h3><div class="comparisonPair"><figure><figcaption>V8 · reaches adjacent appliance</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v8/assets/broken-floor-water-native.png?v=8"></div></figure><figure><figcaption>V9 · sink footprint only</figcaption><div class="assetProof"><img src="/keeper-review/kitchen-room-layout-v9/assets/broken-floor-water-native.png?v=9"></div></figure></div></article></div></section>`
page = page.replace(/<section class="panel"><h2>V7 predecessor ↔ V8 broken-state draft<\/h2>.*?<\/section>(?=<section class="panel"><h2>Scale registration<\/h2>)/s, proof)
page = page.replace(/const predecessorProofUrls=\[[^;]+;/, "const predecessorProofUrls=['/keeper-review/kitchen-room-layout-v8/assets/bowl-broken-native.png?v=8','/keeper-review/kitchen-room-layout-v8/assets/broken-floor-water-native.png?v=8'];")
page = page.replaceAll('Kitchen V8', 'Kitchen V9')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@9', version: 9, createdOn: '2026-10-25',
  status: 'review-only-awaiting-final-broken-state-review', reviewRoute: '/keeper-review/kitchen-room-layout-v9/', supersedesReview: '/keeper-review/kitchen-room-layout-v8/',
  authority: { document: 'docs/KITCHEN_ASSET_AUTHORITY.md', contract: 'data/kitchen_asset_contract_v1.json', roomGrid: 'data/kitchen_room_grid_contract_v2.json', lockedFittedBaseSha256: outputs['fitted-units-static'].sha256 },
  nativeAssets: { register: `${OUT}/extraction-register.json`, registerSha256: hash(`${OUT}/extraction-register.json`), predecessorRegister: V8_REGISTER, predecessorRegisterSha256: V8_REGISTER_SHA256, scaleAppliedToKitchenArt: false, downscalingApplied: false, resamplingApplied: false, colourTransformApplied: false },
  corrections: register.corrections,
  boundary: { runtimeChanged: false, gameplayChanged: false, approvedFittedUnitsChanged: false, roomGridChanged: false, rollback: 'Rejecting V9 discards only its route, page and V9 native correction directory. V1-V8, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.' },
}
fs.writeFileSync('data/kitchen_room_layout_review_v9.json', `${JSON.stringify(record, null, 2)}\n`)
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v9/HANDOFF.md', '# Kitchen Room Layout Review V9\n\nV9 is a reversible review-only correction derived from immutable V8. It removes the remaining striped front-left shell panel from the broken bowl, confines the walking-plane puddle to the sink footprint, and corrects the review-shell version labels. All other V8 pixels, animations, exact pace grid, gameplay and runtime art remain unchanged.\n')
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v9/PROMPT_LOG.md', '# Kitchen V9 edit record\n\nFinal outputs use deterministic 1:1 native-pixel alpha edits to immutable V8 inputs. No asset is scaled, resampled, redrawn or colour-transformed.\n')
console.log(`Built Kitchen V9 with ${Object.keys(outputs).length} native outputs.`)
