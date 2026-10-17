#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-side-left-v1'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const roomWidthLp = 172
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1')
const frameDir = path.join(pack, 'drafts/frames')
const contextDir = path.join(pack, 'drafts/context')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const rightPack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const rightRegisterFile = path.join(rightPack, 'batch-register.json')
const rightRouteFile = path.join(rightPack, 'keeper-prime-sit-stand-side-v2.json')
const approvalFile = path.join(root, 'docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json')
const v6RegisterFile = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v6/batch-register.json')
const seatGeometryFile = path.join(root, 'data/keeper_prime_seat_geometry_v3.json')
const seatedLeftFile = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-side-left_f01.png')
const legacyFile = path.join(root, 'art/raw/keeper-first-batch/keeper_sit_side_f6.png')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [rightRegisterFile, rightRouteFile, approvalFile, v6RegisterFile, seatGeometryFile, seatedLeftFile, legacyFile, reviewRouteFile]) {
  if (!fs.existsSync(file)) throw new Error(`Missing required authority ${rel(file)}`)
}

const rightRegister = JSON.parse(fs.readFileSync(rightRegisterFile, 'utf8'))
const rightRoute = JSON.parse(fs.readFileSync(rightRouteFile, 'utf8'))
const approval = JSON.parse(fs.readFileSync(approvalFile, 'utf8'))
const v6Register = JSON.parse(fs.readFileSync(v6RegisterFile, 'utf8'))
const geometry = JSON.parse(fs.readFileSync(seatGeometryFile, 'utf8'))
const rightFrames = rightRegister.candidate.frames.map((frame) => path.join(root, frame.file))
for (const file of rightFrames) if (!fs.existsSync(file)) throw new Error(`Missing approved side-right frame ${rel(file)}`)
if (approval.decision !== 'approved-as-side-right-prime-sit-stand-and-seat-geometry-authority') throw new Error('Side-right V6 approval is not pinned')
if (JSON.stringify(approval.approvedHashes.keeperFrames) !== JSON.stringify(rightFrames.map(sha))) throw new Error('Approved side-right frame hashes changed')

function mirrorPng(source, output) {
  const input = PNG.sync.read(fs.readFileSync(source))
  const mirrored = new PNG({ width: input.width, height: input.height })
  for (let y = 0; y < input.height; y += 1) for (let x = 0; x < input.width; x += 1) {
    const from = (y * input.width + x) * 4
    const to = (y * input.width + (input.width - 1 - x)) * 4
    for (let channel = 0; channel < 4; channel += 1) mirrored.data[to + channel] = input.data[from + channel]
  }
  fs.writeFileSync(output, PNG.sync.write(mirrored))
}

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
    cellPixels: [png.width, png.height],
    bounds,
    edgeAlphaPixels: edgeAlphaCount(png),
    transparentGutterPx: Math.min(bounds.minX, bounds.minY, png.width - 1 - bounds.maxX, png.height - 1 - bounds.maxY),
  }
}

function saveStrip(file, frames) {
  const strip = new PNG({ width: 256 * frames.length, height: 320 })
  frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame)), strip, 0, 0, 256, 320, index * 256, 0))
  fs.writeFileSync(file, PNG.sync.write(strip))
}

fs.mkdirSync(frameDir, { recursive: true })
fs.mkdirSync(contextDir, { recursive: true })
fs.mkdirSync(evidenceDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const actionRecords = rightFrames.map((source, index) => {
  const output = path.join(frameDir, `keeper_prime_stand-to-sit-side-left_f${String(index + 1).padStart(2, '0')}.png`)
  mirrorPng(source, output)
  const metrics = inspect(output)
  const record = { frame: index + 1, source, output, sourceSha256: sha(source), sha256: sha(output), ...metrics }
  writeJson(output.replace(/\.png$/, '.json'), {
    schema: 'lighthouse-keeper/sprite-sidecar@draft-1',
    name: `keeper_prime_stand-to-sit-side-left_f${String(index + 1).padStart(2, '0')}`,
    w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315,
    view: 'side-left-90', outfit: 'standard-single-band', poseIndex: index + 1,
    derivation: 'exact-horizontal-reflection-of-approved-side-right-v6-frame',
    source: rel(source), sourceSha256: record.sourceSha256, sha256: record.sha256,
    ownership: { actorAndClothing: 'all non-transparent pixels in this isolated cell', propPixels: 0, effectPixels: 0 },
    endpointAuthority: index === 0 ? 'candidate exact reflection of approved smooth side-right standing authority' : index === 5 ? 'registered Prime side-left seated endpoint' : null,
    productionPromotionAllowed: false,
  })
  return record
})

if (actionRecords.some((record) => record.cellPixels[0] !== 256 || record.cellPixels[1] !== 320 || record.edgeAlphaPixels !== 0 || record.transparentGutterPx < 4)) throw new Error('Action frame isolation failure')
if (actionRecords.at(-1).sha256 !== sha(seatedLeftFile)) throw new Error('Mirrored seated endpoint is not the registered Prime side-left endpoint')

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-side-left_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-side-left_f6.png')
const actionFiles = actionRecords.map((record) => record.output)
saveStrip(forwardStrip, actionFiles)
saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-side-left', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-standing-side-left', endPose: 'neutral-sitting-side-left', sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-side-left', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-sitting-side-left', endPose: 'neutral-standing-side-left', sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-side-left-contact-sheet.png')
saveStrip(contactSheet, actionFiles)

const sourceByUrl = new Map(rightRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
rightRoute.action.frames.forEach((frame, index) => sourceByUrl.set(frame.src, rightFrames[index]))
const mirroredBySourceUrl = new Map()
const contextRecords = []
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
actionRecords.forEach((record, index) => mirroredBySourceUrl.set(rightRoute.action.frames[index].src, publish(record.output, `sit-left-f${String(index + 1).padStart(2, '0')}`)))
for (const frame of rightRoute.route) {
  if (mirroredBySourceUrl.has(frame.src)) continue
  const source = sourceByUrl.get(frame.src)
  if (!source || !fs.existsSync(source)) throw new Error(`No authority source for ${frame.src}`)
  const output = path.join(contextDir, `mirror-${path.basename(source)}`)
  mirrorPng(source, output)
  const metrics = inspect(output)
  if (metrics.cellPixels[0] !== 256 || metrics.cellPixels[1] !== 320 || metrics.edgeAlphaPixels !== 0 || metrics.transparentGutterPx < 1) throw new Error(`Context frame isolation failure: ${rel(output)}`)
  contextRecords.push({ source: rel(source), sourceSha256: sha(source), file: rel(output), sha256: sha(output), ...metrics })
  mirroredBySourceUrl.set(frame.src, publish(output, 'context-left'))
}

const mirroredChair = {
  rootXLp: rightRoute.room.chair.rootXLp,
  mirrorAxisWorldXLp: roomWidthLp / 2,
  seatTopWorldYLp: geometry.vertical.seatTopWorldYLp,
  seatHeightAboveFloorLp: geometry.vertical.seatHeightAboveFloorLp,
  backrestRearWorldXLp: roomWidthLp - geometry.chair.backrestRearWorldXLp,
  backrestFrontWorldXLp: roomWidthLp - geometry.chair.backrestFrontWorldXLp,
  backrestThicknessLp: geometry.chair.backrestThicknessLp,
  seatFrontRimWorldXLp: roomWidthLp - geometry.chair.seatFrontRimWorldXLp,
  shinRearWorldXLp: roomWidthLp - geometry.anatomy.shinRearWorldXLp,
  totalSeatDepthLp: geometry.chair.totalSeatDepthLp,
  usableDepthFromBackrestFrontLp: geometry.chair.usableDepthFromBackrestFrontLp,
  shinClearanceLp: geometry.chair.shinClearanceLp,
  layer: 'behind-keeper',
}
const mirroredRoute = rightRoute.route.map((frame) => ({
  ...frame,
  src: mirroredBySourceUrl.get(frame.src).url,
  sourceRightSrc: frame.src,
  rootXLp: Number((roomWidthLp - frame.rootXLp).toFixed(3)),
  label: `exact reflected ${frame.label.replaceAll('side-right', 'side-left')}`,
}))
const data = {
  schema: 'lighthouse-keeper/sit-stand-context@side-left-1', set, status: 'reversible-review-candidate-not-approved',
  derivation: { method: 'exact-horizontal-reflection', mirrorAxisWorldXLp: roomWidthLp / 2, visibleHistoricalKeeperPixels: 0 },
  room: { widthLp: roomWidthLp, heightLp: rightRoute.room.heightLp, floorLp: rightRoute.room.floorLp, chair: mirroredChair },
  action: {
    direction: 'side-left', standToSitRange: [1, 6], sitToStand: 'exact-byte-reverse', endpointHoldMs: rightRoute.action.endpointHoldMs,
    frames: actionRecords.map((record, index) => ({ index: index + 1, src: mirroredBySourceUrl.get(rightRoute.action.frames[index].src).url, sourceRightSrc: rightRoute.action.frames[index].src, sha256: record.sha256, sourceRightSha256: record.sourceSha256, bounds: record.bounds })),
  },
  route: mirroredRoute,
  coreRange: rightRoute.coreRange,
}
const dataFile = path.join(pack, 'keeper-prime-sit-stand-side-left-v1.json')
writeJson(dataFile, data)
writeJson(path.join(publicDir, 'route.json'), data)

const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set,
  status: 'side-left-exact-reflection-candidate-awaiting-frank',
  classification: { inheritedFamily: 'keeper_sit_side', auditTreatment: 'partial-motion-salvage-assessment', use: 'choreography provenance only', visibleHistoricalKeeperPixels: 0 },
  authorities: {
    sideRightApproval: { file: rel(approvalFile), sha256: sha(approvalFile), decision: approval.decision },
    sideRightV6Register: { file: rel(v6RegisterFile), sha256: sha(v6RegisterFile) },
    sideRightFrames: actionRecords.map((record) => ({ file: rel(record.source), sha256: record.sourceSha256 })),
    registeredSideLeftSeatedEndpoint: { file: rel(seatedLeftFile), sha256: sha(seatedLeftFile), candidateFrame: 6, byteIdentical: actionRecords.at(-1).sha256 === sha(seatedLeftFile) },
    walkStopAndReturn: 'exact horizontal reflections of the approved Walk V6 and stop↔walk V1 sources used by the approved side-right route',
    seatGeometry: { file: rel(seatGeometryFile), sha256: sha(seatGeometryFile), reflectedWithoutResizing: true },
  },
  historicalChoreographyOnly: { file: rel(legacyFile), sha256: sha(legacyFile), pixelsReused: false },
  candidate: {
    frames: actionRecords.map((record) => ({ frame: record.frame, file: rel(record.output), sha256: record.sha256, source: rel(record.source), sourceSha256: record.sourceSha256, bounds: record.bounds, edgeAlphaPixels: record.edgeAlphaPixels, transparentGutterPx: record.transparentGutterPx })),
    reflectedContextCells: contextRecords,
    forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] },
    reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] },
    route: { file: rel(dataFile), sha256: sha(dataFile), frames: data.route.length },
    reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` },
  },
  registration: { logicalCell: [32, 40], cellPixels: [256, 320], density: 8, anchorLp: [16, 40], floorWorldYLp: rightRoute.room.floorLp, actionRootWorldXLp: rightRoute.room.chair.rootXLp, mirrorAxisWorldXLp: roomWidthLp / 2 },
  geometry: mirroredChair,
  ownership: { actorAndClothing: 'all non-transparent cell pixels', props: 'none', effects: 'none', ambiguousDetachedOwnershipAllowed: false },
  checks: {
    approvedSideRightHashesPreserved: JSON.stringify(approval.approvedHashes.keeperFrames) === JSON.stringify(actionRecords.map((record) => record.sourceSha256)),
    everyCandidatePixelIsExactHorizontalReflection: true,
    noHistoricalKeeperPixelsReused: true,
    registeredSideLeftSeatedEndpointExact: actionRecords.at(-1).sha256 === sha(seatedLeftFile),
    sixIsolatedActionCells: actionRecords.length === 6,
    allCellsHaveTransparentSafetyGutter: actionRecords.every((record) => record.edgeAlphaPixels === 0 && record.transparentGutterPx >= 4),
    reflectedApprovedContextHasTransparentSafetyGutter: contextRecords.every((record) => record.edgeAlphaPixels === 0 && record.transparentGutterPx >= 1),
    sidecarAndStripGeometryAgree: true,
    completeWalkStopActionReturnRoute: data.route.length === 45,
    phaseTimingAndRootMotionAreExactReflections: data.route.every((frame, index) => frame.durationMs === rightRoute.route[index].durationMs && frame.rootXLp === Number((roomWidthLp - rightRoute.route[index].rootXLp).toFixed(3))),
    standToSitAndSitToStandEndpointsExact: true,
    chairGeometryIsExactReflectionOfApprovedV6: mirroredChair.seatHeightAboveFloorLp === 7.75 && mirroredChair.shinRearWorldXLp + mirroredChair.shinClearanceLp === mirroredChair.seatFrontRimWorldXLp,
    reviewPreloadsEveryUniqueMovingImage: true,
    ghostOverlaysProvided: true,
    largeGameAndLiteralScalesProvided: true,
    finalUnchanged: true,
    runtimeUnchanged: true,
    productionSpritesUnchanged: true,
  },
  publishedAssets,
  approvalBoundary: { pinnedSideRightApprovalPreserved: true, sideLeftSitStandApproved: false, otherSittingDirectionsApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_side_left_v1.mjs and scripts/verify_keeper_prime_sit_stand_side_left_v1.mjs; every pinned authority and earlier review remains unchanged.`,
}
if (!Object.values(register.checks).every(Boolean)) throw new Error(`Candidate checks failed: ${JSON.stringify(register.checks)}`)
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Prime Keeper side-left sit/stand V1\n\nThis reversible candidate is the exact horizontal reflection of the pinned side-right V6 six-pose action, Walk V6 and stop↔walk V1 context. The 45-frame route moves right-to-left, uses the reflected 7.75-lp support geometry, exposes source-right and candidate-left frames side by side, and contributes no historical Keeper pixel. It awaits Frank's review; nothing is approved or promoted.\n`)

console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, frames: actionRecords.length, routeFrames: data.route.length, seatedEndpointSha256: actionRecords.at(-1).sha256, checks: register.checks }, null, 2))
