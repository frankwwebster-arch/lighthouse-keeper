#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Kitchen Countertop Join Cap V22. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root=process.cwd(),file=relative=>path.join(root,relative),json=relative=>JSON.parse(fs.readFileSync(file(relative),'utf8')),sha=relative=>crypto.createHash('sha256').update(fs.readFileSync(file(relative))).digest('hex')
const rel={
  decision:'docs/review/kitchen-countertop-join-cap-v22-approval-2026-10-19.json',
  catalogue:'art/drafts/kitchen-countertop-join-cap-2026-10-19-v22/candidate-catalogue.json',
  register:'art/drafts/kitchen-countertop-join-cap-2026-10-19-v22/batch-register.json',
  page:'public/keeper-review/kitchen-countertop-join-cap-v22/index.html',
  archive:'review-archive/sets/kitchen-countertop-join-cap-v22.json',
}
for(const relative of Object.values(rel))assert.ok(fs.existsSync(file(relative)),`missing ${relative}`)
const decision=json(rel.decision),catalogue=json(rel.catalogue),register=json(rel.register),archive=json(rel.archive)
assert.equal(decision.schema,'lighthouse-keeper/review-decision@1');assert.equal(decision.reviewedOn,'2026-10-19');assert.equal(decision.reviewedBy,'Frank');assert.equal(decision.candidate,'kitchen-countertop-join-cap-2026-10-19-v22');assert.equal(decision.decision,'approved-as-kitchen-modular-countertop-join-authority');assert.equal(decision.wording,"that's VERY good indeed - we should have used that methodology when we were building this days ago! Approved")
assert.equal(decision.approvedHashes.candidateCatalogue,sha(rel.catalogue));assert.equal(decision.approvedHashes.batchRegister,sha(rel.register));assert.equal(decision.approvedHashes.reviewPage,sha(rel.page));assert.equal(decision.approvedHashes.archiveManifest,sha(rel.archive))
assert.equal(catalogue.set,'kitchen-countertop-join-cap-v22');assert.equal(catalogue.version,22);assert.equal(catalogue.joinTreatment.sourceAssetPixelsChanged,false);assert.deepEqual(catalogue.joinTreatment.drawOrder,decision.approvedContract.drawOrder);assert.deepEqual(catalogue.joinTreatment.capRows,decision.approvedContract.countertopRowsInclusive);assert.equal(catalogue.joinTreatment.bodyUnderlapPixelsPerSide,decision.approvedContract.bodyUnderlapPixelsPerSide);assert.equal(catalogue.joinTreatment.capUnderlapPixelsPerSide,decision.approvedContract.capUnderlapPixelsPerSide);assert.equal(catalogue.joinTreatment.minimumAllowedOverlapPixels,decision.approvedContract.minimumOverlapPixels);assert.equal(catalogue.joinTreatment.maximumBridgedGapPixels,decision.approvedContract.maximumGapPixels)
assert.equal(register.set,'kitchen-countertop-join-cap-v22');assert.equal(register.status,'reversible-unapproved-unpromoted')
for(const [name,expected] of Object.entries(decision.approvedHashes.outputs)){const raw=`art/raw/kitchen-countertop-join-cap-2026-10-19-v22/${name}`;assert.equal(sha(raw),expected,`${name} changed after approval`);assert.equal(catalogue.outputs[name],expected);assert.equal(archive.entries[`/keeper-review/kitchen-countertop-join-cap-v22/assets/${name}`].sha256,expected)}
assert.equal(Object.keys(archive.entries).length,13)
for(const flag of ['modularCountertopJoinMethodApproved','exactV11CabinetRunRetained','exactV19SinkCabinetRetained','sourceAssetPixelsRemainUnchanged','separateBodyBackfillApproved','separateForegroundCountertopCapApproved','optionalSoftSeamRetainedAsComparison','automaticCutoffBeyondRange','futureFittedModularCabinetJoinsShouldUseLayeredJoinTreatment'])assert.equal(decision.approvedContract[flag],true,`${flag} changed`)
assert.equal(decision.approvedContract.defaultTreatment,'seamless');assert.deepEqual(decision.approvedContract.countertopRowsInclusive,[134,145]);assert.equal(decision.approvedContract.minimumOverlapPixels,-6);assert.equal(decision.approvedContract.maximumGapPixels,8)
for(const flag of ['kitchenModularCountertopJoinAuthorityApproved','v11V19V20V21RemainImmutable'])assert.equal(decision.approvalBoundary[flag],true)
for(const flag of ['finalChanged','runtimeChanged','productionAssetsChanged','promotionPerformed','promotionAllowedWithoutSeparateInstruction'])assert.equal(decision.approvalBoundary[flag],false,`${flag} boundary changed`)
const page=fs.readFileSync(file(rel.page),'utf8');assert.match(page,/V22 · seamless cap/);assert.match(page,/No source pixels amended/);assert.match(page,/background → body backfill → cabinet sprites → countertop cap → optional soft seam/)
console.log('Kitchen Countertop Join Cap V22 approval verified: exact seamless layered join method is approved and hash-pinned; source sprites, Final and runtime remain unchanged.')
