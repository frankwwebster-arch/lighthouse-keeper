import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const v5raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const rollbackRaw = path.join(root, 'art/raw/kitchen-v5-exact-rollback-2026-10-17-v17')
const v5draft = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v5')
const draft = path.join(root, 'art/drafts/kitchen-v5-exact-rollback-2026-10-17-v17')
const recipe = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_v5_exact_rollback_v17_recipe.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const reviewData = JSON.parse(fs.readFileSync(path.join(draft, 'review-data.json'), 'utf8'))
const v5ReviewData = JSON.parse(fs.readFileSync(path.join(v5draft, 'review-data.json'), 'utf8'))
const sourceMap = JSON.parse(fs.readFileSync(path.join(draft, 'source-map.json'), 'utf8'))
const v5Set = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-basic-assets-v5.json'), 'utf8'))
const rollbackSetFile = path.join(root, 'review-archive/sets/kitchen-v5-exact-rollback-v17.json')
const pageFile = path.join(root, 'public/keeper-review/kitchen-v5-exact-rollback-v17/index.html')
const page = fs.readFileSync(pageFile, 'utf8')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const files = directory => { const result=[]; const walk=current=>fs.readdirSync(current,{withFileTypes:true}).forEach(entry=>{const absolute=path.join(current,entry.name);if(entry.isDirectory())walk(absolute);else if(entry.isFile())result.push(absolute)});walk(directory);return result.sort() }
const treeSha = directory => { const digest=crypto.createHash('sha256');for(const file of files(directory)){digest.update(path.relative(directory,file).split(path.sep).join('/'));digest.update('\0');digest.update(fs.readFileSync(file));digest.update('\0')}return digest.digest('hex') }
const rewrite = value => {
  if (typeof value === 'string') return value.replace('/keeper-review/kitchen-v5-exact-rollback-v17/assets/', '/keeper-review/kitchen-basic-assets-v5/assets/')
  if (Array.isArray(value)) return value.map(rewrite)
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key,item])=>[key,rewrite(item)]))
  return value
}

assert.equal(recipe.id, 'kitchen-v5-exact-rollback-v17')
assert.equal(recipe.authority, 'kitchen-basic-assets-v5')
assert.equal(recipe.scope.assetFamilies, 10)
assert.equal(recipe.scope.visualChangesFromV5, 0)
assert.equal(recipe.scope.metadataChangesFromV5, 0)
assert.equal(recipe.runtimeWiring, false)
assert.equal(recipe.promotion, false)
assert.equal(register.version, 17)
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)
assert.equal(register.runtimeSpriteManifestSha256, sha(path.join(root, 'public/sprites/manifest.json')))
assert.equal(register.animationWorkbenchFinalStateSha256, sha(path.join(root, 'data/keeper_animation_workbench.json')))
assert.equal(register.v5RawTreeSha256, treeSha(v5raw))
assert.equal(register.rollbackRawTreeSha256, treeSha(rollbackRaw))
assert.equal(register.v5RawTreeSha256, register.rollbackRawTreeSha256, 'rollback raw tree is not byte-identical to V5')

const v5Files = files(v5raw).map(file=>path.relative(v5raw,file).split(path.sep).join('/'))
const rollbackFiles = files(rollbackRaw).map(file=>path.relative(rollbackRaw,file).split(path.sep).join('/'))
assert.deepEqual(rollbackFiles, v5Files, 'rollback raw file list differs from V5')
for (const relative of v5Files) assert.equal(sha(path.join(rollbackRaw,relative)),sha(path.join(v5raw,relative)),`rollback raw file differs from V5: ${relative}`)

assert.deepEqual(rewrite(reviewData), v5ReviewData, 'V17 metadata differs from V5 after URL normalization')
assert.deepEqual(Object.keys(reviewData.assets).sort(), ['obj_bin','obj_cooker','obj_cupboard','obj_fridge','obj_kettle','obj_mixer','obj_petbowl','obj_sink','obj_table','obj_toaster'].sort())
assert.equal(Object.keys(sourceMap).length, 153)
assert.equal(register.copiedReviewImages, 153)
for (const [targetUrl, record] of Object.entries(sourceMap)) {
  assert.ok(targetUrl.startsWith('/keeper-review/kitchen-v5-exact-rollback-v17/assets/'))
  assert.ok(record.sourceUrl.startsWith('/keeper-review/kitchen-basic-assets-v5/assets/'))
  assert.deepEqual(record, {sourceUrl:record.sourceUrl,sourceObject:v5Set.entries[record.sourceUrl].object,sha256:v5Set.entries[record.sourceUrl].sha256,bytes:v5Set.entries[record.sourceUrl].bytes})
}

assert.doesNotMatch(page, /\/keeper-review\/kitchen-basic-assets-v5\/assets\//)
assert.doesNotMatch(page, /\/keeper-review\/kitchen-(?:basic-assets-v6|room-flat-cutaway-v7|wall-anchored-v8|fridge-shelf-v9|porthole-backdrop-cutout-v10|kettle-recipe-shelf-v1[12]|countertop-(?:continuity-v13|no-splashback-v14)|option-b-(?:clean-surface-v15|silhouette-clean-v16))\/assets\//)
assert.match(page, /All ten asset families, every state\/frame, all room pieces and both room compositions are byte-identical copies of Kitchen V5/)
assert.match(page, /Promise\.all\(unique\.map/)
assert.match(page, /i\.decode/)
assert.ok(fs.existsSync(path.join(root, 'docs/KITCHEN_V5_EXACT_ROLLBACK_V17_2026-10-17.md')))
assert.ok(fs.existsSync(path.join(root, 'docs/CODEX_TO_CLAUDE_KITCHEN_V5_EXACT_ROLLBACK_V17_2026-10-17.md')))

assert.ok(fs.existsSync(rollbackSetFile), 'V17 archive set is missing')
const rollbackSet = JSON.parse(fs.readFileSync(rollbackSetFile, 'utf8'))
assert.equal(rollbackSet.set, 'kitchen-v5-exact-rollback-v17')
assert.equal(rollbackSet.page.sha256, sha(pageFile))
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-v5-exact-rollback-v17/assets')), false, 'public V17 binaries must be archived')
assert.equal(Object.keys(rollbackSet.entries).length, 153)
for (const [targetUrl, record] of Object.entries(sourceMap)) {
  const target = rollbackSet.entries[targetUrl]
  const source = v5Set.entries[record.sourceUrl]
  assert.ok(target, `archived rollback image missing: ${targetUrl}`)
  assert.equal(target.sha256, source.sha256, `${targetUrl} is not byte-identical to V5`)
  assert.equal(target.bytes, source.bytes, `${targetUrl} byte length differs from V5`)
  assert.equal(target.object, source.object, `${targetUrl} did not deduplicate to the exact V5 object`)
}

console.log(JSON.stringify({set:recipe.id,rawFiles:v5Files.length,reviewImages:Object.keys(sourceMap).length,assetFamilies:Object.keys(reviewData.assets).length,roomPieces:recipe.scope.roomShellPieces,roomCompositions:recipe.scope.roomCompositions,rawTreeExact:true,reviewBytesExact:true,runtimeChanged:false,status:'verified'},null,2))
