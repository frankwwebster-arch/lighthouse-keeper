#!/usr/bin/env node
/** Verify the full standard-outfit palette correction and reusable palette contract. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v3')
const PRIOR_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v2/batch-register.json')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v3')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v3'
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V3: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, PRIOR_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prior = JSON.parse(fs.readFileSync(PRIOR_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v3' || register.status !== 'draft-side-back-turn-v3-full-outfit-palette-awaiting-visual-approval') fail('batch identity/status changed')
if (register.priorDraft?.registerSha256 !== sha256(PRIOR_REGISTER)) fail('V2 provenance changed')
if (sha256(path.join(ROOT, register.generatedPaletteReference.file)) !== register.generatedPaletteReference.sha256 || !register.generatedPaletteReference.disposition.includes('rejected as geometry')) fail('generated palette evidence provenance changed')
const palettePath = path.join(ROOT, register.palette.file)
if (sha256(palettePath) !== register.palette.sha256) fail('palette file changed')
const palette = JSON.parse(fs.readFileSync(palettePath, 'utf8')) as Record<string, any>
if (palette.id !== 'keeper-standard-outfit-palette-2026-10-13-v1-draft' || palette.status !== 'draft-awaiting-visual-approval') fail('palette identity/status changed')
if (palette.futureBatchContract?.componentMasksRequired !== true || palette.futureBatchContract?.noUnmaskedColourChanges !== true || palette.futureBatchContract?.transparentCellGutterRequired !== true) fail('future standard-outfit batch contract changed')
if (JSON.stringify(palette.futureBatchContract?.medianHsvTolerance) !== '[0.02,0.08,0.02]') fail('palette tolerances changed')

const componentNames = ['capCrownBlue', 'capBandNavy', 'jumperBlue', 'jumperCream', 'trouserNavy', 'bootNavy']
if (JSON.stringify(Object.keys(palette.components)) !== JSON.stringify(componentNames)) fail('palette components changed')
for (const name of componentNames) {
  const component = palette.components[name]
  for (const key of ['coverageMask', 'changedMask']) if (!fs.existsSync(path.join(ROOT, component[key])) || sha256(path.join(ROOT, component[key])) !== component[`${key}Sha256`]) fail(`${name} ${key} missing or changed`)
  if (component.target.pixels < 500 || component.source.pixels < 500) fail(`${name} sample is unexpectedly small`)
}

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || JSON.stringify(frames.map((item) => item.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('frame sequence changed')
const pngs = frames.map((item) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
const priorPngs = prior.frames.map((item: Record<string, any>) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
for (let index = 0; index < 7; index += 1) {
  if (!fs.readFileSync(path.join(ROOT, frames[index].file)).equals(fs.readFileSync(path.join(ROOT, prior.frames[index].file)))) fail(`frame ${index + 1} is not byte-identical to V2`)
  if (frames[index].change !== 'none-byte-identical') fail(`frame ${index + 1} change boundary changed`)
}
const current = pngs[7], original = priorPngs[7]
const changedUnion = PNG.sync.read(fs.readFileSync(path.join(ROOT, palette.changedUnion.file)))
const coverageUnion = PNG.sync.read(fs.readFileSync(path.join(ROOT, palette.coverageUnion.file)))
if (sha256(path.join(ROOT, palette.changedUnion.file)) !== palette.changedUnion.sha256 || sha256(path.join(ROOT, palette.coverageUnion.file)) !== palette.coverageUnion.sha256) fail('palette union masks changed')
let changedPixels = 0
for (let pixel = 0; pixel < 256 * 320; pixel += 1) {
  const offset = pixel * 4
  const changed = !current.data.subarray(offset, offset + 4).equals(original.data.subarray(offset, offset + 4))
  const declaredChanged = changedUnion.data[offset] > 0
  const inCoverage = coverageUnion.data[offset] > 0
  if (changed !== declaredChanged) fail(`changed-pixel union disagrees at pixel ${pixel}`)
  if (changed && !inCoverage) fail(`outfit colour changed outside component coverage at pixel ${pixel}`)
  if (current.data[offset + 3] !== original.data[offset + 3]) fail(`F8 alpha changed at pixel ${pixel}`)
  if (changed) changedPixels += 1
}
if (changedPixels < 10000 || frames[7].change !== 'standard-outfit-palette-only' || frames[7].opaqueBoundsExclusive.join(',') !== prior.frames[7].opaqueBoundsExclusive.join(',')) fail('F8 full-outfit change/geometry boundary changed')

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
const median = (values: number[]) => values.sort((a, b) => a - b)[Math.floor(values.length / 2)]
for (const name of componentNames) {
  const component = palette.components[name]
  const coverage = PNG.sync.read(fs.readFileSync(path.join(ROOT, component.coverageMask)))
  const channels: number[][] = [[], [], []]
  for (let pixel = 0; pixel < 256 * 320; pixel += 1) if (coverage.data[pixel * 4] > 0) {
    const offset = pixel * 4
    const values = hsv(current.data[offset], current.data[offset + 1], current.data[offset + 2])
    for (let channel = 0; channel < 3; channel += 1) channels[channel].push(values[channel])
  }
  const measured = channels.map(median)
  const expected = component.target.medianHSV as number[]
  const tolerances = palette.futureBatchContract.medianHsvTolerance as number[]
  for (let channel = 0; channel < 3; channel += 1) if (Math.abs(measured[channel] - expected[channel]) > tolerances[channel]) fail(`${name} median HSV no longer matches palette target`)
  const registered = component.corrected.medianHSV as number[]
  for (let channel = 0; channel < 3; channel += 1) if (Math.abs(measured[channel] - registered[channel]) > 0.001) fail(`${name} registered corrected measurement changed`)
}
if (palette.components.jumperBlue.changedPixels !== 0 || !palette.components.jumperBlue.disposition.includes('retained exact V2 pixels')) fail('already-correct V2 jumper was not retained')

for (const [index, png] of pngs.entries()) {
  for (let x = 0; x < png.width; x += 1) if (png.data[x * 4 + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} touches a horizontal cell edge`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[(y * png.width) * 4 + 3] || png.data[(y * png.width + png.width - 1) * 4 + 3]) fail(`frame ${index + 1} touches a vertical cell edge`)
}
for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  if (sha256(path.join(ROOT, record.file)) !== record.sha256 || sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} strip/sidecar hash changed`)
  const strip = PNG.sync.read(fs.readFileSync(path.join(ROOT, record.file)))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = pngs[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const start = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip frame ${frame + 1} disagrees with source`)
    }
  }
}
for (const flag of ['frames1To7ByteIdenticalToV2', 'frame8AlphaByteIdenticalToV2', 'frame8GeometryUnchanged', 'frame8OnlyRegisteredOutfitPixelsChanged', 'everyFrameTransparentCellEdge']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'approvedBackMasterChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.sideBackTurnV3Approved !== false || register.approvalBoundary?.standardOutfitPaletteApproved !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V3', 'full standard-outfit palette', 'F1–F7 are exact prior bytes', 'cap, jumper, cream band, trousers and boots', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses trailing-slash-dependent relative asset URLs')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`)) fail(`review page does not route frame ${index} correctly`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log(`Keeper Prime side ↔ back Turn V3 verified: ${changedPixels} registered outfit-colour pixels; six component palette anchors match F7; exact alpha/geometry/gutters; no promotion.`)
