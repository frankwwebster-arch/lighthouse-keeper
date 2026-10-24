#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const MASTER_FILE = 'art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png'
const MASTER_HASH = 'a8a6972dd8398ec3cd52f42825a5a5f056a1e289d10b77796f3294b3ac85ab98'
const BOWL_PLATE_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/sources/generated-broken-bowl-source-plate.png'
const BOWL_PLATE_HASH = '799837c86163cbbdeed3a377dfd52ecff28838f50c24980527b168abd356effe'
const CHAIR_PLATE_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/sources/generated-rear-chair-source-plate.png'
const CHAIR_PLATE_HASH = 'c91b6197f016fff31bb1a884812e0dd236c0b7e1e921061aebef858fa8f605a3'
const STEAM_FILE = 'art/drafts/activity-story-ink-marks-and-recipe-pictures-2026-10-22-v1/drafts/components/symbol-steam-puff.png'
const KEEPER_FILE = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f1.png'
const SEATED_KEEPER_FILE = 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/drafts/frames/keeper_prime_stand-to-sit-back_f06.png'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v3/assets'
const PAD = 4

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const readChecked = (file, expected) => {
  const bytes = fs.readFileSync(path.join(ROOT, file))
  if (expected && sha256(bytes) !== expected) throw new Error(`${file} authority hash changed`)
  return { bytes, png: PNG.sync.read(bytes) }
}
const master = readChecked(MASTER_FILE, MASTER_HASH)
const bowlPlate = readChecked(BOWL_PLATE_FILE, BOWL_PLATE_HASH)
const chairPlate = readChecked(CHAIR_PLATE_FILE, CHAIR_PLATE_HASH)
const steam = readChecked(STEAM_FILE)
const keeper = readChecked(KEEPER_FILE)
const seatedKeeper = readChecked(SEATED_KEEPER_FILE)
for (const [label, image] of [['master', master.png], ['broken-bowl plate', bowlPlate.png], ['rear-chair plate', chairPlate.png]]) {
  if (image.width !== 1536 || image.height !== 1024) throw new Error(`${label} must remain 1536 x 1024`)
}

const backgroundLike = (r, g, b, a) => a > 0 && r >= 238 && g >= 234 && b >= 216 && r - g <= 18 && g - b >= 0 && g - b <= 32
function cropPixels(source, [x, y, width, height]) {
  const output = new PNG({ width, height })
  for (let py = 0; py < height; py += 1) {
    const from = ((y + py) * source.width + x) * 4
    const to = py * width * 4
    source.data.copy(output.data, to, from, from + width * 4)
  }
  return output
}
function removeBorderPaper(image) {
  const outside = new Uint8Array(image.width * image.height)
  const queue = []
  const enqueue = (x, y) => {
    const pixel = y * image.width + x
    if (outside[pixel]) return
    const i = pixel * 4
    if (!backgroundLike(image.data[i], image.data[i + 1], image.data[i + 2], image.data[i + 3])) return
    outside[pixel] = 1
    queue.push(pixel)
  }
  for (let x = 0; x < image.width; x += 1) { enqueue(x, 0); enqueue(x, image.height - 1) }
  for (let y = 1; y < image.height - 1; y += 1) { enqueue(0, y); enqueue(image.width - 1, y) }
  for (let head = 0; head < queue.length; head += 1) {
    const pixel = queue[head], x = pixel % image.width, y = Math.floor(pixel / image.width)
    if (x) enqueue(x - 1, y)
    if (x + 1 < image.width) enqueue(x + 1, y)
    if (y) enqueue(x, y - 1)
    if (y + 1 < image.height) enqueue(x, y + 1)
  }
  for (let pixel = 0; pixel < outside.length; pixel += 1) if (outside[pixel]) image.data[pixel * 4 + 3] = 0
  return image
}
function clearGeneratedPaper(image) {
  for (let pixel = 0; pixel < image.width * image.height; pixel += 1) {
    const i = pixel * 4, r = image.data[i], g = image.data[i + 1], b = image.data[i + 2]
    if (r >= 236 && g >= 236 && b >= 226 && Math.max(r, g, b) - Math.min(r, g, b) <= 28) image.data[i + 3] = 0
  }
  return image
}
function pad(image, amount = PAD) {
  const output = new PNG({ width: image.width + amount * 2, height: image.height + amount * 2 })
  for (let y = 0; y < image.height; y += 1) image.data.copy(output.data, ((y + amount) * output.width + amount) * 4, y * image.width * 4, (y + 1) * image.width * 4)
  return output
}
function cutout(source, crop) { return pad(removeBorderPaper(cropPixels(source, crop))) }
function blit(source, target, dx, dy) {
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    const sx = (y * source.width + x) * 4, tx = x + dx, ty = y + dy
    if (tx < 0 || ty < 0 || tx >= target.width || ty >= target.height || source.data[sx + 3] === 0) continue
    const ti = (ty * target.width + tx) * 4
    source.data.copy(target.data, ti, sx, sx + 4)
  }
}
function alphaBounds(image) {
  let minX = image.width, minY = image.height, maxX = -1, maxY = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  if (maxX < 0) throw new Error('empty cutout')
  return [minX, minY, maxX - minX + 1, maxY - minY + 1]
}
function trim(image) { return cropPixels(image, alphaBounds(image)) }
function seamExtend(source, width, height, seamX, insertX, seamY1, insertY1, seamY2, insertY2) {
  const target = new PNG({ width, height })
  for (let y = 0; y < height; y += 1) for (let x = 0; x < width; x += 1) {
    const sx = x < seamX ? x : x < seamX + insertX ? seamX : x - insertX
    let sy = y
    if (y >= seamY1 && y < seamY1 + insertY1) sy = seamY1
    else if (y >= seamY1 + insertY1 && y < seamY2 + insertY1) sy = y - insertY1
    else if (y >= seamY2 + insertY1 && y < seamY2 + insertY1 + insertY2) sy = seamY2
    else if (y >= seamY2 + insertY1 + insertY2) sy = y - insertY1 - insertY2
    if (sx < source.width && sy < source.height) source.data.copy(target.data, (y * width + x) * 4, (sy * source.width + sx) * 4, (sy * source.width + sx) * 4 + 4)
  }
  return target
}

const outputs = {}
const write = (id, image, metadata) => {
  const bytes = PNG.sync.write(image, { colorType: 6 })
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(ROOT, OUT, filename), bytes)
  fs.writeFileSync(path.join(ROOT, PUBLIC, filename), bytes)
  outputs[id] = { file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, dimensions: [image.width, image.height], sha256: sha256(bytes), ...metadata }
}
fs.mkdirSync(path.join(ROOT, OUT), { recursive: true })
fs.mkdirSync(path.join(ROOT, PUBLIC), { recursive: true })
fs.writeFileSync(path.join(ROOT, PUBLIC, 'kitchen-v4-master.png'), master.bytes)
fs.writeFileSync(path.join(ROOT, PUBLIC, 'prime-keeper-neutral-native-256x320.png'), keeper.bytes)
fs.writeFileSync(path.join(ROOT, PUBLIC, 'prime-keeper-seated-back-native.png'), seatedKeeper.bytes)

const standard = {
  'toaster-off': { crop: [38, 915, 111, 90], contactRow: 80 },
  'toaster-broken': { crop: [258, 874, 124, 136], contactRow: 123 },
  'kettle-off': { crop: [392, 886, 116, 120], contactRow: 111 },
  'bin-standard': { crop: [764, 876, 91, 133], contactRow: 128 },
  'bin-broken': { crop: [843, 866, 135, 145], contactRow: 140 },
  'bowl-standard': { crop: [985, 880, 115, 130], contactRow: 121 },
}
for (const [id, spec] of Object.entries(standard)) write(id, cutout(master.png, spec.crop), { source: MASTER_FILE, crop: spec.crop, contactRow: spec.contactRow, method: 'native 1:1 crop; only border-connected paper cleared; four-pixel transparent gutter' })

// ON is the byte-identical OFF toaster body with only native toast pixels added behind it.
const toasterOff = PNG.sync.read(fs.readFileSync(path.join(ROOT, outputs['toaster-off'].file)))
const toast = cutout(master.png, [164, 888, 82, 48])
const toasterOn = new PNG({ width: toasterOff.width, height: toasterOff.height + 48 })
blit(toast, toasterOn, 15, 0)
blit(toasterOff, toasterOn, 0, 48)
write('toaster-on', toasterOn, { source: MASTER_FILE, sourceAdditiveCrop: [164, 888, 82, 48], base: 'toaster-off', baseOffset: [0, 48], contactRow: outputs['toaster-off'].contactRow + 48, method: 'byte-identical OFF body plus native 1:1 toast-only layer; no neighbouring broken sprite pixels' })

// ON is the byte-identical OFF kettle body with only a native steam wisp added at the spout.
const kettleOff = PNG.sync.read(fs.readFileSync(path.join(ROOT, outputs['kettle-off'].file)))
const steamWisp = cropPixels(steam.png, [100, 20, 55, 216])
const kettleOn = new PNG({ width: 155, height: 308 })
blit(steamWisp, kettleOn, 96, 4)
blit(kettleOff, kettleOn, 0, 180)
write('kettle-on', kettleOn, { source: MASTER_FILE, additiveSource: STEAM_FILE, additiveCrop: [100, 20, 55, 216], base: 'kettle-off', baseOffset: [0, 180], contactRow: outputs['kettle-off'].contactRow + 180, method: 'byte-identical OFF body plus native 1:1 steam-only layer at spout' })

// The former ON drawing is the approved broken visual; the former loose-lid BROKEN drawing is excluded.
write('kettle-broken', cutout(master.png, [498, 886, 122, 120]), { source: MASTER_FILE, crop: [498, 886, 122, 120], contactRow: 111, replacesV2State: 'on', excludedV2Crop: [620, 872, 120, 137], method: 'native 1:1 crop; reclassified from ON to BROKEN exactly as requested' })

write('bowl-broken', pad(clearGeneratedPaper(removeBorderPaper(cropPixels(bowlPlate.png, [1085, 879, 145, 134])))), { source: BOWL_PLATE_FILE, crop: [1085, 879, 145, 134], contactRow: 135, method: 'native 1:1 crop from versioned generated correction plate; generated paper cleared; deeper break and left/below shards; no right-hand whisk artefact' })

// Preserve native pixels while extending straight wood runs to the authoritative furniture datums.
const tableSource = trim(removeBorderPaper(cropPixels(master.png, [1230, 887, 194, 118])))
const tablePhysical = seamExtend(tableSource, 217, 157, Math.floor(tableSource.width / 2), 217 - tableSource.width, 58, 157 - tableSource.height, 1000, 0)
write('table-standard', pad(tablePhysical), { source: MASTER_FILE, sourceCrop: [1230, 887, 194, 118], logicalDimensions: [20, 14.5], physicalDimensions: [217, 157], contactRow: 160, method: 'native-pixel seam extension of straight central wood runs; no scaling, resampling or colour transform' })

const chairSource = trim(clearGeneratedPaper(removeBorderPaper(cropPixels(chairPlate.png, [1422, 872, 96, 136]))))
const chairInsertX = 261 - chairSource.width
const chairInsertY = 228 - chairSource.height
let chairSeamX = Math.floor(chairSource.width / 2), fewest = Infinity
for (let x = Math.floor(chairSource.width * .3); x <= Math.floor(chairSource.width * .7); x += 1) {
  let opaque = 0
  for (let y = Math.floor(chairSource.height * .2); y < Math.floor(chairSource.height * .67); y += 1) if (chairSource.data[(y * chairSource.width + x) * 4 + 3]) opaque += 1
  if (opaque < fewest) { fewest = opaque; chairSeamX = x }
}
const chairPhysical = seamExtend(chairSource, 261, 228, chairSeamX, chairInsertX, 47, Math.round(chairInsertY * .68), 99, chairInsertY - Math.round(chairInsertY * .68))
const chairSlat = cropPixels(chairPhysical, [219, 25, 8, 119])
for (const x of [57, 103, 149, 195]) blit(chairSlat, chairPhysical, x, 25)
write('chair-standard', pad(chairPhysical), { source: CHAIR_PLATE_FILE, sourceCrop: [1422, 872, 96, 136], facing: 'rear', visibleSurface: 'rear of chair', logicalDimensions: [24, 21], backrestWidthLogicalPixels: 19, seatTopLogicalPixels: 7.75, physicalDimensions: [261, 228], contactRow: 231, method: 'rear-facing generated source; native-pixel straight-run extension to approved sit geometry; no scaling, resampling or colour transform' })

const register = {
  schema: 'lighthouse-keeper/kitchen-native-assets@2', status: 'review-only-unapproved-v3-correction', createdOn: '2026-10-24',
  source: MASTER_FILE, sourceSha256: MASTER_HASH, sourceDimensions: [1536, 1024], scaleApplied: false, resamplingApplied: false, colourTransformApplied: false,
  correctionSources: {
    brokenBowl: { file: BOWL_PLATE_FILE, sha256: BOWL_PLATE_HASH, use: 'only the broken-bowl crop' },
    rearChair: { file: CHAIR_PLATE_FILE, sha256: CHAIR_PLATE_HASH, use: 'only the rear-chair crop before native-pixel straight-run extension' },
    steam: { file: STEAM_FILE, sha256: sha256(steam.bytes), use: 'native 1:1 steam wisp only' },
  },
  keeperScaleReference: { source: KEEPER_FILE, sha256: sha256(keeper.bytes), dimensions: [keeper.png.width, keeper.png.height] },
  seatedFitReference: { source: SEATED_KEEPER_FILE, sha256: sha256(seatedKeeper.bytes), dimensions: [seatedKeeper.png.width, seatedKeeper.png.height], role: 'approved rear-sitting frame used only for furniture fit proof' },
  fittedRunCrop: { width: 1368, height: 284, sourceX: 65, sourceYByState: { off: 0, on: 282, broken: 570 }, includesTapCrown: true },
  outputs,
}
fs.writeFileSync(path.join(ROOT, OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log(`Built ${Object.keys(outputs).length} Kitchen V3 native assets with no scaling or resampling.`)
