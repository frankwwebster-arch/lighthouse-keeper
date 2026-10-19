import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-layout-plan-2026-10-19-v12')
const draft = path.join(root, 'art/drafts/kitchen-layout-plan-2026-10-19-v12')
const review = path.join(root, 'public/keeper-review/kitchen-layout-plan-v12')
const cabinetPath = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const backgroundPath = path.join(root, 'art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const over = (under, top) => {
  const ta = top[3] / 255; const ua = under[3] / 255; const oa = ta + ua * (1 - ta)
  if (!oa) return [0, 0, 0, 0]
  return [0, 1, 2].map(index => Math.round((top[index] * ta + under[index] * ua * (1 - ta)) / oa)).concat(Math.round(oa * 255))
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-layout-plan-2026-10-19-v12')
assert.equal(catalogue.status, 'geometry-only-awaiting-visual-review')
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.equal(catalogue.authority.approvedCabinetCellSha256, sha(cabinetPath))
assert.equal(catalogue.authority.backgroundSha256, sha(backgroundPath))
assert.deepEqual(catalogue.geometry.cabinetBodyPlacements, [[168, 134], [420, 134]])
assert.deepEqual(catalogue.geometry.fridgeBoundsExclusive, [84, 140, 168, 218])
assert.deepEqual(catalogue.geometry.ovenHobBoundsExclusive, [336, 131, 420, 208])
assert.deepEqual(catalogue.geometry.sinkOverlayRegistration, [504, 118, 588, 151])
assert.deepEqual(catalogue.geometry.tableChairBoundsExclusive, [680, 148, 764, 222])
assert.deepEqual(catalogue.geometry.interactionAnchors, [[126, 218], [210, 218], [294, 218], [378, 218], [462, 218], [546, 218]])
assert.equal(catalogue.geometry.worktopTopY, 134)
assert.equal(catalogue.geometry.walkingDatumY, 218)
assert.equal(catalogue.boundaries.newApplianceArt, false)
assert.equal(catalogue.boundaries.sinkConsumesExtraBay, false)
assert.equal(catalogue.boundaries.standaloneMeansIndependentSprite, true)
assert.equal(catalogue.boundaries.finalChanged, false)
assert.equal(catalogue.boundaries.runtimeChanged, false)
assert.equal(register.status, 'reversible-unapproved-unpromoted')
for (const [relative, expected] of Object.entries(register.files)) {
  assert.ok(fs.existsSync(path.join(root, relative)), `registered file missing: ${relative}`)
  assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)
}

const clean = png(path.join(raw, 'kitchen-layout-clean.png'))
const background = png(backgroundPath)
const cabinet = png(cabinetPath)
assert.deepEqual([clean.width, clean.height], [772, 224])
assert.deepEqual([background.width, background.height], [772, 224])
assert.deepEqual([cabinet.width, cabinet.height], [176, 82])
const placements = [[164, 130], [416, 130]]
for (let y = 0; y < clean.height; y++) for (let x = 0; x < clean.width; x++) {
  let expected = pixel(background, x, y)
  for (const [px, py] of placements) if (x >= px && x < px + 176 && y >= py && y < py + 82) expected = over(expected, pixel(cabinet, x - px, y - py))
  assert.ok(same(expected, pixel(clean, x, y)), `clean room changed outside exact cabinet composites at ${x},${y}`)
}

for (const name of ['kitchen-layout-clean.png', 'kitchen-layout-envelope-proof.png', 'kitchen-layout-anchor-proof.png']) {
  const image = png(path.join(raw, name))
  assert.deepEqual([image.width, image.height], [772, 224])
  assert.equal(catalogue.outputs[name].sha256, sha(path.join(raw, name)))
}
const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/geometry-only room proof/, /Exact approved V11 cabinets/, /No new appliance art/, /84 × 78 at x=84, y=140/, /84 × 77 at x=336, y=131/, /Independent overlay registered to final cabinet bay/, /img\.decode\(\)/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-layout-plan-v12.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, 3)
for (const name of Object.keys(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-layout-plan-v12/assets/${name}`].sha256, catalogue.outputs[name].sha256)

console.log('Kitchen Layout Plan V12 verified: exact approved V11 cabinet reuse, preserved appliance envelopes, sink overlay registration, and unchanged six interaction anchors')
