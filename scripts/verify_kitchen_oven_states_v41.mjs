import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sourceFile = path.join(root, 'art/source/kitchen-oven-states-2026-10-18-v41/generated/oven-three-state-fitted-exact-size-source-v1.png')
const approvedFile = path.join(root, 'art/raw/kitchen-final-assets-2026-10-17-v21/basic-oven.png')
const baseRoomFile = path.join(root, 'art/raw/kitchen-fridge-states-2026-10-18-v39/kitchen-fridge-standard-in-situ.png')
const rawDir = path.join(root, 'art/raw/kitchen-oven-states-2026-10-18-v41')
const draftDir = path.join(root, 'art/drafts/kitchen-oven-states-2026-10-18-v41')
const pageFile = path.join(root, 'public/keeper-review/kitchen-oven-states-v41/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-oven-states-v41.json')
const builderFile = path.join(root, 'scripts/build_kitchen_oven_states_v41.py')

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const offset = (image, x, y) => (y * image.width + x) * 4
const pixel = (image, x, y) => image.data.subarray(offset(image, x, y), offset(image, x, y) + 4)
const alpha = (image, x, y) => pixel(image, x, y)[3]
const bbox = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) if (alpha(image, x, y)) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return maxX < 0 ? null : [minX, minY, maxX + 1, maxY + 1]
}

assert.equal(sha(sourceFile), '6ee0a16d77af2e0d76d8594b611cfc9e48abb963d5746073ab2785039f9828f9', 'V41 generated source changed')
assert.equal(sha(approvedFile), '45658c2649d10efc896d646821b16e12d3a19fc401d04168e00ace3a6f016ba8', 'V21 measurement/colour authority changed')
assert.equal(sha(baseRoomFile), '2778c5712deb7a11ddf4fbefdb6ae23cb825772af0db6d2db192a57ee59c7e85', 'approved V39 room changed')

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 41)
assert.equal(catalogue.asset, 'oven')
assert.equal(catalogue.status, 'exact-approved-size-colour-matched-family-awaiting-review')
assert.deepEqual(catalogue.states, ['off', 'on', 'broken'])
assert.deepEqual(catalogue.cellPixels, [108, 120])
assert.deepEqual(catalogue.approvedOpaqueBoundsExclusive, [12, 31, 96, 108])
assert.deepEqual(catalogue.opaqueFootprintPixels, [84, 77])
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.deepEqual(catalogue.roomCellTopLeft, [324, 100])
assert.deepEqual(catalogue.ovenBoundsInRoomExclusive, [336, 131, 420, 208])
assert.deepEqual(catalogue.measurementAuthority.hobRowsExclusive, [31, 48])
assert.equal(catalogue.measurementAuthority.hobPreservation, 'byte-identical')
assert.equal(catalogue.colourAuthority.opaquePaletteColours, 48)
assert.equal(catalogue.colourAuthority.generatedPanelColoursRestrictedToApprovedOpaquePalette, true)
assert.equal(register.status, 'awaiting-oven-visual-review')
assert.equal(register.supersedesRejectedDraft, 40)
assert.equal(register.preservesApprovedFridge, 39)

const reference = png(approvedFile)
assert.deepEqual([reference.width, reference.height], [108, 120])
assert.deepEqual(bbox(reference), [12, 31, 96, 108])
const approvedPalette = new Set(catalogue.colourAuthority.approvedPaletteRGB.map(rgb => rgb.join(',')))
const states = {}
for (const name of ['off', 'on', 'broken']) {
  const file = path.join(rawDir, `oven-${name}.png`)
  const image = png(file)
  states[name] = image
  assert.deepEqual([image.width, image.height], [108, 120], `${name} cell is not the exact approved size`)
  assert.deepEqual(bbox(image), [12, 31, 96, 108], `${name} does not use the exact approved 84 x 77 footprint`)
  assert.equal(sha(file), catalogue.outputs[`oven-${name}.png`].sha256, `${name} hash drifted`)
  for (let x = 0; x < image.width; x++) {
    assert.equal(alpha(image, x, 0), 0, `${name} touches top edge`)
    assert.equal(alpha(image, x, image.height - 1), 0, `${name} touches bottom edge`)
  }
  for (let y = 0; y < image.height; y++) {
    assert.equal(alpha(image, 0, y), 0, `${name} touches left edge`)
    assert.equal(alpha(image, image.width - 1, y), 0, `${name} touches right edge`)
  }
  // The complete approved hob and sea-glass surround are preserved exactly.
  for (let y = 31; y < 48; y++) for (let x = 0; x < 108; x++) {
    assert.deepEqual([...pixel(image, x, y)], [...pixel(reference, x, y)], `${name} changed approved hob pixel ${x},${y}`)
  }
  // Every generated fascia colour is selected from the V21-derived palette.
  for (let y = 48; y < 108; y++) for (let x = 12; x < 96; x++) {
    const [r, g, b, a] = pixel(image, x, y)
    if (a) {
      assert.equal(a, 255, `${name} generated panel contains partial alpha at ${x},${y}`)
      assert.ok(approvedPalette.has(`${r},${g},${b}`), `${name} panel colour ${r},${g},${b} is outside approved palette`)
    }
  }
}
assert.deepEqual(catalogue.opaqueBounds, { off: [12, 31, 96, 108], on: [12, 31, 96, 108], broken: [12, 31, 96, 108] })

const windowStats = image => {
  let warm = 0; let dark = 0
  for (let y = 70; y < 101; y++) for (let x = 25; x < 87; x++) {
    const [r, g, b, a] = pixel(image, x, y)
    if (!a) continue
    if (r > 100 && r > g * 1.25 && g > b * 1.2) warm++
    if (r < 60 && g < 70 && b < 85) dark++
  }
  return { warm, dark }
}
const offWindow = windowStats(states.off)
const onWindow = windowStats(states.on)
assert.ok(offWindow.dark > 800, 'Off cavity is not predominantly dark')
assert.ok(onWindow.warm > offWindow.warm * 4, 'On state lacks a strongly warm lit cavity and roasting tin')
let brokenRightCopper = 0
for (let y = 48; y < 78; y++) for (let x = 76; x < 96; x++) {
  const [r, g, b, a] = pixel(states.broken, x, y)
  if (a && r > 90 && r > g * 1.35 && g > b * 1.15) brokenRightCopper++
}
assert.ok(brokenRightCopper > 60, 'Broken dial is not visibly hanging beneath the right fascia socket')

const base = png(baseRoomFile)
const cleared = png(path.join(rawDir, 'kitchen-oven-cleared-bay.png'))
assert.deepEqual([cleared.width, cleared.height], [772, 224])
let removedPixels = 0
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  let expected
  if (x >= 336 && x < 420 && y >= 123 && y < 151) expected = pixel(base, x - 252, y)
  else if (x >= 336 && x < 420 && y >= 151 && y < 218) expected = pixel(base, x - 168, y)
  else expected = pixel(base, x, y)
  assert.deepEqual([...pixel(cleared, x, y)], [...expected], `cleared room mismatch at ${x},${y}`)
  if (x >= 336 && x < 420 && y >= 123 && y < 218 && !pixel(base, x, y).equals(expected)) removedPixels++
}
assert.ok(removedPixels > 3500, 'previous oven and hob were not fully removed')

for (const name of ['off', 'on', 'broken']) {
  const file = path.join(rawDir, `kitchen-oven-${name}-in-situ.png`)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [772, 224], `${name} room proof is not exact game size`)
  assert.equal(sha(file), catalogue.outputs[`kitchen-oven-${name}-in-situ.png`].sha256)
  for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
    if (x < 336 || x >= 420 || y < 131 || y >= 208) assert.deepEqual([...pixel(image, x, y)], [...pixel(cleared, x, y)], `${name} changed room outside measured oven footprint at ${x},${y}`)
  }
}

const componentCount = (strip, frame) => {
  const x0 = frame * 120
  const seen = new Uint8Array(120 * 144)
  let components = 0
  for (let y = 0; y < 144; y++) for (let x = 0; x < 120; x++) {
    const index = y * 120 + x
    if (seen[index] || !alpha(strip, x0 + x, y)) continue
    components++
    const stack = [[x, y]]; seen[index] = 1
    while (stack.length) {
      const [cx, cy] = stack.pop()
      for (const [nx, ny] of [[cx + 1, cy], [cx - 1, cy], [cx, cy + 1], [cx, cy - 1]]) {
        if (nx < 0 || nx >= 120 || ny < 0 || ny >= 144) continue
        const next = ny * 120 + nx
        if (seen[next] || !alpha(strip, x0 + nx, ny)) continue
        seen[next] = 1; stack.push([nx, ny])
      }
    }
  }
  return components
}

const verifyEffect = (effect, minOpaque, maxOpaque, minUnique, requireConnected = false) => {
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
    assert.ok(opaque >= minOpaque && opaque <= maxOpaque, `${effect.file} frame ${frame} density changed: ${opaque}`)
    if (requireConnected) assert.equal(componentCount(strip, frame), 1, `${effect.file} frame ${frame} is not one connected plume`)
    hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
  }
  assert.ok(hashes.size >= minUnique, `${effect.file} lacks a ten-second pose range`)
}
verifyEffect(catalogue.effects.flowing_smoke, 1800, 2200, 35, true)
verifyEffect(catalogue.effects.hob_flames, 190, 250, 30)
verifyEffect(catalogue.effects.warning_light_flicker, 0, 600, 4)
assert.equal(catalogue.effects.flowing_smoke.connectedPlume, true)
assert.equal(catalogue.effects.flowing_smoke.discreteBubblePuffs, false)
assert.deepEqual(catalogue.effects.hob_flames.anchors, [[358, 142], [394, 142]])
assert.deepEqual(catalogue.effects.warning_light_flicker.redIndicatorAnchor, [370, 155])
const warning = png(path.join(rawDir, catalogue.effects.warning_light_flicker.file))
let warningFrames = 0; let cavityFrames = 0
for (let frame = 0; frame < 40; frame++) {
  if (alpha(warning, frame * 120 + 52, 81)) warningFrames++
  if (alpha(warning, frame * 120 + 60, 100)) cavityFrames++
}
assert.equal(warningFrames, 21, 'angry red indicator timing changed')
assert.equal(cavityFrames, 5, 'internal cavity flicker timing changed')

const builder = fs.readFileSync(builderFile, 'utf8')
const smokeFunction = builder.match(/def smoke_frame[\s\S]*?\ndef flame_cluster/)[0]
assert.doesNotMatch(smokeFunction, /ellipse/, 'smoke builder regressed to bubble primitives')
assert.deepEqual(catalogue.sfxCues, ['kitchen_oven_on_fan_loop', 'kitchen_oven_broken_smoke_hiss_loop', 'kitchen_oven_hob_flame_loop', 'kitchen_oven_broken_warning_light_angry_blink_loop'])

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /original 108 × 120 px review cell/)
assert.match(page, /original exact 84 × 77 px opaque footprint/)
assert.match(page, /approved hob and sea-glass surround are preserved byte-for-byte/i)
assert.match(page, /smoke rises as one connected curling plume, not discrete bubbles/i)
assert.match(page, /exact 772 × 224 game pixels/)
assert.match(page, /Promise\.all\(unique\.map\(preload\)\)/)
assert.equal((page.match(/data-strip data-frames="40" data-fps="4"/g) || []).length, 6)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-oven-states-v41'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 11)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V41 verified: exact V21 108x120 cell/84x77 footprint, byte-identical approved hob, approved palette, exact room placement, and isolated connected smoke/flame/warning FX')
