import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-rear-facing-chair-2026-10-17-v24/image-edit-source.png')
const rawDir = path.join(root, 'art/raw/kitchen-rear-facing-chair-2026-10-17-v24')
const full = path.join(rawDir, 'full-kitchen-rear-facing-chair.png')
const draft = path.join(root, 'art/drafts/kitchen-rear-facing-chair-2026-10-17-v24')
const pageFile = path.join(root, 'public/keeper-review/kitchen-rear-facing-chair-v24/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-rear-facing-chair-v24.json')
const editSha = '85e50fc43d43538e226e41e9d781cd8eee805b6025fe15302639a8f178ce71b2'
const v23Sha = '5d5451acbaa81a48918268d25482a1d3f657a77c441c9d5b4f87ed547d4f9707'
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))

assert.equal(sha(source), editSha)
assert.equal(sha(full), editSha, 'V24 full room must preserve the selected edit bytes')
assert.equal(sha(path.join(root, 'art/raw/kitchen-continuous-run-approved-2026-10-17-v23/full-kitchen-approved.png')), v23Sha, 'V23 changed')

const fullImage = png(full)
const before = png(path.join(rawDir, 'table-before.png'))
const after = png(path.join(rawDir, 'table-after.png'))
assert.deepEqual([fullImage.width, fullImage.height], [2169, 725])
assert.deepEqual([before.width, before.height], [550, 320])
assert.deepEqual([after.width, after.height], [550, 320])
assert.notEqual(sha(path.join(rawDir, 'table-before.png')), sha(path.join(rawDir, 'table-after.png')), 'chair crop must change')

const data = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(data.version, 24)
assert.equal(data.status, 'requested-chair-correction-awaiting-visual-confirmation')
assert.deepEqual(data.change, {
  object: 'single chair at table for one',
  old: 'side-on, between sink and table',
  new: 'rear view, centred on player-facing side, seat faces table/rear wall',
  keeperOrientation: 'back to player when seated',
  chairCount: 1,
})
assert.deepEqual(data.boundaries, { approved: false, promoted: false, runtimeChanged: false, finalChanged: false, keeperChanged: false })
assert.equal(register.v23Preserved, true)

const outputPins = {
  'full-kitchen-rear-facing-chair.png': editSha,
  'table-before.png': data.outputs['table-before.png'].sha256,
  'table-after.png': data.outputs['table-after.png'].sha256,
}
for (const [name, expected] of Object.entries(outputPins)) assert.equal(sha(path.join(rawDir, name)), expected)

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /Prime faces the rear wall/)
assert.match(page, /backrest faces the player/)
assert.match(page, /exactly one chair/)
assert.match(page, /Promise\.all\(files\.map/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-rear-facing-chair-v24'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 3)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V24 rear-facing table chair verified')
