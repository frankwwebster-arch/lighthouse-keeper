#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = 'art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1'
const v2 = 'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2'
const v2Input = `${v2}/claude-code-model-test-pack`
const v7 = 'art/drafts/activity-cloud-composer-2026-10-20-v7'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const list = value => fs.readdirSync(abs(value), {withFileTypes: true}).filter(item => item.isFile()).map(item => item.name).sort()
const manifest = json(`${pack}/asset-manifest.json`)
const register = json(`${pack}/batch-register.json`)

assert.equal(manifest.schema, 'lighthouse-keeper/claude-activity-cloud-review-pack@1')
assert.equal(register.schema, 'lighthouse-keeper/claude-activity-cloud-review-pack-register@1')
assert.equal(manifest.status, 'immutable-input-only-review-pack')
assert.equal(register.status, manifest.status)
assert.deepEqual(manifest.counts, {
  files: 95,
  pngImages: 78,
  finalUsableVisualAssets: 74,
  approvedPrimeBodyImages: 41,
  activityObjectImages: 20,
  originalSymbolImages: 6,
  genericV7SymbolImages: 7,
  acceptedSourceImages: 3,
  rejectedEvidenceImages: 1,
})
assert.deepEqual(register.counts, manifest.counts)
assert.equal(register.sourcePacksUnchanged, true)
assert.equal(register.runtimeChanged, false)
assert.equal(register.kitchenChanged, false)
assert.equal(register.deployed, false)

for (const item of manifest.files) {
  const file = `${pack}/${item.path}`
  assert.ok(fs.existsSync(abs(file)), `missing packaged file ${item.path}`)
  assert.equal(fs.lstatSync(abs(file)).isSymbolicLink(), false, `symlink is not self-contained: ${item.path}`)
  assert.equal(fs.statSync(abs(file)).size, item.bytes, `byte length mismatch: ${item.path}`)
  assert.equal(sha(file), item.sha256, `hash mismatch: ${item.path}`)
}
assert.equal(new Set(manifest.files.map(item => item.path)).size, manifest.files.length)

const exactDirs = [
  [`${v2Input}/assets/body`, `${pack}/assets/body`],
  [`${v2Input}/assets/activity`, `${pack}/assets/activity`],
]
for (const [sourceDir, packedDir] of exactDirs) {
  assert.deepEqual(list(packedDir), list(sourceDir), `${packedDir} filenames drifted`)
  for (const name of list(sourceDir)) assert.equal(sha(`${packedDir}/${name}`), sha(`${sourceDir}/${name}`), `${name} bytes changed`)
}
const originalSymbols = list(`${v2Input}/assets/symbol`)
assert.deepEqual(list(`${pack}/assets/symbol/original`), originalSymbols)
for (const name of originalSymbols) assert.equal(sha(`${pack}/assets/symbol/original/${name}`), sha(`${v2Input}/assets/symbol/${name}`), `${name} bytes changed`)

const v7Components = list(`${v7}/drafts/components`)
const packedGeneric = list(`${pack}/assets/symbol/generic-v7`)
assert.equal(v7Components.length, 7)
assert.equal(packedGeneric.length, 7)
for (const name of v7Components) {
  const source = `${v7}/drafts/components/${name}`
  const expected = `${path.parse(name).name}-${sha(source).slice(0, 12)}.png`
  assert.ok(packedGeneric.includes(expected), `missing V7 symbol ${expected}`)
  assert.equal(sha(`${pack}/assets/symbol/generic-v7/${expected}`), sha(source))
}

const exactFiles = [
  [`${v2Input}/assets/source/activity-comic-symbols-source-sheet.png`, `${pack}/assets/source/original-six-symbol-source-sheet.png`],
  [`${v7}/source/generic-action-symbols-sheet-source.png`, `${pack}/assets/source/generic-action-symbols-sheet-source.png`],
  [`${v7}/source/generic-question-mark-source.png`, `${pack}/assets/source/generic-question-mark-source.png`],
  [`${v7}/rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png`, `${pack}/evidence/rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png`],
  [`${v2Input}/metadata/approved-prime-sequence.json`, `${pack}/metadata/approved-prime-sequence.json`],
  [`${v2Input}/metadata/activity-vocabulary.json`, `${pack}/metadata/composer-v6-activity-vocabulary.json`],
  [`${v2Input}/metadata/v1-catalogue.json`, `${pack}/metadata/choreography-v1-catalogue.json`],
  [`${v2Input}/metadata/v2-catalogue.json`, `${pack}/metadata/choreography-v2-catalogue.json`],
  [`${v2Input}/asset-manifest.json`, `${pack}/metadata/choreography-v2-original-asset-manifest.json`],
  [`${v2}/batch-register.json`, `${pack}/metadata/choreography-v2-register.json`],
  ['public/keeper-review/activity-cloud-composer-v7/catalogue.json', `${pack}/metadata/composer-v7-catalogue.json`],
  [`${v7}/batch-register.json`, `${pack}/metadata/composer-v7-register.json`],
  ['docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md', `${pack}/guidance/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md`],
  ['docs/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md', `${pack}/guidance/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md`],
  ['docs/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V2_2026-10-20.md', `${pack}/guidance/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V2_2026-10-20.md`],
  ['docs/ACTIVITY_CLOUD_COMPOSER_V7_2026-10-20.md', `${pack}/guidance/ACTIVITY_CLOUD_COMPOSER_V7_2026-10-20.md`],
  ['data/activity_callout_style_contract.json', `${pack}/guidance/activity_callout_style_contract.json`],
  [`${v2}/page-template.html`, `${pack}/review-shells/keeper-prime-rear-action-choreography-v2.html`],
  ['public/keeper-review/activity-cloud-composer-v7/index.html', `${pack}/review-shells/activity-cloud-composer-v7.html`],
]
for (const [source, destination] of exactFiles) assert.equal(sha(destination), sha(source), `copy drift: ${destination}`)

const hashLines = fs.readFileSync(abs(`${pack}/HASHES.sha256`), 'utf8').trim().split('\n')
for (const line of hashLines) {
  const match = line.match(/^([0-9a-f]{64})  (.+)$/)
  assert.ok(match, `bad checksum line: ${line}`)
  assert.equal(sha(`${pack}/${match[2]}`), match[1], `checksum mismatch: ${match[2]}`)
}
assert.equal(register.manifest.sha256, sha(register.manifest.file))
assert.equal(register.hashList.sha256, sha(register.hashList.file))

const readme = fs.readFileSync(abs(`${pack}/README.md`), 'utf8')
const prompt = fs.readFileSync(abs(`${pack}/CLAUDE_REVIEW_PROMPT.md`), 'utf8')
assert.match(readme, /74 final usable visual assets/)
assert.match(prompt, /review task only/i)
assert.match(prompt, /Do not edit any repository file/)
assert.match(prompt, /all 13 symbols/)
assert.match(prompt, /Critical \/ Important \/ Optional/)
assert.match(prompt, /Treat every approved Prime body image as immutable and byte-exact/)

console.log(JSON.stringify({
  pack,
  files: manifest.counts.files,
  pngImages: manifest.counts.pngImages,
  finalUsableVisualAssets: manifest.counts.finalUsableVisualAssets,
  approvedPrimeBodyImages: manifest.counts.approvedPrimeBodyImages,
  activityObjects: manifest.counts.activityObjectImages,
  symbols: manifest.counts.originalSymbolImages + manifest.counts.genericV7SymbolImages,
  acceptedSources: manifest.counts.acceptedSourceImages,
  rejectedEvidence: manifest.counts.rejectedEvidenceImages,
  hashes: 'verified',
  sourcePacks: 'byte-exact',
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
}, null, 2))
