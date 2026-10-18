import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sourceDir = path.join(root, 'art/source/kitchen-oven-states-2026-10-18-v40/generated')
const rawDir = path.join(root, 'art/raw/kitchen-oven-states-2026-10-18-v40')
const draftDir = path.join(root, 'art/drafts/kitchen-oven-states-2026-10-18-v40')
const pageFile = path.join(root, 'public/keeper-review/kitchen-oven-states-v40/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-oven-states-v40.json')
const baseRoomFile = path.join(root, 'art/raw/kitchen-fridge-states-2026-10-18-v39/kitchen-fridge-standard-in-situ.png')
const fridgeApprovalFile = path.join(root, 'docs/review/kitchen-fridge-states-v39-approval-2026-10-18.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const alpha = (image, x, y) => pixel(image, x, y)[3]

const sourceHashes = {
  'oven-three-state-from-scratch-source-v1.png': '8760a7b8ba49ad170c17d5fd1114620fb504449f7bfbad35c34be27ccca95559',
  'oven-three-state-hanging-dial-source-v2.png': 'd21f2ba12fb4fd2b2c5e1483b0792717cd316e964f59c63d75f40dec9ffcca78',
}
for (const [name, expected] of Object.entries(sourceHashes)) assert.equal(sha(path.join(sourceDir, name)), expected, `${name} changed`)

const fridgeApproval = JSON.parse(fs.readFileSync(fridgeApprovalFile, 'utf8'))
assert.equal(fridgeApproval.decision, 'approved-as-kitchen-fridge-review-authority')
assert.equal(fridgeApproval.approvalBoundary.sequenceReleased, 'oven')

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 40)
assert.equal(catalogue.asset, 'oven')
assert.equal(catalogue.status, 'from-scratch-oven-family-awaiting-review')
assert.deepEqual(catalogue.states, ['off', 'on', 'broken'])
assert.deepEqual(catalogue.cellPixels, [104, 112])
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.deepEqual(catalogue.roomCellTopLeft, [326, 119])
assert.deepEqual(catalogue.ovenBayPixels, [336, 123, 420, 218])
assert.equal(catalogue.floorSurfaceY, 218)
assert.equal(catalogue.source.sha256, sourceHashes['oven-three-state-hanging-dial-source-v2.png'])
assert.equal(catalogue.approvedContext.v39RoomSha256, fridgeApproval.approvedHashes.outputs['kitchen-fridge-standard-in-situ.png'])
assert.equal(register.status, 'awaiting-oven-visual-review')
assert.equal(register.supersedesRejectedDraft, 35)
assert.equal(register.preservesApprovedFridge, 39)

const states = {}
for (const name of ['off', 'on', 'broken']) {
  const file = path.join(rawDir, `oven-${name}.png`)
  const image = png(file)
  states[name] = image
  assert.deepEqual([image.width, image.height], [104, 112], `${name} cell geometry changed`)
  assert.equal(sha(file), catalogue.outputs[`oven-${name}.png`].sha256, `${name} output hash drifted`)
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
assert.deepEqual(catalogue.opaqueBounds, {
  off: [10, 4, 94, 99],
  on: [10, 4, 94, 99],
  broken: [10, 4, 94, 99],
})
assert.deepEqual([326 + 10, 119 + 4, 326 + 94, 119 + 99], [336, 123, 420, 218], 'oven family does not fill the measured bay exactly')

const base = png(baseRoomFile)
const cleared = png(path.join(rawDir, 'kitchen-oven-cleared-bay.png'))
assert.deepEqual([cleared.width, cleared.height], [772, 224])
let removedOvenPixels = 0
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  let expected
  if (x >= 336 && x < 420 && y >= 123 && y < 151) expected = pixel(base, x - 252, y)
  else if (x >= 336 && x < 420 && y >= 151 && y < 218) expected = pixel(base, x - 168, y)
  else expected = pixel(base, x, y)
  assert.deepEqual([...pixel(cleared, x, y)], [...expected], `cleared room mismatch at ${x},${y}`)
  if (x >= 336 && x < 420 && y >= 123 && y < 218 && !pixel(base, x, y).equals(expected)) removedOvenPixels++
}
assert.ok(removedOvenPixels > 3500, 'previous oven and hob were not demonstrably cleared')

for (const name of ['off', 'on', 'broken']) {
  const file = path.join(rawDir, `kitchen-oven-${name}-in-situ.png`)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [772, 224], `${name} room proof is not exact game size`)
  assert.equal(sha(file), catalogue.outputs[`kitchen-oven-${name}-in-situ.png`].sha256, `${name} room hash drifted`)
}

const windowStats = image => {
  let warm = 0
  let dark = 0
  for (let y = 45; y < 88; y++) for (let x = 20; x < 85; x++) {
    const [r, g, b, a] = pixel(image, x, y)
    if (!a) continue
    if (r > 120 && r > g * 1.3 && g > b * 1.4) warm++
    if (r < 55 && g < 60 && b < 80) dark++
  }
  return { warm, dark }
}
const offWindow = windowStats(states.off)
const onWindow = windowStats(states.on)
assert.ok(offWindow.dark > 1200, 'Off oven window is not predominantly dark')
assert.ok(onWindow.warm > offWindow.warm * 5, 'On oven lacks a strongly illuminated warm interior and roasting tin')
let offIndicatorEnergy = 0
let onIndicatorEnergy = 0
for (let y = 30; y <= 34; y++) for (let x = 50; x <= 53; x++) {
  const [or, og] = pixel(states.off, x, y)
  const [nr, ng] = pixel(states.on, x, y)
  offIndicatorEnergy += or + og
  onIndicatorEnergy += nr + ng
}
assert.ok(onIndicatorEnergy > offIndicatorEnergy * 1.45, 'On red indicator is not brighter than Off')

let hangingDialCopper = 0
let intactDialCopper = 0
for (let y = 40; y < 60; y++) for (let x = 70; x < 91; x++) {
  for (const [image, key] of [[states.broken, 'hanging'], [states.off, 'intact']]) {
    const [r, g, b, a] = pixel(image, x, y)
    if (a && r > 100 && g > 35 && g < 150 && b < 70 && r > g * 1.3) {
      if (key === 'hanging') hangingDialCopper++
      else intactDialCopper++
    }
  }
}
assert.ok(hangingDialCopper >= 50, 'Broken rotary dial is not visibly hanging below the fascia')
assert.ok(hangingDialCopper > intactDialCopper * 2, 'Broken hanging dial is not distinct from the intact fascia control')

assert.deepEqual(catalogue.construction, {
  fromScratch: true,
  coordinatedFamily: true,
  sameSourceSheet: true,
  previousOvenAndHobClearedBeforeComposite: true,
  objectAnimated: false,
  offInteriorDark: true,
  offIndicatorDark: true,
  onInteriorLight: true,
  onDialsTurned: true,
  onRedIndicator: true,
  onRoastingTin: true,
  brokenDoorAttachedAskew: true,
  brokenDialHangingByWires: true,
  smokeBakedIntoObject: false,
  flamesBakedIntoObject: false,
  warningLightBakedIntoObject: false,
})

const verifyEffect = (effect, minimumOpaque, maximumOpaque, minimumUnique) => {
  assert.equal(effect.reusable, true)
  assert.equal(effect.effectOnly, true)
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
  assert.deepEqual(effect.cellPixels, [120, 144])
  const file = path.join(rawDir, effect.file)
  const strip = png(file)
  assert.deepEqual([strip.width, strip.height], [4800, 144])
  assert.equal(sha(file), catalogue.outputs[effect.file].sha256)
  const hashes = new Set()
  for (let frame = 0; frame < 40; frame++) {
    const x0 = frame * 120
    const bytes = Buffer.alloc(120 * 144 * 4)
    let opaque = 0
    for (let x = 0; x < 120; x++) {
      assert.equal(alpha(strip, x0 + x, 0), 0, `${effect.file} frame ${frame} touches top edge`)
      assert.equal(alpha(strip, x0 + x, 143), 0, `${effect.file} frame ${frame} touches bottom edge`)
    }
    for (let y = 0; y < 144; y++) {
      assert.equal(alpha(strip, x0, y), 0, `${effect.file} frame ${frame} touches left edge`)
      assert.equal(alpha(strip, x0 + 119, y), 0, `${effect.file} frame ${frame} touches right edge`)
      strip.data.copy(bytes, y * 120 * 4, (y * strip.width + x0) * 4, (y * strip.width + x0 + 120) * 4)
      for (let x = 0; x < 120; x++) if (alpha(strip, x0 + x, y)) opaque++
    }
    assert.ok(opaque >= minimumOpaque && opaque <= maximumOpaque, `${effect.file} frame ${frame} effect density changed`)
    hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
  }
  assert.ok(hashes.size >= minimumUnique, `${effect.file} lacks a full ten-second pose range`)
}
verifyEffect(catalogue.effects.billowing_smoke, 2000, 2300, 40)
verifyEffect(catalogue.effects.hob_flames, 180, 240, 30)
verifyEffect(catalogue.effects.warning_light_flicker, 0, 300, 5)
assert.deepEqual(catalogue.effects.hob_flames.anchors, [[365, 134], [393, 134]])
assert.deepEqual(catalogue.effects.warning_light_flicker.redIndicatorAnchor, [378, 151])
assert.equal(catalogue.effects.warning_light_flicker.redBurstFrames, 21)
assert.equal(catalogue.effects.warning_light_flicker.cavityFlickerFrames, 5)
const warning = png(path.join(rawDir, catalogue.effects.warning_light_flicker.file))
let warningFrames = 0
let cavityFrames = 0
for (let frame = 0; frame < 40; frame++) {
  if (alpha(warning, frame * 120 + 60, 77)) warningFrames++
  if (alpha(warning, frame * 120 + 60, 96)) cavityFrames++
}
assert.equal(warningFrames, 21, 'angry red indicator burst timing changed')
assert.equal(cavityFrames, 5, 'occasional internal-light flicker timing changed')
assert.deepEqual(catalogue.sfxCues, ['kitchen_oven_on_fan_loop', 'kitchen_oven_broken_smoke_hiss_loop', 'kitchen_oven_hob_flame_loop', 'kitchen_oven_broken_warning_light_angry_blink_loop'])

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /previous oven and hob removed/i)
assert.match(page, /failed right dial hangs from two exposed wires/)
assert.match(page, /Reusable effects only/)
assert.match(page, /irregular rapid red bursts and rare internal-light flickers/)
assert.match(page, /exact 772 × 224 game pixels/)
assert.equal((page.match(/data-strip data-frames="40" data-fps="4"/g) || []).length, 9)
assert.match(page, /Promise\.all\(unique\.map\(preload\)\)/)
assert.doesNotMatch(page, /kitchen-oven-states-v35\/assets/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-oven-states-v40'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 10)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V40 verified: coordinated Off/On/Broken family, cleared bay, wired hanging dial, exact game placement, and isolated 40-frame smoke/flame/warning-light FX')
