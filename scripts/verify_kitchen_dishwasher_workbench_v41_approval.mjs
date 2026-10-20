#!/usr/bin/env node
/** Pin Frank's exact Dishwasher Workbench V41 approval. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root=process.cwd(),approval=JSON.parse(fs.readFileSync(path.join(root,'docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json')))
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')
assert.equal(approval.schema,'lighthouse-keeper/kitchen-review-approval@1');assert.equal(approval.set,'kitchen-dishwasher-workbench-v41');assert.equal(approval.approvedBy,'Frank');assert.equal(approval.approvalWords,'Dishwasher V41 is approved.');assert.equal(approval.commit,'d997c11b12032b4a48b8350ec08d32ed1746722a');assert.equal(approval.promotion,'none');assert.equal(approval.runtimeChanged,false);assert.equal(approval.finalChanged,false)
for(const [key,file] of Object.entries({candidateCatalogue:'art/drafts/kitchen-dishwasher-workbench-2026-10-20-v41/candidate-catalogue.json',reviewShell:'public/keeper-review/kitchen-dishwasher-workbench-v41/index.html',archiveManifest:'review-archive/sets/kitchen-dishwasher-workbench-v41.json',dishwasherOff:'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/dishwasher-off.png',dishwasherOn:'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/dishwasher-on.png',dishwasherBroken:'art/raw/kitchen-dishwasher-workbench-2026-10-20-v41/dishwasher-broken.png'}))assert.equal(sha(file),approval.hashes[key],`${key} approval hash drifted`)
console.log('Kitchen Dishwasher Workbench V41 approval verified: exact art, Broken movement lock and asset-local effect ownership are pinned.')
