#!/usr/bin/env node
/** Verify the exact-authority Keeper Prime walk → stop → turn front V1 route. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-stop-turn-front-v1')
const PREFIX = '/keeper-review/keeper-prime-walk-stop-turn-front-v1/assets/'
const fail = (message: string): never => { throw new Error(`Keeper Prime walk-stop-turn-front V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-walk-stop-turn-front-2026-10-14-v1' || record.status !== 'draft-walk-stop-turn-front-v1-awaiting-visual-approval') fail('identity/status changed')
for (const [name, authority] of Object.entries(record.authorities) as [string, Record<string, any>][]) if (hash(path.join(ROOT, authority.approval)) !== authority.approvalSha256) fail(`${name} approval changed`)
if (record.authorities.frontSideTurn.acceptedLimitation !== 'very slight visual jump around 45°') fail('accepted turn limitation changed')

const sidecarPath = path.join(ROOT, record.join.sidecar)
const stripPath = path.join(ROOT, record.join.strip)
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
if (record.join.frames !== 13 || record.join.fps !== 8 || record.join.runtimeEntryFrameAfterWalkLoop !== 2) fail('join contract changed')
if (hash(stripPath) !== record.join.sha256 || hash(sidecarPath) !== record.join.sidecarSha256 || sidecar.sha256 !== record.join.sha256 || sidecar.frames !== 13 || sidecar.fps !== 8 || sidecar.runtimeEntryFrameAfterWalkLoop !== 2) fail('join strip/sidecar changed')
if (JSON.stringify(sidecar.rootMotionHighResolutionPixels) !== '[0,18,12,6,2,0,0,0,0,0,0,0,0]' || JSON.stringify(sidecar.frameSha256) !== JSON.stringify(record.join.frameSha256)) fail('join frame/root-motion order changed')
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
if (record.endpointContract.sideStop.sha256 !== record.endpointContract.sideStop.turnSideEndpointSha256 || record.endpointContract.sideStop.byteIdenticalAcrossDecelerationAndTurn !== true) fail('stop/turn side endpoint seam changed')
for (const endpoint of [record.endpointContract.walkContact, record.endpointContract.sideStop, record.endpointContract.front]) if (hash(path.join(ROOT, endpoint.file)) !== endpoint.sha256) fail(`endpoint changed: ${endpoint.file}`)

const route = record.route.framesData as Record<string, any>[]
if (route.length !== 32 || record.route.distanceHighResolutionPixels !== 374 || record.route.walkCycles !== 2 || record.route.neutralSettleFrames !== 1 || record.route.turnFramesAfterSharedEndpoint !== 7 || record.route.frontHoldFrames !== 4 || record.route.rootMotionStopsBeforeTurn !== true) fail('route summary changed')
const expectedDeltas = [...Array(16).fill(21), 18, 12, 6, 2, ...Array(12).fill(0)]
if (JSON.stringify(route.map(frame => frame.dx)) !== JSON.stringify(expectedDeltas)) fail('route displacement schedule changed')
let x = 0
let turnStarted = false
for (const [index, frame] of route.entries()) {
  x += frame.dx
  if (frame.x !== x || !frame.src.startsWith(PREFIX)) fail(`route F${index + 1} position/path changed`)
  if (frame.phase === 'approved turn to camera') turnStarted = true
  if (turnStarted && frame.dx !== 0) fail(`root motion continues after turn starts at F${index + 1}`)
}
if (x !== 374) fail('route distance changed')

for (const asset of record.publishedAssets as Record<string, any>[]) {
  if (hash(path.join(ROOT, asset.source)) !== asset.sourceSha256 || hash(path.join(ROOT, asset.public)) !== asset.publicSha256 || asset.sourceSha256 !== asset.publicSha256 || asset.byteIdentical !== true) fail(`published asset changed: ${asset.public}`)
}
const page = path.join(ROOT, record.reviewPage.file)
if (hash(page) !== record.reviewPage.sha256 || record.reviewPage.assetPrefix !== PREFIX || record.reviewPage.relativeAssetUrls !== false) fail('review page record changed')
const html = fs.readFileSync(page, 'utf8')
for (const phrase of ['walk → stop → turn to camera V1', 'Exact proposed game scale', 'Isolated loop exit → full face', 'Previous frame', 'Next frame', 'one-frame neutral beat', 'character must cease translating before rotation begins', 'Draft only; Final and production remain unchanged']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/')) fail('relative public asset URL remains')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['allArtworkCopiedFromApprovedAuthorities', 'walkToDecelerationContactExact', 'decelerationToTurnSideEndpointExact', 'turnFrontEndpointExact', 'rootMotionStopsBeforeTurn', 'transparentSafetyGutters', 'stripSidecarAgreement']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
if (record.validation?.newCharacterDrawings !== false) fail('new-character-art boundary changed')
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (record.approvalBoundary?.sourceAuthoritiesApproved !== true || record.approvalBoundary?.compositeRouteApproved !== false || record.approvalBoundary?.finalLaneEntryAllowed !== false || record.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
console.log('Keeper Prime walk-stop-turn-front V1 verified: exact approved source frames, 13-frame join, 32-frame route, root motion stopped before turn, gutters/public assets exact, no promotion.')
