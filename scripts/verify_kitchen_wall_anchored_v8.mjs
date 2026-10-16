import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-wall-anchored-2026-10-16-v8')
const draft = path.join(root, 'art/drafts/kitchen-wall-anchored-2026-10-16-v8')
const v6raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-option-b')
const v7raw = path.join(root, 'art/raw/kitchen-room-flat-cutaway-2026-10-16-v7')
const pageFile = path.join(root, 'public/keeper-review/kitchen-wall-anchored-v8/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-wall-anchored-v8.json')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_wall_anchored_v8_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
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
const samePixel = (a, ax, ay, b, bx, by) => pixel(a, ax, ay).every((value, index) => value === pixel(b, bx, by)[index])

assert.equal(recipe.id, 'kitchen-wall-anchored-v8')
assert.equal(recipe.density, 4)
assert.equal(recipe.projection.id, 'flat-cutaway-v1')
assert.equal(recipe.projection.vanishingPoint, null)
assert.equal(recipe.projection.horizontalConvergenceLp, 0)
assert.equal(recipe.projection.verticalConvergenceLp, 0)
assert.equal(recipe.wallAnchoring.rearWallFloorJunctionFromTopLp, 51)
assert.equal(recipe.wallAnchoring.backWallAssetFootLineFromTopLp, 52)
assert.equal(recipe.wallAnchoring.footBeddingIntoFloorLp, 1)
assert.equal(recipe.wallAnchoring.foregroundFloorVisibleLp, 4)
assert.deepEqual(recipe.pedalBin.maximumOpaqueBoundsLp, [10, 12])
assert.equal(recipe.fridge.countertop, 'none')
assert.equal(recipe.sinkPorthole.outerDiameterLp, 19)
assert.equal(recipe.sinkPorthole.apertureDiameterLp, 14)
assert.equal(recipe.sinkPorthole.frameAperture, 'transparent-alpha')
assert.equal(recipe.sinkPorthole.weatherPixelsBakedIntoFrame, false)
assert.deepEqual(recipe.sinkPorthole.weatherAndTimeLayers, ['day', 'sunset', 'night', 'rain'])

assert.equal(catalogue.version, 8)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.recipe, recipe.id)
assert.deepEqual(catalogue.wallAnchoring, recipe.wallAnchoring)
assert.deepEqual(catalogue.sinkPorthole, recipe.sinkPorthole)
assert.equal(register.scope, 'kitchen-surface-fridge-bin-wall-anchor-and-porthole-corrections')
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.v6Overwritten, false)
assert.equal(register.v7Overwritten, false)
assert.equal(register.recipe.sha256, sha(path.join(root, register.recipe.path)))
assert.equal(register.protectedSnapshots.kitchenV6, treeSha(v6raw))
assert.equal(register.protectedSnapshots.kitchenRoomV7, treeSha(v7raw))
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')))

const binStates = ['standard', 'full', 'overflowing']
for (const state of binStates) {
  const record = catalogue.assets.obj_bin.states[state]
  for (const bound of record.bounds) {
    assert.ok(bound.widthLp <= 10, `${state} bin exceeds 10-lp width`)
    assert.ok(bound.heightLp <= 12, `${state} bin exceeds 12-lp height`)
  }
}
assert.ok(catalogue.assets.obj_bin.largestBound.widthLp <= 10)
assert.ok(catalogue.assets.obj_bin.largestBound.heightLp <= 12)

const fridge = png(path.join(raw, 'obj_fridge_standard_f1.png'))
assert.deepEqual([fridge.width, fridge.height], [84, 84])
const oldWood = new Set(['93,48,29', '154,86,48', '211,138,70', '238,174,88'])
let brightTopPixels = 0
for (let y = 4; y <= 13; y += 1) for (let x = 4; x <= 79; x += 1) {
  const [r, g, b, a] = pixel(fridge, x, y)
  if (!a) continue
  assert.equal(oldWood.has(`${r},${g},${b}`), false, 'fridge top must contain no countertop wood')
  if (r > 235 && g > 235 && b > 225) brightTopPixels += 1
}
assert.ok(brightTopPixels > 250, 'fridge top must read as bright white enamel')

const counterSpecs = {
  obj_kettle: { front: 48, wings: [[2, 13], [69, 81]] },
  obj_toaster: { front: 36, wings: [[2, 11], [73, 81]] },
  obj_mixer: { front: 52, wings: [[2, 11], [73, 81]] },
  obj_sink: { front: 48, wings: [[2, 13], [71, 81]] },
}
for (const [stem, spec] of Object.entries(counterSpecs)) {
  const image = png(path.join(raw, `${stem}_standard_f1.png`))
  for (const [x0, x1] of spec.wings) for (let y = spec.front - 6; y < spec.front + 8; y += 1) for (let x = x0; x <= x1; x += 1) {
    assert.equal(pixel(image, x, y)[3], 255, `${stem} has a chipped/transparent countertop pixel at ${x},${y}`)
  }
}

const frame = png(path.join(raw, 'obj_sink_porthole_frame_f1.png'))
assert.deepEqual([frame.width, frame.height], [84, 224])
assert.equal(pixel(frame, 42, 58)[3], 0, 'porthole centre must remain transparent')
let minX = frame.width; let minY = frame.height; let maxX = -1; let maxY = -1
for (let y = 0; y < frame.height; y += 1) for (let x = 0; x < frame.width; x += 1) {
  if (pixel(frame, x, y)[3] === 0) continue
  minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
}
assert.deepEqual([minX, minY, maxX + 1, maxY + 1], [4, 20, 80, 96])
assert.deepEqual([maxX - minX + 1, maxY - minY + 1], [76, 76])
for (let x = 0; x < 4; x += 1) for (let y = 0; y < frame.height; y += 1) {
  assert.equal(pixel(frame, x, y)[3], 0, 'left one-lp porthole gutter')
  assert.equal(pixel(frame, frame.width - 1 - x, y)[3], 0, 'right one-lp porthole gutter')
}
const conditions = recipe.sinkPorthole.weatherAndTimeLayers.map(condition => png(path.join(raw, `obj_sink_porthole_condition_${condition}_f1.png`)))
for (const condition of conditions) assert.equal(pixel(condition, 42, 58)[3], 255, 'condition underlay must fill the aperture')
for (let index = 1; index < conditions.length; index += 1) {
  assert.notEqual(Buffer.compare(Buffer.from(conditions[0].data), Buffer.from(conditions[index].data)), 0, 'weather/time layers must be distinct')
}

for (const bay of [2, 5, 8]) {
  const placement = catalogue.movementPlacementsLp[String(bay)]
  assert.equal(placement.sinkXLp, placement.frameXLp)
  assert.equal(placement.sinkXLp, placement.weatherUnderlayXLp)
}
assert.equal(catalogue.movementPlacementsLp['5'].sinkXLp - catalogue.movementPlacementsLp['2'].sinkXLp, 63)
assert.equal(catalogue.movementPlacementsLp['8'].sinkXLp - catalogue.movementPlacementsLp['5'].sinkXLp, 63)

const room = png(path.join(raw, 'room_kitchen_9bay_day.png'))
const shell = png(path.join(v7raw, 'room_kitchen_shell_9bay.png'))
assert.deepEqual([room.width, room.height], [772, 224])
for (let y = 208; y < 224; y += 1) for (let x = 0; x < room.width; x += 1) {
  assert.ok(samePixel(room, x, y, shell, x, y), `foreground floor must remain completely clear at ${x},${y}`)
}
assert.deepEqual([png(path.join(raw, 'room_kitchen_12bay_wall_anchored_outline.png')).width, png(path.join(raw, 'room_kitchen_12bay_wall_anchored_outline.png')).height], [1024, 224])

assert.match(page, /Units anchored to the rear wall/)
assert.match(page, /Corrected assets and every state/)
assert.match(page, /Larger sink-owned porthole/)
assert.match(page, /transparent weather\/time layers/)
assert.match(page, /Move the sink/)
assert.match(page, /Promise\.all\(urls\.map/)
assert.match(page, /i\.decode/)

assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_WALL_ANCHORED_V8_RECIPE_2026-10-16.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_WALL_ANCHORED_V8_2026-10-16.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-wall-anchored-v8')
assert.equal(archive.page.sha256, sha(pageFile))
assert.ok(Object.keys(archive.entries).length >= 50, 'review set should archive the full state family and proofs')
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-wall-anchored-v8/assets')), false, 'public review binaries must be archived')

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
  set: 'kitchen-wall-anchored-v8', projection: 'flat-cutaway-v1',
  footLineLp: 52, clearForegroundFloorLp: 4,
  binMaxBoundsLp: [10, 12], fridgeCountertop: 'none',
  sinkPorthole: { outerDiameterLp: 19, transparentAperture: true, separateConditions: 4, movesWithSink: true },
  runtimeChanged: false, status: 'verified',
}, null, 2))
