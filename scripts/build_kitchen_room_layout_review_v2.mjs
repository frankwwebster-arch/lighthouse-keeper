#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const SOURCE = 'art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-24-v2/native-cutouts'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v2/assets'
const EXPECTED_SOURCE_HASH = 'a8a6972dd8398ec3cd52f42825a5a5f056a1e289d10b77796f3294b3ac85ab98'
const KEEPER_SOURCE = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f1.png'
const EXPECTED_KEEPER_HASH = 'a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3'

const CROPS = {
  'toaster-off': [38, 915, 111, 90],
  'toaster-on': [146, 873, 120, 136],
  'toaster-broken': [258, 874, 124, 136],
  'kettle-off': [392, 886, 116, 120],
  'kettle-on': [498, 886, 122, 120],
  'kettle-broken': [620, 872, 120, 137],
  'bin-standard': [764, 876, 91, 133],
  'bin-broken': [843, 866, 135, 145],
  'bowl-standard': [985, 880, 115, 130],
  'bowl-broken': [1085, 879, 145, 134],
  'table-standard': [1230, 887, 194, 118],
  'chair-standard': [1431, 850, 100, 157],
}

const sha256 = buffer => crypto.createHash('sha256').update(buffer).digest('hex')
const sourceBytes = fs.readFileSync(path.join(ROOT, SOURCE))
if (sha256(sourceBytes) !== EXPECTED_SOURCE_HASH) throw new Error('Approved Kitchen V4 master hash changed')
const source = PNG.sync.read(sourceBytes)
if (source.width !== 1536 || source.height !== 1024) throw new Error('Approved master must remain 1536 x 1024')
const keeperBytes = fs.readFileSync(path.join(ROOT, KEEPER_SOURCE))
if (sha256(keeperBytes) !== EXPECTED_KEEPER_HASH) throw new Error('Approved Prime Keeper standing reference hash changed')
const keeper = PNG.sync.read(keeperBytes)
if (keeper.width !== 256 || keeper.height !== 320) throw new Error('Prime Keeper density-8 reference must remain 256 x 320')

const backgroundLike = (r, g, b, a) =>
  a > 0 && r >= 238 && g >= 234 && b >= 216 && r - g <= 18 && g - b >= 0 && g - b <= 32

function exactNativeCutout([x, y, width, height]) {
  const output = new PNG({ width, height })
  for (let cy = 0; cy < height; cy += 1) {
    for (let cx = 0; cx < width; cx += 1) {
      const from = ((y + cy) * source.width + x + cx) * 4
      const to = (cy * width + cx) * 4
      source.data.copy(output.data, to, from, from + 4)
    }
  }

  const outside = new Uint8Array(width * height)
  const queue = []
  const enqueue = (cx, cy) => {
    const pixel = cy * width + cx
    if (outside[pixel]) return
    const i = pixel * 4
    if (!backgroundLike(output.data[i], output.data[i + 1], output.data[i + 2], output.data[i + 3])) return
    outside[pixel] = 1
    queue.push(pixel)
  }
  for (let cx = 0; cx < width; cx += 1) {
    enqueue(cx, 0)
    enqueue(cx, height - 1)
  }
  for (let cy = 1; cy < height - 1; cy += 1) {
    enqueue(0, cy)
    enqueue(width - 1, cy)
  }
  for (let head = 0; head < queue.length; head += 1) {
    const pixel = queue[head]
    const cx = pixel % width
    const cy = Math.floor(pixel / width)
    if (cx > 0) enqueue(cx - 1, cy)
    if (cx + 1 < width) enqueue(cx + 1, cy)
    if (cy > 0) enqueue(cx, cy - 1)
    if (cy + 1 < height) enqueue(cx, cy + 1)
  }
  for (let pixel = 0; pixel < outside.length; pixel += 1) {
    if (outside[pixel]) output.data[pixel * 4 + 3] = 0
  }

  const padded = new PNG({ width: width + 8, height: height + 8 })
  for (let cy = 0; cy < height; cy += 1) {
    const from = cy * width * 4
    const to = ((cy + 4) * padded.width + 4) * 4
    output.data.copy(padded.data, to, from, from + width * 4)
  }
  return padded
}

fs.mkdirSync(path.join(ROOT, OUT), { recursive: true })
fs.mkdirSync(path.join(ROOT, PUBLIC), { recursive: true })
fs.writeFileSync(path.join(ROOT, PUBLIC, 'kitchen-v4-master.png'), sourceBytes)
fs.writeFileSync(path.join(ROOT, PUBLIC, 'prime-keeper-neutral-native-256x320.png'), keeperBytes)
const outputs = {}
for (const [id, crop] of Object.entries(CROPS)) {
  const png = exactNativeCutout(crop)
  const bytes = PNG.sync.write(png, { colorType: 6 })
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(ROOT, OUT, filename), bytes)
  fs.writeFileSync(path.join(ROOT, PUBLIC, filename), bytes)
  outputs[id] = {
    crop,
    sourceCropDimensions: crop.slice(2),
    dimensions: [png.width, png.height],
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    sha256: sha256(bytes),
    method: 'native 1:1 crop; only border-connected warm-paper pixels made transparent; four transparent safety pixels added outside each crop; opaque RGB bytes unchanged',
  }
}

const register = {
  schema: 'lighthouse-keeper/kitchen-native-cutouts@1',
  status: 'review-only-unapproved-derived-assets',
  createdOn: '2026-10-24',
  source: SOURCE,
  sourceSha256: EXPECTED_SOURCE_HASH,
  sourceDimensions: [source.width, source.height],
  keeperScaleReference: {
    source: KEEPER_SOURCE,
    sourceSha256: EXPECTED_KEEPER_HASH,
    sourceDimensions: [keeper.width, keeper.height],
    logicalCell: [32, 40],
    density: 8,
    role: 'unchanged approved standing frame used only to prove room scale and clearances',
  },
  scaleApplied: false,
  resamplingApplied: false,
  colourTransformApplied: false,
  outputs,
}
fs.writeFileSync(path.join(ROOT, OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log(`Built ${Object.keys(outputs).length} native-pixel Kitchen V4 cutouts without scaling or resampling.`)
