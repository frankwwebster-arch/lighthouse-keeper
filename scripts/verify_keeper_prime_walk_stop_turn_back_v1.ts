#!/usr/bin/env node
/** Verify the exact-authority Keeper Prime walk → stop → turn away V1 route. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-stop-turn-back-v1')
const PREFIX = '/keeper-review/keeper-prime-walk-stop-turn-back-v1/assets/'
const fail = (message: string): never => { throw new Error(`Keeper Prime walk-stop-turn-back V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-walk-stop-turn-back-2026-10-14-v1' || record.status !== 'draft-walk-stop-turn-back-v1-awaiting-visual-approval') fail('identity/status changed')
for (const [name, authority] of Object.entries(record.authorities) as [string, Record<string, any>][]) {
  if (hash(path.join(ROOT, authority.approval)) !== authority.approvalSha256) fail(`${name} approval changed`)
}
if (hash(path.join(ROOT, record.authorities.timing.policy)) !== record.authorities.timing.policySha256) fail('timing policy changed')
const profile = record.authorities.timing.profile
if (JSON.stringify(profile) !== JSON.stringify({ walkFps: 10, decelerationFps: 12, settleMs: 0, turnFps: 16, frontHoldMs: 625 })) fail('Fast Timing V1 changed')

const sidecarPath = path.join(ROOT, record.join.sidecar)
const stripPath = path.join(ROOT, record.join.strip)
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
if (record.join.frames !== 13 || record.join.runtimeEntryFrameAfterWalkLoop !== 2) fail('join contract changed')
if (hash(stripPath) !== record.join.sha256 || hash(sidecarPath) !== record.join.sidecarSha256 || sidecar.sha256 !== record.join.sha256 || sidecar.frames !== 13 || sidecar.runtimeEntryFrameAfterWalkLoop !== 2) fail('join strip/sidecar changed')
if (JSON.stringify(sidecar.rootMotionHighResolutionPixels) !== '[0,18,12,6,2,0,0,0,0,0,0,0,0]') fail('join root-motion order changed')
if (JSON.stringify(sidecar.frameSha256) !== JSON.stringify(record.join.frameSha256) || JSON.stringify(sidecar.frameDurationsMs) !== JSON.stringify(record.join.frameDurationsMs)) fail('join frame/timing order changed')
const expectedJoinDurations = [100, ...Array(4).fill(1000 / 12), ...Array(8).fill(62.5)]
if (JSON.stringify(record.join.frameDurationsMs) !== JSON.stringify(expectedJoinDurations)) fail('join timing does not match Fast Timing V1')

const strip = PNG.sync.read(fs.readFileSync(stripPath))
if (strip.width !== 3328 || strip.height !== 320) fail('join strip geometry changed')
for (const [index, sourceHash] of (record.join.frameSha256 as string[]).entries()) {
  const published = (record.publishedAssets as Record<string, any>[]).find(asset => asset.sourceSha256 === sourceHash && asset.source.endsWith('.png') && !asset.source.includes('/evidence/'))
  if (!published) fail(`join F${index + 1} source missing`)
  const source = PNG.sync.read(fs.readFileSync(path.join(ROOT, published.source)))
  if (source.width !== 256 || source.height !== 320) fail(`join F${index + 1} source geometry changed`)
  for (let x = 0; x < 256; x += 1) if (source.data[x * 4 + 3] || source.data[((319 * 256 + x) * 4) + 3]) fail(`join F${index + 1} horizontal edge alpha`)
  for (let y = 1; y < 319; y += 1) if (source.data[(y * 256) * 4 + 3] || source.data[(y * 256 + 255) * 4 + 3]) fail(`join F${index + 1} vertical edge alpha`)
  for (let y = 0; y < 320; y += 1) {
    const actual = strip.data.subarray(((y * 3328) + index * 256) * 4, ((y * 3328) + index * 256 + 256) * 4)
    const expected = source.data.subarray(y * 256 * 4, (y + 1) * 256 * 4)
    if (!actual.equals(expected)) fail(`join strip F${index + 1} disagrees with source`)
  }
}

for (const endpoint of [record.endpointContract.walkContact, record.endpointContract.sideStop, record.endpointContract.rear]) {
  if (hash(path.join(ROOT, endpoint.file)) !== endpoint.sha256) fail(`endpoint changed: ${endpoint.file}`)
}
if (hash(path.join(ROOT, record.endpointContract.sideStop.turnEntry)) !== record.endpointContract.sideStop.turnEntrySha256) fail('turn entry changed')
const alphaBounds = (file: string) => {
  const png = PNG.sync.read(fs.readFileSync(file)); let minX = png.width; let minY = png.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) if (png.data[(y * png.width + x) * 4 + 3]) { minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y) }
  return [minX, minY, maxX + 1, maxY + 1]
}
if (JSON.stringify(alphaBounds(path.join(ROOT, record.endpointContract.sideStop.file))) !== JSON.stringify(alphaBounds(path.join(ROOT, record.endpointContract.sideStop.turnEntry)))) fail('side stop and turn entry geometry no longer align')

const route = record.route.framesData as Record<string, any>[]
if (route.length !== 32 || record.route.distanceHighResolutionPixels !== 374 || record.route.walkCycles !== 2 || record.route.neutralSettleFrames !== 0 || record.route.turnFramesAfterSharedEndpoint !== 8 || record.route.rearHoldFrames !== 4 || record.route.rootMotionStopsBeforeTurn !== true) fail('route summary changed')
const expectedDeltas = [...Array(16).fill(21), 18, 12, 6, 2, ...Array(12).fill(0)]
if (JSON.stringify(route.map(frame => frame.dx)) !== JSON.stringify(expectedDeltas)) fail('route displacement schedule changed')
const expectedDurations = [...Array(16).fill(100), ...Array(4).fill(1000 / 12), ...Array(8).fill(62.5), ...Array(4).fill(156.25)]
if (JSON.stringify(route.map(frame => frame.durationMs)) !== JSON.stringify(expectedDurations)) fail('route timing schedule changed')
if (Math.abs(record.route.durationMs - 3058.3333333333335) > 0.001) fail('route duration changed')
let position = 0; let turnStarted = false
for (const [index, frame] of route.entries()) {
  position += frame.dx
  if (frame.x !== position || !frame.src.startsWith(PREFIX)) fail(`route F${index + 1} position/path changed`)
  if (frame.phase === 'approved turn away') turnStarted = true
  if (turnStarted && frame.dx !== 0) fail(`root motion continues after turn starts at F${index + 1}`)
}
if (position !== 374) fail('route distance changed')

for (const asset of record.publishedAssets as Record<string, any>[]) {
  if (hash(path.join(ROOT, asset.source)) !== asset.sourceSha256 || hash(path.join(ROOT, asset.public)) !== asset.publicSha256 || asset.sourceSha256 !== asset.publicSha256 || asset.byteIdentical !== true) fail(`published asset changed: ${asset.public}`)
}
if (hash(path.join(ROOT, record.unchangedAuthorities.runtimeManifest)) !== record.unchangedAuthorities.runtimeManifestSha256) fail('runtime manifest changed')
if (hash(path.join(ROOT, record.unchangedAuthorities.workbenchCatalogue)) !== record.unchangedAuthorities.workbenchCatalogueSha256) fail('workbench catalogue changed')
const page = path.join(ROOT, record.reviewPage.file)
if (hash(page) !== record.reviewPage.sha256 || record.reviewPage.assetPrefix !== PREFIX || record.reviewPage.relativeAssetUrls !== false || record.reviewPage.largeLaneFullWidth !== true || record.reviewPage.gameLaneFullWidth !== true) fail('review page record changed')
const html = fs.readFileSync(page, 'utf8')
for (const phrase of ['walk → stop → turn fully away V1', 'Fast Timing V1', 'Exact proposed game scale', 'Isolated loop exit → full back', 'Previous frame', 'Next frame', 'no stationary duplicate', 'Draft only; Workbench Final, production sprites and runtime manifest remain unchanged']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/')) fail('relative public asset URL remains')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['allArtworkCopiedFromApprovedAuthorities', 'walkToDecelerationContactExact', 'turnFramesExact', 'rearEndpointExact', 'rootMotionStopsBeforeTurn', 'transparentSafetyGutters', 'stripSidecarAgreement', 'fastTimingV1Exact']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
if (record.validation?.newCharacterDrawings !== false) fail('new-character-art boundary changed')
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (record.approvalBoundary?.sourceAuthoritiesApproved !== true || record.approvalBoundary?.compositeRouteApproved !== false || record.approvalBoundary?.finalLaneEntryAllowed !== false || record.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
console.log('Keeper Prime walk-stop-turn-back V1 verified: approved source frames, Fast Timing V1, 13-frame join, 32-frame route, zero root motion during turn, gutters/public assets exact, no promotion.')
