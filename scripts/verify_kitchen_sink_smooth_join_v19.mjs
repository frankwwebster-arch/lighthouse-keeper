import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-smooth-join-2026-10-19-v19')
const draft = path.join(root, 'art/drafts/kitchen-sink-smooth-join-2026-10-19-v19')
const review = path.join(root, 'public/keeper-review/kitchen-sink-smooth-join-v19')
const v11Path = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const v18 = path.join(root, 'art/raw/kitchen-sink-angled-join-2026-10-19-v18')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const px = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const span = (image, y) => {
  const xs = []
  for (let x = 0; x < image.width; x++) if (px(image, x, y)[3]) xs.push(x)
  return [Math.min(...xs), Math.max(...xs), xs.length]
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-sink-smooth-join-2026-10-19-v19')
assert.equal(catalogue.status, 'smooth-join-awaiting-visual-review')
assert.equal(catalogue.construction.frontElevationExactV11, true)
assert.equal(catalogue.construction.frontElevationStartsAtCellY, 43)
assert.equal(catalogue.construction.worktopJoinDirection, 'smooth-down-right')
assert.equal(catalogue.construction.roundedFrontLip, true)
assert.equal(catalogue.construction.basinFixtureByteIdenticalToV18, true)
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.equal(sha(v11Path), '112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81')
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const run = png(v11Path)
const bay = png(path.join(raw, 'structural-bay-exact-v11.png'))
const join = png(path.join(raw, 'worktop-smooth-join-only.png'))
const fixture = png(path.join(raw, 'sink-fixture-only.png'))
const sink = png(path.join(raw, 'sink-cabinet-standard.png'))
for (let y = 0; y < 74; y++) for (let x = 0; x < 84; x++) assert.ok(same(px(bay, x, y), px(run, x + 88, y + 4)), `V11 bay drifted at ${x},${y}`)
assert.equal(sha(path.join(raw, 'sink-fixture-only.png')), sha(path.join(v18, 'sink-fixture-only.png')))
assert.equal(sha(path.join(raw, 'v18-approved-predecessor.png')), sha(path.join(v18, 'sink-cabinet-standard.png')))

const positions = catalogue.construction.worktopBoundaryXByCellRow30To42
assert.equal(positions.length, 13)
for (let index = 1; index < positions.length; index++) {
  assert.ok(positions[index] > positions[index - 1], `worktop boundary did not progress smoothly at row ${index}`)
  assert.ok(positions[index] - positions[index - 1] < 0.75, `worktop boundary jumps too sharply at row ${index}`)
}
for (let row = 0; row < positions.length; row++) {
  const y = 30 + row
  const first = Math.floor(positions[row])
  assert.equal(span(join, y)[0], first, `smooth join starts at wrong x on y=${y}`)
  if (positions[row] % 1) {
    const alpha = px(join, first, y)[3]
    assert.ok(alpha > 0 && alpha < 255, `smooth join lacks partial-alpha coverage on y=${y}: ${alpha}`)
  }
}
assert.ok(catalogue.construction.frontLipBoundaryAlpha >= 90 && catalogue.construction.frontLipBoundaryAlpha <= 135, 'front lip is not softly rounded')
assert.ok(Math.abs(catalogue.construction.frontLipBoundaryAlpha - catalogue.construction.rightWorktopFrontLipReferenceAlpha) <= 10, 'left front lip does not match right-edge alpha finish')
for (let y = 43; y < 104; y++) for (let x = 4; x < 88; x++) assert.ok(same(px(sink, x, y), px(bay, x - 4, y - 30)), `hero front elevation changed at ${x},${y}`)
for (let x = 0; x < sink.width; x++) {
  assert.equal(px(sink, x, 0)[3], 0, `top gutter touched at x=${x}`)
  assert.equal(px(sink, x, sink.height - 1)[3], 0, `bottom gutter touched at x=${x}`)
}
for (let y = 0; y < sink.height; y++) {
  assert.equal(px(sink, 0, y)[3], 0, `left gutter touched at y=${y}`)
  assert.equal(px(sink, sink.width - 1, y)[3], 0, `right gutter touched at y=${y}`)
}
assert.deepEqual(span(fixture, 33).slice(0, 2), [20, 70])
assert.deepEqual(span(fixture, 41).slice(0, 2), [18, 73])
for (const name of ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']) assert.equal(sha(path.join(raw, name)), sha(path.join(raw, 'sink-cabinet-standard.png')))
assert.equal(sha(path.join(raw, 'fx-sink-on-water-f40.png')), sha(path.join(v18, 'fx-sink-on-water-f40.png')))
assert.equal(sha(path.join(raw, 'fx-sink-broken-basin-spouts-f40.png')), sha(path.join(v18, 'fx-sink-broken-basin-spouts-f40.png')))
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40); assert.equal(effect.fps, 4); assert.equal(effect.durationSeconds, 10); assert.equal(effect.byteIdenticalToV18, true)
}
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/Smooth angled join with rounded front lip/, /continuous antialiased down-right edge/, /softly rounded partial-alpha corner/, /V18 basin remain unchanged/, /V18 approved predecessor/, /V19 smoothing draft/, /\.decode\(\)/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-smooth-join-v19.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, Object.keys(catalogue.outputs).length)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-smooth-join-v19/assets/${name}`].sha256, expected)
console.log('Kitchen Sink V19 verified: smooth antialiased down-right join, rounded front lip, exact V11 hero front and unchanged V18 basin/effects')
