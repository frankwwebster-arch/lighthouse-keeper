#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const V9_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v9/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v10/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v10/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v10'
const V9_PAGE = 'public/keeper-review/kitchen-room-layout-v9/index.html'
const V9_REGISTER = `${V9_DIR}/extraction-register.json`
const V9_REGISTER_SHA256 = 'f456edd956703501d1f5607a058f1cd25768ff3f637b7556b803df137b2f90b7'

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V9_REGISTER) !== V9_REGISTER_SHA256) throw new Error('Kitchen V9 register changed')
const v9 = JSON.parse(fs.readFileSync(V9_REGISTER, 'utf8'))
const outputs = {}
for (const [id, source] of Object.entries(v9.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V9 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { ...source, file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, inheritedByteIdenticalFromV9: true }
}

const on = PNG.sync.read(fs.readFileSync(v9.outputs['fitted-overlay-on'].file))
for (let y = 42; y <= 98; y += 1) for (let x = 500; x <= 650; x += 1) {
  if (x >= 552 && x <= 561) continue
  on.data.fill(0, offset(on, x, y), offset(on, x, y) + 4)
}
const onBytes = PNG.sync.write(on, { colorType: 6 })
const onFilename = 'fitted-overlay-on-native.png'
fs.writeFileSync(path.join(OUT, onFilename), onBytes)
fs.writeFileSync(path.join(PUBLIC, onFilename), onBytes)
outputs['fitted-overlay-on'] = {
  ...outputs['fitted-overlay-on'], file: `${OUT}/${onFilename}`, publicReviewFile: `${PUBLIC}/${onFilename}`,
  sha256: sha256(onBytes), dimensions: [on.width, on.height], predecessorSha256: v9.outputs['fitted-overlay-on'].sha256,
  inheritedByteIdenticalFromV9: false, straightStreamBounds: [552, 42, 561, 98], splashPixelsRemoved: true,
  correction: 'ON water retains only the native vertical tap stream; every basin splash and pooling pixel is transparent',
}

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v9/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V9 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const register = {
  ...v9,
  schema: 'lighthouse-keeper/kitchen-native-assets@10',
  status: 'review-only-unapproved-v10-straight-on-tap-stream',
  predecessor: { register: V9_REGISTER, sha256: V9_REGISTER_SHA256 },
  corrections: {
    ...v9.corrections,
    onSink: 'straight vertical native stream from tap outlet; no basin splash or pooling',
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V9_PAGE, 'utf8')
page = page
  .replace('<title>Kitchen V9 · final broken bowl and sink-water correction</title>', '<title>Kitchen V10 · straight ON tap stream</title>')
  .replace('<h1>Final broken bowl and sink-water correction</h1>', '<h1>Straight ON tap stream</h1>')
  .replace('V8 remains immutable predecessor evidence. V9 removes the last striped front-left panel from the broken bowl, confines floor water to the sink footprint, and corrects the review-shell version labels. All other V8 artwork and behaviour remain byte-identical.', 'V9 remains immutable predecessor evidence. V10 changes only the ON sink-water alpha: water falls in one straight vertical line from the tap outlet, with no splash or pooling at its base. Every other V9 pixel and all behaviour remain byte-identical.')
  .replaceAll('/keeper-review/kitchen-room-layout-v9/assets/', '/keeper-review/kitchen-room-layout-v10/assets/')
  .replace("const ROOT='/keeper-review/kitchen-room-layout-v10/assets/',V='?v=9';", "const ROOT='/keeper-review/kitchen-room-layout-v10/assets/',V='?v=10';")
  .replace('Review-only V9', 'Review-only V10')
  .replace('V9 corrected loose family · native source pixels', 'V10 corrected loose family · native source pixels')
  .replace('V9 inherits the approved fitted base byte-for-byte from V4; only the separate bowl and sink-puddle alpha masks change from V8.', 'V10 inherits the approved fitted base byte-for-byte from V4; only the separate ON sink-water alpha mask changes from V9.')
  .replace('Reject V9 by discarding only its page, route and V9 native correction directory. V1–V8 and live 84 × 74 gameplay remain unchanged.', 'Reject V10 by discarding only its page, route and V10 native correction directory. V1–V9 and live 84 × 74 gameplay remain unchanged.')
  .replace("'OFF: locked fitted base and V9 corrected loose bodies.'", "'OFF: locked fitted base and V10 corrected loose bodies.'")
  .replace("'V9 starting layout restored.'", "'V10 starting layout restored.'")
  .replace("'Ready: V9 broken bowl and sink-owned water corrected.'", "'Ready: V10 ON tap stream is straight with no pooling.'")

const proof = `<section class="panel"><h2>V9 predecessor ↔ V10 ON sink correction</h2><p>Only the ON sink-water alpha differs. The approved fitted bodies, Broken-state gush and puddle, loose assets, room geometry, pace lattice and gameplay remain unchanged.</p><div class="comparison"><article><h3>ON sink water</h3><div class="comparisonPair"><figure><figcaption>V9 · stream plus basin pooling</figcaption><div class="effectProof"><img src="/keeper-review/kitchen-room-layout-v9/assets/fitted-units-static-native.png?v=9"><img src="/keeper-review/kitchen-room-layout-v9/assets/fitted-overlay-on-native.png?v=9"></div></figure><figure><figcaption>V10 · straight stream only</figcaption><div class="effectProof"><img src="/keeper-review/kitchen-room-layout-v10/assets/fitted-units-static-native.png?v=10"><img src="/keeper-review/kitchen-room-layout-v10/assets/fitted-overlay-on-native.png?v=10"></div></figure></div></article></div></section>`
page = page.replace(/<section class="panel"><h2>V8 predecessor ↔ V9 final correction<\/h2>.*?<\/section>(?=<section class="panel"><h2>Scale registration<\/h2>)/s, proof)
page = page.replace(/const predecessorProofUrls=\[[^;]+;/, "const predecessorProofUrls=['/keeper-review/kitchen-room-layout-v9/assets/fitted-units-static-native.png?v=9','/keeper-review/kitchen-room-layout-v9/assets/fitted-overlay-on-native.png?v=9'];")
page = page.replaceAll('Kitchen V9', 'Kitchen V10')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@10', version: 10, createdOn: '2026-10-25',
  status: 'review-only-awaiting-on-sink-review', reviewRoute: '/keeper-review/kitchen-room-layout-v10/', supersedesReview: '/keeper-review/kitchen-room-layout-v9/',
  authority: { document: 'docs/KITCHEN_ASSET_AUTHORITY.md', contract: 'data/kitchen_asset_contract_v1.json', roomGrid: 'data/kitchen_room_grid_contract_v2.json', lockedFittedBaseSha256: outputs['fitted-units-static'].sha256 },
  nativeAssets: { register: `${OUT}/extraction-register.json`, registerSha256: hash(`${OUT}/extraction-register.json`), predecessorRegister: V9_REGISTER, predecessorRegisterSha256: V9_REGISTER_SHA256, scaleAppliedToKitchenArt: false, downscalingApplied: false, resamplingApplied: false, colourTransformApplied: false },
  corrections: register.corrections,
  boundary: { runtimeChanged: false, gameplayChanged: false, approvedFittedUnitsChanged: false, roomGridChanged: false, rollback: 'Rejecting V10 discards only its route, page and V10 native correction directory. V1-V9, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.' },
}
fs.writeFileSync('data/kitchen_room_layout_review_v10.json', `${JSON.stringify(record, null, 2)}\n`)
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v10/HANDOFF.md', '# Kitchen Room Layout Review V10\n\nV10 is a reversible review-only correction derived from immutable V9. The ON sink-water overlay retains only its straight vertical native stream from the tap outlet; every splash and pooling pixel is transparent. Broken-state water, all other V9 art, exact pace grid, gameplay and runtime art remain unchanged.\n')
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v10/PROMPT_LOG.md', '# Kitchen V10 edit record\n\nThe final output uses a deterministic 1:1 native-pixel alpha edit to immutable V9. No asset is generated, scaled, resampled, redrawn or colour-transformed.\n')
console.log(`Built Kitchen V10 with ${Object.keys(outputs).length} native outputs.`)
