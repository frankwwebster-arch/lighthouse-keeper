import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const retiredRoot = path.join(root, 'review-archive/retired/kitchen-v1-v4-v6-v19')
const record = JSON.parse(fs.readFileSync(path.join(retiredRoot, 'RETIREMENT.json'), 'utf8'))
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/index.json'), 'utf8'))

assert.equal(record.retiredSets.length, 19)
assert.equal(record.retainedOldFamily, 'kitchen-basic-assets-v5')
assert.equal(record.activeReplacement, 'kitchen-fitted-galley-v20')
assert.equal(record.evidence.publiclyRouted, false)
assert.ok(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-basic-assets-v5/index.html')))
assert.ok(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-fitted-galley-v20/index.html')))

for (const set of record.retiredSets) {
  assert.ok(!fs.existsSync(path.join(root, 'public/keeper-review', set)), `${set} remains publicly deployed`)
  assert.ok(!fs.existsSync(path.join(root, 'review-archive/sets', `${set}.json`)), `${set} remains active in the archive resolver`)
  const page = path.join(retiredRoot, 'review-pages', set, 'index.html')
  const manifestFile = path.join(retiredRoot, 'set-manifests', `${set}.json`)
  assert.ok(fs.existsSync(page), `${set} retired page was not retained`)
  assert.ok(fs.existsSync(manifestFile), `${set} retired manifest was not retained`)
  const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'))
  for (const [legacyPath, entry] of Object.entries(manifest.entries ?? {})) {
    assert.ok(!archive.legacyPaths[legacyPath], `${legacyPath} is still publicly resolvable`)
    assert.ok(fs.existsSync(path.join(root, entry.object)), `${legacyPath} media bytes were deleted`)
  }
}

for (const folder of [
  'art/source/kitchen-basic-assets-2026-10-16-v1',
  'art/raw/kitchen-basic-assets-2026-10-16-v6-option-b',
  'art/drafts/kitchen-v5-v18-in-situ-2026-10-17-v19',
]) assert.ok(fs.existsSync(path.join(root, folder)), `${folder} historical evidence was deleted`)

console.log('Retired kitchen V1–V4/V6–V19 evidence verified: retained offline and absent from public review routing')
