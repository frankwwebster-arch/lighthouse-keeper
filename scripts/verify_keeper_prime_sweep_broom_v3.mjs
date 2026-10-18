#!/usr/bin/env node
/** Deterministically verify the immutable Prime sweep-broom V3 review set. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const read = (name) => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'))
const bytes = (name) => fs.readFileSync(path.join(root, name))
const sha = (name) => crypto.createHash('sha256').update(bytes(name)).digest('hex')
const png = (name) => PNG.sync.read(bytes(name))
const pack = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v3'
const register = read(`${pack}/batch-register.json`)
const route = read(`${pack}/keeper-prime-sweep-broom-v3.json`)
const reviewer = fs.readFileSync(path.join(root, `${pack}/reviewer.html`), 'utf8')
const page = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sweep-broom-v3/index.html'), 'utf8')

assert.equal(register.set, 'keeper-prime-sweep-broom-v3')
assert.equal(register.status, 'prime-sweep-broom-v3-awaiting-frank')
assert.equal(route.set, register.set)
assert.equal(route.status, 'versioned-reversible-review-candidate-not-approved')
assert.ok(fs.existsSync(path.join(root, 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v1/batch-register.json')))
assert.ok(fs.existsSync(path.join(root, 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v2/batch-register.json')))
assert.equal(register.approvalBoundary.candidateApproved, false)
assert.equal(register.approvalBoundary.promotionAllowed, false)
assert.equal(register.approvalBoundary.productionChanged, false)
assert.equal(register.historicalChoreographyOnly.visibleKeeperPixelsReused, 0)
assert.equal(register.authorities.backSitStandV2Approval.promotionPerformed, false)
assert.equal(register.authorities.approvedCoreTurn.frameSha256.length, 9)
for (const authority of Object.values(register.authorities)) if (authority.file && authority.sha256) assert.equal(sha(authority.file), authority.sha256)

const required = ['capCrown','capBandBrim','badge','jumperBlue','creamBand','trousers','boots','skin','hair','beard','outline']
const gaitHashes = new Set()
for (const frame of register.candidate.frames) {
  for (const part of ['actor','prop','composite']) {
    assert.equal(sha(frame[part].file), frame[part].sha256, `${frame.id} ${part} hash`)
    const image = png(frame[part].file)
    assert.deepEqual([image.width, image.height], [384,320])
  }
  assert.equal(frame.composite.edgeAlphaPixels, 0, `${frame.id} shared edge alpha`)
  assert.ok(frame.composite.transparentGutterPx >= 4, `${frame.id} gutter`)
  for (const name of required) assert.equal(frame.colourEvidence[name].status, 'pass', `${frame.id} ${name}`)
  if (frame.id !== 'neutral') {
    assert.equal(frame.lowerJumperRepair.status, 'pass')
    assert.ok(frame.lowerJumperRepair.removedInternalOutlinePixels >= 0)
    assert.ok(frame.walkGait.source.includes('keeper-prime-walk-2026-10-14-v6'))
    gaitHashes.add(frame.walkGait.alphaSha256)
    assert.equal(sha(frame.walkGait.source), frame.walkGait.sourceSha256)
    assert.equal(frame.broomHandContact.status, 'pass')
  }
}
assert.ok(gaitHashes.size >= 5, 'sweep travel must expose distinct approved walk-leg phases')
assert.equal(sha(register.candidate.contactSheet.file), register.candidate.contactSheet.sha256)
assert.equal(sha(register.candidate.route.file), register.candidate.route.sha256)

assert.equal(route.cupboardRoute.length, 59)
assert.deepEqual(route.cupboardRoute.slice(0,8).map(x => x.phase), Array(8).fill('standard walk toward cupboard'))
const turns = route.cupboardRoute.filter(x => x.phase === 'approved core reversal turn')
assert.equal(turns.length, 17)
assert.ok(turns.every(x => x.turnAuthority === 'keeper-prime-turn-side-back-2026-10-13-v9' && x.actorRootXLp === 46))
assert.equal(route.cupboardRoute.some(x => x.phase.includes('proxy')), false)
const sweeps = route.cupboardRoute.filter(x => x.phase.startsWith('sweep-walk'))
assert.equal(sweeps.length, 24)
assert.ok(sweeps.every(x => /approved Walk V6 gait/.test(x.label)))
for (const handoff of route.cupboardRoute.filter(x => x.phase === 'fully obscured state handoff')) {
  assert.equal(handoff.hidden, false, 'door must occlude actual visible layers rather than hide them')
  const { actor, prop, door } = handoff.doorCoverage
  assert.ok(door[0] <= actor[0] && door[1] >= actor[1] && door[0] <= prop[0] && door[1] >= prop[1], 'closed door does not cover full actor/prop placement')
}
for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of ['Cupboard handoff','approved core reversal turn','approved Walk V6 gait','width:80px','Loading and decoding every unique frame','img.decode','Previous-frame ghost','Frame-by-frame Prime comparison']) assert.ok(reviewer.includes(token), token)
assert.equal(reviewer.includes("frame.hidden?'hidden'"), false)
assert.match(page, /__V3_COMMIT__/, 'pin the shell only after the immutable candidate commit exists')
console.log('Prime sweep-broom V3 verified: rebuilt hem, approved Walk V6 gait, approved V9 reversal, full physical door occlusion, all-frame material gates, no promotion.')
