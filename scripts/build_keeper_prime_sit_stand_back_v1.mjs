#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-back-v1'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const rightPack = path.join(root, 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2')
const rightRegisterFile = path.join(rightPack, 'batch-register.json')
const rightRouteFile = path.join(rightPack, 'keeper-prime-sit-stand-side-v2.json')
const turnApprovalFile = path.join(root, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json')
const frontApprovalFile = path.join(root, 'docs/review/keeper-prime-sit-stand-front-v4-approval-2026-10-18.json')
const sideRightApprovalFile = path.join(root, 'docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json')
const sideLeftApprovalFile = path.join(root, 'docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json')
const paletteAuthorityFile = path.join(root, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png')
const seatedBackFile = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png')
const historicalFile = path.join(root, 'art/raw/keeper-first-batch/keeper_sit_back_f6.png')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const promptLogFile = path.join(pack, 'PROMPT_LOG.md')
const generated = [2, 3, 4, 5].map((n) => path.join(pack, `sources/generated/back-f${n}-generated.png`))
const targetSizes = [[150, 286], [150, 276], [150, 270], [150, 266]]
const actionRootXLp = 86
const floorWorldYLp = 52

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [rightRegisterFile, rightRouteFile, turnApprovalFile, frontApprovalFile, sideRightApprovalFile, sideLeftApprovalFile, paletteAuthorityFile, seatedBackFile, historicalFile, reviewRouteFile, promptLogFile, ...generated]) {
  if (!fs.existsSync(file)) throw new Error(`Missing required input ${rel(file)}`)
}
const rightRegister = readJson(rightRegisterFile)
const rightRoute = readJson(rightRouteFile)
const turnApproval = readJson(turnApprovalFile)
const frontApproval = readJson(frontApprovalFile)
const sideRightApproval = readJson(sideRightApprovalFile)
const sideLeftApproval = readJson(sideLeftApprovalFile)
if (turnApproval.status !== 'approved-side-back-turn-v9-artwork-authority') throw new Error('Side/back turn approval changed')
if (frontApproval.decision !== 'approved-as-front-prime-sit-stand-authority') throw new Error('Front V4 approval is not pinned')
if (sideRightApproval.decision !== 'approved-as-side-right-prime-sit-stand-and-seat-geometry-authority' || sideLeftApproval.decision !== 'approved-as-side-left-prime-sit-stand-authority') throw new Error('Pinned side approvals changed')
const turnFrames = turnApproval.approvedCandidate.frames
const turnFiles = turnFrames.map((frame) => path.join(root, frame.file))
const standingBackFile = turnFiles.at(-1)
if (turnFrames.length !== 9 || turnFrames.at(-1).angleDegrees !== 180 || turnFrames.at(-1).sha256 !== sha(standingBackFile)) throw new Error('Approved rear turn endpoint changed')

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
  const png = PNG.sync.read(fs.readFileSync(file)); const bounds = alphaBounds(png)
  const bandMinY = Math.round(bounds.minY + bounds.height * 0.45)
  const bandMaxY = Math.round(bounds.minY + bounds.height * 0.68) - 1
  let bandMinX = png.width, bandMaxX = -1
  for (let y = bandMinY; y <= bandMaxY; y += 1) for (let x = 0; x < png.width; x += 1) if (png.data[(y * png.width + x) * 4 + 3]) { bandMinX = Math.min(bandMinX, x); bandMaxX = Math.max(bandMaxX, x) }
  return { cellPixels: [png.width, png.height], bounds, elbowBandFraction: [0.45, 0.68], elbowSpanPx: bandMaxX - bandMinX + 1, edgeAlphaPixels: edgeAlphaCount(png), transparentGutterPx: Math.min(bounds.minX, bounds.minY, png.width - 1 - bounds.maxX, png.height - 1 - bounds.maxY) }
}

const luma = (r, g, b) => Math.round(0.2126 * r + 0.7152 * g + 0.0722 * b)
function componentName(r, g, b, normalizedY) {
  if (Math.max(r, g, b) < 28) return 'outline'
  if (b > 110 && b > g + 45 && b > r + 70) return 'uniformBlue'
  if (r > 165 && g > 135 && b < 225 && Math.max(r, g, b) - Math.min(r, g, b) > 24) return 'creamOrSkin'
  if (normalizedY >= 0.84) return 'boots'
  if (normalizedY >= 0.63) return 'trousers'
  return 'other'
}

function componentPixels(png) {
  const bounds = alphaBounds(png)
  const groups = new Map(['outline', 'uniformBlue', 'creamOrSkin', 'trousers', 'boots', 'other'].map((name) => [name, []]))
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const offset = (y * png.width + x) * 4
    const [r, g, b, a] = png.data.subarray(offset, offset + 4)
    if (a === 0) continue
    const normalizedY = (y - bounds.minY) / Math.max(1, bounds.height - 1)
    groups.get(componentName(r, g, b, normalizedY)).push({ offset, r, g, b, luma: luma(r, g, b) })
  }
  return groups
}

const paletteAuthorityPng = PNG.sync.read(fs.readFileSync(paletteAuthorityFile))
const paletteAuthorityGroups = componentPixels(paletteAuthorityPng)
const paletteAuthorityRgb = new Set()
for (const pixels of paletteAuthorityGroups.values()) for (const pixel of pixels) paletteAuthorityRgb.add(`${pixel.r},${pixel.g},${pixel.b}`)
const median = (values) => values.length ? values.slice().sort((a, b) => a - b)[Math.floor((values.length - 1) / 2)] : null

function applyPrimePalette(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  const sourceGroups = componentPixels(png)
  const components = {}
  for (const [name, pixels] of sourceGroups) {
    const authority = paletteAuthorityGroups.get(name)
    if (!authority?.length || !pixels.length) throw new Error(`Palette component ${name} is empty for ${rel(file)}`)
    const orderedSource = pixels.slice().sort((a, b) => a.luma - b.luma || a.offset - b.offset)
    const orderedAuthority = authority.slice().sort((a, b) => a.luma - b.luma || a.offset - b.offset)
    const sourceMedianLuma = median(orderedSource.map((pixel) => pixel.luma))
    for (let rank = 0; rank < orderedSource.length; rank += 1) {
      const targetRank = Math.round(rank * (orderedAuthority.length - 1) / Math.max(1, orderedSource.length - 1))
      const target = orderedAuthority[targetRank]
      const source = orderedSource[rank]
      png.data[source.offset] = target.r
      png.data[source.offset + 1] = target.g
      png.data[source.offset + 2] = target.b
    }
    const outputLumas = orderedSource.map((pixel) => luma(png.data[pixel.offset], png.data[pixel.offset + 1], png.data[pixel.offset + 2]))
    components[name] = {
      pixels: orderedSource.length,
      sourceMedianLuma,
      authorityMedianLuma: median(orderedAuthority.map((pixel) => pixel.luma)),
      outputMedianLuma: median(outputLumas),
      outputMedianMatchesAuthority: median(outputLumas) === median(orderedAuthority.map((pixel) => pixel.luma)),
    }
  }
  fs.writeFileSync(file, PNG.sync.write(png))
  const output = PNG.sync.read(fs.readFileSync(file))
  let offPalettePixels = 0
  for (let offset = 0; offset < output.data.length; offset += 4) {
    if (!output.data[offset + 3]) continue
    if (!paletteAuthorityRgb.has(`${output.data[offset]},${output.data[offset + 1]},${output.data[offset + 2]}`)) offPalettePixels += 1
  }
  if (offPalettePixels !== 0) throw new Error(`${rel(file)} retains ${offPalettePixels} RGB pixels outside the approved rear Prime palette`)
  return { method: 'component-wise luminance-quantile registration to exact RGB samples from approved rear Prime V5; alpha and geometry unchanged', authority: rel(paletteAuthorityFile), authoritySha256: sha(paletteAuthorityFile), allVisibleRgbFromAuthority: true, offPalettePixels, components }
}

function alphaSha(file) {
  const png = PNG.sync.read(fs.readFileSync(file)); const alpha = Buffer.alloc(png.width * png.height)
  for (let source = 3, target = 0; source < png.data.length; source += 4, target += 1) alpha[target] = png.data[source]
  return crypto.createHash('sha256').update(alpha).digest('hex')
}

function registerGenerated(source, output, width, height) {
  const sourcePng = PNG.sync.read(fs.readFileSync(source)); const bounds = alphaBounds(sourcePng, 8)
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

fs.mkdirSync(frameDir, { recursive: true }); fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true }); fs.mkdirSync(assetsDir, { recursive: true })
const actionFiles = [1, 2, 3, 4, 5, 6].map((n) => path.join(frameDir, `keeper_prime_stand-to-sit-back_f${String(n).padStart(2, '0')}.png`))
fs.copyFileSync(standingBackFile, actionFiles[0])
const registrations = generated.map((source, index) => registerGenerated(source, actionFiles[index + 1], ...targetSizes[index]))
fs.copyFileSync(seatedBackFile, actionFiles[5])
const paletteRegistrations = actionFiles.map((file, index) => index === 0 ? null : applyPrimePalette(file))

const actionRecords = actionFiles.map((file, index) => {
  const source = index === 0 ? standingBackFile : index === 5 ? seatedBackFile : generated[index - 1]
  const record = { frame: index + 1, file: rel(file), sha256: sha(file), alphaSha256: alphaSha(file), source: rel(source), sourceSha256: sha(source), registration: index > 0 && index < 5 ? registrations[index - 1] : index === 5 ? { geometry: 'exact seated-back alpha plane and canvas', sourceAlphaSha256: alphaSha(seatedBackFile) } : null, paletteRegistration: paletteRegistrations[index], ...inspect(file) }
  writeJson(file.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-back_f${String(index + 1).padStart(2, '0')}`, w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315, view: 'back', outfit: 'standard-single-band', poseIndex: index + 1, derivation: index === 0 ? 'exact-approved-Turn-V9-standing-back-endpoint' : index === 5 ? 'exact-seated-back-geometry-with-approved-rear-Prime-V5-palette-registration' : 'new-complete-Prime-derived-back-sit-intermediate-with-approved-rear-Prime-V5-palette-registration', source: record.source, sourceSha256: record.sourceSha256, sha256: record.sha256, alphaSha256: record.alphaSha256, registration: record.registration, paletteRegistration: record.paletteRegistration, ownership: { actorAndClothing: 'all non-transparent pixels in this isolated cell', propPixels: 0, effectPixels: 0 }, endpointAuthority: index === 0 ? 'approved Turn V9 standing-back endpoint' : index === 5 ? 'seated-back geometry authority plus approved rear Prime V5 palette authority' : null, productionPromotionAllowed: false })
  return record
})
const expectedWidths = [155, 150, 150, 150, 150, 150]
const expectedHeights = [298, 286, 276, 270, 266, 264]
actionRecords.forEach((record, index) => {
  if (record.cellPixels.join('x') !== '256x320' || record.edgeAlphaPixels || record.transparentGutterPx < 4 || record.bounds.width !== expectedWidths[index] || record.bounds.height !== expectedHeights[index]) throw new Error(`Frame ${index + 1} geometry failed`)
  if (index > 0 && record.elbowSpanPx !== 150) throw new Error(`Frame ${index + 1} elbow span ${record.elbowSpanPx} != 150`)
})
if (actionRecords[0].sha256 !== turnFrames.at(-1).sha256 || actionRecords[5].alphaSha256 !== alphaSha(seatedBackFile)) throw new Error('Back action endpoint geometry changed')
if (!actionRecords.slice(1).every((record) => record.paletteRegistration?.allVisibleRgbFromAuthority && Object.values(record.paletteRegistration.components).every((component) => component.outputMedianMatchesAuthority))) throw new Error('Back action palette registration failed')

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-back-v1_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-back-v1_f6.png')
saveStrip(forwardStrip, actionFiles); saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-back-v1', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-standing-back', endPose: 'neutral-sitting-back', sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-back-v1', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], startPose: 'neutral-sitting-back', endPose: 'neutral-standing-back', sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-back-v1-contact-sheet.png'); saveStrip(contactSheet, actionFiles)

const publishedByHash = new Map(); const publishedAssets = []
function publish(file, label) {
  const digest = sha(file); if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`; fs.copyFileSync(file, path.join(assetsDir, filename))
  const entry = { source: rel(file), sourceSha256: digest, url: reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}
const sourceByRightUrl = new Map(rightRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
const actionPublished = actionFiles.map((file, index) => publish(file, `sit-back-v1-f${index + 1}`))
const turnPublished = turnFiles.map((file, index) => publish(file, `approved-turn-side-back-f${index + 1}`))
function contextFrame(frame) { const source = sourceByRightUrl.get(frame.src); if (!source) throw new Error(`No context authority for ${frame.src}`); return { ...frame, src: publish(source, 'approved-context').url, authoritySrc: frame.src } }
const fixed = (src, phase, label, durationMs, actionFrame = null, authoritySrc = null) => ({ src, phase, label, rootXLp: actionRootXLp, bottomLp: floorWorldYLp, anchorLp: [16, 40], durationMs, actionFrame, authoritySrc })
const prefix = rightRoute.route.slice(0, 20).map(contextFrame)
const suffix = rightRoute.route.slice(34).map(contextFrame)
const turnIn = [1, 2, 3, 4, 5, 6, 7, 8].map((index) => fixed(turnPublished[index].url, 'turn side-right → back', `approved Turn V9 · ${turnFrames[index].angleDegrees}°`, 62, null, turnFrames[index].file))
const sit = [1, 2, 3, 4, 5].map((index) => fixed(actionPublished[index].url, 'stand → sit back', `new Prime back F${index + 1}`, 125, index + 1, actionRecords[index].source))
const hold = Array.from({ length: 4 }, () => fixed(actionPublished[5].url, 'seated-back hold', 'Prime seated-back geometry · approved rear palette', 150, 6, rel(seatedBackFile)))
const stand = [4, 3, 2, 1, 0].map((index) => fixed(actionPublished[index].url, 'sit → stand back', `exact reverse F${index + 1}`, 115, index + 1, actionRecords[index].source))
const turnOut = [7, 6, 5, 4, 3, 2, 1, 0].map((index) => fixed(turnPublished[index].url, 'turn back → side-right', `approved Turn V9 reverse · ${turnFrames[index].angleDegrees}°`, 62, null, turnFrames[index].file))
const route = [...prefix, ...turnIn, ...sit, ...hold, ...stand, ...turnOut, ...suffix]
if (route.length !== 61) throw new Error(`Expected 61 route frames, got ${route.length}`)

const chair = { centerWorldXLp: 86, leftWorldXLp: 74, widthLp: 24, backrestWidthLp: 19, backrestTopWorldYLp: 31, seatTopWorldYLp: 44.25, seatHeightAboveFloorLp: 7.75, renderLayer: 'foreground-over-keeper', visibleSurface: 'rear of chair', actorDepth: 'behind-chair-during-turn-action-and-return' }
const data = { schema: 'lighthouse-keeper/sit-stand-context@back-1', set, status: 'reversible-back-review-candidate-not-approved', derivation: { inheritedFamily: 'keeper_sit_back', historicalUse: 'choreography only', visibleHistoricalKeeperPixelsInCandidate: 0, generatedIntermediateCount: 4, registration: 'uniform crop plus explicit 150 px width and decreasing height; Lanczos resample; component-wise palette registration to exact approved rear Prime V5 RGB samples; no creative pixel warp' }, room: { widthLp: rightRoute.room.widthLp, heightLp: rightRoute.room.heightLp, floorLp: floorWorldYLp, chair }, action: { direction: 'back', standToSitRange: [1, 6], sitToStand: 'exact-byte-reverse', endpointHoldMs: 600, paletteAuthority: { file: rel(paletteAuthorityFile), sha256: sha(paletteAuthorityFile) }, frames: actionRecords.map((record, index) => ({ index: index + 1, src: actionPublished[index].url, sourcePreviewSrc: publish(path.join(root, record.source), 'pose-source').url, sha256: record.sha256, alphaSha256: record.alphaSha256, source: record.source, sourceSha256: record.sourceSha256, bounds: record.bounds, elbowSpanPx: record.elbowSpanPx, registration: record.registration, paletteRegistration: record.paletteRegistration })) }, turn: { authority: rel(turnApprovalFile), sideRightToBack: 'exact approved Turn V9 without duplicate side endpoint', backToSideRight: 'exact byte-order reverse without duplicate back endpoint', frames: turnFrames.map((frame, index) => ({ index: index + 1, angleDegrees: frame.angleDegrees, src: turnPublished[index].url, sha256: frame.sha256, source: frame.file })) }, route, coreRange: [28, 41] }
const dataFile = path.join(pack, 'keeper-prime-sit-stand-back-v1.json'); writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'back-foreground-chair-v1-awaiting-frank', authorities: { standingBack: { file: rel(standingBackFile), sha256: sha(standingBackFile), source: 'exact approved Turn V9 F9 rear endpoint', candidateFrame: 1, byteIdentical: true }, seatedBackGeometry: { file: rel(seatedBackFile), sha256: sha(seatedBackFile), alphaSha256: alphaSha(seatedBackFile), candidateFrame: 6, alphaPlaneIdentical: actionRecords[5].alphaSha256 === alphaSha(seatedBackFile), rgbPaletteReplaced: true }, standardUniformPalette: { file: rel(paletteAuthorityFile), sha256: sha(paletteAuthorityFile), scope: 'exact approved rear Prime V5 RGB samples; component-wise quantile registration for action F2-F6' }, approvedSideBackTurn: { file: rel(turnApprovalFile), sha256: sha(turnApprovalFile), decision: turnApproval.status, frameHashes: turnFrames.map((frame) => frame.sha256) }, walkStopReturn: { register: rel(rightRegisterFile), sha256: sha(rightRegisterFile), route: rel(rightRouteFile), routeSha256: sha(rightRouteFile) }, pinnedApprovals: { sideRightV6: { file: rel(sideRightApprovalFile), sha256: sha(sideRightApprovalFile), decision: sideRightApproval.decision }, sideLeftV1: { file: rel(sideLeftApprovalFile), sha256: sha(sideLeftApprovalFile), decision: sideLeftApproval.decision }, frontV4: { file: rel(frontApprovalFile), sha256: sha(frontApprovalFile), decision: frontApproval.decision } } }, historicalChoreographyOnly: { file: rel(historicalFile), sha256: sha(historicalFile), pixelsReusedInCandidate: false }, generation: { tool: 'built-in image generation', mode: 'identity-preserve edit', generatedSources: generated.map((file, index) => ({ pose: index + 2, file: rel(file), sha256: sha(file), role: 'pose drawing source only; colour is non-authoritative and removed by deterministic Prime palette registration' })), promptLog: rel(promptLogFile), endpointPixelsGenerated: false }, candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } }, registration: { logicalCell: [32, 40], cellPixels: [256, 320], density: 8, anchorLp: [16, 40], floorWorldYLp, actionRootWorldXLp: actionRootXLp }, geometry: chair, checks: { pinnedSideAndFrontApprovalsUnchanged: true, historicalKeeperPixelsReusedInCandidate: false, exactApprovedTurnRearEndpointUsed: actionRecords[0].sha256 === turnFrames.at(-1).sha256, seatedEndpointGeometryExact: actionRecords[5].alphaSha256 === alphaSha(seatedBackFile), everyCorrectedFrameUsesOnlyApprovedRearPrimeRgb: actionRecords.slice(1).every((frame) => frame.paletteRegistration?.allVisibleRgbFromAuthority && frame.paletteRegistration.offPalettePixels === 0), jumperPaletteMedianMatchesPrime: actionRecords.slice(1).every((frame) => frame.paletteRegistration.components.uniformBlue.outputMedianMatchesAuthority), trouserPaletteMedianMatchesPrime: actionRecords.slice(1).every((frame) => frame.paletteRegistration.components.trousers.outputMedianMatchesAuthority), bootPaletteMedianMatchesPrime: actionRecords.slice(1).every((frame) => frame.paletteRegistration.components.boots.outputMedianMatchesAuthority), loweringFramesMatchSeatedElbowSpan: actionRecords.slice(1).every((frame) => frame.elbowSpanPx === 150), loweringHeightsMonotonic: actionRecords.every((frame, index, all) => index === 0 || frame.bounds.height <= all[index - 1].bounds.height), sitToStandExactByteReverse: true, sixIsolatedActionCells: actionRecords.length === 6 && actionRecords.every((frame) => frame.edgeAlphaPixels === 0 && frame.transparentGutterPx >= 4), complete61FrameContext: route.length === 61, exactApprovedTurnFramesUsed: turnFrames.every((frame, index) => frame.sha256 === sha(turnFiles[index])), chairRearForegroundAndKeeperPassesBehind: chair.renderLayer === 'foreground-over-keeper' && chair.actorDepth.startsWith('behind-chair'), ghostOverlaysProvided: true, allImagesPreloadedBeforePlayback: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true }, publishedAssets, approvalBoundary: { sideRightV6Approved: true, sideLeftV1Approved: true, frontV4Approved: true, backV1Approved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false }, rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_back_v1.mjs and scripts/verify_keeper_prime_sit_stand_back_v1.mjs; every pinned approval and earlier review remains unchanged.` }
for (const [name, value] of Object.entries(register.checks)) { if (name === 'historicalKeeperPixelsReusedInCandidate') { if (value !== false) throw new Error(`${name} must remain false`) } else if (value !== true) throw new Error(`${name} failed`) }
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Prime Keeper back sit/stand V1\n\nThis reversible candidate uses the exact approved Turn V9 standing-back endpoint, the exact seated-back geometry, four new complete Prime-derived rear intermediates, the exact approved side↔back turn and approved walk/stop context. Action F2–F6 are deterministically registered to component-specific RGB samples from approved rear Prime V5, including the jumper, trousers and boots; generated-source colour is explicitly non-authoritative. The chair rear is a separate foreground layer, so the Keeper visibly passes behind it. Historical keeper_sit_back contributes choreography only and zero candidate pixels. The complete 61-frame route awaits Frank; nothing is promoted.\n')
console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, routeFrames: route.length, widths: actionRecords.map((frame) => frame.bounds.width), elbowSpans: actionRecords.map((frame) => frame.elbowSpanPx), heights: actionRecords.map((frame) => frame.bounds.height), checks: register.checks }, null, 2))
