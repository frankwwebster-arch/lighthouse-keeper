import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-option-b')
const draft = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v6-option-b')
const v5raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const pageFile = path.join(root, 'public/keeper-review/kitchen-basic-assets-v6-option-b/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-basic-assets-v6-option-b.json')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_countertop_option_b_recipe.json'), 'utf8'))
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
const samePixel = (a, b, x, y) => pixel(a, x, y).every((value, index) => value === pixel(b, x, y)[index])
const insideAny = (x, y, masks) => masks.some(([x0, y0, x1, y1]) => x >= x0 && x < x1 && y >= y0 && y < y1)

assert.equal(recipe.id, 'kitchen-countertop-option-b-v1')
assert.equal(recipe.status, 'selected-construction-authority')
assert.equal(recipe.construction.topRevealLp, 1.5)
assert.equal(recipe.construction.topRevealPx, 6)
assert.equal(recipe.construction.fasciaLp, 2)
assert.equal(recipe.construction.fasciaPx, 8)
assert.equal(recipe.construction.shearLp, 0)
assert.equal(recipe.construction.rearEdgeScale, 1)
assert.equal(recipe.construction.ordinaryEdgeLengthLp, 20)
assert.equal(recipe.construction.ordinarySafetyGutterLpEachSide, 0.5)
assert.equal(recipe.construction.runtimeDepthScaling, false)
assert.equal(recipe.futureAssetRules.length, 9)

assert.equal(catalogue.version, 6)
assert.equal(catalogue.variant, 'option-b')
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.density, 4)
assert.equal(catalogue.recipe, recipe.id)
assert.deepEqual(catalogue.room, {
  doorDatumLp: 4, bayLp: 21, heightLp: 56, floorBandLp: 5, footLineLp: 56,
  widthsLp: { 9: 193, 12: 256 },
})
assert.deepEqual(Object.keys(catalogue.assets), ['obj_bin', 'obj_fridge', 'obj_kettle', 'obj_toaster', 'obj_cooker', 'obj_mixer', 'obj_sink', 'obj_table', 'obj_petbowl', 'obj_cupboard'])

assert.equal(register.soleVisualBaseline, 'Kitchen Basic Assets V5')
assert.equal(register.readsFormerV6, false)
assert.deepEqual(register.selectedCalibration, { option: 'B', topRevealLp: 1.5, calibrationSet: 'kitchen-countertop-calibration-v6' })
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.recipe.sha256, sha(path.join(root, register.recipe.path)))
assert.equal(register.protectedSnapshots.kitchenV5, treeSha(v5raw))
assert.equal(register.protectedSnapshots.calibration, treeSha(path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-calibration')))
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')))

const nonCounterExact = ['obj_petbowl', 'obj_cupboard']
for (const stem of nonCounterExact) {
  for (const [state, record] of Object.entries(catalogue.assets[stem].states)) {
    assert.equal(record.v5StripSha256, record.v6StripSha256, `${stem}/${state} must remain exact V5`)
  }
}
assert.equal(catalogue.assets.obj_bin.label, 'Pedal bin')
assert.equal(catalogue.assets.obj_bin.cell[0], 21)
assert.equal(catalogue.assets.obj_bin.largestBound.widthLp, 15)
assert.equal(catalogue.assets.obj_bin.largestBound.heightLp, 15)

for (const [stem, spec] of Object.entries(recipe.compatibleUnits)) {
  const asset = catalogue.assets[stem]
  assert.equal(asset.recipeApplies, true, `${stem} recipe flag`)
  assert.equal(asset.topRevealLp, 1.5, `${stem} Option B reveal`)
  assert.equal(asset.states.standard.meta.contactDatumsLp.worktopOrTable, 19, `${stem} 19-lp contact`)
  const candidate = png(path.join(root, asset.states.standard.png))
  const v5 = png(path.join(v5raw, `${stem}_standard_f1.png`))
  assert.deepEqual([candidate.width, candidate.height], [asset.cell[0] * 4, asset.cell[1] * 4], `${stem} frame geometry`)
  const [mx0, my0, mx1, my1] = spec.maskPx
  for (let y = 0; y < candidate.height; y += 1) {
    for (let x = 0; x < candidate.width; x += 1) {
      if (x < mx0 || x >= mx1 || y < my0 || y >= my1) assert.ok(samePixel(candidate, v5, x, y), `${stem} changed outside selected top mask at ${x},${y}`)
    }
  }
  const width = spec.edgeLengthLp * 4
  const x0 = (candidate.width - width) / 2
  const x1 = x0 + width - 1
  const rearY = spec.frontYPx - 6
  for (let x = x0; x <= x1; x += 1) {
    assert.ok(pixel(candidate, x, rearY)[3] > 0, `${stem} rear edge must cover exact declared width`)
    assert.ok(pixel(candidate, x, spec.frontYPx - 1)[3] > 0, `${stem} front edge must cover exact declared width`)
  }
  for (let y = rearY; y < spec.frontYPx + 8; y += 1) {
    assert.ok(pixel(candidate, x0, y)[3] > 0, `${stem} left slab side vertical`)
    assert.ok(pixel(candidate, x1, y)[3] > 0, `${stem} right slab side vertical`)
  }
  if (stem === 'obj_table') {
    assert.equal(asset.largestBound.widthLp, 40)
    assert.equal(pixel(candidate, 0, 0)[3], 0)
    assert.equal(pixel(candidate, candidate.width - 1, 0)[3], 0)
  } else {
    assert.equal(asset.largestBound.widthLp, 20)
    for (let y = 0; y < candidate.height; y += 1) {
      assert.equal(pixel(candidate, 0, y)[3], 0, `${stem} left shared edge alpha`)
      assert.equal(pixel(candidate, candidate.width - 1, y)[3], 0, `${stem} right shared edge alpha`)
    }
  }
}

for (const stem of ['obj_fridge', 'obj_kettle', 'obj_toaster', 'obj_cooker', 'obj_mixer', 'obj_sink']) {
  const asset = catalogue.assets[stem]
  const base = png(path.join(root, asset.states.standard.png))
  for (const state of ['on', 'broken']) {
    const record = asset.states[state]
    const strip = png(path.join(root, record.png))
    const masks = record.meta.declaredChangeMasksPx
    assert.ok(record.meta.stableBaseOutsideMasks)
    assert.ok(masks.length > 0)
    const frameWidth = record.meta.w * record.meta.density
    assert.equal(frameWidth, base.width)
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      for (let y = 0; y < base.height; y += 1) {
        for (let x = 0; x < base.width; x += 1) {
          if (insideAny(x, y, masks)) continue
          const stripIndex = (y * strip.width + frame * frameWidth + x) * 4
          const baseIndex = (y * base.width + x) * 4
          for (let channel = 0; channel < 4; channel += 1) assert.equal(strip.data[stripIndex + channel], base.data[baseIndex + channel], `${stem}/${state}/f${frame + 1} moved stationary pixel ${x},${y}`)
        }
      }
    }
  }
}

for (const [stem, asset] of Object.entries(catalogue.assets)) {
  for (const [state, record] of Object.entries(asset.states)) {
    const image = png(path.join(root, record.png))
    const { w, h, frames, density } = record.meta
    assert.deepEqual([image.width, image.height], [w * density * frames, h * density], `${stem}/${state} strip geometry`)
    for (let frame = 0; frame < frames; frame += 1) {
      const left = frame * w * density
      const right = left + w * density - 1
      for (let y = 0; y < image.height; y += 1) {
        assert.equal(image.data[(y * image.width + left) * 4 + 3], 0, `${stem}/${state}/f${frame + 1} left gutter`)
        assert.equal(image.data[(y * image.width + right) * 4 + 3], 0, `${stem}/${state}/f${frame + 1} right gutter`)
      }
    }
  }
}

for (const name of ['room_kitchen_repeat_a', 'room_kitchen_repeat_b', 'room_kitchen_repeat_c', 'room_kitchen_stair_cap', 'room_kitchen_far_cap_closed', 'room_kitchen_far_cap_open', ...Array.from({ length: 7 }, (_, index) => `room_kitchen_shell_${index + 6}bay`)]) {
  assert.equal(sha(path.join(raw, `${name}.png`)), sha(path.join(v5raw, `${name}.png`)), `${name} room geometry changed`)
  assert.equal(sha(path.join(raw, `${name}.json`)), sha(path.join(v5raw, `${name}.json`)), `${name} room metadata changed`)
}
assert.deepEqual([png(path.join(raw, 'room_kitchen_9bay_composite.png')).width, png(path.join(raw, 'room_kitchen_9bay_composite.png')).height], [193 * 4, 56 * 4])
assert.deepEqual([png(path.join(raw, 'room_kitchen_12bay_outline.png')).width, png(path.join(raw, 'room_kitchen_12bay_outline.png')).height], [256 * 4, 56 * 4])

assert.match(page, /Option B selected construction/)
assert.match(page, /Every asset and state/)
assert.match(page, /Complete compatible run/)
assert.match(page, /Exact logical game scale/)
assert.match(page, /Modular room shell · 6–12 bays/)
assert.match(page, /Keeper scale beside every major asset/)
assert.match(page, /Table\/chair draw stack/)
assert.match(page, /Right-side-wall cupboard lifecycle/)
assert.match(page, /19-lp cooker check/)
assert.match(page, /Promise\.all\(urls\.map/)
assert.match(page, /i\.decode/)

assert.ok(fs.existsSync(archiveFile), 'content-addressed review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-basic-assets-v6-option-b')
assert.equal(archive.page.sha256, sha(pageFile))
assert.ok(Object.keys(archive.entries).length >= 160)
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-basic-assets-v6-option-b/assets')), false, 'public review binaries must be archived')

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
  set: 'kitchen-basic-assets-v6-option-b', assets: 10, selectedOption: 'B', topRevealLp: 1.5,
  roomWidthsLp: [193, 256], exactOneBayArtWidthLp: 20, stationaryAnimationPixelsLocked: true,
  runtimeChanged: false, status: 'verified',
}, null, 2))
