#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const V4_REGISTER_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v4/native-assets/extraction-register.json'
const V4_REGISTER_HASH = '5d38f77151ccc00d834759f0d72a71b1152cb9c3ea09f2b80f3853d03a5c63a7'
const LOOSE_SOURCE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v5/sources/generated-loose-family-source-plate.png'
const LOOSE_HASH = '2bb031ee62f70cc4231f8ad6efe3d3b4e351ccc98a0cbcb1be99b428744cdd5f'
const FURNITURE_SOURCE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v5/sources/generated-furniture-source-plate.png'
const FURNITURE_HASH = 'acaee761d88d1ff0832cd8ad8c9c767e579749ddeadb144a73ec84301ccfb24d'
const KEEPER_FILE = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f1.png'
const SEATED_KEEPER_FILE = 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/drafts/frames/keeper_prime_stand-to-sit-back_f06.png'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-24-v5/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v5/assets'
const PAD = 8

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const read = (file, expected) => {
  const bytes = fs.readFileSync(path.join(ROOT, file))
  if (expected && sha256(bytes) !== expected) throw new Error(`${file} authority hash changed`)
  return { bytes, png: PNG.sync.read(bytes) }
}
const v4Bytes = fs.readFileSync(V4_REGISTER_FILE)
if (sha256(v4Bytes) !== V4_REGISTER_HASH) throw new Error('V4 register changed')
const v4 = JSON.parse(v4Bytes)
const loose = read(LOOSE_SOURCE, LOOSE_HASH)
const furniture = read(FURNITURE_SOURCE, FURNITURE_HASH)
const keeper = read(KEEPER_FILE)
const seatedKeeper = read(SEATED_KEEPER_FILE)
if (loose.png.width !== 1536 || loose.png.height !== 1024) throw new Error('V5 loose source geometry changed')

function blank(width, height) { return new PNG({ width, height }) }
function crop(source, [x, y, width, height]) {
  const output = blank(width, height)
  for (let py = 0; py < height; py += 1) source.data.copy(output.data, py * width * 4, ((y + py) * source.width + x) * 4, ((y + py) * source.width + x + width) * 4)
  return output
}
function components(image, threshold = 1) {
  const seen = new Uint8Array(image.width * image.height), result = []
  for (let sy = 0; sy < image.height; sy += 1) for (let sx = 0; sx < image.width; sx += 1) {
    const start = sy * image.width + sx
    if (seen[start] || image.data[start * 4 + 3] < threshold) continue
    const pixels = [start]; seen[start] = 1
    for (let head = 0; head < pixels.length; head += 1) {
      const p = pixels[head], x = p % image.width, y = Math.floor(p / image.width)
      for (let dy = -1; dy <= 1; dy += 1) for (let dx = -1; dx <= 1; dx += 1) {
        if (!dx && !dy) continue
        const xx = x + dx, yy = y + dy
        if (xx < 0 || yy < 0 || xx >= image.width || yy >= image.height) continue
        const next = yy * image.width + xx
        if (!seen[next] && image.data[next * 4 + 3] >= threshold) { seen[next] = 1; pixels.push(next) }
      }
    }
    result.push(pixels)
  }
  return result.sort((a, b) => b.length - a.length)
}
function keepComponents(image, minimumPixels = 20, threshold = 1) {
  const output = blank(image.width, image.height)
  for (const component of components(image, threshold)) if (component.length >= minimumPixels) for (const p of component) image.data.copy(output.data, p * 4, p * 4, p * 4 + 4)
  return output
}
function trim(image) {
  let x0 = image.width, y0 = image.height, x1 = -1, y1 = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y) }
  if (x1 < 0) throw new Error('empty image')
  return crop(image, [x0, y0, x1 - x0 + 1, y1 - y0 + 1])
}
function blit(source, target, dx, dy) {
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    const si = (y * source.width + x) * 4
    if (!source.data[si + 3]) continue
    source.data.copy(target.data, ((y + dy) * target.width + x + dx) * 4, si, si + 4)
  }
}
function pad(image) { const output = blank(image.width + PAD * 2, image.height + PAD * 2); blit(image, output, PAD, PAD); return output }
function cleanGeneratedCrop(box) {
  const image = crop(loose.png, box)
  for (let i = 3; i < image.data.length; i += 4) if (image.data[i] < 40) image.data[i] = 0
  return pad(trim(keepComponents(image, 20, 1)))
}
function clearPaper(image) {
  const seen = new Uint8Array(image.width * image.height), queue = []
  const paper = p => { const i = p * 4, r = image.data[i], g = image.data[i + 1], b = image.data[i + 2]; return r >= 232 && g >= 225 && b >= 202 && r - b <= 55 }
  const add = (x, y) => { const p = y * image.width + x; if (seen[p] || !paper(p)) return; seen[p] = 1; queue.push(p) }
  for (let x = 0; x < image.width; x += 1) { add(x, 0); add(x, image.height - 1) }
  for (let y = 1; y < image.height - 1; y += 1) { add(0, y); add(image.width - 1, y) }
  for (let head = 0; head < queue.length; head += 1) { const p = queue[head], x = p % image.width, y = Math.floor(p / image.width); if (x) add(x - 1, y); if (x + 1 < image.width) add(x + 1, y); if (y) add(x, y - 1); if (y + 1 < image.height) add(x, y + 1) }
  for (let p = 0; p < seen.length; p += 1) if (seen[p]) image.data[p * 4 + 3] = 0
  return image
}
function cleanFurnitureCrop(box) { return pad(trim(keepComponents(clearPaper(crop(furniture.png, box)), 20, 1))) }
const contactRow = image => { let row = -1; for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) row = y; return row }

fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(PUBLIC, { recursive: true })
const outputs = {}
function writePng(id, image, metadata) {
  const bytes = PNG.sync.write(image, { colorType: 6 }), filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes); fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, dimensions: [image.width, image.height], sha256: sha256(bytes), ...metadata }
}
function inherit(id) {
  const source = v4.outputs[id], bytes = fs.readFileSync(source.file), filename = `${id}-native.png`
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V4 fitted lock changed`)
  fs.writeFileSync(path.join(OUT, filename), bytes); fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { ...source, file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, inheritedByteIdenticalFromV4: true }
}
for (const id of ['fitted-units-static','fitted-overlay-on','fitted-overlay-broken','dishwasher-warning-1','dishwasher-warning-2','dishwasher-warning-3','oven-broken-cavity-light','broken-floor-water']) inherit(id)

const crops = {
  'toaster-off': [30, 875, 145, 140], 'toaster-on': [176, 875, 148, 140], 'toaster-broken': [330, 875, 178, 145],
  'kettle-off': [515, 875, 148, 145], 'kettle-broken': [674, 875, 152, 145],
  'bin-standard': [846, 865, 126, 150], 'bin-broken': [969, 862, 183, 155],
  'bowl-standard': [1165, 875, 145, 140], 'bowl-broken': [1308, 900, 198, 115],
}
for (const [id, box] of Object.entries(crops)) {
  const image = cleanGeneratedCrop(box)
  writePng(id, image, { source: LOOSE_SOURCE, sourceCrop: box, contactRow: contactRow(image), anchorX: Math.round(image.width / 2), generatedRedraw: true, downscalingApplied: false, shadowAuthoredWithObject: true })
}
// ON is deliberately the exact OFF kettle body. Steam remains a separate future effect.
const kettleOn = fs.readFileSync(outputs['kettle-off'].file)
fs.writeFileSync(path.join(OUT, 'kettle-on-native.png'), kettleOn); fs.writeFileSync(path.join(PUBLIC, 'kettle-on-native.png'), kettleOn)
outputs['kettle-on'] = { ...outputs['kettle-off'], file: `${OUT}/kettle-on-native.png`, publicReviewFile: `${PUBLIC}/kettle-on-native.png`, byteIdenticalTo: 'kettle-off', steamLayer: 'separate-not-drawn' }

const table = cleanFurnitureCrop([45, 920, 380, 300])
const chair = cleanFurnitureCrop([430, 910, 190, 310])
writePng('table-standard', table, { source: FURNITURE_SOURCE, sourceCrop: [45, 920, 380, 300], contactRow: contactRow(table), anchorX: Math.round(table.width / 2), physicalModelMm: { height: 750, width: 1050 }, generatedRedraw: true, downscalingApplied: false })
writePng('chair-standard', chair, { source: FURNITURE_SOURCE, sourceCrop: [430, 910, 190, 310], contactRow: contactRow(chair), anchorX: Math.round(chair.width / 2), facing: 'rear', physicalModelMm: { overallHeight: 900, seatHeight: 460 }, generatedRedraw: true, downscalingApplied: false })

fs.writeFileSync(path.join(PUBLIC, 'prime-keeper-neutral-native-256x320.png'), keeper.bytes)
fs.writeFileSync(path.join(PUBLIC, 'prime-keeper-seated-back-native-256x320.png'), seatedKeeper.bytes)
const register = {
  schema: 'lighthouse-keeper/kitchen-native-assets@5', status: 'review-only-unapproved-v5-redraft', createdOn: '2026-10-24',
  fittedUnits: { register: V4_REGISTER_FILE, registerSha256: V4_REGISTER_HASH, lockedBaseSha256: outputs['fitted-units-static'].sha256, changed: false },
  sources: { loose: { file: LOOSE_SOURCE, sha256: LOOSE_HASH, dimensions: [loose.png.width, loose.png.height] }, furniture: { file: FURNITURE_SOURCE, sha256: FURNITURE_HASH, dimensions: [furniture.png.width, furniture.png.height] } },
  scaleApplied: false, downscalingApplied: false, resamplingApplied: false, colourTransformApplied: false,
  worldDensity: { kitchenPixelsPerLogicalPixel: 228 / 21, keeperSourcePixelsPerLogicalPixel: 8, keeperDisplayScale: 228 / 168, keeperDisplayCell: [347.428571, 434.285714], cabinetWorktopHeightPixels: 213, cabinetWorktopModelMm: 850, primeKeeperModelMm: 1750 },
  placement: { counterSupportLocalY: 84, previousCounterSupportLocalY: 71, movement: '13 native pixels forward onto visible worktop plane', sourcePixelsPerPace: 114 },
  globalStateMap: { off: { toaster: 'off', kettle: 'off', bin: 'standard', bowl: 'standard' }, on: { toaster: 'on', kettle: 'on', bin: 'standard', bowl: 'standard' }, broken: { toaster: 'broken', kettle: 'broken', bin: 'broken', bowl: 'broken' } },
  keeperPresentation: { neutral: { file: KEEPER_FILE, sha256: sha256(keeper.bytes) }, seated: { file: SEATED_KEEPER_FILE, sha256: sha256(seatedKeeper.bytes) }, sourceDimensions: [256, 320], displayDimensions: [347.428571, 434.285714], rationale: 'Prime and kitchen share one world density; camera zoom then scales the composed world uniformly' },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log(`Built ${Object.keys(outputs).length} Kitchen V5 native assets; fitted units remained byte-identical.`)
