#!/usr/bin/env node
/** Split and register the two Prime-referenced V10 four-pose stair sheets. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v10')
const sourceDir = path.join(pack, 'sources/generated')
const frameDir = path.join(pack, 'drafts/frames')
const inputs = [
  { leg: 'right', file: path.join(sourceDir, 'right-leg-four-pose-style-matched.png') },
  { leg: 'left', file: path.join(sourceDir, 'left-leg-four-pose-prime-referenced.png') },
]
const target = { width: 256, height: 320, alphaTop: 31, alphaBottom: 316, alphaHeight: 286, density: 8, safetyGutter: 3 }
const alphaThreshold = 8
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const input of inputs) if (!fs.existsSync(input.file)) throw new Error(`missing ${rel(input.file)}`)
fs.mkdirSync(frameDir, { recursive: true })

function bounds(png, x0 = 0, y0 = 0, x1 = png.width, y1 = png.height) {
  let minX = x1, minY = y1, maxX = -1, maxY = -1, opaque = 0
  for (let y = y0; y < y1; y += 1) for (let x = x0; x < x1; x += 1) {
    if (png.data[(y * png.width + x) * 4 + 3] <= alphaThreshold) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); opaque += 1
  }
  if (maxX < minX) throw new Error('empty alpha region')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaque }
}

function sample(source, x, y, channel) {
  const x0 = Math.max(0, Math.min(source.width - 1, Math.floor(x))), x1 = Math.min(source.width - 1, x0 + 1)
  const y0 = Math.max(0, Math.min(source.height - 1, Math.floor(y))), y1 = Math.min(source.height - 1, y0 + 1)
  const fx = x - x0, fy = y - y0
  const at = (sx, sy) => source.data[(sy * source.width + sx) * 4 + channel]
  return Math.round(((at(x0, y0) * (1 - fx) + at(x1, y0) * fx) * (1 - fy)) + ((at(x0, y1) * (1 - fx) + at(x1, y1) * fx) * fy))
}

function register(source, crop) {
  const scale = target.alphaHeight / crop.height
  const scaledWidth = Math.round(crop.width * scale)
  const upper = bounds(source, crop.minX, crop.minY, crop.maxX + 1, Math.ceil(crop.minY + crop.height * 0.67))
  const upperCentre = ((upper.minX + upper.maxX) / 2 - crop.minX) * scale
  const left = Math.round(target.width / 2 - upperCentre)
  const output = new PNG({ width: target.width, height: target.height, colorType: 6 })
  for (let dy = 0; dy < target.alphaHeight; dy += 1) for (let dx = 0; dx < scaledWidth; dx += 1) {
    const outX = left + dx, outY = target.alphaTop + dy
    if (outX < 0 || outX >= output.width) continue
    const sx = crop.minX + (dx + 0.5) / scale - 0.5
    const sy = crop.minY + (dy + 0.5) / scale - 0.5
    const offset = (outY * output.width + outX) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[offset + channel] = sample(source, sx, sy, channel)
  }
  return { output, scale, left, scaledWidth }
}

function edgeAlpha(png) {
  let count = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  return count
}

const frames = []
for (const input of inputs) {
  const sheet = PNG.sync.read(fs.readFileSync(input.file))
  for (let pose = 1; pose <= 4; pose += 1) {
    const x0 = Math.floor((pose - 1) * sheet.width / 4), x1 = Math.floor(pose * sheet.width / 4)
    const crop = bounds(sheet, x0, 0, x1, sheet.height)
    const prepared = register(sheet, crop)
    const outputBounds = bounds(prepared.output)
    if (outputBounds.minY !== target.alphaTop || outputBounds.maxY !== target.alphaBottom) throw new Error(`${input.leg} F${pose} vertical registration failed`)
    if (outputBounds.minX < target.safetyGutter || target.width - 1 - outputBounds.maxX < target.safetyGutter || edgeAlpha(prepared.output)) throw new Error(`${input.leg} F${pose} gutter failed`)
    const file = path.join(frameDir, `keeper_prime_stair_${input.leg}-leg_side-left_f${String(pose).padStart(2, '0')}.png`)
    fs.writeFileSync(file, PNG.sync.write(prepared.output))
    frames.push({ leg: input.leg, pose, file: rel(file), sha256: sha(file), sourceCell: { x0, x1, bounds: crop }, scale: prepared.scale, alphaBounds: outputBounds, edgeAlpha: 0 })
  }
}

writeJson(path.join(pack, 'source-preparation-v10.json'), {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@10',
  status: 'unapproved-intermediate-motion-source-registration',
  target,
  sources: inputs.map((input) => ({ leg: input.leg, file: rel(input.file), sha256: sha(input.file) })),
  contract: 'Four isolated right-leg phases followed by four isolated left-leg phases; common cap and sole datums; transparent cell-edge gutter.',
  frames,
})
console.log(JSON.stringify({ frames: frames.length, files: frames.map((frame) => frame.file) }, null, 2))
