import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-water-effects-2026-10-19-v14')
const draft = path.join(root, 'art/drafts/kitchen-sink-water-effects-2026-10-19-v14')
const review = path.join(root, 'public/keeper-review/kitchen-sink-water-effects-v14')
const authority = path.join(root, 'art/raw/kitchen-sink-cabinet-2026-10-19-v13/sink-cabinet-standard.png')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))

assert.equal(catalogue.set, 'kitchen-sink-water-effects-2026-10-19-v14')
assert.equal(catalogue.status, 'sink-water-effects-awaiting-visual-review')
assert.equal(catalogue.staticAuthority.sha256, sha(authority))
assert.equal(catalogue.staticAuthority.tapAndBasinChanged, false)
assert.equal(catalogue.boundaries.effectPixelsOnly, true)
assert.deepEqual(catalogue.playback.speedMultiplierRange, [0.1, 4])
assert.equal(catalogue.playback.sourceDurationSeconds, 10)
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
  assert.deepEqual(effect.cellPixels, [92, 108])
}
assert.equal(catalogue.effects.onWater.origin, 'tap-outlet')
assert.equal(catalogue.effects.brokenWater.origin, 'inside-basin')
assert.equal(catalogue.effects.onWater.sfxCue, 'kitchen_sink_water_gentle_loop')
assert.equal(catalogue.effects.brokenWater.sfxCue, 'kitchen_sink_pipe_burst_loop')
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

for (const [name, mode] of [['fx-sink-on-water-f40.png', 'on'], ['fx-sink-broken-basin-spouts-f40.png', 'broken']]) {
  const strip = png(path.join(raw, name))
  assert.deepEqual([strip.width, strip.height], [3680, 108])
  for (let frame = 0; frame < 40; frame++) {
    let count = 0
    for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
      const [r, g, b, a] = pixel(strip, frame * 92 + x, y)
      if (!a) continue
      count++
      assert.ok(x >= 4 && x < 88 && y >= 4 && y < 104, `${mode} frame ${frame} touches cell gutter at ${x},${y}`)
      if (mode === 'on') assert.ok(!(r > g * 1.25 && r > b * 1.25), `${mode} frame ${frame} contains copper/red non-water pixels`)
    }
    assert.ok(count >= (mode === 'on' ? 45 : 180), `${mode} frame ${frame} is unexpectedly empty`)
  }
}
assert.equal(sha(path.join(raw, 'sink-cabinet-static.png')), sha(authority), 'V14 changed the static sink authority')
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)

const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/Sink water states/, /registered beneath the tap outlet/, /spouts shooting upward from inside the basin/, /0\.1/, /max="4"/, /image\.decode\(\)/, /All animation media loaded and decoded/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-water-effects-v14.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, 8)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-water-effects-v14/assets/${name}`].sha256, expected)
console.log('Kitchen Sink Water Effects V14 verified: 40-frame outlet-flow and upward-basin-spout loops, isolated gutters, On strip has no copper pixels, unchanged V13 sink')
