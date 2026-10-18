import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sourceDir = path.join(root, 'art/source/kitchen-fridge-states-2026-10-18-v39/generated')
const rawDir = path.join(root, 'art/raw/kitchen-fridge-states-2026-10-18-v39')
const draftDir = path.join(root, 'art/drafts/kitchen-fridge-states-2026-10-18-v39')
const pageFile = path.join(root, 'public/keeper-review/kitchen-fridge-states-v39/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-fridge-states-v39.json')
const baseRoomFile = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v31/kitchen-bin-standard-in-situ.png')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const alpha = (image, x, y) => pixel(image, x, y)[3]

const sourceHashes = {
  'fridge-two-state-from-scratch-source-v1.png': 'c0b3549d879584c17e9a3db57e15c140c3e99664fc114402b019f3eda71ec66d',
  'fridge-two-state-compact-hinge-source-v2.png': '48a8c8e03e2ea791d69124de2853d8223d8ce62801604461bd40405316fadaba',
}
for (const [name, expected] of Object.entries(sourceHashes)) assert.equal(sha(path.join(sourceDir, name)), expected, `${name} changed`)

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 39)
assert.equal(catalogue.status, 'from-scratch-fridge-correction-awaiting-review')
assert.deepEqual(catalogue.states, ['standard', 'broken_hinge_failed'])
assert.deepEqual(catalogue.cellPixels, [136, 104])
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.deepEqual(catalogue.roomCellTopLeft, [58, 136])
assert.deepEqual(catalogue.fridgeBayPixels, [84, 140, 168, 218])
assert.equal(catalogue.floorSurfaceY, 218)
assert.equal(catalogue.source.sha256, sourceHashes['fridge-two-state-compact-hinge-source-v2.png'])
assert.equal(register.status, 'awaiting-fridge-visual-review')
assert.equal(register.supersedesRejectedDraft, 32)
assert.deepEqual(register.rejectedBatch, [33, 34, 35, 36, 37, 38])
assert.equal(register.nextAssetBlockedUntilApproval, 'kettle')

for (const name of ['fridge-standard.png', 'fridge-broken-hinge-failed.png']) {
  const file = path.join(rawDir, name)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [136, 104], `${name} cell geometry changed`)
  assert.equal(sha(file), catalogue.outputs[name].sha256, `${name} output hash drifted`)
  for (let x = 0; x < image.width; x++) {
    assert.equal(alpha(image, x, 0), 0, `${name} touches top edge`)
    assert.equal(alpha(image, x, image.height - 1), 0, `${name} touches bottom edge`)
  }
  for (let y = 0; y < image.height; y++) {
    assert.equal(alpha(image, 0, y), 0, `${name} touches left edge`)
    assert.equal(alpha(image, image.width - 1, y), 0, `${name} touches right edge`)
  }
  for (let index = 3; index < image.data.length; index += 4) assert.ok(image.data[index] === 0 || image.data[index] === 255, `${name} contains partial alpha`)
}

assert.deepEqual(catalogue.opaqueBounds.standard, [26, 4, 110, 82])
assert.deepEqual(catalogue.opaqueBounds.broken_hinge_failed, [2, 4, 122, 89])
assert.deepEqual([58 + 26, 136 + 4, 58 + 110, 136 + 82], [84, 140, 168, 218], 'standard state does not fill the measured fridge bay exactly')

const base = png(baseRoomFile)
const cleared = png(path.join(rawDir, 'kitchen-fridge-cleared-bay.png'))
assert.deepEqual([cleared.width, cleared.height], [772, 224])
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  const inside = x >= 84 && x < 168 && y >= 151 && y < 218
  const expected = inside ? pixel(base, x + 84, y) : pixel(base, x, y)
  assert.deepEqual([...pixel(cleared, x, y)], [...expected], `cleared room mismatch at ${x},${y}`)
}
let removedWhitePixels = 0
for (let y = 151; y < 218; y++) for (let x = 84; x < 168; x++) {
  const [r0, g0, b0] = pixel(base, x, y)
  const [r1, g1, b1] = pixel(cleared, x, y)
  if (r0 > 190 && g0 > 190 && b0 > 190 && (r1 < 100 || g1 < 130 || b1 < 170)) removedWhitePixels++
}
assert.ok(removedWhitePixels > 1000, 'original white fridge was not demonstrably cleared')

for (const name of ['kitchen-fridge-standard-in-situ.png', 'kitchen-fridge-broken-in-situ.png']) {
  const file = path.join(rawDir, name)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [772, 224], `${name} is not exact game size`)
  assert.equal(sha(file), catalogue.outputs[name].sha256, `${name} output hash drifted`)
}

const broken = png(path.join(rawDir, 'fridge-broken-hinge-failed.png'))
let poolOnFloor = 0
for (let y = 82; y <= 88; y++) for (let x = 2; x <= 80; x++) {
  const [r, g, b, a] = pixel(broken, x, y)
  if (a && b > r * 1.08 && g > r * 1.08) poolOnFloor++
}
assert.ok(poolOnFloor >= 30, 'static pool is not flattened across the measured floor band')
let doorFloorContact = 0
for (let y = 78; y <= 88; y++) for (let x = 35; x <= 65; x++) {
  const [r, g, b, a] = pixel(broken, x, y)
  if (a && r > 150 && g > 145 && b > 140) doorFloorContact++
}
assert.ok(doorFloorContact >= 12, 'fallen door lower-left corner does not reach the floor band')
let hingeArmPixels = 0
for (let y = 68; y <= 84; y++) for (let x = 70; x <= 118; x++) {
  const [r, g, b, a] = pixel(broken, x, y)
  if (a && r > 130 && r > g * 1.4 && g > b * 1.2) hingeArmPixels++
}
assert.ok(hingeArmPixels >= 35, 'connected lower-right hinge arm is no longer readable')

const effect = catalogue.effects.slow_drip_pool_ripple
assert.equal(effect.reusable, true)
assert.equal(effect.effectOnly, true)
assert.equal(effect.frames, 40)
assert.equal(effect.fps, 4)
assert.equal(effect.durationSeconds, 10)
assert.deepEqual(effect.cellPixels, [136, 104])
const strip = png(path.join(rawDir, effect.file))
assert.deepEqual([strip.width, strip.height], [5440, 104])
assert.equal(sha(path.join(rawDir, effect.file)), catalogue.outputs[effect.file].sha256)
const frameHashes = new Set()
for (let frame = 0; frame < 40; frame++) {
  const x0 = frame * 136
  const bytes = Buffer.alloc(136 * 104 * 4)
  let opaque = 0
  for (let x = 0; x < 136; x++) {
    assert.equal(alpha(strip, x0 + x, 0), 0, `effect frame ${frame} touches top edge`)
    assert.equal(alpha(strip, x0 + x, 103), 0, `effect frame ${frame} touches bottom edge`)
  }
  for (let y = 0; y < 104; y++) {
    assert.equal(alpha(strip, x0, y), 0, `effect frame ${frame} touches left edge`)
    assert.equal(alpha(strip, x0 + 135, y), 0, `effect frame ${frame} touches right edge`)
    strip.data.copy(bytes, y * 136 * 4, (y * strip.width + x0) * 4, (y * strip.width + x0 + 136) * 4)
    for (let x = 0; x < 136; x++) if (alpha(strip, x0 + x, y)) opaque++
  }
  assert.ok(opaque >= 2 && opaque <= 45, `effect frame ${frame} is missing or not restrained`)
  frameHashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
}
assert.ok(frameHashes.size >= 30, 'effect lacks a full sedate ten-second pose range')

assert.deepEqual(catalogue.construction, {
  fromScratch: true,
  coordinatedFamily: true,
  sameSourceSheet: true,
  previousFridgeClearedBeforeComposite: true,
  objectAnimated: false,
  topHingeFailed: true,
  lowerRightHingeAttached: true,
  singleGrillePerState: true,
  doorLowerLeftRestsOnFloor: true,
  staticPoolOnFloorSurface: true,
  visibleElectricalEffects: false,
})
assert.equal(catalogue.sfxCues[0].cue, 'kitchen_fridge_low_electrical_buzz_loop')
assert.equal(catalogue.sfxCues[0].visibleEffect, false)

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /does not reuse V32 fridge pixels/)
assert.match(page, /previous fridge removed/)
assert.match(page, /Reusable drip and ripple only/)
assert.match(page, /No fridge artwork is present in this strip/)
assert.match(page, /exact 772 × 224 game pixels/)
assert.match(page, /data-strip data-frames="40" data-fps="4"/)
assert.match(page, /Promise\.all\(unique\.map\(preload\)\)/)
assert.doesNotMatch(page, /fridge-v21-current\.png/)
assert.doesNotMatch(page, /fx-(spark|smoke|flash)/i)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-fridge-states-v39'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 6)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V39 verified: from-scratch family, cleared bay, exact floor contact, single fridge/grille, compact attached hinge, and isolated 40-frame FX')
