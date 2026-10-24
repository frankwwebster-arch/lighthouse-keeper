#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const MASTER_FILE = 'art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png'
const MASTER_HASH = 'a8a6972dd8398ec3cd52f42825a5a5f056a1e289d10b77796f3294b3ac85ab98'
const V3_REGISTER_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/native-assets/extraction-register.json'
const V3_REGISTER_HASH = '5d22d5db0a8906e09dfd821489e53ad3e8ad27f6dd58950e9411323cd63ac5f7'
const BOWL_PLATE_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/sources/generated-broken-bowl-source-plate.png'
const BOWL_PLATE_HASH = '799837c86163cbbdeed3a377dfd52ecff28838f50c24980527b168abd356effe'
const CHAIR_PLATE_FILE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v3/sources/generated-rear-chair-source-plate.png'
const CHAIR_PLATE_HASH = 'c91b6197f016fff31bb1a884812e0dd236c0b7e1e921061aebef858fa8f605a3'
const KEEPER_FILE = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f1.png'
const SEATED_KEEPER_FILE = 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/drafts/frames/keeper_prime_stand-to-sit-back_f06.png'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-24-v4/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v4/assets'
const PAD = 4

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const read = (file, expected) => {
  const bytes = fs.readFileSync(path.join(ROOT, file))
  if (expected && sha256(bytes) !== expected) throw new Error(`${file} authority hash changed`)
  return { bytes, png: PNG.sync.read(bytes) }
}
const master = read(MASTER_FILE, MASTER_HASH)
if (sha256(fs.readFileSync(V3_REGISTER_FILE)) !== V3_REGISTER_HASH) throw new Error('V3 extraction register changed')
const v3 = JSON.parse(fs.readFileSync(V3_REGISTER_FILE, 'utf8'))
const bowlPlate = read(BOWL_PLATE_FILE, BOWL_PLATE_HASH)
const chairPlate = read(CHAIR_PLATE_FILE, CHAIR_PLATE_HASH)
const keeper = read(KEEPER_FILE)
const seatedKeeper = read(SEATED_KEEPER_FILE)
if (master.png.width !== 1536 || master.png.height !== 1024) throw new Error('Kitchen V4 master geometry changed')

function blank(width, height) { return new PNG({ width, height }) }
function crop(source, [x, y, width, height]) {
  const output = blank(width, height)
  for (let py = 0; py < height; py += 1) source.data.copy(output.data, py * width * 4, ((y + py) * source.width + x) * 4, ((y + py) * source.width + x + width) * 4)
  return output
}
function blit(source, target, dx, dy, replace = false) {
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    const si = (y * source.width + x) * 4, tx = x + dx, ty = y + dy
    if (tx < 0 || ty < 0 || tx >= target.width || ty >= target.height) continue
    if (!replace && source.data[si + 3] === 0) continue
    source.data.copy(target.data, (ty * target.width + tx) * 4, si, si + 4)
  }
}
function clearRect(image, [x, y, width, height]) {
  for (let py = Math.max(0, y); py < Math.min(image.height, y + height); py += 1) image.data.fill(0, (py * image.width + Math.max(0, x)) * 4, (py * image.width + Math.min(image.width, x + width)) * 4)
}
const paperLike = (r, g, b, a) => a > 0 && r >= 236 && g >= 232 && b >= 216 && r - g <= 22 && g - b >= -3 && g - b <= 34
const generatedPaperLike = (r, g, b, a) => a > 0 && r >= 236 && g >= 236 && b >= 226 && Math.max(r, g, b) - Math.min(r, g, b) <= 28
function clearPaper(image, predicate = paperLike, global = false) {
  if (global) {
    for (let pixel = 0; pixel < image.width * image.height; pixel += 1) {
      const i = pixel * 4
      if (predicate(image.data[i], image.data[i + 1], image.data[i + 2], image.data[i + 3])) image.data[i + 3] = 0
    }
    return image
  }
  const seen = new Uint8Array(image.width * image.height), queue = []
  const add = (x, y) => {
    const p = y * image.width + x
    if (seen[p]) return
    const i = p * 4
    if (!predicate(image.data[i], image.data[i + 1], image.data[i + 2], image.data[i + 3])) return
    seen[p] = 1; queue.push(p)
  }
  for (let x = 0; x < image.width; x += 1) { add(x, 0); add(x, image.height - 1) }
  for (let y = 1; y < image.height - 1; y += 1) { add(0, y); add(image.width - 1, y) }
  for (let head = 0; head < queue.length; head += 1) {
    const p = queue[head], x = p % image.width, y = Math.floor(p / image.width)
    if (x) add(x - 1, y); if (x + 1 < image.width) add(x + 1, y); if (y) add(x, y - 1); if (y + 1 < image.height) add(x, y + 1)
  }
  for (let p = 0; p < seen.length; p += 1) if (seen[p]) image.data[p * 4 + 3] = 0
  return image
}
function components(image) {
  const seen = new Uint8Array(image.width * image.height), result = []
  for (let sy = 0; sy < image.height; sy += 1) for (let sx = 0; sx < image.width; sx += 1) {
    const start = sy * image.width + sx
    if (seen[start] || image.data[start * 4 + 3] === 0) continue
    const pixels = [start]; seen[start] = 1
    let minX = sx, minY = sy, maxX = sx, maxY = sy
    for (let head = 0; head < pixels.length; head += 1) {
      const p = pixels[head], x = p % image.width, y = Math.floor(p / image.width)
      minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y)
      for (let dy = -1; dy <= 1; dy += 1) for (let dx = -1; dx <= 1; dx += 1) {
        if (!dx && !dy) continue
        const xx = x + dx, yy = y + dy
        if (xx < 0 || yy < 0 || xx >= image.width || yy >= image.height) continue
        const next = yy * image.width + xx
        if (!seen[next] && image.data[next * 4 + 3]) { seen[next] = 1; pixels.push(next) }
      }
    }
    result.push({ pixels, bounds: [minX, minY, maxX, maxY] })
  }
  return result.sort((a, b) => b.pixels.length - a.pixels.length)
}
function keepComponents(image, test) {
  const output = blank(image.width, image.height)
  for (const [index, component] of components(image).entries()) if (test(component, index)) for (const p of component.pixels) image.data.copy(output.data, p * 4, p * 4, p * 4 + 4)
  return output
}
function trim(image) {
  let x0 = image.width, y0 = image.height, x1 = -1, y1 = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y) }
  if (x1 < 0) throw new Error('empty image')
  return crop(image, [x0, y0, x1 - x0 + 1, y1 - y0 + 1])
}
function pad(image) { const output = blank(image.width + PAD * 2, image.height + PAD * 2); blit(image, output, PAD, PAD); return output }
function clearAfter(image, lastRow) { for (let y = lastRow + 1; y < image.height; y += 1) image.data.fill(0, y * image.width * 4, (y + 1) * image.width * 4); return image }
function removeWarmShadow(image, startRatio = .62) {
  const start = Math.floor(image.height * startRatio)
  const shadowLike = pixel => {
    const i = pixel * 4, r = image.data[i], g = image.data[i + 1], b = image.data[i + 2]
    return image.data[i + 3] > 0 && r >= 185 && r < 248 && g >= 155 && g < 235 && b >= 115 && b < 210 && r - g <= 45 && g - b <= 52
  }
  const seen = new Uint8Array(image.width * image.height), queue = []
  const add = (x, y) => {
    const pixel = y * image.width + x
    if (seen[pixel]) return
    const transparent = image.data[pixel * 4 + 3] === 0
    if (!transparent && !(y >= start && shadowLike(pixel))) return
    seen[pixel] = 1; queue.push(pixel)
  }
  for (let x = 0; x < image.width; x += 1) { add(x, 0); add(x, image.height - 1) }
  for (let y = 1; y < image.height - 1; y += 1) { add(0, y); add(image.width - 1, y) }
  for (let head = 0; head < queue.length; head += 1) {
    const pixel = queue[head], x = pixel % image.width, y = Math.floor(pixel / image.width)
    if (x) add(x - 1, y); if (x + 1 < image.width) add(x + 1, y); if (y) add(x, y - 1); if (y + 1 < image.height) add(x, y + 1)
  }
  for (let pixel = 0; pixel < seen.length; pixel += 1) if (seen[pixel] && shadowLike(pixel)) image.data[pixel * 4 + 3] = 0
  return image
}
function largestClean(file, lastRow) {
  const source = PNG.sync.read(fs.readFileSync(file))
  const kept = keepComponents(source, (_component, index) => index === 0)
  const withoutShadow = removeWarmShadow(lastRow == null ? kept : clearAfter(kept, lastRow))
  return pad(trim(keepComponents(withoutShadow, (_component, index) => index === 0)))
}
function seamExtend(source, width, height, seamX, insertX, seamY, insertY) {
  const output = blank(width, height)
  for (let y = 0; y < height; y += 1) for (let x = 0; x < width; x += 1) {
    const sx = x < seamX ? x : x < seamX + insertX ? seamX : x - insertX
    const sy = y < seamY ? y : y < seamY + insertY ? seamY : y - insertY
    if (sx < source.width && sy < source.height) source.data.copy(output.data, (y * width + x) * 4, (sy * source.width + sx) * 4, (sy * source.width + sx) * 4 + 4)
  }
  return output
}
const contactRow = image => { let row = -1; for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) row = y; return row }

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
const outputs = {}
function write(id, image, metadata) {
  const bytes = PNG.sync.write(image, { colorType: 6 }), filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes); fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = { file: `${OUT}/${filename}`, publicReviewFile: `${PUBLIC}/${filename}`, dimensions: [image.width, image.height], sha256: sha256(bytes), ...metadata }
}

// One immutable fitted base. The only correction is the explicitly reported OFF tap joint,
// repaired by transplanting the corresponding aligned native pixels from the approved ON row.
const fittedBase = crop(master.png, [65, 0, 1368, 284])
blit(crop(master.png, [590, 288, 80, 62]), fittedBase, 590 - 65, 288 - 282, true)
write('fitted-units-static', fittedBase, { source: MASTER_FILE, sourceCrop: [65, 0, 1368, 284], tapRepairSourceCrop: [590, 288, 80, 62], tapRepairOffset: [525, 6], immutableAfterV4: true, method: 'native 1:1 approved OFF run; only the reported tap joint replaced with aligned approved ON-row body pixels' })

const overlayOn = blank(1368, 284)
for (const region of [[590, 350, 100, 60], [765, 390, 210, 145], [980, 390, 220, 160]]) blit(crop(master.png, region), overlayOn, region[0] - 65, region[1] - 281, true)
write('fitted-overlay-on', overlayOn, { source: MASTER_FILE, sourceRowOffset: 281, regions: [[590, 350, 100, 60], [765, 390, 210, 145], [980, 390, 220, 160]], role: 'declared sink flow, dishwasher green lenses and oven On aperture/indicator only' })

const overlayBroken = blank(1368, 284)
for (const region of [[765, 670, 210, 155], [980, 670, 220, 160], [1210, 650, 223, 193]]) blit(crop(master.png, region), overlayBroken, region[0] - 65, region[1] - 560, true)
const lampRegions = [[784, 677, 19, 21], [806, 677, 19, 21], [828, 677, 19, 21]]
for (const region of lampRegions) blit(crop(fittedBase, [region[0] - 65, region[1] - 560, region[2], region[3]]), overlayBroken, region[0] - 65, region[1] - 560, true)
const cavityRegion = [1007, 731, 171, 81]
blit(crop(fittedBase, [cavityRegion[0] - 65, cavityRegion[1] - 560, cavityRegion[2], cavityRegion[3]]), overlayBroken, cavityRegion[0] - 65, cavityRegion[1] - 560, true)
write('fitted-overlay-broken', overlayBroken, { source: MASTER_FILE, sourceRowOffset: 560, role: 'declared dishwasher door, oven controls/door and fridge damage; animated lamps/cavity and water excluded' })
for (const [index, region] of lampRegions.entries()) {
  const layer = blank(1368, 284)
  blit(crop(master.png, region), layer, region[0] - 65, region[1] - 560, true)
  write(`dishwasher-warning-${index + 1}`, layer, { source: MASTER_FILE, sourceCrop: region, animation: 'independent intermittent opacity at 4 fps' })
}
const ovenLight = blank(1368, 284)
blit(crop(master.png, cavityRegion), ovenLight, cavityRegion[0] - 65, cavityRegion[1] - 560, true)
write('oven-broken-cavity-light', ovenLight, { source: MASTER_FILE, sourceCrop: cavityRegion, animation: 'intermittent opacity at 4 fps; body and door remain fixed' })
const floorWater = pad(clearPaper(crop(master.png, [65, 835, 1368, 35])))
write('broken-floor-water', floorWater, { source: MASTER_FILE, sourceCrop: [65, 835, 1368, 35], anchor: { x: -4, yFromFloor: -12 }, role: 'separate transparent floor-plane effect; never participates in fitted-run registration' })

const v3file = id => v3.outputs[id].file
const toasterOff = largestClean(v3file('toaster-off'), 82)
write('toaster-off', toasterOff, { source: v3file('toaster-off'), contactRow: contactRow(toasterOff), anchorX: Math.round(toasterOff.width / 2), shadowsRemoved: true })
const toast = pad(trim(keepComponents(clearPaper(crop(master.png, [164, 888, 82, 48])), component => component.pixels.length >= 20)))
const toasterOn = blank(Math.max(toasterOff.width, toast.width), toasterOff.height + 38)
blit(toast, toasterOn, Math.round((toasterOn.width - toast.width) / 2), 10)
blit(toasterOff, toasterOn, Math.round((toasterOn.width - toasterOff.width) / 2), 38)
write('toaster-on', toasterOn, { source: MASTER_FILE, base: 'toaster-off', baseOffset: [Math.round((toasterOn.width - toasterOff.width) / 2), 38], toastOffsetY: 10, contactRow: contactRow(toasterOn), anchorX: Math.round(toasterOn.width / 2), shadowsRemoved: true, method: 'byte-identical OFF body with toast seated into its slots' })
const toasterBroken = largestClean(v3file('toaster-broken'), 126)
write('toaster-broken', toasterBroken, { source: v3file('toaster-broken'), contactRow: contactRow(toasterBroken), anchorX: Math.round(toasterBroken.width / 2), shadowsRemoved: true })

const kettleOff = largestClean(v3file('kettle-off'), 114)
write('kettle-off', kettleOff, { source: v3file('kettle-off'), contactRow: contactRow(kettleOff), anchorX: Math.round(kettleOff.width / 2), shadowsRemoved: true, onAlias: true })
write('kettle-on', kettleOff, { source: v3file('kettle-off'), contactRow: contactRow(kettleOff), anchorX: Math.round(kettleOff.width / 2), shadowsRemoved: true, byteIdenticalTo: 'kettle-off', steamLayer: 'separate-not-drawn-in-this-review' })
const kettleBroken = largestClean(v3file('kettle-broken'), 114)
write('kettle-broken', kettleBroken, { source: v3file('kettle-broken'), contactRow: contactRow(kettleBroken), anchorX: Math.round(kettleBroken.width / 2), shadowsRemoved: true, state: 'broken-only' })

const bowlStandard = largestClean(v3file('bowl-standard'), 118)
write('bowl-standard', bowlStandard, { source: v3file('bowl-standard'), contactRow: contactRow(bowlStandard), anchorX: Math.round(bowlStandard.width / 2), shadowsRemoved: true, neighbourComponentsRemoved: true })
let bowlBrokenSource = crop(bowlPlate.png, [1075, 870, 175, 150])
bowlBrokenSource = clearPaper(bowlBrokenSource, generatedPaperLike, true)
bowlBrokenSource = keepComponents(bowlBrokenSource, (_component, index) => index === 0)
const bowlBroken = pad(trim(bowlBrokenSource))
write('bowl-broken', bowlBroken, { source: BOWL_PLATE_FILE, sourceCrop: [1075, 870, 175, 150], contactRow: contactRow(bowlBroken), anchorX: Math.round(bowlBroken.width * .55), shadowsRemoved: true, expandedTopLeftSafety: true, neighbourComponentsRemoved: true })

const binStandardWithoutShadow = removeWarmShadow(clearAfter(keepComponents(PNG.sync.read(fs.readFileSync(v3file('bin-standard'))), (_component, index) => index === 0), 123))
const binStandardSource = trim(keepComponents(binStandardWithoutShadow, component => component.pixels.length >= 20))
const binStandardLarge = pad(seamExtend(binStandardSource, Math.round(binStandardSource.width * 1.5), Math.round(binStandardSource.height * 1.5), Math.floor(binStandardSource.width * .52), Math.round(binStandardSource.width * .5), Math.floor(binStandardSource.height * .52), Math.round(binStandardSource.height * .5)))
write('bin-standard', binStandardLarge, { source: v3file('bin-standard'), sizeFactor: 1.5, nativePixelStraightRunExtension: true, contactRow: contactRow(binStandardLarge), anchorX: Math.round(binStandardLarge.width / 2), shadowsRemoved: true })
const rawBrokenBin = trim(removeWarmShadow(keepComponents(PNG.sync.read(fs.readFileSync(v3file('bin-broken'))), (_component, index) => index === 0)))
const brokenInsertX = Math.round(binStandardSource.width * .5), brokenInsertY = Math.round(binStandardSource.height * .5)
const binBrokenLarge = blank(rawBrokenBin.width + brokenInsertX, rawBrokenBin.height + brokenInsertY)
for (let y = 0; y < binBrokenLarge.height; y += 1) for (let x = 0; x < binBrokenLarge.width; x += 1) {
  const top = y < 48
  const sx = top ? x - Math.floor(brokenInsertX / 2) : x < Math.floor(rawBrokenBin.width * .56) ? x : x < Math.floor(rawBrokenBin.width * .56) + brokenInsertX ? Math.floor(rawBrokenBin.width * .56) : x - brokenInsertX
  const sy = y < 78 ? y : y < 78 + brokenInsertY ? 78 : y - brokenInsertY
  if (sx >= 0 && sx < rawBrokenBin.width && sy >= 0 && sy < rawBrokenBin.height) rawBrokenBin.data.copy(binBrokenLarge.data, (y * binBrokenLarge.width + x) * 4, (sy * rawBrokenBin.width + sx) * 4, (sy * rawBrokenBin.width + sx) * 4 + 4)
}
const binBroken = pad(binBrokenLarge)
write('bin-broken', binBroken, { source: v3file('bin-broken'), coreSizeFactor: 1.5, nativePixelStraightRunExtension: true, contactRow: contactRow(binBroken), anchorX: Math.round(binBroken.width * .57), shadowsRemoved: true, topRefuseUnscaled: true })

const tableV2File = 'art/drafts/kitchen-room-layout-review-2026-10-24-v2/native-cutouts/table-standard-native.png'
const tableWithoutShadow = removeWarmShadow(clearAfter(keepComponents(PNG.sync.read(fs.readFileSync(tableV2File)), (_component, index) => index === 0), 115))
const tableSource = trim(keepComponents(tableWithoutShadow, (_component, index) => index === 0))
const table = pad(seamExtend(tableSource, tableSource.width, tableSource.height + 11, 0, 0, Math.floor(tableSource.height * .58), 11))
clearRect(table, [34, 31, table.width - 68, table.height - 43])
write('table-standard', table, { source: tableV2File, keeperDensity: 8, surfaceHeightLogicalPixels: 14.5, targetSurfaceHeightPixels: 116, contactRow: contactRow(table), anchorX: Math.round(table.width / 2), method: 'native-pixel leg extension only; no horizontal scaling' })

let chairSource = clearPaper(crop(chairPlate.png, [1429, 881, 76, 121]), generatedPaperLike, true)
chairSource = trim(keepComponents(chairSource, (_component, index) => index === 0))
const chairUpper = seamExtend(chairSource, chairSource.width, chairSource.height + 20, 0, 0, 44, 20)
const chairPhysical = seamExtend(chairUpper, chairUpper.width, chairUpper.height + 16, 0, 0, 104, 16)
const chair = pad(chairPhysical)
write('chair-standard', chair, { source: CHAIR_PLATE_FILE, sourceCrop: [1429, 881, 76, 121], facing: 'rear', keeperDensity: 8, seatTopLogicalPixels: 7.75, targetSeatHeightPixels: 62, contactRow: contactRow(chair), anchorX: Math.round(chair.width / 2), method: 'native-pixel vertical post/leg extension only; original width retained; no scaling or resampling' })

fs.writeFileSync(path.join(PUBLIC, 'prime-keeper-neutral-native-256x320.png'), keeper.bytes)
fs.writeFileSync(path.join(PUBLIC, 'prime-keeper-seated-back-native-256x320.png'), seatedKeeper.bytes)
const register = {
  schema: 'lighthouse-keeper/kitchen-native-assets@3', status: 'review-only-unapproved-v4-loose-correction', createdOn: '2026-10-24',
  authority: { source: MASTER_FILE, sha256: MASTER_HASH, dimensions: [1536, 1024] },
  fittedUnits: { approvedByUser: true, immutableOutput: 'fitted-units-static', permittedFutureChanges: ['warning-light overlays', 'oven-interior-light overlay', 'replaceable broken-SFX declarations'], bodyMovementBetweenStates: false },
  scaleApplied: false, downscalingApplied: false, resamplingApplied: false, colourTransformApplied: false,
  keeperPresentation: { neutral: { file: KEEPER_FILE, sha256: sha256(keeper.bytes) }, seated: { file: SEATED_KEEPER_FILE, sha256: sha256(seatedKeeper.bytes) }, dimensions: [256, 320], cssResize: false, sourcePixelsPerPace: 114 },
  globalStateMap: { off: { toaster: 'off', kettle: 'off', bin: 'standard', bowl: 'standard' }, on: { toaster: 'on', kettle: 'on', bin: 'standard', bowl: 'standard' }, broken: { toaster: 'broken', kettle: 'broken', bin: 'broken', bowl: 'broken' } },
  sfxPlaceholders: { dishwasher: 'intermittent-metal-rattle', oven: 'intermittent-metal-rattle', fridge: 'intermittent-metal-rattle', toaster: 'intermittent-metal-rattle', kettle: 'intermittent-metal-rattle', bin: 'intermittent-metal-rattle' },
  inheritedSources: { v3Register: { file: V3_REGISTER_FILE, sha256: V3_REGISTER_HASH }, brokenBowl: { file: BOWL_PLATE_FILE, sha256: BOWL_PLATE_HASH }, rearChair: { file: CHAIR_PLATE_FILE, sha256: CHAIR_PLATE_HASH } },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log(`Built ${Object.keys(outputs).length} Kitchen V4 native assets and locked the corrected fitted-unit base.`)
