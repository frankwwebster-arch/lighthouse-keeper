#!/usr/bin/env node
/** Verify the reversible Keeper Prime Walk V4 rear-arm cadence draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v4')
const V3 = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-13-v3')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v4')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREFIX = '/keeper-review/keeper-prime-walk-v4/assets/'
const FEEDBACK = 'left are still too static - frames 2 and 3 are almost identical as are 5 6 ad 7'
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V4: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-walk-2026-10-14-v4' || register.status !== 'draft-rear-arm-cadence-v4-awaiting-visual-approval' || register.userFeedback !== FEEDBACK) fail('batch identity, status or feedback changed')
const previousRegister = path.join(ROOT, register.previousCandidate?.register)
if (previousRegister !== path.join(V3, 'batch-register.json') || sha256(previousRegister) !== register.previousCandidate.sha256 || register.previousCandidate.filesChanged !== false) fail('Walk V3 provenance changed')

const selected = register.generation?.selectedSources as Record<string, any>[]
if (!Array.isArray(selected) || selected.map(item => item.frame).join(',') !== '2,3,5,6,7') fail('selected source inventory changed')
for (const item of selected) if (sha256(path.join(ROOT, item.file)) !== item.sha256) fail(`selected source changed for frame ${item.frame}`)
const rejected = register.generation?.rejectedSources as Record<string, any>[]
if (!Array.isArray(rejected) || rejected.length !== 3) fail('rejected source inventory changed')
for (const item of rejected) if (sha256(path.join(ROOT, item.file)) !== item.sha256) fail(`rejected source changed: ${item.file}`)

const frames = register.frames as Record<string, any>[]
if (!Array.isArray(frames) || frames.length !== 8 || register.animation?.frames !== 8 || register.animation?.fps !== 8 || register.animation?.loop !== true) fail('animation contract changed')
const pngs = frames.map((frame, index) => {
  const file = path.join(ROOT, frame.file)
  if (sha256(file) !== frame.sha256 || frame.edgeAlphaPixels !== 0 || frame.opaqueBoundsExclusive[3] !== 316) fail(`frame ${index + 1} hash/floor/gutter changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  for (let x = 0; x < png.width; x += 1) if (png.data[x * 4 + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} horizontal edge alpha`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[(y * png.width) * 4 + 3] || png.data[(y * png.width + png.width - 1) * 4 + 3]) fail(`frame ${index + 1} vertical edge alpha`)
  return png
})

for (const frame of [1, 4, 8]) {
  const v3 = path.join(V3, `drafts/frames/keeper_prime_walk-right_f${frame}.png`)
  if (frames[frame - 1].sha256 !== sha256(v3) || frames[frame - 1].provenance?.byteIdenticalToV3 !== true) fail(`frame ${frame} is not byte-identical to Walk V3`)
}
for (const frame of [2, 3, 5, 6, 7]) {
  const provenance = frames[frame - 1].provenance
  if (provenance?.pixelAudit?.changedPixels <= 0 || provenance?.pixelAudit?.changedOutsideDeclaredRegion !== 0) fail(`frame ${frame} escaped its declared rear-arm region`)
  if (provenance?.registration?.creativeWarp !== false || provenance?.registration?.method !== 'uniform Lanczos scale from significant-alpha height, floor alignment, and cap-badge horizontal alignment') fail(`frame ${frame} registration changed`)
}
const stripPath = path.join(ROOT, register.animation.strip.file)
if (sha256(stripPath) !== register.animation.strip.sha256) fail('strip changed')
const strip = PNG.sync.read(fs.readFileSync(stripPath))
if (strip.width !== 2048 || strip.height !== 320) fail('strip geometry changed')
for (let frame = 0; frame < 8; frame += 1) for (let y = 0; y < 320; y += 1) {
  const actual = strip.data.subarray(((y * strip.width) + frame * 256) * 4, ((y * strip.width) + frame * 256) * 4 + 1024)
  const expected = pngs[frame].data.subarray(y * 1024, y * 1024 + 1024)
  if (!actual.equals(expected)) fail(`strip frame ${frame + 1} disagrees with source frame`)
}
const sidecarPath = path.join(ROOT, register.animation.strip.sidecar)
if (sha256(sidecarPath) !== register.animation.strip.sidecarSha256) fail('sidecar changed')
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
if (sidecar.sha256 !== sha256(stripPath) || sidecar.frames !== 8 || sidecar.fps !== 8 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8 || sidecar.status !== 'walk-v4-review-draft-not-production') fail('strip/sidecar agreement changed')

const previousFrames = register.previousWalkV3FrameComparison as Record<string, any>[]
if (!Array.isArray(previousFrames) || previousFrames.length !== 8) fail('Walk V3 comparison inventory changed')
for (const item of previousFrames) {
  if (sha256(path.join(ROOT, item.source)) !== item.sourceSha256 || sha256(path.join(ROOT, item.public)) !== item.publicSha256 || item.sourceSha256 !== item.publicSha256 || item.byteIdentical !== true) fail(`Walk V3 comparison frame ${item.frame} changed`)
}

for (const flag of ['framesOneFourAndEightByteIdenticalToV3', 'changedPixelsConfinedToDeclaredRegions', 'everyOutputCellHasTransparentEdge', 'stripMatchesFrames', 'sidecarMatchesStrip']) if (register.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV4Approved', 'walkStopApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (register.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)

for (const item of [...frames, register.animation.strip, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const htmlPath = path.join(PUBLIC, 'index.html')
if (register.reviewPage?.sha256 !== sha256(htmlPath) || register.reviewPage?.assetPrefix !== PREFIX || register.reviewPage?.relativeAssetUrls !== false) fail('review page record changed')
const html = fs.readFileSync(htmlPath, 'utf8')
for (const forbidden of ['src="assets/', 'const frames=["assets/']) if (html.includes(forbidden)) fail(`relative URL remains: ${forbidden}`)
for (const phrase of ['Keeper Prime Walk V4 · right-facing', 'Rear-arm cadence redraft · awaiting visual approval', 'rearward → passing → compact return → passing → rearward', 'Walk V3 versus Walk V4 · synchronized exact game size', 'exactly 128 × 160 proposed game display size', 'F1, F4 and F8 remain byte-identical', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)

console.log('Keeper Prime Walk V4 verified: five targeted rear-arm corrections, exact V3 F1/F4/F8, declared-region confinement, transparent gutters, exact strip/sidecar/public agreement and no promotion.')
