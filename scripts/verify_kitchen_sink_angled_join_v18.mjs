import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-angled-join-2026-10-19-v18')
const draft = path.join(root, 'art/drafts/kitchen-sink-angled-join-2026-10-19-v18')
const review = path.join(root, 'public/keeper-review/kitchen-sink-angled-join-v18')
const v11Path = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const v17 = path.join(root, 'art/raw/kitchen-sink-basin-depth-2026-10-19-v17')
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
assert.equal(catalogue.set, 'kitchen-sink-angled-join-2026-10-19-v18')
assert.equal(catalogue.status, 'angled-join-awaiting-visual-review')
assert.equal(catalogue.construction.frontElevationExactV11, true)
assert.equal(catalogue.construction.frontElevationStartsAtCellY, 42)
assert.equal(catalogue.construction.worktopJoinOnlyAboveFrontElevation, true)
assert.equal(catalogue.construction.worktopJoinDirection, 'down-right')
assert.deepEqual(catalogue.construction.worktopJoinOuterStartsByRow, [1, 1, 1, 2, 2, 2, 3, 3, 3])
assert.equal(catalogue.construction.worktopJoinMeetsBodyAtCellX, 4)
assert.equal(catalogue.construction.basinFixtureByteIdenticalToV17, true)
assert.equal(catalogue.construction.basinPerspective.widensTowardFront, true)
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.equal(sha(v11Path), '112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81')
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const run = png(v11Path)
const bay = png(path.join(raw, 'structural-bay-exact-v11.png'))
const join = png(path.join(raw, 'worktop-angled-join-only.png'))
const fixture = png(path.join(raw, 'sink-fixture-only.png'))
const sink = png(path.join(raw, 'sink-cabinet-standard.png'))
for (let y = 0; y < 74; y++) for (let x = 0; x < 84; x++) assert.ok(same(px(bay, x, y), px(run, x + 88, y + 4)), `V11 bay drifted at ${x},${y}`)
assert.equal(sha(path.join(raw, 'sink-fixture-only.png')), sha(path.join(v17, 'sink-fixture-only.png')))

const expectedStarts = [1, 1, 1, 2, 2, 2, 3, 3, 3]
for (let row = 0; row < expectedStarts.length; row++) {
  const actual = span(join, 30 + row)
  assert.deepEqual(actual, [expectedStarts[row], 12, 13 - expectedStarts[row]], `angled join row ${row} is wrong`)
}
for (let y = 39; y < join.height; y++) assert.equal(span(join, y)[2], 0, `angled join extends below the shallow worktop at y=${y}`)

for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
  const under = x >= 4 && x < 88 && y >= 30 && y < 104 ? px(bay, x - 4, y - 30) : [0, 0, 0, 0]
  const joinPixel = px(join, x, y)
  const fixturePixel = px(fixture, x, y)
  if (!joinPixel[3] && !fixturePixel[3]) assert.ok(same(px(sink, x, y), under), `V11 structure changed outside join/fixture at ${x},${y}`)
  if (joinPixel[3] && !fixturePixel[3]) assert.ok(same(px(sink, x, y), joinPixel), `angled join replacement changed at ${x},${y}`)
  if (joinPixel[3]) assert.ok(x >= 1 && x <= 12 && y >= 30 && y <= 38, `angled join escaped its declared worktop region at ${x},${y}`)
}
for (let y = 42; y < 104; y++) for (let x = 4; x < 88; x++) assert.ok(same(px(sink, x, y), px(bay, x - 4, y - 30)), `hero front elevation changed at ${x},${y}`)
for (let x = 0; x < sink.width; x++) {
  assert.equal(px(sink, x, 0)[3], 0, `top gutter touched at x=${x}`)
  assert.equal(px(sink, x, sink.height - 1)[3], 0, `bottom gutter touched at x=${x}`)
}
for (let y = 0; y < sink.height; y++) {
  assert.equal(px(sink, 0, y)[3], 0, `left gutter touched at y=${y}`)
  assert.equal(px(sink, sink.width - 1, y)[3], 0, `right gutter touched at y=${y}`)
}
const rear = span(fixture, 33)
const front = span(fixture, 41)
assert.deepEqual(rear.slice(0, 2), [20, 70])
assert.deepEqual(front.slice(0, 2), [18, 73])
assert.ok(front[0] < rear[0] && front[1] > rear[1], `basin sidelines do not splay toward front: rear=${rear}, front=${front}`)
for (const name of ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']) assert.equal(sha(path.join(raw, name)), sha(path.join(raw, 'sink-cabinet-standard.png')))
assert.equal(sha(path.join(raw, 'fx-sink-on-water-f40.png')), sha(path.join(v17, 'fx-sink-on-water-f40.png')))
assert.equal(sha(path.join(raw, 'fx-sink-broken-basin-spouts-f40.png')), sha(path.join(v17, 'fx-sink-broken-basin-spouts-f40.png')))
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40); assert.equal(effect.fps, 4); assert.equal(effect.durationSeconds, 10); assert.equal(effect.byteIdenticalToV17, true)
}
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/Angled worktop join and shallow inset basin/, /small down-right diagonal/, /widening slightly/, /cabinet front/, /\.decode\(\)/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-angled-join-v18.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, Object.keys(catalogue.outputs).length)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-angled-join-v18/assets/${name}`].sha256, expected)
console.log('Kitchen Sink V18 verified: one down-right worktop join, opposite basin splay, exact V11 hero front and unchanged V17 effects')
