import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-option-b-silhouette-clean-2026-10-17-v16')
const draft = path.join(root, 'art/drafts/kitchen-option-b-silhouette-clean-2026-10-17-v16')
const v5raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const v15raw = path.join(root, 'art/raw/kitchen-option-b-clean-surface-2026-10-17-v15')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_option_b_silhouette_clean_v16_recipe.json'), 'utf8'))
const optionB = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_countertop_option_b_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const pageFile = path.join(root, 'public/keeper-review/kitchen-option-b-silhouette-clean-v16/index.html')
const page = fs.readFileSync(pageFile, 'utf8')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-option-b-silhouette-clean-v16.json')
const png = file => PNG.sync.read(fs.readFileSync(file))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rgba = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const samePixel = (a, b) => a.every((value, index) => value === b[index])
const same = (a, ax, ay, b, bx, by) => samePixel(rgba(a, ax, ay), rgba(b, bx, by))
const treeSha = directory => { const files=[]; const visit=current=>fs.readdirSync(current,{withFileTypes:true}).forEach(entry=>{const absolute=path.join(current,entry.name);if(entry.isDirectory())visit(absolute);else if(entry.isFile())files.push(absolute)});visit(directory);const digest=crypto.createHash('sha256');for(const file of files.sort()){digest.update(path.relative(directory,file).split(path.sep).join('/'));digest.update('\0');digest.update(fs.readFileSync(file));digest.update('\0')}return digest.digest('hex') }
const transparent = [0, 0, 0, 0]
const woodLike = ([r,g,b,a]) => Boolean(a && r > 45 && r > 1.25 * g && g > 1.10 * b && b < 120)
const allowedGold = (stem, x, y, [r,g,b,a]) => stem === 'obj_sink' && a && recipe.units[stem].goldWindowsPx.some(([x0,y0,x1,y1])=>x>=x0&&x<x1&&y>=y0&&y<y1) && r > 150 && g > 75 && b < 90

assert.equal(recipe.id, 'kitchen-option-b-silhouette-clean-v16')
assert.equal(recipe.visualAuthority, 'kitchen-basic-assets-v5')
assert.equal(recipe.geometryAuthority, 'kitchen-countertop-option-b-v1')
assert.deepEqual(recipe.rejectedControls, ['kitchen-basic-assets-v6-option-b', 'kitchen-option-b-clean-surface-v15'])
assert.equal(recipe.surfaceGate.topRevealPx, 6)
assert.equal(recipe.surfaceGate.fasciaPx, 8)
assert.equal(recipe.surfaceGate.ordinaryWidthPx, 80)
assert.equal(recipe.runtimeWiring, false)
assert.equal(catalogue.version, 16)
assert.equal(register.v5TreeSha256, treeSha(v5raw), 'immutable V5 authority tree changed')
assert.equal(register.v15TreeSha256, treeSha(v15raw), 'immutable rejected V15 tree changed')
assert.equal(register.runtimeSpriteManifestSha256, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.animationWorkbenchFinalStateSha256, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)

const rejectedV15 = {}
for (const [stem, stateMap] of Object.entries(catalogue.states)) {
  const construction = optionB.compatibleUnits[stem]
  const unit = recipe.units[stem]
  const [silhouetteLeft, silhouetteRight] = unit.silhouetteXPx
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
    const mask = png(path.join(root, record.maskPng))
    const frameWidth = record.meta.w * 4
    assert.equal(candidate.width, authority.width)
    assert.equal(candidate.height, authority.height)
    assert.equal(mask.width, candidate.width)
    assert.equal(mask.height, candidate.height)
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      const frameX = frame * frameWidth
      for (let y = 0; y < candidate.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
        const inRemoval = y >= unit.removalTopPx && y <= bottomY
        const maskAlpha = rgba(mask, frameX + x, y)[3]
        assert.ok(maskAlpha === 0 || maskAlpha === 255, `${stem}/${state}/f${frame + 1} has a non-binary mask at ${x},${y}`)
        if (!inRemoval) {
          assert.equal(maskAlpha, 0, `${stem}/${state}/f${frame + 1} masks outside the removal zone at ${x},${y}`)
          assert.ok(same(candidate, frameX + x, y, authority, frameX + x, y), `${stem}/${state}/f${frame + 1} changed a V5 pixel outside the removal zone at ${x},${y}`)
          continue
        }
        if (maskAlpha) {
          assert.ok(x >= silhouetteLeft && x < silhouetteRight, `${stem}/${state}/f${frame + 1} mask escapes the measured appliance width at ${x},${y}`)
          const sourcePixel = rgba(authority, frameX + x, y)
          assert.ok(!woodLike(sourcePixel) || allowedGold(stem, x, y, sourcePixel), `${stem}/${state}/f${frame + 1} restores inherited wood at ${x},${y}`)
          assert.ok(same(candidate, frameX + x, y, authority, frameX + x, y), `${stem}/${state}/f${frame + 1} does not preserve its masked V5 appliance pixel at ${x},${y}`)
        } else {
          const expected = y >= rearY ? rgba(template, x, y) : transparent
          assert.ok(samePixel(rgba(candidate, frameX + x, y), expected), `${stem}/${state}/f${frame + 1} breaks the canonical removal zone at ${x},${y}`)
        }
      }
    }
  }
  const correctMask = png(path.join(root, stateMap.standard.maskPng))
  const v15 = png(path.join(v15raw, `${stem}_standard_f1.png`))
  let allMismatch = 0
  let clearanceMismatch = 0
  for (let y = unit.removalTopPx; y <= bottomY; y += 1) for (let x = 0; x < 84; x += 1) {
    if (rgba(correctMask, x, y)[3]) continue
    const expected = y >= rearY ? rgba(template, x, y) : transparent
    if (!samePixel(rgba(v15, x, y), expected)) {
      allMismatch += 1
      if (y < rearY) clearanceMismatch += 1
    }
  }
  assert.ok(allMismatch > 0, `${stem} rejected V15 control unexpectedly passes; regression sensitivity lost`)
  assert.ok(clearanceMismatch > 0, `${stem} rejected V15 does not expose retained old-surface pixels above the slab`)
  rejectedV15[stem] = {allMismatch, clearanceMismatch}
}

for (const record of Object.values(catalogue.sinkOverlays)) {
  assert.equal(record.byteIdentical, true)
  assert.equal(record.sourceSha256, record.copySha256)
  assert.deepEqual(fs.readFileSync(path.join(root, record.sourcePng)), fs.readFileSync(path.join(root, record.png)), 'sink overlay must stay byte-identical to V5')
}

const room = png(path.join(root, catalogue.room.png))
assert.equal(room.width, 193 * 4)
assert.equal(room.height, 56 * 4)
assert.match(page, /V15 left rows of V5’s tapered countertop above the replacement band/)
assert.match(page, /V15 must fail this exact test/)
assert.match(page, /Promise\.all\(unique\.map/)
assert.match(page, /i\.decode/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_OPTION_B_SILHOUETTE_CLEAN_V16_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_OPTION_B_SILHOUETTE_CLEAN_V16_2026-10-17.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V16 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-option-b-silhouette-clean-v16')
assert.equal(archive.page.sha256, sha(pageFile))
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-option-b-silhouette-clean-v16/assets')), false, 'public V16 binaries must be archived')
for (const output of register.outputs) {
  const absolute = path.join(root, output.path)
  if (fs.existsSync(absolute)) assert.equal(sha(absolute), output.sha256, `registered output changed: ${output.path}`)
  else {
    const route = output.path.startsWith('public/') ? `/${output.path.slice(7)}` : null
    assert.ok(route && archive.entries[route], `registered output missing: ${output.path}`)
    assert.equal(archive.entries[route].sha256, output.sha256, `archived output hash mismatch: ${output.path}`)
  }
}
console.log(JSON.stringify({set:recipe.id,completeRemovalZone:true,v15RequiredFailurePixels:rejectedV15,candidateStates:Object.fromEntries(Object.entries(catalogue.states).map(([stem,states])=>[stem,Object.fromEntries(Object.entries(states).map(([state,record])=>[state,record.meta.frames]))])),runtimeChanged:false,status:'verified'},null,2))
