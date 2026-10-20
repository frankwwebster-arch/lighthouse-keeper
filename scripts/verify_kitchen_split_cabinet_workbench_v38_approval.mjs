#!/usr/bin/env node
/** Pin Frank's exact V38 modular-cabinet approval. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root=process.cwd(),approval=JSON.parse(fs.readFileSync(path.join(root,'docs/review/kitchen-split-cabinet-workbench-v38-approval-2026-10-20.json')))
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')
assert.equal(approval.schema,'lighthouse-keeper/kitchen-review-approval@1');assert.equal(approval.set,'kitchen-split-cabinet-workbench-v38');assert.equal(approval.approvedBy,'Frank');assert.equal(approval.approvalWords,'Fantastic.');assert.equal(approval.promotion,'none');assert.equal(approval.runtimeChanged,false);assert.equal(approval.finalChanged,false)
for(const [key,file] of Object.entries({candidateCatalogue:'art/drafts/kitchen-split-cabinet-workbench-2026-10-20-v38/candidate-catalogue.json',reviewShell:'public/keeper-review/kitchen-split-cabinet-workbench-v38/index.html',archiveManifest:'review-archive/sets/kitchen-split-cabinet-workbench-v38.json',cabinetAExposed:'art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38/cabinet-a-le-re.png',cabinetBExposed:'art/raw/kitchen-split-cabinet-workbench-2026-10-20-v38/cabinet-b-le-re.png'}))assert.equal(sha(file),approval.hashes[key],`${key} approval hash drifted`)
console.log('Kitchen Split Cabinet Workbench V38 approval verified: exact independent bays and two-sided healing are pinned.')
