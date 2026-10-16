import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-room-flat-cutaway-2026-10-16-v7')
const draft = path.join(root, 'art/drafts/kitchen-room-flat-cutaway-2026-10-16-v7')
const v6raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-option-b')
const pageFile = path.join(root, 'public/keeper-review/kitchen-room-flat-cutaway-v7/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-room-flat-cutaway-v7.json')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_flat_cutaway_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'room-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const page = fs.readFileSync(pageFile, 'utf8')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))

const treeSha = directory => {
  const files = []
  const visit = current => {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const absolute = path.join(current, entry.name)
      if (entry.isDirectory()) visit(absolute)
      else if (entry.isFile()) files.push(absolute)
    }
  }
  visit(directory)
  const digest = crypto.createHash('sha256')
  for (const file of files.sort()) {
    digest.update(path.relative(directory, file).split(path.sep).join('/'))
    digest.update('\0')
    digest.update(fs.readFileSync(file))
    digest.update('\0')
  }
  return digest.digest('hex')
}

const pixel = (image, x, y) => {
  const index = (y * image.width + x) * 4
  return image.data.subarray(index, index + 4)
}
const equalPixel = (a, ax, ay, b, bx, by) => pixel(a, ax, ay).every((value, index) => value === pixel(b, bx, by)[index])
const pasteOpaque = (target, source, dx, dy, sx = 0, sy = 0, sw = source.width, sh = source.height) => {
  for (let y = 0; y < sh; y += 1) {
    for (let x = 0; x < sw; x += 1) {
      const si = ((sy + y) * source.width + sx + x) * 4
      const ti = ((dy + y) * target.width + dx + x) * 4
      assert.equal(source.data[si + 3], 255, 'room modules must be opaque')
      for (let c = 0; c < 4; c += 1) target.data[ti + c] = source.data[si + c]
    }
  }
}
const overlayBinary = (target, source, dx, dy) => {
  for (let y = 0; y < source.height; y += 1) {
    for (let x = 0; x < source.width; x += 1) {
      const si = (y * source.width + x) * 4
      const alpha = source.data[si + 3]
      assert.ok(alpha === 0 || alpha === 255, 'movable group alpha must be binary')
      if (alpha === 0) continue
      const ti = ((dy + y) * target.width + dx + x) * 4
      for (let c = 0; c < 4; c += 1) target.data[ti + c] = source.data[si + c]
    }
  }
}
const sameBytes = (a, b, message) => assert.equal(Buffer.compare(Buffer.from(a.data), Buffer.from(b.data)), 0, message)

assert.equal(recipe.id, 'kitchen-room-flat-cutaway-v1')
assert.equal(recipe.density, 4)
assert.equal(recipe.projection.id, 'flat-cutaway-v1')
assert.equal(recipe.projection.vanishingPoint, null)
assert.equal(recipe.projection.horizontalConvergenceLp, 0)
assert.equal(recipe.projection.verticalConvergenceLp, 0)
assert.equal(recipe.projection.runtimeDepthScaling, false)
assert.equal(recipe.canvas.heightLp, 56)
assert.equal(recipe.canvas.doorDatumLp, 4)
assert.equal(recipe.canvas.bayWidthLp, 21)
assert.deepEqual(recipe.canvas.supportedBayCounts, [6, 7, 8, 9, 10, 11, 12])
assert.deepEqual(recipe.horizontalZones.floorBand, { topLp: 51, heightLp: 5 })
assert.equal(recipe.floor.diagonalOrConvergingLines, false)
assert.equal(recipe.floor.frontLip, false)
assert.equal(recipe.modularPieces.stairCap.assemblyContributionLp, 4)
assert.deepEqual(recipe.modularPieces.stairCap.assemblyCropLp, [42, 0, 46, 56])
assert.equal(recipe.modularPieces.repeat.assemblyContributionLp, 21)
assert.equal(recipe.modularPieces.farCap.assemblyContributionLp, 0)
assert.equal(recipe.modularPieces.farCap.cupboardHingeXLp, 37)

assert.equal(recipe.sinkPorthole.parentAsset, 'obj_sink')
assert.deepEqual(recipe.sinkPorthole.cellLp, [21, 56])
assert.deepEqual(recipe.sinkPorthole.centreLpFromCellTop, [10.5, 18.5])
assert.equal(recipe.sinkPorthole.centreHeightAboveFloorLp, 37.5)
assert.equal(recipe.sinkPorthole.outerDiameterLp, 15)
assert.equal(recipe.sinkPorthole.glazingDiameterLp, 11)
assert.equal(recipe.sinkPorthole.safetyGutterLpEachSide, 3)
assert.equal(recipe.sinkPorthole.movesWithParent, true)
assert.equal(recipe.sinkPorthole.translationRule, 'childDeltaLp == parentDeltaLp')

assert.equal(catalogue.version, 7)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.recipe, recipe.id)
assert.equal(register.scope, 'kitchen-room-and-sink-porthole-only')
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.v6FurnitureChanged, false)
assert.equal(register.recipe.sha256, sha(path.join(root, register.recipe.path)))
assert.equal(register.protectedSnapshots.kitchenV6, treeSha(v6raw))
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')))

const repeats = ['a', 'b', 'c'].map(letter => png(path.join(raw, `room_kitchen_repeat_${letter}.png`)))
for (const repeat of repeats) {
  assert.deepEqual([repeat.width, repeat.height], [84, 224])
  for (let y = 0; y < repeat.height; y += 1) assert.ok(equalPixel(repeat, 0, y, repeat, repeat.width - 1, y), `repeat edge mismatch at y=${y}`)
  for (let y = 204; y < 224; y += 1) {
    for (let x = 0; x < repeat.width; x += 1) {
      const value = pixel(repeat, x, y)
      assert.equal(value[3], 255, 'floor band must remain opaque')
    }
  }
}
for (const left of repeats) for (const right of repeats) for (let y = 0; y < 224; y += 1) {
  assert.ok(equalPixel(left, left.width - 1, y, right, 0, y), `repeat pair seam mismatch at y=${y}`)
}

const stair = png(path.join(raw, 'room_kitchen_stair_cap.png'))
const far = png(path.join(raw, 'room_kitchen_far_cap_closed.png'))
assert.deepEqual([stair.width, stair.height], [184, 224])
assert.deepEqual([far.width, far.height], [152, 224])

for (const bays of recipe.canvas.supportedBayCounts) {
  const shell = png(path.join(raw, `room_kitchen_shell_${bays}bay.png`))
  assert.deepEqual([shell.width, shell.height], [(4 + 21 * bays) * 4, 224], `${bays}-bay shell geometry`)
  const expected = new PNG({ width: shell.width, height: shell.height })
  pasteOpaque(expected, stair, 0, 0, 168, 0, 16, 224)
  for (let index = 0; index < bays; index += 1) pasteOpaque(expected, repeats[index % 3], 16 + index * 84, 0)
  pasteOpaque(expected, far, shell.width - far.width, 0)
  sameBytes(shell, expected, `${bays}-bay shell must equal exact module assembly`)
}

const porthole = png(path.join(raw, 'obj_sink_porthole_standard_f1.png'))
assert.deepEqual([porthole.width, porthole.height], [84, 224])
let minX = porthole.width; let minY = porthole.height; let maxX = -1; let maxY = -1
for (let y = 0; y < porthole.height; y += 1) for (let x = 0; x < porthole.width; x += 1) {
  if (pixel(porthole, x, y)[3] === 0) continue
  minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
}
assert.deepEqual([minX, minY, maxX + 1, maxY + 1], [12, 44, 72, 104])
assert.deepEqual([maxX - minX + 1, maxY - minY + 1], [60, 60])
for (let y = 0; y < porthole.height; y += 1) for (let x = 0; x < 12; x += 1) {
  assert.equal(pixel(porthole, x, y)[3], 0, 'porthole left 3-lp gutter')
  assert.equal(pixel(porthole, porthole.width - 1 - x, y)[3], 0, 'porthole right 3-lp gutter')
}

const sink = png(path.join(v6raw, 'obj_sink_standard_f1.png'))
const attached = png(path.join(raw, 'obj_sink_with_porthole_review.png'))
assert.deepEqual([attached.width, attached.height], [84, 224])
for (let y = 0; y < attached.height; y += 1) for (let x = 0; x < attached.width; x += 1) {
  const sinkY = y - (attached.height - sink.height)
  const sinkOpaque = sinkY >= 0 && pixel(sink, x, sinkY)[3] === 255
  const expected = sinkOpaque ? pixel(sink, x, sinkY) : pixel(porthole, x, y)
  assert.ok(pixel(attached, x, y).every((value, index) => value === expected[index]), `attached pair mismatch at ${x},${y}`)
}

for (const bay of [2, 5, 8]) {
  assert.equal(catalogue.movementPlacementsLp[String(bay)].sinkXLp, catalogue.movementPlacementsLp[String(bay)].portholeXLp)
  const proof = png(path.join(raw, `sink_porthole_move_bay_${bay}.png`))
  const expected = png(path.join(raw, 'room_kitchen_shell_9bay.png'))
  overlayBinary(expected, attached, (4 + (bay - 1) * 21) * 4, 0)
  sameBytes(proof, expected, `sink/porthole bay ${bay} must translate as one exact group`)
}
assert.equal(catalogue.movementPlacementsLp['5'].sinkXLp - catalogue.movementPlacementsLp['2'].sinkXLp, 63)
assert.equal(catalogue.movementPlacementsLp['8'].sinkXLp - catalogue.movementPlacementsLp['5'].sinkXLp, 63)

assert.deepEqual([png(path.join(raw, 'room_kitchen_9bay_composite.png')).width, png(path.join(raw, 'room_kitchen_9bay_composite.png')).height], [772, 224])
assert.deepEqual([png(path.join(raw, 'room_kitchen_12bay_outline.png')).width, png(path.join(raw, 'room_kitchen_12bay_outline.png')).height], [1024, 224])

assert.match(page, /Locked room recipe/)
assert.match(page, /Previous shell beside room redraw/)
assert.match(page, /Modular pieces/)
assert.match(page, /Exact shell assembly · 6–12 bays/)
assert.match(page, /Sink-owned porthole/)
assert.match(page, /Move the sink · window follows/)
assert.match(page, /9-bay starting kitchen/)
assert.match(page, /12-bay reservation/)
assert.match(page, /Promise\.all\(urls\.map/)
assert.match(page, /i\.decode/)

assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_ROOM_FLAT_CUTAWAY_RECIPE_2026-10-16.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_ROOM_FLAT_CUTAWAY_V7_2026-10-16.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-room-flat-cutaway-v7')
assert.equal(archive.page.sha256, sha(pageFile))
assert.equal(Object.keys(archive.entries).length, 21)
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-room-flat-cutaway-v7/assets')), false, 'public review binaries must be archived')

for (const output of register.outputs) {
  const absolute = path.join(root, output.path)
  if (fs.existsSync(absolute)) assert.equal(sha(absolute), output.sha256, `registered output changed: ${output.path}`)
  else {
    const route = output.path.startsWith('public/') ? `/${output.path.slice('public/'.length)}` : null
    assert.ok(route && archive.entries[route], `registered output missing: ${output.path}`)
    assert.equal(archive.entries[route].sha256, output.sha256, `archived output hash mismatch: ${output.path}`)
  }
}

console.log(JSON.stringify({
  set: 'kitchen-room-flat-cutaway-v7', shells: 7, projection: 'flat-cutaway-v1',
  horizontalConvergenceLp: 0, verticalConvergenceLp: 0, floorBandLp: 5,
  sinkPorthole: { outerDiameterLp: 15, centreHeightAboveFloorLp: 37.5, movesWithSink: true },
  v6FurnitureChanged: false, runtimeChanged: false, status: 'verified',
}, null, 2))
