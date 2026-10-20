#!/usr/bin/env node
/** Verify V41's byte-identical art, broken-position lock and asset-local effects. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const set = 'kitchen-dishwasher-workbench-v41'
const batch = 'kitchen-dishwasher-workbench-2026-10-20-v41'
const raw = path.join(root, 'art/raw', batch)
const draft = path.join(root, 'art/drafts', batch)
const review = path.join(root, 'public/keeper-review', set)
const v40Raw = path.join(root, 'art/raw/kitchen-dishwasher-workbench-2026-10-20-v40')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json')))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json')))

assert.equal(catalogue.schema, 'lighthouse-keeper/kitchen-dishwasher-workbench@1')
assert.equal(catalogue.version, 41)
assert.equal(catalogue.set, set)
assert.equal(register.set, set)
assert.equal(catalogue.status, 'reversible-unapproved-unpromoted')
assert.equal(catalogue.boundaries.v40Changed, false)
assert.equal(catalogue.boundaries.runtimeControllerImplemented, false)
assert.equal(catalogue.brokenAssetLock.scope, 'every movable kitchen asset')
assert.equal(catalogue.brokenAssetLock.directMove, 'reject')
assert.equal(catalogue.brokenAssetLock.displacementBySwap, 'reject')
assert.equal(catalogue.brokenAssetLock.groupMoveIncludingLockedAsset, 'reject')
assert.equal(catalogue.brokenAssetLock.unlockTransition, 'repair to any non-broken state')
assert.equal(catalogue.snapContract.brokenAssetsMovable, false)
assert.equal(catalogue.snapContract.repairUnlocksMovement, true)

const names = Object.keys(catalogue.publishedAssets)
assert.equal(names.length, 49)
for (const name of names) {
  const file = path.join(raw, name)
  const authority = path.join(v40Raw, name)
  assert.ok(fs.existsSync(file), name)
  assert.equal(sha(file), sha(authority), `${name} changed from V40`)
  assert.equal(sha(file), catalogue.publishedAssets[name], `${name} catalogue hash mismatch`)
  const item = register.publishedAssets.find(entry => entry.publicAssemblyPath.endsWith(`/assets/${name}`))
  assert.ok(item, `register missing ${name}`)
  assert.equal(item.sourceSha256, sha(file))
}
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.anchorAssetId, effect.asset)
  assert.equal(effect.transformSpace, 'asset-local')
  assert.equal(effect.remainsAttachedWhileBroken, true)
}

const origins = catalogue.grid.slotOriginsX
const initial = { fridge:84, cabinetA:168, oven:252, cabinetB:336, sink:420, dishwasher:504 }
function attemptMove(position, states, id, target) {
  const out = { ...position }
  const locked = asset => states[asset] === 'broken'
  const other = Object.keys(out).find(asset => out[asset] === target)
  if (locked(id) || (other && other !== id && locked(other))) return { moved:false, position:out }
  const old = out[id]
  if (other && other !== id) out[other] = old
  out[id] = target
  return { moved:true, position:out }
}
const broken = { dishwasher:'broken' }
for (const target of origins) {
  const direct = attemptMove(initial, broken, 'dishwasher', target)
  assert.equal(direct.moved, false)
  assert.deepEqual(direct.position, initial)
  const invader = Object.keys(initial).find(id => id !== 'dishwasher' && initial[id] === target) ?? 'fridge'
  const intoLockedBay = attemptMove(initial, broken, invader, initial.dishwasher)
  assert.equal(intoLockedBay.moved, false)
  assert.deepEqual(intoLockedBay.position, initial)
}
const repaired = attemptMove(initial, { dishwasher:'off' }, 'dishwasher', 84)
assert.equal(repaired.moved, true)
assert.equal(repaired.position.dishwasher, 84)
assert.equal(repaired.position.fridge, 504)

const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [
  /Broken-state lock/,
  /function isLocked\(id\)/,
  /function tryMove\(id,target\)/,
  /Blocked: .* is Broken and fixed/,
  /whole-run rotation would move a Broken asset/,
  /anchorAssetId:'dishwasher'/,
  /pos\[layer\.anchorAssetId\]/,
  /repair to Off\/On before moving/,
  /Promise\.all\(names\.map\(load\)/,
  /\.decode\(\)/,
]) assert.match(html, pattern)
assert.match(fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8'), /source: '\/keeper-review\/kitchen-dishwasher-workbench-v41'/)

const manifestPath = path.join(root, 'review-archive/sets', `${set}.json`)
assert.ok(fs.existsSync(manifestPath), 'archive manifest missing')
const manifest = JSON.parse(fs.readFileSync(manifestPath))
assert.equal(Object.keys(manifest.entries).length, names.length)
for (const [name, hash] of Object.entries(catalogue.publishedAssets)) {
  const entry = manifest.entries[`/keeper-review/${set}/assets/${name}`]
  assert.ok(entry, `archive entry missing ${name}`)
  assert.equal(entry.sha256, hash)
  assert.equal(sha(path.join(root, entry.object)), hash)
}

console.log('Kitchen Dishwasher Workbench V41 verified: 49 V40-identical assets, Broken move/swap/group locks, repair unlock and asset-local effects.')
