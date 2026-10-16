import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10')
const draft = path.join(root, 'art/drafts/kitchen-porthole-backdrop-cutout-2026-10-17-v10')
const v9raw = path.join(root, 'art/raw/kitchen-fridge-shelf-2026-10-17-v9')
const v7raw = path.join(root, 'art/raw/kitchen-room-flat-cutaway-2026-10-16-v7')
const pageFile = path.join(root, 'public/keeper-review/kitchen-porthole-backdrop-cutout-v10/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-porthole-backdrop-cutout-v10.json')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_porthole_backdrop_cutout_v10_recipe.json'), 'utf8'))
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
const assertClearCircle = (image, cx, cy, radius, label) => {
  let checked = 0
  for (let y = cy - radius + 1; y < cy + radius; y += 1) for (let x = cx - radius + 1; x < cx + radius; x += 1) {
    const dx = x + 0.5 - cx; const dy = y + 0.5 - cy
    if ((dx * dx) + (dy * dy) > (radius - 1) ** 2) continue
    assert.equal(pixel(image, x, y)[3], 0, `${label} contains a non-transparent pixel at ${x},${y}`)
    checked += 1
  }
  assert.ok(checked > 2200, `${label} clear-circle check is unexpectedly small`)
}

assert.equal(recipe.id, 'kitchen-porthole-backdrop-cutout-v10')
assert.equal(recipe.density, 4)
assert.equal(recipe.projection.id, 'flat-cutaway-v1')
assert.equal(recipe.projection.vanishingPoint, null)
assert.deepEqual(recipe.porthole.cellLp, [21, 56])
assert.equal(recipe.porthole.outerFrameDiameterLp, 19)
assert.equal(recipe.porthole.roomWallKnockoutDiameterLp, 14)
assert.equal(recipe.porthole.apertureAlpha, 0)
assert.equal(recipe.porthole.glazingPixelsInsideAperture, false)
assert.deepEqual(recipe.porthole.illustratedConditionUnderlays, [])
assert.equal(recipe.porthole.movesWithParent, true)
assert.equal(recipe.porthole.runtimeWiring, false)

assert.equal(catalogue.version, 10)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.recipe, recipe.id)
assert.deepEqual(catalogue.porthole, recipe.porthole)
assert.equal(register.scope, 'approved-reference-family-and-true-backdrop-porthole')
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.v8Overwritten, false)
assert.equal(register.v9Overwritten, false)
assert.equal(register.v9Accepted, false)
assert.equal(register.v9UsedAsVisualBaseline, false)
assert.equal(register.illustratedConditionUnderlaysProduced, 0)
assert.equal(register.recipe.sha256, sha(path.join(root, register.recipe.path)))
assert.equal(register.protectedSnapshots.kitchenV9, treeSha(v9raw))
assert.equal(register.protectedSnapshots.kitchenRoomV7, treeSha(v7raw))
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')))

const frame = png(path.join(raw, 'obj_sink_porthole_frame_f1.png'))
assert.deepEqual([frame.width, frame.height], [84, 224])
assertClearCircle(frame, 42, 58, 28, 'frame aperture')
assert.equal(pixel(frame, 42, 58)[3], 0)

const shell = png(path.join(raw, 'room_kitchen_shell_9bay_porthole_cutout_bay_7.png'))
const baseShell = png(path.join(v7raw, 'room_kitchen_shell_9bay.png'))
assert.deepEqual([shell.width, shell.height], [772, 224])
const globalCx = 562; const globalCy = 58
assertClearCircle(shell, globalCx, globalCy, 28, 'room-wall knockout')
let shellChanges = 0
for (let y = 0; y < shell.height; y += 1) for (let x = 0; x < shell.width; x += 1) {
  if (samePixel(shell, x, y, baseShell, x, y)) continue
  shellChanges += 1
  assert.equal(pixel(shell, x, y)[3], 0, `derived shell changed a non-alpha pixel at ${x},${y}`)
  const dx = x + 0.5 - globalCx; const dy = y + 0.5 - globalCy
  assert.ok((dx * dx) + (dy * dy) <= 29 ** 2, `derived shell changed a pixel outside the aperture at ${x},${y}`)
}
assert.ok(shellChanges > 2300, 'room wall knockout removed too few pixels')

const room = png(path.join(raw, 'room_kitchen_9bay_true_backdrop_opening.png'))
assertClearCircle(room, globalCx, globalCy, 28, 'complete-room aperture')
for (let y = 208; y < 224; y += 1) for (let x = 0; x < room.width; x += 1) {
  assert.ok(samePixel(room, x, y, baseShell, x, y), `foreground floor changed at ${x},${y}`)
}

// The full slab—not just its exposed wings—must be continuously opaque in
// every state and frame. This catches the stepped/chipped V8/V9 join exactly.
const counterFront = { obj_kettle: 48, obj_toaster: 36, obj_mixer: 52, obj_sink: 48 }
for (const [stem, states] of Object.entries(catalogue.correctedCounterStates)) {
  for (const [state, record] of Object.entries(states)) {
    const strip = png(path.join(root, record.png))
    const frameWidth = record.meta.w * 4
    const y = counterFront[stem] - 2
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      for (let x = 2; x <= 81; x += 1) {
        assert.ok(pixel(strip, frame * frameWidth + x, y)[3] > 0, `${stem}/${state}/f${frame + 1} has a chipped slab pixel at x=${x}`)
      }
    }
  }
}
const fridge = png(path.join(raw, 'obj_fridge_standard_f1.png'))
assert.deepEqual([fridge.width, fridge.height], [84, 84])
assert.ok(catalogue.fridge.bound.widthLp >= 18 && catalogue.fridge.bound.heightLp >= 18, 'approved fridge must fill its under-counter cell')
assert.ok(catalogue.shelf.bound.widthLp <= 19, 'shelf must retain a one-lp safety gutter on both sides')

for (const bay of [2, 5, 8]) {
  const placement = catalogue.movementPlacementsLp[String(bay)]
  assert.equal(placement.sinkXLp, placement.frameXLp)
  assert.equal(placement.sinkXLp, placement.wallKnockoutXLp)
  const move = png(path.join(raw, `sink_porthole_cutout_move_bay_${bay}.png`))
  const cx = (4 + (bay - 1) * 21 + 10.5) * 4
  assertClearCircle(move, cx, 58, 28, `bay-${bay} complete aperture`)
}
assert.equal(catalogue.movementPlacementsLp['5'].sinkXLp - catalogue.movementPlacementsLp['2'].sinkXLp, 63)
assert.equal(catalogue.movementPlacementsLp['8'].sinkXLp - catalogue.movementPlacementsLp['5'].sinkXLp, 63)

const rawNames = fs.readdirSync(raw)
assert.equal(rawNames.some(name => /condition|day|sunset|night|rain|weather|sky|sea/i.test(name)), false, 'V10 raw outputs must contain no illustrated condition asset')
assert.doesNotMatch(page, /obj_sink_porthole_condition_/)
assert.doesNotMatch(page, /kitchen-wall-anchored-v8\/assets/)
assert.match(page, /deliberately no illustrated proxy/)
assert.match(page, /global lighthouse backdrop/)
assert.match(page, /V9 is rejected/)
assert.match(page, /Promise\.all\(urls\.map/)
assert.match(page, /i\.decode/)

assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_2026-10-17.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V10 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-porthole-backdrop-cutout-v10')
assert.equal(archive.page.sha256, sha(pageFile))
assert.ok(Object.keys(archive.entries).length >= 6, 'V10 review set must archive frame, shell, room and three moves')
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-porthole-backdrop-cutout-v10/assets')), false, 'public V10 binaries must be archived')

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
  set: recipe.id, projection: recipe.projection.id,
  frameDiameterLp: 19, alphaOpeningDiameterLp: 14,
  illustratedConditionUnderlays: 0, movementBays: [2, 5, 8],
  runtimeChanged: false, status: 'verified',
}, null, 2))
