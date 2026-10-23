#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const draft = path.join(root, 'art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const readPng = relative => PNG.sync.read(fs.readFileSync(path.join(root, relative)))
const sha256 = relative => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relative))).digest('hex')

assert.deepEqual(manifest.gameContract.bodySize, [84, 74])
assert.equal(manifest.gameContract.bayCount, 6)
assert.equal(manifest.gameContract.runWidth, 504)
assert.equal(manifest.gameContract.masterBayWidth, 228)
assert.deepEqual(manifest.gameContract.masterBayBoundariesX, [65, 293, 521, 749, 977, 1205, 1433])
for (let index = 1; index < manifest.gameContract.masterBayBoundariesX.length; index += 1) {
  assert.equal(
    manifest.gameContract.masterBayBoundariesX[index] - manifest.gameContract.masterBayBoundariesX[index - 1],
    228,
    `master bay ${index} is not exactly 228 px`,
  )
}

for (const state of ['off', 'on', 'broken']) {
  for (const name of ['cupboard', 'drawers', 'sink', 'dishwasher', 'oven', 'fridge']) {
    const relative = `art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/candidates/${state}/${name}-${state}-84x74.png`
    const image = readPng(relative)
    assert.deepEqual([image.width, image.height], [84, 74], `${state}/${name} body-size drift`)
    assert.equal(sha256(relative), manifest.states[state][name], `${state}/${name} hash drift`)
  }
}

const nativeRuns = readPng(manifest.evidence.nativeRuns)
assert.deepEqual([nativeRuns.width, nativeRuns.height], [504, 222], 'native six-bay proof geometry drift')

function alpha(image, x, y) {
  return image.data[(y * image.width + x) * 4 + 3]
}

for (const [name, contract] of Object.entries({
  dishwasher: manifest.animation.dishwasher,
  oven: manifest.animation.oven,
})) {
  const strip = readPng(contract.strip)
  assert.deepEqual([strip.width, strip.height], [92 * 40, 82], `${name} strip geometry drift`)
  for (let frame = 0; frame < 40; frame += 1) {
    const x0 = frame * 92
    for (let x = 0; x < 92; x += 1) {
      assert.equal(alpha(strip, x0 + x, 0), 0, `${name} frame ${frame} touches top edge`)
      assert.equal(alpha(strip, x0 + x, 81), 0, `${name} frame ${frame} touches bottom edge`)
    }
    for (let y = 0; y < 82; y += 1) {
      assert.equal(alpha(strip, x0, y), 0, `${name} frame ${frame} touches left edge`)
      assert.equal(alpha(strip, x0 + 91, y), 0, `${name} frame ${frame} touches right edge`)
    }
  }
  assert.equal(sha256(contract.strip), contract.sha256, `${name} strip hash drift`)
}

assert.equal(manifest.animation.frameCount, 40)
assert.equal(manifest.animation.fps, 4)
assert.deepEqual(manifest.animation.cellSize, [92, 82])
assert.equal(manifest.animation.dishwasher.schedules.length, 3)
for (const [index, schedule] of manifest.animation.dishwasher.schedules.entries()) {
  assert.equal(schedule.length, 40, `dishwasher light ${index} schedule length drift`)
  assert.ok(schedule.includes(true) && schedule.includes(false), `dishwasher light ${index} does not blink`)
}
assert.equal(new Set(manifest.animation.dishwasher.schedules.map(schedule => schedule.join(''))).size, 3, 'dishwasher lights are not independent')
assert.equal(manifest.animation.oven.schedule.length, 40)
assert.ok(manifest.animation.oven.schedule.includes(true) && manifest.animation.oven.schedule.includes(false), 'oven cavity does not flicker')

assert.equal(manifest.production.register, false)
assert.equal(manifest.production.promote, false)
assert.equal(manifest.production.runtimeWired, false)

console.log('Kitchen Warm Ligne-Claire Family V4 verification passed.')
