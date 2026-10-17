#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-front-v1'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v1')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const rightPack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const rightRegisterFile = path.join(rightPack, 'batch-register.json')
const rightRouteFile = path.join(rightPack, 'keeper-prime-sit-stand-side-v2.json')
const sideLeftApprovalFile = path.join(root, 'docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json')
const turnRegisterFile = path.join(root, 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v1/batch-register.json')
const standingFrontFile = path.join(root, 'art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png')
const seatedFrontFile = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-front_f01.png')
const historicalFile = path.join(root, 'art/raw/keeper-first-batch/keeper_sit_front_f6.png')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const generated = [2, 3, 4, 5].map((n) => path.join(pack, `sources/generated/front-f${n}-generated.png`))
const targetSizes = [[157, 286], [167, 276], [172, 268], [160, 264]]
const actionRootXLp = 86
const floorWorldYLp = 52

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [rightRegisterFile, rightRouteFile, sideLeftApprovalFile, turnRegisterFile, standingFrontFile, seatedFrontFile, historicalFile, reviewRouteFile, ...generated]) {
  if (!fs.existsSync(file)) throw new Error(`Missing required input ${rel(file)}`)
}
const rightRegister = readJson(rightRegisterFile)
const rightRoute = readJson(rightRouteFile)
const sideLeftApproval = readJson(sideLeftApprovalFile)
const turnRegister = readJson(turnRegisterFile)
if (sideLeftApproval.decision !== 'approved-as-side-left-prime-sit-stand-authority') throw new Error('Side-left approval is not pinned')
if (turnRegister.frames.length !== 8 || turnRegister.frames[0].sha256 !== sha(standingFrontFile)) throw new Error('Front/side turn authority changed')

function alphaBounds(png, threshold = 0) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1, opaquePixels = 0
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (png.data[(y * png.width + x) * 4 + 3] <= threshold) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); opaquePixels += 1
  }
  if (maxX < 0) throw new Error('Empty sprite cell')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaquePixels }
}

function edgeAlphaCount(png) {
  let count = 0
  for (let x = 0; x < png.width; x += 1) {
    if (png.data[x * 4 + 3]) count += 1
    if (png.data[((png.height - 1) * png.width + x) * 4 + 3]) count += 1
  }
  for (let y = 1; y < png.height - 1; y += 1) {
    if (png.data[(y * png.width) * 4 + 3]) count += 1
    if (png.data[(y * png.width + png.width - 1) * 4 + 3]) count += 1
  }
  return count
}

function inspect(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  const bounds = alphaBounds(png)
  return {
    cellPixels: [png.width, png.height], bounds, edgeAlphaPixels: edgeAlphaCount(png),
    transparentGutterPx: Math.min(bounds.minX, bounds.minY, png.width - 1 - bounds.maxX, png.height - 1 - bounds.maxY),
  }
}

function registerGenerated(source, output, width, height) {
  const sourcePng = PNG.sync.read(fs.readFileSync(source))
  const bounds = alphaBounds(sourcePng, 8)
  const filter = `crop=${bounds.width}:${bounds.height}:${bounds.minX}:${bounds.minY},scale=${width}:${height}:flags=lanczos,pad=256:320:(ow-iw)/2:316-ih:color=0x00000000`
  const result = spawnSync('/opt/homebrew/bin/ffmpeg', ['-loglevel', 'error', '-y', '-i', source, '-vf', filter, '-frames:v', '1', output], { encoding: 'utf8' })
  if (result.status !== 0) throw new Error(`ffmpeg registration failed for ${rel(source)}: ${result.stderr}`)
  return { sourceCanvas: [sourcePng.width, sourcePng.height], sourceAlphaBounds: bounds, registeredSize: [width, height], targetAxisX: 128, targetFloorY: 315, filter: 'Lanczos', creativePixelWarp: false }
}

function saveStrip(file, frames) {
  const strip = new PNG({ width: 256 * frames.length, height: 320 })
  frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame)), strip, 0, 0, 256, 320, index * 256, 0))
  fs.writeFileSync(file, PNG.sync.write(strip))
}

fs.mkdirSync(frameDir, { recursive: true })
fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const actionFiles = [1, 2, 3, 4, 5, 6].map((n) => path.join(frameDir, `keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`))
fs.copyFileSync(standingFrontFile, actionFiles[0])
generated.forEach((source, index) => registerGenerated(source, actionFiles[index + 1], ...targetSizes[index]))
fs.copyFileSync(seatedFrontFile, actionFiles[5])

const actionRecords = actionFiles.map((file, index) => {
  const metrics = inspect(file)
  const source = index === 0 ? standingFrontFile : index === 5 ? seatedFrontFile : generated[index - 1]
  const registration = index > 0 && index < 5 ? registerGenerated(source, file, ...targetSizes[index - 1]) : null
  const record = { frame: index + 1, file: rel(file), sha256: sha(file), source: rel(source), sourceSha256: sha(source), registration, ...metrics }
  writeJson(file.replace(/\.png$/, '.json'), {
    schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-front_f${String(index + 1).padStart(2, '0')}`,
    w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315,
    view: 'front', outfit: 'standard-single-band', poseIndex: index + 1,
    derivation: index === 0 ? 'exact-approved-prime-standing-front' : index === 5 ? 'exact-registered-prime-seated-front' : 'new-Prime-derived-front-sit-intermediate',
    source: record.source, sourceSha256: record.sourceSha256, sha256: record.sha256, registration,
    ownership: { actorAndClothing: 'all non-transparent pixels in this isolated cell', propPixels: 0, effectPixels: 0 },
    endpointAuthority: index === 0 ? 'approved Prime standing-front' : index === 5 ? 'registered Prime seated-front' : null,
    productionPromotionAllowed: false,
  })
  return record
})
if (actionRecords.some((record) => record.cellPixels[0] !== 256 || record.cellPixels[1] !== 320 || record.edgeAlphaPixels !== 0 || record.transparentGutterPx < 4)) throw new Error('Front action frame isolation failure')
if (actionRecords[0].sha256 !== sha(standingFrontFile) || actionRecords[5].sha256 !== sha(seatedFrontFile)) throw new Error('Front action endpoints are not exact')

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-front_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-front_f6.png')
saveStrip(forwardStrip, actionFiles); saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-front', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-standing-front', endPose: 'neutral-sitting-front', sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-front', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-sitting-front', endPose: 'neutral-standing-front', sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-front-contact-sheet.png')
saveStrip(contactSheet, actionFiles)

const publishedByHash = new Map()
const publishedAssets = []
function publish(file, label) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`
  fs.copyFileSync(file, path.join(assetsDir, filename))
  const url = reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}`
  const entry = { source: rel(file), sourceSha256: digest, url }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}

const sourceByRightUrl = new Map(rightRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
const turnFiles = turnRegister.frames.map((frame) => path.join(root, frame.file))
const actionPublished = actionFiles.map((file, index) => publish(file, `sit-front-f${String(index + 1).padStart(2, '0')}`))
const turnPublished = turnFiles.map((file, index) => publish(file, `turn-front-side-f${String(index + 1).padStart(2, '0')}`))
function contextFrame(frame, label = frame.label) {
  const source = sourceByRightUrl.get(frame.src)
  if (!source || !fs.existsSync(source)) throw new Error(`No context authority for ${frame.src}`)
  return { ...frame, src: publish(source, 'approved-context').url, authoritySrc: frame.src, label }
}
const prefix = rightRoute.route.slice(0, 20).map((frame) => contextFrame(frame))
const suffix = rightRoute.route.slice(34).map((frame) => contextFrame(frame))
const fixed = (src, phase, label, durationMs, actionFrame = null, authoritySrc = null) => ({ src, phase, label, rootXLp: actionRootXLp, bottomLp: floorWorldYLp, anchorLp: [16, 40], durationMs, actionFrame, authoritySrc })
const turnIn = [6, 5, 4, 3, 2, 1, 0].map((index) => fixed(turnPublished[index].url, 'turn side-right → front', `approved Turn V1 · ${turnRegister.frames[index].angleDegrees}°`, 62, null, turnRegister.frames[index].file))
const sit = [1, 2, 3, 4, 5].map((index) => fixed(actionPublished[index].url, 'stand → sit front', `new Prime front F${index + 1}`, 125, index + 1, actionRecords[index].source))
const hold = Array.from({ length: 4 }, () => fixed(actionPublished[5].url, 'seated-front hold', 'exact registered Prime seated-front', 150, 6, rel(seatedFrontFile)))
const stand = [4, 3, 2, 1, 0].map((index) => fixed(actionPublished[index].url, 'sit → stand front', `exact reverse F${index + 1}`, 115, index + 1, actionRecords[index].source))
const turnOut = [1, 2, 3, 4, 5, 6, 7].map((index) => fixed(turnPublished[index].url, 'turn front → side-right', `approved Turn V1 · ${turnRegister.frames[index].angleDegrees}°`, 62, null, turnRegister.frames[index].file))
const route = [...prefix, ...turnIn, ...sit, ...hold, ...stand, ...turnOut, ...suffix]
if (route.length !== 59) throw new Error(`Expected 59 route frames, got ${route.length}`)

const chair = { centerWorldXLp: actionRootXLp, seatLeftWorldXLp: 74, seatRightWorldXLp: 98, seatWidthLp: 24, seatTopWorldYLp: 44.25, seatHeightAboveFloorLp: 7.75, backrestLeftWorldXLp: 76.5, backrestRightWorldXLp: 95.5, backrestWidthLp: 19, backrestTopWorldYLp: 31, renderLayer: 'behind-keeper' }
const data = {
  schema: 'lighthouse-keeper/sit-stand-context@front-1', set, status: 'reversible-front-review-candidate-not-approved',
  derivation: { inheritedFamily: 'keeper_sit_front', auditTreatment: 'partial-motion-salvage-assessment', historicalUse: 'choreography only', visibleHistoricalKeeperPixelsInCandidate: 0, generatedIntermediateCount: 4, registration: 'uniform crop plus explicit registered width/height and Lanczos resample; no creative pixel warp' },
  room: { widthLp: rightRoute.room.widthLp, heightLp: rightRoute.room.heightLp, floorLp: floorWorldYLp, chair },
  action: { direction: 'front', standToSitRange: [1, 6], sitToStand: 'exact-byte-reverse', endpointHoldMs: 600, frames: actionRecords.map((record, index) => ({ index: index + 1, src: actionPublished[index].url, sourcePreviewSrc: publish(path.join(root, record.source), 'pose-source').url, sha256: record.sha256, source: record.source, sourceSha256: record.sourceSha256, bounds: record.bounds, registration: record.registration })) },
  turn: { authority: rel(turnRegisterFile), sideRightToFront: 'exact reverse of approved Turn V1 without duplicate side endpoint', frontToSideRight: 'exact approved Turn V1 without duplicate front endpoint', frames: turnRegister.frames.map((frame, index) => ({ index: index + 1, angleDegrees: frame.angleDegrees, src: turnPublished[index].url, sha256: frame.sha256, source: frame.file })) },
  route, coreRange: [27, 40],
}
const dataFile = path.join(pack, 'keeper-prime-sit-stand-front-v1.json')
writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'front-prime-redraw-candidate-awaiting-frank',
  classification: data.derivation,
  authorities: {
    standingFront: { file: rel(standingFrontFile), sha256: sha(standingFrontFile), candidateFrame: 1, byteIdentical: true },
    seatedFront: { file: rel(seatedFrontFile), sha256: sha(seatedFrontFile), candidateFrame: 6, byteIdentical: true },
    approvedFrontSideTurn: { file: rel(turnRegisterFile), sha256: sha(turnRegisterFile), frameHashes: turnRegister.frames.map((frame) => frame.sha256) },
    walkStopReturn: { register: rel(rightRegisterFile), sha256: sha(rightRegisterFile), route: rel(rightRouteFile), routeSha256: sha(rightRouteFile) },
    pinnedSideLeftApproval: { file: rel(sideLeftApprovalFile), sha256: sha(sideLeftApprovalFile), decision: sideLeftApproval.decision },
  },
  historicalChoreographyOnly: { file: rel(historicalFile), sha256: sha(historicalFile), pixelsReusedInCandidate: false },
  generation: { tool: 'built-in image generation', generatedSources: generated.map((file, index) => ({ pose: index + 2, file: rel(file), sha256: sha(file) })), promptLog: rel(path.join(pack, 'PROMPT_LOG.md')), endpointPixelsGenerated: false },
  candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } },
  registration: { logicalCell: [32, 40], cellPixels: [256, 320], density: 8, anchorLp: [16, 40], floorWorldYLp, actionRootWorldXLp: actionRootXLp },
  geometry: chair,
  ownership: { actorAndClothing: 'all non-transparent cell pixels', props: 'none', effects: 'none', ambiguousDetachedOwnershipAllowed: false },
  checks: {
    sideLeftApprovalPinnedBeforeNewDirection: true,
    historicalKeeperPixelsReusedInCandidate: false,
    standingEndpointExact: actionRecords[0].sha256 === sha(standingFrontFile),
    seatedEndpointExact: actionRecords[5].sha256 === sha(seatedFrontFile),
    sitToStandExactByteReverse: true,
    sixIsolatedActionCells: actionRecords.length === 6,
    allActionCellsHaveFourPixelTransparentGutter: actionRecords.every((record) => record.edgeAlphaPixels === 0 && record.transparentGutterPx >= 4),
    completeWalkStopTurnActionReturnContext: route.length === 59,
    exactApprovedTurnFramesUsed: turnRegister.frames.every((frame, index) => frame.sha256 === sha(turnFiles[index])),
    approvedLocomotionContextUsed: true,
    chairBehindKeeperAtApprovedSupportHeight: chair.renderLayer === 'behind-keeper' && chair.seatHeightAboveFloorLp === 7.75,
    reviewPreloadsEveryUniqueMovingAndComparisonImage: true,
    ghostOverlaysProvided: true,
    largeGameAndLiteralScalesProvided: true,
    finalUnchanged: true,
    runtimeUnchanged: true,
    productionSpritesUnchanged: true,
  },
  publishedAssets,
  approvalBoundary: { sideRightAndSideLeftApprovalsPreserved: true, frontSitStandApproved: false, backSitStandApproved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_front_v1.mjs and scripts/verify_keeper_prime_sit_stand_front_v1.mjs; every approved authority and earlier review remains unchanged.`,
}
for (const [name, value] of Object.entries(register.checks)) {
  if (name === 'historicalKeeperPixelsReusedInCandidate') {
    if (value !== false) throw new Error(`${name} must remain false`)
  } else if (value !== true) throw new Error(`${name} failed`)
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Prime Keeper front sit/stand V1\n\nThis reversible candidate uses the exact approved Prime standing-front endpoint, exact registered Prime seated-front endpoint, four newly generated and deterministically registered Prime-derived intermediates, exact approved front↔side turn frames and approved walk/stop context. Historical keeper_sit_front contributes choreography only and zero candidate pixels. The 59-frame route awaits Frank's review; back and rear-angle transitions remain unapproved, and nothing is promoted.\n`)

console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, actionFrames: actionRecords.length, routeFrames: route.length, endpointHashes: [actionRecords[0].sha256, actionRecords[5].sha256], checks: register.checks }, null, 2))
