#!/usr/bin/env node
/** Verify the reversible F8 jumper-colour correction draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v2')
const PRIOR_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v1/batch-register.json')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v2')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v2'
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V2: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, PRIOR_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prior = JSON.parse(fs.readFileSync(PRIOR_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v2' || register.status !== 'draft-side-back-turn-v2-jumper-colour-correction-awaiting-visual-approval') fail('batch identity/status changed')
if (register.priorDraft?.registerSha256 !== sha256(PRIOR_REGISTER)) fail('V1 provenance changed')
if (sha256(path.join(ROOT, register.generatedColourReference.file)) !== register.generatedColourReference.sha256 || !register.generatedColourReference.disposition.includes('rejected as geometry')) fail('generated colour evidence provenance changed')

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || JSON.stringify(frames.map((item) => item.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('frame sequence changed')
const pngs = frames.map((item) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
const priorPngs = prior.frames.map((item: Record<string, any>) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
for (let index = 0; index < 7; index += 1) {
  const currentFile = path.join(ROOT, frames[index].file)
  const priorFile = path.join(ROOT, prior.frames[index].file)
  if (!fs.readFileSync(currentFile).equals(fs.readFileSync(priorFile))) fail(`frame ${index + 1} is not byte-identical to V1`)
  if (frames[index].change !== 'none-byte-identical') fail(`frame ${index + 1} change boundary changed`)
}

const maskPath = path.join(ROOT, register.colourCorrection.mask)
if (!fs.existsSync(maskPath) || sha256(maskPath) !== register.colourCorrection.maskSha256) fail('jumper mask missing or changed')
const mask = PNG.sync.read(fs.readFileSync(maskPath))
const current = pngs[7]
const original = priorPngs[7]
if (current.width !== 256 || current.height !== 320 || mask.width !== 256 || mask.height !== 320) fail('F8/mask geometry changed')
let changed = 0
let maskPixels = 0
for (let pixel = 0; pixel < 256 * 320; pixel += 1) {
  const offset = pixel * 4
  const isChanged = !current.data.subarray(offset, offset + 4).equals(original.data.subarray(offset, offset + 4))
  const inMask = mask.data[offset] > 0
  if (isChanged) changed += 1
  if (inMask) maskPixels += 1
  if (isChanged !== inMask) fail(`F8 changed-pixel mask disagrees at pixel ${pixel}`)
  if (current.data[offset + 3] !== original.data[offset + 3]) fail(`F8 alpha changed at pixel ${pixel}`)
}
if (changed !== register.colourCorrection.changedPixels || maskPixels !== changed || changed < 7000) fail('F8 jumper-only changed-pixel count changed')
if (frames[7].change !== 'jumper-colour-only' || frames[7].opaqueHeight !== 298 || frames[7].opaqueBoundsExclusive.join(',') !== prior.frames[7].opaqueBoundsExclusive.join(',')) fail('F8 geometry/change boundary changed')
for (const [index, png] of pngs.entries()) {
  for (let x = 0; x < png.width; x += 1) if (png.data[(x * 4) + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} touches a horizontal cell edge`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[((y * png.width) * 4) + 3] || png.data[((y * png.width + png.width - 1) * 4) + 3]) fail(`frame ${index + 1} touches a vertical cell edge`)
}

const hsv = (r: number, g: number, b: number): [number, number, number] => {
  const rn = r / 255, gn = g / 255, bn = b / 255
  const max = Math.max(rn, gn, bn), min = Math.min(rn, gn, bn), delta = max - min
  let hue = 0
  if (delta) {
    if (max === rn) hue = ((gn - bn) / delta) % 6
    else if (max === gn) hue = (bn - rn) / delta + 2
    else hue = (rn - gn) / delta + 4
    hue /= 6
    if (hue < 0) hue += 1
  }
  return [hue, max === 0 ? 0 : delta / max, max]
}
const jumperValues = (png: PNG) => {
  const values: number[] = []
  for (let y = 84; y <= 204; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const [r, g, b, a] = png.data.subarray(offset, offset + 4)
    const [hue, saturation, value] = hsv(r, g, b)
    if (a >= 8 && b - r >= 24 && hue >= 0.52 && hue <= 0.70 && saturation >= 0.55 && value >= 0.24) values.push(value)
  }
  return values.sort((a, b) => a - b)
}
const median = (values: number[]) => values[Math.floor(values.length / 2)]
const referenceMedian = median(jumperValues(pngs[6]))
const originalMedian = median(jumperValues(original))
const correctedMedian = median(jumperValues(current))
if (originalMedian > referenceMedian - 0.1) fail('V1 F8 no longer demonstrates the reported dark-jumper discontinuity')
if (Math.abs(correctedMedian - referenceMedian) > 0.01) fail('corrected F8 jumper brightness no longer matches F7')
if (Math.abs(register.colourCorrection.referenceMedianHSV[2] - referenceMedian) > 0.001 || Math.abs(register.colourCorrection.originalMedianHSV[2] - originalMedian) > 0.001 || Math.abs(register.colourCorrection.correctedMedianHSV[2] - correctedMedian) > 0.001) fail('registered colour measurements changed')

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  const stripPath = path.join(ROOT, record.file)
  if (sha256(stripPath) !== record.sha256) fail(`${direction} strip hash changed`)
  const strip = PNG.sync.read(fs.readFileSync(stripPath))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = pngs[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const actualStart = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(actualStart, actualStart + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip frame ${frame + 1} disagrees with its source`)
    }
  }
  if (sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} sidecar changed`)
}
for (const flag of ['frames1To7ByteIdenticalToV1', 'frame8AlphaByteIdenticalToV1', 'frame8GeometryUnchanged', 'frame8OnlyMaskPixelsChanged', 'everyFrameTransparentCellEdge']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'approvedBackMasterChanged', 'priorDraftChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.sideBackTurnV2Approved !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V2', 'F8 jumper-colour correction', 'F1–F7 are exact V1 copies', 'Jumper-only amendment', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses trailing-slash-dependent relative asset URLs')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`)) fail(`review page does not route frame ${index} from its versioned directory`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log(`Keeper Prime side ↔ back Turn V2 verified: F1–F7 exact V1; ${changed} jumper-only F8 pixels; alpha/geometry/gutters exact; corrected median brightness matches F7; no promotion.`)
