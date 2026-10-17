#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v1')
const register = JSON.parse(fs.readFileSync(path.join(pack, 'batch-register.json'), 'utf8'))
const route = JSON.parse(fs.readFileSync(path.join(pack, 'keeper-prime-sit-stand-side-v1.json'), 'utf8'))
const page = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sit-stand-side-v1/index.html'), 'utf8')
const workbench = JSON.parse(fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-context-workbench-v10/catalog.json'), 'utf8'))
const workbenchRegister = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-context-workbench-2026-10-17-v10/batch-register.json'), 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

assert.equal(register.status, 'draft-awaiting-frank')
assert.equal(register.approvalBoundary.promotionAllowed, false)
assert.equal(register.candidate.frames.length, 6)
assert.equal(route.route.length, 45)
assert.equal(route.room.chair.seatHeightAboveFloorLp, 11)
assert.equal(route.room.chair.seatTopLp, route.room.floorLp - 11)
assert.ok(page.includes('Promise.all(unique.map(preload))'))
assert.ok(page.includes('Previous-frame ghost'))
assert.ok(page.includes('Proposed game presentation · 4×'))
assert.ok(workbench.sequences.some((entry) => entry.id === 'prime-side-sit-stand-v1' && entry.url === '/keeper-review/keeper-prime-sit-stand-side-v1/'))
assert.equal(workbenchRegister.catalog.choices, 11)
assert.ok(Object.values(workbenchRegister.checks).every((value) => value === true || value === false))
assert.equal(workbenchRegister.checks.everyV9ChoiceRetained, true)
assert.equal(workbenchRegister.checks.sideSitStandAddedOnce, true)
assert.equal(workbenchRegister.checks.inventoryDuplicated, false)

for (const frame of register.candidate.frames) {
  const file = path.join(root, frame.file)
  assert.equal(sha(file), frame.sha256)
  const png = PNG.sync.read(fs.readFileSync(file))
  assert.deepEqual([png.width, png.height], [256, 320])
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x++) {
    edgeAlpha += Number(png.data[x * 4 + 3] !== 0)
    edgeAlpha += Number(png.data[((png.height - 1) * png.width + x) * 4 + 3] !== 0)
  }
  for (let y = 1; y < png.height - 1; y++) {
    edgeAlpha += Number(png.data[(y * png.width) * 4 + 3] !== 0)
    edgeAlpha += Number(png.data[(y * png.width + png.width - 1) * 4 + 3] !== 0)
  }
  assert.equal(edgeAlpha, 0, `frame ${frame.frame} touches a cell edge`)
  assert.ok(frame.transparentGutterPx >= 4)
}

assert.equal(register.candidate.frames[0].sha256, register.authorities.standing.sha256)
assert.equal(register.candidate.frames[5].sha256, register.authorities.seated.sha256)
const forwardHashes = register.candidate.frames.map((frame) => frame.sha256)
const reverseSidecar = JSON.parse(fs.readFileSync(register.candidate.reverseStrip.file.replace(/\.png$/, '.json'), 'utf8'))
assert.deepEqual(reverseSidecar.frameSha256, [...forwardHashes].reverse())
assert.ok(route.route.filter((frame) => frame.phase.includes('sit') || frame.phase === 'seated hold').every((frame) => frame.rootXLp === route.room.chair.rootXLp))
assert.ok(Object.values(register.checks).every(Boolean))

console.log(`Keeper Prime sit/stand side V1 verified: ${register.candidate.frames.length} isolated poses, ${route.route.length} contextual frames, exact endpoints and 11-lp chair contact.`)
