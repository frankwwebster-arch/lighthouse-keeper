#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, '../..')
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'), 'utf8'))
const failures = []
const check = (condition, message) => { if (!condition) failures.push(message) }
const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const load = (file) => PNG.sync.read(fs.readFileSync(file))

check(manifest.schema === 'lighthouse-keeper/kitchen-v8-room-shell@1', 'unexpected manifest schema')
check(JSON.stringify(manifest.modulePx) === JSON.stringify([2048, 576]), 'module must be 2048 x 576')
check(manifest.backWallLineY === 460, 'back-wall line must be y=460')
check(manifest.floorFrontY === 544, 'floor front must be y=544')
check(JSON.stringify(manifest.floorSlabPx) === JSON.stringify([544, 576]), 'floor slab must be y=544..576')
check(manifest.walkY === 502, 'Kitchen walkY must be 502')
check(manifest.backWallSpanPx[0] <= 360 && manifest.backWallSpanPx[1] >= 1995, 'back wall must span at least x=360..1995')
check(manifest.futureRangeWidthPx === 252, 'future range reservation must remain 252 px')
check(manifest.futureRangeDrawn === false, 'future 252 px range must remain undrawn')
check(manifest.doors.left.includes('stage-front') && manifest.doors.right.includes('stage-front'), 'both doors must be stage-front')

for (const [relative, expected] of Object.entries(manifest.files)) {
  const file = path.join(__dirname, relative)
  check(fs.existsSync(file), `missing output ${relative}`)
  if (!fs.existsSync(file)) continue
  const image = load(file)
  check(image.width === expected.canvasPx[0] && image.height === expected.canvasPx[1], `${relative} dimensions changed`)
  check(fs.statSync(file).size === expected.bytes, `${relative} byte length changed`)
  check(sha256(file) === expected.sha256, `${relative} hash changed`)
}

for (const [relative, expectedHash] of Object.entries(manifest.inputFiles)) {
  const file = path.join(ROOT, relative)
  check(fs.existsSync(file), `missing inherited v8 asset ${relative}`)
  if (fs.existsSync(file)) check(sha256(file) === expectedHash, `inherited v8 asset changed: ${relative}`)
}
for (const [relative, expectedHash] of Object.entries(manifest.styleSources)) {
  const file = path.join(ROOT, relative)
  check(fs.existsSync(file), `missing style source ${relative}`)
  if (fs.existsSync(file)) check(sha256(file) === expectedHash, `style source changed: ${relative}`)
}
const keeper = path.join(ROOT, manifest.primeKeeper.file)
check(fs.existsSync(keeper), 'Prime Keeper source missing')
if (fs.existsSync(keeper)) check(sha256(keeper) === manifest.primeKeeper.sha256, 'Prime Keeper source changed')

const shellFile = path.join(__dirname, 'outputs/kitchen-v8-room-shell-empty-1x.png')
const furnishedFile = path.join(__dirname, 'outputs/kitchen-v8-room-furnished-1x.png')
const shell = load(shellFile)
const furnished = load(furnishedFile)
check(shell.width === 2048 && shell.height === 576, 'empty shell is not exact module size')
check(furnished.width === 2048 && furnished.height === 576, 'furnished room is not exact module size')

const paneContains = (x, y) => manifest.windowPanesPx.some(([x0, y0, x1, y1]) => x >= x0 && x < x1 && y >= y0 && y < y1)
let magentaCount = 0
let unexpectedMagenta = 0
let nearMagentaOutside = 0
for (let y = 0; y < shell.height; y++) {
  for (let x = 0; x < shell.width; x++) {
    const offset = (y * shell.width + x) * 4
    const [r, g, b, a] = shell.data.subarray(offset, offset + 4)
    const exact = r === 255 && g === 0 && b === 255 && a === 255
    if (exact) {
      magentaCount++
      if (!paneContains(x, y)) unexpectedMagenta++
    } else if (!paneContains(x, y) && r >= 220 && b >= 220 && g <= 80) nearMagentaOutside++
  }
}
const expectedMagenta = manifest.windowPanesPx.reduce((total, [x0, y0, x1, y1]) => total + (x1 - x0) * (y1 - y0), 0)
check(magentaCount === expectedMagenta, `exact magenta count ${magentaCount} != ${expectedMagenta}`)
check(unexpectedMagenta === 0, `${unexpectedMagenta} exact-magenta pixels lie outside glass panes`)
check(nearMagentaOutside === 0, `${nearMagentaOutside} near-magenta pixels lie outside glass panes`)

// The exact window envelope must be untouched by all furniture and the Keeper.
for (const [x0, y0, x1, y1] of manifest.windowBoundsPx) {
  let changed = 0
  for (let y = y0; y < y1; y++) {
    for (let x = x0; x < x1; x++) {
      const offset = (y * shell.width + x) * 4
      for (let channel = 0; channel < 4; channel++) {
        if (shell.data[offset + channel] !== furnished.data[offset + channel]) { changed++; break }
      }
    }
  }
  check(changed === 0, `furniture occludes window ${x0},${y0}..${x1},${y1} (${changed} pixels)`)
}

// At 168 px/m, the raised window reads as a plausible 1.11 m sill and 2.11 m head.
const metres = (pixels) => pixels / 168
const sillMetres = metres(manifest.backWallLineY - manifest.windowBoundsPx[0][3])
const headMetres = metres(manifest.backWallLineY - manifest.windowBoundsPx[0][1])
check(Math.abs(sillMetres - 1.107142857) < 0.001, `window sill is ${sillMetres.toFixed(3)} m, expected 1.107 m`)
check(Math.abs(headMetres - 2.107142857) < 0.001, `window head is ${headMetres.toFixed(3)} m, expected 2.107 m`)
check(manifest.windowBoundsPx.every(([x0, y0, x1, y1]) => x1 - x0 === 168 && y1 - y0 === 168), 'both window envelopes must be 168 x 168')

// Stage-front doors must visibly occupy both near outer edges down to the floor front.
const countWood = (x0, y0, x1, y1) => {
  let count = 0
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const offset = (y * shell.width + x) * 4
    const r = shell.data[offset]
    const g = shell.data[offset + 1]
    const b = shell.data[offset + 2]
    if (r > 70 && r > g * 1.3 && g > b * 1.15) count++
  }
  return count
}
check(countWood(0, 100, 255, 544) > 45000, 'left stage-front door is not visibly present')
check(countWood(1998, 100, 2048, 544) > 8000, 'right stage-front door is not visibly present')

const outputNames = Object.keys(manifest.files).join('\n').toLowerCase()
check(!outputNames.includes('range'), 'a range output was added despite the deferral')

if (failures.length) {
  console.error(`Kitchen v8 room shell verification failed (${failures.length}):`)
  for (const failure of failures) console.error(`- ${failure}`)
  process.exit(1)
}
console.log(`Kitchen v8 room shell verified: exact 2048 x 576 geometry, ${magentaCount} crisp glass pixels, 1.11 m sills / 2.11 m heads, stage-front doors, inherited v8 assets unchanged, 252 px range absent.`)
