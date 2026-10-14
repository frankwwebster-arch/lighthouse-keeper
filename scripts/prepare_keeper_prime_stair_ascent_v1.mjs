#!/usr/bin/env node
/** Prepare isolated, registered Keeper Prime stair-ascent poses from the generated source sheet. */
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-14-v1')
const rawPath = path.join(pack, 'sources/keeper-prime-stair-ascent-8pose-magenta.png')
const cleanPath = path.join(pack, 'sources/keeper-prime-stair-ascent-8pose-isolated.png')
const rawCells = path.join(pack, 'sources/isolated-cells')
const frameDir = path.join(pack, 'drafts/frames-right')
const mirrorDir = path.join(pack, 'drafts/frames-left')
const sourceCell = [384, 512]
const targetCell = [256, 320]
const alphaThreshold = 8

const readPng = (file) => PNG.sync.read(fs.readFileSync(file))
const writePng = (file, png) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, PNG.sync.write(png, { colorType: 6 }))
}
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

function isolateBackground(source) {
  const count = source.width * source.height
  const output = new PNG({ width: source.width, height: source.height })
  source.data.copy(output.data)
  let removed = 0
  for (let index = 0; index < count; index++) {
    const offset = index * 4
    const r = output.data[offset]
    const g = output.data[offset + 1]
    const b = output.data[offset + 2]
    const magenta = r > 150 && b > 150 && g < 100 && Math.abs(r - b) < 100
    if (magenta) {
      output.data[offset + 3] = 0
      removed++
    }
  }
  for (let pass = 0; pass < 4; pass++) {
    const cut = []
    for (let y = 1; y < source.height - 1; y++) for (let x = 1; x < source.width - 1; x++) {
      const index = y * source.width + x
      const offset = index * 4
      if (!output.data[offset + 3]) continue
      const r = output.data[offset]
      const g = output.data[offset + 1]
      const b = output.data[offset + 2]
      const fringe = r > 70 && b > 70 && g < 100 && r + b > 2 * g + 65 && Math.abs(r - b) < 120
      if (!fringe) continue
      const neighbours = [index - 1, index + 1, index - source.width, index + source.width]
      if (neighbours.some((next) => output.data[next * 4 + 3] === 0)) cut.push(offset)
    }
    for (const offset of cut) {
      output.data[offset + 3] = 0
      removed++
    }
  }
  for (let index = 0; index < count; index++) {
    const offset = index * 4
    if (output.data[offset + 3] !== 0) continue
    output.data[offset] = 0
    output.data[offset + 1] = 0
    output.data[offset + 2] = 0
  }
  return { output, removed }
}

function crop(source, x0, y0, width, height) {
  const output = new PNG({ width, height })
  for (let y = 0; y < height; y++) {
    const start = ((y0 + y) * source.width + x0) * 4
    source.data.copy(output.data, y * width * 4, start, start + width * 4)
  }
  return output
}

function bounds(source) {
  let left = source.width
  let top = source.height
  let right = -1
  let bottom = -1
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    if (source.data[(y * source.width + x) * 4 + 3] < alphaThreshold) continue
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
  for (let x = 0; x < source.width; x++) {
    if (source.data[x * 4 + 3]) count++
    if (source.data[((source.height - 1) * source.width + x) * 4 + 3]) count++
  }
  for (let y = 1; y < source.height - 1; y++) {
    if (source.data[(y * source.width) * 4 + 3]) count++
    if (source.data[(y * source.width + source.width - 1) * 4 + 3]) count++
  }
  return count
}

function composite(target, source, left, top) {
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const tx = left + x
    const ty = top + y
    if (tx < 0 || ty < 0 || tx >= target.width || ty >= target.height) continue
    const si = (y * source.width + x) * 4
    const ti = (ty * target.width + tx) * 4
    const sa = source.data[si + 3] / 255
    if (!sa) continue
    const da = target.data[ti + 3] / 255
    const outA = sa + da * (1 - sa)
    for (let channel = 0; channel < 3; channel++) target.data[ti + channel] = Math.round((source.data[si + channel] * sa + target.data[ti + channel] * da * (1 - sa)) / outA)
    target.data[ti + 3] = Math.round(outA * 255)
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

if (!fs.existsSync(rawPath)) throw new Error(`missing ${path.relative(root, rawPath)}`)
const isolated = isolateBackground(readPng(rawPath))
writePng(cleanPath, isolated.output)
const cells = []
for (let frame = 0; frame < 8; frame++) {
  const cell = crop(isolated.output, (frame % 4) * sourceCell[0], Math.floor(frame / 4) * sourceCell[1], ...sourceCell)
  if (edgeAlpha(cell)) throw new Error(`source frame ${frame + 1} touches cell edge after isolation`)
  const box = bounds(cell)
  const subject = crop(cell, box[0], box[1], box[2] - box[0], box[3] - box[1])
  const file = path.join(rawCells, `frame-${frame + 1}.png`)
  writePng(file, subject)
  cells.push({ file, box, width: subject.width, height: subject.height })
}
const maxHeight = Math.max(...cells.map((cell) => cell.height))
const scale = 296 / maxHeight
const records = []
for (let frame = 0; frame < 8; frame++) {
  const cell = cells[frame]
  const width = Math.round(cell.width * scale)
  const height = Math.round(cell.height * scale)
  const resizedPath = path.join(rawCells, `frame-${frame + 1}-resized.png`)
  const ffmpeg = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', cell.file, '-vf', `scale=${width}:${height}:flags=lanczos`, resizedPath])
  if (ffmpeg.status !== 0) throw new Error(`ffmpeg resize failed for frame ${frame + 1}: ${ffmpeg.stderr}`)
  const resized = readPng(resizedPath)
  const registered = new PNG({ width: targetCell[0], height: targetCell[1] })
  const left = Math.round((targetCell[0] - resized.width) / 2)
  const top = 18
  composite(registered, resized, left, top)
  const rightPath = path.join(frameDir, `keeper_prime_stair-ascent-right_f${frame + 1}.png`)
  const leftPath = path.join(mirrorDir, `keeper_prime_stair-ascent-left_f${frame + 1}.png`)
  writePng(rightPath, registered)
  writePng(leftPath, mirror(registered))
  if (edgeAlpha(registered)) throw new Error(`registered frame ${frame + 1} touches its safety gutter`)
  records.push({
    frame: frame + 1,
    sourceBounds: cell.box,
    registeredBounds: bounds(registered),
    rightFile: path.relative(root, rightPath),
    rightSha256: sha(rightPath),
    leftFile: path.relative(root, leftPath),
    leftSha256: sha(leftPath),
    edgeAlphaPixels: 0,
  })
}
const report = {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@1',
  backgroundRemoval: { method: 'pure-magenta chroma removal', rule: 'r>150,b>150,g<100,abs(r-b)<100', removedPixels: isolated.removed, sourcePixels: isolated.output.width * isolated.output.height },
  sourceCell,
  targetCell,
  sharedScale: scale,
  headTopY: 18,
  frames: records,
}
fs.writeFileSync(path.join(pack, 'source-preparation-v1.json'), `${JSON.stringify(report, null, 2)}\n`)
console.log(JSON.stringify({ clean: path.relative(root, cleanPath), frames: records.length, removedPixels: isolated.removed, sharedScale: scale }, null, 2))
