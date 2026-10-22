#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const relativeSource = 'art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png'
const source = path.join(root, relativeSource)
const pagePath = 'public/keeper-review/kitchen-high-resolution-foundation-v1/index.html'
const manifestPath = 'review-archive/sets/kitchen-high-resolution-foundation-v1.json'
const legacyPath = '/keeper-review/kitchen-high-resolution-foundation-v1/assets/kitchen-fitted-run-first-render-authority.png'
const expectedHash = 'bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2'

const bytes = fs.readFileSync(source)
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex')
assert.equal(sha256(bytes), expectedHash, 'selected first-render bytes changed')
assert.equal(bytes.toString('ascii', 1, 4), 'PNG', 'selected view is not a PNG')
assert.equal(bytes.readUInt32BE(16), 2203, 'selected view width changed')
assert.equal(bytes.readUInt32BE(20), 714, 'selected view height changed')

const contract = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_high_resolution_asset_contract_v1.json'), 'utf8'))
assert.equal(contract.authorities.primaryCompositionView.path, relativeSource)
assert.equal(contract.authorities.primaryCompositionView.sha256, expectedHash)
assert.deepEqual(contract.authorities.primaryCompositionView.dimensions, [2203, 714])
assert.equal(contract.geometry.fittedModules.basicFridge.model, 'undercounter')
assert.equal(contract.geometry.fittedModules.basicFridge.tallUpgradeAllowedHere, false)

const sourceManifest = JSON.parse(fs.readFileSync(path.join(root, 'art/source/kitchen-high-resolution-foundation-2026-10-22-v1/manifest.json'), 'utf8'))
assert.equal(sourceManifest.selectedPrimaryView.file, path.basename(relativeSource))
assert.equal(sourceManifest.selectedPrimaryView.originalSha256, expectedHash)
assert.equal(sourceManifest.selectedPrimaryView.draftCopySha256, expectedHash)

const page = fs.readFileSync(path.join(root, pagePath), 'utf8')
assert.match(page, new RegExp(legacyPath.replaceAll('/', '\\/')))
assert.match(page, /exact first fitted-run render/i)
assert.match(page, /basic fridge remains a one-bay undercounter model/i)
assert.match(page, /adult cinematic ligne claire/i)
assert.match(page, /restrained three-dimensional modelling/i)
assert.match(page, /image\.decode\(\)/, 'review must decode the selected render before enabling controls')
assert.doesNotMatch(page, /state-family-atlas/, 'later atlas must not compete in the primary view')

const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(nextConfig, /source: '\/keeper-review\/kitchen',[\s\S]*?destination: '\/keeper-review\/kitchen-high-resolution-foundation-v1\/index\.html'/)

const manifest = JSON.parse(fs.readFileSync(path.join(root, manifestPath), 'utf8'))
const entry = manifest.entries[legacyPath]
assert(entry, 'selected render missing from content-addressed review manifest')
assert.equal(entry.sha256, expectedHash)
const object = path.join(root, entry.object)
assert.equal(sha256(fs.readFileSync(object)), expectedHash, 'archived selected render differs from source')

console.log('Kitchen high-resolution foundation V1 verified: exact first render is the sole primary review view.')
