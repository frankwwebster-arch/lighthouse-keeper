import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-perspective-correction-2026-10-19-v15')
const draft = path.join(root, 'art/drafts/kitchen-sink-perspective-correction-2026-10-19-v15')
const review = path.join(root, 'public/keeper-review/kitchen-sink-perspective-correction-v15')
const v14 = path.join(root, 'art/raw/kitchen-sink-water-effects-2026-10-19-v14')
const cabinet = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const bbox = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) if (pixel(image, x, y)[3]) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return [minX, minY, maxX + 1, maxY + 1]
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-sink-perspective-correction-2026-10-19-v15')
assert.equal(catalogue.status, 'sink-perspective-and-outlet-correction-awaiting-visual-review')
assert.equal(catalogue.construction.completeStandaloneOneBayUnit, true)
assert.equal(catalogue.construction.overlaysApprovedCabinet, false)
assert.equal(catalogue.construction.projection, 'straight-on-flat-cutaway-parallel')
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.deepEqual(catalogue.construction.bodyOriginInCell, [4, 30])
assert.equal(catalogue.construction.approvedCabinetAuthoritySha256, '112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81')
assert.equal(sha(cabinet), catalogue.construction.approvedCabinetAuthoritySha256)
assert.equal(catalogue.states.staticBasesByteIdentical, true)
assert.equal(catalogue.states.tapAndBasinChangedWhenBroken, false)
assert.deepEqual(catalogue.effects.onWater.translationPixels, [0, -2])
assert.equal(catalogue.effects.onWater.origin, 'tap-outlet')
assert.equal(catalogue.effects.brokenWater.byteIdenticalToV14, true)
assert.deepEqual(catalogue.playback.speedMultiplierRange, [0.1, 4])
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
}
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const states = ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']
for (const name of states) {
  const image = png(path.join(raw, name))
  assert.deepEqual([image.width, image.height], [92, 108])
  assert.deepEqual(bbox(image), [4, 6, 88, 104], `${name} lost its deterministic transparent bounds`)
}
assert.equal(new Set(states.map(name => sha(path.join(raw, name)))).size, 1, 'static state bases are not byte-identical')

const on = png(path.join(raw, 'fx-sink-on-water-f40.png'))
const oldOn = png(path.join(v14, 'fx-sink-on-water-f40.png'))
const brokenPath = path.join(raw, 'fx-sink-broken-basin-spouts-f40.png')
assert.deepEqual([on.width, on.height], [3680, 108])
assert.equal(sha(brokenPath), sha(path.join(v14, 'fx-sink-broken-basin-spouts-f40.png')), 'approved Broken water strip was not retained byte-for-byte')
for (let frame = 0; frame < 40; frame++) {
  let waterCount = 0
  for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
    const actual = pixel(on, frame * 92 + x, y)
    const expected = y + 2 < 108 ? pixel(oldOn, frame * 92 + x, y + 2) : [0, 0, 0, 0]
    assert.ok(same(actual, expected), `On water was changed rather than translated in frame ${frame} at ${x},${y}`)
    if (actual[3]) {
      waterCount++
      assert.ok(x >= 4 && x < 88 && y >= 4 && y < 104, `On frame ${frame} touches a shared cell edge`)
    }
  }
  assert.ok(waterCount >= 45, `On frame ${frame} is unexpectedly empty`)
}

const sink = png(path.join(raw, 'sink-cabinet-standard.png'))
for (let frame = 0; frame < 40; frame++) {
  let outletContact = false
  for (let y = 15; y <= 24; y++) for (let x = 50; x <= 66; x++) {
    if (!pixel(on, frame * 92 + x, y)[3]) continue
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
      if (pixel(sink, x + dx, y + dy)[3]) outletContact = true
    }
  }
  assert.equal(outletContact, true, `On frame ${frame} does not visibly meet the tap outlet`)
}

for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/V11 cabinet projection/, /On flow now begins at the tap outlet/, /Broken water animation is retained byte-for-byte/, /\.decode\(\)/, /min="0\.1"/, /max="4"/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-perspective-correction-v15.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, Object.keys(catalogue.outputs).length)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-perspective-correction-v15/assets/${name}`].sha256, expected)
console.log('Kitchen Sink V15 verified: exact V11 envelope/projection contract, On water translated to outlet, Broken strip byte-identical to V14')
