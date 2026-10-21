#!/usr/bin/env node
/** Build V44: source-faithful review plus kitchen-native production kettle. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-kettle-standalone-v44'
const batch = 'kitchen-kettle-standalone-2026-10-21-v44'
const source = path.join(root, 'art/source', batch)
const raw = path.join(root, 'art/raw', batch)
const draft = path.join(root, 'art/drafts', batch)
const review = path.join(root, 'public/keeper-review', set)
const reviewAssets = path.join(review, 'assets')
const template = path.join(root, 'scripts/templates/kitchen_kettle_standalone_v44.html')
const v41Raw = path.join(root, 'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41')
const v41Catalogue = path.join(root, 'art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json')
const nativeSource = path.join(source, 'native/kettle-native-source.png')
const v43Source = path.join(root, 'art/source/kitchen-kettle-standalone-2026-10-20-v43/generated')
const stateSource = path.join(v43Source, 'kettle-state-family-source.png')
const brokenSource = path.join(v43Source, 'kettle-broken-source.png')
const steamSource = path.join(v43Source, 'kettle-steam-keyframes-source.png')
const generationProvenance = path.join(v43Source, 'generation-provenance.json')
const stateNames = ['off', 'on', 'broken']
const models = ['compact', 'regular', 'emphatic']
const compatibleOrigins = [84, 168, 336, 504]
const supportSurfaceSlots = [
  { origin: 84, supportAssetId: 'fridge', surfaceSlotId: 'fridge-worktop' },
  { origin: 168, supportAssetId: 'cabinetA', surfaceSlotId: 'cabinet-a-worktop' },
  { origin: 336, supportAssetId: 'cabinetB', surfaceSlotId: 'cabinet-b-worktop' },
  { origin: 504, supportAssetId: 'dishwasher', surfaceSlotId: 'dishwasher-worktop' },
]
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const read = file => PNG.sync.read(fs.readFileSync(file))
const clone = image => PNG.sync.read(PNG.sync.write(image))

for (const file of [template, v41Catalogue, nativeSource, stateSource, brokenSource, steamSource, generationProvenance, path.join(v41Raw, 'dishwasher-off-native-room.png'), path.join(v41Raw, 'cabinet-a-le-re.png')]) {
  if (!fs.existsSync(file)) throw new Error(`Missing authority: ${file}`)
}
for (const dir of [raw, draft, review]) {
  fs.mkdirSync(dir, { recursive: true })
  for (const item of fs.readdirSync(dir)) fs.rmSync(path.join(dir, item), { recursive: true, force: true })
}

function composite(dst, src, dx, dy, sx = 0, sy = 0, width = src.width, height = src.height, opacity = 1) {
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
    const xx = dx + x, yy = dy + y
    if (xx < 0 || yy < 0 || xx >= dst.width || yy >= dst.height) continue
    const si = ((sy + y) * src.width + sx + x) * 4, di = (yy * dst.width + xx) * 4
    const a = src.data[si + 3] / 255 * opacity, da = dst.data[di + 3] / 255, oa = a + da * (1 - a)
    if (!oa) continue
    for (let c = 0; c < 3; c++) dst.data[di + c] = Math.round((src.data[si + c] * a + dst.data[di + c] * da * (1 - a)) / oa)
    dst.data[di + 3] = Math.round(oa * 255)
  }
}
function crop(src, x, y, width, height) { const out = new PNG({ width, height }); composite(out, src, 0, 0, x, y, width, height); return out }
function resize(src, width, height) {
  const out = new PNG({ width, height })
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
    const fx = (x + .5) * src.width / width - .5, fy = (y + .5) * src.height / height - .5
    const x0 = Math.max(0, Math.floor(fx)), y0 = Math.max(0, Math.floor(fy)), x1 = Math.min(src.width - 1, x0 + 1), y1 = Math.min(src.height - 1, y0 + 1)
    const tx = Math.max(0, fx - x0), ty = Math.max(0, fy - y0)
    let pa = 0, pr = 0, pg = 0, pb = 0
    for (const [xx, yy, weight] of [[x0,y0,(1-tx)*(1-ty)],[x1,y0,tx*(1-ty)],[x0,y1,(1-tx)*ty],[x1,y1,tx*ty]]) {
      const i = (yy * src.width + xx) * 4, a = src.data[i + 3] / 255
      pa += a * weight; pr += src.data[i] * a * weight; pg += src.data[i + 1] * a * weight; pb += src.data[i + 2] * a * weight
    }
    const o = (y * width + x) * 4
    if (pa) { out.data[o] = Math.round(pr / pa); out.data[o + 1] = Math.round(pg / pa); out.data[o + 2] = Math.round(pb / pa); out.data[o + 3] = Math.round(pa * 255) }
  }
  return out
}
function thresholdAlpha(image, threshold = 18) {
  for (let i = 3; i < image.data.length; i += 4) if (image.data[i] < threshold) image.data[i - 3] = image.data[i - 2] = image.data[i - 1] = image.data[i] = 0
  return image
}
function largestComponentBox(image, x0, x1, threshold = 24) {
  const width = x1 - x0, height = image.height, seen = new Uint8Array(width * height)
  let best = null
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
    const q = y * width + x
    if (seen[q] || image.data[(y * image.width + x0 + x) * 4 + 3] < threshold) continue
    const stack = [q]; seen[q] = 1
    let count = 0, minX = x, maxX = x, minY = y, maxY = y
    while (stack.length) {
      const z = stack.pop(), xx = z % width, yy = (z - xx) / width
      count++; minX = Math.min(minX, xx); maxX = Math.max(maxX, xx); minY = Math.min(minY, yy); maxY = Math.max(maxY, yy)
      for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        const nx = xx + dx, ny = yy + dy, ni = ny * width + nx
        if (nx >= 0 && nx < width && ny >= 0 && ny < height && !seen[ni] && image.data[(ny * image.width + x0 + nx) * 4 + 3] >= threshold) { seen[ni] = 1; stack.push(ni) }
      }
    }
    if (!best || count > best.count) best = { count, x: x0 + minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1 }
  }
  if (!best) throw new Error(`No source component in x=${x0}..${x1}`)
  return best
}
function fitInto(src, width, height) {
  const scale = Math.min(width / src.width, height / src.height)
  return thresholdAlpha(resize(src, Math.max(1, Math.round(src.width * scale)), Math.max(1, Math.round(src.height * scale))))
}
function alphaBounds(image, threshold = 0) {
  let minX = image.width, minY = image.height, maxX = -1, maxY = -1, count = 0
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) if (image.data[(y * image.width + x) * 4 + 3] > threshold) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); count++
  }
  return count ? [minX, minY, maxX + 1, maxY + 1] : [0,0,0,0]
}
function write(image, name) { const file = path.join(raw, name); fs.writeFileSync(file, PNG.sync.write(image)); return file }
function copy(sourceFile, name) { const file = path.join(raw, name); fs.copyFileSync(sourceFile, file); return file }

const outputs = []
outputs.push(copy(path.join(v41Raw, 'dishwasher-off-native-room.png'), 'approved-kitchen-counter-room.png'))
outputs.push(copy(path.join(v41Raw, 'cabinet-a-le-re.png'), 'approved-counter-bay.png'))
outputs.push(copy(stateSource, 'source-quality-state-family.png'))
outputs.push(copy(brokenSource, 'source-quality-broken.png'))

// Preserve the already-established kitchen-native kettle at its authored 48 x 34
// pixels. V43 failed because a large generated painting was reduced to 44 pixels;
// V44 performs no resizing on the production kettle at all.
const nativeSheet = read(nativeSource), nativeBox = largestComponentBox(nativeSheet, 0, nativeSheet.width)
if (nativeBox.width !== 48 || nativeBox.height !== 34) throw new Error(`Native kettle authority drifted: ${nativeBox.width}x${nativeBox.height}`)
const nativeKettle = crop(nativeSheet, nativeBox.x, nativeBox.y, nativeBox.width, nativeBox.height)
function nativeCell() {
  const cell = new PNG({ width: 64, height: 64 })
  composite(cell, nativeKettle, 8, 26)
  return cell
}
const off = nativeCell(), on = clone(off)

function eraseRect(image, x, y, width, height) {
  for (let yy = y; yy < y + height; yy++) for (let xx = x; xx < x + width; xx++) {
    const i = (yy * image.width + xx) * 4
    image.data[i] = image.data[i + 1] = image.data[i + 2] = image.data[i + 3] = 0
  }
}
function setPixel(image, x, y, rgba) {
  if (x < 0 || y < 0 || x >= image.width || y >= image.height) return
  const i = (y * image.width + x) * 4
  for (let c = 0; c < 4; c++) image.data[i + c] = rgba[c]
}
function moveRegion(image, x, y, width, height, dx, dy) {
  const piece = crop(image, x, y, width, height)
  eraseRect(image, x, y, width, height)
  composite(image, piece, x + dx, y + dy)
}
function rotateNearest(image, degrees) {
  const out = new PNG({ width: image.width, height: image.height }), radians = degrees * Math.PI / 180
  const cos = Math.cos(radians), sin = Math.sin(radians), cx = (image.width - 1) / 2, cy = (image.height - 1) / 2
  for (let y = 0; y < out.height; y++) for (let x = 0; x < out.width; x++) {
    const rx = x - cx, ry = y - cy
    const sx = Math.round(cos * rx + sin * ry + cx), sy = Math.round(-sin * rx + cos * ry + cy)
    if (sx < 0 || sy < 0 || sx >= image.width || sy >= image.height) continue
    const si = (sy * image.width + sx) * 4, di = (y * out.width + x) * 4
    for (let c = 0; c < 4; c++) out.data[di + c] = image.data[si + c]
  }
  return out
}
function brokenCell() {
  const cell = clone(off)
  // Break the handle away from its left mount and leave the complete upper arc
  // visibly twisted and hanging from the surviving right side.
  const handle = crop(cell, 19, 26, 36, 18)
  const handleShard = crop(cell, 31, 27, 10, 6)
  eraseRect(cell, 19, 26, 36, 18)
  composite(cell, rotateNearest(handle, 18), 23, 30)
  eraseRect(cell, 31, 30, 13, 9)
  composite(cell, rotateNearest(handleShard, -24), 49, 53)
  eraseRect(cell, 19, 40, 7, 10)
  // Tear the lid upward and left so the dark open mouth remains visible.
  moveRegion(cell, 27, 43, 22, 7, -3, -4)
  // The spout tip is broken downward and no longer meets the original neck.
  moveRegion(cell, 8, 42, 11, 12, -1, 6)
  // Crush the right silhouette inward, then expose a large jagged metal cavity.
  eraseRect(cell, 52, 49, 4, 8)
  for (const [x,y] of [[47,49],[48,49],[49,49],[46,50],[47,50],[48,50],[49,50],[50,50],[46,51],[47,51],[48,51],[49,51],[50,51],[51,51],[46,52],[47,52],[48,52],[49,52],[50,52],[46,53],[47,53],[48,53],[49,53]]) setPixel(cell,x,y,[27,38,43,255])
  for (const [x,y] of [[46,48],[47,48],[48,48],[45,49],[50,49],[45,50],[51,50],[45,51],[45,52],[51,52],[45,53],[50,53],[46,54],[47,54],[48,54],[49,54]]) setPixel(cell,x,y,[196,239,240,255])
  for (const [x,y] of [[42,45],[43,46],[44,47],[43,48],[42,49],[41,50],[40,51],[39,52],[38,53]]) setPixel(cell,x,y,[20,35,42,255])
  // Scorched split at the severed handle mount; damage is part of the appliance,
  // while steam/sparks remain independent kettle-owned effect layers.
  for (const [x,y] of [[20,42],[21,43],[20,44],[22,45],[21,46],[23,47]]) setPixel(cell,x,y,[54,35,31,255])
  return cell
}
const broken = brokenCell()
const states = { off, on, broken }
for (const state of stateNames) outputs.push(write(states[state], `kettle-${state}.png`))

// Keep the broad base pinned while the upper body shears by up to two pixels.
// This gives the attached handle and lid a conspicuous mechanical rattle
// without letting the appliance bounce above the support surface.
function brokenRattleStrip() {
  const amplitudes = [0, 2, -2, 3, -3, 2, -2, 0]
  const strip = new PNG({ width: 64 * amplitudes.length, height: 64 })
  for (let frame = 0; frame < amplitudes.length; frame++) for (let y = 0; y < 64; y++) {
    const shift = Math.round(amplitudes[frame] * Math.max(0, Math.min(1, (59 - y) / 44)))
    for (let x = 0; x < 64; x++) {
      const sx = x - shift
      if (sx < 0 || sx >= 64) continue
      const si = (y * 64 + sx) * 4, di = (y * strip.width + frame * 64 + x) * 4
      for (let c = 0; c < 4; c++) strip.data[di + c] = broken.data[si + c]
    }
  }
  return strip
}
outputs.push(write(brokenRattleStrip(), 'kettle-broken-rattle-f8.png'))

const steam = read(steamSource), steamComponents = []
for (let i = 0; i < 5; i++) {
  const a = Math.floor(i * steam.width / 5), b = Math.floor((i + 1) * steam.width / 5)
  const box = largestComponentBox(steam, a, b)
  steamComponents.push(crop(steam, box.x, box.y, box.width, box.height))
}
const pathFrames = [0,1,2,3,4,3,2,1,0]
const effectSpecs = {
  on: {
    cell: [24, 32],
    sizes: { compact:[6,14], regular:[8,18], emphatic:[10,22] },
    opacity: { compact:.62, regular:.72, emphatic:.82 },
  },
  broken: {
    cell: [28, 36],
    sizes: { compact:[9,18], regular:[12,23], emphatic:[14,27] },
    opacity: { compact:.68, regular:.8, emphatic:.9 },
  },
}
function effectStrip(state, model) {
  const spec = effectSpecs[state], [cellW, cellH] = spec.cell, [targetW, targetH] = spec.sizes[model]
  const keys = steamComponents.map(component => fitInto(component, targetW, targetH))
  const strip = new PNG({ width: cellW * 40, height: cellH })
  for (let frame = 0; frame < 40; frame++) {
    const segment = Math.floor(frame / 5), t = (frame % 5) / 5, a = keys[pathFrames[segment]], b = keys[pathFrames[segment + 1]]
    const place = (image, amount) => composite(strip, image, frame * cellW + Math.round((cellW - image.width) / 2), cellH - 4 - image.height, 0, 0, image.width, image.height, amount * spec.opacity[model])
    place(a, 1 - t); place(b, t)
    if (state === 'broken') {
      const phase = frame % 8, ox = frame * cellW
      const sparks = [
        [4 + phase % 3, 24 - phase, [255,190,52,255]],
        [20 - phase % 4, 18 + phase % 5, [255,111,38,255]],
        [8 + (phase * 2) % 9, 11 + phase % 4, [255,227,124,230]],
      ]
      for (const [x,y,color] of sparks) {
        setPixel(strip, ox + x, y, color)
        if (phase % 2 === 0) setPixel(strip, ox + x + 1, y - 1, color)
      }
      if (phase === 2 || phase === 6) {
        setPixel(strip, ox + 22, 27, [139,196,201,255])
        setPixel(strip, ox + 23, 28, [139,196,201,220])
      }
    }
  }
  return strip
}
for (const state of ['on', 'broken']) for (const model of models) outputs.push(write(effectStrip(state, model), `fx-kettle-${state}-steam--${model}-f40.png`))

const baseRoom = read(path.join(raw, 'approved-kitchen-counter-room.png'))
// y=134 is the approved worktop's rear edge. Its visible top plane continues
// through y=140, so the kettle must end at y=140 (bottom-exclusive y=141).
const KETTLE_ORIGIN = 168, WORKTOP_Y = 134, SUPPORT_Y = 141, CELL_OFFSET = [10, -53]
const effectDefaults = {
  on: { dx: 30, dy: -52, width: 24, height: 32, model: 'regular' },
  broken: { dx: 44, dy: -58, width: 28, height: 36, model: 'regular' },
}
function proof(state, placedOrigin = KETTLE_ORIGIN) {
  const room = clone(baseRoom)
  composite(room, states[state], placedOrigin + CELL_OFFSET[0], WORKTOP_Y + CELL_OFFSET[1])
  if (state !== 'off') {
    const fx = read(path.join(raw, `fx-kettle-${state}-steam--regular-f40.png`)), spec = effectDefaults[state], frame = state === 'on' ? 13 : 22
    composite(room, fx, placedOrigin + spec.dx, WORKTOP_Y + spec.dy, frame * spec.width, 0, spec.width, spec.height)
  }
  return room
}
for (const state of stateNames) outputs.push(write(proof(state), `kettle-${state}-native-room.png`))
outputs.push(write(proof('off', 84), 'kettle-off-fridge-native-room.png'))

const stateBounds = Object.fromEntries(stateNames.map(state => [state, alphaBounds(states[state])]))
const effects = {}
for (const state of ['on', 'broken']) for (const model of models) {
  const spec = effectSpecs[state], defaults = effectDefaults[state], id = `kettle-${state}-steam-${model}`
  effects[id] = {
    file: `fx-kettle-${state}-steam--${model}-f40.png`,
    asset: 'kettle', anchorAssetId: 'kettle', transformSpace: 'asset-local', appliesToState: state,
    remainsAttachedWhileBroken: true, model, baseFps: 4, frameCount: 40, durationSeconds: 10,
    cellPixels: spec.cell, defaultTransform: { dx: defaults.dx, dy: defaults.dy, width: defaults.width, height: defaults.height, crop: [0,0,0,0], speed: 1 },
  }
}
const publishedAssets = Object.fromEntries(outputs.map(file => [path.basename(file), sha(file)]))
fs.mkdirSync(reviewAssets, { recursive: true })
for (const file of outputs) fs.copyFileSync(file, path.join(reviewAssets, path.basename(file)))
const v41 = JSON.parse(fs.readFileSync(v41Catalogue, 'utf8'))
const catalogue = {
  schema: 'lighthouse-keeper/kitchen-kettle-standalone@1', set, version: 44, status: 'reversible-unapproved-unpromoted',
  authorities: {
    dishwasherV41Catalogue: { file: path.relative(root, v41Catalogue), sha256: sha(v41Catalogue) },
    modularStandard: { file: 'docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md', sha256: sha(path.join(root, 'docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md')) },
  },
  sourceProvenance: {
    mode: 'unchanged kitchen-native raster authority; deterministic damage assembly; prior generated concept sources retained for honest review comparison',
    nativeProductionSource: { file: path.relative(root, nativeSource), sha256: sha(nativeSource) },
    stateFamily: { file: path.relative(root, stateSource), sha256: sha(stateSource) },
    brokenState: { file: path.relative(root, brokenSource), sha256: sha(brokenSource) },
    steamKeyframes: { file: path.relative(root, steamSource), sha256: sha(steamSource) },
    generationProvenance: { file: path.relative(root, generationProvenance), sha256: sha(generationProvenance) },
    generatedSourcesUsedAsProductionSprites: false,
    fullQualitySourcesPublishedForComparison: true,
  },
  geometry: {
    roomPixels: [772,224], bayWidthPixels: 84, worktopY: WORKTOP_Y, footLineY: 208, primeStopTurnY: 218,
    logicalFootprintPixels: [84,74], defaultOrigin: KETTLE_ORIGIN, compatibleCounterOrigins: compatibleOrigins, supportSurfaceSlots,
    primeAnchor: [KETTLE_ORIGIN + 42, 218], spriteCellPixels: [64,64], cellOffset: CELL_OFFSET,
    nativeEnvelopeTarget: '48 x 34 authored kitchen-native pixels, unchanged and unscaled; 48 px maximum including handle and spout against the documented 84 px / 60 cm bay',
    brokenDebrisEnvelope: '52 px maximum including the detached handle shard; still isolated inside the 64 px cell and one 84 px bay',
    visibleBounds: stateBounds, supportPlaneY: SUPPORT_Y, contactBottomExclusive: SUPPORT_Y,
  },
  states: {
    off: { file: 'kettle-off.png', effect: null },
    on: { file: 'kettle-on.png', casingSha256: sha(path.join(raw, 'kettle-on.png')), identicalToOff: sha(path.join(raw, 'kettle-on.png')) === sha(path.join(raw, 'kettle-off.png')), effectFamily: 'kettle-on-steam' },
    broken: { file: 'kettle-broken.png', bodyAnimation: { file: 'kettle-broken-rattle-f8.png', frameCount: 8, fps: 4, basePinnedToSupportY: 141 }, staticDamage: ['left handle mounting torn away', 'upper handle displaced and hanging from the surviving side', 'spout tip broken downward and visibly separated', 'large jagged enamel loss exposing dark metal', 'deep body fracture and scorched split'], effectFamily: 'kettle-broken-steam', movementLocked: true },
  },
  effects,
  brokenAssetLock: v41.brokenAssetLock,
  countertopOccupancy: {
    layer: 'countertop-appliance', compatibleOrigins, supportSurfaceSlots,
    placementPersistence: 'store supportAssetId, surfaceSlotId and asset-local placement; derive room origin and Keeper stop point from the current supporting bay',
    moveRule: 'Off/On commits only exact compatible counter origins, including the fridge worktop; Broken rejects direct move, bay-button movement and movement of its supporting asset',
    supportMoveRule: 'a support asset carrying a Broken kettle cannot move until the kettle is repaired or removed',
    movingKettleMovesSupportAsset: false, movingSupportMovesKettle: true,
    cabinetryMovesWithKettle: false, joinsRecomputed: false, reason: 'moving the kettle alone never moves its support; moving an unlocked support carries its locally anchored kettle and recomputes the dynamic tea stop',
  },
  teaInteraction: { actionId: 'make-cup-of-tea', dynamicPlace: true, keeperStopTurnY: 218, keeperStopTurnXRule: 'support bay origin + 42', facing: 'rear', resolvesFrom: ['supportAssetId','surfaceSlotId'], availableStates: ['off','on'], blockedState: 'broken' },
  soundPlaceholders: ['kitchen_kettle_heating_hiss_loop', 'kitchen_kettle_broken_handle_rattle', 'kitchen_kettle_broken_pressure_hiss_loop'],
  reviewProofs: [...stateNames.map(state => `kettle-${state}-native-room.png`), 'kettle-off-fridge-native-room.png'],
  boundaries: { dishwasherV41Changed: false, approvedCabinetryChanged: false, toasterStarted: false, mixingBowlStarted: false, runtimeControllerImplemented: false, finalChanged: false },
  publishedAssets,
}

const catalogueFile = path.join(draft, 'candidate-catalogue.json')
fs.writeFileSync(catalogueFile, `${JSON.stringify(catalogue, null, 2)}\n`)
const shell = path.join(review, 'index.html')
fs.writeFileSync(shell, fs.readFileSync(template, 'utf8').replace('__DATA__', JSON.stringify(catalogue)))
const sourceManifest = {
  set, status: 'source-only-unapproved', generationMode: 'native project source plus prior built-in image-generation concepts',
  files: { 'native/kettle-native-source.png': sha(nativeSource), 'v43/kettle-state-family-source.png': sha(stateSource), 'v43/kettle-broken-source.png': sha(brokenSource), 'v43/kettle-steam-keyframes-source.png': sha(steamSource) },
  normalization: 'Deterministic V44 builder; the native production source is copied without resizing, while generated sources are review references only.',
}
fs.writeFileSync(path.join(source, 'source-manifest.json'), `${JSON.stringify(sourceManifest, null, 2)}\n`)
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: catalogue.status,
  candidate: { catalogue: { file: path.relative(root, catalogueFile), sha256: sha(catalogueFile) }, publicShell: { file: path.relative(root, shell), sha256: sha(shell) } },
  sources: [v41Catalogue, nativeSource, stateSource, brokenSource, steamSource, generationProvenance].map(file => ({ file: path.relative(root, file), sha256: sha(file) })),
  publishedAssets: outputs.map(file => ({ source: path.relative(root, file), sourceSha256: sha(file), publicAssemblyPath: path.posix.join('public/keeper-review', set, 'assets', path.basename(file)) })),
}
fs.writeFileSync(path.join(draft, 'batch-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log(`Built Kitchen Kettle Standalone V44: ${outputs.length} review assets; unscaled 48 x 34 native kettle seated at y140 on exact V41 counters.`)
