#!/usr/bin/env node
/** Verify the reversible Keeper Prime stop → walk → stop V1 route. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const WALK_V6_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v6/batch-register.json')
const WALK_V7_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-stop-walk-stop-v1')
const PREFIX = '/keeper-review/keeper-prime-stop-walk-stop-v1/assets/'
const fail = (message: string): never => { throw new Error(`Keeper Prime stop-walk-stop V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, WALK_V6_REGISTER, WALK_V7_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const walk = JSON.parse(fs.readFileSync(WALK_V6_REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stop-walk-stop-2026-10-14-v1' || record.status !== 'draft-stop-walk-stop-v1-awaiting-visual-approval') fail('identity/status changed')
if (record.approvedWalkAuthority?.registerSha256 !== hash(WALK_V6_REGISTER) || record.approvedWalkAuthority?.approvalRecordSha256 !== hash(WALK_V7_REGISTER)) fail('approved walk provenance changed')
if (record.stopAuthority?.sha256 !== hash(path.join(ROOT, record.stopAuthority.file))) fail('stop authority changed')
for (const source of record.generation.selectedSources as Record<string, any>[]) if (hash(path.join(ROOT, source.file)) !== source.sha256) fail(`generated source changed: ${source.file}`)

const frameFiles = Array.from({ length: 5 }, (_, index) => path.join(PACK, `drafts/frames/keeper_prime_stop-to-walk-right_f${index + 1}.png`))
const frameHashes = frameFiles.map((file, index) => {
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`transition F${index + 1} geometry changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[((319 * 256 + x) * 4) + 3]) fail(`transition F${index + 1} horizontal edge alpha`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`transition F${index + 1} vertical edge alpha`)
  return hash(file)
})
if (frameHashes[0] !== record.stopAuthority.sha256 || frameHashes[4] !== walk.frames[0].sha256) fail('exact stop/Walk F1 endpoints changed')
if (record.transition.startStopSha256 !== frameHashes[0] || record.transition.finalStopSha256 !== frameHashes[0] || record.transition.identicalStopEndpoints !== true) fail('stop endpoints are not byte-identical')
for (const [index, bridge] of (record.transition.bridgeFrames as Record<string, any>[]).entries()) {
  if (bridge.frame !== index + 2 || bridge.sha256 !== frameHashes[index + 1] || bridge.edgeAlphaPixels !== 0 || bridge.registration?.creativeWarp !== false) fail(`bridge F${index + 2} record changed`)
}

const strips = [record.transition.forward, record.transition.reverse] as Record<string, any>[]
for (const [stripIndex, item] of strips.entries()) {
  const file = path.join(ROOT, item.strip)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (hash(file) !== item.sha256 || png.width !== 1280 || png.height !== 320) fail(`${stripIndex ? 'reverse' : 'forward'} strip changed`)
  const expected = stripIndex ? [...frameFiles].reverse() : frameFiles
  for (let frame = 0; frame < 5; frame += 1) {
    const source = PNG.sync.read(fs.readFileSync(expected[frame]))
    for (let y = 0; y < 320; y += 1) {
      const actualRow = png.data.subarray(((y * 1280) + frame * 256) * 4, ((y * 1280) + frame * 256 + 256) * 4)
      const sourceRow = source.data.subarray(y * 256 * 4, (y + 1) * 256 * 4)
      if (!actualRow.equals(sourceRow)) fail(`${stripIndex ? 'reverse' : 'forward'} strip F${frame + 1} disagrees with source`)
    }
  }
  const sidecarPath = path.join(ROOT, item.sidecar)
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
  const expectedHashes = stripIndex ? [...frameHashes].reverse() : frameHashes
  if (hash(sidecarPath) !== item.sidecarSha256 || sidecar.sha256 !== item.sha256 || sidecar.frames !== 5 || sidecar.fps !== 8 || JSON.stringify(sidecar.frameSha256) !== JSON.stringify(expectedHashes)) fail(`${stripIndex ? 'reverse' : 'forward'} sidecar disagrees`)
}

const motion = record.rootMotion
if (motion.bakedIntoStrips !== false || motion.fps !== 8 || JSON.stringify(motion.accelerationDeltasHighResolutionPixels) !== '[2,6,12,18]' || motion.walkDeltaHighResolutionPixels !== 21 || JSON.stringify(motion.decelerationDeltasHighResolutionPixels) !== '[18,12,6,2]' || motion.firstMovementFrameDelta !== 2 || motion.walkingOnSpotFrames !== 0) fail('root-motion contract changed')
const route = motion.route as Record<string, any>[]
if (route.length !== 32 || route[0].x !== 0 || route.at(-1)?.x !== 412) fail('route length/distance changed')
const expectedDeltas = [0, 0, 0, 0, 2, 6, 12, 18, ...Array(16).fill(21), 18, 12, 6, 2, 0, 0, 0, 0]
if (JSON.stringify(route.map(frame => frame.dx)) !== JSON.stringify(expectedDeltas)) fail('route displacement schedule changed')
let cumulative = 0
for (const [index, frame] of route.entries()) {
  cumulative += frame.dx
  if (frame.x !== cumulative || !frame.src.startsWith(PREFIX)) fail(`route F${index + 1} position/path changed`)
  if (frame.phase !== 'stopped hold' && frame.dx <= 0) fail(`gait frame ${index + 1} walks on the spot`)
}

for (const asset of record.publishedAssets as Record<string, any>[]) {
  if (hash(path.join(ROOT, asset.source)) !== asset.sourceSha256 || hash(path.join(ROOT, asset.public)) !== asset.publicSha256 || asset.sourceSha256 !== asset.publicSha256 || asset.byteIdentical !== true) fail(`published asset changed: ${asset.public}`)
}
const page = path.join(ROOT, record.reviewPage.file)
if (hash(page) !== record.reviewPage.sha256 || record.reviewPage.assetPrefix !== PREFIX || record.reviewPage.relativeAssetUrls !== false) fail('review page record changed')
const html = fs.readFileSync(page, 'utf8')
for (const phrase of ['Keeper Prime · stop → walk → stop V1', 'Exact proposed game scale', 'Isolated reversible bridge', 'Previous frame', 'Next frame', 'no walking on the spot', 'Walk V6 is approved authority', 'not Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/')) fail('relative public asset URL remains')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['approvedWalkV6Unchanged', 'stopAuthorityUnchanged', 'startAndFinalStopByteIdentical', 'walkToStopIsExactBridgeReverse', 'movementBeginsOnFirstGaitFrame', 'transparentSafetyGutters', 'stripSidecarAgreement']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['stopToWalkApproved', 'walkToStopApproved', 'completeRouteApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (record.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)
console.log('Keeper Prime stop-walk-stop V1 verified: exact endpoints, reversible bridge, 32-frame root-motion route, transparent gutters, strips/sidecars/public assets, and no promotion.')
