#!/usr/bin/env node
/** Verify Frank's immutable approval of Ladder Transition V4 and deferred turn timing. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const approvalFile = path.join(root, 'docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v4-approval] ${message}`) }
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

if (!fs.existsSync(approvalFile)) fail('approval record missing')
const approval = read(approvalFile)
if (approval.schema !== 'lighthouse-keeper/review-approval@1' || approval.candidate !== 'keeper-prime-ladder-transitions-v4') fail('approval identity changed')
if (approval.approvedBy !== 'Frank' || approval.approvedOn !== '2026-10-16') fail('approver/date changed')
if (approval.wording !== 'Approved. Turn should be twice as fast but that can be fixed another time.') fail('approval wording changed')

for (const key of ['candidateRegister', 'candidateSpec', 'reviewPage']) {
  const authority = approval[key]
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}
const register = read(path.join(root, approval.candidateRegister.file))
const spec = read(path.join(root, approval.candidateSpec.file))
if (register.publishedAssets.length !== 29 || approval.approvedAssets.uniqueFrames !== 29) fail('approved asset inventory changed')
for (const asset of register.publishedAssets) {
  const file = path.join(root, asset.draft)
  if (!fs.existsSync(file) || sha(file) !== asset.draftSha256) fail(`approved asset changed: ${asset.draft}`)
}
const turnFrames = Object.values<any>(spec.routes).flatMap((route: any) => route.frames).filter((frame: any) => frame.phase?.includes('turn'))
if (!turnFrames.length || turnFrames.some((frame: any) => frame.durationMs !== 50)) fail('approved current turn timing changed')
if (approval.timing.currentTurnFrameDurationMs !== 50 || approval.timing.currentTurnFps !== 20 || approval.timing.deferredRequestedTurnFrameDurationMs !== 25 || approval.timing.deferredRequestedTurnFps !== 40 || approval.timing.implementedByThisApproval !== false) fail('deferred timing note changed')
if (!approval.approvalBoundary.candidateApproved || !approval.approvalBoundary.visualAndTransitionAuthorityApproved || approval.approvalBoundary.turnTimingFinal || !approval.approvalBoundary.finalLaneEntryAllowed || approval.approvalBoundary.promotionPerformed) fail('approval boundary changed')
if (approval.promotion.finalChanged || approval.promotion.runtimeChanged || approval.promotion.productionChanged) fail('approval performed a promotion')

console.log('Keeper Prime ladder transitions V4 approval verified: 29 exact frames, complete-ladder persistent compositor and routes approved; 25-ms turn timing deferred; no Final/runtime/production promotion.')
