#!/usr/bin/env node
/** Prepare the deliberately minimal two-contact Stair Ascent V7 cycle. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sourcePack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const outputDir = path.join(pack, 'drafts/frames')
const sources = {
  right: path.join(sourcePack, 'drafts/frames/keeper_prime_stair_right-leg_side-left_f04.png'),
  left: path.join(sourcePack, 'drafts/frames/keeper_prime_stair_left-leg_side-left_f04.png'),
}
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
for (const file of Object.values(sources)) if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
fs.mkdirSync(outputDir, { recursive: true })

function sample(source, x, y, channel) {
  const x0 = Math.max(0, Math.min(source.width - 1, Math.floor(x))), x1 = Math.min(source.width - 1, x0 + 1)
  const y0 = Math.max(0, Math.min(source.height - 1, Math.floor(y))), y1 = Math.min(source.height - 1, y0 + 1)
  const fx = x - x0, fy = y - y0
  const at = (sx, sy) => source.data[(sy * source.width + sx) * 4 + channel]
  return Math.round((at(x0, y0) * (1 - fx) + at(x1, y0) * fx) * (1 - fy) + (at(x0, y1) * (1 - fx) + at(x1, y1) * fx) * fy)
}

function contactLock(source, horizontalCorrection, verticalCorrection) {
  const output = PNG.sync.read(PNG.sync.write(source))
  const startY = 220, fullY = 260, sourceBoundaryX = 110
  for (let y = startY; y < output.height; y += 1) for (let x = 0; x < sourceBoundaryX + horizontalCorrection; x += 1) {
    const offset = (y * output.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[offset + channel] = 0
  }
  for (let y = startY; y <= 316; y += 1) for (let x = 0; x < sourceBoundaryX + horizontalCorrection; x += 1) {
    const factor = Math.max(0, Math.min(1, (y - startY) / (fullY - startY + verticalCorrection)))
    const sx = x - horizontalCorrection * factor
    const sy = y - verticalCorrection * factor
    if (sx < 0 || sx >= sourceBoundaryX || sy < startY || sy >= source.height) continue
    const offset = (y * output.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[offset + channel] = sample(source, sx, sy, channel)
  }
  for (let y = 317; y < output.height; y += 1) for (let x = 0; x < output.width; x += 1) {
    const offset = (y * output.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) output.data[offset + channel] = 0
  }
  return output
}

function edgeAlpha(png) {
  let count = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count += 1
  return count
}

function rowRange(png, y, fromX, toX) {
  const xs = []
  for (let x = fromX; x < toX; x += 1) if (png.data[(y * png.width + x) * 4 + 3] > 64) xs.push(x)
  if (!xs.length) throw new Error(`no contact alpha at y${y}`)
  return { minX: Math.min(...xs), maxX: Math.max(...xs), centreX: (Math.min(...xs) + Math.max(...xs)) / 2 }
}

const frames = []
for (const leg of ['right', 'left']) {
  const source = PNG.sync.read(fs.readFileSync(sources[leg]))
  const horizontalCorrection = leg === 'right' ? 22 : 20
  const verticalCorrection = leg === 'right' ? 5 : 0
  const output = contactLock(source, horizontalCorrection, verticalCorrection)
  if (output.width !== 256 || output.height !== 320 || edgeAlpha(output) !== 0) throw new Error(`${leg} cell contract failed`)
  const moving = rowRange(output, 282, 0, 132)
  const support = rowRange(output, 316, 116, 256)
  const separation = support.centreX - moving.centreX
  if (Math.abs(separation - 48) > 1.5) throw new Error(`${leg} horizontal contact separation ${separation}px is not one 6-lp tread`)
  const file = path.join(outputDir, `keeper_prime_stair_${leg}-contact_side-left_f01.png`)
  fs.writeFileSync(file, PNG.sync.write(output))
  frames.push({
    leg, source: { file: rel(sources[leg]), sha256: sha(sources[leg]) },
    file: rel(file), sha256: sha(file), cell: [256, 320], density: 8,
    supportSole: { y: 316, ...support }, movingSole: { y: 282, ...moving },
    localSeparation: { xPx: separation, yPx: 34, xLp: separation / 8, yLp: 34 / 8 }, edgeAlpha: 0,
  })
}

const prepPath = path.join(pack, 'source-preparation-v7.json')
writeJson(prepPath, {
  schema: 'lighthouse-keeper/stair-ascent-source-preparation@7',
  mode: 'two-contact-only-deterministic-lower-leg-registration',
  rejectedV6: 'Six intermediate phases still allowed boots to pass through tread geometry.',
  correction: { rightMovingLegHorizontalPx: 22, leftMovingLegHorizontalPx: 20, rightMovingLegVerticalPx: 5, leftMovingLegVerticalPx: 0, unchangedUpperBodyThroughY: 219 },
  contract: 'Every frame shows one support sole at y316 and the opposite moving sole at y282, separated horizontally by one 48-px/6-lp tread.',
  frames,
})
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime stair ascent V7\n\nStatus: minimal two-contact mechanical proof awaiting Frank's review.\n\nV7 rejects V6 motion. It contains only two climb drawings: RIGHT foot forward/up, then LEFT foot forward/up. Those two planted-contact states repeat across fourteen treads. There are deliberately no lift, swing, high-pass or weight-transfer drawings. Nothing is approved or promoted.\n`)
console.log(JSON.stringify({ preparation: rel(prepPath), frames }, null, 2))
