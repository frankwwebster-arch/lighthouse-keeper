import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const rel = {
  decision: 'docs/review/kitchen-cabinet-run-v11-approval-2026-10-19.json',
  source: 'art/source/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-generated-source.png',
  catalogue: 'art/drafts/kitchen-cabinet-run-2026-10-19-v11/candidate-catalogue.json',
  register: 'art/drafts/kitchen-cabinet-run-2026-10-19-v11/batch-register.json',
  page: 'public/keeper-review/kitchen-cabinet-run-v11/index.html',
  archive: 'review-archive/sets/kitchen-cabinet-run-v11.json',
}
const sha = relative => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relative))).digest('hex')
const json = relative => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'))
for (const relative of Object.values(rel)) assert.ok(fs.existsSync(path.join(root, relative)), `missing ${relative}`)
const decision = json(rel.decision)
const catalogue = json(rel.catalogue)
const register = json(rel.register)
const archive = json(rel.archive)
assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-19')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'kitchen-cabinet-run-2026-10-19-v11')
assert.equal(decision.decision, 'approved-as-kitchen-cabinet-review-authority')
assert.equal(decision.wording, 'Good this is approved.')
for (const key of ['source', 'catalogue', 'register', 'page', 'archive']) assert.equal(decision.approvedHashes[key], sha(rel[key]), `${key} changed after approval`)
assert.equal(catalogue.status, 'approved-cabinet-review-authority')
assert.equal(register.status, 'approved-review-authority-unpromoted')
assert.equal(register.approvedOn, '2026-10-19')
for (const [name, expected] of Object.entries(decision.approvedHashes.outputs)) {
  const raw = `art/raw/kitchen-cabinet-run-2026-10-19-v11/${name}`
  assert.equal(sha(raw), expected, `${name} changed after approval`)
  assert.equal(archive.entries[`/keeper-review/kitchen-cabinet-run-v11/assets/${name}`].sha256, expected)
}
assert.deepEqual(catalogue.asset.logicalBodyPixels, [168, 74])
assert.deepEqual(catalogue.asset.bayPixels, [84, 74])
assert.equal(catalogue.asset.containsSink, false)
assert.equal(catalogue.asset.containsAppliances, false)
for (const flag of ['cabinetRunApproved', 'duplicateUseApproved', 'sinkRemainsStandalone', 'appliancesRemainStandalone']) assert.equal(decision.approvedContract[flag], true)
for (const flag of ['finalChanged', 'runtimeChanged', 'promotionPerformed', 'promotionAllowedWithoutSeparateInstruction']) assert.equal(decision.approvalBoundary[flag], false)
console.log('Kitchen Cabinet Run V11 approval verified: exact source and derived cabinet pixels are hash-pinned as review authority; Final/runtime remain unchanged')
