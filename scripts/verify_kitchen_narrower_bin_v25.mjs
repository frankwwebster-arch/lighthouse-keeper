import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-narrower-bin-2026-10-17-v25/image-edit-source.png')
const rawDir = path.join(root, 'art/raw/kitchen-narrower-bin-2026-10-17-v25')
const full = path.join(rawDir, 'full-kitchen-narrower-bin.png')
const draft = path.join(root, 'art/drafts/kitchen-narrower-bin-2026-10-17-v25')
const pageFile = path.join(root, 'public/keeper-review/kitchen-narrower-bin-v25/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-narrower-bin-v25.json')
const editSha = '175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a'
const v24Sha = '85e50fc43d43538e226e41e9d781cd8eee805b6025fe15302639a8f178ce71b2'
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))

assert.equal(sha(source), editSha)
assert.equal(sha(full), editSha, 'V25 full room must preserve the selected edit bytes')
assert.equal(sha(path.join(root, 'art/raw/kitchen-rear-facing-chair-2026-10-17-v24/full-kitchen-rear-facing-chair.png')), v24Sha, 'V24 changed')

const fullImage = png(full)
const before = png(path.join(rawDir, 'bin-before.png'))
const after = png(path.join(rawDir, 'bin-after.png'))
assert.deepEqual([fullImage.width, fullImage.height], [2169, 725])
assert.deepEqual([before.width, before.height], [260, 230])
assert.deepEqual([after.width, after.height], [260, 230])
assert.notEqual(sha(path.join(rawDir, 'bin-before.png')), sha(path.join(rawDir, 'bin-after.png')), 'bin crop must change')

const data = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(data.version, 25)
assert.equal(data.status, 'requested-bin-width-correction-awaiting-visual-confirmation')
assert.deepEqual(data.change, {
  object: 'standalone turquoise pedal bin',
  widthFactor: 0.8,
  centrelinePreserved: true,
  heightPreserved: true,
  floorContactPreserved: true,
})
assert.deepEqual(data.boundaries, { approved: false, promoted: false, runtimeChanged: false, finalChanged: false, keeperChanged: false })
assert.equal(register.v24Preserved, true)

const outputPins = {
  'full-kitchen-narrower-bin.png': editSha,
  'bin-before.png': data.outputs['bin-before.png'].sha256,
  'bin-after.png': data.outputs['bin-after.png'].sha256,
}
for (const [name, expected] of Object.entries(outputPins)) assert.equal(sha(path.join(rawDir, name)), expected)

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /Bin 20% narrower/)
assert.match(page, /centreline, height, floor contact/)
assert.match(page, /rear-facing chair/)
assert.match(page, /Promise\.all\(files\.map/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-narrower-bin-v25'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 3)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V25 narrower pedal bin verified')
