#!/usr/bin/env node
/** Prepare Stair Ascent V2: alternating climb poses plus a correctly facing approved walk. */
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v2')
const sourcePath = path.join(pack, 'sources/keeper-prime-stair-ascent-v2-generated.png')
const isolatedPath = path.join(pack, 'sources/keeper-prime-stair-ascent-v2-isolated.png')
const rawCells = path.join(pack, 'sources/isolated-cells')
const rightDir = path.join(pack, 'drafts/frames-right')
const leftDir = path.join(pack, 'drafts/frames-left')
const walkLeftDir = path.join(pack, 'drafts/approved-walk-left')
const walkRightDir = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames')
const sourceCell = [384, 512]
const targetCell = [256, 320]

const readPng = (file) => PNG.sync.read(fs.readFileSync(file))
const writePng = (file, png) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, PNG.sync.write(png, { colorType: 6 }))
}
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

function crop(source, x0, y0, width, height) {
  const output = new PNG({ width, height })
  for (let y = 0; y < height; y++) {
    const start = ((y0 + y) * source.width + x0) * 4
    source.data.copy(output.data, y * width * 4, start, start + width * 4)
  }
  return output
}

function clearPixel(png, pixel) {
  const offset = pixel * 4
  png.data[offset] = 0
  png.data[offset + 1] = 0
  png.data[offset + 2] = 0
  png.data[offset + 3] = 0
}

/**
 * Image generation returned transparent outer gutters plus a smooth connected
 * backdrop around each pose. Remove only that edge-connected smooth field;
 * the Keeper's black contour is a hard colour boundary and remains intact.
 */
function isolateCell(cell) {
  const output = new PNG({ width: cell.width, height: cell.height })
  cell.data.copy(output.data)
  const visited = new Uint8Array(cell.width * cell.height)
  const queued = new Uint8Array(cell.width * cell.height)
  const queue = []
  const enqueue = (pixel) => {
    if (pixel < 0 || pixel >= queued.length || queued[pixel]) return
    queued[pixel] = 1
    queue.push(pixel)
  }
  for (let x = 0; x < cell.width; x++) {
    enqueue(x)
    enqueue((cell.height - 1) * cell.width + x)
  }
  for (let y = 1; y < cell.height - 1; y++) {
    enqueue(y * cell.width)
    enqueue(y * cell.width + cell.width - 1)
  }
  const colourDistance = (a, b) => {
    const ai = a * 4
    const bi = b * 4
    const dr = output.data[ai] - output.data[bi]
    const dg = output.data[ai + 1] - output.data[bi + 1]
    const db = output.data[ai + 2] - output.data[bi + 2]
    return Math.sqrt(dr * dr + dg * dg + db * db)
  }
  let head = 0
  while (head < queue.length) {
    const pixel = queue[head++]
    if (visited[pixel]) continue
    visited[pixel] = 1
    const x = pixel % cell.width
    const y = Math.floor(pixel / cell.width)
    const neighbours = []
    if (x > 0) neighbours.push(pixel - 1)
    if (x + 1 < cell.width) neighbours.push(pixel + 1)
    if (y > 0) neighbours.push(pixel - cell.width)
    if (y + 1 < cell.height) neighbours.push(pixel + cell.width)
    for (const next of neighbours) {
      if (visited[next]) continue
      const alpha = output.data[next * 4 + 3]
      const currentAlpha = output.data[pixel * 4 + 3]
      if (alpha === 0 || (currentAlpha === 0 ? alpha < 64 : colourDistance(pixel, next) <= 12)) enqueue(next)
    }
  }
  let removed = 0
  for (let pixel = 0; pixel < visited.length; pixel++) if (visited[pixel]) {
    if (output.data[pixel * 4 + 3]) removed++
    clearPixel(output, pixel)
  }
  // Remove only faint residual background; retain anti-aliased character edges.
  for (let pixel = 0; pixel < visited.length; pixel++) {
    const alpha = output.data[pixel * 4 + 3]
    if (alpha > 0 && alpha < 18) clearPixel(output, pixel)
  }
  return { output, removed }
}

function bounds(source) {
  let left = source.width
  let top = source.height
  let right = -1
  let bottom = -1
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    if (!source.data[(y * source.width + x) * 4 + 3]) continue
    left = Math.min(left, x)
    top = Math.min(top, y)
    right = Math.max(right, x)
    bottom = Math.max(bottom, y)
  }
  if (right < 0) throw new Error('empty isolated frame')
  return [left, top, right + 1, bottom + 1]
}

function edgeAlpha(source) {
  let count = 0
  for (let x = 0; x < source.width; x++) for (const y of [0, source.height - 1]) if (source.data[(y * source.width + x) * 4 + 3]) count++
  for (let y = 1; y < source.height - 1; y++) for (const x of [0, source.width - 1]) if (source.data[(y * source.width + x) * 4 + 3]) count++
  return count
}

function composite(target, source, left, top) {
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const tx = left + x
    const ty = top + y
    if (tx < 0 || ty < 0 || tx >= target.width || ty >= target.height) continue
    const si = (y * source.width + x) * 4
    const ti = (ty * target.width + tx) * 4
    const alpha = source.data[si + 3]
    if (!alpha) continue
    for (let channel = 0; channel < 4; channel++) target.data[ti + channel] = source.data[si + channel]
  }
}

function mirror(source) {
  const output = new PNG({ width: source.width, height: source.height })
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const from = (y * source.width + x) * 4
    const to = (y * source.width + source.width - 1 - x) * 4
    for (let channel = 0; channel < 4; channel++) output.data[to + channel] = source.data[from + channel]
  }
  return output
}

if (!fs.existsSync(sourcePath)) throw new Error(`missing ${path.relative(root, sourcePath)}`)
const source = readPng(sourcePath)
if (source.width !== 1536 || source.height !== 1024) throw new Error('unexpected generated source dimensions')
const cells = []
const isolatedSheet = new PNG({ width: source.width, height: source.height })
let removedPixels = 0
for (let frame = 0; frame < 8; frame++) {
  const x0 = (frame % 4) * sourceCell[0]
  const y0 = Math.floor(frame / 4) * sourceCell[1]
  const isolated = isolateCell(crop(source, x0, y0, ...sourceCell))
  removedPixels += isolated.removed
  composite(isolatedSheet, isolated.output, x0, y0)
  if (edgeAlpha(isolated.output)) throw new Error(`source frame ${frame + 1} touches cell edge after isolation`)
  const box = bounds(isolated.output)
  const subject = crop(isolated.output, box[0], box[1], box[2] - box[0], box[3] - box[1])
  const file = path.join(rawCells, `frame-${frame + 1}.png`)
  writePng(file, subject)
  cells.push({ file, box, width: subject.width, height: subject.height })
}
writePng(isolatedPath, isolatedSheet)

const maxHeight = Math.max(...cells.map((cell) => cell.height))
const scale = 296 / maxHeight
const frames = []
for (let frame = 0; frame < 8; frame++) {
  const cell = cells[frame]
  const width = Math.round(cell.width * scale)
  const height = Math.round(cell.height * scale)
  const resizedPath = path.join(rawCells, `frame-${frame + 1}-resized.png`)
  const resize = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', cell.file, '-vf', `scale=${width}:${height}:flags=lanczos`, resizedPath])
  if (resize.status !== 0) throw new Error(`ffmpeg resize failed for frame ${frame + 1}: ${resize.stderr}`)
  const registered = new PNG({ width: targetCell[0], height: targetCell[1] })
  composite(registered, readPng(resizedPath), Math.round((targetCell[0] - width) / 2), 18)
  const rightPath = path.join(rightDir, `keeper_prime_stair-ascent-right_f${frame + 1}.png`)
  const leftPath = path.join(leftDir, `keeper_prime_stair-ascent-left_f${frame + 1}.png`)
  writePng(rightPath, registered)
  writePng(leftPath, mirror(registered))
  if (edgeAlpha(registered)) throw new Error(`registered frame ${frame + 1} touches its safety gutter`)
  frames.push({ frame: frame + 1, sourceBounds: cell.box, registeredBounds: bounds(registered), rightFile: path.relative(root, rightPath), rightSha256: sha(rightPath), leftFile: path.relative(root, leftPath), leftSha256: sha(leftPath), edgeAlphaPixels: 0 })
}

const walkFrames = []
for (let frame = 1; frame <= 8; frame++) {
  const rightPath = path.join(walkRightDir, `keeper_prime_walk-right_f${frame}.png`)
  const leftPath = path.join(walkLeftDir, `keeper_prime_walk-left_f${frame}.png`)
  const right = readPng(rightPath)
  writePng(leftPath, mirror(right))
  if (edgeAlpha(right) || edgeAlpha(readPng(leftPath))) throw new Error(`approved walk frame ${frame} has unsafe edge alpha`)
  walkFrames.push({ frame, rightAuthority: path.relative(root, rightPath), rightSha256: sha(rightPath), leftFile: path.relative(root, leftPath), leftSha256: sha(leftPath) })
}

const report = {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@2',
  backgroundRemoval: { method: 'edge-connected local-colour flood', maximumNeighbourRgbDistance: 12, transparentSeedMaximumAlpha: 63, removedPixels, sourcePixels: source.width * source.height },
  sourceCell,
  targetCell,
  sharedScale: scale,
  headTopY: 18,
  directionCorrection: 'Approach frames are exact horizontal mirrors of approved Walk V6 right-facing pixels.',
  alternatingLegAuthority: 'Approved Walk V6 F1-F8 phase order used as the redraw guide.',
  frames,
  walkFrames,
}
fs.writeFileSync(path.join(pack, 'source-preparation-v2.json'), `${JSON.stringify(report, null, 2)}\n`)
console.log(JSON.stringify({ frames: frames.length, walkFrames: walkFrames.length, removedPixels, sharedScale: scale }, null, 2))
