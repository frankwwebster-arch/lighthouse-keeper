#!/usr/bin/env node
/** Verify the approval-only Keeper Prime walk-stop-turn-back V3 record. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime walk-stop-turn-back V3: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-walk-stop-turn-back-2026-10-14-v3' || record.status !== 'approved-walk-stop-turn-back-v2-route-authority') fail('identity/status changed')
if (record.approval?.wording !== 'good now working fine. approved.' || record.approval?.approvedBy !== 'Frank' || record.approval?.approvedOn !== '2026-10-14') fail('approval provenance changed')
const candidate = record.approvedCandidate
for (const [fileKey, hashKey] of [['register', 'registerSha256'], ['reviewPage', 'reviewPageSha256'], ['joinStrip', 'joinStripSha256'], ['joinSidecar', 'joinSidecarSha256']] as const) if (hash(path.join(ROOT, candidate[fileKey])) !== candidate[hashKey]) fail(`${fileKey} authority changed`)
const source = JSON.parse(fs.readFileSync(path.join(ROOT, candidate.register), 'utf8')) as Record<string, any>
for (const key of ['frames', 'durationMs', 'distanceHighResolutionPixels', 'walkCycles', 'neutralSettleFrames', 'turnFramesAfterSharedEndpoint', 'rearHoldFrames']) if (candidate[key] !== source.route[key]) fail(`${key} differs from V2`)
if (JSON.stringify(candidate.decelerationDeltas) !== JSON.stringify(source.route.decelerationDeltas) || candidate.preloadedBeforePlayback !== source.validation.preloadedBeforePlayback) fail('route/preload summary differs from V2')
for (const authority of Object.values(record.unchangedAuthorities) as string[]) if (typeof authority !== 'string') fail('invalid unchanged-authority value')
if (hash(path.join(ROOT, record.unchangedAuthorities.runtimeManifest)) !== record.unchangedAuthorities.runtimeManifestSha256 || hash(path.join(ROOT, record.unchangedAuthorities.workbenchCatalogue)) !== record.unchangedAuthorities.workbenchCatalogueSha256) fail('runtime or workbench authority changed')
if (record.approvalBoundary?.compositeRouteApproved !== true || record.approvalBoundary?.finalLaneEntryAllowed !== false || record.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
for (const flag of ['artPixelsChangedByV3', 'timingChangedByV3', 'productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
console.log('Keeper Prime walk-stop-turn-back V3 verified: Frank approval pinned to exact preload-safe V2, with no artwork, timing, Final or production change.')
