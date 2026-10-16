import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-fridge-shelf-2026-10-17-v9')
const draft = path.join(root, 'art/drafts/kitchen-fridge-shelf-2026-10-17-v9')
const v8raw = path.join(root, 'art/raw/kitchen-wall-anchored-2026-10-16-v8')
const v7raw = path.join(root, 'art/raw/kitchen-room-flat-cutaway-2026-10-16-v7')
const pageFile = path.join(root, 'public/keeper-review/kitchen-fridge-shelf-v9/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-fridge-shelf-v9.json')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_fridge_shelf_v9_recipe.json'), 'utf8'))
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
const alphaBounds = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) {
    if (pixel(image, x, y)[3] === 0) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return [minX, minY, maxX + 1, maxY + 1]
}

assert.equal(recipe.id, 'kitchen-fridge-shelf-v9')
assert.equal(recipe.density, 4)
assert.equal(recipe.bayWidthLp, 21)
assert.equal(recipe.roomHeightLp, 56)
assert.equal(recipe.projection.id, 'flat-cutaway-v1')
assert.equal(recipe.projection.vanishingPoint, null)
assert.equal(recipe.projection.horizontalConvergenceLp, 0)
assert.equal(recipe.projection.verticalConvergenceLp, 0)
assert.deepEqual(recipe.fridge.cellLp, [21, 21])
assert.equal(recipe.fridge.bayOccupancy, 1)
assert.equal(recipe.fridge.countertop, 'none')
assert.equal(recipe.fridge.backWallFootLineFromTopLp, 52)
assert.deepEqual(recipe.fridgeShelf.cellLp, [21, 56])
assert.deepEqual(recipe.fridgeShelf.maximumOpaqueBoundsLp, [19, 17])
assert.equal(recipe.fridgeShelf.parentAsset, 'obj_fridge')
assert.equal(recipe.fridgeShelf.movesWithParent, true)
assert.equal(recipe.fridgeShelf.runtimeWiring, false)

assert.equal(catalogue.version, 9)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.recipe, recipe.id)
assert.equal(register.scope, 'dimensional-white-fridge-and-fridge-owned-wall-shelf')
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.v8Overwritten, false)
assert.equal(register.recipe.sha256, sha(path.join(root, register.recipe.path)))
assert.equal(register.protectedSnapshots.kitchenV8, treeSha(v8raw))
assert.equal(register.protectedSnapshots.kitchenRoomV7, treeSha(v7raw))
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')))

const fridge = png(path.join(raw, 'obj_fridge_standard_f1.png'))
assert.deepEqual([fridge.width, fridge.height], [84, 84])
assert.deepEqual(alphaBounds(fridge), [3, 2, 81, 84])
const oldWood = new Set(['93,48,29', '154,86,48', '211,138,70', '238,174,88'])
const neutralTones = new Set()
for (let y = 2; y <= 21; y += 1) for (let x = 3; x <= 80; x += 1) {
  const [r, g, b, a] = pixel(fridge, x, y)
  if (!a) continue
  assert.equal(oldWood.has(`${r},${g},${b}`), false, 'fridge lid contains a forbidden V6 wood colour')
}
for (let y = 0; y < fridge.height; y += 1) for (let x = 0; x < fridge.width; x += 1) {
  const [r, g, b, a] = pixel(fridge, x, y)
  if (a && Math.max(r, g, b) - Math.min(r, g, b) <= 30 && r > 130) neutralTones.add(`${r},${g},${b}`)
}
assert.ok(neutralTones.size >= 5, `fridge must retain dimensional neutral shading; found ${neutralTones.size} tones`)
assert.notEqual(sha(path.join(raw, 'obj_fridge_standard_f1.png')), sha(path.join(v8raw, 'obj_fridge_standard_f1.png')), 'V9 fridge must differ from V8')
for (const state of ['standard', 'on', 'broken']) {
  const record = catalogue.fridge.states[state]
  assert.deepEqual([record.meta.w, record.meta.h], [21, 21])
  assert.equal(record.bounds.every(bound => bound.xLp >= 0 && bound.yLp >= 0 && bound.xLp + bound.widthLp <= 21 && bound.yLp + bound.heightLp <= 21), true)
}

const shelf = png(path.join(raw, 'obj_fridge_wall_shelf_v9_f1.png'))
assert.deepEqual([shelf.width, shelf.height], [84, 224])
assert.deepEqual(alphaBounds(shelf), [4, 54, 80, 122])
for (let x = 0; x < 4; x += 1) for (let y = 0; y < shelf.height; y += 1) {
  assert.equal(pixel(shelf, x, y)[3], 0, 'left one-lp shelf gutter')
  assert.equal(pixel(shelf, shelf.width - 1 - x, y)[3], 0, 'right one-lp shelf gutter')
}
for (let y = 122; y < shelf.height; y += 1) for (let x = 0; x < shelf.width; x += 1) assert.equal(pixel(shelf, x, y)[3], 0, 'shelf must end above fridge')

for (const bay of [2, 5, 8]) {
  const placement = catalogue.movementPlacementsLp[String(bay)]
  assert.equal(placement.fridgeXLp, placement.shelfXLp)
}
assert.equal(catalogue.movementPlacementsLp['5'].fridgeXLp - catalogue.movementPlacementsLp['2'].fridgeXLp, 63)
assert.equal(catalogue.movementPlacementsLp['8'].fridgeXLp - catalogue.movementPlacementsLp['5'].fridgeXLp, 63)

const room = png(path.join(raw, 'room_kitchen_9bay_day.png'))
const shell = png(path.join(v7raw, 'room_kitchen_shell_9bay.png'))
assert.deepEqual([room.width, room.height], [772, 224])
for (let y = 208; y < 224; y += 1) for (let x = 0; x < room.width; x += 1) {
  assert.ok(samePixel(room, x, y, shell, x, y), `foreground floor changed at ${x},${y}`)
}

assert.match(page, /Fridge redraw · every state/)
assert.match(page, /Separate fridge-owned wall detail/)
assert.match(page, /Move the fridge · shelf follows exactly/)
assert.match(page, /V8 versus V9/)
assert.match(page, /Promise\.all\(urls\.map/)
assert.match(page, /i\.decode/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_FRIDGE_SHELF_V9_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_FRIDGE_SHELF_V9_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'art/source/kitchen-fridge-shelf-2026-10-17-v9/reference_study.png')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V9 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-fridge-shelf-v9')
assert.equal(archive.page.sha256, sha(pageFile))
assert.ok(Object.keys(archive.entries).length >= 25, 'V9 review set must archive every state and proof')
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-fridge-shelf-v9/assets')), false, 'public review binaries must be archived')

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
  set: 'kitchen-fridge-shelf-v9', projection: 'flat-cutaway-v1',
  fridgeCellLp: [21, 21], fridgeCountertop: 'none', neutralTones: neutralTones.size,
  shelfBoundLp: [19, 17], movementBays: [2, 5, 8], runtimeChanged: false, status: 'verified',
}, null, 2))
