#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex')
const approvedPath = 'art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png'
const authorityPath = 'art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png'
const approvedHash = '898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3'
const authorityHash = 'bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2'
const route = 'kitchen-cabinetry-foundation-v1'
const approvedUrl = `/keeper-review/${route}/assets/cabinetry-module-construction-sheet-approved.png`
const authorityUrl = `/keeper-review/${route}/assets/kitchen-fitted-run-first-render-authority.png`

for (const [relative, expected, width, height] of [
  [approvedPath, approvedHash, 1536, 1024],
  [authorityPath, authorityHash, 2203, 714],
]) {
  const bytes = fs.readFileSync(path.join(root, relative))
  assert.equal(sha256(bytes), expected, `${relative} bytes changed`)
  assert.equal(bytes.toString('ascii', 1, 4), 'PNG', `${relative} is not PNG`)
  assert.equal(bytes.readUInt32BE(16), width, `${relative} width changed`)
  assert.equal(bytes.readUInt32BE(20), height, `${relative} height changed`)
}

const contract = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_high_resolution_asset_contract_v1.json'), 'utf8'))
assert.equal(contract.authorities.approvedCabinetryFoundation.path, approvedPath)
assert.equal(contract.authorities.approvedCabinetryFoundation.sha256, approvedHash)
assert.equal(contract.approvalBoundary.approvedCabinetryFoundation, true)
assert.equal(contract.approvalBoundary.productionCropsApproved, false)
assert.equal(contract.approvalBoundary.stateVariantsApproved, false)

const approval = JSON.parse(fs.readFileSync(path.join(root, 'docs/review/kitchen-cabinetry-foundation-v1-approval-2026-10-22.json'), 'utf8'))
assert.equal(approval.approvedSha256, approvedHash)
assert.equal(approval.runtimeChanged, false)

const pagePath = `public/keeper-review/${route}/index.html`
const page = fs.readFileSync(path.join(root, pagePath), 'utf8')
assert.match(page, new RegExp(approvedUrl.replaceAll('/', '\\/')))
assert.match(page, new RegExp(authorityUrl.replaceAll('/', '\\/')))
assert.match(page, /APPROVED VISUAL\/BODY FOUNDATION/)
assert.match(page, /Promise\.all\(images\.map\(decode\)\)/, 'all unique review images must decode before controls unlock')
assert.match(page, /dark construction-sheet backdrop and halo are not game art/i)
assert.match(page, /production crop bounds/i)

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(config, /source: '\/keeper-review\/kitchen',[\s\S]*?destination: '\/keeper-review\/kitchen-cabinetry-foundation-v1\/index\.html'/)
assert.match(config, /source: '\/keeper-review\/kitchen-cabinetry-foundation-v1',[\s\S]*?destination: '\/keeper-review\/kitchen-cabinetry-foundation-v1\/index\.html'/)

const manifest = JSON.parse(fs.readFileSync(path.join(root, `review-archive/sets/${route}.json`), 'utf8'))
for (const [url, expected] of [[approvedUrl, approvedHash], [authorityUrl, authorityHash]]) {
  const entry = manifest.entries[url]
  assert(entry, `${url} missing from review manifest`)
  assert.equal(entry.sha256, expected)
  assert.equal(sha256(fs.readFileSync(path.join(root, entry.object))), expected, `${url} archive object differs`)
}

console.log('Kitchen cabinetry foundation V1 verified: exact approved sheet and original authority are preserved together.')
