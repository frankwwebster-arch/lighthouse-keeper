import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-cabinet-extension-2026-10-19-v16')
const draft = path.join(root, 'art/drafts/kitchen-sink-cabinet-extension-2026-10-19-v16')
const review = path.join(root, 'public/keeper-review/kitchen-sink-cabinet-extension-v16')
const v11Path = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const v15 = path.join(root, 'art/raw/kitchen-sink-perspective-correction-2026-10-19-v15')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const px = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-sink-cabinet-extension-2026-10-19-v16')
assert.equal(catalogue.status, 'exact-cabinet-extension-awaiting-visual-review')
assert.equal(catalogue.construction.standaloneAsset, true)
assert.equal(catalogue.construction.overlaysAnotherCabinetAtRuntime, false)
assert.equal(catalogue.construction.structuralPixelsExactV11, true)
assert.equal(catalogue.construction.fixtureIsOnlyAmendment, true)
assert.deepEqual(catalogue.construction.structuralCropExclusive, [88, 4, 172, 78])
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.equal(sha(v11Path), '112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81')
assert.equal(catalogue.construction.structuralSourceSha256, sha(v11Path))
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const run = png(v11Path)
const bay = png(path.join(raw, 'structural-bay-exact-v11.png'))
const fixture = png(path.join(raw, 'sink-fixture-only.png'))
const sink = png(path.join(raw, 'sink-cabinet-standard.png'))
assert.deepEqual([bay.width, bay.height], [84, 74])
assert.deepEqual([sink.width, sink.height], [92, 108])
for (let y = 0; y < 74; y++) for (let x = 0; x < 84; x++) {
  assert.ok(same(px(bay, x, y), px(run, x + 88, y + 4)), `structural bay differs from exact V11 at ${x},${y}`)
}
for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
  const under = x >= 4 && x < 88 && y >= 30 && y < 104 ? px(bay, x - 4, y - 30) : [0, 0, 0, 0]
  if (!px(fixture, x, y)[3]) assert.ok(same(px(sink, x, y), under), `V11 structure changed outside fixture at ${x},${y}`)
  else {
    assert.ok(y < 40 && x >= 24 && x <= 68, `fixture escaped its declared amendment region at ${x},${y}`)
    assert.ok(px(sink, x, y)[3] > 0, `fixture disappeared from finished sink at ${x},${y}`)
  }
}
for (const name of ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']) assert.equal(sha(path.join(raw, name)), sha(path.join(raw, 'sink-cabinet-standard.png')))
assert.equal(sha(path.join(raw, 'fx-sink-on-water-f40.png')), sha(path.join(v15, 'fx-sink-on-water-f40.png')))
assert.equal(sha(path.join(raw, 'fx-sink-broken-basin-spouts-f40.png')), sha(path.join(v15, 'fx-sink-broken-basin-spouts-f40.png')))
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
  assert.equal(effect.byteIdenticalToV15, true)
}
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/literal approved V11 bay/, /completely separate asset/, /Only the inset basin and intact tap amend/, /\.decode\(\)/, /min="0\.1"/, /max="4"/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-cabinet-extension-v16.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, Object.keys(catalogue.outputs).length)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-cabinet-extension-v16/assets/${name}`].sha256, expected)
console.log('Kitchen Sink V16 verified: separate asset, literal V11 bay structure, fixture-only amendment, unchanged V15 water loops')
