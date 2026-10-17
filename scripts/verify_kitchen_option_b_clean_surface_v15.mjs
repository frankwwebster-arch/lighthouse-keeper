import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-option-b-clean-surface-2026-10-17-v15')
const draft = path.join(root, 'art/drafts/kitchen-option-b-clean-surface-2026-10-17-v15')
const v5raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const v6raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-option-b')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_option_b_clean_surface_v15_recipe.json'), 'utf8'))
const optionB = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_countertop_option_b_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const pageFile = path.join(root, 'public/keeper-review/kitchen-option-b-clean-surface-v15/index.html')
const page = fs.readFileSync(pageFile, 'utf8')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-option-b-clean-surface-v15.json')
const png = file => PNG.sync.read(fs.readFileSync(file))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rgba = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, ax, ay, b, bx, by) => rgba(a, ax, ay).every((value, index) => value === rgba(b, bx, by)[index])
const treeSha = directory => { const files=[]; const visit=current=>fs.readdirSync(current,{withFileTypes:true}).forEach(entry=>{const absolute=path.join(current,entry.name);if(entry.isDirectory())visit(absolute);else if(entry.isFile())files.push(absolute)});visit(directory);const digest=crypto.createHash('sha256');for(const file of files.sort()){digest.update(path.relative(directory,file).split(path.sep).join('/'));digest.update('\0');digest.update(fs.readFileSync(file));digest.update('\0')}return digest.digest('hex') }

assert.equal(recipe.id, 'kitchen-option-b-clean-surface-v15')
assert.equal(recipe.visualAuthority, 'kitchen-basic-assets-v5')
assert.equal(recipe.geometryAuthority, 'kitchen-countertop-option-b-v1')
assert.equal(recipe.regressionBoundary, 'v5-to-v6')
assert.equal(recipe.surfaceGate.topRevealPx, 6)
assert.equal(recipe.surfaceGate.fasciaPx, 8)
assert.equal(recipe.surfaceGate.ordinaryWidthPx, 80)
assert.equal(recipe.runtimeWiring, false)
assert.equal(catalogue.version, 15)
assert.equal(register.v5TreeSha256, treeSha(v5raw), 'immutable V5 authority tree changed')
assert.equal(register.v6TreeSha256, treeSha(v6raw), 'immutable V6 negative-control tree changed')
assert.equal(register.runtimeSpriteManifestSha256, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.animationWorkbenchFinalStateSha256, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)

const failures = {}
for (const [stem, stateMap] of Object.entries(catalogue.states)) {
  const construction = optionB.compatibleUnits[stem]
  const [applianceLeft, applianceRight] = recipe.units[stem].applianceXPxInclusive
  const rearY = construction.frontYPx - recipe.surfaceGate.topRevealPx
  const bottomY = construction.frontYPx + recipe.surfaceGate.fasciaPx - 1
  const template = png(path.join(root, catalogue.templates[stem].png))
  assert.equal(template.width, 84)
  assert.equal(template.height, stateMap.standard.meta.h * 4)
  for (let x = 2; x <= 81; x += 1) {
    assert.deepEqual(rgba(template, x, rearY), optionB.paletteRgba.ink, `${stem} rear edge is not continuous at x=${x}`)
    assert.deepEqual(rgba(template, x, construction.frontYPx - 1), optionB.paletteRgba.ink, `${stem} front edge is not continuous at x=${x}`)
    assert.deepEqual(rgba(template, x, bottomY), optionB.paletteRgba.ink, `${stem} fascia bottom is not continuous at x=${x}`)
    for (let y = rearY; y <= bottomY; y += 1) assert.ok(rgba(template, x, y)[3] > 0, `${stem} canonical surface has a transparent chip at ${x},${y}`)
  }
  for (const [state, record] of Object.entries(stateMap)) {
    const candidate = png(path.join(root, record.png))
    const authority = png(path.join(root, record.sourcePng))
    const frameWidth = record.meta.w * 4
    assert.equal(candidate.width, authority.width)
    assert.equal(candidate.height, authority.height)
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      const frameX = frame * frameWidth
      for (let y = 0; y < candidate.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
        const inMask = x >= construction.maskPx[0] && x < construction.maskPx[2] && y >= construction.maskPx[1] && y < construction.maskPx[3]
        if (!inMask) assert.ok(same(candidate, frameX + x, y, authority, frameX + x, y), `${stem}/${state}/f${frame + 1} changed a V5 pixel outside the countertop band at ${x},${y}`)
      }
      const wings = [[2, applianceLeft - 1], [applianceRight + 1, 81]]
      for (const [left, right] of wings) for (let y = rearY; y <= bottomY; y += 1) for (let x = left; x <= right; x += 1) {
        assert.ok(same(candidate, frameX + x, y, template, x, y), `${stem}/${state}/f${frame + 1} breaks the canonical surface wing at ${x},${y}`)
      }
    }
  }
  const v6 = png(path.join(v6raw, `${stem}_standard_f1.png`))
  let mismatch = 0
  for (const [left, right] of [[2, applianceLeft - 1], [applianceRight + 1, 81]]) for (let y = rearY; y <= bottomY; y += 1) for (let x = left; x <= right; x += 1) {
    if (!same(v6, x, y, template, x, y)) mismatch += 1
  }
  assert.ok(mismatch > 0, `${stem} V6 negative control unexpectedly passes; regression sensitivity lost`)
  failures[stem] = mismatch
}

for (const record of Object.values(catalogue.sinkOverlays)) {
  assert.equal(record.byteIdentical, true)
  assert.equal(record.sourceSha256, record.copySha256)
  assert.deepEqual(fs.readFileSync(path.join(root, record.sourcePng)), fs.readFileSync(path.join(root, record.png)), 'sink overlay must stay byte-identical to V5')
}

const room = png(path.join(root, catalogue.room.png))
assert.equal(room.width, 193 * 4)
assert.equal(room.height, 56 * 4)
assert.match(page, /required V6 perspective change remains/)
assert.match(page, /V6 must fail the same gate/)
assert.match(page, /Promise\.all\(unique\.map/)
assert.match(page, /i\.decode/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_OPTION_B_CLEAN_SURFACE_V15_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_OPTION_B_CLEAN_SURFACE_V15_2026-10-17.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V15 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-option-b-clean-surface-v15')
assert.equal(archive.page.sha256, sha(pageFile))
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-option-b-clean-surface-v15/assets')), false, 'public V15 binaries must be archived')
for (const output of register.outputs) { const absolute=path.join(root,output.path); if(fs.existsSync(absolute))assert.equal(sha(absolute),output.sha256,`registered output changed: ${output.path}`);else{const route=output.path.startsWith('public/')?`/${output.path.slice(7)}`:null;assert.ok(route&&archive.entries[route],`registered output missing: ${output.path}`);assert.equal(archive.entries[route].sha256,output.sha256,`archived output hash mismatch: ${output.path}`)} }
console.log(JSON.stringify({set:recipe.id,v5QualityOutsideBand:true,optionBTopRevealPx:6,optionBFasciaPx:8,v6RequiredFailurePixels:failures,candidateStates:Object.fromEntries(Object.entries(catalogue.states).map(([stem,states])=>[stem,Object.fromEntries(Object.entries(states).map(([state,record])=>[state,record.meta.frames]))])),runtimeChanged:false,status:'verified'},null,2))
