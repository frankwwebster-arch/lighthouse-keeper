import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-game-scale-prime-2026-10-17-v26')
const draftDir = path.join(root, 'art/drafts/kitchen-game-scale-prime-2026-10-17-v26')
const pageFile = path.join(root, 'public/keeper-review/kitchen-game-scale-prime-v26/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-game-scale-prime-v26.json')
const roomSha = '175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a'
const frontSha = 'a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e'
const seatedSha = '28a879bcee43c6d06330d05fb3cd74b4098b2ccce38ce41d15117f5fb0be5167'
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))

assert.equal(sha(path.join(root, 'art/raw/kitchen-narrower-bin-2026-10-17-v25/full-kitchen-narrower-bin.png')), roomSha, 'V25 changed')
assert.equal(sha(path.join(root, 'art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png')), frontSha, 'Prime Master changed')
assert.equal(sha(path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png')), seatedSha, 'seated-back source changed')

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 26)
assert.equal(catalogue.status, 'game-scale-prime-context-review')
assert.deepEqual(catalogue.presentation, {
  densityPxPerLp: 4,
  roomLogical: [193, 56],
  roomPixels: [772, 224],
  sourceCropExclusive: [0, 45, 2064, 643],
  primeLogicalCell: [32, 40],
  primePixels: [128, 160],
  primeFloorAnchorLp: 56,
  seatedContactAboveFloorLp: 11,
})
assert.deepEqual(catalogue.placements.standing, { topLeftPx: [362, 64], rootLp: [106.5, 56], sourceSha256: frontSha })
assert.deepEqual(catalogue.placements.seatedBack, { topLeftPx: [655, 64], rootLp: [179.75, 56], sourceSha256: seatedSha })
assert.deepEqual(catalogue.boundaries, { v25Changed: false, approved: false, promoted: false, runtimeChanged: false, finalChanged: false })
assert.equal(register.v25Preserved, true)

const names = ['kitchen-game-scale-room.png', 'kitchen-game-scale-prime-standing.png', 'kitchen-game-scale-prime-seated-back.png']
for (const name of names) {
  const file = path.join(rawDir, name)
  assert.deepEqual([png(file).width, png(file).height], [772, 224])
  assert.equal(sha(file), catalogue.outputs[name].sha256)
}
assert.notEqual(catalogue.outputs[names[0]].sha256, catalogue.outputs[names[1]].sha256)
assert.notEqual(catalogue.outputs[names[0]].sha256, catalogue.outputs[names[2]].sha256)

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /actual proposed game presentation size/)
assert.match(page, /772 × 224 px/)
assert.match(page, /Prime seated at the one-person table/)
assert.match(page, /final chair\/character occlusion remains a later runtime-layer decision/)
assert.match(page, /Promise\.all\(files\.map/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-game-scale-prime-v26'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 3)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V26 game-scale Prime context verified: 193 × 56 lp at 4 px/lp')
