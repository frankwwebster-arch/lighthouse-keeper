#!/usr/bin/env node
/** Verify Frank's immutable approval of exact stop → walk → stop V1. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2')
const REGISTER = path.join(PACK, 'batch-register.json')
const V1_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-stop-walk-stop-v2')
const ROUTE = '/keeper-review/keeper-prime-stop-walk-stop-v2'
const fail = (message: string): never => { throw new Error(`Keeper Prime stop-walk-stop V2 approval: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V1_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v1 = JSON.parse(fs.readFileSync(V1_REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stop-walk-stop-2026-10-14-v2' || record.status !== 'approved-stop-walk-stop-v1-route-authority') fail('identity/status changed')
if (record.approval?.approvedBy !== 'Frank' || record.approval?.approvedOn !== '2026-10-14' || record.approval?.wording !== 'approved') fail('approval wording changed')
if (record.approvedCandidate?.registerSha256 !== hash(V1_REGISTER)) fail('V1 register provenance changed')
if (JSON.stringify(record.approvedCandidate.transition) !== JSON.stringify(v1.transition) || JSON.stringify(record.approvedCandidate.rootMotion) !== JSON.stringify(v1.rootMotion)) fail('approved transition or root motion changed')
if (record.approvedCandidate.rootMotion.route.length !== 32 || record.approvedCandidate.rootMotion.route.at(-1)?.x !== 412 || record.approvedCandidate.rootMotion.walkingOnSpotFrames !== 0) fail('approved route contract changed')
for (const direction of ['forward', 'reverse']) {
  const item = record.approvedCandidate.transition[direction]
  if (hash(path.join(ROOT, item.strip)) !== item.sha256 || hash(path.join(ROOT, item.sidecar)) !== item.sidecarSha256) fail(`${direction} strip/sidecar changed`)
}
for (const bridge of record.approvedCandidate.transition.bridgeFrames as Record<string, any>[]) if (hash(path.join(ROOT, bridge.file)) !== bridge.sha256) fail(`bridge F${bridge.frame} changed`)
for (const asset of record.reviewSurface.publicAssets as Record<string, any>[]) if (hash(path.join(ROOT, asset.file)) !== asset.sha256) fail(`public asset changed: ${asset.file}`)
const page = path.join(ROOT, record.reviewSurface.publicPage)
if (hash(page) !== record.reviewSurface.publicPageSha256) fail('approval page changed')
const html = fs.readFileSync(page, 'utf8')
for (const phrase of ['approved stop → walk → stop authority', 'Approved core transition authority · 14 October 2026', 'Frank approved exact stop → walk → stop V1', 'Final and production remain unchanged']) if (!html.includes(phrase)) fail(`approval page omits ${phrase}`)
if (html.includes('/keeper-review/keeper-prime-stop-walk-stop-v1/assets/')) fail('approval page still references V1 route')
for (const asset of record.reviewSurface.publicAssets as Record<string, any>[]) if (!html.includes(`${ROUTE}/assets/${path.basename(asset.file)}`) && !path.basename(asset.file).startsWith('contact-') && !path.basename(asset.file).includes('strip-')) fail(`approval page omits ${path.basename(asset.file)}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['v1RegisterUnchanged', 'allTransitionHashesPinned', 'rootMotionPinned', 'publicAssetsByteIdenticalToV1', 'approvalPackDuplicatesNoArtwork']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['artPixelsChangedByV2', 'timingChangedByV2', 'productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV6Approved', 'stopToWalkApproved', 'walkToStopApproved', 'completeRouteApproved', 'coreTransitionAuthority', 'finalLaneEntryAllowed']) if (record.approvalBoundary?.[flag] !== true) fail(`${flag} approval changed`)
if (record.approvalBoundary?.productionPromotionAllowed !== false) fail('production promotion changed')
for (const forbidden of ['drafts', 'sources', 'evidence', 'palette']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval pack duplicates art in ${forbidden}`)
console.log('Keeper Prime stop-walk-stop V2 approval verified: exact V1 route, reversible bridge, root motion and public assets pinned; Final and production unchanged.')
