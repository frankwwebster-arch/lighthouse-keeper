import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sourceDir = path.join(root, 'art/source/kitchen-fridge-states-2026-10-18-v32/generated')
const rawDir = path.join(root, 'art/raw/kitchen-fridge-states-2026-10-18-v32')
const draftDir = path.join(root, 'art/drafts/kitchen-fridge-states-2026-10-18-v32')
const pageFile = path.join(root, 'public/keeper-review/kitchen-fridge-states-v32/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-fridge-states-v32.json')
const approvalFile = path.join(root, 'docs/review/kitchen-fridge-states-v32-approval-2026-10-18.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const alpha = (image, x, y) => pixel(image, x, y)[3]

const sourceHashes = {
  'fridge-two-state-source-v1.png': 'fadbe42e57d9b8611e23d3be10c513e6481c5b847e774c4a26e1d9eb78bc0980',
  'fridge-two-state-contents-source-v2.png': '07dd6abc154ac667ae004f8d133f3c8e681080b642496b8fb11c86b0d78dded3',
  'fridge-two-state-floor-contact-source-v3.png': '0a69aa583eb9964ad17886b88f486e1c7d7d938938725df856cf5118b50e549d',
}
for (const [name, expected] of Object.entries(sourceHashes)) assert.equal(sha(path.join(sourceDir, name)), expected, `${name} changed`)

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 32)
assert.equal(catalogue.status, 'fridge-state-family-awaiting-visual-confirmation')
assert.deepEqual(catalogue.states, ['standard', 'broken_hinge_failed'])
assert.deepEqual(catalogue.cellPixels, [120, 96])
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.deepEqual(catalogue.roomCellTopLeft, [66, 127])
assert.deepEqual(catalogue.fridgeBayPixels, [84, 168])
assert.equal(catalogue.fridgeFootY, 208)
assert.equal(catalogue.source.sha256, sourceHashes['fridge-two-state-floor-contact-source-v3.png'])
assert.deepEqual(catalogue.source.sharedReducedSize, [116, 80])
assert.equal(register.status, 'awaiting-fridge-visual-review')
assert.equal(register.nextAssetBlockedUntilApproval, 'kettle')
assert.equal(register.originalHashes.v21Fridge, 'e59142a1ed4d7181daa2b4968061642416e3d3352c1cbd3fd7e053676c25da6c')
assert.equal(register.originalHashes.v31Room, '027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674')

for (const name of ['fridge-standard.png', 'fridge-broken-hinge-failed.png']) {
  const file = path.join(rawDir, name)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [120, 96], `${name} cell geometry changed`)
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

const standardBounds = catalogue.opaqueBounds.standard
const brokenBounds = catalogue.opaqueBounds.broken_hinge_failed
assert.deepEqual(standardBounds, [18, 13, 101, 81])
assert.deepEqual(brokenBounds, [14, 13, 115, 89])
assert.equal(66 + standardBounds[0], 84, 'standard fridge no longer begins on the fitted bay edge')
assert.ok(66 + standardBounds[2] <= 168, 'standard fridge exceeds the fitted bay width')
assert.equal(127 + standardBounds[1], 140, 'standard sea-glass cap no longer meets the approved worktop top')
assert.equal(127 + standardBounds[3], 208, 'standard fridge no longer meets the approved foot line')
assert.ok(brokenBounds[0] < standardBounds[0] && brokenBounds[2] > standardBounds[2], 'broken door/pool needs a wider footprint than standard')
assert.ok(brokenBounds[3] > standardBounds[3], 'broken pool must extend into the foreground')

const broken = png(path.join(rawDir, 'fridge-broken-hinge-failed.png'))
let floorContactPale = 0
let floorContactWater = 0
for (let y = 84; y <= 88; y++) for (let x = 24; x <= 54; x++) {
  const [r, g, b, a] = pixel(broken, x, y)
  if (a && r > 130 && g > 125 && b > 120) floorContactPale++
  if (a && b > r * 1.1 && g > r * 1.1) floorContactWater++
}
assert.ok(floorContactPale >= 20, 'fallen door lower-left corner does not reach the floor-contact band')
assert.ok(floorContactWater >= 20, 'static pool does not meet the fallen door floor-contact band')

let creamContents = 0
let greenContents = 0
let orangeContents = 0
for (let y = 26; y <= 69; y++) for (let x = 72; x <= 101; x++) {
  const [r, g, b, a] = pixel(broken, x, y)
  if (!a) continue
  if (r > 150 && g > 145 && b > 115) creamContents++
  if (g > r * 1.12 && g > b * 0.9) greenContents++
  if (r > 105 && r > g * 1.18 && g > b * 1.05) orangeContents++
}
assert.ok(creamContents >= 12, 'generic pale milk container is no longer readable')
assert.ok(greenContents >= 6, 'generic green produce is no longer readable')
assert.ok(orangeContents >= 6, 'generic jar/orange produce is no longer readable')

for (const name of ['fridge-v21-current.png', 'kitchen-fridge-standard-in-situ.png', 'kitchen-fridge-broken-in-situ.png']) {
  const file = path.join(rawDir, name)
  assert.equal(sha(file), catalogue.outputs[name].sha256, `${name} output hash drifted`)
}
for (const name of ['kitchen-fridge-standard-in-situ.png', 'kitchen-fridge-broken-in-situ.png']) {
  const image = png(path.join(rawDir, name))
  assert.deepEqual([image.width, image.height], [772, 224], `${name} is not exact game size`)
}

const effect = catalogue.effects.slow_drip_pool_ripple
assert.equal(effect.reusable, true)
assert.equal(effect.frames, 40)
assert.equal(effect.fps, 4)
assert.equal(effect.durationSeconds, 10)
assert.deepEqual(effect.cellPixels, [120, 96])
assert.equal(effect.objectPixelsChanged, false)
assert.equal(effect.sfxCue, 'kitchen_fridge_water_drip_slow')
const effectFile = path.join(rawDir, effect.file)
const strip = png(effectFile)
assert.deepEqual([strip.width, strip.height], [4800, 96])
assert.equal(sha(effectFile), catalogue.outputs[effect.file].sha256)
const frameHashes = new Set()
for (let frame = 0; frame < 40; frame++) {
  const x0 = frame * 120
  const bytes = Buffer.alloc(120 * 96 * 4)
  let opaque = 0
  for (let x = 0; x < 120; x++) {
    assert.equal(alpha(strip, x0 + x, 0), 0, `effect frame ${frame} touches top edge`)
    assert.equal(alpha(strip, x0 + x, 95), 0, `effect frame ${frame} touches bottom edge`)
  }
  for (let y = 0; y < 96; y++) {
    assert.equal(alpha(strip, x0, y), 0, `effect frame ${frame} touches left edge`)
    assert.equal(alpha(strip, x0 + 119, y), 0, `effect frame ${frame} touches right edge`)
    strip.data.copy(bytes, y * 120 * 4, (y * strip.width + x0) * 4, (y * strip.width + x0 + 120) * 4)
    for (let x = 0; x < 120; x++) if (alpha(strip, x0 + x, y)) opaque++
  }
  assert.ok(opaque >= 2 && opaque <= 40, `effect frame ${frame} is missing or no longer restrained`)
  frameHashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
}
assert.ok(frameHashes.size >= 30, 'effect lacks a full sedate ten-second pose range')

assert.deepEqual(catalogue.sfxCues[0], { cue: 'kitchen_fridge_low_electrical_buzz_loop', state: 'broken_hinge_failed', visibleEffect: false })
assert.deepEqual(catalogue.boundaries, {
  approved: false,
  promoted: false,
  runtimeChanged: false,
  finalChanged: false,
  v20ThroughV31Changed: false,
  laterKitchenAssetsStarted: false,
})
assert.deepEqual(catalogue.construction, {
  coordinatedFamily: true,
  sameSourceSheet: true,
  objectAnimated: false,
  topHingeFailed: true,
  lowerRightHingeAttached: true,
  doorLowerLeftRestsOnFloor: true,
  staticPoolIncluded: true,
  visibleElectricalEffects: false,
})

const approval = JSON.parse(fs.readFileSync(approvalFile, 'utf8'))
assert.equal(approval.assetFamily, 'kitchen-fridge-states-v32')
assert.equal(approval.verdict, 'excellent')
assert.equal(approval.scope, 'visual-review authority only; no Final or runtime promotion')
assert.equal(approval.selectedSource.sha256, sourceHashes['fridge-two-state-floor-contact-source-v3.png'])
for (const [name, expected] of Object.entries(approval.approvedOutputs)) assert.equal(catalogue.outputs[name].sha256, expected, `${name} no longer matches the approved V32 record`)
assert.deepEqual(approval.sequenceReleased, ['kettle', 'toaster', 'oven', 'mixing-bowl', 'basin', 'table'])

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /coordinated standard and broken family/)
assert.match(page, /exact 772 × 224 game pixels/)
assert.match(page, /40 frames · 4 fps · 10 seconds/)
assert.match(page, /data-strip data-frames="40" data-fps="4"/)
assert.match(page, /new Set\(/)
assert.match(page, /Promise\.all\(unique\.map\(preload\)\)/)
assert.match(page, /Playback unlocked/)
assert.match(page, /low buzz placeholder/)
assert.match(page, /No smoke, sparks or electrical flash/)
assert.doesNotMatch(page, /fx-(spark|smoke|flash)/i)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-fridge-states-v32'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 6)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V32 verified: coordinated static fridge states, literal door-floor contact, generic contents, isolated 40-frame drip/ripple FX, and named low buzz')
