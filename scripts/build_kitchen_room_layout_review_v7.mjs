#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const V6_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-24-v6/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v7/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v7/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v7'
const V6_PAGE = 'public/keeper-review/kitchen-room-layout-v6/index.html'
const V6_REGISTER_FILE = `${V6_DIR}/extraction-register.json`
const V6_REGISTER_SHA256 = 'ef5dec7a8e622fc1939c6fcff38bbae3ef926db0c25720182d01f5f7fcf5d37f'
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const writePng = (file, png) => {
  const bytes = PNG.sync.write(png, { colorType: 6 })
  fs.writeFileSync(file, bytes)
  return { bytes, sha256: sha256(bytes), dimensions: [png.width, png.height] }
}
const clonePng = png => PNG.sync.read(PNG.sync.write(png, { colorType: 6 }))
const transparent = (png, x, y) => png.data.fill(0, (y * png.width + x) * 4, (y * png.width + x) * 4 + 4)
const copyPixel = (source, target, sx, sy, dx, dy) => {
  if (sx < 0 || sy < 0 || dx < 0 || dy < 0 || sx >= source.width || sy >= source.height || dx >= target.width || dy >= target.height) return
  const si = (sy * source.width + sx) * 4
  if (!source.data[si + 3]) return
  source.data.copy(target.data, (dy * target.width + dx) * 4, si, si + 4)
}
const waterPixel = (png, x, y, allowWhite = false) => {
  const i = (y * png.width + x) * 4
  const r = png.data[i], g = png.data[i + 1], b = png.data[i + 2], a = png.data[i + 3]
  if (!a) return false
  const cyan = b >= 150 && g >= 120 && b >= r + 18
  const paleBlue = allowWhite && r >= 198 && g >= 215 && b >= 225 && b >= r + 3
  return cyan || paleBlue
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })

if (hash(V6_REGISTER_FILE) !== V6_REGISTER_SHA256) throw new Error('Kitchen V6 register changed')
const v6 = JSON.parse(fs.readFileSync(V6_REGISTER_FILE, 'utf8'))
const outputs = {}

for (const [id, source] of Object.entries(v6.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V6 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...source,
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    inheritedByteIdenticalFromV6: true,
  }
}

// The V6 ON sink was an opaque 100 x 60 row crop. Preserve all other ON-state
// pixels, clear that rectangle, then rebuild only the water at native 1:1
// pixels: a vertical fall from the curved outlet and a basin-contained splash.
const onSource = readPng(v6.outputs['fitted-overlay-on'].file)
const on = clonePng(onSource)
for (let y = 69; y <= 128; y += 1) for (let x = 525; x <= 624; x += 1) transparent(on, x, y)

// Extend the existing water texture upward without scaling or interpolation.
// The approved tap outlet is centred at x=557; the V6 stream was at x=568.
for (let y = 42; y <= 96; y += 1) {
  const sy = 84 + ((y - 42) % 10)
  for (let sx = 559; sx <= 580; sx += 1) {
    if (waterPixel(onSource, sx, sy, true)) copyPixel(onSource, on, sx, sy, sx - 11, y)
  }
}
// Retain the original illustrated splash, lifted into the open basin and
// clipped before the opaque front wall begins.
for (let sy = 96; sy <= 107; sy += 1) for (let sx = 525; sx <= 624; sx += 1) {
  if (waterPixel(onSource, sx, sy, true)) copyPixel(onSource, on, sx, sy, sx - 4, sy - 9)
}
const onWritten = writePng(path.join(OUT, 'fitted-overlay-on-native.png'), on)
fs.writeFileSync(path.join(PUBLIC, 'fitted-overlay-on-native.png'), onWritten.bytes)
outputs['fitted-overlay-on'] = {
  ...outputs['fitted-overlay-on'],
  sha256: onWritten.sha256,
  dimensions: onWritten.dimensions,
  inheritedByteIdenticalFromV6: false,
  predecessorSha256: v6.outputs['fitted-overlay-on'].sha256,
  correction: 'opaque sink row crop removed; water starts at approved tap outlet x=557 and is clipped above the opaque basin front',
  scaleApplied: false,
  resamplingApplied: false,
}

// Remove only the five large neutral paper islands enclosed by the chair:
// four gaps between the back slats and the open space below the seat. Small
// white/orange highlight pixels remain part of the drawing.
const chairSource = readPng(v6.outputs['chair-standard'].file)
const chair = clonePng(chairSource)
const seen = new Uint8Array(chair.width * chair.height)
const backgroundLike = p => {
  const i = p * 4, r = chair.data[i], g = chair.data[i + 1], b = chair.data[i + 2], a = chair.data[i + 3]
  return a > 0 && r >= 180 && g >= 180 && b >= 180 && Math.max(r, g, b) - Math.min(r, g, b) <= 65
}
let clearedChairComponents = 0
for (let start = 0; start < seen.length; start += 1) {
  if (seen[start] || !backgroundLike(start)) continue
  const pixels = [start]
  seen[start] = 1
  for (let head = 0; head < pixels.length; head += 1) {
    const p = pixels[head], x = p % chair.width, y = Math.floor(p / chair.width)
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const xx = x + dx, yy = y + dy
      if (xx < 0 || yy < 0 || xx >= chair.width || yy >= chair.height) continue
      const next = yy * chair.width + xx
      if (!seen[next] && backgroundLike(next)) { seen[next] = 1; pixels.push(next) }
    }
  }
  if (pixels.length < 200) continue
  clearedChairComponents += 1
  for (const p of pixels) chair.data[p * 4 + 3] = 0
}
if (clearedChairComponents !== 5) throw new Error(`Expected five trapped chair-paper components, found ${clearedChairComponents}`)
const chairWritten = writePng(path.join(OUT, 'chair-standard-native.png'), chair)
fs.writeFileSync(path.join(PUBLIC, 'chair-standard-native.png'), chairWritten.bytes)
outputs['chair-standard'] = {
  ...outputs['chair-standard'],
  sha256: chairWritten.sha256,
  dimensions: chairWritten.dimensions,
  inheritedByteIdenticalFromV6: false,
  predecessorSha256: v6.outputs['chair-standard'].sha256,
  transparentPaperComponentsRemoved: clearedChairComponents,
  correction: 'source-paper islands between rear-chair slats and below seat made transparent; wood pixels unchanged',
  scaleApplied: false,
  resamplingApplied: false,
}

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const source = path.join('public/keeper-review/kitchen-room-layout-v6/assets', keeperName)
  const archiveIndex = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const legacy = `/keeper-review/kitchen-room-layout-v6/assets/${keeperName}`
  const entry = archiveIndex.legacyPaths[legacy]
  if (!entry) throw new Error(`Missing V6 archived Keeper ${keeperName}`)
  const archived = path.join('review-archive', entry.object.replace(/^review-archive\//, ''))
  const bytes = fs.existsSync(source) ? fs.readFileSync(source) : fs.readFileSync(archived)
  fs.writeFileSync(path.join(PUBLIC, keeperName), bytes)
}

const register = {
  ...v6,
  schema: 'lighthouse-keeper/kitchen-native-assets@7',
  status: 'review-only-unapproved-v7-alpha-and-sink-effect-correction',
  createdOn: '2026-10-25',
  predecessor: { register: V6_REGISTER_FILE, sha256: V6_REGISTER_SHA256 },
  corrections: {
    sinkOn: 'removed opaque rectangular source-row replacement; stream touches the curved tap outlet and water is clipped above the unchanged opaque basin front',
    chair: 'removed five enclosed source-paper alpha islands so the seated Keeper remains visible through the rear-chair slats',
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V6_PAGE, 'utf8')
page = page
  .replace('<title>Kitchen V6 · shadowless assets and corrected furniture depth</title>', '<title>Kitchen V7 · corrected sink flow and transparent chair slats</title>')
  .replace('<h1>Shadowless loose assets, corrected furniture depth</h1>', '<h1>Corrected sink flow and transparent chair slats</h1>')
  .replace('V5 is frozen as rejected shadowed evidence. V6 removes baked contact shadows from every loose object, keeps countertop registration forward on the visible worktop, moves the table clear of the fridge and places the rear-facing chair in front of the table. The approved fitted units remain byte-identical.', 'V6 remains immutable predecessor evidence. V7 changes only the ON water effect and the chair alpha mask: water now falls from the curved tap outlet and stays inside the basin, while the rear-chair gaps are transparent. The approved fitted units and V6 layout remain byte-identical.')
  .replaceAll('/keeper-review/kitchen-room-layout-v6/assets/', '/keeper-review/kitchen-room-layout-v7/assets/')
  .replace("const ROOT='/keeper-review/kitchen-room-layout-v7/assets/',V='?v=6';", "const ROOT='/keeper-review/kitchen-room-layout-v7/assets/',V='?v=7';")
  .replace('V6 loose family · native source pixels', 'V7 corrected loose family · native source pixels')
  .replace('V6 inherits the fitted base and allowed overlays byte-for-byte from V4.', 'V7 inherits the approved fitted base byte-for-byte from V4; only the separate ON water effect changes.')
  .replace('Reject V6 by discarding only its page, route, generated sources and extracted loose outputs. V1–V5 and live 84 × 74 gameplay remain unchanged.', 'Reject V7 by discarding only its page, route and native correction outputs. V1–V6 and live 84 × 74 gameplay remain unchanged.')
  .replace("'OFF: locked fitted base and V6 shadowless loose bodies.'", "'OFF: locked fitted base and V7 corrected loose bodies.'")
  .replace("'V6 starting layout restored.'", "'V7 starting layout restored.'")
  .replace("'Ready: V6 at whole-room camera; table behind seated Keeper and chair in front.'", "'Ready: V7 sink water and rear-chair transparency corrected.'")

const comparisonCss = '.comparison{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:12px}.comparisonPair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.comparison figure{margin:0}.comparison figcaption{font-weight:700;margin-bottom:5px}.sinkProof{position:relative;width:240px;height:150px;overflow:hidden;background:#fdfaea}.sinkProof img{position:absolute;width:1368px;height:284px;left:-450px;top:-25px;max-width:none}.chairProof{height:240px;display:grid;place-items:center;background:#fdfaea}.chairProof img{max-height:224px}@media(max-width:900px){.comparison,.comparisonPair{grid-template-columns:1fr}}'
page = page.replace('</style>', `${comparisonCss}</style>`)
const proof = `<section class="panel"><h2>V6 predecessor ↔ V7 draft</h2><p>Only these two visual boundaries differ. The full fitted-unit base, all other loose assets, room geometry, pace lattice and gameplay remain unchanged.</p><div class="comparison"><article><h3>Sink ON effect</h3><div class="comparisonPair"><figure><figcaption>V6 · rejected rectangular crop</figcaption><div class="sinkProof"><img src="/keeper-review/kitchen-room-layout-v6/assets/fitted-units-static-native.png?v=6"><img src="/keeper-review/kitchen-room-layout-v6/assets/fitted-overlay-on-native.png?v=6"></div></figure><figure><figcaption>V7 · outlet-aligned, basin-clipped</figcaption><div class="sinkProof"><img src="${PUBLIC.replace('public', '')}/fitted-units-static-native.png?v=7"><img src="${PUBLIC.replace('public', '')}/fitted-overlay-on-native.png?v=7"></div></figure></div></article><article><h3>Rear chair alpha</h3><div class="comparisonPair"><figure><figcaption>V6 · trapped white paper</figcaption><div class="chairProof"><img src="/keeper-review/kitchen-room-layout-v6/assets/chair-standard-native.png?v=6"></div></figure><figure><figcaption>V7 · transparent between slats</figcaption><div class="chairProof"><img src="${PUBLIC.replace('public', '')}/chair-standard-native.png?v=7"></div></figure></div></article></div></section>`
page = page.replace('<section class="panel"><h2>Scale registration</h2>', `${proof}<section class="panel"><h2>Scale registration</h2>`)
page = page.replace("const fittedUrls=", "const predecessorProofUrls=['/keeper-review/kitchen-room-layout-v6/assets/fitted-units-static-native.png?v=6','/keeper-review/kitchen-room-layout-v6/assets/fitted-overlay-on-native.png?v=6','/keeper-review/kitchen-room-layout-v6/assets/chair-standard-native.png?v=6'];\nconst fittedUrls=")
page = page.replace('const fittedUrls=[...Object.values(FITTED).flat()].map(f=>ROOT+f+V),assetUrls=[PRIME,SEATED,...fittedUrls,', 'const fittedUrls=[...Object.values(FITTED).flat()].map(f=>ROOT+f+V),assetUrls=[PRIME,SEATED,...predecessorProofUrls,...fittedUrls,')
page = page.replaceAll('Kitchen V6', 'Kitchen V7')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@7',
  version: 7,
  createdOn: '2026-10-25',
  status: 'review-only-awaiting-sink-and-chair-review',
  reviewRoute: '/keeper-review/kitchen-room-layout-v7/',
  supersedesReview: '/keeper-review/kitchen-room-layout-v6/',
  authority: {
    document: 'docs/KITCHEN_ASSET_AUTHORITY.md',
    contract: 'data/kitchen_asset_contract_v1.json',
    roomGrid: 'data/kitchen_room_grid_contract_v2.json',
    lockedFittedBaseSha256: outputs['fitted-units-static'].sha256,
  },
  nativeAssets: {
    register: `${OUT}/extraction-register.json`,
    registerSha256: hash(`${OUT}/extraction-register.json`),
    predecessorRegister: V6_REGISTER_FILE,
    predecessorRegisterSha256: V6_REGISTER_SHA256,
    scaleAppliedToKitchenArt: false,
    downscalingApplied: false,
    resamplingApplied: false,
    colourTransformApplied: false,
  },
  corrections: register.corrections,
  boundary: {
    runtimeChanged: false,
    gameplayChanged: false,
    approvedFittedUnitsChanged: false,
    roomGridChanged: false,
    rollback: 'Rejecting V7 discards only its route, page and V7 native correction directory. V1-V6, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.',
  },
}
fs.writeFileSync('data/kitchen_room_layout_review_v7.json', `${JSON.stringify(record, null, 2)}\n`)
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v7/HANDOFF.md', '# Kitchen Room Layout Review V7\n\nV7 is a reversible review-only correction derived from immutable V6. It removes the opaque rectangular ON sink crop, registers the water fall to the curved tap outlet, clips the splash above the unchanged opaque basin front, and makes the trapped source-paper regions between the rear-chair slats transparent. The approved fitted-unit base, every other loose asset, room grid, pace lattice, gameplay and runtime art remain unchanged.\n')
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v7/PROMPT_LOG.md', '# Kitchen V7 edit record\n\nNo generative redraw was used. The corrections are deterministic native-pixel alpha/layer edits to immutable V6 inputs. No scaling, resampling or colour transform was applied.\n')
console.log(`Built Kitchen V7: sink ON ${v6.outputs['fitted-overlay-on'].sha256} -> ${outputs['fitted-overlay-on'].sha256}; chair ${v6.outputs['chair-standard'].sha256} -> ${outputs['chair-standard'].sha256}.`)
