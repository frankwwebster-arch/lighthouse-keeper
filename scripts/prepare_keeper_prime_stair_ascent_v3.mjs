#!/usr/bin/env node
/** Prepare Stair Ascent V3 from eight individually rendered contact-authority poses. */
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v3')
const sourceDir = path.join(pack, 'sources/rendered-frames')
const cellDir = path.join(pack, 'sources/registered-cells')
const rightDir = path.join(pack, 'drafts/frames-right')
const leftDir = path.join(pack, 'drafts/frames-left')
const walkLeftDir = path.join(pack, 'drafts/approved-walk-left')
const walkRightDir = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames')
const target = { width: 256, height: 320, alphaHeight: 286, soleY: 316, headAnchorX: 128 }

const read = (file) => PNG.sync.read(fs.readFileSync(file))
const write = (file, png) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, PNG.sync.write(png, { colorType: 6 }))
}
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

function bounds(png, minimumAlpha = 18) {
  let left = png.width, top = png.height, right = -1, bottom = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (png.data[(y * png.width + x) * 4 + 3] < minimumAlpha) continue
    left = Math.min(left, x); top = Math.min(top, y); right = Math.max(right, x); bottom = Math.max(bottom, y)
  }
  if (right < 0) throw new Error('empty frame')
  return [left, top, right + 1, bottom + 1]
}

function crop(png, box) {
  const [left, top, right, bottom] = box
  const out = new PNG({ width: right - left, height: bottom - top })
  for (let y = 0; y < out.height; y++) {
    const from = ((top + y) * png.width + left) * 4
    png.data.copy(out.data, y * out.width * 4, from, from + out.width * 4)
  }
  return out
}

function composite(targetPng, source, left, top) {
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const tx = left + x, ty = top + y
    if (tx < 0 || ty < 0 || tx >= targetPng.width || ty >= targetPng.height) continue
    const si = (y * source.width + x) * 4, ti = (ty * targetPng.width + tx) * 4
    if (!source.data[si + 3]) continue
    for (let channel = 0; channel < 4; channel++) targetPng.data[ti + channel] = source.data[si + channel]
  }
}

function mirror(png) {
  const out = new PNG({ width: png.width, height: png.height })
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    const from = (y * png.width + x) * 4, to = (y * png.width + png.width - 1 - x) * 4
    for (let channel = 0; channel < 4; channel++) out.data[to + channel] = png.data[from + channel]
  }
  return out
}

function edgeAlpha(png) {
  let count = 0
  for (let x = 0; x < png.width; x++) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  for (let y = 1; y < png.height - 1; y++) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  return count
}

function contactCentreX(png, y) {
  const xs = []
  for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] >= 32) xs.push(x)
  if (!xs.length) throw new Error(`no opaque sole contact at y=${y}`)
  return (Math.min(...xs) + Math.max(...xs)) / 2
}

const roles = [
  ['far', 'near', 'near lift'],
  ['far', 'near', 'near high pass'],
  ['far', 'near', 'near reaches upper tread'],
  ['far+near', 'none', 'near upper contact / far lower contact'],
  ['near', 'far', 'far lift'],
  ['near', 'far', 'far high pass'],
  ['near', 'far', 'far reaches upper tread'],
  ['near+far', 'none', 'far upper contact / near lower contact'],
]

const frames = []
for (let frame = 1; frame <= 8; frame++) {
  const sourceFile = path.join(sourceDir, `stair-right-f${frame}.png`)
  if (!fs.existsSync(sourceFile)) throw new Error(`missing ${rel(sourceFile)}`)
  const source = read(sourceFile)
  const sourceBox = bounds(source)
  const subject = crop(source, sourceBox)
  const scale = target.alphaHeight / subject.height
  const resizedWidth = Math.round(subject.width * scale)
  const resizedHeight = target.alphaHeight
  if (resizedWidth > 238) throw new Error(`frame ${frame} is too wide for a transparent safety gutter (${resizedWidth}px)`)
  const rawFile = path.join(cellDir, `frame-${frame}-raw.png`)
  const resizedFile = path.join(cellDir, `frame-${frame}-resized.png`)
  write(rawFile, subject)
  const result = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', rawFile, '-vf', `scale=${resizedWidth}:${resizedHeight}:flags=lanczos`, resizedFile])
  if (result.status !== 0) throw new Error(`frame ${frame} resize failed: ${result.stderr}`)
  const resized = read(resizedFile)
  const registered = new PNG({ width: target.width, height: target.height })
  const left = Math.round(target.headAnchorX - resized.width / 2)
  const top = target.soleY - resized.height + 1
  composite(registered, resized, left, top)
  if (edgeAlpha(registered)) throw new Error(`frame ${frame} touches a cell edge`)
  const registeredBox = bounds(registered)
  if (registeredBox[3] - 1 !== target.soleY) throw new Error(`frame ${frame} misses sole datum`)
  const rightFile = path.join(rightDir, `keeper_prime_stair-ascent-right_f${frame}.png`)
  const leftFile = path.join(leftDir, `keeper_prime_stair-ascent-left_f${frame}.png`)
  write(rightFile, registered)
  const leftFacing = mirror(registered)
  write(leftFile, leftFacing)
  frames.push({
    frame,
    sourceFile: rel(sourceFile), sourceSha256: sha(sourceFile), sourceBounds: sourceBox,
    scale, registeredBounds: registeredBox, rightFile: rel(rightFile), rightSha256: sha(rightFile),
    leftFile: rel(leftFile), leftSha256: sha(leftFile), soleY: target.soleY,
    leftContactCentreX: contactCentreX(leftFacing, target.soleY),
    support: roles[frame - 1][0], swing: roles[frame - 1][1], phase: roles[frame - 1][2], edgeAlphaPixels: 0,
  })
}

const walkFrames = []
for (let frame = 1; frame <= 8; frame++) {
  const authority = path.join(walkRightDir, `keeper_prime_walk-right_f${frame}.png`)
  const leftFile = path.join(walkLeftDir, `keeper_prime_walk-left_f${frame}.png`)
  const right = read(authority)
  write(leftFile, mirror(right))
  if (edgeAlpha(right) || edgeAlpha(read(leftFile))) throw new Error(`walk frame ${frame} lacks a safety gutter`)
  walkFrames.push({ frame, rightAuthority: rel(authority), rightSha256: sha(authority), leftFile: rel(leftFile), leftSha256: sha(leftFile) })
}

const report = {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@3',
  method: 'individual transparent renders; per-frame physical-height normalisation; fixed sole datum; exact horizontal mirror',
  target,
  contactRule: 'The lowest declared contact sole ends at source-cell y=316; review placement maps it to the active tread top with a 0.5-lp cell offset.',
  frames,
  walkFrames,
}
fs.writeFileSync(path.join(pack, 'source-preparation-v3.json'), `${JSON.stringify(report, null, 2)}\n`)
console.log(JSON.stringify({ frames: frames.length, walkFrames: walkFrames.length, target }, null, 2))
