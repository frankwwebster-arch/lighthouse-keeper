#!/usr/bin/env node
/** Verify Frank's immutable approval of Kitchen Modular Join Workbench V33. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root=process.cwd(),file=relative=>path.join(root,relative),json=relative=>JSON.parse(fs.readFileSync(file(relative),'utf8')),sha=relative=>crypto.createHash('sha256').update(fs.readFileSync(file(relative))).digest('hex')
const rel={decision:'docs/review/kitchen-modular-join-workbench-v33-approval-2026-10-20.json',catalogue:'art/drafts/kitchen-modular-join-workbench-2026-10-20-v33/candidate-catalogue.json',register:'art/drafts/kitchen-modular-join-workbench-2026-10-20-v33/batch-register.json',page:'public/keeper-review/kitchen-modular-join-workbench-v33/index.html',archive:'review-archive/sets/kitchen-modular-join-workbench-v33.json'}
for(const relative of Object.values(rel))assert.ok(fs.existsSync(file(relative)),`missing ${relative}`)
const decision=json(rel.decision),catalogue=json(rel.catalogue),archive=json(rel.archive)
assert.equal(decision.schema,'lighthouse-keeper/review-decision@1');assert.equal(decision.reviewedBy,'Frank');assert.equal(decision.candidate,'kitchen-modular-join-workbench-2026-10-20-v33');assert.equal(decision.decision,'approved-as-kitchen-modular-join-workbench-authority');assert.equal(decision.wording,'excellent. Approved.')
for(const key of ['catalogue','register','page','archive'])assert.equal(decision.approvedHashes[key==='catalogue'?'candidateCatalogue':key==='register'?'batchRegister':key==='page'?'reviewPage':'archiveManifest'],sha(rel[key]))
assert.equal(catalogue.set,'kitchen-modular-join-workbench-v33');assert.equal(catalogue.version,33);assert.deepEqual(catalogue.grid.slotOriginsX,decision.approvedContract.canonicalOriginsX);assert.deepEqual(catalogue.grid.fixedCabinetOriginsX,decision.approvedContract.fixedCabinetOriginsX);assert.deepEqual(catalogue.grid.freeOriginsX,decision.approvedContract.movableOriginsX);assert.equal(catalogue.grid.bayWidthPixels,decision.approvedContract.bayWidthPixels);assert.equal(catalogue.grid.primeStopTurnY,decision.approvedContract.primeStopTurnY)
for(const [name,expected] of Object.entries(catalogue.publishedAssets)){const raw=`art/raw/kitchen-modular-join-workbench-2026-10-20-v33/${name}`;assert.equal(sha(raw),expected,`${name} changed after approval`);assert.equal(archive.entries[`/keeper-review/kitchen-modular-join-workbench-v33/assets/${name}`].sha256,expected)}
for(const flag of ['singleWorkbenchForSinkAndOven','exactSnapGrid','collisionSafePlacement','primeAnchorFromBodyMidpoint','pairAwareJoinHealing','sinkAndOvenMayBeAdjacentEitherWay','exposedSinkLeftEndHealing','sourceSpritesRemainUnchanged'])assert.equal(decision.approvedContract[flag],true)
for(const flag of ['finalChanged','runtimeChanged','productionAssetsChanged','promotionPerformed','promotionAllowedWithoutSeparateInstruction'])assert.equal(decision.approvalBoundary[flag],false)
console.log('Kitchen Modular Join Workbench V33 approval verified: exact sink/oven snap, anchors and pair-aware healing are hash-pinned.')
