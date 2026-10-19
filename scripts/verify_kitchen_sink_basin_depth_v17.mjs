import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-basin-depth-2026-10-19-v17')
const draft = path.join(root, 'art/drafts/kitchen-sink-basin-depth-2026-10-19-v17')
const review = path.join(root, 'public/keeper-review/kitchen-sink-basin-depth-v17')
const v11Path = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const v16 = path.join(root, 'art/raw/kitchen-sink-cabinet-extension-2026-10-19-v16')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const px = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const span = (image, y) => {
  const xs = []
  for (let x = 0; x < image.width; x++) if (px(image, x, y)[3]) xs.push(x)
  return [Math.min(...xs), Math.max(...xs), xs.length]
}
const luminance = ([r, g, b]) => 0.2126 * r + 0.7152 * g + 0.0722 * b

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-sink-basin-depth-2026-10-19-v17')
assert.equal(catalogue.status, 'inset-basin-depth-awaiting-visual-review')
assert.equal(catalogue.construction.standaloneAsset, true)
assert.equal(catalogue.construction.structuralPixelsExactV11, true)
assert.equal(catalogue.construction.frontElevationExactV11, true)
assert.equal(catalogue.construction.worktopLeftReturnPixels, 2)
assert.equal(catalogue.construction.worktopReturnOnlyAboveFrontElevation, true)
assert.equal(catalogue.construction.fixtureAndReturnAreOnlyAmendments, true)
assert.deepEqual(catalogue.construction.structuralCropExclusive, [88, 4, 172, 78])
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.deepEqual(catalogue.construction.basinPerspective, {rearRim: 'narrower', sideReturns: 'step-out-toward-player', bowl: 'shaded-recess', frontLip: 'wider-brighter'})
assert.equal(sha(v11Path), '112dfb2ed337a15fe76b3fbe41cacf5c752eea93eed79b394eccc378370f6e81')
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const run = png(v11Path)
const bay = png(path.join(raw, 'structural-bay-exact-v11.png'))
const worktopReturn = png(path.join(raw, 'worktop-left-return.png'))
const fixture = png(path.join(raw, 'sink-fixture-only.png'))
const sink = png(path.join(raw, 'sink-cabinet-standard.png'))
let returnPixelCount = 0
for (let y = 0; y < 74; y++) for (let x = 0; x < 84; x++) assert.ok(same(px(bay, x, y), px(run, x + 88, y + 4)), `V11 bay drifted at ${x},${y}`)
for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
  const under = x >= 4 && x < 88 && y >= 30 && y < 104 ? px(bay, x - 4, y - 30) : [0, 0, 0, 0]
  const returnPixel = px(worktopReturn, x, y)
  const fixturePixel = px(fixture, x, y)
  if (!returnPixel[3] && !fixturePixel[3]) assert.ok(same(px(sink, x, y), under), `V11 structure changed outside declared amendments at ${x},${y}`)
  if (returnPixel[3]) {
    returnPixelCount++
    assert.ok(x >= 2 && x <= 3 && y >= 31 && y <= 41, `worktop return escaped its two-pixel join at ${x},${y}`)
    if (!fixturePixel[3]) assert.ok(same(px(sink, x, y), returnPixel), `worktop return changed at ${x},${y}`)
  }
  if (fixturePixel[3]) assert.ok(y < 42 && x >= 18 && x <= 73, `fixture escaped its declared region at ${x},${y}`)
}
assert.equal(returnPixelCount, 20, 'worktop return must contain the exact 1/2/1-pixel stepped profile')
for (let y = 42; y < 104; y++) for (let x = 4; x < 88; x++) assert.ok(same(px(sink, x, y), px(bay, x - 4, y - 30)), `front elevation changed at ${x},${y}`)
const rear = span(fixture, 33)
const front = span(fixture, 41)
assert.ok(front[0] < rear[0] && front[1] > rear[1] && front[2] > rear[2], `basin does not widen toward player: rear=${rear}, front=${front}`)
assert.ok(luminance(px(fixture, 24, 36)) + 20 < luminance(px(fixture, 24, 41)), 'shaded bowl is not visibly darker than front lip')
for (const name of ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']) assert.equal(sha(path.join(raw, name)), sha(path.join(raw, 'sink-cabinet-standard.png')))
assert.equal(sha(path.join(raw, 'fx-sink-on-water-f40.png')), sha(path.join(v16, 'fx-sink-on-water-f40.png')))
assert.equal(sha(path.join(raw, 'fx-sink-broken-basin-spouts-f40.png')), sha(path.join(v16, 'fx-sink-broken-basin-spouts-f40.png')))
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, 40); assert.equal(effect.fps, 4); assert.equal(effect.durationSeconds, 10); assert.equal(effect.byteIdenticalToV16, true)
}
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(sha(path.join(raw, name)), expected)
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/Matching worktop return and inset basin/, /two-pixel stepped left worktop return/, /narrower rear rim/, /angled stepped sides/, /shaded recessed bowl/, /\.decode\(\)/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-basin-depth-v17.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, Object.keys(catalogue.outputs).length)
for (const [name, expected] of Object.entries(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-basin-depth-v17/assets/${name}`].sha256, expected)
console.log('Kitchen Sink V17 verified: exact V11 front, two-pixel left worktop return, perspective basin and unchanged V16 water loops')
