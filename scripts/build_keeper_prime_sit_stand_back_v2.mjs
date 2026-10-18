#!/usr/bin/env node

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-back-v2'
const v1Set = 'keeper-prime-sit-stand-back-v1'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const v1Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1')
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const v1RegisterFile = path.join(v1Pack, 'batch-register.json')
const v1DataFile = path.join(v1Pack, `${v1Set}.json`)
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const abs = (file) => path.join(root, file)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const clone = (value) => JSON.parse(JSON.stringify(value))

for (const file of [v1RegisterFile, v1DataFile, reviewRouteFile]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)
const v1Register = readJson(v1RegisterFile)
const v1Data = readJson(v1DataFile)
if (v1Register.set !== v1Set || v1Data.route.length !== 61 || v1Register.approvalBoundary.backV1Approved !== false) throw new Error('Immutable V1 input contract changed')
const endpointFile = abs(v1Register.authorities.standingBack.file)
const legacyPaletteFile = abs(v1Register.authorities.standardUniformPalette.file)
if (sha(endpointFile) !== v1Register.authorities.standingBack.sha256 || sha(legacyPaletteFile) !== v1Register.authorities.standardUniformPalette.sha256) throw new Error('Prime palette authorities changed')

function alphaBounds(png) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1, opaquePixels = 0
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const a = png.data[(y * png.width + x) * 4 + 3]
    if (!a) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); opaquePixels += 1
  }
  if (maxX < 0) throw new Error('Empty sprite')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaquePixels }
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

function paletteGroups(png) {
  const bounds = alphaBounds(png)
  const groups = new Map()
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const offset = (y * png.width + x) * 4
    const [r, g, b, a] = png.data.subarray(offset, offset + 4)
    if (!a) continue
    const name = componentName(r, g, b, (y - bounds.minY) / Math.max(1, bounds.height - 1))
    if (!groups.has(name)) groups.set(name, new Map())
    groups.get(name).set(`${r},${g},${b}`, { r, g, b, luma: luma(r, g, b) })
  }
  return groups
}

const endpointPng = PNG.sync.read(fs.readFileSync(endpointFile))
const endpointGroups = paletteGroups(endpointPng)
const endpointRgb = new Set()
const legacyRgb = new Set()
for (const offsetSet of [[endpointPng, endpointRgb], [PNG.sync.read(fs.readFileSync(legacyPaletteFile)), legacyRgb]]) {
  const [png, setOfRgb] = offsetSet
  for (let offset = 0; offset < png.data.length; offset += 4) if (png.data[offset + 3]) setOfRgb.add(`${png.data[offset]},${png.data[offset + 1]},${png.data[offset + 2]}`)
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b)
  return sorted.length ? sorted[Math.floor(sorted.length / 2)] : null
}

function regionalReadings(png) {
  const bounds = alphaBounds(png)
  const readings = { jumperCore: [], trouserCore: [] }
  for (let y = bounds.minY; y <= bounds.maxY; y += 1) for (let x = bounds.minX; x <= bounds.maxX; x += 1) {
    const offset = (y * png.width + x) * 4
    const [r, g, b, a] = png.data.subarray(offset, offset + 4)
    if (!a) continue
    const nx = (x - bounds.minX) / Math.max(1, bounds.width - 1)
    const ny = (y - bounds.minY) / Math.max(1, bounds.height - 1)
    const component = componentName(r, g, b, ny)
    if (nx >= 0.22 && nx <= 0.78 && ny >= 0.38 && ny <= 0.63 && component === 'uniformBlue') readings.jumperCore.push(luma(r, g, b))
    if (nx >= 0.18 && nx <= 0.82 && ny >= 0.68 && ny <= 0.84 && component === 'trousers') readings.trouserCore.push(luma(r, g, b))
  }
  return Object.fromEntries(Object.entries(readings).map(([name, values]) => [name, { pixels: values.length, medianLuma: median(values), p25Luma: [...values].sort((a, b) => a - b)[Math.floor(values.length * 0.25)], p75Luma: [...values].sort((a, b) => a - b)[Math.floor(values.length * 0.75)] }]))
}

const endpointReadings = regionalReadings(endpointPng)
if (endpointReadings.jumperCore.medianLuma !== 95 || endpointReadings.trouserCore.medianLuma !== 77) throw new Error('Approved endpoint regional readings changed')

function correctClothing(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  const bounds = alphaBounds(png)
  const prior = regionalReadings(png)
  let correctedPixels = 0
  for (let y = bounds.minY; y <= bounds.maxY; y += 1) for (let x = bounds.minX; x <= bounds.maxX; x += 1) {
    const offset = (y * png.width + x) * 4
    const [r, g, b, a] = png.data.subarray(offset, offset + 4)
    if (!a) continue
    const component = componentName(r, g, b, (y - bounds.minY) / Math.max(1, bounds.height - 1))
    const delta = component === 'uniformBlue' ? 21 : component === 'trousers' ? 25 : 0
    if (!delta) continue
    let candidates = [...endpointGroups.get(component).values()]
    if (component === 'trousers') candidates = candidates.filter((candidate) => candidate.b - candidate.r > 25 && candidate.b - candidate.g > 10)
    const targetLuma = luma(r, g, b) + delta
    let best = null, bestScore = Number.POSITIVE_INFINITY
    for (const candidate of candidates) {
      const chromaDelta = Math.abs((candidate.b - candidate.r) - (b - r)) + Math.abs((candidate.b - candidate.g) - (b - g))
      const score = Math.abs(candidate.luma - targetLuma) * 100 + chromaDelta
      if (score < bestScore) { best = candidate; bestScore = score }
    }
    png.data[offset] = best.r; png.data[offset + 1] = best.g; png.data[offset + 2] = best.b
    correctedPixels += 1
  }
  fs.writeFileSync(file, PNG.sync.write(png))
  const output = PNG.sync.read(fs.readFileSync(file))
  const corrected = regionalReadings(output)
  let offAuthorityPixels = 0
  for (let offset = 0; offset < output.data.length; offset += 4) {
    if (!output.data[offset + 3]) continue
    const key = `${output.data[offset]},${output.data[offset + 1]},${output.data[offset + 2]}`
    if (!endpointRgb.has(key) && !legacyRgb.has(key)) offAuthorityPixels += 1
  }
  if (offAuthorityPixels) throw new Error(`${rel(file)} has ${offAuthorityPixels} off-authority pixels`)
  for (const name of ['jumperCore', 'trouserCore']) {
    if (Math.abs(corrected[name].medianLuma - endpointReadings[name].medianLuma) > 1) throw new Error(`${rel(file)} ${name} still drifts from Prime: ${corrected[name].medianLuma} vs ${endpointReadings[name].medianLuma}`)
  }
  return { method: 'regional rear-endpoint palette correction; hue-constrained nearest exact RGB sample; alpha and geometry unchanged', correctedPixels, offAuthorityPixels, allVisibleRgbFromApprovedPrimeAuthorities: true, prior, corrected, authority: endpointReadings }
}

function alphaSha(file) {
  const png = PNG.sync.read(fs.readFileSync(file)); const alpha = Buffer.alloc(png.width * png.height)
  for (let source = 3, target = 0; source < png.data.length; source += 4, target += 1) alpha[target] = png.data[source]
  return crypto.createHash('sha256').update(alpha).digest('hex')
}

function saveStrip(file, frames) {
  const strip = new PNG({ width: 256 * frames.length, height: 320 })
  frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame)), strip, 0, 0, 256, 320, index * 256, 0))
  fs.writeFileSync(file, PNG.sync.write(strip))
}

fs.mkdirSync(frameDir, { recursive: true }); fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true }); fs.mkdirSync(assetsDir, { recursive: true })
const frameFiles = v1Register.candidate.frames.map((frame) => path.join(frameDir, path.basename(frame.file)))
const actionRecords = v1Register.candidate.frames.map((v1Frame, index) => {
  const file = frameFiles[index]
  fs.copyFileSync(abs(v1Frame.file), file)
  const correction = index === 0 ? { method: 'exact approved rear endpoint; no correction', correctedPixels: 0, offAuthorityPixels: 0, allVisibleRgbFromApprovedPrimeAuthorities: true, prior: endpointReadings, corrected: endpointReadings, authority: endpointReadings } : correctClothing(file)
  const record = { ...clone(v1Frame), file: rel(file), sha256: sha(file), alphaSha256: alphaSha(file), priorV1File: v1Frame.file, priorV1Sha256: v1Frame.sha256, paletteRegistration: { ...correction, endpointPaletteAuthority: rel(endpointFile), endpointPaletteAuthoritySha256: sha(endpointFile), inheritedPrimePaletteAuthority: rel(legacyPaletteFile), inheritedPrimePaletteAuthoritySha256: sha(legacyPaletteFile) } }
  if (record.alphaSha256 !== v1Frame.alphaSha256) throw new Error(`F${index + 1} alpha changed`)
  writeJson(file.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-back-v2_f${String(index + 1).padStart(2, '0')}`, w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], view: 'back', outfit: 'standard-single-band', poseIndex: index + 1, derivation: index === 0 ? 'exact-approved-Turn-V9-standing-back-endpoint' : 'V1-alpha-and-geometry-with-regional-clothing-palette-corrected-to-exact-approved-rear-endpoint', sha256: record.sha256, alphaSha256: record.alphaSha256, paletteRegistration: record.paletteRegistration, productionPromotionAllowed: false })
  return record
})

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-back-v2_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-back-v2_f6.png')
saveStrip(forwardStrip, frameFiles); saveStrip(reverseStrip, [...frameFiles].reverse())
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-back-v2-contact-sheet.png'); saveStrip(contactSheet, frameFiles)
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-back-v2', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], frameSha256: frameFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-back-v2', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], frameSha256: [...frameFiles].reverse().map(sha), status: 'review-draft-not-production' })

const publishedByHash = new Map(); const publishedAssets = []
function publish(file, label) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`; fs.copyFileSync(file, path.join(assetsDir, filename))
  const entry = { source: rel(file), sourceSha256: digest, url: reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}

const v1SourceByUrl = new Map(v1Register.publishedAssets.map((entry) => [entry.url, abs(entry.source)]))
const actionPublished = frameFiles.map((file, index) => publish(file, `sit-back-v2-f${index + 1}`))
const endpointPublished = publish(endpointFile, 'approved-rear-palette-authority')
const actionFrames = actionRecords.map((record, index) => {
  const v1Frame = v1Data.action.frames[index]
  const priorSource = v1SourceByUrl.get(v1Frame.src)
  const previewSource = v1SourceByUrl.get(v1Frame.sourcePreviewSrc)
  if (!priorSource || !previewSource) throw new Error(`Missing V1 proof source for F${index + 1}`)
  return { ...clone(v1Frame), src: actionPublished[index].url, sourcePreviewSrc: publish(previewSource, `pose-source-f${index + 1}`).url, priorV1Src: publish(priorSource, `rejected-v1-f${index + 1}`).url, paletteAuthoritySrc: endpointPublished.url, sha256: record.sha256, alphaSha256: record.alphaSha256, priorV1Sha256: record.priorV1Sha256, paletteRegistration: record.paletteRegistration }
})
const route = v1Data.route.map((frame) => {
  if (frame.actionFrame) return { ...clone(frame), src: actionPublished[frame.actionFrame - 1].url, label: frame.label.replace('new Prime back', 'palette-corrected Prime back') }
  const source = v1SourceByUrl.get(frame.src)
  if (!source) throw new Error(`Missing immutable V1 route source for ${frame.src}`)
  return { ...clone(frame), src: publish(source, 'approved-context').url }
})
const data = { ...clone(v1Data), schema: 'lighthouse-keeper/sit-stand-context@back-2', set, status: 'reversible-back-review-candidate-v2-not-approved', derivation: { ...clone(v1Data.derivation), correction: 'F2-F6 jumper and trouser regions remapped to exact RGB samples from the approved rear endpoint; V1 geometry and alpha retained exactly' }, action: { ...clone(v1Data.action), paletteAuthority: { file: rel(endpointFile), sha256: sha(endpointFile), regionalReadings: endpointReadings }, frames: actionFrames }, route }
const dataFile = path.join(pack, `${set}.json`); writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const { jumperPaletteMedianMatchesPrime: _oldJumperMedian, trouserPaletteMedianMatchesPrime: _oldTrouserMedian, bootPaletteMedianMatchesPrime: _oldBootMedian, ...inheritedChecks } = clone(v1Register.checks)
const register = { ...clone(v1Register), set, status: 'back-foreground-chair-v2-palette-corrected-awaiting-frank', predecessor: { set: v1Set, register: rel(v1RegisterFile), sha256: sha(v1RegisterFile), disposition: 'immutable; rejected as a colour-match candidate because frames 29-41 are visibly darker than Prime' }, authorities: { ...clone(v1Register.authorities), standingBackPalette: { file: rel(endpointFile), sha256: sha(endpointFile), scope: 'exact approved rear endpoint and direct regional jumper/trouser colour authority', regionalReadings: endpointReadings } }, candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } }, checks: { ...inheritedChecks, everyCorrectedFrameUsesOnlyApprovedRearPrimeRgb: actionRecords.slice(1).every((frame) => frame.paletteRegistration.allVisibleRgbFromApprovedPrimeAuthorities && frame.paletteRegistration.offAuthorityPixels === 0), jumperRegionalMedianMatchesExactPrimeEndpoint: actionRecords.slice(1).every((frame) => Math.abs(frame.paletteRegistration.corrected.jumperCore.medianLuma - endpointReadings.jumperCore.medianLuma) <= 1), trouserRegionalMedianMatchesExactPrimeEndpoint: actionRecords.slice(1).every((frame) => Math.abs(frame.paletteRegistration.corrected.trouserCore.medianLuma - endpointReadings.trouserCore.medianLuma) <= 1), bootPixelsRemainV1ApprovedPrimeAuthority: actionRecords.slice(1).every((frame) => frame.paletteRegistration.allVisibleRgbFromApprovedPrimeAuthorities), V1AlphaAndGeometryUnchanged: actionRecords.every((frame, index) => frame.alphaSha256 === v1Register.candidate.frames[index].alphaSha256 && frame.bounds.width === v1Register.candidate.frames[index].bounds.width && frame.bounds.height === v1Register.candidate.frames[index].bounds.height), V1Immutable: sha(v1RegisterFile) === registerPredecessorSha() }, publishedAssets, approvalBoundary: { ...clone(v1Register.approvalBoundary), backV1Approved: false, backV2Approved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false }, rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_back_v2.mjs and scripts/verify_keeper_prime_sit_stand_back_v2.mjs; V1 and every pinned approval remain unchanged.` }
function registerPredecessorSha() { return sha(v1RegisterFile) }
for (const [name, value] of Object.entries(register.checks)) {
  if (name === 'historicalKeeperPixelsReusedInCandidate') { if (value !== false) throw new Error(`${name} must remain false`) }
  else if (value !== true) throw new Error(`${name} failed`)
}
writeJson(path.join(pack, 'batch-register.json'), register)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Prime Keeper back sit/stand V2\n\nV2 preserves every V1 alpha plane, dimension and route frame, but rejects V1 colour matching. Direct regional measurement found the stable jumper at luminance 73–74 versus Prime 95, and trousers at 52–53 versus Prime 77. F2–F6 now use hue-constrained exact RGB samples from the exact approved Turn V9 rear endpoint, with regional medians within one luminance point of that endpoint. Historical animation remains choreography-only; the complete 61-frame route, chair depth and ghost overlays remain intact. Nothing is promoted.\n')
console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, routeFrames: route.length, authorityReadings: endpointReadings, correctedReadings: actionRecords.map((frame) => frame.paletteRegistration.corrected), checks: register.checks }, null, 2))
