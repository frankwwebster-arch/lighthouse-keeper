#!/usr/bin/env node
/** Verify V6's three bounded corrections and synchronized scale-review surface. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v6')
const REGISTER = path.join(PACK, 'batch-register.json')
const V4_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v4/batch-register.json')
const V5_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v5/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v6')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v6'
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V6: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V4_REGISTER, V5_APPROVAL, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v4 = JSON.parse(fs.readFileSync(V4_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v6' || register.status !== 'draft-v6-three-point-refinement-awaiting-visual-approval') fail('batch identity/status changed')
if (register.priorApproval?.registerSha256 !== sha256(V5_APPROVAL) || register.priorApproval?.wording !== 'Approved.') fail('V5 approval provenance changed')
if (sha256(path.join(ROOT, register.palette.file)) !== register.palette.sha256 || register.palette.approvalRegisterSha256 !== sha256(V5_APPROVAL)) fail('approved palette provenance changed')

const smooth = register.smoothBackAuthority
const smoothPath = path.join(ROOT, smooth.file)
if (sha256(smoothPath) !== smooth.sha256 || sha256(path.join(ROOT, smooth.register)) !== smooth.registerSha256 || JSON.stringify(smooth.dimensions) !== '[1122,1402]') fail('approved smooth rear authority changed')
if (!smooth.approvalWording.includes('They don\'t look like toe caps')) fail('rear-master approval wording changed')

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || JSON.stringify(frames.map((item) => item.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('frame sequence changed')
const current = frames.map((item) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
const prior = v4.frames.map((item: Record<string, any>) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
for (const index of [1, 2, 3, 4, 5]) {
  if (!fs.readFileSync(path.join(ROOT, frames[index].file)).equals(fs.readFileSync(path.join(ROOT, v4.frames[index].file)))) fail(`frame ${index + 1} is not byte-identical to V4`)
  if (frames[index].change !== 'none-byte-identical' || frames[index].changedPixels !== 0) fail(`frame ${index + 1} change boundary changed`)
}

const palette = JSON.parse(fs.readFileSync(path.join(ROOT, register.palette.file), 'utf8')) as Record<string, any>
const f1 = register.changes.f1Palette
if (f1.alphaUnchanged !== true || frames[0].change !== 'trouser-and-boot-palette-only' || frames[0].changedPixels !== 4492) fail('F1 declared change boundary changed')
let f1Changed = 0
const f1Coverage = new Set<number>()
for (const name of ['trouserNavy', 'bootNavy']) {
  const check = f1.componentChecks[name]
  for (const [key, hashKey] of [['coverageMask', 'coverageMaskSha256'], ['changedMask', 'changedMaskSha256']] as const) {
    const file = path.join(ROOT, check[key])
    if (sha256(file) !== check[hashKey]) fail(`F1 ${name} ${key} changed`)
  }
  const coverage = PNG.sync.read(fs.readFileSync(path.join(ROOT, check.coverageMask)))
  for (let pixel = 0; pixel < 256 * 320; pixel += 1) if (coverage.data[pixel * 4] > 0) f1Coverage.add(pixel)
  const target = palette.components[name].target.medianHSV as number[]
  const measured = check.corrected.medianHSV as number[]
  for (let channel = 0; channel < 3; channel += 1) if (Math.abs(target[channel] - measured[channel]) > [0.02, 0.08, 0.02][channel]) fail(`F1 ${name} palette target missed`)
}
for (let pixel = 0; pixel < 256 * 320; pixel += 1) {
  const offset = pixel * 4
  const changed = !current[0].data.subarray(offset, offset + 4).equals(prior[0].data.subarray(offset, offset + 4))
  if (changed && !f1Coverage.has(pixel)) fail(`F1 changed outside lower-uniform masks at pixel ${pixel}`)
  if (current[0].data[offset + 3] !== prior[0].data[offset + 3]) fail(`F1 alpha changed at pixel ${pixel}`)
  if (changed) f1Changed += 1
}
if (f1Changed !== 4492) fail('F1 measured changed-pixel count changed')

const f7 = register.changes.f7Height
if (frames[6].change !== 'uniform-floor-anchored-height-correction' || frames[6].opaqueHeight !== 296 || JSON.stringify(frames[6].opaqueBoundsExclusive) !== '[58,20,201,316]') fail('F7 bounds changed')
if (f7.sourceHeight !== 298 || f7.candidateHeight !== 296 || f7.floorY !== 316 || f7.registration?.filter !== 'Lanczos' || f7.registration?.creativePixelWarp !== false || f7.registration?.uniformScale !== 0.993288590604) fail('F7 registration changed')

const f8 = register.changes.f8SmoothMaster
if (frames[7].change !== 'full-frame-approved-smooth-master-rebuild' || JSON.stringify(frames[7].opaqueBoundsExclusive) !== '[50,18,205,316]' || frames[7].opaqueHeight !== 298) fail('F8 smooth endpoint bounds changed')
if (f8.filter !== 'Lanczos' || f8.creativePixelWarp !== false || JSON.stringify(f8.registration?.sourcePixels) !== '[1122,1402]' || JSON.stringify(f8.registration?.normalizedBoundsExclusive) !== '[50,18,205,316]') fail('F8 smooth-master registration changed')
for (const name of ['capCrownBlue', 'capBandNavy', 'jumperBlue', 'jumperCream', 'trouserNavy', 'bootNavy']) {
  const check = f8.componentChecks[name]
  for (const [key, hashKey] of [['coverageMask', 'coverageMaskSha256'], ['changedMask', 'changedMaskSha256']] as const) if (sha256(path.join(ROOT, check[key])) !== check[hashKey]) fail(`F8 ${name} ${key} changed`)
  const target = palette.components[name].target.medianHSV as number[]
  const measured = check.corrected.medianHSV as number[]
  for (let channel = 0; channel < 3; channel += 1) if (Math.abs(target[channel] - measured[channel]) > [0.02, 0.08, 0.02][channel]) fail(`F8 ${name} palette target missed`)
}

for (const [index, png] of current.entries()) {
  if (png.width !== 256 || png.height !== 320 || frames[index].sha256 !== sha256(path.join(ROOT, frames[index].file))) fail(`frame ${index + 1} geometry/hash changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[(((319 * 256) + x) * 4) + 3]) fail(`frame ${index + 1} touches horizontal edge`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`frame ${index + 1} touches vertical edge`)
  if (frames[index].changedPixels) {
    const maskPath = path.join(ROOT, frames[index].changedMask)
    if (sha256(maskPath) !== frames[index].changedMaskSha256) fail(`frame ${index + 1} aggregate changed mask changed`)
  }
}

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  if (sha256(path.join(ROOT, record.file)) !== record.sha256 || sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} strip/sidecar changed`)
  const strip = PNG.sync.read(fs.readFileSync(path.join(ROOT, record.file)))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = current[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const start = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip frame ${frame + 1} disagrees with source`)
    }
  }
}

for (const flag of ['frames2To6ByteIdenticalToV4', 'frame1AlphaUnchanged', 'frame7UniformScaleOnly', 'frame7FloorStable', 'frame8UsesApprovedSmoothMaster', 'frame8UniformRegistrationOnly', 'everyFrameTransparentCellEdge']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.v6Approved !== false || register.approvalBoundary?.v5ApprovalRevoked !== false || register.approvalBoundary?.productionPromotionAllowed !== false || register.approvalBoundary?.finalLaneEntryAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V6', 'three-point refinement', 'F1 lower-uniform colour', 'F7 perceived height', 'F8 rendering smoothness', 'id="previous"', 'id="next"', 'id="largePlayer"', 'id="gamePlayer"', 'width:128px;height:160px', 'large.src=frames[index];game.src=frames[index]', 'F2–F6 are exact V5/V4 bytes']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses relative assets')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`) || sha256(path.join(PUBLIC, 'assets', asset)) !== frames[index - 1].sha256) fail(`public frame ${index} changed or misrouted`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review playback script missing')
new Function(script)

console.log('Keeper Prime side ↔ back Turn V6 verified: F1 palette-only; F2–F6 exact; F7 296px/floor-stable; F8 approved smooth master; synchronized 128×160 review; no promotion.')
