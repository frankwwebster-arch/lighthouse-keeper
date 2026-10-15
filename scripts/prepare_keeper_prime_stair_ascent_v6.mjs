#!/usr/bin/env node
/**
 * Split and register the two V6 six-pose contact sheets.
 *
 * The generated sheets are evidence sources only. This script produces twelve
 * isolated 256x320 authoring cells, all with the same 286 px alpha height,
 * y31 cap datum, y316 lowest-sole datum and upper-body horizontal anchor.
 */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6')
const sourceDir = path.join(pack, 'sources/generated')
const frameDir = path.join(pack, 'drafts/frames')
const prepPath = path.join(pack, 'source-preparation-v6.json')
const alphaThreshold = 8
const target = { width: 256, height: 320, alphaTop: 31, alphaBottom: 316, alphaHeight: 286, density: 8, safetyGutter: 3 }
const inputs = [
  { leg: 'left', file: path.join(sourceDir, 'left-leg-six-pose-corrected.png') },
  { leg: 'right', file: path.join(sourceDir, 'right-leg-six-pose-corrected.png') },
]
const singlePoseOverrides = new Map([
  ['left:4', path.join(sourceDir, 'left-leg-pose04-contact-corrected.png')],
])
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const input of inputs) if (!fs.existsSync(input.file)) throw new Error(`missing ${rel(input.file)}`)
for (const file of singlePoseOverrides.values()) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
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

function sampleBilinear(source, x, y, channel) {
  const x0 = Math.max(0, Math.min(source.width - 1, Math.floor(x)))
  const y0 = Math.max(0, Math.min(source.height - 1, Math.floor(y)))
  const x1 = Math.min(source.width - 1, x0 + 1)
  const y1 = Math.min(source.height - 1, y0 + 1)
  const fx = x - x0, fy = y - y0
  const at = (sx, sy) => source.data[(sy * source.width + sx) * 4 + channel]
  const top = at(x0, y0) * (1 - fx) + at(x1, y0) * fx
  const bottom = at(x0, y1) * (1 - fx) + at(x1, y1) * fx
  return Math.round(top * (1 - fy) + bottom * fy)
}

function registeredCell(sheet, crop) {
  const scale = target.alphaHeight / crop.height
  const scaledWidth = Math.round(crop.width * scale)
  const upperLimit = crop.minY + crop.height * 0.67
  const upper = bounds(sheet, crop.minX, crop.minY, crop.maxX + 1, Math.ceil(upperLimit))
  const upperCentre = ((upper.minX + upper.maxX) / 2 - crop.minX) * scale
  const left = Math.round(target.width / 2 - upperCentre)
  const output = new PNG({ width: target.width, height: target.height, colorType: 6 })
  for (let dy = 0; dy < target.alphaHeight; dy += 1) for (let dx = 0; dx < scaledWidth; dx += 1) {
    const outX = left + dx, outY = target.alphaTop + dy
    if (outX < 0 || outX >= output.width || outY < 0 || outY >= output.height) continue
    const sx = crop.minX + (dx + 0.5) / scale - 0.5
    const sy = crop.minY + (dy + 0.5) / scale - 0.5
    const index = (outY * output.width + outX) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[index + channel] = sampleBilinear(sheet, sx, sy, channel)
  }
  return { output, scale, left, scaledWidth, upperCentreSource: (upper.minX + upper.maxX) / 2 }
}

function mirror(source) {
  const output = new PNG({ width: source.width, height: source.height, colorType: 6 })
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    const from = (y * source.width + x) * 4
    const to = (y * source.width + (source.width - 1 - x)) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[to + channel] = source.data[from + channel]
  }
  return output
}

function edgeAlpha(png) {
  let count = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3] > 0) count += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3] > 0) count += 1
  return count
}

function lowerLegVerticalWarp(source, fromX, startY, fullShiftY, maxShift) {
  const output = PNG.sync.read(PNG.sync.write(source))
  for (let y = startY; y < source.height; y += 1) for (let x = fromX; x < source.width; x += 1) {
    const destination = (y * source.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[destination + channel] = 0
  }
  for (let y = startY; y < source.height; y += 1) for (let x = fromX; x < source.width; x += 1) {
    const shift = maxShift * Math.max(0, Math.min(1, (y - startY) / (fullShiftY - startY)))
    const sy = y - shift
    const destination = (y * source.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[destination + channel] = sampleBilinear(source, x, sy, channel)
  }
  return output
}

const frames = []
for (const input of inputs) {
  const sheet = PNG.sync.read(fs.readFileSync(input.file))
  for (let pose = 1; pose <= 6; pose += 1) {
    const index = pose - 1, col = index % 3, row = Math.floor(index / 3)
    const overrideFile = singlePoseOverrides.get(`${input.leg}:${pose}`)
    const source = overrideFile ? PNG.sync.read(fs.readFileSync(overrideFile)) : sheet
    const x0 = overrideFile ? 0 : Math.floor(col * sheet.width / 3), x1 = overrideFile ? source.width : Math.floor((col + 1) * sheet.width / 3)
    const y0 = overrideFile ? 0 : Math.floor(row * sheet.height / 2), y1 = overrideFile ? source.height : Math.floor((row + 1) * sheet.height / 2)
    const crop = bounds(source, x0, y0, x1, y1)
    const registered = registeredCell(source, crop)
    const rightFile = path.join(frameDir, `keeper_prime_stair_${input.leg}-leg_side-right_f${String(pose).padStart(2, '0')}.png`)
    const leftFile = path.join(frameDir, `keeper_prime_stair_${input.leg}-leg_side-left_f${String(pose).padStart(2, '0')}.png`)
    fs.writeFileSync(rightFile, PNG.sync.write(registered.output))
    fs.writeFileSync(leftFile, PNG.sync.write(mirror(registered.output)))
    const outputBounds = bounds(registered.output)
    if (outputBounds.minY !== target.alphaTop || outputBounds.maxY !== target.alphaBottom) throw new Error(`${input.leg} F${pose} vertical registration failed`)
    if (outputBounds.minX < target.safetyGutter || target.width - 1 - outputBounds.maxX < target.safetyGutter) throw new Error(`${input.leg} F${pose} horizontal gutter failed`)
    if (edgeAlpha(registered.output) !== 0) throw new Error(`${input.leg} F${pose} touches cell edge`)
    frames.push({
      leg: input.leg, pose, sourceCell: overrideFile ? { overrideFile: rel(overrideFile), overrideSha256: sha(overrideFile), bounds: crop } : { col, row, bounds: crop }, scale: registered.scale,
      upperBodyAnchorX: 128, alphaBounds: outputBounds, soleDatumY: target.alphaBottom,
      rightFile: rel(rightFile), rightSha256: sha(rightFile), leftFile: rel(leftFile), leftSha256: sha(leftFile), edgeAlpha: 0,
    })
  }
}

// Lock the approved-looking upper silhouette to one V6 authority so the two
// independently generated leg passes cannot make the Keeper's head or torso
// flicker. The feather sits inside the jumper hem/hip join; legs remain wholly
// pose-specific.
const upperAuthorityFile = path.join(frameDir, 'keeper_prime_stair_left-leg_side-right_f01.png')
const upperAuthority = PNG.sync.read(fs.readFileSync(upperAuthorityFile))
const exactThroughY = 212
const featherThroughY = 220
for (const frame of frames) {
  const rightFile = path.join(root, frame.rightFile)
  let pose = PNG.sync.read(fs.readFileSync(rightFile))
  for (let y = 0; y <= featherThroughY; y += 1) for (let x = 0; x < pose.width; x += 1) {
    const offset = (y * pose.width + x) * 4
    const authorityWeight = y <= exactThroughY ? 1 : (featherThroughY - y) / (featherThroughY - exactThroughY)
    if (authorityWeight <= 0) continue
    for (let channel = 0; channel < 4; channel += 1) {
      pose.data[offset + channel] = Math.round(upperAuthority.data[offset + channel] * authorityWeight + pose.data[offset + channel] * (1 - authorityWeight))
    }
  }
  if (frame.leg === 'left' && frame.pose === 4) {
    pose = lowerLegVerticalWarp(pose, 148, 220, 260, 12)
    for (let y = target.alphaBottom + 1; y < pose.height; y += 1) for (let x = 0; x < pose.width; x += 1) {
      const offset = (y * pose.width + x) * 4
      for (let channel = 0; channel < 4; channel += 1) pose.data[offset + channel] = 0
    }
  }
  const leftFile = path.join(root, frame.leftFile)
  fs.writeFileSync(rightFile, PNG.sync.write(pose))
  fs.writeFileSync(leftFile, PNG.sync.write(mirror(pose)))
  const outputBounds = bounds(pose)
  if (edgeAlpha(pose) !== 0 || outputBounds.minY !== target.alphaTop || outputBounds.maxY !== target.alphaBottom) throw new Error(`${frame.leg} F${frame.pose} composite registration failed: ${JSON.stringify({ outputBounds, edgeAlpha: edgeAlpha(pose) })}`)
  frame.alphaBounds = outputBounds
  frame.rightSha256 = sha(rightFile)
  frame.leftSha256 = sha(leftFile)
}

writeJson(prepPath, {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@6',
  mode: 'deterministic-contact-sheet-split-bilinear-registration-and-exact-mirror',
  target,
  sources: [...inputs.map((input) => ({ leg: input.leg, file: rel(input.file), sha256: sha(input.file) })), ...[...singlePoseOverrides.entries()].map(([pose, file]) => ({ pose, file: rel(file), sha256: sha(file), role: 'binding single-pose contact correction' }))],
  order: 'top-left to top-right, then bottom-left to bottom-right',
  upperBodyLock: { authority: rel(upperAuthorityFile), exactThroughY, featherThroughY },
  contactCorrection: { leftPose4: 'binding single-pose render plus deterministic 12 px lower-leg contact warp from y220 to y260; upper-body pixels unchanged' },
  invariant: 'Every registered pose has the same exact upper body through y212, feathered hip join through y220, y31 cap datum, y316 lowest-sole datum, 286 px alpha height, x128 upper-body anchor and transparent cell-edge gutter.',
  frames,
})
console.log(JSON.stringify({ output: rel(prepPath), frames: frames.length, target }, null, 2))
