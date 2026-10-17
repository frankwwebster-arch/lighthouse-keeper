import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-countertop-continuity-2026-10-17-v13')
const draft = path.join(root, 'art/drafts/kitchen-countertop-continuity-2026-10-17-v13')
const v10raw = path.join(root, 'art/raw/kitchen-porthole-backdrop-cutout-2026-10-17-v10')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_countertop_continuity_v13_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const pageFile = path.join(root, 'public/keeper-review/kitchen-countertop-continuity-v13/index.html')
const page = fs.readFileSync(pageFile, 'utf8')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-countertop-continuity-v13.json')
const png = file => PNG.sync.read(fs.readFileSync(file))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const pixel = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const same = (a, ax, ay, b, bx, by) => pixel(a, ax, ay).every((value, index) => value === pixel(b, bx, by)[index])
const treeSha = directory => {
  const files = []
  const visit = current => fs.readdirSync(current, { withFileTypes: true }).forEach(entry => {
    const absolute = path.join(current, entry.name)
    if (entry.isDirectory()) visit(absolute); else if (entry.isFile()) files.push(absolute)
  })
  visit(directory)
  const digest = crypto.createHash('sha256')
  for (const file of files.sort()) { digest.update(path.relative(directory, file).split(path.sep).join('/')); digest.update('\0'); digest.update(fs.readFileSync(file)); digest.update('\0') }
  return digest.digest('hex')
}

assert.equal(recipe.id, 'kitchen-countertop-continuity-v13')
assert.equal(recipe.slab.heightPx, 14)
assert.deepEqual(recipe.slab.xPxInclusive, [2, 81])
assert.equal(recipe.runtimeWiring, false)
assert.equal(catalogue.version, 13)
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.v10TreeSha256, treeSha(v10raw), 'immutable V10 negative-control tree changed')
assert.equal(register.runtimeSpriteManifestSha256, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.animationWorkbenchFinalStateSha256, sha(path.join(root, 'data/keeper_animation_workbench.json')))

const v10Name = { obj_kettle: 'kettle', obj_toaster: 'toaster', obj_mixer: 'mixer', obj_sink: 'sink' }
for (const [stem, stateMap] of Object.entries(catalogue.states)) {
  const spec = recipe.units[stem]
  const template = png(path.join(root, catalogue.templates[stem].png))
  const [left, right] = recipe.slab.xPxInclusive
  const allowed = spec.intentionalOcclusionXPxInclusive
  let v10StandardMismatch = 0
  for (const [state, record] of Object.entries(stateMap)) {
    const image = png(path.join(root, record.png))
    const frameWidth = record.meta.w * recipe.density
    assert.equal(image.width, frameWidth * record.meta.frames)
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      for (let y = spec.frontYPx + recipe.slab.topOffsetPx; y <= spec.frontYPx + recipe.slab.bottomOffsetPx; y += 1) {
        for (let x = left; x <= right; x += 1) {
          assert.ok(pixel(image, frame * frameWidth + x, y)[3] > 0, `${stem}/${state}/f${frame + 1} has a transparent countertop pixel at ${x},${y}`)
          if (allowed && x >= allowed[0] && x <= allowed[1]) continue
          assert.ok(same(image, frame * frameWidth + x, y, template, x, y), `${stem}/${state}/f${frame + 1} overwrites canonical countertop RGBA at ${x},${y}`)
        }
      }
    }
    if (state === 'standard') {
      const old = png(path.join(v10raw, `${v10Name[stem]}_standard.png`))
      for (let y = spec.frontYPx + recipe.slab.topOffsetPx; y <= spec.frontYPx + recipe.slab.bottomOffsetPx; y += 1) for (let x = left; x <= right; x += 1) {
        if (allowed && x >= allowed[0] && x <= allowed[1]) continue
        if (!same(old, x, y, template, x, y)) v10StandardMismatch += 1
      }
    }
  }
  assert.equal(v10StandardMismatch, catalogue.v10NegativeControlStandardMismatchCounts[stem])
  assert.ok(v10StandardMismatch > 0, `${stem} V10 negative control unexpectedly passes; test sensitivity lost`)
}

assert.deepEqual(catalogue.v10NegativeControlStandardMismatchCounts, {
  obj_kettle: 148,
  obj_toaster: 111,
  obj_mixer: 167,
  obj_sink: 248,
})
assert.match(page, /complete 80 × 14-pixel Option-B slab/)
assert.match(page, /V10 as a negative control/)
assert.match(page, /Promise\.all\(unique\.map/)
assert.match(page, /i\.decode/)
assert.match(page, /npm test/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_COUNTERTOP_CONTINUITY_V13_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_COUNTERTOP_CONTINUITY_V13_2026-10-17.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V13 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-countertop-continuity-v13')
assert.equal(archive.page.sha256, sha(pageFile))
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-countertop-continuity-v13/assets')), false, 'public V13 binaries must be archived')
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
  set: recipe.id,
  slabPixelsCheckedPerFrame: 80 * 14,
  v10NegativeControlFailures: catalogue.v10NegativeControlStandardMismatchCounts,
  candidateStates: Object.fromEntries(Object.entries(catalogue.states).map(([stem, states]) => [stem, Object.fromEntries(Object.entries(states).map(([state, record]) => [state, record.meta.frames]))])),
  runtimeChanged: false,
  status: 'verified',
}, null, 2))
