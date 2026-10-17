import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-countertop-no-splashback-2026-10-17-v14')
const draft = path.join(root, 'art/drafts/kitchen-countertop-no-splashback-2026-10-17-v14')
const v13raw = path.join(root, 'art/raw/kitchen-countertop-continuity-2026-10-17-v13')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_countertop_no_splashback_v14_recipe.json'), 'utf8'))
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'asset-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const pageFile = path.join(root, 'public/keeper-review/kitchen-countertop-no-splashback-v14/index.html')
const page = fs.readFileSync(pageFile, 'utf8')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-countertop-no-splashback-v14.json')
const png = file => PNG.sync.read(fs.readFileSync(file))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rgba = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, ax, ay, b, bx, by) => rgba(a, ax, ay).every((value, index) => value === rgba(b, bx, by)[index])
const wood = new Set(['93,48,29,255', '154,86,48,255', '211,138,70,255', '238,174,88,255'])
const treeSha = directory => { const files=[]; const visit=current=>fs.readdirSync(current,{withFileTypes:true}).forEach(entry=>{const absolute=path.join(current,entry.name);if(entry.isDirectory())visit(absolute);else if(entry.isFile())files.push(absolute)});visit(directory);const digest=crypto.createHash('sha256');for(const file of files.sort()){digest.update(path.relative(directory,file).split(path.sep).join('/'));digest.update('\0');digest.update(fs.readFileSync(file));digest.update('\0')}return digest.digest('hex') }

assert.equal(recipe.id, 'kitchen-countertop-no-splashback-v14')
assert.equal(recipe.rearZone.woodPixelsAllowed, 0)
assert.equal(recipe.fascia.heightPx, 8)
assert.equal(recipe.runtimeWiring, false)
assert.equal(catalogue.version, 14)
assert.equal(register.v13TreeSha256, treeSha(v13raw), 'immutable V13 negative-control tree changed')
assert.equal(register.runtimeSpriteManifestSha256, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.animationWorkbenchFinalStateSha256, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.runtimeChanged, false); assert.equal(register.finalChanged, false); assert.equal(register.keeperChanged, false)

for (const [stem, stateMap] of Object.entries(catalogue.states)) {
  const spec = recipe.units[stem]
  const [applianceLeft, applianceRight] = spec.applianceXPxInclusive
  const fasciaTemplate = png(path.join(root, catalogue.templates[stem].png))
  let v13Violations = 0
  const old = png(path.join(v13raw, `${stem.slice(4)}_standard.png`))
  for (let y = spec.frontYPx - 6; y < spec.frontYPx; y += 1) for (let x = 0; x < old.width; x += 1) {
    const pixel = rgba(old, x, y)
    if (wood.has(pixel.join(',')) || (pixel[3] && !(x >= applianceLeft && x <= applianceRight))) v13Violations += 1
  }
  assert.equal(v13Violations, catalogue.v13NegativeControlViolationCounts[stem])
  assert.ok(v13Violations > 0, `${stem} V13 negative control unexpectedly passes; test sensitivity lost`)
  for (const [state, record] of Object.entries(stateMap)) {
    const image = png(path.join(root, record.png)); const frameWidth = record.meta.w * recipe.density
    for (let frame = 0; frame < record.meta.frames; frame += 1) {
      for (let y = spec.frontYPx - 6; y < spec.frontYPx; y += 1) for (let x = 0; x < frameWidth; x += 1) {
        const pixel = rgba(image, frame * frameWidth + x, y)
        assert.equal(wood.has(pixel.join(',')), false, `${stem}/${state}/f${frame + 1} retains rear countertop wood at ${x},${y}`)
        if (pixel[3]) assert.ok(x >= applianceLeft && x <= applianceRight, `${stem}/${state}/f${frame + 1} retains a rear ridge pixel outside the appliance at ${x},${y}`)
      }
      const allowed = spec.fasciaOcclusionXPxInclusive
      for (let y = spec.frontYPx; y <= spec.frontYPx + 7; y += 1) for (let x = 2; x <= 81; x += 1) {
        assert.ok(rgba(image, frame * frameWidth + x, y)[3] > 0, `${stem}/${state}/f${frame + 1} has a transparent fascia pixel at ${x},${y}`)
        if (allowed && x >= allowed[0] && x <= allowed[1]) continue
        assert.ok(same(image, frame * frameWidth + x, y, fasciaTemplate, x, y), `${stem}/${state}/f${frame + 1} changes the exact fascia at ${x},${y}`)
      }
    }
  }
}

assert.match(page, /stepped brown rear reveal has been removed/)
assert.match(page, /zero wood or structural ridge above the fascia/)
assert.match(page, /Promise\.all\(unique\.map/)
assert.match(page, /i\.decode/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_COUNTERTOP_NO_SPLASHBACK_V14_RECIPE_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_COUNTERTOP_NO_SPLASHBACK_V14_2026-10-17.md')))
assert.ok(fs.existsSync(archiveFile), 'content-addressed V14 review set missing')
const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
assert.equal(archive.set, 'kitchen-countertop-no-splashback-v14')
assert.equal(archive.page.sha256, sha(pageFile))
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-countertop-no-splashback-v14/assets')), false, 'public V14 binaries must be archived')
for (const output of register.outputs) { const absolute=path.join(root,output.path); if(fs.existsSync(absolute))assert.equal(sha(absolute),output.sha256,`registered output changed: ${output.path}`);else{const route=output.path.startsWith('public/')?`/${output.path.slice(7)}`:null;assert.ok(route&&archive.entries[route],`registered output missing: ${output.path}`);assert.equal(archive.entries[route].sha256,output.sha256,`archived output hash mismatch: ${output.path}`)} }
console.log(JSON.stringify({set:recipe.id,rearWoodAllowed:0,fasciaPixelsCheckedPerFrame:80*8,v13NegativeControlFailures:catalogue.v13NegativeControlViolationCounts,candidateStates:Object.fromEntries(Object.entries(catalogue.states).map(([stem,states])=>[stem,Object.fromEntries(Object.entries(states).map(([state,record])=>[state,record.meta.frames]))])),runtimeChanged:false,status:'verified'},null,2))
