#!/usr/bin/env node
/**
 * Prepare V11 from the established V6/V7 stair family.
 *
 * V10's generated motion studies are retained but rejected because they did
 * not hold the exact Prime silhouette. V11 takes three same-family lift/pass
 * drawings from V6 and the contact-locked endpoint from V7. A bounded smooth
 * arm warp adds the requested contralateral counter-motion without touching
 * the cap, face, beard, tread-contact legs or transparent cell edges.
 */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v6 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6')
const v7 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const v10 = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v10')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v11')
const frameDir = path.join(pack, 'drafts/frames')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sources = {
  right: [1, 2, 3].map((pose) => path.join(v6, `drafts/frames/keeper_prime_stair_right-leg_side-left_f${String(pose).padStart(2, '0')}.png`)).concat(path.join(v7, 'drafts/frames/keeper_prime_stair_right-contact_side-left_f01.png')),
  left: [1, 2, 3].map((pose) => path.join(v6, `drafts/frames/keeper_prime_stair_left-leg_side-left_f${String(pose).padStart(2, '0')}.png`)).concat(path.join(v7, 'drafts/frames/keeper_prime_stair_left-contact_side-left_f01.png')),
}
for (const file of [...sources.right, ...sources.left, path.join(v10, 'source-preparation-v10.json')]) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
fs.mkdirSync(frameDir, { recursive: true })

function sample(source, x, y, channel) {
  const x0 = Math.max(0, Math.min(source.width - 1, Math.floor(x))), x1 = Math.min(source.width - 1, x0 + 1)
  const y0 = Math.max(0, Math.min(source.height - 1, Math.floor(y))), y1 = Math.min(source.height - 1, y0 + 1)
  const fx = x - x0, fy = y - y0
  const at = (sx, sy) => source.data[(sy * source.width + sx) * 4 + channel]
  return Math.round(((at(x0, y0) * (1 - fx) + at(x1, y0) * fx) * (1 - fy)) + ((at(x0, y1) * (1 - fx) + at(x1, y1) * fx) * fy))
}

function armWarp(source, forwardPixels) {
  const output = PNG.sync.read(PNG.sync.write(source))
  for (let y = 128; y <= 246; y += 1) for (let x = 96; x <= 184; x += 1) {
    const dx = (x - 140) / 31
    const xWeight = Math.exp(-Math.pow(Math.abs(dx), 4))
    const yWeight = y < 154 ? (y - 128) / 26 : y <= 224 ? 1 : (246 - y) / 22
    const displacement = Math.max(0, yWeight) * xWeight * forwardPixels
    const sx = x + displacement
    const offset = (y * output.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[offset + channel] = sample(source, sx, y, channel)
  }
  return output
}

function edgeAlpha(png) {
  let count = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  return count
}

function alphaBounds(png) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 }
}

const amplitudes = { right: [0.75, 1.5, 2.25, 3], left: [1.75, 3.5, 5.25, 7] }
const frames = []
for (const leg of ['right', 'left']) for (let index = 0; index < 4; index += 1) {
  const sourceFile = sources[leg][index]
  const source = PNG.sync.read(fs.readFileSync(sourceFile))
  if (source.width !== 256 || source.height !== 320) throw new Error(`${leg} F${index + 1} source cell changed`)
  const output = armWarp(source, amplitudes[leg][index])
  if (edgeAlpha(output)) throw new Error(`${leg} F${index + 1} touches a cell edge`)
  const file = path.join(frameDir, `keeper_prime_stair_${leg}-leg_side-left_f${String(index + 1).padStart(2, '0')}.png`)
  fs.writeFileSync(file, PNG.sync.write(output))
  frames.push({
    leg, pose: index + 1, phase: ['lift', 'pass', 'reach', 'plant'][index], arm: leg === 'right' ? 'left' : 'right',
    armForwardPixels: amplitudes[leg][index], sourceFile: rel(sourceFile), sourceSha256: sha(sourceFile), file: rel(file), sha256: sha(file),
    alphaBounds: alphaBounds(output), cell: [256, 320], density: 8, edgeAlpha: 0,
  })
}

writeJson(path.join(pack, 'source-preparation-v11.json'), {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@11',
  status: 'same-family-lift-pass-plus-bounded-arm-warp',
  rejectedV10: { file: rel(path.join(v10, 'source-preparation-v10.json')), sha256: sha(path.join(v10, 'source-preparation-v10.json')), reason: 'generated half-cycles did not preserve one exact Prime silhouette and contact geometry' },
  method: 'V6 same-family lift/pass/reach drawings plus V7 contact-locked plant drawings; bounded bilinear arm-region warp only.',
  armContract: { rightLeg: 'left arm modestly forward', leftLeg: 'right arm clearly forward', amplitudesPx: amplitudes, headAndCapUnchangedThroughY: 127, legsUnchangedFromY: 247 },
  frames,
})
console.log(JSON.stringify({ preparation: rel(path.join(pack, 'source-preparation-v11.json')), frames: frames.length, amplitudes }, null, 2))
